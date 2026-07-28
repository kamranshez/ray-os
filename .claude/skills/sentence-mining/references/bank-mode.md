# Bank mode

**Input:** a list of target words. **Output:** one new card per word.

> "I keep forgetting 同期, give me a card."

Video mode is for when Ray has a *specific clip* he wants to mine. Bank mode is the other
direction: he names the words, and the skill goes and finds a good sentence for each.

**Everything after SOURCE is [the shared pipeline](pipeline.md).** This file only covers the
two stages that differ.

## Triggers

- Ray pastes a list of Japanese words: "make cards", "mine these", "find sentences for"
- Ray names one word he keeps forgetting
- `/sentence-mining` with no URL and a list of words

A URL instead → [video mode](video-mode.md). A word that **already has a card** →
[replace mode](replace-mode.md) (the ask is a *better* sentence, not a new card).

**"leech these" is NOT a bank-mode trigger** — it used to be listed here and it never worked.
Every leech already has a card, and `find_sentences.py` skips any word that does, so the whole
list came back as misses reading "already has a card". Leeches go to
[leech mode](leech-mode.md).

---

## 1 · SOURCE — word list → the cascade

```bash
python3 <skill-dir>/scripts/find_sentences.py \
    --words "同期,西暦,和暦" \
    --output <work>/banksearch.json
```

Per word, in order:

1. **Skip if a card already exists** in the mining decks. (`push.py` sets
   `allowDuplicate: False` so it'd be rejected at the end anyway — catching it here means we
   don't burn a cascade lookup and a TTS call on it first.)
2. **Warn if the word is already known** — an exact lemma/normalized match at or above the
   maturity threshold — but **build the card anyway**. Ray typed this word on purpose, and the
   known-word diff is a hint about sequencing, never a verdict on worth (and it is wrong
   sometimes). `--skip-known` refuses instead. See
   [pipeline.md §ROUTE](pipeline.md#6--route).
3. **Run [the cascade](pipeline.md#the-sentence-cascade)** — Immersion Kit → Nadeshiko →
   sentencesearch → kotu → local bank, re-ranked by Ray's own i+1.
4. **Route by i-level** — `i1` → main deck, anything denser → deferred. (Same rule as video
   mode. Pass `--no-defer-above-i1` to force everything to main.)

Words with no usable hit anywhere become **misses** — report them; don't invent a sentence.

Other flags: `--words-file <path>` (one word per line, extra columns ignored, so a pasted leech
export just works) · `--top N` runner-ups per word · `--refresh-known`.

### Why this replaced the old bank-only search

Until July 2026 this mode called `search_banks.py --words`, which searched **only the local
`.apkg` banks** — the *last* tier of the cascade — using its own scoring table, substring-only
matching, and no known-word check at all. Replace mode, meanwhile, had the full five-tier
cascade with i+1 re-ranking. The same word therefore produced a measurably **worse** card
through bank mode than through replace mode, which is exactly backwards.

Both now call the same `_sources.best_for_word()`. `search_banks.py` still exists and still
does the within-bank ranking, but it is reached **only as tier 5 of the cascade**, never as
the whole search.

The trade-off Ray accepted: sentences now come from the web tiers far more often than from his
own indexed shows, so fewer cards carry a subs2srs screenshot from a series he's actually
watching. Coverage and i+1 quality won out. The bank tier is still there and still preferred
over nothing — it just has to earn the slot.

---

## 4 · MEDIA

```bash
python3 <skill-dir>/scripts/generate_media_bank.py \
    --candidates <work>/banksearch.json \
    --output <work>/bank.draft.json
```

Stages each candidate's clip and screenshot. The cascade hands over `sound_url` / `image_url`,
which are **URLs** for the web tiers and **local file paths** for the bank tier — one `_stage`
helper handles both, so which tier a sentence came from stops mattering once it's been chosen.
Then Gemini-TTS the explanation.

The audio-only tiers (sentencesearch, kotu) ship no image; `push.py` writes the `。` filler.
That's the normal path, not an error — see [pipeline.md §MEDIA](pipeline.md#4--media).

Sentence TTS is now a *fallback*, not a routine step: every cascade tier requires native audio,
so it only fires for a legacy draft or a hand-edited candidate with no source clip.

---

## 5 · WRITE

```bash
python3 <skill-dir>/scripts/push.py --draft <work>/bank.draft.json
```

Standard `addNotes`. Tagged `claude-sentence-bank` + the i-level.

> The `claude-sentence-bank` tag predates the cascade, so it now means **"mined from a word
> list"**, not "sourced from a local bank". Kept as-is for continuity with the cards already
> in Ray's collection.

Then **[Step 7 · QUEUE](pipeline.md#7--queue--offer-this-every-mode-every-time)** — offer it,
every time.

### Summary shape

```
Pushed 3 cards from a word list ✓

  → Sentence Mining (i+1): 2
    1. 皮算用 [nadeshiko] 🔊🖼 "交渉は皮算用で行えます"
    2. 泰然  [nadeshiko] 🔊🖼 "どうして こんな泰然としていられるんだ?"

  → Deferred (i+2 and above): 1
    3. 面食らう [i2] [nadeshiko] 🔊🖼 "予備知識 ねえと 面食らうのも当然か"

  Misses: 和暦 — no usable sentence in any tier.
  Skipped: 同期 (already has a card).
```

---

## One-time setup: indexing banks (cascade tier 5)

Banks are the `.apkg` files in `config.banks.source_dir` (set at setup):

```bash
python3 <skill-dir>/scripts/extract_bank.py                      # all of source_dir
python3 <skill-dir>/scripts/extract_bank.py "/path/to/one.apkg"  # or just one
```

Output lands in `config.banks.index_dir` (default `~/Downloads/sentence-mining/banks/index/`):
`<bank-id>.notes.json` (one record per note: sentence, audio/image refs, meaning) and
`<bank-id>.media/`. The `<bank-id>` derives from the filename (NFC-normalized). See
[bank-formats.md](bank-formats.md) for known notetypes and [apkg-schema.md](apkg-schema.md) for
the ZIP/SQLite layout.

**Re-extraction is safe** — `cp -n` semantics for media, JSON overwritten. Re-run when Ray adds
a bank. **Big banks are slow**: a 1GB audiobook bank is mostly mp3s and extraction copies all
of them.

## Gotchas

- **The bank tier is substring-only.** `言う` won't match a sentence containing `言って`. A real
  fix needs SudachiPy tokenization at index time with per-note lemma sets. Not done. This
  matters much less now that the bank is tier 5 rather than the whole search.
- **`Migaku Japanese`'s Audio field is often empty** even though the notetype declares it. The
  detector says the bank "has audio" structurally, but resolution at media time finds nothing
  and the candidate is dropped from the bank tier. Correct behavior — just don't be surprised
  that a "Migaku" bank contributes fewer hits than its size suggests.
