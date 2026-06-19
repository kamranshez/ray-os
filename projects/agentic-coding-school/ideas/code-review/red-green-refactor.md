---
class: "code-review"
status: "idea"
aliases: [red-green-refactor]
---

https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
![[red-green-refactor.png]]

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

# Not Everyone is a fan

DHH — the guy who created Rails — famously declared *"TDD is dead"* in 2014. His argument wasn't that testing is bad; it was that test-first as a design practice had calcified into dogma, and that the relentless focus on isolated unit tests was producing baroque architectures full of service objects, mocks, and indirection whose only job was to avoid hitting the database.

His pushback, summarised:

- Test-first started as a useful training wheel and got corrupted into a litmus test for who counts as a "real" engineer.
- Mock-heavy unit tests warp system design — you end up building for testability, not for the actual problem.
- The centre of gravity should shift from unit tests to slower, higher-level **system tests** (Capybara-style, full stack).
- Don't replace one religion with another. "System tests only!" is just the next golden calf.

### What he actually means, plainly

- **The cultural problem.** TDD started as a helpful habit and turned into a religion. People stopped asking *"is this useful here?"* and started asking *"am I a good engineer?"* — judged by whether they wrote the test first.
- **The technical problem.** If tests must run in milliseconds, they can't touch the database, filesystem, or network. So you invent layers — service objects, repositories, command patterns, dependency injection — purely so you can swap in fakes during tests. Your architecture gets shaped by what's easy to mock, not by what's natural for the problem. Twenty tiny classes where two would do.
- **His preference.** Fewer, slower tests that exercise the real system end-to-end — real database, real HTTP, real browser. They take longer to run, but they tell you whether the thing *actually works*, not just whether your mocks agree with each other.
- **The deeper point.** Tests serve the design. If the testing style is bending your code into knots, the testing style is wrong — not the code.

This connects directly to the AI version of the same trap: agents generating self-affirming unit tests that pass coverage but validate nothing. DHH was making that argument about humans a decade before LLMs made it worse.

Worth holding alongside the RGR enthusiasm: the loop is powerful, but the *kind* of test you write at the Red step matters more than the ritual. Behavioural tests against stable contracts age well; tests glued to implementation details rot fast — which is exactly the trap DHH was warning about.


## Sources

- Grok thread: https://grok.com (Red-Green Refactor in AI Coding)
- Matt Pocock's skills library — `/tdd` skill that enforces strict RGR in Claude Code
- Ryan Hart's "Superpowers" framework — auto-triggers planning → bite-sized tasks → enforced TDD
