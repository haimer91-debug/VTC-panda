# Your First 7 Days After the Workshop

You built an AI team in a few hours. Now what?

Here's a simple plan. One thing per day. No pressure. Skip a day if you want. The system isn't going anywhere.

---

## Day 1: Create Something Real

You made your first output during the workshop. Now do it again, but with a real topic.

**What to do:**
1. Open your track folder in `T-tools/02-prompts/` (content, sales, or thinking)
2. Copy prompt `03-...` and paste it in Claude Code
3. This time, use a real topic. Something you actually need to write/decide/summarize.
4. When it's done, read the output in `O-output/`. Close to your voice? If not, that's normal. It gets better.
5. Run `04-close-the-loop.md` to capture what you learned. This is what makes the next output better.

**Bonus:** Try a different track. If you did content in the workshop, try sales or thinking. Same system, completely different output.

---

## Day 2: Feed the Brain

The more your agents know, the better they perform. Today is about making them smarter.

**What to do:**
1. Open your samples folder in `B-brain/02-my-samples/` (01-content, 02-sales, or 03-thinking)
2. Add 2-3 more samples of your real work. The best pieces you've written.
3. Run prompt `02-learn-my-style.md` from your track folder again
4. Compare the new output to yesterday's. You'll see the difference.

**Why this matters:** 3 samples is the minimum. 5-7 is where it starts getting really good. The agents learn your rhythm, your word choices, even your paragraph length.

**Tip:** Got random notes, ideas, or files you're not sure about? Drop them in `B-brain/04-INBOX/`. It's your junk drawer. You can sort them later, or ask Claude to sort them for you.

---

## Day 3: Meet the Bonus Prompts

There are 9 bonus prompts in `T-tools/02-prompts/BONUS/`. Today, explore them.

**Start with one of these:**

| Prompt | What It Does | Good For |
|---|---|---|
| `09-content-calendar.md` | Plans your content for the next 2 weeks | If you want structure and consistency |
| `10-repurpose-content.md` | Takes one piece and turns it into 5 formats | If you have a good post that could be more |
| `12-create-hook-bank.md` | Builds a collection of opening lines | If you stare at blank pages too often |

**How:** Open the file, copy the prompt, fill in your details, paste in Claude Code.

Don't try all 9 today. Pick one. Play with it.

---

## Day 4: Create Your First Agent

Your team already has Adam (COO), Copywriter, Gatekeeper, Researcher, Strategist, and more. But there's always room for someone new.

**What to do:**
1. Open `T-tools/02-prompts/BONUS/05-create-new-agent.md`
2. Think: what repeatable task do you need help with?
3. Fill in the details and paste the prompt

**Agent ideas:**
- **Editor** Reviews your writing for clarity and flow before the Gatekeeper checks it
- **Researcher** Gathers information and data before you write
- **Translator** Adapts your content between Hebrew and English
- **Social Media Manager** Repurposes one piece of content across platforms
- **Client Communication Manager** Drafts all client-facing messages in your tone

**Remember:** One clear job per agent. "Does everything" is a bad agent. "Expert in growth marketing" is a good agent.

---

## Day 5: Build Your First Skill

Skills are expert playbooks. They teach your agents how to do specific tasks.

**What to do:**
1. Open `T-tools/02-prompts/BONUS/06-create-new-skill.md`
2. Think: what content type do you create regularly that has specific rules?
3. Fill in the details and paste the prompt

**Note:** Your system already includes powerful skills: social post, blog post, newsletter, sales proposal, document summary, meeting notes, PRD, stakeholder update, Hebrew writing, and more. Check `T-tools/01-skills/` to see them all.

**Skill ideas for new ones:**
- **Product description skill** If you write product or service descriptions
- **Case study skill** If you create client case studies
- **Pitch deck skill** If you create investor or client presentations
- **Code review skill** If you review code regularly

**The result:** A playbook file in `T-tools/01-skills/` that any agent can reference when doing that type of work.

**Quick guide to T-tools:**
- **Skills** = Knowledge. What an agent knows HOW to do. (e.g., "how to write a newsletter")
- **Prompts** = Triggers. What YOU paste to start something. (e.g., "create a social post about X")
- **Workflows** = Pipelines. Multi-step processes that connect agents and skills. (e.g., "draft → review → revise → approve")

Rule of thumb: If it's knowledge, make it a skill. If it's a shortcut you paste, make it a prompt. If it has 3+ steps with handoffs between agents, make it a workflow.

---

## Day 6: Close The Loop (Deep Version)

By now you've created content, added samples, maybe built a new agent. Time for a deep Loop closing.

**What to do:**

1. **Update the memory.** Open `M-memory/learning-log.md` and add what you've learned this week:
   - What output sounded like you?
   - What didn't work?
   - What feedback would you give the agents?

2. **Refine the voice.** Open `C-core/voice-dna.md`. Specific enough? Add concrete examples:
   - Words you always use
   - Words you never use
   - How long your paragraphs are
   - How you open a piece

3. **Close The Loop.** Run prompt `04-close-the-loop.md` from your track folder. This promotes your best insights from Memory back into Core, so next time the agents start from a stronger foundation.

4. **Sort your INBOX.** Check `B-brain/04-INBOX/`. Anything in there? Move it to the right folder, or ask Claude to sort it for you.

---

## Day 7: Enable Auto-Revision and Plan Ahead

Two things today. One makes the system smarter, one makes you more organized.

**Morning: Enable the auto-revision loop**
1. Open `T-tools/02-prompts/BONUS/07-enable-auto-revision-loop.md`
2. Copy and paste the prompt
3. From now on, the Copywriter and Gatekeeper iterate automatically. You only see the approved version.

**Afternoon: Plan next week's content**
1. Open `T-tools/02-prompts/BONUS/09-content-calendar.md`
2. Fill in your topics, frequency, and time period
3. You'll get a structured calendar you can follow

---

## After Day 7: Keep Going

The system compounds. Week 1 is rough. Week 10 is magic.

**Weekly habit (5 minutes):**
- Run the weekly review: `T-tools/02-prompts/BONUS/13-weekly-review.md`
- Update `M-memory/learning-log.md` with what worked

**Monthly habit (15 minutes):**
- Add new writing samples to `B-brain/`
- Review and update `C-core/voice-dna.md`
- Run The Loop: `04-close-the-loop.md` from your track folder
- Sort `B-brain/04-INBOX/`
- Create a new agent or skill if you need one

**When finished with a project in O-output/:**
- Add `-done` to the folder name (e.g., `01-linkedin-post/` becomes `01-linkedin-post-done/`)
- This keeps your active work clean and easy to scan

**When you're stuck:**
- Type `/tom` and ask your question
- Check `@ALL-GUIDES-HERE/04-tom-agent-knowledge/common-questions.md`
- Ask in the workshop alumni WhatsApp group

---

## Quick Reference: All Bonus Prompts

| # | File | What It Does | Best Time to Try |
|---|------|-------------|-----------------|
| 05 | `create-new-agent.md` | Recruit a new team member | Day 4 |
| 06 | `create-new-skill.md` | Build an expert playbook | Day 5 |
| 07 | `auto-revision-loop.md` | Agents review each other automatically | Day 7 |
| 08 | `connect-api-keys.md` | Connect external tools (search, images) | When you're ready for advanced stuff |
| 09 | `content-calendar.md` | Plan your content schedule | Day 7, then monthly |
| 10 | `repurpose-content.md` | One piece becomes 5 formats | Day 3 or whenever you have a good post |
| 11 | `analyze-competitor.md` | See what works for competitors | When you need inspiration |
| 12 | `create-hook-bank.md` | Build a collection of opening lines | Day 3 or when you're stuck |
| 13 | `weekly-review.md` | Review performance and improve | Every week |

---

## The Golden Rule

**Use the system.** That's it.

Every time you create something, the agents learn. Every time you give feedback, the memory grows. Every time you close The Loop, the foundation strengthens.

You don't need to do everything at once. You just need to keep showing up.

Yalla, go build something today.

---

> **Tom Even**
> Workshops & future dates: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
