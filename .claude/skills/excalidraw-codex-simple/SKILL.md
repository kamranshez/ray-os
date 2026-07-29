---
name: excalidraw-codex-simple
description: Generate SIMPLE, single-idea excalidraw diagrams for video frames and slides — one concept per image, ten words maximum, abstract geometry only, enormous negative space. Use whenever a diagram is going on screen in a video, a slide, or an explainer and must be readable in two seconds. Triggers on "make a diagram for this", "simple excalidraw image", "visual for this section", "excalidraw-codex-simple", or any request for explanatory visuals where the image will be shown to an audience rather than read up close. Prefer this over [[excalidraw-codex]] for anything presented on screen; use the older skill only when you deliberately want a dense, complete poster that summarises a whole section.
---

## What makes this skill different

`excalidraw-codex` mandates passing source text **verbatim**. That is exactly what makes its output cluttered: the model treats every sentence as something it must render, optimises for completeness, and returns an exhaustive poster with no focal point and text far too small to read at 1080p.

This skill inverts that rule.

> **Pass ONE idea, stated as meaning. Never pass source text verbatim, and never prescribe the geometry.**

Everything else follows from that. The wrapper adds a hard constraint set — one idea, no illustration, ten words maximum, enormous margins, one focal point — and explicitly tells the model *"the geometry is yours to invent."* Handing over the geometry is what produces diagrams that are better than what you would have specified.

## Engine

Drives the **Codex CLI** headlessly (`codex exec --skip-git-repo-check --json`) and lets Codex's bundled `image_gen` tool produce the images. No API key; requires a completed `codex login` and codex **0.144.1+**.

Simple diagrams render *much* faster than dense ones: a 16-image fan-out completes in about 4 minutes, versus ~33 for the poster-style skill.

## Writing the prompt — the whole skill in one rule

Write what the diagram must **mean**. Do not write what it should look like, and do not paste the script.

**Bad** (verbatim source — produces a poster):
```
LAYER 4 — The trajectory. Artifact on screen: an agent trajectory log.
commands: rg "invitation" apps/api · git log --grep="8486" · pnpm test
What it catches — "Nothing on the board. Not one row..."  [+400 more words]
```

**Bad** (prescribed geometry — produces a copy of whatever you described):
```
One long horizontal rounded rectangle with a blue diagonal-hatched block at the
left end, labelled "the prompt", and a dashed line two thirds along.
```

**Good** (meaning — produces an invented solution):
```
Four kinds of checking each judge the final result. A fifth thing is not another
check of the result at all — it watches the path taken to get there, and so it
encloses and protects the other four rather than sitting alongside them.
```

Guidelines that matter:
- **State the relationship, not the shapes.** Most good diagrams are two or three things in a fixed spatial relationship, with the relationship carrying the meaning.
- **Name what the image is *about*.** "The uncovered gaps between their coverage are the point of the image" tells the model where the focal point goes.
- **Say what should feel true.** "The image must make the shortness of the cheating route feel obvious and inevitable" beats specifying line lengths.
- **One idea per image.** If your paragraph contains two ideas, that is two images.

## Usage

```bash
.claude/skills/excalidraw-codex-simple/scripts/generate.sh \
  -p "<the idea, stated as meaning>" \
  -o "/Users/ray/Desktop/ray-os/images" \
  -x "<unique-slug>" \
  -n 3
```

**Options**
- `-n, --count` — variations per call (default 5; **3 is usually plenty** here, since variations are genuinely different solutions rather than recolours).
- `-x, --name <slug>` — globally-unique kebab-case basename → `<slug>-1.png`, `<slug>-2.png`, …
- `-w, --words <n>` — word budget for text inside the image (default **10**). Raise to ~15 only for a diagram that genuinely needs five labels; lower to 4-6 for a closing or thesis frame.
- `-a, --aspect` — advisory only on this path; codex decides final dimensions (~1672×941).
- `-r, --ref <file>` — extra style reference, repeatable.
- `--no-default-refs` — skip the bundled references. **Use this when you want to explore a new design language** — attached references guarantee imitation, which is precisely their job, so remove them to diverge.

## Output location

All images go to the single vault-root `images/` folder — flat, no per-note subfolders. Uniqueness comes from the `-x` slug, never from a folder path. Embeds are filename-only wikilinks: `![[my-slug-1.png]]`.

## Whole-file / whole-deck mode

Don't split by `##` headings. Split by **idea**, then write one meaning-statement per idea. A single section often yields two diagrams (its claim, and how it fails); some sections yield none.

Fan out **all ideas at once** — each `generate.sh` call is its own codex session, and there is no shared rate limit. Write a single driver `.sh` to the scratchpad that writes each idea to its own `.txt` heredoc, launches every call with `&`, `wait`s, then tallies per slug. Launch that driver once with `run_in_background: true`.

## Bundled references

`assets/reference1-3.png` are the chosen house style — hand-sketched excalidraw on near-black, muted red/blue/amber/green, scribbled cross-hatch fills, handwriting throughout. The wrapper attaches them on every call and tells codex they are **style-only**.

These deliberately contain **no characters, robots, or illustrated objects**. The predecessor skill's references did, and that alone was enough to pull every image toward illustration regardless of the prompt. If output ever drifts back toward cute drawings, check the references before touching the prompt.

## Recovering a killed run

Codex writes PNGs to `~/.codex/generated_images/<thread_id>/` and the wrapper copies them out only at the end, so a killed run appears to have produced nothing. It hasn't. Map sessions back to slugs by grepping the rollout files for distinctive prompt text:

```bash
cd ~/.codex/sessions/YYYY/MM/DD
LC_ALL=C grep -l -a "<distinctive phrase>" rollout-*.jsonl
```

Then copy the PNGs out of the matching `~/.codex/generated_images/<thread_id>/` by hand.

## Requirements

- `codex` CLI on PATH with a completed `codex login`. Auth expiry produces a `401` / `turn.failed`; the wrapper detects it and prints the fix.
- codex **0.144.1+**. `0.140–0.143` generate a valid PNG but never save it (openai/codex#28422); `0.139` is rejected outright by the account's default model. Both fail silently — trust the wrapper's version warning, not an empty log.
