---
name: sentence-mining
description: Build and maintain Japanese sentence-mining cards for Anki, fully self-contained (no AnkiMorphs install required) and configurable per user via a one-time `/sentence-mining setup`. Four modes, and the skill ASKS which one you want on every launch. (1) Video mode — paste any Instagram reel, YouTube video/Short, TikTok, Twitter video, or local file → yt-dlp + AssemblyAI + SudachiPy + a built-in i+1 known-word diff produces draft cards. (2) Bank mode — give a list of target words → find the best example sentence for each through one canonical cascade (Immersion Kit → Nadeshiko → sentencesearch → kotu → your locally-indexed subs2srs .apkg banks), re-ranked by your own i+1, with native audio and a screenshot where the source ships one. (3) Replace mode — fix existing cards whose example sentence is bad (too short, a fragment, incomprehensible): pull a better sentence through the same cascade, edit the card in place (archiving the old sentence to a previous_versions field), and rehabilitate the card so you re-learn it fresh. (4) Audiobook mode — adopt cards that an EXTERNAL audiobook miner (audiobook-viewer, tag:audiobook) pushed into Anki half-built: rewrite their explanations in house style so they lead with the word, generate the missing explanation TTS, strip the tool's leftover English `definition`/frequency fields, fix blank picture fields that make cards double-play audio on mobile, and auto-route every card by your i+1 diff — already-known words get retired, and sentences above i+1 are RESCUED with an easier sentence from the cascade rather than dumped in the deferred deck. All modes push via AnkiConnect onto a note type and decks you choose at setup. Use proactively whenever input is (a) a Japanese-language video URL, (b) a list of Japanese words, (c) a request to improve/replace sentences on existing cards, or (d) any mention of audiobook cards needing explanations, audio, or cleanup. Trigger phrases include "mine this video", "make sentence cards from <url>", "turn this reel into cards", "mine these words", "find sentences for [w1, w2, …]", "i keep forgetting <word>", "pull cards from my <show> bank", "leech these", "search the banks for X", "replace the sentence for <word>", "find a better sentence for X", "fix my flag:1 cards", "these sentences are too short/confusing", "write better explanations for my audiobook cards", "generate the audio for those explanations", "the cards I made audiobook mining", "clean up my audiobook cards", "this card is too hard, defer it", "set up sentence mining", `/sentence-mining`, `/sentence-mining setup`, or any video URL paired with a mention of Anki / cards / morphs / i+1.
---

# Sentence Mining

**There is one pipeline. The four modes are four entry points into it.**

They differ at exactly two stages — where the sentence comes from (SOURCE) and whether the
card is added or updated (WRITE). Everything else is shared, and all of it is written down
once, in **[references/pipeline.md](references/pipeline.md)**.

```
        video          bank          replace        audiobook
    a URL or file   a word list   bad sentence   external tool's
                                  on my card     half-built cards
          │              │              │              │
          ▼              ▼              ▼              ▼
    ┌───────────────────────────────────────────────────────────┐
    │  1 SOURCE   ◀── the modes differ here                      │
    │  2 CURATE       ai_instructions, then drop the junk        │
    │  3 EXPLAIN      house style — LEAD WITH THE WORD           │
    │  4 MEDIA        clip + image + TTS, via store_media()      │
    │  5 WRITE    ◀── the modes differ here (add vs update)      │
    │  6 ROUTE        i+1 → main · i+2 → deferred · known → retire│
    │  7 QUEUE        or it never surfaces                       │
    └───────────────────────────────────────────────────────────┘
                              │
                              ▼
                            Anki
```

**Read [pipeline.md](references/pipeline.md) once you know the mode.** Then read that mode's
reference, which is short and covers only its SOURCE/WRITE deltas and its own gotchas. If you
go looking for a rule in a mode doc and it isn't there, that's intentional — it's in pipeline.md.

## Step 0 — Ask which mode. Every launch.

**Open every invocation by asking, even when the request looks unambiguous.** Use
`AskUserQuestion`. Ray asked for this in July 2026: he often launches the skill with a
half-formed idea, and the menu is how he *decides*, not just how he confirms. A skill that
silently guesses from a pasted URL robs him of that moment — and when it guesses wrong he only
finds out after it has burned an API call and written cards.

Pre-select the mode the input implies and say why (`"Looks like a YouTube URL → video mode"`),
so agreeing is one keystroke. But let him say no. If he answers with the mode *and* the target
in one breath ("audiobook mode on the ryu cards"), that IS his answer — skip the question.

| Mode      | Input                          | What it does                                    | Reference |
|-----------|--------------------------------|-------------------------------------------------|-----------|
| video     | URL or local file              | transcribe → i+1 diff → **new** cards            | [video-mode.md](references/video-mode.md) |
| bank      | a list of words                | cascade → **new** cards                          | [bank-mode.md](references/bank-mode.md) |
| replace   | `flag:1` / "find a better sentence" | swap in a better sentence, **in place**     | [replace-mode.md](references/replace-mode.md) |
| audiobook | cards tagged `audiobook`       | bring an external tool's cards up to house standard | [audiobook-mode.md](references/audiobook-mode.md) |
| setup     | first run / no `config.json`   | write the per-user config                        | [setup.md](references/setup.md) |

### Telling the modes apart

**Create vs fix.** If the word has no card yet → **video** or **bank**. If the card already
exists and the ask is to make it *better* → **replace** or **audiobook**.

**Bank vs replace** is the one people get wrong: both take a word and find a sentence for it,
through the *same* cascade. The difference is only whether a card already exists. "I keep
forgetting 同期" with no card → bank. "The sentence on my 同期 card is a fragment" → replace.

**Replace vs audiobook** — both edit existing cards; the difference is *what's wrong*:
- **replace** — the card is Ray's own and its **sentence** is bad (fragment, too short,
  incomprehensible). The fix is a better sentence.
- **audiobook** — the card came from *outside the skill* (the audiobook-viewer), so it's
  structurally off-standard: explanation doesn't lead with the word, no explanation TTS, blank
  picture, leftover English fields, and nothing ever checked it against Ray's known words. The
  fix is normalization + i+1 routing. Cards whose sentences turn out to be too hard get an
  easier one from the cascade — the same SOURCE stage, not a call into another mode.

## Before anything else

**Ensure Anki is up** (skip for setup mode, which has no collection to hit yet):

```bash
bash <skill-dir>/scripts/ensure_anki.sh
```

It pings AnkiConnect, launches Anki if it's down, waits up to ~3 min for the collection to
load, and confirms it stays up (3 pings — Anki has crashed mid-load on this machine, answering
a single version ping before dying). **Don't verify by hand.** Exit 0 = proceed. Exit 1 =
surface its stderr to Ray; something is actually wrong (a sync/database modal blocking the
addon, or the addon disabled). Don't just retry.

**Then check setup.** No `config.json` → route to [setup mode](references/setup.md) first, then
continue with Ray's actual request.

## Inputs and required env

The skill is **shareable**: nothing about a specific person's Anki is hardcoded. Two
git-ignored files hold all per-user state.

- **`<skill-dir>/config.json`** — note type, field mapping, deck names, known-word sources,
  sentence-bank locations. Written by `/sentence-mining setup`; see `config.example.json` for
  the shape. Read by every script through `_config.py`. Setup is also how a friend imports this
  skill into their own Anki.
- **`<skill-dir>/.env`** — API keys only (`cp .env.example .env`, then paste):

  | Key | Needed for |
  |-----|-----------|
  | `ASSEMBLYAI_API_KEY` | video mode |
  | `GEMINI_API_KEY`     | all modes — explanation TTS |
  | `NADESHIKO_API_KEY`  | optional — enables cascade tier 2 |

  Real env vars override `.env`. If a key is missing, the script exits pointing at `.env` —
  **don't fall back to alternatives without asking.**

**Other hard dependencies:** Anki + AnkiConnect (port 8765) · `yt-dlp`, `ffmpeg` on PATH ·
`pip3 install --break-system-packages google-genai sudachipy sudachidict_core`.

**AnkiMorphs is NOT required.** The i+1 known-word diff is re-implemented inside the skill: it
reads the cards in the decks/note-types you name at setup, SudachiPy-tokenizes the configured
field, and treats a lemma as "known" once its highest card interval ≥ threshold (default 21
days) — the same idea AnkiMorphs uses, computed live through AnkiConnect with the same
tokenizer the miner uses. See [known-words.md](references/known-words.md).

> **The known-word scan is cached.** The first mine of the day scans every configured
> known-source deck (~100s for a large collection); later runs reuse the cache for
> `config.known_words.cache_hours` (default 6). After a big review session, pass
> `--refresh-known` (or wait out the TTL) so freshly-matured words drop out of mining.

## Scripts

| script                   | stage        | purpose |
|--------------------------|--------------|---------|
| `ensure_anki.sh`         | pre-flight   | ping AnkiConnect; launch Anki if down; wait for load + verify stable. **Run first, every mode.** |
| `setup.py`               | setup        | probe Anki (note types/fields/decks), tools, keys; validate `config.json` |
| `_config.py`             | all          | load `config.json` merged over defaults — single source of truth |
| `_env.py`                | all          | load `.env` into `os.environ` |
| `_anki.py`               | all          | AnkiConnect helper + `store_media()` (sniffs audio bytes, auto-corrects a mismatched extension — **use its return value**) |
| **`_sources.py`**        | **1 SOURCE** | **THE sentence engine.** The 5-tier cascade + the i+1 re-ranking. Shared by bank and replace mode. |
| `transcribe.py`          | 1 SOURCE     | *video* — AssemblyAI Universal-3 Pro JP transcription with diarization |
| `analyze.py`             | 1 SOURCE     | *video* — SudachiPy tokenize + known-word diff (cached) + JPDB rank |
| `find_sentences.py`      | 1 SOURCE     | *bank* — word list → cascade → new-card candidates (dedupes vs existing + known words) |
| `replace_search.py`      | 1 SOURCE     | *replace* — resolve target cards (flag / note-ids / words) → cascade → replace-draft |
| `audiobook_scan.py`      | 1 SOURCE     | *audiobook* — `--groups` buckets cards by book; `--query` diffs each card against the house standard + the i+1 set → draft with `defects[]` and a `main`/`rescue`/`retire` route |
| `extract_bank.py`        | 1 SOURCE     | one-time — parse `.apkg` → local index JSON + media dir (feeds cascade tier 5) |
| `search_banks.py`        | 1 SOURCE     | cascade **tier 5** only — within-bank ranking. *Not an entry point any more; reached through `_sources.py`.* |
| `generate_media.py`      | 4 MEDIA      | *video* — ffmpeg clip + screenshot + Gemini TTS (3 parallel); pushes each card inline as it finishes (`--no-push` = draft only) |
| `generate_media_bank.py` | 4 MEDIA      | *bank* — stage the cascade's clip/image (URL **or** local bank file) + Gemini TTS |
| `push.py`                | 5 WRITE      | AnkiConnect `addNotes` onto `config.note_type` via `config.field_map` |
| `replace_apply.py`       | 4–6          | *replace* — stage media + TTS, archive the old sentence, overwrite fields, retag, rehabilitate, retire misses. `--dry-run` for the mandatory gate; `--rehab-flag N` to rehabilitate a batch with no field changes |
| `audiobook_apply.py`     | 4–6          | *audiobook* — TTS the explanation, overwrite, clear the tool's foreign fields, `。` a blank picture, retag, route. `--dry-run`, `--only <ids>` |
| `queue_cards.py`         | 7 QUEUE      | make finished cards actually appear. `--due-now` (default choice) or `--raise-limit N`. Main deck only — refuses to queue deferred cards |
| `audit_media.py`         | maintenance  | scan collection.media for extension/content mismatches; `--fix` corrects + updates every referencing note |

## Reference files

- **[pipeline.md](references/pipeline.md)** — the 7 stages. Every shared rule lives here.
- [video-mode.md](references/video-mode.md) · [bank-mode.md](references/bank-mode.md) ·
  [replace-mode.md](references/replace-mode.md) · [audiobook-mode.md](references/audiobook-mode.md)
  — the per-mode deltas.
- [setup.md](references/setup.md) — the interview that writes `config.json`
- [known-words.md](references/known-words.md) — how "known" is computed (replaces AnkiMorphs)
- [note-type.md](references/note-type.md) — note-type fields and how `config.field_map` maps on
- [explanation-prompt.md](references/explanation-prompt.md) — verbatim prompt from Ray's addon
- [bank-formats.md](references/bank-formats.md) · [apkg-schema.md](references/apkg-schema.md) ·
  [transcript-schema.md](references/transcript-schema.md) — data-format details
