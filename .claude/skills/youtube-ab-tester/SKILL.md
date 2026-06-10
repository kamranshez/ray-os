---
name: youtube-ab-tester
description: End-to-end YouTube A/B testing for Ray's channel (@RAmjad) — title generation via subagent, thumbnail image generation via `gemini-3-pro-image-preview` at 1K, results recording, and the underlying scripts/golden references all live here. Use whenever the user wants to brainstorm titles, generate thumbnails (text or images), record A/B test results, analyze title/thumbnail performance, or asks things like "suggest titles", "what titles should I test", "make a thumbnail", "thumbnail variations", "5 thumbnails for this video", "Matt style", "Nate style", "record these results", "what's working", or "update the A/B test results". Also trigger when the user shares a screenshot of YouTube A/B test results and wants analysis or recording. Do NOT use for competitor title research (use youtube-title-researcher instead) or video scripting (use youtube-scriptwriter instead).
---

## What This Skill Does

End-to-end YouTube A/B testing — titles, thumbnails (text AND images), results recording, all under one roof.

Two main modes:

1. **Pairing mode (title + thumbnail concepts)** — user asks for titles or pairings. Spawn a subagent, get back a pre-paired slate.
2. **Image generation mode** — user asks for actual thumbnail images. Use `scripts/generate.ts` (Gemini) with face references and Matt or Nate golden refs.

Plus results recording, manifest tracking, and cross-video pattern analysis — these stay in main context.

**Hard rule: title generation is ALWAYS delegated to a subagent.** Never brainstorm titles in main context — the reference data is heavy (master-summary + anti-patterns + 4-6 recent video files + the transcript) and synthesizing it inline pollutes the conversation. See "Title generation: always delegate to a subagent" below.

What stays in main context:
- Framing the user's ask, spawning the subagent, presenting the slate
- Recording A/B results (mechanical file work)
- Analyzing CTR/watch-share screenshots
- Firing `scripts/generate.ts` with Ray's chosen pairings
- Cross-video pattern discussion

## Folder layout of this skill

```
youtube-ab-tester/
├── SKILL.md                  ← this file
├── .env                      ← GEMINI_API_KEY lives here
├── package.json, tsconfig.json, node_modules/
├── scripts/generate.ts       ← image generation (gemini-3-pro-image-preview at 1K)
├── app.py, compare.html      ← Streamlit lab for browsing thumbnails
├── feedback.json             ← global feedback rules + per-thumbnail comments
├── golden-references/        ← image references for Matt and Nate styles
│   ├── matt-style/
│   └── nate-style/
└── references/
    ├── matt-style.md         ← Matt-style layout rules
    ├── nate-style.md         ← Nate-style layout rules
    ├── thumbnail-analysis.md
    ├── rays-face/            ← face reference for image generation
    ├── results/              ← per-video A/B test results (YYYY-MM/ folders)
    └── thumbnails/           ← generated thumbnails (v{N}-{slug}/ folders)
```

## Before you do anything: read the reference data

The reference data is the source of truth — re-derive recommendations from actual test results each time, not from baked-in formulas.

- `references/results/YYYY-MM/` — Per-video A/B test results organized by year-month folders. Each file is `YYYY-MM-DD-slug.md`. **Read the most recent 4-6 video files (glob the latest month folder) for current patterns.**
- `references/results/_master-summary.md` — Winning formula rankings and key rules
- `references/results/_anti-patterns.md` — Documented failures to never repeat
- `references/results/_tests-still-worth-running.md` — Untested hypotheses worth exploring
- `references/results/_overview.md` — Document overview
- `references/thumbnails/v{N}-{slug}/tested/` — winning thumbnails by video, browse to see what worked

## Recency Weighting

Audience preferences drift over time. When patterns from older videos conflict with newer ones, **trust the newer data**:

- **Last ~4 videos:** Full weight — reflects current audience behavior
- **5-9 videos ago:** High weight — verify against recent results
- **10+ videos ago:** Reduced weight — foundational anti-patterns are durable, but specific scores drift

**Durable patterns** (structural): parentheticals, multiple features in title, pipe format, "Stop X" accusatory, "Explained" framing.

**Trend-sensitive patterns** (re-evaluate when newer data contradicts): verb rankings, whether "Anthropic" authority is required, optimal title length, which curiosity frames resonate.

---

# PART 1 — Title generation (always via subagent)

**Never write titles in main context.** Title brainstorming requires reading the full reference corpus (master-summary, anti-patterns, 4-6 recent video files, the transcript or topic brief, and `socials/youtube/videos/uploaded/` for stale-template checks). Doing this inline burns main-context tokens and pollutes the conversation.

Instead: spawn a fresh `general-purpose` subagent with a self-contained prompt. The subagent reads the data, synthesizes the slate, and returns title + thumbnail **pairings** as one structured output.

### How to dispatch

Use the `Agent` tool with `subagent_type: "general-purpose"`. Pass the full briefing in the prompt — the subagent has zero conversation history.

**Template prompt:**

```
You are generating a YouTube A/B test slate for Ray's channel (@RAmjad). You will produce TITLE + THUMBNAIL PAIRINGS — not two separate lists.

# Video context
Topic: <one-line summary>
Transcript: <inline OR path to file>

# Required reading (read all before generating)
1. /Users/ray/Desktop/ray-os/.claude/skills/youtube-ab-tester/references/results/_master-summary.md
2. /Users/ray/Desktop/ray-os/.claude/skills/youtube-ab-tester/references/results/_anti-patterns.md
3. /Users/ray/Desktop/ray-os/.claude/skills/youtube-ab-tester/references/results/_tests-still-worth-running.md
4. The 4-6 most recent video result files under references/results/YYYY-MM/ (latest month first)
5. socials/youtube/videos/uploaded/ — list filenames to check 60-day template reuse
6. Optionally browse references/thumbnails/v{N}-{slug}/tested/ folders from recent videos to see what winning thumbnails looked like

# Hard rules
- Apply recency weighting (last 4 videos full weight; 5-9 ago high; 10+ durable anti-patterns only).
- Flag template reuse from the last 60 days. Justify any reuse in writing.
- Frame diversity: at least 3 genuinely different framing categories.
- Title + thumbnail must be COMPLEMENTARY, not redundant. Title says WHY/WHO, thumbnail says WHAT.
- Format-ceiling warning: thesis/paradigm/leak/pillar videos historically pull ~17K vs ~45K for single-feature. Pillar exception: 5x masterclass CTR.
- Anti-patterns: parentheticals, "Explained" framing, "Stop X" accusatory, pipe format, multiple features in title, FOMO/guilt, faceless thumbnails (V13), vague time refs, year labels, feature-framing thumbnails over personal.

# Output format

## Format-ceiling warning
<only if applicable. Skip otherwise.>

## R1 recommended trio (3 frame-diverse pairings)
For each:
- Title: "..."
- Frame: <authority | observable social proof | concrete-proof | pillar/insider | concrete-mechanic>
- Thumbnail concept: <Matt-structural | Nate-folder | hybrid>
- Thumbnail text: "..." (2-3 words ideal)
- Complementarity check: <one line>
- Risk flags: <stale template / topic ceiling / anti-pattern adjacent>

## Extras (5-7 more options)
Same format. Cover authority, social-proof, concrete-proof, insider/pillar, concrete-mechanic.

## Hard rules for THIS video
3-5 bullets: stale templates to avoid, frames to NOT reuse, format-specific cautions.

# Required: be terse. Numbered lists, not paragraphs. Pairings, not separate sections.
```

When the subagent returns, present the slate to Ray as-is (do not re-narrate). Help him pick the R1 trio if he asks, and write the manifest when he commits.

### Why a fresh subagent (not a fork)

- Reference data load (~6-10 file reads) is heavy and one-shot — clean context handles it best
- Title synthesis is closed-task with a clear output spec — no conversation state needed
- Main context stays clean for the pairing-selection conversation that follows

---

# PART 2 — Thumbnail image generation

When Ray asks for actual thumbnail images (not just text concepts), use `scripts/generate.ts`. This was formerly the `youtube-thumbnail-generator` skill — same scripts, now consolidated here.

### The two style systems

Before generating, commit to ONE style per batch — never mix.

| Style | Feels like | When to use |
|---|---|---|
| **Matt Pocock** | Well-designed explainer slide | Features, comparisons, how-it-works, announcements, teaching |
| **Nate Herk** | Big folder / app-icon studio shot with a slash command | New command/tool launches, integration videos, "I built X" |

Each has a golden reference library under `golden-references/matt-style/` or `golden-references/nate-style/`, and its own rules:
- **Matt style** → read `references/matt-style.md`
- **Nate style** → read `references/nate-style.md`

### Standard workflow

1. **Determine video slug + folder.** Target folder is `references/thumbnails/v{N}-{slug}/` (for tested videos) or `references/thumbnails/pending-{slug}/` (for untested). Create if missing.
2. **Confirm style** (Matt or Nate) with the user if not clear from context.
3. **Get the content** — transcript or script/description.
4. **Read the style's reference file** (`references/matt-style.md` or `references/nate-style.md`).
5. **Read `feedback.json`** for global feedback rules (facial expressions, hairstyle, outfit).
6. **Write 5 prompts by hand**, each using a different golden reference. Never use subagents for prompt writing — they lose visual context.
7. **Fire 5 generations in parallel** with `run_in_background: true`. Use `--name` to save directly to the target folder.
8. **Wait via Monitor tool** watching the target folder for the final count.
9. **Open the folder** when done.

### Generate command

```bash
cd .claude/skills/youtube-ab-tester && npx ts-node scripts/generate.ts "<prompt>" \
  -n 1 -o "references/thumbnails/v{N}-{slug}" \
  --name "<style-prefix>-<concept>-<variant>" \
  -r "golden-references/<style>/<golden-ref>.png" \
  -t 240
```

**Options:**
- `-n, --count` — Number of images (use `-n 1` for thumbnails — always)
- `-o, --output` — Output directory
- `-t, --timeout` — Timeout per image in seconds (always use 240)
- `-r, --reference` — Single golden reference image (use ONE per generation — multiple wash styles into a generic average)
- `--no-face` — Skip face references (the default V13 anti-pattern; ONLY use when explicitly requested as a deliberate test)
- `--text` — Text with stronger spelling emphasis
- `--name` — Output filename without `.png` extension; saves as `<output>/<name>.png`
- `--clone` — Clone mode: pass an existing thumbnail to recreate with different text. Requires `--text`.

### Why 5 variants, not 20

The explore phase (mapping the design space) is done — the golden libraries ARE the explore output. For a new video, generate 5 well-targeted variants using 5 different golden references. If the user wants more, generate another 5.

### Clone mode

Same composition, different text:

```bash
cd .claude/skills/youtube-ab-tester && npx ts-node scripts/generate.ts \
  --clone "references/thumbnails/v18-ultraplan/folder-ultraplan-golden-ref.jpeg" \
  --text "/ultrareview" \
  --name "folder-ultrareview-contemplative" \
  -n 1 -o "references/thumbnails/v19-ultrareview"
```

Use clone mode when: same as X with different text, variant of an existing thumbnail for a new video, generating a series with consistent style.

Don't use clone mode when the user wants different composition, expression, or layout.

### Hard rules (image generation)

**Subject:**
- Ray = young South Asian man, glasses, naturally straight dark hair (NOT curly, NOT wavy)
- Outfit: black t-shirt OR plain white collared long-sleeve shirt — nothing else
- Expression: warm genuine smile, knowing smirk, or contemplative — NEVER shock, surprise, or exaggerated reactions
- Shure SM7B podcast microphone rising from the bottom-right foreground (when composition has room)

**Face reference:**
- Default: `references/rays-face/go-to-face.png` — transparent-background head-and-shoulders. Resolution: `gemini-3-pro-image-preview`-friendly, no extraction step required.
- Fallback: `references/rays-face/go-to-face.jpg` (legacy, opaque). The script auto-prefers the PNG if both exist.
- Always used, always alone. Script loads it automatically; no isolation step needed.

**Face composition (Nate-style):**
- The transparent background lets the generator place Ray's head ANYWHERE in the frame — exploit this.
- Default position: **bottom-right or right-of-center**, with the subject of the thumbnail (folder, terminal, diagram, slash command) occupying the **left two-thirds** of the canvas. This mirrors Nate Herk's winning compositions (v16 dream-folder 34.9%, v17 leak-folder 35.5%).
- Face should be **3/4-frontal or slightly turned toward the subject** so the eyeline directs the viewer to the visual element.
- Crop tightly: head + shoulders only. No empty headroom above the hair.
- The transparent PNG means the model can match face lighting/edges to any background — black, white, gradient, terminal-screen blue, folder-icon yellow. Specify the background explicitly in the prompt.
- When the composition needs the subject centered (rare — usually announcement/news only), use a smaller face inset in the bottom-right corner instead of dropping the face entirely.

**Generation mechanics:**
- `-n 1` per run (never `-n 2`)
- One golden reference per generation
- Up to 5 parallel `Bash` calls with `run_in_background: true`
- `-t 240` (4-minute timeout) on every call
- `--name` to save directly to final folder — no temp dirs

**Never do:**
- Subagents for prompt writing (they lose visual context)
- Multiple competitor references in one generation
- Metaphor illustrations (cameras, bells, zzz clouds, cartoons) — failed in testing
- Giant single-word typography as the only element — failed in testing
- Crossed-out / X-marked commands — Ray rejected these
- Faceless thumbnails (V13 anti-pattern) — ONLY override when Ray explicitly requests it as a test

### Golden references (current set)

```
golden-references/
├── matt-style/
│   ├── ray-command-list-v1-37pct.png                  ← original command list (37.2% R1 peak)
│   ├── ray-command-list-v2-40pct.png                  ← ✅ BEST: subtly impressed white oxford, 40.3% R2 peak
│   ├── winner-v20-advisor-command-list-41pct.png      ← v20 R1 1st: command-list excalidraw (41.1%)
│   ├── winner-v18-plan-mode-icons-39pct.png           ← v18 R1 1st: plan-mode 2-icon (38.5%)
│   ├── winner-v20-advisor-before-after-37pct.png      ← v20 R2 1st: before/after (37.2%)
│   ├── winner-v21-monitor-slash-list-36pct.png        ← v21 R1 1st: slash-list top structural (36.2%)
│   ├── winner-v15-shift-dark-icons-34pct.png          ← v15 1st tied: dark-icon shift (34.3%)
│   ├── winner-v15-github-future-of-coding-34pct.png   ← v15 1st tied: github-card mockup (33.9%)
│   └── liked-examples/                                ← Ray's eye-picked compositions
└── nate-style/
    ├── winner-v16-auto-dream-folder-35pct.png         ← v16 R1 1st: dream-folder (34.9%)
    ├── winner-v17-leak-folder-serious-36pct.jpg       ← v17 R1 1st: leak-folder serious (35.5%)
    └── folder-command/
        ├── folder-command.png                          ← contemplative medium shot
        └── folder-command-closeup.jpeg                 ← close-up face crop
```

When Ray marks a new generation as a winner, save it into the appropriate style folder so future sessions benefit.

### Regenerate from feedback

When the user says "regenerate from feedback":
1. Read `feedback.json`
2. Find all thumbnails with non-empty comments
3. For each, construct a new prompt keeping what Ray liked and fixing what he didn't
4. Apply all `global_feedback` rules
5. Generate into the video's folder with `-v2` suffix

### Feedback system

`feedback.json` is the single source of truth for user preferences. Before every generation run:
1. Read `feedback.json`
2. Apply all `global_feedback` rules to every prompt
3. Check `preferred_style` for the default if not specified
4. If regenerating from comments, incorporate per-thumbnail feedback

### YouTube Lab (Streamlit app)

```bash
cd .claude/skills/youtube-ab-tester && streamlit run app.py --server.port 8503
open http://localhost:8503
```

Three pages: Dashboard (all videos), Review (shortlist per video), Results (A/B test outcomes). Data in `lab/data.json`.

### Image generation settings

- **Model**: `gemini-3-pro-image-preview` (set via `MODEL_NAME` in scripts/generate.ts)
- **Resolution**: 1K (set via `imageSize: "1K"` in scripts/generate.ts)
- **Aspect ratio**: 16:9 (YouTube standard)
- **Timeout**: 240s per image (`-t 240`)
- **Parallel cap**: up to 5 concurrent generation processes
- **Auth**: `GEMINI_API_KEY` in this skill's `.env` or project root `.env`

---

# PART 3 — Tracking, recording, diagnosis

## Tracking uploaded variants (write the manifest BEFORE the test runs)

Every video's thumbnail folder lives at `references/thumbnails/v{N}-{slug}/`. That folder holds the **full generated pool** at the top level. A single file, `uploaded.json`, pins which of those files are actually live on YouTube for the current A/B test.

**When to write the manifest:** the moment Ray says "testing these three", "uploading X/Y/Z", or otherwise commits a set to a live YouTube test. Write it BEFORE the test runs.

**Format** — `references/thumbnails/v{N}-{slug}/uploaded.json`:

```json
{
  "video_id": "EhiJX0WvRz4",
  "video_title": "Anthropic's New Ultrareview Is Coming: What You Need to Know",
  "uploaded_at": "YYYY-MM-DD",
  "round": 2,
  "variants": [
    "matt-structural-three-modes-b.png",
    "matt-comparative-before-after-d.png",
    "plan-mode-2-faceless-icons-v2.png"
  ]
}
```

**Rules:**
- Every filename in `variants` MUST exist at the top level of the same folder. If Ray names a file that isn't there, stop and ask.
- If a new round of the same test starts, bump `round` and overwrite. The ranked copies from the previous round already live in `tested/`.
- The manifest is the single source of truth for "what's live right now."

## Recording A/B Test Results

**IMPORTANT: Record results immediately.** As soon as the user shares A/B test results, record them to the reference files BEFORE suggesting the next round.

When the user shares A/B test screenshots or results:

1. **Read `references/thumbnails/v{N}-{slug}/uploaded.json` first.** It tells you exactly which files are live. Never guess from the full pool.
2. Match each file in `variants` to its rank and pct from the screenshot.
3. Copy (don't move — keep originals in the pool) each tested file into `references/thumbnails/v{N}-{slug}/tested/` as `{rank}-{pct}pct-{original-stem}.{ext}`.
4. Record results in `references/results/YYYY-MM/YYYY-MM-DD-slug.md` with the markdown table format. Round header: `### Title A/B Test Round N (YYYY-MM-DD)`. For a brand-new video, create the month folder if needed.
5. Write "Key takeaways" referencing specific data points from previous videos.
6. End with a clear recommendation for the next round.

### Folder layout (results archive)

```
references/thumbnails/v{N}-{slug}/
  uploaded.json                          # manifest — what's currently live
  tested/                                # ranked copies of completed rounds
    1st-38.5pct-<original-stem>.png
    2nd-35.3pct-<original-stem>.png
    3rd-26.2pct-<original-stem>.png
  <all generated variants>.png           # the full pool
```

### Diagnosing Bottlenecks

When results are flat across title variants:
- All titles share the same frame → the frame is the problem, test different frames
- Titles use diverse frames but all score ~0-2% spread → thumbnail is the ceiling, switch to thumbnail testing
- A proven winner formula suddenly scores ~33% → something external is capping it (thumbnail mismatch, audience fatigue, topic ceiling)

### When to Recommend What

- **Title testing first** — almost always start here. Titles have wider performance range than thumbnails.
- **Switch to thumbnail testing** when 3+ diverse title frames produce identical results.
- **Consider topic ceiling** when both title and thumbnail optimization plateau.
- **CTR/impressions problem (not watch-share)** — banked from V29/V30: when YouTube flags "fewer subscribers choosing to watch" within ~90 min, recommendations crater. That's a thumbnail or topic problem, not a title problem. Don't keep re-testing titles.
