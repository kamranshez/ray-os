---
tags: [linkedin, competitor-analysis, content-system]
aliases: [Linas Beliunas source system]
date: 2026-07-18
---

Reverse-engineering of Linas Beliunas's LinkedIn content machine (fintech/AI creator, funnels to linas.substack.com), from a 30-post live-feed capture on 2026-07-18 (full dump: [[2026-07-linas-beliunas-feed]]). Historical reference only. Ray's posts use the Stanislav skeleton exclusively ([[2026-07-stanislav-beliaev-source-system]]). This note does NOT feed the source scout ([[source-scout]]); Templates A and B below are Linas's, not Ray's, and must never be used to draft.

## The system in one line

Post 1-2x/day by pouring launches, earnings, funding news, conference talks, and memes into three fixed templates, each ending in a rotating Claude-themed lead magnet that funnels to his Substack.

## Cadence and engagement

- 30 posts in ~3 weeks, ~1-2/day, all originals (no reposts observed).
- Engagement 34 to 16,043 reactions (median ~600-1,500), up to 1,261 reposts. Posts 3-4x as often as Stanislav with ~5x his peak.

## Templates

**Template A -- news/launch breakdown (dominant):**
1. One-word punch hook + colon + emoji ("Wild:", "Huge:", "Epic:" ... 😳)
2. One-line plain-language expansion
3. Arrow-bullet stat block (→ 88.3 on Terminal-Bench, → $3/M input tokens)
4. "That means..." interpretation paragraph
5. Broad thesis one-liner ("Open source AI is eating closed AI.")
6. Occasional caveats paragraph for credibility
7. P.S. with a rotating lead magnet via lnkd.in
8. 150-450 words

**Template B -- weekly newsletter recap:** opens with a FAKE celebrity endorsement ("...the Apple of AI &amp; FinTech" - Tim Cook*), asterisk-disclaimed at the bottom ("*Cook probably never said this"), bullets the week's 2-3 stories with parenthetical why-it-matters teasers, closes "in the latest Weekly AI &amp; Tech Digest 👇".

**Template C -- meme/one-liner:** screenshot or graphic + 2-4 lines of commentary + P.S.

## Data sources, ranked (30 posts)

1. **AI model/product launches** (Kimi K3, X Money, Claude Science, Fable 5 restore...) -- his biggest well.
2. **Conference talks and YouTube lectures repackaged** (Andrew Ng at LangChain, Stanford lectures, Code w Claude talks) -- the "watch this instead of Netflix" device.
3. **Authority quote hooks** (Karpathy, Luca Maestri, Boris Cherny).
4. **Industry reports and earnings** (Worldpay Global Payments Report, Micron earnings) -- fintech-specific, chart-driven.
5. **Funding/M&amp;A announcements** (Oxylabs $130M, Nuvei-Payoneer, Revolut).
6. **News events** (Apple v OpenAI lawsuit).
7. **Memes/screenshots** + his own newsletter recaps.

## What differs from Stanislav

1. Topic: fintech/markets/macro + AI vs Stanislav's dev-tools/repos. Overlap only on model launches.
2. **Image dependence:** many Linas posts carry a SECOND full essay as image-overlay text (a chart or graphic with ~200 words baked in). Text-only scraping loses this unless alt text survives. Stanislav's images are mere product screenshots.
3. The fake-celebrity-endorsement gimmick (always asterisk-disclaimed) is uniquely his.
4. CTA: rotates a different lead magnet per post (all → Substack) vs Stanislav's single fixed P.S.
5. Adds his own thesis line to every story; Stanislav mostly curates + light reframe + "Your thoughts?".

## What Ray steals

- The **thesis one-liner** slot -- a quotable opinion line turns a news summary into a take.
- The **conference-talk/lecture repackaging** lane (maps perfectly to agentic-coding talks).
- The **authority-quote hook** (Karpathy/Boris Cherny-style quotes are native to Ray's niche).
- Rotating lead magnets > one static CTA (Ray equivalents: specific ACS videos/classes rather than the homepage).
- Skip: the fake-endorsement gimmick (off-brand for Ray), fintech earnings lane.
