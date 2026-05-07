---
tags: [agentic-coding, bitter-lesson, prompts, architecture]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
---

## What this video covers

Every multi-agent system you build today has a half-life. The next model release threatens to make your carefully designed orchestration logic obsolete. The fix is the bitter lesson applied to architecture: keep the logic in prompts and skills, not in code. When the model gets better, you remove things, you don't add them.

## Why this matters

If you've built anything substantial with agents, you know the dread. A new model lands, and it's better at the thing your hard-coded state machine was carefully working around. Your code is now fighting the model instead of leveraging it.

Luke names the fear and shows the design choice that defuses it.

> "Every person building multi-agent systems has this fear of the next model release sort of like making their architecture obsolete overnight."

## Sub-chapter 1: The fear

Concrete version of the dread: you've spent two months building a state machine that handles "if the planning agent fails to produce a milestone, retry with this prompt, then escalate to this fallback." The next model lands and just does the right thing on the first try. Your state machine is now dead weight that adds latency and failure modes.

The bitter lesson, applied: every time someone hard-codes a strategy that the model could figure out, the next model embarrasses them. The history of ML is the history of hand-engineered features being replaced by learned ones.

## Sub-chapter 2: Logic in prompts, not state machines

The architectural decision missions makes:

> "Almost all of the orchestration logic is defined in prompts and skills instead of like a hard-coded state machine."

What this looks like in practice:

> "How it decomposes failures and decomposes features and handles failures is all in about 700 lines of text."

700 lines of *text*. Not 700 lines of code with branches and retry policies. The orchestration is a prompt. The model reads it and makes decisions.

The leverage:

> "Four sentences of this can alter the execution strategy pretty dramatically."

You can change behavior by editing four sentences. No deployment, no tests, no migration. Compare to changing four sentences worth of state machine code. Different game entirely.

## Sub-chapter 3: Why prompts win on iteration speed

Three properties that hard-coded logic doesn't have:

- **Faster to change.** Edit a sentence, run a mission, see what happens. No compile cycle.
- **Faster to evaluate.** You can A/B prompt variants in a way that's painful with code-level branches.
- **Faster to remove.** When the model improves, you delete the workaround. With code, "delete the workaround" is a refactor.

This is the bit most teams miss. The bitter lesson isn't just "the model will be smarter." It's "the model getting smarter means you'll be removing code, not adding it." Architectures that make removal cheap win over time.

## Sub-chapter 4: Skills as the worker-level version

Workers don't get one prompt. They get skills, selected per mission by the orchestrator.

> "Worker behavior is driven by skills that the orchestrator defines per mission. So you get very customized behavior."

Skills are the same idea at a different layer: customized worker behavior expressed as text the model reads, not as branches in code. When you want a worker to behave differently for a Rails project versus a TypeScript project, you don't write two different worker classes. You write two different skills and let the orchestrator pick.

This is also how you make the system extensible without forking. New skill for a new domain, no code change.

## Sub-chapter 5: Thin deterministic logic for bookkeeping only

Some things should be code. Luke's framing:

> "The only deterministic logic is very thin and it's focused on enabling models to do what they do best while the system handles like the bookkeeping."

What stays in code:
- Running validators (start the test suite, capture exit codes).
- Persisting handoffs to disk.
- Blocking progress when handoff issues are unaddressed.
- Tracking budget and progress for mission control.

What stays in prompts:
- How to decompose a goal into milestones.
- How to recover from a validation failure.
- How to scope a follow-up feature.
- How to decide a milestone is done.

The split: code handles plumbing, models handle judgment.

> "Missions sort of ensure the discipline and the models provide the intelligence."

## Sub-chapter 6: Removal as the upgrade path

The clearest sign your architecture has the bitter lesson built in: when a new model arrives, your changelog has more deletions than additions.

Most architectures don't have this property. The model improves; you can't take advantage because your scaffolding assumed the model couldn't do the thing you're now seeing it do. So you either rip out the scaffolding (expensive) or live with the legacy (drag).

If your orchestration is in prompts, the upgrade is: read the prompts, identify the parts that are now redundant, delete them, run a mission. The system gets simpler with each model release.

This is the architecture-level version of the bitter lesson. Bet on the model getting smarter, and structure your system so that bet pays off as deletions, not rewrites.

## Sub-chapter 7: Model-agnostic as a structural advantage

A side benefit of putting logic in prompts: you're not locked to one provider.

> "Validation might use a different model provider entirely to make sure that it's not biased by the same training data. This is a structural advantage of a model agnostic architecture."

> "You're only as strong as your weakest link. And if you're locked into one model provider, then you're constrained by that family's weakest capability."

If your orchestration logic is a prompt, it works on any model that can follow prompts well enough. If it's a state machine wired to a specific provider's tool-call schema, you're locked in.

## Talking points for filming

- Open with the dread (everyone building agents has felt this)
- "700 lines of text" and "four sentences" as the punchy specifics
- Code for plumbing, prompts for judgment is the framing
- End on "deletion as the upgrade path" — the inversion is the memorable point

## Key takeaway

Put orchestration logic in prompts; when the next model lands, you'll be deleting code, not rewriting it.
