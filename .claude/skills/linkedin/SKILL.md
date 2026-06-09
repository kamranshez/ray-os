---
name: linkedin
description: All LinkedIn tasks — writing posts (text or carousel), checking post performance, browsing the feed, or analyzing competitors. Triggers on any mention of LinkedIn, including "write a LinkedIn post", "make a LinkedIn carousel", "swipeable LinkedIn post", "LinkedIn slides", "check my LinkedIn", "how did my posts do", "LinkedIn competitors", "post on LinkedIn", "browse LinkedIn feed". Also triggers on "check post engagement", "update post metrics", or reviewing social media performance. This is the single master LinkedIn skill — carousel generation, text-post writing, performance checking, and feed browsing all live here.
---

# LinkedIn

Single master skill for everything LinkedIn — writing (text or carousel), checking performance, and browsing.

## Step 0: Always read `todos.yaml` first

**On every invocation of this skill, before doing anything else, read `todos.yaml` in this skill directory.** It tracks drafts waiting to be posted, posts needing engagement checks, and other LinkedIn follow-ups.

- If any entries are overdue or due today, surface them to the user before taking their current request: *"Heads up — you have N LinkedIn drafts/follow-ups waiting: [list]. Want to handle those first, or continue with [current request]?"*
- If nothing is due, proceed silently with the user's request.
- When you complete a todo (post a draft, check engagement, etc.), update its `status` to `done` or remove it. Do not let completed entries pile up.
- When you create a new draft, add an unposted post, or need a follow-up, add a new entry to `todos.yaml` — not to any global todos file. LinkedIn todos live inside this skill.

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

Both flows share the same upstream: read `references/viral-playbook.md` (especially the 8 format patterns), read the most recent month folder in `references/viral-examples/`, then run the **earned-authority quiz** before drafting. The quiz step is described in `references/write-post.md` and applies to carousels too.

## Quick Reference

- **Profile:** https://www.linkedin.com/in/rayamjad/
- **Activity:** https://www.linkedin.com/in/rayamjad/recent-activity/all/
- **Post history:** `references/post-history/` (one file per post, YAML frontmatter + body)
- **Viral examples:** `references/viral-examples/<YYYY-MM>/` — per-author files with engagement metrics + what-to-steal notes
- **Viral playbook:** `references/viral-playbook.md` — 8 format patterns + 6 emotional triggers
- **Carousel scripts:** `scripts/render-carousel.py`, `scripts/prep-carousel-profile.py`
- **Carousel assets:** `assets/profile.png` (Ray's pre-cropped avatar)
- **Chrome automation:** All browser interactions use `mcp__claude-in-chrome__*` tools

## Maintenance

When Ray asks to refresh the viral examples (or notices the discourse has shifted), spawn a fresh capture sweep:

1. Open LinkedIn search for "Claude Code" (or whichever niche keyword), sort by Top Match
2. Scroll several screens, capture page text
3. For each post with 50+ reactions or notable engagement structure, write a file to `references/viral-examples/<YYYY-MM>/<author-slug>.md` with the YAML schema used in the 2026-06 examples (engagement counts, why_it_works, what_to_steal_for_ray)
4. After 10-15 posts captured, distill any new cross-cutting patterns into the format-patterns section of `viral-playbook.md`

The format patterns evolve. Don't assume the 8 in the playbook are eternal — check what's actually working in the latest month folder before drafting.
