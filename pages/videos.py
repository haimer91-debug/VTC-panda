"""Videos page — list, notes, watch, AI analysis."""
from __future__ import annotations
import io
from pathlib import Path

import streamlit as st
from PIL import Image

from coach import db, swingvision, claude_client, config
from pages.stats import _in_pct
from pages.history_widget import save_btn, history_tab


def render():
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    view = st.radio("", ["🎬 ניתוח", "📚 היסטוריה"], horizontal=True,
                    label_visibility="collapsed", key="videos_view")
    if view == "📚 היסטוריה":
        history_tab("videos")
        return
    st.title("סרטונים")

    sessions = db.get_sessions()
    if not sessions:
        _import_section()
        return

    # ── Import bar ────────────────────────────────────────────────────────────
    _import_section()
    st.divider()

    # ── Session selector ──────────────────────────────────────────────────────
    def _label(s):
        opp = s["note"].get("opponent", "")
        tag = f" vs {opp}" if opp else ""
        return f"{s['date']}  •  {s['shots']} מכות{tag}"

    sel = st.selectbox("בחר סרטון", sessions,
                       format_func=_label, label_visibility="collapsed")
    if not sel:
        return

    mid = sel["match_id"]

    # ── Two columns: notes | stats ────────────────────────────────────────────
    col_notes, col_stats = st.columns([1, 1], gap="large")

    with col_notes:
        _notes_form(mid, sel["note"])

    with col_stats:
        s = sel["stats"]
        if s.get("strokes"):
            for stroke, d in s["strokes"].items():
                spd = d.get("avg_speed", d.get("avg", "—"))
                ip  = d.get("in_pct",   d.get("in_rate", "—"))
                st.metric(stroke, f"{spd} קמ\"ש", f"{ip}% IN")
        st.metric("% IN כללי", f"{_in_pct(sel)}%")

    st.divider()

    # ── Video + Analysis ──────────────────────────────────────────────────────
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("▶️ צפה בסרטון", use_container_width=True):
            with st.spinner("טוען..."):
                url = swingvision.fetch_fresh_video_url(mid)
            if url:
                db.update_video_url(mid, url)
                st.session_state[f"vurl_{mid}"] = url
            else:
                st.warning("הסרטון לא זמין עדיין")

    with c2:
        num_frames = st.number_input("פריימים", 4, 16, 8, 2,
                                     label_visibility="collapsed")

    if st.session_state.get(f"vurl_{mid}"):
        st.video(st.session_state[f"vurl_{mid}"])

    cached_analysis = db.get_analysis(f"video_{mid}")
    if cached_analysis:
        st.markdown("**ניתוח שמור:**")
        st.markdown(cached_analysis)
        c1, c2 = st.columns(2)
        with c1:
            save_btn("videos", f"ניתוח סרטון {sel['date']}", cached_analysis, f"vid_{mid}")
        with c2:
            if st.button("🔄 נתח מחדש", type="secondary"):
                db.save_analysis(f"video_{mid}", "")
                st.rerun()
    else:
        from pages.cost_guard import confirm
        if confirm("video_analysis", "🎬 נתח סרטון", key="analyze_vid"):
            _run_analysis(mid, sel, ntrp_cur, ntrp_next, num_frames)


def _import_section():
    tab_file, tab_link = st.tabs(["📁 העלאת קובץ (מומלץ)", "🔗 לינק SwingVision"])

    # ── Tab 1: file upload — the easy, recommended path ──────────────────────
    with tab_file:
        st.caption("ייצא קובץ מתוך אפליקציית SwingVision (Excel / CSV / JSON) והעלה אותו כאן — "
                   "כל הסשנים ייובאו בבת אחת.")
        uploaded = st.file_uploader(
            "גרור קובץ לכאן או לחץ לבחירה",
            type=["xlsx", "xls", "csv", "json", "jsonl"],
            label_visibility="collapsed",
            key="sv_file_uploader",
        )
        if uploaded is not None:
            if st.button("📥 ייבא קובץ", type="primary", use_container_width=True, key="btn_import_file"):
                _handle_file_import(uploaded)

    # ── Tab 2: paste a SwingVision share link (single session) ───────────────
    with tab_link:
        col_link, col_btn = st.columns([5, 1])
        with col_link:
            link = st.text_input("", placeholder="🔗 הדבק לינק SwingVision — https://swing.vision/matches/...",
                                 label_visibility="collapsed", key="sv_link_input")
        with col_btn:
            if st.button("ייבא", use_container_width=True) and link.strip():
                mid = swingvision.extract_match_id(link.strip())
                if not mid:
                    st.error("לינק לא תקין")
                elif db.session_exists(mid):
                    st.info("הסרטון כבר קיים")
                else:
                    with st.spinner("מייבא..."):
                        try:
                            s = swingvision.parse_session(mid)
                            db.save_session(s["match_id"], s["date"], s["shots"],
                                            s["rallies"], s, s.get("video_url"))
                            st.toast(f"✅ {s['shots']} מכות יובאו", icon="🎾")
                            st.rerun()
                        except Exception as e:
                            st.error(f"שגיאה: {e}")


def _handle_file_import(uploaded_file):
    """Parse an uploaded export file and bulk-import any new sessions found."""
    import tempfile, os
    from coach import swingvision_parser as svp

    suffix = Path(uploaded_file.name).suffix or ".xlsx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    try:
        with st.spinner("קורא את הקובץ..."):
            rows = svp.parse_file(tmp_path)

        if not rows:
            st.warning("לא נמצאו שורות נתונים בקובץ")
            return

        if not svp.looks_like_session_summary(rows):
            st.warning(
                "פורמט הקובץ לא זוהה כייצוא סשנים. ודא שזה קובץ '📤 ייצוא נתוני סשנים' "
                "מתוך SwingVision (לא קובץ מכות בודדות)."
            )
            return

        sessions = svp.sessions_from_summary_rows(rows)
        if not sessions:
            st.warning("לא נמצאו סשנים תקינים בקובץ")
            return

        new_count, dup_count = 0, 0
        with st.spinner(f"מייבא {len(sessions)} סשנים..."):
            for s in sessions:
                if db.session_exists(s["match_id"]):
                    dup_count += 1
                    continue
                stats = {k: v for k, v in s.items()
                         if k not in ("match_id", "date", "shots", "rallies", "video_url", "note")}
                db.save_session(s["match_id"], s["date"], s["shots"], s["rallies"],
                                stats, s.get("video_url"))
                if s.get("note", {}).get("opponent") or s.get("note", {}).get("free"):
                    db.save_note(s["match_id"], s["note"])
                new_count += 1

        if new_count:
            st.success(f"✅ יובאו {new_count} סשנים חדשים" +
                       (f" • {dup_count} כבר היו קיימים ודולגו" if dup_count else ""))
            st.rerun()
        else:
            st.info(f"כל ה-{dup_count} הסשנים בקובץ כבר קיימים — אין מה לייבא")

    except Exception as e:
        st.error(f"שגיאה בייבוא הקובץ: {e}")
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def _notes_form(mid: str, note: dict):
    with st.form(f"notes_{mid}"):
        st.caption("הערות על הסרטון")
        opponent = st.text_input("יריב", value=note.get("opponent", ""))
        c1, c2 = st.columns(2)
        with c1:
            match_type = st.selectbox("סוג", ["אימון", "משחק"],
                                       index=0 if note.get("type","אימון")=="אימון" else 1)
            opp_level  = st.selectbox("רמת יריב",
                                       ["לא ידוע","חלש","שווה","חזק","הרבה חזק"],
                                       index=["לא ידוע","חלש","שווה","חזק","הרבה חזק"].index(
                                           note.get("opp_level","לא ידוע")))
        with c2:
            score = st.text_input("תוצאה", value=note.get("score",""))
            fmt   = st.selectbox("פורמט", ["יחידים","זוגות"],
                                  index=0 if note.get("format","יחידים")=="יחידים" else 1)
        free = st.text_area("הערות", value=note.get("free",""), height=60)
        if st.form_submit_button("💾 שמור"):
            db.save_note(mid, {"opponent": opponent, "type": match_type,
                               "opp_level": opp_level, "score": score,
                               "format": fmt, "free": free})
            st.toast("✅ נשמר")
            st.rerun()


def _run_analysis(mid: str, sess: dict, ntrp_cur: str, ntrp_next: str, num_frames: int):
    url = sess.get("video_url") or swingvision.fetch_fresh_video_url(mid)
    if not url:
        st.error("אין URL לסרטון זה — לחץ על 'צפה בסרטון' קודם")
        return

    # Extract frames via ffmpeg (handles CDN URLs natively)
    frames_b64 = []
    try:
        import subprocess, tempfile, os, glob, base64
        with st.spinner(f"מחלץ {num_frames} פריימים..."):
            tmpdir = tempfile.mkdtemp()
            cmd = [
                "ffmpeg", "-y",
                "-user_agent", "SwingVision/11.9.58",
                "-i", url,
                "-vf", f"fps=1/30,scale=960:-1",
                "-frames:v", str(num_frames),
                "-q:v", "3",
                os.path.join(tmpdir, "f%02d.jpg")
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)
            for f in sorted(glob.glob(os.path.join(tmpdir, "f*.jpg"))):
                with open(f, "rb") as fh:
                    frames_b64.append(base64.b64encode(fh.read()).decode())
                os.unlink(f)
            try: os.rmdir(tmpdir)
            except Exception: pass
    except Exception as e:
        st.error(f"שגיאה בחילוץ פריימים: {e}")
        return

    if not frames_b64:
        st.error("לא הצלחתי לחלץ פריימים — הסרטון אולי לא הסתיים להתעדכן ב-SwingVision")
        return

    if not frames_b64:
        st.error("לא הצלחתי לחלץ פריימים")
        return

    # Show frames
    st.markdown(f"**{len(frames_b64)} פריימים:**")
    cols = st.columns(min(len(frames_b64), 4))
    for i, b64 in enumerate(frames_b64):
        import base64 as _b64
        img_bytes = _b64.b64decode(b64)
        with cols[i % 4]:
            st.image(Image.open(io.BytesIO(img_bytes)), use_container_width=True)

    note = sess["note"]
    ctx = ""
    if note.get("type") == "משחק":
        ctx = f"\nהקשר: משחק נגד {note.get('opponent','?')} (רמה: {note.get('opp_level','?')}). תוצאה: {note.get('score','?')}."

    st.markdown("**ניתוח המאמן:**")
    ph = st.empty(); result = []
    for chunk in claude_client.analyze_video(frames_b64, ctx, ntrp_cur, ntrp_next):
        result.append(chunk)
        ph.markdown("".join(result))
    db.save_analysis(f"video_{mid}", "".join(result))
