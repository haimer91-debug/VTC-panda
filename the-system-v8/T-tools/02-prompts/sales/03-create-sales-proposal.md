# Prompt: Create a Sales Proposal

Copy and paste this into your chat (fill in the client details first):

---

```
I need to write a proposal/offer for a client. Here's the situation:

---
Client: [Who is this for? Company name, person's name, their role]
What they need: [What problem are they trying to solve? What did they ask for?]
What I'm proposing: [Your solution, service, or offer]
Budget/pricing (optional): [Price range, package details, or "help me figure this out"]
Context: [How did this lead come in? Any previous conversations? What do they already know about you?]
---

Adam, please manage this project:

1. Pre-flight check: Read C-core/project-brief.md, C-core/voice-dna.md, and C-core/icp-profile.md. If any of these files are empty or still have placeholder text, STOP and tell me which files need to be filled first.

2. Read the workflow in T-tools/03-workflows/sales-workflow.md to understand the full process

3. Read my client communication samples: B-brain/02-my-samples/02-sales/

4. Read the Sales Proposal skill: T-tools/01-skills/sales-proposal-skill/sales-proposal-skill.md

5. Read past learnings: M-memory/learning-log.md

6. Now delegate to the Strategist (read A-agents/strategist-agent.md first):
   - Analyze the client's situation and real needs
   - Map the opportunity and positioning
   - Identify what makes this proposal compelling for THIS specific client
   - Create a new folder in O-output/ with the next available number (e.g., 01-proposal-[client-name]), and a _process/ subfolder inside it
   - Save as _process/strategist-analysis.md

7. Review the Strategist's work, then delegate to the Copywriter (read A-agents/copywriter-agent.md first):
   - Write the proposal/email in MY voice and style
   - Use the Strategist's analysis to inform the approach
   - Apply the Sales Proposal skill format
   - Save as _process/copywriter-draft.md with notes about choices made

8. Send to the Gatekeeper (read A-agents/gatekeeper-agent.md first):
   - Review for persuasiveness, clarity, and voice match
   - Check: Would I actually send this? Does it sound like me?
   - Save as _process/gatekeeper-review.md
   - If approved, create final-proposal.md at the PROJECT FOLDER ROOT (not inside _process/) — ready to send
   - If not approved, manage revisions

9. Update M-memory/learning-log.md with what you learned from this process

Show me the final proposal and tell me if it's ready to send or needs revision.
```

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
