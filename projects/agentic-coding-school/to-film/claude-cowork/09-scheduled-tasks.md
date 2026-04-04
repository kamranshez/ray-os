---
tags: [script, claude-cowork, video-9]
status: draft
---

## Video 9 — Scheduled Tasks

**Goal**: Viewer creates their first scheduled task, understands timing/frequency options, and builds a task that runs on autopilot.

---

### HOOK (0:00–0:30)

> "What if Claude CoWork could run tasks without you even opening the app? Every morning at 8am, it checks your email, reads your calendar, and sends you a briefing in Slack. Every Monday, it processes your invoices and updates your spreadsheet. Every evening, it summarizes what got done. That's scheduled tasks — and this is where CoWork goes from useful to indispensable."

---

### SECTION 1: What Are Scheduled Tasks? (0:30–2:00)

**On screen**: CoWork Scheduled Tasks panel.

> "A scheduled task is exactly what it sounds like — you tell CoWork to run a specific task at a specific time, on a recurring schedule. You set it once and it runs automatically."

**The concept**:
- You pick a task (or a skill)
- You pick a time and frequency (daily, weekly, weekdays, custom)
- CoWork runs it automatically at that time
- You can review the results whenever you want

**Critical requirement**:
> "And I need to say this upfront because it catches everyone off guard: scheduled tasks only run when your computer is ON and the Claude desktop app is OPEN. If your laptop is closed at 8am, the morning briefing doesn't run. CoWork isn't running on a cloud server — it's running on your machine."

**Reference from competitors**: Every single competitor mentions this. Brock: "scheduled tasks only operate when your Claude desktop app is open and your computer is turned on." Ryan & Matt: "if your computer is off at 10am, it's not going to do this automatically." It's the number one gotcha.

---

### SECTION 2: Creating Your First Scheduled Task — Step by Step (2:00–7:00)

**On screen**: Full screen recording.

> "Let's set one up. I'm going to create a morning briefing that runs every weekday at 8am."

**Step 1: Navigate to Scheduled Tasks**
- In the left sidebar, click "Scheduled" (or find it in your project)
- > "You'll see any existing scheduled tasks listed here. Right now it's probably empty."

**Step 2: Create a new scheduled task**
- Click the "+" or "Create" button
- A form appears

**Step 3: Name it**
- Type: "Morning Briefing"
- > "Give it a clear name so you can identify it later."

**Step 4: Write the instructions**
- This is what CoWork will execute each time:

```
Run my morning briefing workflow:

1. Check Gmail for unread emails from the last 24 hours
   - Categorize as: urgent, needs reply, FYI, or skip
   - Draft replies for urgent emails

2. Check Google Calendar for today's meetings
   - Note any prep needed

3. Check Slack for messages that need my attention

4. Create a morning briefing report saved as:
   /outputs/briefings/YYYY-MM-DD-morning-brief.md

Format with clear sections and bullet points. 
Keep it scannable — I want to read this in 2 minutes.
```

> "I'm writing detailed instructions because I won't be here to clarify. This runs on autopilot, so the instructions need to be complete."

**Step 5: Set the schedule**
- Frequency: Weekdays
- Time: 8:00 AM
- > "You can choose daily, weekdays, weekly, or set a custom schedule. For a morning briefing, weekdays makes sense."

**Step 6: Choose the model**
- Show model selector
- > "For routine tasks like this, use Sonnet — it's cheaper and fast enough. Save Opus for tasks that need heavy reasoning."

**Reference from competitors**: Brock mentions using cheaper models for simple tasks. Ryan & Matt show the model selector and suggest "maybe we don't need Sonnet for this one, we can use Haiku."

**Step 7: Set the folder**
- Select the project folder
- > "Make sure it's pointed at the right folder so it has access to the right files."

**Step 8: Save**
- Click Save
- Show the scheduled task appearing in the list
- Show the next run time

> "Done. Tomorrow at 8am, this will run automatically. Let's not wait — let's test it right now."

**Step 9: Run it manually**
- Click "Run Now"
- Watch CoWork execute the morning briefing
- Show the output file

> "There's the briefing. Urgent emails, today's calendar, Slack highlights, and my top priorities. This will be waiting for me every morning when I open my laptop."

---

### SECTION 3: Scheduled Task with a Skill (7:00–9:00)

**On screen**: Creating another scheduled task, this time using a skill.

> "Even better — you can attach a skill to a scheduled task. Remember the invoice processing skill from the last video? Let's schedule it."

**Step 1: Create new scheduled task**
- Name: "Weekly Invoice Processing"

**Step 2: Instructions — reference the skill**
```
Run the /process-invoices skill.
After processing, send a summary to Slack in the #accounting channel.
```

**Step 3: Set schedule**
- Frequency: Weekly
- Day: Monday
- Time: 9:00 AM

**Step 4: Save and test**
- Show it scheduled
- > "Every Monday at 9am, CoWork will process any new invoices, sort them, update the spreadsheet, and send a summary to Slack. Fully autonomous."

**Reference from competitors**: Bart does this exact flow — creates the invoice skill, then says "create a scheduled task that runs that skill every Monday at 9am." Brock schedules his morning briefing skill and end-of-day wrap-up.

---

### SECTION 4: More Scheduled Task Ideas (9:00–11:00)

**On screen**: List of scheduled task ideas with descriptions.

> "Let me give you a bunch of ideas for scheduled tasks that are actually useful."

**Daily tasks**:
- **Morning briefing** — email, calendar, Slack summary (we just built this)
- **End-of-day wrap-up** — summarize what CoWork did today, what's unfinished, what's tomorrow's priority
- **Inbox triage** — categorize and draft replies to emails twice a day

**Weekly tasks**:
- **Invoice processing** — sort and summarize new invoices
- **Competitor research** — check competitor websites/YouTube channels for new content
- **Content calendar review** — check what's coming up, flag gaps
- **Analytics report** — pull stats from connected tools, create a weekly summary

**Monthly tasks**:
- **Expense categorization** — sort bank statements or receipts
- **Client report generation** — compile monthly deliverables and results

**Reference from competitors**: Brock builds both a morning briefing AND an end-of-day wrap-up. Jack Roberts mentions "email triage twice a day." The end-of-day wrap-up is a particularly good one — Brock's shows "11 activities CoWork did, what moved forward, what's still open, and tomorrow's focus."

**Demo: End-of-Day Wrap-up**

Create one more scheduled task live:
- Name: "End of Day Wrap-up"
- Schedule: Weekdays at 6:00 PM
- Instructions:

```
Create an end-of-day summary:

1. List everything I worked on today (check recent CoWork tasks and files modified)
2. What got completed?
3. What's still in progress?
4. What should be my #1 priority tomorrow?
5. Any deadlines coming up this week?

Save as /outputs/daily/YYYY-MM-DD-end-of-day.md
Keep it brief — 5 minute read max.
```

> "Now I've got a morning briefing at 8am and an end-of-day wrap-up at 6pm. My day is bookended by AI summaries."

---

### SECTION 5: Managing Scheduled Tasks (11:00–12:30)

**On screen**: Scheduled tasks panel with multiple tasks.

> "Once you have a few scheduled tasks running, you need to manage them."

**Show how to**:
- **View all scheduled tasks**: Click Scheduled in the sidebar
- **Edit a task**: Click into it, modify instructions or schedule
- **Pause a task**: Toggle it off without deleting
- **Delete a task**: Remove it entirely
- **View run history**: See past runs and their results

> "Check your scheduled tasks once a week. Are they still useful? Are the results good? If a task consistently produces garbage, fix the instructions or delete it."

---

### SECTION 6: The "Computer Must Be On" Problem (12:30–14:00)

**On screen**: Talking head or diagram.

> "Let's address the elephant in the room. Your computer has to be on."

**The problem**:
- Scheduled tasks only run when the Claude desktop app is open
- If your laptop is closed, sleeping, or off — the task doesn't run
- If you miss the scheduled time, it doesn't catch up later

**Workarounds**:
1. **Keep your computer awake during scheduled times**
   - Use energy settings to prevent sleep during work hours
   - > "Set your computer to never sleep between 7am and 7pm. That covers most scheduled tasks."

2. **Use a dedicated machine**
   - > "Some people run CoWork on a dedicated Mac Mini or old laptop that stays on 24/7. It's like having a dedicated AI workstation."

3. **Schedule around your habits**
   - > "If you always open your laptop at 9am, schedule tasks for 9:15am. Work with your routine, not against it."

**What happens if you miss a run?**
> "If CoWork misses a scheduled time, it doesn't automatically retry. You can manually trigger it when you're back, but there's no built-in catch-up. Keep this in mind when scheduling critical tasks."

**Reference from competitors**: Brock mentions "you can get CoWork to constantly keep your computer awake. I'm not sure I'd recommend it, but it's an option." Ryan & Matt confirm "if your computer is off, it's not going to do this automatically."

---

### SECTION 7: Token Budgeting (14:00–15:00)

**On screen**: Quick math on screen.

> "One more thing — scheduled tasks use credits every time they run."

**Quick math**:
- Morning briefing: runs 5x/week = 20x/month
- Invoice processing: runs 4x/month
- End-of-day: runs 5x/week = 20x/month
- Total: ~44 automated runs per month

> "Each run uses tokens depending on complexity. A morning briefing might use as much as 5-10 regular chat messages worth of tokens. 44 runs adds up. If you're on the Pro plan, you might hit limits. This is where Max starts making sense."

**Tips**:
- Use Sonnet (not Opus) for routine scheduled tasks
- Keep instructions focused — don't have it do 15 things in one run
- Review usage monthly and cut tasks that aren't delivering value

---

### OUTRO (15:00–15:30)

> "You now have CoWork running on autopilot. Morning briefings, invoice processing, end-of-day wrap-ups — all happening without you lifting a finger. In the next video, I'm going to show you Computer Use and Dispatch — how CoWork can take control of apps on your desktop and how you can trigger tasks from your phone."

---

### NOTES FOR FILMING

- Show the full scheduled task creation flow — no jump cuts during setup
- The "Run Now" test is important — prove it works before moving on
- The end-of-day wrap-up is a good second demo — viewers will want both
- The token budgeting section is quick but important — don't skip it
- Target length: ~15 minutes
