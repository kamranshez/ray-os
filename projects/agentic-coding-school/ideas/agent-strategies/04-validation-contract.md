---
tags: [agentic-coding, validation, tdd, planning]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
status: "idea"
---

## What this video covers

Why tests written after the code don't catch bugs, and what to do instead. Specifically: writing a validation contract during planning, before any code exists, that defines correctness independently of whatever implementation eventually satisfies it. This is the validation pillar's foundational video.

## Why this matters

The single most common failure mode I see in agent-driven workflows: the agent writes the code, the agent writes the tests, the tests pass, coverage is 95%, and the feature is broken anyway. Luke names exactly why.

> "Tests written after implementation don't catch bugs. They confirm decisions."

If you take one thing from this entire validation pillar, take that line.

## Sub-chapter 1: The pattern that looks fine and isn't

The agent loop most people run today:

1. Agent reads the spec.
2. Agent writes the implementation.
3. Agent writes tests for the implementation.
4. Tests pass.
5. Agent reports done.

> "An agent builds a feature, it writes some tests, the tests pass, there's full coverage, but the tests were sort of shaped by the code, not by what the code was attempting to actually do."

Read that twice. The tests were shaped by the code. The code was supposed to be shaped by the spec. Somewhere in step 3, the spec stopped mattering and the implementation became the source of truth.

## Sub-chapter 2: Tests confirm; they don't catch

Why does this matter? Because what you wanted from the tests was bug-catching. What you got was decision-confirming.

> "Tests written after implementation don't catch bugs. They confirm decisions. So if you rely on validation like that, your system will eventually drift."

A test that says "the function returned 42" only catches bugs if "42" was the right answer in the first place. If the agent decided 42 was the answer and then wrote a test asserting 42, the test passes regardless of whether 42 was correct.

For one feature, you might catch this in code review. For a system running unattended for sixteen days, you won't. The drift compounds silently and you don't notice until everything is wrong.

## Sub-chapter 3: The validation contract

The fix: define correctness before any code exists.

> "That's why this validation contract exists. It's written during planning before any code and it defines correctness independently of implementation."

A validation contract is a list of assertions about what "done" means. It's produced during planning, by the orchestrator, in conversation with the human. It's written as a markdown file (`validation-contract.md` in the missions architecture).

> "For a complex project, this can be hundreds of assertions and each feature is assigned one or more assertions that it must satisfy. The sum of all features must mean that every assertion is covered."

Two structural points:
- **Hundreds of assertions.** Real contracts are big. They cover edge cases, error states, integration behaviors, performance bounds.
- **Coverage requirement.** Every assertion in the contract must be claimed by at least one feature. The feature decomposition isn't done until the contract is fully covered.

## Sub-chapter 4: Why this is TDD generalized

If you've used TDD, this should feel familiar. Tests-first works because the tests cannot be shaped by the code that doesn't exist yet. The validation contract is the same idea, scaled up to multi-day work.

The difference: a unit test specifies behavior at the function level. A validation contract specifies behavior at the *system* level: "the user can sign up and receive a confirmation email," "the migration runs without locking the table for more than five seconds." Things you can't reasonably write a unit test for at planning time, but you can write an assertion for.

The contract becomes the spec for the validators (next video). Implementation correctness is graded against it, by an agent that has never seen the implementation.

## Sub-chapter 5: Forcing the human to think first

There's a second-order benefit. Writing the contract forces the human and the orchestrator to actually nail down what they want before the implementation starts.

> "When you describe what you want, the orchestrator is kind of like your sounding board. It asks you the right strategic questions. It checks out if there's any unclear requirements in the problem space."

A vague spec produces a vague contract, which is the orchestrator telling you "I don't know what done means." That's a pre-implementation correction, which is dramatically cheaper than a post-implementation rewrite.

If you can't write the contract, you can't write the code yet.

## Sub-chapter 6: What goes in, what doesn't

Good contract assertions:
- "User authentication uses bcrypt with cost factor 12 or higher."
- "The /api/messages endpoint returns 401 when called without a valid session."
- "Migrations from v1 to v2 preserve all existing user records."
- "The page renders correctly at viewport widths from 320px to 1920px."

Bad contract assertions:
- "The code is well-architected." (Ambiguous; not a verifier-friendly question.)
- "It's performant." (No threshold.)
- "Users will like it." (Not testable from the contract alone.)

The rule is the same as for any verifier: narrow, unambiguous, answerable. If a fresh agent reading just the contract can't determine pass/fail, the assertion is too vague.

## Talking points for filming

- Open with the "tests confirm decisions" quote, slow and clean
- Walk through the broken loop (1-5) explicitly so viewers see themselves in it
- Show a real fragment of a validation contract on screen
- Close on "if you can't write the contract, you can't write the code yet"

## Key takeaway

Define done before any code exists; tests written after implementation confirm decisions instead of catching bugs.
