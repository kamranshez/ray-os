---
class: "prompt-engineering"
chapter: "Aligning to Your Intent"
status: "scripted"
---

## Intent Beats Instruction

Here is the whole video in one line: tell the agent **why**, not just **how**, and the why will shape the how for you.

Most people prompt by listing steps. Do this, then this, use this library, put it here. You are trying to specify every decision up front. But you can't. There are a hundred small decisions inside any real task that you never thought to mention, and the agent is going to make every one of them whether you guided it or not.

When you only give instructions, the agent fills those gaps with whatever it guesses you meant. When you give intent, it fills those gaps with what you actually wanted.

That is the difference between a prompt that does the thing and a prompt that does the right thing.

---

## Watch It Break

Let me show you the failure, because it is subtle and it will bite you in production.

Same task, two prompts.

**Prompt one, pure instruction:**

> Add a 30 second cache to this pricing endpoint.

The agent does exactly that. It wraps the whole response in a 30 second cache. Clean code, passes the build, looks done.

Except this endpoint returns two things: a price that changes hourly, and a "spots remaining" counter that has to be live. You just cached the live counter. Now it shows "3 spots left" for 30 seconds after they sell out. The agent did precisely what you said, and it shipped a bug.

**Prompt two, same task, but with the why:**

> This pricing endpoint gets hammered on our landing page and it is expensive to compute. The price only changes once an hour, so it is safe to serve a slightly stale price. Make it cheap to call.

Now watch what the agent does that you never asked for. It notices the response has more than one field. It reasons that "safe to serve stale" applies to the price but not to anything real-time. It caches the price and leaves the counter live. Some agents will even split the endpoint or add a short ttl on the volatile field.

You did not tell it which field to cache. You told it why you were caching. The why carried the decision.

[IMAGE: dark background, one task box on the left, two arrows out. Top arrow labeled "instruction: cache the endpoint" leads to a single rigid path ending in a red broken field. Bottom arrow labeled "intent: it is safe to serve a stale price" fans into the agent choosing the right path, ending in green. Same task, two outcomes.]

![[intent-engineering-instruction-vs-intent-1.png]]
![[intent-engineering-instruction-vs-intent-2.png]]
![[intent-engineering-instruction-vs-intent-3.png]]
![[intent-engineering-instruction-vs-intent-4.png]]
![[intent-engineering-instruction-vs-intent-5.png]]

This is the front half of an idea we cover later in **Don't Verify Against the Plan**. There, the lesson is that your plan is full of disposable implementation detail and one piece of durable intent, and you should verify against the intent, not the detail. Same coin. Here we are learning to write that durable intent in the first place. There we learn to hold the agent to it.

---

## The Why-Statement

"Give it the why" is a nice sentence and a useless instruction on its own. So here is the actual artifact. Four parts. Write these and you have a why-statement.

**1. Why this exists.** The user or business problem behind the task. Not the feature, the reason for the feature. "Support keeps getting tickets because users can't tell which plan they are on." That sentence does more work than three paragraphs of specs.

**2. What done looks like.** The success condition, stated so a machine could check it. "Done means a logged-in user sees their current plan name on the billing page without clicking anything." This is the part that later becomes your verification. If you can't write it, you don't know what you are asking for yet.

**3. Hard constraints.** The things that must never break, no matter how the agent solves it. Regulatory, performance, data integrity. "Never log card numbers. The page must render under 200 milliseconds. Never write to the production billing table from this flow." These are non-negotiable and you say so.

**4. What is negotiable.** The part everyone forgets, and the part that stops the agent gold-plating. "I don't care which charting library you use. The exact wording is up to you. Don't build settings for this, one hardcoded value is fine." You are handing the agent permission to make cheap choices cheaply, so it spends its effort where it matters.

[IMAGE: dark background, a four-panel grid titled "The Why-Statement". Top-left "Why this exists" with a small person-and-problem icon. Top-right "What done looks like" with a checkmark. Bottom-left "Hard constraints" with a lock. Bottom-right "What's negotiable" with an open hand. Clean, screenshot-friendly, like a reference card.]

![[intent-engineering-why-statement-frame-1.png]]
![[intent-engineering-why-statement-frame-2.png]]
![[intent-engineering-why-statement-frame-3.png]]
![[intent-engineering-why-statement-frame-4.png]]
![[intent-engineering-why-statement-frame-5.png]]

A quick note so you don't confuse this with **Prompt Contracts**. A contract pins down the *what* for one specific task and you approve it before building. A why-statement pins down the *why*, and unlike the contract, it is meant to outlive the task. More on that in a second.

---

## Why The Why Works

You don't need the math to use this, but the mechanism is worth thirty seconds because it tells you when intent matters most.

The model is always filling gaps with priors. Every place you were vague, it reaches for the most statistically likely interpretation given everything else in context. Left alone, "add a cache" reaches for the most generic cache pattern it has ever seen. That is the prior.

The why redirects which prior it reaches for. "Safe to serve a stale price" pulls the model toward a completely different region of solutions than "cache the endpoint," before it writes a single line.

Think back to the slot-machine problem from **Why Search Isn't Enough**. Same prompt, run it five times, sometimes a great plan, sometimes a terrible one, because the model is sampling from a wide space of interpretations. Intent narrows that space *before* the sampling happens. You are not getting luckier. You are giving the model less room to be wrong.

So the rule of thumb: the more interpretation a task allows, the more the why is worth. Tiny mechanical edit, skip it. Anything with judgment in it, lead with the why.

---

## Where The Why Has To Live

Here is the mistake that wastes a good why-statement. You write a beautiful one, paste it into a single prompt, the agent nails the task, and then you hit `/clear` or the context fills up and you start fresh. The why is gone. The next session is back to guessing.

Intent is not a one-off prompt. It is **durable context**. So it belongs in the two places that survive a reset.

**The spec or plan file.** Put the why-statement at the top of the plan, above the steps. Every fresh session that reads the plan inherits the intent, not just the task list. When you start a new context window and point it at the plan, the why comes with it.

**The layer node.** For intent that is true across the whole project, not just one task, it goes in your CLAUDE.md or AGENTS.md. "We optimize for read latency over write latency, this is a read-heavy product." "We never break the public API, mobile clients lag releases by weeks." That is project-level why. Written once, it shapes every decision the agent makes in that directory forever, and it survives every reset because it reloads on every session.

[IMAGE: dark background, left side shows a single prompt bubble with a why-statement inside, then a "/clear" guillotine, and the bubble is gone. Right side shows the same why-statement written into a "spec header" file and a "CLAUDE.md" layer node, with arrows looping back into three fresh sessions, persisting. Caption feel: ephemeral vs durable.]

![[intent-engineering-where-why-lives-1.png]]
![[intent-engineering-where-why-lives-2.png]]
![[intent-engineering-where-why-lives-3.png]]
![[intent-engineering-where-why-lives-4.png]]
![[intent-engineering-where-why-lives-5.png]]

A one-off prompt is a sticky note. The spec header and the layer node are the contract on the wall. Put the why where the agent will read it again tomorrow.

---

## Get Over The Cringe

One honest barrier. Writing "we are building this because users feel anxious when they can't find their plan" to a machine feels ridiculous. You feel like you are talking to a person who isn't there.

Do it anyway, because it measurably works. This is not just my opinion. Anthropic's own prompting guidance for Opus 4.8 tells you to give the model context for why you are doing something, and that it will do a better job when you do.

Source: Anthropic prompting documentation for Claude Opus 4.8

If you come from a non-technical background, this is your superpower, not your handicap. You don't have to know how to specify the implementation. You are the only one who knows why the thing should exist. That is exactly the input the model wants most. You are not the coder here. You are the product manager, and the product manager's whole job is owning the why.

---

## Demo

Here is what the camera shows, end to end.

1. Start in a real repo with a pricing endpoint that returns a hourly price and a live "spots remaining" counter.
2. Run the instruction-only prompt: "Add a 30 second cache to this endpoint." Let it finish. Open the endpoint in the browser, sell out the last spot, and watch the counter sit on "3 spots left" for 30 stale seconds. Bug shipped.
3. Reset. Run the intent version: "This endpoint is hammered and expensive, the price only changes hourly so a stale price is fine, make it cheap to call." Show the agent caching the price and leaving the counter live, with no extra instruction from me.
4. Pull up the four-part why-statement frame on screen and write one live for a second, messier task, filling each box out loud: why it exists, what done means, hard constraints, what's negotiable.
5. Lift that why-statement out of the prompt and paste it into the top of the plan file. Then add the one project-level line to CLAUDE.md.
6. Run `/clear`, start a completely fresh session, point it at the plan, and show the agent making the same intent-aligned choice it made in step 3, with zero context carried by hand. The why persisted.

---

## Key Insight

> Instructions tell the agent what to do. Intent tells it what you would have decided, in all the moments you weren't there to decide.

---

Stop writing longer instruction lists. Start writing shorter, sharper why-statements, and put them where the agent will read them again. You will specify less and get more, because the model is finally making your decisions instead of guessing at them.
