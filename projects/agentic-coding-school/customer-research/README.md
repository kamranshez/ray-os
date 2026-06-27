# Customer Research — Agentic Coding School

**Purpose:** the standing source of truth on *who buys this class, what they want, and how to position to them.* Read this folder instead of re-deriving the audience every time. When you write or revise landing-page copy, VSL scripts, ads, or pricing, start here.

**Last major update:** 2026-06-26 (first build — 6-source market analysis).
**Owner:** Ray. Built with a fan-out of research subagents (PostHog, PlanetScale, Gmail, course content, Exa web research, customer enrichment).

## How to use this folder

1. Start with **`00-synthesis-personas-positioning.md`** — the personas + the positioning recommendation + the open decisions. This is the part you actually act on.
2. Drop into the numbered source files only when you need the evidence behind a claim, or to re-check a number.
3. When new data comes in (re-pull the survey, new buyer cohort, A/B results, real student outcomes), **append to the relevant source file and update `00-...`'s "Last reviewed" line.** Keep this folder current; it's meant to be ongoing.

## Files

| File | What's in it |
|---|---|
| `00-synthesis-personas-positioning.md` | **The deliverable.** 5 customer personas, the positioning recommendation, naming/price/team decisions, and open questions. |
| `01-newsletter-survey-posthog.md` | Confirm-page newsletter survey: role, experience, biggest-challenge distributions + free-text themes. Acquisition channels. |
| `02-paying-customers-db.md` | PlanetScale buyer profile: 2,155 paying customers, tier breakdown, email-domain (corporate vs freemail) profile. |
| `03-customer-enrichment.md` | Who specific corporate buyers actually are (roles, seniority, companies) — incl. the MCG Health 60-seat enterprise rollout. |
| `04-gmail-testimonials.md` | First-party testimonial language + friction signals mined from the inbox. Copy-ready verbatim quotes. |
| `05-course-content-arc.md` | What the curriculum actually teaches beyond tool basics (Loopy AI L1-L7, context engineering, orchestration) + the transformation arc + proof points. |
| `06-competitor-naming-pricing.md` | "agent engineer" vs "agentic coding" vs "AI engineer" term maturity; competitor positioning table; price anchors. |
| `07-youtube-catalog.md` | @RAmjad top-video catalog + the power-user signal. (Note: real comment text could NOT be retrieved — see file.) |

## One-line takeaway

The audience is **senior, already fluent in the tools, and asking to level up.** Position around the **"agent engineer" identity** (elite, loop/orchestration-level), keep a **fundamentals on-ramp** for the ~1/3 beginner/non-traditional-dev tail, lead SEO with **"agentic coding,"** and **$500–600** is supported if the identity earns it. There's an untapped **team/enterprise lane.**

## Key caveats baked into the data (don't forget these)

- Survey experience/challenge questions are **small-n (~32–35), launched ~Jun 21 2026** — re-pull in a few weeks to firm up.
- Buyer **tier/cadence is inferred** (DB `tier` col is uniformly 'pro'); amount/source cols mostly NULL (un-backfilled, not $0 sales).
- "Corporate vs freemail" (30/70) is a **floor** on professionalism — many senior engineers buy with a personal Gmail.
- **YouTube comment text was not retrievable** by headless tools; that signal is title/topic-derived only. To get real comments: YouTube Data API `commentThreads` or a logged-in Chrome session.
- Strongest proof point (19hr / ~300 Chrome flows / Boris "Nice") is **Ray's own result, not a student's** — frame accordingly. Verified student outcomes are still thin.
