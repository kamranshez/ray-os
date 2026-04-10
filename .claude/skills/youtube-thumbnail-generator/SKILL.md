---
name: youtube-thumbnail-generator
description: Generate YouTube thumbnails using Gemini Nano Banana 2 image generation with face references for consistent likeness. Two modes — research competitor thumbnails by keyword, or generate thumbnail variations for an upcoming video. Use when the user wants to create thumbnails, research thumbnail styles, find competing thumbnails, generate thumbnail ideas, or anything related to YouTube thumbnail creation. Triggers on "generate a thumbnail", "make a thumbnail", "thumbnail ideas", "find thumbnails for", "research thumbnails", "thumbnail variations", or any YouTube thumbnail request.
---

## Workflow Overview

The thumbnail workflow is iterative: research → generate → feedback → regenerate.

1. **Research** competitors (or use provided competitor data)
2. **Generate** thumbnails using 1 competitor reference per generation for maximum variety
3. **Open Streamlit app** for the user to rate, favorite, and leave comments
4. **Regenerate** from feedback — read `feedback.json` and incorporate user notes
5. **Repeat** until user has a winner

---

## Output Organization

All generated thumbnails are stored by video title (kebab-case) with descriptive names:

```
output/
  <video-title-kebab>/
    folder-ultraplan-a.png
    folder-ultraplan-b.png
    icons-ultraplan-a.png
    ...
```

**Before generating, always ask for the video title** so you can create a properly named folder. This keeps history organized by video, not by opaque video IDs.

The `output/` folder is gitignored (large generated images).

---

## Golden References

Golden references are previously successful outputs that already have Ray's likeness baked in. They produce much more consistent results than raw Nate Herk references because the model has less to reconcile between face ref + style ref.

```
research/golden-references/
  folder-command.png              ← best folder + /command style (contemplative)
  folder-command-smiling.png      ← best folder + /command style (smiling/pointing)
  folder-command-closeup.png      ← best folder + /command style (close-up crop)
  icons-black.png                 ← best icons on black style
  old-vs-new.png                  ← best comparison style
  cli-chat.png                    ← best CLI terminal style
  ...
```

**Golden refs should be saved per style AND per expression/crop.** For example, the folder style has multiple golden refs:
- `folder-command.png` — contemplative, medium shot
- `folder-command-smiling.png` — smiling/pointing, medium shot  
- `folder-command-closeup.png` — close-up face crop (used for ultraplan/ultrareview)

When the user asks for "same as X but different text", use the golden ref that matches the exact composition — not just the style category. Save the best output from each video as a new golden ref if it improves on the existing one.

### How Golden References Work

1. **One-time setup per style**: Generate a thumbnail using a Nate Herk reference. When the result is good, copy it to `research/golden-references/` with a descriptive name.
2. **All future generations use golden refs**: Instead of the raw Nate Herk image, pass the golden reference as `-r`. The output will match Ray's established look much more closely.
3. **Update golden refs when you get a better one**: If a new generation is even better, replace the golden reference.

### Generation Workflow (V16)

1. **Ask for video title** → create `output/<video-title-kebab>/`
2. **Check `research/golden-references/`** — if golden refs exist for the styles you need, use those
3. **If no golden ref exists for a style** — fall back to the Nate Herk reference, then save the best result as a new golden reference
4. **Generate variations** using golden refs (3 variants per style, 10 parallel)
5. After generation, rename and consolidate into the video folder

---

## Feedback System

`feedback.json` is the single source of truth for user preferences.

### Structure

```json
{
  "preferred_style": {
    "name": "GitHub repo card",
    "description": "...",
    "reference": "<competitor-video-id>",
    "example": "<video-id>/<filename>.png"
  },
  "global_feedback": {
    "facial_expressions": "Keep expressions modest and natural — no exaggerated shock/surprise. Contemplative, serious, or subtly concerned work best.",
    "hairstyle": "Don't make hair too curly — keep it natural to the reference photos."
  },
  "<video-id>/<filename>.png": {
    "favorite": true,
    "rating": 5,
    "comment": "Feedback text here"
  }
}
```

- **preferred_style** — The user's go-to style for future generations
- **global_feedback** — Cross-cutting rules that apply to ALL future generations. Always read these before generating.
- **Per-thumbnail entries** — Ratings, favorites, and specific comments

### Reading Feedback Before Generating

Before every generation run:
1. Read `feedback.json`
2. Apply all `global_feedback` rules to every prompt (e.g., modest expressions, natural hair)
3. Check `preferred_style` to know the default style reference
4. If regenerating from comments, incorporate per-thumbnail feedback into the new prompts

---

## YouTube Lab (Streamlit App)

The centralized app for all thumbnail management — generation tracking, review/shortlisting, uploads, and A/B test results.

Launch with:
```bash
cd .claude/skills/youtube-thumbnail-generator/lab && streamlit run app.py --server.port 8503
```

The app has 3 pages:
- **Dashboard** — All videos as cards sorted by publish date, status badges, progress bar, export tools
- **Review** — Pick a video, see thumbnails with reference images, click to shortlist (max 5), mark as uploaded
- **Results** — Record A/B test watch-time % and winners after 7 days, summary table

**Data:** `lab/data.json` — single source of truth for all video state. Supports `output_folder` field for videos with custom output directory names.

Open in browser after launching:
```bash
open http://localhost:8503
```

---

## Key Rule: 1 Competitor Reference Per Generation

**CRITICAL**: Never pass multiple competitor thumbnails as references to a single generation. This causes styles to "wash out" into a generic average.

Instead:
- Pick 10 different competitors
- Run 10 separate generations, each with `-r <single-competitor.jpg>`
- Each output will have a distinct style matching its inspiration
- Use separate output directories per batch to avoid filename collisions

For parallel generation, run up to 5 Bash commands simultaneously, each generating 1-2 thumbnails in its own output directory.

---

## Mode 1: Research Thumbnails

The user will specify where to pull competitor references from. There are four sources:

### From a Specific Channel (when user provides a channel URL)

When the user provides a YouTube channel URL (e.g., `https://www.youtube.com/@nateherk/videos`), scrape that channel's recent thumbnails directly.

**Steps:**

1. Use `yt-dlp` to get recent video IDs and titles:
   ```bash
   yt-dlp --flat-playlist --print "%(id)s %(title)s" "<channel-url>" --playlist-end 15
   ```
2. Create the output directory:
   ```bash
   mkdir -p research/competitor-thumbnails/
   ```
3. Download maxresdefault thumbnails for each video:
   ```bash
   curl -sL "https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg" -o "research/competitor-thumbnails/<VIDEO_ID>.jpg"
   ```
4. Visually inspect each thumbnail using the Read tool
5. Write a style analysis summarizing the channel's patterns (face placement, text style, colors, props, layout)

This is the fastest method and produces the most cohesive style reference set since all thumbnails come from one creator's visual identity.

### Auto-Scrape from YouTube Studio

The best competitor data from Ray's own audience comes from YouTube Studio's "What your audience watches" section. Use browser automation to scrape it automatically.

**YouTube Studio Analytics URL:**
```
https://studio.youtube.com/channel/UCLA7cJBnqr0nLF2bQBD9uUg/analytics/tab-build_audience/period-default
```

**Steps:**

1. Use Chrome browser automation (mcp__claude-in-chrome) or Playwright to navigate to the URL above
2. Wait for the "What your audience watches" section to load
3. Click through all pages (look for pagination like "1/3" with arrow buttons) to get all videos
4. For each video entry, extract:
   - Video title
   - Channel name
   - View count
   - Thumbnail image URL (contains the video ID: `https://i.ytimg.com/vi/<VIDEO_ID>/mqdefault.jpg`)
5. Extract video IDs from thumbnail URLs
6. Download maxresdefault thumbnails for each:
   ```bash
   curl -sL "https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg" -o "research/competitor-thumbnails/<VIDEO_ID>.jpg"
   ```
7. Store in `research/competitor-thumbnails/`
8. Visually inspect each thumbnail using the Read tool
9. Write analysis to `research/analysis.md`

**Scraping tips:**
- The page uses shadow DOM / web components — use `get_page_text` or `read_page` to extract the data
- Look for elements with class `yta-audience-interests-card` for the video cards
- Each card has a thumbnail `<img>` with the video ID embedded in the src URL
- Pagination arrows are at the bottom of each card group — click "next" to load more
- The user must be logged in to YouTube Studio already in their browser

### From User-Provided HTML/Data

When the user copies and pastes HTML from YouTube Analytics:

1. Extract video IDs from the HTML (look for `src="https://i.ytimg.com/vi/<ID>/..."`)
2. Download thumbnails via curl
3. Store in `research/competitor-thumbnails/`

### From Keyword Search

Use the supadata skill:
```bash
python3 .claude/skills/supadata/scripts/supadata.py batch-thumbnails "<query>" --max 15 --out-dir research/competitor-thumbnails
```

### Analysis Framework

Read `references/thumbnail-analysis.md` for the outlier framework. Key patterns to identify:
- Face vs no-face usage and which performs better
- Text approach (word count, font style, placement)
- Color palette and background style
- Composition patterns
- What makes the top-viewed thumbnails stand out

---

## Mode 2: Generate Thumbnail Variations

### The V15 Standard (ALWAYS follow this)

**CRITICAL: Do NOT use subagents for ANY part of thumbnail generation.** Subagents lose context about prompt quality, reference matching, and transcript details. All prompt writing and generation must happen in the main session.

#### Core Rules

1. **Ask for the video title FIRST** — create `output/<video-title-kebab>/` folder
2. **Fetch the transcript** — use supadata to get the full video transcript before writing any prompts
3. **Read `feedback.json`** for global feedback rules and preferred style
4. **Use golden references first** — check `research/golden-references/` for existing proven outputs. Only fall back to Nate Herk references from `research/competitor-thumbnails/nateherk/` if no golden ref exists for that style.
5. **Visually inspect each reference** before writing its prompt — use the Read tool to see the actual image, then describe its exact visual composition
6. **Write each prompt yourself** — describe the EXACT visual layout of the reference, only changing the text/topic to match the video content. Do NOT get creative with composition — match the reference precisely.
7. **3 variants per reference** — generate 3 slightly different prompts per reference (vary the text overlay and minor details, keep composition identical)
8. **Generate with `-n 1`** (one image per run, NOT `-n 2`)
9. **Run 10 parallel generations** per batch (Gemini API handles this)
10. **Isolate face reference** — move all photos except `go-to-face.jpg` out of `assets/face/` before generating, restore after

#### Steps

1. **Ask for video title** → create `output/<video-title-kebab>/`
2. Get the video URL and fetch transcript via supadata
3. Read `feedback.json` for global feedback rules
4. Read the transcript thoroughly — identify key concepts, features, emotional hooks
5. **Check golden references** — list `research/golden-references/` and visually inspect relevant ones
6. For styles without a golden ref, visually inspect the Nate Herk reference instead
7. For each reference (golden or Nate Herk), craft 3 prompts that:
   - **Match the exact visual composition** of the reference (person LEFT or RIGHT, prop position, background type)
   - Only change the text/topic to match the video's content
   - Use the proven person description (see Prompt Template below)
   - Follow all global feedback rules
8. Isolate `go-to-face.jpg` (move others to `assets/face-backup/`)
9. Generate directly into the final output folder using `--name`:

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts "<prompt>" \
  -n 1 -o "output/<video-title-kebab>" \
  --name "folder-<concept>-a" \
  -r "research/golden-references/<style>.png"  # or nateherk/<ref-id>.jpg if no golden ref
```

For clone-mode (same thumbnail, different text):
```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts \
  --clone "output/<source-video>/folder-<source>-golden-ref.jpeg" \
  --text "/newcommand" \
  --name "folder-<newcommand>-contemplative" \
  -n 1 -o "output/<video-title-kebab>"
```

10. **Save best outputs as golden refs** — if a generation produced a great result for a style that has no golden ref yet, copy it to `research/golden-references/` with a descriptive name including the expression/crop type
11. Restore face photos from backup
12. **Auto-open the output folder** — always run `open output/<video-title-kebab>/` in Finder after generation so the user can review immediately

### 11 Curated Nate Herk Reference Styles

These are Ray's hand-picked references from `research/competitor-thumbnails/nateherk/`. Archived refs are in `nateherk/archived/` if needed later.

| # | File | Style | Face? |
|---|------|-------|-------|
| 1 | `OUyfxhFtGCo.jpg` | Folder + `/command` + pointing | Yes |
| 2 | `X6EGzi9qm3E.jpg` | Folder + `/command` + smiling | Yes |
| 3 | `LrgfmZkl3nc.jpg` | Icons on black + bold statement | **No** (`--no-face`) |
| 4 | `Wu67lLD8bB0.jpg` | Icons on black + short phrase | **No** (`--no-face`) |
| 5 | `mpALXah_PBg.jpg` | Whiteboard numbered list + face | Yes |
| 6 | `BlNJFa3Btm8.jpg` | CLI chat input + "Game Over" style | Yes |
| 7 | `vDVSGVpB2vc.jpg` | Folder + agent network diagram | Yes |
| 8 | `1EPsUXSManU.jpg` | Pixel art agent diagram + face | Yes |
| 9 | `27Y44JYXZJ8.jpg` | Dark terminal agent network + face | Yes |
| 10 | `sboNwYmH3AY.jpg` | Icons on black (Claude + second app) | **No** (`--no-face`) |
| 11 | `B2Kh_ZoLVTM.jpg` | Icons on black (Claude + Codex) | **No** (`--no-face`) |

When generating a subset (e.g., 5 of 11), randomly select different ones per video for variety.

### Matt Pocock Reference Styles

A second reference set from `research/competitor-thumbnails/mattpocockuk/`. Matt's style is distinct from Nate Herk — warm room lighting, podcast mic visible, educational diagrams with red curved arrow annotations, and handwritten-style text. His top videos get 200K+ views.

**Key styles (all have face + podcast mic on RIGHT):**

| # | File | Style | Views |
|---|------|-------|-------|
| 1 | `EJyuu6zlQCg.jpg` | Slash command list + "(my favourite)" annotation | 238K |
| 2 | `kZ-zzHVUrO4.jpg` | Terminal window + "MY FAVORITE CODING AGENT" | 240K |
| 3 | `hX7yG1KVYhI.jpg` | Checklist + "Watch Me Work" | 80K |
| 4 | `WNx-s-RxVxk.jpg` | Flowchart cycle diagram + bold text bottom | 52K |
| 5 | `Ah9p7v7nJWg.jpg` | Two-column flow diagram (phases/steps) | 35K |
| 6 | `9tmsq-Gvx6g.jpg` | Big command text + "Don't run this!" | 60K |
| 7 | `hYZdIwFIy-c.jpg` | Numbered steps (1/2/3) + holding book | 38K |
| 8 | `uC44zFz7JSM.jpg` | Colored grid diagram + "Is this your codebase?" | 65K |
| 9 | `yv8VZpov8bk.jpg` | Tweet screenshot + contemplative face | 72K |
| 10 | `9VNG0h4pLh0.jpg` | AI logos + red arrows + "LIARS" | 32K |

**When to use Matt Pocock refs vs Nate Herk:** Use Matt's style when the thumbnail needs educational diagrams, flowcharts, numbered steps, or slash command lists. Use Nate Herk for folder/icon/studio styles.

**IMPORTANT: Diagrams should look hand-drawn/excalidraw-style** — NOT clean vector/polished boxes. Matt's diagrams have a casual, sketched quality. When writing prompts for diagram thumbnails, specify "hand-drawn excalidraw-style" or "sketched whiteboard-style" for the diagram elements.

### Prompt Construction

**CRITICAL**: You MUST visually inspect (Read tool) each Nate Herk reference image before writing its prompt. Describe the exact layout you see — don't guess from the style name.

**The key insight**: Describe the EXACT visual composition of the reference image, then only swap the text/topic for the video's content. Do NOT add extra conceptual elements or get creative with layout — the reference's layout IS the prompt structure.

#### Proven Person Description (use this exact phrasing for face thumbnails)

```
a young South Asian man with glasses and naturally straight dark hair — not curly, not wavy
(matching the reference photos exactly) — with a [EXPRESSION]
```

Expressions that work:
- **Folder styles**: "warm enthusiastic smile showing teeth, pointing at the folder"
- **CLI styles**: "big warm smile showing teeth"
- **Whiteboard/agent styles**: "warm enthusiastic smile showing teeth"
- **Network/terminal styles**: "contemplative serious expression"

#### Proven Prompt Template (with-face styles)

```
A YouTube thumbnail in the style of the reference image. [BACKGROUND from reference — e.g. "Clean gray studio background" or "Dark background with faint code editor elements"].
On the [LEFT/RIGHT — match reference], [PROP DESCRIPTION — e.g. "a large manila folder with an orange-red rounded-square app icon featuring a white 8-pointed starburst and bold black text '/command-here'"].
On the [OTHER SIDE], a young South Asian man with glasses and naturally straight dark hair — not curly, not wavy (matching the reference photos exactly) — with a [EXPRESSION from list above].
[Any additional reference-specific elements — badges, icons with X/checkmarks, etc.]
Clean minimal composition optimized for YouTube thumbnail viewing.
```

#### Proven Prompt Template (no-face styles — refs #3, #4, #10, #11)

```
A YouTube thumbnail in the style of the reference image. Pure black background.
Large white bold text at the top reading '[VIDEO-SPECIFIC TEXT].' with a subtle chalk-style underline scribble.
Below, two large rounded-square app icons side by side with a white '+' between them:
on the left an orange-red rounded square with a white 8-pointed starburst icon,
on the right a dark rounded square with a [TOPIC-RELEVANT ICON] and subtle warm glow.
No person in the image. Clean minimal composition optimized for YouTube thumbnail viewing.
```

Add `--no-face` flag for refs #3, #4, #10, and #11.

#### What NOT to do
- Do NOT add code backgrounds, busy conceptual diagrams, or extra elements not in the reference
- Do NOT describe "a flowchart showing X → Y → Z" unless the reference literally shows a flowchart
- Do NOT use generic descriptions — be specific about LEFT/RIGHT positioning, icon styles, text placement
- Do NOT delegate prompt writing to subagents — they lose context about visual composition

### Naming Convention

Name files descriptively based on their concept. Use `-a`, `-b`, `-c` suffixes for the 3 variants per reference:
- `folder-skills-strategy-a.png` — Folder /command style, variant a
- `folder-skills-strategy-b.png` — Folder /command style, variant b (different text)
- `folder-skills-strategy-c.png` — Folder /command style, variant c (different text)
- `icons-override-defaults-a.png` — Icons on black style
- `cli-boring-works-a.png` — CLI terminal style

---

## Mode 3: Regenerate from Feedback

When the user says "regenerate from feedback":

1. Read `feedback.json`
2. Find all thumbnails with non-empty comments
3. For each, construct a new prompt that:
   - Keeps what the user liked (e.g., "background is great")
   - Fixes what they didn't like (e.g., "facial reaction too extreme")
   - Applies global feedback rules
4. Generate into `output/<video-id>/` with a `-v2` suffix on the name
5. Update Streamlit app

---

## Generate Command Reference

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts <prompt> [options]
```

**Options:**
- `-n, --count` — Number of images (default: 5)
- `-o, --output` — Output directory (created automatically if it doesn't exist)
- `-t, --timeout` — Timeout per image in seconds (default: 180)
- `-r, --reference` — Single competitor reference image (use ONE per generation)
- `--no-face` — Skip loading face reference images
- `--text` — Text to render on the thumbnail (passed separately for stronger emphasis on exact spelling)
- `--name` — Output filename (without .png). Saves directly as `<output>/<name>.png` instead of `thumbnail_N.png`. For multiple images, appends `-1`, `-2`, etc.
- `--clone` — Clone mode: pass an existing thumbnail to recreate with different text. Auto-constructs the prompt. Requires `--text`.
- `--system-prompt` — Override the default system prompt

The script automatically loads face reference images from `assets/face/`.

### Clone Mode (V17 — "Same But Different Text")

When the user wants the same thumbnail composition with just the text changed (e.g., `/ultraplan` → `/ultrareview`), use clone mode. This skips prompt writing entirely:

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts \
  --clone "output/ultraplan/folder-ultraplan-golden-ref.jpeg" \
  --text "/ultrareview" \
  --name "folder-ultrareview-contemplative" \
  -n 1 -o "output/ultrareview"
```

**How it works:**
1. The `--clone` source image is added as a reference
2. The prompt is auto-generated: "Recreate this exact thumbnail but change the text to [X]"
3. The `--name` flag saves directly to the final output folder — no temp dirs needed
4. Face references are still loaded for likeness consistency

**When to use clone mode:**
- User says "same as X but with different text"
- User wants a variant of an existing thumbnail for a new video
- Generating a series with consistent style (e.g., all `/command` thumbnails)

**When NOT to use clone mode:**
- User wants a different composition, expression, or layout
- The source thumbnail doesn't exist or wasn't a good result

---

## Face References

Located in `assets/face/`.

**Primary reference: `go-to-face.jpg`** — This is the go-to face photo that performs best for thumbnail generation. When running generations:
- If only one face reference is needed (most cases), use `go-to-face.jpg` exclusively by temporarily isolating it or ensuring the script only loads it
- The script randomly selects up to 5 from `assets/face/`, so when you want consistency, move other photos to `assets/face-backup/` before generating, then restore after
- Other photos in the folder are supplementary — useful for variety but `go-to-face.jpg` should always be included

---

## Requirements

- Node.js with dependencies installed (`npm install` in skill folder)
- `GEMINI_API_KEY` in `.env` file (same key as excalidraw-gen skill)
- Face reference photos in `assets/face/`
- `yt-dlp` installed (for research mode)
- Supadata skill installed (for research mode)
- Streamlit installed (`pip install streamlit`)

## Important Notes

- **Aspect ratio**: All thumbnails generate at 16:9 (YouTube standard)
- **Resolution**: 2K output (2752x1536) — YouTube recommends 1280x720 minimum
- **Rate limits**: Up to 5 parallel generation processes, each doing 1-2 images
- **Timeout**: Allow up to 3 minutes per image. Use 180000ms timeout for Bash calls.
- **Filename collisions**: Always use separate output directories for parallel batches, then rename and consolidate after
