"""Reusable PDF export button for all pages."""
from datetime import datetime
import streamlit as st
from coach.pdf_export import text_to_pdf


def pdf_button(content: str, title: str, filename_prefix: str = "export"):
    """Show download button if content exists."""
    if not content or not content.strip():
        return
    try:
        pdf = text_to_pdf(title, content)
        st.download_button(
            "💾 ייצוא PDF",
            data=pdf,
            file_name=f"{filename_prefix}_{datetime.now().strftime('%Y-%m-%d')}.pdf",
            mime="application/pdf",
            type="secondary",
        )
    except Exception as e:
        st.caption(f"PDF: {e}")
