#!/usr/bin/env python3
"""Fetch a1zhang's last-day tweets + replies and the originals they replied to.

Uses twitter-api45 on RapidAPI (same service tensor-ai uses).
Endpoints: timeline.php, replies.php, tweet.php (parent lookup).
"""
import os, sys, json, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

API_KEY = os.environ["RAPID_API_KEY"]
HOST = "twitter-api45.p.rapidapi.com"
TARGET = "a1zhang"
LOOKBACK_HOURS = 24
OUTDIR = os.path.dirname(os.path.abspath(__file__))

def api(path, **params):
    qs = urllib.parse.urlencode(params)
    url = f"https://{HOST}/{path}?{qs}"
    req = urllib.request.Request(url, headers={
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST,
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {}
        except Exception as e:
            sys.stderr.write(f"  retry {attempt+1} on {path} {params}: {e}\n")
            time.sleep(2)
    return {}

def parse_dt(s):
    # "Fri May 29 02:21:33 +0000 2026"
    try:
        return datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
    except Exception:
        return None

now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=LOOKBACK_HOURS)
print(f"Now: {now.isoformat()}  Cutoff: {cutoff.isoformat()}", file=sys.stderr)

# 1. Timeline (own tweets)
print("Fetching timeline...", file=sys.stderr)
timeline = api("timeline.php", screenname=TARGET)
own_tweets = timeline.get("timeline", []) or []
pinned = timeline.get("pinned")
user = timeline.get("user", {})

# 2. Replies (own replies + context)
print("Fetching replies...", file=sys.stderr)
replies_resp = api("replies.php", screenname=TARGET)
reply_items = replies_resp.get("timeline", []) or []

# Split a1zhang's own content vs others' context
def author_handle(t):
    return ((t.get("author") or {}).get("screen_name") or "").lower()

own_replies = [t for t in reply_items if author_handle(t) == TARGET.lower()]
context_items = [t for t in reply_items if author_handle(t) != TARGET.lower() and author_handle(t)]

# 3. Filter to last day
def recent(t):
    dt = parse_dt(t.get("created_at", ""))
    return dt is not None and dt >= cutoff

own_tweets_recent = [t for t in own_tweets if recent(t)]
own_replies_recent = [t for t in own_replies if recent(t)]

# 4. Resolve parent tweets (the things a1zhang replied to)
parent_ids = []
seen = set()
for t in own_replies_recent:
    pid = t.get("in_reply_to_status_id_str")
    if pid and pid not in seen:
        seen.add(pid)
        parent_ids.append(pid)

print(f"Resolving {len(parent_ids)} parent tweets...", file=sys.stderr)
parents = {}
for pid in parent_ids:
    data = api("tweet.php", id=pid)
    if data and data.get("text"):
        parents[pid] = data
    time.sleep(0.4)

result = {
    "fetched_at": now.isoformat(),
    "cutoff": cutoff.isoformat(),
    "target": TARGET,
    "user": user,
    "pinned": pinned,
    "own_tweets_recent": own_tweets_recent,
    "own_tweets_all": own_tweets,
    "own_replies_recent": own_replies_recent,
    "own_replies_all": own_replies,
    "context_items": context_items,
    "parents": parents,
}

with open(os.path.join(OUTDIR, "raw.json"), "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(json.dumps({
    "own_tweets_recent": len(own_tweets_recent),
    "own_tweets_total": len(own_tweets),
    "own_replies_recent": len(own_replies_recent),
    "own_replies_total": len(own_replies),
    "context_items": len(context_items),
    "parents_resolved": len(parents),
}, indent=2))
