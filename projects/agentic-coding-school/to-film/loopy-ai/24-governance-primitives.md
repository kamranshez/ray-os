---
duration: "12-16 min"
batch: 7
order: 24
batch_name: "L6 Governance"
class: "loopy-ai"
chapter: "Governance Primitives"
aliases: [governance-primitives]
---

The first time a loop costs you a thousand dollars overnight, you build governance. This segment is so you build it before that.

Everything below L6 produces things. Code, PRs, titles, cards, shortlists. L6 doesn't produce anything. L6 watches the things that produce things, and decides whether they get to keep running. It operates on loops as the unit, not on artifacts. That's the whole reason it's its own level.

There are four primitives. Token budgets. Kill switches. Action log review. Retirement. That's it. They are not glamorous. They are the brake, and you don't notice you needed a brake until you're already going too fast.

---

## Why you can't teach this in the abstract

Governance only bites when there's something real to govern.

If I'd opened the class with "you'll need token budgets and kill switches," you'd have nodded and forgotten it. Of course you would. There was nothing running. A brake on a parked car is a piece of trivia.

So we sat this segment exactly here on purpose. At the gate of The Climb, after L3, right before L4 workers. By now you've watched a Ralph loop from the [[ralph-loops]] segment churn through a fresh context window twenty times against a PRD. You've watched a [[goal-mode]] loop keep itself alive against an objective. You've seen the autoresearch loop in [[autoresearch]] run unattended, mutating a prompt, logging every attempt.

Every one of those can run away. The Ralph loop with a brittle outer loop and no clear exit. The goal loop that treats budget exhaustion as completion, the exact trap we named in goal mode. The autoresearch loop that runs all night because nobody told it to stop.

You've now felt the shape of the thing that needs a brake. So now the four primitives stop being plumbing and start being the thing standing between you and a surprise invoice.

The rest of the class assumes you have these. When the [[l4-workers]] segment says "kill switch," it means the one we build here. When [[l5-discovery]] says "token budget," it means this one. We're paying the tax once, up front, so every later loop can spend it.

---

## What "fleet" actually means

Before the primitives, one definition, because every primitive is scoped to it.

A fleet is the set of loops that share one budget, one kill switch, one log directory, and one retirement policy. The boundary is the shared governance, not the shared topic.

Read that twice, because the instinct is wrong. People draw fleet boundaries by what the loops *do*. "These three are my content loops, those two are my code loops." That's not it.

Two loops doing completely different work, one mining sentence cards and one merging Dependabot PRs, governed by the same kill switch and drawing from the same daily budget, are one fleet. Two loops doing nearly identical work, each with its own budget and its own kill file, are two fleets.

The boundary is the governance, full stop. And it matters because the four primitives are scoped to the fleet, not to "every loop running on your machine." If you never draw the boundary, you can't enforce any of them. A budget with no defined scope is a number with nothing to cap.

[IMAGE: dark canvas, two dashed rectangles each labeled "fleet". The left fleet contains two unlike loop icons (a card and a merge arrow) wired to a single shared budget bar, kill file, and log folder. The right fleet contains two similar loops each wired to its own separate budget, kill file, and log. A caption reads "the boundary is the shared governance, not the topic".]
![[images/governance-primitives/fleet-boundary.png]]

---

## The four primitives

Four. No more. If a fifth thing feels load-bearing, it's usually one of these four wearing a costume.

**Token budgets.** Per loop, per fleet, per day. A hard cap, a soft cap, and a daily report. If a loop spends two times its expected budget, it stops. No exceptions, no "let me just finish this one task." The whole point of a budget is that it overrides the loop's own opinion about whether it's nearly done.

**Kill switches.** A single file or env var that every loop in the fleet checks at the top of every iteration. Flip it, and every loop exits cleanly at its next check. This is the brake, not the off switch. The off switch is `kill -9` and a corrupted state file. The brake lets the loop stop where it's safe to stop.

**Action log review.** Every loop writes a structured log, one line per action. A human reads the log on a cadence. This is the one people skip, and the diagnostic is brutal: if you can't bring yourself to read the log, you don't trust the loop, and you shouldn't be running it unattended. Trust is a thing you earn by reading, the same ratchet we drew on the [[autonomy-dial]].

**Retirement.** A loop that hasn't produced anything useful in N days gets paused. Loops are cheap to start and expensive to leave running. Every idle loop is still polling, still holding a slot in your attention, still a thing that can wake up at 3am and spend money. Retirement is the cleanup nobody schedules until the fleet is a junkyard.

That's the set. Now the part that actually trips people up.

---

## Why budgets live in the runtime, not the prompt

Here's the mistake. You write "you have a budget of five dollars, stop when you hit it" into the system prompt, and you feel safe.

You are not safe. The model cannot count its own spend. It has no live access to the bill. Ask it how much it's spent and it will give you a confident, fluent, wrong number, the same way the self-grader in [[borrowed-verifiers]] gave you a confident, fluent "looks good." Budget tracking is a self-grading problem in disguise: you're asking the thing doing the spending to also be the thing reporting the spending.

The model will lie about its remaining budget. Not maliciously. It simply doesn't have the information, so it fills the gap with something plausible, and "I've got plenty left" is always plausible.

The runtime will not lie, because the runtime counts tokens it actually emitted. So the budget has to be enforced one level down from the model, in the loop that wraps the model. This is the same lesson as goal mode moving the exit condition out of the transcript and into a Stop hook. Anything the model can talk its way past is not a control. It's a suggestion.

[IMAGE: dark canvas. Top path: a prompt bubble saying "budget: $5, stop when you hit it" feeding a model that emits a thought bubble "I've got plenty left" while a meter behind it reads $41, crossed out with a red X. Bottom path: the same model wrapped in a runtime box that holds a real token counter wired to a hard STOP gate, marked with a green check. Caption: "the model can't count its own spend".]
![[images/governance-primitives/budget-in-runtime.png]]

---

## How to actually wire it

Intent is not a control. Pick the mechanics now and commit, because "I'll add budgets later" is how the thousand-dollar night happens.

**Budgets.** The Claude Agent SDK exposes `max_budget_usd` and `max_turns` per session. Use them, but know what they are: client-side estimates that can drift from the actual bill. Belt and braces, not the source of truth. The source of truth is two things. One, `ccusage` tailing the JSONL transcript files Claude Code already writes to disk; run `ccusage daily --json` and you get real token counts and estimated cost per day, per session, without uploading anything. Source: https://ccusage.com/. Two, the Anthropic Usage and Cost Admin API for the authoritative per-workspace number, hit with an `sk-ant-admin...` key against `/v1/organizations/usage_report/messages`. Source: https://platform.claude.com/docs/en/manage-claude/usage-cost-api. The Admin API is built for finance and reporting, not live throttling, so for a real-time cut-off you count tokens client-side from the Messages API response and keep a running total. The clean move: per-loop workspaces, so each loop's spend lands in its own bucket, plus a `ccusage` aggregator running as its own little L2 that checks totals and trips the kill switch when a fleet runs hot.

**Kill switches.** A single file, `.fleet/KILL`, or an env var, that every loop reads at the top of each iteration. Present means stop. The cleanest enforcement point in Claude Code is the Stop hook, the same hook we used as the worker trigger in [[l4-workers]] and as the exit gate in goal mode. The hook reads the file and aborts the turn. Do not ask the model to check its own kill switch and exit politely. It will forget, or rationalise one more turn. Put the check in code that runs whether the model cooperates or not.

**Action logs.** Structured JSONL, one line per action, each line carrying a timestamp, the tool call, and a reference to the artifact it produced. Not prose. Prose logs are unreadable at fleet scale and unparseable by the retirement check. This is the action log the autonomy dial's ship-and-log notch was writing into. Now it has a reader.

**Retirement.** A loop that hasn't written a log line marked `useful=true` in N days gets paused. And notice the trap: "useful" is itself a verifier. Retirement runs entirely on that one signal, so if `useful` is self-graded by the loop that wants to keep living, you've built a loop that votes for its own survival. Pick the signal carefully. Tie it to something external where you can, a merged PR, a shipped card, a real-world metric moving, the borrowed verifiers from earlier in the class, not the loop's own opinion of its work.

---

## Is L6 itself a loop?

Yes. And saying so honors the Russian-doll framing from [[loop-stack]] without falling into infinite regress.

L6 wires up as a plain L2, the builder-verifier shape from [[closing-the-loop]]. The builder is the four primitives running their checks: the budget tally, the kill-switch poll, the log writer, the retirement audit. The work artifact is a fleet health report, spend by loop, kills triggered, stale loops, retirement candidates. The verifier is a human, you, on a Sunday cadence, reading that report. The exit condition is a portfolio decision: keep, retire, reallocate, or escalate.

L6 doesn't recurse forever because its verifier runs on a human cadence, not on every turn. That's the structural line between L6 and L7. L6 is the runtime watching the loops, fast and mechanical. L7 is you deciding which loops should exist at all, and L7 isn't just slow L6. It integrates information that doesn't live in the runtime: revenue, strategy, what you're trying to become. The budget tally can tell you a loop spent forty dollars. It cannot tell you whether that loop should exist. We come back to that in [[mission-command]].

---

## The diagnostic

One question tells you whether you have governance.

Can your loops run forever without you noticing?

If yes, you don't have governance. You have loops and hope. Governance is precisely the property that something stops, or pages you, or shows up in a report you actually read, before the spend or the damage compounds past the point you'd have chosen.

It is not a monitoring tool. It is not an observability dashboard. You can bolt the fanciest dashboard in the world onto a fleet and still have no governance, because a dashboard nobody reads is the action-log failure mode with better graphics. Governance is the four primitives doing their job whether or not you're paying attention, plus you, on a cadence, closing the loop on them.

---

## Demo

Four artifacts on screen, two minutes, deliberately unglamorous.

1. **The budget config.** Open a loop's launch script. Show `max_budget_usd: 5.00` and `max_turns: 40` passed to the Agent SDK. Then flip to a terminal and run `ccusage daily --json`, pipe it through `jq` to pull today's cost, and point out: this number, not the one in the prompt, is the truth. Show a one-line guard that compares it against the cap.

2. **The kill switch.** Show `.fleet/KILL` not existing. Show the three lines at the top of the loop, and the same check inside the Stop hook. Then `touch .fleet/KILL` live, and watch the running loop exit cleanly at its next iteration instead of mid-write. Delete the file, it runs again.

3. **The action log.** Tail one loop's JSONL. One line per action, timestamp, tool, artifact ref, and the `useful` flag. Scroll a few lines. This is the thing a human actually reads on Sunday.

4. **The retirement rule.** Show the one-liner that scans every loop's log for the last `useful=true` line and pauses anything past seven days. Run it against a fleet where one loop has gone cold. Watch it flag exactly that one.

Then pull up the fleet health report that stitches all four together: spend per loop, kills this week, stale loops, retirement candidates. That report is the L6 work artifact. You reading it is the L6 verifier.

The point of the demo is that none of this is clever. Four small mechanical things. That's the whole layer.

---

## Key Insight

> If your loops can run forever without you noticing, you don't have governance, you have loops and hope. The brake lives in the runtime, never in the prompt, because the model can't count its own spend.

---

## Where we go next

You now have the brake. Four primitives, scoped to a fleet, enforced in the runtime, closed by you on a cadence.

But a brake you have to walk over to a terminal to read is a brake you'll stop using by week two. The fleet health report needs to come to you, in the place you already live. Next segment, we wire the whole thing into Slack and make it your command center.

See you in the next one.
