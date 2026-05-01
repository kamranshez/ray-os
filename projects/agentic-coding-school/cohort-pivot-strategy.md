---
tags: [strategy, pricing, cohort, agentic-coding-school]
date: 2026-05-01
status: draft
---

## TL;DR

Close the sub to new members. Pivot to uncapped cohort-based enrollment, 6 cohorts/year (every 8 weeks), $399 first-week launch price discounted from $699. Each cohort gets: full backlog + curated "what matters most this month" drops + lifetime access to all future cohort drops + 1 live office hour every weekday. Alumni from any past cohort get every future cohort's new content for free.

This pivot is supported by:
- Ray's own April 2026 lifetime-retirement event ($32K in 4 days, ~67% lifetime SKU)
- The badass-dot-dev corpus (Marie Poulin's lifetime-alumni model is the closest precedent)
- External peer pricing (AI cohort peers charge $2,200-$2,500; £1,299 is market-correct longer-term)
- Matt Pocock's proven uncapped + pre-recorded + lifetime-access mechanic at AI Hero (Cohort 01 of DeepSearch >1,000 learners)

## Why this works

**The buyer psychographic data already exists.** April's $32K spike showed buyers want commitment + ownership, not access. They paid $226-$349 for lifetime when £15/mo was right next to it. That same psychographic will pay $399-$1,299 for a cohort with curation and live access.

**Curation-as-product solves a real customer pain.** Subscribers don't know what to watch in a 240-lesson library when Claude Code ships 3 things a week. "Here are the 6 things that matter THIS month, drip-fed live with an instructor" is a fundamentally different value prop from "240 lessons on demand."

**Closing the sub stops Ray competing with himself.** £15/mo is a bad price anchor for premium positioning. Cohort-only forces every new buyer up-ladder.

**Upfront cash > deferred sub revenue** when:
- Capital reinvestment matters (production, ads, future hires)
- Typical course sub LTV (~£107 at ~7-month avg lifetime) is under cohort price (£399+)
- "Always on" support obligation is taxing without scaling revenue

## The offer (Cohort 01)

**Master Claude Code: Cohort 01**

- **$399 founding price** (first week of enrollment)
- **$699 standard price** (after first week, before doors close)
- **2-week cohort, uncapped enrollment**
- Pre-recorded daily videos drop during the 2 weeks (curated "what matters most this month")
- 1 live office hour every weekday (10 sessions / cohort)
- Lifetime access to:
  - 240-lesson backlog
  - This cohort's curated drops
  - Every future cohort's new curated drops
  - Alumni Discord
- Subscription closed to new members on the day enrollment opens. Existing subscribers grandfathered indefinitely.

## Pricing rationale

| Anchor | Price |
|---|---|
| Matt Pocock — Claude Code for Real Engineers (2-week cohort, weekly drops, 6 office hours total) | $795 |
| IndyDevDan — Tactical Agentic Coding (lifetime self-paced) | $599 |
| Stanford / Mihail Eric — AI Software Development | $2,200 |
| Product Faculty — AI Product Management | $2,500 |
| altMBA | $3,000-$4,500 |
| **Ray — Cohort 01 founding** | **$399** |
| **Ray — Cohort 01 standard** | **$699** |

$399 is intentionally low for first cohort — buys testimonials, social proof, and operational learning. The $699 standard price anchors the ladder for future cohorts. Cohort 02 should bump to $499/$899. Cohort 04+ targets $1,299+ to align with peer market rates.

## Cadence

**6 cohorts per year, every 8 weeks.** 2 weeks intensive + 6 weeks recovery/prep/marketing.

Why not every 4 weeks: corpus says compressed cycle = burnout treadmill. Every 8 weeks gives:
- Real scarcity between enrollment windows
- Time to pre-record next cohort's curated drops before the live window
- Marketing runway for each launch

## Operational structure

**Pre-recorded daily drops** — record the 6-10 curated videos before the cohort starts. During the 2 weeks, drop one per weekday. No daily live recording treadmill.

**Live office hours (1/day, weekdays)** — 10 sessions per cohort. Sustainable solo at <200 students.

**Sub-cohort fallback plan** — if Cohort 01 unexpectedly clears 200 students:
- Activate 3-5 pre-invited alumni coaches (existing engaged subscribers given free lifetime upgrade in exchange)
- Split office hours into multiple sub-cohort rooms
- Don't wait until you're drowning to set this up; have it pre-warmed by enrollment day

**Alumni-attend-future-cohorts** is the retention compound. Marie Poulin's model: never expire anyone. Every cohort makes the alumni community more valuable, every alumni makes future cohorts more valuable.

## What changes in the codebase

Per April's git timeline, Ray already shipped most of the scaffolding:
- Lifetime retirement banner mechanic (`04f66e96`)
- Countdown to deadline (`90cfac00`)
- Lifetime SKU restored on hidden `/lifetime` page (`2a8c02d5`)
- Annual sub Stripe price ID system in place

Net new work for Cohort 01:
- Cohort-specific Stripe SKU at $399 founding price
- Enrollment-window mechanic (open/close on dates, waitlist after close)
- Sub closed to new signups on enrollment open day
- Cohort-specific Discord channel + onboarding
- Curation page for that cohort's drops

## Pre-launch checklist

1. **Validate with 10 recent lifetime buyers (last 30 days).** DM or email: "If I ran a 2-week live cohort with daily drops + 1 live session/day + lifetime alumni access, would you join at $399?" Need 5+ yes before building. Their objections become your sales copy.
2. **Define cohort 01's 6-10 curated topics** — what matters MOST this month for Claude Code users? This list IS the product. Get it right.
3. **Pre-invite 3-5 alumni coaches** as fallback scaling.
4. **Pre-record 2 of the 6-10 videos** before opening enrollment to de-risk delivery.
5. **Draft sales page** modeled on Matt's Real Engineers page (high-empathy problem framing → engineering-mindset hook → curriculum → office hours promise → lifetime alumni → price reveal with $399 founding scarcity).
6. **Set enrollment dates.** Open 7 days, $399 first 24-48 hours, $699 thereafter, doors close on day 7. Cohort starts day 14.

## What to measure during Cohort 01

- Total enrollment (founding vs standard split — tells you price sensitivity)
- Office hour attendance rate (tells you whether daily cadence is right)
- NPS / "would you recommend" (gates Cohort 02 marketing)
- Refund rate (warning signal)
- Alumni engagement post-cohort (retention signal — do they come back for Cohort 02 drops?)

## What NOT to do

- **Don't rebrand to "Agent Engineer Pro" yet.** "Master Claude Code" has SEO + intent demand. Keep the wedge, ladder above it later.
- **Don't run two cohorts in parallel for Cohort 01.** Tempting after Marily Nika's playbook, but operational complexity at first run is high. Single cohort, learn, then parallelize from Cohort 03.
- **Don't promise twice-daily office hours initially.** 1/day is sustainable solo. Add 2/day in Cohort 02 if first cohort demands it.
- **Don't kill grandfathered subs.** They're a marketing asset (testimonials, social proof, alumni-coach pool).

## Future evolution

After Cohort 02-03 success:
- Raise prices to peer market rates ($999 founding / $1,299 standard)
- Add concurrent enrollment windows (Marily Nika model)
- Activate alumni-as-coaches formally
- Consider parallel sub-cohorts at scale
- Eventually, the brand could ladder up to "Agentic Engineer" as an umbrella with Master Claude Code as Track 1 — but only after the cohort model is proven solo.

## References

- Ray's April 2026 git timeline: lifetime-retirement event Apr 9-23, 2026 (commits `04f66e96`, `90cfac00`, `2a8c02d5`)
- Stripe data: $32K spike Apr 21-24, 2026; ~67% lifetime SKU (after correcting LASTCALL discount math: $349 × 0.65 = $226.85)
- Badass corpus: Marie Poulin (Notion Mastery — alumni-forever access), Brennan Dunn (live as research engine), Joel Hooks ("undercharging by an order of magnitude")
- External: Matt Pocock (Claude Code for Real Engineers, $795), Marily Nika (AI Product Academy, $1M+ revenue), Wes Kao (Maven, sub-cohort pattern)
