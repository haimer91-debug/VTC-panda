Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

base = "C:\TennisCoach"
py   = base & "\venv\Scripts\python.exe"

' Kill existing
sh.Run "taskkill /F /IM python.exe /T", 0, True
WScript.Sleep 1500

' Start Streamlit (hidden)
sh.Run """" & py & """ -m streamlit run """ & base & "\app.py"" --server.headless true --browser.gatherUsageStats false", 0, False

WScript.Sleep 3000

' Start Telegram bot (hidden)
sh.Run """" & py & """ """ & base & "\telegram_bot.py""", 0, False

WScript.Sleep 3000

' Open browser
sh.Run "http://localhost:8501", 1, False
