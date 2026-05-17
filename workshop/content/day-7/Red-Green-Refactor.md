Optional but powerful closing technique for Day 7. Where reviewers catch problems after the fact, Red-Green-Refactor prevents them upstream by making the test the spec.

## The cycle

- **Red** — write a failing test that describes the behaviour. The test is the spec.
- **Green** — simplest possible code to make it pass. Often ugly, deliberately.
- **Refactor** — clean up structure, naming, duplication. Tests stay green the whole time.

Repeat per tiny slice of functionality.

## Why it matters with AI

Unsupervised agents almost always write the implementation first and then bolt on tautological tests that just restate the code. RGR inverts the order so the agent can't fake correctness:

- Test first = zero ambiguity. The agent can't drift into "looks right."
- Pass/fail is binary. Reviewers give fuzzy signal; tests give a light.
- Refactoring is fearless. Tests catch regressions instantly.
- Prevents over-engineering. Only write what the test demands.

## Backend vs frontend

- **Backend** (APIs, business logic, data layers) — RGR pays off. Bugs are expensive and invisible until they ship.
- **Frontend** (components, styling, layout) — direct implementation + visual check is usually faster. RGR optional.

This is the "update the do-work skill to use red-green-refactor for backend, direct implementation for frontend" idea.

## Where this sits in Day 7

Day 7 is mostly post-hoc verification (reviewers, adversarial agents, codex second opinions). RGR is the upstream version of the same goal: trust. Reviewers cover what tests can't (architecture, taste, subtle correctness). Tests cover what reviewers shouldn't have to (correctness on the happy path and named edge cases).

If a `/tdd` skill enforces the loop, the agent literally cannot proceed past Red without a failing test, or past Green without it passing. That's the form most teams are converging on.

## Sources

- Grok thread: https://grok.com (Red-Green Refactor in AI Coding)
- Matt Pocock's skills library — `/tdd` skill that enforces strict RGR in Claude Code
- Ryan Hart's "Superpowers" framework — auto-triggers planning → bite-sized tasks → enforced TDD
