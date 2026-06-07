@echo off
cd /d "C:\TennisCoach"
call venv\Scripts\activate
start "" "http://localhost:8501"
streamlit run app.py --server.headless true --browser.gatherUsageStats false
pause
