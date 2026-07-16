#!/usr/bin/env python3
"""
Search X (Twitter) by freeform query via the RapidAPI twitter-api45 API,
paginate, dedup, rank by a composite engagement+reach score, and surface the
top tweets so a model can synthesize insights without reading hundreds of raw
entries.

The script does the noisy part (paginated fetching, dedup, ranking, surfacing).
The model does the smart part (reading surfaced.md and writing the synthesis).

Usage:
  python search_x.py --query "<X-search syntax>" \
      [--query "<another>"] \
      [--search-type Top|Latest|People|Photos|Videos] \
      [--max-pages N] [--top-n N] [--out DIR] \
      [--min-faves N] [--lang en] [--since YYYY-MM-DD] [--exclude-replies]

Convenience flags (--min-faves, --lang, --since, --exclude-replies) just inject
the equivalent X advanced-search operators into the query string. Power users
can pass everything via raw --query syntax instead.

Key resolution order: $RAPIDAPI_KEY env var, then ~/.rapidapi_key file.

Exit codes:
  0 — success (including the legitimate "no useful results" case; check
      meta.json.total and surfaced.md to see what happened).
  1 — usage error (bad CLI args).
  2 — auth failure (RapidAPI key missing, invalid, or unsubscribed).
  3 — transport / unknown failure (all retries exhausted).

The "no useful results" exit-0 contract exists so calling workflows can drop the
output without erroring out. Reserve non-zero codes for genuine breakage.
"""
import argparse
import datetime as _dt
import email.utils
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = "twitter-api45.p.rapidapi.com"
ALLOWED_SEARCH_TYPES = {"Top", "Latest", "People", "Photos", "Videos"}


# ----- key loading (mirrors x-thread-miner) -----

def load_key():
    k = os.environ.get("RAPIDAPI_KEY") or os.environ.get("RAPIDAPI_TWITTER_KEY")
    if k:
        return k.strip()
    for p in ("~/.rapidapi_key", "~/.config/rapidapi/key"):
        fp = os.path.expanduser(p)
        if os.path.exists(fp):
            return open(fp).read().strip()
    sys.stderr.write(
        "x-search: no API key found. Set $RAPIDAPI_KEY or create ~/.rapidapi_key\n"
    )
    sys.exit(2)


# ----- network call with retries + auth detection -----

class AuthError(RuntimeError):
    pass


def call(path, params, key, max_retries=3):
    """
    GET twitter-api45/<path> with params. Returns parsed JSON dict on success.

    Raises AuthError on HTTP 403 / "not subscribed" envelopes. Returns {} after
    transport retries are exhausted so the caller can decide whether that
    counts as a hard fail or just an empty page.
    """
    url = f"https://{HOST}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "x-rapidapi-host": HOST,
            "x-rapidapi-key": key,
            "Content-Type": "application/json",
        },
    )
    last_err = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                body = json.load(r)
                # Top-level "message" with no "timeline" is the auth-failure envelope.
                if (
                    isinstance(body, dict)
                    and "message" in body
                    and "timeline" not in body
                ):
                    raise AuthError(f"twitter-api45: {body.get('message')}")
                return body
        except AuthError:
            raise
        except urllib.error.HTTPError as e:
            # 403 is the canonical auth/subscription failure.
            if e.code == 403:
                try:
                    body = json.load(e)
                    msg = body.get("message") if isinstance(body, dict) else str(body)
                except Exception:
                    msg = e.reason
                raise AuthError(f"twitter-api45 HTTP 403: {msg}")
            # 429 / 5xx: back off and try again.
            last_err = e
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    if last_err is not None:
        sys.stderr.write(f"x-search: request failed after retries: {last_err}\n")
    return {}


# ----- query string composition -----

def build_query(base, *, min_faves=None, lang=None, since=None, exclude_replies=False):
    """
    Append X advanced-search operators to the user query if convenience flags
    are set. We don't try to deduplicate against operators already in `base`
    because false positives are worse than redundancy here (X tolerates dupes).
    """
    parts = [base.strip()]
    if min_faves is not None and min_faves > 0:
        parts.append(f"min_faves:{int(min_faves)}")
    if lang:
        parts.append(f"lang:{lang}")
    if since:
        # Normalize accidental ISO-with-time to date only.
        parts.append(f"since:{since[:10]}")
    if exclude_replies:
        parts.append("-filter:replies")
    return " ".join(p for p in parts if p)


# ----- pagination loop -----

def paginate(query, search_type, key, max_pages, raw_pages_dir=None):
    """
    Loop /search.php pages until exhaustion or one of the stop conditions
    described in references/endpoints.md fires.

    Returns (rows, exit_reason). `rows` is the concatenated, NOT-yet-deduped
    timeline entries. Exit reason is one of:
      "empty"         — timeline came back empty (no results for this query)
      "exhausted"     — hit max_pages with results still coming
      "no_cursor"     — next_cursor missing or repeating
      "failed_status" — server returned status != "ok"
      "transport"     — call() returned {} after retries
    """
    rows = []
    cursor = None
    seen_cursors = set()
    last_reason = "exhausted"
    for page_idx in range(max_pages):
        params = {"query": query, "search_type": search_type}
        if cursor:
            params["cursor"] = cursor
        d = call("search.php", params, key)

        if not isinstance(d, dict) or not d:
            last_reason = "transport"
            break

        if raw_pages_dir:
            with open(os.path.join(raw_pages_dir, f"page-{page_idx + 1:02d}.json"), "w") as f:
                json.dump(d, f, indent=1)

        status = d.get("status")
        if status and status != "ok":
            last_reason = "failed_status"
            break

        timeline = d.get("timeline") or []
        if not timeline:
            # If this is the very first page, that's "empty"; otherwise we just ran out.
            last_reason = "empty" if page_idx == 0 else "exhausted"
            break

        rows.extend(timeline)
        nc = d.get("next_cursor")
        if not nc or nc in seen_cursors:
            last_reason = "no_cursor"
            break
        seen_cursors.add(nc)
        cursor = nc
        time.sleep(0.7)
    else:
        last_reason = "exhausted"
    return rows, last_reason


# ----- normalization -----

def _int(v, default=0):
    """`views` comes back as a string; favorites/retweets as ints; guard everything."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _parse_created_at(s):
    """Legacy Twitter date: 'Tue Apr 21 05:15:00 +0000 2026'. Returns datetime or None."""
    if not s:
        return None
    try:
        return _dt.datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
    except Exception:
        try:
            return email.utils.parsedate_to_datetime(s)
        except Exception:
            return None


def _is_promoted(entry):
    tid = entry.get("tweet_id") or ""
    return isinstance(tid, str) and tid.startswith("promoted-")


def norm_tweet(t):
    """Normalize a `type: "tweet"` entry into a flat dict we can rank and surface."""
    ui = t.get("user_info") or {}
    quoted = t.get("quoted") or {}
    quoted_author = (quoted.get("author") or {}) if isinstance(quoted, dict) else {}
    media = t.get("media")
    has_video = False
    has_photo = False
    if isinstance(media, dict):
        has_video = bool(media.get("video"))
        has_photo = bool(media.get("photo"))
    elif isinstance(media, list):
        # Rare list shape; flatten naively.
        for item in media:
            if isinstance(item, dict):
                has_video = has_video or "video" in item or item.get("type") == "video"
                has_photo = has_photo or "photo" in item or item.get("type") == "photo"

    return {
        "tweet_id": t.get("tweet_id"),
        "screen_name": t.get("screen_name") or ui.get("screen_name"),
        "name": ui.get("name"),
        "followers": _int(ui.get("followers_count"), 0),
        "verified": bool(ui.get("verified") or ui.get("blue_verified") or ui.get("is_blue_verified")),
        "verified_type": ui.get("verified_type"),
        "created_at": t.get("created_at"),
        "lang": t.get("lang"),
        "text": (t.get("text") or "").strip(),
        "favorites": _int(t.get("favorites")),
        "retweets": _int(t.get("retweets")),
        "replies": _int(t.get("replies")),
        "quotes": _int(t.get("quotes")),
        "views": _int(t.get("views")),
        "bookmarks": _int(t.get("bookmarks")),
        "has_video": has_video,
        "has_photo": has_photo,
        "is_reply": bool(t.get("in_reply_to_screen_name")),
        "in_reply_to": t.get("in_reply_to_screen_name"),
        "quoted_author": quoted_author.get("screen_name"),
        "quoted_text": (quoted.get("text") or "").strip() if isinstance(quoted, dict) else "",
    }


def norm_user(u):
    """Normalize a `type: "user"` entry (only from search_type=People)."""
    return {
        "kind": "user",
        "user_id": u.get("user_id"),
        "screen_name": u.get("screen_name"),
        "name": u.get("name"),
        "followers": _int(u.get("followers_count")),
        "friends": _int(u.get("friends_count")),
        "statuses": _int(u.get("statuses_count")),
        "media_count": _int(u.get("media_count")),
        "verified": bool(u.get("is_blue_verified") or u.get("verified")),
        "verified_type": u.get("verified_type"),
        "description": (u.get("description") or "").strip(),
        "created_at": u.get("created_at"),
        "avatar": u.get("avatar"),
    }


# ----- ranking -----

def score(row):
    """
    Composite engagement+reach score for tweet entries. Log-dampened because
    raw counts span 8+ orders of magnitude on X (a single megastar would
    otherwise drown out every sharp take from a small account).

    See references/endpoints.md §6 for the rationale and tuning notes.
    """
    eng = math.log1p(
        row["favorites"]
        + 2 * row["retweets"]
        + 3 * row["quotes"]
        + 2 * row["bookmarks"]
    )
    view_signal = 0.3 * math.log1p(row["views"])
    reach = 0.4 * math.log1p(max(row["followers"], 1))
    return eng + view_signal + reach


def recency_score(row):
    """Fallback ranking for Latest mode where engagement counts are near-zero."""
    dt = _parse_created_at(row["created_at"])
    age_hours = 1e6
    if dt:
        now = _dt.datetime.now(_dt.timezone.utc)
        age_hours = max((now - dt).total_seconds() / 3600.0, 0.01)
    # Recency dominant, follower count as a tiebreaker.
    return -math.log1p(age_hours) + 0.4 * math.log1p(max(row["followers"], 1))


# ----- surfacing -----

def _truncate(s, n):
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


def _one_line(s):
    return " ".join(s.split())


def tweet_url(row):
    sn = row.get("screen_name") or "i"
    tid = row.get("tweet_id") or ""
    return f"https://x.com/{sn}/status/{tid}"


def surfaced_md_for_tweets(query, search_type, rows, top_n, pages_fetched, exit_reason):
    """Build the surfaced.md content for tweet-style results."""
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not rows:
        return (
            f"# X search: \"{query}\" ({search_type})\n\n"
            f"_No results._ Fetched {pages_fetched} page(s), exit reason: `{exit_reason}`. {ts}\n"
        )

    # Pick the ranking function based on mode.
    if search_type == "Latest":
        ranker = recency_score
    else:
        ranker = score
    ranked = sorted(rows, key=ranker, reverse=True)
    top = ranked[: top_n]

    # Low-signal warning: everything tiny accounts and zero engagement.
    low_signal = all(
        r["favorites"] < 5 and r["followers"] < 100 for r in top
    )

    lines = [f"# X search: \"{query}\" ({search_type})\n"]
    lines.append(
        f"Fetched {len(rows)} unique tweets across {pages_fetched} page(s) "
        f"on {ts}. Showing top {len(top)} by composite score.\n"
    )
    if low_signal:
        lines.append(
            "**Low-signal warning:** the matched tweets are from low-reach accounts "
            "with minimal engagement. The calling workflow may want to drop this output "
            "or broaden the query.\n"
        )

    # Headline accounts: distinct authors with the largest reach in the result set.
    by_account = {}
    for r in ranked:
        sn = r.get("screen_name")
        if not sn:
            continue
        if sn not in by_account or r["followers"] > by_account[sn]["followers"]:
            by_account[sn] = r
    headline = sorted(by_account.values(), key=lambda r: -r["followers"])[:8]
    if headline:
        lines.append("## Headline accounts (by follower count in result set)\n")
        for r in headline:
            badge = " ✓" if r.get("verified") else ""
            lines.append(
                f"- @{r['screen_name']}{badge} ({r['followers']:,}f) — "
                f"{_truncate(_one_line(r['text']), 160)}"
            )
        lines.append("")

    # The main reading surface.
    lines.append(f"## Top tweets by composite score\n")
    for i, r in enumerate(top, 1):
        text = _truncate(_one_line(r["text"]), 280)
        meta = (
            f"{r['favorites']}♥ {r['retweets']}↻ {r['quotes']}\" "
            f"{r['views']}👁 {r['bookmarks']}🔖"
        )
        date = r.get("created_at") or ""
        reply_tag = f" [reply to @{r['in_reply_to']}]" if r.get("in_reply_to") else ""
        quote_tag = (
            f" [quoting @{r['quoted_author']}]" if r.get("quoted_author") else ""
        )
        media_tag = ""
        if r.get("has_video"):
            media_tag = " [video]"
        elif r.get("has_photo"):
            media_tag = " [photo]"
        lines.append(
            f"{i}. @{r['screen_name']} ({r['followers']:,}f){reply_tag}{quote_tag}{media_tag}\n"
            f"   {text}\n"
            f"   {meta} — {date} — {tweet_url(r)}"
        )

    # If the user asked for Latest, also show a strict-recency view (the composite
    # score already weights recency for Latest, but a pure-recency cut helps when
    # the caller wants the freshest takes regardless of reach).
    if search_type == "Latest":
        by_recency = sorted(
            rows,
            key=lambda r: -((_parse_created_at(r["created_at"]) or _dt.datetime.min.replace(tzinfo=_dt.timezone.utc)).timestamp()),
        )[: min(top_n, 20)]
        lines.append("\n## Most recent (Latest mode)\n")
        for i, r in enumerate(by_recency, 1):
            text = _truncate(_one_line(r["text"]), 200)
            date = r.get("created_at") or ""
            lines.append(
                f"{i}. @{r['screen_name']} ({r['followers']:,}f): {text} — {date} — {tweet_url(r)}"
            )

    return "\n".join(lines) + "\n"


def surfaced_md_for_users(query, rows, top_n, pages_fetched, exit_reason):
    """search_type=People returns user objects, not tweets — render differently."""
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not rows:
        return (
            f"# X search (People): \"{query}\"\n\n"
            f"_No accounts found._ Fetched {pages_fetched} page(s), exit reason: `{exit_reason}`. {ts}\n"
        )

    ranked = sorted(rows, key=lambda r: -r["followers"])
    top = ranked[: top_n]
    lines = [f"# X search (People): \"{query}\"\n"]
    lines.append(
        f"Fetched {len(rows)} unique accounts across {pages_fetched} page(s) on {ts}. "
        f"Showing top {len(top)} by follower count.\n"
    )
    lines.append("## Accounts\n")
    for i, r in enumerate(top, 1):
        badge = " ✓" if r.get("verified") else ""
        desc = _truncate(_one_line(r["description"]), 200)
        lines.append(
            f"{i}. @{r['screen_name']}{badge} — {r['name']} "
            f"({r['followers']:,} followers, {r['statuses']:,} posts)\n"
            f"   {desc}\n"
            f"   https://x.com/{r['screen_name']}"
        )
    return "\n".join(lines) + "\n"


# ----- main -----

def main():
    ap = argparse.ArgumentParser(
        description="Search X (Twitter) and surface ranked results for synthesis."
    )
    ap.add_argument(
        "--query", action="append", required=True,
        help="X-search syntax string. Repeatable; results from all queries are merged and deduped."
    )
    ap.add_argument(
        "--search-type", default="Top", choices=sorted(ALLOWED_SEARCH_TYPES),
        help="Top (engagement-ranked, default), Latest (recency), People (accounts), Photos, Videos."
    )
    ap.add_argument(
        "--max-pages", type=int, default=5,
        help="Max pages per query (~20 results/page). Default 5 = up to ~100/query."
    )
    ap.add_argument("--top-n", type=int, default=60, help="How many to surface in surfaced.md.")
    ap.add_argument("--out", default="./x-search-results", help="Output directory.")
    # Convenience flags that just inject X operators into the query string.
    ap.add_argument("--min-faves", type=int, help="Convenience: appends `min_faves:N` to each query.")
    ap.add_argument("--lang", help="Convenience: appends `lang:xx` to each query.")
    ap.add_argument("--since", help="Convenience: appends `since:YYYY-MM-DD` to each query.")
    ap.add_argument(
        "--exclude-replies", action="store_true",
        help="Convenience: appends `-filter:replies` to each query."
    )
    args = ap.parse_args()

    if args.search_type not in ALLOWED_SEARCH_TYPES:
        sys.stderr.write(
            f"x-search: invalid --search-type {args.search_type!r}. "
            f"Allowed: {sorted(ALLOWED_SEARCH_TYPES)}\n"
        )
        sys.exit(1)

    key = load_key()
    raw_dir = os.path.join(args.out, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    composed_queries = [
        build_query(
            q,
            min_faves=args.min_faves,
            lang=args.lang,
            since=args.since,
            exclude_replies=args.exclude_replies,
        )
        for q in args.query
    ]

    is_people = args.search_type == "People"
    all_rows = []
    per_query_meta = []
    total_pages = 0
    try:
        for qi, q in enumerate(composed_queries):
            sub_raw_dir = os.path.join(raw_dir, f"query-{qi + 1:02d}")
            os.makedirs(sub_raw_dir, exist_ok=True)
            raw_rows, reason = paginate(
                q, args.search_type, key, args.max_pages, raw_pages_dir=sub_raw_dir
            )
            pages_this_query = len(os.listdir(sub_raw_dir))
            total_pages += pages_this_query
            normalized = []
            for entry in raw_rows:
                if not isinstance(entry, dict):
                    continue
                etype = entry.get("type")
                if is_people:
                    if etype == "user":
                        normalized.append(norm_user(entry))
                else:
                    if etype == "tweet" and not _is_promoted(entry):
                        normalized.append(norm_tweet(entry))
                    # Quietly skip any other type (promoted_tweet, cursor, module, etc).
            all_rows.extend(normalized)
            per_query_meta.append({
                "query": q,
                "pages": pages_this_query,
                "raw_count": len(raw_rows),
                "normalized": len(normalized),
                "exit_reason": reason,
            })
    except AuthError as e:
        sys.stderr.write(f"x-search: {e}\n")
        sys.exit(2)

    # Dedup across queries by tweet_id (or user_id for People mode).
    seen = set()
    deduped = []
    key_field = "user_id" if is_people else "tweet_id"
    for r in all_rows:
        k = r.get(key_field)
        if not k or k in seen:
            continue
        seen.add(k)
        deduped.append(r)

    # Write normalized data for grep/inspection.
    with open(os.path.join(args.out, "normalized.json"), "w") as f:
        json.dump(deduped, f, indent=1, default=str)

    # Pick exit reason for the surfaced.md header — first non-empty wins, then "empty".
    overall_reason = next(
        (m["exit_reason"] for m in per_query_meta if m["exit_reason"] != "empty"),
        per_query_meta[0]["exit_reason"] if per_query_meta else "empty",
    )

    # Build surfaced.md.
    if is_people:
        md = surfaced_md_for_users(
            " | ".join(composed_queries), deduped, args.top_n, total_pages, overall_reason
        )
    else:
        md = surfaced_md_for_tweets(
            " | ".join(composed_queries), args.search_type, deduped,
            args.top_n, total_pages, overall_reason,
        )
    with open(os.path.join(args.out, "surfaced.md"), "w") as f:
        f.write(md)

    meta = {
        "queries": composed_queries,
        "search_type": args.search_type,
        "pages_fetched": total_pages,
        "raw_total": sum(m["raw_count"] for m in per_query_meta),
        "normalized_total": sum(m["normalized"] for m in per_query_meta),
        "deduped_total": len(deduped),
        "surfaced_top_n": min(args.top_n, len(deduped)),
        "per_query": per_query_meta,
        "exit_reason": overall_reason,
        "low_signal": (
            not is_people
            and bool(deduped)
            and all(r.get("favorites", 0) < 5 and r.get("followers", 0) < 100
                    for r in sorted(deduped, key=score, reverse=True)[: args.top_n])
        ),
    }
    with open(os.path.join(args.out, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)

    print(json.dumps({k: v for k, v in meta.items() if k != "per_query"}, indent=1))
    if len(deduped) == 0:
        print(f"\nNo results. Wrote empty surfaced.md to {os.path.join(args.out, 'surfaced.md')}.")
    else:
        print(f"\nGathered {len(deduped)} unique results. "
              f"Read {os.path.join(args.out, 'surfaced.md')} to synthesize.")
        print(f"Normalized data in {os.path.join(args.out, 'normalized.json')}")


if __name__ == "__main__":
    main()
