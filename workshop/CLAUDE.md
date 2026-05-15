# Workshop

A 7-day live workshop being built by combining material across the Agentic Coding School catalogue (147-video Master Claude Code class, Codex, Techniques, Context Engineering, Prompt Engineering, Workflows). The workshop is the *distilled* version — the canonical path through the material, not a re-recording of every video.

## Current stage

Curriculum design, structure **A1 locked** (see [[Class Structure]]). Day 0 is async pre-work; Days 1–7 are live. Most `content/` notes are intentional stubs — placeholders with links to source material that will expand into full topic write-ups. Pricing sketched in [[Pricing Structure]] ($299 early-bird → $599 → $3k with coaching). No live content recorded yet.

## Folder map

- `content/` — one note per workshop topic. Includes the `agent-teams/` archetype series.
- `ideas/` — raw idea-atoms not yet placed on the curriculum. Mostly empty now that A1 promoted most of them.
- `images/` — diagrams referenced by content notes (`mission.png`, `libraries-vs-products.png`).
- `Class Structure.md` — the locked 7-day curriculum, plus an explicit Merges / Separations / Open Questions section.
- `Pricing Structure.md` — pricing tiers.

## How to work on this

- When adding a topic: drop a stub in `content/` with links to the source X/YouTube/blog post, then place it on the right day in `Class Structure.md`.
- When promoting an idea: `git mv` from `ideas/` to `content/` (basename unchanged so wiki-links keep resolving) and add it to a day.
- When merging notes: leave the merge note in `Class Structure.md`'s Merges section so the reasoning survives.
- Source ACS videos via the `mcp__claude_ai_Agentic_Coding_School__*` tools. The Master Claude Code class is the primary spine to draw from.

## Conventions

- `content/` uses **mixed casing on purpose**: Title Case for canonical workshop topics (`Spec Developer.md`, `Adversial Reviewers.md`) and kebab-case for atomic-idea notes promoted from `ideas/` (`auto-advancing-design-destroys-implementations.md`). Obsidian resolves `[[wiki-links]]` by exact basename, so either works.
- `ideas/` uses kebab-case (matches vault-wide convention from root [CLAUDE.md](../CLAUDE.md)).
- Never delete a note without explicit user permission. Stubs are fine and expected.
- Most notes are intentionally short stubs that will expand later.
