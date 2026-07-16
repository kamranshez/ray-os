---
name: x-search
description: >-
  Search X (Twitter) by topic, keyword, hashtag, or X advanced-search syntax
  and get back a ranked, deduplicated list of tweets (or accounts) for
  synthesis. Use this whenever the user wants to discover what's being said
  about a topic on X without already having tweet URLs in hand. Trigger on
  phrases like "search X for X", "search Twitter for X", "what is being said
  about X on X", "find tweets about X", "pull recent X discourse on Y", "any X
  chatter about Y", "scan X for Z", "what are people tweeting about X", "is
  anyone on X talking about Y", or any request to discover, sample, or harvest
  X content on a topic the user does not already have URLs for. Also use it
  proactively inside multi-agent workflows where one agent needs fresh X
  signal on a topic before generating ideas, drafting copy, doing competitor
  research, or sizing a hot take. Distinguished from `x-thread-miner`: if the
  user hands you a tweet URL, use x-thread-miner to mine its replies and quote
  tweets; if the user hands you a topic, a keyword, a hashtag, or an account
  to drill into, use x-search.
---

# X Search

Discover X content on a topic. Returns a ranked, deduplicated list of tweets
(or accounts, when searching People) in a single readable `surfaced.md`, plus
the raw and normalized data for follow-up grepping. Sibling to
[`x-thread-miner`](../x-thread-miner/SKILL.md): that one mines the
conversation *around* a tweet you already know about; this one finds tweets
you didn't know existed.

The division of labor is the same as the sibling skill. The bundled script
does the noisy part (paginated fetching, dedup, ranking by composite
engagement and reach). You do the smart part: read `surfaced.md` and write
the synthesis. Don't try to load raw JSON of hundreds of tweets into
context — that is what `surfaced.md` is for.

## When to skip the quiz

Unlike x-thread-miner, x-search does not need a quiz. The defaults (Top
ranking, 5 pages, top 60 surfaced) are right for almost every use case. Fire
the script immediately on a clear request. Only ask the user if the request
is genuinely ambiguous in a way the defaults can't resolve (e.g. "search X"
with no topic at all).

## Step 1 — Compose the query

The endpoint forwards X's advanced-search syntax verbatim, so the highest
leverage you have is in building a smart query, not in post-filtering. The
syntax is exactly what works at `https://x.com/search?q=…`:

| Goal | Operator | Example |
|---|---|---|
| Exact phrase | `"…"` | `"agentic loops"` |
| From an account | `from:` | `from:karpathy claude` |
| Replies to an account | `to:` | `to:elonmusk cybertruck` |
| Engagement floor | `min_faves:`, `min_retweets:` | `claude min_faves:100` |
| Language | `lang:` | `claude lang:ja` |
| Date range | `since:`, `until:` | `claude since:2026-01-01 until:2026-04-01` |
| Exclude word | `-word` | `claude -anthropic` |
| Exclude replies | `-filter:replies` | `claude -filter:replies` |
| Media filters | `filter:videos`, `filter:images` | `claude filter:videos` |
| URL match | `url:` | `claude url:github.com` |
| Hashtag | `#tag` | `#claudecode` |
| Boolean | `AND`, `OR` | `claude OR anthropic` |

Combine them. The single highest-signal default query shape for "what is the
discourse saying about X" is:

```
<topic> min_faves:50 lang:en -filter:replies since:<recent-date>
```

That filters out conversational noise, replies, and tiny accounts in one
pass. The script's `--min-faves`, `--lang`, `--since`, and
`--exclude-replies` convenience flags inject those operators if it's easier.

If a single query keeps returning the same accounts or topics, pass
`--query` multiple times to fan out across operator variants — the script
merges and dedupes by `tweet_id`. Example: pair a hashtag query with a
plain-word query, or a `from:` query with a `to:` query, to triangulate on a
sub-community.

### Recency recipes

The most common ask is "what's recent on this topic." There are two paths
and one of them is almost always wrong, so be deliberate:

- **`--search-type Latest`** is pure reverse-chronological. Tweets are
  seconds old, so engagement counts are near-zero and the ranking falls
  back to recency plus author followers. Use this only when freshness
  beats signal: live event monitoring, breaking news, watching a launch
  unfold in real time.
- **`--search-type Top --since YYYY-MM-DD`** is recent AND high-signal.
  X's `since:` operator is forwarded verbatim and constrains the Top
  ranking to a date window. This is what you almost always want.

Default to the second path. The first path is a trap for "I want fresh
tweets" — it gives you fresh tweets nobody has read yet, which is usually
not what the calling agent needs.

Common recipes:

| Want | Command shape |
|---|---|
| What broke through this week | `--search-type Top --since <7-days-ago> --min-faves 100` |
| Last 48h discourse, no noise | `--search-type Top --since <2-days-ago> --min-faves 20 --exclude-replies` |
| Live monitoring of a hashtag | `--search-type Latest --query "#tag"` |
| What launched today | `--search-type Latest --query "<topic> filter:videos"` (videos surface launches faster than text) |
| Recent takes from one account | `--search-type Top --query "from:<handle> <topic> since:<recent>"` |

For multi-agent workflows feeding fresh X data into idea generation, the
"Top + since" recipe with a 7 to 14 day window is the right default. It
gives the calling agent enough sample to find patterns while still being
genuinely recent.

## Step 2 — Fetch

```bash
python3 <skill-dir>/scripts/search_x.py \
  --query "<X-search syntax>" \
  [--query "<another variant>"] \
  [--search-type Top|Latest|People|Photos|Videos] \
  [--max-pages 5] \
  [--top-n 60] \
  [--min-faves 50] [--lang en] [--since 2026-01-01] [--exclude-replies] \
  --out "<output-dir>"
```

- The key is loaded from `$RAPIDAPI_KEY` or `~/.rapidapi_key` automatically.
  Same convention as x-thread-miner. If the script reports no key, tell the
  user to put their RapidAPI key in `~/.rapidapi_key` — it's kept out of the
  skill on purpose so it never syncs to git.
- Pick `--search-type` deliberately:
  - **Top** (default): ranked by X's engagement signal. Use for "what is the
    discourse," "who is making the strongest argument," "best tweets on
    topic." Almost always the right default.
  - **Latest**: reverse chronological. Use only when freshness matters more
    than signal (breaking news, monitoring a launch, sentiment on a fresh
    event). Includes replies; counts are near-zero because tweets are
    seconds old.
  - **People**: returns *accounts*, not tweets. Use when the user wants "who
    on X talks about X," "list of accounts in the niche," or "experts on
    Y." The output shape is different (no tweet text), so the surfaced.md
    is rendered differently.
  - **Photos / Videos**: tweets with media of that kind. Use for visual
    discovery, demo hunting, or product launch screenshots.
- `--max-pages` is the only knob on cost. Each page is ~20 results and one
  API call. 5 pages (~100 tweets) is a sweet spot for most synthesis
  prompts. Go higher only when you need exhaustive coverage of a small
  niche.
- The script may need the sandbox disabled for network access; if a call
  fails with a "failed to change group id" or network error, rerun with the
  sandbox off.

Outputs land in `--out`:

- `surfaced.md` — top-N ranked tweets with text, engagement, author, date,
  and the canonical tweet URL. **Read this.**
- `normalized.json` — every deduped result as a flat dict, for grep / sort
  by specific themes.
- `raw/query-NN/page-NN.json` — verbatim API responses per query per page,
  if you need to inspect the raw envelope.
- `meta.json` — query strings, search type, page count, dedup counts, exit
  reason, and a `low_signal` flag.

## Step 3 — Handle the "no useful results" case

The whole point of this skill living inside multi-agent workflows is that
the calling agent can drop the result if it's noise. Two cases to recognize
before synthesizing:

1. **`surfaced.md` says `_No results._`** — the query matched nothing.
   `meta.json.deduped_total` is 0, exit code is still 0. Don't synthesize;
   either broaden the query (drop operators, lower `--min-faves`, widen
   `--since`) or tell the user nothing came back.
2. **`meta.json.low_signal` is true** — results exist but are all from
   tiny accounts with minimal engagement. The surfaced.md will have a
   `**Low-signal warning:**` line at the top. Either dig into the raw data
   if you really want the long-tail content, or tell the upstream caller
   the topic is too obscure (or the query too narrow) to produce a useful
   sample.

Non-zero exit codes are reserved for real failures (auth, transport). If
you see exit 2, the RapidAPI key is missing, invalid, or unsubscribed —
surface that to the user verbatim; don't try to work around it.

## Step 4 — Synthesize

Lead with the patterns, not the tweets. Suggested structure:

```markdown
# X search: <topic> — what the discourse reveals

## Headline read
The 2 to 3 things that matter most, stated as conclusions.

## Camps and framings
The distinct positions people are taking. Group by framing, name each one,
attribute with @handle and a short verbatim quote.

## Notable accounts
High-reach or high-signal accounts that engaged. Useful for follow-up
research (their other recent tweets, who they retweet, etc.).

## Surprises
Things that show up in the data that contradict the obvious read. The
counter-narrative under the dominant one.

## Suggested follow-up
- Specific tweet URLs worth mining via x-thread-miner for second-order
  insight (pick the highest-engagement ones, especially the controversial
  takes).
- Account handles worth pulling timelines on.
- Adjacent queries worth running.
```

Adapt sections to the topic — drop ones that don't apply, add ones that
do. The "surprises" section is often the part the upstream caller cares
about most: the data tells you something they didn't ask for, and that's
where the leverage is.

Hand off to `x-thread-miner` whenever a single tweet in the surfaced
results is doing too much heavy lifting in your synthesis. Mining its
replies and quote tweets often gives you the spectrum of reactions the
search alone can't.

## Notes

- For exact API behavior, response schema, ranking formula rationale, and
  the gotchas I had to bake in (`views` is a string, `media` is sometimes
  a list, retweets never appear in search results, etc.), see
  `references/endpoints.md`. You rarely need it — the script handles
  everything — but it's there if you want to call a related endpoint the
  script doesn't wrap.
- The composite ranking favors high-engagement-per-follower. A 10K
  follower account that gets 500 likes will often outrank a 10M follower
  account that gets 5K. That's deliberate: the script is built for
  surfacing sharp takes, not viral fluff. If you want pure-reach ordering
  instead, sort `normalized.json` by `followers` directly.
- Use multiple `--query` invocations to triangulate. The cost is small
  (each query is independent and runs sequentially), and the dedup means
  you get the union of all results without paying for overlap twice in
  cognitive load.
