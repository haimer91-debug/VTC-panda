"""REST API layer — exposes coach/* to a future mobile app (FastAPI).
Run: uvicorn api:app --reload --port 8000

Design rules baked in from the start:
- sport: "tennis" | "padel" passed per-request (stored on user/session)
- lang: "he" | "en" | "es" via Accept-Language or ?lang= (i18n-ready)
- stateless: every call takes user_id explicitly (no global session state)
"""
from __future__ import annotations
import tempfile, os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coach import db, config, claude_client, swingvision_parser as svp

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
        "sport": config.get_pro(uid) and "tennis" or "tennis",  # placeholder until sport pref added
    }


class ProfileIn(BaseModel):
    username: Optional[str] = None
    sport: Optional[str] = None  # "tennis" | "padel"


@app.patch("/users/{uid}/profile")
def update_profile(uid: str, body: ProfileIn):
    if body.username:
        config.save_username(body.username.strip(), uid)
    # sport preference: stored via config (extend config.py with get/save_sport if needed)
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


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
