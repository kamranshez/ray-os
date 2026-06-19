---
class: "skills"
chapter: "Build Your AI Employees"
status: "scripted"
tags: [course, script, skills]
lesson: "4.2 The Content Director"
---

## The Content Director

In the last video we built a single skill — the morning briefing. One skill, one job. That's fine for focused tasks. But what happens when you need a workflow that spans multiple skills? Ideation, then scriptwriting, then scheduling — all from one command?

That's what we're building now. Not one skill. A chain. And the result isn't a tool. It's a content director.

### What a Skill Chain Looks Like (0:00–1:30)

Here's the concept. Right now, if I wanted to plan a batch of content, I'd invoke the research skill to find topics. Then I'd take those topics and invoke a writing skill to draft scripts. Then I'd take those scripts and organize them into a calendar. Three separate steps. Three separate prompts. I'm the orchestrator.

But what if I just said "plan and script my next batch of videos" and all three happened automatically?

That's skill chaining. Claude reads the task, checks which skills it has available, and fires them in sequence — ideation first, then writing, then calendar. You don't tell it "use skill A, then skill B, then skill C." You describe what you want and it figures out the order.

And when it works, the result is like having a person who does this whole workflow for you. Not a tool you click through. An employee who handles the entire pipeline.

### Building the Three Skills (1:30–5:30)

We need three skills. I'm going to build them fast because you already know how Skill Creator works.

**Skill one — ideation.**

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build an ideation skill. Given a content niche, it should research what's trending in the last 30 days, analyze competitor content to find gaps, and generate 9 video ideas tagged by funnel stage — top, middle, bottom. Each idea should have a title, a one-line hook, and a relevance score from 1-10."]

> [SHOW: Skill Creator building it — the questions, the draft]

Done. The skill pulls from web search, scores topics, and organizes by funnel stage.

**Skill two — scriptwriting.**

> [TYPE: /skill-creator]

> [TYPE: "Build a scriptwriting skill. Given a video idea with title and hook, write a full script in my voice. Pull from brand-context/voice-tone.md for tone. Structure: hook, problem, solution, demo walkthrough, key insight, closer. Target 8-12 minutes of spoken content."]

This one references the brand context folder we built in Chapter 3. So the scripts come out sounding like me, not like generic Claude.

> [SHOW: the skill draft — process steps pointing to brand-context/ reference files]

**Skill three — calendar.**

> [TYPE: /skill-creator]

> [TYPE: "Build a content calendar skill. Given a list of video ideas with scripts, organize them into a publishing calendar. Assign upload dates — two videos per week, Tuesday and Thursday. Order by relevance score, highest first. Output as a markdown table."]

Simple skill. Maybe 50 lines. It just sorts and schedules.

> [SHOW: all three skills in the skills folder]

Three skills. Each does one thing. Now let's see what happens when they work together.

### The One-Command Demo (5:30–7:30)

> [SCREEN: Claude terminal — fresh session, all three skills active]

> [TYPE: "Plan and script my next batch of videos about Claude Code skills"]

I didn't invoke any skill by name. I just described the task. Watch what happens.

> [SHOW: Claude activating the ideation skill — researching, scoring topics]

The ideation skill fires first. It's researching trending topics, checking what competitors have covered, finding gaps. It comes back with nine ideas, each scored and tagged.

> [SHOW: the ideation output — 9 video ideas with scores and funnel tags]

Now Claude looks at those ideas and realizes it should write scripts for them. The scriptwriting skill kicks in.

> [SHOW: Claude activating the scriptwriting skill — drafting scripts, pulling brand context]

It's writing scripts for the top-scored ideas, pulling my voice profile from brand context. Each script comes out structured — hook, problem, solution, demo, insight, closer.

And then the calendar skill takes over.

> [SHOW: the final calendar output — markdown table with dates, titles, funnel stages]

Nine ideas. Scripts for the top ones. A publishing calendar with dates. From one sentence.

That's auto-routing. Claude read my request, scanned its available skills, and figured out: this needs ideation, then scripting, then calendaring. It picked the order. It passed the output of each skill into the next. No manual orchestration.

### Adding Visual Output (7:30–9:00)

Now I want to push this further. A content director shouldn't just produce text — it should produce visuals too.

I've got a slide deck skill. It takes content and generates a branded presentation — using the visual style from my brand context. Let me add it to the mix.

> [TYPE: "Also create a slide deck for the first video in the batch"]

> [SHOW: Claude picking up the slide deck skill, generating a presentation]

It built a presentation deck for the first video. Branded with my colors, my font choices, my layout preferences. All from the same pipeline.

This is where skills start to feel less like automation and more like an actual creative team. Research, writing, scheduling, and visual design — from one command.

### The Humanizer Gate (9:00–10:00)

One more pattern I want to show you. A skill that runs at the end of a chain as a quality gate.

I call it the humanizer gate. It's a skill that reviews everything the other skills produced and checks for AI-sounding patterns. Generic phrasing. Overused transitions. That "leverage synergies to unlock value" energy.

The way it works: the scriptwriting skill produces a draft. Before Claude saves it, the humanizer skill runs automatically. It scans the text, flags anything that sounds like AI slop, and rewrites those sections to sound more natural.

You add it to the chain by including a line in your scriptwriting skill.md:

```markdown
## Post-processing
Before finalizing any written output, invoke the humanizer skill
to review and clean the text.
```

That's a skill calling another skill. The scriptwriting skill handles the content. The humanizer handles the polish. Neither one is bloated — they're each doing one job. But together, the output is better than either could produce alone.

### Why Chains Beat Mega-Skills (10:00–10:30)

And this is the key architectural point. You could try to build one massive "content director" skill that does ideation AND scriptwriting AND calendaring AND design AND humanizing. But that skill.md would be 800 lines. It would load everything at once. And Claude would get confused about which step it's on.

Chains are better. Small, focused skills that pass output to each other. Each one stays under 200 lines. Each one loads only its own context. And you can mix and match — swap the scriptwriting skill for a different one, add a new skill to the chain, remove one you don't need.

Skills calling sub-skills. That's how you build depth without building bloat.

### What's Next

We've got our content director. In the next video, we're building the operations side — a receipt scanner and an invoice generator. The boring stuff that eats your time. Except now it won't.
