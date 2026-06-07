# Folder Guide

What each folder does and how to use it.

---

## A-agents/

**Purpose:** Your AI team definitions

**What goes here:**
- Agent personality files (one per agent)
- Each file defines: who they are, what they read, how they work

**Current agents:**
- `copywriter-agent.md` - Writes all content
- `gatekeeper-agent.md` - Reviews quality
- `tom-agent.md` - Your guide to the system

**How to create a new agent:**
1. Create `[role]-agent.md` in this folder
2. Copy structure from existing agent
3. Define: identity, required reading, responsibilities
4. Use prompt: `T-tools/02-prompts/BONUS/05-create-new-agent.md`

**Tips:**
- One job per agent (don't make generalists)
- Be specific about what "good" means
- Always include Required Reading section

---

## B-brain/

**Purpose:** Knowledge your agents need. **Brain is what you bring.**

**What goes here:**
- `01-about-me.md` - Answer questions about yourself and your business
- `02-my-samples/` - Your past writing, organized by track (01-content, 02-sales, 03-thinking)
- `03-api-keys-registry.md` - API keys for external tools (keep private, don't share)
- `04-INBOX/` - Quick capture point. Drop anything new here first, organize later.
- Research documents, reference materials, data

**How to use:**
1. Fill in `01-about-me.md` to get started
2. Add your past content to `02-my-samples/` in the subfolder matching your track
3. Add sales/references as needed
4. Use `04-INBOX/` when you're not sure where something goes. Sort it later.

**Brain vs Memory:**
- Brain = What YOU bring to the system (your knowledge, research, examples)
- Memory = What you LEARN TOGETHER with the system (patterns, feedback, decisions)

**"Brain is what you bring. Memory is what you learn together."**

**Tips:**
- More knowledge = smarter agents
- Add real examples, not descriptions
- Keep it organized (subfolders help)
- When in doubt, drop it in 04-INBOX

---

## C-core/

**Purpose:** Your brand's DNA

**The three files:**

### project-brief.md
What you do, who you serve, what makes you different.
- Your mission
- The problem you solve
- What makes you unique

### voice-dna.md
How your brand speaks.
- Tone and style
- Words you use / avoid
- Formatting preferences
- Example sentences

### icp-profile.md
Your ideal customer.
- Who they are
- What they want
- Their problems
- Where they hang out

**How to fill these:**
1. Answer questions in `B-brain/01-about-me.md`
2. Run prompt `T-tools/02-prompts/[your-track]/01-learn-about-me.md`
3. Claude fills in C-core automatically

**Not sure what a filled-in file looks like?**
Check `C-core/_examples/` for real examples across 3 roles (freelancer, product manager, content creator).

**Tips:**
- Be specific (not "professional" but "short sentences, no jargon")
- Include examples
- These start stable but evolve through The Loop (insights from Memory get promoted here)

---

## T-tools/

**Purpose:** Skills, workflows, and prompts

**Structure:**
```
T-tools/
├── 01-skills/                              → Expert playbooks
├── 02-prompts/                             → Copy-paste instructions
└── 03-workflows/                           → Multi-step processes
```

### 01-skills/
Specialized knowledge for specific tasks.
- `social-post-skill/` - Social media best practices
- `blog-post-skill/` - Blog post structure and writing
- `newsletter-skill/` - Newsletter writing and engagement
- `case-study-skill/` - Turn client wins into social proof
- `internal-communication-skill/` - Team announcements and updates
- `sales-proposal-skill/` - Client proposals and offers
- `professional-email-skill/` - Email writing
- `document-summary-skill/` - Summarizing documents and interviews
- `meeting-notes-skill/` - Meeting note capture and structure
- `prd-skill/` - Product requirement documents
- `stakeholder-update-skill/` - Stakeholder status updates
- `strategic-decision-skill/` - Decision brief framework
- `tom-guide/` - System guidance

### 02-prompts/
Numbered instructions for common actions.
```
content/
├── 01-learn-about-me.md
├── 02-learn-my-style.md
├── 03-create-content.md
└── 04-close-the-loop.md
sales/
└── ... (same structure)
thinking/
└── ... (same structure)
BONUS/
├── 05-create-new-agent.md
├── 06-create-new-skill.md
└── ... (up to 13-weekly-review.md)
```

**Quick guide to T-tools:**
- **Skills** = Knowledge. What an agent knows HOW to do. (e.g., "how to write a newsletter")
- **Prompts** = Triggers. What YOU paste to start something. (e.g., "create a social post about X")
- **Workflows** = Pipelines. Multi-step processes that connect agents and skills. (e.g., "draft → review → revise → approve")

Rule of thumb: If it's knowledge, make it a skill. If it's a shortcut you paste, make it a prompt. If it has 3+ steps with handoffs between agents, make it a workflow.

### 03-workflows/
Multi-step processes that chain actions. One workflow per track:
- `content-workflow.md` - Idea → research → draft → review → publish (social posts, blogs, newsletters)
- `sales-workflow.md` - Client context → strategy → draft → review → send
- `thinking-decision-workflow.md` - Decision → analysis → debate → synthesis → review
- `thinking-summary-workflow.md` - Raw material → extraction → polish → review

**How to create new tools:**
- New skill: `T-tools/02-prompts/BONUS/06-create-new-skill.md`
- Skills go in their own subfolder
- Prompts are numbered for order

---

## O-output/

**Purpose:** Everything your agents create

**Organization:**
```
O-output/
└── your-project/
    ├── final-[type].md      ← YOUR DELIVERABLE (copy-paste ready)
    └── _process/
        ├── research/draft    ← Internal work
        └── review files      ← Quality checks
```

**How to use:**
- One project per folder
- The final file is always at the project root (copy-paste ready)
- All process files (drafts, reviews, research) go in `_process/`
- Open any project folder: your deliverable is right there

**Tips:**
- Consistent naming helps you find things
- Don't delete process files (you might need them)
- Let agents save here automatically

---

## M-memory/

**Purpose:** What you learn together with the system. **Memory is what you learn together.**

**The three files:**

### learning-log.md
Execution patterns. What worked, what didn't.
- "Short hooks perform better"
- "Avoid starting with questions"
- "The gatekeeper catches too much, lower threshold"

### feedback.md
Audience signals. What they say after you publish.
- Comments and reactions
- Questions people ask
- What resonates

### decisions.md
Strategic rationale. Why you chose what you chose.
- "We focus on LinkedIn because that's where ICP is"
- "We don't use emojis in headlines"
- "Bilingual content, Hebrew for local, English for newsletter"

**When to update:**
- `learning-log.md` → After each review cycle
- `feedback.md` → After publishing and seeing reactions
- `decisions.md` → When you make strategic choices

**Why this matters:**
Agents read memory before starting work. Every entry makes future output better. This is the compounding effect.

**The Loop:** The best insights from Memory don't just stay here. They get promoted back into Brain (as new knowledge) and Core (as updated rules). That's what closes The Loop and makes the system compound.

Run `04-close-the-loop.md` from your track folder to close The Loop explicitly.

---

## Quick Reference

| Folder | Contains | Changes How Often |
|--------|----------|-------------------|
| A-agents/ | Team definitions | Rarely |
| B-brain/ | Knowledge, examples (what you bring) | Often (as you learn) |
| C-core/ | Brand DNA | Rarely (but evolves through The Loop) |
| T-tools/ | Skills, prompts, workflows | Sometimes (as you need more) |
| O-output/ | Created content | Every project |
| M-memory/ | Learnings (what you learn together) | After every project |

---

## The Pattern: The ABC-TOM Loop

1. **ABC feeds the system** (who you are, what you know)
2. **TOM executes** (skills create output, memory captures learning)
3. **The Loop: Memory feeds back into Brain and Core** (best learnings become knowledge and rules)
4. **The system starts stronger next time** (and keeps compounding)

This is The Loop. It's what makes the difference between a static template and a living system that grows with you.

---

> **© Tom Even**
> Workshops: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
