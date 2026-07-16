---
name: x-thread-miner
description: >-
  Fetch the replies and/or quote tweets for one or more individual X/Twitter
  posts, then mine them for OUTLIER ideas — non-obvious takes, contrarian
  theses, sharp objections, and novel framings — and render them into a
  navigable HTML artifact with pin/group/export. Use this whenever the user
  points at one or more tweets (URLs or ids) and wants to know what people
  are saying back, gather the reactions, harvest the replies and quote tweets,
  see how a feature or idea is being received, or turn viral threads into
  research. Trigger on phrases like "mine this tweet", "get the replies and
  quotes for this", "what are people saying under these posts", "pull the
  quote tweets", "gather reactions", "what's the discourse on this", "find
  outliers", "what's the non-obvious take", or any time the user shares
  tweet links and wants the conversation around them distilled rather than
  just the tweets themselves. Always quiz the user first on whether they
  want quote tweets, replies, or both. Use this even when the user does
  not say "API" or "scrape" — if they want the conversation around tweets
  turned into insight, this is it.
---

# X Thread Miner

Turn the conversation *around* a tweet into structured research. Most of the
signal about how an idea, launch, or take is landing lives not in the tweet but
in its replies and quote tweets, scattered across hundreds of posts in several
languages. This skill fetches that engagement, mines it adversarially for
**outlier ideas** (the consensus thesis is filtered out on purpose — the user
already knows that part), and renders the result into a self-contained HTML
artifact the user can browse, pin, and export from.

## The flow

1. **Quiz** — ask what to fetch and how deep.
2. **Fetch** — paginated, ranked-by-reach harvest of replies + quotes (+ deep layer).
3. **Mine outliers** — bundled Workflow does extract → adversarially verify → cluster + synthesize.
4. **Render HTML** — bundled Python builder turns the workflow result into an interactive artifact with pin tray, persistence, copy-to-clipboard, and Markdown export.
5. **Report back** — open in Chrome, summarize the headline outliers.

## Step 1 — Quiz the user first (always)

Before fetching anything, ask with `AskUserQuestion`. Quote tweets and replies
are different conversations — quotes are people broadcasting their own take to
their own audience (more framings, more reach), replies are direct responses
(more questions, objections, quick reactions).

Ask these in one call:

1. **What to fetch** (required): "Quote tweets only" / "Replies only" / "Both".
2. **Depth**: "Surface" (just anchor replies/quotes) or "Deep" (also pull
   replies *under* the top quote tweets — second-order use cases hide here,
   costs more API calls). Default to Surface unless the user wants exhaustive
   coverage.

If the user already specified mode in their message, skip that question and
confirm depth only.

## Step 2 — Fetch

```bash
python3 <skill-dir>/scripts/fetch_engagement.py \
  --tweet "<url-or-id>" [--tweet "<another>"] \
  --mode {replies|quotes|both} \
  [--deep N] \
  --out "<output-dir>"
```

- `--mode` comes from the quiz answer.
- `--deep N` only when the user chose Deep (N = how many top quote tweets to
  dig under; 15–22 is a good range).
- The key is read from `$RAPIDAPI_KEY` or `~/.rapidapi_key` automatically. If
  the script reports no key, ask the user to put their RapidAPI key in
  `~/.rapidapi_key` (kept out of the skill on purpose so it never syncs to git).
- If the sandbox blocks network ("failed to change group id" or similar),
  rerun with the sandbox off.

Outputs land in `--out`:
- `data/<author>_<id>.json` — anchor + replies + quotes per anchor tweet.
- `data/quote_replies/*.json` — the deep layer, if `--deep` was used.
- `surfaced.md` — top tweets ranked by author reach (still produced; useful
  for a quick sanity check before the workflow runs).
- `summary.json` — counts per anchor.

For multi-tweet runs, the fetch can be slow (deep + many anchors = a few
minutes). Run it via Bash `run_in_background: true` so the user can keep
chatting; you'll be notified on completion.

## Step 3 — Mine outliers via the bundled Workflow

Once fetching finishes, invoke the bundled workflow:

```
Workflow({
  scriptPath: "<skill-dir>/scripts/mine_outliers.workflow.js",
  args: {
    dataDir: "<absolute path to the --out dir from Step 2>",
    topic: "<short description of what the user is researching>",
    consensusThesis: "<optional: the obvious take to filter out; otherwise inferred>",
  }
})
```

The workflow:
1. **Discover** — lists `dataDir/data/*.json`, reads each anchor's text, and
   states the **consensus thesis** for the topic (the obvious take that's
   NOT an outlier — used as the rejection criterion by every extraction
   agent). If the caller passes `consensusThesis`, the discovery agent
   refines/uses it; otherwise it infers from anchor texts.
2. **Extract** — fans out one agent per anchor. Each reads its full anchor
   JSON (anchor + replies + quotes + deep-layer files keyed by quote id)
   and returns up to 7 outlier candidates in 6 categories: contrarian-thesis,
   novel-use-case, sharp-objection, mental-model, specific-tooling,
   meta-observation. Quote tweets are weighted over replies.
3. **Verify** — for every candidate, an adversarial skeptic tries to refute
   it. Default verdict is *reject* unless the verifier is confident (≥0.6)
   the idea is genuinely non-obvious vs the consensus.
4. **Synthesize** — one agent clusters survivors into themes and writes a
   structured report.

The workflow returns:
```json
{
  "topic": "...",
  "consensus_thesis": "...",
  "stats": { "anchors": N, "candidates_extracted": N, "candidates_verified": N, "candidates_rejected": N },
  "report": {
    "headline":         [ ...3-5 most important outliers... ],
    "themes":           [ ...5-10 named clusters with supports... ],
    "mental_models":    [ ...one-liners worth stealing verbatim... ],
    "sharpest_objections": [ ...steelmanned skeptic case... ],
    "specific_tooling": [ ...concrete named files, slash commands, libs... ]
  },
  "verified_outliers": [ ...all survivors, full records... ],
  "all_candidates":    [ ...everything pre-verification, for transparency... ]
}
```

After the workflow returns, **write the full result to disk**:

```
<dataDir>/workflow-result.json
```

so the HTML builder can read it and so the user has an archival copy.

## Step 4 — Render the HTML artifact

```bash
python3 <skill-dir>/scripts/build_outlier_html.py \
  --result <dataDir>/workflow-result.json \
  --out <dataDir>/outlier-report.html
```

Then open it:

```bash
open -a "Google Chrome" <dataDir>/outlier-report.html
```

The HTML artifact has:
- Header with the consensus thesis explicitly called out (so the user can
  see what's been filtered).
- Stats row.
- 6 navigable sections: **The 5** (hero outliers), **Themes**, **Mental
  models**, **Objections**, **Tooling**.
- Pin button (☆) on every item.
- Sticky sidebar **Pin tray** with three actions:
  - **📋 Copy Markdown** — copies all pinned items to clipboard.
  - **⬇ Download .md** — saves `outlier-pins.md`.
  - **Clear all**.
- Pins persist in `localStorage` so the user can close the tab and come back.

## Step 5 — Report back

Tell the user where the HTML is, surface the 5 headline outliers as a quick
preview (1-line each), and note the pin/copy/export controls. They take it
from there.

## Notes

- **Why mine outliers and not everything**: 2,000+ tweets is too much for any
  reader. The user already knows the consensus thesis (whatever drove them to
  collect these tweets). What they need is the *non-obvious* — counter-takes,
  specific receipts, novel framings, named tools. The workflow's adversarial
  verify step exists to keep noise out: the default is to reject anything
  that's just a rephrasing of the consensus.
- **When to skip the workflow**: if the user explicitly asks for a quick
  surface read (e.g. "just give me the top replies by reach"), skip Steps 3–4
  and just read `surfaced.md` directly. The workflow is for when the user
  wants insight, not headlines.
- **Iteration**: if the workflow's consensus_thesis came out wrong, re-invoke
  with an explicit `args.consensusThesis` and the resume option to cache
  unchanged steps. (See the Workflow tool's resume flag.)
- **Endpoints reference**: for the exact API endpoints, fields, pagination,
  and the quote-tweet trick (`search.php?query=quoted_tweet_id:<id>`), see
  `references/endpoints.md`. The fetcher handles all of it, but the
  reference is there for endpoints the script doesn't wrap (trends,
  community posts, user timelines, etc.).
- **Non-English content**: the extraction agents are instructed to translate
  JP/CN/KR/etc. tweets in their head before deciding outlier-ness. Don't
  skip them — the non-English wave is often where independent confirmation
  of a pattern shows up.
