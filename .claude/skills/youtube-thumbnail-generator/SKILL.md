---
name: youtube-thumbnail-generator
description: Generate YouTube thumbnails using Gemini Nano Banana 2 image generation with face references for consistent likeness. Two modes — research competitor thumbnails by keyword, or generate thumbnail variations for an upcoming video. Use when the user wants to create thumbnails, research thumbnail styles, find competing thumbnails, generate thumbnail ideas, or anything related to YouTube thumbnail creation. Triggers on "generate a thumbnail", "make a thumbnail", "thumbnail ideas", "find thumbnails for", "research thumbnails", "thumbnail variations", or any YouTube thumbnail request.
---

## First: Ask the User

Before doing anything, ask which mode they want:

1. **Research** — Find and download thumbnails for a category or keyword search
2. **Generate** — Create thumbnail variations for an upcoming video

Use AskUserQuestion with options:
- "Research" — I'll search YouTube and download competitor thumbnails for analysis
- "Generate" — I'll create thumbnail variations for your video using Nano Banana 2

---

## Mode 1: Research Thumbnails

Use the supadata skill to search YouTube and batch-download thumbnails for competitive analysis.

### Steps

1. Ask for the search query / category / keyword
2. Run the supadata batch-thumbnails command:

```bash
python3 .claude/skills/supadata/scripts/supadata.py batch-thumbnails "<query>" --max 15 --out-dir /tmp/thumbnail-research/<slugified-query>
```

3. Read the generated `manifest.json` to get the list of downloaded thumbnails
4. Use the Read tool to visually inspect each thumbnail (they're images, so Claude can see them)
5. Present findings to the user:
   - Which thumbnails stand out and why
   - Common patterns (colors, text placement, face expressions, composition)
   - Specific thumbnails worth emulating

6. Read `references/thumbnail-analysis.md` for the outlier framework to structure the analysis

### Output

Save a summary to the research directory as `analysis.md` with:
- Screenshot references (file paths)
- Pattern observations
- Recommendations for the user's next thumbnail

---

## Mode 2: Generate Thumbnail Variations

Use Nano Banana 2 (Gemini 3.1 Flash Image) to generate thumbnail candidates with Ray's face for consistent likeness.

### Steps

1. Ask the user for:
   - Video title or topic
   - Any specific text they want on the thumbnail
   - Style preferences (if any)
   - Whether to include competitor thumbnails as references (optional)

2. Read the `references/thumbnail-analysis.md` to understand what makes thumbnails perform well

3. Construct the thumbnail prompt. A great thumbnail prompt includes:
   - The concept/scene description
   - Text to render (keep it to 2-4 bold words max)
   - Emotional expression for the face (surprise, excitement, curiosity, etc.)
   - Color palette and contrast requirements
   - Composition guidance (rule of thirds, focal points)

4. Run the generate script with face references:

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts "<prompt>" -n 5 -o "<output-dir>"
```

If competitor thumbnails should be used as style references, add them with `-r`:
```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts "<prompt>" -n 5 -o "<output-dir>" -r /path/to/competitor1.jpg -r /path/to/competitor2.jpg
```

5. Use the Read tool to visually review each generated thumbnail
6. Present the variations to the user for selection

### Prompt Construction Guidelines

YouTube thumbnails that get clicks follow these patterns:

- **Bold, simple text**: 2-4 words max, large sans-serif font, high contrast against background
- **Expressive face**: Exaggerated emotion (shock, excitement, curiosity) — this is the #1 click driver
- **High contrast**: Bright colors that pop against YouTube's white/dark UI
- **Simple composition**: One clear focal point, no clutter
- **Curiosity gap**: Visual that makes viewers want to click to learn more

**Prompt template:**
```
A YouTube thumbnail for a video titled "[TITLE]".
[SCENE DESCRIPTION].
The person (matching the reference photos exactly) has a [EMOTION] expression.
Bold text reading "[TEXT]" in [FONT STYLE] positioned [LOCATION].
[COLOR/STYLE NOTES].
The composition is clean and optimized for small mobile viewing.
Background must be [BACKGROUND DESCRIPTION].
```

### Batch Generation

For maximum variety, generate 5 thumbnails per concept, trying different:
- Emotions (surprised, excited, thoughtful, intense)
- Text placements (top-left, center, right-side)
- Color schemes (dark bg/light text, gradient, split-screen)
- Compositions (close-up face, medium shot with props, text-dominant)

Process in batches of 2 to avoid Gemini API rate limits (same as excalidraw-gen).

---

## Generate Command

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts <prompt> [options]
```

**Options:**
- `-n, --count` — Number of images (default: 5)
- `-o, --output` — Output directory
- `-t, --timeout` — Timeout per image in seconds (default: 180)
- `-r, --reference` — Additional reference image (repeatable, e.g., competitor thumbnails)
- `--no-face` — Skip loading face reference images
- `--text` — Text to render on the thumbnail (passed separately for emphasis)
- `--system-prompt` — Override the default system prompt

The script automatically loads all face reference images from `assets/face/` and passes them to Nano Banana 2 for likeness consistency.

---

## Face References

Place 3-5 high-quality photos of your face in `.claude/skills/youtube-thumbnail-generator/assets/face/`.

Best reference photos:
- Different angles (front, 3/4 profile)
- Different expressions (neutral, smiling, surprised)
- Good lighting, clear face
- Head-and-shoulders framing

The generate script loads ALL images from `assets/face/` automatically as character references.

---

## Requirements

- Node.js with dependencies installed (`npm install` in skill folder)
- `GEMINI_API_KEY` in `.env` file
- Face reference photos in `assets/face/`
- `yt-dlp` installed (for research mode)
- Supadata skill installed (for research mode)

## Important Notes

- **Aspect ratio**: All thumbnails generate at 16:9 (YouTube standard)
- **Resolution**: 2K output (2752x1536) — YouTube recommends 1280x720 minimum
- **Rate limits**: Never run more than 2 generation tasks simultaneously
- **Timeout**: Allow up to 3 minutes per image. Use 180000ms timeout for Bash calls.
