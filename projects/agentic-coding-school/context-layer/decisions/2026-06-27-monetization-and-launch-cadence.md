# Monetization model and launch cadence

**Status:** Final. This is the direction going forward (decided with Ray, 2026-06-27; launch model confirmed by Ray same day).
**Basis:** a full Stripe year-to-date data pull plus an independent second-opinion review, same day.
**Touches:** `pricing.md`, `positioning/brief.md`, `positioning/open-decisions.md`, `voice.md`, `positioning/copy-bank.md`. This decision **reverses** the earlier "future classes are separate products" policy (2026-05-08) and **closes** the open "price-raise timing" item.

---

## The decision

1. **Keep the course one-time / all-access. No monthly course membership, no subscription-led model.** The lifetime all-access pass stays the anchor product.
2. **All-access is ONE growing pass: buy once, get every class, including future ones, kept current forever.** New classes are folded into the pass, not sold as separate products. (This reverses the 2026-05-08 "separate products" policy. See reconciliation below.)
3. **Every brand-new class launch ratchets the all-access price up, with a ~2-week launch sale at the old price.** The new class is the occasion and the deadline. The sale runs roughly two weeks at about 30% off the about-to-rise price.
4. **Frame it as a price step-up, not a standing discount.** The message is "the price goes up when this two-week sale ends, now that [new class] is in the pass," so buying now locks today's lower price forever. Urgency is a real, dated raise, not an always-on "% off."
5. **Recurring revenue ambition lives on the SaaS side, not the course.** Put that energy into one SaaS product, not a course membership.

## Why (the data behind it)

- **One-time is 96% of revenue.** YTD 2026: $259k of $270k is one-time. Subscriptions are 4% (~$15.6k ARR, about 3% of the business).
- **Monthly course subscriptions churn structurally.** Median subscriber lifetime was 1.0 month; 25 to 30% retained by month 3. The cancellation feedback that exists was "unused" and "too complex," and only 1 of 12 said "too expensive." A course is consumed, so a monthly charge has nothing to keep justifying. This is physics, not a tunable pricing bug.
- **Annual is not a true retention engine.** The $247/yr tier retained 84% at month 1, but annual "cancellations" mostly mean the buyer turned off auto-renew right after purchase and kept the year they paid for. Annual behaves like a cheaper one-year lifetime, not a stay-forever product.
- **Revenue is launch-driven.** Each new video or feature drives the spike (the top video earned about $24.8k in its first three days). A per-launch sale tied to a real new-class deadline matches how the money actually arrives, which is in concentrated bursts, not a smooth monthly stream.
- **Per-customer:** average $161, median $152, max $1,875 (a team purchase).

## How we got here (the discussion)

The starting worry was Ray's, in his words: "every single month I'm basically chasing for more revenue." The instinct was to build recurring revenue by **removing the lifetime plan and going monthly-only**, on the theory that an always-on subscription would smooth the income out.

We pulled the Stripe year and that theory did not survive it:
- Monthly is the **worst-retaining, lowest-LTV** tier (median subscriber lasted 1.0 month, 25 to 30% left by month 3). Going monthly-only would have bet a ~$250k engine on a churny ~$15k experiment.
- The cancellation feedback was **"unused" and "too complex," only 1 of 12 said "too expensive."** So the churn is structural: a course is consumed, and a monthly charge on a finished course has nothing left to justify. Lowering or restructuring the price would not fix a value-decay problem.
- Annual looked like retention but was really a **cheaper one-year lifetime** (buyers turned off auto-renew immediately and kept the year). Not a stay-forever engine.

So the honest read is that the course income is **launch-driven and lumpy by nature**, and that is fine. Ray then proposed the shape we landed on: keep lifetime, and make the lumpiness *deliberate and repeatable* by running a real sale at every new-class launch. Confirmed as: one growing all-access pass, future classes included, price ratcheting up per launch.

## My recommendations (Claude's read, and an independent second opinion agreed)

A fresh subagent was given the same data cold and reached the same conclusion, plus surfaced the first two points below. These are recommendations, not part of the locked decision, but they are where the leverage is:

1. **The launch ladder IS your "recurring" answer.** It will not feel like chasing if the new-class cadence is predictable. A steady drumbeat of launches, each with a dated price step-up, turns the lumpiness into a schedule you control rather than a monthly scramble. Treat "ship the next class" as the revenue ritual.
2. **B2B / team is the most under-exploited lane and the strongest next bet.** The largest payments all year were team buys ($1,800, $1,663, $1,067, $880). A Team Stripe product already exists, the acquisition cost is the same videos, and it does not deplete the consumer audience the way another lifetime sale does. This is higher willingness-to-pay sitting almost untouched.
3. **Put the real recurring bet on ONE SaaS, not three, and not a course membership.** Recurring revenue belongs where value is recurring (daily-use software), not on a finished course. ~$1,299 MRR after a year is not yet an engine; spreading attention across several SaaS plus a newsletter dilutes the content bandwidth that drives 96% of revenue. Pick one and watch its cohort retention / LTV the same way we just watched the course.
4. **Keep the content cadence deliberate.** YouTube is the shared top-of-funnel for the course AND the SaaS. "Make videos whenever" quietly starves SaaS acquisition. The videos are the demand engine for the whole portfolio, so protect that cadence.
5. **Guard the sale's honesty.** The price step-up only works long-term if the raise is real and dated every time. No standing "% off," no fake countdowns. The trust that the calm, honest positioning is built on is the same trust the launch urgency leans on; do not spend it.
6. **One consequence to keep in view:** now that future classes are included for existing buyers, you cannot re-sell new classes back to your base. That is the intended loyalty payoff, but it means growth has to come from **new buyers** (the ladder) and **teams** (B2B), not from re-monetizing the existing list. Keep the funnel healthy accordingly.

## Alternatives considered and rejected

- **Monthly-only (drop lifetime):** rejected. It is the worst-retaining, lowest-LTV tier; it would roughly halve revenue per customer and bet a ~$250k engine on a churny ~$15k experiment. The churn driver is value/usage, not price, so removing lifetime would not fix it.
- **Annual as the recurring engine:** parked. Fine as a cheaper entry rung if ever wanted, but not a retention play (small sample, immediate auto-renew-off pattern).
- **A community / cohort layer to make course-recurring work:** parked. It is the one thing that could sustain course-recurring, because accountability attacks the "unused" churn directly, but it is high ongoing effort, which cuts against the lower-hassle goal. Revisit only if course-recurring is wanted badly enough to staff it.

## Opportunities surfaced (not in this decision, worth revisiting)

- **B2B / team is the highest-willingness-to-pay segment and is under-exploited.** The biggest payments overall were team buys ($1,800, $1,663, $1,067, $880). A Team Stripe product already exists. This lane has budget, low acquisition cost (same videos), and does not deplete the consumer audience the way another lifetime sale does. Strongest candidate for the next revenue lane.
- **Concentrate recurring on one SaaS, not three.** About $1,299 MRR after a year is not yet an engine. Spreading across multiple SaaS products plus the newsletter dilutes the content bandwidth that drives 96% of revenue.

## Exact mechanics (the specifics)

**The product.** One all-access pass, three ways to buy it: monthly, yearly, lifetime. Every tier grants the entire catalog. Lifetime is the anchor and the hero.

**What "all-access" includes.** Every class that exists today AND every class shipped later. A lifetime buyer from today gets next quarter's brand-new class at no extra charge. This is the "buy once, get everything, including what's coming" promise. It is now true, so landing copy may say it plainly.

**The price ladder.** The lifetime anchor is ~$397 today and climbs over time, one step per brand-new-class launch. Each launch is a new, higher rung. Earlier buyers keep the price they locked; the raise applies to new buyers from the sale's end onward. The earlier "~$397 now to ~$500 once Loopy AI ships" is no longer a single milestone, it is just the first couple of rungs on this ladder.

**The launch sale (the recurring engine).**
- **Trigger:** a brand-new class going live. Not a calendar date, the class is the event.
- **Window:** roughly two weeks.
- **Depth:** about 30% off, i.e. the about-to-rise price held at the old (lower) anchor for the window.
- **Message:** "The new [class] is in. The all-access price goes up when this two-week sale ends. Buy now and lock today's price forever." Real, dated raise. No always-on discount, no fake countdowns.
- **Who it targets:** new buyers. Existing all-access holders already get the new class free (that is the loyalty payoff), so the sale is an acquisition push, not a re-sell to the base.

**What stays put.**
- Refund terms unchanged: monthly no refund; yearly and lifetime keep the 14-day money-back guarantee.
- Team / B2B lane unchanged: 5+ seats, invoice billing, "talk to us." Highest-WTP segment, still the strongest next revenue lane.
- Always-current still holds and is now strictly bigger: the classes you own keep getting updated AND you get new classes too. The old honesty carve-out ("not new classes free") is retired because new classes ARE now included.

**One open sub-item:** the exact dollar size of each ladder step is set per launch (round-number targets, e.g. toward $447, then $497, then beyond), not fixed here. The mechanic is fixed; the step amount is a per-launch call.

## Reconciliation (resolved 2026-06-27)

The earlier policy (`pricing.md`, brief, voice, copy-bank) said **future classes are separate products, not bundled into lifetime**, and that copy must not imply "buy once, get every future class." Ray chose the opposite: **one growing all-access pass that includes future classes, with the price ratcheting up at each launch.** That reversal is now propagated to `pricing.md`, `positioning/brief.md`, `voice.md`, `positioning/open-decisions.md`, and the scope notes in `positioning/copy-bank.md`. The price-raise-timing open item is closed: the trigger is each new-class launch, after its two-week sale.

## Provenance

- Stripe REST pull (checkout sessions, paid invoices, subscriptions), YTD 2026, on 2026-06-27.
- Full analysis memo: `.claude/skills/youtube-video-revenue/reports/2026-06/2026-06-27-recurring-vs-onetime-model.md`.
- Per-video revenue (3-day time-proximity) is stored in each script's frontmatter under `revenue` / `revenue-lift` / `revenue-utm` / `revenue-sessions`.
- An independent second-opinion review was run the same day; it surfaced the B2B and single-SaaS points and confirmed the one-time direction.
