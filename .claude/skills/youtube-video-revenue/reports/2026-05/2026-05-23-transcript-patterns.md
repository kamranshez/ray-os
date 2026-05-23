# Transcript pattern analysis — 2026-05-23

**Source snapshot:** `snapshots/2026-05-23.json` (50 videos, $239k YTD revenue, 11.24% UTM coverage, 67.42% time-proximity coverage)

**Method:** 5 forked subagents analyzed all 27 non-zero-revenue 2026 videos through different lenses (hook + title promise, pitch positioning, demo density, content shelf-life, authority signals). Each fork had the full revenue table and all 27 transcripts inherited from the parent conversation. Transcripts fetched via VidTempla (15) and Supadata fallback (12, after VidTempla rate-limited).

**Why this exists:** The revenue snapshot tells you *which* videos converted. This report explains *why* — what Ray was doing differently in HIGH-RPV ($1.20-$0.43 per view) videos vs LOW-RPV (<$0.10) videos. The 5-angle decomposition was used because pattern analysis is genuinely subjective and parallel perspectives surface convergent vs idiosyncratic findings.

---

## The single structural finding

**The masterclass is a demo prop, not a sponsor read.** Every one of the top-3 RPV videos uses the masterclass MCP server or landing page as the *substrate* of a live Claude Code demo:

- ASAaKhK1B5w ($1.20 RPV) — customer-journey HTML artifact pulls real PostHog + Stripe data from the masterclass landing page
- _QGgk9F9CSM ($1.02 RPV) — masterclass MCP server is the use case for forked subagents
- XVEodnI0aHA ($0.46 RPV) — Telegram bot's first demo query is literally "search online for Ray Amjad's Master Claude Code class and tell me why I should buy it"

Pitch and demo aren't separate sections; they're the same section. When the masterclass IS what you're demoing on, scarcity + objection-handling pitches land 3-7x harder than the same lines bolted onto a feature explainer.

---

## Convergent findings across all 5 lenses

| Pattern | Evidence | Mechanism |
|---|---|---|
| **Demo-led × personal-project surface = revenue** | Demo-led avg RPV $0.36 vs educational $0.12 vs speculation $0.18. HyperWhisper / RayOS / masterclass appear in every top-RPV demo. | Viewer has to think "I want to do that on my own work." Talking about features doesn't trigger that. |
| **Never undercut your title** | UNhA17l6CWw "you may be underwhelmed" ($0.08), rj7xi-s4Ssg "I won't really use this" ($0.04). | Critical conclusion negates buy intent. If you reach that conclusion mid-recording, restructure as "use X instead" with a demo. |
| **Reverse-engineering INVERSELY correlates with RPV** | OnQ4BGN8B-s $0.06 (99k views), UNhA17l6CWw $0.08, EhiJX0WvRz4 $0 time, rj7xi-s4Ssg $0.04, c0gVowvMR-g $0.02. Zero in HIGH tier. | Binary spelunking attracts tech-curious tourists, not buyers. Ungated features have no "I need this now" urgency. Authority shifts from practitioner to decompiler. |
| **Sequel videos cannibalize originals** | 4oqJ9wgy87k ($0.07) reran the same Telegram demo as XVEodnI0aHA ($0.46) two weeks later. 7x RPV gap. | If you cover the same feature twice within 2 weeks, the second one craters. |
| **Newsletter-first close concentrates in LOW** | OnQ4BGN8B-s, UNhA17l6CWw, 4oqJ9wgy87k, rj7xi-s4Ssg all lead the close with newsletter, demote masterclass to "you also get free videos." | Soft ask used when the hard ask isn't ready. Newsletter fine as secondary, not as primary close. |
| **News roundups never bomb (0% LOW rate)** | All 4 roundups ($0.26-$0.73) earned mid-or-better. | The biweekly "here's what's new" cadence is reliable RPV insurance. Keep it. |

---

## The 99k-view dud autopsy (OnQ4BGN8B-s)

Every lens flagged this video. The reasons stack:

- **Hook**: title was viral-clickbait ("Feature Nobody Knew They Needed"), open delivered passive observation
- **Demo**: 8 minutes of watching the agent dream; no aspirational "I want to do that"
- **Authority**: reverse-engineering insider angle attracts curiosity not commerce
- **Shelf-life**: ungated feature, peaks on publish, dies fast
- **Pitch**: generic end-link drop, no scarcity, no objection-handler

**Conclusion:** brought the biggest 2026 audience and converted at the lowest rate. 99k views are tourists, not customers. Stop optimizing for that headline shape.

---

## Specific "stop" list

1. Stop reverse-engineering binaries on camera as the main angle. Costing more than it earns. (5 LOW videos do this.)
2. Stop closing with "I won't really use this myself." Restructure to recommend an alternative with a demo.
3. Stop publishing sequels within 2 weeks of the same villain or feature. XVEodnI0aHA → 4oqJ9wgy87k lost ~$6k.
4. Stop leading the close with the newsletter. Demote it to secondary CTA.
5. Stop using "most comprehensive class online" as the load-bearing pitch line. It's wallpaper. Every tier uses it equally, so it's signal-free.
6. Stop the "I was early to this 7 months ago" credit-claim. Reads defensive. Concentrated in MID/LOW, absent from HIGH.

## Specific "do" list

1. Make the masterclass landing page or MCP your demo substrate at least once per month. The 3 highest RPV videos all do this.
2. Open with a thesis, not a description. "X is the most important Y" beats "today we have an update." (JTW_sEXLH_o, _QGgk9F9CSM both do this.)
3. Pair scarcity with a specific date ("removing lifetime April 23rd", not "sale going on"). Top 3 videos all date the pitch.
4. Pre-empt the lifetime objection in one sentence: "in a year there will be a better tool, you get lifetime access to that class too." Verbatim in top 3 RPV videos.
5. Name principles you own ("instruction budget", "leverage hierarchy", "3 layers of artifacts"). LOW-tier videos leave the viewer with feature names Anthropic owns.
6. Front one proprietary number per video ("I analyzed 1000 CLAUDE.md files", "<0.2% refund rate"). Specific beats superlative.
7. One personal-failure beat per video. "I had a 650-line CLAUDE.md and it was making things worse." Every HIGH video has this; LOW videos don't.

---

## Content-mix rebalance

| Type | Current ~ | Target |
|---|--:|--:|
| Demo-led with personal-project surface | 56% | **70%** |
| Leverage-framed evergreen (JTW template) | 4% | **15%** |
| News roundup (demo per feature) | 7% | **10%** |
| Reverse-engineering / speculation | ~15% | **5%** |
| Critical reviews ("I won't use this") | ~7% | **0%** (move to newsletter) |

---

## Undervalued videos worth repurposing

The 3-day attribution window caps long-tail revenue. Two videos almost certainly earn 2-3x what the snapshot shows over 12 months:

- **JTW_sEXLH_o** (CLAUDE.md leverage, $0.43 RPV) — every new Claude Code user hits this eventually
- **AzmnaoVP8sk** (Top 0.01% / 60 tips, $0.21 RPV) — anniversary compendium new subscribers binge

Consider chopping each into 5-10 short-form clips for shorts / LinkedIn / X. Already-proven principles, just need more surface area.

---

## Open question for next analysis

The masterclass MCP server appears to be a structural conversion asset (mentioned by both pitch and demo forks independently). Worth investigating whether MCP-install events correlate with subsequent conversion in Stripe data. Could be the highest-leverage product feature on the masterclass.

---

## Provenance

- Fork agent IDs: a4dbf9d85e7621679 (hook), a881a1f5b82a2fb35 (pitch), a9c79712dc826bd25 (demo), a1b103e6a882a04a5 (shelf-life), af43006399073f714 (authority)
- Parent session: `/Users/ray/.claude/projects/-Users-ray-Desktop-agentic-coding-school/a82e966c-3385-496c-b4c0-aef788abf569.jsonl`
- All 27 transcripts referenced are in the parent conversation; not re-stored here to avoid duplication. Re-fetch via `mcp__claude_ai_VidTempla__get_video_transcript` or `mcp__claude_ai_Supadata__supadata_transcript` if needed.
