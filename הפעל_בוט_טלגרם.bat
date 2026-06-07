@echo off
cd /d "C:\TennisCoach"
call venv\Scripts\activate
echo 🎾 מפעיל בוט טלגרם...
python telegram_bot.py
pause
