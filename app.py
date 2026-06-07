"""Virtual Tennis Coach — entry point."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from coach import db, config
from pages import videos, stats, coaching, chat

st.set_page_config(
    page_title="Virtual Tennis Coach",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init()

# ── Login (beta: username only, no password) ─────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_id:
    st.markdown("## 🎾 Virtual Tennis Coach — כניסה")
    st.caption("גרסת בטא: הזן שם משתמש כדי להמשיך (ללא סיסמה).")
    existing = config.list_users()
    name = st.text_input("שם משתמש", placeholder="לדוגמה: haim")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("כניסה", type="primary") and name.strip():
            uid = name.strip().lower()
            config.ensure_user(uid, default_username=name.strip())
            st.session_state.user_id = uid
            st.rerun()
    with col2:
        if existing:
            st.caption("משתמשים קיימים: " + ", ".join(existing))
    st.stop()

# Apply the logged-in user to both the config and db layers so every call
# in this Streamlit run (including pages/) is automatically scoped to them.
db.set_current_user(st.session_state.user_id)
config.set_current_user(st.session_state.user_id)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family:'Heebo',sans-serif!important; direction:rtl; }
.stButton>button { border-radius:8px; font-weight:700; }
.stButton>button[kind="primary"] { background:#BBFD00; color:#111; border:none; }
.stButton>button[kind="primary"]:hover { background:#ccff20; }
div[data-testid="stMetricValue"] { font-weight:900; color:#BBFD00; }
div[data-testid="stDecoration"],#MainMenu,footer { display:none; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    username = config.get_username() or "Player"
    ntrp     = config.get_ntrp()
    initials = "".join(w[0].upper() for w in username.split()[:2])

    st.markdown(f"""
<div style="padding:16px 8px 8px">
  <div style="font-size:1.1rem;font-weight:900;color:#fff">🎾 Virtual Tennis Coach</div>
  <div style="font-size:.6rem;font-weight:700;color:#BBFD00;letter-spacing:4px">BY PANDA</div>
</div>
<div style="background:#1a1a1a;border-radius:12px;padding:12px;margin:8px">
  <span style="background:#BBFD00;color:#111;font-weight:900;border-radius:50%;
        width:36px;height:36px;display:inline-flex;align-items:center;
        justify-content:center;float:right;margin-left:10px">{initials}</span>
  <div style="font-weight:700;color:#fff">{username}</div>
  {'<div style="display:inline-block;background:#1e1e1e;color:#BBFD00;font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:20px;margin-top:8px">🎯 NTRP ' + ntrp + '</div>' if ntrp else ''}
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    PAGES = {
        "🎬  סרטונים":   videos,
        "📊  סטטיסטיקות": stats,
        "📋  אימון":      coaching,
        "💬  מאמן":       chat,
    }
    page = st.radio("", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("---")
    with st.expander("⚙️ הגדרות"):
        u = st.text_input("שם משתמש", value=username, label_visibility="collapsed")
        if st.button("עדכן") and u.strip():
            config.save_username(u.strip())
            st.rerun()
        st.caption(f"מחובר/ת כ: {st.session_state.user_id}")
        if st.button("התנתק/י"):
            st.session_state.user_id = None
            st.rerun()

# ── Render page ───────────────────────────────────────────────────────────────
PAGES[page].render()
