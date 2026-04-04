---
tags: [script, claude-cowork, video-3]
status: draft
---

## Video 3 — Chat vs Code vs CoWork

**Goal**: Viewer understands exactly when to use each Claude product so they stop wasting time and credits on the wrong tool.

---

### HOOK (0:00–0:30)

> "Claude has three products now — Chat, Code, and CoWork. And I see people using the wrong one constantly. They'll open CoWork to ask a simple question and burn through credits. Or they'll use Chat when they need CoWork to actually do something on their computer. In this video I'm going to give you a simple framework so you always pick the right tool."

---

### SECTION 1: The One-Sentence Version (0:30–1:30)

**On screen**: Three columns — Chat | Code | CoWork

> "Here's the simplest way to think about it."

- **Chat** = you ask, it answers. It's a conversation.
- **Code** = you describe software, it builds it. It's for developers.
- **CoWork** = you assign a task, it executes it on your computer. It's for everyone.

> "Chat talks. Code builds. CoWork works."

**Reference from competitors**: Bart uses almost this exact framing: "Claude chat is an assistant who answers questions. Claude Code is a developer who builds software. Claude CoWork is an employee who can complete tasks." Mikey says: "Cloud chat works, Cloud Code builds, and Cloud CoWork works."

---

### SECTION 2: When to Use Chat (1:30–4:00)

**On screen**: Switch to Claude Chat tab. Do a live demo.

> "Chat is your go-to for quick thinking tasks. Anything where you want an answer, not an action."

**Demo examples — do each one live**:

1. **Ask a question**: "What's the difference between an LLC and an S-Corp?"
   - Show the answer appearing
   - > "Fast, conversational, no file access needed."

2. **Brainstorm**: "Give me 10 video title ideas for a Claude CoWork tutorial"
   - Show the list
   - > "Perfect for ideation. You don't need CoWork to generate a list."

3. **Rewrite something**: Paste in a paragraph, ask it to rewrite in a different tone
   - > "Quick text editing — Chat handles this in seconds."

**When NOT to use Chat**:
> "Chat cannot access your files. It can't open your browser. It can't move things around on your computer. It can't connect to Gmail or your calendar. If your task requires any kind of action beyond generating text, Chat is the wrong tool."

**Cost note**:
> "Chat is also the cheapest option credit-wise. A quick question in Chat costs a fraction of what the same question in CoWork would cost. So don't use CoWork as an expensive chatbot."

---

### SECTION 3: When to Use CoWork (4:00–7:30)

**On screen**: Switch to CoWork tab. Do a live demo.

> "CoWork is for anything that requires Claude to take action on your machine or in your apps."

**Demo examples — do each one live**:

1. **File task**: "Organize the files in my Downloads folder by type"
   - Show CoWork actually moving files
   - > "This is the classic CoWork use case. It's not telling you how to organize — it's doing the organizing."

2. **Research + output**: "Research the top 5 project management tools, compare their pricing, and save a comparison table as an Excel file in my Documents folder"
   - Show CoWork browsing the web, gathering data, creating the file
   - > "It searched the web, compiled the data, and saved an actual file to my computer. Chat can't do any of that."

3. **App interaction**: "Check my Gmail for any unread emails from this week and draft replies to the important ones"
   - Show CoWork reading emails, drafting responses
   - > "It just read my actual inbox and drafted real replies. That's the power."

**When NOT to use CoWork**:
> "Don't use CoWork to ask simple questions. If you just want to know 'what is a P/E ratio' — use Chat. CoWork will spin up a whole task execution pipeline for a question that Chat answers in 2 seconds. You're wasting credits and time."

**The sub-agents advantage**:
> "One thing CoWork can do that Chat can't is run multiple things in parallel. If I ask it to research 5 competitors, it can spawn 5 sub-agents that each research one at the same time. Chat does everything sequentially."

---

### SECTION 4: When to Use Code (7:30–9:30)

**On screen**: Switch to Claude Code (terminal or desktop UI).

> "Code is specifically for building software. If you're a developer — or want to become one — this is where you go."

**Demo examples**:

1. **Build an app**: "Build me a Python script that scrapes prices from Amazon"
   - Show Code writing the script, running it in terminal
   - > "Code writes actual software, runs it, debugs it."

2. **Fix a bug**: Show a broken piece of code, ask Code to fix it
   - > "It reads the code, understands the error, writes the fix."

**When NOT to use Code**:
> "If you're not building software, Code is overkill. You don't need Code to organize your files or draft emails. That's CoWork territory."

**The overlap**:
> "Here's where it gets interesting. Code and CoWork can actually do a lot of the same things. Code can organize files, browse the web, run scripts — technically. But CoWork does it through a visual interface with a plan you can approve. Code does it through command-line tools. Same engine, different steering wheel."

**Reference from competitors**: Tim explains "to be honest, Code can pretty much do everything CoWork can do. The real difference is who it's designed to be used by. CoWork is for those who aren't familiar with development tools and the command line."

---

### SECTION 5: The Decision Framework (9:30–11:30)

**On screen**: A simple flowchart or decision tree.

> "Here's the framework I use every time."

**Question 1: Do I need Claude to take action, or just answer a question?**
- Just answer → **Chat**
- Take action → next question

**Question 2: Is the action about building software?**
- Yes, writing code → **Code**
- No, it's a task on my computer or in my apps → **CoWork**

**Question 3: Do I need this to run automatically on a schedule?**
- Yes → **CoWork** (scheduled tasks)
- No → CoWork for complex tasks, Chat for simple ones

**Practical examples — rapid fire**:

| Task | Tool | Why |
|------|------|-----|
| "What's the capital of France?" | Chat | Just a question |
| "Summarize this PDF" | Chat (paste it in) or CoWork (if it's on your computer) | Depends on where the file is |
| "Organize my desktop" | CoWork | Needs file access |
| "Build me a website" | Code | Software development |
| "Draft replies to my unread emails" | CoWork | Needs Gmail connector |
| "Rewrite this paragraph" | Chat | Just text transformation |
| "Every Monday, check my calendar and send me a summary" | CoWork | Scheduled task + app access |
| "Write a Python script" | Code | Software |
| "Research competitors and make a spreadsheet" | CoWork | Web research + file creation |

---

### SECTION 6: Credits & Cost (11:30–12:30)

**On screen**: Usage dashboard if available, or just talking head.

> "One thing nobody talks about enough is cost. CoWork uses significantly more credits than Chat for the same question. Here's why."

- Chat: sends your message, gets a response. One round trip.
- CoWork: creates a plan, executes multiple steps, may spawn sub-agents, interacts with files and apps. Many round trips.

> "A task that takes Chat 30 seconds and barely touches your credits might take CoWork 5 minutes and use 10x the credits. That's fine when CoWork is doing real work. It's wasteful when you're just asking it a question."

**Rule of thumb**:
> "If you can get your answer from Chat, always use Chat. Only escalate to CoWork when you need it to actually do something."

---

### OUTRO (12:30–13:00)

> "Now you know exactly when to reach for Chat, Code, or CoWork. Stop burning credits in CoWork for simple questions. Save it for the real work. In the next video, we're going to set up Projects — this is how you give CoWork persistent memory so it stops forgetting who you are every session."

---

### NOTES FOR FILMING

- This video needs clear visual separation between the three tools — consider color coding or labels
- Do quick live demos in each tool to show the difference viscerally, not just theoretically
- The decision framework table should be on screen long enough for viewers to screenshot it
- Keep the Code section brief — this is a CoWork course, Code is just for context
- Target length: ~13 minutes
