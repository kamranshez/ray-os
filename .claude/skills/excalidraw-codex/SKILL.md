---
name: excalidraw-codex
description: Generate excalidraw-style explanation images using the Codex CLI (codex exec --json) instead of a paid API. Use when the user wants visual explanations, diagrams, or illustrations in the hand-drawn excalidraw aesthetic and asks for the codex path. Codex's bundled image_gen tool runs through the logged-in account, so no GEMINI_API_KEY is required and it's often faster than the Gemini route. Triggers on "generate an excalidraw image", "excalidraw-codex", "use codex for excalidraw", or any request for excalidraw-style diagrams where no engine is named. This is the RECOMMENDED DEFAULT path for excalidraw image generation: it needs no API key and runs through the logged-in Codex account. Sibling skill [[excalidraw-gemini]] does the same job through the paid Gemini API. Default to codex whenever the user does not explicitly ask for the Gemini route.
---

## Engine

This skill drives the **Codex CLI** in headless mode (`codex exec --skip-git-repo-check --json`) and lets Codex's bundled `image_gen` tool produce the images. Reference images attach via `-i <file>` flags. The CLI must already be authenticated (`codex login` was run once).

For the **Gemini API** path (uses `gemini-3-pro-image-preview` via `GEMINI_API_KEY`), see [[excalidraw-gemini]] instead.

## Prompt Content Rule — CRITICAL

**ALWAYS pass the entire raw content verbatim as the prompt.** Never summarize, paraphrase, or condense the content. Whether it's a single section or a whole file, the full text goes into the wrapper as-is. This gives the model the richest context to produce accurate visuals. The wrapper script wraps the verbatim text with headless directives and aesthetic guidance — do not pre-wrap or rewrite it yourself.

**Production timestamps are auto-stripped.** Video-script section headers often carry timecodes, e.g. `### Don't waste the run on one leaf (7:55 - 9:25)`. Left in, the model renders the timecode into a corner of the image. The wrapper now scrubs timestamp ranges (`(2:15 - 4:00)`, bare `7:55 - 9:25`, lone `(0:00)`; `-`/en/em dash separators) from the prompt before it reaches Codex, so you can still pass the section verbatim and the timecodes will not appear in the diagram. This is the only content the wrapper removes.

## Output Location — CRITICAL

**All generated images go into the single vault-root `images/` folder — flat, no per-note subfolders.** This matches the vault's image convention (see the repo CLAUDE.md). Concretely, for this vault: `-o /Users/ray/Desktop/ray-os/images`.

- Name every set with a **globally-unique kebab-case slug** via `-x <slug>` so files never collide in the flat folder. Include the class/note in the slug, e.g. `-x loopy-intro-loop-stack` → produces `loopy-intro-loop-stack-1.png … -5.png`.
- Embeds are **filename-only** wikilinks: `![[loopy-intro-loop-stack-1.png]]` (no path). Because every name is unique and the folder is flat, these resolve from any note and survive note moves.
- Do **not** create `images/<section>/` subfolders. The wrapper handles this automatically once you pass `-o <vault>/images -x <slug>`.

## Semantic Chunking

Don't chunk solely by `## ` headings. Look for:
- Concept definitions ("What is X?", "X are the boundaries where...")
- Distinct examples or scenarios
- Shifts in topic within a section
- Before/after comparisons
- Standalone explanations (like "**What are contracts?**" paragraphs)

Each chunk = one image set. A single `## ` section might produce 2-4 chunks if it covers multiple concepts. When analyzing content, identify these semantic boundaries first, then generate images for each chunk.

---

## First: Ask the User

Before generating, ask which mode they want:

1. **Specific section** — Generate images for one section only (user provides the content)
2. **Whole file** — Parse a markdown file into `## sections`, generate images for ALL sections in parallel

Use AskUserQuestion with options:
- "Specific section" — I'll generate images for content you provide
- "Whole file" — I'll split the file by ## headings and generate for all sections in parallel

## Mode 1: Specific Section

For a single section:

1. Get the section content from the user.
2. Pick a globally-unique kebab-case slug (class + note + section, e.g. `loopy-intro-loop-stack`).
3. Run the wrapper, passing the **entire section content verbatim** as the `-p` prompt (never summarize), outputting into the vault-root `images/` folder:

```bash
.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<entire section content verbatim>" \
  -o "/Users/ray/Desktop/ray-os/images" \
  -x "<unique-slug>" \
  -n 5
```

4. The wrapper prints absolute paths of every PNG it saved. Add embeds to the markdown after the section (see "Adding Image Embeds" below).

## Mode 2: Whole File (Parallel)

For an entire markdown file:

1. Read the file and split into semantic chunks (see "Semantic Chunking").
2. **Fan out ALL chunks at once (full parallelism, no artificial cap).** The Codex CLI's `image_gen` tool serializes per-session, so throughput comes entirely from launching separate `codex exec` calls, each its own session UUID. Launch every chunk simultaneously so a whole deck finishes in one wave (one call's wall-clock, ~5 to 12 min) instead of several sequential waves. There is no shared rate-limit gateway (unlike the Gemini API), so the only ceiling is whatever the codex account allows.
3. **Preferred pattern for more than ~4 chunks: one driver script, launched once in the background.** Writing N separate `run_in_background` Bash tasks is noisy and hard to track. Instead write a single driver `.sh` to the scratchpad that: (a) writes each chunk's verbatim prompt to its own `.txt` (heredoc, so backticks and quotes survive), (b) loops the slugs launching every `generate.sh` call concurrently with `&` (set `MAX` to the chunk count for a single wave; drop it only if you actually hit quota errors), (c) `wait`s for all, then (d) tallies produced files per slug. Launch that driver once with `run_in_background: true`. Each `generate.sh` gets its own `-x <unique-chunk-slug>` and a per-slug log so you can retry only the failures.
   - Output dir: the vault-root `images/` folder (`-o /Users/ray/Desktop/ray-os/images`)
   - Name: `-x <unique-chunk-slug>` (class + note + chunk, so files never collide)
   - Prompt: the **entire chunk content verbatim**
4. Wait for the whole batch, then add all embeds.

**On concurrency:** default to launching everything at once; the codex account is the only real limit. If the JSONL stream shows auth or quota errors, back off (halve the wave and retry the failed slugs), but do NOT pre-throttle to a small number just to be cautious. Full fan-out is the intended behavior so decks render fast.

**Subagent template:**
```
Run this bash command (timeout 900000ms):
/Users/ray/Desktop/ray-os/.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<entire chunk content verbatim>" \
  -o "/Users/ray/Desktop/ray-os/images" \
  -x "<unique-chunk-slug>" \
  -n 5
```

## Wrapper Command Reference

```bash
generate.sh -p "<verbatim prompt>" -o /abs/out/dir [options]
```

**Options:**
- `-n, --count` — Number of variations per call (default 5). Codex produces N images in a single session.
- `-x, --name <slug>` — Basename for saved files (default `excalidraw`). Output is `<slug>-1.png`, `<slug>-2.png`, … Always pass a globally-unique slug so files don't collide in the flat vault-root `images/` folder.
- `-a, --aspect` — Aspect ratio hint embedded in the prompt (default `16:9`). Codex doesn't expose ratio flags directly; the wrapper inlines this into the directive.
- `-r, --ref <file>` — Add an extra reference image. Repeatable. The wrapper auto-attaches every `reference*.png` from `assets/` unless `--no-default-refs` is passed.
- `--no-default-refs` — Skip the bundled `assets/reference*.png` images (use only `-r` files, or none).

**Defaults baked into the wrapper:**
- `codex exec --skip-git-repo-check --json` — headless, JSONL events on stdout.
- Auto-attaches `assets/reference1.png` … `reference4.png` so the model copies the pencil-textured robot and sketchy aesthetic. The wrapper text explicitly tells codex the refs are **STYLE EXAMPLES ONLY** — do not reuse their subject matter, labels, or composition. This prevents the prior failure mode where codex pattern-matched the refs' diagrams (MCP/agent boxes) and ignored the actual prompt content.
- Prompt is passed via stdin (codex's `-i` flag is variadic and would otherwise eat a positional prompt as another image path).
- Prompt is wrapped with: "Do not load skills, do not read files, do not copy outputs — call `image_gen` N times in this single turn and list the saved paths." This is necessary because, left alone, the Codex agent auto-loads `~/.codex/skills/imagegen` and burns ~150k tokens reading skill markdown and copying outputs around.
- Near-black dark-charcoal (#0E1116) background and excalidraw aesthetic directives are inlined in the wrapper prompt.

**Where the images land:**
- Codex writes each PNG to `~/.codex/generated_images/<thread_id>/ig_<hash>.png` first.
- The wrapper reads the `thread_id` from the first JSONL event, then copies every PNG from that session dir into your `-o` directory as `<slug>-1.png`, `<slug>-2.png`, … (where `<slug>` is the `-x` value; auto-incremented; no overwrites).

## X Article Thumbnails

For X/Twitter article cover images use `-a 21:9`:

```bash
.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<thumbnail prompt with bold 3-5 word text>" \
  -o "/Users/ray/Desktop/ray-os/images" \
  -x "<unique-slug>" \
  -n 5 -a 21:9
```

For vibrant brand-colored thumbnails (not the white-background look), the default no-refs mode already avoids the sketchy-white pull. If you want a specific style example, attach it explicitly with `-r path/to/style.png`.

## Adding Image Embeds

After generation completes, add **all N images** to the markdown file under the relevant section. The user picks their favorite(s) later.

**Embed format (Obsidian) — filename-only, no path:**
```markdown
![[<slug>-1.png]]
![[<slug>-2.png]]
![[<slug>-3.png]]
![[<slug>-4.png]]
![[<slug>-5.png]]
```

Place embeds at the end of each section, before the next `---` or `##` heading.

## Important Notes

- **No overwrites:** wrapper increments `<slug>-N.png` to the next free number.
- **Flat vault-root folder:** all images land directly in the vault-root `images/` folder — never per-note subfolders. Uniqueness comes from the `-x` slug, not from a folder path.
- **Embed every variation:** drop all N into the markdown so the user can pick.
- **Timeout:** allow 15 minutes per call (use `timeout: 900000` on Bash invocations).
- **Aspect ratio is advisory only on this path.** Codex's `image_gen` tool decides the final dimensions — output tends to land near 16:9 (~1672×941). If you need pixel-exact ratios, prefer [[excalidraw-gemini]] which has true `-a` control.

## Requirements

- `codex` CLI on PATH (`brew install codex` or via OpenAI installer) and a completed `codex login`.
- No API key required for this skill; the codex session reuses whatever auth Codex stores in `~/.codex/auth.json`.
- **Requires codex `0.144.1`+** (`npm install -g @openai/codex@latest`). Two dead zones below that, both verified 2026-07-12: `0.140.0`–`0.143.x` shipped a regression ([openai/codex#28422](https://github.com/openai/codex/issues/28422)) where `image_gen` produces a valid PNG but never saves it to disk (fixed in `0.144`); and the old `0.139.0` pin this skill used to mandate is now ALSO broken, because the account's configured default model (`gpt-5.6-terra` in `~/.codex/config.toml`) rejects old CLIs with "requires a newer version of Codex". The failure is silent either way — the wrapper's `set -e` exits 1 with no output — so trust the wrapper's version warning, not the empty log. Do NOT re-pin to 0.139.

## Bundled Assets

The `assets/` folder contains reference images (reference1-4.png) that define the excalidraw style — these are now **dark-mode** examples (extracted from the Loops deck). The wrapper attaches them automatically on every call. All 8 source dark images live in `assets/dark-source/`; the previous white-background refs are preserved in `assets/white-backup/`.
