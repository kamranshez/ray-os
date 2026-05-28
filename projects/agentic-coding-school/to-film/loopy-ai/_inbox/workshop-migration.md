---
tags: [loopy-ai, inbox, workshop, migration]
date: 2026-05-28
status: inbox
---

The workshop is being retired and its Day 9 "Loopy AI" block becomes this class. Everything below already exists in the repo and should be pulled in / re-watched when scripting.

## Workshop Day 9 stubs (source: `workshop/content/day-9/`)

All currently thin stubs. Migrate the framing, then expand:

- **Ralph Loops** — "run the same prompt in a fresh window over and over until the goal is met. Cheap, dumb, surprisingly effective." TODO it carries: in-window vs out-of-window variants, when to compact vs restart, the "/goal contract" anatomy (commit a6c99c4).
- **Closing the Loop** — empty stub. There is already a *filmed* ACS video for this: `projects/agentic-coding-school/filmed/techniques/closing-the-loop.md`. Re-watch and reuse.
- **Autoresearch** — Karpathy-style autonomous loop: run a skill, score against binary evals, mutate the prompt, keep improvements. Local skill lives at `~/.claude/skills/autoresearch/` (confirmed present). Pairs with Ralph and /goal.
- **/goal** (`goal.md`) — saved links: jarrodwatts + kingbootoshi (both now in [[sources-x]]).
- **Writing Effective Goals** — saved links: vincent_koc + _avichawla (both in [[sources-x]]; Avi's 9-section template is the centrepiece).
- **Missions** — referenced from the stubs as a sibling of /goal and Autoresearch; no stub file yet, needs defining.

## Existing long-form asset (reuse as the spine)

`socials/youtube/videos/uploaded/codex-goal-vs-ralph.md` — full ~10-min script, "Codex /goal vs Ralph." Contains the best framework we have:

- **vibes-based completion** as the shared enemy (agent feels done, isn't).
- Ralph = discipline pattern (you write the PRD + gates); /goal = infrastructure pattern (runtime owns the state machine, model can't cheat).
- **pre-decomposable vs unfolding work** decision tree: can you list the steps before you start? Yes -> Ralph. No -> /goal.
- compaction / summary-fidelity as the real frontier-model advantage on long loops.
- the **hybrid**: Ralph as outer loop, /goal inside each iteration.
- "don't run /goal cold" — do a setup interview first (matches Jarrod's /interview point).

This is the strongest existing material. Build the class around it and layer the new X sources on top.

## Other real Ray assets

- `projects/slides/slash-goal-slides.html` — existing /goal slide deck.
- Newsletter teasers on the theme: `.claude/skills/newsletter-writer-teaser/references/example-emails/02-11-tips-for-coding-with-ralph-wiggum.md` and `08-the-official-anthropic-ralph-plugin-sucks.md`.

## Missing / to-locate

- The codex-goal-vs-ralph script references two B-roll HTML artifacts (`goal-feature-explainer.html`, `goal-vs-ralph.html` under `to-film/codex-app/`) that are **not** in the repo right now. Either they were never committed or were moved. Find or rebuild before filming.
- The Ralph repo referenced in the script (`agentic-coding-school/claude-ralph-wiggum`) is not in this vault. Confirm its location.
- "Also check with Grok for other skills" (Apple Notes) — open to-do before scripting.
