# Virtual Tennis Coach — Session Context

## Player
- **Name:** Haim Ezra (Panda)
- **NTRP:** read from `player_config.json` → `ntrp_level`
- **Target:** NTRP next level (`get_ntrp_next()`)
- **Style ref:** João Fonseca — two-handed backhand ONLY

## Project Location
`C:\TennisCoach`

## Architecture
```
app.py              → Streamlit routing
pages/
  videos.py         → sessions, notes, video analysis
  stats.py          → SwingVision stats + 7 charts + level assessment
  coaching.py       → training plan (multi-agent) + strategy
  chat.py           → coach chat with video access
  loop.py           → close-the-loop widget
coach/
  db.py             → SQLite (sessions table + analyses cache)
  swingvision.py    → SwingVision API (creds: swingvision_creds.txt)
  claude_client.py  → all Claude calls + multi-agent pipeline
  config.py         → player_config.json R/W
telegram_bot.py     → @VirtualTenniscoach_bot
weekly_review.py    → Sunday 9:00 auto-review → Telegram
memory/
  decisions.md      → locked coaching decisions
  learning-log.md   → patterns discovered
  feedback.md       → player reactions
  agents.md         → agent role definitions
```

## Key Rules (from memory/decisions.md)
- Compare player to NTRP next level — NEVER to pro player
- João Fonseca = style inspiration only, not benchmark
- Two-handed backhand — never compare to one-handed BH players
- All AI analyses cached in DB — never regenerate without explicit request

## Running
- App: `python -m streamlit run app.py` → http://localhost:8501
- Bot: `python telegram_bot.py`
- Both: `הפעל_הכל.bat`

## Data
- 19+ sessions in `coach.db` (Apr–Jun 2026)
- Import: SwingVision share links only (`swing.vision/matches/...`)
- Stats format: `strokes[stroke]{avg_speed, in_pct}`, `spin[stroke]{topspin%}`, `in_out{in_pct}`
- Old format also has: `speed[stroke]{avg}`, `in_out{in_pct}`

## Known Patterns (from memory/learning-log.md)
- BH topspin inconsistent (13–75% across sessions) — always include BH drill
- IN% drops under competitive pressure — add pressure drills
- FH ~5 km/h faster than BH consistently

## Start Every Session
1. Read `memory/decisions.md` — what NOT to do
2. Read `memory/learning-log.md` — what works
3. Check `player_config.json` for current NTRP
