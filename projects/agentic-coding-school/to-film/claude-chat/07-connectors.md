---
tags: [script, claude-chat, video-7]
status: draft
---

## Video 7 — Connectors (Gmail, Calendar, Drive)

**Goal**: Viewer connects their Google Workspace to Claude and runs real workflows pulling from their actual email, calendar, and files.

---

### HOOK (0:00–0:30)

> "What if Claude could actually read your emails, check your calendar, and pull files from your Google Drive — without you copying and pasting anything? That's what Connectors do. In this video I'm connecting Gmail, Calendar, and Drive, and showing you what becomes possible when Claude has access to your real data."

---

### SECTION 1: What Are Connectors? (0:30–2:00)

**On screen**: Connectors panel.

> "Connectors let Claude talk directly to your apps. Instead of you downloading a file and uploading it to Claude, Claude just reads it from the source."

**How to access**:
- Click "+" on the chat input
- Click "Connectors"
- Click "Manage connectors"

**Available connectors**:
- Gmail
- Google Calendar
- Google Drive
- (More being added — Notion, Slack, etc.)

> "Right now the main ones are Google Workspace — Gmail, Calendar, Drive. Anthropic is adding more over time."

**Reference from competitors**: AI Edge calls connectors "underrated" and notes "you can connect to Gmail, Google Calendar, or Google Drive — so it can pull things for you without keep getting documents and loading them in."

---

### SECTION 2: Connecting Gmail (2:00–4:00)

**Step by step**:
1. Manage Connectors → Find Gmail → Click Connect
2. Google sign-in flow
3. Approve permissions
4. Done

**Test it**:
```
How many unread emails do I have? List the 5 most recent with subject and sender.
```
- Show real email data appearing

**What Gmail can do**:
- Read your emails
- Search for specific emails
- Draft replies (saves as draft, doesn't send)
- > "Claude can read your inbox but it won't send emails on your behalf without asking."

---

### SECTION 3: Connecting Calendar (4:00–5:30)

**Same flow** — Connect → Sign in → Approve.

**Test it**:
```
What's on my calendar for the rest of this week?
```
- Show real calendar events

**What Calendar can do**:
- Read your events
- Check availability
- Create new events
- > "Ask Claude to schedule a meeting and it'll check your availability first."

---

### SECTION 4: Connecting Google Drive (5:30–7:00)

**Same flow**.

**Test it**:
```
Find the most recently modified document in my Drive and summarize it.
```
- Show Drive file being accessed and summarized

**What Drive can do**:
- Search your files
- Read document contents
- Find specific information across files

---

### SECTION 5: Real Workflows (7:00–11:00)

> "Now that everything's connected, here's where it gets useful."

**Workflow 1: Email briefing**
```
Check my Gmail for the most important unread emails from the last 48 hours.
Categorize them: urgent, needs reply, FYI, and spam.
For urgent ones, draft a short reply.
Summarize everything in a clean bullet-point format.
```
- Show Claude reading real emails and categorizing them

**Workflow 2: Meeting prep**
```
I have a meeting with [name] tomorrow. 
Check my email history for any recent conversations with them.
Check my Drive for any shared documents.
Prepare a brief: what we last discussed, any open items, and talking points.
```
- Show Claude pulling from both email and Drive

**Workflow 3: Weekly planning**
```
Look at my calendar for next week.
Check my email for anything that might affect my schedule.
Create a weekly plan with my top 3 priorities and any prep I need to do for meetings.
```
- Show Claude combining calendar and email data

> "In 2 minutes, Claude just checked my email, read my calendar, and gave me a weekly plan based on real data. Not hypothetical — my actual schedule and my actual emails."

---

### SECTION 6: Tips & Caveats (11:00–12:00)

- **Privacy**: Claude reads your data to answer your question, then doesn't store it beyond the conversation
- **Start focused**: Don't connect everything at once. Start with the one you'll use most (usually Gmail)
- **Combine with projects**: Use connectors inside a project for maximum context
- **Don't over-rely**: For sensitive emails, always review Claude's interpretation

---

### OUTRO (12:00–12:30)

> "Claude now has access to your email, calendar, and files. Combined with projects and memory, it's starting to feel like a real assistant. In the next video, we're going to look at Extended Thinking — Claude's ability to reason through complex problems step by step before giving you an answer."

---

### NOTES FOR FILMING

- Blur sensitive email content during screen recording
- The meeting prep demo is the most relatable — everyone has meetings they're underprepared for
- Keep connector setup fast — it's the same flow repeated, don't belabor it
- Target length: ~12 minutes
