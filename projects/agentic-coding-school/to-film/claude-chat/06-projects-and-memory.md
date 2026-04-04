---
tags: [script, claude-chat, video-6]
status: draft
---

## Video 6 — Projects & Memory

**Goal**: Viewer creates their first project, understands how memory works, and sets up an organized workspace so Claude remembers their context.

---

### HOOK (0:00–0:30)

> "Every time you start a new Claude chat, it forgets everything. Your name, your business, what you talked about yesterday — gone. Projects fix that. A project gives Claude a dedicated workspace with your files, your instructions, and persistent memory. After this video, Claude will know who you are from the first message."

---

### SECTION 1: The Problem (0:30–2:00)

**Demo the amnesia**:
- Start a new chat. Say: "My name is [name] and I run a YouTube channel about AI tools."
- Claude acknowledges
- Start ANOTHER new chat. Ask: "What's my name?"
- Claude: "I don't have any prior context about you."
- > "Clean slate every time. Frustrating if you're working on the same thing across multiple days."

---

### SECTION 2: What is a Project? (2:00–3:30)

> "A project is a folder inside Claude that holds three things."

1. **Instructions** — persistent rules Claude follows in every conversation within this project
2. **Files** — documents Claude can reference (brand guides, data, templates)
3. **Memory** — things Claude learns and remembers across conversations

> "Think of it like creating a dedicated workspace for a specific area of your life. A 'Business' project. A 'Content' project. A 'Side Project' project. Each one has its own context."

**Reference from competitors**: AI Edge sets up projects by topic — "executive assistant, AI Edge channel, lifestyle, crypto research." He emphasizes "think of projects as folders — that's basically what they are." AI Foundations creates a similar structure and builds an "AI operating system" around it.

---

### SECTION 3: Creating a Project — Step by Step (3:30–7:00)

**On screen**: Full screen recording.

**Step 1: Navigate to Projects**
- Click "Projects" in the left sidebar
- Click "New Project"

**Step 2: Name it**
- Example: "YouTube Channel" or "My Business" or "Executive Assistant"
- > "Name it after what this workspace is FOR, not something generic."

**Step 3: Write the description/instructions**

Type:
```
This project is for managing my YouTube channel about AI productivity tools.

About me:
- Name: [Name]
- Channel: [Channel Name]  
- Audience: non-technical professionals aged 25-45
- Upload schedule: Tuesdays and Fridays

How to work with me:
- Be concise and actionable
- Match my casual, direct tone
- Use bullet points over long paragraphs
- When creating content, think about what my audience needs to hear, not what sounds impressive

What to avoid:
- Corporate jargon (no "leverage," "synergize," "cutting-edge")
- Overly long responses unless I ask for detail
- Making assumptions about my audience — they're not developers
```

> "These instructions load into every conversation in this project. Claude reads them before it even looks at your message."

**Step 4: Upload files**
- Drag in relevant files: brand guide, content calendar, audience research
- > "Anything Claude should reference goes here. It can read PDFs, docs, spreadsheets, images."

**Step 5: Create the project**
- Click Create
- Show the new project interface

**Reference from competitors**: AI Edge recommends creating a "one-pager with details about you, your business, your objectives" and uploading it. "Some of mine are 3-6 pages." AI Foundations creates an elaborate "AI operating system" project with dedicated sub-chats.

---

### SECTION 4: Working Inside a Project (7:00–9:00)

**On screen**: Inside the project.

**Creating chats within a project**:
- Click "New chat" inside the project
- Each chat inherits the project's instructions and files
- > "Every conversation in this project already knows everything from your instructions and files."

**Demo the difference**:

Inside the project, type:
```
Write me 5 YouTube video titles about Claude's new features.
```
- Show the result — tailored to your audience, matching your tone

Outside the project (regular chat), type the same thing:
- Show the result — generic, no audience awareness

> "Same prompt, different context. The project instructions did all the work."

**Organizing chats**:
> "I create separate chats within a project for different purposes."

- "Brainstorming" — for ideation sessions
- "Script writing" — for actual content creation  
- "Analytics review" — for analyzing performance data
- "Admin" — for scheduling, planning

**Reference from competitors**: AI Edge does this exact organization: "create chat for brainstorming, create chat for day-to-day ops — set up your folders so everything is clearly differentiated."

---

### SECTION 5: Memory (9:00–11:30)

**On screen**: Memory panel.

> "Memory is where it gets really interesting. Claude now remembers things across conversations within a project."

**How memory works**:
- As you chat, Claude picks up on important facts about you and your work
- It saves these in a memory file that persists
- New conversations in the same project can access these memories

**Demo: Build memory**

In a chat, tell Claude things:
```
My most popular video has 50K views and it's about Claude Code for beginners.
My email list has 3,000 subscribers.
I'm planning to launch a paid course in Q3.
```

- Show Claude acknowledging
- Click on the Memory tab
- Show the memories being stored

**Start a new chat in the same project**:
```
What do you know about my channel performance and upcoming plans?
```
- Show Claude recalling the information from memory
- > "Different conversation, same project. It remembered everything."

**What memory stores**:
- Facts about you and your business
- Preferences you've expressed
- Decisions you've made
- Key metrics and data

**What memory doesn't store**:
- Entire conversation transcripts
- Temporary or one-off data
- Anything from outside this project

> "Memory builds over time. After a week of using a project, Claude will feel like it genuinely knows your situation."

**Reference from competitors**: AI Edge notes "Claude just expanded their memory window — it can read across a multitude of chats." Riley Brown covers auto-memory in Claude Code.

---

### SECTION 6: Project Organization Tips (11:30–13:00)

**On screen**: Example project setup.

> "Here's how I'd recommend organizing your projects."

**Recommended project structure** (3-5 projects to start):

1. **Executive Assistant / Personal** — daily tasks, planning, admin
2. **Business / Work** — strategy, operations, client work
3. **Content** — writing, ideas, scripts, research
4. **Learning** — courses, research, skill development

**Per project, upload these files**:
- A one-pager about yourself and your goals
- Any brand/style guidelines
- Relevant data (spreadsheets, reports)
- Templates you use repeatedly

**Rules of thumb**:
- Don't create too many projects — 5 max to start
- Put instructions that apply everywhere in each project's description
- Keep files updated as things change
- Check memory periodically — remove anything outdated

---

### OUTRO (13:00–13:30)

> "Projects give Claude persistent context, organized files, and growing memory. It's the difference between a stranger and a colleague who knows your business. In the next video, we're connecting Claude to your actual apps — Gmail, Calendar, Google Drive — so it can pull real data into your conversations."

---

### NOTES FOR FILMING

- The amnesia demo at the start is the pain point — make it frustrating
- The inside-project vs outside-project comparison should be dramatic
- Memory demo needs to show the actual memory panel with stored info
- Target length: ~13 minutes
