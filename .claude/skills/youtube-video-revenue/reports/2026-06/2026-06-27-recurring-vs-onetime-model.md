---
date: 2026-06-27
topic: business-model — recurring (monthly/annual) vs one-time (lifetime)
source: Stripe REST API live pull on 2026-06-27 (no saved snapshot JSON; figures embedded below)
method: >
  Stripe checkout sessions + paid invoices + subscriptions (YTD 2026), pulled
  directly via REST with an rk_live_ restricted read key. Video revenue uses the
  youtube-video-revenue skill's 3-day time-proximity attribution
  (scripts/time_attribute.py). Subscription retention computed as cohort survival
  (subs old enough to have reached month N that were still active / not yet
  canceled by month N), split by plan interval and price tier.
---

# Recurring vs One-Time Model — Decision Memo (2026-06-27)

## Why this exists
Ray was weighing whether to shift the Agentic Coding School from a one-time/lifetime
course model toward monthly recurring revenue (MRR) — specifically considering
**removing the lifetime plan and going monthly-only** to build recurring revenue and
stop "chasing revenue every month." This memo captures the Stripe data that informed
the decision and the conclusion reached, so the reasoning is on record next time
pricing comes up.

## Data pulled (YTD 2026, as of 2026-06-27)
- **1,730** completed checkout sessions — gross **$269,963**
- **1,793** paid invoices; **134** of them subscription invoices (88 creates + 46 renewal cycles) = **$13,168** recurring gross
- **93** subscriptions all-time (any status)

## Business-model split
| Mode | Sessions | Revenue | Share |
|---|---|---|---|
| One-time (`payment`) | 1,642 | $259,048 | **96%** |
| Subscription | 88 | $10,915 (first payment) | 4% |

Recurring run-rate at pull time: **~$1,299 MRR (~$15.6k ARR)** — roughly **3%** of the business.

By `purchaseType`: lifetime 554 sessions / $122,375 · team 20 / $7,320 · (untagged) 1,148 / $138,993.

## Subscription tiers (main product `prod_Txu9CChG1vUwSd`)
Pricing was experimented with heavily (8 distinct price points; plans toggled on/off
over the year, so raw signup *volumes* per month are unreliable — retention/LTV is the
honest lens).

| Tier | n | Active | Canceled | Median LTV | Retention m1 / m2 / m3 |
|---|---|---|---|---|---|
| $247/yr | 19 | 15 | 4 | $247 | 84% / 67% / — |
| $199/yr | 31 | 17 | 14 | $199 | 55% / 52% / 48% |
| $49/mo | 26 | 11 | 15 | $67 | 81% / 46% / **30%** |
| $76/mo | 10 | 1 | 9 | $82 | 60% / 30% / **10%** |
| misc legacy ($39/$50/mo, old $199/yr) | ~7 | mixed | — | low | — |

## Retention & LTV (monthly vs annual)
- **Monthly plans (n=42):** survive to month 1 **74%** → m2 45% → m3 **25%**. Churned monthlies lasted a **median of 1.0 month**. Avg total paid ~$98, median ~$76.
- **Annual plans (n=51):** median total ~$199. "Cancellations" are misleading — churned annuals had median life **0.2 months**, i.e. they turned off auto-renew right after buying but **keep (and paid for) the full year**. Annual cash is secure even when "canceled."
- **All customers (1,697 with invoices):** avg total paid **$161**, median **$152**, max **$1,875** (multi-seat/team; top individual $1,800). Best recurring customer: **$416** (a loyal $77/mo).

## Cancellation reasons (47 canceled subs)
- 44 voluntary ("cancellation_requested"), 3 involuntary ("payment_failed"); only 5 "cancel at period end."
- Qualitative feedback (only 12 left any): **"unused" and "too complex" lead; only 1 "too expensive."**
- Takeaway: **churn is a value/usage problem, not a price problem.** A course is *consumed* — once watched, a monthly charge has nothing left to justify, so people leave after ~1 month. Structural, not tunable.

## Full-year video revenue (3-day time-proximity, all 32 videos)
Total time-attributed **$179,595** of $267,345 clean revenue; baseline $668/day.
Top earners: forked-subagents $24,772 · "17 Features"/Jan-18 $14,641 · Feature-That-Kills/Mar-07 $14,168 · interactive-artifacts-bun $12,986 · skills-2.0 $12,312 · Biggest-Update-in-Months/Jan-08 $10,936. (Per-video numbers also written into each script's frontmatter under `revenue`, `revenue-lift`, `revenue-utm`, `revenue-sessions`.) Revenue is **launch-driven** — concentrated in each video's first 3 days.

## Decision (2026-06-27)
1. **Keep the course one-time.** Anchor = **$397 lifetime**, with occasional sales on launches. Do **not** go monthly-only — monthly is the worst-retaining, lowest-LTV tier, and the churn is structural (consumed course), not fixable by pricing.
2. **Put recurring revenue where value is recurring: the SaaS products** (HyperWhisper, AgentStack) — daily-use software earns its subscription in a way a finished course never will.
3. **Keep a deliberate content cadence.** YouTube is the shared top-of-funnel for course *and* SaaS; "make videos whenever" risks starving SaaS acquisition. The videos are the demand engine for the whole portfolio.
4. **Lifetime-only is lumpy by design** — revenue will always feel launch-to-launch. The SaaS MRR base is the stabilizer the course spikes ride on top of. The retention discipline used here (cohort survival, LTV by tier) is exactly what to watch on the SaaS, where it actually compounds.

## Caveats
- LTV figures are still maturing (most subs are Feb–Apr cohorts, right-censored), but the median-1-month monthly churn is already unambiguous.
- Plan availability was toggled through the year, so signup-volume trends are not reliable; conclusions rest on retention and LTV.
- UTM attribution undercounts (code shipped 2026-03-13); time-proximity is the retroactive estimate for video revenue.
