---
duration: "6-8 min"
order: 5
class: "codex-app"
chapter: "Codex App"
status: "to-film"
tags: [course, script, codex, codex-app, automations]
lesson: "Thread Automations"
---

## Thread Automations

This video is about the difference between a standalone automation and a thread automation.

A standalone automation starts from a prompt and runs as its own scheduled job. A thread automation wakes up the same conversation later, so it keeps the context that already exists in the thread: the project, the tools, the output style, the edge cases, and the corrections the user made along the way.

## Big Picture

Thread Automations turn a good Codex conversation into a recurring worker or follow-up loop.

Instead of rebuilding context every time, Codex wakes the same thread back up on a schedule and continues from the accumulated understanding in that conversation.

Codex has two automation shapes worth naming clearly:

| Automation type | Big picture | Best for |
| ---------------- | ----------- | -------- |
| Heartbeat | Wakes up this same thread later and continues the conversation. | Reminders, short follow-ups, checking back later today, continuing a useful thread. |
| Cron | Runs a standalone scheduled job against one or more workspace directories. | Recurring repo or workspace tasks, like weekly inspections, daily summaries, or scheduled file checks. |

The important teaching move is that the user should describe the schedule naturally: "in 30 minutes," "every weekday at 9 AM," or "every Friday." Codex handles the scheduling format internally.

For existing automations, Codex should find and update the matching automation instead of creating duplicates.

## Teaching Line

> A cron automation starts from a scheduled job. A heartbeat automation starts from this thread, so the context comes with it.

## Key Distinction

Heartbeat automations are the thread-native version. They are best when the value comes from the conversation itself: what has already been explained, corrected, decided, or refined.

Cron automations are the workspace-native version. They are best when the value comes from running the same task against files, repos, logs, or project folders on a recurring schedule.

## Recording Emphasis

Do not make students think they need to know recurrence-rule syntax. The skill is describing the job and schedule in plain English, then verifying that Codex created the right automation.

Use examples like:

- "Remind me in 45 minutes to come back to this."
- "Check this thread again tomorrow morning and continue from here."
- "Every Monday, inspect this repo for stale TODOs."
- "Every weekday at 9 AM, summarize the latest workspace changes."

## Visual Variations

### Variation 1: Cron vs Heartbeat

Big idea: compare a standalone scheduled workspace job with a context-rich thread that wakes up later.

Core labels: cron job, workspace task, heartbeat, same thread, preserved context.

### Variation 2: Conversation Becomes Worker

Big idea: show a useful chat transforming into a recurring worker.

Core labels: useful chat, knows the job, heartbeat, schedule, recurring result.

### Variation 3: Context Snowball

Big idea: show a thread accumulating project knowledge, corrections, preferences, and output examples over time.

Core labels: project context, user corrections, output style, edge cases, better next wake-up.

![[images/05-thread-automations/thread-automations.png]]
