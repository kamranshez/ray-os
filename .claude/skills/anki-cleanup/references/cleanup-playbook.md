# Cleanup playbook

Exact recipes per bucket. All AnkiConnect calls go to `localhost:8765` (or the
`anki_connect_url` in the sentence-mining `config.json`). If your shell sandboxes
localhost, run these with the sandbox disabled. Prefer `curl` for one-off AnkiConnect
calls — in some sandboxes Python's socket to localhost is blocked while `curl` works.

**Golden rule:** preview every change and get an explicit OK before applying. These are
cards the user has studied for months. Never delete without specific per-action approval.

A reusable curl shape (note the apostrophe-escaping for deck names like `Ray's …`):

```bash
curl -s localhost:8765 -X POST -d '{"action":"<ACTION>","version":6,"params":{ ... }}'
```

---

## Replace — under-contextualized / messy sentences

The fix is a better example sentence, not more reps. This is **sentence-mining replace
mode** end to end — don't reimplement it.

1. Identify the target cards from the audit (e.g. struggling cards with short
   `sentence_len`). Collect their `note_id`s.
2. Run the search (read-only). Pass note-ids directly:
   ```bash
   python3 <repo>/.claude/skills/sentence-mining/scripts/replace_search.py \
     --note-ids <id,id,...> --output ~/Downloads/sentence-mining/replace.json
   ```
   (You can also target `--flag 1` or `--words a,b,c`. See the sentence-mining
   replace-mode reference.)
3. Curate the proposals: drop any where the new sentence is *harder* than the old (e.g.
   a higher i-level), and note any misses (no usable hit).
4. Write the Japanese explanations inline for each survivor (sentence-mining Step 2 /
   the explanation prompt).
5. **Review gate** — show the old→new table, get the OK.
6. Apply:
   ```bash
   python3 <repo>/.claude/skills/sentence-mining/scripts/replace_apply.py \
     --draft ~/Downloads/sentence-mining/replace.json --keep-misses
   ```
   This archives the old sentence to `previous_versions`, swaps in the new
   sentence/audio/image/explanation, removes `leech`, unsuspends, resets to due, zeroes
   lapse/rep counters, and flags the batch `3` for review. `--keep-misses` leaves
   unfixable cards untouched instead of auto-retiring them.

---

## Disambiguate — semantic collisions (synonym pairs)

When two near-synonyms are *both* struggling, they're interfering with each other. A new
sentence won't help; the card needs explicit contrast.

1. Identify the colliding pair/cluster (same meaning, both in the struggle set).
2. For each member, append a one-line contrast to the definition/explanation field via
   `updateNoteFields`, spelling out how it differs from its twin and a quick collocation:
   ```bash
   curl -s localhost:8765 -X POST -d '{"action":"updateNoteFields","version":6,
     "params":{"note":{"id":<note_id>,"fields":{"<explanation_field>":"…復旧=元の状態に戻す（システム・インフラ）／回復=体・関係が良くなる…"}}}}'
   ```
   (Read the field first and append, don't clobber existing content.)
3. Reschedule the pair so they don't come up together — e.g. `forgetCards` one and leave
   the other, or set different due dates with `setDueDate`, so they re-enter spaced apart.
4. Optionally tag both (e.g. `confusable`) so the cluster is easy to revisit.

---

## Retire — false-positive leeches (common / known words)

Genuinely-known, high-frequency words (low `freq_rank`) that leech for mechanical
reasons (usually the card tests whole-sentence comprehension, not the word). They don't
need study.

- De-leech and push the interval out so they stop nagging:
  ```bash
  curl -s localhost:8765 -X POST -d '{"action":"removeTags","version":6,"params":{"notes":[<id>,...],"tags":"leech"}}'
  curl -s localhost:8765 -X POST -d '{"action":"setDueDate","version":6,"params":{"cards":[<cid>,...],"days":"90"}}'
  ```
- Or, if the user agrees the card has no value, **delete it** (explicit approval per
  deletion): `deleteNotes` with the note ids.
- If the real problem is the format (the card tests the wrong thing), that's a template
  issue — flag it to the user rather than papering over it card by card.

---

## Defer — rare + low payoff

Real but very rare words (high `freq_rank`) that aren't worth daily review time. Move
them out of the main queue into the Deferred deck (from the sentence-mining config —
typically "Ray's Sentence Mining Deferred").

```bash
curl -s localhost:8765 -X POST -d '{"action":"changeDeck","version":6,
  "params":{"cards":[<cid>,...],"deck":"Ray'"'"'s Sentence Mining Deferred"}}'
```

Show the exact word list + frequency ranks and confirm before moving. Watch for
false-rare words: a high frequency rank on the *kanji form* of a word that's normally
written in kana (e.g. 折角/せっかく) overstates rarity — keep those.

---

## Rehabilitate — mature-but-lapsing / spinning, no content change

When a card's content is fine but its history is a mess (leeched, suspended, lapse-heavy)
and you just want a clean restart:

```bash
# de-leech + unsuspend + reset scheduling
curl -s localhost:8765 -X POST -d '{"action":"removeTags","version":6,"params":{"notes":[<id>],"tags":"leech"}}'
curl -s localhost:8765 -X POST -d '{"action":"unsuspend","version":6,"params":{"cards":[<cid>]}}'
curl -s localhost:8765 -X POST -d '{"action":"forgetCards","version":6,"params":{"cards":[<cid>]}}'
# zero the counters — forgetCards leaves reps/lapses, so the card would re-leech fast
curl -s localhost:8765 -X POST -d '{"action":"setSpecificValueOfCard","version":6,
  "params":{"card":<cid>,"keys":["reps","lapses"],"newValues":[0,0],"warning_check":true}}'
```

`newValues` must be integers (`0`, not `"0"`), and `warning_check:true` is required for
`reps`/`lapses`. This is per-card. For a whole flagged batch with no field changes,
sentence-mining's `replace_apply.py --rehab-flag N` does the de-leech/unsuspend/reset/zero
in one shot.

---

## Systemic — whole deck in ease hell

If `ease_floor_artifact` is true (a large fraction of reviewed cards pinned at minimum
ease), the deck is likely on the legacy SM-2 scheduler with cards that have bottomed out.
The deck-wide lever is **FSRS**, which handles lapse-prone cards far better than per-card
fixes. **Don't change scheduler settings yourself** — surface it: explain what the ease
floor means, that FSRS would reduce future leeching across the whole deck, and point them
at Deck Options → FSRS to flip it on. Let the user decide.

---

## Verification queries (Step 6)

After any fix, confirm it took. Examples:

```bash
# leeches gone in the batch?
curl -s localhost:8765 -X POST -d '{"action":"findCards","version":6,"params":{"query":"deck:\"<deck>\" flag:3 tag:leech"}}'
# state of specific cards (lapses/queue/suspended)
curl -s localhost:8765 -X POST -d '{"action":"cardsInfo","version":6,"params":{"cards":[<cid>,...]}}'
# deferred count moved?
curl -s localhost:8765 -X POST -d '{"action":"findCards","version":6,"params":{"query":"deck:\"<deferred deck>\""}}'
```

Report the verified numbers (lapses=0, 0 leech tags, N cards moved, old sentence
archived), not just "done".
