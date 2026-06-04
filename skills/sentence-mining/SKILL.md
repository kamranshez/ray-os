---
name: sentence-mining
description: Turn a video (Instagram reel, YouTube video/Short, TikTok, or local file) into Japanese sentence-mining cards for Ray's Anki deck. Downloads with yt-dlp, transcribes with AssemblyAI, tokenizes with mecab, diffs against Ray's AnkiMorphs database to find i+1 sentences (one unknown word), and stages cards for review before pushing via AnkiConnect. Use whenever Ray says "mine this video", "make sentence cards from <url>", "turn this reel into cards", or pastes a video URL in a context where he clearly wants Japanese study cards. Also trigger if he says "/sentence-mining" or references the Instagram/YouTube/TikTok URL alongside any mention of Anki, sentence cards, morphs, or i+1.
---

# Sentence Mining

Takes a video URL, produces draft Japanese sentence cards in Ray's exact note-type, stages them for review, then pushes to Anki on his approval.

## How it works (high level)

```
URL ─► yt-dlp ─► AssemblyAI ─► mecab ─► AnkiMorphs diff ─► dedupe ─► rank
                                                                       │
                                          ┌────────────────────────────┘
                                          ▼
                            per-candidate: clip audio + screenshot + Claude explanation + Gemini TTS
                                          │
                                          ▼
                                    draft.json + media/
                                          │
                                          ▼ (Ray confirms)
                                    AnkiConnect addNotes
```

## Inputs Ray will give

- A URL (Instagram reel, YouTube video, YouTube Short, TikTok, Twitter/X video) — yt-dlp handles all of these
- Or a local video file path — skip the download step
- He may also mention preferences like "only top 10" or "skip deferred" — respect those

## Required environment

API keys live in `<skill-dir>/.env` (git-ignored). To set up the first time:

```bash
cp <skill-dir>/.env.example <skill-dir>/.env
# Then edit .env and paste the two keys.
```

Required keys:
- `ASSEMBLYAI_API_KEY`
- `GEMINI_API_KEY` (Google AI Studio key works fine)

Real environment variables override `.env`, so a key already in the shell still wins.

Also required:
- Anki running with AnkiConnect (port 8765) — verify with `curl -s http://localhost:8765 -d '{"action":"version","version":6}'`
- `yt-dlp`, `ffmpeg`, `mecab` on PATH (all present on Ray's machine)
- `python3` with stdlib + the `google-genai` package (`pip install google-genai`)

If a key is missing, the script will exit with a clear message pointing at `.env`. Don't fall back to alternatives without asking.

## Step 1: Download

```bash
mkdir -p ~/Downloads/sentence-mining
cd ~/Downloads/sentence-mining
# Use a stable, descriptive output template so re-runs are idempotent.
yt-dlp -o "%(extractor)s-%(id)s.%(ext)s" --no-playlist <URL>
```

For local files, skip — note the path.

Record the resulting file path. Everything below assumes you know `VIDEO_PATH` and `SOURCE_ID` (e.g. `instagram-DZHudfuRmdJ`).

## Step 2: Transcribe

```bash
python3 <skill-dir>/scripts/transcribe.py "$VIDEO_PATH" > ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json
```

Output is sentence-segmented with word-level timing (see `references/transcript-schema.md`).

## Step 3: Analyze — tokenize, diff, dedupe, rank

```bash
python3 <skill-dir>/scripts/analyze.py \
    --transcript ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json \
    --source-id "$SOURCE_ID" \
    --source-url "$URL" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.candidates.json
```

This single script does everything deterministic:
- Tokenizes each sentence with mecab
- Looks up each lemma in Ray's AnkiMorphs DB; classifies as known (interval ≥ 21), learning (1–20), or unknown (not in DB / interval 0)
- For each unknown lemma, finds the **best sentence** (i+1 preferred; falls back i+2, i+3…)
- Queries AnkiConnect for existing `wordForm:<lemma>` in `Ray's Sentence Cards`; drops dupes
- Ranks remaining unknowns by JPDB lemma priority (lower line number in `ja-JPDBv2.2-lemma-priority.csv` = more frequent = higher priority)
- Caps output at 50 candidates

Output: a list of candidate cards with `lemma`, `reading`, `sentence`, `sentence_start_ms`, `sentence_end_ms`, `target_word_start_ms`, `unknown_count_in_sentence`, `jpdb_rank`, `deck`, and `i_level` (`i1`, `i2`, `i3`, …). Deck routing:

- **i+1 cards** (one unknown — cleanest context) → `Ray's Sentence Cards` (Ray's main study deck; they enter normal daily review)
- **i+2 and higher** → `Ray's Sentence Mining Deferred` (top-level sibling deck, NOT a subdeck — kept separate so Ray can sweep messy ones out later, but cards stay unsuspended)

Both decks are checked for duplicates before adding.

Read this file. If it's empty or has zero candidates, tell Ray why (all words known? all dupes? no Japanese detected?) and stop.

## Step 4: Generate explanations (Claude does this directly)

For **each** candidate, generate the Japanese explanation **inline** — don't shell out. Use this prompt verbatim, swapping `{word}` and `{sentence}` (it's the exact prompt from Ray's `ai-language-explainer` addon, so cards will match the style of his existing 9000+ cards):

```
Please write a short explanation of the word '{word}' using the context of the original sentence: '{sentence}'.

Write an explanation that helps a Japanese beginner understand the word and how it is used with this context as an example.

Explain it in the same way a native would explain it to a 13-year-old. Don't use any English, only use simpler Japanese.

1. Don't write the furigana for any of the words in brackets after the word.
2. Don't start with stuff like という言葉を簡単に説明するね, just dive straight into explaining after starting with the word.
```

Write each explanation into the candidate's `explanation` field in memory (or to a sidecar file). Keep each under ~250 Japanese characters — it gets read aloud by TTS.

**Why Claude (you) writes this and not a script:** the prompt depends on contextual Japanese fluency; you produce better, more natural output than a separate API call to a smaller model would, and you can react to the sentence's tone (formal vs. casual vs. anime-speak).

## Step 5: Generate media (parallel)

```bash
python3 <skill-dir>/scripts/generate_media.py \
    --video "$VIDEO_PATH" \
    --candidates <candidates-with-explanations.json> \
    --source-id "$SOURCE_ID" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.draft.json
```

For each candidate this:
- Clips sentence audio with ffmpeg → `<anki-media>/sm_<source-id>_<idx>.mp3`
- Grabs the middle frame as a JPEG → `<anki-media>/sm_<source-id>_<idx>.jpg`
- Calls Gemini 3.1 Flash TTS Preview on the explanation text → `<anki-media>/sm_explain_<source-id>_<idx>.mp3`

Anki media folder: `/Users/ray/Library/Application Support/Anki2/User 1/collection.media/`

The script parallelizes (semaphore of 5 for Gemini, no limit for ffmpeg). Expect ~30–90 seconds for 20 cards.

Output `draft.json` is the final card list with media paths filled in.

## Step 6: Show Ray the draft and wait for approval

Print a concise summary in chat:

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

Wait for Ray's explicit approval. He may:
- Say "push" — go to Step 7
- Say "drop 3, 7, and 11" — remove those from draft.json, then ask again
- Say "regenerate explanation for 5" — redo the explanation, regen the TTS for that one card
- Say "no" — leave draft.json on disk; he can come back to it

## Step 7: Push to Anki

```bash
python3 <skill-dir>/scripts/push.py --draft ~/Downloads/sentence-mining/$SOURCE_ID.draft.json
```

This:
- Calls AnkiConnect `addNotes` with the full card list — i+1 cards land in `Ray's Sentence Cards`, higher-i cards land in `Ray's Sentence Mining Deferred`. **Nothing is suspended** — Ray studies them all and decides per-card whether to mark hard/easy/suspend.
- Tags every card with `claude-sentence-mining`, `auto-mined:YYYY-MM-DD`, `source:<source-id>`, and an `i1`/`i2`/`i3` level tag so you can filter by context cleanliness later.
- Prints the resulting note IDs.

If any addNote fails (usually a late-detected duplicate), `push.py` reports which and skips it without aborting the batch.

## Step 8: Cleanup

Leave the video in `~/Downloads/sentence-mining/`. Ray asked for this — it lets him re-run, re-watch, or scrub for context. Don't auto-delete.

The intermediate JSON files (transcript, candidates, draft) also stay — useful for debugging and for a future "re-mine this with looser settings" command.

## Reference files

- `references/note-type.md` — the 13 fields of `Ray's Sentence Mining`, what each one is for, which we populate
- `references/ankimorphs-db.md` — schema of `ankimorphs.db`, why interval ≥ 21 means "known", how lemma vs inflection works
- `references/transcript-schema.md` — shape of AssemblyAI's response we use
- `references/explanation-prompt.md` — the verbatim prompt template from Ray's addon (so Step 4 stays in sync if it ever changes)

## Gotchas

- **AssemblyAI Japanese transcription quality varies wildly.** Music-heavy reels with overlaid voice may give garbage. If a transcript has obvious errors (broken sentences, kana-only output where kanji should be), surface this to Ray before generating cards — bad sentences mean bad cards.
- **Mecab segmentation isn't perfect.** Compound words may split or fuse differently than your AnkiMorphs DB expects. Trust the diff result but spot-check the wordForm field for weirdness in the draft summary.
- **AnkiConnect must be running.** If `curl http://localhost:8765` fails, Anki is closed or the AnkiConnect addon is disabled. Tell Ray rather than retrying.
- **Gemini TTS preview model can rate-limit.** The semaphore in `generate_media.py` caps concurrency at 5; if you still get 429s, drop to 2 or serialize.
- **Don't push cards whose explanation is empty.** If Step 4 failed for a card (you got confused mid-sentence, refused to generate, etc.), drop that card from the draft rather than pushing a hollow one.
