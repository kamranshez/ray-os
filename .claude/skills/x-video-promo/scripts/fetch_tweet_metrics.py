#!/usr/bin/env python3
"""Pull engagement for one X post and ground it against the author's own recent
posts, so "is it looking good" has a baseline. Raw like counts mean nothing
without the account's own distribution.

Usage:
    python3 fetch_tweet_metrics.py <tweet-url-or-id> [--author screenname]

The RapidAPI key is read from $RAPIDAPI_KEY or ~/.rapidapi_key (twitter-api45
host, the same key the x-thread-miner skill uses). If --author is given, the
script also pulls that user's recent timeline to compute where this post ranks.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HOST = "twitter-api45.p.rapidapi.com"


def load_key():
    key = os.environ.get("RAPIDAPI_KEY")
    if key:
        return key.strip()
    path = os.path.expanduser("~/.rapidapi_key")
    if os.path.exists(path):
        return open(path).read().strip()
    sys.exit("No RapidAPI key. Put it in ~/.rapidapi_key or set $RAPIDAPI_KEY.")


def get(path, params, key):
    url = f"https://{HOST}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def to_int(x):
    try:
        return int(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return 0


def parse_id(s):
    m = re.search(r"status/(\d+)", s)
    if m:
        return m.group(1)
    if s.isdigit():
        return s
    sys.exit(f"Could not parse a tweet id from: {s}")


# field names vary between endpoints; check several
def metric(obj, *names):
    for n in names:
        if n in obj and obj[n] not in (None, ""):
            return to_int(obj[n])
    return 0


def pct_rank(value, pool):
    """Percentile of value within pool (0-100)."""
    if not pool:
        return None
    below = sum(1 for v in pool if v < value)
    return round(100 * below / len(pool))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tweet", help="tweet URL or id")
    ap.add_argument("--author", help="screen name, to compute a baseline")
    ap.add_argument("--baseline-n", type=int, default=40,
                    help="how many recent posts to sample for the baseline")
    args = ap.parse_args()
    key = load_key()
    tid = parse_id(args.tweet)

    t = get("tweet.php", {"id": tid}, key)
    likes = metric(t, "likes", "favorites", "favorite_count")
    rts = metric(t, "retweets", "retweet_count")
    replies = metric(t, "replies", "reply_count")
    quotes = metric(t, "quotes", "quote_count")
    views = metric(t, "views", "view_count")
    bms = metric(t, "bookmarks", "bookmark_count")
    text = (t.get("text") or t.get("display_text") or "").strip()

    print("=" * 60)
    print(f"POST {tid}")
    if text:
        print(text[:280])
    print("-" * 60)
    print(f"likes     {likes:>8}")
    print(f"reposts   {rts:>8}")
    print(f"replies   {replies:>8}")
    print(f"quotes    {quotes:>8}")
    print(f"bookmarks {bms:>8}")
    print(f"views     {views:>8}")
    if views:
        print(f"like rate {100*likes/views:>7.2f}%  (likes/views)")
        print(f"save rate {100*bms/views:>7.2f}%  (bookmarks/views, the truest 'worked' signal)")

    result = {
        "tweet_id": tid, "text": text, "likes": likes, "reposts": rts,
        "replies": replies, "quotes": quotes, "bookmarks": bms, "views": views,
    }

    if args.author:
        author = args.author.lstrip("@")
        likes_pool, view_pool, bm_pool = [], [], []
        cursor = None
        seen = set()
        while len(likes_pool) < args.baseline_n:
            params = {"screenname": author}
            if cursor:
                params["cursor"] = cursor
            try:
                d = get("timeline.php", params, key)
            except Exception as e:  # noqa: BLE001
                print(f"\n(baseline fetch stopped: {e})")
                break
            tl = d.get("timeline", [])
            if not tl:
                break
            for p in tl:
                pid = p.get("tweet_id")
                if pid in seen or pid == tid:
                    continue
                seen.add(pid)
                # original posts only: skip replies to other people
                irs = p.get("in_reply_to_screen_name") or ""
                if irs and irs.lstrip("@").lower() != author.lower():
                    continue
                likes_pool.append(to_int(p.get("favorites")))
                view_pool.append(to_int(p.get("views")))
                bm_pool.append(to_int(p.get("bookmarks")))
            cursor = d.get("next_cursor") or ""
            if not cursor:
                break
            time.sleep(0.7)

        if likes_pool:
            srt = sorted(likes_pool)
            median = srt[len(srt) // 2]
            p75 = srt[int(len(srt) * 0.75)]
            rank = pct_rank(likes, likes_pool)
            print("-" * 60)
            print(f"baseline: {len(likes_pool)} recent original posts by @{author}")
            print(f"  their median likes   {median:>8}")
            print(f"  their top-quartile   {p75:>8}")
            print(f"  THIS post's likes    {likes:>8}  ({rank}th percentile)")
            if bm_pool:
                bm_srt = sorted(bm_pool)
                bm_rank = pct_rank(bms, bm_pool)
                print(f"  bookmark percentile  {bm_rank:>7}th")
            verdict = (
                "LANDED WELL (top quartile)" if likes >= p75 else
                "FINE (around median)" if likes >= median else
                "UNDERPERFORMED (below his median)"
            )
            print(f"  verdict: {verdict}")
            result["baseline"] = {
                "n": len(likes_pool), "median_likes": median,
                "p75_likes": p75, "likes_percentile": rank, "verdict": verdict,
            }
        else:
            print("\n(no baseline posts gathered)")

    print("=" * 60)
    print("JSON:", json.dumps(result))


if __name__ == "__main__":
    main()
