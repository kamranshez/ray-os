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
- Python packages: `google-genai` (TTS) and `jamdict` + `jamdict-data` (JMDict-aware dedup). Install with:
  ```bash
  pip3 install --break-system-packages google-genai jamdict jamdict-data
  ```

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

## Step 2: Transcribe (raw)

```bash
python3 <skill-dir>/scripts/transcribe.py "$VIDEO_PATH" > ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json
```

Output contains `full_text` and a flat `words` array. Each word has `start_ms`, `end_ms`, and a **`speaker`** label (`"A"`, `"B"`, …) from AssemblyAI's diarization pass. **Sentence splitting is intentionally NOT done here** — see Step 2.5 below.

Why no rule-based splitter: AssemblyAI's Japanese sentence segmenter is unreliable for casual/fast speech, and earlier rule-based splitters chopped at character/duration caps regardless of meaning. You (Claude) do this with full context instead.

Why diarization: speaker turn changes are the strongest "natural meaning boundary" signal we have, much better than punctuation alone for casual conversation. We deliberately don't pass `speakers_expected` — auto-detection handles 1, 2, or N speakers.

## Step 2.5: Correct + split (YOU do this, inline — no script)

Read the raw transcript. You have:
- `full_text`: the entire transcribed string (may contain mistranscriptions)
- `words`: every spoken word with `start_ms`, `end_ms`, and a `speaker` label (e.g. `"A"`, `"B"`)

Your job is to produce a `sentences` array where each sentence is a card-worthy chunk: roughly **3–12 seconds** of audio, **20–60 Japanese characters**, ending at a natural meaning boundary.

**Speaker turn = strongest natural boundary.** Every time the speaker changes, close the current chunk. Within a single speaker's turn you can let a chunk run a bit longer (up to ~12s / 60 chars) if it adds useful context — that's the whole point of having diarization. Inside a long turn, prefer secondary boundaries: sentence-final particle, clause break, hard punctuation.

A chunk's `speaker` field is the speaker of its words. If a chunk straddles speakers (rare — usually means diarization mis-tagged a backchannel), pick the dominant speaker and don't worry about it; backchannels like "うん" and "そうだね" are the known weak spot.

**Correction pass first.** Walk through `full_text`. For each suspicious sequence — anything that doesn't read as natural Japanese — figure out what was likely actually said given the surrounding context, and substitute. Common patterns:
- Phonetically similar mistakes (`線理眼` → `千里眼`, `特度` → `得度`)
- Wrong kanji homophones picked when the topic is clear (`公開` ↔ `後悔`)
- Numbers transcribed weirdly (`いっこ` written as `1個` is fine; `1` floating alone is a transcription bug)

Don't over-correct — if something is ambiguous, leave it. The point is to fix obvious errors, not rewrite the speaker's words.

**Then split.** Use the corrected text plus the word-level timings + speaker labels to decide chunk boundaries. Each chunk needs:
- `text`: the corrected sentence (one self-contained thought, no run-ons)
- `start_ms`: from the first word in the chunk
- `end_ms`: from the last word
- `speaker`: the dominant speaker label for the chunk
- `words`: the slice of the input `words` array spanning the chunk (timing must be monotonic; don't reorder)

When you correct text, the `text` field reflects the correction but the `words` array preserves original timings — ffmpeg slices audio off `start_ms`/`end_ms`, so the correction is purely textual.

Write the result back to the same file:

```python
import json
path = "~/Downloads/sentence-mining/<SOURCE_ID>.transcript.json"
data = json.load(open(path))
data["sentences"] = [
    {"text": "...", "start_ms": ..., "end_ms": ..., "words": [...]},
    ...
]
json.dump(data, open(path, "w"), ensure_ascii=False, indent=2)
```

Before moving on, print a short summary of the splits in chat (duration + char count + first 50 chars of text per chunk) so Ray can spot any obvious mistakes before we tokenize.

## Step 3: Analyze — tokenize, diff, dedupe, rank

Single video:

```bash
python3 <skill-dir>/scripts/analyze.py \
    --transcript ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json \
    --source-id "$SOURCE_ID" \
    --source-url "$URL" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.candidates.json
```

**Batch mode (preferred when mining ≥2 videos)** — share one mecab + jamdict + AnkiConnect load across all of them. Write a manifest file `manifest.json`:

```json
[
  {"transcript": "~/Downloads/sentence-mining/instagram-AAA.transcript.json", "source_id": "instagram-AAA", "source_url": "https://..."},
  {"transcript": "~/Downloads/sentence-mining/instagram-BBB.transcript.json", "source_id": "instagram-BBB", "source_url": "https://..."}
]
```

Then run:

```bash
python3 <skill-dir>/scripts/analyze.py \
    --manifest ~/Downloads/sentence-mining/manifest.json \
    --output-dir ~/Downloads/sentence-mining/
```

The batch form writes one `<source-id>.candidates.json` per entry. Same analysis per video, but jamdict (~100MB index) opens once instead of N times, and the `findNotes`/`notesInfo` AnkiConnect dedup query runs once instead of N times — that query was the source of the parallel-run timeout we hit before.

This single script does everything deterministic:
- Tokenizes each sentence with mecab
- Three-layer dedup for "Ray already knows this word":
  1. **Exact AnkiMorphs interval** — lemma's `highest_lemma_learning_interval ≥ 21` → known
  2. **JMDict entry equality** — any alternate writing in the same JMDict entry is mature (catches すべて↔全て, ご飯↔御飯, わたし↔私)
  3. **Kanji-stem match** — any mature lemma shares the leading kanji run (catches 支払う↔支払い, 取る↔取り — JMDict treats these as separate entries but Ray clearly knows both)
- For each unknown lemma, finds the **best sentence** (i+1 preferred; falls back i+2, i+3…)
- Also queries AnkiConnect for existing `wordForm:<lemma>` in `Ray's Sentence Cards` or `Ray's Sentence Mining Deferred`; drops dupes
- Ranks remaining unknowns by JPDB lemma priority (lower line number in `ja-JPDBv2.2-lemma-priority.csv` = more frequent = higher priority)
- Caps output at 50 candidates

Output: a list of candidate cards with `lemma`, `reading`, `sentence`, `sentence_start_ms`, `sentence_end_ms`, `target_word_start_ms`, `unknown_count_in_sentence`, `jpdb_rank`, `deck`, `i_level` (`i1`, `i2`, `i3`, …), and `speaker` (carried through from the splitting step). Deck routing:

- **i+1 cards** (one unknown — cleanest context) → `Ray's Sentence Cards` (Ray's main study deck; they enter normal daily review)
- **i+2 and higher** → `Ray's Sentence Mining Deferred` (top-level sibling deck, NOT a subdeck — kept separate so Ray can sweep messy ones out later, but cards stay unsuspended)

Both decks are checked for duplicates before adding.

Read this file. If it's empty or has zero candidates, tell Ray why (all words known? all dupes? no Japanese detected?) and stop.

## Step 3.5: Curate — drop low-value candidates (YOU do this, inline)

Before generating explanations, walk the candidate list and drop entries that aren't worth a card. Filter aggressively — a Ray-quality card teaches a generalizable word he'll hit again, not a one-off label from this specific video. Drop:

- **Pop-culture proper nouns** — anime/manga/game titles (`ヒーローアカデミア`, `鬼滅`), character names, song titles, group/idol names. Real-world brand or place names that someone might genuinely encounter in life (`スターバックスコーヒー`, `富士山`, `東京`) are fine; pop-culture-specific titles are not.
- **mecab fragments** — lemmas that are clearly mid-word cuts (`ざいって` from "うざいって", `けんぽ` from "じゃんけんぽい", `ーマジ`, `ゃんけんじゃね`). Tell: the lemma starts with a particle/conjugation marker, ends mid-syllable, or doesn't match any JMDict entry.
- **Transcription garbage** — words that read as nonsense given the sentence's clear topic, especially when JPDB rank is `1000000000` (no entry exists) and the sentence has other obvious AssemblyAI errors. Don't try to rescue a contaminated sentence; drop the candidate.
- **Trail-off / partial sentences** — if the candidate's `sentence` ends mid-clause or starts with a connecting particle ("はい、のトール一つ"), the audio clip will sound broken. Drop unless you can re-anchor the sentence to a clean boundary.
- **Compound katakana redundant with components** — if both `アイスアメリカーノ` and `アメリカーノ` are candidates from the same video, drop the compound — the simpler word is more learnable.

When dropping is judgment-call, lean toward dropping. Ray would rather mine 3 great cards than 15 mediocre ones.

Apply the curation by deleting entries from `data["candidates"]` and saving the file back. Print a short "kept N / dropped M because …" summary in chat.

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
- Tags every card with `claude-sentence-mining`, `auto-mined:YYYY-MM-DD`, `source:<source-id>`, an `i1`/`i2`/`i3` level tag, and a `speaker:A`/`speaker:B`/… tag (skipped if diarization unavailable). The card's sentence field is prefixed with `<b>A:</b> ` so it's visually clear who's talking.
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
