"""Cost guard — show estimate and ask confirmation before expensive calls."""
import streamlit as st

# Rough cost per call in USD
COSTS = {
    "video_analysis":   ("~$0.08", "ניתוח סרטון — Opus + תמונות"),
    "training_plan":    ("~$0.05", "תכנית אימון — Opus"),
    "pipeline":         ("~$0.20", "Multi-agent pipeline — 4 קריאות Opus"),
    "stats_analysis":   ("~$0.03", "ניתוח סטטיסטיקות — Opus"),
    "strategy":         ("~$0.04", "אסטרטגיה — Opus"),
    "level_assessment": ("~$0.06", "הערכת רמה — Opus + כל הסשנים"),
    "chat":             ("~$0.001","שיחה — Haiku (זול מאוד)"),
}


def confirm(action_key: str, button_label: str = "▶️ הפעל", key: str = "") -> bool:
    """Show cost estimate. Returns True only after user confirms."""
    cost, desc = COSTS.get(action_key, ("?", action_key))
    st.caption(f"💰 עלות משוערת: **{cost}** | {desc}")
    return st.button(button_label, key=key or action_key, type="primary",
                     use_container_width=True)
