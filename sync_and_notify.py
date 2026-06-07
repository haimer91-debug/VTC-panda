"""
Daily sync script — runs at 10:00 and 11:00.
Checks SwingVision for new sessions + new videos, sends Telegram notification.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import requests
import sqlite3
import json
from datetime import datetime, date

TOKEN_FILE = Path(__file__).parent / "telegram_token.txt"
CHAT_ID_FILE = Path(__file__).parent / "telegram_chat_id.txt"
DB_PATH = Path(__file__).parent / "coach.db"
SV_DIR = Path(r"G:\האחסון שלי\טניס\מאמן וירטואלי\Swing vision")


def _send(msg: str):
    if not TOKEN_FILE.exists() or not CHAT_ID_FILE.exists():
        return
    token = TOKEN_FILE.read_text().strip()
    chat_id = CHAT_ID_FILE.read_text().strip()
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"},
        timeout=10
    )


def _get_saved_ids() -> set:
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("SELECT file_path FROM swingvision_sessions").fetchall()
        conn.close()
        return {r[0] for r in rows}
    except Exception:
        return set()


def sync_sessions() -> list[str]:
    """Pull new sessions from SwingVision API."""
    try:
        from coach.swingvision_sync import sync_new_sessions
        return sync_new_sessions()
    except Exception as e:
        print(f"Session sync error: {e}")
        return []


def check_new_videos() -> list[str]:
    """Check for new MP4 files added today."""
    if not SV_DIR.exists():
        return []
    today = date.today()
    new_vids = []
    for f in SV_DIR.iterdir():
        if f.suffix.lower() in {".mp4", ".mov", ".avi", ".mkv"}:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).date()
            if mtime == today:
                new_vids.append(f.name)
    return new_vids


def main():
    print(f"[{datetime.now().strftime('%H:%M')}] Starting sync...")
    new_sessions = sync_sessions()
    new_videos = check_new_videos()

    if not new_sessions and not new_videos:
        print("Nothing new.")
        return

    # Build Telegram message
    lines = [f"🎾 *עדכון SwingVision — {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n"]

    if new_sessions:
        lines.append(f"✅ *{len(new_sessions)} סשנים חדשים נמצאו:*")
        try:
            from coach.swingvision_excel_parser import load_all_sessions
            all_s = load_all_sessions()
            for sid in new_sessions[:3]:
                s = next((x for x in all_s if sid in x.get("file", "")), None)
                if s:
                    io = s.get("in_out", {})
                    spd = s.get("speed", {})
                    fh = spd.get("Forehand", {}).get("avg", "—")
                    lines.append(
                        f"  📅 {s.get('session_date','?')} | "
                        f"{s.get('total_shots',0)} מכות | "
                        f"IN {io.get('in_pct',0)}% | "
                        f"FH {fh} קמ\"ש"
                    )
        except Exception:
            pass

    if new_videos:
        lines.append(f"\n🎬 *{len(new_videos)} סרטונים חדשים בתיקייה:*")
        for v in new_videos[:3]:
            lines.append(f"  • {v}")
        lines.append("\n➡️ פתח את האפליקציה לניתוח: http://localhost:8501")

    msg = "\n".join(lines)
    _send(msg)
    print(f"Notified: {len(new_sessions)} sessions, {len(new_videos)} videos")


if __name__ == "__main__":
    main()
