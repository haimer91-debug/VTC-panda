"""Close the Loop — capture learnings after each session."""
from datetime import datetime
from pathlib import Path

MEMORY = Path(__file__).parent.parent / "memory"


def log_learning(pattern: str, evidence: str, strength: int = 1) -> None:
    """Add a pattern to learning-log.md."""
    f = MEMORY / "learning-log.md"
    entry = (
        f"\n### {datetime.now().strftime('%Y-%m-%d')} | {pattern}\n"
        f"**תצפית:** {evidence}\n"
        f"**חוזק:** {strength}/3\n"
    )
    current = f.read_text(encoding="utf-8") if f.exists() else ""
    # Insert before "## Promoted to Core"
    if "## Promoted to Core" in current:
        current = current.replace("## Promoted to Core", entry + "\n## Promoted to Core")
    else:
        current += entry
    f.write_text(current, encoding="utf-8")
    # Clear LRU cache so next prompt sees new data
    from coach.claude_client import _read_memory
    _read_memory.cache_clear()


def log_decision(decision: str, rationale: str, trigger: str = "") -> None:
    """Add a decision to decisions.md."""
    f = MEMORY / "decisions.md"
    entry = (
        f"\n### {datetime.now().strftime('%Y-%m-%d')} | {decision}\n"
        f"**נימוק:** {rationale}\n"
        + (f"**טריגר:** {trigger}\n" if trigger else "")
    )
    current = f.read_text(encoding="utf-8") if f.exists() else ""
    if "## Pending Review" in current:
        current = current.replace("## Pending Review", entry + "\n## Pending Review")
    else:
        current += entry
    f.write_text(current, encoding="utf-8")
    from coach.claude_client import _read_memory
    _read_memory.cache_clear()


def log_feedback(text: str) -> None:
    """Add player feedback to feedback.md."""
    f = MEMORY / "feedback.md"
    entry = f"\n### {datetime.now().strftime('%Y-%m-%d')}\n{text}\n"
    current = f.read_text(encoding="utf-8") if f.exists() else ""
    f.write_text(current + entry, encoding="utf-8")


def render_loop_widget(session_date: str = ""):
    """Streamlit widget for closing the loop after a session."""
    import streamlit as st
    with st.expander("🔄 סגור לולאה — מה למדת מהסשן?", expanded=False):
        st.caption("הזן תובנות — הן ישפרו את הניתוחים הבאים")
        pattern  = st.text_input("דפוס שגילית", placeholder="למשל: BH topspin משתפר בחימום ארוך יותר")
        evidence = st.text_input("על בסיס מה?", placeholder="למשל: 3 סשנים אחרונים — topspin עלה מ-33% ל-75%")
        strength = st.slider("כמה פעמים ראית את זה?", 1, 3, 1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 שמור תובנה", type="primary") and pattern:
                log_learning(pattern, evidence or "לא צוין", strength)
                st.success("✅ נשמר ב-learning-log")
        with col2:
            feedback = st.text_area("משוב אישי", placeholder="מה עבד? מה לא?", height=60)
            if st.button("💬 שמור משוב") and feedback:
                log_feedback(f"**סשן {session_date}:** {feedback}")
                st.success("✅ נשמר ב-feedback")
