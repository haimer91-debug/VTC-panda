# Common Questions

Answers to the most frequent questions about the ABC-TOM system.

---

## Getting Started

### "Where do I start?"

Start with Exercise 1: Feed Your Core.

1. Open `B-brain/01-about-me.md`
2. Answer the questions (10-15 minutes)
3. Copy the prompt from `T-tools/02-prompts/[your-track]/01-learn-about-me.md`
4. Claude fills in your C-core files

Everything else builds from knowing who you are.

---

### "I finished the workshop. Now what?"

Do these in order:

1. **Add more writing samples** to your track folder in `B-brain/02-my-samples/` (at least 3-5)
2. **Run Exercise 2** to teach agents your style
3. **Create your first real piece** using prompt 03 from your track
4. **Close The Loop** using prompt 04 from your track
5. **Explore the BONUS prompts** when ready

Then: Use the system. The more you use it, the better it gets.

---

### "How long until my agents sound like me?"

Honestly? Week 1 is rough. Week 10 is magic.

The system compounds. Every correction you make, every learning you log, improves future output.

To speed this up:
- Add more writing samples
- Be specific in voice-dna (examples, not descriptions)
- Update learning-log after every project

---

## Understanding the System

### "What's the difference between Brain and Memory?"

**Brain** (B-brain/) = What YOU bring to the system.
- Your knowledge, research, examples
- Things you already know and want agents to have
- Input you provide from outside

**Memory** (M-memory/) = What you LEARN TOGETHER with the system.
- Patterns discovered through working together
- Feedback from your audience
- Decisions made along the way

**"Brain is what you bring. Memory is what you learn together."**

Think of it this way:
- Brain is the textbook you hand to a new employee on day one
- Memory is the notes you both take as you work together over months

---

### "What's The Loop?"

The Loop is what makes the system compound over time. It's the process of promoting insights from Memory back into Brain and Core.

Here's how it works:
1. You create output using the system
2. You review it and log what worked in M-memory
3. The best insights get promoted back into B-brain (as knowledge) and C-core (as updated rules)
4. Next time agents run, they start from a stronger foundation

Example: You notice in `learning-log.md` that "posts opening with a personal story get 3x more engagement." That insight gets promoted to `voice-dna.md` as a rule: "Always open with a personal story."

Run `04-close-the-loop.md` from your track folder to close The Loop explicitly.

---

### "Where do I put new stuff?"

Use `B-brain/04-INBOX/`.

It's a visible capture point. When you have something new (an article, a screenshot, a competitor example, a random idea) and you're not sure where it goes, drop it in INBOX.

Later, when you have time, organize it into the right folder. Or ask Claude to help you sort it.

The point: Don't lose things because you're overthinking where they go. Capture first, organize later.

---

### "Do I need all 6 folders?"

Yes, but you don't need to fill them all at once.

**Start with:**
- C-core (who you are) - Essential
- A-agents (your team) - Already set up
- B-brain (knowledge) - Add writing samples

**Build over time:**
- T-tools (add skills as needed)
- O-output (grows naturally)
- M-memory (update after each project)

---

### "Can I change the folder names?"

You can, but I don't recommend it. The ABC-TOM naming is:
1. Memorable (easy to remember the system)
2. Alphabetical (folders sort in order)
3. Referenced in all the prompts

If you change names, you'll need to update every prompt and agent file.

---

## Creating Content

### "My agent output sounds generic, not like me"

Most common issue. Check these:

1. **Voice-dna is too vague**
   - Open `C-core/voice-dna.md`
   - Add specific examples, not descriptions
   - "Never use em-dashes" is better than "write naturally"

2. **Not enough writing samples**
   - Add 3-5 real pieces to your track folder (e.g., `B-brain/02-my-samples/01-content/`)
   - Run `02-learn-my-style.md` again

3. **Learning-log has wrong patterns**
   - Check `M-memory/learning-log.md`
   - Remove entries that pushed wrong direction

---

### "The gatekeeper rejects everything"

Your quality bar might be too high. Two options:

1. **Lower the threshold** - Edit gatekeeper-agent.md, adjust what "acceptable" means
2. **Improve input** - Better voice-dna and samples = better first drafts

The gatekeeper should catch real issues, not create busywork.

---

### "How do I create content for a different platform?"

1. Check if there's a skill in `T-tools/01-skills/`
2. If not, create one using `06-create-new-skill.md`
3. Update the workflow to include the new platform

Each platform has different best practices. Skills capture those.

---

## Agents

### "How do I create a new agent?"

1. Copy an existing agent file structure
2. Create `A-agents/[role]-agent.md`
3. Define: identity, required reading, responsibilities
4. Or use: `T-tools/02-prompts/BONUS/05-create-new-agent.md`

**Rule:** One clear job per agent. "Social media manager" is too broad. "LinkedIn post writer" is focused.

---

### "How many agents do I need?"

Start with 2: Copywriter + Gatekeeper.

Add more when:
- You have a repeatable task that's different enough
- The existing agents are getting complex
- You want specialized quality (e.g., SEO reviewer)

Most people don't need more than 4-5 agents.

---

### "Can agents talk to each other?"

Yes, through the workflow system.

Example flow:
```
Copywriter creates draft → Gatekeeper reviews → Copywriter revises → Gatekeeper approves
```

Define this in your workflows. Agents read each other's output.

---

## Technical

### "Where are my files stored?"

On your computer. In the folder you chose in Obsidian.

Nothing is in the cloud (unless you set up Obsidian Sync or GitHub).

You own your files. That's the point.

---

### "How do I back up my system?"

Options:

1. **Obsidian Sync** ($4/month) - Easiest. Automatic.
2. **GitHub** (free) - Version history included. For technical users.
3. **Manual backup** - Copy the folder periodically.

I recommend Obsidian Sync if you're not technical. Set it and forget it.

---

### "Can I use this with a different AI (not Claude)?"

The system is designed for Claude Code, but the concepts work anywhere:
- The folder structure works with any AI
- Agent files can be used as system prompts
- Skills can be copy-pasted into any chat

Claude Code is special because it reads and writes files directly. Other AIs need more copy-pasting.

---

## Troubleshooting

### "/tom or /adam isn't working"

This always means one thing: wrong working directory.

Claude Code slash commands only work when you open Claude Code with the `the-system` folder as your working directory.

**Fix:**
1. Close Claude Code
2. Reopen it
3. When choosing the working directory, navigate INTO the `the-system` folder (not your Obsidian vault root)
4. The correct directory ends in `.../the-system/` (or whatever you renamed it)

Then `/tom` and `/adam` will both work.

**Quick test:** Type `/tom` — if it shows a command option, you're in the right folder. If nothing happens, you're in the wrong folder.

---

### "Claude isn't reading my files"

Check:
1. Are you in the right folder? (Claude should be opened in the `the-system` folder)
2. Did you tell Claude which files to read?
3. Are file paths correct in Required Reading sections?

Try: "Read all files in C-core/ and summarize what you learned"

---

### "I'm getting inconsistent results"

This usually means:
1. Voice-dna isn't specific enough
2. Learning-log has contradicting entries
3. Agents have different "Required Reading" lists

Fix: Make sure all agents read the same core files.

---

### "I broke something"

Don't panic.

1. Check what changed recently
2. If you edited a file wrong, undo or restore
3. If memory is causing issues, clear the problematic entry
4. Worst case: Download fresh ABC-TOM template, copy your C-core content over

Files are just text. Nothing is permanent.

---

## Advanced

### "How do I connect APIs?"

Use `T-tools/02-prompts/BONUS/08-connect-api-keys.md`.

Common integrations:
- Replicate (image generation)
- Notion
- Todoist

Store keys in `B-brain/03-api-keys-registry.md` (don't share this file).

---

### "How do I automate the revision loop?"

Use `T-tools/02-prompts/BONUS/07-enable-auto-revision-loop.md`.

This sets up: Agent creates → Gatekeeper reviews → Agent revises (automatically).

Good for when you want less manual intervention.

---

### "Can I use this for multiple projects?"

Yes. Duplicate the folder.

1. Copy the entire ABC-TOM folder
2. Rename it (e.g., `client-project/`)
3. Fill with new context
4. Same system, different content

One system. Infinite projects.

---

## Still Stuck?

Type `/tom` and ask your question. Tom explains the system.

Want to build something new? Type `/adam`. Adam is your builder.

Or check:
- `@ALL-GUIDES-HERE/04-tom-agent-knowledge/system-guide.md` - Full system explanation
- `@ALL-GUIDES-HERE/04-tom-agent-knowledge/folder-guide.md` - Each folder explained
- The README in your project root

---

> **© Tom Even**
> Workshops: [www.getagents.today](https://www.getagents.today)
> Newsletter: [www.agentsandme.com](https://www.agentsandme.com)
