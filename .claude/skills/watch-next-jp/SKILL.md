---
name: watch-next-jp
description: Curiosity engine for JAPANESE-immersion video discovery — "what Japanese video should I watch next?" Harvests candidate Japanese videos from YouTube's unauthenticated graph (related-video rails around what you loved, JP-native search, fresh uploads from your channels), then YOU (this session — no cloud LLM) judge, rank, and diversify them against the taste on record. Bare `/watch-next-jp` does an open curiosity pass (breadth across genres, novelty-weighted); `/watch-next-jp about <topic>` narrows the region but keeps the variety. Reads taste.json (your watch history + channels) as seeds; writes nothing to it. Use for "/watch-next-jp", "/watch-next-jp about X", "what Japanese video should I watch", "recommend me something to immerse in", "find me new Japanese channels", "what should I watch for immersion tonight". ONLY for Japanese-language immersion viewing — do NOT use for general/English video recommendations, for Ray's own YouTube channel (that is youtube-ab-tester / youtube-outlier-research), or for any non-video recommendation request.
---

# /watch-next-jp — curiosity orchestrator

A discovery engine for Japanese listening immersion. **The dumb tool
(`harvest.py`) fetches raw candidates; the judgment is yours.** Harvesting hits
YouTube's own graph unauthenticated — no key, no account, no PO token, no cloud
LLM. The one thing an API would normally do here — expand taste into native
search terms and judge candidates — **you do inline** (this session is the LLM).

```
  DUMB TOOL (harvest.py)                     THIS SESSION (judgment, no API)
  seeds ─► run(related+search+rss) ──────► [YOU: expand · judge · rank · diversify] ─► picks
            │                                        │                                    │
      YouTube graph, unauth              taste.json + rated history              enqueue / watch
      → discover.db                      → JP queries, scoring, clustering
```

Why independent, not "harvest YouTube's algorithm": the personalized home feed
is unreachable unauthenticated (returns empty), and it optimizes watch-time /
centroid-convergence — the opposite of the novelty-seeking curiosity engine we
want. The reachable edges (similarity rail, search, RSS) are the right raw
material.

## Conventions

- `ROOT` = this package's directory. Run every command **from `ROOT`**.
- `PY` = the repo venv if present, else any Python 3.10+ with `requests`:
  `PY="$( [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3 )"`.
- Tool: `$PY harvest.py {seeds | run | list | set-status | gate-speech}`.
- **Pass multi-id seeds as separate words, not one string.** `--related` / `--rss`
  take `nargs="*"`. Under zsh an unquoted `$IDS` does NOT word-split, so
  `--related $IDS` arrives as a single bogus id, InnerTube/RSS return nothing, and
  the edge silently contributes **0 candidates** while `search` still works. Use
  `${=IDS}` (zsh) or pass the ids literally. Symptom: `list` shows only `edge=search`.
- Discovery store: `<data_dir>/discover.db` (default `./data/discover.db`) — the
  crawl pool. Separate from your taste input by design.
- **Taste input:** `taste.json` (default `./data/taste.json`) — the structured
  record of what you've watched and how you rated it. You maintain it by hand
  (or generate it from your own watch history); see `taste.example.json`.
- `taste.md` (optional): a hand-written prose taste digest. The legible profile
  you rank against; you edit it. See `taste.example.md`.

## Step 0 — preflight

1. **Taste present?** If `taste.json` has **no rated episodes and no channels**
   (`harvest seeds` → empty `rated` *and* empty `channels`), the recommender has
   no taste to learn from yet — tell the user to seed `taste.json` with a few
   videos/channels they like first (even just `liked_video_ids` + `channels`),
   then come back. A cold recommender guesses.
2. **Topic?** `/watch-next-jp about <topic>` → focused mode (Step 2 seeds from the
   topic). Bare `/watch-next-jp` → open mode. Note the count if they asked for one
   ("recommend 5"); default to **6–8 picks**.

## Step 1 — read the taste (seeds)

```sh
$PY harvest.py seeds   # rated[], channels[], liked_video_ids[], blocked_channel_ids[], watched_count
```

Read it, plus `taste.md` if it exists. Build a working model of the taste from:

- **rated[]** — per episode: `{title, channel, rating, tags[], genre, format,
  topics[], axes{}, axis_valid{}, difficulty, taste_valid, adjusted_enjoyment,
  follow, note}`, best first. How to read it:
  - **`axes`** are graded 1–5 on their own vectors — `topic_pull` (did the subject
    grip me), `presenter` (did I enjoy listening to this person), `audio_fidelity`
    (recording), `speech_clarity` (delivery — fast/slurred vs clean), `difficulty`.
    Don't average them; each steers a different lever.
  - **`axis_valid` is the censor.** When a video was too hard (`difficulty` 5), the
    comprehension-dependent axes are marked `false` — trust only the `true` ones.
    The classic case: understood-nothing content where `presenter`=5 is valid but
    `topic_pull` is not → learn "more of this performer," NOT "more of that topic."
    `taste_valid=false` / `adjusted_enjoyment=null` says the same about the overall
    star: keep the topic, don't read the low score as a taste-negative.
  - **`follow`** is a per-channel intent decoupled from the star — `more` means keep
    this channel a strong seed even on a mediocre video; treat it as a positive
    channel signal regardless of `rating`.
  - **`note`** is free text — parse it to fill any axis the user didn't record.
  - **chips (`tags`)**: `fascinating`/`loved_format` (+), `didnt_grab` (−, move off
    the cluster), `already_knew` (−, down-rank domain). `over_my_head` is the legacy
    difficulty flag (same as `difficulty`=5).
  (All axis/tag fields are optional in `taste.json`; use whatever is present.)
- **channels[]** — `{channel, channel_id, best_rating, follow_state, profile}`,
  followed-first. The strongest single taste predictor and your RSS + related seeds.
  **`profile`** is the presenter fingerprint — a prose `characterization` +
  attributes (dialect, register, energy, humor, speaking rate…). Roll the profiles
  of liked channels into a **taste-in-presenters** ("calm, clear, mid-register solo
  explainers with dry humor") and match *that* against a candidate's channel/title
  to discover **unknown** channels, not just resurface known ones. A `follow=more` /
  high `presenter` means deliberately re-surface that speaker's OTHER videos too
  (repeat exposure is a top listening booster).
- **liked_video_ids[]** — rating ≥ 4 **or** `follow=more`; the related-rail seeds.
- **blocked_channel_ids[]** — `follow=block`. A hard veto: never recommend these, and
  drop any candidate whose `channel_id` is in the list.

If `taste.md` is missing or stale, note it — you can offer to write one in Step 6.

## Step 2 — expand taste into JP-native queries (your highest-leverage job)

This is the single highest-leverage thing you do here. The user can't type these
— the genre/format vocabulary is *cultural*, not translational. From the taste
model, write **~15–20 native Japanese search strings**, deliberately **broad
across clusters** (a curiosity engine, not a niche-finder):

- The 解説 (explainer) ecosystem when it fits the taste: `雑学`, `都市伝説`,
  `歴史解説`, `科学解説`, `なるほど系` (skip the synthetic-TTS `ゆっくり解説` family
  unless the user wants it — see Step 4).
- The user's demonstrated veins from the rated titles (e.g. `散歩 vlog`,
  `秘境 旅`, `廃墟 探訪`, `限界ニュータウン` — read what they actually rated high).
- **Focused mode** (`about <topic>`): seed from the topic but keep novelty — emit
  ~5 *different angles* on it (native format variants), not 5 near-duplicates.

Breadth is the policy: jump between subcultures, don't drill one.

## Step 3 — harvest

Feed all three edges in one run — liked-video related-rails, your JP queries, and
channel RSS:

```sh
$PY harvest.py run \
  --related <liked_video_id> [<id> ...] \
  --search "<jp query 1>" "<jp query 2>" ... \
  --rss <channel_id> [<channel_id> ...]
```

It prints the **new** candidates (already filtered against what you've seen and
deduped). Then pull the full open pool so earlier harvests are in the running:

```sh
$PY harvest.py list --status new
```

Each candidate: `{video_id, title, channel, channel_id, duration, view_count,
edge, seed, meta}`. `edge` tells you provenance (`related` = similarity to a
liked video; `search` = your query; `rss` = fresh from a known channel);
`meta.info` on related carries the view/age text, `meta.published` on RSS the
upload date.

## Step 4 — judge · rank · diversify (the intelligence; no API)

This is the LLM-judge, running as **you**. Score each candidate against the taste
model and the objective function:

- **relevance** — title/channel/topic fit to what they rate high (use the *valid*
  axes only — a censored `topic_pull` is not evidence about topic),
- **presenter-fit** — does the candidate's channel/title match the rolled-up
  taste-in-presenters (dialect, register, energy, delivery from the fingerprints)?
  This is how an unknown channel earns a slot,
- **follow pull** — `follow=more` channels get their own uploads + related surfaced
  (manufactured repeat-exposure); `follow=block` channels and their candidates are
  dropped outright,
- **novelty** — topical distance from recently-watched: **rewarded, not penalized**
  (push away from the centroid while staying glancingly-intellectual),
- **− expertise-redundancy** — down-rank domains tagged `already_knew` or rated low,
- **− repetition** — don't stack one channel/format/topic; spread them,
- **glance-fit** — does it read like the calm, curious, learnable content they like
  (vs engagement-bait drama, rage-clickbait, overlong 総集編 unless matched).

Then **diversify**: round-robin across genre/format clusters so the final list is
deliberately varied, and every few picks **force a wildcard** from a cluster
they've never sampled — serendipity injection. A curiosity engine that converges
stops being curious; keep the exploration budget.

Drop obvious junk (non-Japanese unless clearly wanted, livestream VODs, pure
music, misparses). Land on the requested count (default 6–8).

**Synthetic-TTS voices are hard-filtered by default — a two-tier filter you back
up.** Many learners can't tolerate the ゆっくり / VOICEROID / VOICEVOX / ずんだもん
synthetic-narrator voice, and it's poor listening-practice material. Tier 1 is
deterministic: `harvest run` marks candidates whose title/channel hit the format
blocklist (built-in default, override via `discover.format_blocklist` in
config.json) as `status='filtered'`, so they never reach you as `new`. Tier 2 is
**you**: those formats brand themselves in the title, but an occasional one uses
the voice without labeling it. If you recognize a candidate as synthetic-TTS
narration, **drop it and `set-status <id> dismissed`**, even though it passed
Tier 1. (To see what got auto-filtered: `harvest list --status filtered`; to tune,
edit `discover.format_blocklist` then `harvest refilter`. If the user *wants* TTS
content, set `format_blocklist` to `[]` in config.json.)

## Step 4.5 — speech gate (mandatory, before you present)

A pick is worthless if there's nothing to hear: **every recommendation must
contain Japanese speech to mine.** Wordless / music-only / ambient footage — a
整地 (land-leveling) work video, a ジオラマ build, a pure-ambient 4K walk with no
narration — can score perfectly on taste and still be a non-starter. Metadata
alone can't tell (titles don't say "silent"), so this is a deterministic probe.
Run it on your **ranked shortlist** (a few more than the target, so drops don't
leave you short) before writing the block:

```sh
$PY harvest.py gate-speech <id> <id> <id> ...
```

It probes each via yt-dlp and returns a `verdict` per id, moving the speechless
ones to `status='no_speech'` (cached in `meta.speech`, so re-runs are free):

- `ja` — Japanese speech present → **keep, present it.**
- `silent` — no speech at all (music/ambient) → **dropped; do not present.**
- `non_ja` — speech, but not Japanese → **dropped** (also fails the JP filter).
- `unknown` — probe failed (private/geo/removed) → left `new`; mention the
  uncertainty in the pick's line rather than vouching for it.

Only present `ja` picks. If drops leave you under the count, pull the next
candidates from the ranked pool and gate those too. (The signal: YouTube's ASR
emits a `ja-orig` caption track / sets `language=ja` only when it actually hears
Japanese — a plain `ja` auto-caption is just a translation, and manual `ja` subs
can be uploader text on a silent video, so neither is trusted. Rare miss: a
Japanese video whose uploader disabled auto-captions reads as `silent`; if a pick
you're confident is spoken comes back `silent`, `gate-speech --recheck` it or
trust your judgment and note it.)

## Step 5 — present + hand off

Present the ranked picks as one compact block — per pick: **title · channel**, a
one-line *why* (the relevance/novelty rationale, and the edge if telling — "same
walking-vlog neighborhood as ★5 ガマランド" / "new cluster: wildcard"), and the URL
`https://www.youtube.com/watch?v=<video_id>`.

Then hand off however your setup wants (open the URL, add to a playlist, feed it
to whatever downstream immersion tooling you use). Record the outcome on each
candidate so nothing re-surfaces next run:

```sh
$PY harvest.py set-status <video_id> queued        # taken
$PY harvest.py set-status <video_id> dismissed     # user rejected it
```

(Leave un-mentioned candidates `new` — they stay in the pool for next time.)

## Step 6 — refresh taste.md (offer, when useful)

If `taste.md` is missing or the rated set has grown a lot since it was written,
offer to (re)write it from the rated history — the legible digest ("you reliably
rate high: …; you bail on: …; ambiguous: …"). Three jobs: it feeds your next
ranking pass, it's **editable** so the user corrects you, and it answers "I don't
know what I'm looking for" by reflecting taste back. Keep it short and honest to
the data; don't invent preferences the ratings don't show.

## Notes

- **No cloud LLM, no account, no key.** Harvest is anonymous HTTP to YouTube;
  judgment is this session.
- **The `related` edge is additive, not idempotent** — YouTube's `/next` returns a
  slightly different neighborhood each call, so re-running `run --related` on the
  same seeds legitimately discovers *more* of the cluster; the store dedupes, so
  it only ever grows with genuinely-new videos. Re-harvest freely.
- **Seeds are thin early.** With few rated episodes and sparse channel provenance,
  lean on `search` (your JP expansion) more than `related`/`rss`; as `taste.json`
  fills, the graph edges get richer. One good seed unravels a subculture.
- The `/next` rail is a *similarity* edge, not personalization — treat it as
  "near what you liked," which is exactly what you want it for.

## Failure modes

| symptom | meaning | move |
|---|---|---|
| `harvest seeds` → empty `rated` **and** `channels` | no taste yet | stop; tell the user to seed taste.json with a few liked videos/channels first |
| `harvest run` → `0 new` on every edge | pool exhausted / all already seen | widen the JP queries (new clusters), or re-run `--related` (additive); or rank what's already in `list` |
| `related` returns nothing for a seed | InnerTube `/next` shape changed or bot-checked | fine — search + rss still carry the run; if persistent, bump `INNERTUBE_CLIENT_VERSION` in `harvest.py` |
| `search` empty for a query | yt-dlp bot-check or too-narrow query | broaden the query; if all queries fail, the IP may be flagged — try later |
| `gate-speech` → most picks `silent`/`unknown` | yt-dlp bot-check / IP flagged (extraction failing), not genuinely silent | verify one by hand; if extraction is broken, gate can't vouch — say so and lean on judgment, don't drop everything |
