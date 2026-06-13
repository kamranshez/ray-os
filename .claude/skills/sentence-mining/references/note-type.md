# Note type & field mapping

The skill writes onto whatever note type the user picks at setup (`config.note_type`).
It does **not** assume any specific field names — instead `config.field_map` maps the
skill's internal field **roles** onto that note type's actual fields. Only roles the
user mapped (non-empty) are written, so a minimal note type with just a word + a
sentence field works fine.

## Internal roles

| Role (config key) | Required | What this skill puts in it |
|---|---|---|
| `word` | **yes** | Dictionary form (lemma) of the unknown word, e.g. `気迫` |
| `sentence` | **yes** | The source sentence containing the word (video: as AssemblyAI transcribed it, with a `<b>Speaker:</b>` prefix when diarized; bank: the bank's sentence) |
| `reading` | no | Hiragana reading from mecab, e.g. `きはく` |
| `sentence_audio` | no | `[sound:…mp3]` — ffmpeg clip (video) or bank audio / Gemini TTS (bank) |
| `picture` | no | `<img src="…jpg">` — middle frame (video) or bank screenshot (bank) |
| `explanation` | no | Claude-generated short Japanese explanation (style mirrors Ray's existing 9000+ cards) |
| `explanation_audio` | no | `[sound:…mp3]` — Gemini TTS of the explanation |
| `source_url` | no | The original video URL (video mode) |

Any other fields the note type has (definition, pitch accent, frequency, etc.) are
left untouched for the user to fill at review time (e.g. via Yomitan).

## Ray's mapping (for reference)

Ray's note type is `Ray's Sentence Mining` (15 fields). His `config.field_map`:
`word→wordForm`, `reading→reading`, `sentence→sentence`, `sentence_audio→sentenceAudio`,
`picture→picture`, `explanation→explanation`, `explanation_audio→explanationAudio`,
`source_url→source_url`. The remaining fields (`definition`, `wordAudio`,
`pitchAccent`, `frequency_yomitan`, `frequency_addon`) are left empty.

## Tags

Every card gets exactly two tags (set by `push.py`):
- the permanent kind tag — `claude-sentence-mining` (video) or `claude-sentence-bank` (bank)
- the i-level — `i1` / `i2` / `i3` / `i?`

Nothing is suspended. Deferred (i+2/i+3) video cards go to `config.decks.deferred`
(a top-level sibling deck), not a subdeck, and stay unsuspended.
