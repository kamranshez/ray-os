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

All generated thumbnails are stored by video ID with descriptive kebab-case names:

```
output/
  <video-id>/
    github-card-last-framework.png
    github-pr-dario-merged.png
    face-laptop-2027-ai-code.png
    icon-grid-the-shift.png
    ...
```

The `output/` folder is gitignored (large generated images).

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

### The V11 Standard (ALWAYS follow this)

V11 ("The Top 0.01% User's Guide to Claude Code") produced the best thumbnails. Every generation must follow this exact approach:

1. **Fetch the transcript FIRST** — use supadata to get the full video transcript before writing any prompts
2. **Read `feedback.json`** for global feedback rules and preferred style
3. **Read `references/thumbnail-analysis.md`** for outlier patterns
4. **Use Nate Herk references only** — from `research/competitor-thumbnails/nateherk/`. These 15 styles are proven. Do NOT use random competitor thumbnails as references — they produce inconsistent/poor results.
5. **Write each prompt yourself** with specific detail from the transcript — do NOT delegate prompt writing to subagents. Generic prompts produce generic thumbnails.
6. **Generate with `-n 1`** (one image per run, NOT `-n 2`) — this produces higher quality output
7. **Run 10 parallel generations** per batch (user preference, Gemini API handles this)
8. **Isolate face reference** — move all photos except `go-to-face.jpg` out of `assets/face/` before generating, restore after

### Steps

1. Get the video URL and fetch transcript via supadata
2. Read `feedback.json` for global feedback rules
3. Read the transcript thoroughly — identify key concepts, features mentioned, emotional hooks
4. For each Nate Herk reference, craft a unique detailed prompt that:
   - Matches the visual style of that specific reference thumbnail
   - References actual content/features from the transcript (not just the title)
   - Includes specific text overlays relevant to the video's content
   - Follows all global feedback rules
5. Isolate `go-to-face.jpg` (move others to `assets/face-backup/`)
6. Generate using separate output directories per reference:

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts "<prompt>" \
  -n 1 -o "output/<video-id>-tmp-<ref>" \
  -r "research/competitor-thumbnails/nateherk/<ref-id>.jpg"
```

7. After generation, rename files with descriptive kebab-case names and move to `output/<video-id>/`
8. Clean up temp batch directories
9. Restore face photos from backup
10. Generate HTML picker for the video
11. Launch Streamlit app or Backfill Lab for user review

### 15 Nate Herk Reference Styles

Always use these references from `research/competitor-thumbnails/nateherk/`:

| # | File | Style | Face? |
|---|------|-------|-------|
| 1 | `OUyfxhFtGCo.jpg` | Folder + `/command` + pointing | Yes |
| 2 | `X6EGzi9qm3E.jpg` | Folder + `/command` + smiling | Yes |
| 3 | `LrgfmZkl3nc.jpg` | Icons on black + bold statement | **No** (`--no-face`) |
| 4 | `Wu67lLD8bB0.jpg` | Icons on black + short phrase | **No** (`--no-face`) |
| 5 | `pkSxISewcw8.jpg` | Old vs New comparison + face center | Yes |
| 6 | `ZeJXI2MAhj0.jpg` | BASIC vs PRO + shh face | Yes |
| 7 | `T6_Ges4j1qY.jpg` | Holding prop/device + bold text | Yes |
| 8 | `4Zaoo0YbYaw.jpg` | Feature grid on screen + face | Yes |
| 9 | `mpALXah_PBg.jpg` | Whiteboard numbered list + face | Yes |
| 10 | `hem5D1uvy-w.jpg` | Screen with flow arrows + face | Yes |
| 11 | `l1jnOXc52NY.jpg` | Retro game leaderboard/score | Yes |
| 12 | `vFepZE_wrfg.jpg` | CLI chat input + bold text overlay | Yes |
| 13 | `BlNJFa3Btm8.jpg` | CLI chat input + "Game Over" style | Yes |
| 14 | `NDnv16PY2XQ.jpg` | Dark dashboard with stats | Yes |
| 15 | `vDVSGVpB2vc.jpg` | Folder + agent network diagram | Yes |

When generating a subset (e.g., 7 of 15), randomly select different ones per video for variety.

### Prompt Construction

**CRITICAL**: Read the transcript first. Prompts must reference actual video content, not just the title.

Always apply global feedback rules from `feedback.json`. Current rules:
- **Expressions**: Modest and natural — contemplative, serious, subtly concerned. NO exaggerated shock/open-mouth surprise.
- **Hair**: Keep natural to reference photos, don't make too curly.

**Prompt template:**
```
A YouTube thumbnail in the style of the reference image.
[SCENE DESCRIPTION — specific to actual video content from transcript].
A young South Asian man with glasses (matching the reference photos exactly) with a [MODEST EXPRESSION] expression.
[TEXT AND LAYOUT DESCRIPTION — use actual terms/features from the video].
[COLOR/BACKGROUND matching the reference style].
Clean composition optimized for small mobile YouTube thumbnail viewing.
```

For no-face thumbnails (refs #3 and #4), add `--no-face` flag and omit face description.

### Naming Convention

Name files descriptively based on their concept:
- `folder-top-secrets-a.png` — Folder /command style
- `icons-black-they-dont-know-b.png` — Icons on black style
- `cli-boring-but-works-a.png` — CLI terminal style
- `retro-game-leaderboard-b.png` — Retro arcade style

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
- `-o, --output` — Output directory
- `-t, --timeout` — Timeout per image in seconds (default: 180)
- `-r, --reference` — Single competitor reference image (use ONE per generation)
- `--no-face` — Skip loading face reference images
- `--text` — Text to render on the thumbnail (passed separately for emphasis)
- `--system-prompt` — Override the default system prompt

The script automatically loads face reference images from `assets/face/`.

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
