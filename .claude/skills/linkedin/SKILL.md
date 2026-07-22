---
name: linkedin
description: All LinkedIn tasks — writing posts (text or carousel), scouting sources to post about, checking post performance, browsing the feed, or analyzing competitors. Triggers on any mention of LinkedIn, including "write a LinkedIn post", "make a LinkedIn carousel", "swipeable LinkedIn post", "LinkedIn slides", "check my LinkedIn", "how did my posts do", "LinkedIn competitors", "post on LinkedIn", "browse LinkedIn feed". Also triggers on "check post engagement", "update post metrics", or reviewing social media performance. Also use it for finding something to post about — "find me a LinkedIn topic", "run a source sweep", "scout me something on MCP", "what should I post today", or reviewing the drafts the daily scout left in Slack #li-source-scout. This is the single master LinkedIn skill — sourcing, carousel generation, text-post writing, performance checking, and feed browsing all live here.
---

# LinkedIn

Single master skill for everything LinkedIn — writing (text or carousel), checking performance, and browsing.

## Step 0: Check for drafts waiting from the last sweep

The source scout (below) runs daily in the cloud and leaves its drafts in Slack **#li-source-scout**. That thread is the queue — so before taking Ray's request, read the **most recent sweep only** (Slack MCP `slack_read_channel`) and work out what is still pending:

- A draft is **handled** if a file in `references/post-history/` covers the same topic. Everything else in that thread is pending.
- Only the latest sweep is ever surfaced. Looking further back would resurrect drafts Ray deliberately passed on, since killing a draft leaves no history file to mark it dead. One sweep of memory means a passed-over draft reappears once at most, then tomorrow's sweep replaces it.
- If there are pending drafts, say so before anything else: *"This morning's sweep left N unreviewed drafts: [list]. Review those, run a fresh sweep, or something else?"*
- If the latest sweep is pending-free, or is older than about a day, mention that a fresh sweep is available and move on to Ray's request. A conspicuously missing sweep is worth flagging out loud — it is the only visible sign the cloud routine has stopped running.
- If Slack is unreachable, say so in one line and continue. Never block the request on it.

## Routing

Figure out which sub-flow the request needs. If Ray's message doesn't already make it obvious, ask:

1. **Write a post** → next question: text post or carousel?
2. **Check post performance** → Read `references/check-performance.md`
3. **Browse / research / analyze competitors** → Read `references/browser-navigation.md`
4. **Scout for sources** ("find me something to post about", "run a sweep", "scout me something on MCP") → Read `references/source-scout.md`

### When Ray wants to write a post

**Always ask first: text post or carousel?** Carousels in Ray's niche skew much higher on reactions and reposts than text posts (e.g. Anthropic carousel: 2,523 reactions / 181 reposts; Charly's Zero Trust carousel: 491 / 82). But they take more time and have a different drafting flow.

Use AskUserQuestion with two options:

- **Text post** — single LinkedIn post, 10 variations generated, Ray picks one. Use `references/write-post.md`.
- **Carousel** — multi-slide swipeable PNG deck (cover + content slides + CTA), proposed outline first then rendered. Use `references/carousel.md`.

Both flows share the same upstream: read `references/viral-playbook.md` — the **Stanislav template**, the single fixed skeleton every post uses — plus 3-5 recent files in `references/post-history/` for dedupe. Use only files carrying `template: stanislav` in frontmatter for VOICE; if none do yet, take structure from the skeleton alone. Untagged history files predate the template and will pull you off it. All variations are generated inside that skeleton; never invent a new structure per post.

### When Ray wants a sweep

`references/source-scout.md` is the scout: four source lanes (GitHub trending, Hacker News, launch news and talks, Reddit), 2-3 picks, each drafted in the Stanislav skeleton and passed through the same `post-gate.md` as everything else.

Two things worth knowing before running it:

- **It always posts to Slack**, even when Ray is sitting right there. The channel's 14-day history is the dedupe ledger — a sweep that stays local is invisible to tomorrow's cloud run, which will then re-surface the same repo. Slack is a side effect; Ray still gets the drafts inline and in the HTML preview.
- **A focus is optional.** Bare "run a sweep" does exactly what the cloud does. "Scout me something on MCP" or "just Hacker News today" filters the candidates or the lanes and changes nothing else.

When Ray picks a draft, the scout hands off to `references/write-post.md` at its "After Ray Picks" step. Refinement, the `post-history/` file, and publishing all live there.

## Scheduled work

The scout is the one LinkedIn job that runs on a schedule: daily, 9am JST, as a cloud routine. `routines/linkedin-source-scout.md` is a stub whose only job is to point back here and name the cloud contract; the real instructions are `references/source-scout.md`, which the cloud and Ray run alike. Fix scout behaviour in the skill, never in the routine stub.

## Quick Reference

- **Profile:** https://www.linkedin.com/in/rayamjad/
- **Activity:** https://www.linkedin.com/in/rayamjad/recent-activity/all/
- **Post history:** `references/post-history/` (one file per post, YAML frontmatter + body)
- **Template:** `references/viral-playbook.md` — the Stanislav skeleton, variation axes, house rules
- **Pre-post gate:** `references/post-gate.md` — the 10-point checklist; every flow runs this same file
- **Source scout:** `references/source-scout.md` — the 4-lane sweep, run daily by cloud cron and on demand by Ray
- **Drafts queue:** Slack `#li-source-scout` — main message per sweep, one threaded reply per draft
- **Source research:** `references/analysis/` — Stanislav's source-system note and raw feed capture, plus archived competitor analysis
- **Carousel scripts:** `scripts/render-carousel.py`, `scripts/prep-carousel-profile.py`
- **Carousel assets:** `assets/profile.png` (Ray's pre-cropped avatar)
- **Chrome automation:** All browser interactions use `mcp__claude-in-chrome__*` tools

## Maintenance

The template evolves from two feedback sources only:

1. **Ray's edits** — when he rewrites a draft by hand, diff it and append the lesson to the "Learning loop" section of `viral-playbook.md` before the session ends.
2. **Engagement data** — post-history engagement numbers. When a post clearly over- or under-performs, note which variation axes (hook type, closer, angle) it used.

To recalibrate against the source, re-scrape Stanislav's feed (linkedin.com/in/stasbel) and update `references/analysis/2026-07-stanislav-beliaev-source-system.md` — the skeleton in the playbook derives from that analysis.

Everything the scout needs — lanes, skeleton, gate — now lives in this skill, so there is nothing outside it to keep in sync. `routines/linkedin-source-scout.md` is a pointer, not a copy. Change the template or the lanes here and the daily cloud run picks it up on its next clone.
