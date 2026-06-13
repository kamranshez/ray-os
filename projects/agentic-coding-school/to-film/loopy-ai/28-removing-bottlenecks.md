---
duration: "8-12 min"
batch: 8
order: 28
batch_name: "L7 Closing"
class: "loopy-ai"
chapter: "Removing Bottlenecks"
aliases: [removing-bottlenecks]
---

By now every loop in your fleet hands its work up to one place. You. And the moment that became true, you became the slowest part of the system.

That is not a failure. That is the destination. The whole climb up the stack was about moving the bottleneck off the model, off the harness, off the prompts, and up onto you. Now it's here. This segment is about what you do when you are the constraint.

The answer is not "work harder." The answer is to keep removing yourself, one bottleneck at a time, until the only thing left in your hands is the thing only you can do.

---

## You are the constraint now

Mission command thinned the decisions coming up. Keeping you in the loop built the pipe that carries them. But a thinner stream into a cleaner pipe is still a stream into you, and you have a fixed number of hours.

So look at where the work actually piles up. It is never the agents. We said this back at the worker loops: the bottleneck is you keeping up, not agent count. Adding a second loop when you can't clear the first one just floods you faster.

[IMAGE: dark canvas, many loops on the left all funneling arrows into a single narrow human figure on the right, work visibly stacking up at the neck of the funnel]
![[images/removing-bottlenecks/human-as-funnel.png]]

The question stops being "how do I do this faster" and becomes "why am I in this step at all." Every place you touch the work is a candidate for removal. Some of those touches are real judgment that only you can supply. Most of them are not. They are habit, or a missing actuator, or a decision you've already made a hundred times and could write down once.

Removing bottlenecks is the discipline of telling those two apart.

---

## The trap: automate everything

The obvious move is to automate everything that can be automated. Anything a loop can touch, hand to a loop. Empty your hands completely.

That instinct is wrong, and the person who'll tell you why is the most agent-pilled skeptic on the timeline. David Cramer, zeeg, the Sentry co-founder, spent eight weeks writing every line of production code through an agent and came out the other side with a warning, not a victory lap. His conclusion: the tools impress you, then you spend a lot of time fighting the current. The feedback cycles take longer, the results are poorer.
Source: https://unrollnow.com/status/1950299260060389764

The sharpest line in that thread is the one that matters here. He kept catching himself "attempting to automate tasks that would have been better solved, for correctness and reliability, as scripts plus prompts, versus prompts alone." His example: "create a pull request." A thing he tried to make the model do, that was better solved deterministically.

We have a name for that already. Strip the model out. If the deterministic version of the step works, the model has no business in that slot. Cramer rediscovered the founding diagnostic of this whole class under fire on a real production service.

So "automate everything" is the wrong target because it automates the wrong layer. It puts a probabilistic model in slots that wanted a script, and it leaves you reviewing slop that a linter would have caught for free.

The right target is narrower and it has a shape.

[IMAGE: dark canvas, a bottleneck funnel split into three colored bands labeled DELETE, SCRIPT, LOOP, with a small fourth band at the bottom labeled KEEP]
![[images/removing-bottlenecks/four-band-funnel.png]]

---

## The four fates of a bottleneck

Take any step where you are the constraint. It has exactly four honest fates, and you try them in order.

**Delete it.** The cheapest automation is the work that didn't need doing. Before you wire anything, ask whether the step exists because the world needs it or because you've always done it. Half of "I'm so busy" is ceremony. Status updates nobody reads. A review gate on a reversible action. Kill the step and the bottleneck is gone for zero dollars and zero tokens.

**Script it.** This is Cramer's lesson. If the step is deterministic, give it a script, not a model. "Create a pull request" is a script. Renaming files, moving cards, posting a digest on a cadence, formatting output, enforcing a gate. The deterministic version is faster, free, and unchallengeable. A model here is a downgrade that also costs money.

**Loop it.** Only now, when the step survives deletion and can't be reduced to a script, does it earn a model in the loop. And it earns a *loop*, not a one-off prompt, which means it earns everything the class made you build for one: a borrowed verifier so it isn't grading itself, an autonomy-dial notch so it knows when to ship and when to ask, a budget and a kill switch so it can't run away, and a slot in the pipe so its output reaches you. A bottleneck you "loop" without those is not removed. It's relocated to 2am.

**Keep it.** Some steps are yours. The irreversible call. The taste judgment. The relationship. The decision that defines what the fleet is even for. We'll spend the whole next segment on what survives here, so for now just mark it: keeping a step is a decision, not a default. You keep it because it passed the other three fates, not because you never questioned it.

The order is load-bearing. People reach for "loop it" first because it's the exciting one, and they end up paying a model to do a script's job badly, or worse, paying a model to do work that should not have existed. Delete, script, loop, keep. Run every bottleneck down that ladder.

---

## Mine your own transcripts

Here is the part people skip. You don't have to guess where you're the bottleneck. The record already exists.

Every place you touched the fleet this week is logged. The action logs from governance. The Slack threads from your command center. Your own terminal history. Your sent folder. That is a dataset of you-as-a-constraint, and you can point a discovery loop at it.

This is L5 turned inward. A discovery loop reads the world to find what should become work. Point one at your own activity and it finds what should become *automation*. It reads a month of your decisions and clusters them: here are forty times you approved the same kind of migration, here are twelve identical "no" replies to scope-creep, here are the three reports you rewrite every Monday by hand.

Each cluster is a bottleneck with its fate already half-decided. Forty identical approvals is an autonomy-dial promotion waiting to happen: you've ratcheted trust forty times, demote the gate. Twelve identical refusals is a constraint that belongs in the intent doc so the loop never asks again. Three hand-rewritten reports is a script, or a loop with a borrowed verifier if the rewrite needs judgment.

The transcript is the borrowed verifier on your own habits. You can't grade your own busyness by vibe any more than a model can grade its own code. But the log doesn't flatter you. It just shows where your hands keep landing.

[IMAGE: dark canvas, a stack of transcript and log files on the left feeding a triager agent in the middle, which outputs a ranked list on the right where each row is tagged delete, script, or loop]
![[images/removing-bottlenecks/transcript-miner.png]]

---

## Don't hand-build your tools either

There is a second bottleneck hiding inside the first, and it's the one you feel last. It isn't the work the loops do. It's the work of building the loops. The prompts. The skills. The verifiers. Right now you write those by hand, and you treat each one as a thing you craft once and keep.

Cramer's other line lands here. "Anything that can be automated, should be automated," he wrote, and then the part that bites: "don't hand write prompts and skills. Build a process that gives you repeatability, even if it's non deterministic, because as the technology advances so will your implementations."
Source: https://x.com/zeeg/status/2045706645108609230

Read that twice. A hand-written skill is frozen at the moment you wrote it. The model underneath it gets better every few months, and your prompt doesn't move with it. So you become the bottleneck on your own tooling, re-tuning by hand, always a step behind the capability you're already paying for.

The fix is the eval-driven loop from the autoresearch segment. You don't author the skill, you author the process that authors the skill. A spec, an eval suite, and a loop that rewrites the SKILL.md and keeps the change when the score goes up. It's the same delete, script, loop ladder, turned on your tools instead of your tasks. When the next model ships, you don't rewrite forty skills by hand. You rerun the loop.

That's the deepest cut. Removing yourself from the doing is the obvious half. Removing yourself from the building is the half that keeps paying off long after you've stopped looking at it.

---

## Removing yourself is a ratchet, not a switch

You do not empty your hands in one weekend. You do it the way you built trust with the autonomy dial: one notch at a time, and only up when the evidence earns it.

Every bottleneck you remove surfaces the next one. Clear the approval queue and you notice you're now the bottleneck on triage. Automate triage and you're the bottleneck on deciding which loops exist at all. That last one is L7, and it's the one you're not trying to remove. That's the point of the climb. You're not automating yourself out of existence. You're automating yourself *up* the stack until the only thing in your hands is the portfolio decision: which loops should exist, which to kill, where the leverage is.

And the ratchet runs backward too, which is the part Cramer was warning about. Automate a step that wanted your judgment and the cost doesn't show up today. It shows up as slop you have to unwind next month, a net liability, in his words. So the dial has a down notch here as well: if a looped bottleneck keeps producing work you have to redo, demote it. Pull it back to script, or back into your hands. Removing yourself is a ratchet you're allowed to reverse.

---

## Demo

Let me run my own week through the ladder, live.

1. Pull the raw material. `cat` the last seven days of the fleet action log, the #loop-deck Slack export, and my shell history into one folder. No editing. This is the evidence.

2. Point a discovery loop at it with one instruction: cluster every point where a human had to act, and for each cluster propose a fate, delete, script, or loop, with the reason. Let it run unattended and post the result to Slack.

3. Read the shortlist on screen. Top cluster: thirty-one times I approved a "publish the daily digest" action. Fate: script. There is no judgment in it. It was a model call that should have been a cron job. Strip the model out, replace with a scheduled task, gone.

4. Second cluster: nine times I typed some version of "no, that's out of scope" at the title loop. Fate: delete the gate by moving the constraint up. I add one line to the loop's intent doc under tradeoff order. The loop stops asking. Nine future interruptions, gone.

5. Third cluster: every Monday I hand-rewrite the week's experiment summary because the auto-generated one reads flat. Fate: loop, not script, because the rewrite is real judgment. So I pair it. A writer skill and the slop-hunter attacker from segment seven, with my last four hand-edits as the borrowed reference. It now drafts something I only tweak instead of rewrite.

6. Tally on screen. One scripted, one deleted, one looped. Three places my hands were landing every week, removed in twenty minutes, and not one of them was "add another agent."

Total demo: six minutes. The point is that the bottleneck list wrote itself. I just read it back and ran each row down the ladder.

---

## Key Insight

> You are the bottleneck now, and that's the win, not the bug. So run every step where your hands land down one ladder, delete, script, loop, keep, until the only thing left in your hands is the one decision a loop can't make for you.

---

## Where we go next

Removing yourself has a floor. You run the ladder, you delete and script and loop everything that'll move, and you hit a small set of steps that won't go. The irreversible calls. The taste. The decision about what the whole machine is for.

That floor is not a failure of automation. It's the shape of the job at the top of the stack. The last segment is about what lives there, and why taste is the thing that survives every loop you'll ever build.

See you in the last one.
