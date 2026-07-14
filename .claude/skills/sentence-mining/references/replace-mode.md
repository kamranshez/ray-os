# Replace mode

**Input:** existing cards whose *sentence* is bad. **Output:** the same cards, better, in place.

Bad means: too short, a mid-conversation fragment, a proper-noun false positive (a card for
紅葉 "autumn leaves" that actually shows 紅葉くん, a character name), or just incomprehensible
standalone. Replace mode swaps in a better sentence **in place** and archives the old one. It
does not create cards — that's [bank](bank-mode.md) / [video](video-mode.md) mode.

**Everything except SOURCE and WRITE is [the shared pipeline](pipeline.md).**

## Triggers

- "find a better sentence for X" · "this sentence is too short / makes no sense"
- "fix my flag:1 cards" — **flag:1 is Ray's input queue** for cards he's struggling with
- audiobook mode's rescue set arrives here as `--note-ids`

The word must **already have a card**. If it doesn't, that's [bank mode](bank-mode.md).

---

## 1 · SOURCE

```bash
python3 <skill-dir>/scripts/replace_search.py \
    --flag 1 \                       # OR --note-ids a,b,c  OR --words 同期,西暦
    --output <work>/replace.json
```

Resolves the target cards, then runs each one's word through
**[the cascade](pipeline.md#the-sentence-cascade)** — identical engine to bank mode.

**The one replace-specific rule:** a candidate **identical to the card's current sentence** is
excluded, since that's not an improvement. So a word whose only hit is already on the card is
reported as a genuine **miss**, not a no-op "replacement".

Input selectors: `--flag N` (every card flagged N in the mining decks) · `--note-ids` ·
`--words` (resolves each word's existing card; a word with no card is reported, not mined).

### Then curate

Read `replace.json`. **Start with each entry's `ai_instructions`** — it overrides the ranking
and your judgment; see [pipeline.md §CURATE](pipeline.md#2--curate). Then spot-check the top
pick per word: is the target in its normal sense? Is the sentence complete? If the top pick is
weak, take one from `runner_ups[]` (overwrite the entry's `new_sentence` / `translation` /
`image_url` / `sound_url` / `ik_id` / `i_level` from the chosen runner-up), or drop the entry.

---

## 3 · Review gate — ALWAYS. Every run. No exceptions.

Replace **overwrites cards Ray has already studied**, so it never auto-applies — the one mode
that always gates.

```bash
python3 <skill-dir>/scripts/replace_apply.py --draft <work>/replace.json --dry-run
```

Present the old→new table. Let Ray drop or swap any (edit the draft JSON). **Only proceed once
he confirms.**

---

## 5 · WRITE — apply in place

```bash
python3 <skill-dir>/scripts/replace_apply.py --draft <work>/replace.json
```

Per card:

- stages the chosen image + audio (URL or local bank file) via `store_media()`
- Gemini-TTS the new explanation — **best-effort**: a dead `GEMINI_API_KEY` leaves only
  `explanation_audio` empty and never blocks the card's text/audio/image update
- **archives** the current sentence into `previous_versions` (newest block first, dated), so
  every prior version is recoverable and the old media never becomes "unused"
- overwrites `sentence`, `sentence_audio`, `picture`, `explanation`, `explanation_audio`
- retags the i-level to reflect the **new** sentence's complexity
- **rehabilitates** the card — de-leech, unsuspend, reset to new at the FRONT of the queue, zero
  the reps/lapses counters. See [pipeline.md §ROUTE](pipeline.md#6--route) for why each step is
  load-bearing.
- **clears flag:1** so the redone card just rejoins the study queue (`--done-flag N` to set a
  colored flag instead; `-1` to leave the input flag untouched)

**Unfixable misses are retired**: tagged `not-worth-learning`, suspended, cleared off flag:1 —
so they leave the fix queue and `--flag 1` stops re-picking them every run. `--keep-misses`
leaves them on the flag instead.

Re-running the same draft is safe (idempotency guard on the live sentence).

> ⚠ **`new/day = 0` buries a reset card.** A rehabilitated card is a NEW card, and new cards
> only surface through the deck's `new/day` limit — which Ray keeps at 0 on purpose. The script
> detects this per deck and prints a `⚠ … new/day = 0` warning: **relay it.** The fix is
> `--due-now` (setDueDate 0, skips the learning steps) or Custom Study. **Don't change his deck
> preset yourself.**

Then **[Step 7 · QUEUE](pipeline.md#7--queue--offer-this-every-mode-every-time)**.

Summarize: replaced N, retired M, draft path.

---

## Rehabilitate a flagged batch with no field changes

De-leech + unsuspend + reset-to-new-at-front every card flagged N, changing nothing else (e.g.
after a batch was applied before this behavior existed). Add `--due-now` to also make them due
today:

```bash
python3 <skill-dir>/scripts/replace_apply.py --rehab-flag 3
```

## The `previous_versions` field

Added to the note type June 2026 (`config.field_map.previous_versions`). An append-only,
newest-first stack of archived sentence blocks:

```html
<div class="sm-prev" data-archived="2026-06-16">傘がないので雨宿りしています</div>
```

To revert a card, copy the archived sentence back into the live field by hand.
