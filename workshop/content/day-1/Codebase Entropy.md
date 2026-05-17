---
status: stub
acs: []
mapping: workshop-original
recording-needed: true
day: 1
block: core
---

The load-bearing mental model for the whole workshop: **AI amplifies whatever is already in your codebase**. A clean repo compounds AI gains. A messy one accelerates decay faster than humans can refactor it back.

This is the frame every later day plugs into. Alignment (Day 2), codebase design (Day 5), skills (Day 6), verification (Day 7) — all of it is "how you push back on entropy so AI keeps amplifying upward instead of downward."

## The thesis in one line

Productivity gains from AI correlate weakly with token spend (~0.20 R²) and strongly with codebase cleanliness (~0.40 R²). How you use AI matters more than how much you use it, and the codebase it lands in matters most of all.

## The entropy spiral

Unchecked AI in a messy codebase doesn't just fail to help — it actively makes things worse:

1. AI ships more PRs.
2. Code quality drops because the agent is pattern-matching against existing mess.
3. Rework and refactor time climbs to compensate.
4. Engineers start rejecting AI output.
5. Trust collapses. AI gets abandoned. The mess remains, now larger.

One real case study: 14% more PRs, 9% drop in code quality, 2.5× rework. Net effective output: roughly zero. The team thought they were winning because PR counts went up.

## What "clean" actually means for an agent

Not "pretty." Not "DRY." Specifically:

- **Test coverage** — behavioural tests against stable contracts, not implementation details.
- **Type coverage** — agents can't reason about untyped surface area.
- **Documentation** — CLAUDE.md hierarchies, glossaries, AGENTS.md (Day 2, Day 5).
- **Modularity** — deep modules, small interfaces (Day 5: [[Designing Codebases AI Loves]]).
- **Predictable shape** — folders an agent can guess at, names that read like sentences.

## How the rest of the workshop fights entropy

- **Day 2 — Alignment.** Give the agent the right context up front so it stops pattern-matching against the wrong examples.
- **Day 5 — Context Architecture.** Make the repo physically and documentationally legible.
- **Day 6 — Skills.** Encode hygiene as repeatable skills (`/simplify`, `/improve-codebase`).
- **Day 7 — Verification.** Catch entropy at the door with reviewers, TDD, and adversarial agents.

Without this Day 1 frame, those days look like a checklist. With it, they're one coherent strategy: amplify the upward loop, starve the downward one.

## The handoff

The rest of Day 1 ([[Context is Everything]], [[Subagents]], [[Understanding a Repo]], [[The Core Loop]]) shows you how an agent actually reads and works in a repo. Keep this entropy frame in mind while you watch — every technique on later days is either "make the codebase amplify the agent" or "stop the agent from amplifying the codebase's mess."
