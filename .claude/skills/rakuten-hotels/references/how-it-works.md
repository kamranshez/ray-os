# How jphotels works, and how to upgrade it

This is the maintenance brain of the skill. Read it when the tool returns
nothing / garbage, when Rakuten changes their site, or when you want to add a
feature. The tool was reverse-engineered from Rakuten Travel's own search
endpoint using `agent-browser` + HAR capture; there is no official API involved.

## The core discovery

Rakuten Travel's hotel search is a **plain server-rendered GET** — there is no
JSON hotel API. Every XHR on the results page is ad/analytics noise. The hotel
list comes from:

```
https://search.travel.rakuten.co.jp/ds/vacant/searchVacant?<f_...params>
```

A normal HTTP client (curl / urllib) with a browser User-Agent gets the full
~1MB results HTML back. No cookies, no auth, no JS execution needed.

### Query parameters (all prefixed `f_`)

| Param | Meaning |
| --- | --- |
| `f_dai=japan` | top region (always `japan`) |
| `f_chu` | prefecture code, e.g. `kyoto`, `osaka`, `tokyo` (romaji) |
| `f_shou` | sub-area within a prefecture (e.g. Tokyo `tokyo`=23 wards, `nishi`=Tama) |
| `f_sai` | sub-sub-area (e.g. Tokyo ward groups use **uppercase** `A`,`B`,`C`) |
| `f_nen1/f_tuki1/f_hi1` | check-in year / month / day |
| `f_nen2/f_tuki2/f_hi2` | check-out year / month / day |
| `f_otona_su` | adults total |
| `f_heya_su` | rooms |
| `f_hyoji` | results per page (use 30) |
| `f_page` | page number |
| `f_sort` | sort code (see below) |
| `f_teikei=quick` | required boilerplate |

The full prefecture-name → `f_chu` map (all 47) is embedded in `jphotels.py`
(`PREFECTURES`), extracted from the homepage prefecture `<select>`.

### Sort codes (`f_sort`)

| CLI value | `f_sort` | meaning |
| --- | --- | --- |
| `recommended` | `hotel` | Rakuten's default ranking |
| `price` | `hotel_kin_low` | cheapest total first |
| `price-desc` | `hotel_kin_high` | most expensive first |
| `rating` | `hotel_hotel_eval` | review score |
| `size` | `hotel_hotel_wide` | room size |

## The variable-depth area hierarchy (the tricky part)

Prefectures are **not** uniformly searchable. Some (Kyoto, Osaka) resolve a
whole-prefecture hotel list directly from `searchVacant?f_chu=kyoto`. Broad
metros (Tokyo, and Hokkaido) instead **302-redirect to the `jparea` area
picker** because the area is too big and needs drilling:

```
prefecture (f_chu) -> district/area (f_shou) -> sub-area (f_sai) -> hotel list
```

Depth varies: Kyoto = 0 extra levels, Tokyo = up to 3.

The tool handles this uniformly with a **recursive resolver** (`collect()`):

1. Fetch `searchVacant` for the current area codes.
2. Detect the outcome by the **final URL** (`urllib` follows redirects):
   - stays on `/ds/vacant/searchVacant` → it's a hotel list → parse it (leaf).
   - lands on `/jparea/` → it's an area picker → parse child area links and
     recurse into each, aggregating + de-duplicating hotels.
3. After aggregation, re-sort globally (per-leaf order is meaningless once we
   merge many sub-areas) and apply `--limit`.

Two gotchas that cost real debugging time (don't reintroduce them):
- **Sub-area codes mix case.** Tokyo ward groups use `f_sai=A`. The code-extract
  regex must be `[A-Za-z_0-9]*`, not lowercase-only, or every ward collapses to
  the parent signature and gets skipped as "visited".
- **Two kinds of drill-down link.** A `jparea` page mixes `jparea→jparea`
  district-nav links (e.g. `data-locate`, `id="t-01"`) AND `searchVacant`
  "search now" links. `child_areas()` captures **any** anchor carrying area
  codes, but constrains recursion to links that stay in the same prefecture
  branch and are strictly deeper — otherwise it wanders into other prefectures
  or loops.

`--subarea <text>` prunes the drill-down to child areas whose label matches the
text (e.g. `--subarea 函館` for Hakodate), so a huge prefecture searches in ~1s
instead of scanning everything.

## Parsing the results HTML

Per-hotel block = from one name anchor to the next. Extract per block (regex in
`parse_hotels()`):

| Field | Markup |
| --- | --- |
| id + name | `<a id="<id>_link" ...>NAME</a>` |
| price (total) | `<span class="ndPrice">合計<strong>10,980</strong>円` — take the **min** across plans in the block |
| rating + count | `<strong>4.35</strong>（7596件）` inside the `_review` anchor |
| access | `class="htlAccess"> <span>...</span>` |
| detail URL | `https://travel.rakuten.co.jp/HOTEL/<id>/<id>.html` |

**Why block-based, not fixed-window:** promoted hotels carry long sponsor
blurbs that push their price hundreds of lines below the name. A fixed
character window missed them and reported `price: null`. Splitting on the next
hotel anchor fixes this.

## Price filtering is client-side (deliberate)

The server's own `f_kin` (min) / `f_kin2` (max) use an inconsistent per-night
scale and return **zero** results when combined. So the tool ignores them
(`f_kin=""`, `f_kin2=0`) and filters `--min-price`/`--max-price` on the parsed
**total** price instead. Predictable, matches the displayed number. Because it's
client-side, it only sees fetched hotels — widen with `--pages`.

`--filter <text>` similarly matches name/access/area substrings (e.g.
`--filter 温泉` for onsen) after parsing.

## Upgrade playbook

**If the tool returns 0 hotels for an area that should have them:**
1. Print the final URL — did it redirect to `/jparea/`? Then it's an area that
   needs drilling; check `child_areas()` is finding children (label + codes).
2. `curl -sL -A 'Mozilla/5.0' '<searchVacant URL>' | grep -c 'id="[0-9]*_link"'`
   to confirm the endpoint itself still returns hotels.

**If names/prices/ratings come back empty (markup changed):**
The regexes in `parse_hotels()` are the fragile surface. Re-derive them:
1. Recapture fresh HTML: `curl -sL -A 'Mozilla/5.0' '<searchVacant URL>' -o /tmp/list.html`
2. Grep for the new class names around a known hotel and update the regex.
3. Compare against the stored baseline HAR (see below) to see what changed.

**To recapture a fresh HAR** (when the whole flow shifts), replay the original
capture with agent-browser:
```bash
agent-browser --session rakuten open https://travel.rakuten.co.jp
agent-browser --session rakuten network har start --content all
# select prefecture + dates in the form, click 検索, then:
agent-browser --session rakuten network har stop fresh.har
```
Then hunt for the hotel-list document and diff its params/markup against this
skill's baseline.

**To add a feature** (e.g. `--meals`, station-distance sort): the parse layer
already has the access blurb; most attribute filters are a client-side pass over
the parsed hotel dicts, mirroring how `--filter` and price filtering work. Keep
new filters client-side unless you've verified the server param behaves.

## The baseline HAR

`rakuten-search.har.gz` (gunzip to ~11MB) is the original capture that this tool
was built from: a full Kyoto search from `travel.rakuten.co.jp`, 393 requests
with response bodies embedded. It is the ground-truth evidence of the endpoint,
params, and markup at build time (2026-07-20). Use it to diff against a fresh
capture when something breaks.

Inspect it without loading 11MB into context:
```bash
gunzip -c references/rakuten-search.har.gz > /tmp/base.har
python3 -c "import json; h=json.load(open('/tmp/base.har')); \
print(len(h['log']['entries']),'requests'); \
[print(e['response']['status'], e['request']['url'][:90]) \
 for e in h['log']['entries'] if 'searchVacant' in e['request']['url'] or 'jparea' in e['request']['url']]"
```
