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
3. Strip HTML and `漢字[furigana]` annotations, then **mecab-tokenize** the field.
4. For each content lemma, record its **highest** card interval across all cards
   (this is exactly AnkiMorphs' `highest_lemma_learning_interval`).

A lemma counts as **known** when that highest interval ≥ `interval_threshold`.
New/learning cards report interval ≤ 0 (or seconds), so they fall below the
threshold and stay "unknown" — i.e. learning words still count as mineable, which
matches the original behaviour.

### Why this is at least as good as the old AnkiMorphs read

The miner tokenizes the *mined* sentences with the same `mecab_tokenize`. Now the
*known* set is built with the **same tokenizer**, so a lemma the learner knows is
spelled identically in both places. The old setup mixed AnkiMorphs' bundled mecab
(for the known DB) with system mecab (for candidates), which could disagree on a
lemma and leak a known word through as a false "unknown". Same-tokenizer removes
that class of error.

Beyond the raw interval check, `analyze.py` also treats a lemma as known if:
- any JMDict **alternate form** (kanji/kana variant) is known — so knowing 籠る
  marks こもる known; and
- its leading **kanji stem** appears among mature kanji stems — catches inflected
  or compound forms.

(Sanity check on Ray's collection during the migration: the new set agreed with
the old `ankimorphs.db` on ~85% of known lemmas — Jaccard 0.78, 7178 vs 7624
known — with the remainder explained by mecab-dictionary lemmatization differences
and stale note types AnkiMorphs had recorded.)

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

Scanning a large collection (10k+ sentence cards) takes ~100s because every
sentence is tokenized. The result is cached at `<work_dir>/.known_cache.json`,
keyed on the exact `sources` list (so editing config auto-invalidates) and the
threshold, with a TTL of `cache_hours`. Force a rescan with
`analyze.py --refresh-known`. In manifest (multi-video) mode the known set is
loaded once and shared across all videos regardless of cache.
