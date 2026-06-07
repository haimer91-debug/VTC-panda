---
name: meeting-notes-skill
description: Capture and structure meeting notes that drive action. Use this when taking notes during or after meetings, calls, or working sessions. Produces notes that focus on decisions and next steps, not play-by-play transcripts.
---

# Meeting Notes Skill

Turn meetings into decisions and actions. Not transcripts.

## When to Use

- Taking notes during or after meetings
- Processing meeting recordings
- Creating follow-up summaries for stakeholders
- Capturing decisions from ad-hoc conversations

---

## Meeting Notes Fundamentals

**What makes meeting notes useful:**
- Decisions are captured with reasoning
- Every action item has an owner and deadline
- Context is enough to understand without attending
- They're short enough that people actually read them

**The golden rule:** Nobody wants to read what happened minute-by-minute. They want to know: What was decided? What do I need to do? What's still open?

---

## The Meeting Notes Template

```markdown
# [Meeting Name]: [Date]

**Type:** [Standup / Planning / Review / 1:1 / Client / Other]
**Attendees:** [Names]
**Duration:** [Length]

---

## TL;DR
[1-2 sentences: the one thing that matters most from this meeting]

---

## Decisions
| # | Decision | Reasoning | Owner |
|---|----------|-----------|-------|
| 1 | [What was decided] | [Why] | [Who owns it] |
| 2 | [What was decided] | [Why] | [Who owns it] |

---

## Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | [Specific task] | [Name] | [Date] |
| 2 | [Specific task] | [Name] | [Date] |

---

## Discussion Notes

### [Topic 1]
- [Key point]
- [Key point]
- **Decision:** [What was decided]

### [Topic 2]
- [Key point]
- [Key point]
- **Open:** [What needs follow-up]

---

## Open Questions
- [ ] [Question that wasn't resolved — who will follow up?]
- [ ] [Question that wasn't resolved — who will follow up?]

---

## Next Meeting
**When:** [Date/time]
**Focus:** [What we'll cover next]
```

---

## Meeting Type Templates

### Standup / Daily Sync

```markdown
# Daily Sync: [Date]

**Attendees:** [Names]

| Person | Yesterday | Today | Blocked? |
|--------|-----------|-------|----------|
| [Name] | [Done] | [Doing] | [Yes/No: detail] |

**Blockers to resolve:**
- [Blocker] → [Who's handling it]
```

### Client Meeting

```markdown
# Client Meeting: [Client Name] — [Date]

**Attendees:** [Names from both sides]
**Context:** [Why this meeting happened]

---

## Client's Key Points
- [What they said, in their words]
- [What they emphasized]
- [What they asked for]

## Our Commitments
| # | What we promised | Owner | By When |
|---|-----------------|-------|---------|
| 1 | [Commitment] | [Name] | [Date] |

## Follow-Up Required
- [ ] [Send them X by Friday]
- [ ] [Schedule next check-in]

## Internal Notes (Don't share with client)
- [Observation about their priorities]
- [Risk or opportunity we noticed]
```

### 1:1 Meeting

```markdown
# 1:1: [Person A] + [Person B] — [Date]

---

## Topics Covered
1. [Topic] — [Key points and any decisions]
2. [Topic] — [Key points and any decisions]

## Action Items
- [Person A]: [Action] by [Date]
- [Person B]: [Action] by [Date]

## Notes for Next 1:1
- Follow up on: [Topic]
- Check: [Status of something]
```

---

## Note-Taking Rules

### Rule 1: Decisions Over Discussion
Capture the conclusion, not the debate. If 30 minutes of discussion led to "we'll use Option B," write that. Add reasoning in one line.

### Rule 2: Every Action Has an Owner
```
Bad: "We should update the docs."
Good: "Sarah: Update API docs by Friday."
```

### Rule 3: Use Their Words for Key Quotes
When someone says something important, capture it exactly:
> "We can't ship until the security review is done." — CTO

### Rule 4: Note What Was NOT Decided
Open questions are as important as decisions. They tell you what's still uncertain.

### Rule 5: Write It Within 24 Hours
Meeting notes lose 50% of their value every day you delay. Send same-day if possible.

---

## Quality Checklist

Before sharing:

- [ ] TL;DR captures the key outcome?
- [ ] All decisions have reasoning and owners?
- [ ] All action items have owners and due dates?
- [ ] Open questions are listed with follow-up owners?
- [ ] Someone who wasn't there would understand the context?
- [ ] Notes are concise (not a transcript)?
- [ ] Client-sensitive content is clearly marked as internal?

---

## Integration with ABC-TOM

When using this skill:

1. **Read from C-core:** Project brief for context
2. **Check M-memory:** Previous meeting notes for continuity
3. **Output to O-output:** Save in appropriate project folder
4. **Update M-memory:** Log key decisions to `decisions.md`

---

*The best meeting notes make the next meeting unnecessary.*

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
