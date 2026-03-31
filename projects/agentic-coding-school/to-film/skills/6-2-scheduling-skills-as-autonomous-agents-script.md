---
tags: [course, script, skills]
status: draft
lesson: "6.2 Scheduling Skills as Autonomous Agents"
duration: "7-10 min"
---

## Scheduling Skills as Autonomous Agents

Up until now, every skill we've built requires you to invoke it. You type a command, the skill runs, you get output. But the real shift happens when skills run without you. On a clock. While you sleep.

Any skill can become a scheduled task. And once it is, it's not a tool you use — it's an employee that works on a schedule.

### Setting Up a Scheduled Task (0:00–2:30)

I'm going to take the morning briefing from Chapter 4 and schedule it to run every day at 7am.

> [SCREEN: Claude Co-work]

There are two ways to do this. First — just tell Claude in the chat.

> [TYPE: "Turn the morning briefing into a scheduled task that runs every day at 7am"]

Claude asks for confirmation. I confirm.

> [SHOW: the scheduling confirmation — "This will run every day at 7:00 AM"]

Done. Every morning at 7am, the morning briefing skill fires. It checks my calendar, scans my email, compiles the dashboard. By the time I open my laptop, it's already there.

Second way — through the schedule interface. Click the schedule button at the top of Co-work. You get a form where you set the frequency — hourly, daily, specific days, weekly, monthly. Set the time. Set the prompt. Save.

> [SHOW: the schedule interface — setting up the receipt scanner for Fridays at 5pm]

I'm adding the receipt scanner from Chapter 4. Every Friday at 5pm. It scans whatever receipts accumulated in the folder that week, generates the spreadsheet and dashboard. End of week, finances organized, no effort.

### The Scheduled Tasks Dashboard (2:30–3:30)

> [SCREEN: Co-work — scheduled tasks list]

Here's where all your scheduled tasks live. I can see my morning briefing — daily at 7am. Receipt scanner — Fridays at 5pm. I could add the LinkedIn content planner — every Monday morning so I have the week's posts ready.

Each task shows when it last ran, when it'll run next, and whether the last run succeeded. If something fails — maybe a connector expired or a file moved — you'll see it here and can fix it.

And you can hit "Run Now" on any scheduled task to test it without waiting for the clock. Always do that when you first set one up. Make sure it works before you trust the schedule.

### Delivery — Getting Output to Your Phone (3:30–5:00)

Now, a scheduled task that runs at 7am doesn't help much if you have to open your laptop to see the result. So you connect it to a delivery channel.

> [SCREEN: the morning briefing task — adding Slack delivery]

I'm adding Slack as a delivery channel. When the morning briefing runs, it doesn't just save the dashboard to a file — it sends it to me in Slack. I wake up, check my phone, and the briefing is there.

You can use Slack, Telegram, email — whatever you have connected. For Telegram, you'd set up a bot and add the channel. For Slack, it's just enabling the Slack connector.

The receipt scanner sends its weekly summary to a Slack channel too. Friday at 5pm, my phone buzzes with the expense dashboard. I glance at it over the weekend or deal with it Monday. Either way, it happened.

### The CEO Pattern (5:00–6:30)

And this is where the whole class comes together into a daily reality.

Sunday evening — or whenever you do your weekly planning — you open your laptop. Your scheduled tasks have already done the prep work. The morning briefing is ready. The receipt scanner ran Friday. The LinkedIn planner has next week's posts drafted.

You're not starting from zero. You're reviewing work that's already been done by your AI employees. You make decisions — approve this, adjust that, skip this one. Strategy, not execution.

Your day becomes: wake up, check briefing, make decisions, do the creative work only you can do. The operational stuff — tracking, organizing, drafting, summarizing — runs in the background on schedules.

And you can stack these schedules however you want. Monday morning: content plan for the week. Wednesday: check project status and draft client updates. Friday: financial summary. Sunday: plan next week. Each one a scheduled skill that produces output waiting for you.

This is operating as a one-person CEO. Not because you're doing less — because the repetitive operational work is handled.

### What's Next

Your skills run on schedules now. You've got a system — content, marketing, operations, all automated. In the next video, we're going to step back and visualize this entire system. A dashboard that shows every skill, how they connect, what's scheduled, and what it all looks like as a complete operating system.
