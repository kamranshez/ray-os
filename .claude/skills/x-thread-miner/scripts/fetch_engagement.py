#!/usr/bin/env python3
"""
Fetch replies and/or quote tweets for one or more tweets via the RapidAPI
twitter-api45 API, normalize them, and surface the most substantive engagement
so a model can synthesize insights without loading hundreds of raw entries.

The script does the noisy part (paginated fetching + filtering + ranking).
The model does the smart part (reading surfaced.md and writing the synthesis).

Usage:
  python fetch_engagement.py --tweet <url-or-id> [--tweet ...] \
      --mode {replies,quotes,both} \
      [--deep N] [--max-pages N] [--out DIR]

Key resolution order: $RAPIDAPI_KEY env var, then ~/.rapidapi_key file.
"""
import argparse, glob, json, os, re, sys, time, urllib.parse, urllib.request

HOST = "twitter-api45.p.rapidapi.com"


def load_key():
    k = os.environ.get("RAPIDAPI_KEY") or os.environ.get("RAPIDAPI_TWITTER_KEY")
    if k:
        return k.strip()
    for p in ("~/.rapidapi_key", "~/.config/rapidapi/key"):
        fp = os.path.expanduser(p)
        if os.path.exists(fp):
            return open(fp).read().strip()
    sys.exit("No API key found. Set $RAPIDAPI_KEY or create ~/.rapidapi_key")


def tid_from(s):
    """Accept a full tweet URL or a bare id."""
    m = re.search(r"status/(\d+)", s) or re.search(r"(\d{8,})", s)
    return m.group(1) if m else s.strip()


def call(path, params, key):
    url = f"https://{HOST}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key,
                 "Content-Type": "application/json"},
    )
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception:
            time.sleep(2)
    return {}


def norm(t):
    ui = t.get("user_info") or t.get("author") or {}
    return {
        "tweet_id": t.get("tweet_id") or t.get("id"),
        "screen_name": ui.get("screen_name"),
        "name": ui.get("name"),
        "followers": ui.get("followers_count") or ui.get("followers") or 0,
        "verified": ui.get("verified"),
        "created_at": t.get("created_at"),
        "text": (t.get("text") or "").strip(),
        "favorites": t.get("favorites") or t.get("likes"),
        "replies": t.get("replies"),
        "retweets": t.get("retweets"),
        "quotes": t.get("quotes"),
        "views": t.get("views"),
        "in_reply_to": t.get("in_reply_to_screen_name"),
    }


def paginate(path, base_params, key, max_pages):
    rows, cursor, seen = [], None, set()
    for _ in range(max_pages):
        params = dict(base_params)
        if cursor:
            params["cursor"] = cursor
        d = call(path, params, key)
        tl = d.get("timeline", []) if isinstance(d, dict) else []
        rows += tl
        cursor = d.get("next_cursor")
        if not cursor or cursor in seen or not tl:
            break
        seen.add(cursor)
        time.sleep(0.7)
    return rows


def fetch_replies(tid, key, max_pages):
    raw = paginate("latest_replies.php", {"id": tid}, key, max_pages)
    return [norm(t) for t in raw if (t.get("text") or "").strip()]


def fetch_quotes(tid, key, max_pages):
    raw = paginate("search.php",
                   {"query": f"quoted_tweet_id:{tid}", "search_type": "Latest"},
                   key, max_pages)
    return [norm(t) for t in raw if (t.get("text") or "").strip()]


def dedup(rows):
    seen, out = set(), []
    for r in rows:
        k = r.get("tweet_id")
        if k and k not in seen:
            seen.add(k)
            out.append(r)
    return out


def clean(t):
    return (t or "").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tweet", action="append", required=True,
                    help="Tweet URL or id. Repeatable.")
    ap.add_argument("--mode", choices=["replies", "quotes", "both"], default="both")
    ap.add_argument("--deep", type=int, default=0,
                    help="Also fetch replies under the top N quote tweets by reach.")
    ap.add_argument("--max-pages", type=int, default=15)
    ap.add_argument("--out", default="./x-mining")
    args = ap.parse_args()

    key = load_key()
    data_dir = os.path.join(args.out, "data")
    deep_dir = os.path.join(data_dir, "quote_replies")
    os.makedirs(data_dir, exist_ok=True)

    summary, all_rows = {}, []
    for raw_tweet in args.tweet:
        tid = tid_from(raw_tweet)
        info = call("tweet.php", {"id": tid}, key)
        author = (info.get("author") or {}).get("screen_name") or tid
        label = f"{author}_{tid}"

        replies = fetch_replies(tid, key, args.max_pages) if args.mode in ("replies", "both") else []
        quotes = fetch_quotes(tid, key, args.max_pages) if args.mode in ("quotes", "both") else []
        replies, quotes = dedup(replies), dedup(quotes)

        json.dump({"anchor": {"id": tid, "author": author,
                              "text": clean(info.get("text")),
                              "likes": info.get("likes"), "replies_count": info.get("replies"),
                              "quotes_count": info.get("quotes"), "views": info.get("views")},
                   "replies": replies, "quotes": quotes},
                  open(os.path.join(data_dir, f"{label}.json"), "w"), indent=1)

        for r in replies:
            r["_src"] = label; r["_kind"] = "reply"; r["_under"] = author
        for q in quotes:
            q["_src"] = label; q["_kind"] = "quote"; q["_under"] = author
        all_rows += replies + quotes

        # Deep layer: replies under the highest-reach quote tweets.
        deep_count = 0
        if args.deep > 0 and quotes:
            os.makedirs(deep_dir, exist_ok=True)
            cands = [q for q in quotes if (q.get("replies") or 0) > 0 and (q.get("followers") or 0) > 1000]
            cands.sort(key=lambda q: -(q.get("followers") or 0))
            for q in cands[: args.deep]:
                qid, qsn = q["tweet_id"], q.get("screen_name") or q["tweet_id"]
                sub = fetch_replies(qid, key, max_pages=2)
                json.dump({"quote": q, "replies": sub},
                          open(os.path.join(deep_dir, f"{qsn}_{qid}.json"), "w"), indent=1)
                for r in sub:
                    r["_src"] = label; r["_kind"] = "deep-reply"; r["_under"] = qsn
                all_rows += sub
                deep_count += len(sub)
                time.sleep(0.7)

        summary[label] = {"tweet_id": tid, "author": author,
                          "n_replies": len(replies), "n_quotes": len(quotes),
                          "n_deep_replies": deep_count}

    all_rows = dedup(all_rows)
    json.dump(summary, open(os.path.join(args.out, "summary.json"), "w"), indent=1)

    # surfaced.md — top substantive tweets by author reach, the model's reading surface.
    sub = [r for r in all_rows if len(clean(r.get("text"))) > 70]
    sub.sort(key=lambda r: -(r.get("followers") or 0))
    top_authors = sub[:8]
    lines = ["# Surfaced engagement (read this to synthesize)\n"]
    total = sum(s["n_replies"] + s["n_quotes"] + s["n_deep_replies"] for s in summary.values())
    lines.append(f"Anchors: {len(summary)} | total tweets gathered: {total} | substantive (>70 chars): {len(sub)}\n")
    lines.append("Highest-reach quote authors give a sense of amplification:")
    seen_a = set()
    for r in top_authors:
        if r["screen_name"] in seen_a:
            continue
        seen_a.add(r["screen_name"])
        lines.append(f"- @{r['screen_name']} ({r['followers']}f)")
    lines.append("\n## Top substantive tweets by reach\n")
    shown = set()
    for r in sub[:90]:
        k = (r.get("screen_name"), clean(r.get("text"))[:40])
        if k in shown:
            continue
        shown.add(k)
        lines.append(f"- [{r['_kind']} | under @{r['_under']}] @{r['screen_name']} ({r['followers']}f): {clean(r['text'])[:260]}")
    open(os.path.join(args.out, "surfaced.md"), "w").write("\n".join(lines))

    print(json.dumps(summary, indent=1))
    print(f"\nGathered {total} tweets. Read {os.path.join(args.out, 'surfaced.md')} to synthesize.")
    print(f"Raw normalized data in {data_dir}/")


if __name__ == "__main__":
    main()
