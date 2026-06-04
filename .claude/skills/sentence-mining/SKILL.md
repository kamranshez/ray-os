---
name: sentence-mining
description: Build Japanese sentence-mining cards for Ray's Anki deck in two modes. (1) Video mode — paste any Instagram reel, YouTube video/Short, TikTok, Twitter video, or local file → yt-dlp + AssemblyAI + mecab + AnkiMorphs i+1 diff produces draft cards. (2) Bank mode — give a list of target words → search across Ray's locally-indexed subs2srs .apkg banks (Tokyo Ghoul, Harry Potter, LOGH, etc.) for natural example sentences, reusing the bank's original audio + screenshot when available. Both modes stage drafts for Ray's approval before pushing via AnkiConnect. Use proactively whenever input is (a) a Japanese-language video URL or (b) a list of Japanese words — don't ask if Ray wants cards, start drafting. Trigger phrases include "mine this video", "make sentence cards from <url>", "turn this reel into cards", "mine these words", "find sentences for [w1, w2, …]", "i keep forgetting <word>", "pull cards from my <show> bank", "leech these", "search the banks for X", `/sentence-mining`, or any video URL paired with a mention of Anki / cards / morphs / i+1.
---

# Sentence Mining

Two ways in:

```
┌────────────────────────┐                  ┌──────────────────────────────┐
│   Video URL or file    │                  │   List of target words       │
│   "mine this reel"     │                  │   "make a card for 同期"     │
└──────────┬─────────────┘                  └─────────────┬────────────────┘
           │                                              │
           ▼                                              ▼
┌──────────────────────┐                       ┌─────────────────────────┐
│   VIDEO MODE         │                       │   BANK MODE             │
│   yt-dlp →           │                       │   search bank indexes   │
│   AssemblyAI →       │                       │   for each word →       │
│   mecab + i+1 diff   │                       │   pick best sentence    │
└──────────┬───────────┘                       └────────────┬────────────┘
           │                                                │
           └──────────────┬─────────────────────────────────┘
                          ▼
              ┌─────────────────────────┐
              │   Shared post-process   │
              │   curate → explain →    │
              │   media → draft → push  │
              └─────────────────────────┘
```

**Route the request.** Look at what Ray gave you:

| Input                                                    | Mode    | Reference                          |
|----------------------------------------------------------|---------|------------------------------------|
| URL (instagram, youtube, tiktok, twitter) or local video | video   | [references/video-mode.md](references/video-mode.md) |
| Plain list of Japanese words                             | bank    | [references/bank-mode.md](references/bank-mode.md)   |
| Both (URL + words)                                       | ask Ray | —                                   |

The mode-specific reference walks through Steps 1–3 (and the mode-specific bits of Step 5). Then come back here for the shared post-processing.

## Inputs and required env

API keys live in `<skill-dir>/.env` (git-ignored). First-time setup:

```bash
cp <skill-dir>/.env.example <skill-dir>/.env
# Then edit and paste the keys.
```

Required keys:
- `ASSEMBLYAI_API_KEY` — video mode only
- `GEMINI_API_KEY` (Google AI Studio works) — both modes (explanation TTS + sentence TTS fallback)

Real environment variables override `.env`, so a key already in the shell still wins.

Also required:
- Anki running with **AnkiConnect** (port 8765) — verify with `curl -s http://localhost:8765 -d '{"action":"version","version":6}'`
- `yt-dlp`, `ffmpeg`, `mecab` on PATH (all present on Ray's machine)
- Python: `pip3 install --break-system-packages google-genai jamdict jamdict-data`

If a key is missing, the script exits with a clear message pointing at `.env`. Don't fall back to alternatives without asking.

For **bank mode**, the banks must be indexed first — see [references/bank-mode.md](references/bank-mode.md) §"One-time setup".

## Steps 1–3 (mode-specific)

Follow the reference for the mode you routed into. By the end of those steps you have a `candidates.json` (or `banksearch.json`) shaped as:

```jsonc
{
  "source": "video" | "bank-search",
  "source_id": "...",
  "source_url": "...",     // optional, video only
  "candidates": [
    { "lemma": "...", "sentence": "...", "deck": "Ray's Sentence Cards", "i_level": "i1" | "i?", ... },
    ...
  ]
}
```

Read it. Zero candidates? Tell Ray why (all words known, all dupes, no hits across banks, etc.) and stop.

## Step 3.5 — Curate (shared, inline)

Walk the candidate list and drop entries that aren't worth a card. **Filter aggressively** — a Ray-quality card teaches a generalizable word he'll hit again, not a one-off label from this specific source. Drop:

- **Pop-culture proper nouns** — anime/manga/game titles, character names, song titles, group/idol names. Real-world brands or places (`スターバックスコーヒー`, `富士山`, `東京`) are fine; pop-culture-specific titles are not.
- **mecab fragments** — lemmas that are clearly mid-word cuts (`ざいって` from "うざいって", `けんぽ` from "じゃんけんぽい"). Tell: starts with a particle, ends mid-syllable, no JMDict entry. (Video mode only — bank mode doesn't tokenize.)
- **Transcription garbage** — nonsense given the sentence's clear topic, especially when JPDB rank is `1000000000` (no entry). Don't try to rescue a contaminated sentence; drop the candidate. (Video mode only.)
- **Trail-off / partial sentences** — sentence ends mid-clause or starts with a connecting particle; the audio clip will sound broken.
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

See [references/video-mode.md](references/video-mode.md) §"Step 5" or [references/bank-mode.md](references/bank-mode.md) §"Step 5" for the script invocation.

## Step 6 — Show Ray the draft and wait for approval

Print a concise summary. Example (video mode):

```
Mined 17 candidate cards from <SOURCE_ID>:

  → "Ray's Sentence Cards" (i+1, one unknown — cleanest context): 12
    1. 気迫 (きはく) — "彼は気迫のこもった目で..." [JPDB rank 4823]
    2. 寡黙 (かもく) — "彼女は寡黙な少女だった" [JPDB rank 8901]
    ...

  → "Ray's Sentence Mining Deferred" (i+2 / i+3 / i+N): 5
    13. 揶揄う (からかう) — "..." [unknown_count=2, JPDB rank 12044]
    ...

Skipped: 4 dupes, 2 already known.
Draft: ~/Downloads/sentence-mining/<source>.draft.json
Media staged in Anki collection.media/. Say 'push' to commit, or tell me which to drop.
```

Example (bank mode):

```
Mined 2 bank cards (word list: 同期, 西暦, 和暦):

  1. 同期 [tokyo_ghoul_season_1] 🔊🖼
     "同期では二人 二人共 聡明で強い意思を持った女性でした"
  2. 西暦 [legend_of_the_galactic_heroes_eng_jp]
     "西暦2166年には 木星の衛星 イオに" (sentence TTS synthesized; no image)

  Misses: 和暦 — no hit across N indexed banks.
```

Wait for Ray's explicit approval. He may:
- Say "push" — go to Step 7
- Say "drop 3, 7, 11" — remove those, ask again
- Say "regenerate explanation for 5" — redo, regen TTS for that one
- Say "try a different sentence for X" — look at the runner-up bank hits and re-stage
- Say "no" — leave draft.json on disk; he can come back to it

## Step 7 — Push to Anki (shared)

```bash
python3 <skill-dir>/scripts/push.py --draft ~/Downloads/sentence-mining/<source>.draft.json
```

This:
- Calls AnkiConnect `addNotes` with the full card list
- **Tags** every card with EXACTLY one tag: `claude-sentence-mining` (video) OR `claude-sentence-bank` (bank).

  No other tags are added — Ray asked in June 2026 that the skill only emit `claude-*` tags, after the per-run `source:*`, `speaker:*`, `bank:*`, `auto-mined:*`, and `i1/i2/i?` tags accumulated without adding study value. The full context (`source_id`, `source_url`, `i_level`, `speaker`, `bank_id`, mining date) still lives in the draft JSON for debugging — it just doesn't ride along into Anki.
- Sentence field is prefixed with `<b>A:</b> ` for video diarized cards so it's clear who's talking
- Nothing is suspended — Ray studies them all and decides per-card

If any `addNote` fails (usually a late-detected duplicate), `push.py` reports which and skips it without aborting the batch.

## Step 8 — Cleanup

Leave the video / draft / intermediate JSONs in `~/Downloads/sentence-mining/`. Ray asked for this — it lets him re-run, re-watch, or scrub for context. Don't auto-delete.

## Reference files

- [references/video-mode.md](references/video-mode.md) — Steps 1–3 and Step 5 for video-URL input
- [references/bank-mode.md](references/bank-mode.md) — Steps 1–3 and Step 5 for word-list input + one-time bank indexing setup
- [references/apkg-schema.md](references/apkg-schema.md) — `.apkg` ZIP/SQLite layout and field separators
- [references/bank-formats.md](references/bank-formats.md) — field-role detection heuristics + known notetypes
- [references/note-type.md](references/note-type.md) — the 13 fields of `Ray's Sentence Mining` and which we populate
- [references/ankimorphs-db.md](references/ankimorphs-db.md) — schema of `ankimorphs.db`, why interval ≥ 21 means "known"
- [references/transcript-schema.md](references/transcript-schema.md) — shape of AssemblyAI's response
- [references/explanation-prompt.md](references/explanation-prompt.md) — verbatim prompt from Ray's addon

## Scripts inventory

| script                  | mode  | purpose                                                      |
|-------------------------|-------|--------------------------------------------------------------|
| `transcribe.py`         | video | AssemblyAI Universal-3 Pro JP transcription with diarization |
| `analyze.py`            | video | mecab tokenize + AnkiMorphs diff + JPDB rank                 |
| `generate_media.py`     | video | ffmpeg clip + screenshot + Gemini TTS explanation            |
| `extract_bank.py`       | bank  | parse `.apkg` → local index JSON + media dir                 |
| `search_banks.py`       | bank  | word-list → top-N sentence candidates across indexed banks   |
| `generate_media_bank.py`| bank  | copy bank media (or TTS fallback) + Gemini TTS explanation   |
| `push.py`               | both  | AnkiConnect addNotes; tags driven off `source` in draft      |
| `_env.py`               | both  | loads `.env` into `os.environ`                               |

## Gotchas (universal)

- **AnkiConnect must be running.** If `curl http://localhost:8765` fails, Anki is closed or the addon is disabled. Tell Ray rather than retrying.
- **Don't push cards with empty explanation.** If Step 4 failed for a card (you got confused, refused, etc.), drop it from the draft rather than pushing a hollow one.
- **Gemini TTS preview model rate-limits.** Free tier is 10 RPM. `generate_media.py` and `generate_media_bank.py` both cap concurrency at 2 with exponential 429 backoff. If you still hit limits, drop to 1 or serialize.
- **`allowDuplicate: False` in push.py** means re-pushing the same `wordForm` is silently rejected. To check ahead of time: query `wordForm:<lemma> deck:"Ray's Sentence Cards"` against AnkiConnect during curation.
