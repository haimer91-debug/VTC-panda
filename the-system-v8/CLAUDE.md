# AI Agent Team - Project Instructions (v8)

## Session Start Protocol (MANDATORY)

When starting ANY new conversation from this folder, ALWAYS read these files first before responding:

### 1. Core Files (C-core/)
- `C-core/project-brief.md` (What you do and who you serve)
- `C-core/voice-dna.md` (How you communicate)
- `C-core/icp-profile.md` (Who your audience is)

### 2. Memory Files (M-memory/)
- `M-memory/learning-log.md` (What we've learned together)
- `M-memory/feedback.md` (Audience reactions and signals)
- `M-memory/decisions.md` (Strategic choices made)

### 3. Agent Definitions (A-agents/)
- `A-agents/adam-agent.md` (Your COO - manages the team and workflows)
- `A-agents/copywriter-agent.md` (Content creation agent)
- `A-agents/gatekeeper-agent.md` (Quality review agent)
- `A-agents/researcher-agent.md` (Research and web intelligence agent)
- `A-agents/analyst-agent.md` (Turns raw material into structured documents)
- `A-agents/strategist-agent.md` (Strategic analysis from business/growth perspective)
- `A-agents/devils-advocate-agent.md` (Challenges assumptions and finds blind spots)
- `A-agents/chief-of-staff-agent.md` (Synthesizes multiple perspectives into decision briefs)
- `A-agents/tom-agent.md` (Your guide to the ABC-TOM system)

---

## How This Works

Claude Code automatically reads this file when you open a conversation from this folder.

The files above are your "memory". They persist between sessions. When you update them, future sessions will have that context.

**IMPORTANT:** Actually read these files before responding. Don't just acknowledge them. Scan C-core to understand the brand, check what's in A-agents, and review M-memory for context. This makes your responses relevant to THIS user's system.

---

## The 3 Workshop Tracks

| Track | Folder | What It Creates | Agents Involved |
|-------|--------|----------------|-----------------|
| **Content** | `T-tools/02-prompts/content/` | Social posts, blog posts, newsletters | Adam → Researcher → Copywriter → Gatekeeper |
| **Sales** | `T-tools/02-prompts/sales/` | Client proposals, offers, sales emails | Adam → Strategist → Copywriter → Gatekeeper |
| **Thinking** | `T-tools/02-prompts/thinking/` | Decision briefs, summaries, PRDs | Adam → Strategist/Analyst → (team) → Gatekeeper |

---

## The ABC-TOM Loop (v8)

After completing significant work, close The Loop:

1. **New insight about what works?** Update `M-memory/learning-log.md`
2. **Received feedback?** Update `M-memory/feedback.md`
3. **Made a strategic decision?** Update `M-memory/decisions.md`
4. **Pattern strong enough to become a rule?** Promote it to `C-core/voice-dna.md`
5. **Research worth keeping?** Move it from `B-brain/04-INBOX/` to the right subfolder

The Loop is what makes the system compound. Every project that closes The Loop makes the next project better.

Run `04-close-the-loop.md` from your track folder to close The Loop explicitly.

---

## Quick Commands

- "כתוב פוסט על [נושא]" - Creates content using your voice
- "תכתוב הצעה ל[לקוח]" - Creates a client proposal
- "תסכם את [הישיבה/הראיון]" - Creates a structured summary
- "תבדוק את האיכות" - Runs gatekeeper review
- "מה למדנו?" - Shows learning log summary
- "סגור את הלופ" - Runs The Loop (updates memory + promotes insights)
- `/tom [question]` - Get help from Tom on the ABC-TOM system
- `/adam [what you want to build]` - Your COO helps you build agents, skills, connect tools

---

## Need Help?

**Want to understand the system?** Type `/tom` and ask.
Tom explains how ABC-TOM works, what each folder does, and answers questions about the framework.

**Want to build something?** Type `/adam` and tell him what you need.
Adam manages the team, creates agents, builds skills, connects external tools, organizes your system, and sets up workflows.

Both work in Hebrew and English.

---

> **© Tom Even**
> Workshops: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
