"""Telegram bot — import sessions, get coaching on mobile."""
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from coach import db, swingvision, claude_client, config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

TOKEN = Path("telegram_token.txt").read_text().strip()
CHAT_ID_FILE = Path("telegram_chat_id.txt")


def _save_chat(cid: int):
    CHAT_ID_FILE.write_text(str(cid))


def _summary(s: dict) -> str:
    stats = s.get("stats", {})
    in_pct = stats.get("in_pct") or s.get("in_pct", 0)
    lines = [
        f"📅 {s['date']} | {s['shots']} מכות | {s['rallies']} ראלים",
        f"✅ IN: {in_pct}%",
    ]
    for stroke, d in stats.get("strokes", {}).items():
        lines.append(f"  {stroke}: {d['avg_speed']} קמ\"ש")
    return "\n".join(lines)


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    _save_chat(update.effective_chat.id)
    ntrp = config.get_ntrp()
    await update.message.reply_text(
        f"🎾 *Virtual Tennis Coach*\n"
        f"NTRP: {ntrp or 'לא הוגדר'}\n\n"
        f"שלח לינק SwingVision לניתוח מיידי\n"
        f"swing\\.vision/matches/\\.\\.\\.\n\n"
        f"/plan — תכנית אימון\n/history — 5 סשנים אחרונים",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def cmd_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sessions = db.get_sessions(limit=5)
    if not sessions:
        await update.message.reply_text("אין סשנים עדיין")
        return
    text = "📁 *5 סשנים אחרונים:*\n\n" + "\n\n".join(_summary(s) for s in sessions)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)


async def cmd_plan(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ בונה תכנית...")
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    sessions  = db.get_sessions(limit=1)
    stats_text = _summary(sessions[0]) if sessions else "אין נתונים"
    result = []
    for chunk in claude_client.training_plan(stats_text, "", 60, ntrp_cur, ntrp_next):
        result.append(chunk)
    text = "".join(result)
    try:
        await msg.edit_text(f"📋 *תכנית אימון:*\n\n{text}", parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        await msg.edit_text(f"📋 תכנית אימון:\n\n{text}")


async def handle_link(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    mid  = swingvision.extract_match_id(text)
    if not mid:
        await update.message.reply_text(
            "שלח לינק SwingVision:\n`https://swing.vision/matches/...`",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    if db.session_exists(mid):
        s = db.get_session(mid)
        await update.message.reply_text(f"✅ כבר קיים:\n{_summary(s)}")
        return

    msg = await update.message.reply_text("⏳ מייבא...")
    try:
        s = swingvision.parse_session(mid)
        db.save_session(s["match_id"], s["date"], s["shots"],
                        s["rallies"], s, s.get("video_url"))
        await msg.edit_text(f"🎾 *נוסף\\!*\n\n{_summary(db.get_session(mid))}",
                            parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        await msg.edit_text(f"❌ שגיאה: {e}")


def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .build()
    )
    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("history", cmd_history))
    app.add_handler(CommandHandler("plan",    cmd_plan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("🎾 Bot running...")
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
