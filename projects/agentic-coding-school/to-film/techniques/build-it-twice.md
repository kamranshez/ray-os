---
duration: "10-14 min"
batch: 1
order: 2
batch_name: "The First Build Is a Prototype"
class: "techniques"
chapter: "The First Build Is a Prototype"
---

## The Cheapest Spec Is a Finished Build

Here is the idea this whole video turns on. The most accurate spec you will ever have for a feature is the feature itself, built once and thrown away.

That sounds wasteful. It used to be. Building was the expensive part, so you front-loaded all your thinking into a plan, a doc, a Figma, and you protected that plan because rebuilding cost weeks.

Tokens broke that math. The thing that used to take three days now takes an hour, and most of that hour is the agent's, not yours. So the smart move is no longer to plan harder before you build. It is to build the whole thing cheaply, learn everything it teaches you, and then ask one question:

**Given everything we now know, how would we build this from scratch?**

Then you build it again. Properly this time. The first build was never the product. It was the highest-fidelity prototype you have ever had.

---

## You Know the Least at the Start

Think about when you write the plan. It is the very first thing you do. Before you have touched the data, before you have hit the edge cases, before the API surprised you, before you found out the "simple" part was the hard part.

So your plan is written at the exact moment you understand the problem worst.

[IMAGE: dark chalkboard, a rising "understanding" curve over a time axis, a pin labeled "you write the plan" sitting at the lowest point on the left, a pin labeled "you actually understand it" near the top on the right]

![[images/build-it-twice/knowledge-curve.png]]

Every decision in that plan is a guess made from the bottom of the curve. Which abstraction to use. Where the boundaries go. What the data model should be. You are choosing all of it while you know almost nothing.

And then you spend the next however-long defending those guesses, because the cost of changing them felt high. That is the trap. You let your dumbest version of the project lock in the architecture.

---

## Building Is How You Buy Knowledge

Here is the reframe. When you build the throwaway version, you are not spending tokens to get code. You are spending tokens to buy information.

Building forces every hidden decision into the open. A plan lets you stay vague about the part you do not understand yet. A build does not. The agent has to actually wire the thing together, and the moment it does, every soft assumption becomes a hard fact you can see and react to.

You learn more in the first hour of building than in a week of planning. Not because planning is useless, but because planning happens in your head, where the hard parts can hide. Building drags them onto the screen.

[IMAGE: dark chalkboard, two stacked bars labeled "1 week of planning" (short, thin understanding) and "1 hour of building" (tall, full understanding), arrow showing build buys more knowledge per unit time]

![[images/build-it-twice/build-buys-knowledge.png]]

So the cost question flips. A token costs a fraction of a cent. An hour of agent build time costs you almost nothing. A wrong abstraction shipped to production costs you months. When the cheap thing buys down the expensive risk, you do the cheap thing twice.

---

## This Is Not New. It Just Got Fast.

Good engineering teams have always done a version of this. They just called it a quarter.

Before AI, a team would spend three or four months shipping a feature, watch it meet the real world, and then say "okay, now that we actually understand this, here is how we should have built it." The rewrite was almost always better, cleaner, and faster than the original. Everyone knew the second system was the good one.

Fred Brooks wrote this down fifty years ago.

Source: https://en.wikipedia.org/wiki/The_Mythical_Man-Month

> Plan to throw one away. You will, anyhow.

Shopify built this into how they operate. They rewrote the entire Admin, then later the whole storefront engine, from scratch, because they hold that any decision must be open to challenge at any time. Their own engineering team states the principle plainly, borrowing from Martin Fowler:

Source: https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity

> The best time to refactor and re-architect is as late as possible, as you are constantly learning more about your system and business domain as you build.

The only thing that has changed is the clock. The build-then-rebuild loop used to run on a scale of quarters, so most teams only ever got to run it once. Now it runs on a scale of days. You can do deliberately, in an afternoon, what used to happen by accident over a fiscal year.

[IMAGE: dark chalkboard, two horizontal timelines stacked. Top labeled "Before AI": a long bar "build (3 to 4 months)" then a long bar "rewrite". Bottom labeled "Now": a tiny bar "build (1 day, throwaway)" then a bar "rebuild", same loop compressed]

![[images/build-it-twice/timeline-compression.png]]

So stop treating the rebuild as a failure you are trying to avoid. It is the part where the real engineering happens. The first pass just earns you the right to do it well.

---

## Reset. Do Not Refactor.

This is the part people get wrong, so be precise about it.

When you go to build version two, do not open version one and start cleaning it up. That is refactoring, and refactoring inherits everything. It inherits the wrong abstraction you picked at the bottom of the knowledge curve. It inherits the dead ends, the workarounds, the scar tissue from decisions you made when you knew nothing.

A clean rebuild inherits only the learnings.

[IMAGE: dark chalkboard, two paths from a tangled box labeled "prototype". Top path "refactor" arrives at a still-tangled box carrying the same knots. Bottom path "reset" passes through a filter labeled "keep the learnings, drop the code" and arrives at a clean box]

![[images/build-it-twice/reset-vs-refactor.png]]

So you do not hand the agent the old code. You hand it the knowledge. You write down what you learned: the real data model, the edge cases that bit you, the boundary that turned out to be in the wrong place, the part that was secretly simple and the part that was secretly hard. Then you start a fresh build from that.

The prototype's job was to generate that list. Once you have the list, the prototype has done its job, and keeping it around just drags its mistakes into the future.

This is the same instinct behind starting a clean v2 branch instead of grinding on the original. The code is cheap. The learnings are the asset.

---

## Demo

Let me show the full loop on a real feature.

1. Take a feature with real uncertainty, say an integration that pulls data from a third-party API and reshapes it. The kind of thing where you do not actually know the right data model until you have seen the responses.
2. Build the whole thing in one pass with the agent. No careful planning. Tell it to get to something working end to end as fast as possible. Let it make rough choices.
3. Use it. Hit the edge cases. Watch where it breaks, where the abstraction fights you, where the "simple" part turned out to be three special cases in a trench coat.
4. Open a fresh chat and write the learnings file. Not the code. Just what the build taught you: the real shape of the data, the boundaries that moved, the decisions you would now make differently.
5. Ask the question: "Given everything in this learnings file, how would we build this from scratch?" Let the agent propose the clean architecture, informed by the trench it just climbed out of.
6. Build version two against that. Then delete the prototype.

Show both side by side at the end. Version two is smaller, clearer, and it handles the cases version one discovered. That is not luck. That is the knowledge gradient paying out.

---

## Where This Goes Wrong

Two failure modes, so the video is not naive about it.

You do not build everything twice. You build the uncertain things twice. If you already know the exact shape of what you are making, the prototype teaches you nothing and you just paid twice for the same answer. Reserve this for the parts where you genuinely do not know the right design yet.

And the reset has to be real. If you "rebuild" by quietly pasting the old code in as a reference, you have not reset, you have refactored with extra steps, and version two will be version one wearing a clean shirt. Feed the learnings. Withhold the code.

---

## Key Insight

> Your first build is not the product. It is the most honest spec you will ever get, written by reality instead of by you at the moment you understood the problem least. Spend cheap tokens to learn the real shape of the thing, then rebuild it from the learnings, not the leftovers.

---

You used to get one shot at the architecture, taken when you knew the least. Now you get to take the shot, see where it lands, and take it again from the spot you actually wanted to stand. Build it once to learn it. Build it twice to keep it.
