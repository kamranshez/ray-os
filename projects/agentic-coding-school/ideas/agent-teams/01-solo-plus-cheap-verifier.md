---
status: stub
acs: []
mapping: workshop-original
day: 7
block: core
recording-needed: true
---
# Archetype 1: Solo + Cheap Verifier

## What This Video Covers

The simplest and most underused agent team pattern: one generator, one cheap verifier, a tight loop between them. Not two equally capable agents debating. A smart generator paired with a narrow, stupid, reliable oracle that says "yes" or "no" and nothing else.

This is the foundation every other archetype builds on. If you only ever learn one convergence pattern, learn this one.

## Why This Matters

From the retreat, the insight that reframes TDD:

> "Test-driven development produces dramatically better results from AI coding agents. The mechanism is specific: TDD prevents a failure mode where agents write tests that verify broken behavior. When the tests exist before the code, agents cannot cheat by writing a test that simply confirms whatever incorrect implementation they produced."

> "This reframes TDD as a form of prompt engineering. The tests become deterministic validation for non-deterministic generation."

The whole trick: a 95% accurate generator paired with a 99% accurate verifier gives you a system that is effectively 99%+. The verifier doesn't have to be smart. It has to be right about one narrow question.

## The Pattern

```
┌───────────────┐
│  GENERATOR    │ ← smart, non-deterministic (LLM)
│   produces X  │
└───────┬───────┘
        ↓
┌───────────────┐
│   VERIFIER    │ ← narrow, deterministic (or cheap LLM with one job)
│  X correct?   │
└───────┬───────┘
        ↓
    ┌───┴───┐
  yes     no
    ↓       ↓
   ship   regenerate
```

The loop keeps running until the verifier passes. Generator can be expensive. Verifier has to be cheap enough that running it many times is fine.

## What Counts As a Verifier

Listed cheapest to most expensive:

1. **Typecheck / compile** — free, fast, catches a class of errors for zero effort
2. **Tests** — slightly more expensive, catches behavior
3. **Linter / formatter** — free, catches style drift
4. **Diff against known-good output** — if you have a golden output, a literal diff is a perfect verifier
5. **Schema validation** — JSON schema, SQL schema, API response shape
6. **Narrow LLM verifier** — an LLM with one question: "Does this output mention a date? Y/N." Cheap model, clear question, high accuracy on narrow tasks.

A good verifier is one where the answer is almost unambiguous. "Does this code compile?" Unambiguous. "Is this code good?" Ambiguous, so not a useful verifier.

## Why TDD Is This Pattern

The retreat flags TDD as the strongest form of prompt engineering. The reason is the pattern: tests are the verifier, the agent is the generator, the loop is tight. The agent cannot cheat because the tests existed before the code. The agent cannot argue because the tests either pass or don't.

Every time you tell Claude "here are the tests, make them pass," you are running this archetype. You are just not naming it.

## Designing the Verifier

The design question is not "how do I make my generator better." It is: "What is the cheapest reliable oracle for correctness on this task?"

Examples:
- Generating a SQL query → verifier is "does it parse and return a non-empty result on the test database"
- Generating a React component → verifier is "does it compile, render without error, and match a snapshot"
- Generating a blog post draft → verifier is a narrow LLM checking "does it follow the structure in the style guide" (yes/no)
- Generating a config file → verifier is schema validation plus a dry-run
- Generating a refactor → verifier is "all existing tests still pass"

If you cannot name a cheap verifier for a task, that is a signal. Either you need to invest in building one, or the task is genuinely ambiguous and a single-shot agent is appropriate.

## When the Verifier Passes But the Code Is Wrong

This is the failure mode worth naming. The tests pass but the code is wrong. The typecheck succeeds but the logic is inverted. The schema validates but the values are garbage.

This is why the verifier asymmetry has to be real. If your verifier is as likely to be wrong as your generator, you don't have a convergence system, you have two coin flips. The design job is to make sure the verifier answers a narrower, more deterministic question than the generator answers.

When this fails, the fix is usually to add a second, different verifier. Typecheck + tests + schema validation together are much harder to fool than any one alone.

## Key Concepts to Cover

- The pattern: generator → verifier → loop
- Why the verifier must be cheaper and narrower than the generator
- The six verifier types: typecheck, tests, linter, golden diff, schema, narrow LLM
- TDD as this archetype in disguise
- Designing the cheapest reliable oracle for your task
- The failure mode: verifier passes but code is wrong (and the fix: layer verifiers)
- This archetype as the foundation all others extend

## Demo Plan

1. Give Claude a task with no verifier. Accept the first output. Show it has a subtle bug.
2. Same task. Write the tests first. Give Claude the tests and the task. Loop until green.
3. Add a typecheck verifier on top. Show it catching a different class of error.
4. Show a narrow LLM verifier on a text task (blog post matches style guide).
5. Show the failure mode: verifier passes, code still wrong. Layer a second verifier.

## Suggested Class Placement

Agent Teams — Video 2. The foundation. Every subsequent archetype builds on this one.
