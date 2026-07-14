# Video mode

**Input:** a video URL (Instagram reel, YouTube video/Short, TikTok, Twitter/X) or a local file.
**Output:** new cards, with the sentence, audio and screenshot taken from the video itself.

This is the one mode that does **not** use the sentence cascade — the whole point is that the
sentence comes from the clip Ray actually watched.

**Everything after SOURCE is [the shared pipeline](pipeline.md).**

## Triggers

- Ray pastes any of the URL types above
- "mine this video" · "make sentence cards from \<url\>" · "turn this reel into cards"

A list of words instead → [bank mode](bank-mode.md).

---

## 1 · SOURCE

### 1a — Download

```bash
mkdir -p ~/Downloads/sentence-mining && cd ~/Downloads/sentence-mining
yt-dlp -o "%(extractor)s-%(id)s.%(ext)s" --no-playlist <URL>
```

The stable output template keeps re-runs idempotent. Local files: skip, note the path.

Record `VIDEO_PATH` and `SOURCE_ID` (e.g. `instagram-DZHudfuRmdJ`) — everything downstream
depends on them.

### 1b — Transcribe

```bash
python3 <skill-dir>/scripts/transcribe.py "$VIDEO_PATH" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json
```

Output has `full_text` and a flat `words` array, each word with `start_ms`, `end_ms`, and a
`speaker` label from AssemblyAI's diarization.

**Sentence splitting is intentionally NOT done here.** AssemblyAI's Japanese segmenter is
unreliable for casual/fast speech, and earlier rule-based splitters chopped at character or
duration caps regardless of meaning. You do it in 1c, with full context.

**Why diarization:** speaker turn changes are the strongest "natural meaning boundary" signal —
much better than punctuation alone for casual conversation. Don't pass `speakers_expected`;
auto-detection handles 1, 2, or N speakers.

### 1c — Correct + split (inline, no script)

Read the raw transcript. Produce a `sentences` array where each chunk is card-worthy: roughly
**3–12 seconds**, **20–60 Japanese characters**, ending at a natural meaning boundary.

**Correct first.** Walk `full_text`; for each sequence that doesn't read as natural Japanese,
work out what was likely said and substitute:
- phonetically similar mistakes (`線理眼` → `千里眼`, `特度` → `得度`)
- wrong kanji homophones where the topic is clear (`公開` ↔ `後悔`)
- numbers transcribed weirdly (a `1` floating alone is a bug)

**Don't over-correct** — ambiguous, leave it. Fix obvious errors; don't rewrite the speaker.

**Then split.** **Speaker turn = strongest boundary**: every time the speaker changes, close the
chunk. Within one speaker's turn a chunk can run longer (~12s / 60 chars) if it adds useful
context — that's the whole point of having diarization. Inside a long turn, prefer secondary
boundaries: sentence-final particle, clause break, hard punctuation.

Each chunk needs `text` (corrected), `start_ms` / `end_ms` (from first/last word), `speaker`
(the dominant one — a chunk straddling speakers usually means diarization mis-tagged a
backchannel like うん / そうだね), and `words` (the input slice, **preserving original timings** —
ffmpeg slices off these, so the correction stays purely textual).

Write back into the same transcript file under the `sentences` key. Print a short summary
(duration + char count + first 50 chars per chunk) so Ray can spot bad splits.

### 1d — Analyze

```bash
python3 <skill-dir>/scripts/analyze.py \
    --transcript ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json \
    --source-id "$SOURCE_ID" --source-url "$URL" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.candidates.json
```

It loads the [known-word set](known-words.md) (cached), tokenizes with SudachiPy (SplitMode C),
finds each unknown lemma's best sentence (i+1 preferred, falling back to i+2, i+3…), drops words
that already have cards in the mining decks, ranks by JPDB frequency if `config.jpdb_priority_csv`
is set, and caps at 50 candidates. Routes by i-level per
[pipeline.md §ROUTE](pipeline.md#6--route).

**Batch form (preferred for ≥2 videos)** — one SudachiPy load, one known-word scan, one
AnkiConnect dedup query shared across all of them (that query was the source of the parallel-run
timeout we used to hit). Write a `manifest.json`:

```json
[
  {"transcript": "…/instagram-AAA.transcript.json", "source_id": "instagram-AAA", "source_url": "…"},
  {"transcript": "…/instagram-BBB.transcript.json", "source_id": "instagram-BBB", "source_url": "…"}
]
```

```bash
python3 <skill-dir>/scripts/analyze.py --manifest …/manifest.json --output-dir ~/Downloads/sentence-mining/
```

Zero candidates? Tell Ray why (all words known? all dupes? no Japanese detected?) and stop.

---

## 4–5 · MEDIA + WRITE (one command)

```bash
python3 <skill-dir>/scripts/generate_media.py \
    --video "$VIDEO_PATH" \
    --candidates <candidates-with-explanations.json> \
    --source-id "$SOURCE_ID" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.draft.json
```

Per candidate: ffmpeg-clips the sentence audio, grabs the middle frame as a JPEG (640px max),
and Gemini-TTSes the explanation.

**Video mode pushes inline by default.** Three workers run in parallel and each card is inserted
into Anki the instant *its own* media is ready — cards stream in one by one while the next batch
is still generating, so **completion order is not input order. That's expected.** The push path
reuses `push.py`'s note builder, so tags / field-mapping / dedup are identical to the batch path.

`--no-push` stages the draft only, for a separate `push.py` run.

Then **[Step 7 · QUEUE](pipeline.md#7--queue--offer-this-every-mode-every-time)**.

### Summary shape

```
Pushed 17 cards from <SOURCE_ID> to Anki ✓

  → Sentence Mining (i+1): 12
    1. 気迫 (きはく) — "彼は気迫のこもった目で..." [JPDB rank 4823]
    …
  → Deferred (i+2/i+3): 5
    13. 揶揄う (からかう) — "…" [JPDB rank 12044]
    …

Skipped during curation: <N> (ads / tokenizer fragments / transcription errors).
Draft: ~/Downloads/sentence-mining/<source>.draft.json
```

---

## Gotchas

- **AssemblyAI's Japanese quality varies wildly.** Music-heavy reels with overlaid voice may give
  garbage. If a transcript has obvious errors (broken sentences, kana-only where kanji should
  be), **surface it to Ray before generating cards** — bad sentences mean bad cards.
- **Segmentation isn't perfect.** SplitMode C keeps most compounds whole, but words still split
  or fuse oddly. Because the known-set and the candidates use the *same* tokenizer, segmentation
  is at least self-consistent — but spot-check the target-word field in the draft summary.
- **Diarization is not clean for backchannels.** うん / そうだね interjections may flip speaker
  labels mid-sentence. Use judgment in 1c to consolidate.
