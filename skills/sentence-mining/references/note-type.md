# `Ray's Sentence Mining` note type — field reference

13 fields. Names and order match what AnkiConnect reports for this model.

| Field | What this skill puts in it |
|---|---|
| `wordForm` | Dictionary form (lemma) of the unknown word, e.g. `気迫` |
| `reading` | Hiragana reading from mecab, e.g. `きはく` |
| `sentence` | The source sentence containing the word, as AssemblyAI transcribed it |
| `sentenceAudio` | `[sound:sm_<source-id>_<idx>.mp3]` — ffmpeg-clipped from the video |
| `picture` | `<img src="sm_<source-id>_<idx>.jpg">` — middle frame of the sentence's audio span |
| `explanation` | Claude-generated short Japanese explanation (style mirrors Ray's existing 9000+ cards) |
| `explanationAudio` | `[sound:sm_explain_<source-id>_<idx>.mp3]` — Gemini TTS of the explanation |
| `definition` | Empty — Ray fills via Yomitan at review time if needed |
| `wordAudio` | Empty — historically empty in Ray's deck |
| `pitchAccent` | Empty — could wire up NHK/Wadoku later, but not v1 |
| `frequency_yomitan` | Empty |
| `frequency_addon` | Empty |
| `source_url` | The original video URL Ray pasted |

Tags applied on every card:
- `auto-mined:YYYY-MM-DD` — so a day's batch is searchable
- `source:<source-id>` — e.g. `source:instagram-DZHudfuRmdJ`

Deferred (i+2/i+3+) cards go to deck `Ray's Sentence Cards::Deferred` and are suspended after add.
