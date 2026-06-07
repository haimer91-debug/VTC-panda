---
name: prd-skill
description: Write clear Product Requirement Documents (PRDs) that align teams. Use this when defining features, projects, or initiatives that need clear scope, requirements, and success criteria. Produces PRDs that engineers, designers, and stakeholders can all understand.
---

# PRD Skill

Write PRDs that get built as intended. Clarity is the feature.

## When to Use

- Defining a new feature or product
- Scoping a project before development starts
- Aligning stakeholders on what we're building and why
- Creating a reference document for the team during execution

---

## PRD Fundamentals

**What makes a great PRD:**
- Anyone on the team can read it and understand what we're building
- The "why" is as clear as the "what"
- Success is measurable (not "improve user experience")
- Edge cases and non-goals are explicit

**PRD length:**
- **Small feature:** 1-2 pages
- **Medium feature:** 2-4 pages
- **Large initiative:** 4-6 pages

**The rule:** A PRD is not a spec. It's a decision document. It answers "what" and "why," then points to specs for "how."

---

## The PRD Template

```markdown
# PRD: [Feature/Project Name]

**Author:** [Name]
**Date:** [Date]
**Status:** [Draft / In Review / Approved / In Development]
**Last Updated:** [Date]

---

## 1. Summary

[2-3 sentences: What are we building and why? If someone reads ONLY this, they should understand the project.]

---

## 2. Problem Statement

### What's happening now
[Describe the current state. Be specific — use data, quotes, or examples.]

### Why it matters
[Business impact: revenue, retention, efficiency, user satisfaction. Use numbers.]

### Who's affected
[Which users/personas? How many? How often do they hit this problem?]

---

## 3. Goals & Success Metrics

### Goals
1. [Primary goal — what does success look like?]
2. [Secondary goal]

### Success Metrics
| Metric | Current | Target | How We Measure |
|--------|---------|--------|----------------|
| [Metric] | [Baseline] | [Goal] | [Tool/method] |

### Non-Goals (Explicitly Out of Scope)
- [Thing we are NOT doing, and why]
- [Thing we are NOT doing, and why]

---

## 4. Proposed Solution

### Overview
[High-level description of the solution. 1-2 paragraphs.]

### User Flow
1. User does [action]
2. System responds with [response]
3. User sees [result]

### Key Screens / States
[Describe or reference mockups for each key state]

---

## 5. Requirements

### Must Have (P0)
- [ ] [Requirement] — [Why it's critical]
- [ ] [Requirement] — [Why it's critical]

### Should Have (P1)
- [ ] [Requirement] — [Why it matters]

### Nice to Have (P2)
- [ ] [Requirement] — [Why we'd want it]

---

## 6. Edge Cases & Error States

| Scenario | Expected Behavior |
|----------|------------------|
| [What if X happens?] | [System does Y] |
| [What if user does Z?] | [System responds with W] |
| [Empty state] | [What the user sees] |
| [Error state] | [Error message and recovery] |

---

## 7. Technical Considerations

[Notes for engineering: API changes, data model impacts, dependencies, performance requirements. Keep it high-level — detailed specs go in separate docs.]

---

## 8. Timeline & Milestones

| Milestone | Target Date | Owner |
|-----------|-------------|-------|
| Design review | [Date] | [Name] |
| Dev start | [Date] | [Name] |
| QA ready | [Date] | [Name] |
| Launch | [Date] | [Name] |

---

## 9. Open Questions

- [ ] [Question that needs an answer before or during development]
- [ ] [Decision that's still pending]

---

## 10. Appendix

[Links to: mockups, user research, competitive analysis, technical specs, related PRDs]
```

---

## Writing Rules for PRDs

### Rule 1: The Problem Comes Before the Solution
If the team doesn't agree on the problem, the solution doesn't matter. Spend more time on Section 2 than Section 4.

### Rule 2: Success Must Be Measurable
```
Bad: "Improve the onboarding experience"
Good: "Increase Day-7 retention from 34% to 45%"
```

### Rule 3: Non-Goals Are as Important as Goals
Explicitly saying what you're NOT doing prevents scope creep and misaligned expectations.

### Rule 4: Write for Your Audience
- Engineers need: requirements, edge cases, technical considerations
- Designers need: user flows, states, context
- Stakeholders need: problem, goals, timeline
- A good PRD serves all three.

### Rule 5: Keep It Updated
A PRD that's out of date is worse than no PRD. Update status, decisions, and scope changes as they happen.

---

## PRD Review Checklist

Before sharing for review:

- [ ] Summary is clear in 2-3 sentences?
- [ ] Problem is backed by data or user evidence?
- [ ] Success metrics are specific and measurable?
- [ ] Non-goals are explicit?
- [ ] Requirements are prioritized (P0/P1/P2)?
- [ ] Edge cases are covered?
- [ ] Timeline has owners?
- [ ] Open questions are listed?
- [ ] An engineer could read this and start planning?
- [ ] A stakeholder could read this and understand the tradeoffs?

---

## Integration with ABC-TOM

When using this skill:

1. **Read from C-core:** Project brief and ICP for context
2. **Check M-memory:** Previous decisions for consistency
3. **Output to O-output:** Save in project folder
4. **Update M-memory:** Log decisions made during PRD process

---

*A PRD is a contract between "what we want" and "what we'll build." Make both sides crystal clear.*

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
