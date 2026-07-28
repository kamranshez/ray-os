# Leech mode

**Everything after SOURCE is [the shared pipeline](pipeline.md).** This file covers only
what leech mode does differently: how it SELECTS, and what it does with cards the cascade
can't help.

## The one thing to understand first

`tag:leech` is a **scar, not a diagnosis**. Anki adds it when a card hits its deck's
`leechFails` (5 on Ray's main deck) and **never removes it**. So the tag answers "did this
card give me trouble at some point", not "is this card a problem now".

When leech mode was written (July 2026) Ray's collection had 78 tagged cards — and **43 of
them had recovered**, sitting at intervals of 21 to 338 days. One carried 10 lapses and a
338-day interval. Running replace mode's rehabilitation over `tag:leech` would have called
`forgetCards` on every one of them and thrown away most of a year of scheduling each.

So the tag is a **filter**, and current interval is the **signal**.

| bucket | test | what happens |
|--------|------|--------------|
| **struggling** | interval < `config.leech.struggling_interval` (default 21d) | full treatment — new sentence, media, rehabilitation |
| **recovered** | interval ≥ that | `leech` tag stripped, **scheduling untouched** |

The threshold defaults to `known_words.interval_threshold`, so the collection has one idea
of "this has stuck" instead of two that drift apart.

De-tagging a recovered card is not suppression. Anki re-tags on further lapses, so the tag
goes back to being a *live* signal instead of a permanent mark.

## Triggers

- "do we have anything for leeches", "fix my leeches", "leech these"
- the launch check reporting a non-zero struggling count
- `/sentence-mining` and choosing leech from the mode menu

Note: "leech these" used to be listed as a **bank mode** trigger. That was wrong — bank mode
skips any word that already has a card, and every leech has one by definition, so the whole
list came back as misses reading "already has a card".

## 1 SOURCE — `leech_scan.py`

```bash
python3 scripts/leech_scan.py --summary          # launch check: counts only, ~1s
python3 scripts/leech_scan.py --out <work>/leech.draft.json
```

Scoped to `config.note_type` inside the mining decks — a leech sitting in an unrelated deck
is someone else's card and is reported but never touched.

For each struggling card it emits `defects[]`:

| defect | means |
|--------|-------|
| `word_not_in_sentence` | the card's own word isn't in its sentence |
| `word_only_in_compound` | every occurrence is glued into another word — the card is mis-teaching |
| `sentence_short` | under 15 chars: a fragment, not a context |
| `above_i+1(n:…)` | n content words beyond the target are still unknown |
| `picture_blank` | back template re-renders sentence audio → double-play on mobile |
| `explanation_not_house_style` | doesn't lead with the word |
| `interference_twin(xN)` | another card in the collection tests the same word |
| `target_already_known` | the lemma matured elsewhere while this card kept failing |

**The defects drive the report, not the remedy.** A struggling card gets a sentence swap
whether or not its sentence looks bad — Ray's call, July 2026, and the data is why: 21 of
the 35 struggling cards had a perfectly good sentence and were failing anyway. 几帳面 had 8
lapses on a clean, natural sentence. Resetting the scheduler over unchanged material just
fails again on the same material, and the old sentence is archived to `previous_versions`,
so a swap costs nothing that isn't recoverable.

The vivid case for suspecting even a "clean" card: **穏当** carried
「不穏当な発言は慎んだ方がよろしいかと」 — the target appears only inside 不穏当, which
means the *opposite*. 19 lapses across 87 reps against a card teaching the wrong word.
`_sources.looks_misleading()` catches that class as `word_only_in_compound`. (穏当 was
ultimately *deferred* rather than fixed — see the rare-word rule below, which is the other
lesson that card taught.)

**Three things override the swap**, in this order: the word is too rare, the card's own
sentence beats what the cascade offered, or an interference twin. Each has its own
disposition, and none of them deletes anything.

### Rare words are deferred, not re-mined

A struggling leech whose **JPDB lemma rank** is worse than `config.leech.rare_rank_cutoff`
(default 20,000) never reaches the cascade. It keeps its sentence and moves to the deferred
deck at the **back** of the new queue.

Ray's call, July 2026, and the evidence is 穏当: rank **39,096**, and it had cost 19 lapses
across 87 reps. Fighting a word that barely appears is the expensive kind of failure. The
first run deferred 5 — 捨て身 (21,791), 福祉 (29,403), 放映 (30,129), 穏当 (39,096),
意志力 (49,483).

Deferred, **never deleted**. Rare means "later", not "not worth learning" — the same
sequencing-vs-worth rule the rest of the skill follows.

The check runs *before* the cascade, so a rare word costs no API call. It needs
`jpdb_priority_csv` set; without it the rule is off and the scan says so. Set
`rare_rank_cutoff` to 0 to disable.

**The cutoff is corpus-shaped, so sanity-check the edges.** JPDB ranks an anime/novel
corpus, and some genuinely everyday words sit deep in it — 几帳面 (18,738) and 福祉
(29,403) are far more common in real life than their rank suggests. 20,000 was chosen over
15,000 for exactly this reason.

### `keep_sentence` — when the card's own sentence is the better one

The cascade can return a *worse* sentence than the card already has. 屈託 (2026-07-28):
the card carried 「太一の屈託ない笑顔って　珍しくない？」 — the 屈託ない collocation, which
is how the word overwhelmingly appears — and the cascade offered a rarer standalone-noun
use. Rank 15,310 put it under the rare cutoff, so no rule caught it; a human did.

That's what the `keep_sentence` disposition is for: same sentence, same deck, picture
fixed, clean slate, due today. **Look at the old→new column in the dry run.** The gate is
there because the cascade optimises for i+1 and length, and neither of those notices that
a collocation is the thing actually worth learning.

## 5 WRITE — `leech_apply.py`

```bash
python3 scripts/leech_apply.py --draft <work>/leech.draft.json --dry-run   # the gate
python3 scripts/leech_apply.py --draft <work>/leech.draft.json
python3 scripts/leech_apply.py --draft <work>/leech.draft.json --confirm-delete
```

Deliberately thin: media staging, explanation TTS, the `previous_versions` archive,
rehabilitation and i+1 routing are **imported from `replace_apply.py`**, not reimplemented.
Two front doors, one implementation of each mechanism.

Four things happen, in order:

1. **Recovered** → strip the tag. No `forgetCards`, no deck move, no field write.
2. **Swaps** → new sentence + media + TTS, old sentence archived, blank picture filled with
   `。`, i-level retag, route by i+1, then full rehabilitation (reps and lapses zeroed,
   front of the queue) **with `--due-now` on by default**.
3. **Deletes** → misses and twin losers, gated (below).
4. **Twin survivors** → lose the tag, keep their scheduling. No swap: they were never
   diagnosed with a bad sentence.

### Why `--due-now` is the default here

The main deck runs at `new/day = 0`. A rehabilitated card is a **new** card, so without
`setDueDate 0` it sits at the front of a queue that never serves anything — invisible.
`--no-due-now` restores the learning steps (better for a word failed 5+ times) but then you
must raise the limit yourself; `queue_cards.py --raise-limit N` exists for that.

### Misses and twins are DELETED, not suspended

This is the one place leech mode departs from the rest of the skill, which never suspends
and never tags `not-worth-learning`. A word with no usable sentence in **any** corpus, on a
card that has already failed five or more times, is a card Ray asked to have deleted rather
than parked.

The gate: `leech_apply.py` prints every proposed deletion — word, note id, why, lapses,
interval, spellings the cascade tried, current sentence — and deletes **nothing** unless
`--confirm-delete` is passed. Pass it only after a human has read that table. Anki logs
deleted notes' fields to `deleted.txt` in the collection folder, so the text survives; the
scheduling history and the note id do not.

Without `--confirm-delete` the misses keep their leech tag and reappear on the next scan.

### The merge proposal

When two cards test the same word, `survivor_of()` proposes the healthier one: higher
current interval first (it's the card that's working), then fewer lapses, then the sentence
closest to the cascade's length sweet spot. Both cards are printed in full so the choice can
be flipped by editing `proposed_survivor` / `proposed_delete` in the draft.

Anki's dupe suffix means the pair is spelled differently in the word field (主張 vs
「主張 (2)」), which is why `find_twins()` searches by prefix and then compares
`_style.norm_word()` values rather than matching the field exactly.

**The detector cannot tell a duplicate from POLYSEMY, and it gets this wrong.** On the
first run it produced two proposals and one was wrong:

- **主張** — genuinely redundant. Both cards taught "state an opinion". Merged: the
  603-day / 1-lapse card survived, the 17-day / 9-lapse leech was deleted.
- **生地** — *not* interference. The leech taught 生地 = dough (「こっちの生地にザラメを
  足して」) and the card proposed for deletion taught 生地 = fabric (「ラバー素材が生地と
  して使われとるんや」). Two real meanings. Deleting it would have destroyed the only card
  covering the fabric sense — and that card was unstudied with an empty explanation, so
  what it actually needed was building out, not deleting. It went to `flag:2` instead.

So **read both sentences at the gate, every time.** If the two cards teach different
meanings, cancel the merge: the leech takes the `keep_sentence` disposition and the
under-built twin goes to `flag:2` ("flesh out"). A script cannot make this call — sense
disambiguation is exactly the judgment the confirmation gate exists to collect.

## No trace, and what that costs

**Every card leech mode touches loses the `leech` tag** — recovered, swapped, or twin
survivor. There is deliberately no `ex-leech` marker (Ray's call, July 2026).

That's what makes re-running safe: the tag *is* the queue, so a handled card doesn't come
back, and Anki re-tags it within a lapse or two if the fix didn't hold.

The cost, stated plainly: a card that re-leeches in two months is indistinguishable from a
fresh one, so leech mode will happily swap its sentence a second time. Partial mitigation —
swapped cards carry `previous_versions`, so `tag:leech` **and** a non-empty
`previous_versions` is a genuine repeat offender and deserves a look by hand rather than
another automatic swap.

## Gotchas

- **Read `picture` and `sentence_audio` RAW, never through `strip_html()`.** An
  `<img src="…">` strips to `""`, so a stripped check reports `picture_blank` on every card
  that has an image. The first version of `diagnose()` did exactly this and reported all 35
  struggling cards as picture-blank when not one of them was. Fixed 2026-07-28;
  `audiobook_scan.scan_note()` had it right all along. Nothing was damaged, because
  `apply_skipped()` and `replace_apply.process_one()` both test the raw value.
- **An `AQ.…` GEMINI_API_KEY is FINE.** It's Google's newer *authorization key* format
  (53 chars, permanent, bound to a service account) and AI Studio issues nothing else for
  new keys now. `_env.require_healthy_gemini_key()` used to reject it as an ephemeral OAuth
  token and blocked this mode's first run outright — over a key that had sat unchanged in
  `.env` since 16 June and still worked. Fixed 2026-07-28. What genuinely IS ephemeral is a
  `ya29.…` OAuth access token. Note the legacy `AIzaSy` keys are the ones on the way out:
  the Gemini API stops accepting standard keys in **September 2026**.
- **Run the scan when Anki is actually up.** `ensure_anki.sh` has reported "up and stable"
  and then had Anki die seconds later on this machine (2026-07-28). If a script dies with
  `Connection refused`, relaunch and re-run — don't assume the collection is broken.
- **The cascade is rate-limited**, ~1.2s between Immersion Kit requests. A 33-card scan
  takes several minutes; that's the API being polite, not a hang.
- **`--no-search`** diagnoses without touching any corpus — use it to look at defects
  without burning API calls.
- **`--limit N`** takes the N *worst* (lowest interval) cards, for a smaller first batch.
- A card whose new sentence is still above i+1 routes to the deferred deck, and `--due-now`
  is deliberately **not** applied to it — a deferred card is deferred precisely so it
  doesn't come up today.
