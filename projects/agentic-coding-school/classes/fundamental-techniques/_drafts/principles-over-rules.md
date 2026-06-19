---
class: "fundamental-techniques"
chapter: "Fundamental Techniques"
status: "scripted"
---

# Principles Over Rules

Here is the technique in one line. When you write instructions for an agent, principles beat rules, because rules overfit and principles transfer.

That is the whole video. Everything below is why it is true, how the rule-based version fails, and how to write the principle-based version instead.

This applies everywhere you author instructions. A skill file. A CLAUDE.md. A system prompt. A subagent brief. Anywhere you are trying to get a model to make the same kind of call you would make.

---

## The first version is always a checklist

Watch what happens the first time you write a skill for judgment work.

You start listing cases. If someone reports a bug, say this. If someone compares us to a competitor, say that. If someone asks about pricing, mention this plan. If the tone is angry, apologize first. If they are on the free tier, do not promise a fix date.

It feels responsible. You are being thorough. You are covering the cases.

You are also building a decision tree by hand, and it is going to break.

The prompt gets longer with every case you remember. The replies start to sound robotic, because the model is pattern-matching to your branches instead of thinking. And the first time a situation walks in that you did not enumerate, the agent has nothing. It either freezes or picks the nearest wrong branch.

A checklist of rules is brittle by construction. It can only handle the world you already imagined. Reality is bigger than your list, and it always will be.

[IMAGE: dark canvas, a sprawling tangled decision tree labeled "rules" with dozens of branching if/then nodes, several branches dead-ending into a red question mark labeled "case you didn't list"]

![[principles-over-rules-brittle-tree.png]]

---

## One principle eats a hundred rules

Here is the contrast that makes it click.

The rule: "never mention pricing in the first sentence of a reply." Narrow. It fixes exactly one symptom you saw once. It says nothing about the next forty awkward replies.

The principle: "if someone is venting, lead with empathy, not a pitch." That one line covers the pricing case, and the feature-request case, and the angry-bug case, and a hundred situations you never wrote down. It does not tell the agent what to type. It tells the agent how to read the room.

That is the move. A rule encodes an answer. A principle encodes the judgment that produces answers.

Source: https://x.com/petradonka/status/2054897826149101588
"Principles beat rules, because rules overfit and principles transfer."

When you swap rules for principles, two things happen at once that feel like they should be a tradeoff and are not. The file gets smaller. The agent gets better. Smaller because one principle replaces a cluster of rules. Better because the instructions stopped being a lookup table the model recites and became a way of thinking the model applies.

---

## Why principles transfer

A principle generalizes because it is compressed judgment, not a stored answer.

Think about what a rule actually is. It is the output of some reasoning you did, with the reasoning thrown away. "Never mention pricing first" is the conclusion. The thing you were actually protecting was "do not make a hurting person feel sold to." You kept the conclusion and deleted the cause, so the agent inherits a fact it cannot extend.

A principle keeps the cause. And the cause is the part that transfers, because the same judgment fires across cases that look nothing alike on the surface.

This is also how you encode taste into a system instead of trying to enumerate it. Taste is not a list of approved outputs. It is a small set of values applied consistently under pressure. You cannot list your way to taste. You can name it.

The test for whether you have written a principle: does it tell the agent how to decide in a case you did not mention? If yes, it is a principle. If it only covers the exact case in front of you, it is a rule wearing a principle's clothes.

---

## How to write one

Rewriting rules into principles is a craft, and it is mostly subtraction.

1. Find the cluster. Three or four rules that are all guarding the same thing. The pricing rule, the no-hard-sell rule, the apologize-first rule are all the same instinct.
2. Name the instinct. Ask what value those rules were protecting. Write that down in one sentence. That sentence is the principle.
3. Describe the thinking, not the action. "Lead with empathy when someone is venting" beats "do not mention pricing first." Describe how to think, not what to do.
4. Keep it short. A principle that runs four sentences is usually two principles, or a principle with a rule smuggled inside it.
5. Delete what it subsumes. This is the step people skip. Once the principle is in, the rules it replaced are dead weight. Cut them. If you leave both, the agent gets a contradiction and the file is no smaller.
6. Merge overlaps. Two principles that fire in the same situations are one principle you have not finished writing yet.

The output of doing this well is counterintuitive. A skill that used to be three pages of cases becomes half a page of values, and it handles more of the world than the long version did.

The Loopy AI class has a video, [[teach-the-agent-to-learn]], that runs this exact move automatically. An outer loop watches corrections roll in and, instead of bolting on a new rule each time, distills the correction into a principle and edits the skill. Same craft, done on a schedule, by the agent itself. This video is the manual version you need to understand first. If you have also watched [[the-one-pattern-rule-for-agents]], this is the same energy applied to instructions instead of code.

---

## Demo

1. Open a real support-reply skill that has grown to thirty-plus bullet rules. Scroll it. Let the length speak.
2. Highlight a cluster: the pricing rule, the no-pitch rule, the apologize-first rule, the do-not-overpromise rule. Four rules, one instinct.
3. Write the principle live: "When someone is frustrated, lead with empathy and understanding before anything else. Never make a hurting user feel sold to."
4. Delete the four rules it replaced. Watch the file shrink in real time.
5. Run both versions against three messages the skill was never written for: a sarcastic tweet, a confused beginner, a furious churn threat. Show the rule version reaching for the wrong branch and the principle version reading each one correctly.
6. Count the lines before and after. Smaller file, broader coverage. That is the whole claim, demonstrated.

---

## Key Insight

> A rule stores an answer and breaks on the next new case. A principle stores the judgment that produces answers, so it covers cases you never imagined. Describe how to think, not what to do.

---

Stop trying to enumerate the world. You will lose, because the world is bigger than your list and it keeps adding cases.

Name the handful of values you actually want the agent to hold, write them as principles, and delete the rules they replace. The file gets shorter, the agent gets sharper, and the next unseen situation stops being a crisis.
