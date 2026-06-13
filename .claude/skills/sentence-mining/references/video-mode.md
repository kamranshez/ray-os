# Video Mode

Source: a **video URL** (Instagram reel, YouTube video/Short, TikTok, Twitter/X video) or a **local video file path**. The flow downloads (if URL), transcribes via AssemblyAI, splits into sentence chunks, runs mecab + the built-in known-word diff (see [known-words.md](known-words.md)) to find i+1 sentences (one unknown word), and produces draft cards.

When this mode triggers:
- Ray pastes any of the URL types above
- Ray says "mine this video", "make sentence cards from <url>", "turn this reel into cards"
- Ray writes `/sentence-mining` with a URL

If Ray gives a list of words instead → that's [bank-mode](bank-mode.md).

## Step 1: Download

```bash
mkdir -p ~/Downloads/sentence-mining
cd ~/Downloads/sentence-mining
# Stable, descriptive output template so re-runs are idempotent.
yt-dlp -o "%(extractor)s-%(id)s.%(ext)s" --no-playlist <URL>
```

For local files, skip — note the path.

Record `VIDEO_PATH` and `SOURCE_ID` (e.g. `instagram-DZHudfuRmdJ`) — everything downstream depends on these.

## Step 2: Transcribe (raw)

```bash
python3 <skill-dir>/scripts/transcribe.py "$VIDEO_PATH" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json
```

Output contains `full_text` and a flat `words` array. Each word has `start_ms`, `end_ms`, and a `speaker` label (`"A"`, `"B"`, …) from AssemblyAI's diarization pass. **Sentence splitting is intentionally NOT done here** — see Step 2.5.

**Why no rule-based splitter:** AssemblyAI's Japanese sentence segmenter is unreliable for casual/fast speech, and earlier rule-based splitters chopped at character/duration caps regardless of meaning. Claude does this with full context instead.

**Why diarization:** speaker turn changes are the strongest "natural meaning boundary" signal — much better than punctuation alone for casual conversation. Don't pass `speakers_expected`; auto-detection handles 1, 2, or N speakers.

## Step 2.5: Correct + split (inline — no script)

Read the raw transcript. Produce a `sentences` array where each sentence is a card-worthy chunk: roughly **3–12 seconds** of audio, **20–60 Japanese characters**, ending at a natural meaning boundary.

**Speaker turn = strongest natural boundary.** Every time the speaker changes, close the current chunk. Within a single speaker's turn you can let a chunk run a bit longer (up to ~12s / 60 chars) if it adds useful context — that's the whole point of having diarization. Inside a long turn, prefer secondary boundaries: sentence-final particle, clause break, hard punctuation.

A chunk's `speaker` field is the speaker of its words. If a chunk straddles speakers (rare — usually means diarization mis-tagged a backchannel like "うん" / "そうだね"), pick the dominant speaker.

**Correction pass first.** Walk through `full_text`. For each suspicious sequence — anything that doesn't read as natural Japanese — figure out what was likely actually said given context and substitute:
- Phonetically similar mistakes (`線理眼` → `千里眼`, `特度` → `得度`)
- Wrong kanji homophones picked when topic is clear (`公開` ↔ `後悔`)
- Numbers transcribed weirdly (`1` floating alone is a bug)

Don't over-correct — ambiguous → leave it. The goal is fixing obvious errors, not rewriting the speaker.

**Then split.** Use the corrected text + word-level timings + speaker labels. Each chunk needs:
- `text` — corrected sentence (one self-contained thought)
- `start_ms`, `end_ms` — from first/last word
- `speaker` — dominant speaker label
- `words` — slice of input `words` (preserves original timings; ffmpeg slices off these)

When you correct text, the `text` field reflects the correction but the `words` array preserves originals — the correction is purely textual.

Write back to the same transcript file (set the `sentences` key).

Before moving on, print a short summary (duration + char count + first 50 chars per chunk) so Ray can spot obvious splitting mistakes.

## Step 3: Analyze — tokenize, diff, dedupe, rank

Single video:

```bash
python3 <skill-dir>/scripts/analyze.py \
    --transcript ~/Downloads/sentence-mining/$SOURCE_ID.transcript.json \
    --source-id "$SOURCE_ID" \
    --source-url "$URL" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.candidates.json
```

**Batch mode (preferred when mining ≥2 videos)** — share one mecab + jamdict + AnkiConnect load across all of them. Write `manifest.json`:

```json
[
  {"transcript": "~/Downloads/sentence-mining/instagram-AAA.transcript.json", "source_id": "instagram-AAA", "source_url": "..."},
  {"transcript": "~/Downloads/sentence-mining/instagram-BBB.transcript.json", "source_id": "instagram-BBB", "source_url": "..."}
]
```

```bash
python3 <skill-dir>/scripts/analyze.py \
    --manifest ~/Downloads/sentence-mining/manifest.json \
    --output-dir ~/Downloads/sentence-mining/
```

The batch form writes one `<source-id>.candidates.json` per entry. Same analysis per video, but jamdict (~100MB) opens once instead of N times, the known-word set is scanned once and shared, and the AnkiConnect dedup query runs once instead of N — that query was the source of the parallel-run timeout we hit before.

**What analyze.py does:**
- Loads the **known-word set** once from `config.known_words.sources` (cached; see [known-words.md](known-words.md))
- Tokenizes each sentence with mecab
- Three-layer dedup for "learner already knows this word":
  1. **Highest card interval ≥ threshold** — lemma's highest interval across the configured known-source cards ≥ `interval_threshold` (default 21) → known
  2. **JMDict entry equality** — any alternate writing in the same JMDict entry is mature (catches すべて↔全て, ご飯↔御飯, わたし↔私)
  3. **Kanji-stem match** — any mature lemma shares the leading kanji run (catches 支払う↔支払い, 取る↔取り — JMDict treats them as separate entries but the learner clearly knows both)
- For each unknown lemma, finds the **best sentence** (i+1 preferred; falls back i+2, i+3…)
- Queries AnkiConnect for the existing target-word field across the configured mining decks (`config.decks`); drops dupes
- Ranks remaining unknowns by JPDB lemma priority if `config.jpdb_priority_csv` is set (lower line = more frequent = higher priority); otherwise keeps source order
- Caps output at 50 candidates

Output: candidate cards with `lemma`, `reading`, `sentence`, `sentence_start_ms`, `sentence_end_ms`, `target_word_start_ms`, `unknown_count_in_sentence`, `jpdb_rank`, `deck`, `i_level` (`i1`, `i2`, `i3`, …), and `speaker`.

**Deck routing** (deck names come from `config.decks`):
- **i+1 cards** (one unknown — cleanest context) → `decks.main` (enter normal daily review)
- **i+2 and higher** → `decks.deferred` (a top-level sibling deck, kept separate so messy ones can be swept later, but cards stay unsuspended). Falls back to `decks.main` if no deferred deck is configured.

Both decks are checked for duplicates before adding.

Read the output. If zero candidates, tell Ray why (all words known? all dupes? no Japanese detected?) and stop.

## Step 5 (video-specific): Generate media

```bash
python3 <skill-dir>/scripts/generate_media.py \
    --video "$VIDEO_PATH" \
    --candidates <candidates-with-explanations.json> \
    --source-id "$SOURCE_ID" \
    > ~/Downloads/sentence-mining/$SOURCE_ID.draft.json
```

Per candidate:
- Clips sentence audio with ffmpeg → `<anki-media>/sm_<source-id>_<idx>.mp3`
- Grabs middle frame as JPEG (640px wide max) → `<anki-media>/sm_<source-id>_<idx>.jpg`
- Calls Gemini 3.1 Flash TTS Preview on the explanation → `<anki-media>/sm_explain_<source-id>_<idx>.mp3`

Anki media folder: `/Users/ray/Library/Application Support/Anki2/User 1/collection.media/`

TTS concurrency is capped at 2 with 429 backoff — Gemini's free-tier limit is 10 RPM. If you still hit rate limits, drop concurrency to 1 or serialize.

## Gotchas specific to video mode

- **AssemblyAI Japanese quality varies wildly.** Music-heavy reels with overlaid voice may give garbage. If a transcript has obvious errors (broken sentences, kana-only output where kanji should be), surface this to Ray before generating cards — bad sentences mean bad cards.
- **Mecab segmentation isn't perfect.** Compound words may split or fuse in odd ways. Because the known-set and the candidates use the *same* mecab, segmentation is at least self-consistent — but still spot-check the target-word field for weirdness in the draft summary.
- **Diarization is not always clean for backchannels.** "うん" / "そうだね" interjections may flip speaker labels mid-sentence. Use judgment in Step 2.5 to consolidate.
