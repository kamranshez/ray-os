---
name: excalidraw-gen
description: Generate excalidraw-style explanation images using Gemini API. Use when the user wants to create visual explanations, diagrams, or illustrations in the hand-drawn excalidraw aesthetic. Supports parallel generation of multiple variations with configurable timeout. Triggers on requests like "generate an excalidraw image", "create a visual explanation", "make a diagram for [concept]", or "illustrate [topic] in excalidraw style".
---

## Prompt Content Rule — CRITICAL

**ALWAYS pass the entire raw content verbatim as the prompt.** Never summarize, paraphrase, or condense the content. Whether it's a single section or a whole file, the full text goes into the generate command as-is (with the white background prefix/suffix wrapped around it). This gives Gemini the richest context to produce accurate visuals.

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
2. Create a descriptive subfolder name (kebab-case from section title)
3. Run the generate command, passing the **entire section content verbatim** as the prompt (never summarize):

```bash
cd .claude/skills/excalidraw-gen && npx ts-node scripts/generate.ts "<entire section content verbatim>" -n 10 -o "/path/to/images/<section-name>"
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
   - Subfolder: `images/<section-name-kebab-case>/`
   - Prompt: The **entire section content verbatim** — NEVER summarize, always pass the full raw text
   - Use `run_in_background: true`
4. Add all 10 image embeds after each section in the markdown (see "Adding Image Embeds" below)

**Rate limit constraint:** Never run more than 2 generation tasks simultaneously. The Gemini API will rate-limit if you exceed this.

**Subagent template:**
```
Run this bash command (timeout 900000ms):
cd "/path/to/.claude/skills/excalidraw-gen" && npx ts-node scripts/generate.ts "<entire section content verbatim>" -n 10 -o "/path/to/images/<section-name>"
```

**Batch workflow:**
```
Batch 1: section-1, section-2 → wait for completion
Batch 2: section-3, section-4 → wait for completion
...continue until done
```

## Generate Command

```bash
cd .claude/skills/excalidraw-gen && npx ts-node scripts/generate.ts <prompt> [options]
```

**Prompt requirements — CRITICAL:**
- **START every prompt with:** `"CRITICAL: Use a plain white background (#FFFFFF). No gradients, no colors, no textures — pure white only."`
- This instruction MUST appear at the very beginning of the prompt, before any content description
- The excalidraw style requires a clean white background — Gemini tends to add colored/gradient backgrounds if not explicitly forbidden
- Reinforce at the end: `"Background must be solid white (#FFFFFF), nothing else."`

**Options:**
- `-n, --count` — Number of images (default: 5, recommend 10)
- `-o, --output` — Output directory (use subfolder per section)
- `-t, --timeout` — Timeout per image in seconds (default: 180)
- `-a, --aspect-ratio` — Aspect ratio (default: 16:9). Supported: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
- `--image-size` — Image size hint (default: 2K)

## X Article Thumbnails

For X/Twitter article cover images, use **21:9** (the closest supported ratio to 5:2). X articles display cover images in a wide cinematic format.

```bash
cd .claude/skills/excalidraw-gen && npx ts-node scripts/generate.ts "<prompt>" -n 5 -a 21:9 -o "/path/to/images/<slug>"
```

Use a bold, high-contrast design with minimal text (3-5 words max). The image must be readable at small sizes in the X feed. Skip the white background instruction for thumbnails — use vibrant colors instead.

## Adding Image Embeds

After generation completes, add **all 10 images** to the markdown file under the relevant section. The user picks their favorite(s) later.

**Embed format (Obsidian):**
```markdown
![[images/section-name/excalidraw_1.png]]
![[images/section-name/excalidraw_2.png]]
![[images/section-name/excalidraw_3.png]]
![[images/section-name/excalidraw_4.png]]
![[images/section-name/excalidraw_5.png]]
![[images/section-name/excalidraw_6.png]]
![[images/section-name/excalidraw_7.png]]
![[images/section-name/excalidraw_8.png]]
![[images/section-name/excalidraw_9.png]]
![[images/section-name/excalidraw_10.png]]
```

Place embeds at the end of each section, before the next `---` or `##` heading.

## Important Notes

- **No overwrites:** Script auto-increments filenames if images exist
- **Subfolders:** Always use a descriptive subfolder per section (e.g., `images/core-insight/`, `images/kitchen-sink/`)
- **Embed all 10:** Always add all 10 images per section so the user can pick their favorite
- **Timeout:** Allow 15 minutes for generation. Use 900000ms timeout for subagents and Bash calls.

## Requirements

- Node.js with dependencies installed (`npm install` in skill folder)
- `GEMINI_API_KEY` in `.env` file (already configured)

## Bundled Assets

The `assets/` folder contains reference images (reference1-4.png) that define the excalidraw style. These load automatically.
