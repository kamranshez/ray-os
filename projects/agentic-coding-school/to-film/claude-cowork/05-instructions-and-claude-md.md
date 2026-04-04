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

### SECTION 2: Setting Up Global Instructions (3:00–5:30)

**On screen**: Settings → CoWork → Global Instructions.

**Step 1: Navigate to settings**
- Click your avatar (bottom left)
- Click Settings
- Click CoWork
- Find "Global Instructions"

**Step 2: Write your global instructions**

> "These should be things that are true about you regardless of what project you're working on."

Show typing in example:

```
About me:
- My name is [Name]
- I'm based in [City/Timezone]

How I want you to work:
- Be concise. Don't over-explain.
- Always ask before deleting any files
- When creating files, use descriptive names (not "output.txt")
- If a task is ambiguous, ask me to clarify before starting
- Show me your plan before executing anything destructive
- Save all work to the project folder, never to random locations

Formatting:
- Use markdown for any documents
- Use bullet points over paragraphs when possible
```

> "Notice I'm not putting project-specific stuff here. No mention of YouTube or clients or specific work. That goes in project instructions. Global is for universal preferences."

**Reference from competitors**: Bart sets up global instructions but doesn't separate them from project instructions, which leads to confusion. Jack Roberts mentions "you can add default screeners for you" in global settings. Show the clear separation.

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

### SECTION 4: Claude.md Files (9:00–11:30)

**On screen**: Finder showing a CLAUDE.md file in a project folder.

> "There's one more way to give CoWork instructions that most people don't know about: Claude.md files."

**What is a Claude.md file?**
> "If you put a file literally called CLAUDE.md in your project folder, CoWork will automatically read it at the start of every task. It works like project instructions, but it lives as a file on your computer instead of in the CoWork settings."

**When to use Claude.md vs project instructions**:
- Project instructions: quick preferences, things you edit often
- Claude.md: detailed reference material, structured documentation, version-controlled instructions

**Demo: Create a Claude.md file**

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

> "Now every time I start a task in this project, CoWork has read this file and knows my entire workflow, my folder structure, and my SEO rules. I never have to explain it again."

---

### SECTION 5: Common Mistakes (11:30–13:00)

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

### SECTION 6: The Instructions Checklist (13:00–14:00)

**On screen**: Checklist graphic.

> "Before you move on, make sure you have these set up."

- [ ] Global instructions with your name, timezone, and universal preferences
- [ ] Project instructions for your main project with context, voice, and workflow rules
- [ ] A CLAUDE.md file in your project folder with detailed reference material
- [ ] Test it — start a new conversation and ask CoWork something that proves it read your instructions

> "If CoWork knows your name, your audience, and your preferred style without you telling it — your instructions are working."

---

### OUTRO (14:00–14:30)

> "Instructions are the foundation of everything in CoWork. Get them right and every task, every skill, every scheduled task inherits that context automatically. In the next video, we're connecting CoWork to your apps — Gmail, Calendar, Google Drive, Slack — so it can start doing real work beyond just your files."

---

### NOTES FOR FILMING

- The before/after demo is the money shot — make the difference dramatic
- Show the actual settings screen for global instructions, not just talking about it
- When typing instructions, go slow enough that viewers can read along
- The Claude.md file creation should show it in Finder AND show CoWork reading it
- Target length: ~14 minutes
