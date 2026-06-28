---
duration: "12-16 min"
batch: 8
order: 31
batch_name: "L7 Closing"
class: "loopy-ai"
chapter: "Where Loops Fail Right Now"
status: "scripted"
aliases: [where-loops-fail, where-loops-fail-right-now]
---

Every failure mode in this class has been taught next to the segment that cures it. This is the one segment where we put them all in a row.

Not because a list is tidy. Because a loop almost never dies of one cause. It dies of the weakest section you got lazy on, and you can't see which section that is until you can see all of them at once.

So this is the field guide. Nine ways a loop fails, the one-line tell for each, and the segment that goes deep. Watch it last, then keep it open the next time a loop of yours quietly stops working and you can't say why.

One more thing before the list, and it's the whole frame. Half of these failures are temporary. They exist because of what the models can't do yet, and that floor is rising every few months. The other half don't move at all, because they're about what you want, not what the model can do. Knowing which is which is the last thing this class teaches you.

[IMAGE: dark canvas, a loop drawn as a chain of labeled links (trigger, verifier, kill switch, dial, goal). One ordinary-looking link snapping under load while the rest hold, labeled "the weakest section you got lazy on". Off to the side a small field-guide booklet labeled "nine failure modes". Caption: "a loop dies of one weak link, not all of them".]
![[loopy-where-loops-fail-right-now-intro-v1-1.png]]
![[loopy-where-loops-fail-right-now-intro-v1-2.png]]
![[loopy-where-loops-fail-right-now-intro-v1-3.png]]
![[loopy-where-loops-fail-right-now-intro-v1-4.png]]
![[loopy-where-loops-fail-right-now-intro-v1-5.png]]

---

## Read the list as two columns, not one

[IMAGE: dark canvas, two columns of failure cards. Left column header "model-limited, eroding" with a downward fading arrow. Right column header "human-owned, durable" drawn solid and unchanging. A dotted line down the middle]

![[loopy-where-loops-fail-two-columns-1.png]]
![[loopy-where-loops-fail-two-columns-2.png]]
![[loopy-where-loops-fail-two-columns-3.png]]
![[loopy-where-loops-fail-two-columns-4.png]]
![[loopy-where-loops-fail-two-columns-5.png]]

Before the nine, hold the two columns in your head.

**Model-limited failures.** These come from things the model is currently bad at. Holding coherence across a fifty-turn run. Checking its own work honestly. Running unattended for hours without wandering. Every model release pushes these back. A failure that bit you hard in early 2026 may be a non-issue by the time you watch this, because the context windows got longer, the self-verification got sharper, and the reliable unattended window stretched from minutes to hours. When I say "right now" in this segment, this is the column I mean.

**Human-owned failures.** These don't erode, because no model release fixes them. A vague goal is vague no matter how smart the worker is. A missing kill switch is missing. An autonomy dial you never set is unset. The model getting better just means a more capable agent executes your unclear intent more confidently in the wrong direction. These failures are not a model problem. They're a you problem, and they're permanent.

Here's the trap most people will fall into over the next two years. They'll watch the model-limited column shrink, conclude loops "just work now," and stop doing the human-owned work entirely. Then they'll hand a more autonomous, longer-running, more trusted loop a goal that defers to the model and a dial that was never set, and the blast radius of that mistake will be larger than anything we saw in 2026. Better models make the human-owned failures more dangerous, not less.

Now the nine.

---

## The model-limited failures (the column that's eroding)

### One. The verifier is fake

The most common death in the whole class. The loop has a check, the check passes, and the check was never testing reality.

The tell: your loop reports success and the work is wrong. Every time that happens, the verifier is the suspect, not the worker.

This is the entire L2 chapter, so I'll only name the variants. Verifying against the plan instead of against the world, when the plan itself was the thing that was wrong. A verifier the worker can sweet-talk, the sycophantic-attacker problem. A bar set so low it passes slop, or so high the loop finds infinite criticism and never ships. A check that reads the worker's own summary instead of touching the running system. Go back to the real-verifiers-touch-reality and where-to-set-the-bar segments for the cures. The headline: a loop is only as honest as the thing grading it.

Why it's eroding: as models get better at running real commands, reading real output, and judging honestly, the cheap verifier gets more trustworthy on its own. But slowly. Today you still build the verification environment by hand.

### Two. The verifier goes stale

A check that was meaningful in January is theatre by April. It still passes. It just stopped meaning anything.

The tell: a green check you no longer feel relieved to see.

We covered this in the verifiers-go-stale segment. Tests that ossified around old behaviour, eval cases the world moved past, a quality bar that learned its idea of "good" from a narrowing band of outputs. A passing verifier is a claim with an expiry date, and almost nobody dates it.

### Three. The loop eats its own tail

A compounding loop that only ever reads its own output converges to a fixed point. Same hooks, same structure, same three jokes. It looks like the loop found its voice. It collapsed.

The tell: outputs getting more consistent and you feel relief instead of alarm.

This was the echo-chamber segment. The fix was exogenous signal at exactly one stage, plus blind rubric-drift detection on a calendar. It belongs in the eroding column with an asterisk: better models converge *faster* and *more fluently*, which makes the collapse harder to spot, not easier. The mechanism doesn't go away, the disguise gets better.

### Four. Ambiguity compounds into the wrong branch

You hand the loop a goal with one unmade decision in it. The worker picks at turn three, picks blind, and you find out at turn forty that the whole run went down a fork you never wanted.

The tell: a finished run that solved a problem next to the one you had.

The cure was in the writing-effective-goals segment, the interview that fires the questions at you before any autonomous turn. This is the most clearly eroding failure on the list. Longer reliable runs and better mid-run clarification will absorb a lot of it. But it never hits zero, because the ambiguity was never in the worker. It was in you.

[IMAGE: dark canvas, four failure cards in a row labeled "fake verifier", "stale verifier", "loop eats its own tail", "ambiguity compounds", each card fading and crumbling under a shared downward arrow labeled "every model release pushes these back". A small asterisk on the echo-chamber card noting "converges faster, harder to spot". Caption: "real today, eroding by the next release".]
![[loopy-where-loops-fail-right-now-the-model-limited-failures-the-column-that-s-erodi-v1-1.png]]
![[loopy-where-loops-fail-right-now-the-model-limited-failures-the-column-that-s-erodi-v1-2.png]]
![[loopy-where-loops-fail-right-now-the-model-limited-failures-the-column-that-s-erodi-v1-3.png]]
![[loopy-where-loops-fail-right-now-the-model-limited-failures-the-column-that-s-erodi-v1-4.png]]
![[loopy-where-loops-fail-right-now-the-model-limited-failures-the-column-that-s-erodi-v1-5.png]]

---

## The human-owned failures (the column that doesn't move)

[IMAGE: dark canvas, four solid stone tablets in a row labeled "vague goal", "no kill switch", "no dial", "no exogenous anchor", each with a small icon of a model-version number bouncing off it without leaving a mark]

![[loopy-where-loops-fail-human-owned-tablets-1.png]]
![[loopy-where-loops-fail-human-owned-tablets-2.png]]
![[loopy-where-loops-fail-human-owned-tablets-3.png]]
![[loopy-where-loops-fail-human-owned-tablets-4.png]]
![[loopy-where-loops-fail-human-owned-tablets-5.png]]

### Five. The goal defers to the model

"Make the app production-ready." Production-ready according to whom? Nothing in the world can prove that string true, so the loop runs until the budget dies or the worker decides it feels done and the judge nods along.

The tell: a success criterion no command could ever confirm.

Straight from the writing-effective-goals segment. The fix is a DONE WHEN the worker's own output can prove, backed by a VERIFY command whose raw result lands in the transcript. A smarter model does not fix this. It just gives you a more convincing argument that the unprovable thing is done.

### Six. No kill criteria

A goal with a destination and no off-ramp. No turn cap, no failure condition. On a goal it cannot actually reach, it auto-continues forever, burning every dollar you gave it, because the judge keeps saying not done and the runtime keeps obeying.

The tell: a loop you have to remember to turn off.

Budget exhaustion is a decision point, not a defeat. Every goal needs a turn cap and ideally an explicit "stop and ask if X" line. This one gets *worse* as models run longer unattended, because the window in which a missing kill switch can spend your money quietly gets wider, not narrower.

### Seven. Too much authority, too early

The autonomy-dial chapter, compressed. The dial set once, per loop, globally, so the setting that's right for "format this file" is the setting that emails your client. A vague never-list the model reads generously, against you. No ship-and-log tier, so trust never accumulates. Reversibility judged on the filesystem when the recipient already read the email. And the loop allowed to edit its own dial, which means it has no dial at all.

The tell: the loop did something you'd have stopped, and you realise you never told it not to.

This is the most dangerous entry on the entire list in a world of better models, and I want to be loud about it. Everything else degrades gracefully. This one degrades catastrophically, because a more capable, longer-running, more trusted loop with no dial is exactly the loop that can do the most damage in the time you're not watching. The dial is reversibility first, nudged up by blast radius, low verifiability, and cost. It is human-owned, full stop, and it gets *more* important every time the model gets *more* capable.

### Eight. The artifact silently rots

Your CLAUDE.md gets longer. Your skill picks up a rule from a project three months ago. Your rubric tightens past the point of usefulness. The loop feels worse and you blame the model.

The tell: "the model got dumber." It almost never did.

The model probably didn't change. Your artifact drifted and nothing was watching it. We made this argument in the self-improvement segment and again in where-taste-went: the prompt is perishable, the best one today is not the best one next month, and the only defence is reading the action log and the diff on a cadence. Swapping the model hides this, because a fresh model is fluent enough to make the drifted artifact sound fine for a few more weeks. Then you're back, blaming the next model.

### Nine. The trigger fires on the wrong thing

The quietest one, because the loop runs perfectly. It just runs on the wrong cue, or on everything, or on nothing. A loop that fires on every event drowns you. A loop that fires on the wrong event solves problems you don't have.

The tell: a healthy loop producing output nobody asked for.

We met this back in the where-loops-hide segment. The trigger is the first primitive and the one people set most carelessly, because it feels like plumbing. It isn't. It's the question of what is even worth a loop at all, and no model release answers that for you.

---

## The diagnostic

[IMAGE: dark canvas, a single checklist titled "my loop stopped working and I don't know why", nine rows, each a one-line tell, a hand-drawn checkbox next to each]

![[loopy-where-loops-fail-diagnostic-checklist-1.png]]
![[loopy-where-loops-fail-diagnostic-checklist-2.png]]
![[loopy-where-loops-fail-diagnostic-checklist-3.png]]
![[loopy-where-loops-fail-diagnostic-checklist-4.png]]
![[loopy-where-loops-fail-diagnostic-checklist-5.png]]

When a loop goes wrong, you don't reach for the model. You walk the nine tells in order.

Did it report success on wrong work? Fake verifier. Does a green check no longer relieve you? Stale verifier. Are outputs converging? Echo chamber. Did it solve the adjacent problem? Compounded ambiguity. Is the success criterion unprovable? Deferring goal. Do you have to remember to turn it off? No kill switch. Did it do something you'd have stopped? No dial. Did it just start feeling worse? Drifted artifact. Is it producing output nobody wanted? Wrong trigger.

Notice what's not on the list. "The model is bad." That's almost never the answer, and reaching for it is how people avoid the work in the two columns. The model is the one part of this system you didn't build and can't fix. Every part you can fix is on the checklist.

---

## What changes, and what you carry forward

[IMAGE: dark canvas, a timeline arrow pointing right labeled "model capability". The left column of failures fades out along the arrow. The right column stays fully drawn the entire length]

![[loopy-where-loops-fail-timeline-erosion-1.png]]
![[loopy-where-loops-fail-timeline-erosion-2.png]]
![[loopy-where-loops-fail-timeline-erosion-3.png]]
![[loopy-where-loops-fail-timeline-erosion-4.png]]
![[loopy-where-loops-fail-timeline-erosion-5.png]]

Run the tape forward two years. The reliable unattended window goes from minutes to a full working day. Context stops rotting halfway through a long run. Self-verification gets honest enough that you stop hand-building every verifier. The left column thins out. Some of these segments will feel like history.

The right column does not move. A goal that defers to the model is still vague. A missing kill switch is still missing. A dial you never set is still unset. An artifact nobody reads still rots. These are not waiting on a better model. They were never about the model.

So the through line of this whole class lands here. The work that lasts is not prompting the worker. It's owning the goal, the kill switch, the dial, the anchor, and the rubric. The better the models get, the more of the loop they run, and the more it matters that the few things still in your hands are the right few things, set well.

Which is exactly the question the last segment of this class answers. If the model does the doing, where did the judgment go? That's where taste went, and it's where we finish.

---

## Demo

Don't demo a working loop. Demo a broken one, on purpose, because the diagnostic is the skill here.

1. Open a loop of yours that has actually misbehaved, and pull its action log for a run that went wrong. Real one, not a toy.

2. On screen, walk the nine tells out loud against that log. Narrate it. "Did it report success on wrong work? Let's see what the check actually tested." Point at the line in the log where the failure first shows, not where you noticed it. There's almost always a gap between the two, and the gap is the lesson.

3. Name which column it's in. If it's a fake or stale verifier, say "this one the models will help with over time." If it's a deferring goal or an unset dial, say "this one is mine forever, no model fixes it."

4. Fix the human-owned one live. Edit the goal's DONE WHEN to something a command can prove, or add the missing line to the never-list, on camera. Save. Re-run. Show the loop behave.

5. Close on the checklist itself. Put the nine tells up as a single card and say: "Next time a loop of yours dies, you don't guess, and you don't blame the model. You walk this."

Total demo: six minutes. The point is the walk, not the fix. People need to watch you refuse to blame the model.

---

## Key Insight

> A loop almost never dies of one cause. It dies of the weakest section you got lazy on. Half the failure modes erode as the models improve. The other half, the vague goal, the missing kill switch, the unset dial, the rotting artifact, never move, because they were never about the model. Better models make those more dangerous, not less.

---

## Closing

That's the field guide. Nine failures, two columns, one checklist.

Keep it nearby. The next time something you built quietly stops working, you'll feel the urge to say the model got worse. Resist it. Walk the nine. The answer is almost always a section you can fix, sitting in a column you own.

And carry the bigger point into the final segment. As the models get better, they take the left column off your plate and hand you the right column to own completely. That's not less work. It's the only work. We finish on where that work lives, and what it's called.

See you in the last one.
