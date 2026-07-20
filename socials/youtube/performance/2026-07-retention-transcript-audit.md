---
tags: [youtube, retention, self-audit, strategy]
aliases: [July 2026 Retention Audit]
date: 2026-07-18
---

Channel-wide audit of 36 videos — **every video published in 2026 (35)** plus 5 older evergreen outliers: retention curves (VidTempla) + full transcripts, analyzed by 8 parallel agents (winners / tier-2 winners / guides / news losers / format experiments / evergreens / 2 gap-fill batches) and cross-checked against the A/B archive (V1–V37). Analysis date 2026-07-18, view counts = Oct 2025 → Jul 2026 window unless noted.

## The headline

**The channel's fate is decided at the click, not in the video.** Of the 11 underperformers analyzed, 10 had normal-to-excellent retention — several (CLAUDE.md leverage 31.6%, nested subagents, Fable-5 "1 Day Left") retained *better* than the 30–100K winners. Views collapsed because fewer people clicked, not because people left. The one true content collapse was a redundancy: "(Fully Explained)" re-cover posted 7 days after the 46K news video → instant 98%→34% wall in the first 3% of the video.

This confirms the two ceilings in the A/B archive, now visible live in retention data:

- **Thesis/framework lane ~17K max** vs **single-named-feature lane ~45K** (Boris levels + Loop Engineering cluster at the bottom of first-7h cohorts; fires the subscriber-skip card; title A/Bs flatline within ~1pp = external cap)
- **Non-Anthropic topic cap** independent of format (Codex videos cap ~7K vs 40K+ Claude equivalents)

## What wins the click (title/packaging patterns, retention-verified)

1. **Concrete noun + tactic-promise.** The cleanest natural experiments:
   - "Even Anthropic Engineers Use This **Workflow**" (11.4K) vs "**I Spent a Day** With Anthropic Engineers" (4.3K, best raw AVD in its batch). Naming authority is fine as social proof; the title's core promise must be a transferable capability, not a person or a story.
   - "The Highest Point of Leverage" flop (8.2K) had the **highest avg-view-% of all five guide videos** — but the title names no concrete noun (never says CLAUDE.md), no number, no feature → no CTR → zero algorithmic legs after day 2.
2. **Dated event + loss-framed FOMO.** "Fable 5 **Is Back Tomorrow!** (Don't Waste It)" 22K vs "1 Day Left… Maximize It" 5.6K — same subject, same week, equal-or-better retention on the loser. 4x gap bought entirely by the concrete date + sharper loss frame.
3. **No re-covers, no title reruns.** Near-duplicate title ("Biggest Subagent Upgrade Yet" twice) → second run got 1/3 the views. Deep-dive follow-up a week after the news video → the only true retention collapse in the dataset. Cover a topic once, fresh angle each time.
4. **Task-query titles are the evergreen engine.** "How to Make **Anki Flashcards** 10x Faster with AI" = 341K lifetime and still ~200K/9mo because it's the literal answer to a durable search query. Its sibling ("The AI Study Method Top Students Use") runs the identical workflow with a vague concept title → 10x less. Search-shaped retention fingerprint on both: skip-and-rebound, spikes on every concrete on-screen step.

## What holds viewers (retention mechanics)

- **Live demos are the retention engine.** Every relative-performance spike across all 27 videos maps to the feature *running on screen* (/btw inline answer caused a mid-video retention RISE; two-session task list; /tasks dreaming; 13-hour Codex goal). Every recurring cliff maps to one of four killers: **abstract theory/taxonomy blocks, config/setup instructions, waiting-for-process dead air, end-of-video speculation monologues**.
- **Payoff in sentence one.** The top retention %s (cron "killed OpenClaw" 35.9%, /btw 33.2%) deliver the payoff instantly; the steepest early cliffs follow setup preamble (env vars, tmux-alternatives history).
- **Single-topic depth with a back-half payoff beats roundups.** Task System (36.4%, strengthens toward the finish) and Ultra Plan (second relPerf surge at the hidden-modes reveal) vs "Biggest Update in Months" — roundups leak at every feature transition and its tail collapsed (relPerf 0.52→0.05) during closing speculation.
- **Reverse-engineering reveals are a signature asset.** Binary teardowns produce *late-video* retention surges (Ultra Plan hidden modes; Ultrareview's set-high 0.72–0.75 spike at 74–80%). Structure videos so a reveal lands in the back half.
- **The honest-review contract produces end-peaks.** Replit review: relPerf *peaks* at 78–82% (the verdict) — 31.6% avg-view on 18 minutes. Almost nothing else on the channel makes people stay for the ending.
- **Chapter density carries long videos.** 60-tips/41-min guide: 60 timestamps = 60 micro-hooks, jumpable, no sponsor → 347s AVD, no cliffs, holding 13% at 41 minutes.
- **Sponsor reads in the 0:12–3:10 window cost a measurable dip every single time** (worst case: the 1:40 read detonated the steepest cliff of its batch, 46%→27%). Reads placed after value ("Loop Engineering" ~8min, woven into momentum) show shallow dips with clean recovery. The no-mid-roll 60-tips video had no plug-shed at all.
- **Back-third drift off the titular promise bleeds.** Agent Teams held best-in-batch until it finished the promised content and pivoted to a grab-bag of unrelated updates; Anki video decayed through its use-case list tail.

## Do / stop / try

**Do:**
- Default lane stays: single named feature, "Anthropic Just Dropped" + stakes (competitor-kill / nobody-knew-they-needed / going-viral), demo-led, payoff in sentence one.
- Smuggle frameworks inside feature videos (feature = hook, thesis = payload) — never as the packaging.
- Build a reverse-engineering reveal into the back half whenever there's one to find.
- More brutally-honest reviews — the only format with an end-of-video retention peak, and it compounds reputation (matches the [[project_format_strategy_test_vs_news]] thesis).
- Feed the study niche deliberately but surgically: a small cadence of **task-query** tutorials ("make Anki cards from a PDF" class of titles), kept structurally separate from the coding identity.

**Stop:**
- Sponsor/newsletter reads before ~3:00 (and before ~60% on search-shaped how-to videos).
- "(Fully Explained)" follow-ups within days of the news video; near-duplicate title reuse off-topic.
- Ending on speculation monologues; tacking unrelated news onto a titled feature video.
- Meta/defensive hooks ("there's a lot of noise on YouTube…", "a year ago I was the first to…") — bury the payoff every time.
- Config/setup walkthroughs played in real time — compress or B-roll them.

**Try (open experiments):**
- Boris-levels video (V37): content is fine (AVD green), lane is capped — accept it, but the level-by-level demo style transfers to feature videos.
- Pair the prompting-guide's title discipline (authority + number + benefit) with 60-tips chapter density for the next big guide.
- Move effort-hours/numbers to thumbnails (archive PATTERN), title carries stakes; thumbnail names the thing.

## Gap-fill addendum (remaining nine 2026 videos)

The second pass confirmed the core findings and sharpened four of them:

1. **Non-Anthropic cap: hard confirmation.** "The New Codex Update That Manages All Your Agents" (May 31) had arguably the best conceptual hook and densest teaching payload of its batch — and still landed under 3.9K (below the channel's top-60 cutoff), ~1/5 of same-week Anthropic-titled videos. The cap is a title-brand effect, not an execution effect.
2. **The subagent title-rerun gap is pure novelty decay.** The April original (24.7K) both clicked (superlative problem-solved promise) and retained above-typical (relPerf 0.66–0.72 flat plateau); its only bad retention event was the mid-roll lifetime-plan pitch. The June near-duplicate's 7.5K is a freshness/impressions story, not weaker content.
3. **Benefit-equivalence titles are retention-verified, not just CTR-verified.** "Makes Sonnet Feel Like Opus" posts the dataset-high 38.7% avg-view with the healthiest curve shape (0.70 still watching at 30s, shallow intro shed) — the title sets a crisp testable expectation the content immediately delivers. Contrast the literal-descriptive "just shipped the monitor tool" (fine retention, capped clicks). Formula > description.
4. **Roundups have a severity dial, not a death sentence.** The 17-feature/16.8-min video shed a third of viewers in 40s (opened on a newsletter plug before naming any feature) and flatlined at relPerf ~0.10 from 41% on. The January roundup front-loaded ONE well-explained feature before fanning out and held 0.6+ for two minutes, finishing at 32% avg-view. If a roundup is unavoidable: lead with the single best feature, keep the count and runtime down.
5. **Thesis nuance:** "Where Coding Is Heading" out-viewed its single-feature neighbors (19.4K) — a curiosity title CAN buy thesis clicks — but relPerf never cleared ~0.52 and collapsed through the setup weeds into a speculative tail. Thesis pieces fail on *payoff*, not always on clicks; the title writes a check the musing can't cash.
6. **Theory doesn't cliff when it's a walkthrough.** The Internal Skills Strategy breakdown (18.7 min) had the smoothest cliff-free decay of its batch — concrete examples in a continuous walkthrough decay slowly; its low 25.9% avg-view is a length artifact. The real first-order lever across all nine: **what happens in the first 40 seconds** — the two worst early sheds both opened on a plug or a "just woke up" beat instead of the payoff.

## Revenue attribution (Stripe, 72h post-publish windows)

Method: every succeeded Stripe payment/new customer within 72h of a video's publish attributed to that video (Ray's rule). Period 2025-12-30 → 2026-07-18, all USD. Renewals (subscription_cycle) excluded. Overlapping windows (6 clustered publish groups) counted per-window but corrected in totals. **Attribution is temporal correlation, not causation** — email blasts and promo windows co-occur with publishes; the heavy coupon spread (573 distinct amounts; list-price $397 paid only 13x, modal payment $226.85) makes *payment count* a cleaner signal than dollars.

**Topline:** video-adjacent days run **~3.0x the payments and ~2.5x the revenue** of baseline days ($1,856/day vs $739/day). Overlap-corrected 2026 attribution: **$175K across 1,139 signups**. Period grand total ~$274K, refunds $12.5K.

**The key finding: reach and revenue are different leaderboards.** New customers per 1K views (views = Oct 2025 → Jul 2026):

| Video | Views | New custs | Custs/1K views |
|---|---|---|---|
| Even Anthropic Engineers Use This Workflow (Apr 15) | 11.4K | 65 | ~5.7 |
| Biggest Update in Months (Jan 8) | 25.0K | 157 | ~6.3 (Jan promo caveat) |
| Top 0.01% User's Guide (Mar 2) | 22.2K | 82–87 | ~3.9 |
| Biggest Subagent Upgrade original (Apr 23) | 24.7K | 75–79 | ~3.2 |
| My Claude Code Workflow for 2026 (Jan 2) | 27.1K | 89 | ~3.3 |
| I Spent a Day With Anthropic Engineers (Jul 5) | 4.3K | ~16 | ~4 (overlap) |
| — | — | — | — |
| Auto-memory / "Nobody Knew They Needed" (Mar 24) | 100.5K | 35 | ~0.35 |
| Dynamic Workflows news (May 22) | 45.7K | 5–6 | ~0.13 |
| Codex Going Viral (May 4) | 28.4K | 8 | ~0.28 |
| Fable 5 Is Back Tomorrow (Jun 25) | 22.5K | 4 | ~0.18 |
| Claude Code + Anki (Jun 20) | 10.6K | 4 | ~0.38 |

- **Guide/workflow/insider-tactic videos convert 10–40x harder per viewer than broad-reach news.** The two "view flops" with elite retention — "Even Anthropic Engineers" and "Day With Anthropic Engineers" — are top-3 and top-10 *revenue* videos. The small audience that clicks tactic/insider content is the buying audience.
- **The biggest reach winners are the worst converters.** The 100K auto-memory video produced 35 customers; the 46K Dynamic Workflows video produced ~6. Broad-curiosity news pulls viewers outside the buyer profile. (Within-month comparisons hold the pattern, so it's not purely the Jan–Apr vs May+ revenue trend: Apr guide 65 custs vs Apr 6 Ultra Plan news 9–12; May 22 news 6 vs May 29 deep-dive 18–19.)
- **Zero/near-zero windows:** Jul 14 New-Kind-of-Subagent ($0, truncated window), Fable-5 reminder ($705), Anki tie-in ($1.7K — study audience doesn't buy the coding course, consistent with keeping that niche as a separate search asset, not a funnel).
- **Strategic read:** the channel is a two-engine machine — news winners are top-of-funnel (reach, subs), guide/workflow/insider videos are the conversion engine. Don't judge guide videos on views, and don't expect news spikes to monetize. The A/B ceiling lanes rank formats by *views*; the revenue lens partially inverts that ranking.

## Notes

- Data gaps: retention unavailable for XLA-sTSJ-Wc (too new), XVEodnI0aHA, YSbB5gc_1K8, AS4mYVnFM5g, JTW_sEXLH_o, 4oqJ9wgy87k, 3aMWv9FIu4o (empty from API; substituted daily analytics/structure/transcript); pOsGxVKYd3s returned only the first 21% of its curve.
- ⚠️ Two fetched transcripts contained embedded prompt-injection strings aimed at AI analysis tools (OnQ4BGN8B-s via one source, ASAaKhK1B5w via Supadata). Agents ignored them; be aware when running transcript pipelines.
- A/B archive source of truth: `.claude/skills/youtube-ab-tester/references/results/` (`_master-summary.md`, `_anti-patterns.md`, V37 record `2026-07/2026-07-18-boris-levels.md`).
