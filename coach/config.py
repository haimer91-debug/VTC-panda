"""Player config — NTRP level, username, pro reference.

Multi-user structure (new):
    {
      "users": {
          "haim":  { "username": "...", "ntrp_level": "...", ... },
          "guest1": { ... }
      },
      "video_notes": { ... }   # kept global/shared (legacy, per match_id)
    }

Backward compatibility: older single-user files store these fields at the
top level (no "users" key). On first load we migrate them into
users["haim"] automatically and persist the new structure — nothing is
deleted, the old flat keys stay untouched as a safety net.

All getters/setters take an optional `user_id` (defaults to the "current
user" set via set_current_user(), which itself defaults to 'haim').
"""
import json
import re
from pathlib import Path

_CFG = Path(__file__).parent.parent / "player_config.json"

DEFAULT_USER = "haim"

_USER_FIELDS = (
    "username", "ntrp_level", "ntrp_text", "ntrp_date",
    "level_assessment_text", "level_assessment_date",
    "pro_player", "pro_rationale",
)

_current_user = DEFAULT_USER


def set_current_user(user_id: str) -> None:
    global _current_user
    _current_user = (user_id or DEFAULT_USER).strip().lower() or DEFAULT_USER


def get_current_user() -> str:
    return _current_user


def _uid(user_id: str | None) -> str:
    return (user_id or _current_user or DEFAULT_USER)


def _raw_load() -> dict:
    return json.loads(_CFG.read_text(encoding="utf-8")) if _CFG.exists() else {}


def _raw_save(data: dict) -> None:
    _CFG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _load() -> dict:
    """Load full config, migrating legacy flat (single-user) structure to
    the new users-keyed structure on the fly. Persists the migration once."""
    data = _raw_load()
    if "users" not in data:
        legacy = {k: data[k] for k in _USER_FIELDS if k in data}
        migrated = {"users": {DEFAULT_USER: legacy}} if legacy else {"users": {}}
        # preserve any other top-level keys (e.g. video_notes)
        for k, v in data.items():
            if k not in _USER_FIELDS:
                migrated[k] = v
        data = migrated
        try:
            _raw_save(data)
        except Exception:
            pass
    data.setdefault("users", {})
    return data


def _user_data(user_id: str | None = None) -> dict:
    return _load().get("users", {}).get(_uid(user_id), {})


def _save_user(fields: dict, user_id: str | None = None) -> None:
    uid = _uid(user_id)
    data = _load()
    data.setdefault("users", {})
    data["users"].setdefault(uid, {})
    data["users"][uid].update(fields)
    _raw_save(data)


def list_users() -> list[str]:
    return sorted(_load().get("users", {}).keys()) or [DEFAULT_USER]


def ensure_user(user_id: str, default_username: str | None = None) -> None:
    """Create an empty profile for a new user if one doesn't exist yet."""
    uid = (user_id or DEFAULT_USER).strip().lower()
    data = _load()
    data.setdefault("users", {})
    if uid not in data["users"]:
        data["users"][uid] = {"username": default_username or uid}
        _raw_save(data)


# ── Getters / setters (all per-user, default = current user) ────────────────

def get_username(user_id: str | None = None) -> str:
    return _user_data(user_id).get("username", "Player")


def save_username(name: str, user_id: str | None = None) -> None:
    _save_user({"username": name}, user_id)


def get_ntrp(user_id: str | None = None) -> str:
    return _user_data(user_id).get("ntrp_level", "")


def get_ntrp_next(user_id: str | None = None) -> str:
    cur = get_ntrp(user_id)
    try:
        nums = re.findall(r"\d+\.\d+", cur)
        return f"{float(nums[-1]) + 0.5:.1f}" if nums else "4.0"
    except Exception:
        return "4.0"


def save_ntrp(level: str, assessment_text: str, user_id: str | None = None) -> None:
    from datetime import datetime
    _save_user({
        "ntrp_level": level,
        "ntrp_text": assessment_text,
        "ntrp_date": datetime.now().strftime("%Y-%m-%d"),
    }, user_id)


def get_ntrp_assessment(user_id: str | None = None) -> dict:
    d = _user_data(user_id)
    return {"ntrp": d.get("ntrp_level", ""), "text": d.get("ntrp_text", ""), "date": d.get("ntrp_date", "")}


def get_pro(user_id: str | None = None) -> str:
    return _user_data(user_id).get("pro_player", "")


def save_pro(name: str, user_id: str | None = None) -> None:
    _save_user({"pro_player": name}, user_id)
