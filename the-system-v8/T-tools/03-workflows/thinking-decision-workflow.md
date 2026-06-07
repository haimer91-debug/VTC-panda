# Thinking Workflow: Decision Brief

> Adam (COO) orchestrates the Strategist, Devil's Advocate, Chief of Staff, and Gatekeeper to create a multi-perspective decision brief.

---

## Process Overview

```
[You] describe the decision and options
          ↓
[Adam] reads C-core, assigns the team, manages the debate
          ↓
[Strategist] analyzes options from business/growth perspective
          ↓
[Devil's Advocate] challenges assumptions and surfaces risks
          ↓
[Chief of Staff] synthesizes into one clear decision brief
          ↓
[Gatekeeper] reviews for quality and completeness
          ↓
[Adam] delivers final brief and updates memory
```

---

## Step 1: Preparation

### Adam Reads Context

Before starting, Adam reads:
- `C-core/project-brief.md` - What we do and who we serve
- `C-core/voice-dna.md` - How the brand communicates
- `M-memory/decisions.md` - Past strategic choices
- `M-memory/learning-log.md` - What we learned from previous rounds

### Adam Creates Project Folder

```
O-output/
└── decision-[topic]/
    ├── final-decision-brief.md        ← THE DELIVERABLE (copy-paste ready)
    └── _process/
        ├── strategist-analysis.md       ← Strategic perspective
        ├── devils-advocate-review.md    ← Challenges and risks
        ├── chief-of-staff-brief.md      ← Synthesized brief
        └── gatekeeper-review.md         ← Quality review
```

---

## Step 2: Strategist Analyzes

### What the Strategist Does

1. **Reads `A-agents/strategist-agent.md`** and `T-tools/01-skills/strategic-decision-skill/`
2. **Analyzes each option** with numbers: upside, downside, resources, timeline
3. **Evaluates "Do Nothing"** — the cost of inaction
4. **Delivers a clear recommendation** — takes a stand

### Deliverable: `_process/strategist-analysis.md`

```markdown
# Strategic Analysis: [Decision]

## Recommendation
[Clear recommendation in 1-2 sentences]

## Options
### Option A: [Name]
- Upside: [Best case with numbers]
- Downside: [Worst case with numbers]
- Resources: [What it takes]
- Timeline: [When we'd see results]

### Option B: [Name]
[Same structure]

### Option C: Do Nothing
[Status quo trajectory]

## Key Assumptions
1. [Assumption] — [What happens if wrong]

## Questions for the Devil's Advocate
- [What should they challenge?]
```

---

## Step 3: Devil's Advocate Challenges

### What the Devil's Advocate Does

1. **Reads the Strategist's analysis** and `A-agents/devils-advocate-agent.md`
2. **Tests every major assumption** — What if the opposite is true?
3. **Identifies underweighted risks** — What could go wrong?
4. **Proposes a missing option** — The alternative nobody mentioned
5. **Runs a pre-mortem** — If this fails in 12 months, what went wrong?

### Deliverable: `_process/devils-advocate-review.md`

```markdown
# Devil's Advocate Review: [Decision]

## Assumption Stress-Test
| # | Assumption | Risk If Wrong | Confidence |
|---|-----------|---------------|-----------|
| 1 | [Assumption] | [Impact] | Low/Med/High |

## Risks Underweighted
1. **[Risk]** — why it's bigger than the analysis suggests

## The Missing Option
[Alternative not considered]

## Pre-Mortem: If This Fails
[12-month failure scenario]

## The Hard Question
[The question you need to answer honestly]

## Summary
- **Agree:** [Points of consensus]
- **More risk:** [Points of disagreement]
- **Biggest concern:** [One sentence]
```

---

## Step 4: Chief of Staff Synthesizes

### What the Chief of Staff Does

1. **Reads both perspectives** and `A-agents/chief-of-staff-agent.md`
2. **Resolves conflicts** — Where they agree = high confidence. Where they disagree = judgment call.
3. **Produces one clear brief** — Scannable in 2 minutes, actionable immediately

### Deliverable: `_process/chief-of-staff-brief.md`

```markdown
# Decision Brief: [Topic]

**Prepared by:** Strategist, Devil's Advocate, Chief of Staff

## Decision Required
[One sentence]

## Context
[2-3 sentences]

## Options
[Each with pros, cons, numbers, confidence]

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Action] |

## Where Advisors Agree
[High-confidence points]

## Where Advisors Disagree
[Judgment calls for the decision-maker]

## Recommendation
[Clear recommendation with confidence level]

## What We Don't Know
[Explicit uncertainties]

## Next Steps
[Who, what, by when]
```

---

## Step 5: Gatekeeper Reviews

### What the Gatekeeper Does

1. **Checks completeness** — All options explored? Risks quantified?
2. **Checks quality** — Numbers real? Recommendation justified?
3. **Checks usability** — Could the decision-maker act on this in 5 minutes?
4. **Decision** — Approved / Revisions Needed

---

## Step 6: Adam Delivers

1. **Saves final version** to `final-decision-brief.md` (at the project folder root — NOT inside `_process/`)
2. **Presents to user** with key recommendation highlighted
3. **Updates memory:**
   - `M-memory/learning-log.md` with process insights
   - `M-memory/decisions.md` with the decision and reasoning

---

## Quick Checklist

- [ ] All agents read C-core context
- [ ] Strategist took a clear stand
- [ ] Devil's Advocate challenged specific assumptions
- [ ] Chief of Staff resolved (not just listed) conflicts
- [ ] Gatekeeper verified rigor
- [ ] Final brief is scannable in 2 minutes
- [ ] Memory updated with decision

---

*4 agents debating one decision. The tension between perspectives is the feature, not a bug.*

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
