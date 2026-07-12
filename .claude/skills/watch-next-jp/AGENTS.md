# Agent guide

This directory **is a skill for you** (a CLI AI coding agent). The user drives it
by asking for JAPANESE-immersion video recommendations — e.g. "/watch-next-jp",
"/watch-next-jp about <topic>", "what Japanese video should I watch next",
"find me something new to immerse in".

When that happens, **read [`SKILL.md`](SKILL.md) and follow it end to end.** It is
the complete playbook: read the user's taste, expand it into ~15–20 native
Japanese search queries, harvest candidates, rank/diversify them, run the speech
gate, and present a short list of URLs with a one-line reason each. The judgment
is *yours* — there is no LLM API in this project; you are the intelligence.

## The one tool

Everything runs through `harvest.py`. Use the repo's virtualenv Python if it
exists, else any Python 3.10+ with `requests`:

```sh
PY="$( [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3 )"
$PY harvest.py seeds        # the user's taste bootstrap (JSON)
$PY harvest.py run …        # crawl related/search/rss edges
$PY harvest.py list …       # the candidate pool
$PY harvest.py gate-speech … # drop speechless picks (run before presenting)
$PY harvest.py set-status … # record outcomes so nothing re-surfaces
```

Run all commands from the repo root. Full semantics, scoring rubric, the
synthetic-TTS filter, and failure modes are in [`SKILL.md`](SKILL.md) — defer to
it over this summary.

## Preflight

If `harvest.py seeds` returns empty `rated` **and** empty `channels`, there's no
taste to learn from yet — tell the user to seed `data/taste.json` (a few liked
videos/channels is enough; see `taste.example.json`) before recommending.
