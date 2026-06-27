# 02 — Paying-Customer Profile (PlanetScale DB)

**Source:** PlanetScale Postgres `agentic-coding-school`, branch `main`. Pulled 2026-06-26. Read-only.

## How "paying customer" was defined
Paid status lives in **`user_subscriptions`** (one entitlement row per paying user; free users get **no row** — 4,275 total users, only 2,157 have a subscription row). Definition: distinct `user_id` with a **non-revoked** row (`revoked_at IS NULL`), excluding `purchase_source = 'manual_grant'` comps (2 users).

Schema facts that shaped this:
- `tier` is almost always `'pro'` (product name) → does NOT encode billing cadence. Cadence derived from `forever_pass` (=Lifetime), `expires_at − granted_at` (term), `stripe_subscription_id` (active recurring).
- "NULL/NULL sentinel" (`forever_pass=true`, no stripe, no expires) = Lifetime grant (largest bucket).
- `amount_paid_cents`, `stripe_price_id`, `purchase_source` NULL for most rows = **un-backfilled metadata, not $0 sales** (NULLs span the whole Dec 2025→Jun 2026 lifetime; columns are newer than most purchases).

## Totals: 2,155 distinct paying customers
| Tier (derived) | Customers | % |
|---|---|---|
| Lifetime (`forever_pass`) | 1,645 | 76.3% |
| Yearly (~12-mo term) | 281 | 13.0% |
| One-time, no-expiry (~$250 all-access) | 131 | 6.1% |
| Team / org seat (corporate bulk, ~90-day) | 63 | 2.9% |
| Other fixed-term (122–180 day) | 25 | 1.2% |
| Monthly (≤47-day / recurring) | 10 | 0.5% |

**Overwhelmingly a one-time/lifetime base** — Lifetime + one-time no-expiry = **1,776 (82%)**. Recurring subscriptions are a small minority; the monthly tier (added Apr 8) has barely sold.

## Email-domain profile (all 2,155)
| Bucket | Customers | % | Distinct domains |
|---|---|---|---|
| Corporate / custom domain | 624 | 29.0% | 501 |
| Freemail / personal / alias | 1,457 | 67.6% | 35 |
| Internal test (`rayamjad.com`) | 74 | 3.4% | 1 |

Excluding 74 internal test accounts (plus-addressed bots, e.g. `r+1@`, `r+2252@rayamjad.com`): of **2,081 real customers, ~30% corporate / ~70% freemail.**

**Top domains:** gmail.com 1,228 · mcg.com 60 (corporate bulk — MCG Health) · hotmail 41 · icloud 33 · yahoo 28 · outlook 22 · **n26.com 19** (fintech) · georgebrown.ca 14 (edu) · protonmail 13 · **pengine.com 12** · me.com 12 · proton.me/pm.me 16 · **commercetools.com 7** · subtel.de 5 · redmonks.in 5 · copilotsearch.com 4 · heyjane.co 3 · gmx/web.de 11.

The corporate 624 spreads across **501 distinct domains** (mostly 1–2 buyers each — individual pros on work email), with a few genuine bulk/team buyers concentrating counts (mcg.com 60, n26 19, pengine 12, commercetools 7).

## Caveats
- **Cadence is inferred**, not stored (`tier` uniformly 'pro'). Treat Lifetime + one-time together (~82%) as the safe figure.
- ~90% of rows have NULL amount/price/source (newer columns, un-backfilled). Entitlement = paid; not revenue-verified per row vs Stripe.
- Corporate-vs-freemail is a **proxy** — many skilled engineers use personal Gmail. 30% corporate is a **floor** on "professionals at companies"; the 501 distinct corporate domains (N26, AUTO1, commercetools, Trusted Shops, MCG, NYU) confirm a substantial professional/enterprise base.
- **mcg.com skew:** ~60 of 624 corporate are one enterprise team rollout; recent-customer view over-represents this single account.
- 74 `rayamjad.com` = internal test bots, excluded from real-customer %s.
