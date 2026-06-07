#!/usr/bin/env python3
"""🎾 מאמן טניס וירטואלי"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from coach.database import init_db
from coach.config import get_pro_player, get_swingvision_videos
from coach.progress_chart import plot_all_progress, plot_swingvision_speed_overview

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    RICH = True
    console = Console()
except ImportError:
    RICH = False
    console = None


def header():
    pro = get_pro_player()
    pro_line = f"\n[bold yellow]שחקן ייחוס: {pro}[/bold yellow]" if pro else \
               "\n[dim red]טרם זוהה שחקן ייחוס — בחר אפשרות 1[/dim red]"
    if RICH:
        console.print(Panel.fit(
            f"[bold green]🎾 מאמן טניס וירטואלי[/bold green]{pro_line}",
            border_style="green"
        ))
    else:
        print("\n" + "="*50)
        print("🎾 מאמן טניס וירטואלי")
        if pro:
            print(f"שחקן ייחוס: {pro}")
        print("="*50)


def menu(pro: str | None):
    options = [
        ("1", "🔍 זהה שחקן ייחוס" + (" (כבר זוהה: " + pro + ")" if pro else " ← התחל כאן!")),
        ("2", "🎬 נתח סרטון SwingVision"),
        ("3", "🖼️  נתח תמונה"),
        ("4", "📊 נתח נתוני SwingVision (CSV/JSON)"),
        ("5", "📋 בנה תכנית אימון"),
        ("6", "📈 ניתוח התקדמות"),
        ("7", "🎯 אסטרטגיית משחק"),
        ("8", "💬 שאל את המאמן"),
        ("9", "📉 הפק גרפי התקדמות"),
        ("0", "❌ יציאה"),
    ]
    if RICH:
        t = Table(show_header=False, box=None, padding=(0, 2))
        for k, label in options:
            color = "bold cyan" if k == "1" and not pro else "cyan"
            t.add_row(f"[{color}]{k}[/{color}]", label)
        console.print(t)
    else:
        for k, label in options:
            print(f"  {k}. {label}")


def ask(prompt: str, default: str = "") -> str:
    if RICH:
        return Prompt.ask(prompt, default=default) if default else Prompt.ask(prompt)
    val = input(f"{prompt}{' [' + default + ']' if default else ''}: ").strip()
    return val or default


def pick_swingvision_video() -> str | None:
    """Let user pick a SwingVision video or use latest."""
    videos = get_swingvision_videos()
    if not videos:
        print("❌ לא נמצאו סרטוני SwingVision בתיקיית 'Swing vision'")
        return None
    print("\nסרטוני SwingVision זמינים:")
    for i, v in enumerate(videos, 1):
        size_mb = v.stat().st_size / 1_000_000
        print(f"  {i}. {v.name}  ({size_mb:.0f} MB)")
    print(f"  Enter = האחרון ({videos[-1].name})")
    choice = input("בחר מספר: ").strip()
    if not choice:
        return str(videos[-1])
    try:
        idx = int(choice) - 1
        return str(videos[idx])
    except (ValueError, IndexError):
        return str(videos[-1])


def run():
    init_db()
    conversation_history: list = []

    while True:
        print()
        pro = get_pro_player()
        header()
        menu(pro)
        choice = ask("\n[bold]בחר אפשרות[/bold]" if RICH else "בחר אפשרות")

        if choice == "0":
            print("להתראות! 🎾")
            break

        elif choice == "1":
            force = False
            if pro:
                ans = ask(f"שחקן ייחוס קיים: {pro}. לזהות מחדש?", default="לא")
                force = ans.strip() in ("כן", "y", "yes", "1", "כ")
            from coach.identify_pro import identify_pro_player
            identify_pro_player(force=force)

        elif choice == "2":
            if not pro:
                print("⚠️  זהה שחקן ייחוס קודם (אפשרות 1)")
                continue
            path = pick_swingvision_video()
            if path:
                from coach.ai_coach import analyze_swingvision_video
                analyze_swingvision_video(path)

        elif choice == "3":
            path = ask("נתיב לתמונה")
            if not path or not Path(path).exists():
                print("❌ קובץ לא נמצא")
                continue
            context = ask("הקשר (רשות)")
            from coach.ai_coach import analyze_image
            analyze_image(path, context)

        elif choice == "4":
            path = ask("נתיב לקובץ SwingVision (CSV/JSON)")
            if not path or not Path(path).exists():
                print("❌ קובץ לא נמצא")
                continue
            from coach.ai_coach import analyze_swingvision_data
            analyze_swingvision_data(path)

        elif choice == "5":
            focus = ask("נושא דגש (רשות)")
            mins = ask("משך האימון בדקות", default="90")
            from coach.ai_coach import generate_training_plan
            generate_training_plan(focus, int(mins))

        elif choice == "6":
            from coach.ai_coach import analyze_progress
            analyze_progress()

        elif choice == "7":
            surface = ask("משטח (קשה/חימר/עשב)", default="קשה")
            opponent = ask("תאר את היריב (רשות)")
            from coach.ai_coach import game_strategy
            game_strategy(opponent, surface)

        elif choice == "8":
            print("(הקלד 'חזור' לחזור לתפריט)")
            from coach.ai_coach import ask_coach
            while True:
                q = ask("שאלה למאמן")
                if q.lower() in ("חזור", "back", "exit", "quit"):
                    break
                _, conversation_history = ask_coach(q, conversation_history)

        elif choice == "9":
            print("📉 מייצר גרפים...")
            paths = plot_all_progress()
            sv_chart = plot_swingvision_speed_overview()
            if sv_chart:
                paths.append(sv_chart)
            if paths:
                print(f"✅ {len(paths)} גרפים נשמרו בתיקיית charts/")
                for p in paths:
                    print(f"   {p}")
            else:
                print("⚠️  אין מספיק נתונים לגרפים עדיין")
        else:
            print("⚠️  בחירה לא תקינה")


if __name__ == "__main__":
    run()
