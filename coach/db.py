"""Single source of truth for all database operations.

Multi-user support: every table that stores per-player data now carries a
`user_id` column (TEXT, default 'haim' for backward compatibility with the
original single-user data). Call `set_current_user(...)` once per Streamlit
session (done by the login layer) and all functions below will default to
that user when `user_id` is not explicitly supplied — so existing call sites
keep working untouched.
"""
import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB = Path(__file__).parent.parent / "coach.db"

DEFAULT_USER = "haim"

# ── Cloud DB support ──────────────────────────────────────────────────────────
# If DATABASE_URL is set (Postgres / Supabase), use it so the app works from
# any device, not just this machine. Otherwise fall back to local SQLite —
# keeps everything working untouched for local/offline use.
DATABASE_URL = os.environ.get("DATABASE_URL")
_USE_PG = bool(DATABASE_URL)

if _USE_PG:
    import psycopg2
    import psycopg2.extras


def _pg_translate(sql: str) -> str:
    """Best-effort translation of the SQLite SQL used in this module to Postgres."""
    s = sql
    s = s.replace("?", "%s")
    s = re.sub(r"INTEGER PRIMARY KEY( AUTOINCREMENT)?", "SERIAL PRIMARY KEY", s, flags=re.I)
    s = re.sub(r"INSERT OR IGNORE", "INSERT", s, flags=re.I)
    s = re.sub(r"INSERT OR REPLACE INTO (\w+) \(([^)]+)\)", r"INSERT INTO \1 (\2)", s, flags=re.I)
    s = re.sub(r"datetime\('now'\)", "now()", s, flags=re.I)
    # INSERT OR IGNORE -> add ON CONFLICT DO NOTHING when no explicit ON CONFLICT present
    if re.search(r"^\s*INSERT\b", s, flags=re.I) and "ON CONFLICT" not in s.upper() \
            and re.search(r"INSERT OR IGNORE", sql, flags=re.I):
        s = s.rstrip().rstrip(";") + " ON CONFLICT DO NOTHING"
    return s


class _Row:
    """Dict-like row that also supports integer indexing — mirrors sqlite3.Row,
    since some call sites in this module do both dict(row) and row[0]/row[5]."""
    __slots__ = ("_d",)

    def __init__(self, d: dict):
        self._d = d

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._d.values())[key]
        return self._d[key]

    def keys(self):
        return self._d.keys()

    def __iter__(self):
        return iter(self._d.values())

    def get(self, key, default=None):
        return self._d.get(key, default)


class _PgCursorWrapper:
    """Wraps a psycopg2 RealDictCursor so call sites written for sqlite3.Row
    (dict(row), row['col'], row[0]) keep working unchanged."""
    def __init__(self, cur):
        self._cur = cur

    def execute(self, sql, params=()):
        self._cur.execute(_pg_translate(sql), tuple(params) if params else None)
        return self

    def fetchall(self):
        return [_Row(dict(r)) for r in self._cur.fetchall()]

    def fetchone(self):
        r = self._cur.fetchone()
        return _Row(dict(r)) if r is not None else None


class _PgConnWrapper:
    """Wraps a psycopg2 connection to behave like the sqlite3 connection used
    here: context-manager commits on exit, .execute() proxies to a cursor."""
    def __init__(self, conn):
        # Autocommit so each statement is its own transaction — mirrors the
        # sqlite3 usage here where individual failures (caught by try/except
        # in migration code) must not poison subsequent statements.
        conn.autocommit = True
        self._conn = conn
        self._cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def execute(self, sql, params=()):
        return _PgCursorWrapper(self._cur).execute(sql, params)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._cur.close()
        self._conn.close()
        return False

    def close(self):
        self._cur.close()
        self._conn.close()

# Process/session-wide "current user" — set by the login layer via
# set_current_user(). Defaults to 'haim' so existing single-user behaviour
# (and Haim's 19+ existing sessions) keeps working untouched.
_current_user = DEFAULT_USER


def set_current_user(user_id: str) -> None:
    """Set the active user for subsequent db calls that omit user_id."""
    global _current_user
    _current_user = (user_id or DEFAULT_USER).strip().lower() or DEFAULT_USER


def get_current_user() -> str:
    return _current_user


def _uid(user_id: str | None) -> str:
    return (user_id or _current_user or DEFAULT_USER)


def _conn():
    if _USE_PG:
        return _PgConnWrapper(psycopg2.connect(DATABASE_URL))
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def _ensure_user_id_column(c, table: str) -> None:
    """Add a user_id TEXT column defaulting to 'haim' if missing (safe migration)."""
    try:
        if _USE_PG:
            cols = [r["column_name"] for r in c.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name=%s",
                (table,)).fetchall()]
        else:
            cols = [r[1] for r in c.execute(f"PRAGMA table_info({table})").fetchall()]
        if "user_id" not in cols:
            c.execute(
                f"ALTER TABLE {table} ADD COLUMN user_id TEXT NOT NULL DEFAULT '{DEFAULT_USER}'"
            )
    except Exception:
        pass


def init() -> None:
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                match_id   TEXT PRIMARY KEY,
                date       TEXT NOT NULL,
                shots      INTEGER DEFAULT 0,
                rallies    INTEGER DEFAULT 0,
                stats_json TEXT,
                video_url  TEXT,
                note_json  TEXT,
                user_id    TEXT NOT NULL DEFAULT 'haim',
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        _ensure_user_id_column(c, "sessions")

        # migrate old table if it exists
        try:
            rows = c.execute(
                "SELECT file_path, session_date, total_shots, total_rallies, "
                "stats_json, video_url FROM swingvision_sessions"
            ).fetchall()
            for r in rows:
                mid = r[0].replace("api://", "") if r[0] else r[0]
                if mid and not mid.startswith("G:"):
                    c.execute(
                        "INSERT OR IGNORE INTO sessions "
                        "(match_id, date, shots, rallies, stats_json, video_url, user_id) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (mid, r[1] or "", r[2] or 0, r[3] or 0, r[4], r[5], DEFAULT_USER)
                    )
            # migrate notes from player_config.json
            cfg = Path(__file__).parent.parent / "player_config.json"
            if cfg.exists():
                data = json.loads(cfg.read_text(encoding="utf-8"))
                for mid, note in data.get("video_notes", {}).items():
                    c.execute(
                        "UPDATE sessions SET note_json=? WHERE match_id=?",
                        (json.dumps(note, ensure_ascii=False), mid)
                    )
        except Exception:
            pass

        # Make sure dependent tables exist + carry user_id (created lazily
        # elsewhere too, but creating here lets us migrate them up front).
        # Global cache of parsed SwingVision matches, shared across all users —
        # avoids re-fetching the same public match from the SwingVision API
        # when more than one player imports the same link.
        c.execute("""CREATE TABLE IF NOT EXISTS match_cache
                     (match_id TEXT PRIMARY KEY, date TEXT, shots INTEGER,
                      rallies INTEGER, stats_json TEXT, video_url TEXT,
                      cached_at TEXT DEFAULT (datetime('now')))""")

        c.execute("""CREATE TABLE IF NOT EXISTS analyses
                     (key TEXT PRIMARY KEY, text TEXT, created_at TEXT,
                      user_id TEXT NOT NULL DEFAULT 'haim')""")
        _ensure_user_id_column(c, "analyses")

        c.execute("""CREATE TABLE IF NOT EXISTS chat
                     (id INTEGER PRIMARY KEY, messages TEXT, updated_at TEXT,
                      user_id TEXT NOT NULL DEFAULT 'haim')""")
        _ensure_user_id_column(c, "chat")

        c.execute("""CREATE TABLE IF NOT EXISTS history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      category TEXT, title TEXT, content TEXT,
                      messages_json TEXT,
                      user_id TEXT NOT NULL DEFAULT 'haim',
                      created_at TEXT DEFAULT (datetime('now')))""")
        _ensure_user_id_column(c, "history")
        try:
            c.execute("ALTER TABLE history ADD COLUMN messages_json TEXT")
        except Exception:
            pass


def save_session(match_id: str, date: str, shots: int, rallies: int,
                 stats: dict, video_url: str | None = None,
                 user_id: str | None = None) -> None:
    uid = _uid(user_id)
    with _conn() as c:
        c.execute(
            "INSERT INTO sessions (match_id, date, shots, rallies, stats_json, video_url, user_id) "
            "VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(match_id) DO UPDATE SET "
            "shots=excluded.shots, rallies=excluded.rallies, "
            "stats_json=excluded.stats_json, "
            "video_url=COALESCE(excluded.video_url, sessions.video_url)",
            (match_id, date, shots, rallies,
             json.dumps(stats, ensure_ascii=False), video_url, uid)
        )


def get_cached_match(match_id: str) -> dict | None:
    """Look up a previously-fetched SwingVision match, regardless of which
    user imported it first — lets us skip calling their API again."""
    with _conn() as c:
        r = c.execute(
            "SELECT * FROM match_cache WHERE match_id=?", (match_id,)
        ).fetchone()
    if not r:
        return None
    d = dict(r)
    d["stats"] = json.loads(d.pop("stats_json") or "{}")
    return d


def save_cached_match(match_id: str, date: str, shots: int, rallies: int,
                       stats: dict, video_url: str | None = None) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO match_cache (match_id, date, shots, rallies, stats_json, video_url) "
            "VALUES (?,?,?,?,?,?) "
            "ON CONFLICT(match_id) DO UPDATE SET "
            "shots=excluded.shots, rallies=excluded.rallies, "
            "stats_json=excluded.stats_json, "
            "video_url=COALESCE(excluded.video_url, match_cache.video_url)",
            (match_id, date, shots, rallies, json.dumps(stats, ensure_ascii=False), video_url)
        )


def get_sessions(limit: int = 50, user_id: str | None = None) -> list[dict]:
    uid = _uid(user_id)
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM sessions WHERE user_id=? ORDER BY date DESC, created_at DESC LIMIT ?",
            (uid, limit)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["stats"] = json.loads(d.pop("stats_json") or "{}")
        d["note"]  = json.loads(d.pop("note_json") or "{}")
        result.append(d)
    return result


def get_session(match_id: str, user_id: str | None = None) -> dict | None:
    uid = _uid(user_id)
    with _conn() as c:
        r = c.execute(
            "SELECT * FROM sessions WHERE match_id=? AND user_id=?", (match_id, uid)
        ).fetchone()
    if not r:
        return None
    d = dict(r)
    d["stats"] = json.loads(d.pop("stats_json") or "{}")
    d["note"]  = json.loads(d.pop("note_json") or "{}")
    return d


def save_note(match_id: str, note: dict, user_id: str | None = None) -> None:
    uid = _uid(user_id)
    with _conn() as c:
        c.execute(
            "UPDATE sessions SET note_json=? WHERE match_id=? AND user_id=?",
            (json.dumps(note, ensure_ascii=False), match_id, uid)
        )


def update_video_url(match_id: str, url: str, user_id: str | None = None) -> None:
    uid = _uid(user_id)
    with _conn() as c:
        c.execute(
            "UPDATE sessions SET video_url=? WHERE match_id=? AND user_id=?",
            (url, match_id, uid)
        )


def save_analysis(key: str, text: str, user_id: str | None = None) -> None:
    """Cache AI analysis by key (e.g. 'compare', 'session_sw2-xxx'), per user."""
    uid = _uid(user_id)
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS analyses
            (key TEXT PRIMARY KEY, text TEXT, created_at TEXT,
             user_id TEXT NOT NULL DEFAULT 'haim')
        """)
        _ensure_user_id_column(c, "analyses")
        # key is globally unique in the old schema; namespace it per-user so
        # different users don't collide / overwrite each other's cache.
        ukey = key if uid == DEFAULT_USER else f"{uid}::{key}"
        c.execute(
            "INSERT OR REPLACE INTO analyses (key, text, created_at, user_id) "
            "VALUES (?,?,datetime('now'),?)",
            (ukey, text, uid)
        )


def get_analysis(key: str, user_id: str | None = None) -> str | None:
    uid = _uid(user_id)
    ukey = key if uid == DEFAULT_USER else f"{uid}::{key}"
    with _conn() as c:
        try:
            r = c.execute("SELECT text FROM analyses WHERE key=?", (ukey,)).fetchone()
            if r is None and uid == DEFAULT_USER:
                # fall back to legacy un-namespaced key
                r = c.execute("SELECT text FROM analyses WHERE key=?", (key,)).fetchone()
            return r[0] if r else None
        except Exception:
            return None


def save_chat(messages: list[dict], user_id: str | None = None) -> None:
    """Persist full chat history, per user."""
    import json as _json
    uid = _uid(user_id)
    try:
        conn = sqlite3.connect(DB)
        conn.execute("""CREATE TABLE IF NOT EXISTS chat
                        (id INTEGER PRIMARY KEY, messages TEXT, updated_at TEXT,
                         user_id TEXT NOT NULL DEFAULT 'haim')""")
        _ensure_user_id_column(conn, "chat")
        conn.execute("DELETE FROM chat WHERE user_id=?", (uid,))
        conn.execute(
            "INSERT INTO chat (messages, updated_at, user_id) VALUES (?, datetime('now'), ?)",
            (_json.dumps(messages, ensure_ascii=False), uid)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"save_chat error: {e}")


def load_chat(user_id: str | None = None) -> list[dict]:
    """Load persisted chat history for the given (or current) user."""
    import json as _json
    uid = _uid(user_id)
    try:
        conn = sqlite3.connect(DB)
        conn.execute("""CREATE TABLE IF NOT EXISTS chat
                        (id INTEGER PRIMARY KEY, messages TEXT, updated_at TEXT,
                         user_id TEXT NOT NULL DEFAULT 'haim')""")
        _ensure_user_id_column(conn, "chat")
        r = conn.execute("SELECT messages FROM chat WHERE user_id=? LIMIT 1", (uid,)).fetchone()
        if r is None and uid == DEFAULT_USER:
            # legacy rows created before the user_id column existed
            r = conn.execute("SELECT messages FROM chat LIMIT 1").fetchone()
        conn.close()
        return _json.loads(r[0]) if r else []
    except Exception:
        return []


def save_history(category: str, title: str, content: str,
                 messages_json: str | None = None,
                 user_id: str | None = None) -> None:
    """Save to history — one entry per (user, category, title), overwrites if exists."""
    import json as _json
    uid = _uid(user_id)
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      category TEXT, title TEXT, content TEXT,
                      messages_json TEXT,
                      user_id TEXT NOT NULL DEFAULT 'haim',
                      created_at TEXT DEFAULT (datetime('now')))""")
        # add columns if missing (migration)
        try:
            c.execute("ALTER TABLE history ADD COLUMN messages_json TEXT")
        except Exception:
            pass
        _ensure_user_id_column(c, "history")
        existing = c.execute(
            "SELECT id FROM history WHERE category=? AND title=? AND user_id=?",
            (category, title, uid)
        ).fetchone()
        if existing:
            c.execute(
                "UPDATE history SET content=?, messages_json=?, created_at=datetime('now') WHERE id=?",
                (content, messages_json, existing[0])
            )
        else:
            c.execute(
                "INSERT INTO history (category, title, content, messages_json, user_id) VALUES (?,?,?,?,?)",
                (category, title, content, messages_json, uid)
            )


def get_history(category: str | None = None, limit: int = 30,
                user_id: str | None = None) -> list[dict]:
    uid = _uid(user_id)
    with _conn() as c:
        try:
            if category:
                rows = c.execute(
                    "SELECT id, category, title, content, messages_json, created_at FROM history "
                    "WHERE category=? AND user_id=? ORDER BY created_at DESC LIMIT ?",
                    (category, uid, limit)).fetchall()
            else:
                rows = c.execute(
                    "SELECT id, category, title, content, messages_json, created_at FROM history "
                    "WHERE user_id=? ORDER BY created_at DESC LIMIT ?", (uid, limit)).fetchall()
            return [{"id": r[0], "category": r[1], "title": r[2],
                     "content": r[3], "messages_json": r[4], "date": r[5][:16]} for r in rows]
        except Exception:
            return []


def delete_history(row_id: int, user_id: str | None = None) -> None:
    uid = _uid(user_id)
    with _conn() as c:
        try:
            c.execute("DELETE FROM history WHERE id=? AND user_id=?", (row_id, uid))
        except Exception:
            pass


def session_exists(match_id: str, user_id: str | None = None) -> bool:
    uid = _uid(user_id)
    with _conn() as c:
        return bool(c.execute(
            "SELECT 1 FROM sessions WHERE match_id=? AND user_id=?", (match_id, uid)
        ).fetchone())
