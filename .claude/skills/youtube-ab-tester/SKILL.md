---
name: youtube-ab-tester
description: Generate A/B test title and thumbnail text options for Ray's YouTube videos, and record A/B test results. Use this skill whenever the user wants to brainstorm YouTube titles, generate thumbnail text ideas, record A/B test results, analyze title/thumbnail performance, or asks things like "suggest titles", "what titles should I test", "record these results", "what's working", "title ideas for my next video", "thumbnail text options", or "update the A/B test results". Also trigger when the user shares a screenshot of YouTube A/B test results and wants analysis or recording. Do NOT use for competitor title research (use youtube-title-researcher instead) or video scripting (use youtube-scriptwriter instead).
---

## What This Skill Does

You generate data-driven YouTube title and thumbnail text options for A/B testing, and record/analyze test results.

Before generating any titles or thumbnail text, **always read this reference file first** — it is your ground truth:

- `references/ab-test-results.md` — All historical A/B test data (titles AND thumbnails), winning formulas, anti-patterns, and key learnings. Derive your proven formulas, verb rankings, and pattern hierarchy fresh from this data each time. Per-video thumbnail images live under `references/thumbnails/v{N}-{slug}/tested/` — browse those folders when you want to see what winning thumbnails actually look like.

The reference data is the source of truth for what works and what doesn't. Rather than relying on a static list of formulas baked into this skill file, re-derive your recommendations from the actual test results each time. This ensures your suggestions reflect the latest patterns, not stale rankings.

## Recency Weighting

Audience preferences drift over time. When patterns from older videos conflict with newer ones, **trust the newer data**. Apply exponential decay:

- **Last ~4 videos:** Full weight — reflects current audience behavior
- **5-9 videos ago:** High weight — still relevant but verify against recent results
- **10+ videos ago:** Reduced weight — foundational anti-patterns (parentheticals, "Stop doing X", listing features) are durable, but specific formulas and scores may have drifted

**Durable patterns** (structural, unlikely to decay): anti-patterns like parentheticals, multiple features in title, pipe format, accusatory "Stop" framing, "Explained" educational framing.

**Trend-sensitive patterns** (re-evaluate when newer data contradicts): verb rankings, whether "Anthropic" authority is required, optimal title length, which curiosity frames resonate. Don't dismiss newer counter-evidence just because older data was stronger.

## Generating Title Options

When the user asks for title ideas, provide 8-10 options as a **numbered list** (not a table). For each title, briefly note which proven pattern it draws from or what untested hypothesis it explores. Tables make it hard to select and copy individual titles — always use numbered lists for title and thumbnail text suggestions.

### Check for template reuse BEFORE proposing titles

**Always glob `socials/youtube/videos/uploaded/` for recent scripts and scan their titles before suggesting new ones.** Repeated title templates lose novelty fast.

Ray's March 2026 audit caught a clean example: "Anthropic Just Dropped the Feature Nobody Knew They Needed" was used twice in March (Mar 11 /btw at 39K views, Mar 24 Auto Dream at 97K views but only $6K revenue) and once in Feb. The second and third uses underperformed on the revenue axis even when views held up.

**Rule:** flag any proposed title that reuses a template (same opening clause, same curiosity frame) from the last 60 days. If you must reuse, tell the user explicitly and explain why this time is different (new feature class, different audience segment, etc.).

### Format matters for expected view count

March 2026 data is unambiguous on format:

| Format | Avg March views | Examples |
|--------|----------------:|----------|
| Single-feature deep dive | **45,215** | Skills 2.0, /btw, Auto Dream, Scheduled Tasks, Telegram |
| Thesis / leak / pillar | **17,318** | Top 0.01%, Internal Skills Strategy, Where Coding Is Heading, Claude Code 3.0 |

Single-feature titles averaged **2.6x the views** of thesis/leak/pillar titles. When the user asks for A/B titles on a thesis or leak video, flag this upfront: "This format historically pulls ~17K vs ~45K for single-feature — the test should be between thesis variants, not thesis vs single-feature, because the format ceiling is different."

Pillar videos are the exception: they underperform on raw views but have **5x the per-view click-through to the masterclass site** (Top 0.01% hit 3.16% CTR vs 0.55–1.27% for single-feature). If the user is testing a pillar title, optimize for *curious-clicker* not *feed-scroller* language.

### Frame Diversity

Include at least 3 genuinely different framing categories. If all options share the same frame, the A/B test can't find a winner. The test needs real variety — different frames, not just different words on the same frame.

### Title + Thumbnail Complementarity

Title and thumbnail should be complementary, not redundant. If the thumbnail already communicates the event (e.g., "/leaked"), the title should focus on the *implication* or *what changes*, not restate what the thumbnail shows. Redundancy wastes the title's curiosity budget.

## Generating Thumbnail Text Options

When suggesting thumbnail text, derive your patterns from the reference data. Key behavioral rules:

- Shorter is better — 2-3 words ideal
- Match the title's energy — news title needs news thumbnail, workflow title needs personal thumbnail
- Never use vague time references

## Tracking uploaded variants (write the manifest BEFORE the test runs)

Every video's thumbnail folder lives at `references/thumbnails/v{N}-{slug}/`. That folder holds the **full generated pool** at the top level (every variant Ray ever generated for the video). A single file, `uploaded.json`, pins which of those files are actually live on YouTube for the current A/B test. This eliminates the "which three did Ray upload?" guessing step.

**When to write the manifest:** the moment Ray says "testing these three", "uploading X/Y/Z", "going live with A/B/C", or otherwise commits a set to a live YouTube test. Write it *before* the test runs, not after results come back.

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
- Every filename in `variants` MUST already exist at the top level of the same folder. If Ray names a file that isn't there, stop and ask — don't invent a match.
- If a new round of the same test starts, bump `round` and overwrite `uploaded.json`. The ranked copies from the previous round already live in `tested/` so nothing is lost.
- The manifest is the single source of truth for "what's live right now." Never guess from the generated pool.

## Recording A/B Test Results

**IMPORTANT: Record results immediately.** As soon as the user shares A/B test results (screenshots or numbers), record them to the reference files *before* suggesting the next round. Do not wait for the user to ask — recording is automatic and happens inline with your analysis. This ensures no data is lost between conversation turns.

When the user shares A/B test screenshots or results:

1. **Read `references/thumbnails/v{N}-{slug}/uploaded.json` first.** It tells you exactly which files are live. Never guess from the full pool.
   - If the manifest is missing (legacy video, or Ray forgot to mark it), stop and ask Ray to identify the three files before recording. Do not guess.
2. Match each file in `variants` to its rank and pct from the screenshot.
3. **Resolve each filename** using the lookup order in "Finding variant files" below. If a file lives only in the generator's `output/` folder, copy it into the v{N} folder first so the ab-tester archive becomes self-contained.
4. Copy (don't move — keep the originals in the pool) each tested file into `references/thumbnails/v{N}-{slug}/tested/` as `{rank}-{pct}pct-{original-stem}.{ext}`. Example: `matt-structural-three-modes-b.png` → `tested/1st-38.5pct-matt-structural-three-modes-b.png`.
5. Record results in `references/ab-test-results.md` with the established markdown table format. Round header: `### Title A/B Test Round N (YYYY-MM-DD)`.
6. Write "Key takeaways" that reference specific data points from previous videos.
7. End with a clear recommendation for the next round.

### Finding variant files

When resolving a filename from `uploaded.json`, search in this order:

1. `references/thumbnails/v{N}-{slug}/<filename>` — the canonical home. All new generations should land here directly (see `youtube-thumbnail-generator/SKILL.md`).
2. `../../youtube-thumbnail-generator/output/<slug>/<filename>` — transitional fallback for files that were generated before the direct-to-ab-tester convention. If found here, **copy (not move) the file into the v{N} folder** before writing the `tested/` rank copy. This way the ab-tester archive becomes self-contained as old tests get recorded.

If the file is missing from BOTH locations, stop and ask Ray. Never invent a match from similar filenames.

### Folder layout

```
references/thumbnails/v{N}-{slug}/
  uploaded.json                          # manifest — what's currently live
  tested/                                # ranked copies of completed rounds
    1st-38.5pct-<original-stem>.png
    2nd-35.3pct-<original-stem>.png
    3rd-26.2pct-<original-stem>.png
  <all generated variants>.png           # the full pool (winners + losers + unused)
```

The top-level pool is kept intact so future thumbnail suggestions can browse everything Ray has ever generated for a video, not just the winners.

### Diagnosing Bottlenecks

When results are flat across title variants:
- If all titles share the same frame → the frame is the problem, test different frames
- If titles use diverse frames but all score the same (~0-2% spread) → the thumbnail is likely the ceiling, switch to thumbnail testing
- If a proven winner formula suddenly scores ~33% → something external is capping it (thumbnail mismatch, audience fatigue, topic ceiling)

### When to Recommend What

- **Title testing first** — almost always start here. Titles have wider performance range than thumbnails
- **Switch to thumbnail testing** when 3+ diverse title frames produce identical results
- **Consider topic ceiling** when both title and thumbnail optimization plateau
