---
duration: "10-14 min"
batch: 5
order: 16
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "Routines And Scheduled Tasks"
aliases: [routines-scheduled-tasks]
---

A worker needs a queue. But the queue needs something to fill it. The cleanest filler for a whole class of work is a clock.

Last segment we built the worker: trigger source, pick rule, process, report, retry. Five parts, four of them old, one of them new. We spent the whole time on the pick rule because that was the interesting bit. We waved a hand at the trigger source and said "something feeds the queue."

This segment is that something. The clock. Routines and scheduled tasks.

It's the dumbest trigger you can give a loop, and for a surprising amount of real work it's the right one.

---

## What everyone gets wrong about scheduling

People treat "schedule it" as the lazy option. The thing you do when you can't be bothered to wire up a real event.

That's backwards. A schedule is a real trigger, and it's the correct trigger whenever the work is *periodic against the world* rather than *reactive to an event*.

Some work has a clean event you can hook. A PR opens. A ticket gets labeled. A test goes red. That work belongs on a Stop hook or a webhook, the way we set up the worker. We met that taxonomy last segment with Daniel San's "what makes the agent take another turn" framing.

But a huge amount of valuable work has no event at all. Nobody fires a signal when your dependencies drift out of date. Nothing pings you when a competitor ships a feature overnight. There is no webhook for "the backlog has gone stale" or "yesterday's metrics are worth a look." The trigger for that work is just: it's morning again.

[IMAGE: dark canvas, two columns. Left column "reactive" with an event icon (PR opens, test goes red) firing a loop. Right column "periodic" with a clock face firing the same loop shape. Caption: same loop, different trigger.]
![[images/routines-scheduled-tasks/reactive-vs-periodic.png]]

The mistake is thinking the clock is a downgrade from the event. It isn't. It's a different sensor. Some loops perceive an event. Some loops perceive the passage of time. Both are legitimate triggers, and the trigger primitive we named back in strip-the-model-out doesn't care which one you use.

So this is not "the easy version of a worker." This is the worker, with a clock in the trigger slot.

---

## The core insight: the clock is the trigger, the prompt is the work

Go back to the five primitives. Trigger, work, check, terminate, state. A scheduled task swaps exactly one slot. The trigger stops being an event and becomes a cron expression. Everything else is the same L3 you already know how to write.

That's the whole idea. A routine is not a new kind of loop. It's an L4 worker whose trigger source is a schedule instead of a queue event. The agent still runs a full task lifecycle each time it fires. It still needs a borrowed verifier, a kill switch, a budget, and a log. Nothing about the climb resets just because a clock pulled the trigger.

Source: https://code.claude.com/docs/en/routines

Which means the danger is also the same. A loop that fires on a clock and grades itself is still vibes on a timer. A loop that fires on a clock with no kill switch is the runaway we keep warning about, except now it's runaway on a schedule, which is worse, because you're not watching when it fires at 3am.

The clock makes a loop unattended. Unattended is exactly when your governance has to already be in place. We'll build the real governance layer later in the class. For now, hold the rule: the moment a loop runs without you in the room, every guardrail from the worker segment becomes mandatory, not optional.

---

## Two homes for a schedule: in-session and durable

There are two places a schedule can live, and they solve two different problems. Conflating them is the most common setup mistake.

**In-session scheduling.** Inside an open Claude Code session, `/loop` and the cron tools (`CronCreate`, `CronList`, `CronDelete`) let you re-run a prompt on an interval without leaving the conversation. Poll a deployment every two minutes. Babysit a PR. Check back on a long build. Remind yourself later in the session.

Source: https://code.claude.com/docs/en/scheduled-tasks

The catch is the lifetime. These tasks are session-scoped. They live in the current conversation and die when you start a new one. Recurring tasks auto-expire seven days after creation, fire one last time, and delete themselves. That expiry is a feature, not a bug. It bounds how long a forgotten loop can run. The scheduler checks for due tasks and fires the prompt *between your turns*, never mid-response, so a scheduled fire waits politely for the current turn to finish.

In-session scheduling is for "while I'm working, keep an eye on this." It is not for unattended automation. The moment you close the laptop, it's gone.

**Durable scheduling.** When the work has to survive past the session, past the seven days, past your laptop being shut, you reach for a routine.

A routine is a saved Claude Code configuration: a prompt, one or more repositories, a set of connectors, packaged once and run automatically on Anthropic-managed cloud infrastructure. It keeps working when your laptop is closed. You create one from the web at claude.ai/code/routines, from the Desktop app, or conversationally in the CLI with `/schedule daily PR review at 9am`.

Source: https://code.claude.com/docs/en/routines

[IMAGE: dark canvas, a spectrum from left to right. Far left "in-session /loop" (lives in the conversation, dies in 7 days), middle "Desktop scheduled task" (local machine, only while awake), far right "cloud routine" (Anthropic infra, runs with laptop closed). One axis: durability.]
![[images/routines-scheduled-tasks/scheduling-spectrum.png]]

A routine takes one or more triggers. The schedule trigger is the one we care about here: hourly, daily, weekdays, or weekly presets, with a one-hour minimum interval. Anything more frequent gets rejected, which is the platform quietly enforcing the same rule we've been preaching. If you think you need a loop firing every thirty seconds, you've misdesigned the loop. Times are entered in your local zone and converted automatically, so a "9am" routine fires at 9am wall-clock no matter where the cloud box lives. For a custom interval, you pick the closest preset and then `/schedule update` to drop in a raw cron expression.

Routines also take API and GitHub triggers, and a single routine can mix all three. But those are events, and events were last segment's job. Our lane here is the clock.

---

## What actually belongs on a clock

Here's the filter. A task earns a schedule when it is unattended, repeatable, and tied to a clear outcome. If you can't verify the run's output in under two minutes the next morning, the task is too vague or too large to schedule.

Source: https://amux.io/guides/ai-coding-agents-overnight/

That second half is the real test, and it's the borrowed-verifier discipline wearing a clock. A scheduled loop runs while you're asleep. You don't get to babysit it. So the run has to leave behind something concrete and checkable: a log line, a file, a digest, a drafted PR, a Slack message. A scheduled job whose only output is "it ran" is a job you can't actually trust.

The canonical scheduled jobs all share that shape.

**Backlog grooming.** Every weeknight, a routine reads issues opened since the last run, labels them, assigns owners based on the area of code referenced, and posts a summary to Slack so the team starts the day with a groomed queue. Notice what this is: it's a discovery-flavored worker fed by the clock. The output, a triaged backlog, becomes the input queue for tomorrow's coding workers. The clock loop fills the event loop's queue. That's the handoff the worker segment promised.

**Dependency and health audits.** Weekday mornings, a routine runs `npm audit` or `pip-audit`, checks the TypeScript error count against yesterday, the coverage delta, the bundle-size delta, and reports anything that got worse to a tech-debt channel and anything that got better to a wins channel. This is the uptime checker from strip-the-model-out, grown up. Same deterministic check primitive, now firing on a daily cron with a model in the work slot to explain the deltas.

**Docs drift.** Weekly, a routine scans merged PRs since the last run, flags docs that reference changed APIs, and opens update PRs against the docs repo for an editor to review.

**Morning briefings.** A local Desktop scheduled task that starts a fresh session at 8am, pulls from your calendar and inbox, and writes you a digest.

Source: https://code.claude.com/docs/en/desktop-scheduled-tasks

Every one of these takes over an hour a week, has clearly defined repeatable steps, and produces a checkable artifact. That triad is the spec for "should this be a routine."

What does *not* belong on a clock: anything with a clean event already (hook the event), anything you can't verify cheaply in the morning (sharpen it first), and anything truly deterministic like a data pull or a file move. If there's no judgment involved, a plain cron on a cheap box is still simpler and cheaper than a model. Routines earn their keep when the task needs judgment: reading a stack trace, deciding which PR filter applies, grooming issues by code area.

Source: https://allthings.how/claude-code-routines-how-anthropics-scheduled-ai-agents-work/

---

## The four traps of unattended scheduling

Scheduling adds its own failure modes on top of the worker's four. These bite specifically because nobody is watching when they fire.

**Overlap.** A daily job that sometimes takes longer than a day will start a second copy on top of the first. Two runs touching the same files, the same branch, the same queue item. The fix is a lock or a run-state file: before launching, check whether the last run is still going. One schedule should never pile up copies of itself.

Source: https://dev.to/toji_openclaw_fd3ff67586a/the-complete-guide-to-ai-agent-cron-jobs-and-scheduling-2c3f

**No timeout.** An unbounded scheduled agent becomes a zombie: it hangs, the next fire stacks on top, and your spend runs away in the dark. Every scheduled run needs a hard cap. If you can't explain why a job should run longer than fifteen to thirty minutes, it probably needs to be split into smaller jobs.

**Non-idempotent runs.** Scheduled systems must assume retries and duplicates happen. Posting from an approved queue should mark the item as used. Memory consolidation should key off the date. A sales check should track the last processed event ID. Otherwise the second fire re-does the first fire's work and you get duplicate PRs, duplicate posts, duplicate spend.

**Green is not done.** This one is specific to cloud routines and it's the trap I most want you to remember. A green run status means the session started and exited without an *infrastructure* error. It does not mean the task in your prompt succeeded. Blocked network requests, missing connector tools, and task-level failures all hide behind a green checkmark. You have to open the run and read the transcript to know what actually happened.

Source: https://code.claude.com/docs/en/routines

That last one is the self-grading failure relocated to the dashboard. The status light is the loop grading its own infrastructure, not its own work. A green light with no borrowed verifier behind it is exactly the lie we've been hunting since the closing-the-loop segment, except now it's a single reassuring dot you'll glance at and trust. Don't. The verifier still has to live inside the prompt, and the proof of work still has to land in the transcript.

[IMAGE: dark canvas, a green checkmark labeled "infrastructure ran" sitting on top, and underneath it a separate red/green gate labeled "did the work actually pass?" with an arrow showing they are two different questions. Caption: green status is not a verifier.]
![[images/routines-scheduled-tasks/green-is-not-done.png]]

---

## Demo

I'll build one durable scheduled loop end to end: a nightly dependency and health audit.

1. In a session, I run `/schedule weeknights at 7pm, audit dependencies and report regressions`. Claude walks me through the same fields the web form collects: the prompt, the repo, the connectors. On screen I show it resolving "weeknights at 7pm" to a weekday preset and confirming the cadence.

2. I open the routine on the web to harden it. I scope the environment's network access down to just the package registries it needs. I trim the connectors to one: Slack. Everything Claude doesn't need to reach, it can't reach.

3. I show the prompt itself, and I point at the three lines that make it a real loop and not vibes. The VERIFY line: run `npm audit --json` and `tsc --noEmit`, count the errors, diff against the numbers in last night's report file. The OUTPUT line: write `audit/YYYY-MM-DD.md` and post the deltas to `#tech-debt`. The cap: stop after fifteen minutes. Borrowed verifier, checkable artifact, timeout. The three things that survive the loop going unattended.

4. I click Run now instead of waiting for 7pm. The run fires, opens as a full session, and I watch it clone the repo, run the audit, write the dated file, and post to Slack.

5. Then the punchline. The run list shows a green check. I open the run anyway and scroll the transcript, and I point out a blocked network request that the green status said nothing about. Green meant "it ran." The transcript meant "here's what it actually did." I fix the allowed-domains list and re-run.

Total demo: about six minutes. The point lands on its own. The clock pulled the trigger, the agent ran a full L3, and the only reason I can trust the result is that I wired in a verifier and read the transcript instead of the status light.

---

## Key Insight

> A schedule is not the lazy trigger. It's the right trigger when the work is periodic against the world instead of reactive to an event. But the clock makes the loop unattended, and unattended is exactly when every guardrail stops being optional. A green run status is not a verifier.

---

## Where we go next

You now have the full L4 picture. Workers triggered by events, workers triggered by the clock, both running a real task lifecycle with real guardrails.

Next we point a scheduled loop at the most valuable periodic job there is: research that compounds. Every overnight run becomes a row in a table the agent reads before the next try. That's autoresearch, and it's where the clock stops being a way to maintain things and becomes a way to learn things.

See you in the next one.
