---
tags: [script, claude-cowork, video-11]
status: draft
---

## Video 11 — Putting It All Together

**Goal**: Viewer watches a complete end-to-end build of an automated CoWork system — combining projects, instructions, connectors, skills, scheduled tasks, and dispatch into one functioning "AI employee."

---

### HOOK (0:00–0:30)

> "Over the last 10 videos, you've learned every feature of Claude CoWork individually. Now I'm going to put all of them together — live, from scratch — and build a complete automated system. By the end of this video, you'll have a CoWork setup that checks your email, manages your calendar, processes your files, generates reports, and runs on autopilot every day. This is the video where it all clicks."

---

### SECTION 1: The Plan (0:30–2:00)

**On screen**: Whiteboard or diagram showing the system.

> "Here's what we're building. A complete weekly business management system. It's going to have five components."

Draw out or show:

```
1. PROJECT: "My Business" — with instructions, folder structure, memory
2. CONNECTORS: Gmail, Calendar, Google Drive, Slack
3. SKILLS:
   - /morning-brief — daily email + calendar + Slack summary
   - /process-invoices — weekly invoice sorting and spreadsheet
   - /weekly-report — compile a weekly summary of everything
4. SCHEDULED TASKS:
   - Morning Brief: weekdays at 8am
   - Invoice Processing: Mondays at 9am
   - Weekly Report: Fridays at 5pm
   - End-of-Day: weekdays at 6pm
5. DISPATCH: Trigger any skill from your phone
```

> "By the end of this video, all five are live and running. Let's build it."

---

### SECTION 2: Build the Project (2:00–5:00)

**On screen**: Creating the project from scratch.

**Step 1: Create the project**
- New Project → Start from scratch
- Name: "My Business"

**Step 2: Write the instructions**

Type (show on screen):

```
## Project: Business Management

### About Me
- Name: [Your Name]
- Business: [Description]
- Timezone: [Your timezone]

### How Claude Should Work
- Be concise and actionable
- Save all outputs to /outputs with date-prefixed filenames
- Use markdown for reports
- Ask before deleting anything
- When drafting emails, never send — always save as draft

### Folder Structure
- /invoices — incoming invoices to process
- /outputs/briefings — daily morning and evening briefings
- /outputs/reports — weekly and monthly reports
- /outputs/drafts — email drafts and document drafts
- /context — reference documents and templates

### Key Contacts
- Accountant: [name] ([email])
- Main client: [name] ([email])
- Team Slack channel: #general
```

**Step 3: Click Create**
- Show the project created
- Show the folder structure on disk

> "Project is live. Instructions are set. CoWork now knows who I am, how I work, and where to save things."

---

### SECTION 3: Connect the Apps (5:00–7:00)

**On screen**: Connecting all four apps quickly.

> "We covered this in detail in the connectors video. I'm going to speed through the connections."

- **Gmail**: Connect → sign in → set permissions (read: allow, draft: allow, send: needs approval, delete: block)
- **Calendar**: Connect → sign in → set permissions
- **Drive**: Connect → sign in → set permissions
- **Slack**: Connect → sign in → set permissions

> "Four apps connected in about 2 minutes. CoWork now has access to my email, calendar, files, and team communication."

Quick verification — type in CoWork:
```
Confirm you can access my Gmail, Calendar, Drive, and Slack. 
Tell me how many unread emails I have and what's on my calendar today.
```

- Show CoWork confirming access to all four
- > "All four connected and working. Let's build the skills."

---

### SECTION 4: Build the Skills (7:00–14:00)

**On screen**: Creating each skill.

> "We need four skills. I'm going to build each one."

**Skill 1: Morning Brief**

Ask CoWork:
```
Create a skill called /morning-brief that does the following:

1. Check Gmail for unread emails from the last 24 hours
   - Categorize each as: urgent, needs-reply, FYI, or skip
   - For urgent emails, draft a reply

2. Check Google Calendar for today's meetings
   - For each meeting, note the time, attendees, and any prep needed

3. Check Slack #general for messages from the last 24 hours
   - Flag anything that mentions me or needs my response

4. Compile into a morning briefing and save as:
   /outputs/briefings/YYYY-MM-DD-morning.md

Format:
## Urgent Emails (need action)
## Today's Calendar  
## Slack Highlights
## Top 3 Priorities
```

- Show CoWork generating the skill
- Show the skill file
- Test it: `/morning-brief`
- Show the output

> "Skill one done. Let's move on."

**Skill 2: Process Invoices**

```
Create a skill called /process-invoices that does the following:

1. Scan /invoices for any PDF files
2. Read each invoice and extract: vendor, category, date, subtotal, tax, total
3. Move processed invoices into category subfolders (software, services, hardware, other)
4. Update /outputs/reports/invoice-tracker.xlsx with new entries
5. Give a summary of what was processed

If the xlsx doesn't exist, create it with the appropriate headers.
```

- Show CoWork generating the skill
- Have some test invoices in the folder
- Test it
- Show the spreadsheet

> "Skill two done. Invoices get sorted and tracked automatically."

**Skill 3: Weekly Report**

```
Create a skill called /weekly-report that does the following:

1. Review all morning briefings from this week (/outputs/briefings/)
2. Check what tasks CoWork completed this week
3. Review the invoice tracker for this week's expenses
4. Check Calendar for next week's upcoming meetings

Compile into a weekly summary saved as:
/outputs/reports/YYYY-MM-DD-weekly-report.md

Format:
## This Week's Highlights
## Tasks Completed
## Expenses This Week (from invoice tracker)
## Next Week's Calendar
## Recommendations
```

- Show CoWork generating the skill
- Test it

**Skill 4: End-of-Day Wrap-up**

```
Create a skill called /end-of-day that does the following:

1. Summarize what was worked on today (check recent tasks, modified files)
2. List what got completed vs what's still in progress
3. Check Calendar for tomorrow's schedule
4. Suggest the #1 priority for tomorrow morning

Save as /outputs/briefings/YYYY-MM-DD-end-of-day.md

Keep it brief — 3 minute read max.
```

- Show CoWork generating the skill
- Test it

> "Four skills, all tested. Now let's put them on autopilot."

**Reference from competitors**: Brock builds morning-brief and end-of-day as separate skills, then schedules them. Jack Roberts builds morning briefing with HTML output. Bart converts manual invoice processing into a skill. We're combining all of these into one cohesive system.

---

### SECTION 5: Schedule Everything (14:00–17:00)

**On screen**: Creating scheduled tasks.

> "Now we schedule each skill."

**Scheduled Task 1: Morning Brief**
- Name: "Morning Briefing"
- Instructions: "Run /morning-brief"
- Schedule: Weekdays at 8:00 AM
- Model: Sonnet

**Scheduled Task 2: Invoice Processing**
- Name: "Weekly Invoice Processing"
- Instructions: "Run /process-invoices"
- Schedule: Weekly, Mondays at 9:00 AM
- Model: Sonnet

**Scheduled Task 3: Weekly Report**
- Name: "Weekly Report"
- Instructions: "Run /weekly-report"
- Schedule: Weekly, Fridays at 5:00 PM
- Model: Sonnet

**Scheduled Task 4: End of Day**
- Name: "End of Day Wrap-up"
- Instructions: "Run /end-of-day"
- Schedule: Weekdays at 6:00 PM
- Model: Sonnet

- Show all four scheduled tasks in the list
- Show next run times for each

> "Four scheduled tasks. My week now looks like this:"

Show a weekly timeline:
```
WEEKDAYS:
  8:00 AM — Morning Briefing (email, calendar, Slack)
  6:00 PM — End-of-Day Wrap-up (what got done, tomorrow's priority)

MONDAYS:
  9:00 AM — Invoice Processing (sort, track, spreadsheet)

FRIDAYS:
  5:00 PM — Weekly Report (full week summary, next week prep)
```

> "That's 12 automated runs per week. All running without me touching anything."

---

### SECTION 6: Test Dispatch (17:00–18:30)

**On screen**: Phone + desktop split screen.

> "One last thing. Let's make sure I can trigger any of this from my phone."

On phone, dispatch:
```
Run /morning-brief
```

- Show the task hitting the desktop
- Show CoWork executing
- Show the result coming back to the phone

> "I'm at a coffee shop, I dispatch the morning briefing from my phone, and 2 minutes later I have my email summary, calendar, and Slack highlights on my phone. The full system works from anywhere."

---

### SECTION 7: The Complete System (18:30–20:00)

**On screen**: Recap diagram showing everything connected.

> "Let's zoom out and look at what we built."

Show the complete system:

```
┌──────────────────────────────────────────────┐
│                MY BUSINESS PROJECT            │
│                                               │
│  Instructions: who I am, how I work           │
│  Memory: learns my preferences over time      │
│                                               │
│  CONNECTORS                                   │
│  ├── Gmail (read, draft)                      │
│  ├── Calendar (read, create)                  │
│  ├── Drive (read, create)                     │
│  └── Slack (read, post)                       │
│                                               │
│  SKILLS                                       │
│  ├── /morning-brief                           │
│  ├── /process-invoices                        │
│  ├── /weekly-report                           │
│  └── /end-of-day                              │
│                                               │
│  SCHEDULED TASKS                              │
│  ├── Morning Brief     (weekdays 8am)         │
│  ├── Invoice Processing (Mondays 9am)         │
│  ├── Weekly Report     (Fridays 5pm)          │
│  └── End of Day        (weekdays 6pm)         │
│                                               │
│  DISPATCH: trigger anything from your phone   │
└──────────────────────────────────────────────┘
```

> "A project with persistent memory. Four app connections. Four reusable skills. Four scheduled automations. And mobile access through Dispatch. This is what it looks like when CoWork becomes your AI employee."

---

### SECTION 8: What to Do Next (20:00–21:00)

**On screen**: Talking head or summary slide.

> "Here's what I'd recommend from here."

1. **Use it for a week** — let the scheduled tasks run, review the outputs, see what's useful and what needs tweaking
2. **Edit your skills** — after a few runs, you'll see what's missing or wrong. Update the skill files.
3. **Update your instructions** — as CoWork learns your preferences through memory, add new rules to your project instructions
4. **Build more skills** — identify your next repetitive task and turn it into a skill
5. **Expand connectors** — connect more apps as you need them

> "The system gets better the more you use it. Memory accumulates. Skills get refined. Instructions get tighter. After a month, CoWork will feel like it genuinely knows your business."

**Reference from competitors**: Jack Roberts frames this as "skills + connectors = plugins = an AI employee playbook." Mikey talks about "chaining actions into structured systems" and "workflow compounding."

---

### SECTION 9: Course Recap (21:00–22:00)

**On screen**: Recap of all 11 videos.

> "Let's do a quick recap of everything we covered in this course."

1. **What is CoWork** — installation and first look
2. **Your First Task** — folder access, file organization
3. **Chat vs Code vs CoWork** — picking the right tool
4. **Projects & Memory** — persistent context across sessions
5. **Instructions & Claude.md** — the three-layer instruction hierarchy
6. **Connectors** — Gmail, Calendar, Drive, Slack
7. **Browser Automation** — Chrome extension, web research
8. **Skills** — reusable one-command workflows
9. **Scheduled Tasks** — autopilot automation
10. **Computer Use & Dispatch** — desktop control and mobile access
11. **Putting It All Together** — the complete AI employee system

> "You went from installing Claude CoWork to building a fully automated business management system. Everything from here is iteration — more skills, more connectors, better instructions."

---

### OUTRO (22:00–22:30)

> "That's the complete Claude CoWork course. If you got value from this, subscribe and let me know in the comments what system you built. I'd love to see what you're automating. I'll see you in the next one."

---

### NOTES FOR FILMING

- This is the capstone video — it needs to feel like a culmination, not just another tutorial
- Build everything live and show the results — no pre-built shortcuts
- The system diagram at the end should be screenshot-worthy
- The weekly timeline (8am briefing, 6pm wrap-up, etc.) is a strong visual — keep it on screen
- Energy should build throughout — start calm with the plan, end excited with the complete system
- Target length: ~22 minutes
