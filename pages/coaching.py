"""Training plan + Strategy — combined page."""
from __future__ import annotations

import streamlit as st

from coach import db, swingvision, claude_client, config
from pages.stats import _in_pct
from pages.history_widget import save_btn, history_tab


def _latest_stats_text() -> str:
    sessions = db.get_sessions(limit=1)
    if not sessions:
        return "אין נתונים"
    s = sessions[0]
    stats = s.get("stats", {})
    lines = [f"סשן: {s['date']} | {s['shots']} מכות"]
    lines.append(f"IN: {_in_pct(s)}%")
    for stroke, d in stats.get("strokes", {}).items():
        spd = d.get("avg_speed", d.get("avg", 0))
        ip  = d.get("in_pct",   d.get("in_rate", 0))
        lines.append(f"{stroke}: {spd} קמ\"ש | IN {ip}%")
    return "\n".join(lines)


def render():
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    view = st.radio("", ["📋 אימון ואסטרטגיה", "📚 היסטוריה"], horizontal=True,
                    label_visibility="collapsed", key="coach_view")
    if view == "📚 היסטוריה":
        history_tab("coaching")
        return
    st.title("אימון ואסטרטגיה")

    tab_plan, tab_strategy = st.tabs(["📋 תכנית אימון", "🎯 אסטרטגיה"])

    # ── Training plan ─────────────────────────────────────────────────────────
    with tab_plan:
        c1, c2 = st.columns(2)
        with c1:
            focus = st.text_input("נושא דגש (רשות)", placeholder="פורהנד, תנועה...")
        with c2:
            dur_sel    = st.selectbox("משך", ["45 דק'","60 דק'","75 דק'","90 דק'","120 דק'"], index=2)
            dur_custom = st.text_input("או הקלד ידנית", placeholder="60")
            duration   = int(dur_custom) if dur_custom.strip().isdigit() else int(dur_sel.replace(" דק'",""))

        use_pipeline = st.toggle("🤖 Multi-agent (איכות גבוהה, איטי יותר)", value=False)
        cached_plan = db.get_analysis("training_plan")
        if cached_plan:
            st.markdown(cached_plan)
            c1, c2 = st.columns(2)
            with c1: save_btn("coaching", "תכנית אימון", cached_plan, "plan")
            with c2:
                if st.button("🔄 בנה מחדש", type="secondary"):
                    db.save_analysis("training_plan", ""); st.rerun()
        else:
            from pages.cost_guard import confirm
            cost_key = "pipeline" if use_pipeline else "training_plan"
            if confirm(cost_key, "📋 בנה תכנית", key="build_plan"):
                stats_text = _latest_stats_text()
                ph = st.empty(); result = []
                fn = claude_client.training_plan_pipeline if use_pipeline else claude_client.training_plan
                for chunk in fn(stats_text, focus, duration, ntrp_cur, ntrp_next):
                    result.append(chunk)
                    ph.markdown("".join(result))
                db.save_analysis("training_plan", "".join(result))
                st.rerun()

    # ── Strategy ──────────────────────────────────────────────────────────────
    with tab_strategy:
        c1, c2, c3 = st.columns(3)
        with c1:
            surface = st.selectbox("משטח", ["קשה","חימר","עשב","שטיח"])
        with c2:
            fmt = st.selectbox("פורמט", ["יחידים","זוגות"])
        with c3:
            sets_fmt = st.selectbox("סטים", ["3 סטים","2 סטים","פרו סט"])

        # Opponent
        st.markdown("#### יריב")
        sessions  = db.get_sessions()
        all_notes = {s["match_id"]: s["note"] for s in sessions}
        known_opps = sorted({n.get("opponent","") for n in all_notes.values() if n.get("opponent")})

        opp_type = st.radio("", ["יריב ידוע","יריב חדש"], horizontal=True,
                            label_visibility="collapsed")
        opponent = ""
        opp_data_str = ""
        guest_data = {}

        if opp_type == "יריב ידוע" and known_opps:
            opponent = st.selectbox("בחר יריב", known_opps, label_visibility="collapsed")
            opp_sessions = [mid for mid, n in all_notes.items() if n.get("opponent") == opponent]

            if opp_sessions and st.checkbox(f"נתח סרטון מול {opponent}"):
                # pick sessions with this opponent
                opp_rows = [s for s in sessions if s["match_id"] in opp_sessions]
                if opp_rows:
                    sel_opp = st.selectbox("סרטון", opp_rows,
                                           format_func=lambda s: f"{s['date']} • {s['shots']} מכות",
                                           label_visibility="collapsed")
                    if st.button("📊 טען נתוני יריב"):
                        with st.spinner("מושך נתוני שחקן 2..."):
                            try:
                                guest_data = swingvision.analyze_opponent(sel_opp["match_id"])
                                st.session_state["guest_data"] = guest_data
                                st.session_state["guest_opp"] = opponent
                            except Exception as e:
                                st.error(f"שגיאה: {e}")

            if st.session_state.get("guest_opp") == opponent and st.session_state.get("guest_data"):
                guest_data = st.session_state["guest_data"]
                lines = [f"נתוני {opponent} כשחקן 2:"]
                for stroke, d in guest_data.get("strokes", {}).items():
                    lines.append(f"  {stroke}: {d['avg_speed']} קמ\"ש | IN {d['in_pct']}% | ספין: {d['spin']}")
                if guest_data.get("dirs"):
                    lines.append(f"  כיוונים: {list(guest_data['dirs'].keys())[:3]}")
                opp_data_str = "\n".join(lines)
                st.caption(opp_data_str)
        else:
            opponent = st.text_input("שם יריב", placeholder="אופציונלי", label_visibility="collapsed")
            opp_style = st.text_area("תאר את סגנון היריב",
                                     placeholder="Baseliner אגרסיבי, פורהנד חזק...",
                                     height=68, label_visibility="collapsed")
            if opp_style:
                opp_data_str = f"תיאור יריב: {opp_style}"

        opp_level = st.selectbox("רמת היריב",
                                  ["לא ידוע","חלש ממני","שווה","חזק ממני","הרבה חזק"])

        opponent_full = f"יריב: {opponent or 'לא ידוע'} | רמה: {opp_level}\n{opp_data_str}"

        strat_key = f"strategy_{opponent or 'general'}"
        cached_strat = db.get_analysis(strat_key)
        if cached_strat:
            st.markdown(cached_strat)
            c1, c2 = st.columns(2)
            with c1: save_btn("coaching", f"אסטרטגיה — {opponent or surface}", cached_strat, "strat")
            with c2:
                if st.button("🔄 בנה מחדש", type="secondary", key="strat_redo"):
                    db.save_analysis(strat_key, ""); st.rerun()
        elif st.button("🎯 בנה אסטרטגיה", type="primary", use_container_width=True):
            my_stats = _latest_stats_text()
            ph = st.empty(); result = []
            for chunk in claude_client.strategy(my_stats, opponent_full, surface,
                                                 f"{fmt} | {sets_fmt}", ntrp_cur):
                result.append(chunk)
                ph.markdown("".join(result))
            db.save_analysis(strat_key, "".join(result))
            st.rerun()
