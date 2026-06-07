"""Statistics page — per-session stats + comparison."""
from __future__ import annotations

import streamlit as st
import pandas as pd

from coach import db, claude_client, config
from pages.history_widget import save_btn, history_tab
from pages.loop import render_loop_widget


def _in_pct(s: dict) -> float:
    """Extract in_pct from any session dict format (old or new)."""
    st = s.get("stats", {})
    return (st.get("in_pct")
            or st.get("in_out", {}).get("in_pct")
            or s.get("in_pct", 0)
            or 0)


def _stats_text(s: dict) -> str:
    stats = s.get("stats", {})
    lines = [f"סשן: {s['date']} | {s['shots']} מכות | {s['rallies']} ראלים"]
    lines.append(f"IN: {_in_pct(s)}%")
    for stroke, d in stats.get("strokes", {}).items():
        spd = d.get("avg_speed", d.get("avg", 0))
        ip  = d.get("in_pct",   d.get("in_rate", 0))
        lines.append(f"{stroke}: {spd} קמ\"ש | IN {ip}%")
    for stroke, spins in stats.get("spin", {}).items():
        top = max(spins, key=spins.get) if spins else "?"
        lines.append(f"  ספין {stroke}: {top}")
    return "\n".join(lines)


def render():
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    view = st.radio("", ["📊 נתונים", "📚 היסטוריה"], horizontal=True,
                    label_visibility="collapsed", key="stats_view")
    if view == "📚 היסטוריה":
        history_tab("stats")
        return
    st.title("סטטיסטיקות")

    sessions = db.get_sessions()
    if not sessions:
        st.info("טרם יובאו סרטונים — הדבק לינק בעמוד הסרטונים")
        return

    tab_session, tab_compare, tab_level = st.tabs(["📊 סשן", "📈 השוואה", "🎯 רמה"])

    # ── TAB 1: Single session ─────────────────────────────────────────────────
    with tab_session:
        def _label(s):
            opp = s["note"].get("opponent", "")
            return f"{s['date']}  •  {s['shots']} מכות" + (f" vs {opp}" if opp else "")

        sel = st.selectbox("סשן", sessions, format_func=_label,
                           label_visibility="collapsed")
        if not sel:
            return

        stats   = sel.get("stats", {})
        strokes = stats.get("strokes", {})

        # KPIs
        cols = st.columns(2 + len(strokes))
        cols[0].metric("מכות", sel["shots"])
        cols[1].metric("% IN", f"{_in_pct(sel)}%")
        for i, (stroke, d) in enumerate(strokes.items()):
            spd = d.get("avg_speed", d.get("avg", "—"))
            ip  = d.get("in_pct",   d.get("in_rate", "—"))
            cols[2+i].metric(stroke, f"{spd} קמ\"ש", f"{ip}% IN")

        # Stroke table
        if strokes:
            rows = [{"מכה": k,
                     "כמות": v.get("count", 0),
                     "מהירות ממוצעת": v.get("avg_speed", v.get("avg", 0)),
                     "מהירות מקס": v.get("max_speed", v.get("max", 0)),
                     "% IN": v.get("in_pct", v.get("in_rate", 0))}
                    for k, v in strokes.items()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Spin + directions
        c1, c2 = st.columns(2)
        with c1:
            spin = stats.get("spin", {})
            if spin:
                spin_rows = [{"מכה": k, "ספין": sp, "%": pct}
                             for k, spins in spin.items()
                             for sp, pct in spins.items()]
                st.dataframe(pd.DataFrame(spin_rows), use_container_width=True, hide_index=True)
        with c2:
            dirs = stats.get("directions", {})
            if dirs:
                st.dataframe(pd.DataFrame(list(dirs.items()), columns=["כיוון","מכות"]),
                             use_container_width=True, hide_index=True)

        st.divider()
        cache_key = f"stats_{sel['match_id']}"
        cached = db.get_analysis(cache_key)
        if cached:
            st.markdown(cached)
            c1, c2 = st.columns(2)
            with c1: save_btn("stats", f"ניתוח {sel['date']}", cached, f"stats_{sel['match_id']}")
            with c2:
                if st.button("🔄 נתח מחדש", type="secondary"):
                    db.save_analysis(cache_key, ""); st.rerun()
        elif st.button("🧠 ניתוח AI", type="primary"):
            ph = st.empty(); result = []
            for chunk in claude_client.analyze_stats(_stats_text(sel), ntrp_cur, ntrp_next):
                result.append(chunk)
                ph.markdown("".join(result))
            db.save_analysis(cache_key, "".join(result))

    # ── TAB 2: Comparison ─────────────────────────────────────────────────────
    with tab_compare:
        if len(sessions) < 2:
            st.info("נדרשים לפחות 2 סשנים")
        else:
            def _spd(st2: dict, stroke: str) -> float:
                """Get avg speed regardless of old/new format."""
                # New format: strokes[stroke]["avg_speed"]
                v = st2.get("strokes", {}).get(stroke, {}).get("avg_speed")
                if v: return v
                # Old format: speed[stroke]["avg"]
                v = st2.get("speed", {}).get(stroke, {}).get("avg")
                if v: return v
                return 0

            def _ts(st2: dict, stroke: str) -> float:
                """Get topspin % regardless of format."""
                sp = st2.get("spin", {}).get(stroke, {})
                # New: {"topspin": 80.5, ...}  Old: same structure
                return sp.get("topspin", sp.get("Topspin", 0))

            def _volley(st2: dict) -> int:
                v = st2.get("strokes", {}).get("Volley", {})
                return v.get("count", 0)

            def _deep(st2: dict) -> float:
                bd = st2.get("zones", {}).get("bounce_depth", {})
                if not bd: return 0
                total = sum(bd.values()) or 1
                deep = bd.get("deep", 0) + bd.get("baseline", 0)
                return round(deep / total * 100, 1)

            # Build metrics per session (chronological order)
            rows = []
            for s in reversed(sessions[:20]):
                st2 = s.get("stats", {})
                in_p = _in_pct(s)
                rows.append({
                    "תאריך":           s["date"],
                    "FH קמ\"ש":        _spd(st2, "Forehand"),
                    "BH קמ\"ש":        _spd(st2, "Backhand"),
                    "% IN":            in_p,
                    "% OUT":           round(100 - in_p, 1),
                    "Topspin FH %":    _ts(st2, "Forehand"),
                    "Topspin BH %":    _ts(st2, "Backhand"),
                    "כדורים עמוקים %": _deep(st2),
                    "כמות וולי":       _volley(st2),
                })

            df = pd.DataFrame(rows).set_index("תאריך")

            import plotly.graph_objects as go

            def _chart(title: str, series: dict[str, str], yaxis: str):
                """series = {column_name: display_label} — zeros treated as missing."""
                fig = go.Figure()
                colors = ["#BBFD00", "#00bfff", "#ff6b6b", "#ffa500"]
                for ci, (col, label) in enumerate(series.items()):
                    if col not in df.columns:
                        continue
                    # Replace 0 with NaN so they don't pull the line to zero
                    data = df[col].replace(0, float("nan")).dropna()
                    if data.empty:
                        continue
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data.values,
                        mode="lines+markers",
                        name=label,
                        line=dict(color=colors[ci % len(colors)], width=2.5),
                        marker=dict(size=7),
                        connectgaps=False,  # don't connect over missing values
                    ))
                fig.update_layout(
                    title=dict(text=title, font=dict(size=13, color="#fff")),
                    paper_bgcolor="#111", plot_bgcolor="#111",
                    font=dict(color="#aaa", size=11),
                    xaxis=dict(gridcolor="#222", tickangle=-30),
                    yaxis=dict(gridcolor="#222", title=yaxis),
                    legend=dict(orientation="h", y=-0.25),
                    margin=dict(l=30, r=10, t=40, b=60),
                    height=220,
                )
                return fig

            # Summary table — drop columns that are all-zero
            display_df = df.replace(0, float("nan"))
            display_df = display_df.dropna(axis=1, how="all").reset_index()
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            st.divider()

            c1, c2 = st.columns(2)
            charts = [
                ("Topspin — פורהנד ובקהנד",  {"Topspin FH %": "FH", "Topspin BH %": "BH"}, "%"),
                ("מהירות — פורהנד ובקהנד",   {"FH קמ\"ש": "FH",    "BH קמ\"ש": "BH"},      "קמ\"ש"),
                ("% IN לאורך זמן",            {"% IN": "IN"},                                "%"),
                ("% OUT לאורך זמן",           {"% OUT": "OUT"},                              "%"),
                ("כדורים עמוקים %",           {"כדורים עמוקים %": "עמוק"},                  "%"),
                ("כמות וולי",                 {"כמות וולי": "וולי"},                         "מכות"),
            ]
            for i, (title, series, yaxis) in enumerate(charts):
                with (c1 if i % 2 == 0 else c2):
                    st.plotly_chart(_chart(title, series, yaxis),
                                    use_container_width=True)

            cmp_cached = db.get_analysis("compare_all")
            if cmp_cached:
                st.markdown(cmp_cached)
                c1, c2 = st.columns(2)
                with c1: save_btn("stats", "ניתוח השוואתי", cmp_cached, "compare")
                with c2:
                    if st.button("🔄 עדכן ניתוח", type="secondary"):
                        db.save_analysis("compare_all", ""); st.rerun()
            elif st.button("🧠 ניתוח השוואתי AI", type="primary"):
                sessions_text = "\n\n---\n".join(_stats_text(s) for s in sessions[:6])
                prompt = f"""השוואה עצמית — {len(sessions)} סשנים. רמה {ntrp_cur} → {ntrp_next}

{sessions_text}

## נקודות שהתחזקו (עם מספרים)
## נקודות שנחלשו (עם מספרים)
## דפוסים עקביים
## פערים מרמת {ntrp_next}
## 3 עדיפויות לחודש הקרוב

השווה את השחקן לעצמו בלבד. ענה בעברית."""
                ph = st.empty(); result = []
                from coach.claude_client import stream
                for chunk in stream(prompt, "מאמן טניס. השוואה עצמית. ענה בעברית."):
                    result.append(chunk)
                    ph.markdown("".join(result))
                db.save_analysis("compare_all", "".join(result))

    # ── TAB 3: Level assessment ───────────────────────────────────────────────
    with tab_level:
        lvl = config.get_ntrp_assessment()
        if lvl["ntrp"]:
            st.success(f"🎯 רמה נוכחית: **NTRP {lvl['ntrp']}** (הוערך {lvl['date']})")
            st.markdown(lvl["text"])
            st.divider()
            if st.button("🔄 עדכן הערכה", type="secondary"):
                _run_level_assessment(sessions, ntrp_cur, ntrp_next)
        else:
            st.info("טרם בוצעה הערכת רמה")
            if st.button("🎯 הערך רמה", type="primary"):
                _run_level_assessment(sessions, ntrp_cur, ntrp_next)

    # Loop widget — appears below all tabs
    st.divider()
    render_loop_widget()


def _run_level_assessment(sessions: list, ntrp_cur: str, ntrp_next: str):
    sessions_text = "\n\n---\n".join(_stats_text(s) for s in sessions)
    prompt = f"""הערכת רמת NTRP מנתוני SwingVision בלבד.

{sessions_text}

## רמת NTRP משוערת: [X.X – X.X]
- FH: [ממוצע] קמ"ש → נורמת NTRP X.X
- BH: [ממוצע] קמ"ש → נורמת NTRP X.X
- IN%: [ממוצע]% → נורמת NTRP X.X
- עקביות בין סשנים

## חוזקות (עם מספרים)
## חולשות (עם מספרים)
## יעד ריאלי ל-6 חודשים: NTRP X.X
| מדד | עכשיו | יעד |

## שחקן ייחוס חובבני לרמה הנוכחית

ענה בעברית. היצמד לנתונים בלבד."""

    ph = st.empty(); result = []
    from coach.claude_client import stream
    for chunk in stream(prompt, "מאמן טניס עם ידע ב-NTRP. ענה בעברית.", max_tokens=4096):
        result.append(chunk)
        ph.markdown("".join(result))

    text = "".join(result)
    import re
    m = re.search(r"NTRP[^\d]*(\d\.\d\s*[–\-]\s*\d\.\d|\d\.\d)", text)
    ntrp_str = m.group(1).strip() if m else ""
    config.save_ntrp(ntrp_str, text)
    st.toast(f"✅ רמה {ntrp_str} נשמרה", icon="🎯")
    st.rerun()
