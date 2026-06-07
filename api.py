"""REST API layer — exposes coach/* to a future mobile app (FastAPI).
Run: uvicorn api:app --reload --port 8000

Design rules baked in from the start:
- sport: "tennis" | "padel" passed per-request (stored on user/session)
- lang: "he" | "en" | "es" via Accept-Language or ?lang= (i18n-ready)
- stateless: every call takes user_id explicitly (no global session state)
"""
from __future__ import annotations
import tempfile, os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coach import db, config, claude_client, swingvision, swingvision_parser as svp

app = FastAPI(title="Virtual Coach API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

db.init()

SUPPORTED_LANGS = ("he", "en", "es")
SUPPORTED_SPORTS = ("tennis", "padel")


def _lang(accept_language: Optional[str], lang: Optional[str]) -> str:
    if lang in SUPPORTED_LANGS:
        return lang
    if accept_language:
        code = accept_language.split(",")[0].split("-")[0].lower()
        if code in SUPPORTED_LANGS:
            return code
    return "he"


# ── Auth (beta: username only) ────────────────────────────────────────────────
class LoginIn(BaseModel):
    username: str


@app.post("/auth/login")
def login(body: LoginIn):
    uid = body.username.strip().lower()
    if not uid:
        raise HTTPException(400, "username required")
    config.ensure_user(uid, default_username=body.username.strip())
    return {"user_id": uid, "username": config.get_username(uid)}


# ── Profile ───────────────────────────────────────────────────────────────────
@app.get("/users/{uid}/profile")
def get_profile(uid: str):
    return {
        "user_id": uid,
        "username": config.get_username(uid),
        "ntrp": config.get_ntrp(uid),
        "ntrp_next": config.get_ntrp_next(uid),
        "sport": config.get_sport(uid),
    }


class ProfileIn(BaseModel):
    username: Optional[str] = None
    sport: Optional[str] = None  # "tennis" | "padel"


@app.patch("/users/{uid}/profile")
def update_profile(uid: str, body: ProfileIn):
    if body.username:
        config.save_username(body.username.strip(), uid)
    if body.sport:
        config.save_sport(body.sport.strip().lower(), uid)
    return {"ok": True}


# ── Sessions ──────────────────────────────────────────────────────────────────
@app.get("/users/{uid}/sessions")
def list_sessions(uid: str, limit: int = 50):
    return db.get_sessions(limit=limit, user_id=uid)


@app.get("/users/{uid}/sessions/{match_id}")
def get_session(uid: str, match_id: str):
    s = db.get_session(match_id, user_id=uid)
    if not s:
        raise HTTPException(404, "session not found")
    return s


class NoteIn(BaseModel):
    opponent: str = ""
    type: str = ""
    opp_level: str = ""
    score: str = ""
    format: str = ""
    free: str = ""


@app.put("/users/{uid}/sessions/{match_id}/note")
def save_note(uid: str, match_id: str, body: NoteIn):
    db.save_note(match_id, body.dict(), user_id=uid)
    return {"ok": True}


# ── Import (file-based — the legal, scalable path) ───────────────────────────
@app.post("/users/{uid}/import")
async def import_file(uid: str, file: UploadFile = File(...)):
    suffix = Path(file.filename or "upload.xlsx").suffix or ".xlsx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        rows = svp.parse_file(tmp_path)
        if not rows:
            return {"imported": 0, "skipped": 0, "message": "no rows found"}
        if not svp.looks_like_session_summary(rows):
            raise HTTPException(422, "unrecognized file format — expected a session-summary export")

        sessions = svp.sessions_from_summary_rows(rows)
        new_count, dup_count = 0, 0
        for s in sessions:
            if db.session_exists(s["match_id"], user_id=uid):
                dup_count += 1
                continue
            stats = {k: v for k, v in s.items()
                     if k not in ("match_id", "date", "shots", "rallies", "video_url", "note")}
            db.save_session(s["match_id"], s["date"], s["shots"], s["rallies"],
                            stats, s.get("video_url"), user_id=uid)
            if any(s.get("note", {}).values()):
                db.save_note(s["match_id"], s["note"], user_id=uid)
            new_count += 1
        return {"imported": new_count, "skipped": dup_count}
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


class LinkIn(BaseModel):
    url: str


@app.post("/users/{uid}/import_link")
def import_link(uid: str, body: LinkIn):
    link = (body.url or "").strip()
    mid = swingvision.extract_match_id(link)
    if not mid:
        raise HTTPException(422, "invalid SwingVision link")
    if db.session_exists(mid, user_id=uid):
        return {"imported": 0, "skipped": 1, "match_id": mid}
    try:
        s = swingvision.parse_session(mid)
        db.save_session(s["match_id"], s["date"], s["shots"], s["rallies"],
                        s, s.get("video_url"), user_id=uid)
        return {"imported": 1, "skipped": 0, "match_id": s["match_id"], "shots": s["shots"]}
    except Exception as e:
        raise HTTPException(422, f"import failed: {e}")


# ── Chat (streaming would need SSE/WebSocket — kept simple/blocking for v0) ──
class ChatIn(BaseModel):
    messages: list[dict]


@app.post("/users/{uid}/chat")
def chat(uid: str, body: ChatIn,
         accept_language: Optional[str] = Header(None), lang: Optional[str] = None):
    ntrp_cur = config.get_ntrp(uid) or "3.5"
    ntrp_next = config.get_ntrp_next(uid)
    player_summary = f"NTRP {ntrp_cur} -> {ntrp_next or '?'}"
    reply = "".join(claude_client.chat(body.messages, player_summary, ntrp_cur, ntrp_next))
    db.save_chat(body.messages + [{"role": "assistant", "content": reply}], user_id=uid)
    return {"reply": reply}


# ── Saved chat conversations (leave + keep aside, like chat history) ─────────
import json as _json


@app.get("/users/{uid}/conversations")
def list_conversations(uid: str):
    rows = db.get_history(category="chat", limit=50, user_id=uid)
    return [{"id": r["id"], "title": r["title"], "date": r["date"]} for r in rows]


class ConversationIn(BaseModel):
    title: Optional[str] = None
    messages: list[dict]


@app.post("/users/{uid}/conversations")
def save_conversation(uid: str, body: ConversationIn):
    if not body.messages:
        raise HTTPException(400, "no messages")
    title = (body.title or "").strip() or datetime.now().strftime("%Y-%m-%d %H:%M")
    db.save_history("chat", title, "", _json.dumps(body.messages, ensure_ascii=False), user_id=uid)
    rows = db.get_history(category="chat", limit=50, user_id=uid)
    row = next((r for r in rows if r["title"] == title), None)
    return {"ok": True, "title": title, "id": row["id"] if row else None}


@app.put("/users/{uid}/conversations/{conv_id}")
def update_conversation(uid: str, conv_id: int, body: ConversationIn):
    rows = db.get_history(category="chat", limit=200, user_id=uid)
    row = next((r for r in rows if r["id"] == conv_id), None)
    if not row:
        raise HTTPException(404, "not found")
    db.save_history("chat", row["title"], "", _json.dumps(body.messages, ensure_ascii=False), user_id=uid)
    return {"ok": True, "id": conv_id}


@app.get("/users/{uid}/conversations/{conv_id}")
def get_conversation(uid: str, conv_id: int):
    rows = db.get_history(category="chat", limit=200, user_id=uid)
    for r in rows:
        if r["id"] == conv_id:
            return {"id": r["id"], "title": r["title"], "messages": _json.loads(r["messages_json"] or "[]")}
    raise HTTPException(404, "not found")


@app.delete("/users/{uid}/conversations/{conv_id}")
def delete_conversation(uid: str, conv_id: int):
    db.delete_history(conv_id, user_id=uid)
    return {"ok": True}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
