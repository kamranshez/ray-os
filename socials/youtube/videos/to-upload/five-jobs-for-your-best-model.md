---
tags: [youtube, script, claude-code]
date: 2026-07-01
youtube-title: "Five Jobs Worth Your Best Model"
duration: "10-14 min"
status: draft
---

## Access Was Never the Point

Here is the idea this whole video turns on. The moment your best model is rationed, getting access to it stops being the skill. Knowing the handful of jobs actually worth spending it on becomes the skill.

Watch what just happened. The most capable model came back, and it came back metered. A slice of your weekly usage, then you are paying credits. And buried in the announcement was the real tell: some routine coding and debugging now falls back to a cheaper model.

Read that again. They did not split the work by task type, cheap model for writing and expensive model for thinking. They split coding itself straight down the middle by difficulty. The routine half drops to the cheaper model. The hard half stays on the expensive one.

That is the entire lesson, and the model maker is already doing it to you inside the product. So the only question left is which jobs deserve your most expensive model. It turns out there are about five.

[IMAGE: dark background, a usage meter ticking up and slamming into a red weekly cap on the left, and on the right a stack of model tiers from a wide cheap band at the bottom to a thin glowing gold band at the top labeled "the expensive one"]

![[five-jobs-rationed-tiers-1.png]]
![[five-jobs-rationed-tiers-2.png]]
![[five-jobs-rationed-tiers-3.png]]
![[five-jobs-rationed-tiers-4.png]]
![[five-jobs-rationed-tiers-5.png]]

---

## Two Ways You Waste It

You waste a rationed model in two opposite directions, and most people manage to do both.

The first is overspending. You point your scarcest model at work a cheap one handles perfectly. Copy changes. Boilerplate. A self-contained feature nothing else depends on. You just burned premium budget on a job Haiku would have nailed.

The second is underspending, and it is quieter. There are a few jobs where the expensive model is the only thing that actually works, and you skip it. You let a cheap model design your auth flow, it hands you something that looks reasonable, and you ship a decision you will be unwinding for a year.

The fix for both is one question you ask before you spend anything.

**Would a cheap model get this wrong, or only just good enough?**

If the honest answer is yes, this is a job for your best model. If the answer is no, it never was. Every idea in the rest of this video is a category of work where the answer is yes.

[IMAGE: dark background, a single decision gate in the center labeled "would a cheap model get this wrong?", with a wide arrow flowing left to a cheap model and a thin gold arrow flowing right to the expensive one]

![[five-jobs-the-test-1.png]]
![[five-jobs-the-test-2.png]]
![[five-jobs-the-test-3.png]]
![[five-jobs-the-test-4.png]]
![[five-jobs-the-test-5.png]]

---

## Job One: The Golden Reference

Start here, because it changes how you think about the other four.

Models are much better at writing new code than at renovating old code. And they get better still when you hand them an example to copy. So the highest leverage thing you can do with your best model is not to make it grind through your whole codebase. It is to make it build one thing, once, to a very high bar.

One canonical implementation. The reference endpoint. The reference component. The one service module that does everything right, the way you wish the whole codebase looked.

Then you hand that reference to your cheap models and point at it. Make the other forty look like this one. You have converted an open ended instruction, do this well, into a closed one, match this. Cheap models are reliable at matching. They are unreliable at judgment. So you spent the judgment once, at the top, and turned it into a template the cheap tier copies for free.

One expensive run. A pattern the rest of your stack replicates indefinitely.

[IMAGE: dark background, one glowing gold "reference" block at the top, arrows fanning down to many plain grey blocks that each mirror its shape, labeled "cheap models pattern-match"]

![[five-jobs-golden-reference-1.png]]
![[five-jobs-golden-reference-2.png]]
![[five-jobs-golden-reference-3.png]]
![[five-jobs-golden-reference-4.png]]
![[five-jobs-golden-reference-5.png]]

---

## Job Two: A Routing Map In Your CLAUDE.md

Once you accept that different jobs want different models, the obvious next move is to stop deciding it in your head every single time.

Because it is not even a two-way choice. Updating copy is a Haiku job. A small isolated feature is a Sonnet or an Opus job. The load-bearing core is the only place the expensive model earns its keep. And the thing that decides which tier a piece of code belongs to is its blast radius. How many things depend on it. How far a change ripples.

Low blast radius, get it wrong and you fix a typo. High blast radius, get it wrong and it breaks everything downstream.

So you build a map, and you write it into your CLAUDE.md, in the one file the agent reads every session.

```
# Model routing
- copy, docs, marketing        -> Haiku / Sonnet
- isolated features            -> Opus
- high blast radius            -> the expensive model
  (auth, payments, schema, shared API layer)
```

Two things make this better than it looks.

It is cheap to build. Blast radius is knowable without ever touching your expensive model. How many files import this, how many things break if it changes. A cheap model, or a one line dependency count, draws the whole map. You never spend your scarce model figuring out where to spend it.

And it shrinks itself. When you do spend an expensive run cleaning up a high blast zone and making it properly isolated, its blast radius drops, and it graduates down a tier. The map is also your cleanup backlog. A clean codebase is one where the expensive column is nearly empty. That is the goal.

This is the same instinct security researchers use when they rank a codebase before spending on it, and the same one the model makers now bake into their own routing.

Source: https://securitycryptographywhatever.com/2026/03/25/ai-bug-finding/
Source: https://red.anthropic.com/2026/mythos-preview/

[IMAGE: dark background, a codebase drawn as regions on a map, each region tinted by tier from pale grey to glowing gold, with a small CLAUDE.md file card in the corner holding the routing table]

![[five-jobs-routing-map-1.png]]
![[five-jobs-routing-map-2.png]]
![[five-jobs-routing-map-3.png]]
![[five-jobs-routing-map-4.png]]
![[five-jobs-routing-map-5.png]]

---

## Job Three: The Cross-Cutting Refactor

Now pick a high blast zone off that map and actually work in it.

A wide refactor has a trap. The typing is cheap and the knowing what breaks is expensive. A cheap model does the forty obvious edits perfectly and misses the three that matter, because it works file by file and loses the whole picture.

So you split the job the same way the model maker split coding.

Your best model builds the blast radius map. Given the change, it traces every place it reaches, including the ones nobody sees. The raw SQL string. The serialized blob another service reads. The analytics event contract. The test that silently encodes an assumption. Then it hands back a plan. What changes, in what order, and the two or three spots that will break in silence.

Your cheap models execute the edits against that plan.

Picture renaming a database column. The rename in code is nothing. But it lives in the ORM, in a raw query, in a JSON field the frontend reads, in an analytics event, in a cached object, in a downstream pipeline. The reasoning is the migration order and the contracts that break quietly. That is the expensive part. The thirty mechanical edits are not.

Notice the plan it produces is just another reference, the same as Job One, except this one describes a change instead of a component.

[IMAGE: dark background, one change at the center rippling outward to a dozen connected files, three of them flagged red as "breaks silently", with a gold overlay labeled "the map"]

![[five-jobs-blast-radius-1.png]]
![[five-jobs-blast-radius-2.png]]
![[five-jobs-blast-radius-3.png]]
![[five-jobs-blast-radius-4.png]]
![[five-jobs-blast-radius-5.png]]

---

## Job Four: The Irreversible Decision

Some choices you make once and live inside forever.

Auth and OAuth flows. The database schema. A public API contract. A migration strategy. These are one-way doors. A cheap model will pick a locally reasonable option and move on, and you will not feel the cost today. You feel it in a year, when the wrong shape has calcified and everything is built on top of it.

This is exactly what the expensive model is for. Its edge is reasoning many steps ahead, holding a dozen constraints at once, and seeing the consequence three moves out that the cheap model never simulated. On a throwaway function that does not matter. On the decision that everything hangs off, it is the whole game.

So the rule is simple. If the decision is expensive to unwind, it does not go to the cheap tier, no matter how small the code looks. The code for an auth flow is not much. The decision is enormous.

[IMAGE: dark background, a path arriving at a fork, one branch is an ordinary open door, the other is a heavy one-way door labeled "expensive to unwind" that clicks shut behind you]

![[five-jobs-one-way-door-1.png]]
![[five-jobs-one-way-door-2.png]]
![[five-jobs-one-way-door-3.png]]
![[five-jobs-one-way-door-4.png]]
![[five-jobs-one-way-door-5.png]]

---

## Job Five: Red-Team Your Own Design

Job Four has a natural partner, and you run them back to back.

You made the big decision. Before you commit to it, you spend a second expensive run trying to break it. Not to write more code. To attack the plan. How does this fail. What happens at ten times the scale. Where is the security hole. What did I quietly assume that is not true.

This is a job cheap models cannot do, and the failure is specific. A cheap model rubber-stamps. Ask it if your design is sound and it agrees, warmly. Real adversarial foresight needs depth, because the failure modes that actually hurt you are the non-obvious ones, the interaction between two systems that each look fine alone.

Design with your best model. Then attack the design with your best model. The cheapest bug is the one you kill on the whiteboard, before a single cheap model has written a line against a plan that was broken from the start.

[IMAGE: dark background, a design sketch in the center being hit by inbound arrows labeled "scale", "security", "hidden assumption", with a commit gate on the right that only opens once the design survives]

![[five-jobs-red-team-1.png]]
![[five-jobs-red-team-2.png]]
![[five-jobs-red-team-3.png]]
![[five-jobs-red-team-4.png]]
![[five-jobs-red-team-5.png]]

---

## A Better Harness Beats A Bigger Model

Here is the move that sits above all five, and it is the one to reach for first.

Before you spend the expensive model on any job, ask a prior question. Could a cheaper model, wrapped in a better harness, get there instead?

Raw model intelligence is only one of the two inputs. The scaffold around the model is the other, and it is the one you fully control. A cheap model on its own gets one guess. The same cheap model inside a loop can produce, get critiqued, and fix, over and over, until the work is actually good.

Here is one I run. My design had drifted out of consistency, the kind of thing that happens when twenty components get built at different times. Spacing off, colors slightly wrong, patterns that no longer match. The obvious move is to throw the expensive model at it. I do not. Instead I run a harness with two cheap roles that go back and forth. A builder makes a pass at fixing the inconsistencies. Then an adversarial reviewer, whose only job is to hunt for what is still off, tears the result apart. The builder fixes what the reviewer found. They loop, up to three rounds. By the third pass the reviewer runs out of real complaints, and the design is consistent, without a single expensive call.

Look at what the loop is doing. The adversarial reviewer is manufacturing the judgment you would have paid the expensive model for. One cheap model producing and one cheap model attacking, on repeat, closes most of the gap to a single expensive pass. On plenty of tasks it closes all of it.

Dynamic workflows are the sharpest version of this. The pipeline decides at runtime how many rounds to run, how many agents to spawn, and when it is genuinely stuck. That last part matters most. It escalates to the expensive model only on the specific pieces the cheap loop could not resolve. Escalation becomes a fallback triggered by failure, not a default you reach for out of habit.

So the routing map from Job Two quietly gains a third column. Not just which model, but which model in which harness. The expensive tier stops being where you start. It becomes where you end up only when a well-built cheap loop has genuinely run out of room.

This is the whole point restated. The goal was never to use your best model more. It was to need it less. A good harness is how you get there.

[IMAGE: dark background, a loop between two grey blocks labeled "builder" and "adversarial reviewer" with a circular arrow marked "up to 3 rounds", the output flowing right to a green "consistent" check, and a thin dashed arrow escaping upward to a small gold "expensive model" block labeled "only if the loop gets stuck"]

![[five-jobs-harness-loop-1.png]]
![[five-jobs-harness-loop-2.png]]
![[five-jobs-harness-loop-3.png]]
![[five-jobs-harness-loop-4.png]]
![[five-jobs-harness-loop-5.png]]

---

## Demo

I will run the whole loop on my own course funnel, and the point to notice is how little of it actually touches the expensive model.

1. Open the codebase. Run a one line dependency count across the modules to get a rough blast radius for each. `paywall` and `entitlements` are imported everywhere. The legal pages are imported nowhere.
2. Hand that to a cheap model and have it draft the routing table. Copy to Haiku, isolated UI to Opus, `auth`, `payments`, and `schema` to the expensive tier. Write the table straight into CLAUDE.md.
3. Take the top blast radius zone, entitlements, and spend one expensive run on the golden reference: the entitlement state machine, the failure matrix for declined cards, refunds, and expired subscriptions, and the acceptance tests. Small, expensive, load bearing.
4. Hand that reference to a cheap model and let it build the surrounding React component against it. It matches the pattern. It does not have to invent it.
5. Take a rename that spans the whole repo. Expensive model produces the blast radius map and the migration order. Cheap models execute the thirty edits.
6. Before committing the auth change, one expensive red-team pass against it. It finds the refresh-token edge case. You fix it on paper, not in production.
7. The pricing components had drifted out of visual consistency. I do not open the expensive model for it. I run the builder and adversarial reviewer loop, three rounds, and the spacing, colors, and patterns snap back into line on the cheap tier alone.

One map, one reference, one refactor plan, one red-team, and a whole design cleanup that never needed the expensive model at all. Everything else in that session ran on the cheap tier.

---

## Key Insight

> When your best model is rationed, the skill is not access, it is aim. Spend it only where a cheap model would be wrong, not merely slower: the reference others copy, the map that routes the rest, the change whose danger is the implications, the decision you cannot unwind, and the attack that kills a bad plan early.

---

## What Changes For You

You stop treating your most capable model like a faster version of the cheap one. You start treating it like a scarce specialist you call in for five specific jobs and nothing else.

Build the routing map this week, on the cheap models, and write it into your CLAUDE.md. Then the next time the expensive model is in front of you and the clock is running, there is no deciding. You already know the five things worth pointing it at.

And the sessions you will be proudest of are the ones where a good harness meant you never had to.
