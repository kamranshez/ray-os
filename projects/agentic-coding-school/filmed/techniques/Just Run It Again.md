---
status: filmed
---

You come up with a plan. You run your spec developer agent. It produces something reasonable. You move on.

That's the mistake. You should have run it again.

AI agents are **non-deterministic**. Every time they run, they load context differently, traverse the codebase in a different order, weigh information differently. The same agent, same task, same codebase — different output. Not wildly different, but different enough that each run catches things the previous run missed.

The fix is dead simple: **repeat it five times.**

![[images/best-of-5.png]]

---

## What this looks like in practice

Say you need a plan for a new feature.

**Run 1:** You kick off the spec developer. It produces a solid plan. Good structure, reasonable steps, covers the main cases. You read it and think, "Yeah, that looks right."

**Run 2:** You run it again. Same agent, same task. This time it catches a dependency you missed, reorders two steps that were in the wrong sequence, and adds an edge case. The plan is noticeably better.

**Run 3:** Run it again. Now it's questioning some of the assumptions from run one. Maybe the data model needs an extra field. Maybe step four should actually be two separate steps. Things tighten up.

**Run 4:** Again. At this point the changes are smaller. A clarification here, a missing test case there. But each one matters.

**Run 5:** One more time, as a sanity check. If this run comes back with nothing meaningful to add, you've converged. The plan is stable. You can trust it.

![[images/best-of-5-3.png]]

---

## Why this works

It's not magic. It's just probability.

Each run samples the problem space differently. The agent reads files in a different order, makes slightly different associations, prioritizes different concerns. Run one might nail the architecture but miss an edge case. Run two might catch that edge case but overlook a dependency. By run five, you've covered enough of the problem space that the gaps are filled.

Think of it like asking five different developers to review the same PR. They don't all catch the same things. The value isn't in any single review — it's in the _union_ of all five.

Except here, you're not coordinating five people. You're just clicking "run" again.

![[images/best-of-5-6.png]]

---

## Where to apply it

**Planning:** Run your planning agent, then run it again. Each pass refines dependencies, sequencing, and scope. By pass five the plan actually holds up under scrutiny.

**Implementation:** After the code is written, run your review agents. Not once — run a batch of them in parallel. Five independent reviewers hitting the same code from different angles. Merge their findings.

**Verification:** After tests pass, run your verification agents again. Are the tests actually testing the right things? Are there gaps? Each run surfaces something the last one didn't.

**Design:** Before you build anything, run your design review five times. This is where it pays off the most, because design mistakes are the most expensive to fix downstream.

![[images/best-of-5-4.png]]

---

## The parallel trick

You don't have to do this sequentially. After a plan is done, fire off five review agents in parallel. Each one independently evaluates the output. Because they're non-deterministic, they'll each find different issues. Collect all five results, apply the fixes, and you're in a dramatically better place than one review would have gotten you.

Same with code. Write it once, then launch five parallel reviewers. One catches a race condition. Another flags a naming inconsistency. A third spots a missing error handler. None of them would have caught everything alone. Together, they cover the space.

![[images/best-of-5-2.png]]