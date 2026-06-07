"""Ask the coach — data-aware chat with video analysis."""
from __future__ import annotations
import base64, re

import streamlit as st

from coach import db, claude_client, config, swingvision
from pages.stats import _in_pct
from pages.history_widget import save_btn, history_tab


def _player_summary() -> str:
    """Full player data — all sessions, all metrics."""
    sessions  = db.get_sessions(limit=20)
    ntrp_cur  = config.get_ntrp()
    ntrp_next = config.get_ntrp_next()
    lines = [f"רמה: NTRP {ntrp_cur} → {ntrp_next} | סה״כ סשנים: {len(sessions)}", ""]

    for s in sessions:
        st     = s.get("stats", {})
        stk    = st.get("strokes", {})
        spd    = st.get("speed", {})
        spin   = st.get("spin", {})
        note   = s.get("note", {})

        def _v(stroke, key, alt_key=None):
            v = stk.get(stroke, {}).get(key) or spd.get(stroke, {}).get(alt_key or key)
            return v or "—"

        fh_spd = _v("Forehand", "avg_speed", "avg")
        bh_spd = _v("Backhand", "avg_speed", "avg")
        fh_in  = stk.get("Forehand", {}).get("in_pct") or stk.get("Forehand", {}).get("in_rate", "—")
        bh_in  = stk.get("Backhand", {}).get("in_pct") or stk.get("Backhand", {}).get("in_rate", "—")
        fh_ts  = spin.get("Forehand", {}).get("topspin", "—")
        bh_ts  = spin.get("Backhand", {}).get("topspin", "—")
        vols   = stk.get("Volley", {}).get("count", 0)
        opp    = f" vs {note['opponent']}" if note.get("opponent") else ""
        score  = f" ({note['score']})" if note.get("score") else ""

        lines.append(
            f"{s['date']}{opp}{score}: {s['shots']} מכות | IN {_in_pct(s)}% | "
            f"FH {fh_spd}/{fh_in}%IN | BH {bh_spd}/{bh_in}%IN | "
            f"TS-FH {fh_ts}% TS-BH {bh_ts}% | וולי {vols}"
        )

    lvl = config.get_ntrp_assessment().get("text", "")
    if lvl:
        lines += ["", "## הערכת רמה:", lvl[:500]]

    return "\n".join(lines)


def _detect_video_request(text: str) -> str | None:
    """Return match_id if user mentions a specific video/session."""
    sessions = db.get_sessions(limit=20)
    # Match by date pattern in the question
    dates = re.findall(r"\d{2}[/\-\.]\d{2}[/\-\.]\d{2,4}|\d{4}-\d{2}-\d{2}", text)
    for d in dates:
        # normalize to YYYY-MM-DD
        d_norm = d.replace("/", "-").replace(".", "-")
        if len(d_norm) == 8:  # DD-MM-YY
            parts = d_norm.split("-")
            d_norm = f"20{parts[2]}-{parts[1]}-{parts[0]}"
        for s in sessions:
            if s["date"] == d_norm or s["date"].endswith(d_norm[-5:]):
                return s["match_id"]
    # "האחרון" / "last" → latest session
    if any(w in text for w in ["האחרון", "אחרון", "הכי חדש", "last"]):
        return sessions[0]["match_id"] if sessions else None
    return None


def _frame_cost_estimate(num_frames: int) -> str:
    """Rough USD cost estimate for sending num_frames images + question to Opus."""
    cost = 0.015 + num_frames * 0.008
    return f"~${cost:.2f}"


def _get_frames_for_session(match_id: str, num_frames: int = 7) -> list[str]:
    """
    Get frames for a session:
    1. Try thumbnail from API (fast, 1 frame)
    2. Download full video and extract frames
    Returns list of base64 JPEG strings (capped at num_frames).
    """
    import requests as _req
    frames = []
    headers = {"User-Agent": "SwingVision/11.9.58"}

    if num_frames <= 0:
        return frames

    # Step 1: get thumbnail (fast)
    try:
        data = swingvision.fetch_match(match_id)
        vids = data.get("match_videos") or data.get("pending_match_videos") or []
        thumb_url = vids[0].get("thumbnail_url") if vids else None
        if thumb_url:
            r = _req.get(thumb_url, headers=headers, timeout=10)
            if r.status_code == 200:
                frames.append(base64.b64encode(r.content).decode())
    except Exception:
        pass

    if len(frames) >= num_frames:
        return frames[:num_frames]

    # Step 2: ffmpeg extracts remaining frames directly from CDN URL
    try:
        import subprocess, tempfile, os, glob
        video_url = swingvision.fetch_fresh_video_url(match_id)
        if video_url:
            remaining = num_frames - len(frames)
            tmpdir = tempfile.mkdtemp()
            cmd = [
                "ffmpeg", "-y",
                "-user_agent", "SwingVision/11.9.58",
                "-i", video_url,
                "-vf", "fps=1/30,scale=960:-1",   # 1 frame every 30s
                "-frames:v", str(remaining),
                "-q:v", "3",
                os.path.join(tmpdir, "f%02d.jpg")
            ]
            subprocess.run(cmd, capture_output=True, timeout=45)
            for f in sorted(glob.glob(os.path.join(tmpdir, "f*.jpg"))):
                with open(f, "rb") as fh:
                    frames.append(base64.b64encode(fh.read()).decode())
                os.unlink(f)
            try: os.rmdir(tmpdir)
            except Exception: pass
    except Exception:
        pass

    return frames[:num_frames]


def _build_video_message(question: str, frames_b64: list[str], session_date: str) -> list[dict]:
    """Build a multimodal message with frames + question."""
    content: list = [{"type": "text", "text": f"סרטון מתאריך {session_date}:"}]
    for i, b64 in enumerate(frames_b64):
        content.append({"type": "text", "text": f"פריים {i+1}:"})
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg", "data": b64
        }})
    content.append({"type": "text", "text": question})
    return content


def render():
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    view = st.radio("", ["💬 שיחה", "📚 היסטוריה"], horizontal=True,
                    label_visibility="collapsed", key="chat_view")
    if view == "📚 היסטוריה":
        history_tab("chat")
        return
    st.title("שאל את המאמן")

    # Load from DB on first render
    if "chat_msgs" not in st.session_state:
        saved = db.load_chat()
        st.session_state.chat_msgs = saved          # display messages
        # Rebuild API history (text only — images too large to persist)
        st.session_state.chat_api = [
            {"role": m["role"], "content": m["content"]}
            for m in saved
        ]

    # Banner when continuing a saved conversation
    if st.session_state.get("chat_loaded_title"):
        title = st.session_state.pop("chat_loaded_title")
        st.success(f"✅ ממשיך שיחה: **{title}**")

    # Session selector — in main area
    sessions = db.get_sessions(limit=20)
    def _lbl(s):
        opp = s["note"].get("opponent","") if s else ""
        return f"{s['date']}" + (f" vs {opp}" if opp else "") if s else "ללא סרטון"

    c_sel, c_frames, c_btn = st.columns([3, 1, 1])
    with c_sel:
        sel_vid = st.selectbox(
            "📹 שתף סרטון עם המאמן",
            [None] + sessions,
            format_func=lambda s: _lbl(s),
            label_visibility="collapsed",
            key="chat_sel_vid"
        )
    with c_frames:
        num_frames = st.number_input(
            "פריימים לניתוח", min_value=1, max_value=15, value=7, step=1,
            key="chat_num_frames", label_visibility="collapsed"
        )
    with c_btn:
        if st.button("📹 שתף", use_container_width=True) and sel_vid:
            st.session_state["send_video_with_next"] = True
            st.toast(f"✅ סרטון {sel_vid['date']} יישלח עם ההודעה הבאה", icon="📹")

    if sel_vid:
        st.caption(f"💰 עלות משוערת לניתוח {num_frames} פריימים: **{_frame_cost_estimate(num_frames)}**")

    # Display history
    for msg in st.session_state.chat_msgs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if q := st.chat_input("שאל... (למשל: תסתכל על הסרטון האחרון ותגיד מה הבעיה בבקהנד)"):
        st.session_state.chat_msgs.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)

        # Load frames only when:
        # 1. User explicitly pressed "שתף סרטון" button (not just selected from dropdown)
        # 2. Question text explicitly mentions video keywords AND auto-detect finds a match
        video_frames = []
        video_date   = ""

        video_keywords = ["תסתכל","תצפה","תראה","תבדוק","סרטון","פריים","תנועה"]
        question_asks_for_video = any(w in q for w in video_keywords)

        target_session = None
        if st.session_state.get("send_video_with_next") and sel_vid:
            # User explicitly pressed the share button
            target_session = sel_vid
            st.session_state.pop("send_video_with_next", None)
        elif question_asks_for_video:
            # Auto-detect from question
            mid = _detect_video_request(q)
            if mid:
                target_session = db.get_session(mid)

        if target_session:
            with st.spinner("טוען פריימים..."):
                try:
                    video_frames = _get_frames_for_session(target_session["match_id"], int(num_frames))
                    video_date   = target_session["date"]
                    if video_frames:
                        st.caption(f"✅ {len(video_frames)} פריימים מ-{video_date}")
                    else:
                        st.warning("לא הצלחתי לטעון פריימים")
                except Exception as e:
                    st.warning(f"שגיאה: {e}")

        with st.chat_message("assistant"):
            ph = st.empty(); result = []
            summary = _player_summary()
            system = (f"אתה מאמן טניס אישי. רמה: {ntrp_cur} → {ntrp_next}.\n"
                      f"פרופיל שחקן:\n{summary}\n"
                      f"ענה בעברית. היצמד לנתונים.")

            if video_frames:  # override system with video-aware version
                system = (f"אתה מאמן טניס אישי. רמה: {ntrp_cur} → {ntrp_next}.\n"
                          f"פרופיל שחקן:\n{summary}\n"
                          f"קיבלת {len(video_frames)} פריימים מסרטון {video_date}. "
                          f"נתח אותם ויזואלית לפי בקשת השחקן. ענה בעברית.")
                api_msgs = st.session_state.chat_api + [{
                    "role": "user",
                    "content": _build_video_message(q, video_frames, video_date)
                }]
            else:
                api_msgs = st.session_state.chat_api + [{"role": "user", "content": q}]

            for chunk in claude_client.stream_messages(api_msgs, system=system, max_tokens=2000):
                result.append(chunk)
                ph.markdown("".join(result))

        resp = "".join(result)
        st.session_state.chat_msgs.append({"role": "assistant", "content": resp})
        st.session_state.chat_api.append({"role": "user",      "content": q})
        st.session_state.chat_api.append({"role": "assistant", "content": resp})
        # Persist to DB
        db.save_chat(st.session_state.chat_msgs)

    # Bottom bar
    if st.session_state.chat_msgs:
        c1, c2 = st.columns(2)
        with c1:
            chat_text = "\n\n".join(
                f"{'אני' if m['role']=='user' else 'מאמן'}: {m['content']}"
                for m in st.session_state.chat_msgs
            )
            # Use first user message as title — same conversation = same title = overwrites
            first_q = next((m["content"][:40] for m in st.session_state.chat_msgs
                            if m["role"] == "user"), "שיחה")
            save_btn("chat", first_q, chat_text, "chat_save",
                     messages=st.session_state.chat_msgs)
        with c2:
            if st.button("נקה שיחה", type="secondary"):
                st.session_state.chat_msgs = []
                st.session_state.chat_api  = []
                db.save_chat([])
                st.rerun()
