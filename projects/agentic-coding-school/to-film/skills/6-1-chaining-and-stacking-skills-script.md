---
tags: [course, script, skills]
status: draft
lesson: "6.1 Chaining and Stacking Skills"
duration: "10-12 min"
---

## Chaining and Stacking Skills

Chapter 6 is about wiring everything together. And it starts with understanding two patterns for how skills work together. Most people only know about one of them.

### Chaining — The Pipeline (0:00–3:00)

Chaining is when skills run in sequence. Skill A produces output. That output becomes the input for skill B. Which produces output for skill C. A pipeline.

We actually built this in Chapter 4 with the content director. Ideation skill finds topics. Scriptwriting skill takes those topics and writes scripts. Calendar skill takes those scripts and organizes them. One command, three skills, sequential.

But I want to show a different example to make the pattern clearer.

> [SCREEN: Claude terminal]

> [TYPE: "Process this week's client work — summarize the project status, draft an update email for each client, and create an invoice for any completed milestones"]

Watch the chain fire.

> [SHOW: Claude activating skills in sequence]

First — the project status skill activates. It reads my project files, checks what's been updated, produces a status summary for each active client.

Then — the email drafter picks up. It takes each status summary and drafts a personalized update email. Pulls from brand-context for voice. References the conversation history for each client.

Then — the invoice generator. It checks the status summaries for completed milestones, and for each one, generates a branded invoice.

> [SHOW: the outputs — 3 status summaries, 3 draft emails, 1 invoice]

Three skills. Sequential. The output of each feeds the next. And I said one sentence.

That's chaining. Departments working in sequence. Research hands off to writing. Writing hands off to scheduling. Status hands off to communication. Communication hands off to billing.

### Stacking — The Layers (3:00–5:30)

Now stacking is different. Stacking is when multiple skills are active simultaneously on the same task. They don't run in sequence — they run in parallel, layering on top of each other.

> [SCREEN: Claude terminal]

> [TYPE: "Create a client proposal for Acme Corp — AI consulting engagement, 3-month scope"]

Now watch `/context` while this runs.

> [TYPE: /context]

> [SHOW: context view — multiple skills loaded at the same time]

Three skills loaded simultaneously. The proposal template skill — it knows the structure, the sections, the format. The brand applicator — it's applying my colors, logo, typography. And the voice skill — making sure the copy sounds like me.

They're not waiting for each other. They're all active at the same time. The proposal comes out structured correctly, branded correctly, and written in my voice — because three skills layered their expertise onto one task.

That's stacking. Not a pipeline — a filter stack. Like applying three photo filters at once. Each one adds a dimension.

### Combined — Chains with Stacks (5:30–7:30)

And the real power is when you combine both.

> [TYPE: "Process this week's finances and produce a branded report"]

This is a chain — receipt scanner runs first, then expense categorizer, then report generator. Sequential. Pipeline.

But the brand applicator is stacked on top of the entire chain. Every output — the spreadsheet, the dashboard, the report — comes out branded. The brand skill isn't a step in the pipeline. It's a layer that applies to every step.

> [SHOW: the financial outputs — all consistently branded]

Chaining handles the workflow. Stacking handles the quality. Together, you get output that follows a process AND meets your standards.

### Auto-Routing — You Don't Orchestrate This (7:30–9:00)

Now here's the thing that makes all of this practical. You don't manually tell Claude "use skill A, then skill B, then stack skill C on top." You just describe what you want.

Claude reads your request. It scans the available skills — remember, it has the menu of names and descriptions from tier one. It figures out which skills apply, in what order, and whether they should chain or stack. You just talk to it like a person.

"Plan my next batch of videos." Chain: ideation → scripting → calendar.

"Create a branded proposal." Stack: template + brand + voice.

"Process finances and send me a report." Chain with stack: scanner → categorizer → report, with brand layered on top.

Once your skills are set up, you're talking to your AI employees the way you'd talk to real ones. "Hey, plan my content." "Hey, process the receipts." "Hey, draft those client emails." The routing happens automatically.

And this is why focused skills beat mega-skills. If you'd built one giant "do everything" skill, Claude couldn't chain or stack. It would load one enormous file and try to do everything at once. But with focused skills, Claude can compose them — chain when it needs sequence, stack when it needs layers, and use only the ones each task requires.

### The Architecture Summary (9:00–9:30)

> [SCREEN: simple diagram]

```
CHAINING = Departments (sequential pipeline)
  A → B → C
  Each skill's output feeds the next

STACKING = Layers (parallel enrichment)
  A + B + C
  All active on the same task simultaneously

COMBINED = Pipeline with quality layers
  (A → B → C) + D stacked on everything
```

### What's Next

Your skills can chain and stack. In the next video, we make them run without you — scheduled tasks that fire on a clock. Morning briefing at 7am. Receipt scanner every Friday. Your AI employees working while you sleep.
