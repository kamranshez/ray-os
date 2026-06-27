---
duration: "8-12 min"
batch: 9
order: 34
batch_name: "Loops In The Wild"
class: "loopy-ai"
chapter: "The Five-Minute Maintainer"
status: "scripted"
aliases: [five-minute-maintainer]
---

The last loop waited for a plan. This one writes its own.

Every five minutes, while you work on something else, an agent makes one small, verified improvement to your repository. What to improve is the agent's call, not yours and not a hardcoded script. That decision is the entire video.

This is a reconciliation loop from chapter five, the thermostat, pinned to one standing ideal: this repo always trends cleaner, never messier.

[IMAGE: dark canvas, a thermostat dial mounted on a repo folder, its setpoint labeled "always cleaner, never messier". A 5-minute clock wired to it. Every tick the dial fires a small "one verified improvement" spark into the repo. A sleeping human in the corner labeled "you, working on something else". Caption: "the agent picks the work, not you".]

---

## The problem it kills

Repositories rot in a thousand tiny ways that no ticket will ever capture.

A flaky test nobody re-runs. A comment that describes code that changed two refactors ago. A function that should have a type and does not. None of these are worth a Linear ticket. All of them are worth fixing. So they never get fixed, because the unit of work is too small to ever rise to the top of a backlog, and the pile grows forever.

You do not have a task here. You have a direction. And a direction is exactly what a reconciliation loop holds.

[IMAGE: dark canvas, a repo drawn as a house quietly rotting in tiny ways, each labeled: "flaky test nobody re-runs", "stale comment from two refactors ago", "missing type". Each tiny rot has a Linear ticket floating beside it stamped "too small to file", so they pile into a growing heap labeled "never gets fixed". Off to the side, a compass labeled "direction, not a task" pointing toward "cleaner". Caption: "rot too small to ever rise to the top of a backlog".]

---

## The loop

This is Peter Steinberger's, and the numbers are the reason to take it seriously. He merged 859 pull requests across his repositories in a single month, at a 95 percent acceptance rate. A real chunk of that volume is this one loop, left running on a five minute timer while he does other work.

```
/loop 5m make one small verified repository improvement: a flaky test, a stale comment, a missing type. One change, one commit, tests green. Never touch anything risky.
```

There is no queue here. There is no ticket. The loop wakes every five minutes, reads the current state of the repo, finds the single biggest small gap, and closes it. Then it sleeps and does it again. Forever, or until you close the session.

[IMAGE: dark canvas, a horizontal "ideal state" line at top labeled "always trending cleaner", a wobbling "current state" line below it drifting down from entropy, small correction arrows firing every five minutes yanking it back up, a clock icon ticking 5m]

![[loopy-litw-five-minute-maintainer.png]]

---

## Why it works: a setpoint, not a destination

This is the reconciliation shape, so name it. A worker reaches a destination and stops. This loop has no destination. It has a setpoint it never stops holding, the way a thermostat does not finish heating a room and retire.

That is why the timer matters. The loop is not racing to a finish line, it is holding a line against drift. Five minutes is just how often it checks the temperature. Entropy never finishes pulling your repo toward mess, so the loop never finishes pulling it back.

And notice what you did to start it. You did not assign a task. You declared a direction and pointed a loop at the gap. That is the whole move that takes you from running loops to living in them.

[IMAGE: dark canvas, split contrast. On the left, a worker reaching a "finish line" flag and stopping, labeled "destination". On the right, a thermostat holding a flat "setpoint" line forever against a downward "entropy" arrow that never stops pulling, labeled "no finish line, just hold". A 5m clock between them captioned "the timer is just how often it checks the temperature". Caption: "a setpoint, not a destination".]

---

## The constraints are the safety

Read the back half of that command again, because it is not decoration. It is the entire reconciliation discipline compressed into one sentence.

"One change, one commit, tests green" is the borrowed verifier and the deadband in one breath. The tests are the grader, so the loop cannot lie to itself about whether it helped. And one change per tick is the deadband, the thing that stops a standing loop from thrashing your whole repo every time it wakes up. A real thermostat does not fire the furnace over a half-degree wobble. Neither does this.

"Never touch anything risky" is the autonomy notch. It pins the loop to low-blast-radius maintains and keeps it away from anything you would want to approve yourself. A loop running unattended every five minutes is exactly the kind of thing you keep on a short leash, and that clause is the leash.

Source: https://x.com/mvanhorn (Matt Van Horn, "WTF Is a Loop? Part 2", Jun 2026)

[IMAGE: dark canvas, the command broken into three labeled safety parts. "One change, one commit, tests green" splits into a grader badge labeled "borrowed verifier" and a thermostat deadband zone labeled "no firing on a half-degree wobble". "Never touch anything risky" drawn as a short leash clipped to the loop, with a risky "major version bump" item held back behind a fence labeled "you approve this". Caption: "the constraints are the safety".]

---

## Demo

Put one maintainer on screen and let it tick.

1. Show there is no queue. No plan file, no ticket, no list. Just the repo and the command. Say it plainly: the input is a direction, not a task.

2. Run one tick. The loop wakes, scans, and decides on its own that a stale docstring is the biggest small gap right now. It fixes that one thing, runs the tests, commits. One change, one commit, green.

3. Run the next tick. Five minutes later it wakes again and picks something completely different, a missing return type. Point at the screen: nobody told it what to do either time. It chose.

4. Show the leash hold. Seed a tempting but risky change, a dependency major-version bump. Watch the loop notice it, decide it counts as risky, and leave it alone. That is "never touch anything risky" doing its job.

5. Walk away and come back. Ten commits later, each one tiny and green, the repo is measurably cleaner and you did not read a single one while it happened.

Total demo: three minutes. The point is that you declared how the repo should always be, and a loop now holds it there without you watching.

---

## Key Insight

> A worker reaches a destination and stops. This loop holds a setpoint and never stops. You did not give it a task, you gave it a direction, and it generates its own work forever inside that direction.

---

## Where we go next

You have now seen a loop that picks its own work while you watch.

The next one does it while you sleep. Same idea, longer leash, and a different command for the job.
