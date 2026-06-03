---
name: excalidraw-codex
description: Generate excalidraw-style explanation images using the Codex CLI (codex exec --json) instead of a paid API. Use when the user wants visual explanations, diagrams, or illustrations in the hand-drawn excalidraw aesthetic and asks for the codex path. Codex's bundled image_gen tool runs through the logged-in account, so no GEMINI_API_KEY is required and it's often faster than the Gemini route. Triggers on "generate an excalidraw image with codex", "excalidraw-codex", "use codex for excalidraw", or when the user explicitly asks for the codex/headless route. Sibling skill [[excalidraw-gemini]] does the same job through the Gemini API — default to whichever variant the user names; if unspecified, ask.
---

## Engine

This skill drives the **Codex CLI** in headless mode (`codex exec --skip-git-repo-check --json`) and lets Codex's bundled `image_gen` tool produce the images. Reference images attach via `-i <file>` flags. The CLI must already be authenticated (`codex login` was run once).

For the **Gemini API** path (uses `gemini-3-pro-image-preview` via `GEMINI_API_KEY`), see [[excalidraw-gemini]] instead.

## Prompt Content Rule — CRITICAL

**ALWAYS pass the entire raw content verbatim as the prompt.** Never summarize, paraphrase, or condense the content. Whether it's a single section or a whole file, the full text goes into the wrapper as-is. This gives the model the richest context to produce accurate visuals. The wrapper script wraps the verbatim text with headless directives and aesthetic guidance — do not pre-wrap or rewrite it yourself.

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
2. Create a descriptive subfolder name (kebab-case from section title).
3. Run the wrapper, passing the **entire section content verbatim** as the `-p` prompt (never summarize):

```bash
.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<entire section content verbatim>" \
  -o "/path/to/images/<section-name>" \
  -n 5
```

4. The wrapper prints absolute paths of every PNG it saved. Add embeds to the markdown after the section (see "Adding Image Embeds" below).

## Mode 2: Whole File (Parallel)

For an entire markdown file:

1. Read the file and split into semantic chunks (see "Semantic Chunking").
2. **Process up to 5 chunks in parallel.** The Codex CLI's `image_gen` tool serializes per-session, so to get throughput we launch separate `codex exec` calls — each its own session UUID.
3. For each chunk, run the wrapper in a **background Bash task** (`run_in_background: true`):
   - Output dir: `images/<chunk-slug>/`
   - Prompt: the **entire chunk content verbatim**
4. Wait for the whole batch, then add all embeds.

**Why 5 instead of 2:** unlike the Gemini API there is no shared rate-limit gateway to worry about — the bottleneck is whatever the codex account allows. Stay polite at 5 concurrent and back off if you see auth or quota errors in the JSONL stream.

**Subagent template:**
```
Run this bash command (timeout 900000ms):
/Users/ray/Desktop/ray-os/.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<entire chunk content verbatim>" \
  -o "/path/to/images/<chunk-slug>" \
  -n 5
```

## Wrapper Command Reference

```bash
generate.sh -p "<verbatim prompt>" -o /abs/out/dir [options]
```

**Options:**
- `-n, --count` — Number of variations per call (default 5). Codex produces N images in a single session.
- `-a, --aspect` — Aspect ratio hint embedded in the prompt (default `16:9`). Codex doesn't expose ratio flags directly; the wrapper inlines this into the directive.
- `-r, --ref <file>` — Add an extra reference image. Repeatable. The wrapper auto-attaches every `reference*.png` from `assets/` unless `--no-default-refs` is passed.
- `--no-default-refs` — Skip the bundled `assets/reference*.png` images (use only `-r` files).

**Defaults baked into the wrapper:**
- `codex exec --skip-git-repo-check --json` — headless, JSONL events on stdout.
- Auto-attaches `assets/reference1.png` … `reference4.png` so the model copies the cute light-blue robot and sketchy aesthetic.
- Prompt is wrapped with: "Do not load skills, do not read files, do not copy outputs — call `image_gen` N times in this single turn and list the saved paths." This is necessary because, left alone, the Codex agent auto-loads `~/.codex/skills/imagegen` and burns ~150k tokens reading skill markdown and copying outputs around.
- Pure white background and excalidraw aesthetic directives are inlined in the wrapper prompt.

**Where the images land:**
- Codex writes each PNG to `~/.codex/generated_images/<thread_id>/ig_<hash>.png` first.
- The wrapper reads the `thread_id` from the first JSONL event, then copies every PNG from that session dir into your `-o` directory as `excalidraw_1.png`, `excalidraw_2.png`, … (auto-incremented; no overwrites).

## X Article Thumbnails

For X/Twitter article cover images use `-a 21:9`:

```bash
.claude/skills/excalidraw-codex/scripts/generate.sh \
  -p "<thumbnail prompt with bold 3-5 word text>" \
  -o "/path/to/images/<slug>" \
  -n 5 -a 21:9
```

For vibrant brand-colored thumbnails (not the white-background look), pass `--no-default-refs` so the bundled excalidraw refs don't pull the result back toward sketchy white.

## Adding Image Embeds

After generation completes, add **all N images** to the markdown file under the relevant section. The user picks their favorite(s) later.

**Embed format (Obsidian):**
```markdown
![[images/section-name/excalidraw_1.png]]
![[images/section-name/excalidraw_2.png]]
![[images/section-name/excalidraw_3.png]]
![[images/section-name/excalidraw_4.png]]
![[images/section-name/excalidraw_5.png]]
```

Place embeds at the end of each section, before the next `---` or `##` heading.

## Important Notes

- **No overwrites:** wrapper increments `excalidraw_N.png` to the next free number.
- **Subfolders:** always use a descriptive subfolder per section (`images/core-insight/`, `images/kitchen-sink/`).
- **Embed every variation:** drop all N into the markdown so the user can pick.
- **Timeout:** allow 15 minutes per call (use `timeout: 900000` on Bash invocations).
- **Aspect ratio is advisory only on this path.** Codex's `image_gen` tool decides the final dimensions — output tends to land near 16:9 (~1672×941). If you need pixel-exact ratios, prefer [[excalidraw-gemini]] which has true `-a` control.

## Requirements

- `codex` CLI on PATH (`brew install codex` or via OpenAI installer) and a completed `codex login`.
- No API key required for this skill; the codex session reuses whatever auth Codex stores in `~/.codex/auth.json`.

## Bundled Assets

The `assets/` folder contains reference images (reference1-4.png) that define the excalidraw style. The wrapper attaches them automatically on every call.
