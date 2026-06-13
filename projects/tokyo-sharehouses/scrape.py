#!/usr/bin/env python3
"""Scrape X-House Tokyo sharehouse listings, geocode them, dump JSON.

Pipeline (all reverse-engineered from the public site, no key needed):
  1. GET the list page -> session cookie + CSRF token
  2. POST /api/cn-h/ajax/load_more_properties paginated (take/skip) with
     form_datas[city]=<38 Tokyo ward codes> -> HTML cards
  3. parse cards -> id, name, rent, stations, campaigns, available, url
  4. GET each detail page -> address from the Google Maps iframe q= param
  5. geocode address via GSI (free, no key) -> lat/lng
"""
import json, re, time, urllib.parse, html as H
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, http.cookiejar

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
LIST_URL = "https://x-house.co.jp/en/tokyo/city/?vacant_room_flg=1"
API_URL  = "https://x-house.co.jp/api/cn-h/ajax/load_more_properties"
GSI      = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
CITY = ("68,70,72,67,60,77,69,79,83,62,66,59,63,71,75,85,74,78,84,65,64,76,"
        "88,90,98,96,93,80,100,122,124,125,129,130,133,134,136,139")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def _do(req, timeout):
    last = None
    for attempt in range(5):
        try:
            with opener.open(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))  # backoff on reset/timeout
    raise last

def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    return _do(req, 30)

def post(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body,
        headers={"User-Agent": UA, "X-Requested-With": "XMLHttpRequest", **(headers or {})})
    return _do(req, 60)

# ---- 1. session + csrf -------------------------------------------------
print("Fetching list page for session + CSRF ...")
page = get(LIST_URL)
csrf = re.search(r'name="csrf-token" content="([^"]+)"', page).group(1)
print("CSRF:", csrf[:12], "...")

# ---- 2. paginate the API ----------------------------------------------
def fetch_page(skip, first):
    data = {
        "take": 30, "skip": skip, "is_first_load": "true" if first else "false",
        "language": "en", "url_language": "en",
        "form_datas[vacant_room_flg]": "1",
        "form_datas[sort]": "recommend",
        "form_datas[city]": CITY,
    }
    return json.loads(post(API_URL, data, {"X-CSRF-TOKEN": csrf}))

first = fetch_page(0, True)
total = int(first["property_count"])
print(f"Total Tokyo properties: {total}")
all_html = [first["html"]]
for skip in range(30, total + 30, 30):
    try:
        all_html.append(fetch_page(skip, False)["html"])
    except Exception as e:
        print("page skip", skip, "err", e)
    time.sleep(0.3)
big = "\n".join(all_html)

# ---- 3. parse cards ----------------------------------------------------
def strip(s): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

cards = re.split(r'<article class="c-property-card">', big)[1:]
listings, seen = [], set()
for c in cards:
    m = re.search(r'<a href="(https://x-house\.co\.jp/en/[^"]+/)"', c)
    if not m: continue
    url = m.group(1)
    pid_m = re.search(r'property_id=(\d+)', c) or re.search(r'xross-(\d+)', url)
    pid = pid_m.group(1) if pid_m else url.rstrip("/").split("/")[-1]
    if pid in seen: continue
    seen.add(pid)
    name = strip(re.search(r'<h2 class="ttl"[^>]*>(.*?)</h2>', c, re.S).group(1)) \
           if re.search(r'<h2 class="ttl"', c) else ""
    stations = [f"{strip(a)} {strip(b)}" for a, b in re.findall(r'<span class="station-head">(.*?)</span>(.*?)</span>', c, re.S)]
    campaigns = [strip(x) for x in re.findall(r'<li><span class="tag">(.*?)</span></li>', c, re.S)]
    # real monthly rents live in <span class="num">NN,NNN<span class="unit"> yen</span></span>,
    # one row per available room type. The leading "20,000 yen off" is a campaign, not rent.
    room_rents = [int(x.replace(",", "")) for x in
                  re.findall(r'<span class="num">\s*([\d,]+)\s*<span class="unit">', c)]
    rent = min(room_rents) if room_rents else None
    avail_m = re.search(r'(\d{4}-\d{2}-\d{2})', c)
    listings.append({
        "id": pid, "name": name, "url": url, "rent": rent,
        "rent_max": max(room_rents) if room_rents else None,
        "room_count": len(room_rents),
        "stations": stations, "campaigns": campaigns,
        "available": avail_m.group(1) if avail_m else None,
    })
print(f"Parsed {len(listings)} unique listings")

# ---- 4. detail page -> address ----------------------------------------
def _pairs(html):
    """All <th>label</th><td>value</td> pairs from the detail tables, cleaned."""
    out = {}
    for th, td in re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', html, re.S):
        k, v = strip(th), strip(td)
        if k and k not in out:
            out[k] = v
    return out

def fetch_address(l):
    try:
        html = get(l["url"])
        m = re.search(r'maps\.google[^"]*?[?&]q=([^&"]+)', html)
        if m:
            l["address"] = urllib.parse.unquote(m.group(1))
        zipm = re.search(r'〒\s*([\d\-]+)', html)
        if zipm: l["zip"] = zipm.group(1)

        p = _pairs(html)
        # floor area, e.g. "7.5～19.0㎡" -> min/max
        fa = p.get("Floor area", "")
        areas = [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*㎡', fa)] \
                or [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)', fa)]
        if areas:
            l["area_min"], l["area_max"] = min(areas), max(areas)
        # room types -> list of normalized tokens
        rt = p.get("Room type", "")
        types = []
        for token, label in [("Dormitory", "Dormitory"), ("Private room", "Private room"),
                             ("Furnished apartment", "Apartment"), ("Apartment", "Apartment")]:
            if token.lower() in rt.lower() and label not in types:
                types.append(label)
        if types: l["room_types"] = types
        l["property_type"] = p.get("Property type", "")
        cap = re.search(r'(\d+)', p.get("Capacity", ""))
        if cap: l["capacity"] = int(cap.group(1))
        l["structure"] = p.get("Structure", "")
        l["age_limit"] = p.get("Age limit", "")
        l["smoking"] = p.get("About smoking", "")
        # gender restriction if present anywhere on page
        if re.search(r'women only|female only|for women', html, re.I):
            l["gender"] = "Women only"
        elif re.search(r'men only|male only|for men', html, re.I):
            l["gender"] = "Men only"
        else:
            l["gender"] = "Mixed"
    except Exception as e:
        l["address_err"] = str(e)
    return l

print("Fetching detail pages for addresses ...")
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(fetch_address, l): l for l in listings}
    done = 0
    for f in as_completed(futs):
        done += 1
        if done % 25 == 0: print(f"  {done}/{len(listings)} detail pages")

# ---- 5. geocode --------------------------------------------------------
geo_cache = {}
def _gsi_one(q):
    try:
        r = json.loads(get(GSI + urllib.parse.quote(q)))
        if r:
            lng, lat = r[0]["geometry"]["coordinates"]
            return (lat, lng)
    except Exception:
        pass
    return None

def geocode(addr):
    if not addr: return None
    if addr in geo_cache: return geo_cache[addr]
    queries = [addr]
    # fallbacks: drop trailing building number, then trailing block, for coarser match
    trimmed = re.sub(r'[-ー\d\s]+$', '', addr)
    if trimmed and trimmed != addr:
        queries.append(trimmed)
    for q in queries:
        c = _gsi_one(q)
        if c:
            geo_cache[addr] = c
            return c
    geo_cache[addr] = None
    return None

print("Geocoding addresses (GSI) ...")
def add_coords(l):
    c = geocode(l.get("address"))
    if c: l["lat"], l["lng"] = c
    return l
with ThreadPoolExecutor(max_workers=6) as ex:
    list(ex.map(add_coords, listings))

geocoded = sum(1 for l in listings if "lat" in l)
print(f"Geocoded {geocoded}/{len(listings)}")

out = "/Users/ray/Desktop/ray-os/projects/tokyo-sharehouses/listings.json"
json.dump(listings, open(out, "w"), ensure_ascii=False, indent=2)
print("Wrote", out)
