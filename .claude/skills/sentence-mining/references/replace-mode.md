# Replace mode

Fix **existing** cards whose example sentence is bad — too short, a mid-conversation
fragment, a tokenizer/proper-noun false positive (e.g. a card for 紅葉 "autumn leaves"
that actually shows 紅葉くん, a character name), or just incomprehensible standalone.
Replace mode swaps in a better, more comprehensible sentence **in place** and archives
the old one. It does NOT create new cards (that's bank/video mode).

## Canonical source order: Immersion Kit → Nadeshiko → sentencesearch → kotu → local sentence bank

This is the order the skill **always** uses for finding example sentences — both here
(fixing struggled-with cards) and for new-card mining. Each tier is tried only if the
previous yields nothing usable *for Ray*. IK/Nadeshiko ship a screenshot; tiers 3–4 are
**audio-only web corpora** (no image — `score_candidate(require_image=False)`, and
`replace_apply` writes the picture's `。` filler) with far broader coverage; the local
bank is the indexed-subset last resort:

1. **Immersion Kit** (`apiv2.immersionkit.com`) — broadest corpus, anime-skewed. A June
   2026 head-to-head on 12 flagged leeches: IK won 9, tied 1, **0 misses** vs the local
   index's 3. Ships translation + audio + image; `sort=sentence_length:asc` + a length
   floor skips `(speaker) word word` subtitle junk.
2. **Nadeshiko** (`api.nadeshiko.co`, needs `NADESHIKO_API_KEY`) — drama-heavy corpus
   that covers formal/abstract words IK's anime corpus misses. Recovered `奉る`, `証券`,
   and the *real* `紅葉` (autumn leaves, not the character name) in testing.
3. **sentencesearch.neocities** — the site ships its whole ~45k-sentence corpus as one
   static JSON (`/data/all_v11.json`) it searches client-side, so `load_sentencesearch`
   mirrors that file into `work_dir/cache/` once a month and substring-searches it
   locally (no per-word HTTP, no rate limit). Clean JLPT-tango / Anki-core native audio
   at `receptomanijalogi.web.app/audio/<audio_jap>`; no image. Each record is
   `{source, audio_jap, jap, eng}`.
4. **kotu.io** (`api.kotu.io/v2/media/anki/subtitles?q=<word>`) — huge TV / anime / news
   / audiobook corpus, live API. Each `item` has `text`, `externalFile.id` (clip audio at
   `api.kotu.io/v2/media/audio/external/<id>`), and `video.title` (source). No gloss, no
   image. Substring (not exact) match, so `looks_misleading` earns its keep dropping
   `鉱山`-in-`住友金属鉱山` compound hits.
5. **Local sentence bank** — the indexed subs2srs `.apkg` banks (bank mode's corpus),
   media served from local files. Last resort; only what's been indexed.

None of these know what *Ray* knows, so `replace_search.py` grafts that back on: every
candidate from every tier is tokenized with the same SudachiPy + known-word machinery as
`analyze.py` and ranked by how few OTHER words are unknown (true i+1 for Ray, not generic
JLPT). A candidate **identical to the card's current sentence** is dropped (no
improvement) — which is why a word whose only hit is already on the card is reported as a
genuine miss rather than a no-op "replacement".

## API

Live endpoint (the documented `api.immersionkit.com` is a dead PythonAnywhere
placeholder — do NOT use it):

```
GET https://apiv2.immersionkit.com/search
  q=<word>  exactMatch=true  sort=sentence_length:asc  showUrlInMedia=true  limit=30
```

Returns `examples[]` with `sentence`, `sentence_with_furigana`, `translation`,
`word_list`, `image` (URL when `showUrlInMedia=true`), `sound` (URL), `title`, `id`.
Media is on a Linode CDN — downloadable even when the API itself is throttling.

**Rate limiting:** apiv2 throttles bursts hard (you'll see `No route to host` /
timeouts on apiv2 specifically while the rest of the internet is fine). `replace_search.py`
does ALL words in one process with a single connection — let it run; do NOT fire ad-hoc
`curl` loops alongside it or you'll get the IP throttled. If throttled, wait ~3–5 min.

**Nadeshiko (tier 2):**

```
POST https://api.nadeshiko.co/v1/search          Authorization: Bearer <NADESHIKO_API_KEY>
  body: {"query":{"search":"<word>","exactMatch":true},"take":30,
         "sort":{"mode":"ASC"},"filters":{"category":["ANIME","JDRAMA"]}}
```

Returns `segments[]`; each has `textJa.content` (sentence), `textEn.content`
(translation), `urls.imageUrl` / `urls.audioUrl`. `take` max is ≤50 (60 → HTTP 400).
`replace_search.py` normalizes these into the same shape as IK so the scorer/filters are
identical. Key from https://nadeshiko.co/user/developer (scope `READ_MEDIA`).

## Steps

### Step 1 — find the candidates (read-only)

**Flag convention:** Ray marks struggling cards with **flag:1** (input queue). Replace
mode reads flag:1 and, after he confirms, **clears the flag** on each redone card so it
just rejoins the study queue (it's reset to due, so it queues up next — no separate review
bucket). Genuine misses stay on flag:1 so they remain in the "still needs fixing" bucket.
(Override with `--done-flag N` if you ever want the redone set on a colored flag instead.)

```bash
python3 <skill-dir>/scripts/replace_search.py \
  --flag 1 \                                  # OR --note-ids a,b,c  OR --words 同期,西暦
  --output ~/Downloads/sentence-mining/replace.json
```

- `--flag N` operates on every card flagged N in the mining decks (default input: flag:1).
- `--words` resolves each word to its existing card in the mining decks.
- Set `NADESHIKO_API_KEY` in `.env` to enable tier 2; tier 3 needs indexed banks
  (`config.banks.index_dir`). The script logs which fallbacks are active.
- It spaces IK requests (`REQUEST_DELAY`) and backs off on HTTP 429 — apiv2 throttles
  bursts hard. Don't fire ad-hoc `curl` loops alongside a run.
- First run scans the known-word set (~100s, then cached — see [known-words.md](known-words.md)).
- Filters applied per candidate: target present as a **bare token** (drops compound-swamp
  like 攻撃抑制 for 抑制), not glued to adjacent kanji, not a name (紅葉くん), not a
  mis-teaching idiom (聞いて呆れる), has BOTH image and sound, length 10–45 chars.
- Ranks by (fewest other-unknowns, bare-token, closest to ~22 chars). Keeps runner-ups.
- Words with no usable hit go to `misses` (each carries its `note_id`). Abstract/
  financial/archaic words (称える, 奉る, 咥える, 証券) are the usual misses — anime corpora
  just don't carry a clean simple sentence for them; that's expected, report them.
  These are **retired** at apply time (see Step 4): an unfixable card isn't worth Ray's
  review time, so it's tagged `not-worth-learning`, suspended, and dropped off flag:1.

Read `replace.json`. **Curate (Step 1.5):** spot-check the top pick per word the same way
Step 3.5 does for mining. The filters catch most junk, but you still judge: is the target
in its normal sense? Complete sentence? If the top pick is weak, look at `runner_ups[]`
and swap it in (overwrite the entry's `new_sentence` / `translation` / `image_url` /
`sound_url` / `ik_id` / `i_level` from the chosen runner-up), or drop the entry entirely.

### Step 2 — write explanations (Claude, inline)

For each entry, write the `explanation` field using the **exact same prompt** as Step 4 of
the main flow (see [explanation-prompt.md](explanation-prompt.md)) over the entry's
`word` + `new_sentence`. Keep under ~250 JP chars. Drop any entry you can't explain.

### Step 3 — review gate (ALWAYS confirm — every run)

Replace overwrites cards Ray has already studied, so it **never** auto-applies. **Every
run**, show the old→new table and wait for his explicit OK before applying — no exceptions:

```bash
python3 <skill-dir>/scripts/replace_apply.py --draft ~/Downloads/sentence-mining/replace.json --dry-run
```

Present the table; let Ray drop/swap any (edit the draft JSON accordingly). Only proceed
to Step 4 once he confirms — the per-run confirmation is mandatory.

### Step 4 — apply in place

```bash
python3 <skill-dir>/scripts/replace_apply.py --draft ~/Downloads/sentence-mining/replace.json
```

Per card this:
- stages the chosen image + audio — downloaded from a URL (IK/Nadeshiko) or copied from
  a local file (bank) — into Anki via `storeMediaFile`
- Gemini-TTS the new explanation. **Best-effort:** if the GEMINI key is missing/expired
  the card still updates with the new explanation TEXT; only `explanation_audio` is left
  empty (regenerate later once the key is refreshed). A dead key never blocks a card.
- **archives** the current sentence + its old audio/image refs into `previous_versions`
  (newest block first, dated) — so every prior version is recoverable and the old media
  never becomes "unused". Appends on each subsequent replace.
- overwrites `sentence`, `sentence_audio`, `picture`, `explanation`, `explanation_audio`
- retags the i-level (`i1`/`i2`/…) to reflect the NEW sentence's complexity for Ray
- **rehabilitates** the card so the fresh sentence is re-learned cleanly: removes the
  `leech` tag, unsuspends, `forgetCards` to reset scheduling → the card becomes due, and
  zeroes the `reps`/`lapses` counters (forgetCards alone leaves them, so a card would keep
  its lapse history and re-leech too soon)
- **clears the flag**: input `flag:1` ("fix these") → **no flag** (default `--done-flag 0`).
  The card was just reset to due, so clearing the flag lets it simply rejoin the study
  queue and come up next — no separate review bucket to babysit. Genuine misses stay on
  flag:1 (still-to-fix). `--done-flag N` (1-7) sets a colored flag instead; `--done-flag -1`
  leaves the input flag untouched. The `claude-sentence-*` tag is kept.

It also **retires the unfixable misses**: every word in `misses` (no usable replacement
in IK / Nadeshiko / bank) is tagged `not-worth-learning`, suspended, and cleared off
flag:1 — so it leaves the fix queue and `replace_search --flag 1` stops re-picking it
every run. Pass `--keep-misses` to leave them on flag:1 for a later manual pass instead.

Re-running the same draft is safe: an **idempotency guard** skips any card whose live
sentence already equals the draft's new one (no double-archiving). Media download + TTS
run concurrently; Anki writes are serialized.

Then summarize: replaced N, retired M (not-worth-learning + suspended), draft path.

### Rehabilitate a whole flagged batch (no field changes)

To de-leech + unsuspend + reset-to-due every card flagged N without changing any field
(e.g. after a batch was applied before this behavior existed):

```bash
python3 <skill-dir>/scripts/replace_apply.py --rehab-flag 3
```

## The `previous_versions` field

Added to the note type June 2026 (`config.field_map.previous_versions` → `previous_versions`).
Holds an append-only, newest-first stack of archived sentence blocks:

```html
<div class="sm-prev" data-archived="2026-06-16">傘がないので雨宿りしています [sound:OLD.mp3]<img src="OLD.webp"></div>
```

To revert a card, copy the archived sentence/audio/image back into the live fields by hand.
