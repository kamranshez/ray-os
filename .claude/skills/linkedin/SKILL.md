---
name: linkedin
description: All LinkedIn tasks — writing posts (text or carousel), checking post performance, browsing the feed, or analyzing competitors. Triggers on any mention of LinkedIn, including "write a LinkedIn post", "make a LinkedIn carousel", "swipeable LinkedIn post", "LinkedIn slides", "check my LinkedIn", "how did my posts do", "LinkedIn competitors", "post on LinkedIn", "browse LinkedIn feed". Also triggers on "check post engagement", "update post metrics", or reviewing social media performance. This is the single master LinkedIn skill — carousel generation, text-post writing, performance checking, and feed browsing all live here.
---

# LinkedIn

Single master skill for everything LinkedIn — writing (text or carousel), checking performance, and browsing.

## Routing

Once todos are handled, figure out which sub-flow the request needs. If Ray's message doesn't already make it obvious, ask:

1. **Write a post** → next question: text post or carousel?
2. **Check post performance** → Read `references/check-performance.md`
3. **Browse / research / analyze competitors** → Read `references/browser-navigation.md`

### When Ray wants to write a post

**Always ask first: text post or carousel?** Carousels in Ray's niche skew much higher on reactions and reposts than text posts (e.g. Anthropic carousel: 2,523 reactions / 181 reposts; Charly's Zero Trust carousel: 491 / 82). But they take more time and have a different drafting flow.

Use AskUserQuestion with two options:

- **Text post** — single LinkedIn post, 10 variations generated, Ray picks one. Use `references/write-post.md`.
- **Carousel** — multi-slide swipeable PNG deck (cover + content slides + CTA), proposed outline first then rendered. Use `references/carousel.md`.

Both flows share the same upstream: read `references/viral-playbook.md` — the **Stanislav template**, the single fixed skeleton every post uses — plus 3-5 recent files in `references/post-history/` for dedupe. Use only files carrying `template: stanislav` in frontmatter for VOICE; if none do yet, take structure from the skeleton alone. Untagged history files predate the template and will pull you off it. All variations are generated inside that skeleton; never invent a new structure per post.

## Quick Reference

- **Profile:** https://www.linkedin.com/in/rayamjad/
- **Activity:** https://www.linkedin.com/in/rayamjad/recent-activity/all/
- **Post history:** `references/post-history/` (one file per post, YAML frontmatter + body)
- **Template:** `references/viral-playbook.md` — the Stanislav skeleton, variation axes, house rules
- **Pre-post gate:** `references/post-gate.md` — the 10-point checklist; the cloud routine runs this same file
- **Source research:** `references/analysis/` — Stanislav's source-system note and raw feed capture, plus archived competitor analysis
- **Carousel scripts:** `scripts/render-carousel.py`, `scripts/prep-carousel-profile.py`
- **Carousel assets:** `assets/profile.png` (Ray's pre-cropped avatar)
- **Chrome automation:** All browser interactions use `mcp__claude-in-chrome__*` tools

## Maintenance

The template evolves from two feedback sources only:

1. **Ray's edits** — when he rewrites a draft by hand, diff it and append the lesson to the "Learning loop" section of `viral-playbook.md` before the session ends.
2. **Engagement data** — post-history engagement numbers. When a post clearly over- or under-performs, note which variation axes (hook type, closer, angle) it used.

To recalibrate against the source, re-scrape Stanislav's feed (linkedin.com/in/stasbel) and update `references/analysis/2026-07-stanislav-beliaev-source-system.md` — the skeleton in the playbook derives from that analysis.

`routines/linkedin-source-scout.md` (the daily cloud routine) reads `references/viral-playbook.md` and `references/post-gate.md` directly from this skill on every run. It owns sourcing; this skill owns writing. Change the template here and the routine picks it up for free — never fix a writing rule by editing the routine.
