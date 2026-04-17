# Chart HTML Template

The canonical chart template is the previous month's HTML file (most recently `/Users/ray/Desktop/ray-os/socials/youtube/performance/2026-03-chart.html`). Copy it, then edit these four things:

## 1. Header text

- `<title>` → `{Month} Video Revenue — 3-Day Post-Upload`
- `<h1>` → `{Month} Video Revenue — 3-Day Post-Upload Window`
- `.subtitle` → pulled date + data source note

## 2. Stat cards (4 cards)

- **Total Net Revenue** (green) — sum of per-video net values
- **Total Sales** (blue) — sum of per-video sales values
- **Avg Revenue / Video** (purple) — total net / video count
- **UTM Attribution Coverage** (orange) — e.g., `~8%` for March. Match the coverage % from PostHog Query 1. If coverage jumps significantly from the previous month, note it in the subtitle.

## 3. Data array

The only data-bearing code in the chart is the `const data = [...]` array. Each item:

```js
{
  title: "Display title",
  date: "Mar 24",
  views: 97233,              // from VidTempla
  visitors: 642,             // from PostHog pageview query
  sales: 38,                 // from Stripe 3-day window
  gross: 6029,               // from Stripe, dollars
  refunds: 569,              // from Stripe, dollars
  net: 5460,                 // gross - refunds
  avg: 159,                  // gross / sales, rounded
  tagged: 1449,              // from PostHog tagged purchase query, dollars
  pitch: "Newsletter mid / class end",  // one-line description
}
```

The `ctr` field is computed automatically: `data.forEach(d => { d.ctr = (d.visitors / d.views * 100); });`

## 4. Table (auto-renders from `data`)

The table has 11 columns and renders from the data array — no manual edits needed:
`Video, Upload, Views, Sales, Gross, Net, Avg Order, Site Visitors, CTR, Tagged $, Pitch`

## Chart definitions (unchanged)

Four charts, all rendered from the same `data` array:
1. **Revenue bar + sales line** (`revenueChart`)
2. **Views vs Revenue** (`viewsChart`) — surfaces the "high views / low revenue" mismatch
3. **AOV line** (`priceChart`)
4. **Click-through rate bar** (`ctrChart`) — the PostHog-reliable signal

Do not change chart definitions unless you're adding a new dimension (e.g., comparing to previous month). If you add a chart, add a `<canvas>` in the body and a new `new Chart(...)` block in the script.

## What to double-check before shipping

- All 9 (or however many) videos are in the data array
- No NaN or undefined values
- `ctr` renders as a percentage (two decimals)
- `tagged` is dollars, not cents (divide by 100 if pulling from PostHog's `amount` field)
- File opens cleanly in a browser with no JS errors in the console
