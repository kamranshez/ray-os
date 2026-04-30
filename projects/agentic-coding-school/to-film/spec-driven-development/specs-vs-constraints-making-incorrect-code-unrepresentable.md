## What This Video Covers

A distinction that unlocks safer agent work: specifications describe what should change, constraints describe what must not be touched. Most people conflate them. Pulling them apart lets you give agents freedom where freedom is safe, and hard guardrails where it isn't.

The deeper move: stop reviewing code after generation and start making incorrect code unrepresentable in the first place. Types, CLAUDE.md boundaries, file-level don't-touch lists, compiler-enforced invariants. If the agent literally cannot express the wrong thing, you don't have to catch the wrong thing.

## Why This Matters

From the retreat:

> "A key insight was the separation of specifications from constraints. Specifications describe what should change; constraints define the bounded contexts in which change is allowed, including what must not be touched. These constraints limit blast radius and let agents work safely across domain boundaries."

> "When a constraint must be broken, it signals a new system boundary and prompts refactoring."

And the principle that underwrites the whole approach:

> "The group converged on a principle: what is good for AI is good for humans. Languages that make incorrect code unrepresentable (through strong types, restricted computation models and formal constraints) help agents produce correct output and help humans verify it."

Constraints are cheaper than review. A typecheck runs in milliseconds. A reviewer reading the diff costs minutes. If you can move a class of mistakes from "things I have to catch" to "things that literally can't compile," that is pure leverage.

## The Distinction

**Specification** (what to change):
- "Add a new endpoint that returns the last 30 days of user activity"
- "Refactor the billing module to use the new pricing tiers"
- "Add email notification when a subscription expires"

**Constraint** (what must hold / what not to touch):
- "Do not modify the payments module"
- "All currency values must be stored as integer cents, never floats"
- "The public API surface in `api/v1/` is frozen — new endpoints go in `api/v2/`"
- "No changes that break these test files"

Specs change every task. Constraints persist across tasks. That is the clearest way to tell them apart.

## Where Constraints Live

A layered approach, cheapest to most expensive:

1. **Type system**: the compiler enforces. Free at runtime. Rust and TypeScript can encode an enormous amount of "don't do that."
2. **CLAUDE.md boundaries**: don't-touch lists, invariants, naming conventions, architectural rules. Read by the agent every session.
3. **Hooks**: pre-commit, pre-push, tool-call gates. Block destructive operations before they happen.
4. **Tests as constraints**: existing tests that encode "this behavior must not change." Agent-generated changes have to keep these green.
5. **Code review (last resort)**: human catches what the earlier layers missed.

Notice that review is the last line, not the first. If review is where you catch a class of errors, those errors will eventually slip through. Move them earlier.

## When a Constraint Has to Break

The retreat line worth memorizing:

> "When a constraint must be broken, it signals a new system boundary and prompts refactoring."

If an agent genuinely cannot complete the spec without breaking a constraint, that is information. It means the spec crossed a boundary that needs an explicit decision. The right response is not "override the constraint quietly." The right response is to stop, surface the conflict, and either change the spec, change the constraint, or refactor the boundary.

This turns constraint violations into a useful signal instead of an obstacle.

## Practical CLAUDE.md Patterns

Things to show in the video:

- A "Don't touch" section listing paths that are frozen
- A "Invariants" section listing rules that must hold across all changes ("currency is integer cents")
- An "Architecture" section defining bounded contexts ("routes go here, business logic goes there, no cross-imports")
- A "When in doubt" section pointing to the right human to ask, rather than guessing

## Key Concepts to Cover

- The spec / constraint distinction (what changes vs what doesn't)
- Constraints persist, specs are per-task
- "Make incorrect code unrepresentable" as a design goal
- The layered constraint stack: types → CLAUDE.md → hooks → tests → review
- Why review is the last line, not the first
- "What is good for AI is good for humans" (the quote, and why)
- Breaking a constraint as a refactoring signal, not an override
- Practical CLAUDE.md patterns (don't-touch, invariants, bounded contexts)
- The blast-radius connection: tighter constraints around higher-blast-radius code

## Demo Plan

1. Show a task given to Claude with no constraints — agent wanders into sensitive code
2. Add a don't-touch section to CLAUDE.md — agent respects it
3. Show a typecheck catching an error that would have required review
4. Show a hook blocking a destructive operation
5. Walk through a real constraint conflict: agent says "I can't do X without touching Y"
6. Use that as the prompt for a refactor, not an override

## Suggested Class Placement

Spec-Driven Development — pairs directly with "Specs are the New Product." Specs answer "what changes." Constraints answer "what doesn't." Both are needed.
