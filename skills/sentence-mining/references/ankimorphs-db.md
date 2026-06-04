# AnkiMorphs DB — what we read

Located at `~/Library/Application Support/Anki2/User 1/ankimorphs.db`. SQLite. Four tables; we only need `Morphs`.

```sql
CREATE TABLE Morphs (
    lemma TEXT,
    inflection TEXT,
    highest_lemma_learning_interval INTEGER,
    highest_inflection_learning_interval INTEGER,
    PRIMARY KEY (lemma, inflection)
);
```

A "morph" is a lemma + a specific inflection. A single lemma can appear in many rows.

`highest_lemma_learning_interval` is the longest current Anki SRS interval among all cards that contain that lemma in any inflection. We use that field because Ray's AnkiMorphs profile has `evaluate_morph_lemma: true` (lemma-based) — so an inflection counts as known the moment any form of its lemma is mature.

## What counts as "known"

Ray's config: `algorithm_upper_target_all_morphs: 6` (advanced threshold) but the universal AnkiMorphs convention is **interval ≥ 21 days = mature/known**. We follow that.

So per lemma:
- `SELECT MAX(highest_lemma_learning_interval) FROM Morphs WHERE lemma = ?`
- result ≥ 21 → known, skip when picking unknowns
- result < 21 → learning, still counts as "unknown" for i+1 purposes (Ray confirmed this in interview)
- lemma absent from table → never seen, definitely unknown

The `analyze.py` script preloads all lemma intervals into a dict in one query for speed.

## Why we ignore `inflection`

Ray's lemma-priority config means the goal is to know each *word*, not each conjugation. Mining `行く` once is enough; we don't want separate cards for `行った`, `行きます`, `行かない`. Mecab gives us the lemma directly so we key everything off that.

If Ray ever flips `evaluate_morph_inflection: true`, the diff logic needs to change to key by `(lemma, inflection)` instead. Don't do that silently — ask him.
