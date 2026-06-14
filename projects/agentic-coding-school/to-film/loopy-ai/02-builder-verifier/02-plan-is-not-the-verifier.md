---
duration: 10-14 min
batch: 2
order: 2
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [plan-is-not-the-verifier, dont-verify-against-the-plan]
---

In the last video I showed you the builder-verifier loop, and I gave you a menu of things the verifier can check against. Tests. A rubric. Guidelines. User flows. The plan. I told you one of those was a trap and I'd come back to it. This is me coming back to it.

The trap is the plan.

Here's the whole video in one line. Your plan is the most ignorant document in the entire project, because you wrote it before you'd done any of the work. Verify your finished build against it and you will tear out everything the build taught you.

---

## The plan is a guess you make before you know anything

Think about when the plan gets written. It's the very first thing. No code exists. No edge cases have surfaced. You have not yet discovered that the library you picked doesn't do the one thing you needed, or that the clean two-table schema falls apart the moment real data hits it, or that the bullet point reading "sync the two systems" is secretly three weeks of work.

The plan is a hypothesis. It's your best guess at the shape of the work, made at the exact moment you understand the work least.

And that's fine. That's what a plan is for. It points you in a direction so you can start moving. Nobody writes a perfect plan, and chasing one is how you spend a week planning and zero days building.

But here's the part people miss. The moment the builder starts working, the plan begins going out of date. Every fix, every dead end, every "oh, it actually has to work like this" is information the plan does not have and never will, because the plan stopped learning the instant you finished writing it.

The build learns. The plan doesn't. By the time the loop is halfway done, the plan is the oldest, dumbest artifact in the room.

[IMAGE: dark canvas, hand-drawn. A staircase climbing left to right, each step labeled with something the build discovered: "lib won't do it", "schema wrong", "extra edge case", "renamed the flow". A small figure climbing the steps upward labeled "BUILD". Down at the bottom of the stairs, a heavy anchor labeled "PLAN" with a taut rope pulling the climbing figure backward toward step one. Caption underneath, sketch font: "the plan only knows step one"]

![[loopy-plan-is-not-the-verifier-stale-anchor-1.png]]
![[loopy-plan-is-not-the-verifier-stale-anchor-2.png]]
![[loopy-plan-is-not-the-verifier-stale-anchor-3.png]]
![[loopy-plan-is-not-the-verifier-stale-anchor-4.png]]
![[loopy-plan-is-not-the-verifier-stale-anchor-5.png]]

---

## The trap looks exactly like a real loop

Now watch how this kills a loop, because it's seductive and it's everywhere.

The agent writes a plan. Then it builds. And because it's a good agent, it adapts as it goes. It hits the library wall and swaps the library. It hits the schema problem and splits the table. The adversarial reviewer from later in this chapter pushes back, the builder revises, and the thing slowly converges on something that actually works. That back-and-forth, that divergence from the original plan, is not a bug. It is the single most valuable thing the loop produced.

Then you bolt on a final verifier and you tell it: check the build against the plan.

And the verifier does its job. It reads the plan, reads the build, and reports back, "this has drifted a long way from what we agreed. The plan said one table, this has two. The plan said library X, this uses Z. Reverting to spec."

It just deleted every correct decision the build made. It snapped the work back to the version from before you knew anything. The plan won, and the plan was the most ignorant participant in the entire project.

This is the cruelest version of the failure, because it has the exact shape of L2. There's a build step. There's a check step. There's a loop that exits when the check passes. It looks like everything I taught you in the last video. But the check is pointing at the wrong target, so the better your build gets, the harder the verifier fights it. You built a machine whose job is to undo learning.

---

## Not everything in the plan is disposable

So you might be thinking: fine, throw the plan away, never check against it. Not quite. The plan isn't uniformly worthless. It's two different things wearing one cover.

Open any plan and you'll find two kinds of statements mixed together.

One kind is **intent**. What does the user actually need to be able to do. What must never happen. The budget. The deadline. The promise you're making to whoever asked for this. This stuff is durable. It was true before you wrote a line and it's true at the end. The user still needs to log in. The thing still can't leak data. These don't go stale, because they were never guesses about *how*, they were statements about *what* and *why*.

The other kind is **implementation guesses**. Use this library. Store it in that table. Do it in these three steps. This is the part that was always provisional. You wrote "use library X" because at planning time X looked right, not because the universe requires X. The build is allowed to overturn every one of these, and a good build will.

The disaster is verifying against the second kind. You gate the finished work against your opening guesses about implementation, and you punish the build for being smarter than the plan was.

So the move isn't "ignore the plan." It's separate the two. Keep the intent, because that's the thing you're actually trying to satisfy. Let the implementation flex, because that's the thing the build exists to figure out.

[IMAGE: dark canvas, hand-drawn. A single document outline down the middle, splitting into two columns. Left column, drawn solid and bright, headed "INTENT (durable)" with items: "what the user needs", "hard constraints", "budget / deadline". Right column, drawn faint and dashed like it's dissolving, headed "IMPLEMENTATION (disposable)" with items: "use library X", "one table", "these 3 steps". A bold check mark pointing at the left column, a small "let it flex" note by the right. Caption: "verify the what, not the how"]

![[loopy-plan-is-not-the-verifier-durable-vs-disposable-1.png]]
![[loopy-plan-is-not-the-verifier-durable-vs-disposable-2.png]]
![[loopy-plan-is-not-the-verifier-durable-vs-disposable-3.png]]
![[loopy-plan-is-not-the-verifier-durable-vs-disposable-4.png]]
![[loopy-plan-is-not-the-verifier-durable-vs-disposable-5.png]]

---

## What to actually point the verifier at

If the plan's implementation half is off limits, what does the check aim at? Three things, and notice they're all things the build can't quietly rewrite to make itself pass.

**Constraints.** The hard rules that don't move. Security, budget, the data that can't leak, the latency ceiling, the thing the regulator requires. These came from intent, not from a guess, so they're safe to gate on. The build doesn't get a vote on whether it's allowed to leak credentials.

**User flows.** This is the big one, and it's the one most people skip. Don't ask "did it match the plan." Ask "can the user actually do the thing they came to do." Walk the real path. Sign up, land on the dashboard, create the item, see it persist, log back in, find it still there. A user flow doesn't care which library you used or how many tables there are. It only cares whether the goal is reachable. That's exactly why it survives the build: it's defined in terms of intent, the one part of the plan that never goes stale.

The thread connecting all three: every one is independent of *how you built it*. They test whether you arrived, not whether you took the route you sketched at the start. That independence is the whole point. A verifier earns its keep by being able to disagree with the build for reasons the build can't just edit away, and your opening implementation guesses fail that test completely.

---

## So write a looser plan on purpose

Here's the part that surprises people. Once you accept that you verify against intent and not implementation, it changes how you should write the plan in the first place.

A heavy, hyper-detailed plan is actively harmful. Every specific implementation decision you pin down in advance is one more thing the build will rightly diverge from, which is one more false "you drifted" violation waiting to fire, and one more temptation to revert good work back to your worst-informed guess. The more precise your plan, the more surface area it has to be wrong about, and the louder it argues with the build.

So write the plan loose. Nail the intent: what the user needs, the constraints, the bar for done. Stay vague on the implementation: gesture at an approach, then let the build discover the details. You're not being lazy. You're refusing to pretend you know things you can't know yet.

And if you want a record of what got built, the direction flips. The plan doesn't judge the build. The build updates the plan. When the loop discovers the real schema, it writes that back into the plan, so the document tracks reality instead of fighting it. The plan becomes a living log of what you learned, not a frozen contract you're in breach of.

---

## Name it on the five components

Map it onto the spine from the start of this chapter. Trigger, Work, Check, Terminate, State.

This is a **Check** failure, and now you can say exactly what's wrong with it. The check got wired to **State**, specifically to the stalest piece of state in the whole loop.

The plan is state. It's context the loop carried forward from iteration zero. And it's the one piece of state that never gets refreshed, because while the build updates everything around it, the original plan just sits there frozen at its most ignorant. Point your Check at it and you're grading today's work against the loop's first-draft memory of itself.

The fix is the same shape every time. Check points outward, at a signal the build did not author and can't rewrite: a constraint, a user flow, reality. Never back at the frozen plan.

[IMAGE: dark canvas, hand-drawn. The five components in a row: TRIGGER, WORK, CHECK, TERMINATE, STATE. The STATE box has a small "plan, frozen at step one" label and a little ice/snowflake mark on it. A red arrow loops from CHECK back to STATE with an x over it. A green arrow runs from CHECK outward to a box off to the right labeled "CONSTRAINTS / USER FLOWS / REALITY". Caption: "Check points out, not back at frozen state"]

![[loopy-plan-is-not-the-verifier-check-points-out-1.png]]
![[loopy-plan-is-not-the-verifier-check-points-out-2.png]]
![[loopy-plan-is-not-the-verifier-check-points-out-3.png]]
![[loopy-plan-is-not-the-verifier-check-points-out-4.png]]
![[loopy-plan-is-not-the-verifier-check-points-out-5.png]]

---

## Demo

I'll make it concrete and let you watch the trap spring.

1. Give an agent a small feature and a loose plan: "let users save notes, must persist across logins." The plan also carries one throwaway implementation guess, "store notes as a single JSON blob per user."
2. Let it build. Partway through, the agent discovers the JSON-blob idea makes "find a note" painful, so it switches to a proper notes table. Good call. It diverged from the plan and the build got better.
3. Now run the wrong verifier. Point a reviewer at the build and tell it to confirm the build matches the plan. Watch it flag the divergence as a defect: "spec says single JSON blob, implementation uses a table, reverting." It tears out the better design to satisfy the dumber plan.
4. Reset. Run the right verifier instead. Don't mention the plan's implementation. Just walk the user flow: create a note, log out, log back in, the note is still there, search finds it. It passes. The thing the user actually needed works.
5. Put the two runs side by side. Same build, same model. One verifier destroyed the best decision in the project. The other only ever asked whether the user got what they came for.

---

## Key Insight

> Your plan is the most ignorant document in the project, because you wrote it before you did the work. Verify against the constraints and the user flow, never against the plan, or you'll revert everything the build taught you.

---

Last video handed you the loop. This video tells you the one place you must never anchor the check: your own first guess. Aim it at what's durable, intent, flows, reality, and let the build outgrow the plan. Next we take the strongest model-based check and weaponize it, by pairing the creator with an attacker whose only job is to break the work.
