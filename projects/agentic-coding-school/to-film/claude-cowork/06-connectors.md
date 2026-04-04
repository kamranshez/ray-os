---
tags: [script, claude-cowork, video-6]
status: draft
---

## Video 6 — Connectors

**Goal**: Viewer connects Gmail, Google Calendar, Google Drive, and Slack to CoWork and runs a real workflow using connected apps.

---

### HOOK (0:00–0:30)

> "So far CoWork can organize your files and browse the web. But the real power comes when you connect it to the apps you actually use every day — Gmail, Calendar, Drive, Slack. Once it's connected, CoWork can read your emails, check your schedule, move files in Drive, and post to Slack. In this video, I'm connecting everything and showing you what becomes possible."

---

### SECTION 1: What Are Connectors? (0:30–2:00)

**On screen**: CoWork Customize → Connectors panel.

> "Connectors are how CoWork talks to your apps. They're built-in integrations — no coding, no API keys. You click connect, sign in, and you're done."

**Navigate to connectors**:
- Click "Customize" in the left sidebar
- Click "Connectors"
- Show the list of available connectors

> "You'll see a list of apps you can connect. Gmail, Google Drive, Google Calendar, Slack, GitHub, Canva, Notion, and more. Anthropic keeps adding new ones."

**Key concept: Permissions**

> "When you connect an app, CoWork doesn't get unlimited access. Each connector has specific permissions you can control — read, write, create, delete. You decide what it's allowed to do."

**Reference from competitors**: Jack Roberts walks through connector permissions for Gmail — "I'm going to let it create Gmail drafts freely because there's no issue in doing that. Won't let you send. That's for your protection." Brock shows Gmail, Slack, Google Calendar all connected. Include the permission granularity.

---

### SECTION 2: Connecting Gmail — Step by Step (2:00–5:00)

**On screen**: Full screen recording of the connection process.

**Step 1: Click "Browse Connectors"**
- Find Gmail in the list
- Click Connect

**Step 2: Google sign-in**
- Show the Google OAuth flow
- Sign in with your Google account
- Approve the permissions

**Step 3: Set permissions**
- Show the permission toggles:
  - **Read emails**: Allow (you want CoWork to read your inbox)
  - **Create drafts**: Allow (so it can draft replies for you)
  - **Send emails**: Needs approval (you want to review before sending)
  - **Delete emails**: Block (don't let it delete anything)
- > "I always set 'send' to 'needs approval.' I want to see every email before it goes out. Drafts are fine — I can review those. But sending? I want final say."

**Step 4: Test it**

Go back to a CoWork task and type:
```
Check my inbox and tell me how many unread emails I have. 
List the 5 most recent ones with subject lines and senders.
```

- Show CoWork reading the actual inbox
- Show results with real (or demo) email subjects

> "It just read my actual Gmail inbox. Not a simulation — my real emails. That's the connector working."

---

### SECTION 3: Connecting Google Calendar (5:00–6:30)

**On screen**: Same flow for Calendar.

**Quick walkthrough** (same pattern as Gmail):
- Browse Connectors → Google Calendar → Connect → Sign in → Set permissions

**Permissions**:
- Read events: Allow
- Create events: Allow
- Modify events: Needs approval
- Delete events: Block

**Test it**:
```
What's on my calendar for today and tomorrow?
```

- Show CoWork pulling real calendar events

> "Now it knows my schedule. This becomes incredibly powerful when combined with other connectors."

---

### SECTION 4: Connecting Google Drive (6:30–8:00)

**On screen**: Same flow for Drive.

**Quick walkthrough**:
- Connect → Sign in → Set permissions

**Permissions**:
- Read files: Allow
- Create files: Allow
- Modify files: Needs approval
- Delete files: Block

**Test it**:
```
Find the most recently modified Google Doc in my Drive and summarize it.
```

- Show CoWork searching Drive and summarizing a document

---

### SECTION 5: Connecting Slack (8:00–9:30)

**On screen**: Same flow for Slack.

**Quick walkthrough**:
- Connect → Sign in to Slack workspace → Set permissions

**Permissions**:
- Read messages: Allow
- Send messages: Needs approval
- Create channels: Block

**Test it**:
```
What were the last 5 messages in the #general channel?
```

- Show CoWork reading Slack messages

---

### SECTION 6: Real Workflow — All Connectors Together (9:30–14:00)

**On screen**: CoWork ready for a combined task.

> "Now that everything's connected, let me show you what CoWork can actually do when it has access to all your apps at once."

**Demo 1: Morning Briefing**

Type:
```
Give me a morning briefing:
1. Check my Gmail for any urgent or important unread emails from the last 24 hours
2. Look at my calendar for today — what meetings do I have?
3. Check Slack for any messages that mention me or need my attention
4. Summarize everything in a clean report and save it as today's-briefing.md in my project folder
```

- Show CoWork executing each step
- Show the final briefing document

> "In about 2 minutes, CoWork just checked my email, my calendar, and my Slack — and gave me a single summary. That's a task that would take me 15 minutes every morning."

**Reference from competitors**: Brock builds a morning briefing that generates "a beautiful interactive HTML dashboard." Jack Roberts builds one that shows "high priority emails, calendar, trending news, and an affirmation of the day." Both are good examples — keep yours practical and grounded.

**Demo 2: Email Triage**

Type:
```
Go through my unread emails from the last 3 days. For each one:
1. Categorize it: urgent, needs reply, FYI only, or spam
2. For any that need a reply, draft a response
3. Save all drafts to Gmail (don't send them)
4. Give me a summary of what you found and what you drafted
```

- Show CoWork reading emails, categorizing, drafting
- Show the drafts in Gmail
- Show the summary

> "It categorized 23 emails, identified 5 that need replies, and drafted all 5 responses. The drafts are sitting in my Gmail now — I just need to review and hit send."

**Reference from competitors**: Jack Roberts emphasizes "you go from the creator to the simple approver" — the mental shift of reviewing drafts instead of writing from scratch. Good framing to use.

**Demo 3: Meeting Prep**

Type:
```
I have a meeting with [Client Name] tomorrow at 2pm. Can you:
1. Check my email history for any recent threads with them
2. Check Google Drive for any shared documents
3. Prepare a one-page brief: what we last discussed, any open items, and suggested talking points
4. Save it as meeting-prep-[client-name].md
```

- Show CoWork pulling from multiple sources
- Show the meeting prep document

> "It searched my email, checked Drive, and compiled a prep document. Before this meeting, I would have spent 20 minutes scrolling through old emails trying to remember where we left off."

---

### SECTION 7: Permission Best Practices (14:00–15:00)

**On screen**: Summary table.

> "Before we wrap up, here's my recommended permission setup."

| Connector | Read | Create/Draft | Send/Modify | Delete |
|-----------|------|-------------|-------------|--------|
| Gmail | Allow | Allow | Needs Approval | Block |
| Calendar | Allow | Allow | Needs Approval | Block |
| Drive | Allow | Allow | Needs Approval | Block |
| Slack | Allow | Needs Approval | Needs Approval | Block |

> "The pattern is simple: let CoWork read everything and create drafts freely. But anything that sends a message, modifies existing data, or deletes something — require your approval. You're the final checkpoint."

**The Zapier workaround** (brief mention):
> "What if the app you need isn't in the connectors list? There's a workaround using Zapier's MCP server that lets you connect almost anything. We'll cover that in a later video when we talk about MCP servers."

**Reference from competitors**: Brock and Jack Roberts both demo the Zapier MCP workaround. Good to mention here but save the full walkthrough for the MCP/advanced video.

---

### OUTRO (15:00–15:30)

> "CoWork now has access to your files, your email, your calendar, and your Slack. It can read, draft, and prepare — with you as the final approver. In the next video, we're going to unlock browser automation. CoWork can actually open Chrome, navigate to websites, click through pages, and gather information. That's when it starts feeling like a real AI employee."

---

### NOTES FOR FILMING

- The Gmail connection flow needs to be recorded cleanly — viewers are doing this alongside you
- Use real (or realistic demo) email for the inbox demos — generic stuff kills credibility
- The morning briefing demo is the hero moment — make it look effortless
- Permission table should be screenshot-ready
- Blur any sensitive email content during recording
- Target length: ~15 minutes
