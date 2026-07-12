# recommend — an AI-driven "what Japanese video should I watch next?" skill

> **Vendored copy — read this first.** This is a *copy* (not a symlink, not a
> submodule) of https://github.com/abalint/recommend, installed here as the
> ray-os project skill **`watch-next-jp`**. Renamed because bare `recommend` is
> too generic a trigger. Upstream's `/recommend` in the text below is
> `/watch-next-jp` here; `SKILL.md` and `AGENTS.md` are already updated — this
> README is left close to upstream on purpose, as the provenance record.
>
> It is a copy so that a `git pull` can never silently rewrite `SKILL.md`, which
> is a file your agent *executes as instructions*. To take an upstream update:
> clone it fresh somewhere scratch, `diff` `SKILL.md`/`AGENTS.md`/`harvest.py`,
> and copy over deliberately. Audited clean as of 2026-07-12 (only network calls
> are to youtube.com; no eval/exec, no credential access, no exfiltration).
>
> Ray's `data/` (taste.json + discover.db) is gitignored and stays local.

A curiosity engine for Japanese listening immersion, built to be **driven by a
CLI AI coding agent** (Claude Code, Cursor, Codex, Aider, …). You type
`/watch-next-jp` at your agent; it reads your taste, invents native-Japanese search
queries, crawls YouTube's public graph, ranks and diversifies the results, and
hands you a short list of videos with a one-line reason for each.

The design is a deliberate **dumb-tool + smart-agent split**:

- **`harvest.py`** is the dumb tool. It pulls raw candidate videos from YouTube's
  *unauthenticated* graph and stores them. No key, no account, no cloud calls.
- **The agent** is the brain. It follows [`SKILL.md`](SKILL.md) — expanding your
  taste into ~15–20 Japanese search terms (the part a human can't easily do:
  the genre vocabulary is *cultural*, not translational), then judging, ranking,
  and diversifying candidates against what you've liked.

There is **no LLM API key anywhere in this project.** The intelligence is
whichever agent runs the playbook — so you pay nothing extra and nothing leaves
your machine except anonymous requests to YouTube.

> Extracted from a larger personal immersion pipeline. In the original, your
> taste came from a database of post-watch surveys; here it's a plain
> [`taste.json`](taste.example.json) you maintain, so it runs standalone.

---

## Quickstart (with a CLI AI agent — the intended path)

```sh
git clone https://github.com/abalint/recommend.git
cd recommend

# 1. Prereqs: yt-dlp on PATH + a venv with requests
brew install yt-dlp                       # or pipx install yt-dlp
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 2. Seed your taste (a few videos/channels you like — that's enough to start)
cp taste.example.json data/taste.json
$EDITOR data/taste.json

# 3. Make the skill discoverable to your agent (Claude Code shown)
mkdir -p ~/.claude/skills && ln -s "$(pwd)" ~/.claude/skills/recommend
```

Now, from inside this repo, just ask your agent:

> **`/recommend`** — an open curiosity pass, breadth across genres
> **`/recommend about 廃線跡`** — same engine, narrowed to a topic
> **`recommend me 5 things to watch`**

The agent walks the [`SKILL.md`](SKILL.md) steps end to end and replies with
something like:

```
1. 【廃線探訪】旧国鉄・倉吉線の廃線跡を歩く · 山あるき
   Same quiet-walk-with-narration lane as your ★5 京都散歩; new topic (haikyo).
   https://www.youtube.com/watch?v=…

2. 限界集落に一人で暮らす93歳 · ドキュメンタリー堂
   Wildcard — a cluster you've never sampled; calm solo speaker, clear delivery.
   https://www.youtube.com/watch?v=…
…
```

Any agent that can read a Markdown playbook and run shell commands works —
`SKILL.md` is just instructions. You can also drop it into an `AGENTS.md`-aware
tool (this repo ships one) or follow it yourself.

---

## How it works

```
  harvest.py (dumb tool)                       the AGENT (judgment, no API key)
  seeds ─► run(related + search + rss) ─────► [ expand · judge · rank · diversify ] ─► picks
            │                                          │
      YouTube graph, unauthenticated          taste.json + rated history
      → discover.db (candidate pool)          → JP queries, scoring, clustering
```

Three harvest edges, all reachable without login:

| edge | source | what it gives you |
|---|---|---|
| **related** | InnerTube `/next` watch-next rail | content-similar videos around ones you liked (a *similarity* edge, **not** personalized) |
| **search** | `yt-dlp ytsearch` | the landing pad for the Japanese queries the agent writes from your taste — the highest-leverage step |
| **rss** | a channel's `feeds/videos.xml` | fresh uploads from channels you follow |

Then two filters keep the list worth watching:

- **Format blocklist** (deterministic) — drops synthetic-TTS narrator formats
  (ゆっくり解説 / VOICEROID / ずんだもん …), poor listening material for many
  learners. On by default; fully configurable.
- **Speech gate** (`gate-speech`) — probes each shortlisted pick with yt-dlp and
  drops silent / music-only / non-Japanese videos, because a *listening* pick
  with nothing to hear is worthless. (It reads YouTube's ASR language signal:
  Japanese speech ⇔ a `ja-orig` auto-caption / `language=ja`.)

Why not just use YouTube's own recommendations? The personalized feed is
unreachable without logging in, and it optimizes watch-time and centroid
convergence — the opposite of a novelty-seeking curiosity engine. The reachable
public edges (similarity rail, search, RSS) are the right raw material; the
*curation* is what the agent adds.

---

## Your taste file

[`taste.json`](taste.example.json) is the one thing you maintain. Minimum viable
is a couple of liked videos and channels:

```json
{
  "liked_video_ids": ["<a youtube id you loved>"],
  "channels": [
    { "channel": "…", "channel_id": "UC…", "follow_state": "more",
      "profile": { "characterization": "calm mid-register solo narrator, dry humor" } }
  ]
}
```

The richer you make it — per-video ratings, sub-axis scores, a presenter
"fingerprint" per channel — the sharper the agent's ranking. Every field beyond
the two above is optional; see [`taste.example.json`](taste.example.json) for the
full shape and [`taste.example.md`](taste.example.md) for an optional prose
digest the agent can also read. Your real `taste.json` lives in `data/` and is
gitignored, so **your watch history never ships**.

---

## Using the tool directly (no agent)

Everything the agent does is just these CLI verbs:

```sh
PY=.venv/bin/python

$PY harvest.py seeds                                       # your taste bootstrap (JSON)
$PY harvest.py run --related VIDEOID \
                   --search "散歩 vlog" "廃墟 探訪" \
                   --rss UCxxxx                            # crawl the three edges
$PY harvest.py list --status new                           # the candidate pool (JSON)
$PY harvest.py gate-speech VID1 VID2 VID3                  # drop speechless picks
$PY harvest.py set-status VID dismissed                    # record an outcome
$PY harvest.py list --status filtered                      # what the blocklist caught
```

No config file is required — data defaults to `./data/`. Override the location
with a `config.json` (`{"data_dir": "…"}`) or `HARVEST_DATA_DIR`, and tune the
format blocklist there too (see [`config.example.json`](config.example.json)).

---

## Project layout

| file | what it is |
|---|---|
| [`SKILL.md`](SKILL.md) | **the agent playbook** — the actual recommendation logic |
| [`AGENTS.md`](AGENTS.md) | pointer so any AGENTS-aware CLI agent finds the skill |
| `harvest.py` | the dumb tool: harvest edges, discovery store, speech gate |
| `paths.py` | resolves `yt-dlp` from PATH |
| `config.py` | resolves the data dir + optional `config.json` |
| `taste.example.json` | template for your taste input |
| `taste.example.md` | template for an optional prose taste digest |
| `config.example.json` | template for optional overrides |
| `data/` | your discovery db + `taste.json` land here (gitignored) |

---

## Requirements

- **Python 3.10+** with `requests` (`pip install -r requirements.txt`)
- **yt-dlp** on your PATH (`brew install yt-dlp`, `pipx install yt-dlp`, …)
- A CLI AI coding agent to drive it (optional — you can run the verbs yourself)

## Notes & limits

- **The similarity rail drifts by design** — re-running `run --related` on the
  same seed surfaces *more* of that neighborhood each call; the store dedupes, so
  it only ever grows. Re-harvest freely.
- **InnerTube versions drift.** If `related` starts returning empty, bump
  `INNERTUBE_CLIENT_VERSION` at the top of `harvest.py` (yt-dlp bumps theirs the
  same way).
- **YouTube rate-limits aggressive extraction.** If `search` / `gate-speech`
  mostly fail or return `unknown`, your IP is likely being bot-checked — back off
  and retry later; the gate never drops a video on a failed probe.
- **The speech gate proxies "has speech" via captions**, valid only while you
  rely on those captions. If you later transcribe caption-less videos yourself,
  switch the gate to an audio-based signal or it will wrongly drop
  caption-less-but-spoken videos.
- This crawls **public, unauthenticated** YouTube endpoints. Be a good citizen:
  it's for personal discovery, not bulk scraping.

## License

Public domain — [The Unlicense](LICENSE). Do whatever you want with it; no
attribution required. (`taste.json` — your watch history — is gitignored so it
doesn't ship; still worth a sanity pass for personal data before publishing a
fork.)
