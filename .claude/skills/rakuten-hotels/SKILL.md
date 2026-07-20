---
name: rakuten-hotels
description: >-
  Find and compare hotels & ryokan anywhere in Japan for specific dates via
  Rakuten Travel, straight from the command line — no API key, no browser.
  Use this whenever the user wants to find, search, compare, browse, or pick a
  place to stay in Japan — a city, prefecture, onsen town, or specific district
  like Hakodate, Kyoto, Tokyo, Osaka, Hokkaido — especially when they mention
  dates, nights, a budget, number of guests, an onsen/ryokan preference, or want
  results sorted by price or rating. Trigger it even if they don't say "Rakuten"
  or "hotel" explicitly (e.g. "where should I stay in Kyoto next month",
  "cheap onsen near Hakodate for one night", "book me somewhere in Osaka").
  Also use it to maintain, debug, or upgrade the jphotels tool, or to inspect
  the captured Rakuten Travel HAR.
---

# Rakuten hotels (jphotels)

A zero-dependency CLI that searches Rakuten Travel for real hotel availability
and prices in Japan on given dates. Reverse-engineered from Rakuten's own search
endpoint, so it needs only Python 3 stdlib — no API key, no browser, no network
setup. `scripts/jphotels.py` is the whole tool.

## Quick start

Run the script directly (path is relative to this skill directory):

```bash
python3 scripts/jphotels.py <area> --checkin YYYY-MM-DD [--nights N | --checkout YYYY-MM-DD] [options]
```

Give it a concrete area + a check-in date and it prints ranked hotels with total
price, review score, access blurb, and a booking URL. Use `--json` when you need
to filter/sort the results further yourself.

**Common recipes:**
```bash
# Cheapest Kyoto hotels, 2 nights, 2 adults
python3 scripts/jphotels.py kyoto --checkin 2026-08-15 --nights 2 --sort price

# Onsen stay in/near Hakodate (huge prefecture -> target the sub-area + filter)
python3 scripts/jphotels.py hokkaido --checkin 2026-09-05 --nights 1 --adults 1 \
    --subarea 函館 --filter 温泉 --sort rating --max-areas 40

# Tokyo under a budget, top-rated, machine-readable
python3 scripts/jphotels.py tokyo --checkin 2026-10-10 --nights 2 \
    --max-price 30000 --sort rating --json

# Every prefecture code
python3 scripts/jphotels.py --list-areas
```

## Choosing the area

Pass one of: a **romaji code** (`kyoto`, `osaka`, `tokyo`, `hokkaido`), an
**English alias** (`kobe`, `nagoya`, `sapporo`, `yokohama`, `naha`), or a
**Japanese prefecture** (`京都府`). `--list-areas` prints them all.

Big prefectures (Tokyo, Hokkaido) contain many sub-areas and would otherwise
aggregate hundreds of hotels from all over. When the user wants a specific city
or district, add **`--subarea <text>`** to prune the search to matching areas —
it matches the Japanese drill-down labels, so `--subarea 函館` (Hakodate),
`--subarea 新宿`, `--subarea 京都駅` all work and keep the search fast (~1s).

## Options worth knowing

| Option | Use it for |
| --- | --- |
| `--nights N` / `--checkout` | trip length |
| `--adults` / `--rooms` | party size (default 2 adults, 1 room) |
| `--sort` | `recommended` (default), `price`, `price-desc`, `rating`, `size` |
| `--subarea <text>` | narrow a big prefecture to a city/district |
| `--filter <text>` | keep only hotels whose name/access/area matches, e.g. `温泉` (onsen), `駅前` (near station) |
| `--min-price` / `--max-price` | total-price range in JPY (filters fetched results; widen with `--pages`) |
| `--pages N` | fetch more result pages per area (30 hotels/page) |
| `--max-areas N` | cap sub-areas fetched for broad metros (default 20; raise for Hokkaido/Tokyo) |
| `--limit N` | cap hotels shown |
| `--json` | structured output |

## Reading results to the user

Lead with a clear top pick and a couple of runner-ups (include a cheaper
option). Note that onsen ryokan prices are often per-person and include
dinner + breakfast, which is why totals look high — worth saying so the user
isn't surprised. Prices/availability shift by season and by the day, so results
are a live snapshot, not a quote.

**This tool is read-only — it cannot book or pay.** To reserve, the user opens
the hotel's URL themselves, or you can walk the Rakuten checkout with them in the
browser. Never imply a booking was placed.

## Understanding, debugging, or upgrading the tool

When the tool misbehaves (empty results, wrong prices after a site change), or
you want to add a feature (a new filter, a `--meals` flag, station-distance
sort), read **`references/how-it-works.md`**. It documents the endpoint and every
`f_` param, the variable-depth area hierarchy and the redirect-detection trick,
the HTML-parsing regexes and why they're block-based, the deliberately
client-side price filter, and a step-by-step upgrade playbook (including how to
recapture a fresh HAR with `agent-browser`).

`references/rakuten-search.har.gz` is the original HAR capture the tool was built
from (gunzip to ~11MB) — the ground-truth record of the endpoint and markup as of
2026-07-20. Diff a fresh capture against it to see what Rakuten changed. The
reference file shows how to inspect it without loading 11MB into context.
