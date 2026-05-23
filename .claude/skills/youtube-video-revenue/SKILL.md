---
name: youtube-video-revenue
description: Produce a per-video revenue and performance comparison for the Agentic Coding School / Ray Amjad YouTube channel, combining YouTube view counts (VidTempla), site visitor traffic (PostHog), and the source-of-truth checkout sessions (Stripe REST API). Saves a timestamped snapshot so future runs can show which old videos kept earning. Use this skill whenever Ray asks to compare videos, rank videos by revenue, see which video made the most, audit YouTube attribution, rerun the video performance report, check if a recent video paid off, or any phrasing about "which YouTube video drove sales." Trigger this even if Ray only says "rerun the comparison" or "do the video thing again."
---

# YouTube Video Revenue Tracker

This skill answers the question **"which of my YouTube videos has driven the most revenue, and how is that changing over time?"** It combines three data sources and saves a historical snapshot each run so old videos that keep selling get visible credit.

## Why this exists

Ray ships ~5 YouTube videos a month and most attribution analysis in PostHog covers only ~10% of actual sales (90% of Stripe Checkout Sessions have no `utm_campaign` metadata). The truth lives in Stripe Checkout Session metadata, which the Stripe MCP can't search. This skill bypasses that by hitting the Stripe REST API directly with a restricted live key Ray provides per run.

Each snapshot is a point-in-time view of cumulative per-video metrics, so a video published in January that closes a sale in May shows up in the May snapshot's delta.

## What the skill produces

1. A **markdown comparison report** with two ranked tables:
   - **UTM revenue** (lower-bound truth, ~11–25% coverage in 2026 depending on window)
   - **Time-proximity revenue** (best retroactive estimate, ~48% coverage)
   Plus secondary columns for YouTube views, PostHog visitors, workshop checkouts, and lift over baseline.
2. A **snapshot JSON** at `snapshots/<YYYY-MM-DD>.json` containing the full per-video data for both methods.
3. A **delta block** comparing this run to the most recent prior snapshot: which videos earned new revenue since last time, which dropped, which new videos appeared.

## Two attribution methods — why both

**UTM attribution** (`metadata.utm_campaign` on Stripe Checkout Sessions) is the lower-bound truth: it's set at checkout creation, persists through redirects, and is never wrong. BUT the code that writes it only shipped on **2026-03-13** (commit `2a08f84f`), so every session before that date structurally cannot carry UTMs. That single fact suppresses YTD coverage to ~11%; the post-Mar-13 slice alone is ~21–25%. There has been no regression — UTM attribution has only ever moved up. Don't bother re-investigating that.

**Time-proximity attribution** credits every clean Stripe session to the most-recently-published video whose [publishedAt, publishedAt + 3 days] window contains the session, then subtracts a baseline daily median to estimate genuine video lift. This recovers ~48% of YTD revenue and is the best way to see what early-2026 videos (which predate UTM tracking) actually earned. Always run it — the marginal cost is ~1 second of Python.

When the two disagree by a lot, time-proximity is usually right for old videos and UTM is right for recent ones. Mention both in the report.

## When to invoke

Strong triggers (run the skill):
- "Which video made the most money this year?"
- "Rerun the video comparison."
- "How did [video title] do?"
- "Pull the video revenue report."
- "Compare my last N videos by sales."
- "Did the workshop video pay off?"

Don't invoke for:
- Pure YouTube analytics questions (use VidTempla MCP directly).
- One-off "how much did I make today" — that's a Stripe balance question, not a video question.

## Workflow

### Step 1 — Get the Stripe key

Check the env first:

```bash
echo "${STRIPE_RESTRICTED_KEY:-(not set)}"
```

If unset, ask Ray to paste it (he uses an `rk_live_` restricted key with read access to checkout sessions). Export it for the current shell only — never write it to a file, never echo it back, never commit it.

```bash
export STRIPE_RESTRICTED_KEY='rk_live_...'
```

### Step 2 — Determine the window

Default to year-to-date of the current calendar year. If Ray gives a window ("last 90 days", "since March"), honor it. The window controls **which Stripe sessions to fetch** and **which videos to list in the published-in-window section** — but the snapshot itself always captures every video the channel has, so older videos that keep selling still show up in the delta.

Convert dates to Unix timestamps. For YTD with today being `2026-05-23`, that's `created[gte]=1767225600` (Jan 1 2026 UTC).

### Step 3 — Fetch the three data sources in parallel

Do these in one tool-use block so they run concurrently. Save each to a temp file under `/tmp/yvr-<run_id>/`.

**A) VidTempla — channel videos + YouTube views**

The channel ID is `UCLA7cJBnqr0nLF2bQBD9uUg` (Ray Amjad). Call:
- `list_videos` with `sort: publishedAt:desc`, `limit: 100`. **Always fetch at least the past 12 months** of videos — even if the reporting window is shorter, old videos keep generating attributed revenue and must be in the index so their Stripe sessions don't fall into "unknown utm_campaign" anomalies. Paginate via the response cursor until `publishedAt` falls more than 365 days before today. For typical Ray channel volume (5 videos/month), 12 months = ~60 videos.
- `query_analytics` with `dimensions: video`, `metrics: views,estimatedMinutesWatched,averageViewDuration`, filter `video==<id1>,<id2>,...` for the videos returned. YouTube Analytics lags by ~24-48h, so videos published in the last day or two may be absent — fall back to Ray's stated view count if he mentions one, or note the gap.

If `list_videos` returns a "result exceeds maximum tokens" error (>100 videos), spawn a subagent to read the cached file in chunks and return only `videoId | title | publishedAt`. See the failure pattern in `references/data_sources.md`.

The report distinguishes between "published in window" (the videos Ray cares about most for the current snapshot) and "still earning" (older videos with non-zero revenue), so always-fetching-12-months doesn't bloat the main table.

Save normalized output to `/tmp/yvr-<run_id>/vidtempla.json`:

```json
{
  "videos": [
    {"videoId": "c0gVowvMR-g", "title": "...", "publishedAt": "2026-05-22", "youtube_views": 17000}
  ]
}
```

**B) PostHog — visitors + workshop checkouts**

Project: `Agentic Coding School` (id 236619). Run `query-trends` with `breakdownFilter` on `utm_campaign`, filtered to the list of video IDs. The `weekly_active` math gives correctly-deduplicated unique visitor counts for the full window (don't use `dau` and sum — that double-counts returning visitors).

Three series, one breakdown query each:
1. `$pageview`, `math: weekly_active`, filter event `utm_campaign in [video_ids]`, breakdown on event `utm_campaign` — gives visitors per video.
2. `workshop_checkout_started`, `math: total`, filter person `$initial_utm_campaign in [video_ids]`, breakdown on person `$initial_utm_campaign` — gives workshop checkouts per video.
3. `purchase_complete`, `math: total`, filter person `$initial_utm_campaign in [video_ids]`, breakdown on person `$initial_utm_campaign` — PostHog's view of class purchases (will undercount vs Stripe — keep it as a sanity column).

Save to `/tmp/yvr-<run_id>/posthog.json`:

```json
{
  "visitors": {"c0gVowvMR-g": 180, ...},
  "workshop_checkouts": {"c0gVowvMR-g": 8, ...},
  "posthog_purchases": {"_QGgk9F9CSM": 24, ...}
}
```

**C) Stripe — every completed checkout session in window**

Run the fetch script:

```bash
python3 .claude/skills/youtube-video-revenue/scripts/fetch_stripe.py \
  --created-gte 1767225600 \
  --output /tmp/yvr-<run_id>/stripe.json
```

The script reads `STRIPE_RESTRICTED_KEY` from env, paginates `GET /v1/checkout/sessions?status=complete` until exhausted (max 100 pages safety), and writes a normalized JSON array. Expect ~1,600 sessions YTD and ~30 seconds runtime.

### Step 4 — Compute time-proximity attribution

Before building the snapshot, run the time-attribution script. It produces a JSON the snapshot builder will merge in:

```bash
python3 .claude/skills/youtube-video-revenue/scripts/time_attribute.py \
  --vidtempla /tmp/yvr-<run_id>/vidtempla.json \
  --stripe /tmp/yvr-<run_id>/stripe.json \
  --output /tmp/yvr-<run_id>/time_attribution.json
```

Default window is 3 days after publish. Override with `--window-days N` if Ray asks. Sessions with `metadata.purchaseType == "team_add_seats"` or `metadata.upgrade_from` set are excluded as noise (not video-driven). See `references/data_sources.md` for the full method.

### Step 5 — Build the snapshot

Run the snapshot builder. It does the joining, applies known aliases (e.g. the `SbB5gc_1K8` → `YSbB5gc_1K8` Y-prefix bug), merges in time-attribution, and renders the markdown report:

```bash
python3 .claude/skills/youtube-video-revenue/scripts/build_snapshot.py \
  --vidtempla /tmp/yvr-<run_id>/vidtempla.json \
  --posthog /tmp/yvr-<run_id>/posthog.json \
  --stripe /tmp/yvr-<run_id>/stripe.json \
  --time-attribution /tmp/yvr-<run_id>/time_attribution.json \
  --snapshots-dir .claude/skills/youtube-video-revenue/snapshots \
  --window-from 2026-01-01 \
  --window-to <today> \
  --aliases .claude/skills/youtube-video-revenue/references/aliases.json
```

The script writes `snapshots/<YYYY-MM-DD>.json` (overwrites if same day) and prints the markdown report to stdout. Pass that report back to Ray.

### Step 6 — Surface anomalies

After rendering, scan the snapshot's `anomalies` array and explicitly call out:
- Unknown `utm_campaign` values that look like YouTube IDs (11 chars, alphanumeric + `_-`) — could be missed videos or another instance of the Y-prefix bug.
- Videos with high visitor counts but $0 revenue — possible attribution gap or genuinely poor converters.
- Sudden drops in cumulative revenue vs previous snapshot (would indicate refunds or data fetch issues).

## Important constraints

- **Never log or persist `STRIPE_RESTRICTED_KEY`.** It only lives in env for the current shell. If Ray pastes a key, do not echo it back, do not write it to a file, do not commit it.
- **Stripe metadata is the source of truth for revenue.** PostHog `purchase_complete` undercounts (server-side capture loss). When the two disagree, trust Stripe and note the gap.
- **YouTube Analytics has ~24-48h lag.** Videos published in the last two days may show 0 views — fall back to user-stated counts and note it.
- **The Y-prefix bug is real.** Until fixed in code, the aliases file maps `SbB5gc_1K8` → `YSbB5gc_1K8`. Keep this file updated when you find new aliases.
- **Workshop sales attribution is broken on this Stripe account.** The workshop product (`prod_UWxc36YNXREZcA`) lives here, but most workshop sessions lack `utm_campaign` because the agentengineer.pro checkout flow doesn't forward it. Filter Stripe sessions on `metadata.purchaseType=workshop` for a workshop-specific count, then note the attribution gap separately.

## File layout

```
youtube-video-revenue/
├── SKILL.md                       (this file)
├── scripts/
│   ├── fetch_stripe.py            # Paginates Stripe Checkout Sessions API
│   ├── time_attribute.py          # 3-day proximity attribution with baseline lift
│   └── build_snapshot.py          # Combines all sources, writes snapshot + markdown
├── snapshots/
│   └── YYYY-MM-DD.json            # One per snapshot day; carries both UTM and time-attribution per video
├── reports/
│   └── YYYY-MM/
│       └── YYYY-MM-DD-<topic>.md  # Free-form analyses derived from snapshots (transcript patterns, A/B post-mortems, channel-strategy memos, etc.)
└── references/
    ├── data_sources.md            # Schemas, gotchas, attribution caveats, time-method details
    └── aliases.json               # Known utm_campaign → real videoId mappings
```

### Saving derived analyses

Whenever a snapshot is followed by deeper analysis (pattern-mining transcripts, hypothesis investigations, strategy memos), save the result as `reports/<YYYY-MM>/<YYYY-MM-DD>-<short-topic>.md`. Always include at the top: the source snapshot filename, the method (especially if subagents were spawned with specific lenses), and the "why this exists" framing — these reports should still be readable in 12 months when the underlying transcripts and conversation context are gone.

## Report template

ALWAYS use this exact structure when returning the markdown to Ray:

```
# Video Revenue Snapshot — <YYYY-MM-DD>
Window: <YYYY-MM-DD> to <YYYY-MM-DD>
Stripe sessions captured: <N>
Total revenue: $<XXX,XXX>
UTM attribution: <X.X>% (lower-bound — only post-2026-03-13 sessions can carry UTMs)
Time-proximity attribution (3-day window): <X.X>% raw / <X.X>% lift-adjusted

## Top earners by UTM revenue (lower-bound truth)
| Rank | Video | Published | UTM rev | Sessions | Visitors | YT views | $/view |

## Top earners by time-proximity (best retroactive estimate)
| Rank | Video | Published | Time-attrib | Lift | UTM rev | Δ (time − UTM) |

## Published in window (chronological)
| Published | Video | Revenue | Sessions | Visitors | YT views | CTR | Δ since last snapshot |

## Older videos still earning
(videos published before window that still attribute revenue inside it)

## Movers since last snapshot (<previous-date>)
- <videoId> earned $<X> in new revenue (<N> new sessions). Median age <D> days.
- <new-video-id> appeared.

## Anomalies
- <list>
```

## Subsequent runs

When Ray asks you to rerun this skill, **always load the previous snapshot** from `snapshots/` (most recent `.json` file by name) and compute the delta. The historical accumulation is the whole point — without the delta, old videos look static.
