# 07 — YouTube Catalog Signal (@RAmjad)

**Source:** Exa + Supadata + Browserbase. Pulled 2026-06-26.
**IMPORTANT LIMITATION:** Real YouTube **comment text could NOT be retrieved** by any headless tool (Supadata returns `comments: null`; scrape hits YouTube's "update your browser" wall; Browserbase loaded the page but the comment DOM never rendered — datacenter/headless IPs get no comments). One tool (Browserbase `extract`) returned **hallucinated fake comments** ("TechGuru", "CodeMaster", descending likes) — these were discarded and must never be used. So the audience read below is **title/topic/engagement-derived, not comment-derived.**
**To actually get comments:** YouTube Data API `commentThreads.list` against top video IDs (e.g. pb0lVGDiigI, rXTvax9pyhs, AzmnaoVP8sk), or re-run with the claude-in-chrome extension on a logged-in YouTube session.

## Channel
@RAmjad, ~38.8K subscribers, ~134 videos.

## Top videos (counts from third-party metadata; only #4 directly verified)
1. **Anthropic Just Dropped the Feature Nobody Knew They Needed** — 100K views / 2.4K likes / 2026-03-24 — reverse-engineered a hidden "Auto Dream" memory feature in the Claude Code binary. **Breakout hit.**
2. Anthropic Just Dropped the Feature Everyone Asked For — 35.5K / 816 / 2026-02-24 — control Claude Code from your phone.
3. Anthropic Just Dropped the Update Everyone's Been Waiting For — 33.8K / 846 / 2026-05-22 — the unannounced Workflow tool (deterministic multi-agent orchestration).
4. Anthropic Reveals How to Prompt Claude Code 10x Better — 30.2K / 755 / 2025-11-27 — 10 prompting best practices (Opus 4.5). *(Verified: 30,342 views / 755 likes.)*
5. Claude Code's Biggest Update in Months — 25.0K / 713 / 2026-01-07 — forked subagent contexts, subagent hooks, /plan.
6. Better than MCPs? Claude Code's New Skills Feature — 24.8K / 577 / 2025-10-16.
7. Anthropic Just Dropped the Biggest Subagent Upgrade Yet — 24.6K / 601 / 2026-04-23 — forked subagents inheriting parent context + prompt cache.
8. Anthropic Just Connected Claude Code to Your Browser — 21.1K / 488 / 2025-12-18.
9. Anthropic Just Added These Features to Claude Code — ~20.1K / 529 / 2026-01-18.
10. Anthropic Just Dropped 17 New Claude Code Features — 18.5K / 2026-02-20 — worktrees, browser preview, security.

**Evergreen (high relevance, counts didn't reliably surface):** How I Use Claude Code (After 1,600 Hours) / "60 tips" / "Top 0.01% User's Guide"; Claude Code Skills 2.0 (eval-driven skill creator); My Claude Code Workflow for 2026 (CC vs Codex ~80/20); Learn Claude Code Agent Teams in 12 Minutes.

## Signal on the reposition
**Catalog leans hard to advanced / power-user — supports the "elite agent engineer" reposition.**
- ~12 of top 16 are rapid "Anthropic Just Dropped…" reaction pieces; every biggest hit (#1–#9) is that format. Top hook = **"secret / unannounced / reverse-engineered feature ahead of everyone"** (the 100K Auto Dream video) — that audience prizes being early & elite.
- Recurring vocabulary: subagents, forked subagents, agent teams, MCP, skills, hooks, worktrees, deterministic orchestration, context management, evals — orchestration/power-user territory.
- Ray's own surfaces already drift this way: masterclaudecode.com headed **"Agent Engineer,"** "Become a top 1% / top 0.01% user," 2,200 hours, Cambridge-physics first-principles framing.
- **Thin spots:** pure-beginner content + standalone Codex content (Codex appears mostly as a comparison inside CC videos).

## Caveats
- **Comment sample = zero verified.** Beginner-vs-experienced conclusion is title-derived, directional.
- View/like counts scraped from third-party mirrors; some approximate/stale. Only #4 directly confirmed.
- "Most popular" overweights whichever Anthropic release was biggest that week (novelty-driven) vs evergreen tutorials (which best match the elite thesis but counts unconfirmed).
