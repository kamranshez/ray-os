# The pipeline

**This is the canonical doc. Every rule in the skill is stated here, exactly once.**

There is only one pipeline. The four modes are not four pipelines — they are four *entry
points* into this one, and they differ at exactly two stages: **SOURCE** (where the
sentence comes from) and **WRITE** (add a new note, or update an existing one). Every
other stage is identical no matter how you got here.

```
                video      bank      replace     audiobook
                  │          │          │            │
                  ▼          ▼          ▼            ▼
        ┌──────────────────────────────────────────────────────┐
        │  1  SOURCE     ← modes differ here                    │
        │  2  CURATE                                            │
        │  3  EXPLAIN                                           │
        │  4  MEDIA                                             │
        │  5  WRITE      ← modes differ here (add vs update)    │
        │  6  ROUTE                                             │
        │  7  QUEUE                                             │
        └──────────────────────────────────────────────────────┘
                                  │
                                  ▼
                                Anki
```

A mode reference tells you only its SOURCE and WRITE deltas plus its own gotchas. If you
find yourself looking for a rule in a mode doc, it isn't there — it's here.

---

## 1 · SOURCE

Produce a list of `{word, sentence}` pairs. How, depends on the mode:

| Mode      | Where the sentence comes from                                              |
|-----------|----------------------------------------------------------------------------|
| video     | The video itself — transcribe, correct, split. See [video-mode.md](video-mode.md) |
| bank      | The **sentence cascade** below, given a word list. See [bank-mode.md](bank-mode.md) |
| replace   | The **sentence cascade** below, given the card's word (excluding its current sentence). See [replace-mode.md](replace-mode.md) |
| audiobook | The audiobook's own sentence — unless the defect scan finds it too hard, in which case that card re-enters the cascade. See [audiobook-mode.md](audiobook-mode.md) |

### The sentence cascade

**One engine, one source order, one ranking** — `scripts/_sources.py`, `best_for_word()`.
Every tier is tried only if the previous ones yield nothing usable *for Ray*:

| # | Tier | Media | Notes |
|---|------|-------|-------|
| 1 | **Immersion Kit** `apiv2.immersionkit.com` | image + audio | Broadest corpus, anime-skewed. June 2026 head-to-head on 12 flagged leeches: IK won 9, tied 1, **0 misses** vs the local index's 3. |
| 2 | **Nadeshiko** `api.nadeshiko.co` | image + audio | Drama-heavy; covers the formal/abstract words IK's anime corpus misses (奉る, 証券, the *real* 紅葉). Needs `NADESHIKO_API_KEY`. |
| 3 | **sentencesearch.neocities** | audio only | ~45k sentences shipped as one static JSON, mirrored to `work_dir/cache/` monthly and searched locally — no per-word HTTP, no rate limit. Clean JLPT-tango native audio. |
| 4 | **kotu.io** | audio only | Huge TV / anime / news / audiobook corpus, live API. Substring (not exact) match, so the compound filter earns its keep here. |
| 5 | **Local sentence bank** | image + audio | The indexed subs2srs `.apkg` banks. Last resort — only covers what's been indexed. |

**None of these corpora know what Ray knows**, so the engine grafts that back on: every
candidate from every tier is tokenized with the same SudachiPy + known-word machinery
`analyze.py` uses, and ranked by **how few OTHER content words are unknown** — a true i+1
*for this collection*, not a generic JLPT level. See [known-words.md](known-words.md).

Candidates are dropped outright when: length is outside 10–45 chars · there's no native
audio · an image-bearing tier shipped no image · the target is glued into a kanji compound
(`攻撃抑制` for 抑制) · it reads as a name (`紅葉くん`) · it sits inside a mis-teaching idiom
(`聞いて呆れる`). Then ranked by *(fewest other-unknowns, bare token, closest to ~22 chars)*.

> **Rate limits.** IK's apiv2 throttles bursts hard — you'll see `No route to host` on
> apiv2 specifically while the rest of the internet is fine. Both callers do all words in
> **one process with one connection** and space requests. Do **not** fire ad-hoc `curl`
> loops alongside a run or you'll get the IP throttled. If throttled, wait 3–5 min.

**One tier's failure never kills the cascade** — a dead API logs and falls through.
Zero picks across all five tiers = a genuine **miss**, and that's a real answer. Abstract /
financial / archaic words (称える, 奉る, 証券) are the usual ones; the corpora simply don't
carry a clean simple sentence for them. Report misses; don't invent a sentence.

---

## 2 · CURATE

### 2a — Read `ai_instructions` FIRST. It overrides you.

The note type's last field is a free-text scratchpad where Ray leaves notes for the next
AI pass on that specific card, written while reviewing in Anki. The search scripts print a
loud `⚠ <word> — ai_instructions: …` to stderr and attach it to every entry and miss.

**Obey it before applying any of your own judgment or the automatic ranking.**

| Ray wrote                              | Do this                                                                 |
|----------------------------------------|-------------------------------------------------------------------------|
| "I already know this word"             | Don't fix it — move the entry into `misses` so it gets retired (`not-worth-learning` + suspend + clear flag) |
| "sentence is too long" / "shorter one" | Pick a shorter `runner_ups[]` candidate instead of the top pick          |
| "wrong reading" / "wrong sense"        | Re-check the candidate uses the **card's** reading; drop wrong-reading hits |
| "this is a name, not a word"           | Retire it (same as "already know")                                       |
| "explanation is confusing"             | Rewrite the explanation; keep the sentence                              |

**Clear the field once you've honored it** (`updateNoteFields` → `ai_instructions: ""`) so
a one-shot instruction doesn't re-fire forever. Leave it only if it reads as a *standing*
preference ("always keep sentences under 20 chars for this card"). If an instruction is
ambiguous, don't guess — leave the card untouched, leave the field alone, tell Ray what it said.

### 2b — Drop what isn't worth a card

**Filter aggressively. Ray would rather mine 3 great cards than 15 mediocre ones.** When
dropping is a judgment call, lean toward dropping.

- **Pop-culture proper nouns** — anime/manga/game titles, character names, song titles, idol
  groups. Real-world brands and places (`スターバックスコーヒー`, `富士山`, `東京`) are fine.
- **Trail-off / partial sentences** — ends mid-clause, or starts with a connecting particle;
  the audio clip will sound broken. A sentence ending in a bare object particle (`…を`, `…が`
  with no verb) is a fragment — drop it **even if it has zero other unknowns**. A complete
  sentence with one extra common word beats a 0-unknown fragment.
- **Wrong reading / wrong sense** — when the word has multiple readings (熟す = こなす *handle*
  vs じゅくす *ripen*; 相対する = あいたい *face* vs そうたい *relative*), verify the candidate uses
  the **card's** reading. Search matches on surface form and will happily return じゅくす hits
  for a こなす card. No candidate with the right reading → drop it (a miss) rather than teach
  the wrong word.
- **Prefer the canonical collocation** — between equally clean candidates, pick the one showing
  the word's most natural pairing (`株価が暴落`, `握力が落ちる`, `憂いを残す`) over incidental usage.
- **Tokenizer fragments** *(video)* — mid-word cuts (`ざいって` from うざいって). Tell: starts with
  a particle, ends mid-syllable, no dictionary entry. Rare now that SudachiPy SplitMode C keeps
  compounds whole, but spot-check.
- **Transcription garbage** *(video)* — nonsense given the sentence's clear topic, especially
  when JPDB rank is `1000000000` (no entry). Don't try to rescue a contaminated sentence.
- **Word only inside a speaker-name label** *(bank tier)* — subs2srs rips prefix each line with
  the speaker's name in brackets: `（亜湖）しょうがない`. These names routinely *contain* an
  unrelated target's kanji — `湖` ("lake") lives inside `亜湖` (the name "Ako") — so the search
  mines the word from a **character's name**. `search_banks.py` strips leading `（…）`/`【…】`
  labels and rejects a word that only survived inside one, but spot-check the kept sentence.
- **Subs2srs concatenated frames** *(bank tier)* — `(line1)   (line2)`: keep only the chunk
  containing the target word.
- **Compound katakana redundant with its components** — if both `アイスアメリカーノ` and
  `アメリカーノ` are candidates, drop the compound.

Apply by deleting entries from the draft JSON and saving it back. Print a short
"kept N / dropped M because …" summary.

---

## 3 · EXPLAIN

For **each** entry, write the Japanese explanation **inline — do not shell out to a script.**
The prompt below is lifted from Ray's `ai-language-explainer` addon, so new cards match the
style of his 9000+ existing ones. Use it verbatim, swapping `{word}` and `{sentence}`:

```
Please write a short explanation of the word '{word}' using the context of the original sentence: '{sentence}'.

Write an explanation that helps a Japanese beginner understand the word and how it is used with this context as an example.

Explain it in the same way a native would explain it to a 13-year-old. Don't use any English, only use simpler Japanese.

1. Don't write the furigana for any of the words in brackets after the word.
2. Don't start with stuff like という言葉を簡単に説明するね, just dive straight into explaining after starting with the word.
```

### ⚠ Lead with the word. This is the single most-missed rule in the skill.

**Every explanation MUST begin with the target word itself**, then dive straight in. Ray's
9000+ cards all open by naming the word. An explanation that opens on the definition reads
wrong *and the TTS never says the headword* — which is the whole point of the audio.

- ✅ `やり残すは、やろうと思っていたことを途中で残してしまうことだよ。…`
- ❌ `やろうと思っていたことを途中で残してしまうことだよ。…` ← word never named
- ❌ `首の後ろ側、特にそこに生えている髪の毛を指します。…` ← what the audiobook tool writes

**Check before you save each one: does the first token contain the lemma?** If not, rewrite it.
(`audiobook_scan.py` checks this mechanically via `leads_with_word`, and tolerates the
dictionary form of an inflected card word — 突っ伏した → `突っ伏すは、…`.)

Keep each under ~250 Japanese characters; it gets read aloud. Write it into the entry's
`explanation` field.

**Why you write this and not a script:** the prompt needs contextual Japanese fluency. You
produce more natural output than a separate API call would, and you can react to tone
(formal vs casual vs anime-speak). [explanation-prompt.md](explanation-prompt.md) archives
the verbatim addon prompt if you ever need to verify it.

**Never push a card with an empty explanation.** If this stage failed for a card, drop it
from the draft rather than pushing a hollow one.

---

## 4 · MEDIA

| Mode              | Script                            | What it does                                              |
|-------------------|-----------------------------------|-----------------------------------------------------------|
| video             | `generate_media.py`               | ffmpeg clip + screenshot from the video, TTS the explanation |
| bank              | `generate_media_bank.py`          | stage the cascade's clip/image (URL *or* bank file), TTS the explanation |
| replace/audiobook | `replace_apply.py` / `audiobook_apply.py` | same staging, inline with the write                |

Media lands in `/Users/ray/Library/Application Support/Anki2/User 1/collection.media/`.

### Never leave the picture field blank — write `。`

The note type's Back template has a `{{^picture}}` branch that re-renders `sentence_audio`
and forces `.audio { display: block }`. So a card with a **blank** picture replays the
sentence audio on the back — on AnkiMobile/AnkiDroid it autoplays on *both* sides. Any
non-empty value flips `{{#picture}}` truthy and silences it. `。` is the minimal harmless
filler, and every script already writes it. **Don't "fix" this back to an empty string.**

The audio-only cascade tiers (sentencesearch, kotu) legitimately ship no image, so this
fires often — it is the normal path, not an error.

### A `.wav`/`.mp3` extension does not guarantee the bytes inside match

Desktop Anki decodes by content and doesn't care. **AnkiMobile/AnkiDroid trust the extension**
and pick a decoder from it — so a mismatched file is *silently unplayable on mobile with no
error*, which is why this goes unnoticed until someone studies on their phone. Found twice in
July 2026: an external "saeko" import (MP3 bytes in a RIFF/WAVE container named `.wav`) and a
kotu.io download (M4A/AAC content saved as `.mp3`, since kotu's audio endpoint doesn't always
return what its URL implies).

All audio routes through **`_anki.store_media()`**, which sniffs the real container before
registering and auto-corrects — a same-content rename for wav↔mp3, a real ffmpeg transcode for
anything else. **Every caller must use `store_media()`'s RETURN value**, not the filename it
was given, since it may differ.

This protects everything the skill generates but **not** cards from an external source (another
add-on, a manual import, a shared deck) — those bypass `store_media()` entirely. Run
`python3 scripts/audit_media.py --fix` periodically, and always after importing outside cards.

### TTS rate limits

Gemini's free tier is 10 RPM. `generate_media.py` caps TTS concurrency at 3,
`generate_media_bank.py` at 2 (override with `SM_TTS_CONCURRENCY`); both back off
exponentially on 429. If you still hit limits, lower the cap or serialize.

**Explanation TTS is best-effort in the fix modes**: a dead/expired `GEMINI_API_KEY` must not
block a card's sentence/audio/image update. On failure the explanation TEXT still lands and
only `explanation_audio` is left empty — regenerate later.

---

## 5 · WRITE

The only stage besides SOURCE where modes genuinely differ.

### Add a new note — video, bank

```bash
python3 scripts/push.py --draft <draft.json>
```

Calls `addNotes` with `allowDuplicate: False`, mapping the skill's internal field roles onto
Ray's actual note-type field names via `config.field_map` (so any note type with at least
`word` + `sentence` works). Pre-filters duplicates with `canAddNotes` so one collision can't
abort the batch. Video-diarized sentences get a `<b>A:</b> ` speaker prefix.

**Video mode pushes inline by default** — `generate_media.py` inserts each card the moment its
own media finishes, so cards stream in one by one (out of order is normal). Pass `--no-push` to
stage the draft only.

### Update an existing note — replace, audiobook

`replace_apply.py` / `audiobook_apply.py` call `updateNoteFields` in place, and **archive the
old sentence** into the `previous_versions` field first (newest block first, dated) so every
prior version is recoverable and the old media never becomes "unused":

```html
<div class="sm-prev" data-archived="2026-06-16">傘がないので雨宿りしています</div>
```

Re-running the same draft is safe — an idempotency guard skips any card whose live sentence
already equals the draft's new one, so nothing double-archives.

### Tags

- **the i-level** — `i1` / `i2` / `i3` / `i?` — on **every** card, every mode, so Ray can filter
  by complexity in Anki. Applying it clears any stale i-tag first.
- **a kind tag**, on cards this skill *created*: `claude-sentence-mining` (video) ·
  `claude-sentence-bank` (word-list). *Historical note: `claude-sentence-bank` predates the
  cascade, so it now means "mined from a word list", not "sourced from a local bank".*

**Audiobook mode adds no marker tag, on purpose.** Done-ness lives in the *fields* — a card with
a house-style explanation, explanation audio, a non-blank picture and no foreign fields is done,
which is exactly what the scan's defect check computes. An earlier version stamped a
`claude-audiobook` tag and it was wrong twice over: it duplicated a check that already existed,
and Ray's audiobook-viewer **rewrites tags on re-sync**, so finished cards lost the marker and
reappeared anyway. Re-scanning a finished card is free (it reports zero defects). Don't add a
marker tag back.

Per-run context (`source:*`, `speaker:*`, `bank:*`, `auto-mined:*`) is deliberately **not**
promoted to tags — Ray asked these be dropped in June 2026 because they cluttered the tag tree
without adding study value. The full data still lives in the draft JSON for debugging.

### Approval gates — deliberately asymmetric

| Mode              | Gate                        | Why |
|-------------------|-----------------------------|-----|
| video, bank       | **none** — push immediately | New cards are additive. Anki's own review queue is the real gate: bad cards get suspended or deleted there. Ray confirmed in June 2026 that asking "say push to commit" was pure friction. |
| audiobook         | **none** — apply immediately | Nothing here is destructive: retire is tag+suspend, a deck move is a deck move. (Ray, July 2026.) |
| **replace**       | **ALWAYS, every run**       | It **overwrites cards Ray has already studied.** Show the old→new table (`replace_apply.py --dry-run`) and wait for explicit confirmation. No exceptions. |

Skip auto-push only if Ray explicitly said "draft only" / "don't push" / "let me review first"
in the originating message. Then print the summary, add *"Say 'push' to commit, or tell me
which to drop"*, and wait. He may say "push", "drop 3, 7, 11", "regenerate explanation for 5",
or "try a different sentence for X" (look at `runner_ups[]` and re-stage).

---

## 6 · ROUTE

Where each card ends up, by its i-level and its state. Deck names come from `config.decks`.

| Situation                            | Destination |
|--------------------------------------|-------------|
| **i+1** — the target is the only unknown | `decks.main` — normal daily review |
| **i+2 or higher**                    | `decks.deferred` — a top-level sibling deck, kept separate so messy ones can be swept later. Cards stay **unsuspended**. Falls back to `main` if no deferred deck is configured. |
| **Target word already known**        | `decks.deferred` (fix modes) · a warning, but the card still gets built (bank mode). **Never a suspend.** See the rule below. |
| **Unfixable miss** — replace mode only, no sentence in any tier | **Retire**: tag `not-worth-learning`, suspend, clear the flag. The card is *already* broken and Ray already flagged it for fixing; retiring stops `replace_search --flag 1` re-picking it every run. (`--keep-misses` leaves it on the flag instead.) |

### The known-word diff sequences cards. It never judges their worth.

**Never suspend a card, and never tag one `not-worth-learning`, because the diff says the word
is already known.** Ray mined these words on purpose — a card that exists is a card he wants,
and the skill doesn't get to overrule that. The diff is a hint about **sequencing** (show it to
him later), never a verdict on worth. It is also *wrong sometimes*: it wanted to bin 突っ伏す
because 突 appears in 突然. A card sent to deferred that didn't need to be is one click to undo;
a card suspended on a bad diff result is a word he chose vanishing silently. Ray was explicit
in July 2026 — **"everything is worth learning at some point."**

So: an already-known word routes to `deferred` in audiobook mode, and in bank mode it just
prints a ⚠ and builds the card anyway (`--skip-known` to refuse). `audiobook_scan.py` emits no
`retire` route at all, and `audiobook_apply.py` never suspends.

The **one** exception is a replace-mode unfixable miss, and it earns the exception on different
grounds: that card is already broken, Ray already flagged it as needing a fix, and no corpus
anywhere has a usable sentence for it. It's retired for being *unfixable*, not for being
*unworthy*.

> **Never use `analyze.py`'s mature-kanji-stem heuristic to decide whether a TARGET word is
> known.** That heuristic exists for the opposite job — skipping possible unknowns *inside* a
> sentence, where a false "known" merely costs you a candidate. Applied to a target it
> **buries a card Ray wants**, and it misfires constantly (突っ伏す / 突然, above).
> `audiobook_scan.py` and `find_sentences.py` both require an **exact lemma (or
> spelling-variant) match**. Don't "optimize" that back.

### Rehabilitation (fix modes only)

A card getting a fresh sentence should be **re-learned cleanly**, so `replace_apply.py`:
removes the `leech` tag → unsuspends → `forgetCards` (reset to new) → **zeroes the reps/lapses
counters** (`forgetCards` alone leaves them, so the card keeps its lapse history and re-leeches
far too soon) → **repositions to the FRONT of the new queue** (`forgetCards` keeps the card's
original due position, which for an old card can be a million deep — without repositioning,
"rehabilitated" means "buried") → **clears flag:1** so it just rejoins the study queue.

`--rehab-flag N` does all of that for a whole flagged batch with no field changes.

> **Never use `analyze.py`'s mature-kanji-stem heuristic to decide whether a TARGET word is
> known.** That heuristic exists for the opposite job — skipping possible unknowns *inside* a
> sentence, where a false "known" merely costs you a candidate. Deciding a target is known
> **retires a card Ray wants**, and the heuristic misfires constantly: 突っ伏す shares the stem
> 突 with 突然, so a single matured kanji would bin the whole word. `audiobook_scan.py` and
> `find_sentences.py` both require an **exact lemma (or spelling-variant) match**. Don't
> "optimize" that back.

---

## 7 · QUEUE — offer this every mode, every time

**A card that exists but never surfaces is not a finished card.** Ray's main deck sits at
`new/day = 0`, so cards this skill "successfully pushed" can be completely invisible — he
found this in July 2026 when a whole day's mining never appeared in a single review.
Reporting "pushed 12 cards ✓" while all 12 sit in a dead queue is the most misleading thing
this skill can do.

So after the push/apply summary, **ask whether to queue them**:

```bash
python3 scripts/queue_cards.py --draft <the draft you just applied> --due-now
```

**`--due-now` is the right default, and `new/day = 0` is not a bug to fix.** Ray keeps his main
deck at zero on purpose — he meters his own intake rather than letting Anki do it. So surface
*this batch* (`setDueDate 0` bypasses the limit for exactly these cards) and leave the deck
config alone. The trade-off is that they become review cards and skip the learning steps; he's
accepted that. `--raise-limit N` is the opposite choice — cards stay new and keep their learning
steps, but the limit changes for the *whole deck* — so only reach for it if he asks.

**Only ever queue the main-deck (i+1) cards.** Deferred cards are deferred *because* they're
above i+1, and retired cards were deliberately killed — pulling either into today's queue undoes
the routing. `queue_cards.py` skips the deferred deck and skips suspended cards, so you can't do
this by accident.

If Ray says "leave them", say plainly that they're built but won't appear until he surfaces
them, so he isn't surprised by an empty queue tomorrow.

---

## 8 · Cleanup

Leave the video / draft / intermediate JSONs in the work dir. Ray asked for this — it lets him
re-run, re-watch, or scrub for context. **Don't auto-delete.**
