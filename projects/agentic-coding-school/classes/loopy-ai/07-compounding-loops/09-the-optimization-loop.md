---
duration: "12-16 min"
batch: 6
order: 21
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Optimization Loop"
status: "scripted"
aliases: [the-optimization-loop, optimization-loop]
---

Last segment the outer loop learned from a human. This one learns from a machine.

Same architecture, one part swapped. The self-improvement loop you just built reads human corrections because the work had no cheap grader. But some work does have a grader. Code that builds or does not. A page that renders or breaks. A test that passes or fails. When the grader exists, you do not need a person in the seat at all, and the whole loop changes character. It stops waiting for feedback to trickle in and starts manufacturing its own.

That is the optimization loop. It is the [[self-improvement-loop]] with the human seat filled by an automated check, and that single substitution is what lets it run on a corpus, converge, and stop.

[IMAGE: dark canvas, the self-improvement loop with one seat swapped. The old seat, a human grader, slides out; an automated check slides in (test passes or fails, page renders or breaks, build compiles or does not). Beside the change, the loop's character flips from "waits for real feedback to trickle in" to "manufactures its own feedback on demand". Caption: "one seat swapped, human to machine, and the loop stops waiting".]

---

## The grader is not the improver

Before anything else, untangle two jobs that look like one.

When you read about loops like this, you will see them described as a single "observer" skill that watches the work and makes it better. That bundling hides the most important distinction in the whole architecture. There are two roles in here, not one, and they fail in completely different ways.

A **grader** judges an output. It takes one run of the inner skill, measures it against criteria, and returns a verdict. Did the page render. How many pixels drifted. How many tokens did it burn. That is all it does. It never touches the skill file. It is read-only on the instructions and it answers exactly one question: how good was this?

An **improver** rewrites the instructions. It takes a stack of those verdicts, reads the current skill file, finds the pattern in the failures, and edits the skill. It answers a different question: what change makes the next runs better?

The cleanest way to hold this is the one borrowed from training models. **The grader is the loss function. The improver is the optimizer.**

The grader defines what good means and scores against it. It has no idea how to fix anything. The improver does gradient descent on the instructions. It has no idea what good is on its own, it just chases the signal the grader hands it. One measures. One moves. Measuring and moving are not the same skill, and pretending they are is how the loop quietly breaks.

Because once you see them as two roles, you see two independent failure modes.

Good optimizer, bad loss, and you efficiently optimize the wrong thing. The grader rewards a gamed metric, or it went stale and no longer reflects reality, and the improver dutifully marches the skill toward a worse place at full speed.

Good loss, bad optimizer, and you get the right signal turned into monkey patches. The grader is honest, the improver overfits each verdict into a brittle one-off, and you are back in the failure mode from [[teach-the-agent-to-learn]].

You cannot diagnose either one if the two roles are mashed into a single box in your head.

[IMAGE: dark canvas, two distinct boxes side by side with a one-way arrow from left to right. Left box labeled "GRADER = loss function", read-only eyeglasses icon, reading a single output and emitting a score card, caption under it "measures, never edits". Right box labeled "IMPROVER = optimizer", a pen-and-diff icon, taking a stack of score cards plus the skill file and emitting a diff, caption under it "edits, never measures". A thin dotted line under both reading "two roles, two failure modes". Caption: "the grader scores, the improver moves".]
![[loopy-optimization-loop-grader-vs-improver-1.png]]
![[loopy-optimization-loop-grader-vs-improver-2.png]]
![[loopy-optimization-loop-grader-vs-improver-3.png]]
![[loopy-optimization-loop-grader-vs-improver-4.png]]
![[loopy-optimization-loop-grader-vs-improver-5.png]]

---

## The optimization loop

Now wire the two roles together and you have the loop.

Warp built one to tune a skill that replatforms websites, moving a site off a no-code builder onto hosted code.
Source: https://www.warp.dev/blog/building-a-skill-optimization-loop

The skill is the inner loop. Point it at a site, it ports the site. On its own that is just a worker. The optimization loop is the thing wrapped around it, and it runs a fixed cycle.

It takes a set of N sites as input. It calls the inner skill on each one. It builds the results, then it actually looks at them, using computer use and browser use to compare the port against the original for visual and behavioral differences. It records where each run fell short. Then a strong model reads the whole pile of failures, finds the patterns, and writes a diff to the inner skill. Then it does it again.

Run the inner skill. Grade the outputs. Diff the skill. Repeat.
Source: https://www.warp.dev/blog/building-a-skill-optimization-loop

Notice the part that has no equivalent in the human-feedback loop. **This loop generates its own data.** The self-improvement loop had to sit and wait for real issues to get filed and real corrections to land. This one does not wait for anything. It owns a corpus of test inputs and it runs the inner skill against them on demand, as many times as it wants. The feedback is not incoming, it is summoned.

That is only possible because the grader is a machine. A human grader cannot review a thousand synthetic runs this week and a thousand more tomorrow. An automated one can, which is why the moment you have a real grader, the bottleneck on learning disappears.

[IMAGE: dark canvas, a tight cycle of four nodes drawn as a loop. Node one "corpus of N sites" feeding into node two "run inner skill on each". Node two flows to node three "grade outputs" drawn with a small browser window and a magnifying glass spotting a red defect. Node three flows to node four "diff the skill" drawn as a file with a green plus/minus. An arrow loops node four back to node two through the skill file. Off to the side, a small box labeled "self-generated data, no waiting" with an arrow pointing at the corpus. Caption: "run, grade, diff, repeat, on a corpus you own".]
![[loopy-optimization-loop-the-cycle-1.png]]
![[loopy-optimization-loop-the-cycle-2.png]]
![[loopy-optimization-loop-the-cycle-3.png]]
![[loopy-optimization-loop-the-cycle-4.png]]
![[loopy-optimization-loop-the-cycle-5.png]]

---

## This is the left column you were promised

Go back to the boundary picture from [[self-improvement-loop]]. Two columns. On the right, judgment work with no grader, where human deviation is the signal and the outer loop runs slow because real feedback is slow. On the left, work that has a grader, with a dotted arrow labeled "swap in an auto-grader later" pointing at an empty seat.

This is that seat, filled.

The architecture did not change. The improver is the exact same learning skill, doing the exact same job: read the verdicts, find the pattern, edit the instructions. The only thing that changed is who sits in the grader's chair. Pull out the human, drop in a computer-use check that scores the work without a person, and the same machine now runs unattended.

That swap buys you two things, and they are the two things the human seat could never give.

It buys volume. A person grades a handful of outputs before they get tired and start rubber-stamping. The machine grades the whole corpus, every cycle, without drift in attention.

And it buys initiative. The human loop is reactive by nature, it can only learn from work that actually happened in production. The optimization loop is proactive, it goes and creates the work it wants to learn from. You are no longer mining the past. You are running experiments.

So these are not two competing designs. They are the same loop at two points on one dial. The dial is "how cheap and honest is your grader." When grading needs human taste, you are on the right, learning slowly from real deviations. When grading can be automated, you slide left, and the loop speeds up, runs on synthetic inputs, and stops needing you in the room.

[IMAGE: dark canvas, a horizontal dial or slider running left to right. Far left end labeled "automated grader" showing a fast tight loop spinning on a stack of synthetic test inputs, no human. Far right end labeled "human grader" showing a slow wide loop fed by sparse real-world deviations, a small person icon in the seat. The slider knob sits in the middle. Under the axis a single label reads "how cheap and honest is your grader". A ghosted note on the left reads "the seat the last segment left empty, now filled". Caption: "same loop, one dial, the grader decides the speed".]
![[loopy-optimization-loop-left-column-1.png]]
![[loopy-optimization-loop-left-column-2.png]]
![[loopy-optimization-loop-left-column-3.png]]
![[loopy-optimization-loop-left-column-4.png]]
![[loopy-optimization-loop-left-column-5.png]]

---

## It converges, then it stops

Here is the property that makes this loop genuinely different from everything else in this chapter.

Every other loop you have built runs forever. The worker runs per event, the goal loop keeps itself alive against an objective, the self-improvement loop runs on a schedule until the end of time because the environment never stops drifting. None of them have a finish line.

This one does.

The optimization loop is chasing a fixed grader on a fixed corpus. So it makes progress and then it runs out of progress to make. The first cycle finds the obvious defects and the diff is large. The next finds subtler ones. A few cycles in, the diffs the improver proposes get smaller and less meaningful, because the skill is already handling the common cases. That tapering is the signal. When the changes stop mattering, you stop.
Source: https://www.warp.dev/blog/building-a-skill-optimization-loop

Which means this loop needs something none of the others did: **an exit condition.** Bake it into the loop directly. Stop when the diffs fall below a meaningfulness bar. Stop when scores plateau across cycles. And put a hard token budget on top of all of it, because a loop that improves itself will happily spend your entire account chasing the last half percent. Optimizing forever is not optimizing, it is burning money on diminishing returns.

Be honest about the ceiling too. Tuning a skill is local search. It climbs the hill it is standing on, and it can absolutely get stuck on a local maximum, polishing a fundamentally limited approach instead of finding a better one. There is only so much a prompt diff can buy you. The optimization loop makes a skill the best version of itself. It does not reinvent the skill. Knowing the difference is what keeps you from running it long past the point where the real fix is a rewrite, not another diff.

[IMAGE: dark canvas, a curve climbing left to right and flattening into a plateau. Early on the curve are large vertical jumps labeled "big diffs", later the jumps shrink to tiny steps labeled "diminishing diffs", and a dashed horizontal "stop here" line sits where the steps go flat. Above the plateau a small flag marks "local maximum", with a faint higher peak drawn separately and unreachable, labeled "needs a rewrite, not a diff". A small meter in the corner labeled "token budget" draining toward empty. Caption: "it converges, so give it a finish line".]
![[loopy-optimization-loop-converge-1.png]]
![[loopy-optimization-loop-converge-2.png]]
![[loopy-optimization-loop-converge-3.png]]
![[loopy-optimization-loop-converge-4.png]]
![[loopy-optimization-loop-converge-5.png]]
![[loopy-optimization-loop-converge-6.png]]

---

## Grade the cost, not just the output

One more thing the machine grader can do that a human one practically cannot. It can grade more than correctness.

The replatforming loop does not only check whether the port looks right. It also tracks how many tokens the run took, and it tries to drive that down while holding quality steady.
Source: https://www.warp.dev/blog/building-a-skill-optimization-loop

That is a second axis, and it matters more than it sounds. A skill that gets the right answer by burning a fortune in tokens on every run is a skill you cannot afford to run at scale. Correctness is the floor. Cost is the thing that decides whether the loop is actually deployable.

So the grader returns more than pass or fail. It returns a verdict on a plane: how good, and how expensive. And the improver optimizes the tradeoff, looking for instructions that keep the output just as correct while spending fewer tokens to get there. Trim a redundant step, tighten a verbose instruction, stop the inner skill from re-reading a file it already has.

This is why the grader being a real measurement, not a vibe, pays off. A number you can push on. Quality held flat, cost sliding down, cycle after cycle, is a thing only an automated grader can see and only an automated loop has the patience to chase.

[IMAGE: dark canvas, a two-axis plot. Vertical axis "quality", horizontal axis "cost in tokens". A dashed horizontal line near the top labeled "quality held flat". A series of dots marching left along that line, from a dot on the far right labeled "cycle 1, correct but expensive" to a dot on the far left labeled "cycle N, just as correct, far cheaper". An arrow under the dots pointing left labeled "optimize the tradeoff". Caption: "correctness is the floor, cost decides if it ships".]
![[loopy-optimization-loop-cost-axis-1.png]]
![[loopy-optimization-loop-cost-axis-2.png]]
![[loopy-optimization-loop-cost-axis-3.png]]
![[loopy-optimization-loop-cost-axis-4.png]]
![[loopy-optimization-loop-cost-axis-5.png]]

---

## Demo

The replatforming loop, end to end, on a site you can watch break and then watch get fixed.

1. **Run the inner skill once.** Take a real no-code site, point the replatforming skill at it, and ship the port to a preview URL. Put the two side by side, original and port. Find the obvious defect: a set of dropdown toggles that lost their icons. The skill almost worked. That gap is the whole reason the loop exists.

2. **Show the grader, alone.** Open the observer and read just the grading half out loud. It builds the port, drives a browser over it, and diffs it against the original. It flags the missing icons and it logs the token cost of the run. Point at what it produced: a verdict and a number. No edit to the skill. This is the loss function and nothing more.

3. **Show the improver, alone.** Now the second half. Feed the verdict and the current skill file to the learning step. It reads the failure, finds the cause, and proposes a diff to the replatforming skill so the next port carries the icons across. A change to the instructions, written from the grade. This is the optimizer.

4. **Close the loop and let it run.** Wire them together and let it cycle on a small corpus of sites. Watch the first diff land big, the second smaller, the third barely worth merging. Show the exit condition firing when the diffs fall below the bar, and the token meter stopping the run instead of grinding forever.

5. **Point at what did not happen.** No human reviewed a single port. No one wrote a rule by hand. A machine graded the work, a machine rewrote the instructions, and the skill got measurably better and measurably cheaper across a handful of cycles, then stopped on its own.

The source skills are open, so you can read both halves yourself.
Source: https://github.com/warpdotdev-demos/replatformer

---

## Key Insight

> When the work has a grader, you do not need a human in the loop. Split the grader from the improver, let the grader manufacture data on a corpus, and the loop tunes the skill on its own until the diffs stop mattering.

---

## Where we go next

You now have both halves of the self-improvement picture. The right column, where a human's deviation is the only grader you have, and the left column, where an automated check takes the seat and the loop runs unattended on its own data until it converges.

What has stayed constant across both is the improver. It is always the same learning skill turning verdicts into edits, and it is always proposing a change to a file that drives real behavior. We do not let it merge that change on its own authority, whoever sat in the grader's chair. Next, [[skills-as-code]], we put the gate in place: every diff the loop writes arrives as a reviewed pull request, with history and rollback, so the skill can keep tuning itself without ever quietly going off the rails.

See you in the next one.
