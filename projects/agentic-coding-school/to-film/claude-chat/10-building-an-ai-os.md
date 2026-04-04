---
tags: [script, claude-chat, video-10]
status: draft
---

## Video 10 — Building Your AI Operating System

**Goal**: Viewer combines everything from the course into one organized system — projects, memory, connectors, artifacts, and prompting techniques — creating a personal "AI OS" inside Claude.

---

### HOOK (0:00–0:30)

> "Over the last 9 videos you've learned every feature Claude has. Now I'm going to show you how to combine all of them into one system — a personal AI operating system. By the end of this video, you'll have Claude set up as your executive assistant, your content strategist, your researcher, and your analyst — all organized, all persistent, all working together."

---

### SECTION 1: The Architecture (0:30–2:30)

**On screen**: Diagram showing the full system.

> "Here's what we're building. It's a set of interconnected projects, each designed for a specific area of your life or work."

Show the structure:
```
MY AI OPERATING SYSTEM
│
├── Executive Assistant (project)
│   ├── Instructions: who I am, how I work, priorities
│   ├── Files: goals doc, one-pager about me
│   ├── Connectors: Gmail, Calendar, Drive
│   ├── Chats: Morning review, Weekly planning, Decision log
│   └── Memory: builds over time
│
├── Content Creation (project)
│   ├── Instructions: brand voice, audience, content rules
│   ├── Files: content calendar, style guide, audience data
│   ├── Chats: Ideation, Script writing, Research
│   └── Memory: what topics work, audience feedback
│
├── Business Operations (project)
│   ├── Instructions: business context, team, finances
│   ├── Files: P&L, client list, SOPs
│   ├── Chats: Finance review, Client work, Strategy
│   └── Memory: business decisions, metrics
│
└── Learning & Research (project)
    ├── Instructions: interests, learning goals
    ├── Chats: AI research, Industry analysis, Book notes
    └── Memory: key insights, reading list
```

> "Four projects. Each one has its own instructions, files, and memory. Together, they cover every major area of your work."

**Reference from competitors**: AI Edge sets up a similar system with "executive, AI Edge, lifestyle, crypto" projects. AI Foundations calls this the "AI operating system" and builds it as the core framework of the video. Both emphasize that projects + memory + files = persistent AI assistant.

---

### SECTION 2: Build Project 1 — Executive Assistant (2:30–6:00)

**On screen**: Creating the project live.

> "Let's build the most important one first: your executive assistant."

**Create the project**:
- Name: "Executive Assistant"
- Instructions:

```
You are my executive assistant. Your job is to help me stay organized, 
make good decisions, and manage my time effectively.

About me:
- [Name], [Role], based in [City/Timezone]
- I run [Business/Job description]
- My top priority right now: [Current focus]
- I work best in mornings. Protect my deep work time.

How to assist me:
- Be concise. I read fast and prefer bullet points.
- When I share a problem, ask me 2-3 clarifying questions before advising.
- For decisions, always give me a recommendation with reasoning — don't just list options.
- Flag things I might be forgetting or deprioritizing.

Communication preferences:
- Direct and honest. Don't sugarcoat.
- Use data when available. Opinions are fine but label them.
- If I'm overcomplicating something, tell me.
```

**Upload the one-pager**:
- Create a quick one-page doc with: your goals, current projects, team info, pain points
- Drag it into the project files

**Connect apps**:
- Gmail, Calendar, Drive (if not already connected)

**Create starter chats**:
1. "Morning Review" — for daily check-ins
2. "Weekly Planning" — for weekly priorities
3. "Decisions" — for when you need to think through something important

**Test it**:
In the Morning Review chat:
```
Good morning. Check my calendar for today and my email for anything urgent.
What should my top 3 priorities be today?
```
- Show Claude pulling from calendar and email
- Show a personalized, context-aware response

> "It knows my priorities from the instructions, checks my real calendar and email, and gives me actionable priorities. That's an executive assistant."

---

### SECTION 3: Build Project 2 — Content Creation (6:00–9:00)

**On screen**: Creating the second project.

> "Next: content creation. This is where I brainstorm, write, and research."

**Create the project**:
- Name: "Content"
- Instructions:

```
This project is for my content creation across YouTube, newsletters, and social media.

My brand voice:
- Casual but knowledgeable — like explaining to a smart friend
- Short sentences. No jargon.
- Direct. Say what I mean, not what sounds impressive.
- Use "you" and "I" — never "one should" or "users can"

My audience:
- Non-technical professionals aged 25-45
- They want practical AI skills, not theory
- They're busy — give them actionable takeaways

Content rules:
- YouTube titles: under 60 characters, include primary keyword
- Scripts: include [SHOW ON SCREEN] markers for B-roll
- Newsletters: under 800 words, one clear takeaway
```

**Upload files**:
- Content calendar
- Audience data / analytics
- Examples of past content that performed well

**Create starter chats**:
1. "Ideation" — brainstorming new content ideas
2. "Scripting" — writing video scripts and articles
3. "Research" — competitive research and trend analysis

**Test it**:
```
I want to make a video about how to use Claude for small business owners.
Before we write anything, interview me — ask questions about what angle 
I want to take and what my audience already knows.
```
- Show Claude asking smart follow-up questions
- > "It knows my audience and brand voice from the instructions. The questions it asks are tailored to my specific situation."

---

### SECTION 4: Build Project 3 — Business Ops (9:00–11:00)

**On screen**: Quick setup of the third project.

> "Third project: business operations. Where the real numbers live."

**Create the project** (move faster, same pattern):
- Name: "Business"
- Instructions: business context, team, financial goals
- Files: P&L spreadsheet, client list, SOPs
- Chats: "Finance Review," "Client Work," "Strategy"

**Test it**:
```
I uploaded my Q1 P&L. Analyze it and tell me:
1. How's revenue trending vs Q4?
2. Which expense categories grew the most?
3. What should I watch out for in Q2?
```
- Show Claude analyzing the spreadsheet with business context
- > "It's not just crunching numbers — it knows my business context from the instructions, so the analysis is relevant."

**Bonus: Create an artifact**
```
Create a financial dashboard from this P&L data. 
Monthly revenue trend, expense breakdown, and profit margin over time.
```
- Show the interactive dashboard
- > "Project instructions + real data + artifacts = a custom dashboard built in seconds."

**Reference from competitors**: AI Edge built a personal operating system with finances, task prioritization, and connected APIs. AI Foundations does an executive assistant project with multiple dedicated chats.

---

### SECTION 5: Build Project 4 — Learning (11:00–12:00)

**On screen**: Quick setup.

> "Last one: learning and research. A place to store insights and do deep dives."

- Name: "Learning"
- Instructions: your interests, what you're studying, how you learn best
- Chats: "AI Research," "Industry Analysis," "Book Notes"

**Test it**:
```
I just read an article claiming that AI will replace 40% of knowledge work by 2028.
Help me think critically about this claim. What evidence would support it? 
What would undermine it? What's the most likely reality?
```
- Show Claude thinking through it with extended thinking
- > "This is my thinking partner. I dump articles, ideas, and questions here and Claude helps me process them."

---

### SECTION 6: The Daily Workflow (12:00–14:00)

**On screen**: Walking through a typical day.

> "Here's how I actually use this system day to day."

**Morning (5 min)**:
- Open Executive Assistant → Morning Review chat
- "What's my day look like? Any urgent emails?"
- Get priorities and calendar briefing

**During work**:
- Working on content? Switch to Content project → Scripting chat
- Need to analyze data? Switch to Business project → Finance Review
- Found an interesting article? Drop it in Learning → AI Research

**Before a meeting**:
- Executive Assistant → ask Claude to prep a brief from email and calendar

**End of day (2 min)**:
- Executive Assistant → "Summarize what I worked on today. What should I tackle first tomorrow?"

> "The key is that each project maintains its own context and memory. My content project knows my brand voice. My business project knows my financials. My executive assistant knows my schedule. They don't bleed into each other."

---

### SECTION 7: Course Recap (14:00–15:00)

**On screen**: Full course summary.

> "Let's recap everything we covered."

1. **What is Claude** — installation, plans, interface tour
2. **Prompting** — the 5-part structure, ask it to ask you questions
3. **Models** — Opus for depth, Sonnet for daily use, Haiku for speed
4. **Web Search & Research** — quick lookups vs deep analysis
5. **Artifacts** — interactive dashboards, apps, documents
6. **Projects & Memory** — persistent workspaces with context
7. **Connectors** — Gmail, Calendar, Drive integration
8. **Extended Thinking** — deeper reasoning for complex problems
9. **Files & Documents** — PDF, spreadsheet, image analysis
10. **AI Operating System** — putting it all together

> "You went from signing up to having a full AI operating system. Four projects, real app connections, persistent memory, and a system that gets smarter the more you use it."

---

### OUTRO (15:00–15:30)

> "That's the complete Claude Chat course. Your AI OS is set up and ready. From here, it's about using it consistently — the more you chat, the more memory builds, and the better Claude gets at helping you. If you got value from this course, let me know in the comments what you built. I'll see you in the next one."

---

### NOTES FOR FILMING

- This is the capstone — energy should be high, building momentum
- Build all 4 projects live but move faster on projects 3 and 4 (viewers get the pattern)
- The daily workflow section is key — shows how it all connects in practice
- The system diagram at the start should be screenshot-worthy
- Target length: ~15 minutes
