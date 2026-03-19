---
status: filmed
---

## Source

- https://www.intent-systems.com/learn/context-is-your-constraint#agentic-search

---

## The Core Principle

Every token in context can every other token.

This means **signal-to-noise ratio is everything**.

Your job as a context engineer is to curate the smallest, highest-signal slice of context for the task at hand.

---

## The Tradeoff

More context seems like it should always help. But it's a double-edged sword:

- More context = more potential signal
- More context = more noise drowning out signal
- More context = less room for reasoning and output

If your context window fills with noise before you establish enough signal, that's a dead chat. The model has what it needs buried somewhere in the mess, but it can't find it.

---

## The Blindfolded Genius

Here's a useful mental model.

When you hand an AI a giant repo and say "fix this," you're blindfolding a genius and dropping them in an unfamiliar building.

- **Agentic search** lets them fumble around and feel the shape of the room
- **Manual context engineering** takes the blindfold off for a specific task
	- This can be your AGENTS.md file or CLAUDE.md file but we'll be going further
- **A systematic context layer** turns the lights on permanently

The genius is still a genius. But without the right context, they're working in the dark.

---

## You Only Get The Behavior You Load

If the model doesn't see specific context, it fills the gap with generic training priors.

This is the fundamental rule: **you only get the behavior you load.**

When the model encounters a gap in its understanding and no relevant context is available, it falls back to patterns from training. The output looks plausible but doesn't match your system.

**Example:** Your codebase has a custom error handling pattern — all errors go through a central `ErrorBoundary` class. But you don't show the model that class or any code that uses it.

The model encounters a situation where it needs to handle an error. What does it do?

It writes standard try/catch with console.log. That's what it saw millions of times in training. It doesn't know your `ErrorBoundary` exists.

You only got the behavior you loaded — which was nothing about your error handling. So you got the generic default.

Now flip it. If you *do* load the `ErrorBoundary` class and an example of it being used, the model follows that pattern. You loaded the behavior, so you got it.

The more specific and unique your codebase, the more this matters. Generic training data hasn't seen your:

- Custom conventions
- Historical decisions
- Domain-specific invariants
- Integration patterns
- Enforcement boundaries

---

## Why This Is Foundational

Signal-to-noise isn't just one problem among many. It's the meta-constraint that underlies everything else in this chapter.

- Search adds noise (next video)
- Too many instructions add noise
- The model's default patterns are noise when they don't match your codebase

Every technique you'll learn in this class is ultimately about improving signal-to-noise ratio. Keep this lens in mind.
