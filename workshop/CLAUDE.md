# Workshop

A 7-day live workshop being built by combining material across the Agentic Coding School catalogue (147-video Master Claude Code class, Codex, Techniques, Context Engineering, Prompt Engineering, Workflows). The workshop is the *distilled* version — the canonical path through the material, not a re-recording of every video.

## Current stage

Curriculum design, structure **A1 locked** with **comprehensive ACS video mapping applied** (see [[Class Structure]]). Day 0 is async pre-work; Days 1–7 are live, each with Core watch-along / Practice / Deep cuts blocks drawn from the 289-video ACS catalogue. Most `content/` notes are intentional stubs. Pricing sketched in [[Pricing Structure]] ($299 early-bird → $599 → $3k with coaching).

**Net-new recording planned** (see Class Structure's Recording Plan section): convergence thesis + 5 archetypes (Day 7), Status of Agents, long-context trio synthesis, Missions/Goals merge, Languages, Removing Bottlenecks, OpenAI Symphony.

**Pending follow-up pass**: stub triage — ~17 stubs to slim to one-line pointers (ACS video covers them), ~10 to expand past their matching ACS video. Plus 6 open calls captured in Class Structure's Findings section.

**ACS frontmatter applied**: every `content/*.md` file now declares `mapping` / `day` / `block` / `acs:` pairs in YAML frontmatter — read `What a stub is` below before editing any content note.

## What a "stub" is (read this before touching content/)

Every file in `content/` is one of three things. The YAML frontmatter at the top of each file says which:

```yaml
---
status: stub
acs:
  - class: claude-code
    title: Spec Developer
  - class: claude-code
    title: Checking After Spec Developer
mapping: mapped         # mapped | mapped-partial | workshop-original
day: 1
block: core             # core | practice | deep-cut | n/a
---
```

Meanings:

- **`mapping: mapped`** — the stub is a *pointer* to one or more existing ACS videos. The body of the file should be short: enough framing to remind you what the topic is and which day it lives on, then a list of the ACS videos. **Don't expand these stubs into full notes** — the videos do the teaching. When fleshing out, you re-watch the named ACS videos and write the *workshop framing* (transitions, intro, post-watch discussion prompts), not a duplicate of what the video already says.
- **`mapping: mapped-partial`** — an ACS video covers part of the topic, but the workshop angle is bigger (more context, more recent thinking, a stronger frame). The body should capture *what the workshop adds past the video*. When fleshing out, expand the body with new framing; the video is supporting material.
- **`mapping: workshop-original`** — there is no matching ACS video. `acs: []` and `recording-needed: true`. These stubs *will* expand into full notes that drive a net-new recording. Day 7's archetype series, [[Status of Agents]], the long-context trio synthesis, etc.

The `acs:` field is a list of `(class, title)` pairs — these are the IDs the MCP uses (`mcp__claude_ai_Agentic_Coding_School__get_video` takes `classSlug` + `videoTitle`). To re-watch a video while fleshing out a stub: feed those pairs into `get_video` and the transcript comes back.

`day:` and `block:` are denormalised from `Class Structure.md` so each stub stands alone. If you move a topic between days, update both.

## Folder map

- `content/` — one note per workshop topic. Frontmatter tells you what each is. Includes the `agent-teams/` archetype series (all `mapping: workshop-original`).
- `ideas/` — raw idea-atoms not yet placed on the curriculum. Mostly empty now that A1 promoted most of them. No frontmatter required.
- `proposals/` — numbered design proposals from parallel curation agents. Read these to understand *why* the current structure is what it is. Don't edit — they're frozen artefacts.
- `images/` — diagrams referenced by content notes.
- `Class Structure.md` — the locked 7-day curriculum, plus Recording Plan / Stub Triage / Merges / Separations / Open Questions.
- `Pricing Structure.md` — pricing tiers.

## How to work on this

- **Adding a topic**: drop a stub in `content/` with the frontmatter block above, then place it on the right day in `Class Structure.md`.
- **Promoting an idea from `ideas/`**: `git mv` into `content/` (basename unchanged so `[[wiki-links]]` keep resolving), add frontmatter, add to a day.
- **Fleshing out a stub**: check `mapping`. If `mapped`, watch the named ACS video(s) and write the workshop framing. If `mapped-partial` or `workshop-original`, write the full note — that's where workshop IP lives.
- **Merging notes**: leave the merge decision in `Class Structure.md`'s Merges section so the reasoning survives.
- **Re-watching an ACS video**: use the `(class, title)` pairs in the frontmatter and `mcp__claude_ai_Agentic_Coding_School__get_video`.

## Conventions

- `content/` uses **mixed casing on purpose**: Title Case for canonical workshop topics (`Spec Developer.md`, `Adversial Reviewers.md`) and kebab-case for atomic-idea notes promoted from `ideas/` (`auto-advancing-design-destroys-implementations.md`). Obsidian resolves `[[wiki-links]]` by exact basename, so either works.
- `ideas/` uses kebab-case (matches vault-wide convention from root [CLAUDE.md](../CLAUDE.md)).
- Never delete a note without explicit user permission. Stubs are fine and expected.
- Most notes are intentionally short stubs that will expand later.
