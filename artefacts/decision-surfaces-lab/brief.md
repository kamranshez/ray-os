---
tags: [decision-surfaces, acs, analytics]
date: 2026-07-13
---

Shared brief for the decision-surface variation sweep. Every agent building a variation reads this first.

## Who this is for

Ray Amjad, YouTube educator (@RAmjad) who sells the **Agentic Coding School** course: **$397 one-time lifetime purchase**. That course is effectively all site revenue. There is no monthly membership and none is planned. Primary acquisition is his YouTube channel; the site at agentic-coding-school also hosts member class pages and a newsletter.

## The job of your surface

Ray will open your HTML file and should be able to make **real revenue decisions** from it, today. The twin goals:

1. Improve his understanding of what the traffic data means for revenue.
2. Be a candidate for the *standing format* he adopts for consistently good decisions going forward.

## The data

Read `/Users/ray/Desktop/ray-os/artefacts/acs-traffic-dashboard.html`. The real data arrays are embedded in the `<script>` block (`daily`, `hourly`, `channels`, `pages`, `pagesFull`). Headline facts:

- 12,684 unique visitors last 30 days, **−14%** vs previous 30 (14,665). Pageviews and sessions flat, avg session +6%, bounce −8%.
- Channels (visitors / views): Direct 5,400/8,914 · Referral 3,649/16,066 · Organic Video 1,975/1,981 · Organic Search 1,575/2,581 · Email 912/1,266 · Organic Shopping 275/332 · Organic Social 131/176.
- Notable ratios: Referral averages 4.4 views/visitor (deep engagement); Organic Video averages 1.0 (lands and leaves).
- Top pages (visitors): `/` 6,891 · `/auth/sign-in` 2,631 · `/member` 1,117 · `/member/class/claude-code` 899 · `/newsletter` 736 · `/member/class/loopy-ai` 673 · `/auth/callback` 500 · `/auth/sign-up` 475 · `/unsubscribe` 408 · more class pages ~300-350 each.
- Daily series contains a big spike on 2026-06-20 (1,367 visitors, an outlier) and a visible drift down through July. 2026-07-12 is a partial day.

**Do not query external services or PostHog.** The embedded data plus clearly-labeled adjustable assumptions IS your dataset. Anything not in the data (conversion rate to purchase, revenue per period, YouTube upload dates) must be exposed as an explicit, user-adjustable assumption — never invented as fact.

## Quality bar

Read `/Users/ray/Desktop/ray-os/artefacts/decision-surfaces.md` (Ray's own essay — this sweep exists to test its thesis). Apply at minimum:

- **Surface decisions, not documents.** Concrete open questions with options, tradeoffs, evidence, and a recommended default are first-class interactive objects, visually distinct from background analysis. Aim for 3-7 real decisions.
- **Provenance tags on every claim**: `data` (computed from the arrays), `assumption` (adjustable input), `judgment` (your recommendation). A misleading surface is worse than none.
- **Write-back channel**: every choice, slider setting, annotation, and note the user makes must be capturable via a "Copy decisions JSON" (or download) export so an agent can re-ingest it. Use localStorage so state survives reload.
- **Whole before parts**: the first screenful gives the gestalt; detail on demand.
- **Honest at every altitude**: label the partial day, the spike outlier, the channel double-count (channel visitors sum above the 30-day unique total because returners re-enter via different channels).

## Tech constraints

- One **self-contained HTML file**, vanilla JS + inline SVG/CSS. **No CDN, no external requests** — must work offline via `file://`.
- **DARK theme by default** — dark background always, regardless of OS `prefers-color-scheme` (match the dashboard's dark palette variables if you like), `system-ui` font.
- Genuinely interactive: hover detail, click-to-drill, sliders/inputs per your direction. Not a static poster.
- Write your file to `/Users/ray/Desktop/ray-os/artefacts/decision-surfaces-lab/<your-assigned-filename>`.

## Return format

Return 3-4 sentences: what your surface does, the single most important decision it surfaces, one non-obvious insight you found in the data, and your filename.
