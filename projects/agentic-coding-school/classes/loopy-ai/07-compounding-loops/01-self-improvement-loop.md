---
video_id: "nHJTMAhf"
duration: "14-18 min"
batch: 6
order: 20
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Self-Improvement Loop"
aliases: [self-improvement-loop]
---

There isn't one agent here. There are two loops, running at two different speeds, and the slow one rewrites the fast one.

That sentence is the whole chapter. Up to now you have built loops that do work. A worker churns through a backlog. A goal loop keeps itself alive against an objective. Those are inner loops, and they run constantly, one run per event. This segment adds a second loop on top: one that runs on a schedule, reads many runs of the inner loop, and edits the skill the inner loop is built on.

The shift is small to say and large to absorb. The thing you iterate on stops being the answer. It becomes the instructions that produce answers. You stop hand-correcting outputs and start improving the document that generates them.

This is the move from [[l4-workers]] into compounding loops. A worker gets a task done. A compounding loop gets a little better at the task every day, without you touching it between runs.

---

## Why your skill is already rotting

Here is the uncomfortable part. The skill you wrote last month is already worse than it was the day you shipped it.

> "The best prompt you write today will not be the best prompt a month from now."
Source: https://x.com/petradonka/status/2054897826149101588

Prompts are perishable. And most people only see one of the two reasons they decay, so they only defend against half of it.

The first reason is environment drift. Your product changes. Your users change. Your taste sharpens. New edge cases walk in that you never wrote a line for. None of that touches the model, and the skill still rots, because the skill was a snapshot of a world that has since moved. This is the decay everyone feels, and it is the one the daily feedback loop is built to handle.

The second reason is the one almost nobody plans for. Substrate change. A model upgrade.

A mature skill is not just instructions. A large part of it is compensation. Every "always restate the constraints first," every "do not invent file paths," every careful workaround is you patching the current model's specific weaknesses and defaults. That scaffolding is calibrated to one model.

Upgrade the model and some of that scaffolding goes stale on contact. The new model already does the thing your principle was forcing. Or it does it differently, and now your principle is fighting it. A workaround for a weakness that no longer exists is not neutral. It is noise the new model has to reason around.

So a model release is not a "does it still run" check. It is a re-tune and a prune. The right mental model: a skill is calibrated to a specific model, and you recalibrate on upgrade. Two triggers, two cadences. Environment drift you handle continuously. Substrate change you handle on release day.

[IMAGE: dark canvas, a single skill file in the center slowly decaying, with two distinct arrows of erosion hitting it. One arrow labeled "environment drift" made of small icons (a changed product, a new user, a fresh edge case) chipping at it gradually. A second, sharper arrow labeled "model upgrade" striking it all at once, with a few of the skill's lines lighting up red as "now redundant". Caption: "a skill is calibrated to a specific model".]
![[loopy-self-improvement-loop-prompts-perishable-1.png]]
![[loopy-self-improvement-loop-prompts-perishable-2.png]]
![[loopy-self-improvement-loop-prompts-perishable-3.png]]
![[loopy-self-improvement-loop-prompts-perishable-4.png]]
![[loopy-self-improvement-loop-prompts-perishable-5.png]]

If the skill decays from two directions, hand-patching it forever is a losing game. You need something that watches the skill and repairs it. That something is a second loop.

---

## The two loops

Stop thinking about one agent doing a job. Think about two loops at two cadences.

The inner loop does the work. It runs per event, constantly, in the moment. It triages the issue that just landed. It drafts the reply to the mention that just came in. Every run leaves a trace: a file, an agent trace, a Slack thread, a GitHub label. The trace matters more than it looks, because the outer loop has nothing to read without it. A run that left no record never happened, as far as improvement is concerned.

The outer loop improves the skill. It runs on a schedule, on the order of daily to weekly, and it does not do the work at all. It reads a stack of inner-loop runs, looks at how they actually went, and proposes a change to the skill file. Since skills are just files, that change is a diff.

> "Since Skills are just files, this means it should make a diff to improve [the] Skill."
Source: https://x.com/zachlloydtweets/status/2066908445425496348

That is the entire architecture. A fast loop that acts and records. A slow loop that reads and rewrites. Warp runs exactly this shape to maintain their own open-source repository, with a coding agent reading past runs and opening changes to the skills that drive them.
Source: https://x.com/zachlloydtweets/status/2066908445425496348

[IMAGE: dark canvas, two nested cycles. The inner cycle is tight and fast, labeled "inner loop, per event": an event comes in, the skill runs, an action ships, a trace is written, repeat. The outer cycle is large and slow, labeled "outer loop, scheduled": it reads a stack of those traces, finds where runs went wrong, and writes a diff back into the skill file at the center that the inner loop reads from. An arrow shows the diff feeding back into the inner loop's skill. Caption: "the slow loop rewrites the fast one".]
![[loopy-self-improvement-loop-two-loops-1.png]]
![[loopy-self-improvement-loop-two-loops-2.png]]
![[loopy-self-improvement-loop-two-loops-3.png]]
![[loopy-self-improvement-loop-two-loops-4.png]]
![[loopy-self-improvement-loop-two-loops-5.png]]

Make it concrete with the issue triage example. The skill sorts every incoming issue into one of three buckets: ready to implement, duplicate, needs info.

The inner loop is a GitHub Action. A new issue is filed, the action fires, the triage skill runs, and a label gets applied. That is it. One issue, one run, one label, a trace left on the issue itself.

The outer loop is a scheduled agent. Once a day it pulls every issue that got triaged, and it looks for one specific thing: where did a human change the label after the agent set it. The agent said ready to implement, a maintainer flipped it to needs info and left a comment about why. Each of those is a correction. The outer loop reads the pile of them, finds the pattern, and opens a diff to the triage skill so tomorrow's runs get the call right.

You did not retrain anything. You did not write a single new rule by hand. The skill got better because a loop read how the last hundred runs went and edited the instructions.

---

## How often the outer loop should run

The moment a piece of feedback lands, there is a pull to go fix the skill right then. A comment comes in on a pull request, you open the agent, point it at the comment, and say update the skill. It feels responsive. It is the wrong move, and it fails for a reason you already understand from writing code.

> "You end up with monkey patches on the skill that address each of these one by one, but they kind of miss the broader picture."
Source: https://www.youtube.com/watch?v=jcfDKXc7Zxg

Handle one report in isolation and the agent reaches for the most literal fix that points at that one complaint. Run the outer loop per event and the skill fills with those one-off patches, each solving a single case and none of them catching the shape of all the cases together. That is overfitting, and now it is the outer loop doing it.

So you wait. You let feedback pool, a few days, maybe a week, until there are enough data points to show a pattern instead of a point.

This is a design instinct you already trust, moved into skills. You do not pull an abstraction out of code the second time you repeat yourself. You wait for the third and fourth instance to tell you what the abstraction actually is. One or two corrections are not a pattern. A batch of them might be.

Which means cadence is a real knob, with a failure mode on each side. Too frequent and the loop monkey-patches every report as it arrives. Too rare and the skill rots faster than the loop repairs it, while real corrections sit unread. The right setting is not a fixed number of days. It is whatever gives each run a batch big enough to generalize from. High-volume feedback, like Buzz's thousands of mentions a month, makes daily a full batch. A quieter skill might need a week to collect the same signal. Set the clock by the volume, not the calendar.

This is the cadence twin of the per-edit lesson in [[teach-the-agent-to-learn]]. There the trap was turning one correction into one rule. Here it is running the loop so often that one correction is all it ever sees. Batching the feedback is what gives the learning skill something to zoom out from in the first place.

[IMAGE: dark canvas, two horizontal timelines stacked. Top timeline "too frequent": every incoming feedback dot triggers an immediate tiny skill edit, and the skill file beside it grows into a tall stack of brick-like one-off patches labeled "monkey patches", tinted red. Bottom timeline "batched": feedback dots accumulate into a holding bin for a week, then one scheduled run reads the whole bin and emits a single clean diff into the skill file, which stays short, tinted green. Caption: "set the cadence by feedback volume, not the calendar".]
![[loopy-self-improvement-loop-cadence-1.png]]
![[loopy-self-improvement-loop-cadence-2.png]]
![[loopy-self-improvement-loop-cadence-3.png]]
![[loopy-self-improvement-loop-cadence-4.png]]
![[loopy-self-improvement-loop-cadence-5.png]]

---

## When you actually reach for this

This architecture is not for every loop. It exists for one specific situation, and naming that situation tells you when to build it and when not to bother.

Reach for it when the work is judgment-heavy and there is no cheap external grader.

Think about why the builder-verifier loops earlier in this class could self-correct in the moment. Code has graders. Tests pass or fail. The build compiles or it does not. The browser check renders or throws. That signal is fast, cheap, and honest, so the inner loop can check its own work and retry on the spot. No second loop required.

Now look at the other kind of work. Social replies. Support responses. Code review comments. Issue triage. Recruiting outreach. None of these have a test suite. You cannot ship a reply, wait to see whether people trust you more, and retry. The feedback is too slow, too noisy, and too expensive to use live.

So you substitute. The grader you do not have gets replaced by human deviation. The human does the work the way they would anyway, and where they diverge from the agent is the signal. The agent proposed, the human disposed, and the gap between the two is the gradient you learn from. Because that signal is slow and sparse, learning cannot happen in the inner loop. It moves to the slow outer loop, which is exactly why the outer loop runs daily and not per event.

This filtering pays off before any drafting does. Warp's community-reply agent, Buzz, runs on around fifteen skills and processes thousands of mentions a month across Twitter, Reddit, Bluesky, and LinkedIn. About half of those need no reply at all. The loop's first and most valuable job is deciding what not to act on, not writing the perfect response.
Source: https://x.com/petradonka/status/2054897826149101588

And here is the corollary that makes the whole frame click. The human in the outer loop is a stand-in for a grader you do not have yet. The day you can write that grader, an automated check that scores the work without a person, you swap the human out and the exact same machine runs unattended. The architecture does not change. Only who sits in the verifier seat does.

[IMAGE: dark canvas, two columns. Left column "has a grader", showing a code loop with a green tests/build/browser check wired directly into the inner loop, self-correcting in the moment, no second loop. Right column "no grader", showing a judgment-work loop (a reply, a triage label) where the inner loop cannot self-check, so human deviation is captured and fed up into a slow outer loop that edits the skill. A dotted arrow on the right labeled "swap in an auto-grader later" shows the human seat being replaced by a machine. Caption: "human deviation is the grader you don't have yet".]
![[loopy-self-improvement-loop-boundary-condition-1.png]]
![[loopy-self-improvement-loop-boundary-condition-2.png]]
![[loopy-self-improvement-loop-boundary-condition-3.png]]
![[loopy-self-improvement-loop-boundary-condition-4.png]]
![[loopy-self-improvement-loop-boundary-condition-5.png]]

One more thing this depends on, and it gets its own segment next door. The outer loop can only learn from a deviation it can measure. That is why the inner loop's output has to be a clean, comparable decision and not a wall of prose. We build that in [[decision-surfaces]]. And turning those deviations into instructions that generalize, instead of a pile of brittle one-offs, is its own skill, which is [[teach-the-agent-to-learn]].

---

## Demo

Four things on screen, the triage loop end to end.

1. The inner loop firing. Open a fresh GitHub issue live. Watch the Action kick off, the triage skill run, and a label land on the issue: ready to implement. Show the trace it left, the label plus a one-line rationale comment, because that trace is what the outer loop will read.

2. The human deviation. Switch to a maintainer's view. Flip that label from ready to implement to needs info, and leave a comment: the feature is ambiguous on whether it needs a setting. That edit is the entire training signal. Do nothing else.

3. The outer loop running. Trigger the scheduled improvement agent by hand so we do not wait a day. Watch it pull every triaged issue, find the handful where a human overrode the label, and read the comments on why. It is not looking at outputs in isolation. It is looking at agent-said versus human-did.

4. The diff. The outer loop opens a pull request against the triage skill file. Read the diff out loud. It is a change to how the skill decides between ready and needs info, written from the corrections it just saw. Merge it. Re-run the inner loop on a similar issue and watch it make the call the human would have made.

Then point at what did not happen. No fine-tuning. No new model. No hand-written rule. A loop read how the work went and edited the instructions, and the system got better overnight.

---

## Key Insight

> Stop iterating on the answer. Iterate on the instructions that produce answers, and let a slow scheduled loop do that iterating by reading how the fast loop's runs actually went.

---

## Where we go next

You now have the shape: an inner loop that acts and records, an outer loop that reads and rewrites, and a clear test for when it is worth building, which is judgment work with no cheap grader.

What you just built by hand has a formal name and a cleaner decomposition. The next segment, [[ace-three-role-split]], is the formal three-role version of the loop we just built: a generator that does the work, a reflector that diagnoses it, and a curator that edits the playbook. Same idea, sharper edges.

See you in the next one.
