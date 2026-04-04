---
tags: [script, claude-cowork, video-4]
status: draft
---

## Video 4 — Projects & Memory

**Goal**: Viewer creates their first project, understands memory, and sees how CoWork finally stops forgetting everything between sessions.

---

### HOOK (0:00–0:30)

> "Every time you open Claude CoWork, it starts from zero. It doesn't remember your last task. It doesn't know your name. It doesn't know your business. And you're re-explaining yourself every single session. Projects fix that. In this video I'm going to show you how to create a project that gives CoWork persistent memory — so it knows your context from the first message, every time."

**Reference from competitors**: Ryan & Matt open with this exact pain point. Jack Roberts frames it as "without projects, we have to re-explain context every single chat."

---

### SECTION 1: The Problem — No Memory (0:30–2:30)

**On screen**: CoWork with two separate tasks.

**Demo the problem live**:

1. Open a new CoWork task
2. Say: "My name is [your name] and I run a YouTube channel about AI tools"
3. Let it respond
4. Now open a SECOND new task
5. Say: "What's my name and what do I do?"
6. Show it saying "This is the start of our conversation — I don't have any prior context"

> "See? Complete amnesia. Every new task is a blank slate. If you're doing one-off tasks, that's fine. But if you're working on the same project over days or weeks, re-explaining your context every time is exhausting and wastes credits."

**Reference from competitors**: Tim demos this exact scenario — opens a new task and asks "what did I just ask you to do?" and shows CoWork doesn't know.

---

### SECTION 2: What is a Project? (2:30–4:00)

**On screen**: CoWork projects section.

> "A project is a dedicated workspace inside CoWork. It has three things that make it different from just selecting a folder."

1. **Persistent instructions** — rules and context that apply to every conversation in this project
2. **Memory** — CoWork remembers things across conversations within the project
3. **A dedicated folder** — all files, outputs, and context live in one place on your computer

> "Think of a project like hiring an employee for a specific role. You give them a job description (instructions), they learn over time (memory), and they have their own desk and filing cabinet (folder)."

---

### SECTION 3: Creating Your First Project — Step by Step (4:00–9:00)

**On screen**: Full screen recording.

**Step 1: Navigate to Projects**
- In the CoWork sidebar, scroll to the bottom
- Click the "+" next to Projects, or go to the folder dropdown and select "Projects" at the bottom
- > "It's a bit hidden right now. You have to scroll down or click the folder dropdown. I expect Anthropic will make this more prominent soon."

**Reference from competitors**: Ryan & Matt note "to select a project, you're going to have to go over here, click on this dropdown, and go all the way to the bottom. I 100% anticipate in the future we're going to see projects here on this sidebar."

**Step 2: Choose how to start**
- Show the three options:
  - **Start from scratch** — set up a new folder with instructions
  - **Import a file** — bring in a project from Chat
  - **Use an existing folder** — point to a folder you already work from

> "For your first project, go with 'Start from scratch.' We'll use an existing folder later once you understand how projects work."

**Step 3: Name your project**
- Type a descriptive name (e.g., "YouTube Channel" or "Weekly Reporting" or "Client Work")
- > "Pick something specific. Not 'My Stuff' — that's too vague. 'Client Invoices' or 'YouTube Channel' — something that tells you what this workspace is for."

**Step 4: Write your instructions**
- This is the most important step
- Show the instructions text area
- Type in example instructions:

```
This project is for managing my YouTube channel about AI tools.

About me:
- My name is [Name]
- I run a YouTube channel called [Channel Name]
- My audience is non-technical professionals who want to use AI

How you should work:
- Always be concise and actionable
- When creating content, match my casual but informative tone
- Save all outputs to the /outputs subfolder
- Ask clarifying questions before starting large tasks

What you should never do:
- Don't use corporate jargon
- Don't create files outside the project folder
- Don't make assumptions about my audience — they're not developers
```

> "These instructions get loaded into every conversation you have inside this project. CoWork reads them before it starts any task. This is what stops it from forgetting who you are."

**Reference from competitors**: Bart creates three MD files — about-me, brand-voice, working-preferences. Jack Roberts sets up instructions with tone, rules, and output format. Ryan & Matt show the instructions panel on the right side. All slightly different approaches, same idea.

**Step 5: Add files (optional)**
- Drag in any relevant files — brand guidelines, templates, reference docs
- > "If you have files that CoWork should always have access to — like brand guidelines or a client brief — drop them in here."

**Step 6: Choose project location**
- Show the folder path (defaults to Documents/Claude/Projects)
- > "This is where the actual files live on your computer. You can change it, but the default is fine."

**Step 7: Click Create**
- Show the project being created
- Show the new UI with:
  - Instructions panel on the right
  - Memory section
  - Scheduled tasks area
  - Conversations list

> "Notice the interface changed. You now have your instructions on the right, a memory section, and a list of conversations. This is your workspace."

---

### SECTION 4: Using Memory (9:00–12:00)

**On screen**: Inside the project, start a conversation.

> "Now let's see memory in action."

**Demo 1: Save something to memory**

Type:
```
Remember that my upload schedule is every Tuesday and Friday at 9am EST.
```

- Show CoWork confirming it saved this
- Click on the Memory tab in the right panel
- Show the memory entry appearing

> "It just created a memory file. This will persist across every conversation in this project. Next time I ask about my upload schedule, it already knows."

**Demo 2: Prove memory works across conversations**

- Start a NEW conversation within the same project
- Type: "When do I upload videos?"
- Show CoWork answering correctly from memory

> "Different conversation, same project. It remembered. This is the game changer."

**Demo 3: Memory builds over time**

> "The more you use a project, the more it learns. Every time you tell it something about your preferences, your business, your workflow — it saves it. After a week of use, it knows you well enough that you barely need to explain anything."

**What memory stores vs what it doesn't**:
- Stores: facts about you, preferences, project details, decisions you've made
- Doesn't store: entire conversation transcripts, temporary data, one-off questions

---

### SECTION 5: Project vs Just Selecting a Folder (12:00–13:30)

**On screen**: Side-by-side comparison.

> "I want to clear up a common confusion. Selecting a folder and creating a project are NOT the same thing."

| | Selecting a Folder | Creating a Project |
|---|---|---|
| File access | Yes | Yes |
| Persistent instructions | No | Yes |
| Memory across conversations | No | Yes |
| Scheduled tasks | No | Yes (built in) |
| Dedicated UI | No | Yes |

> "If you just click 'Work in a folder' and select your Desktop, you get file access. That's it. No memory, no instructions, no project structure. You're back to the amnesia problem."

> "Always create a project if you're going to work on something more than once."

**Reference from competitors**: Ryan & Matt demo this exact distinction — they select a folder without a project and show the UI is completely different, no memory, no scheduled tasks.

---

### SECTION 6: Recommended Project Structure (13:30–15:00)

**On screen**: Finder showing a project folder structure.

> "Here's how I'd recommend setting up your project folders."

Show a structure like:
```
My-Project/
├── context/          ← background docs, brand guides, reference material
├── projects/         ← active work organized by task
├── outputs/          ← finished deliverables
└── memory/           ← CoWork manages this automatically
```

> "The context folder is for things CoWork should reference — your brand guide, a client brief, style examples. The projects folder is for active work. Outputs is where finished deliverables go. And memory is managed by CoWork automatically."

**Reference from competitors**: Bart has CoWork create this exact structure — "context, projects, output" subfolders with readme files explaining each one.

**How many projects should you have?**

> "Don't go overboard. 3 to 5 projects max to start. One for your business, one for content creation, maybe one for a specific client. If you create 15 projects you'll never use most of them."

**Reference from competitors**: Jack Roberts recommends "never have more than seven to eight. If your categories exceed eight, you've likely gone too far."

---

### OUTRO (15:00–15:30)

> "You now have a project with persistent instructions and memory. CoWork knows who you are, what you do, and how you like to work. In the next video, we're going deep on instructions and Claude.md files — because the quality of your instructions determines the quality of everything CoWork does for you."

---

### NOTES FOR FILMING

- Show the amnesia demo first — it's the pain point that motivates everything else
- The project creation walkthrough needs to be click-by-click, no skipping
- Memory demo should feel magical — start a new conversation and show it remembering
- The folder vs project comparison table should be on screen for a screenshot moment
- Target length: ~15 minutes
