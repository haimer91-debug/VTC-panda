"""
Analyze SwingVision videos → identify closest ATP/WTA pro player.
Runs once, saves result to player_config.json.
"""
from pathlib import Path

import anthropic

from coach.video_analyzer import extract_frames, frames_to_base64
from coach.config import set_pro_player, get_swingvision_videos, get_pro_player

MODEL = "claude-opus-4-7"

def _get_api_key():
    key_file = Path(__file__).parent.parent / "api_key.txt"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    return None

SYSTEM_PROMPT = """אתה מומחה בזיהוי דמיון בין שחקני טניס חובבים לשחקני עילית ATP/WTA.
אתה מכיר לעומק את הטכניקה, הביומכניקה וסגנון המשחק של כל שחקן מקצועי מובהק.
ענה בעברית."""


def _sample_videos(videos: list[Path]) -> list[Path]:
    """Pick the most recently modified video only."""
    sorted_by_time = sorted(videos, key=lambda v: v.stat().st_mtime, reverse=True)
    return sorted_by_time[:1]


def identify_pro_player(force: bool = False) -> str:
    existing = get_pro_player()
    if existing and not force:
        print(f"\n✅ שחקן ייחוס קיים: {existing}")
        return existing

    videos = get_swingvision_videos()
    if not videos:
        print("❌ לא נמצאו סרטוני SwingVision")
        return ""

    sample = _sample_videos(videos)
    print(f"\n🎬 מנתח {len(sample)} סרטונים לזיהוי סגנון:")
    for v in sample:
        print(f"   {v.name}")

    api_key = _get_api_key()
    client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
    content: list = []

    for i, video_path in enumerate(sample, 1):
        print(f"\n   מחלץ פריימים מ-{video_path.name}...")
        try:
            frames = extract_frames(str(video_path), max_frames=4)
            b64_frames = frames_to_base64(frames)
            content.append({"type": "text", "text": f"\n**סרטון {i}: {video_path.name}**"})
            for b64 in b64_frames:
                content.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}
                })
        except Exception as e:
            print(f"   ⚠️  שגיאה: {e}")

    if not any(b.get("type") == "image" for b in content):
        print("❌ לא הצלחתי לחלץ פריימים")
        return ""

    content.append({"type": "text", "text": """
צפית בסרטונים של שחקן טניס. זהה לאיזה שחקן ATP/WTA הוא הכי קרוב בסגנון.

⚠️ חשוב מאוד: קבע תחילה האם הבקהנד הוא יד אחת או שתי ידיים — ובחר שחקן ייחוס עם אותו סגנון בקהנד בלבד. אין להשוות שחקן בקהנד שתי ידיים לשחקן בקהנד יד אחת.

נתח:
1. **בקהנד** — יד אחת או שתיים? זוויות, תנועה, סיבוב (זה הקריטריון הראשון לבחירת הפרו)
2. **פורהנד** — אחיזה, סיבוב הגוף, נקודת מגע, follow-through, ספין/פלאט
3. **תנועה ורגליים** — סגנון ריצה, split step, פוזיציה
4. **מבנה גוף ואנרגיה** — כיצד משפיע על הסגנון
5. **מנטליות** — אגרסיבי / counter-puncher / all-court
6. **הגשה** (אם נראית)

## פלט נדרש (עקוב בדיוק):

**סגנון בקהנד:** [יד אחת / שתי ידיים]

**שחקן ייחוס:** [שם מלא — חייב להיות עם אותו סגנון בקהנד]
**התאמה:** [X%]

**למה דווקא הוא:**
- בקהנד: [השוואה ספציפית]
- פורהנד: [השוואה ספציפית]
- תנועה: [השוואה ספציפית]
- סגנון כללי: [השוואה ספציפית]

**שחקן ייחוס משני:** [שם עם אותו סגנון בקהנד] — [הסבר קצר]

**3 דברים ללמוד:**
1.
2.
3.
"""})

    messages = [{"role": "user", "content": content}]

    print("\n🧠 Claude מנתח ומחפש את הפרו המתאים...\n")
    full_text = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text.append(text)
    print()

    response = "".join(full_text)
    pro_name = _extract_pro_name(response)

    if pro_name:
        set_pro_player(pro_name, response)
        print(f"\n✅ שחקן הייחוס שלך: {pro_name}")
        print("   כל הניתוחים הבאים ישוו אליו.")
    else:
        print("\n⚠️  לא הצלחתי לזהות שם אוטומטית.")
        manual = input("הכנס ידנית את שם שחקן הייחוס: ").strip()
        if manual:
            set_pro_player(manual, response)
            pro_name = manual

    return pro_name


def _extract_pro_name(text: str) -> str:
    import re
    # Hebrew label
    m = re.search(r"שחקן ייחוס[:\*\*\s]+([A-Za-zא-ת][^\n\*]{2,40})", text)
    if m:
        return m.group(1).strip().strip("*").strip()
    # Bold English name
    m = re.search(r"\*\*([A-Z][a-z]+ [A-Z][a-z]+)\*\*", text)
    if m:
        return m.group(1).strip()
    return ""
