"""Shared save + history widget for all pages."""
import json
import streamlit as st
from coach.db import save_history, get_history, delete_history


def save_btn(category: str, title: str, content: str, key: str = "",
             messages: list | None = None):
    """'שמור שיחה' button — saves to history table."""
    if not content or not content.strip():
        return
    if st.button("💾 שמור שיחה", key=f"save_{key or category}", type="secondary"):
        msgs_json = json.dumps(messages, ensure_ascii=False) if messages else None
        save_history(category, title, content, msgs_json)
        st.toast("✅ נשמר בהיסטוריה", icon="💾")


def history_tab(category: str):
    """Renders history list for a category."""
    rows = get_history(category)
    if not rows:
        st.info("אין שיחות שמורות עדיין")
        return

    for r in rows:
        with st.expander(f"📅 {r['date']}  |  {r['title']}", expanded=False):
            st.markdown(r["content"])
            col_cont, col_del = st.columns([1, 1])

            # "המשך שיחה" — only for chat entries that have saved messages
            if category == "chat" and r.get("messages_json"):
                with col_cont:
                    if st.button("▶️ המשך שיחה", key=f"cont_{r['id']}", type="primary"):
                        try:
                            msgs = json.loads(r["messages_json"])
                            st.session_state["chat_msgs"] = msgs
                            st.session_state["chat_api"] = [
                                {"role": m["role"], "content": m["content"]}
                                for m in msgs
                            ]
                            st.session_state["chat_view"] = "💬 שיחה"
                            st.session_state["chat_loaded_title"] = r["title"]
                            st.rerun()
                        except Exception as e:
                            st.error(f"שגיאה בטעינה: {e}")

            with col_del:
                if st.button("🗑️ מחק", key=f"del_{r['id']}", type="secondary"):
                    delete_history(r["id"])
                    st.rerun()
