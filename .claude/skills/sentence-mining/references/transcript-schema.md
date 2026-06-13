# Transcript JSON schema

The file goes through two stages:

## Stage A: raw output from `transcribe.py`

```json
{
  "transcript_id": "abc123...",
  "language": "ja",
  "audio_duration_ms": 17400,
  "full_text": "あのね、あなたに必要なのは気迫なの。それさえあれば...",
  "words": [
    {"text": "あのね", "start_ms": 1234, "end_ms": 1750, "speaker": "A"},
    {"text": "、",     "start_ms": 1750, "end_ms": 1800, "speaker": "A"},
    {"text": "あなたに", "start_ms": 1800, "end_ms": 2200, "speaker": "A"},
    ...
  ]
}
```

Flat word stream with timings + per-word `speaker` label from AssemblyAI diarization. We don't pass `speakers_expected` — auto-detection handles 1, 2, or N speakers. AssemblyAI's own sentence breaks are unreliable for casual/fast Japanese speech, so we don't ship them.

## Stage B: after Claude's correction + splitting (Step 2.5 of SKILL.md)

The same file gains a `sentences` array:

```json
{
  ...same fields as Stage A...,
  "sentences": [
    {
      "text": "あのね、あなたに必要なのは気迫なの。",
      "start_ms": 1234,
      "end_ms": 4567,
      "speaker": "A",
      "words": [
        {"text": "あのね", "start_ms": 1234, "end_ms": 1750, "speaker": "A"},
        ...
      ]
    },
    ...
  ]
}
```

The `text` field reflects any corrections Claude made (e.g. 線理眼 → 千里眼). The `words` array preserves AssemblyAI's original timing so ffmpeg can still slice the right audio segment — the correction is purely textual.

`analyze.py` reads from `sentences`, so step 2.5 must complete before it.

## Quality notes

- AssemblyAI's word-level timing is per its tokenization, not per SudachiPy token. The mapping back to SudachiPy tokens in `analyze.py` is heuristic (substring match) — good enough to pick a screenshot frame, but don't trust it for sub-character precision.
- Music-heavy videos can produce 10–30% transcription errors. Claude's correction step catches the obvious ones (phonetic confusions, wrong homophones) but won't fix systemic garbage — for those, surface the issue to Ray rather than churning out bad cards.
