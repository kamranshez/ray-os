---
duration: "12-16 min"
batch: 4
order: 12
batch_name: "L3 Task Lifecycle"
class: "loopy-ai"
chapter: "Writing Effective Goals"
aliases: [writing-effective-goals]
---

The runtime owns the loop now. The only thing left for you to own is the goal. So the goal is where all the leverage went.

In the last segment we handed the L3 outer loop to the runtime. A cheap judge reads every turn, a hidden message forces auto-continuation, and the expensive worker runs until the goal clears. You don't write the bash anymore. You write the objective the whole machine grinds against.

Which means the objective is no longer a prompt. It's a spec for an autonomous process that might run for fifty turns without you in the room. Write it like a wish and you get a wish: vague, looping forever, or self-reporting "done" on work that was never done.

This segment is how to write the one artifact that still matters.

---

## A goal is not a task

The most expensive mistake here is treating `/goal` like a bigger version of a chat prompt.

Vincent Koc ran goal mode on OpenClaw for three days, thirteen runs, a stack of PRs. His one line for this whole segment: "/goal is not a 'do my ticket' button. It's a constraint workflow. I want to keep the ship on course."
Source: https://x.com/vincent_koc/status/2050983370902184019

Sit with that. A task says do this thing. A constraint workflow says here is the destination, here are the walls you may not cross to get there, and here is exactly how you'll know you arrived. The model fills in the middle. You own the edges.

This is the same shape we keep meeting. In the strip-the-model-out segment, a loop was five primitives: trigger, work, check, terminate, state. A goal file is those same primitives written in prose for a human to read and a judge to grade. The trigger is you running `/goal`. The work is the worker's turns. The check is your DONE WHEN. The terminate is your turn cap. The state is the goal file itself, sitting on disk, surviving every context reset the way Ralph's three-file contract did.

You already know the parts. Writing an effective goal is just filling each slot so the judge can't be fooled and the worker can't wander.

[IMAGE: dark canvas, left side a short chat bubble labeled "task: do my ticket", right side a structured document with labeled sections GOAL / CONSTRAINTS / DONE WHEN, an arrow between them labeled "the upgrade you have to make"]
![[images/writing-effective-goals/task-vs-goal.png]]

---

## The nine sections

There's a template circulating that nails the anatomy. Avi Chawla's nine-section goal file.
Source: https://x.com/_avichawla/status/2055930732930122158

Nine sections sounds like a lot. It isn't. Most are one line. Here's the whole thing, and why each slot exists.

**GOAL.** The objective in one sentence. Name the outcome and the source of truth in the same breath. Not "improve the app." "Make the dashboard render real revenue from the Stripe data, matching the live reference at watchllm.com."

**CONTEXT.** The background the worker would otherwise burn turns rediscovering. Where the code lives, what the stack is, what's already done. Every fact you put here is a turn you don't pay for later. Remember the judge is cheap and the worker is not, so anything that stops the worker exploring aimlessly is money.

**CONSTRAINTS.** The hard walls. This is the constraint in "constraint workflow." No paid APIs. No production writes. No OAuth flows without approval. Seeded data only where a real integration isn't safe. These are the moves the model may not make even if they'd close the goal faster.

**PRIORITY.** The order. Easy wins first, dependencies before dependents. An autonomous worker with no priority order will happily start with the hardest, most ambiguous slice and strand itself there.

**PLAN.** The explicit approach. Not a full spec, a spine. Audit, then map, then build in dependency order. This is the difference between a worker that executes and a worker that wanders.

**DONE WHEN.** The one that decides whether you have a loop at all. A binary, observable outcome. `pytest exits 0`. "The dashboard loads and shows non-zero revenue pulled from the seeded Stripe table." Never "the app is production-ready," never "the migration is complete." We'll come back to why those two specific phrasings are poison.

**VERIFY.** A specific command whose raw output lands in the transcript. `npm test`. `curl localhost:3000/api/revenue`. This is the move that saves you. Recall from the goal-mode segment that the judge grades the transcript and nothing else. If the worker runs a real command and the real output prints into the transcript, the cheap judge is now reading machine evidence instead of the worker's own summary of itself.

**OUTPUT.** What to surface when it's done. A requirement-by-requirement report. The final diff. The dashboard URL. So the end of a fifty-turn run is something you can actually read in thirty seconds.

The ninth slot is the **turn cap** itself, which lives in how you invoke goal mode, not in the prose. Budget is a first-class part of the goal, not an afterthought, because budget exhaustion is not completion. We established that in the last segment and it's worth carving into the wall here too.

[IMAGE: dark canvas, a single-page goal file with nine labeled rows GOAL CONTEXT CONSTRAINTS PRIORITY PLAN "DONE WHEN" VERIFY OUTPUT, plus a small budget gauge in the corner, each row one short handwritten line]
![[images/writing-effective-goals/nine-sections.png]]

---

## Anchor on the theoretical max

There's one trick that changes what a goal can produce, and it has nothing to do with the template.

Max Weinbach ran goal mode to optimize a speech model for a Snapdragon chip and roughly tripled its performance on the NPU. The reusable tip from how he started it: "A good way to start it out is having it calculate the theoretical maximum performance and work towards the goal."
Source: https://x.com/mweinbach/status/2054216215007010827

Read what that does. Most people anchor the goal to current performance. "Make it faster." Faster than what? The worker finds a ten percent win, the DONE WHEN is satisfied in spirit, and it stops. You anchored on the present, so the present is the ceiling.

Weinbach anchored on the upper bound. First turn: compute what this chip could theoretically do if everything were perfect. Now the goal isn't "faster," it's "close the gap to the theoretical max." Ten percent isn't done anymore. The worker keeps grinding because the target is the physics of the hardware, not yesterday's number.

This generalizes past kernels. The theoretical max for a landing page is every Lighthouse subscore at 100. For a test suite it's full coverage with zero flakes. For a cold-email rewrite it's the best email a human expert in the domain could write. You don't always reach it. That's fine. The point is the gap to the ceiling is what gives an autonomous loop somewhere to keep climbing, instead of letting it cash out at the first local win and call it a day.

Put the theoretical-max calculation in the PLAN as turn one. The worker derives the ceiling, then every later turn measures the gap.

---

## The three ways a goal rots

Three failure modes, and each one maps cleanly to a slot you got lazy on.

**Success criteria that defer to the model.** "Make the app production-ready." Production-ready according to whom? Nothing in the world can prove that string true, so the loop either runs until the budget dies or the worker decides it feels production-ready and the judge, reading only the transcript, nods along. This is the completion-audit trap from the goal-mode segment, walking in through a vague DONE WHEN. The fix is a DONE WHEN the worker's own output can prove, backed by a VERIFY command whose raw result the judge can read.

**No kill criteria.** A goal with a destination but no off-ramp. "Complete the migration" with no turn cap and no failure condition will, on a goal it cannot actually reach, burn every dollar you gave it auto-continuing forever, because the judge keeps saying not done and the runtime keeps obeying. Every goal needs a turn cap and ideally an explicit "stop and ask if X" line. Budget exhaustion is a decision point, not a defeat.

**No tradeoff order.** The goal wants three things and never says which wins when they collide. Fast, correct, and cheap, with no ranking. So the worker hits the first conflict, makes a coin-flip call, and you discover three runs later it quietly sacrificed correctness for speed because nothing told it not to. CONSTRAINTS and PRIORITY together are your tradeoff order. Write the ranking before the worker has to guess it at turn nineteen with no one watching.

Notice the pattern. Every rot is a slot you left soft. A goal is only as strong as its weakest section, and the weak one is always the one you couldn't be bothered to make concrete.

[IMAGE: dark canvas, three failing goal cards in a row, each crossed out, labeled "defers to the model", "no kill switch", "no tradeoff order", each with a small arrow pointing to the template slot that fixes it]
![[images/writing-effective-goals/three-failure-modes.png]]

---

## Demo

Open the real one. This is the WatchLLM goal I actually ran to build a Promptwatch-style product, on screen, top to bottom.

**One.** Read the GOAL line out loud. One sentence: build the app so the dashboard runs on real data and matches the live reference. Notice the source of truth is named right there in the sentence, the live reference URL. The judge now has something concrete to grade against.

**Two.** Scroll to CONSTRAINTS. Point at the explicit wall: avoid paid, external, OAuth, and production actions unless approved, provide safe local fallbacks instead. This is the constraint workflow in writing. The worker is free to build anything inside these walls and forbidden to touch anything outside them.

**Three.** Scroll to PLAN. Read the numbered phases: audit the codebase, produce an implementation map, build slices in dependency order, and for each slice do schema, then logic, then tests, then verification. That last clause is the borrowed-verifier habit from the L2 segments, baked into the plan: "regularly spawn verifier subagents to click around the local app and compare against the live reference." The goal carries its own attacker.

**Four.** Scroll to SUCCESS, which is this file's DONE WHEN. Read the checkable end states: the app runs locally, the core loop works end to end, the dashboard is powered by real data, REST validation passes, browser verification proves the flows. Every one is something a command or a subagent can confirm and print into the transcript. Nothing in there says "production-ready."

**Five.** Run it. `/goal` against this file with a turn cap. Let the camera sit on a few auto-continuations so you can see the cheap judge clearing turn after turn, reading the `npm test` and `curl` output the VERIFY lines forced into the transcript, until the SUCCESS conditions go green.

Total demo: five minutes. The point lands without narration. This is one page of prose, and it drove an autonomous build that would've been fifty manual prompts.

---

## Key Insight

> When the runtime owns the loop, the goal file is the only thing you still own. Write it as a constraint workflow with a provable DONE WHEN, anchor it to the theoretical max, and you've turned one page of prose into a worker that won't wander and can't lie about being finished.

---

## Where we go next

You can write a single goal now. Tight constraints, a DONE WHEN the judge can't be talked out of, anchored to the ceiling instead of the present.

The reflex this builds is to over-specify: to sit down and pre-sequence the entire backlog into one giant goal before the worker takes a single step. That's the next trap, and the next segment is about why pre-sequencing the backlog quietly kills the thing that made these loops worth building.

And much later, when we climb to the top of the stack, you'll see this same artifact again at a bigger scale. A `/goal` is the tactical version of a commander's intent doc: same anatomy, same constraint-workflow spirit, narrower scope. We'll get to mission command near the end of the class. For now, just notice you've been writing intent docs this whole time.

See you in the next one.
