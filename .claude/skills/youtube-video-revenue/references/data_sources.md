# Data sources, schemas, and gotchas

## 1. VidTempla (YouTube views + canonical video list)

**Why this source:** It's the only one that returns YouTube's own view counts. PostHog only sees clicks on your domains; YouTube view counts come from Google.

**Tool calls:**

- `list_channels` — returns Ray's channel UUID. Channel ID for "Ray Amjad" is `UCLA7cJBnqr0nLF2bQBD9uUg`.
- `list_videos(channelId, sort: publishedAt:desc, limit: 100)` — returns video metadata. **Watch out:** if more than ~50 videos are returned, the response can exceed token limits and you'll get a "result exceeds maximum allowed tokens" error pointing you at a temp file. Spawn a subagent to read it in chunks.
- `query_analytics(channelId, startDate, endDate, dimensions: video, metrics: views,..., filters: video==id1,id2,...)` — returns per-video metrics. **24-48h lag:** videos published today won't appear; fall back to Ray's stated count.

**Output normalization:** Map to `{videoId, title, publishedAt, youtube_views}` per video.

## 2. PostHog (top-of-funnel attribution)

**Why this source:** Tracks visitors arriving on the site with a `utm_campaign`, plus persistent `$initial_utm_campaign` on the person.

**Project:** `Agentic Coding School` (id 236619). Not the default HyperWhisper project.

**Critical:** Use `math: weekly_active` for unique visitors over a multi-day window, not `math: dau` summed (DAU double-counts returning visitors).

**Three breakdown queries:**

1. **Visitors per video** (event-level):
   ```
   series: [{event: $pageview, math: weekly_active,
             properties: [{key: utm_campaign, operator: exact, type: event, value: [<video_ids>]}]}]
   breakdownFilter: {breakdowns: [{property: utm_campaign, type: event}], breakdown_limit: 50}
   ```
2. **Workshop checkouts per video** (person-level for persistence):
   ```
   event: workshop_checkout_started, math: total
   property filter: $initial_utm_campaign on person
   breakdown: $initial_utm_campaign on person
   ```
3. **PostHog purchases per video** (person-level): same shape with `purchase_complete`. **Will undercount vs Stripe** because `purchase_complete` is server-side-captured and Vercel terminates serverless functions before the event flushes unless `captureImmediate` is used. Keep it as a sanity column — don't treat it as truth.

**Common failure modes:**
- Properties on event vs person mix up: `utm_campaign` is on the EVENT (set when pageview fires); `$initial_utm_campaign` is on the PERSON (set once at first identification).
- 502 from PostHog API on heavy queries — retry once before giving up.

## 3. Stripe REST API (revenue ground truth)

**Why this source:** Only place that has every paid session with its checkout metadata. The Stripe MCP can't search checkout_sessions; we must hit `/v1/checkout/sessions` directly.

**Auth:** Restricted key `rk_live_...` in env as `STRIPE_RESTRICTED_KEY`. Never log or commit it.

**Endpoint:**
```
GET https://api.stripe.com/v1/checkout/sessions
  ?limit=100
  &status=complete
  &created[gte]=<unix>
  [&starting_after=<last_id>]
```

**Pagination:** `has_more=true` → take last `id`, pass as `starting_after`. Sleep 100ms between pages to be polite. ~16 pages for YTD 2026 (~1,600 sessions).

**Key fields per session:**
- `id`, `created`, `amount_total` (cents), `currency`, `mode` (payment | subscription)
- `customer_details.email` (or `customer_email` if set on session creation)
- `metadata.*` — Stripe-side attribution. Most useful keys ranked by frequency on this site:
  | key | what it's for |
  |---|---|
  | `classSlug` | Which course (e.g. claude-code-masterclass) |
  | `purchaseType` | `lifetime`, `yearly`, `monthly`, `workshop`, `team_add_seats` |
  | `posthog_distinct_id` | **The key cross-walk to PostHog persons.** 23% coverage vs utm_campaign's 7.6%. |
  | `promo_code` | Coupon code |
  | `ppp_country` / `ppp_percent` | Purchasing power parity discount |
  | `utm_source` / `utm_campaign` / `utm_medium` | UTM forwarded from landing page (only ~10% coverage) |
  | `signupSource` | e.g. `checkout_gate` |
  | `upgrade_from` | If this is a tier upgrade |

## Known issues

### The Y-prefix bug (`SbB5gc_1K8` → `YSbB5gc_1K8`)

Two Stripe sessions ($534 total YTD as of 2026-05-23) carry `utm_campaign=SbB5gc_1K8` — a 10-char string. Real YouTube video IDs are always 11 chars. The leading `Y` was stripped somewhere in URL or template generation. The `aliases.json` file maps this to the real ID until the source bug is fixed in code.

**To find new aliases:** after each snapshot, look at the `anomalies` array for `unknown_utm_campaign` entries that look ALMOST like a known video ID (one char shorter, one char different, etc).

### Workshop sales attribution gap

The workshop product (`prod_UWxc36YNXREZcA`) lives in the Agentic Coding School Stripe account, but the workshop checkout flow on `agentengineer.pro` doesn't forward `utm_campaign` into Stripe metadata. So workshop sales appear in the $214k "unattributed" bucket, even when they came from a YouTube video.

**Workaround:** Filter Stripe sessions on `metadata.purchaseType=workshop` for a workshop-revenue total, then accept that per-video workshop attribution is missing until the checkout-creation code is fixed to set `metadata.utm_campaign`.

### PostHog `purchase_complete` undercounts vs Stripe

PostHog reports ~1,269 `purchase_complete` events YTD; Stripe shows 1,609 completed Checkout Sessions. The 340-event gap (~21%) is mostly Vercel terminating serverless functions before PostHog flushes — fixed per-call by `captureImmediate` but not retroactively. **Always trust Stripe for revenue counts.**

### YouTube Analytics lag

Videos published in the last 24-48 hours often show 0 views in `query_analytics` because YouTube hasn't ingested the data yet. The skill should fall back to user-stated counts and add a "(estimated)" marker.

## Attribution hierarchy (when sources disagree)

1. **Stripe `metadata.utm_campaign`** — truth, set at checkout creation time, persists through redirects. **But only for sessions created after 2026-03-13** (commit `2a08f84f`).
2. **Time-proximity (3-day window)** — best retroactive estimate, especially for pre-Mar-13 sessions. See section below.
3. **PostHog person-level `$initial_utm_campaign`** — also subject to the Mar-13 ceiling for capture, and misses people whose initial visit had no UTM.
4. **PostHog event-level `utm_campaign` on `purchase_complete`** — worst; only ~10% coverage because UTMs drop on the Stripe redirect.

If Stripe sessions exceed PostHog purchase_complete count for a video, trust Stripe. If PostHog person-level shows attribution where Stripe metadata is empty, it's often a returning customer whose first visit was tagged but who checked out later — note it as "person-level only" in the anomalies.

## Time-proximity attribution method (the second source)

Implemented in `scripts/time_attribute.py`. Run with `--window-days 3` (default).

**Algorithm:**
1. Drop noise sessions: `metadata.purchaseType == "team_add_seats"` and any session with `metadata.upgrade_from` set (these are internal upgrades and seat-adds, not video-driven).
2. For each clean session, find the set of videos whose `[publishedAt, publishedAt + 3d]` interval contains `created`. If multiple match, attribute to the most recently published (newest videos absorb attribution from earlier ones in their 3-day shadow). Count the overlap-loser sessions as `competing_video_overlap_sessions` for the winner.
3. Sessions outside every video window go to the "baseline" pool. Compute baseline daily revenue and take the median.
4. Per-video **lift** = `max(0, time_attributed_revenue − baseline_median × window_days)`. This is the revenue beyond what the day would have produced organically.

**Typical 2026 YTD outputs (with ~50 videos in scope):**
- Baseline median ≈ $617/day
- Time-attributed total ≈ $154k (≈ 65% of YTD)
- Lift-adjusted total ≈ $115k (≈ 48% of YTD)
- vs UTM attribution ≈ $26k (≈ 11% of YTD)

**Limitations to keep in mind:**
- **Long-tail miss:** the 3-day window throws away revenue from people who watch on day 5+, capping coverage at ~48% even when lift-adjusted. A 7-day window would catch more but multiplies overlap problems.
- **Newer-wins bias in publishing clusters:** when Ray ships two videos within 3 days, the newer one absorbs nearly all of the overlap revenue. In 2026 the early-March cluster (Mar 4 → 11 → 19 → 20 → 21 → 24) over-credits the most recent videos. Always note overlap counts in the report.
- **Subscription renewals aren't double-counted:** every Stripe Checkout Session is a *new* subscription; renewals fire `invoice.payment_succeeded` and don't appear in `/v1/checkout/sessions`. Safe.
- **Median is conservative:** the baseline daily mean is typically ~50% higher than the median, so true lift is somewhere between `lift_median` and roughly `lift_median − (mean−median)*window_days`. The skill reports both means and medians so Ray can eyeball the range.

## Historical context: no attribution regression has ever happened

If Ray asks "did attribution regress?" — the answer is no, and it has been investigated. The full investigation is in the conversation history at `/Users/ray/.claude/projects/-Users-ray-Desktop-agentic-coding-school/a82e966c-3385-496c-b4c0-aef788abf569.jsonl` (regression-hunter subagent on 2026-05-23). Key facts:

- Commit `2a08f84f` (2026-03-13) **introduced** UTM-to-Stripe-metadata writing. Before that, the code path didn't exist.
- Commit `4bdaf5f2` (2026-03-28) added `posthog_distinct_id` to the same metadata.
- Commit `40d31553` (2026-04-10) added sessionStorage UTM persistence across landing-page navigation.
- Commit `aafd4f73` (2026-04-22) upgraded to a 30-day first-touch cookie and added `utm_content/term`.
- `git log -S "utm_campaign"` returns only ADD commits, never deletions.
- Pre-2026 Stripe volume was effectively zero (1 test session in 2024, 4 in 2025 H1, 140 in 2025 H2 — all in December). There is no historical "good attribution era" to compare against; pre-Mar-13 sessions all show 0% utm_campaign because the code didn't exist.

**Two real attribution leaks are still open** as of 2026-05-23:
- Workshop checkout (`use-workshop-register.ts`, commit `0693314e` on 2026-05-17): doesn't call `useUtmParams()`, so workshop sales lose UTMs at the source. Every `masterclaudecode.com` workshop sale is unattributable until fixed.
- Workshop checkout: doesn't pass `posthog_distinct_id` either. Same fix surface.

If a future snapshot shows workshop coverage still at ~0%, these leaks haven't been fixed yet.
