---
class: "prompt-engineering"
chapter: "Core Techniques"
status: "scripted"
---
Asking for options with a recommendation is a single move that changes how you make decisions with a model. Instead of "give me the answer," you ask for a few genuinely different answers and have the model flag the one it would pick, with its reasoning. You walk away with the menu *and* a default.

### The Problem With Asking For "The Answer"

When you ask a model for one answer, you get one path and lose every path it considered on the way there.

Think about what actually happens inside the model. It weighs naming conventions, architectures, opening lines, positioning angles. It branches, compares, discards. Then it collapses all of that into a single output and hands you the survivor. The branches it rejected, the tradeoffs it weighed, the second-best idea that might have been better for *your* situation, all of it gets thrown away before it reaches you.

So you're left with two bad options. Accept the single answer blindly and hope it fits. Or reject it and relitigate the whole thing from a blank page, re-explaining everything you wanted in the first place.

Both are wasteful. The model already did the work of exploring the decision space. You just never got to see it.

### The Move: Options Plus A Default

The fix is one sentence longer than your normal prompt.

> "Give me three genuinely different options for X. Tell me which one you'd recommend and why."

That's it. You've asked for two things at once: breadth and a pick. The three options surface the decision space the model would otherwise have hidden. The recommendation gives you a default so you're not paralyzed by the menu.

You're no longer an author staring at a blank page. You're a chooser reacting to concrete proposals. And reacting is always easier than generating. You can look at three real naming schemes and instantly feel which one is right far faster than you could invent one from nothing.

The recommendation matters as much as the options. Without it, you've just shifted the work onto yourself, three things to evaluate instead of one to accept. With it, you get a clear default you can take in one second when you don't care, and a real spread you can override when you do.

[IMAGE: dark canvas, a single node fanning out into three distinct branches labeled Option A, Option B, Option C; one branch (B) drawn bolder with a star and the word "recommended", the other two lighter]

![[images/options-with-a-recommendation/the-fan.png]]

### Why It Beats A Single Answer

Three things are happening under the hood.

**It fights the crowded center.** Remember steering distributions. A single answer lands you on the statistical center of mass, the most consensus response. When you force three *distinct* options, option one is usually that crowded center, but options two and three push the model off-center into territory it would never have shown you otherwise. The variety requirement is a distribution-spreading instruction in disguise.

**It forces commitment.** Asking the model to recommend one is the same trick as the enum from structured output. It can't hedge with "it depends" or "both are valid." It has to commit to a pick and defend it. That commitment is where the real signal lives, because a model that has to choose reveals its actual judgment instead of safe fence-sitting.

**It externalizes the tradeoffs.** When the model explains why it recommends option two over options one and three, it's handing you the comparison it ran internally. Now you can see the axis the decision turns on. Maybe you disagree with how it weighted that axis, and now you can say so, precisely, instead of vaguely feeling that the single answer was off.

### How To Do It Well

The move is simple. Doing it well takes a few specifics.

**Name the count.** Three is the sweet spot. Two isn't a real choice, it's a coin flip. Five or more turns into noise you have to wade through. Ask for three unless you have a reason not to.

**Demand a real axis of difference.** The most common failure is three options that are the same idea in slightly different clothes. Kill that by naming the axis: "three options that differ in how aggressive the tone is," "three architectures that trade off differently between simplicity and scale." Now the options have to actually spread.

**Require a one-line rationale per option.** Not just the option, but the case for it. This is chain of thought applied per branch. It makes each option self-justifying so you can evaluate without re-deriving why it might be good.

**Make it state its criteria.** Either tell it what to optimize for ("recommend the one that's easiest to maintain"), or ask it to tell you what it optimized for. Half of disagreements with a recommendation are really disagreements about the criteria, and surfacing the criteria resolves them instantly.

**Optionally, give it a shape.** A small table, or a JSON array with a `recommended: true` flag, makes the output scannable and lets you feed it straight into the next step. This is structured output doing its job.

### The Failure Modes

Three things go wrong, and each has a clean fix.

**Fake variety.** The three options are near-identical. Fix: name the axis they must differ on, as above. If they still cluster, ask explicitly for "one safe option, one bold option, one weird option."

**The recommendation is always option one.** Models anchor on the first thing they generate. Fix: ask it to argue *against* its own pick, or to name the single condition under which it would switch recommendations. If it can't mount a real argument against its choice, the choice was lazy.

**Menu paralysis.** Too many options, and you're back to doing all the work yourself. Fix: keep it to three, and lean on the recommendation as your default. The whole point is that you can ignore the menu when you don't care.

### When To Reach For It

This move earns its keep on decisions that branch and matter: architecture calls, naming, positioning, copy direction, how to structure a feature, which approach to take on a hard problem. Anywhere there's genuinely more than one good answer and the choice has consequences.

Skip it when there's one correct answer. You don't ask for three options on "what's the syntax for a Python list comprehension." You ask for it when the model's first instinct might be the consensus default and you suspect the better answer for *you* is off-center.

It also pairs naturally with iterative refinement. Get three options, pick one, then refine that one. You've used the options to find the right starting point, which is exactly the hard part that refinement alone doesn't solve.

### Demo

1. Ask for a single product name in the normal way, then ask for "three product names that differ in how playful vs. serious they are, and tell me which you'd recommend and why." Compare what you get.
2. Show the distribution effect: point out that option one is the obvious consensus name, and options two and three are the ones you'd never have generated yourself.
3. Add the structured shape: request a markdown table with columns for the option, its one-line case, and a recommended flag.
4. Trigger the anchoring failure on purpose, then fix it by asking the model to argue against its own recommendation and name when it would switch.
5. Chain into refinement: take the recommended option and refine it in two passes, showing how options-then-refine beats refining a single first answer.

### Key Insight

> When you ask a model for one answer, it explores the decision space and then throws the map away, handing you only the destination. Asking for a few distinct options with a recommendation gives you the map back. You get breadth from the options, a default from the recommendation, and the actual tradeoffs from its reasoning. You stay the decider, but you're choosing between concrete proposals instead of authoring from a blank page, and choosing is always the cheaper, sharper act.

You stop accepting the model's first instinct and start seeing what it was choosing between. That single extra sentence turns the model from an oracle that hands down answers into an advisor that lays out your options and tells you where it stands.
