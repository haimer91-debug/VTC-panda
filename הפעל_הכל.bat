@echo off
cd /d "C:\TennisCoach"
call venv\Scripts\activate

echo עוצר תהליכים קיימים...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo מפעיל Streamlit...
start "" "venv\Scripts\python.exe" -m streamlit run app.py --server.headless true --browser.gatherUsageStats false

timeout /t 3 /nobreak >nul

echo מפעיל בוט טלגרם...
start "" "venv\Scripts\python.exe" telegram_bot.py

timeout /t 3 /nobreak >nul

echo פותח דפדפן...
start "" "http://localhost:8501"

echo.
echo ✅ הכל פועל!
echo    אפליקציה: http://localhost:8501
echo    בוט טלגרם: @VirtualTenniscoach_bot
echo.
pause
