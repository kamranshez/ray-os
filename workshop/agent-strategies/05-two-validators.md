---
tags: [agentic-coding, validation, behavior-validation, computer-use]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
---

## What this video covers

There are two validators, not one. The first runs static checks: lints, types, tests, code review. The second runs the actual application and clicks through it like a human. Most agent systems only have the first. Missions has both, and most of the wall-clock time goes to the second.

## Why this matters

You can have 100% test coverage and still ship a broken application. The tests verify the code; they don't verify that the running system does what the user expects. Behavior validation closes that gap.

> "Most systems validate by maybe running lint, type check, tests, maybe they do code review. Missions does all of that, but we also validate behavior."

This is the difference between a system that drifts after a few hours and one that runs for sixteen days.

## Sub-chapter 1: The scrutiny validator

Traditional. Familiar. Necessary but not sufficient.

> "The first one is more traditional. It runs the test suite, type checking, lints and critically it spawns dedicated code review agents for each completed feature within the milestone."

What it does:
- **Test suite.** Run everything; report failures.
- **Type checking.** TypeScript compiler, mypy, whatever applies.
- **Lints.** Style, common bugs, dead code.
- **Code review.** This is the interesting part. Per feature, a fresh code reviewer agent spawns and reviews just that feature's diff.

The code review per feature is what most teams skip. It's also the highest-signal piece. A reviewer that has never seen the implementation reads the diff and the validation contract assertions for that feature and asks: does this code do what the contract says?

This validator is fast. Tokens, not wall-clock time, dominate.

## Sub-chapter 2: The user-testing validator

Less traditional. Slow. The reason missions can ship working software.

> "The second one which is the user testing validator is more interesting. It kind of acts like a QA engineer. It spawns the application. It interacts with it through computer use or something similar to that. It fills out forms, you know, checks that pages render correctly, clicks buttons and ensures that functional flows work holistically."

What it does:
- Spawns the actual application (dev server, deployed instance, whatever the project ships).
- Drives it through computer use or browser automation.
- Walks through the validation contract assertions that require behavior verification.
- Reports pass/fail with traces.

Concrete: "User authentication uses bcrypt" can be checked statically. "The user can sign up, receive a confirmation email, and log in" requires actually doing it. The user-testing validator does the second class.

## Sub-chapter 3: This is where the time goes

The most counterintuitive fact about long-running missions:

> "This step takes significantly longer than the previous one of the scrutiny validator because the system is interacting with a live application. And what we've noticed is that most of the mission's wall clock time is actually spent here waiting for this real world execution to occur instead of generating tokens."

If you measure mission cost in dollars, implementation dominates. If you measure in wall-clock time, user-testing dominates. The system is sitting there waiting for forms to submit, pages to render, async jobs to complete. That's not a bug. That's what it costs to verify behavior.

If you find your agent system is "fast" because it skips this, you don't have a fast system. You have a system that doesn't actually verify the work.

## Sub-chapter 4: Why both, not just one

Couldn't the user-testing validator catch everything? In principle, yes. In practice, no.

- **Static checks are cheap.** A type error caught by tsc costs almost nothing. The same error caught by behavior testing costs you a full app spawn and traversal.
- **Static checks are precise.** A type error points at line 42. A behavior failure points at "the form didn't submit."
- **Behavior checks catch what static can't.** Misconfigured environment variables, missing migrations, broken integrations, race conditions in async flows.

Two validators because they're catching different classes of bugs. Skipping either one leaves a gap.

## Sub-chapter 5: Validation never passes the first time

This sounds like a critique. It's actually the point.

> "Notice how validation never succeeds on the first go. We almost always have to create follow-up features. So that really demonstrates the value of a system that does this QA loop."

If validation passed the first time, you'd suspect the validators weren't doing their job. The system is *designed* to find the gaps and scope follow-up work to close them. A mission's wall-clock time is dominated by user-testing precisely because every milestone produces follow-ups, and the mission iterates until the contract is satisfied.

## Sub-chapter 6: Integrating the two at milestone boundaries

Both validators run at every milestone. Order matters: scrutiny first (cheap, fast), then user-testing (slow, expensive). If scrutiny fails, you don't run user-testing yet; fix the easy stuff first.

Output of both feeds the orchestrator, which decides:
- Are there follow-up features to scope?
- Should the milestone be re-run after corrections?
- Is the milestone done and the next one ready to start?

This is where milestone boundaries earn their keep. They're the natural pause points where the mission self-corrects before drift compounds.

## Talking points for filming

- The scrutiny / user-testing split, named explicitly
- "Most of the mission's wall clock time" — emphasize this is the *good* property
- Concrete examples of what only behavior validation catches
- "Validation never succeeds on the first go" as the punchline

## Key takeaway

Two validators catch two classes of bugs: static checks for code, behavior validation for the running system.
