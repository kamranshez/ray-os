---
name: youtube-thumbnail-generator
description: Generate YouTube thumbnails for Ray's channel (@RAmjad) using Gemini Nano Banana 2 with face references for consistent likeness. Two style systems available — Matt Pocock (structured explainer slide) or Nate Herk (folder + /command studio). Use whenever the user wants to create thumbnails, make a thumbnail, generate thumbnail variations, design a thumbnail for a video, or anything related to YouTube thumbnail creation. Triggers on "generate a thumbnail", "make a thumbnail", "thumbnail ideas", "thumbnail variations", "5 thumbnails for this video", "Matt style thumbnails", "Nate style thumbnails", or any YouTube thumbnail request.
---

## The two style systems

Ray's thumbnails come in **two distinct visual systems**. Before generating anything, ask which style the user wants (if not already clear from context).

| Style | Feels like | When to use |
|---|---|---|
| **Matt Pocock** | A well-designed explainer slide from an educational deck | Features, comparisons, how-it-works videos, announcements, any video where you're teaching or contrasting something |
| **Nate Herk** | A big folder or app-icon studio shot with a slash command | New command/tool launches, integration videos, "I built X" videos, anything that has a clear feature name to showcase |

Each style has its own **golden reference library** under `research/golden-references/matt-style/` or `research/golden-references/nate-style/`, and its own set of rules. You should commit to ONE style per batch — never mix them.

Read the style-specific reference file before generating:
- **Matt style** → read `references/matt-style.md` for layouts, rules, and golden refs
- **Nate style** → read `references/nate-style.md` for layouts, rules, and golden refs

---

## The standard workflow (both styles)

Whatever style the user picks, the workflow is the same:

1. **Ask for the video title** → determine the target folder in the ab-tester archive (see "Where generations land" below). If the folder doesn't exist yet, create it.
2. **Ask which style** if not obvious — Matt or Nate
3. **Get the video content** — either the transcript (fetch via supadata if URL) or a script/description the user provides
4. **Read the style's reference file** (`references/matt-style.md` or `references/nate-style.md`)
5. **Read `feedback.json`** for global feedback rules (e.g., facial expressions, hairstyle)
6. **Isolate `go-to-face.jpg`** — move all other photos out of `references/rays-face/` to `references/rays-face-backup/`
7. **Write 5 prompts** by hand, each using a different golden reference from the chosen style's library. Never use subagents for prompt writing — they lose visual context.
8. **Fire all 5 generations in parallel** using `run_in_background: true`. Use `--name` to save directly to the target folder.
9. **Wait via Monitor tool** that watches the target folder for the final count
10. **Restore face photos** from `face-backup/`
11. **Open the target folder** — `open ../youtube-ab-tester/references/thumbnails/v{N}-{slug}/`

### Where generations land

All thumbnails — the generated pool AND the eventual tested winners — live in the **youtube-ab-tester** skill, not here. This skill is pure compute; the ab-tester holds state.

```
../youtube-ab-tester/references/thumbnails/
  v{N}-{slug}/          ← canonical home for a video with a confirmed v-number
    uploaded.json       ← manifest pinning the currently-live variants
    tested/             ← ranked copies of completed rounds
    <all generated variants>.png
  pending-{slug}/       ← video doesn't have a v-number yet (unreleased / un-tested)
```

**Before generating:**
- If you know the video's `v{N}` number (it's been tested before, or Ray tells you), use `v{N}-{slug}/`.
- If it's a brand-new video with no test yet, use `pending-{slug}/`. When Ray runs his first A/B test on it, the folder gets renamed to `v{N}-{slug}/` and added to `ab-test-results.md`.
- Never generate into `youtube-thumbnail-generator/output/` — that folder no longer exists.

### Parallel generation snippet

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts "<prompt>" \
  -n 1 -o "../youtube-ab-tester/references/thumbnails/v{N}-{slug}" \
  --name "<style-prefix>-<concept>-<variant>" \
  -r "research/golden-references/<style>/<golden-ref>.png" \
  -t 240
```

Run 5 of these in a single message with `run_in_background: true`, then use the Monitor tool to watch for completion.

### Why 5 variants, not 20

The explore phase (generating dozens of variants to map the design space) is done — the golden libraries ARE the explore output. For a new video, generate 5 well-targeted variants using 5 different golden references from the chosen style. If the user wants more variety, generate another 5; don't front-load 20 in one batch.

---

## Hard rules (both styles)

These apply to every thumbnail Ray generates, regardless of style:

**Subject:**
- Ray = young South Asian man, glasses, naturally straight dark hair (NOT curly, NOT wavy — match the reference photos exactly)
- Outfit: black t-shirt OR plain **white collared long-sleeve shirt** — nothing else. No plaid, no beige, no patterns.
- Expression: warm genuine smile, knowing smirk, or contemplative — NEVER shock, surprise, or exaggerated reactions
- Shure SM7B podcast microphone rising from the bottom-right foreground (used when the composition has room for it)

**Face references:**
- Always isolate `references/rays-face/go-to-face.jpg` as the ONLY face reference before generating
- Move other photos to `references/rays-face-backup/`, restore after the batch completes
- Without isolation, outputs drift off-likeness because the script randomly samples up to 5 photos

**Generation mechanics:**
- `-n 1` per run (never `-n 2`)
- One golden reference per generation (never pass multiple — styles wash out into a generic average)
- Run up to 5 parallel Bash calls at once with `run_in_background: true`
- Use `-t 240` (4-minute timeout per image) — Gemini sometimes takes a while
- Use `--name` to save directly to the final folder — no temp dirs

**Never do:**
- Subagents for prompt writing (they lose visual context)
- Multiple competitor references in one generation
- Metaphor illustrations (cameras, bells, zzz clouds, cartoons) — these failed in testing
- Giant single-word typography as the only element — these failed in testing
- Crossed-out / X-marked commands — Ray rejected these

---

## Output organization

Files land in `../youtube-ab-tester/references/thumbnails/v{N}-{slug}/` (or `pending-{slug}/` for untested videos).

```
v{N}-{slug}/
  uploaded.json                         # written by ab-tester when Ray picks variants
  tested/                               # populated from A/B results
  matt-structural-radial-a.png
  matt-comparative-table-b.png
  matt-mockup-tweet-c.png
  ...
```

Naming convention for the `--name` flag: `<style>-<concept>-<variant>`
- Matt style: `matt-command-list-radial-a`, `matt-before-after-b`, `matt-tweet-c`
- Nate style: `nate-folder-command-a`, `nate-icons-black-b`

---

## Golden references — the winning set

Golden refs are previous generations that Ray liked enough to treat as canonical. They already have Ray's face baked in, so the model has less to reconcile between face ref + style ref.

```
research/golden-references/
├── matt-style/
│   ├── ray-command-list-v1-37pct.png                  ← original command list (open-mouth, black tee, 37.2% R1 peak)
│   ├── ray-command-list-v2-40pct.png                  ← ✅ BEST: subtly impressed, white oxford, 40.3% R2 peak — use this one
│   ├── winner-v22-advisor-command-list-41pct.png      ← v22 R1 1st: command-list excalidraw (41.1%)
│   ├── winner-v20-plan-mode-icons-39pct.png           ← v20 R1 1st: plan-mode 2-icon structural (38.5%)
│   ├── winner-v22-advisor-before-after-37pct.png      ← v22 R2 1st: before/after excalidraw (37.2%)
│   ├── winner-v23-monitor-slash-list-36pct.png        ← v23 R1 1st: slash-list top structural (36.2%)
│   ├── winner-v17-shift-dark-icons-34pct.png          ← v17 1st (tied): the-shift dark-icon (34.3%)
│   ├── winner-v17-github-future-of-coding-34pct.png   ← v17 1st (tied): github-card mockup with face (33.9%)
│   └── liked-examples/                                ← Ray's eye-picked compositions (no CTR data, flat)
│       ├── v3-06-two-column-flow.png
│       ├── v3-09-fake-tweet.png
│       ├── v4-B3-radial-diagram.png
│       ├── v4-C2-events-actions-dense.png
│       ├── v4-C4-before-after-state.png
│       ├── v4-C5-three-column.png
│       ├── v4-D3-mac-notification.png
│       ├── v4-D4-changelog-card.png
│       ├── v5-C1-feature-table.png
│       ├── v5-C2-mood-columns.png
│       ├── v5-C5-bar-chart.png
│       ├── v5-M5-raycast-search.png
│       ├── v5-M6-reddit-post.png
│       └── v5-S1-radial-six-spokes.png
└── nate-style/
    ├── winner-v18-auto-dream-folder-35pct.png         ← v18 R1 1st: dream-folder face shot (34.9%)
    ├── winner-v19-leak-folder-serious-36pct.jpg       ← v19 R1 1st: leak-folder serious face (35.5%)
    └── folder-command/
        ├── folder-command.png                          ← contemplative, medium shot
        └── folder-command-closeup.jpeg                 ← close-up face crop
```

When Ray marks a new generation as a winner, **save it to `matt-style/` (top level for command-list heroes, `liked-examples/` for other layouts) or `nate-style/`** so future sessions benefit.

---

## Mode 1: Research competitor thumbnails

(Unchanged from V15 — still useful for discovering new styles or expanding the reference library.)

When the user wants to research new competitor thumbnails, there are four sources:

### From a specific channel URL
```bash
yt-dlp --flat-playlist --print "%(id)s %(title)s" "<channel-url>" --playlist-end 15
curl -sL "https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg" -o "research/competitor-thumbnails/<VIDEO_ID>.jpg"
```

### From YouTube Studio "What your audience watches"
URL: `https://studio.youtube.com/channel/UCLA7cJBnqr0nLF2bQBD9uUg/analytics/tab-build_audience/period-default`

Use browser automation (mcp__claude-in-chrome or Playwright). Extract video IDs from thumbnail image URLs and download.

### From keyword search
```bash
python3 .claude/skills/supadata/scripts/supadata.py batch-thumbnails "<query>" --max 15 --out-dir research/competitor-thumbnails
```

### From user-provided HTML
Extract video IDs from pasted HTML (look for `src="https://i.ytimg.com/vi/<ID>/..."`), download thumbnails.

After downloading, visually inspect each with the Read tool and write a short style analysis to `research/analysis.md`.

---

## Mode 3: Regenerate from feedback

When the user says "regenerate from feedback":
1. Read `feedback.json`
2. Find all thumbnails with non-empty comments
3. For each, construct a new prompt that keeps what the user liked and fixes what they didn't
4. Apply all `global_feedback` rules
5. Generate into the video's folder in `../youtube-ab-tester/references/thumbnails/v{N}-{slug}/` with a `-v2` suffix on the name

---

## Generate command reference

```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts <prompt> [options]
```

**Options:**
- `-n, --count` — Number of images (default: 5 — override with `-n 1` for thumbnails)
- `-o, --output` — Output directory
- `-t, --timeout` — Timeout per image in seconds (use 240 for thumbnails)
- `-r, --reference` — Single competitor/golden reference image (use ONE per generation)
- `--no-face` — Skip loading face reference images
- `--text` — Text to render with stronger emphasis on exact spelling
- `--name` — Output filename (without .png). Saves directly as `<output>/<name>.png`
- `--clone` — Clone mode: pass an existing thumbnail to recreate with different text. Requires `--text`.
- `--system-prompt` — Override the default system prompt

The script automatically loads face reference images from `references/rays-face/`.

### Clone mode ("same but different text")

When Ray wants the same composition with just the text changed:
```bash
cd .claude/skills/youtube-thumbnail-generator && npx ts-node scripts/generate.ts \
  --clone "../youtube-ab-tester/references/thumbnails/v20-ultraplan/folder-ultraplan-golden-ref.jpeg" \
  --text "/ultrareview" \
  --name "folder-ultrareview-contemplative" \
  -n 1 -o "../youtube-ab-tester/references/thumbnails/v21-ultrareview"
```

Use clone mode when:
- Same as X but with different text
- Variant of an existing thumbnail for a new video
- Generating a series with consistent style (e.g., all `/command` thumbnails)

Don't use clone mode when the user wants a different composition, expression, or layout.

---

## Feedback system

`feedback.json` is the single source of truth for user preferences.

```json
{
  "preferred_style": {
    "name": "Matt Pocock structured explainer",
    "description": "Structured diagram / comparison / mockup on black left half, Ray right-side with mic",
    "reference_dir": "research/golden-references/matt-style/"
  },
  "global_feedback": {
    "facial_expressions": "Keep expressions modest and natural — no exaggerated shock/surprise. Contemplative, serious, warm smile, or subtly concerned work best.",
    "hairstyle": "Don't make hair too curly — keep it naturally straight to match the reference photos.",
    "outfit": "Black t-shirt OR plain white collared long-sleeve shirt only. No plaid, no beige, no patterns.",
    "diagrams": "Diagrams should look hand-drawn/excalidraw-style — NOT clean vector/polished boxes. Casual sketched quality."
  },
  "<video-id>/<filename>.png": {
    "favorite": true,
    "rating": 5,
    "comment": "Feedback text here"
  }
}
```

**Before every generation run:**
1. Read `feedback.json`
2. Apply all `global_feedback` rules to every prompt
3. Check `preferred_style` to know the default style if not specified
4. If regenerating from comments, incorporate per-thumbnail feedback into the new prompts

---

## YouTube Lab (Streamlit app)

The centralized app for all thumbnail management:
```bash
cd .claude/skills/youtube-thumbnail-generator/lab && streamlit run app.py --server.port 8503
open http://localhost:8503
```

3 pages: Dashboard (all videos), Review (shortlist per video), Results (A/B test outcomes). Data in `lab/data.json`.

---

## Face references

`references/rays-face/go-to-face.jpg` is the primary face reference. For consistency:
- Move all other photos to `references/rays-face-backup/` before generating
- The script randomly samples up to 5 photos from `references/rays-face/` — isolating prevents drift
- Restore from backup after the batch completes

---

## Requirements

- Node.js with dependencies installed (`npm install` in skill folder)
- `GEMINI_API_KEY` in `.env` file
- `references/rays-face/go-to-face.jpg` present
- `yt-dlp` installed (for research mode)
- Supadata skill installed (for research mode)
- Streamlit installed (`pip install streamlit`) for the Lab

## Important notes

- **Aspect ratio**: 16:9 (YouTube standard)
- **Resolution**: 2K output (2752x1536)
- **Rate limits**: Up to 5 parallel generation processes
- **Timeout**: 240s (4 minutes) per image — use `-t 240` on every call
- **Wait strategy**: After firing 5 background generations, use the Monitor tool with a small polling script to watch the target v{N}-{slug}/ folder for completion, rather than sleeping or polling manually
