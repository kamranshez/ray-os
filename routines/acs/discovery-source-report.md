You are the weekly report on the **checkout-gate discovery picker** — the optional "What helped you decide to join?" tile grid in `CheckoutGateModal.tsx`. The selected tile is forwarded into Stripe Checkout Session metadata as `discovery_source` and mirrored onto these PostHog events:

- `checkout_modal_source_selected` — fired the instant the tile is clicked (client-side, ad-blockable)
- `checkout_modal_continue_clicked` — fired on "Continue to Stripe" (client-side)
- `checkout_session_created` — server-side, when the Stripe session opens
- `purchase_complete` — server-side, from the Stripe webhook. **This is the source of truth.**

The `discovery_source` property was added to `purchase_complete` and `checkout_session_created` on **2026-06-02**. Events older than that will be missing the field — bucket those as `(unknown)`, not `(skipped)`. The two modal-level events have carried it since the modal shipped.

Valid source ids: `podcast_or_newsletter`, `github`, `rays_youtube`, `google_search`, `rays_x_or_twitter`, `email_announcement`, `coworker_or_friend`, `other`, plus the implicit `(skipped)` bucket.

Only send a message if there is data to report. If `purchase_complete` returned zero rows in the last 7 days, exit silently.

## Required MCPs

- **PostHog** — analytics queries (`switch-project`, `query-run`)

## STEP 0: PIN POSTHOG PROJECT

Call `switch-project` with `projectId: 236619` ("Agentic Coding School"). The default "HyperWhisper" (id 224249) returns 0 for every ACS event — do NOT report that as a tracking outage.

## STEP 1: QUERY POSTHOG

Run these HogQL queries against `events`. **Always** filter `properties.source = 'server'` on `purchase_complete` to avoid double-counting client-side duplicates.

**Query A — Completed purchases by source, last 7 days:**
```
SELECT coalesce(nullIf(properties.discovery_source, ''), '(skipped)') AS source,
       count() AS purchases,
       sum(toFloat64OrNull(properties.amount)) / 100 AS revenue_usd
FROM events
WHERE event = 'purchase_complete'
  AND properties.source = 'server'
  AND timestamp > now() - interval 7 day
  AND timestamp >= toDateTime('2026-06-02 00:00:00')
GROUP BY source
ORDER BY purchases DESC
```

**Query B — Same, last 30 days** (swap `7 day` for `30 day`).

**Query C — Purchases by source × purchaseType, last 30 days:**
```
SELECT coalesce(nullIf(properties.discovery_source, ''), '(skipped)') AS source,
       properties.purchaseType AS purchase_type,
       count() AS purchases
FROM events
WHERE event = 'purchase_complete'
  AND properties.source = 'server'
  AND timestamp > now() - interval 30 day
  AND timestamp >= toDateTime('2026-06-02 00:00:00')
GROUP BY source, purchase_type
ORDER BY source, purchases DESC
```

**Query D — Selection→purchase funnel by source, last 30 days:**
```
SELECT properties.source AS source,
       count() AS selections
FROM events
WHERE event = 'checkout_modal_source_selected'
  AND timestamp > now() - interval 30 day
GROUP BY source
ORDER BY selections DESC
```

**Query E — Prior 7d window for week-over-week movers:** re-run Query A's logic for the 8–14d-ago window.

If Query A returns zero rows → stop. Do not send any message.

## STEP 2: COMPUTE METRICS

For both 7d and 30d windows:

- Total purchases, total revenue.
- Per-source share (purchases as % of total, revenue as % of total). Sort desc by purchases.
- Attach rate — share of buyers who picked any source (not `(skipped)`).
- Selection→purchase conversion per source (30d) — `purchases / selections`. Flag sources materially above/below average.
- Movers (7d vs prior 7d) — change in purchase share. Highlight any ≥5 percentage points.

## STEP 3: GENERATE 1–2 RECOMMENDATIONS

Tied to specific numbers, not generic. Skip recommendations entirely if data is too thin (<15 purchases in 7d).

## STEP 4: POST TO SLACK

Channel: `#acs-discovery`. Post via the Slack Web API with curl (NOT webhooks):

```bash
MESSAGE=$(cat <<'MSG'
{message text}
MSG
)
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$(jq -n --arg ch 'acs-discovery' --arg txt "$MESSAGE" '{channel: $ch, text: $txt, mrkdwn: true, unfurl_links: false}')"
```

Inspect the response. If `ok: false`, log the error and retry once. Use Slack mrkdwn (single asterisks for bold), not GFM. If `SLACK_BOT_TOKEN` is empty, write the full report to stdout instead.

### Message format

```
*Discovery Source Report* _(past 7 days · 30d in parens)_

*Top sources (7d):*
```
{source_padded}  {purchases}  ({share}%)  ${revenue}
...
```

*Attach rate:* {X}% picked a source · {Y}% skipped (7d) · {X30}% / {Y30}% (30d)

*Selection → purchase conversion (30d, ranked):*
{source} {conv}% · {source} {conv}% · ...

*Movers vs prior 7d:*
- {source}: {old}% → {new}% ({±Δ}pp)

*Read:*
- {Recommendation tied to a specific number above}
```

Drop a section if it has nothing meaningful, rather than padding.

## ERROR HANDLING

If a PostHog query errors, retry once. If the second attempt fails, post a one-line alert to `#acs-discovery` and exit:

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$(jq -n --arg ch 'acs-discovery' --arg txt '⚠️ *Discovery Source Routine Failed* — step: {step}, error: {error}' '{channel: $ch, text: $txt}')"
```

## KEY PRINCIPLES

- **Source of truth is `purchase_complete` with `source = 'server'`.** Modal-click events are leading indicators only.
- **Cut off all queries at 2026-06-02.** Earlier rows pre-date the property.
- **Read-only.** Do not modify repo files.
- **Cap runtime at ~5 minutes.**
