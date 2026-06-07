"""Generate clean Hebrew PDF reports from tennis analysis."""
import re
import io
from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from PIL import Image

FONT_PATH = str(Path(__file__).parent.parent / "fonts" / "NotoSansHebrew.ttf")
REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def _clean_text(text: str) -> str:
    """Remove markdown, fix whitespace."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"#{1,4}\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


def _parse_frame_sections(text: str) -> dict[int, str]:
    """Extract per-frame analysis blocks. Returns {frame_num: text}."""
    sections = {}
    # Handles: פריים 1: / **פריים 1:** / פריים 1 — / **פריים 1**
    pattern = re.finditer(
        r"\*{0,2}פריים\s+(\d+)\*{0,2}[:\s\-–—]+(.*?)(?=\*{0,2}פריים\s+\d+\*{0,2}[:\s\-–—]|###|##|\Z)",
        text, re.DOTALL
    )
    for m in pattern:
        num = int(m.group(1))
        content = _clean_text(m.group(2))
        if content:
            sections[num] = content
    return sections


class TennisPDF(FPDF):
    def __init__(self, pro_name: str, video_name: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.pro_name = pro_name
        self.video_name = video_name
        self.add_font("Hebrew", "", FONT_PATH)
        self.add_font("Hebrew", "B", FONT_PATH)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Hebrew", "B", 14)
        self.set_fill_color(26, 107, 60)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"🎾  ניתוח טניס — {self.pro_name}", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.set_font("Hebrew", "", 9)
        self.set_fill_color(240, 240, 240)
        date_str = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 6, f"{date_str}  |  {self.video_name}", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Hebrew", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"עמוד {self.page_no()}", align="C")

    def rtl_paragraph(self, text: str, font_size: int = 10, bold: bool = False, spacing: float = 5):
        style = "B" if bold else ""
        self.set_font("Hebrew", style, font_size)
        self.set_text_color(0, 0, 0)
        # Write lines RTL
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                self.ln(spacing * 0.5)
                continue
            self.cell(0, spacing, line, align="R", new_x="LMARGIN", new_y="NEXT")

    def section_title(self, title: str):
        self.ln(3)
        self.set_fill_color(232, 245, 238)
        self.set_font("Hebrew", "B", 11)
        self.set_text_color(26, 107, 60)
        self.cell(0, 8, title, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)


def generate_analysis_pdf(
    frames_bytes: list[bytes],
    analysis_text: str,
    pro_name: str,
    video_name: str,
) -> bytes:
    """Build PDF and return as bytes for Streamlit download."""

    clean = _clean_text(analysis_text)
    frame_sections = _parse_frame_sections(analysis_text)

    pdf = TennisPDF(pro_name=pro_name, video_name=Path(video_name).name)

    # ── Page 1: Full analysis text ─────────────────────────────────────────────
    pdf.add_page()

    # Split into sections by headings
    lines = clean.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(2)
            continue
        # Detect section headings (lines starting with digits+dot or all-caps-ish)
        if re.match(r"^(##|###|\d+\.)", stripped) or len(stripped) < 60 and stripped.endswith(":"):
            pdf.section_title(stripped.lstrip("#").strip())
        elif stripped.startswith("- ") or stripped.startswith("• "):
            pdf.set_font("Hebrew", "", 10)
            pdf.cell(0, 5, "  " + stripped, align="R", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("Hebrew", "", 10)
            pdf.cell(0, 5, stripped, align="R", new_x="LMARGIN", new_y="NEXT")

    # ── Pages 2+: Frame-by-frame with images ──────────────────────────────────
    if frames_bytes:
        pdf.add_page()
        pdf.section_title("פריים-פריים: השחקן לעומת " + pro_name)

        for i, frame_bytes in enumerate(frames_bytes, 1):
            frame_num = i
            frame_text = frame_sections.get(frame_num, "")

            # Save frame image to temp
            img = Image.open(io.BytesIO(frame_bytes))
            img_path = str(REPORTS_DIR / f"_frame_{i}.jpg")
            img.save(img_path, "JPEG", quality=85)

            # Check space — start new page if needed
            if pdf.get_y() > 220:
                pdf.add_page()

            y_start = pdf.get_y()
            page_w = pdf.w - pdf.l_margin - pdf.r_margin  # ~170mm

            img_w = 80
            img_h = 55

            # Draw frame image on LEFT side
            pdf.image(img_path, x=pdf.l_margin, y=y_start, w=img_w, h=img_h)

            # Frame label under image
            pdf.set_xy(pdf.l_margin, y_start + img_h + 1)
            pdf.set_font("Hebrew", "B", 9)
            pdf.set_text_color(26, 107, 60)
            pdf.cell(img_w, 5, f"פריים {frame_num}", align="C")

            # Analysis text on RIGHT side
            text_x = pdf.l_margin + img_w + 5
            text_w = page_w - img_w - 5
            pdf.set_xy(text_x, y_start)
            pdf.set_font("Hebrew", "", 9)
            pdf.set_text_color(0, 0, 0)

            if frame_text:
                for line in frame_text.split("\n")[:10]:  # max 10 lines per frame
                    line = line.strip()
                    if not line:
                        continue
                    pdf.set_xy(text_x, pdf.get_y())
                    pdf.cell(text_w, 5, line, align="R", new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_xy(text_x, y_start)
                pdf.cell(text_w, 5, "ראה ניתוח כללי", align="R")

            pdf.set_y(max(pdf.get_y(), y_start + img_h + 8))
            pdf.ln(3)

            # Separator
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(3)

    return bytes(pdf.output())


def generate_comparison_pdf(
    sessions: list[dict],
    analysis_text: str,
    pro_name: str,
) -> bytes:
    """Build a comparison PDF with stats table + AI analysis."""
    pdf = TennisPDF(pro_name=pro_name, video_name="השוואה בין סשנים")
    pdf.add_page()

    # ── Summary table ─────────────────────────────────────────────────────────
    pdf.section_title("השוואה בין סשנים")

    # Table headers
    headers = ["תאריך", "מכות", "IN%", "FH קמ\"ש", "BH קמ\"ש"]
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / len(headers)

    pdf.set_font("Hebrew", "B", 9)
    pdf.set_fill_color(26, 107, 60)
    pdf.set_text_color(255, 255, 255)
    for h in headers:
        pdf.cell(col_w, 7, h, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Hebrew", "", 9)
    pdf.set_text_color(0, 0, 0)
    for i, s in enumerate(sessions):
        fill = i % 2 == 0
        pdf.set_fill_color(245, 250, 246) if fill else pdf.set_fill_color(255, 255, 255)
        io = s.get("in_out", {})
        speed = s.get("speed", {})
        fh = speed.get("Forehand", {}).get("avg", "—")
        bh = speed.get("Backhand", {}).get("avg", "—")
        row = [
            s.get("session_date", "?"),
            str(s.get("total_shots", 0)),
            f"{io.get('in_pct', 0)}%",
            f"{fh}",
            f"{bh}",
        ]
        for cell in row:
            pdf.cell(col_w, 6, cell, border=1, align="C", fill=fill)
        pdf.ln()

    pdf.ln(5)

    # ── AI Analysis text ───────────────────────────────────────────────────────
    if analysis_text:
        pdf.section_title(f"ניתוח השוואתי — {pro_name}")
        clean = _clean_text(analysis_text)
        for line in clean.split("\n"):
            stripped = line.strip()
            if not stripped:
                pdf.ln(2)
                continue
            if re.match(r"^(##|###|\d+\.)", stripped) or (len(stripped) < 60 and stripped.endswith(":")):
                pdf.section_title(stripped.lstrip("#").strip())
            else:
                pdf.set_font("Hebrew", "", 10)
                pdf.cell(0, 5, stripped, align="R", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def text_to_pdf(title: str, content: str, subtitle: str = "") -> bytes:
    """Generic: any text → PDF. Used by all pages."""
    from datetime import datetime
    pdf = TennisPDF(pro_name=subtitle or title, video_name=datetime.now().strftime("%d/%m/%Y"))
    pdf.add_page()
    clean = _clean_text(content)
    for line in clean.split("\n"):
        s = line.strip()
        if not s:
            pdf.ln(2)
        elif re.match(r"^(##|###|\d+\.)", s) or (len(s) < 60 and s.endswith(":")):
            pdf.section_title(s.lstrip("#").strip())
        else:
            pdf.set_font("Hebrew", "", 10)
            pdf.cell(0, 5, s, align="R", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
