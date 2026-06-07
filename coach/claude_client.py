"""Single Claude client. All prompts live here. Never crashes — returns error string on failure."""
from __future__ import annotations
from pathlib import Path
from typing import Generator
from functools import lru_cache

import anthropic

_client: anthropic.Anthropic | None = None
_MEMORY = Path(__file__).parent.parent / "memory"


@lru_cache(maxsize=8)
def _read_memory(filename: str) -> str:
    """Read a memory file (cached per session)."""
    f = _MEMORY / filename
    return f.read_text(encoding="utf-8") if f.exists() else ""


def _memory_context() -> str:
    """Inject relevant memory into every system prompt."""
    decisions = _read_memory("decisions.md")
    log       = _read_memory("learning-log.md")
    parts = []
    if decisions:
        parts.append(f"## החלטות קבועות (אל תחזור עליהן)\n{decisions[:800]}")
    if log:
        parts.append(f"## דפוסים שנמצאו\n{log[:600]}")
    return "\n\n".join(parts)


# Model tiers — Haiku for simple tasks, Opus only when needed
MODEL_FAST  = "claude-haiku-4-5"   # $1/M tokens — chat, stats summary
MODEL_SMART = "claude-opus-4-7"    # $25/M tokens — video analysis, training plan


def _get() -> anthropic.Anthropic:
    global _client
    if _client is None:
        kf = Path(__file__).parent.parent / "api_key.txt"
        ak = kf.read_text(encoding="utf-8").strip() if kf.exists() else None
        _client = anthropic.Anthropic(api_key=ak) if ak else anthropic.Anthropic()
    return _client


def stream(prompt: str, system: str, max_tokens: int = 3000,
           fast: bool = False) -> Generator[str, None, None]:
    """Stream text tokens. fast=True uses Haiku (~25x cheaper)."""
    model = MODEL_FAST if fast else MODEL_SMART
    try:
        kw = {"thinking": {"type": "adaptive"}} if not fast else {}
        with _get().messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kw,
        ) as s:
            yield from s.text_stream
    except Exception as e:
        yield f"\n⚠️ שגיאה: {e}"


def stream_messages(messages: list[dict], system: str, max_tokens: int = 2000,
                    fast: bool = False) -> Generator[str, None, None]:
    """Stream for multi-turn chat."""
    model = MODEL_FAST if fast else MODEL_SMART
    kw = {"thinking": {"type": "adaptive"}} if not fast else {}
    try:
        with _get().messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            **kw,
        ) as s:
            yield from s.text_stream
    except Exception as e:
        yield f"\n⚠️ שגיאה: {e}"


# ── System prompts ────────────────────────────────────────────────────────────

def _coach_system(ntrp_cur: str, ntrp_next: str) -> str:
    mem = _memory_context()
    base = (
        f"אתה מאמן טניס אישי של Haim Ezra. רמה: NTRP {ntrp_cur} → {ntrp_next}.\n"
        f"כל המלצה מגובה במספרים ספציפיים. ענה בעברית, קצר וישיר."
    )
    return f"{base}\n\n{mem}" if mem else base


# ── Prompt functions ──────────────────────────────────────────────────────────

def analyze_video(frames_b64: list[str], session_context: str,
                  ntrp_cur: str, ntrp_next: str) -> Generator[str, None, None]:
    content: list = []
    for i, b64 in enumerate(frames_b64):
        content.append({"type": "text", "text": f"פריים {i+1}:"})
        content.append({"type": "image", "source": {"type": "base64",
                        "media_type": "image/jpeg", "data": b64}})
    content.append({"type": "text", "text": f"""נתח כל פריים.{session_context}

עבור כל פריים:
**פריים [N]:** מה השחקן עושה | מה לשפר לרמת NTRP {ntrp_next} | פעולה אחת

לאחר הפריימים:
### 3 בעיות מרכזיות לקידום מ-{ntrp_cur} ל-{ntrp_next}
### שיעורי בית לאימון הבא

ענה בעברית."""})
    yield from stream_messages(
        [{"role": "user", "content": content}],
        system=_coach_system(ntrp_cur, ntrp_next),
        max_tokens=4096
    )


def analyze_stats(stats_text: str, ntrp_cur: str, ntrp_next: str) -> Generator[str, None, None]:
    yield from stream(
        f"""נתוני SwingVision — רמה {ntrp_cur} → {ntrp_next}:

{stats_text}

## ממצאים עיקריים מהמספרים
## פערים מרמת {ntrp_next} (עם נתונים)
## 3 יעדים מדידים לסשן הבא

ענה בעברית.""",
        system=_coach_system(ntrp_cur, ntrp_next)
    )


def training_plan(recent_stats: str, focus: str, duration: int,
                  ntrp_cur: str, ntrp_next: str) -> Generator[str, None, None]:
    yield from stream(
        f"""בנה תכנית אימון של {duration} דקות.
{'נושא דגש: ' + focus if focus else ''}

נתוני סשן אחרון:
{recent_stats}

## חימום ({max(10, duration//8)} דק') — ממוקד בחולשות מהנתונים
## טכניקה ({duration//3} דק') — 3 תרגילים לפערים בין {ntrp_cur} ל-{ntrp_next}
## טקטיקה ({duration//3} דק') — patterns של שחקן {ntrp_next}
## סיום ({max(5, duration//12)} דק')
## 3 KPIs למדידה ב-SwingVision

ענה בעברית.""",
        system=_coach_system(ntrp_cur, ntrp_next)
    )


def strategy(my_stats: str, opponent_data: str, surface: str,
             fmt: str, ntrp_cur: str) -> Generator[str, None, None]:
    yield from stream(
        f"""בנה אסטרטגיית משחק.
שחקן: NTRP {ntrp_cur} | משטח: {surface} | {fmt}

{opponent_data}

נתוני שחקן:
{my_stats}

## ניתוח היריב — חוזקות/חולשות מהדאטא
## Pattern of Play מומלץ (הגשה, ראלי ראשון, סיום)
## ניהול מצבים קריטיים (Break/Deuce)
## 3 משפטי focus לשינוי צדדים

ענה בעברית. ספציפי ומעשי.""",
        system=f"מאמן טניס. ענה בעברית. ספציפי."
    )


def chat(messages: list[dict], player_summary: str,
         ntrp_cur: str, ntrp_next: str) -> Generator[str, None, None]:
    system = f"""{_coach_system(ntrp_cur, ntrp_next)}

פרופיל שחקן:
{player_summary}

כללים: ענה על בסיס הנתונים הספציפיים. אל תשאל שאלות כלליות."""
    yield from stream_messages(messages, system=system, fast=True)  # Haiku — 25x cheaper


# ── Multi-agent pipeline ───────────────────────────────────────────────────────

def _call(prompt: str, system: str, max_tokens: int = 1500) -> str:
    """Single synchronous call — for chaining agents."""
    try:
        with _get().messages.stream(
            model="claude-opus-4-7",
            max_tokens=max_tokens,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": prompt}],
        ) as s:
            return "".join(s.text_stream)
    except Exception as e:
        return f"⚠️ {e}"


def _gatekeeper(content: str, criteria: str) -> str:
    """Quality check: returns APPROVED or REVISION: <reason>."""
    result = _call(
        f"בדוק את הפלט הבא לפי הקריטריונים:\n{criteria}\n\nפלט:\n{content}\n\n"
        "ענה: APPROVED או REVISION: [סיבה קצרה]",
        system="אתה Gatekeeper. תפקידך: לאשר רק פלט שעומד בקריטריונים. שמור על קצר.",
        max_tokens=200
    )
    return result.strip()


def training_plan_pipeline(recent_stats: str, focus: str, duration: int,
                           ntrp_cur: str, ntrp_next: str) -> Generator[str, None, None]:
    """Analyst → Coach → Devil's Advocate → Chief of Staff → Gatekeeper → stream."""
    mem = _memory_context()

    yield "🔍 **Analyst** — מנתח נתונים...\n"
    analyst_out = _call(
        f"נתוני שחקן:\n{recent_stats}\n\nחלץ: 3 חולשות עיקריות + 2 חוזקות. מספרים בלבד, ללא המלצות.",
        system=f"אתה Analyst. עובדות ומספרים בלבד. {mem}", max_tokens=600
    )

    yield f"\n📋 **Coach** — בונה תכנית...\n"
    coach_out = _call(
        f"על בסיס הניתוח:\n{analyst_out}\n\nבנה תכנית {duration} דק' ל-NTRP {ntrp_cur}→{ntrp_next}."
        + (f"\nדגש: {focus}" if focus else "")
        + "\n\nחימום | טכניקה | טקטיקה | KPIs",
        system=_coach_system(ntrp_cur, ntrp_next), max_tokens=1200
    )

    yield f"\n😈 **Devil's Advocate** — מאתגר...\n"
    devil_out = _call(
        f"תכנית:\n{coach_out}\n\nמצא: 2 הנחות שגויות + תנאי הצלחה שחסרים. קצר.",
        system=f"אתה Devil's Advocate. מצא חורים בתכנית. {mem}", max_tokens=400
    )

    yield f"\n👔 **Chief of Staff** — מסכם...\n"
    final = _call(
        f"תכנית:\n{coach_out}\n\nאתגרים:\n{devil_out}\n\n"
        "כתוב גרסה סופית משופרת שמתייחסת לאתגרים. זו הגרסה שהשחקן יראה.",
        system=_coach_system(ntrp_cur, ntrp_next), max_tokens=1500
    )

    # Gatekeeper check
    gate = _gatekeeper(final, "כל תרגיל כולל KPI מדיד | אין המלצות שסותרות decisions.md | ספציפי לנתונים")
    if gate.startswith("REVISION"):
        yield f"\n⚠️ Gatekeeper: {gate}\n\n"

    yield "\n---\n" + final


def weekly_review(sessions_text: str, ntrp_cur: str, ntrp_next: str) -> str:
    """Full weekly review — returns text for Telegram + memory update."""
    mem = _memory_context()
    review = _call(
        f"""סקירה שבועית — NTRP {ntrp_cur} → {ntrp_next}

{sessions_text}

## התקדמות השבוע (עם מספרים)
## 3 נקודות שהשתפרו
## 3 נקודות לעבוד עליהן
## מוקד לשבוע הבא (דבר אחד בלבד)
## KPI שצריך לשפר עד השבוע הבא

קצר. מספרים. ענה בעברית.""",
        system=f"מאמן טניס. {mem}", max_tokens=1000
    )
    return review
