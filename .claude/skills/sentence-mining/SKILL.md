---
name: sentence-mining
description: Build and maintain Japanese sentence-mining cards for Anki, fully self-contained (no AnkiMorphs install required) and configurable per user via a one-time `/sentence-mining setup`. (1) Video mode — paste any Instagram reel, YouTube video/Short, TikTok, Twitter video, or local file → yt-dlp + AssemblyAI + SudachiPy + a built-in i+1 known-word diff produces draft cards. (2) Bank mode — give a list of target words → search across your locally-indexed subs2srs .apkg banks for natural example sentences, reusing the bank's original audio + screenshot when available. (3) Replace mode — fix existing cards whose example sentence is bad (too short, a fragment, incomprehensible): pull a better, more comprehensible sentence (Immersion Kit → Nadeshiko → local bank, re-ranked by your own i+1), edit the card in place (archiving the old sentence to a previous_versions field), and rehabilitate the card (de-leech, unsuspend, reset-to-due) so you re-learn it fresh. All modes push via AnkiConnect onto a note type and decks you choose at setup. Use proactively whenever input is (a) a Japanese-language video URL, (b) a list of Japanese words, or (c) a request to improve/replace sentences on existing cards. Trigger phrases include "mine this video", "make sentence cards from <url>", "turn this reel into cards", "mine these words", "find sentences for [w1, w2, …]", "i keep forgetting <word>", "pull cards from my <show> bank", "leech these", "search the banks for X", "replace the sentence for <word>", "find a better sentence for X", "fix my flag:1 cards", "these sentences are too short/confusing", "set up sentence mining", `/sentence-mining`, `/sentence-mining setup`, or any video URL paired with a mention of Anki / cards / morphs / i+1.
---

# Sentence Mining

**Three modes** (plus a one-time `setup`). Two of them *create* new cards and share one
post-processing pipeline; the third *fixes existing* cards in place.

```
        ── CREATE NEW CARDS ──                      ── FIX EXISTING CARDS ──
┌────────────────────┐  ┌─────────────────────┐    ┌──────────────────────────┐
│  Video URL / file  │  │  List of words      │    │  flag:1 / "fix" / a word │
│  "mine this reel"  │  │  "card for 同期"    │    │  "better sentence for X" │
└─────────┬──────────┘  └──────────┬──────────┘    └────────────┬─────────────┘
          ▼                        ▼                             ▼
   ┌─────────────┐         ┌──────────────┐           ┌───────────────────────┐
   │ VIDEO MODE  │         │  BANK MODE   │           │     REPLACE MODE      │
   │ yt-dlp →    │         │ search local │           │ IK → Nadeshiko → bank │
   │ AssemblyAI →│         │ .apkg banks  │           │ re-ranked by your i+1 │
   │ i+1 diff    │         │              │           │                       │
   └──────┬──────┘         └──────┬───────┘           └───────────┬───────────┘
          └───────────┬───────────┘                               ▼
                      ▼                              ┌───────────────────────────┐
       ┌─────────────────────────┐                  │  edit card IN PLACE:       │
       │  Shared post-process    │                  │  archive old → new + media │
       │  curate → explain →     │                  │  → rehab → reflag / retire │
       │  media → draft → push   │                  └───────────────────────────┘
       └─────────────────────────┘
```

Video and bank mode share the **Steps 1–8** below: the mode reference covers the
mode-specific Steps 1–3 (and the Step 5 specifics), then you come back here for the
shared post-processing. Replace mode runs its own pipeline end-to-end — see
[references/replace-mode.md](references/replace-mode.md).

**Route the request.** Look at what Ray gave you:

| Input                                                    | Mode    | Reference                          |
|----------------------------------------------------------|---------|------------------------------------|
| `setup` / "set up sentence mining" / no `config.json` yet  | setup   | [references/setup.md](references/setup.md)           |
| URL (instagram, youtube, tiktok, twitter) or local video | video   | [references/video-mode.md](references/video-mode.md) |
| Plain list of Japanese words                             | bank    | [references/bank-mode.md](references/bank-mode.md)   |
| "replace"/"swap"/"better sentence for" existing cards, or "fix my flag:1 cards" | replace | [references/replace-mode.md](references/replace-mode.md) |
| Both (URL + words)                                       | ask Ray | —                                   |

**Replace vs bank/video:** if the words/cards already exist in Anki and the ask is
to swap in a *better* example sentence (the current one is too short, a fragment, or
incomprehensible) — that's **replace mode**, not bank mode. Bank/video mode *create*
new cards; replace mode *edits existing* ones in place and archives the old sentence.

**Canonical sentence-source order (policy):** when finding an example sentence for a
word, try **Immersion Kit → Nadeshiko → sentencesearch.neocities → kotu.io → local
sentence bank** in that order, keeping the first hit usable at Ray's i+1. IK/Nadeshiko
ship a screenshot; the two web corpora are audio-only but far broader (they catch the
niche/loanword vocab the anime-skewed sources miss); the local bank is the indexed-subset
last resort. This is **fully implemented in replace mode**. The new-card modes don't use
it yet — video mode takes sentences from the video, bank mode from local banks; moving
them onto this same order is the intended next step (not done yet). See
[references/replace-mode.md](references/replace-mode.md).

**Before anything else, ensure Anki is up** (skip for setup mode, which has no collection to hit yet). The create/fix modes all need AnkiConnect, so run `bash <skill-dir>/scripts/ensure_anki.sh` first — it launches Anki for you if it's closed and waits for it to load, instead of dying mid-pipeline on "Connection refused". Only stop and tell the user if it exits non-zero.

**Then check setup.** If `<skill-dir>/config.json` does not exist, the skill is unconfigured — route to **setup mode** ([references/setup.md](references/setup.md)) first, then continue with the user's actual request. Setup is also how a friend imports this skill into their own Anki: it interviews them for their note type, fields, decks, known-word sources, and sentence banks, then writes their own `config.json` (git-ignored, never shared).

## Inputs and required env

The skill is designed to be **shareable**: nothing about a specific person's Anki
is hardcoded. Two git-ignored files hold all the per-user state:

- **`<skill-dir>/config.json`** — note type, field mapping, deck names, known-word
  sources, sentence-bank locations. Written by `/sentence-mining setup`. See
  `config.example.json` for the shape. Read by every script through `_config.py`.
- **`<skill-dir>/.env`** — API keys only:

  ```bash
  cp <skill-dir>/.env.example <skill-dir>/.env   # then paste the keys
  ```

  Required keys: `ASSEMBLYAI_API_KEY` (video mode only) and `GEMINI_API_KEY`
  (both modes — explanation TTS + sentence TTS fallback). Real env vars override
  `.env`. If a key is missing, the script exits pointing at `.env` — don't fall
  back to alternatives without asking.

**The only hard dependencies besides those two files:**
- Anki running with **AnkiConnect** (default port 8765) — **don't verify by hand; run `bash <skill-dir>/scripts/ensure_anki.sh` once at the start of any mode.** It pings AnkiConnect, launches Anki (`open -a Anki`) if it's down, waits up to ~3 min for it to load, and confirms it stays up (3 pings — Anki sometimes answers once then crashes during a big-collection load on this machine). Exit 0 = good to proceed; exit 1 = surface its stderr to the user (likely a sync/database modal blocking the addon, or the addon disabled).
- `yt-dlp`, `ffmpeg` on PATH
- Python: `pip3 install --break-system-packages google-genai sudachipy sudachidict_core`
  (SudachiPy is the Japanese tokenizer — pure pip, no `brew install mecab` needed)

**AnkiMorphs is NOT required.** The i+1 known-word diff is re-implemented inside
the skill: it reads the cards in the decks/note-types you name at setup,
SudachiPy-tokenizes the configured field, and treats a lemma as "known" once its
highest card interval ≥ threshold (default 21 days) — the same idea AnkiMorphs
uses, but computed live through AnkiConnect with the same tokenizer the miner uses.
See [references/known-words.md](references/known-words.md).

For **bank mode**, the banks must be indexed first — setup offers to do this, or
see [references/bank-mode.md](references/bank-mode.md) §"One-time setup".

If `config.json` is missing when a script runs, it exits telling the user to run
`/sentence-mining setup`.

## Steps 1–3 (mode-specific)

Follow the reference for the mode you routed into. By the end of those steps you have a `candidates.json` (or `banksearch.json`) shaped as:

```jsonc
{
  "source": "video" | "bank-search",
  "source_id": "...",
  "source_url": "...",     // optional, video only
  "candidates": [
    { "lemma": "...", "sentence": "...", "deck": "<config.decks.main>", "i_level": "i1" | "i?", ... },
    ...
  ]
}
```

Read it. Zero candidates? Tell Ray why (all words known, all dupes, no hits across banks, etc.) and stop.

## Step 3.5 — Curate (shared, inline)

Walk the candidate list and drop entries that aren't worth a card. **Filter aggressively** — a Ray-quality card teaches a generalizable word he'll hit again, not a one-off label from this specific source. Drop:

- **Pop-culture proper nouns** — anime/manga/game titles, character names, song titles, group/idol names. Real-world brands or places (`スターバックスコーヒー`, `富士山`, `東京`) are fine; pop-culture-specific titles are not.
- **Tokenizer fragments** — lemmas that are clearly mid-word cuts (`ざいって` from "うざいって", `けんぽ` from "じゃんけんぽい"). Tell: starts with a particle, ends mid-syllable, no dictionary entry. Rarer now that SudachiPy SplitMode C keeps compounds whole, but still spot-check. (Video mode only — bank mode doesn't tokenize.)
- **Transcription garbage** — nonsense given the sentence's clear topic, especially when JPDB rank is `1000000000` (no entry). Don't try to rescue a contaminated sentence; drop the candidate. (Video mode only.)
- **Trail-off / partial sentences** — sentence ends mid-clause or starts with a connecting particle; the audio clip will sound broken. A sentence ending in a bare object particle (`…を`, `…が` with no verb) is a fragment — drop it or pick a complete runner-up, **even if the fragment has zero other unknowns**. A complete sentence with one extra common word beats a 0-unknown fragment.
- **Wrong reading / wrong sense for the card** — when the target word has multiple readings (熟す = こなす *to handle* vs じゅくす *to ripen*; 相対する = あいたい *to face* vs そうたい *relative*), verify the candidate uses the **card's** reading/sense, not just the same kanji surface. The search matches on surface form and will happily return じゅくす hits for a こなす card. If no candidate matches the card's reading, drop it (a miss) rather than teaching the wrong word.
- **Prefer the canonical collocation** — between equally-clean candidates, pick the one showing the word's most natural pairing (`株価が暴落`, `握力が落ちる`, `憂いを残す`) over an incidental usage.
- **Word only inside a speaker-name label** — subs2srs rips of Japanese TV prefix each line with the speaker's name in full-width brackets: `（亜湖）しょうがない`, `【フランセス】自信ある？`. These names routinely *contain* an unrelated target word's kanji — `湖` ("lake", みずうみ) lives inside `亜湖` (the name "Ako") — so the search mines the word from a character's **name**, not a real usage. `search_banks.py` now strips leading `（…）`/`【…】` labels before matching and rejects a word that only survived inside one, but spot-check the kept `sentence`: if the target word appears *only* inside a bracketed name (not in the spoken line), drop it as a miss. (Bank mode.)
- **Subs2srs concatenated frames** — bank-mode sentences like `(line1)   (line2)`: keep only the chunk containing the target word.
- **Compound katakana redundant with components** — if both `アイスアメリカーノ` and `アメリカーノ` are candidates, drop the compound.

When dropping is judgment-call, lean toward dropping. **Ray would rather mine 3 great cards than 15 mediocre ones.**

Apply by deleting entries from `data["candidates"]` and saving back. Print a short "kept N / dropped M because …" summary.

## Step 4 — Generate explanations (shared, inline)

For **each** candidate, generate the Japanese explanation inline — don't shell out. Use this prompt verbatim, swapping `{word}` and `{sentence}` (it's the prompt from Ray's `ai-language-explainer` addon, so cards match the style of his 9000+ existing ones):

```
Please write a short explanation of the word '{word}' using the context of the original sentence: '{sentence}'.

Write an explanation that helps a Japanese beginner understand the word and how it is used with this context as an example.

Explain it in the same way a native would explain it to a 13-year-old. Don't use any English, only use simpler Japanese.

1. Don't write the furigana for any of the words in brackets after the word.
2. Don't start with stuff like という言葉を簡単に説明するね, just dive straight into explaining after starting with the word.
```

Write each explanation into the candidate's `explanation` field. Keep each under ~250 Japanese characters — it gets read aloud by TTS.

**Why Claude (you) writes this and not a script:** the prompt depends on contextual Japanese fluency. You produce more natural output than a separate API call would, and you can react to tone (formal vs casual vs anime-speak). See [references/explanation-prompt.md](references/explanation-prompt.md) for the canonical addon prompt if you ever need to verify.

## Step 5 — Generate media (mode-specific)

Different script per mode — both write the same `draft.json` shape so Step 7 (push) is shared.

| Mode  | Script                          | What it does                                                              |
|-------|---------------------------------|---------------------------------------------------------------------------|
| video | `scripts/generate_media.py`     | ffmpeg clip + screenshot from the video, Gemini TTS on explanation        |
| bank  | `scripts/generate_media_bank.py`| copy bank's audio/image (or Gemini TTS sentence if absent), TTS explanation |

Both write `sentenceAudio_file`, `picture_file`, `explanationAudio_file` (the latter two may be empty strings for bank cards where the bank shipped no image). Media lands in `/Users/ray/Library/Application Support/Anki2/User 1/collection.media/`.

Cards are processed by a pool of 3 concurrent workers (ffmpeg clip + screenshot + Gemini TTS per card, staying under Gemini's 10 RPM free-tier cap). **Video mode pushes inline by default:** `generate_media.py` inserts each card into Anki the moment its own media finishes — three generations in flight, cards streaming in one by one as they complete (out of order is normal). This folds Steps 5–7 into one command. Pass `--no-push` to only write the draft for a separate `push.py` run (the legacy two-step / draft-only flow, still used by bank mode).

See [references/video-mode.md](references/video-mode.md) §"Step 5" or [references/bank-mode.md](references/bank-mode.md) §"Step 5" for the script invocation.

## Step 6 — Push & summarize

**Default behavior: push immediately after Step 5 succeeds.** No approval gate. Ray confirmed in June 2026 that the curation + explanation pass in Steps 3.5 + 4 has been reliable enough that asking "say push to commit" was just adding friction. Anki's own review queue is the real gate — bad cards get suspended or deleted there. Push first; show the result. For video mode this is automatic — Step 5 generates and inserts in one pass (pass `--no-push` only when Ray says "draft only"); bank mode still calls `push.py` afterward.

Skip auto-push only if Ray explicitly said "draft only" / "don't push" / "let me review first" in the originating message. In that case, fall through to the legacy approval flow at the bottom of this section.

Go to Step 7, then print the summary in this shape (video mode):

```
Pushed 17 cards from <SOURCE_ID> to Anki ✓

  → "Ray's Sentence Cards" (i+1): 12
    1. 気迫 (きはく) — "彼は気迫のこもった目で..." [JPDB rank 4823]
    ...

  → "Ray's Sentence Mining Deferred" (i+2/i+3): 5
    13. 揶揄う (からかう) — "..." [JPDB rank 12044]
    ...

Skipped during curation: <N> (ads / tokenizer fragments / transcription errors).
Draft: ~/Downloads/sentence-mining/<source>.draft.json
```

Example (bank mode):

```
Pushed 2 bank cards (word list: 同期, 西暦, 和暦) ✓

  1. 同期 [tokyo_ghoul_season_1] 🔊🖼
     "同期では二人 二人共 聡明で強い意思を持った女性でした"
  2. 西暦 [legend_of_the_galactic_heroes_eng_jp]
     "西暦2166年には 木星の衛星 イオに" (sentence TTS synthesized; no image)

  Misses: 和暦 — no hit across N indexed banks.
```

If `push.py` reports any `failed`, list them with the reason from the response so Ray knows what didn't make it in.

### Legacy approval flow (only when Ray says "draft only" / "don't push")

Print the same summary but with "Mined N candidate cards" and a "Say 'push' to commit, or tell me which to drop" line. Then wait. He may:
- Say "push" — run Step 7
- Say "drop 3, 7, 11" — remove those, ask again
- Say "regenerate explanation for 5" — redo, regen TTS for that one
- Say "try a different sentence for X" — look at runner-up bank hits and re-stage
- Say "no" — leave draft.json on disk; he can come back to it

## Step 7 — What `push.py` does (tags, formatting, dedup)

```bash
python3 <skill-dir>/scripts/push.py --draft ~/Downloads/sentence-mining/<source>.draft.json
```

This:
- Calls AnkiConnect `addNotes` with the full card list
- **Tags** every card with two tags:
  - `claude-sentence-mining` (video) OR `claude-sentence-bank` (bank) — the permanent kind tag
  - `i1` / `i2` / `i3` / `i?` — the current i-level (count of unknown content words in the sentence) so Ray can filter by complexity in Anki

  Other context — per-run `source:*`, `speaker:*`, `bank:*`, `auto-mined:*` — is intentionally NOT promoted to tags (Ray asked these be dropped in June 2026 because they cluttered the tag tree without adding study value). The full data still lives in the draft JSON for debugging.
- Sentence field is prefixed with `<b>A:</b> ` for video diarized cards so it's clear who's talking
- **Empty picture → `。` filler, never blank.** The note type's Back template has a `{{^picture}}` branch that re-renders `sentence_audio` and forces `.audio { display: block }`. So a card with a *blank* picture field replays the sentence audio on the back — on AnkiMobile/AnkiDroid the audio autoplays on both front and back. `push.py` (and `replace_apply.py`) therefore write `。` into the picture field whenever there's no image, which flips `{{#picture}}` truthy and silences the back replay. Don't "fix" this back to an empty string.
- Nothing is suspended — Ray studies them all and decides per-card

If any `addNote` fails (usually a late-detected duplicate), `push.py` reports which and skips it without aborting the batch.

## Step 8 — Cleanup

Leave the video / draft / intermediate JSONs in `~/Downloads/sentence-mining/`. Ray asked for this — it lets him re-run, re-watch, or scrub for context. Don't auto-delete.

## Reference files

- [references/setup.md](references/setup.md) — the `/sentence-mining setup` interview that writes `config.json`
- [references/known-words.md](references/known-words.md) — the built-in i+1 known-word diff (replaces AnkiMorphs); how "known" is computed and configured
- [references/video-mode.md](references/video-mode.md) — Steps 1–3 and Step 5 for video-URL input
- [references/bank-mode.md](references/bank-mode.md) — Steps 1–3 and Step 5 for word-list input + one-time bank indexing setup
- [references/replace-mode.md](references/replace-mode.md) — fix existing cards' sentences in place via Immersion Kit, re-ranked by your i+1, archiving to `previous_versions`
- [references/apkg-schema.md](references/apkg-schema.md) — `.apkg` ZIP/SQLite layout and field separators
- [references/bank-formats.md](references/bank-formats.md) — field-role detection heuristics + known notetypes
- [references/note-type.md](references/note-type.md) — note-type fields and how `config.field_map` maps onto them
- [references/transcript-schema.md](references/transcript-schema.md) — shape of AssemblyAI's response
- [references/explanation-prompt.md](references/explanation-prompt.md) — verbatim prompt from Ray's addon

## Scripts inventory

| script                  | mode  | purpose                                                      |
|-------------------------|-------|--------------------------------------------------------------|
| `setup.py`              | setup | probe Anki (note types/fields/decks), tools, keys; validate `config.json` |
| `_config.py`            | all   | load `config.json` (merged over defaults) — single source of truth |
| `transcribe.py`         | video | AssemblyAI Universal-3 Pro JP transcription with diarization |
| `analyze.py`            | video | SudachiPy tokenize + built-in known-word diff (cached) + JPDB rank |
| `generate_media.py`     | video | ffmpeg clip + screenshot + Gemini TTS (3 parallel); pushes each card inline as it finishes (`--no-push` = stage draft only) |
| `extract_bank.py`       | bank  | parse `.apkg` → local index JSON + media dir                 |
| `search_banks.py`       | bank  | word-list → top-N sentence candidates across indexed banks   |
| `generate_media_bank.py`| bank  | copy bank media (or TTS fallback) + Gemini TTS explanation   |
| `replace_search.py`     | replace | resolve target cards (flag / note-ids / words) → search Immersion Kit → Nadeshiko → sentencesearch → kotu → local bank → filter + re-rank by your i+1 → replace-draft JSON |
| `replace_apply.py`      | replace | stage media (URL or local) + TTS explanation (best-effort), archive old sentence to `previous_versions`, overwrite fields, retag i-level, rehabilitate (de-leech/unsuspend/reset-to-due), clear flag:1 so the redone card just rejoins the study queue (`--done-flag N` to flag instead, `-1` to leave). Retires unfixable misses (`not-worth-learning` + suspend + clear flag; `--keep-misses` to skip). `--rehab-flag N` rehabilitates a batch with no field changes |
| `push.py`               | both  | AnkiConnect addNotes onto `config.note_type` via `config.field_map` |
| `ensure_anki.sh`        | all   | ping AnkiConnect; `open -a Anki` if down; wait for load + verify stable (run first) |
| `_env.py`               | both  | loads `.env` into `os.environ`                               |
| `_anki.py`              | both  | AnkiConnect helper + `store_media()` (sniffs audio bytes and auto-corrects a mismatched .wav/.mp3 extension before registering — see Gotchas) |
| `audit_media.py`        | any   | standalone scan of collection.media for extension/content mismatches on any note-referenced audio; `--fix` corrects + updates every referencing note; `--include-orphans` also lists stale unreferenced files |

## Gotchas (universal)

- **AnkiConnect must be running** — but don't make Ray launch it. Run `bash <skill-dir>/scripts/ensure_anki.sh` at the start of every mode; it launches Anki if closed, waits for the collection to load, and verifies stability (Anki has crashed once mid-load right after launch on this machine, answering a single version ping before dying — the 3-ping stability check catches that). Only if it exits 1 after launching is something actually wrong (sync/database modal blocking the addon, or addon disabled) — surface that to Ray rather than retrying.
- **Don't push cards with empty explanation.** If Step 4 failed for a card (you got confused, refused, etc.), drop it from the draft rather than pushing a hollow one.
- **Gemini TTS preview model rate-limits.** Free tier is 10 RPM. `generate_media.py` (video) caps TTS concurrency at 3, `generate_media_bank.py` (bank) at 2 (override with `SM_TTS_CONCURRENCY`); both back off exponentially on 429. If you still hit limits, lower the cap or serialize.
- **`allowDuplicate: False` in push.py** means re-pushing the same word is silently rejected. To check ahead of time: query `<word-field>:<lemma> deck:"<main-deck>"` (from `config.field_map.word` / `config.decks.main`) against AnkiConnect during curation. `analyze.py` already pre-dedupes against the configured mining decks.
- **Known-word scan is cached.** The first mine of the day scans every configured known-source deck (~100s for a large collection); subsequent runs reuse the cache for `config.known_words.cache_hours` (default 6). After a big review session, pass `analyze.py --refresh-known` (or just wait out the TTL) so freshly-matured words drop out of mining.
- **Never leave the picture field blank — write `。`.** A blank picture makes the Back template replay the sentence audio (double audio on mobile, front + back). All create/fix scripts already default an imageless card's picture to `。`. To bulk-fix legacy blank-picture cards: `updateNoteFields` setting `picture` to `。` on every note matching `note:"<note_type>" picture:`. Done once in June 2026 across 1626 cards.
- **A `.wav`/`.mp3` extension doesn't guarantee the bytes inside match.** Desktop Anki's bundled player decodes by content and doesn't care, but AnkiMobile/AnkiDroid trust the extension and pick a decoder from it — a mismatched file is silently unplayable on mobile with no error, which is why this goes unnoticed until someone studies on their phone. Found twice in July 2026: an external "saeko" import batch (9 cards, MP3 bytes wrapped in a RIFF/WAVE container named `.wav`) and one `replace_apply.py` download from kotu.io (M4A/AAC content saved as `.mp3`, since kotu's audio endpoint doesn't always return what its URL implies). All current scripts route audio through `_anki.store_media()`, which now sniffs the real container before registering and auto-corrects it — a same-content rename for wav↔mp3, or a real ffmpeg transcode to mp3 for anything else (m4a/ogg/flac/webm). **Every caller must use `store_media()`'s return value** (not the filename it was given) when building a `[sound:...]` field, since it may differ. This protects everything the skill itself generates, but NOT cards from an external source (another add-on, a manual import, a shared deck) — those bypass `store_media()` entirely, so run `python3 scripts/audit_media.py --fix` periodically or after importing outside cards to catch those too.
