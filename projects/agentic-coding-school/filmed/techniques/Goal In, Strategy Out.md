---
status: filmed
---

Most engineers approach AI the same way they'd brief a junior developer: "Here's the problem, here's how I'd solve it, now go implement my solution." They describe the procedure. Step one, do this. Step two, do that. Use this library. Structure it this way.

It works. But it leaves performance on the table.

The better move: **describe the goal and the constraints, then ask the model for its recommended approach.** Don't hand it a procedure — hand it a problem. Let it propose the architecture, the patterns, the tradeoffs. Then pick the one you like best.

This works because models have seen millions of codebases, thousands of architectural patterns, and every common (and uncommon) way to solve most problems. When you prescribe the procedure, you're capping the solution at what *you* know. When you describe the goal, you're tapping into what the *model* has seen — which, for implementation patterns, is almost certainly broader than any single engineer's experience.

![[images/goal-in-strategy-out-intro.png]]

---

## Why engineers get this backwards

Experienced engineers are the most likely to fall into this trap, and it's precisely *because* they're experienced.

When a senior engineer sees a problem, they immediately see a solution path. Years of pattern matching fire instantly. They know how they'd build it. So when they prompt an AI, they describe that path — not the destination.

This made sense with older, weaker models. GPT-3 needed hand-holding. Early Copilot needed precise leading context. You had to steer hard or the output was garbage.

But models have gotten dramatically better at reasoning about architecture, weighing tradeoffs, and proposing solutions — often across a wider range of patterns than any one person has encountered. The habit of prescribing procedure hasn't caught up with that reality. People are still driving manual when the car has an autopilot that knows every road.

![[images/goal-in-strategy-out-why-backwards.png]]

---

## What this looks like in practice

### The procedural way (limited)

> "Build me a rate limiter. Use Redis with a sorted set. On each request, add the timestamp, remove entries older than the window, check the count. Use a Lua script for atomicity."

The model will implement exactly this. It's a fine rate limiter. But you've locked out sliding window counters, token bucket algorithms, leaky bucket approaches, or a hybrid that might better fit your actual traffic pattern.

### The goal-oriented way (better)

> "I need rate limiting for an API that handles bursty traffic with occasional sustained spikes. The system uses Redis. Give me three different approaches with tradeoffs, then recommend the one you'd pick for this use case."

Now the model is thinking, not just typing. It'll propose approaches you might not have considered, explain why each one fits or doesn't, and make a recommendation based on the specific constraints you gave it.

### The compounding version (best)

> "I need rate limiting for an API. Here's what matters: bursty traffic, occasional sustained spikes, Redis is available, and we need to be able to adjust limits per-customer without redeployment. Give me your recommended approach and explain why you'd pick it over the alternatives."

You've given it the *problem shape* — the goal plus the constraints that actually matter. The model fills in the implementation strategy. You evaluate the output on whether it solves the real problem, not whether it matches the procedure you had in mind.

![[images/goal-in-strategy-out-practice.png]]

---

## Why this becomes more true over time

This technique has a built-in tailwind: **it gets more valuable as models improve.**

With weaker models, prescribing procedure was sometimes necessary because the model couldn't reliably reason about tradeoffs or propose coherent architectures. You had to think for it.

With stronger models, that procedural scaffolding becomes a ceiling. The model can reason about tradeoffs better than you expected, but only if you give it room to do so. Over-specifying the how is like hiring an expert and then reading them a script.

This is the same dynamic described in [[Boxing the Model In]] — rigid orchestration constrains the model to your solution path, not the best solution path. Goal In, Strategy Out is the positive framing: instead of avoiding the anti-pattern, actively lean into the model's ability to recommend.


![[images/goal-in-strategy-out-tailwind.png]]

---

## How to do it

**1) State the outcome, not the steps.**
Replace "do X, then Y, then Z" with "I need a system that achieves [outcome] under [constraints]."

**2) Ask for multiple approaches.**
"Give me three options with tradeoffs" forces the model to explore the solution space instead of jumping to the first viable answer. You see the landscape, then choose.

**3) Include the constraints that actually matter.**
Don't just say "build a cache." Say "build a cache for a read-heavy workload where stale data is acceptable for 30 seconds but cache stampedes would be catastrophic." The constraints shape the recommendation. Without them, you get generic advice.

**4) Ask it to recommend.**
"Which approach would you pick and why?" forces the model to commit to a position and justify it. This is where the model's breadth of pattern exposure pays off — it's synthesizing across everything it's seen to make a judgment call.

**5) Then iterate on the recommendation.**
Once you have the model's preferred approach, *now* you can steer. "I like approach B but I'm worried about [specific concern]" is a much more productive conversation than "implement my predetermined solution."

![[images/goal-in-strategy-out-how-to.png]]

---

## The relationship to other techniques

This pairs naturally with [[Boxing the Model In]] (the anti-pattern this avoids), [[Just Run It Again]] (run the goal-oriented prompt multiple times to explore different solution paths), and [[High Level Strategy, Low Level Details]] (the Planner should receive goals, not procedures).

It's also the difference between a good CLAUDE.md and a bad one. A bad context file prescribes how the model should work. A good one describes what success looks like and lets the model figure out how to get there.

---

## The meta-level shift

Zoom out and the real idea is about **where you place your expertise in the workflow.**

The old way: your expertise goes into *prescribing the solution*. You think, then tell the model what to do.

The new way: your expertise goes into *evaluating the output*. You let the model think, then judge whether it's right.

It's a shift from being the architect to being the reviewer. You're still the expert — you still need to know enough to recognize a good answer from a bad one. But you're moving your judgment *downstream* in the process, from input to output, because that's where it's more leveraged.

That's also what makes this scale. A reviewer can evaluate five proposals faster than an architect can design one. Your bottleneck moves from "how fast can I think of solutions" to "how fast can I evaluate them."
