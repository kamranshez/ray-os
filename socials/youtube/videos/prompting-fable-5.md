---
tags: [youtube, script, claude-code, fable-5]
status: draft
date: 2026-06-10
---
## Title Options

| #   | Formula                       | Title                                                  |
| --- | ----------------------------- | ------------------------------------------------------ |
| 1   | Bold claim + anthropomorphism | Claude Doesn't Want Your Instructions Anymore          |
| 2   | Bold claim + specificity      | How to Prompt Fable 5 (Everything Just Reversed)       |
| 3   | Curiosity gap + exclusivity   | Anthropic Changed How You're Supposed to Prompt Claude |

**Frame:** how to prompt and use Fable 5. Five shifts, organized by one analogy: you were managing a junior, you're now directing a senior.
**Coined frame:** stop supervising, start directing.
**Format:** single-topic deep dive, ~13 min
**Pitch system:** masterclass only (soft anchor 1:30 + closing urgency). No newsletter mention anywhere.
**Demo surface:** masterclass landing page
**Free artifact:** prompt-debt audit skill, free inside the class platform (signup tripwire, no credit card)
**Urgency numbers:** Loopy AI launches next week. 30% off Lifetime ends in 5 days. Every current class included in Lifetime.

---

## Hook (0:00 - 0:35)

*Screen: terminal with the Fable 5 banner, then a slow scroll of Anthropic's prompting guide.*

So Fable 5, Anthropic's new flagship model, dropped yesterday, and it's live in Claude Code for everyone right now. And I spent most of yesterday doing something I didn't expect to be doing. Re-learning how to prompt.

Because alongside the model, Anthropic published a guide on how to prompt it, and it quietly reverses half of what we were taught over the last two years. The caps lock. The checklists. The "think step by step." Not just unnecessary now. Some of it actively makes the model worse, and one habit can get your request rejected entirely.

An engineer on the Claude Code team summed up the shift in one line, and it's the thesis of this whole video. With previous models, his job was checking whether Claude was doing the work right. With Fable 5, his job is checking whether Claude is doing the right work.

## The Reframe (0:35 - 1:30)

*Screen: simple progressive-reveal drawing. A junior figure with a rulebook, then a senior figure at the same desk.*

Here's the way to think about everything that follows.

For two years, you've been managing a junior. Smart, fast, but it missed instructions, skipped steps, gave up early. So you compensated. You wrote rules in all caps. You listed every edge case. You repeated yourself three times because once was not enough. And that was correct. Juniors need scaffolding.

Yesterday, a senior sat down at that desk. And every habit you built for the junior is now the wrong habit. Not because the senior ignores your rules. The opposite. It follows them to the letter, even when it can see a better path. You hired senior judgment, and your old prompts override it.

So this video is the new operating manual. Five shifts in how you prompt and use this model, from smallest to biggest.

## Soft Anchor (1:30 - 2:00)

Before we get into them, this video is sponsored by myself and my Claude Code Masterclass. Over 1,500 engineers from companies you've definitely heard of have taken it, and many are now the best Claude Code user at their company.

And you're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. That's the whole point. Loopy AI launches next week, every current class is included in Lifetime, and the 30% Lifetime discount ends in five days. Link below.

## Shift 1: Stop Micromanaging (2:00 - 4:15)

*Screen: a real CLAUDE.md scrolling. Highlight the ALL-CAPS lines.*

Shift one. Delete the scaffolding you wrote for the junior.

Anthropic is blunt about this. The prompting guide says, quote: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality." And their launch tips repeat it: "Instructions written for prior models anchor Fable to stale patterns, let it use its own judgment first."

*Screen: both quotes side by side. Linger.*

There's a name for what's sitting in your files. I call it prompt debt. Every CRITICAL, every MUST, every eleven-item checklist was a patch over a weakness some previous model actually had. The weakness is gone. The patches now bind the model to old behavior.

Four things to hunt down today.

One, emphasis inflation. CRITICAL, MUST, ALWAYS. Older models under-triggered, so we shouted. This model doesn't under-trigger, so the same shouting causes over-triggering. Anthropic's own docs now say to replace "CRITICAL: You MUST use this tool when" with just "use this tool when." One carve-out: safety rules stay loud. "NEVER force push to prod" is not scaffolding, it's policy.

Two, enumerated edge cases. Replace the list with one sentence describing the outcome you want.

Three, anti-laziness nudges. "If in doubt, do X" now means X happens constantly.

Four, and this is the one that can reject your request outright: any line asking the model to show, echo, or explain its reasoning. Fable 5 never exposes its raw chain of thought, and a classifier watches for attempts to extract it. When that line trips it, your request doesn't fail, it gets rerouted to Opus 4.8, clearly labeled, billed at Opus prices. You asked for the newest model and your own prompt downgraded you to the previous one. "Explain your reasoning step by step" was a best practice we all taught. Delete it.

## Shift 2: Talk Normally (4:15 - 6:00)

Shift two. Once the shouting is gone, what does good prompting actually sound like? Calm, short, and outcome-shaped. Anthropic shows you, and I want to put their actual examples on screen because the shape of them is the lesson.

The guide says you can now, quote, "steer most behaviors with a brief instruction rather than enumerating each behavior by name." Here's their replacement for the entire verbose-output problem:

*Screen: the verbatim snippet, full screen, linger 3 seconds.*

> "Lead with the outcome. Your first sentence after finishing should answer 'what happened' or 'what did you find': the thing the user would ask for if they said 'just give me the TLDR.' Supporting detail and reasoning come after."

Two sentences. No caps. And Anthropic says it works as well as listing every verbose habit by name.

Here's the one for long autonomous runs, where models used to invent status updates:

*Screen: the grounding snippet, full screen, linger 3 seconds.*

> "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly."

One plain paragraph, and in their testing it "nearly eliminated fabricated status reports even on tasks designed to elicit them." Nearly eliminated.

Now notice what both snippets have in common. Neither tells the model how to do its job. They describe what you want from the result. That's the entire grammar of prompting this model: what, not how. Your old prompts shouted at a model that wasn't listening. The new ones talk normally to a model that is.

## Shift 3: Give Context, Not Constraints (6:00 - 8:00)

Shift three, and this is where it gets interesting, because shifts one and two were about writing less. This one is about what you write instead.

The same Claude Code engineer from the intro gives the perfect example. Instead of writing "keep it simple, don't over-engineer this," he writes: this feature is an experiment, there's a real chance we delete it in a month, so don't build anything that would be painful to throw away.

Look at the difference. The constraint told the model how to behave. The context lets it work out how to behave, and catch things you never thought to ask for. Maybe it skips the abstraction layer. Maybe it leaves a comment for whoever deletes it. You didn't specify any of that, and you didn't have to. Anthropic's guide has the same advice in general form: give the reason, not only the request. Tell it what you're working on, who it's for, what the output enables. The model connects the task to the intent instead of guessing at it.

And this extends to before the work even starts. The engineer treats Fable as a thought partner. He starts with a small spec and asks the model to interview him about the implementation before writing the final spec. Or hands it an idea and asks for a few directions with HTML mockups to review. The senior doesn't just execute. You can think with it, and the failure mode it catches is the expensive one: not knowing what you actually want until after it's built.

## Shift 4: Objectives, Not Tasks (8:00 - 10:30)

Shift four is the big one. Anthropic's own framing: move from providing tasks to providing objectives. Describe what done looks like and how to verify it, then let Fable find the path.

This works now because of what changed under the hood. This model runs for hours and stays coherent. It tests its own work. It dispatches subagents and keeps them on track. The bottleneck stopped being the model's stamina and became the quality of your goal definition.

*Screen: terminal on the masterclass landing page repo. Narrate over pre-recorded footage.*

Let me show you the shape of this on a real project. This is the landing page for my masterclass. The old way, I'd feed Claude a task at a time: build this component, fix this section, now wire it up. Me as the project manager, checking each step.

The new way: I give it the spec and an objective. Implement this fully, then verify each part against the spec and report anything that differs. And then I leave. Claude Code has two features built exactly for this, /goal, which keeps the model working until the objective is genuinely met instead of stopping at the first plausible answer, and workflows, which fan out agents to verify the work. The demo you're watching ran while I made coffee. What I came back to wasn't output to review. It was a report on which parts of the spec are done and which one deviated and why.

That's the supervision-to-direction flip from the intro, made concrete. You're not reviewing keystrokes anymore. You're reading a report from someone you delegated to.

## Shift 5: Raise Your Ambition (10:30 - 11:45)

Shift five is the simplest one to say and the hardest one to internalize. Anthropic's first tip for this model is just: give it bigger, more ambitious tasks than what previous models could handle.

The teams getting the most out of Fable 5 are pointing it at their hardest unsolved problems, not their routine ones. Testing it on the easy stuff actually undersells it, because on easy stuff it just looks like a slightly better version of the old model. The gap shows up on the work you assumed was out of reach. The engineer from earlier edits his videos with it. Their guidance is literally: if there's something you assumed LLMs couldn't do, give it a chance.

One practical dial to know about: effort. It's a setting, low up to xhigh, that controls how hard the model thinks per request. High is the default, and here's the part worth remembering: lower effort on Fable 5 often beats the maximum setting on prior models. All those paragraphs we wrote begging the model to be thorough? That's a knob now.

## What Survives (11:45 - 12:30)

So if the how-instructions are getting deleted and the tasks are becoming objectives, what's left that's yours?

Your preferences. Your conventions, your company's rules, your taste about what done looks like. The model will never wake up knowing your team ships behind feature flags, or that claims over ten thousand dollars need a police report. Those lines never expire. Everything teaching the model how is on a countdown timer. Everything telling it what you want is a permanent asset. That's the lens for every line you keep.

And one level up: at the Code with Claude keynote in Tokyo, hours after launch, Anthropic said the developers who win are the ones whose setups can absorb the next jump in intelligence, and that smarter models do more with basic primitives, a file system, a sandbox, and, quote, "far less with sophisticated or too complex harnesses." Simpler setups, clearer objectives, your judgment encoded as preferences. That's the durable stack.

## Close (12:30 - 13:15)

So that's the new manual. Stop micromanaging, talk normally, give context instead of constraints, hand over objectives instead of tasks, and aim it at bigger problems than you used to.

The first shift is the one to do today, and I built a skill that does it for you. It scans your CLAUDE.md and your skills folder and flags every line of prompt debt: the caps, the checklists, the nudges, and the reasoning lines that can get you rerouted. It's called the prompt-debt audit skill and it's free inside the class platform. No credit card, just sign up and grab it. Link's in the description, and while you're in there, install the masterclass MCP. It'll recommend videos based on what your workflow actually looks like.

If you want the full system, how I structure skills, CLAUDE.md files, and objectives so they don't rot when the next model drops, that's the masterclass. And the timing genuinely matters this week: Loopy AI launches next week, every current class is included in Lifetime, and the 30% Lifetime discount ends in five days. After that it's gone. There's a 14-day money-back guarantee, and less than 0.2% of buyers have ever asked for a refund. If you have questions, email me directly, my address is in the description.

And tell me in the comments: what's the most ambitious thing you've thrown at Fable 5 so far? The best ones are going in a future video. See you in the next one.
