# PostHog HogQL Query Cookbook

All queries target the Agentic Coding School project (`projectId: 236619`). Switch to that project first with `mcp__claude_ai_PostHog__switch-project`.

Use `mcp__claude_ai_PostHog__query-run` with a `DataVisualizationNode` wrapping a `HogQLQuery`. All queries below are templates — replace `<START>`, `<END>`, and the `utm_campaign IN (...)` list with the target month's values.

## Query 1: Attribution coverage sanity check (RUN FIRST)

Before doing anything else, measure how much of the month's revenue is UTM-attributed. This tells you how much weight to put on PostHog findings vs the Stripe 3-day window.

```sql
SELECT
  count() AS total_purchases,
  countIf(properties.utm_campaign IS NOT NULL) AS tagged_purchases,
  round(countIf(properties.utm_campaign IS NOT NULL) * 100.0 / count(), 1) AS coverage_pct,
  sum(toFloat(properties.amount))/100 AS total_revenue_usd,
  sumIf(toFloat(properties.amount), properties.utm_campaign IS NOT NULL)/100 AS tagged_revenue_usd
FROM events
WHERE event = 'purchase_complete'
  AND properties.source = 'server'
  AND timestamp >= '<START>'
  AND timestamp < '<END>'
```

**Interpreting the result:**
- **Coverage < 5%**: Attribution is broken or checkout flow regressed. Flag this prominently in the audit. Do not draw per-video conclusions from tagged revenue. Lean heavily on pageview CTR + Stripe 3-day windows instead.
- **Coverage 5–20%**: Normal (March 2026 baseline was ~8%). Tagged revenue is a lower bound. Still useful for directional per-video comparisons but caveat it.
- **Coverage 20–60%**: The checkout UTM fix is partially working. Tagged revenue becomes a more reliable signal but still not ground truth.
- **Coverage > 60%**: The fix shipped. Tagged revenue is now the primary attribution source. De-emphasize the Stripe 3-day window and put tagged revenue front-and-center.

The audit's "Methodology and its limits" section must quote the exact coverage % and explain how it shapes the confidence of the rest of the report.

## Query 2: Pageview traffic per video (the reliable signal)

```sql
SELECT
  properties.utm_campaign AS campaign,
  count(DISTINCT properties.$device_id) AS unique_visitors,
  count() AS pageviews
FROM events
WHERE event = '$pageview'
  AND timestamp >= '<START>'
  AND timestamp < '<END>'
  AND properties.utm_source = 'youtube'
  AND properties.utm_campaign IN ('<id1>','<id2>',...)
GROUP BY campaign
ORDER BY unique_visitors DESC
```

**Notes:**
- Some video IDs get truncated in PostHog (e.g., `YSbB5gc_1K8` → `SbB5gc_1K8`). Query with both forms if you don't see a video you expect.
- `unique_visitors` is the reliable top-of-funnel metric. Use it to compute CTR = `visitors / YouTube viewCount * 100%`.
- Also query without the `utm_campaign IN (...)` filter to find older videos still driving traffic in the current month — often worth a callout in the audit.

## Query 3: Tagged purchases per video

```sql
SELECT
  properties.utm_campaign AS campaign,
  count() AS purchases,
  sum(toFloat(properties.amount))/100 AS revenue_usd,
  avg(toFloat(properties.amount))/100 AS avg_order
FROM events
WHERE event = 'purchase_complete'
  AND timestamp >= '<START>'
  AND timestamp < '<END>'
  AND properties.utm_campaign IS NOT NULL
  AND properties.amount IS NOT NULL
GROUP BY campaign
ORDER BY revenue_usd DESC
```

Use this for the "tagged revenue" column in the per-video table. If coverage is low, present these numbers as a lower bound only.

## Query 4: Daily pageview flow (for the daily log table)

```sql
SELECT
  toDate(timestamp) AS day,
  properties.utm_campaign AS campaign,
  count(DISTINCT properties.$device_id) AS visitors
FROM events
WHERE event = '$pageview'
  AND timestamp >= '<START>'
  AND timestamp < '<END>'
  AND properties.utm_source = 'youtube'
  AND properties.utm_campaign IN ('<id1>','<id2>',...)
GROUP BY day, campaign
ORDER BY day
```

Useful for understanding when each video's traffic actually peaks — does the traffic decay in 2 days (normal) or sustain over 5+ days (long-tail pillar)?

## Query 5: Person-level attribution (secondary check)

```sql
SELECT
  person.properties.$initial_utm_campaign AS campaign,
  count() AS purchases,
  sum(toFloat(properties.amount))/100 AS revenue
FROM events
WHERE event = 'purchase_complete'
  AND properties.source = 'server'
  AND timestamp >= '<START>'
  AND timestamp < '<END>'
GROUP BY campaign
ORDER BY revenue DESC
```

Joins on the person record's `$initial_utm_campaign`. Usually even more null than Query 3 because the Stripe return page overwrites the initial referrer with `checkout.stripe.com`. But if it returns different numbers from Query 3, that's a signal worth investigating.

## Known PostHog quirks

- **Leading-char truncation**: Some queries return video IDs missing their first character (e.g., `YSbB5gc_1K8` → `SbB5gc_1K8`, `XVEodnI0aHA` → `XVEodnI0a`). Treat truncated forms as the same video. Cross-check with the full ID if unsure.
- **Client-side pageviews are noisy**: The `/purchase-complete` page fires a `$pageview` with `utm_campaign: null` because it's reached via a Stripe redirect. Always filter to `utm_source = 'youtube'` to exclude these.
- **Subscription renewals lack UTM**: Monthly subscription renewals fire `purchase_complete` events with no UTM because they don't go through the checkout flow. They inflate "dark" revenue. If Ray's offering subscriptions, subtract subscription renewals before computing coverage.
