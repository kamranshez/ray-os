---
duration: "8-12 min"
batch: 9
order: 36
batch_name: "Loops In The Wild"
class: "loopy-ai"
chapter: "The Anti-Spin Loop"
status: "scripted"
aliases: [anti-spin-loop]
---

Every loop so far in this chapter knew when to stop. This video is about the loops that do not, and the one command that fixes it.

Most agent loops never pause to ask whether they are actually making progress. So they retry the same broken approach, flip-flop between two wrong fixes, or quietly edit the failing test to make it pass. The loop looks busy. The loop is green. The loop is lying.

This is the governance chapter made into a single pasteable command, and it is the best-designed loop in the whole cookbook.

---

## The problem it kills

A loop with no brake is a money fire.

The romantic version of loops is a thousand agents building your company overnight. The production version is a bill. One person on Reddit torched about six thousand dollars overnight with a single command, in a thread that drew over a thousand upvotes. Uber capped its engineers at fifteen hundred dollars per tool per month, after burning its annual AI budget in four months.
Source: https://www.reddit.com/r/codex

The funniest summary of the entire movement was a comment written as code: while you have tokens, burn them in a loop. That is what an unbounded loop is. The fix is not to be smarter about the prompt. The fix is to put real stops in the body.

[IMAGE: dark canvas, a loop arrow circling on itself with dollar-sign flames underneath, a "no progress" meter flatlined in the center, the same broken patch being tried three times labeled "retry, retry, retry", contrast panel on the right showing the same loop with four small stop signs labeled "no progress, repeat, flip-flop, budget"]

![[loopy-litw-anti-spin-loop.png]]

---

## The loop

This one surfaced as a Claude Code skill on r/claudeskills, and it is built entirely around knowing when to quit.

```
/loop build toward the goal, then audit and verify against a machine-checkable contract. Stop if you make no progress, repeat an approach, flip-flop between approaches, or hit the budget. Finish only when the contract passes.
```

Look at how many ways it is allowed to stop. No progress. Repeating an approach. Flip-flopping between approaches. Hitting the budget. That is four independent brakes, and a loop that runs unattended needs every one of them, because each maps to a real way loops rot.

And look at the one way it is allowed to succeed: the contract passes. Not "the agent feels done." A machine-checkable contract, graded by something other than the agent's mood.

---

## Why it works: progress is a verifier too

Chapter three taught you to verify the work. This loop verifies the loop itself.

No-progress detection is a verifier pointed at motion instead of output. It asks "is this turn actually closer than the last one," and if the answer is no for too long, it stops. That single check kills the most common failure in autonomous loops, the agent retrying the same broken approach with total confidence, forever, on your dime.

Flip-flop detection is the same instinct aimed at oscillation. If the loop keeps swapping between approach A and approach B without converging, it is not exploring, it is stuck, and it should stop and surface rather than burn another ten dollars discovering that again.

The budget is the hard backstop under all of it. Even if every other brake fails, the loop dies when it hits the ceiling. You set that ceiling before you walk away, not after the email arrives.

---

## The deeper point: a loop is a money fire with a verifier on top

This is the line to carry out of the chapter.

A loop that cannot tell good output from bad does not save you work. It just produces wrong answers faster. Writing the loop is the easy part. The verifier inside it, and the brakes around it, are the hard part, and they are the whole part.

Everything in the governance chapter, the kill switch, the budget, the log review, lives inside this one command in miniature. If you only ever paste one safety pattern from this class, paste this one.

---

## Demo

Put a deliberately stuck task in front of it.

1. Show the contract. One machine-checkable file: the exact condition that counts as done. Not a vibe, a check that passes or fails.

2. Let it work normally. The loop builds, audits against the contract, fails, tries again, gets closer. Normal healthy progress. Point at the progress check passing each round.

3. Trigger no-progress. Feed it a task where the obvious fix does not work. Watch it try, get no closer, try again, and then stop itself and surface, instead of grinding. Name it: that is the no-progress brake.

4. Trigger the budget. Set a tiny ceiling and a big task. Watch the loop hit the budget and halt cleanly with a report, not a surprise invoice.

5. Show the clean finish. Give it a solvable task and watch it stop the only good way, the contract passing.

Total demo: four minutes. The point is that this loop is allowed to stop four different ways and succeed only one way, and that asymmetry is what makes it safe to leave alone.

---

## Key Insight

> A loop that cannot tell good output from bad just automates being wrong, faster. The brakes are not a feature of a good loop. They are the loop.

---

## Where we go next

You have now seen the brakes that keep one loop honest with itself. The last loop in the cookbook adds a second set of eyes from a different model entirely, so two independent judges have to agree before anything ships.
