# T-tools: Your Toolbox

Skills, prompts, and workflows. The things that give your agents superpowers.

---

## Three Types of Tools

### Skills (Expert Playbooks)
Specialized knowledge for specific content types.

**Content skills:**
- `01-skills/social-post-skill/` - Social media best practices
- `01-skills/blog-post-skill/` - Blog post structure and writing
- `01-skills/newsletter-skill/` - Newsletter writing and engagement
- `01-skills/case-study-skill/` - Turn client wins into social proof
- `01-skills/internal-communication-skill/` - Team announcements, policy changes, company updates

**Sales skills:**
- `01-skills/sales-proposal-skill/` - Client proposals and offers
- `01-skills/professional-email-skill/` - Email writing expertise

**Thinking skills:**
- `01-skills/document-summary-skill/` - Summarizing documents and interviews
- `01-skills/meeting-notes-skill/` - Meeting note capture and structure
- `01-skills/prd-skill/` - Product requirement documents
- `01-skills/stakeholder-update-skill/` - Stakeholder status updates
- `01-skills/strategic-decision-skill/` - Decision brief framework

**System skills:**
- `01-skills/hebrew-writing-skill/` - Hebrew writing quality
- `01-skills/web-research-skill/` - Web research techniques
- `01-skills/tom-guide/` - System guidance
- `01-skills/adam-coo/` - COO orchestration

### Prompts (Copy-Paste Instructions)
Saved instructions you paste into Claude Code.

**Workshop flow (01-04) — in each track folder:**

| # | File | What It Does |
|---|------|-------------|
| 01 | `learn-about-me.md` | Teaches Claude about you and fills core files |
| 02 | `learn-my-style.md` | Teaches agents your voice |
| 03 | `create-[output].md` | Creates your first output (varies by track) |
| 04 | `close-the-loop.md` | Promotes insights from Memory to Core |

**Bonus prompts (05-13):**

| # | File | What It Does |
|---|------|-------------|
| 05 | `create-new-agent.md` | Recruit a new team member |
| 06 | `create-new-skill.md` | Build an expert playbook |
| 07 | `enable-auto-revision-loop.md` | Agents review each other automatically |
| 08 | `connect-api-keys.md` | Connect external tools |
| 09 | `content-calendar.md` | Plan your content schedule |
| 10 | `repurpose-content.md` | One piece becomes 5 formats |
| 11 | `analyze-competitor.md` | Research competition |
| 12 | `create-hook-bank.md` | Build opening line collection |
| 13 | `weekly-review.md` | Review and improve weekly |

### Workflows (Multi-Step Processes)
Recipes that coordinate multiple agents. Adam (COO) orchestrates all workflows.

- `03-workflows/content-workflow.md` — Content track (Researcher → Copywriter → Gatekeeper). Handles social posts, blog posts, newsletters.
- `03-workflows/sales-workflow.md` — Sales track (Strategist → Copywriter → Gatekeeper). Handles proposals.
- `03-workflows/thinking-decision-workflow.md` — Decision brief (Strategist → Devil's Advocate → Chief of Staff → Gatekeeper).
- `03-workflows/thinking-summary-workflow.md` — Summary (Analyst → Copywriter → Gatekeeper). Handles meeting notes, documents, PRDs.

---

## Folder Structure

```
T-tools/
├── 01-skills/
│   ├── social-post-skill/
│   ├── blog-post-skill/
│   ├── newsletter-skill/
│   ├── sales-proposal-skill/
│   ├── professional-email-skill/
│   ├── document-summary-skill/
│   ├── meeting-notes-skill/
│   ├── prd-skill/
│   ├── stakeholder-update-skill/
│   ├── strategic-decision-skill/
│   ├── case-study-skill/
│   ├── internal-communication-skill/
│   ├── hebrew-writing-skill/
│   ├── web-research-skill/
│   ├── tom-guide/
│   └── adam-coo/
├── 02-prompts/
│   ├── content/          → Content track prompts (01-04)
│   ├── sales/            → Sales track prompts (01-04)
│   ├── thinking/         → Thinking track prompts (01-04)
│   └── BONUS/            → Advanced prompts (05-13)
└── 03-workflows/
```

---

## Creating New Tools

**New skill:** Use `02-prompts/BONUS/06-create-new-skill.md`
**New prompt:** Create numbered file in `02-prompts/`
**New workflow:** Create in `03-workflows/`

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
