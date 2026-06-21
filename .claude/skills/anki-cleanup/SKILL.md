---
name: anki-cleanup
description: >-
  Audit and clean up an Anki deck the user is struggling with — find the cards
  that aren't sticking, surface the HIGH-LEVEL PATTERNS behind them (not just a flat
  list), triage the problems into prioritized buckets, fix the bucket the user picks,
  then loop back and re-offer the rest. Use this whenever the user wants to tidy up,
  audit, clean up, fix, prune, reprioritize, or "do something about" an Anki deck or
  their spaced-repetition reviews — phrasings like "clean up my deck", "what am I
  struggling with in Anki", "my leeches are out of control", "audit my sentence mining
  deck", "fix the cards I keep forgetting", "tidy up my reviews", "reset my hard cards",
  "what's wrong with this deck", or "help me get my Anki under control". Also trigger
  when the user points at AnkiConnect / a deck name and asks for analysis or maintenance,
  even if they don't say the word "cleanup". For finding/replacing a single bad example
  sentence or mining new cards, defer to the sentence-mining skill; this skill is the
  deck-wide audit-and-triage loop that *calls* those mechanics as one of its fixes.
---

# Anki Cleanup

A **diagnose → triage → fix → loop** workflow for a deck that has gotten messy. The
value isn't running one fix; it's looking at the deck from several angles, finding the
*patterns* behind the struggling cards, and then working down the buckets with the user
one at a time. After each fix you circle back and re-offer what's left — cleanup is
rarely one-and-done, and the user should stay in the driver's seat about what to tackle
next.

This skill **orchestrates**. The actual sentence-level fixes (replacing a bad example,
rehabilitating a card) live in the **sentence-mining** skill — call those rather than
reinventing them.

## The loop

```
ensure Anki ─▶ pick deck ─▶ AUDIT (multi-angle) ─▶ find PATTERNS ─▶ triage into BUCKETS
                                                                          │
        ┌─────────────────────────────────────────────────────────────┘
        ▼
   user PICKS a bucket ─▶ preview + CONFIRM ─▶ execute ─▶ VERIFY ─▶ LOOP BACK
        ▲                                                              │
        └──────────────────── re-offer remaining buckets ◀────────────┘
```

## Step 0 — Anki up, deck chosen

The audit hits AnkiConnect, so make sure Anki is running first. The sentence-mining
skill ships a launcher that handles the "Anki is closed / crashed mid-load" cases:

```bash
bash <repo>/.claude/skills/sentence-mining/scripts/ensure_anki.sh
```

If the user named a deck, use it. If not, run `audit.py` with no `--deck` to list decks
with card counts and ask which one. (Watch for speech-to-text mangling of deck names —
"raised sentence mining" → "Ray's Sentence Cards".)

## Step 1 — Gather, from several angles at once

```bash
python3 <skill-dir>/scripts/audit.py --deck "<deck name>"
```

This pulls the deck apart from independent angles and writes a full JSON report (path
printed at the end) plus a stdout summary. It does the *gathering*; you do the
*thinking*. Read the JSON.

`audit.py` reuses the sentence-mining `config.json` for the field map (so `sentence` /
`word` / `frequency` resolve correctly) and falls back to heuristics for other note
types. If localhost calls are sandboxed in your environment, run it with the sandbox
disabled — it only talks to `localhost:8765`.

## Step 2 — Audit angles (the important part)

A flat "here are your 50 worst cards" list is not useful. The goal is to look at the
struggle set through different lenses and notice what *clusters*. Work through these
angles against the report — they each catch a different kind of problem:

**Pick the real signals; discard the fakes.** Lapses and the `leech` tag are honest
signals. **Ease/factor often is not** — if a big fraction of reviewed cards sit at the
minimum ease (the report flags this as `ease_floor_artifact`), that's the deck's ease
floor, a *settings* effect, not "these cards are hard". Don't rank by ease when that's
true. Also weigh: cards mature **and** still lapsing (high interval + high lapses = it
keeps slipping no matter how long the gap), and cards **spinning** (many reps, tiny
interval = never escaping learning).

**Read what the card actually TESTS.** Look at `front_sample` (the rendered front). A
card "for" a word may be graded on something else entirely — e.g. a listening card that
shows the reading and plays sentence audio is really testing whole-sentence
comprehension, which is why a trivially-known word (a day of the week) can leech. The
format, not the word, is the problem. This single check reframes a whole class of
"impossible" leeches.

**Then cluster the worst cards by the *kind* of problem.** Common high-level patterns:

- **Under-contextualized** — the example sentence is a fragment or too short to anchor
  meaning (`sentence_len` small, trailing particles, the bare word alone). The fix is a
  better sentence, not more reps.
- **Semantic collisions** — near-synonyms competing in memory, where *both* members are
  struggling (e.g. two words that both mean "recovery"). Fresh sentences won't fix this;
  they need *contrast*. Look for pairs/clusters by meaning across the struggle set.
- **Format / template mismatch** — see "what it tests" above.
- **Wrong card type** — grammar points, particles, or counters wearing a vocab card's
  clothing. They're slippery as meaning-recall cards by nature.
- **False positives** — common, genuinely-known words (low `freq_rank` = frequent)
  leeching for mechanical reasons. They don't need study; they need retiring.
- **Genuinely rare + low payoff** — real but very rare words (high `freq_rank`) whose
  review cost outweighs their value. Candidates to defer, not fix.

Cross-reference angles: a card can be both under-contextualized *and* rare. Use
`freq_rank` to separate "common word I shouldn't be failing" (investigate format) from
"rare word not worth the fight" (defer).

Be honest about counts and don't silently cap — if the detail pull was truncated, say so.

## Step 3 — Triage into buckets

Turn the patterns into a small set of **action buckets**, each with: a count, the
recommended action, and a rough effort. Buckets map onto the playbook in
[references/cleanup-playbook.md](references/cleanup-playbook.md):

| Pattern found | Bucket / action |
|---|---|
| Under-contextualized sentences | **Replace** via sentence-mining replace mode |
| Semantic collisions (synonym pairs) | **Disambiguate**: add a contrast note + space the pair apart |
| False-positive leeches (common/known) | **Retire**: de-leech + long interval, or delete |
| Wrong card type (grammar/counter) | **Reformat or suspend** |
| Rare + low payoff | **Defer**: move to the Deferred deck |
| Mature-but-lapsing / spinning | **Rehabilitate**: de-leech, unsuspend, reset, zero counters |
| Whole deck in ease hell (artifact) | **Systemic**: suggest checking FSRS vs SM-2 (don't change settings without asking) |

Lead with the highest-leverage bucket. Mechanical fixes (replace) clear volume;
conceptual fixes (disambiguate) move the needle on the stubborn ones. Present the buckets
to the user as a short prioritized summary — see the report style the sentence-mining
session produced (counts + one-line rationale per bucket).

## Step 4 — Let the user pick

Use the **AskUserQuestion** tool to offer the buckets, with a "do the full sweep" option
and a recommendation on the highest-leverage one. One question, the buckets as options.
The user is the expert on their own deck — don't assume which bucket matters most to them.

## Step 5 — Execute the chosen bucket (preview, then confirm)

**Always preview before changing anything.** These are cards the user has already
studied; surprise edits erode trust. Show what *will* change — for replacements, the
old→new sentence table; for defers/retires, the exact word list and destination — and
wait for an explicit OK. Only then apply. Follow the per-bucket recipe in
[references/cleanup-playbook.md](references/cleanup-playbook.md); it has the exact
AnkiConnect calls and the sentence-mining hand-offs.

A few load-bearing details that recur (full versions in the playbook):
- **Replace** = `sentence-mining` replace mode (`replace_search.py` → review gate →
  `replace_apply.py`). It already archives the old sentence, de-leeches, unsuspends,
  resets to due, and zeroes lapse/rep counters.
- **Rehabilitate** standalone = remove `leech` tag → `unsuspend` → `forgetCards` →
  **zero `reps`/`lapses`** (`setSpecificValueOfCard`, integer values, `warning_check:true`).
  `forgetCards` alone leaves the counters, so the card would re-leech almost immediately.
- **Defer** = `changeDeck` into the Deferred deck from the sentence-mining config.
- **Retire** = `removeTags leech` + a long interval or suspend; only delete with explicit
  per-action permission.
- **Delete is never silent** — the user must approve deletions specifically.

## Step 6 — Verify

After applying, re-query AnkiConnect to confirm the change actually took — counts moved,
leech tags gone, cards unsuspended/due, lapses zeroed, old content archived. Report the
verified state, not just "done". (The sentence-mining session caught a real bug this way:
`forgetCards` left lapse counts intact.)

## Step 7 — Loop back

This is the part the user specifically wants. After a bucket is done and verified, **come
back and re-offer the remaining buckets** — a quick recap of what's left and an ask of
what to do next (AskUserQuestion again, or a plain "want me to take the synonym pairs
next, or stop here?"). Keep looping until the user says they're done or the buckets are
empty. End by noting anything still outstanding (e.g. misses with no good replacement) so
nothing silently falls through.

## Reference files

- [references/cleanup-playbook.md](references/cleanup-playbook.md) — exact per-bucket
  execution recipes: AnkiConnect calls, sentence-mining hand-offs, verification queries.
