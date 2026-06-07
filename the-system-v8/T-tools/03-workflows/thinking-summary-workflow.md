# Thinking Workflow: Document Summary

> Adam (COO) orchestrates the Analyst, Copywriter, and Gatekeeper to turn raw material into clear, structured summaries.

---

## Process Overview

```
[You] provide the raw material (transcript, notes, document)
          ↓
[Adam] reads C-core, assigns the team, manages the workflow
          ↓
[Analyst] extracts key information and structures it
          ↓
[Copywriter] polishes the language in your voice
          ↓
[Gatekeeper] reviews for quality and completeness
          ↓
[Adam] delivers final summary and updates memory
```

---

## Step 1: Preparation

### Adam Reads Context

Before starting, Adam reads:
- `C-core/project-brief.md` - Who you are and what you do
- `C-core/voice-dna.md` - How the brand communicates
- `M-memory/learning-log.md` - What we learned from previous rounds

### Adam Creates Project Folder

```
O-output/
└── summary-[topic]/
    ├── final-summary.md            ← THE DELIVERABLE (copy-paste ready)
    └── _process/
        ├── analyst-extraction.md     ← Structured extraction
        ├── copywriter-draft.md       ← Polished version
        └── gatekeeper-review.md      ← Quality review
```

---

## Step 2: Analyst Extracts and Structures

### What the Analyst Does

1. **Reads the raw material** — Transcript, notes, or document
2. **Reads `A-agents/analyst-agent.md`** — Understands the role
3. **Reads the relevant skill:**
   - Meeting → `T-tools/01-skills/meeting-notes-skill/`
   - Document → `T-tools/01-skills/document-summary-skill/`
   - PRD → `T-tools/01-skills/prd-skill/`
   - Stakeholder update → `T-tools/01-skills/stakeholder-update-skill/`
4. **Extracts key information** — Facts, decisions, actions, quotes
5. **Structures the output** — Using the appropriate template

### Extraction Principles
- **Keep:** Decisions, action items, key quotes, data points
- **Compress:** Repetitive discussion, general context
- **Skip:** Small talk, tangential topics, repeated information

### Deliverable: `_process/analyst-extraction.md`

```markdown
# Analysis: [Topic/Meeting/Document]

**Source:** [What was analyzed]
**Date:** [Date]

---

## TL;DR
[2-3 sentences capturing the essence]

---

## Key Points
1. [Most important finding/point]
2. [Second most important]
3. [Third most important]

---

## Decisions Made
- [Decision]: [Context and reasoning]

---

## Action Items
| Who | What | By When |
|-----|------|---------|
| [Name] | [Action] | [Date] |

---

## Key Quotes
> "[Exact quote that captures something important]"

---

## Open Questions
- [What wasn't resolved]

---

## Analyst Notes
- [Patterns noticed]
- [Connections to previous work]
- [Recommendations for follow-up]
```

---

## Step 3: Copywriter Polishes

### What the Copywriter Does

1. **Reads the Analyst's extraction** — Understands the structure and content
2. **Reads C-core voice DNA** — Applies your communication style
3. **Polishes the language** — Makes it read naturally, in your voice
4. **Does NOT change the structure** — The Analyst's organization stays, the words get refined

### Focus Areas
- TL;DR reads like a human wrote it
- Key points are crisp and clear
- Action items are specific and actionable
- The whole thing flows when read top-to-bottom

---

## Step 4: Gatekeeper Reviews

### What the Gatekeeper Does

1. **Completeness** — Is anything important from the source material missing?
2. **Accuracy** — Are facts, names, numbers correct?
3. **Usability** — Can someone act on this without reading the source?
4. **Voice** — Does it sound like the user?
5. **Decision** — Approved / Revisions Needed

---

## Step 5: Adam Delivers

1. **Saves final version** to `final-summary.md` (at the project folder root — NOT inside `_process/`)
2. **Presents to user** with TL;DR highlighted
3. **Updates memory:**
   - `M-memory/learning-log.md` with summary insights
   - `M-memory/decisions.md` if decisions were captured

---

## Summary Types Reference

| Type | Skill to Use | Key Focus |
|------|-------------|-----------|
| Meeting summary | meeting-notes-skill | Decisions, actions, owners |
| User interview | document-summary-skill | Quotes, pain points, workarounds |
| Research doc | document-summary-skill | Findings, implications, actions |
| PRD | prd-skill | Requirements, scope, success metrics |
| Stakeholder update | stakeholder-update-skill | Status, risks, asks |

---

## Quick Checklist

- [ ] Adam read C-core context
- [ ] Analyst extracted key information
- [ ] Structure follows the appropriate skill template
- [ ] Copywriter polished in user's voice
- [ ] Gatekeeper verified completeness and accuracy
- [ ] TL;DR captures the essence
- [ ] Action items have owners and deadlines
- [ ] Final version is saved and ready

---

*Raw material in, clear thinking out. The Analyst structures, the Copywriter refines, the Gatekeeper verifies.*

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
