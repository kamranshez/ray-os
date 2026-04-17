# Markdown Audit Template

The canonical reference is the previous month's audit (most recently `/Users/ray/Desktop/ray-os/socials/youtube/performance/2026-03.md`). Match its structure exactly. This file lists the 5 required sections, the mandatory tables, and the rules that make the doc publish-ready.

## Global rules

- **No H1 title** — the filename is the title (Obsidian convention)
- **No em or en dashes** anywhere — use hyphens, colons, or periods. This is a hard rule from Ray's feedback memory.
- Dates as `Mar 2`, `Mar 11`, etc. in tables; `2026-03-02` in the daily log
- kebab-case filenames: `YYYY-MM.md` and `YYYY-MM-chart.html`
- Section headers use `##`, subsections `###`
- Never invent data. If a number isn't available, write "N/A" or omit the row. Never guess.

## Required structure

### Part 1: Content Audit — Views & Structure

- Opening paragraph: date, data sources, channel sub count at time of audit
- **Videos at a Glance** table: `#, Title, Upload, Views, Duration, Format`
- Average views / sub count ratio, compared to previous month
- **Focus vs Views** table: structure types (single-feature, pillar, thesis, etc.) with avg views
- **What Worked This Month**: 3–5 numbered observations with evidence
- **What Didn't**: 2–4 numbered observations
- **Scorecard** table: techniques from outlier research, previous month's score, this month's score, change direction

### Part 2: Revenue Audit

- **Methodology and its limits** subsection — explain the three data sources, the 3-day window, and quote the exact attribution coverage % for the month. **The coverage % determines how much weight you put on PostHog findings in the rest of the audit.** See `methodology.md` for the rubric.
- **Revenue Summary**: baseline vs video-window vs multiplier. Compare to previous month's multiplier.
- **Per-video table**: `#, Video, Date, Views, Sales, 3-Day Gross, Net, Avg Order, Opening Tactic`
- **Note on overlap** callout if any 2+ uploads land within 72 hours of each other
- **PostHog Cross-Check** table: `#, Video, YT Views, Site Visitors (unique), Click-Through %, Tagged Purchases, Tagged Revenue, Stripe 3-day`
- **3 findings the PostHog data reveals** that Stripe-only couldn't — pick the three biggest divergences between the two sources
- **Daily Revenue Log** table: every day of the month, `Date, Sales, Gross, What Happened`
- **Pricing Over Time** table: coupons, AOV drift, comparison to prev month

### Part 3: Pitch-to-Revenue Correlation

For each notable video (usually 5–7 of the month's uploads):

- Header: `**Video N — Date — $Gross / Sales / $AvgOrder — LABEL**` where LABEL might be "BEST REVENUE", "WEAKEST", "LOWEST AOV", etc.
- Verbatim quoted opening (first ~60s)
- Verbatim quoted mid-video or closing pitch
- 2–3 sentences of commentary on what worked or didn't, tied to revenue shape

Then:
- **Tactic-by-Tactic Revenue table**: `Tactic, With, Without, Diff` — compute from the month's videos
- **Spike Shape by Pitch Type**: `Video, Day 1, Day 2, Day 3, Shape`

### Part 4: Hypotheses to Test

- **Core Tensions** subsection — 2–4 paragraphs on the month's biggest observations
- **Carry over** previous month's hypotheses (H1, H2, ...) and mark each as **Validated**, **Invalidated**, or **Still open** with one line of evidence from this month
- **Add new hypotheses** (usually 1–3) numbered H-N with test proposals
- **Testing Priority** list — numbered, with the top item usually being any engineering fix that unblocks measurement (like H7 from the March doc on checkout UTM persistence)

### Part 5: Specific Fixes for Next Month

- **Opening formula** (name it after the winning video, e.g., "the Mar 7 template")
- **Closing formula** (same pattern)
- **What NOT to do** bullet list
- **Revenue target for next month** with reasoning grounded in this month's numbers

## Voice and tone

Plain, direct, analytical. Short sentences. No hedging like "perhaps" or "it seems that." Quote verbatim when quoting, paraphrase sparingly. Don't try to sound smart — try to be clear. Use the previous month's doc for tone calibration.
