# Known words — the built-in i+1 diff (no AnkiMorphs)

The whole point of i+1 mining is to only make cards for words the learner does
**not** already know. This skill computes the "known" set itself — it does **not**
read `ankimorphs.db` and does **not** require the AnkiMorphs add-on to be
installed. (Historically it read AnkiMorphs' SQLite DB; that coupling was removed
so the skill is self-contained and shareable.)

## How "known" is computed

Configured in `config.json` under `known_words`:

```jsonc
"known_words": {
  "interval_threshold": 21,   // a lemma is "known" once its highest card interval >= this
  "cache_hours": 6,           // reuse the scanned set for N hours (0 = always rescan)
  "sources": [
    { "query": "note:\"My Mining\"", "field": "sentence" },
    { "query": "note:\"Core 2k/6k\"", "field": "Vocabulary-Kanji" }
  ]
}
```

For every source (`analyze.py` → `load_known_intervals`):

1. `findCards(query)` — `query` is any Anki search (deck, note type, tag…).
2. `cardsInfo` in chunks of 500 → for each card, read the `field` value and the
   card's `interval`.
3. Strip HTML and `漢字[furigana]` annotations, then tokenize the field with
   **SudachiPy** (SplitMode C).
4. For each content lemma, record its **highest** card interval across all cards
   (this is exactly AnkiMorphs' `highest_lemma_learning_interval`).

A lemma counts as **known** when that highest interval ≥ `interval_threshold`.
New/learning cards report interval ≤ 0 (or seconds), so they fall below the
threshold and stay "unknown" — i.e. learning words still count as mineable, which
matches the original behaviour.

### Why SudachiPy (and why same-tokenizer matters)

The miner tokenizes the *mined* sentences with the same `tokenize()`. The *known*
set is built with the **same tokenizer**, so a lemma the learner knows is spelled
identically in both places — no cross-tokenizer leakage where a known word slips
through as a false "unknown".

SudachiPy (SplitMode C) was chosen over mecab+ipadic and fugashi+unidic after a
head-to-head benchmark on Ray's 12.7k known-word cards (see the migration note
below). It wins on every axis that matters here: ~180× faster (in-process, no
subprocess spawn per sentence — the known-set tokenize dropped from ~60s to ~1s),
correct on hard conjugations where ipadic fails (`籠もって` → ipadic gives `籠`/`もつ`,
Sudachi gives `籠もる`), and SplitMode C keeps meaningful compounds whole
(`警察官`, `被写体`, `美少女` as single vocab words instead of `警察`+`官`), which
both improves card quality and gives the lowest single-kanji-fragment rate.

Beyond the raw interval check, `analyze.py` also treats a lemma as known if:
- a spelling **variant** is known — done via SudachiPy's `normalized_form()`, which
  collapses orthographic variants to one canonical form, so knowing 籠る marks
  こもる known (both normalize to 籠もる). This is built into the tokenizer and
  replaced the old jamdict alt-form lookup (dropping the `jamdict`/`jamdict-data`
  dependency); and
- its leading **kanji stem** appears among mature kanji stems — catches inflected
  or compound forms.

(Migration benchmark on Ray's collection: each tokenizer's recomputed known-set
vs the old `ankimorphs.db` gold scored Jaccard 0.78 (ipadic) / 0.64 (unidic) /
0.61 (Sudachi). ipadic "wins" agreement only because the gold was *itself* built
with ipadic — it measures dictionary-sameness, not correctness. Since the skill
now recomputes the known-set self-consistently and a friend starts with no
`ankimorphs.db` at all, forward-looking accuracy/speed/compound-handling were the
deciding factors, all of which favor Sudachi. Expect a one-time ~24% shift in the
known-set the first time you switch — it self-corrects as you review.)

## Choosing sources (what AnkiMorphs called "note filters")

Mirror whatever fields actually contain Japanese the learner has studied:
- the **sentence-mining deck's** sentence field (captures every morph seen in
  context — the big one);
- any **vocab decks** (the word/expression field); tokenizing a single-word field
  just yields that word, so it works uniformly.

If migrating from AnkiMorphs, its configured note filters live in
`addons21/<ankimorphs-id>/meta.json` under `config.filters` (each has `note_type`
+ `field`). Translate each to `{ "query": "note:\"<note_type>\"", "field": "<field>" }`.
Drop any whose note type now has 0 cards.

## Threshold

`interval_threshold` default is **21** — the universal AnkiMorphs convention for
"mature/known". Raising it makes the skill mine more aggressively (treats fewer
words as known); lowering it mines less.

## Caching

Scanning a large collection (10k+ sentence cards) takes ~30s on a cold run — now
dominated by the AnkiConnect pull of card data, not tokenization (SudachiPy chews
through the whole set in ~1s). The result is cached at `<work_dir>/.known_cache.json`,
keyed on the exact `sources` list (so editing config auto-invalidates) and the
threshold, with a TTL of `cache_hours`. Force a rescan with
`analyze.py --refresh-known`. In manifest (multi-video) mode the known set is
loaded once and shared across all videos regardless of cache.
