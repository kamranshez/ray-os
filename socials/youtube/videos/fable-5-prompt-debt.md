---
tags: [youtube, script, claude-code, fable-5]
status: draft
date: 2026-06-10
---

## Title Options

| # | Formula | Title |
|---|---------|-------|
| 1 | Bold claim + anthropomorphism | Claude's New Model Hates Your Prompts |
| 2 | Bold claim + specificity | Fable 5 Just Made Your Prompt Library Obsolete |
| 3 | Curiosity gap + exclusivity | Anthropic Quietly Admitted Your Prompts Are the Problem |

**Coined term:** prompt debt
**Format:** single-feature deep dive, ~11 min
**Pitch system:** masterclass only (soft anchor 1:30 + closing urgency). No newsletter mention anywhere.
**Demo surface:** masterclass landing page / MCP
**Free artifact:** prompt-debt audit skill, free inside the class platform (signup tripwire, no credit card)
**Urgency numbers:** Loopy AI launches next week. 30% off Lifetime ends in 5 days. Every current class included in Lifetime.

---

## Hook (0:00 - 0:30)

*Screen: terminal, Fable 5 model banner visible. Then a quick flash of the docs page with one sentence highlighted.*

So Fable 5 dropped yesterday, and I did what I always do when a new model comes out. I pointed it at my repo, ran my usual skills, and waited to be impressed.

And a couple of them came back... worse. Not broken. Just flatter. More mechanical. Like the model was working with one hand tied behind its back.

Then I found one sentence buried in Anthropic's new prompting guide that explains the whole thing. They wrote, and I'm quoting directly: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality."

Your prompts. The ones you spent months refining. They're now actively hurting the model. There's a name for this, and once you see it you can't unsee it. It's prompt debt.

## The Problem (0:30 - 1:30)

*Screen: a real CLAUDE.md or SKILL.md scrolling slowly. Highlight the ALL-CAPS lines as they're mentioned.*

If you've been using Claude Code for more than a few months, your prompt files probably look like mine did. CRITICAL: you MUST do this. IMPORTANT: never do that. Numbered lists covering every edge case you ever hit. The same instruction repeated three times in different words because once wasn't enough.

And here's the thing. None of that was wrong when you wrote it. Older models genuinely needed it. They'd miss instructions, skip steps, give up early. So you compensated. Every one of those ALL-CAPS lines is a patch over a weakness some previous model actually had.

But a patch over a weakness becomes a problem when the weakness goes away. That's the debt part. You borrowed against the model's limitations, and with Fable 5, the bill just came due.

## Soft Anchor (1:30 - 2:00)

Before we get into what the guide actually says, this video is sponsored by myself and my Claude Code Masterclass. Over 1,500 engineers from companies you've definitely heard of have taken it, and many are now the best Claude Code user at their company.

And you're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. That's the whole point. Loopy AI launches next week, every current class is included in Lifetime, and the 30% Lifetime discount ends in five days. Link below.

## The Analogy: The Onboarding Doc (2:00 - 3:30)

*Screen: simple progressive-reveal drawing. A document with rules, a junior figure, then a senior figure reading the same document.*

Here's the way to think about this.

Imagine you hire a junior engineer. They're smart but new, so you write them an onboarding doc. Always run the tests before pushing. Never touch the deploy config. If the build fails, check these five things in this exact order. And it works. The doc is scaffolding, and juniors need scaffolding.

Two years later you hire a staff engineer. Fifteen years of experience. And on day one, you hand them the same doc.

Now here's what's interesting. The staff engineer doesn't ignore the doc. That's the trap. They're a professional, so they follow it. To the letter. They check those five things in that exact order even when they can see the actual problem instantly. They ask permission for things they should just do. You hired senior judgment and then you overrode it with rules written for someone who didn't have any.

That's exactly what's happening when Fable 5 reads your old prompts. It's an extremely strong instruction follower. The guide is explicit about this. So every over-specified instruction doesn't get ignored, it gets obeyed. Your micromanagement is no longer compensating for weak judgment. It's overriding strong judgment.

## What the Guide Actually Says (3:30 - 7:45)

*Screen: the actual docs page. Scroll slowly, highlight each quoted line. Let each one linger.*

So let's go through the guide, because Anthropic is unusually direct in this one.

**First: brief instructions now beat enumerated ones.**

The guide says instruction following is improved enough that, quote, "you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." And they show you what that looks like. This is the actual replacement prompt from the docs:

*Screen: the verbatim snippet from the guide, full screen, linger 3 seconds.*

> "Lead with the outcome. Your first sentence after finishing should answer 'what happened' or 'what did you find': the thing the user would ask for if they said 'just give me the TLDR.' Supporting detail and reasoning come after."

Look at what that is. Two sentences. No caps. No MUST. And Anthropic says that one instruction is as effective as listing every verbose habit by name. The era of the 40-line behavioral checklist is over. One good sentence does what ten emphatic ones used to.

And notice the shape of it, because every sample prompt in this guide has the same shape. Here's the one for long autonomous runs, where models used to invent status updates:

*Screen: the grounding snippet, full screen, linger 3 seconds.*

> "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly."

Plain sentences. Calm. And their result from testing it, quote: it "nearly eliminated fabricated status reports even on tasks designed to elicit them." Nearly eliminated. One paragraph. That's what prompting this model looks like. Your old prompts shout at a model that wasn't listening. The new ones talk normally to a model that is.

**Second: the polarity flipped on emphasis.**

This one is subtle and it's where most prompt debt lives. All that anti-laziness language we wrote, the "if in doubt, use the tool," the "CRITICAL: you MUST," that language existed because older models under-triggered. They'd skip the tool, skip the step.

The new models don't under-trigger. So the same language now causes over-triggering. Anthropic's own best-practices page says it directly: where you might have said "CRITICAL: You MUST use this tool when," you should now just say "use this tool when." Your prompt was a thermostat set for a cold room, and the room got warm. The setting didn't break. The room changed.

**Third, and this is the one that genuinely surprised me: some of your old instructions now cause refusals.**

Fable 5 never returns its raw chain of thought. There's a classifier watching for attempts to extract it. And the guide warns that prompts or skills that tell the model to, quote, "echo, transcribe, or explain its internal reasoning as response text" can trigger that classifier and bounce your request down to a fallback model.

Think about how many skills have a line like "explain your reasoning step by step" or "show your thinking before answering." That was a best practice. We taught it. It's in thousands of CLAUDE.md files right now. On Fable 5, that line is a landmine. Not a style problem. A refusal trigger.

**Fourth: effort replaced a lot of prompting entirely.**

The guide says lower effort settings on Fable 5 "often exceed xhigh performance on prior models." A lot of what we used prompts for, push harder here, be more thorough there, is now a dial in the API. You don't write paragraphs to make the model try harder anymore. You turn a knob.

So add it up. Brief beats enumerated. Emphasis over-triggers. Reasoning instructions cause refusals. Effort replaced thoroughness prompting. Four different ways the prompts you wrote for the last generation actively work against this one.

## Demo: Auditing a Real Skill (7:45 - 9:15)

*Screen: split view. Left, the bloated SKILL.md. Right, Fable 5 running against the masterclass landing page repo. Narrate over pre-recorded footage, do not build live.*

Let me show you what this looks like in practice instead of in theory.

This is a skill from my masterclass landing page repo. It generates components for the site, and I wrote it months ago, which means it's a museum of prompt debt. Look at this. Three CRITICAL blocks. An eleven-item checklist for a four-step task. And right here, the landmine: "explain your reasoning for each design decision before writing code."

*Highlight each as it's named. Linger two seconds on each.*

Running it on Fable 5, watch what happens. It dutifully marches through all eleven checklist items, including the seven that don't apply to this component. It writes me a reasoning essay I didn't ask for. The output works, but it's generic. Staff engineer, micromanaged.

Now here's the same skill after the audit. Sixty percent shorter. The checklist became one sentence about what done looks like. The CRITICAL blocks are gone. The reasoning instruction is deleted entirely.

*Side-by-side of the two outputs. Let it linger.*

Same model, same task. The stripped version is just better. More specific to the actual component, better judgment calls on the parts I didn't specify, and it got there faster. I didn't add anything. I only removed. That's the strange part of paying down prompt debt. The work is deletion.

## The Part Nobody's Connecting (9:15 - 10:45)

*Screen: simple two-column drawing, progressive reveal. "Capability uplift" on one side, "encoded preference" on the other.*

Now here's the thing I haven't seen anyone say about this yet.

A few months ago I made a video about skill evals, and in it, Anthropic drew a distinction between two types of skills. Capability uplift, which is a skill that teaches the model something it can't do well on its own. And encoded preference, which is a skill that sequences things the way you want them done. The model could already do every step, you're just encoding your taste.

At the time that felt like a nice taxonomy. Fable 5 turns it into a survival map.

Because prompt debt isn't evenly distributed. It's concentrated almost entirely on the capability side. Every instruction that taught the model how to do something is on a countdown timer, because models keep getting better at how. Your preferences, your conventions, your company's rules about what done looks like, those don't expire. The model will never wake up one day knowing that your team ships behind feature flags or that claims over ten thousand dollars need a police report.

So the audit question for every line in every prompt file you own is: is this teaching the model how, or telling it what I want? The how lines are debt. The what lines are assets.

And this also explains why Anthropic shipped skill evals before they shipped this model. An eval is a debt detector. It's the thing that tells you the base model caught up and the scaffolding can come down. They built the measuring tool, then they shipped the model that makes you need it. Every model generation from here on out, the half-life of a "how" instruction gets shorter. The people who keep winning won't be the ones with the biggest prompt libraries. They'll be the ones with the smallest.

## What To Actually Do (10:45 - 11:30)

*Screen: the audit checklist, revealed one line at a time.*

So the practical version. Open your CLAUDE.md and your skills and hunt for four things.

One, emphasis inflation. CRITICAL, MUST, ALWAYS, IMPORTANT. Downgrade them to plain sentences and see if anything breaks. It mostly won't.

Two, enumerated edge cases. Replace the list with one sentence describing the outcome you want.

Three, anti-laziness nudges. "If in doubt, do X" now means the model does X constantly. Cut them.

Four, and do this one today: any line asking the model to show, echo, or explain its reasoning. On Fable 5 those can trigger refusals. Delete them.

I built a skill that does this whole audit for you. It scans your CLAUDE.md and your skills folder, flags all four categories, and tells you exactly what to cut. It's called the prompt-debt audit skill and it's free inside the class platform. No credit card, just sign up and grab it. Link's in the description, and while you're in there, install the masterclass MCP. It'll recommend videos based on what your workflow actually looks like.

## Closing Pitch (11:30 - 12:15)

So that's prompt debt. The prompts that made old models better make this one worse, and the fix is an audit, not a rewrite.

If you want to go deeper, the masterclass covers how I structure skills and CLAUDE.md files so they don't rot when the next model drops, the whole system, not just the audit. And the timing genuinely matters this week: Loopy AI launches next week, every current class is included in Lifetime, and the 30% Lifetime discount ends in five days. After that it's gone.

There's a 14-day money-back guarantee, and less than 0.2% of buyers have ever asked for a refund. If you have questions, email me directly, my address is in the description.

Link below. See you in the next one.
