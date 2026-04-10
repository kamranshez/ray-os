---
name: youtube-ab-tester
description: Generate A/B test title and thumbnail text options for Ray's YouTube videos, and record A/B test results. Use this skill whenever the user wants to brainstorm YouTube titles, generate thumbnail text ideas, record A/B test results, analyze title/thumbnail performance, or asks things like "suggest titles", "what titles should I test", "record these results", "what's working", "title ideas for my next video", "thumbnail text options", or "update the A/B test results". Also trigger when the user shares a screenshot of YouTube A/B test results and wants analysis or recording. Do NOT use for competitor title research (use youtube-title-researcher instead) or video scripting (use youtube-scriptwriter instead).
---

## What This Skill Does

You generate data-driven YouTube title and thumbnail text options for A/B testing, and record/analyze test results.

Before generating any titles or thumbnail text, **always read these reference files first** — they are your ground truth:

- `references/ab-test-results.md` — All historical A/B test data, winning formulas, anti-patterns, and key learnings. Derive your proven formulas, verb rankings, and pattern hierarchy fresh from this data each time.
- `references/thumbnails/index.md` — Visual archive of all tested thumbnails with performance data. Browse per-video folders to see actual images that were tested.

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

## Recording A/B Test Results

**IMPORTANT: Record results immediately.** As soon as the user shares A/B test results (screenshots or numbers), record them to the reference files *before* suggesting the next round. Do not wait for the user to ask — recording is automatic and happens inline with your analysis. This ensures no data is lost between conversation turns.

When the user shares A/B test screenshots or results:

1. Record them in `references/ab-test-results.md` in this skill's directory
2. Use the established format with markdown tables
3. Include timestamp in the round header: `### Title A/B Test Round N (YYYY-MM-DD)`
4. Write "Key takeaways" that reference specific data points from previous videos
5. End with a clear recommendation for the next round
6. Save any thumbnail images shared alongside results (see below)
7. Update `references/thumbnails/index.md` if thumbnail results were included

### Storing Thumbnail Images

When the user shares actual thumbnail images alongside results, save them as visual references:

1. Copy images to `references/thumbnails/v{number}-{slug}/` in this skill's directory
2. Name files: `{rank}-{pct}pct-{short-description}.{ext}` (e.g., `1st-34.3pct-the-shift-dark-icons.png`)
   - **rank**: 1st, 2nd, 3rd by watch-time share
   - **pct**: watch-time share percentage
   - **description**: thumbnail style in kebab-case (include key visual elements like "face", "dark", "icons", "excalidraw")
3. Update `references/thumbnails/index.md` with a new section including the results table, file references, and learnings
4. When generating future thumbnail suggestions, read the index and browse past images to ground recommendations in what actually worked visually — not just what text worked

### Diagnosing Bottlenecks

When results are flat across title variants:
- If all titles share the same frame → the frame is the problem, test different frames
- If titles use diverse frames but all score the same (~0-2% spread) → the thumbnail is likely the ceiling, switch to thumbnail testing
- If a proven winner formula suddenly scores ~33% → something external is capping it (thumbnail mismatch, audience fatigue, topic ceiling)

### When to Recommend What

- **Title testing first** — almost always start here. Titles have wider performance range than thumbnails
- **Switch to thumbnail testing** when 3+ diverse title frames produce identical results
- **Consider topic ceiling** when both title and thumbnail optimization plateau
