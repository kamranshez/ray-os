---
name: excalidraw-gemini
description: Generate excalidraw-style explanation images using the Gemini API (gemini-3-pro-image-preview). Use when the user wants to create visual explanations, diagrams, or illustrations in the hand-drawn excalidraw aesthetic via the Gemini path. Supports parallel generation of multiple variations with configurable timeout. Triggers ONLY when the user explicitly asks for the Gemini route ("generate an excalidraw image with gemini", "excalidraw-gemini", "use gemini for excalidraw"). Sibling skill [[excalidraw-codex]] does the same job through the `codex exec` headless CLI with no API key, and is the RECOMMENDED DEFAULT. Prefer codex unless the user explicitly names Gemini.
---

## Engine

This skill calls the **Gemini API** (`gemini-3-pro-image-preview`) via a bundled Node/TypeScript script. Requires `GEMINI_API_KEY` in `.env`.

For the **Codex CLI** path (no API key, uses Codex's bundled `image_gen` tool, often faster), see [[excalidraw-codex]] instead.

## Prompt Content Rule — CRITICAL

**ALWAYS pass the entire raw content verbatim as the prompt.** Never summarize, paraphrase, or condense the content. Whether it's a single section or a whole file, the full text goes into the generate command as-is (with the dark background prefix/suffix wrapped around it). This gives Gemini the richest context to produce accurate visuals.

## Output Location — CRITICAL

**All generated images go into the single vault-root `images/` folder — flat, no per-note subfolders.** This matches the vault's image convention (see the repo CLAUDE.md). Concretely, for this vault: `-o /Users/ray/Desktop/ray-os/images`.

- Name every set with a **globally-unique kebab-case slug** via `-x <slug>` so files never collide in the flat folder. Include the class/note in the slug, e.g. `-x loopy-intro-loop-stack` → produces `loopy-intro-loop-stack-1.png … -10.png`.
- Embeds are **filename-only** wikilinks: `![[loopy-intro-loop-stack-1.png]]` (no path). Because every name is unique and the folder is flat, these resolve from any note and survive note moves.
- Do **not** create `images/<section>/` subfolders.

## Semantic Chunking

Don't chunk solely by `## ` headings. Look for:
- Concept definitions ("What is X?", "X are the boundaries where...")
- Distinct examples or scenarios
- Shifts in topic within a section
- Before/after comparisons
- Standalone explanations (like "**What are contracts?**" paragraphs)

Each chunk = one image. A single `## ` section might produce 2-4 chunks if it covers multiple concepts. When analyzing content, identify these semantic boundaries first, then generate images for each chunk.

---

## First: Ask the User

Before generating, ask the user which mode they want:

1. **Specific section** — Generate images for one section only (user provides the content)
2. **Whole file** — Parse a markdown file into `## sections`, generate images for ALL sections in parallel using subagents

Use AskUserQuestion with options:
- "Specific section" — I'll generate images for content you provide
- "Whole file" — I'll split the file by ## headings and generate for all sections in parallel

## Mode 1: Specific Section

For a single section:

1. Get the section content from the user
2. Pick a globally-unique kebab-case slug (class + note + section, e.g. `loopy-intro-loop-stack`)
3. Run the generate command, passing the **entire section content verbatim** as the prompt (never summarize), outputting into the vault-root `images/` folder:

```bash
cd .claude/skills/excalidraw-gemini && npx ts-node scripts/generate.ts "<entire section content verbatim>" -n 10 -o "/Users/ray/Desktop/ray-os/images" -x "<unique-slug>"
```

4. Add all 10 image embeds to the markdown after the section (see "Adding Image Embeds" below)

## Mode 2: Whole File (Batched)

For an entire markdown file:

1. Read the file and split by `## ` headings (or semantic chunks)
2. **Process in batches of 2** to avoid Google API rate limits:
   - Launch 2 background Bash tasks at a time
   - Wait for both to complete before starting the next batch
   - Repeat until all sections are done
3. For each section, spawn a **background subagent** (Bash type) to generate images:
   - Output dir: the vault-root `images/` folder (`-o /Users/ray/Desktop/ray-os/images`)
   - Name: `-x <unique-section-slug>` (class + note + section, so files never collide)
   - Prompt: The **entire section content verbatim** — NEVER summarize, always pass the full raw text
   - Use `run_in_background: true`
4. Add all 10 image embeds after each section in the markdown (see "Adding Image Embeds" below)

**Rate limit constraint:** Never run more than 2 generation tasks simultaneously. The Gemini API will rate-limit if you exceed this.

**Subagent template:**
```
Run this bash command (timeout 900000ms):
cd "/path/to/.claude/skills/excalidraw-gemini" && npx ts-node scripts/generate.ts "<entire section content verbatim>" -n 10 -o "/Users/ray/Desktop/ray-os/images" -x "<unique-section-slug>"
```

**Batch workflow:**
```
Batch 1: section-1, section-2 → wait for completion
Batch 2: section-3, section-4 → wait for completion
...continue until done
```

## Generate Command

```bash
cd .claude/skills/excalidraw-gemini && npx ts-node scripts/generate.ts <prompt> [options]
```

**Prompt requirements — CRITICAL:**
- **START every prompt with:** `"CRITICAL: Use a near-black dark charcoal background (#0E1116) — dark mode. Solid dark only, no gradients, no textures. Chalk-style off-white lines and light labels, soft glowing accent colors."`
- This instruction MUST appear at the very beginning of the prompt, before any content description
- The excalidraw dark-mode style requires a consistent near-black background — Gemini tends to drift to white/gradient backgrounds if not explicitly forbidden
- Reinforce at the end: `"Background must be solid near-black charcoal (#0E1116), nothing else."`

**Options:**
- `-n, --count` — Number of images (default: 5, recommend 10)
- `-o, --output` — Output directory (the vault-root `images/` folder)
- `-x, --name <slug>` — Basename for saved files (default `excalidraw`). Output is `<slug>-1.png`, `<slug>-2.png`, … Always pass a globally-unique slug so files don't collide in the flat folder.
- `-t, --timeout` — Timeout per image in seconds (default: 180)
- `-a, --aspect-ratio` — Aspect ratio (default: 16:9). Supported: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
- `--image-size` — Image size hint (default: 2K)

## X Article Thumbnails

For X/Twitter article cover images, use **21:9** (the closest supported ratio to 5:2). X articles display cover images in a wide cinematic format.

```bash
cd .claude/skills/excalidraw-gemini && npx ts-node scripts/generate.ts "<prompt>" -n 5 -a 21:9 -o "/Users/ray/Desktop/ray-os/images" -x "<unique-slug>"
```

Use a bold, high-contrast design with minimal text (3-5 words max). The image must be readable at small sizes in the X feed. Skip the dark background instruction for thumbnails — use vibrant colors instead.

## Adding Image Embeds

After generation completes, add **all 10 images** to the markdown file under the relevant section. The user picks their favorite(s) later.

**Embed format (Obsidian) — filename-only, no path:**
```markdown
![[<slug>-1.png]]
![[<slug>-2.png]]
![[<slug>-3.png]]
![[<slug>-4.png]]
![[<slug>-5.png]]
![[<slug>-6.png]]
![[<slug>-7.png]]
![[<slug>-8.png]]
![[<slug>-9.png]]
![[<slug>-10.png]]
```

Place embeds at the end of each section, before the next `---` or `##` heading.

## Important Notes

- **No overwrites:** Script auto-increments filenames if images exist
- **Flat vault-root folder:** all images land directly in the vault-root `images/` folder — never per-note subfolders. Uniqueness comes from the `-x` slug, not from a folder path.
- **Embed all 10:** Always add all 10 images per section so the user can pick their favorite
- **Timeout:** Allow 15 minutes for generation. Use 900000ms timeout for subagents and Bash calls.

## Requirements

- Node.js with dependencies installed (`npm install` in skill folder)
- `GEMINI_API_KEY` in `.env` file (already configured)

## Bundled Assets

The `assets/` folder contains reference images (reference1-4.png) that define the excalidraw style — these are now **dark-mode** examples (extracted from the Loops deck). They load automatically. The previous white-background refs are preserved in `assets/white-backup/`.
