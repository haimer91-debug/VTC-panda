# Prompt: Enable Automatic Revision Loop

Use this once to make the revision process automatic for all future posts.

Copy and paste this into your chat:

---

```
I want to update the workflow so that the Copywriter and Gatekeeper always iterate automatically until the content is approved, without needing my input.

Please update the following files:

1. Update T-tools/03-workflows/content-workflow.md:
   - Add a new section called "Automatic Revision Loop"
   - Explain that after the first draft, if the Gatekeeper sends it back, the Copywriter must automatically create a new version based on the feedback
   - The loop continues until approved or until 3 revision attempts (then escalate to human)
   - Only the final approved version should be presented to the human

2. Update A-agents/gatekeeper-agent.md:
   - Add instructions that when sending back, the Gatekeeper must immediately hand back to the Copywriter with specific fixes
   - Add that this loop should happen automatically without waiting for human input

3. Update A-agents/copywriter-agent.md:
   - Add instructions to always check the Gatekeeper's feedback and revise automatically if not approved
   - Add that the Copywriter should keep the version history (v1, v2, v3...)

4. Update M-memory/learning-log.md:
   - Document this new automatic revision process

From now on, when I ask for a LinkedIn post, I should only see the final approved version. The iteration happens in the background.

Confirm the updates are done.
```

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
