---
tags: [script, claude-cowork, video-5]
status: draft
---

## Video 5 — Instructions & Claude.md

**Goal**: Viewer understands the instruction hierarchy in CoWork (global → project → task) and writes instructions that actually influence behavior.

---

### HOOK (0:00–0:30)

> "The number one reason people get bad results from Claude CoWork is bad instructions. Not bad prompts — bad instructions. There's a difference. Your prompt is what you ask CoWork to do right now. Your instructions are what CoWork knows about you all the time. Get your instructions right and every single task gets better automatically. In this video I'll show you exactly how."

---

### SECTION 1: The Three Layers of Instructions (0:30–3:00)

**On screen**: Diagram showing three layers stacked.

> "CoWork has three layers of instructions, and they stack on top of each other. Understanding this hierarchy is the key to getting consistent results."

**Layer 1: Global Instructions**
- Apply to ALL CoWork sessions, across all projects
- Set in Settings → CoWork → Global Instructions
- > "This is your universal rules. Things like 'always ask before deleting files' or 'I prefer concise responses over detailed ones.' These apply everywhere."

**Layer 2: Project Instructions**
- Apply to all conversations within a specific project
- Set when you create a project (or edit later)
- > "This is your project-specific context. For a YouTube project: your channel name, audience, upload schedule, content style. For a client project: the client's name, brand voice, deliverables."

**Layer 3: Task Prompt**
- The specific instruction you type for this one task
- > "This is what you type in the chat box. It inherits everything from Layer 1 and Layer 2 automatically."

> "When you send a task, CoWork reads all three: your global instructions, then your project instructions, then your task prompt. They combine. So if your global instructions say 'be concise' and your project instructions say 'match a casual tone' and your task says 'write a blog post about AI' — you get a concise, casual blog post about AI."

---

### SECTION 2: Setting Up Global Instructions — Your Personal Profile (3:00–7:00)

**On screen**: Settings → CoWork → Global Instructions.

> "Global instructions are the most underrated feature in CoWork. This is your personal profile — it gets injected into EVERY session, across EVERY project. When this is set up right, Claude stops giving you generic advice and starts giving you advice tailored to your actual situation."

**Step 1: The before/after demo (show this FIRST)**

Ask CoWork WITHOUT any global instructions:
```
What's the best way to handle my growing workload? I'm falling behind on tasks.
```
- Show the generic response — "prioritize with Eisenhower matrix, hire a VA, use time blocking"
- > "Generic productivity advice you could find in any blog post. It doesn't know anything about me."

Now add global instructions (next steps) and ask the EXACT same question.

**Step 2: Navigate to settings**
- Click your avatar (bottom left)
- Click Settings
- Click CoWork
- Find "Global Instructions"

**Step 3: Write your personal profile**

> "This isn't just preferences — it's your identity. The more Claude knows about you, the more tailored every single response becomes."

Show typing in a comprehensive profile:

```
## About Me
- Name: [Name]
- Based in [City], [Timezone]
- I run a YouTube channel about AI tools (~30K subscribers)
- Revenue: ~$15K/month (courses + sponsorships + consulting)
- Team: just me + a part-time video editor
- Personality: direct, impatient with fluff, prefer speed over perfection

## Current Priorities
- Growing YouTube to 50K subscribers by end of Q3
- Launching a paid course on Claude
- Building an email list (currently 3K subscribers)
- Time is my bottleneck, not money — recommend the fastest option, not the cheapest

## How I Make Decisions
- I value speed and iteration over perfection
- Give me a recommendation with reasoning, don't just list options
- If something takes more than 2 hours, suggest breaking it into smaller pieces
- Challenge my assumptions if you think I'm wrong

## How I Want You to Work
- Be concise. Don't over-explain — I can read.
- Always ask before deleting any files
- Use descriptive file names (not "output.txt")
- If a task is ambiguous, ask me to clarify before starting
- Show your plan before executing anything destructive
- Save all work to the project folder, never to random locations
- Use markdown for documents, bullet points over paragraphs
```

**Step 4: Show the difference — same question, with profile**

Ask the exact same question:
```
What's the best way to handle my growing workload? I'm falling behind on tasks.
```

- Show the tailored response — it now considers: solo creator with a part-time editor, revenue level, time as the bottleneck, preference for speed
- It might suggest: "hire a second editor to free up your production time" instead of "use a to-do list"
- > "Completely different advice. It knows my revenue, my team, my bottleneck. It recommended hiring help because it knows money isn't my constraint — time is. Without the profile, it would have recommended free tools and time management techniques."

> "This is why global instructions matter. Every task, every project, every conversation — Claude now knows who it's working for."

**What goes in global (about YOU) vs project (about THE WORK)**:
- Global: your name, role, revenue, team, decision-making style, communication preferences
- Project: brand voice, audience details, workflow rules, file structure, current tasks
- > "If it's true about you regardless of what project you're in — it goes in global. If it's specific to one area of work — it goes in the project."

**Reference from competitors**: Bart sets up global instructions but doesn't separate them from project. Jack Roberts mentions "default screeners." Neither shows the before/after demo that proves the impact — this demo is the key differentiator.

---

### SECTION 3: Writing Project Instructions (5:30–9:00)

**On screen**: Inside a project, editing instructions.

> "Project instructions are where the real power is. This is what makes CoWork feel like it actually knows your business."

**Step 1: Open project instructions**
- Click the pencil icon next to instructions in the right panel
- Or navigate to project settings

**Step 2: Write structured instructions**

> "I'm going to show you the structure I use for every project. You can copy this template and fill in your own details."

Type in a complete example:

```
## Project: YouTube Channel Management

### Context
This project manages my YouTube channel [Channel Name]. 
I publish 2 videos per week (Tuesday and Friday).
My audience is non-technical professionals aged 25-45 who want to use AI tools.
My niche is AI productivity tools — specifically Claude, ChatGPT, and automation.

### My Brand Voice
- Casual but knowledgeable — like explaining to a smart friend
- Use "you" and "I" — never "one should" or "users can"
- Short sentences. No corporate jargon.
- Examples: "Here's the thing" / "Let me show you" / "This is where it gets interesting"
- Avoid: "leverage" / "utilize" / "synergy" / "cutting-edge"

### Workflow Rules
- Always save outputs to the /outputs folder
- Name files with dates: YYYY-MM-DD-description.md
- When researching competitors, check their last 5 videos minimum
- When writing scripts, include [SHOW ON SCREEN: ...] markers for B-roll
- Never publish or post anything without my explicit approval

### Key Files
- /context/brand-guide.md — full brand guidelines
- /context/content-calendar.md — upcoming video topics
- /context/audience-notes.md — notes on audience demographics and feedback

### Current Priorities
- Growing to 50K subscribers (currently at 30K)
- Expanding into non-developer content
- Building an email list
```

> "See how specific this is? I've told it about my audience, my voice, my workflow rules, my file naming conventions, and my current priorities. Every conversation in this project will have this context from the start."

**Step 3: Show the impact**

Do a before/after demo:

**Without project instructions** — start a new task outside the project:
```
Write me a YouTube video title about Claude CoWork
```
- Show the generic result (probably formal, generic titles)

**With project instructions** — start a task inside the project:
```
Write me a YouTube video title about Claude CoWork
```
- Show the result that matches your brand voice, considers your audience
- > "See the difference? Same prompt, completely different result. The project instructions did all the heavy lifting."

---

### SECTION 4: Claude.md Files — Global and Local (9:00–13:00)

**On screen**: Finder showing file paths.

> "There's one more way to give CoWork instructions that most people don't know about: Claude.md files. And there are actually TWO types."

**Two types of Claude.md files**:

1. **Global CLAUDE.md** — lives at `~/.claude/CLAUDE.md`
   - Injected into EVERY session, EVERY project, EVERY conversation
   - This is like a supercharged version of your global instructions
   - Perfect for your full personal profile, reasoning strategies, and universal rules

2. **Local/Project CLAUDE.md** — lives in a project's folder
   - Only read when working inside that specific project folder
   - Perfect for project-specific workflows, file structure, and conventions

> "The global one is about YOU. The local one is about THE PROJECT. Together with the settings-based instructions, you have a complete hierarchy."

**Demo: The Global CLAUDE.md (~/.claude/CLAUDE.md)**

**Step 1: Find the file**
- On Mac: the `.claude` folder is hidden in your home directory
- Show pressing Shift+Cmd+Period in Finder to reveal hidden files
- Navigate to `~/.claude/`
- Open (or create) `CLAUDE.md`

> "This file is hidden by default. Most people don't even know it exists."

**Step 2: Write a global CLAUDE.md**

> "This is where you can go deeper than the settings-based global instructions. I put my full personal profile, my reasoning strategies, and my token conservation rules here."

Show writing:

```markdown
# Personal Profile

## Role & Context
- Solo YouTube creator and course builder
- Revenue: ~$15K/month (courses 60%, sponsorships 30%, consulting 10%)
- Team: me + part-time video editor
- Based in [City], [Timezone]
- Time is my bottleneck, not money

## Decision-Making Style
- Default to the fastest option, not the cheapest
- I prefer 80% done now over 100% done next week
- When presenting options, give me your recommendation first, then alternatives
- Challenge my thinking — don't just agree with me
- If I'm overcomplicating something, say so directly

## Communication Preferences
- Be concise — bullet points over paragraphs
- Don't summarize what you just did at the end of every response
- Don't over-explain things I already understand
- If something takes 1 sentence to say, don't use 3

## Token Conservation
- Use one write operation instead of many sequential edits
- Fetch API docs before attempting unfamiliar tools
- Don't add comments, docstrings, or type annotations to code you didn't change
- Don't refactor surrounding code when fixing a specific issue
```

> "This is powerful. Every conversation now inherits this. If I ask for business advice, it knows my revenue and team size. If I ask for a recommendation, it gives me the fastest option. If I'm rambling, it'll push back."

**Step 3: Using /insights to discover what to add**

> "Here's a trick nobody talks about. If you've been using CoWork or Claude Code for a while, you can use /insights to see patterns in how you work. Things like: what tools you use most, what kind of tasks you do repeatedly, what conventions you follow. Use those insights to update your global CLAUDE.md."

- Show running /insights (or mention it for Code users)
- > "But here's the critical thing: manually review before adding. Don't let Claude auto-update your global file without you reading it. This is the compound probability problem — if Claude generates instructions, and then another session of Claude reads and interprets those instructions, errors compound. An AI reviewing AI reviewing AI means small mistakes snowball. YOU need to be the human in the loop for your global profile."

**Demo: The Local/Project CLAUDE.md**

> "Now let's do the project-level one. This lives in the project folder and only applies to that project."

Show creating a CLAUDE.md file in the project folder:

```markdown
# YouTube Channel Project

## File Organization
- /scripts/ — video scripts in progress
- /research/ — competitor analysis and topic research  
- /outputs/ — finished deliverables (thumbnails, descriptions, etc.)
- /templates/ — reusable templates for recurring tasks

## Video Production Workflow
1. Research topic (save to /research/)
2. Write outline (save to /scripts/)
3. Write full script (save to /scripts/)
4. Generate thumbnail concepts (save to /outputs/)
5. Write video description and tags (save to /outputs/)

## SEO Rules
- Titles: 50-60 characters, include primary keyword
- Descriptions: first 150 characters are most important
- Tags: 10-15 relevant tags, mix broad and specific
- Always include a CTA in the first paragraph of the description
```

> "Now every time I start a task in this project, CoWork reads the global CLAUDE.md first — my personal profile — then this project CLAUDE.md — the YouTube-specific rules. I never have to explain who I am OR how this project works."

**The complete hierarchy (recap)**:

```
1. Global CLAUDE.md (~/.claude/CLAUDE.md) — who YOU are
2. Global Instructions (Settings → CoWork) — universal preferences  
3. Project Instructions (project settings) — project context
4. Project CLAUDE.md (project folder) — detailed project rules
5. Task Prompt — what you want done RIGHT NOW
```

> "All five layers stack. CoWork reads them top to bottom before executing your task. The more context at the top, the less you need to repeat at the bottom."

---

### SECTION 5: Common Mistakes (13:00–14:30)

**On screen**: List of mistakes with corrections.

> "Here are the mistakes I see most often with instructions."

**Mistake 1: Instructions that are too vague**
- Bad: "Be helpful and professional"
- Good: "Write in a casual, first-person voice. Use short sentences. Address the reader as 'you'."
- > "Vague instructions get vague results. Be specific about behavior."

**Mistake 2: Putting task-specific stuff in project instructions**
- Bad: "Write me a blog post about Claude CoWork" (in project instructions)
- Good: Keep project instructions about WHO you are and HOW you work, not WHAT to do right now
- > "Instructions are persistent context. Tasks are one-time requests. Don't mix them."

**Mistake 3: Never updating instructions**
- > "Your instructions should evolve. After a week of using a project, go back and update your instructions based on what worked and what didn't. Add new rules. Remove ones that don't matter."

**Mistake 4: Writing a novel**
- > "CoWork reads your instructions every time. If you wrote 5 pages, it's processing all of that before it even looks at your task. Keep instructions focused and scannable. Use headers, bullet points, and short lines."

**Reference from competitors**: Ryan & Matt note the instruction editing interface is small, recommending you write externally and paste in. Good tip to include.

---

### SECTION 6: The Instructions Checklist (14:30–15:30)

**On screen**: Checklist graphic.

> "Before you move on, make sure you have these set up."

- [ ] Global CLAUDE.md (`~/.claude/CLAUDE.md`) with your full personal profile
- [ ] Global instructions (Settings) with universal work preferences
- [ ] Project instructions for your main project with context, voice, and workflow rules
- [ ] A project CLAUDE.md file with detailed workflows and conventions
- [ ] Test it — start a new conversation and ask CoWork something that proves it read your instructions

> "If CoWork knows your name, your revenue, your decision-making style, and your project workflows without you telling it — your instructions are working."

---

### OUTRO (15:30–16:00)

> "Instructions are the foundation of everything in CoWork. Get them right and every task, every skill, every scheduled task inherits that context automatically. The personal profile in your global CLAUDE.md is the single highest-leverage thing you can set up — it changes every conversation from generic to tailored. In the next video, we're connecting CoWork to your apps — Gmail, Calendar, Google Drive, Slack — so it can start doing real work beyond just your files."

---

### NOTES FOR FILMING

- The before/after demo (generic advice vs tailored advice) is the money shot — do it FIRST in the global instructions section, same question asked twice
- Show navigating to the hidden ~/.claude/ folder (Shift+Cmd+Period on Mac)
- Show the actual settings screen for global instructions AND the CLAUDE.md file — viewers need to see both
- When typing the personal profile, go slow enough for viewers to read and screenshot
- The 5-layer hierarchy recap at the end of Section 4 should be a clear diagram on screen
- Mention /insights briefly but don't belabor it — it's a power-user tip
- The compound probability warning is important — emphasize human review for global files
- Target length: ~16 minutes
