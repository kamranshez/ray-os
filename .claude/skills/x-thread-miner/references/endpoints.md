# twitter-api45 endpoint reference

RapidAPI host: `twitter-api45.p.rapidapi.com`. Every request needs two headers:

```
x-rapidapi-host: twitter-api45.p.rapidapi.com
x-rapidapi-key: <key from $RAPIDAPI_KEY or ~/.rapidapi_key>
```

The bundled `fetch_engagement.py` wraps everything you normally need. This file is
for the cases where you want an endpoint the script doesn't cover.

## Gotcha

In zsh, do NOT assign a tweet id to a shell variable named `GID` — it is the
reserved real-group-id variable and the assignment fails with "failed to change
group id." Use `TID`/`ANCHOR`. Also: network calls may need the sandbox disabled.

## Endpoints that matter for engagement mining

| Purpose | Path | Key params | Returns |
|---|---|---|---|
| Replies to a tweet | `latest_replies.php` | `id`, `cursor` | `timeline[]` of replies, each with `user_info` (followers, verified, bio), plus `next_cursor` |
| Quote tweets of a tweet | `search.php` | `query=quoted_tweet_id:<id>`, `search_type=Latest`, `cursor` | `timeline[]` of quote tweets, ~20/page, plus `next_cursor` |
| One tweet's metadata | `tweet.php` | `id` | text, counts (likes/replies/retweets/quotes/views), `conversation_id`, `quoted`, `author` |
| Threaded view | `tweet_thread.php` | `id`, `cursor` | OP + self-thread + replies as a tree |
| A user's tweets | `timeline.php` | `screenname`, `cursor` | recent tweets with counts (use to locate a high-engagement tweet by author) |
| Retweeters | `retweets.php` | `id`, `cursor` | accounts that retweeted |
| Profile | `screenname.php` | `screenname` | followers, bio, location |
| A user's replies | `replies.php` | `screenname`, `cursor` | that user's replies across the site |

### Getting quote tweets (no dedicated endpoint)

There is no "quotes" endpoint. Use search with the X advanced-search operator:

```
search.php?query=quoted_tweet_id:<TWEET_ID>&search_type=Latest
```

Paginate via `next_cursor` until it is empty or repeats.

## Pagination pattern (replies and search)

Both return `{ "timeline": [...], "next_cursor": "...", "prev_cursor": "..." }`.
Loop: call → collect `timeline` → pass `next_cursor` back as `cursor` → stop when
`next_cursor` is falsy, repeats, or `timeline` is empty. Sleep ~0.7s between
calls. De-dup by `tweet_id`.

## Field map (timeline entry)

```
tweet_id, text, created_at, lang
favorites (likes), replies, retweets, quotes, views
in_reply_to_screen_name, in_reply_to_status_id_str   (replies)
user_info: { screen_name, name, followers_count, verified, description, location, rest_id }
```

Top-level `tweet.php` payloads put the author under `author` and the quoted
parent under `quoted`.

## Other endpoints available (for future ideas)

User's Media, Following, Followers, Trends, Check Retweet, Check follow, List
timeline / followers / members, Community Info / Members / Posts (+ search),
Spaces info, Jobs Search, Inspiration Posts, About profile, Profiles By RestIds,
User live, Affiliates. Trends + Community + Search are the interesting ones for a
broader "social sensing" workflow.
