# ABC-TOM System — Project Template
> Copy this folder to any new project. Fill in the blanks. Done.

---

## Step 1 — Fill CLAUDE.md (session context)

Edit `CLAUDE.md` with your project details. Claude reads this automatically at session start.

---

## Step 2 — Fill memory/decisions.md

Add rules that should NEVER change:
```
### DATE | DECISION
**Rationale:** why
**Trigger:** what caused this decision
```

## Step 3 — Fill memory/agents.md

Define your team (copy relevant agents from the list below):

| Agent | Use when |
|---|---|
| Analyst | Raw data → structured insights (numbers only) |
| Builder/Coach | Create output based on analysis |
| Strategist | Options with tradeoffs → recommendation |
| Devil's Advocate | Challenge assumptions before shipping |
| Chief of Staff | Synthesize multiple agents → one decision |
| Gatekeeper | Quality check before showing to user |

## Step 4 — Close the Loop after every session

After each work session, log to memory/:
- What pattern emerged → `learning-log.md`
- What decision was made → `decisions.md`  
- What feedback received → `feedback.md`

When a pattern appears 3+ times → promote to core rules in CLAUDE.md.

---

## The Compound Effect

Week 1: Claude starts fresh each session.  
Week 4: Claude knows your patterns, avoids past mistakes.  
Week 10: Claude anticipates what you need.
