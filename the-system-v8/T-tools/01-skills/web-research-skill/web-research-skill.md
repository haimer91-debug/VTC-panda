---
name: web-research-skill
description: Deep web research for content, competitors, and audience intelligence. Use this when you need real-time information from the internet, LinkedIn profiles, company websites, industry data, or any online research. Triggers on "תחקור", "research", "חפש באינטרנט", "find online", "LinkedIn research", "competitor analysis", or any request requiring up-to-date web information.
---

# Web Research Skill

Find, verify, and structure real information from the web.

## When to Use

- Researching a person, company, or competitor online
- Finding up-to-date information for content creation
- LinkedIn profile research (for outreach, content, or audience understanding)
- Market research and trend analysis
- Fact-checking claims before publishing
- Gathering data for briefings and strategy

---

## How Web Research Works in Claude

Claude Code has built-in web tools. Here's what you can do:

### WebSearch
Search the internet for any topic. Returns search results with links.
```
Use when: You need current information, data, news, or facts
```

### WebFetch
Visit a specific URL and read its content.
```
Use when: You have a specific page to analyze (article, profile, website)
```

### Combined Power
Search first to find the right pages, then fetch specific pages for deep reading.

---

## Research Workflows

### Workflow 1: Person Research (LinkedIn / Professional)

**Goal:** Build a profile of someone for outreach, content, or collaboration.

**Steps:**
1. **Search** for their name + company + role
2. **Fetch** their LinkedIn profile or personal website
3. **Search** for recent articles, talks, or interviews they've done
4. **Search** for their company's recent news

**What to capture:**
- Current role and company
- Professional background (career path, expertise areas)
- Recent public activity (posts, articles, talks)
- Topics they care about (based on what they share/write)
- Mutual connections or shared interests
- Language they use (formal? casual? technical?)

**Output format:**
```markdown
## Person Brief: [Name]

**Role:** [Title] at [Company]
**LinkedIn:** [URL]
**Key Focus Areas:** [2-3 topics]

### Professional Background
[2-3 sentences on career path]

### Recent Activity
- [What they've posted/published recently]
- [Topics they're engaging with]

### Relevant for Us Because
[Why this person matters to our goals]

### Conversation Starters
- [Specific thing to reference in outreach]
- [Shared interest or connection point]
```

---

### Workflow 2: Company / Competitor Research

**Goal:** Understand what a company does, how they position, and where the gaps are.

**Steps:**
1. **Search** for company name + industry
2. **Fetch** their homepage and key pages (about, pricing, product)
3. **Search** for recent news and press
4. **Search** for reviews or customer feedback
5. **Search** for their leadership team

**What to capture:**
- What they sell (products/services)
- Who they sell to (target audience)
- How they position (messaging, tone, unique claims)
- Pricing (if public)
- Strengths and weaknesses
- Recent changes or news

**Output format:**
```markdown
## Company Brief: [Company Name]

**Website:** [URL]
**Industry:** [Industry]
**Founded:** [Year] | **Size:** [Team size if available]

### What They Do
[2-3 sentences, plain language]

### Target Audience
[Who they serve]

### Positioning & Messaging
[How they talk about themselves, key claims]

### Pricing
[If available]

### Strengths
- [What they do well]

### Weaknesses / Gaps
- [What's missing or weak]

### Recent News
- [Latest developments]

### Implications for Us
[What this means for our strategy]
```

---

### Workflow 3: Topic / Trend Research

**Goal:** Understand the current state of a topic for content creation or strategy.

**Steps:**
1. **Search** for the topic + "2025" or "2026" (get recent results)
2. **Search** for the topic + "statistics" or "data"
3. **Fetch** the 2-3 most relevant articles
4. **Search** for contrarian or unique angles on the topic
5. **Search** for Hebrew content on the topic (if writing for Israeli audience)

**What to capture:**
- Current state (what's happening now)
- Key statistics (real numbers)
- Expert opinions (who's saying what)
- Contrarian takes (what most people get wrong)
- Content angles (what hasn't been covered yet)

**Output format:**
```markdown
## Topic Brief: [Topic]

**Research Date:** [Date]

### Current State
[What's happening now, 2-3 sentences]

### Key Numbers
- [Stat 1 + source]
- [Stat 2 + source]
- [Stat 3 + source]

### What Experts Say
- [Expert 1]: "[Quote or summary]"
- [Expert 2]: "[Quote or summary]"

### The Contrarian Angle
[What most coverage gets wrong or misses]

### Content Opportunities
- [Angle 1: Why it's interesting]
- [Angle 2: Why it's interesting]
- [Angle 3: Why it's interesting]

### Sources
- [URL 1]
- [URL 2]
- [URL 3]
```

---

### Workflow 4: Content Research (Before Writing)

**Goal:** Gather ammunition for a specific piece of content.

**Steps:**
1. **Search** for your content topic to see what already exists
2. **Fetch** the top 3 articles to understand what's been said
3. **Search** for data/statistics to support your angle
4. **Search** for real examples or case studies
5. **Search** for Hebrew-language sources if writing in Hebrew

**What to capture:**
- What's already been written (so you don't repeat it)
- Statistics that support your point
- Real examples and stories
- Quotes you can reference
- Gaps in existing content (your unique angle)

**The goal:** Not to copy. To know what exists so you can write something different and better.

---

## Research Quality Rules

### Rule 1: Verify Before You Trust
One source is a claim. Two sources is a pattern. Three sources is a fact.

Don't include a statistic you found in only one place without labeling it: "According to [source]..."

### Rule 2: Date Everything
Information expires. Always note when something was published.
- Last 6 months: solid
- 6-12 months: still useful
- Over 12 months: use carefully, might be outdated

### Rule 3: Source Everything
Every fact, number, and quote needs a source. "According to reports" is not a source. A URL is.

### Rule 4: Separate Facts from Interpretation
```
Fact: "Company X raised $50M in January 2026" (source: TechCrunch)
Signal: They posted 12 job listings in the last month
Interpretation: They're likely expanding into enterprise
```

### Rule 5: Search in the Right Language
- English searches: broader results, more data
- Hebrew searches: local market, Israeli perspective, Hebrew-speaking audience insights
- Do both when researching for Israeli content

### Rule 6: Go Beyond Page 1
The most interesting findings are rarely in the first result. Refine your search, try different keywords, dig deeper.

---

## Search Tips

### Better Search Queries
| Bad Query | Better Query |
|-----------|-------------|
| "AI marketing" | "AI marketing tools for small business 2026" |
| "competitor analysis" | "[specific competitor name] pricing reviews" |
| "LinkedIn tips" | "LinkedIn engagement rate by post type 2026" |

### Useful Search Operators
- `"exact phrase"` - Search for exact words
- `site:linkedin.com [name]` - Search within a specific site
- `[topic] filetype:pdf` - Find reports and whitepapers
- `[topic] -[exclude word]` - Exclude irrelevant results
- `[topic] after:2025` - Recent results only

### For LinkedIn Research
- Search: `site:linkedin.com/in/ "[person name]" [company]`
- Search: `site:linkedin.com/posts/ "[person name]"` (find their posts)
- Search: `site:linkedin.com/company/ "[company name]"`

---

## When Web Search Isn't Available

Sometimes Claude doesn't have web access. In that case:

1. **Be transparent:** "I don't have web access right now. Here's what I know from my training data..."
2. **Use what you have:** Work with the files in B-brain/ and M-memory/
3. **Ask the human:** "Could you paste the LinkedIn profile / article / page here?"
4. **Note limitations:** "This is based on information up to [date]. For current data, I'd recommend checking..."

---

## Integration with ABC-TOM

1. **Before research:** Read `C-core/project-brief.md` to understand context
2. **During research:** Cross-reference with `B-brain/` for existing knowledge
3. **After research:** Save valuable findings to `B-brain/` (right subfolder, not INBOX)
4. **Close the loop:** Log research insights in `M-memory/learning-log.md`

---

*Good research is invisible. The reader just thinks the content is really smart.*

---

> **© Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
