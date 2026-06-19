---
class: "skills"
chapter: "Build Your AI Employees"
status: "idea"
tags: [course, script, skills]
lesson: "4.1 The Morning Briefing Employee"
---

## The Morning Briefing Employee

Chapter 4 is called Build Your AI Employees. And I'm starting with this one because it's the skill that makes the whole concept click. It's not abstract — you'll feel it the first morning it runs.

We're going to build two skills in this video. A morning briefing that starts your day. And an update skill that ends it. Together, they form a loop — your AI system tells you what's ahead, you do the work, then you tell your AI system what happened. And everything stays in sync.

But first, we need to connect Claude to the apps you actually use.

### Connecting Your Apps (0:00–2:00)

So far, every skill we've built has worked with local files or web searches. The morning briefing needs more than that. It needs your email. Your calendar. Maybe Slack or Notion.

> [SCREEN: Co-work — Customize → Connectors panel]

In Co-work, go to Customize and you'll see a Connectors section. These are direct integrations — Gmail, Google Calendar, Notion, Slack, Canva, HubSpot, and about 50 others. Click one, authorize it, and now Claude can read your emails, check your calendar, post to Slack — whatever that connector allows.

For this demo, I'm connecting Gmail and Google Calendar.

> [SHOW: authorizing Gmail and Calendar connectors]

Done. Two clicks each. Now Claude can pull my emails and my schedule.

Now — what if the app you need isn't on this list? There's a hack for that. Zapier has an MCP server with over 8,000 apps preconfigured. You create a custom MCP server on Zapier, pick the apps you want — Stripe, Google Drive, whatever — add the tools, and paste the connection URL into Claude's MCP settings.

> [SHOW: briefly — Zapier MCP setup flow, adding an app, copying the URL]

Now Claude can interact with that app too. I'm not going to go deep on MCP setup here — there's a full video on that in the Claude Code class if you need it. The point is: if an app exists, you can probably connect it.

### Building the Morning Briefing (2:00–5:00)

Now the fun part.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build a morning briefing skill. Every morning, it should pull my calendar for the day, check my email inbox for anything urgent, and give me a summary dashboard with: today's schedule, emails I need to respond to with suggested replies, and any to-dos or follow-ups from yesterday."]

Skill Creator asks its questions. "Which email accounts? How do you define 'urgent'? Do you want industry news or just personal tasks? What format — markdown, HTML dashboard, or both?"

I tell it: just my main Gmail, urgent means unread from real people in the last 24 hours not newsletters, skip the news for now, and give me an HTML dashboard I can open in my browser.

> [SHOW: Skill Creator building the skill]

It builds the skill. The skill.md has the process — step one, fetch calendar events for today. Step two, search inbox for unread emails from the last 24 hours, filter out newsletters and automated messages. Step three, for each email that needs a response, draft a suggested reply. Step four, check for any open to-dos or follow-ups. Step five, compile into an HTML dashboard.

> [SHOW: running the skill — the morning briefing output]

And there it is. An HTML page I can open in my browser. Today's schedule across the top. Three emails flagged as needing responses, each with a one-paragraph suggested reply. Two follow-ups from yesterday that I haven't closed out yet.

> [SHOW: the HTML dashboard in a browser]

That used to be the first 30 minutes of my day. Open email, scan for urgent stuff, check calendar, make a mental to-do list. Now it takes 15 seconds and I've got a dashboard.

We'll turn this into a scheduled task in Chapter 6 so it runs automatically at 7am. For now it's a skill we invoke manually.

### Building the Update Skill (5:00–7:00)

So the morning briefing tells you what's ahead. But what happens at the end of the day when you've done things? Had meetings. Made decisions. Finished tasks. Your system doesn't know about any of that unless you tell it.

That's the update skill.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build an update skill. When I describe what I've done — meetings I had, tasks I completed, decisions I made — it should update all relevant project files. Mark completed items as done. Add new information to project briefs. Flag anything that changes the next steps."]

This one is simpler than the morning briefing. The skill.md is straightforward — listen to my update, identify what changed, find the relevant project files, update them. If I say "we decided to push the launch to April," it finds the project brief and updates the timeline. If I say "I finished the first milestone of the deck project," it marks it done and surfaces whatever's next.

> [TYPE: "Update — I had a call with the client today. They approved the proposal but want the timeline pushed back two weeks. I also finished the first draft of the marketing plan."]

> [SHOW: the skill processing — updating project files, marking tasks, adjusting timelines]

It updated the client project brief with the new timeline. Marked the marketing plan draft as complete. And flagged that the pushed timeline means I need to re-sequence two dependent tasks.

That's the loop. Morning briefing says "here's what's ahead." You do the work. Update skill says "here's what happened." Tomorrow's morning briefing reflects the changes. Everything stays in sync without you manually maintaining files.

### The Employee Metaphor (7:00–8:00)

And this is why this chapter is called Build Your AI Employees. An employee doesn't just do one task. They maintain context. They track what happened yesterday and what's needed tomorrow. They keep things organized so you can focus on the actual work.

The morning briefing and the update skill together are your first AI employee. Not a chatbot you ask questions to — an actual persistent assistant that maintains state across days.

Over the next four videos, we're going to build more. A content director that plans and scripts your content. An operations manager that handles receipts and invoices. A marketing director that runs your social strategy. Each one builds on the same pattern — skills that pull from your context, connect to your apps, and maintain state over time.

### What's Next

In the next video, we're going to build something more ambitious — a content director that chains multiple skills together. Ideation, scriptwriting, and calendar planning, all from one command. That's where skills start to feel less like individual tools and more like a team.
