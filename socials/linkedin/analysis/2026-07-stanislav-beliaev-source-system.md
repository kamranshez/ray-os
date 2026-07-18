---
tags: [linkedin, competitor-analysis, content-system]
aliases: [Stanislav Beliaev source system]
date: 2026-07-18
---

Reverse-engineering of Stanislav Beliaev's LinkedIn content machine (Co-Founder/CTO GetFluently.App, YC W24, ex-Nvidia -- linkedin.com/in/stasbel), from a saved copy of his activity feed (9 posts, Jul 3-17 2026). Feeds the [[linkedin-source-scout]] routine (`routines/linkedin-source-scout.md`).

## The system in one line

Monitor GitHub trending + model launch announcements + viral X charts, pour every find into ONE fixed template with a shock hook and arrow-bullet specs, post 4-5x/week, self-repost winners after ~24h, and end every post with the same P.S. funnel CTA for his product.

## Cadence

- Posts Jul 3, 6, 7, 9, 10, 10, 15, 17 -- roughly every 1-2 days, ~4-5/week, late morning/early afternoon UTC, weekdays.
- Self-reposts a winning post ~24h later to bump it (observed once: identical text, same engagement object).
- All posts marked "Edited" (he tweaks after posting).

## Data sources, ranked (8 unique posts)

1. **GitHub trending / high-star repos -- 5 of 8 posts.** Tells: star-count hooks ("just hit 87k+ stars", "crossed 28k+"), "Link to the repo:" + lnkd.in shortlink, spec bullets lifted straight from READMEs. Bias toward AI-agent tooling (memory, voice, knowledge graphs) plus anything virally interesting even off-niche (AirPods protocol reverse-engineering).
2. **Model/vendor launch announcements -- 1-2 posts.** Sourced from official launch blogs; always includes pricing, tokens/sec, and benchmark tables, plus a CEO quote.
3. **Viral charts/analyses from X or HN -- 1 post.** Tell: "Someone charted/shipped/reverse-engineered..." hook -- re-narrating someone else's artifact, adding his own extrapolation, usually without attribution.
4. **Personal founder story / company milestones -- 1 post,** used sparingly. His single best performer (3,299 reactions vs 174-1,755 for content posts): the "At 18: rejected... At 26: YC + $2.5M" rejection-arc template.

No arxiv.org or huggingface.co in the sample -- he is repo-first, not paper-first.

## The template (7 of 8 posts)

1. Hook line ending in a colon: news + superlative/shock ("China open-sourced a model that...", "This repo just hit 87k+ stars 🔥", "🚨 X JUST launched Y").
2. 1-3 short scene-setting lines ("One camera. No LiDAR. No calibration rig.").
3. Name reveal: "It's called <Name>."
4. Arrow bullets (→) for specs/benchmarks, hyphen bullets for feature lists. Numbers everywhere: stars, FPS, %, $/M tokens.
5. One "why it matters" paragraph.
6. "Link to the repo:" + lnkd.in shortlink (never a raw URL -- shortlinks dodge LinkedIn's external-link penalty tracking and let him swap destinations).
7. Optional "Your thoughts?" engagement bait.
8. Identical P.S. every post: "P.S. We're building the best AI English tutor in the world... 15x cheaper than a human one → GetFluently.app". The content pipeline exists to feed this funnel line.

Length ~150-250 words. Engagement observed: 174 to 3,299 reactions per post.

## Implications for Ray's version

- The moat is not writing quality, it is **source monitoring + a fixed template + relentless cadence**. Each post is ~30 min of human effort at most; his inputs are public and automatable.
- Ray's equivalents: GitHub trending (agentic-coding tools), HN front page / Show HN, model vendor launch blogs, viral X posts. Funnel P.S. slot = Agentic Coding School.
- Content posts feed reach; the rare personal-story post is the engagement outlier. Keep a ~1-in-8 personal slot.
- Implemented as the daily cloud routine `routines/linkedin-source-scout.md` posting draft candidates to Slack #li-source-scout.

Full extracted posts (all 9, verbatim, with engagement): captured 2026-07-18 from the saved HTML; source file `/Users/ray/Downloads/(1) Activity _ Stanislav Beliaev _ LinkedIn.html`.
