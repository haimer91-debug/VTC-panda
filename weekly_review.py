"""Weekly review — runs every Sunday, sends to Telegram."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from coach import db, config
from coach.claude_client import weekly_review
from pages.stats import _in_pct


def _week_stats() -> str:
    sessions = db.get_sessions(limit=10)
    lines = []
    for s in sessions[:7]:  # last 7 sessions
        stats = s.get("stats", {})
        fh = stats.get("strokes", {}).get("Forehand", {}).get("avg_speed",
             stats.get("speed", {}).get("Forehand", {}).get("avg", 0))
        bh = stats.get("strokes", {}).get("Backhand", {}).get("avg_speed",
             stats.get("speed", {}).get("Backhand", {}).get("avg", 0))
        lines.append(f"{s['date']}: {s['shots']} מכות | IN {_in_pct(s)}% | FH {fh} | BH {bh}")
    return "\n".join(lines)


def _send_telegram(msg: str):
    import requests
    token = Path("telegram_token.txt").read_text().strip()
    chat_id_f = Path("telegram_chat_id.txt")
    if not chat_id_f.exists():
        return
    chat_id = chat_id_f.read_text().strip()
    # Split long messages
    for i in range(0, len(msg), 4000):
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": msg[i:i+4000]},
            timeout=10
        )


def main():
    print("Running weekly review...")
    ntrp_cur  = config.get_ntrp() or "3.5"
    ntrp_next = config.get_ntrp_next()
    stats_text = _week_stats()

    if not stats_text.strip():
        print("No sessions this week")
        return

    review = weekly_review(stats_text, ntrp_cur, ntrp_next)

    # Save to memory
    from pages.loop import log_learning
    from datetime import datetime
    from pathlib import Path as P
    mem = P("memory/learning-log.md")
    entry = f"\n### {datetime.now().strftime('%Y-%m-%d')} | סקירה שבועית\n{review[:500]}\n"
    mem.write_text(mem.read_text(encoding="utf-8") + entry, encoding="utf-8")

    # Send to Telegram
    header = f"📊 *סקירה שבועית — {datetime.now().strftime('%d/%m/%Y')}*\n\n"
    _send_telegram(header + review)
    print("Sent to Telegram")


if __name__ == "__main__":
    main()
