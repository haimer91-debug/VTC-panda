# Prompt: Create Your Output

Choose your output type, fill in the details, then copy and paste into your chat:

**Which option should I pick?**
- Need to make a decision with multiple options? → **Option A** (Decision Brief)
- Have raw material to summarize (meeting notes, transcript, document)? → **Option B** (Summary Document)
- Option B also handles: stakeholder updates, PRDs, meeting summaries, board updates, quarterly reviews

---

## Option A: Decision Brief

Use this when you need to make a strategic decision and want multiple perspectives.

```
I need to make a decision. Here's what I'm facing:

---
Decision: [What decision do you need to make?]

Options I'm considering:
- Option A: [describe]
- Option B: [describe]
- Option C (optional): [describe]

Context: [Why is this decision coming up now? What's the timeline?]

What's at stake: [What happens if we get this wrong?]
---

Adam, please manage this project:

1. Pre-flight check: Read C-core/project-brief.md, C-core/voice-dna.md, and C-core/icp-profile.md. If any of these files are empty or still have placeholder text, STOP and tell me which files need to be filled first.

2. Read the workflow in T-tools/03-workflows/thinking-decision-workflow.md

3. Read my samples: B-brain/02-my-samples/ (check all subfolders)

4. Read the Strategic Decision skill: T-tools/01-skills/strategic-decision-skill/strategic-decision-skill.md

5. Read past decisions and learnings: M-memory/decisions.md and M-memory/learning-log.md

6. Delegate to the Strategist (read A-agents/strategist-agent.md first):
   - Analyze each option from a business perspective
   - Include the "do nothing" option
   - Produce a clear recommendation
   - Create a new folder in O-output/ (e.g., 01-decision-[topic]), and a _process/ subfolder inside it
   - Save as _process/strategist-analysis.md

7. Send to the Devil's Advocate (read A-agents/devils-advocate-agent.md first):
   - Challenge every major assumption
   - Identify risks the Strategist missed
   - Propose at least one alternative
   - Run a pre-mortem
   - Save as _process/devils-advocate-review.md

8. Send both to the Chief of Staff (read A-agents/chief-of-staff-agent.md first):
   - Synthesize into a single decision brief
   - Resolve conflicts between perspectives
   - Save as _process/chief-of-staff-brief.md

9. Send to the Gatekeeper (read A-agents/gatekeeper-agent.md first):
   - Review for quality and completeness
   - Save as _process/gatekeeper-review.md
   - If approved, create final-decision-brief.md at the PROJECT FOLDER ROOT (not inside _process/)
   - If not approved, manage revisions

10. Update M-memory/learning-log.md and M-memory/decisions.md

Show me the final decision brief and tell me if it's ready to use or needs revision.
```

---

## Option B: Summary Document

Use this when you have raw material (meeting transcript, call notes, interview recording, etc.) and need a structured summary.

```
I need to create a structured summary. Here's the raw material:

---
Source: [Meeting transcript / Call notes / Interview recording / Other]

What to summarize:
[PASTE YOUR RAW MATERIAL HERE - transcript, notes, or recording summary]

Output format (pick one):
- Meeting summary
- User interview summary
- Stakeholder update
- PRD / Product brief
- General document summary
---

Adam, please manage this project:

1. Pre-flight check: Read C-core/project-brief.md, C-core/voice-dna.md, and C-core/icp-profile.md. If any of these files are empty or still have placeholder text, STOP and tell me which files need to be filled first.

2. Read the workflow in T-tools/03-workflows/thinking-summary-workflow.md

3. Read my document samples: B-brain/02-my-samples/03-thinking/

4. Read the relevant skill from T-tools/01-skills/:
   - Meeting summary → document-summary-skill or meeting-notes-skill
   - User interview → document-summary-skill
   - Stakeholder update → stakeholder-update-skill
   - PRD → prd-skill
   - General → document-summary-skill

5. Read past learnings: M-memory/learning-log.md

6. Delegate to the Analyst (read A-agents/analyst-agent.md first):
   - Extract key information from the raw material
   - Organize into structured sections
   - Identify decisions, action items, and open questions
   - Create a new folder in O-output/ (e.g., 01-summary-[topic]), and a _process/ subfolder inside it
   - Save as _process/analyst-draft.md

7. Send to the Copywriter (read A-agents/copywriter-agent.md first):
   - Polish the language to match MY document style
   - Ensure consistency with my voice-dna
   - Save as _process/copywriter-draft.md

8. Send to the Gatekeeper (read A-agents/gatekeeper-agent.md first):
   - Review for completeness, clarity, and style match
   - Save as _process/gatekeeper-review.md
   - If approved, create final-summary.md at the PROJECT FOLDER ROOT (not inside _process/)
   - If not approved, manage revisions

9. Update M-memory/learning-log.md

Show me the final summary and tell me if it's ready to use or needs revision.
```

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
