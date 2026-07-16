# twitter-api45 `/search.php` reference

Condensed from a real probe of the endpoint (28 captured JSON payloads,
2026-06-07). The full probe report with raw evidence lives at
`/tmp/x-search-probe-report.md` and `/tmp/x-search-probe/` on the machine
where the skill was built; this file is the version intended to live with
the skill.

The bundled `scripts/search_x.py` wraps everything below. Read this file
only when you need an endpoint or behavior the script doesn't cover.

## Gotcha (zsh)

In zsh, do NOT assign a tweet id to a shell variable named `GID` — it is
the reserved real-group-id variable and the assignment fails with "failed
to change group id." Use `TID`/`Q`/`CUR`. Also: network calls may need
the sandbox disabled.

## Auth

```
x-rapidapi-host: twitter-api45.p.rapidapi.com
x-rapidapi-key: <from $RAPIDAPI_KEY or ~/.rapidapi_key>
```

Bad / missing key returns HTTP 403 with body
`{"message": "You are not subscribed to this API."}` — no `status`, no
`timeline`. The script raises `AuthError` and exits 2 in this case.

## Endpoint

`GET https://twitter-api45.p.rapidapi.com/search.php`

| Param | Required | Type | Notes |
|---|---|---|---|
| `query` | yes | string | Free X-search syntax. Forwarded verbatim. |
| `search_type` | optional | enum | Default Top. See matrix below. |
| `cursor` | optional | opaque string | From a prior call's `next_cursor`. |

### `search_type` matrix (verified)

| Value | Entry shape | Notes |
|---|---|---|
| `Top` | `type: "tweet"` | Engagement-ranked. **Default. Use for almost everything.** |
| `Latest` | `type: "tweet"` | Reverse-chronological. Includes replies. Engagement counts near-zero. |
| `People` | `type: "user"` | Different shape entirely — user objects, no tweets. |
| `Photos` | `type: "tweet"` | Forces a `media` block. Skews video in practice. |
| `Videos` | `type: "tweet"` | Same shape as Photos. |
| `Media` | (empty) | Silently empty. Don't use. |
| anything else | falls back to Top | Validate against the allow-list client-side. |

## Query operators (all forwarded verbatim to X)

Every operator below was probed and confirmed. Document any operator that
works on twitter.com/search and it will work here.

| Operator | Example |
|---|---|
| Plain phrase | `claude code` |
| Exact phrase | `"claude code"` |
| Author | `from:karpathy claude` |
| Reply target | `to:karpathy claude` |
| Min favorites | `claude min_faves:100` |
| Min retweets | `claude min_retweets:50` |
| Language | `claude lang:en` |
| Since date | `claude since:2026-01-01` |
| Until date | `claude until:2026-04-01` |
| Exclude replies | `claude -filter:replies` |
| Filter videos | `claude filter:videos` |
| Filter images | `claude filter:images` |
| URL match | `claude url:github.com` |
| Hashtag | `#claudecode` |
| Boolean AND | `claude AND skills` |
| Boolean OR | `claude OR anthropic` |
| Exclude word | `claude -anthropic` |

**Composition rule of thumb** for high-signal recent discourse:

```
<topic> min_faves:50 lang:en -filter:replies since:<date>
```

The script's `--min-faves`, `--lang`, `--since`, and `--exclude-replies`
flags inject the equivalent operators if you'd rather not hand-build the
query string.

## Pagination

8-page test with `query=claude code` and `search_type=Latest` returned
160 unique tweets across 8 pages with zero duplicates. `next_cursor` is
opaque base64 (~99 chars for plain queries, sometimes 600+ for heavy
ones).

**Stop conditions:**
- `timeline` is empty (most reliable signal — even empty-query results
  return non-null cursors, so don't rely on cursor presence alone).
- `next_cursor` is missing or repeats a value seen earlier.
- `status` field is present and != `"ok"` (bad cursor returns
  `status: "failed"`).

Sleep ~0.7s between calls. Not strictly necessary in light probing but
courteous and unlikely to trip rate limits.

## Result schema

### Top-level envelope (every search_type returns this)

```json
{
  "status": "ok" | "failed",
  "timeline": [ /* entries */ ],
  "next_cursor": "DAACCgAC...",
  "prev_cursor": "DAACCgAC..."
}
```

### Tweet entry (`type: "tweet"` — Top, Latest, Photos, Videos)

Key fields the script normalizes:

```jsonc
{
  "type": "tweet",
  "tweet_id": "2046457651932901652",
  "screen_name": "MarioNawfal",
  "created_at": "Tue Apr 21 05:15:00 +0000 2026",   // legacy Twitter format, NOT ISO
  "text": "Cybertruck just dropped a nuke ...",
  "lang": "en",
  "favorites": 662,
  "retweets": 65,
  "replies": 42,
  "quotes": 4,
  "bookmarks": 72,
  "views": "151561",                                 // STRING, cast with int()
  "user_info": {
    "screen_name": "MarioNawfal",
    "followers_count": 3570227,
    "verified": true,
    "verified_type": null,
    "blue_verified": true,                           // alternate verification key
    "description": "..."
  },
  "media": {                                         // dict OR list, sometimes absent
    "video": [ /* variants with bitrate, content_type, url */ ],
    "photo": [ /* sizes */ ]
  },
  "quoted": {                                        // present iff quote tweet
    "tweet_id": "...",
    "text": "...",
    "author": { "screen_name": "...", "blue_verified": true }
  },
  "in_reply_to_screen_name": "..."                   // only on Latest results
}
```

### User entry (`type: "user"` — People mode only)

```jsonc
{
  "type": "user",
  "user_id": "1686044379910131718",
  "screen_name": "cybertruck",
  "followers_count": 251517,
  "is_blue_verified": true,                          // key differs from user_info.verified
  "description": "📐"
}
```

## Field-presence gotchas (baked into the script)

| Field | Gotcha |
|---|---|
| `views` | String, not int. Always `int(e.get("views") or 0)`. |
| `media` | Usually dict, rarely list. Type-check before key access. |
| `created_at` | Legacy Twitter format. Parse with `%a %b %d %H:%M:%S %z %Y` or `email.utils.parsedate_to_datetime`. |
| Retweets | Do **not** appear in search results. Only quote tweets do (as their own entries with `quoted` set). Don't expect `retweeted_status`. |
| Verification | Inconsistent keys: `verified` (top-level user_info), `blue_verified` / `is_blue_verified` (nested or in user entries). Check all three. |
| Promoted tweets | `tweet_id` starts with `promoted-`. The script filters them out automatically. |
| Unknown `type` | Some queries may return `cursor` / `module` / other types. Skip anything not in {`tweet`, `user`}. |

## Ranking signals

All counts are populated (no nulls observed). Reliability for ranking:

| Field | Reliability | Notes |
|---|---|---|
| `favorites` | high | Most consistent engagement floor. |
| `retweets` | high | Sparse for small tweets but never null. |
| `quotes` | high | Quote-rich tweets are often higher-signal takes. |
| `bookmarks` | high | Underused but strong: tracks "save for later" intent. |
| `replies` | medium | Inflated by ratios; high replies + low likes often = controversy. |
| `views` | medium | Always populated, but ~0 on Latest (tweets are fresh). |
| `followers_count` | high | Use as separate reach factor, not mixed into engagement. |

The script's composite score:

```python
eng        = log1p(favs + 2*rts + 3*quotes + 2*bookmarks)
view_signal = 0.3 * log1p(views)
reach      = 0.4 * log1p(followers)
score      = eng + view_signal + reach
```

Everything log-dampened because raw counts span 8+ orders of magnitude on
X. Tweak the coefficients in `scripts/search_x.py:score` if a calling
workflow needs different weighting. For Latest mode the script falls back
to a pure-recency ranker.

## Other endpoints on the same provider

Available but not wrapped by the search script (call directly with
`x-thread-miner/scripts/fetch_engagement.py:call` or with raw curl):

- `tweet.php` (single-tweet metadata)
- `latest_replies.php` (a tweet's replies — used by x-thread-miner)
- `tweet_thread.php` (threaded view)
- `timeline.php` (a user's recent tweets)
- `retweets.php` (who retweeted)
- `screenname.php` (profile lookup)
- `replies.php` (a user's replies across the site)
- `trends.php` (trends)
- `community_*.php`, `list_*.php`, `spaces_info.php` (community + list +
  Space endpoints)

For broader "social sensing" workflows, `trends.php`, the community
endpoints, and `search.php` together are the interesting trio.

## Open questions (not blockers)

- **Rate limits.** Not tripped in ~35 calls in 5 minutes. The RapidAPI
  standard is HTTP 429 with `X-RateLimit-*` headers; the script catches
  that and retries with exponential backoff, but we don't have a recorded
  example of this provider's exact 429 body.
- **Cursor stability over time.** Not tested. If a workflow ever wants
  to resume a previous search session by replaying a cursor, verify the
  cursor still works on the second run.
- **Total result count.** No `count` or `total` field is returned. The
  only way to know how big a query's full result set is, is to paginate
  to exhaustion. Cap `--max-pages` accordingly.
- **GIF shape.** GIFs appear under `media.video` with a single MP4
  variant, not a separate `media.gif` key. Confirmed in cybertruck
  probe; re-verify on a meme-heavy query before relying on a dedicated
  GIF branch.
