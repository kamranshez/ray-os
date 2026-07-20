#!/usr/bin/env python3
"""
jphotels - find hotels in Japan on Rakuten Travel from the command line.

Reverse-engineered from the Rakuten Travel vacant-hotel search endpoint
(search.travel.rakuten.co.jp/ds/vacant/searchVacant), which is a plain
server-rendered GET. No API key, no browser, stdlib only.

Examples:
  jphotels.py kyoto --checkin 2026-08-15 --nights 1
  jphotels.py osaka --checkin 2026-09-01 --checkout 2026-09-03 --adults 2 --sort price
  jphotels.py tokyo --checkin 2026-10-10 --nights 2 --max-price 20000 --json
"""

import argparse
import datetime as dt
import gzip
import html as htmlmod
import io
import json
import re
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://search.travel.rakuten.co.jp/ds/vacant/searchVacant"

# prefecture (Japanese display name) -> Rakuten f_chu area code
PREFECTURES = {
    "北海道": "hokkaido", "青森県": "aomori", "岩手県": "iwate", "宮城県": "miyagi",
    "秋田県": "akita", "山形県": "yamagata", "福島県": "hukushima", "茨城県": "ibaragi",
    "栃木県": "tochigi", "群馬県": "gunma", "埼玉県": "saitama", "千葉県": "tiba",
    "東京都": "tokyo", "神奈川県": "kanagawa", "新潟県": "niigata", "山梨県": "yamanasi",
    "長野県": "nagano", "富山県": "toyama", "石川県": "ishikawa", "福井県": "hukui",
    "岐阜県": "gihu", "静岡県": "shizuoka", "愛知県": "aichi", "三重県": "mie",
    "滋賀県": "shiga", "京都府": "kyoto", "大阪府": "osaka", "兵庫県": "hyogo",
    "奈良県": "nara", "和歌山県": "wakayama", "鳥取県": "tottori", "島根県": "simane",
    "岡山県": "okayama", "広島県": "hiroshima", "山口県": "yamaguchi", "徳島県": "tokushima",
    "香川県": "kagawa", "愛媛県": "ehime", "高知県": "kouchi", "福岡県": "hukuoka",
    "佐賀県": "saga", "長崎県": "nagasaki", "熊本県": "kumamoto", "大分県": "ooita",
    "宮崎県": "miyazaki", "鹿児島県": "kagoshima", "沖縄県": "okinawa",
}
# romaji code -> Japanese display name (reverse lookup)
CODE_TO_JP = {v: k for k, v in PREFECTURES.items()}
# common English aliases -> romaji code
ALIASES = {
    "hokkaido": "hokkaido", "sapporo": "hokkaido",
    "tokyo": "tokyo", "kyoto": "kyoto", "osaka": "osaka",
    "kanagawa": "kanagawa", "yokohama": "kanagawa",
    "aichi": "aichi", "nagoya": "aichi",
    "fukuoka": "hukuoka", "hukuoka": "hukuoka",
    "hyogo": "hyogo", "kobe": "hyogo",
    "okinawa": "okinawa", "naha": "okinawa",
    "hiroshima": "hiroshima", "nagano": "nagano", "nara": "nara",
    "chiba": "tiba", "tiba": "tiba",
    "shizuoka": "shizuoka", "ishikawa": "ishikawa", "kanazawa": "ishikawa",
    "miyagi": "miyagi", "sendai": "miyagi",
}

SORTS = {
    "recommended": "hotel",
    "price": "hotel_kin_low",
    "price-desc": "hotel_kin_high",
    "rating": "hotel_hotel_eval",
    "size": "hotel_hotel_wide",
}


def resolve_area(area):
    """Accept romaji code, English alias, or Japanese prefecture name -> f_chu code."""
    a = area.strip()
    if a in PREFECTURES:            # Japanese name given
        return PREFECTURES[a], a
    low = a.lower()
    if low in ALIASES:
        code = ALIASES[low]
        return code, CODE_TO_JP.get(code, code)
    if low in CODE_TO_JP:           # already a valid romaji code
        return low, CODE_TO_JP[low]
    return None, None


def parse_date(s):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"bad date '{s}' (use YYYY-MM-DD)")


def build_url(codes, checkin, checkout, adults, rooms, sort, per_page, page):
    # Note: price is filtered client-side on the parsed total (see main). The
    # server's own f_kin/f_kin2 params use an inconsistent per-night scale and
    # return nothing when combined, so we don't use them.
    params = {
        "f_dai": "japan",
        "f_chu": codes["f_chu"], "f_shou": codes.get("f_shou", ""),
        "f_sai": codes.get("f_sai", ""),
        "f_nen1": checkin.year, "f_tuki1": checkin.month, "f_hi1": checkin.day,
        "f_nen2": checkout.year, "f_tuki2": checkout.month, "f_hi2": checkout.day,
        "f_otona_su": adults, "f_heya_su": rooms,
        "f_hyoji": per_page, "f_page": page,
        "f_sort": SORTS[sort], "f_tab": "hotel", "f_teikei": "quick",
        "f_kin": "", "f_kin2": 0,
    }
    return ENDPOINT + "?" + urllib.parse.urlencode(params)


def fetch(url, timeout=25):
    """Return (html, final_url). final_url differs from url when the endpoint
    redirects a broad area to the jparea area-picker."""
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/151.0.0.0 Safari/537.36"),
        "Accept-Language": "ja,en;q=0.8",
        "Accept-Encoding": "gzip",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        final = resp.geturl()
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    return raw.decode("utf-8", "replace"), final


# any anchor on a jparea page that points to a deeper area (either a
# jparea->jparea district link or a searchVacant "search now" link)
AREA_ANCHOR_RE = re.compile(
    r'<a\b[^>]*href="([^"]*(?:jparea/|searchVacant)\?[^"]*\bf_chu=[^"]*)"'
    r'[^>]*>(.*?)</a>', re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")


def _codes_from(query):
    q = query.replace("&amp;", "&")
    codes = {}
    for key in ("f_chu", "f_shou", "f_sai"):
        mm = re.search(r"[?&]%s=([A-Za-z_0-9]*)" % key, q)
        codes[key] = mm.group(1) if mm else ""
    return codes


def _depth(c):
    return sum(1 for k in ("f_chu", "f_shou", "f_sai") if c[k])


def child_areas(html, parent):
    """From a jparea area-picker page, return the next drill-down level as a
    list of (label, codes). Only links that stay in the parent's prefecture
    branch and are strictly more specific are kept, so recursion always
    descends and never wanders into a different prefecture."""
    out, seen = [], set()
    pdepth = _depth(parent)
    for m in AREA_ANCHOR_RE.finditer(html):
        codes = _codes_from(m.group(1))
        if not codes["f_chu"]:
            continue
        # must stay in the same branch as the parent
        if codes["f_chu"] != parent["f_chu"]:
            continue
        if parent["f_shou"] and codes["f_shou"] != parent["f_shou"]:
            continue
        if _depth(codes) <= pdepth:      # not strictly deeper -> skip
            continue
        sig = (codes["f_chu"], codes["f_shou"], codes["f_sai"])
        if sig in seen:
            continue
        seen.add(sig)
        label = htmlmod.unescape(TAG_RE.sub("", m.group(2))).strip()
        out.append((label or sig[-1] or sig[-2], codes))
    return out


NAME_RE = re.compile(r'id="(\d+)_link"[^>]*>([^<]+)</a>')
PRICE_RE = re.compile(r'class="ndPrice"[^>]*>合計<strong>([\d,]+)</strong>円')
RATING_RE = re.compile(r'<strong>([\d.]+)</strong>（([\d,]+)件）')
ACCESS_RE = re.compile(r'class="htlAccess">\s*<span>([^<]+)</span>')


def parse_hotels(html):
    """Split the page into per-hotel blocks (name anchor -> next name anchor)
    and extract fields from each block, so long sponsor blurbs never push the
    price out of range."""
    matches = list(NAME_RE.finditer(html))
    hotels = []
    for i, m in enumerate(matches):
        hid = m.group(1)
        name = htmlmod.unescape(m.group(2)).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        block = html[m.start():end]
        # cheapest total across all plans in the block
        prices = [int(p.replace(",", "")) for p in PRICE_RE.findall(block)]
        rating = RATING_RE.search(block)
        access = ACCESS_RE.search(block)
        hotels.append({
            "id": hid,
            "name": name,
            "price": min(prices) if prices else None,
            "rating": float(rating.group(1)) if rating else None,
            "reviews": int(rating.group(2).replace(",", "")) if rating else None,
            "access": htmlmod.unescape(access.group(1)).strip() if access else None,
            "url": f"https://travel.rakuten.co.jp/HOTEL/{hid}/{hid}.html",
        })
    return hotels


def is_leaf(final_url):
    """A hotel list stays on /ds/vacant/searchVacant; a broad area redirects
    to /jparea/ (the area picker)."""
    return "/jparea/" not in final_url


def collect(codes, opts, label, budget, visited, notes, matched=True):
    """Recursively resolve an area to a flat list of hotels.

    Directly-searchable areas (Kyoto, Osaka) return in one fetch. Broad metros
    (Tokyo, Hokkaido) redirect to the area picker; we drill into each child area
    and aggregate. `budget` is a 1-item list acting as a mutable leaf-fetch cap.

    `matched` tracks the --subarea filter: when a subarea keyword is set we only
    keep leaves under a drill-down branch whose label matched the keyword.
    """
    sig = (codes["f_chu"], codes.get("f_shou", ""), codes.get("f_sai", ""))
    if sig in visited or budget[0] <= 0:
        return []
    visited.add(sig)

    url = build_url(codes, opts["checkin"], opts["checkout"], opts["adults"],
                    opts["rooms"], opts["sort"], 30, 1)
    try:
        html, final = fetch(url)
    except Exception as e:
        notes.append(f"fetch failed for {label}: {e}")
        return []

    if is_leaf(final):
        if opts.get("subarea") and not matched:
            return []          # reached a hotel list outside the wanted subarea
        budget[0] -= 1
        hotels = parse_hotels(html)
        for h in hotels:
            h["area"] = label
        # extra pages for this leaf
        for page in range(2, opts["pages"] + 1):
            if len(hotels) % 30 != 0:      # previous page wasn't full -> no more
                break
            purl = build_url(codes, opts["checkin"], opts["checkout"],
                             opts["adults"], opts["rooms"], opts["sort"], 30,
                             page)
            try:
                phtml, _ = fetch(purl)
            except Exception:
                break
            more = parse_hotels(phtml)
            for h in more:
                h["area"] = label
            hotels.extend(more)
            if len(more) < 30:
                break
        return hotels

    # area picker -> drill into children
    kids = child_areas(html, codes)
    if not kids:
        notes.append(f"no sub-areas found for {label}")
        return []

    sub = opts.get("subarea")
    if sub and not matched:
        # only descend branches whose label matches the wanted subarea; if none
        # match at this level, descend all to look for a match deeper down
        hits = [(l, c) for l, c in kids if sub.lower() in l.lower()]
        if hits:
            kids = [(l, c, True) for l, c in hits]
        else:
            kids = [(l, c, False) for l, c in kids]
    else:
        kids = [(l, c, matched) for l, c in kids]

    hotels = []
    for clabel, ccodes, cmatched in kids:
        if budget[0] <= 0:
            notes.append(f"stopped early (leaf budget reached) before: {clabel}")
            break
        hotels.extend(collect(ccodes, opts, clabel, budget, visited, notes,
                              cmatched))
    return hotels


SORT_KEY = {
    "price": lambda h: (h["price"] is None, h["price"] or 0),
    "price-desc": lambda h: (h["price"] is None, -(h["price"] or 0)),
    "rating": lambda h: (-(h["rating"] or 0), -(h["reviews"] or 0)),
    "size": None, "recommended": None,
}


def main():
    ap = argparse.ArgumentParser(
        description="Find hotels in Japan on Rakuten Travel (no API key required).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Areas: pass a romaji code (kyoto, osaka, tokyo, ...), an English "
               "alias (kobe, nagoya, sapporo), or a Japanese prefecture (京都府).\n"
               "Run with --list-areas to see every prefecture code.")
    ap.add_argument("area", nargs="?", help="prefecture / area to search")
    ap.add_argument("--checkin", type=parse_date, help="check-in date YYYY-MM-DD")
    ap.add_argument("--checkout", type=parse_date, help="check-out date YYYY-MM-DD")
    ap.add_argument("--nights", type=int, help="nights (alternative to --checkout)")
    ap.add_argument("--adults", type=int, default=2, help="adults total (default 2)")
    ap.add_argument("--rooms", type=int, default=1, help="rooms (default 1)")
    ap.add_argument("--sort", choices=SORTS, default="recommended",
                    help="sort order (default recommended)")
    ap.add_argument("--min-price", type=int,
                    help="min total price JPY (filters fetched results; "
                         "widen with --pages)")
    ap.add_argument("--max-price", type=int,
                    help="max total price JPY (filters fetched results; "
                         "widen with --pages)")
    ap.add_argument("--pages", type=int, default=1,
                    help="result pages per area (30 hotels/page)")
    ap.add_argument("--max-areas", type=int, default=20,
                    help="max sub-areas to fetch for broad metros like Tokyo "
                         "(default 20)")
    ap.add_argument("--subarea",
                    help="narrow a big prefecture to matching sub-areas only, "
                         "e.g. --subarea 函館 (matches drill-down area labels)")
    ap.add_argument("--filter",
                    help="keep only hotels whose name/access/area contains this "
                         "text, e.g. --filter 温泉 (onsen)")
    ap.add_argument("--limit", type=int, help="cap number of hotels shown")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--list-areas", action="store_true", help="print area codes and exit")
    args = ap.parse_args()

    if args.list_areas:
        for jp, code in PREFECTURES.items():
            print(f"{code:<12} {jp}")
        return 0

    if not args.area:
        ap.error("area is required (e.g. 'kyoto'). See --list-areas.")
    if not args.checkin:
        ap.error("--checkin is required (YYYY-MM-DD)")

    code, jp = resolve_area(args.area)
    if not code:
        print(f"Unknown area '{args.area}'. Try --list-areas.", file=sys.stderr)
        return 2

    if args.checkout:
        checkout = args.checkout
    elif args.nights:
        checkout = args.checkin + dt.timedelta(days=args.nights)
    else:
        checkout = args.checkin + dt.timedelta(days=1)
    if checkout <= args.checkin:
        print("checkout must be after checkin", file=sys.stderr)
        return 2

    opts = {
        "checkin": args.checkin, "checkout": checkout,
        "adults": args.adults, "rooms": args.rooms, "sort": args.sort,
        "pages": args.pages, "subarea": args.subarea,
    }
    notes = []
    budget = [args.max_areas]
    hotels = collect({"f_chu": code, "f_shou": "", "f_sai": ""},
                     opts, jp, budget, set(), notes,
                     matched=args.subarea is None)

    # de-dup by id, preserve first occurrence
    seen, unique = set(), []
    for h in hotels:
        if h["id"] not in seen:
            seen.add(h["id"])
            unique.append(h)
    hotels = unique

    # price filter on the parsed total (predictable; server params are flaky)
    if args.min_price is not None:
        hotels = [h for h in hotels
                  if h["price"] is not None and h["price"] >= args.min_price]
    if args.max_price is not None:
        hotels = [h for h in hotels
                  if h["price"] is not None and h["price"] <= args.max_price]

    # keyword filter on name / access / area (e.g. onsen)
    if args.filter:
        needle = args.filter.lower()
        hotels = [h for h in hotels
                  if needle in " ".join(str(h.get(k) or "")
                                        for k in ("name", "access", "area")).lower()]

    # when we aggregated across many sub-areas, re-sort globally
    keyfn = SORT_KEY.get(args.sort)
    if keyfn:
        hotels.sort(key=keyfn)

    if args.limit:
        hotels = hotels[:args.limit]

    nights = (checkout - args.checkin).days
    meta = {
        "area": jp, "code": code,
        "checkin": args.checkin.isoformat(), "checkout": checkout.isoformat(),
        "nights": nights, "adults": args.adults, "rooms": args.rooms,
        "sort": args.sort, "count": len(hotels),
    }

    if args.json:
        print(json.dumps({"query": meta, "notes": notes, "hotels": hotels},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"\n{jp}  {args.checkin}  →  {checkout}  ({nights} night(s), "
          f"{args.adults} adult(s), {args.rooms} room(s))  sort={args.sort}")
    areas = {h.get("area") for h in hotels if h.get("area")}
    if len(areas) > 1:
        print(f"aggregated across {len(areas)} sub-areas")
    print(f"{len(hotels)} hotels\n")
    for i, h in enumerate(hotels, 1):
        price = f"¥{h['price']:,}" if h["price"] else "sold out"
        rating = (f"★{h['rating']} ({h['reviews']:,})"
                  if h["rating"] else "no reviews")
        area = f"  [{h['area']}]" if len(areas) > 1 and h.get("area") else ""
        print(f"{i:>2}. {h['name']}{area}")
        print(f"    {price:<12}  {rating:<18}  {h['url']}")
        if h["access"]:
            print(f"    {h['access']}")
        print()
    for n in notes:
        print(f"note: {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
