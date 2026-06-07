### Preparation: Installing the Project Files

1. Download the ZIP file and extract it.
2. Drag the extracted folder into your Obsidian Vault.
3. On Windows? It sometimes creates an extra ".obsidian" folder inside the Vault. Ignore it.
4. Make sure you can see all folders (A-agents, B-brain, C-core, T-tools, etc.) in the left sidebar in Obsidian. They're inside the the-system folder you extracted from the ZIP file.

### Preparation: Opening Claude Code

4. Open a new session in Claude Code.
5. **Important:** Select the the-system folder as your working directory. This is how Claude knows where to read, edit, and create files.

---

### Step 1: Choose Your Track

Before you start, pick the track that fits your work:

**Content** (תוכן)
Social media posts, blog posts, articles, newsletters, content creation.
*For: marketers, designers, creators, anyone who publishes content. Also great for leaders sharing thought leadership or managers writing team updates.*

**Sales** (מכירות)
Client proposals, offers, follow-up emails, sales communication.
*For: founders, freelancers, consultants, anyone who writes to clients.*

**Thinking** (חשיבה)
Decision briefs, meeting summaries, user interview summaries, PRDs, stakeholder updates.
*For: PMs, CEOs, business owners, managers, team leads, anyone who organizes information and makes decisions. Also great for board updates, quarterly reviews, and strategy memos.*

**Not sure which to pick?** Ask yourself:
- Do you publish things people read? → **Content**
- Do you write to clients and sell? → **Sales**
- Do you make decisions and summarize information? → **Thinking**

---

## Phase 1: Feed the Brain

*Do this in Obsidian first — before running any prompts. Just fill in the two files below.*

### Step 2: Fill in Your Information

Open the file `B-brain/01-about-me.md`

Fill in the text with your information (copy-paste from the document you filled in beforehand).

**Don't have a "business"?** No problem. This works for anyone:
- If you work at a company: write about your role, your team, and the people you serve
- If you're a freelancer: write about what you do and who your clients are
- If you're exploring: write about what you want to create and who it's for

**Do not change file names.** The prompts are linked to them.

### Step 3: Add Your Writing Samples

Open the samples folder that matches your track:
- **Content** → `B-brain/02-my-samples/01-content/`
- **Sales** → `B-brain/02-my-samples/02-sales/`
- **Thinking** → `B-brain/02-my-samples/03-thinking/`

Each folder has a README explaining exactly what to paste. Read it first.

Paste your text (Hebrew or English) into each of the 3 files: `sample-01`, `sample-02`, `sample-03`.

**Pro tip:** The better your samples, the better the output. Pick pieces you're proud of.

✋ **Finish both steps above before moving on. Don't run any prompts yet.**

---

## Phase 2: Run Your New Team

*Now go to Claude Code. Run one prompt at a time. Wait for it to finish before pasting the next one.*

All 4 prompts are inside your track folder: `T-tools/02-prompts/[your-track]/`

**Prompt 1. Learn About Me**

- Copy the entire content of `01-learn-about-me.md`
- Paste it in Claude Code and send.
- Claude reads your answers and automatically updates the C-core files: `project-brief`, `icp-profile`, `voice-dna`.

**Prompt 2. Learn My Writing Style**

- Copy `02-learn-my-style.md` and paste it.
- Claude reads the 3 samples and updates the Core documents, the agents, and Memory.

**Prompt 3. Create Your Output**

- Copy the `03-...` file from your track folder and paste it.
- Fill in the details (your topic, client situation, or raw material depending on the track).
- Adam (your COO agent) manages the entire team to create the output.

What each track produces:

- **Content** Choose: social media post, blog post, or newsletter article. 3 agents collaborate: Researcher finds angles → Copywriter writes in your voice → Gatekeeper reviews quality.
- **Sales** A tailored client proposal or offer. 3 agents collaborate: Strategist analyzes the client situation → Copywriter writes in your voice → Gatekeeper reviews quality.
- **Thinking** Choose: decision brief OR document summary.
  - Decision brief: 4 agents debate your decision (Strategist → Devil's Advocate → Chief of Staff → Gatekeeper)
  - Summary: 3 agents process your raw material (Analyst → Copywriter → Gatekeeper)

**Prompt 4. Close The Loop**

- Copy `04-close-the-loop.md` and paste it.
- Adam reviews what was just created, logs what worked and what didn't to M-memory, and promotes strong insights to C-core.
- This is what makes the system get smarter over time.

---

### Important Tip: Permissions

When Claude asks for permission to read or edit files, click **"Allow always for session"** so you don't have to approve each action separately.

---

### What Happens Next?

- Your output is saved in the `O-output/` folder as a new file. You can read it both in Obsidian and in Claude's chat.
- Want to keep going? There are 9 bonus prompts (05-13) in `T-tools/02-prompts/BONUS/` for creating new agents, skills, API connections, and more.
- You can also try a different track. Pick a different track folder and run Prompt 3 again to see the same system produce a completely different output.
- **Tip:** Got a file and not sure where it goes? Drop it in `B-brain/04-INBOX/`. It's your junk drawer. Sort it later, or ask Claude to sort it for you.

Yalla, good luck.
