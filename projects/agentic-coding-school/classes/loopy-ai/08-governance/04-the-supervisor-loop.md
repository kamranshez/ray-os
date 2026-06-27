---
duration: "7-10 min"
batch: 5
order: 21
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "The Supervisor Loop"
status: "scripted"
aliases: [supervisor-loop, loop-over-loops, watching-the-watchers]
---

In the last video you aimed a reconciliation loop at a codebase. This one aims the same loop at a stranger target: your other loops.

You have built loops that drain queues, loops that hunt for new work, and loops that hold reality to an ideal. Run enough of them and you have a new problem, and it is one none of those loops can see. The loops themselves.

A supervisor loop is a reconciliation loop whose room is your fleet. Its ideal state is not "main is green" or "churn under two percent." It is "every loop I am running is alive, inside budget, and actually closing its gap." Same thermostat. The thing it holds to a setpoint is the health of your other loops.

[IMAGE: dark canvas, a thermostat icon with two arrows leaving it. Arrow one points down at a codebase labeled "last video: aim it at your work". Arrow two points at a cluster of small running loop-machines labeled "this video: aim it at your loops". Caption: "the same reconciliation loop, pointed at a stranger target".]

---

## A fleet is invisible by design

The whole pitch of a loop is that it runs without you watching. That is the feature. Now multiply it by twenty. What you have built is a room full of machines you deliberately stopped looking at.

Background is the point. Background is also exactly why failure goes silent. A loop can die. It can hang. It can thrash. It can quietly drain its budget. Worst of all, it can keep running perfectly while making no progress at all. And the first you will hear of any of it is when the outcome that loop was guarding has already rotted.

The property that made loops worth building, their autonomy, is the same property that hides their failure. You cannot watch what you built specifically so you would not have to watch it. This is the oldest question there is, older than computing. Who watches the watchers.

[IMAGE: dark canvas, a dim room full of small humming loop-machines with the human walked out the door. In the back corner one machine has stalled and thrown a small red spark, completely unnoticed. Caption: "autonomy is why they are valuable, and why their failure is silent".]

---

## The core insight: green is not the same as winning

The naive supervisor checks one thing. Is each loop still alive. That check is table stakes, and liveness is not the interesting failure.

The dangerous loop is the one that is alive, never errors, runs green on every single tick, and is not closing its gap. Picture a churn reconciliation loop that fires every hour, never breaks, while churn climbs anyway, because its correction is simply too weak for the force pulling against it. Green light. Losing battle.

So the supervisor's real measurement is not the heartbeat. It is the gap trend. Over the last several runs, is the distance between current state and ideal shrinking, holding, or widening. A loop that is busy and green and on budget, but whose gap is widening, is the single most important thing this loop exists to catch, because nothing else in your whole system will catch it. Every other check that loop passes.

[IMAGE: dark canvas, two loops side by side, both lit with a green "no errors" light. Left loop: a gap line steadily shrinking toward its ideal, labeled "winning". Right loop: a gap line steadily widening away from its ideal despite the green light, labeled "losing". A magnifier held by the supervisor reads the gap TREND, not the light. Caption: "watch the gap, not the heartbeat".]

---

## The shape: the same thermostat, a different room

It is the five primitives again, filled the reconciliation way, just pointed sideways at your fleet instead of out at the world.

The trigger is a clock. The supervisor wakes on a schedule and sweeps.

The current state is read from each loop's telemetry. Is it running. When did it last succeed. How much of its budget has it burned. And, the important one, what has its gap been doing over the last handful of runs.

The ideal state is the fleet invariant. Every registered loop is alive, inside its budget, and trending toward its own setpoint.

The check is the borrowed verifier, and here it is almost free, because the verifier is the telemetry your loops already emit. Last success timestamps. Budget counters. The gap metric each reconciliation loop already reports. The supervisor reads numbers, not vibes. The moment its check becomes the model saying "the fleet seems fine," you have rebuilt the self grading failure one level up.

The state is the memory of what it already restarted or already flagged, so it does not spam you with the same dead loop every hour.

The terminate is per run. Sweep the fleet, act, sleep.

[IMAGE: dark canvas, the five-primitive loop drawn as a supervisor. Trigger: a clock. Current state input: a small dashboard of fleet telemetry (running? last success? budget burned? gap trend?). Ideal state: "all loops alive, in budget, gap shrinking". Check: the telemetry itself as the borrowed verifier, not the model's read. State: a memory of what it already restarted or flagged. Terminate: per-run sweep then sleep. Caption: "the same thermostat, the room is your loops".]

---

## What the supervisor actually does: four diagnoses

When the supervisor finds an unhealthy loop, its job is to name which kind of unhealthy, because each kind has a different correction.

Dead or stalled, meaning no successful run inside the window it should have run in. The correction is restart, and if it will not come back, alert. Low blast radius, usually a clean self-heal.

Thrashing, meaning it is firing far more often than it was designed to, oscillating, yanking at every tiny wobble. The correction is to widen its deadband or pause it. It is over-correcting, so the fix is less loop, not more.

Drifted, meaning it is running perfectly against an ideal that has gone stale. The correction is to flag it for re-scope. This is a taste call about whether the setpoint is still right, not a mechanical one, so it comes to you.

Busy but not winning, meaning green, on budget, and the gap is widening anyway. The correction is to escalate, because the loop needs a rethink. Maybe more authority, maybe a different approach, maybe the problem itself changed under it. Only a human decides that.

The supervisor names which of the four is happening, then acts or escalates by blast radius. That is the autonomy dial from earlier in this chapter, applied to loops instead of edits.

[IMAGE: dark canvas, one "unhealthy loop" box fanning out into four labeled paths. Dead then restart. Thrashing then widen the deadband or pause. Drifted then flag for re-scope. Busy but not winning then escalate. Each path tagged with an autonomy notch, the first two marked "auto", the last two marked "human". Caption: "name what is wrong, then act or escalate by blast radius".]

---

## Who watches the watcher

Here is the honest objection. The supervisor is itself a loop. So who supervises the supervisor.

If your answer is a supervisor of the supervisor, you have built turtles all the way down and solved nothing, because that loop can fail silently too. You terminate the recursion the dumbest way possible, and you do it on purpose.

The supervisor is the one loop you keep a thin human thread on. It emits a heartbeat. "Swept the fleet, all checked, one restarted, one flagged." And a dumb external dead-man's switch, a plain cron job with no intelligence in it at all, watches only for that heartbeat to arrive. If the supervisor ever goes silent, the cron pings you.

You do not make the root of trust smart. You make it loud. Exactly one loop in your whole system is allowed to fail straight to a human, and this is the one. That is the bottom turtle, and it is a human.

[IMAGE: dark canvas, a tall stack of "supervisor of a supervisor of a supervisor" boxes crossed out and labeled "turtles all the way down, solves nothing". Beside it the real design: a supervisor loop emitting a heartbeat into a small dumb cron icon, which pings a human the moment the heartbeat stops. Caption: "do not make the root of trust smart, make it loud".]

---

## Where you stay in the loop, and where you don't

The split is the same one you have seen at every level, with one structural twist.

You do not stay in the loop for the sweeping. If you are personally checking whether your loops ran, you have appointed yourself the supervisor, and you will be as lossy and forgetful as you always were.

You absolutely stay in the loop for two things. Re-scoping a drifted loop, because deciding whether an ideal is still the one you want is a taste question, the same human-only call as declaring an ideal in the last video. And approving the dangerous kills, because killing or re-authorizing a high blast radius loop is not a decision you hand to a thermostat.

And the twist. You are the dead-man's switch for the supervisor itself. Out of everything in this fleet, that one heartbeat is the single wire you keep your hand on.

[IMAGE: dark canvas, the human placed at exactly two points and removed from a third, plus one wire. Removed: "watching whether my loops ran", crossed out with "do this yourself and you are just a lossy recorder". Present: "re-scope a drifted loop" tagged taste, and "approve the dangerous kills" tagged blast radius. A separate wire runs the supervisor's heartbeat straight to the human, labeled "the one thread you keep your hand on". Caption: "out of the sweeping, in for the taste, the kills, and the heartbeat".]

---

## Demo

Put one supervisor loop on screen, watching exactly three loops, kept deliberately small.

1. Show the fleet manifest. One file listing three registered loops, each with its ideal, its budget, its expected run interval, and the gap metric it reports. That manifest is the whole configuration. No tasks, no queue, just a roster of loops and what healthy means for each.

2. Show the trigger. A scheduled routine fires every hour. Same scheduled-task primitive from earlier in the class, pointed at your own fleet instead of at a stream of issues.

3. Show the read. The supervisor pulls telemetry on all three. Loop A: alive, on budget, gap shrinking, healthy. Loop B: no successful run in three days, dead. Loop C: green every hour, on budget, gap quietly widening for a week.

4. Show the corrections branch on blast radius. Loop B is a low-stakes maintain, so the supervisor restarts it automatically and notes it. Loop C is the dangerous one, so the supervisor does not touch it. It posts to Slack: "Loop C is green and on budget but its gap has widened seven days running, its correction is too weak, re-scope it?" Same loop shape, two different notches on the autonomy dial.

5. Show the state file. What it already restarted and already flagged this week, so loop B does not generate a fresh restart alert every single hour and loop C does not get re-flagged before you have answered.

6. Show the heartbeat. The supervisor pings you, "fleet swept, one restarted, one flagged." Then show the dumb external cron that watches for that ping, and what it sends you if the ping ever fails to arrive.

Total demo: three minutes. The point is that you never once checked on a loop yourself. You wrote down what healthy means for each one, and a loop now holds your whole fleet to it, including catching the one that looked perfectly fine and was quietly losing.

---

## Key Insight

> A worker can fail and you notice. A loop can fail and you do not, because you built it precisely so you would stop watching. The supervisor loop is the one thermostat whose room is your other loops, and its real job is not checking that they are alive. It is catching the one that is green, on budget, and quietly losing.

---

## Where we go next

Step back and look at what the governance chapter has actually given you. A discovery loop that finds your next loops. A reconciliation loop that holds reality to an ideal. And now a supervisor loop that keeps the whole fleet honest, including itself, all the way down to a single heartbeat you keep your hand on.

That is a system that can grow itself, hold itself to a standard, and watch itself, without quietly rotting the moment you look away. Which is the entire point of governance: not slowing the loops down, but making it safe to stop watching them.

See you in the next one.
