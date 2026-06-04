# Transcript JSON schema (output of `transcribe.py`)

```json
{
  "transcript_id": "abc123...",
  "language": "ja",
  "audio_duration_ms": 17400,
  "sentences": [
    {
      "text": "あのね、あなたに必要なのは気迫なの。",
      "start_ms": 1234,
      "end_ms": 4567,
      "words": [
        {"text": "あのね", "start_ms": 1234, "end_ms": 1750},
        {"text": "、",     "start_ms": 1750, "end_ms": 1800},
        {"text": "あなたに", "start_ms": 1800, "end_ms": 2200},
        ...
      ]
    },
    ...
  ]
}
```

AssemblyAI's `/transcript/<id>/sentences` endpoint returns sentence-segmented output natively for Japanese, with start/end times in milliseconds and a `words` array per sentence. We pass it through with minor renaming.

## Quality notes

- AssemblyAI's Japanese sentence segmentation is decent but not perfect. It sometimes splits on partial particles or merges two short utterances.
- Word-level timing is per AssemblyAI's token, not per mecab token. The mapping back to mecab tokens in `analyze.py` is heuristic (substring match) — good enough to pick a screenshot frame, but don't trust it for sub-character precision.
- For music-heavy videos, expect 10-30% transcription noise. The `analyze.py` script doesn't try to clean this; bad input → fewer i+1 candidates.
