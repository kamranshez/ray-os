---
duration: "12-16 min"
batch: 5
order: 20
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "The Reconciliation Loop"
status: "scripted"
aliases: [reconciliation-loop, current-state-ideal-state]
---

A discovery loop watches the world and asks "what is worth doing." A reconciliation loop watches you, and asks "are you still where you said you wanted to be."

That is the last shape in this chapter. It is also the one that finally takes loops out of the codebase.

Everything up to here has been pointed at work. A worker drains a queue of tasks. A discovery loop scans your streams for new tasks. Both produce or consume tasks, and tasks live in your repo, your tracker, your inbox. The reconciliation loop is pointed at something else entirely: **the gap between a state you declared and the state you are actually in.**

Once you see it, you cannot unsee it. Because almost everything you care about, in life and in work, is a gap between where you are and where you want to be.

---

## The three shapes, finally side by side

You have now built two of the three fundamental loop shapes, and this video adds the third. Hold them next to each other, because the contrast is the whole lesson.

**A worker** takes a problem in and emits a solution. One queue in, finished tasks out. It needs your instructions.

**A discovery loop** takes the world in and emits problems. Many streams in, a short list out. It generates your instructions.

**A reconciliation loop** takes a declared ideal in, compares it against reality, and emits the corrections that close the gap. It does not wait for a task. It does not hunt for novelty. It holds a target and continuously asks "how far off are we, and what moves us closer." A thermostat, not a worker and not a scout.

The worker has a destination it reaches and then stops. The reconciliation loop has a setpoint it never stops holding. That difference, destination versus setpoint, is the entire reason this is a separate level.

[IMAGE: dark canvas, three loop shapes in a row. Left "worker": one queue arrow in, finished-task arrow out. Middle "discovery": many stream arrows in, short-list arrow out. Right "reconciliation": a single "ideal state" target line at top, a "current state" line below it, a gap between them, and a correction arrow pulling current up toward ideal. A thermostat dial icon on the reconciliation panel]

---

## What everyone gets wrong: a goal is not an ideal state

Back in the toolbox you learned to write goals, and a goal feels like this. It is not, and the difference is the thing to get right.

A goal is a destination. "Ship the auth rewrite." "Close the gap to the theoretical max latency." You run a loop at it, the loop converges, the goal is met, the loop terminates. That is a worker with a finish line. Healthy, finite, done.

An ideal state is a standing description of how things should always be. "My test suite is always green on main." "My churn is never above two percent." "Every customer who emails support gets a reply within an hour." There is no finish line. The world keeps moving, entropy keeps pulling your current state away from the ideal, and the loop's job is to keep pulling it back. Forever.

You do not complete an ideal state. You maintain it. That is why a reconciliation loop never terminates the way a worker does. Its terminate condition is per-run, not per-objective: this tick, the gap is closed or the correction is queued, sleep until the next tick. The objective itself is immortal.

If you treat an ideal state like a goal, you build a loop that fixes the thing once and walks away, and three weeks later you are back where you started and did not notice. If you treat a goal like an ideal state, you build a loop that burns budget forever guarding a target that was only ever meant to be hit once. Naming which one you have is the first move.

---

## The core insight: current state to ideal state

The person who has thought about this longest and hardest is Daniel Miessler, and he has been building it since 2023. He compressed the whole idea into one tweet:

> The best way to think of loops is as a precursor to PROACTIVE AI Assistants. This combines with you providing your DA your goals in life and work. So then your assistant goes through and sets up tons of constant checks (loops) to proactively make sure your current state is as close as possible to your ideal state.
>
> Daniel Miessler
Source: [PASTE EXACT TWEET URL, x.com/DanielMiessler, Jun 18 2026]

Read what he is actually claiming, because it is bigger than the tweet looks. The loop is not the product. The loop is the precursor. The product is a proactive assistant, and the mechanism that makes it proactive instead of reactive is a pile of constant background checks, each one a reconciliation loop, each one comparing one slice of your current state against your declared ideal and acting to close the difference.

He has written the long version of this for years. The foundational essay frames it as the universal problem for anything alive:

> One way to characterize the universal challenge for anything alive is how to go from its current situation to its desired situation. This applies to finances, employment, starting a business, relationships, raising children, health, and so on.
Source: https://danielmiessler.com/blog/ai-state-management

And the mechanism, stated plainly in his maturity model, is exactly the loop body you already know how to build:

> Your Assistant takes periodic inventory of all inputs and assesses Current State relative to Desired State, in order to plan actions to move towards Desired State.
Source: https://danielmiessler.com/blog/personal-ai-future-state

That sentence is a loop. The trigger is "periodic." The work is "assess current relative to desired." The output is "plan actions to move towards desired." He is describing the same five primitives you stripped a model down to in the toolbox, pointed at your life instead of your repo. His own framing of what a whole agent harness is for lands in the same place: it is "an advocate for you to move you towards your ideal state."
Source: https://danielmiessler.com/blog/we-are-all-building-single-digital-assistant

[IMAGE: dark canvas, a horizontal bar labeled "ideal state" at the top and a wobbling line labeled "current state" below it that keeps drifting down and getting yanked back up by repeated small "correction" arrows firing on a clock. Caption strip: "the loop never finishes, because entropy never finishes"]

---

## The shape: a setpoint controller

Every reconciliation loop has the same physical shape, and it is the thermostat. Reach back to the strip-the-model-out primitives, because a reconciliation loop is just those five slots filled a particular way.

The trigger is a clock or a state-change event. The loop wakes on a schedule, or it wakes because a watched value moved.

The work is the comparison plus the correction. Read the current state from the world, hold the ideal state from your declaration, compute the gap, and decide the action that shrinks it. The comparison is the genuinely new muscle here, and it is where all the leverage lives.

The check is the part people skip, and skipping it is fatal at this level. A reconciliation loop's verifier is the ideal state itself, written down as something testable. This is the deepest tie back to everything you learned about verifiers, and it is worth saying slowly. Miessler's sharpest insight is that the criteria that define your ideal state are the same criteria you verify against:

> The Ideal State Criteria carry through to become the VERIFICATION criteria as well. In fact that's their entire point.
Source: https://danielmiessler.com/blog/nobody-is-talking-about-generalized-hill-climbing

That is the borrowed verifier from the builder-verifier chapter, all the way up at the altitude of your life. If your ideal state is "churn never above two percent," the verifier is a Stripe query, not the model's opinion. If your ideal state is "main is always green," the verifier is the test run, not a vibe. The moment your reconciliation loop's check is the model saying "this seems fine," you have rebuilt the self-grading failure, just pointed at something that matters far more than a pull request.

The state is the memory of what it already corrected, so it does not fire the same fix every tick and so it can tell drift from a one-off.

The terminate is per-run. Gap closed or correction dispatched, sleep until the next trigger. The loop as a standing thing never ends.

---

## The three kinds of ideal, in plain words

Miessler's framing in the tweet has a quieter cousin worth naming, because most people's ideal states fall into exactly three buckets, and each one builds a slightly different loop.

Things you want to always be true. The maintain-invariant. Main is always green. Backups ran in the last twenty four hours. Every prospect in the pipe has a next action dated. When the loop finds one of these broken, its job is to restore it, automatically if the blast radius is low, or by surfacing it to you if it is not.

Things you want to never be true. The guard-invariant. Spend never exceeds budget. No secret is ever committed to the repo. Churn never breaks two percent. When the loop catches one of these crossing the line, its job is to alarm, block, or roll back. This is the one you keep pinned to surface-as-decision, because the never-list is your never-list precisely because the stakes are high.

Things you want to happen if something else happens. The event-condition-action rule. If a customer's usage drops to zero for a week, open a check-in. If a dependency ships a security patch, open an upgrade. These are the reconciliation loops that look the most like discovery loops, except the trigger is a declared condition rather than open-ended scanning.

Write your ideal state as a list under those three headers and you have just specified a fleet of loops. That list, the always, the never, and the if-then, is the input. The loops are what you point at it.

---

## It was never about code

This is the part of the chapter where the whole class breaks out of the IDE, so sit with it.

Every example so far has been a repo. But nothing about a reconciliation loop is specific to code, and Miessler's entire point is that the same shape runs your health, your finances, your relationships, your business. His list of what a personal assistant should hold an ideal state for is blunt: "for me, for my businesses, for my finance, for my health, for my relationships."
Source: https://danielmiessler.com/blog/we-are-all-building-single-digital-assistant

The mechanism does not change across those domains. Only the verifier does. "I work out three times a week" reconciles against a fitness API. "My runway never drops below six months" reconciles against your bank balance. "I talk to my closest friends at least monthly" reconciles against your messages. The loop reads current state, compares to the declared ideal, and surfaces the gap. The criteria look completely different in each domain, but the process of writing them, checking against them, and correcting is identical. That sameness is what makes it a primitive and not a trick.

And it composes with everything you already built. A reconciliation loop that finds a gap does not have to fix the gap itself. It can mint a task and hand it to a worker. "Main is red" becomes a fix-it ticket for the worker loop from earlier in this chapter. In fact, you can now see that a discovery loop is just a reconciliation loop with one specific ideal state: "there is no unaddressed signal in my streams." Discovery is the special case. Reconciliation is the general one. That is why this video sits at the top of the climb.

[IMAGE: dark canvas, a central "ideal state" document icon labeled with five domains stacked (code, health, finance, business, relationships). Five small reconciliation loops radiate out, each reading a different real-world source (test runner, fitness API, bank, Stripe, messages) and each emitting a correction arrow back toward the central document. Caption: "one shape, five verifiers"]

---

## Where you stay in the loop, and where you don't

The human role here is the cleanest in the whole stack, and it splits in two.

You do not stay in the loop for the comparison. Reading the world and computing the gap is the entire reason you built the loop. If you are personally checking whether main is green or whether spend crossed budget, you have not built a reconciliation loop, you have appointed yourself the thermostat.

You absolutely stay in the loop for two things. First, declaring the ideal state, because that is a values question and a taste question and it is irreducibly yours. Miessler is emphatic that the hard part, the human part, is "deeply thinking about and clearly articulating your ideal state."
Source: https://danielmiessler.com/blog/ai-state-management

Second, you stay in the loop for the high-blast-radius corrections. A maintain-invariant on a green test suite can self-heal silently. A guard-invariant on money or anything public comes to you with the gap, the proposed correction, and a recommendation, and it waits. This is the autonomy dial applied to a whole class of loop: low-stakes maintains get notch one, the never-list gets notch three, every time.

---

## The failure mode this level is most prone to

There is one way reconciliation loops rot, and it is specific to this level: a wrong or stale ideal state, enforced perfectly.

A worker that does the wrong task wastes one run. A reconciliation loop pointed at the wrong ideal does damage continuously and confidently, because its whole nature is to keep pulling reality toward the target without stopping. If the target is wrong, you have built a machine that fights you forever, and because it is quietly succeeding at its declared job, nothing alarms. The loop is green. The outcome is bad.

The defense is that the ideal state is itself a living document, not a stone tablet. Miessler treats articulating and re-articulating the ideal as the most important and hardest work there is, something you tighten, prune, and expand over time. So a mature reconciliation system has a slower meta-loop above it whose entire job is to re-examine the targets: are these still the states I want held. That is the same self-improvement instinct from the compounding-loops chapter, aimed one level up, at the setpoints instead of the work.

The second, smaller failure is over-correction. A loop that yanks too hard at every tiny deviation thrashes. Give your corrections a deadband, the way a real thermostat does not fire the furnace for a half-degree wobble. Small drift inside the band is tolerated. Only real gaps trigger action.

---

## Demo

Put a single reconciliation loop on screen, kept deliberately small.

1. Show the ideal state file. One markdown file, three headers: always-true, never-true, if-then. Under always-true: "main is green." Under never-true: "no AWS key is ever committed." Under if-then: "if a dependency has a published CVE, open an upgrade PR." That file is the entire configuration. No tasks, no queue.

2. Show the trigger. A scheduled routine fires every hour, and a second trigger fires on every push. Same scheduled-task and hook primitives from earlier in the class, pointed at state instead of work.

3. Show the comparison for one invariant. For "main is green," the loop runs the test suite. That run is the borrowed verifier: the suite is the external grader, not the model's read. Green means the gap is zero, the loop sleeps. Red means a gap exists.

4. Show the correction path branch on blast radius. The green-main maintain is low stakes, so on red the loop mints a fix-it task and hands it to the worker loop you already built. The never-commit-a-key guard is high stakes, so on a hit it blocks the push and surfaces to Slack with the offending line, and it waits for you. Same loop shape, two different notches on the autonomy dial.

5. Show the state file. A record of what it has already corrected this week, so it does not re-open the same upgrade PR every hour and so it can tell genuine drift from a flake.

Total demo: three minutes. The point is that you wrote down how the world should be, in three short lists, and a loop now holds reality against it without you watching. You did not assign a single task. You declared a state and pointed a loop at the gap.

---

## Key Insight

> A worker reaches a destination and stops. A discovery loop hunts for new destinations. A reconciliation loop holds a setpoint and never stops. The first two move you through the world. The third one keeps the world the way you said it should be.

---

## Where we go next

You can now build all three loop shapes: one that does the work, one that finds the work, and one that holds your declared state against reality. That is the full vocabulary of the climb.

What is left is not a new shape but a habit: noticing, in your own day, which repeated frictions are secretly one of these three loops waiting to be written. That is the next one, and it is how you stop learning loops and start living in them.

See you in the next one.
