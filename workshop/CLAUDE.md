# Workshop

A new 7-day live workshop being built by combining material across the Agentic Coding School catalogue (147-video Master Claude Code class, Codex, Techniques, Context Engineering, Prompt Engineering, Workflows). The workshop is the *distilled* version — the canonical path through the material, not a re-recording of every video.

## Current stage

Curriculum design. Pricing is sketched ($299 early-bird → $599 → $3k with coaching, see [[Pricing Structure]]). [[Class Structure]] holds the current proposed shape and explicit merge/separation decisions. No live content has been recorded yet for this workshop specifically.

## Folder map

- `content/` — one note per workshop topic. Most are stubs with links to the source X/YouTube/blog post the topic came from. Title Case filenames so Obsidian `[[wiki-links]]` resolve.
- `ideas/` — raw idea-atoms not yet placed on the curriculum. kebab-case. Includes `agent-teams/` (6-archetype series) and standalone observations (e.g. long-context behaviour, sycophancy, auto-advancing design).
- `images/` — diagrams referenced by content notes (`mission.png`, `libraries-vs-products.png`).
- `Class Structure.md` — the live curriculum proposal.
- `Pricing Structure.md` — pricing tiers.

## How to work on this

- When adding a topic: drop a stub in `content/` (Title Case) with links to source material, then add it to the right day in `Class Structure.md`.
- When promoting an idea: move the file from `ideas/` to `content/`, rename to Title Case, and place it on a day.
- When merging notes: leave the merge note in the `Merges` section of `Class Structure.md` so the reasoning survives.
- Source ACS videos via the `mcp__claude_ai_Agentic_Coding_School__*` tools. The Master Claude Code class is the primary spine to draw from.

## Conventions

- `content/` uses Title Case with spaces (matches Obsidian wiki-link norm).
- `ideas/` uses kebab-case (matches vault-wide convention from root [CLAUDE.md](../CLAUDE.md)).
- Never delete a note without explicit user permission. Stubs are fine.
- Most notes are intentionally short stubs that will expand later.
