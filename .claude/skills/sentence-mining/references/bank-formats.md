# Bank Formats

Each `.apkg` ships its own notetype with arbitrary field names. `extract_bank.py` detects field **roles** (sentence, audio, image, reading, meaning, target_word) per notetype via heuristics over a sample of notes. This doc explains those heuristics and lists known notetypes Ray's library uses.

## Field-role detection (what `detect_field_roles` actually does)

For each field of each notetype, we compute:
- `has_sound` — any value contains `[sound:…]`
- `has_img` — any value contains `<img src="…">`
- `has_furigana` — any value contains the `漢字[かんじ]` pattern
- `avg_jp` — average count of Japanese characters (kanji + kana) per value
- `avg_len` — average string length (after HTML strip)
- `mostly_ascii` — non-empty values are ≥80% ASCII

Then we assign roles in this order:

1. **audio** → first field with `has_sound`
2. **image** → first field with `has_img`
3. **sentence** → preferred candidate: a field whose *name* contains one of `expression`, `sentence`, `sentkanji`, `sentjp`, `japanese`, `context`, `text`, `front`, AND has Japanese content, AND is not a `notes`/`definition`/`extra` field. Among matches, prefer the one with **less furigana** (clean form > annotated form). If no named candidate, fall back to any Japanese-content field with the most kanji+kana that isn't audio/image.
4. **reading** → field with `has_furigana` (separate from sentence if possible). If only the sentence field has furigana, reading = sentence.
5. **meaning** → first `mostly_ascii` field (non-empty) that isn't audio/image/sentence.
6. **target_word** → field whose name contains `vocab`, `word`, `target`, or `morph`, AND has Japanese content with short avg length. Fall back to any short Japanese-content field that isn't the sentence.

### Why "less furigana wins" for sentence detection

`Japanese + subs2srs` (the Zelda Deathly Loneliness bank) has both `Expression` (clean) and `Reading` (with furigana). The Reading field has MORE Japanese characters because of the inline bracketed kana — a naive "most JP chars wins" heuristic picks it. But for review cards we want the clean form. Prefer non-furigana fields.

### Why we demote `Notes` fields

`subs2srs` notetypes have a `Notes` field that often contains a full dictionary entry — long, kanji-heavy, but not a sentence Ray would put on a card. Anything named `notes`, `definition`, `dict`, `extra`, or `comment` is excluded from the sentence-candidate pool.

## Known notetypes in Ray's library

These are the notetypes we've seen, with their detected role mapping. New banks may introduce new notetypes — re-run `extract_bank.py` to log them and update this list.

### `subs2srs` (Tokyo Ghoul, Madoka drama CD)
```
Fields: [SequenceMarker2, SequenceMarker, Audio, Snapshot, Expression, English, Reading, Notes]
Roles:  sentence=Expression, audio=Audio, image=Snapshot, meaning=English
```
Sentence is the subtitle line. Audio is the clipped audio. Snapshot is the screenshot.

### `Japanese + subs2srs` (Zelda Deathly Loneliness)
```
Fields: [Snapshot, Expression, Sentencee, Meaning, Reading, 2ndDef, Audio, SequenceMarker]
Roles:  sentence=Expression, audio=Audio, image=Snapshot, meaning=Meaning, reading=Reading
```
Identical to subs2srs but with extra dictionary fields. `Sentencee` (sic) is usually empty.

### `Japanese (recognition)` (Rick & Morty, Little Mermaid)
```
Fields: [Vocab, Reading, Expression, Meaning, Image, Audio]   # R&M variant — 6 fields
Fields: [Expression, Meaning, Reading]                         # Little Mermaid variant — 3 fields, no media
Roles:  sentence=Expression, meaning=Meaning, reading=Reading (often via furigana)
```
Common Refold/MIA shape. Sometimes ships with media, often doesn't.

### `Japanese v2-62274-e76b4` (Harry Potter 1 & 2)
```
Fields: [Expression, Reading, English, Audio]
Roles:  sentence=Expression, meaning=English, reading=Reading
```
Book deck. `Audio` field is present but empty in practice — these decks ship without TTS.

### `Japanese Sentences Listening 2020` (Legend of the Galactic Heroes)
```
Fields: [Expression, Reading, Context, MorphMan_FocusMorph, Meaning, SentenceAudio,
         EnglishTL, Vocab, VocabReading, VocabAudio, Episode, Homophones, Reverse]
Roles:  sentence=Expression, audio=SentenceAudio, image=Context, meaning=Meaning
```
Heavy notetype. Media references exist but the `.apkg` doesn't ship the files — they live in the user's `collection.media/`. Bank mode handles this by falling back to Gemini TTS when `existing_audio` doesn't resolve to a real file.

### `Migaku Japanese` (くまクマ熊ベアー)
```
Fields: [Expression, Meaning, Audio, Audio on Front]
Roles:  sentence=Expression, audio=Audio (often empty)
```
Vocab-style notetype where `Expression` IS the full sentence (one sentence per note).

### `Basic`
Standard Anki notetype. Fields: `[Front, Back]`. Hard to use for bank mining — `Front` and `Back` are application-specific, often Japanese ↔ English flashcards. Detection usually returns `sentence=None`. Skip unless overridden.

## Overriding role detection

When the heuristic guesses wrong (e.g., picks the Notes field as the sentence), edit `<bank-id>.notes.json` directly — the `models.<mid>.roles` block. Then re-run `search_banks.py`; it reads roles from the JSON, not from the heuristic.

A cleaner override path (TODO) would be a `references/bank-formats-overrides.json` file that lets you pin per-notetype role mappings. Worth adding the next time a new bank fights the heuristic.

## Edge cases

**Empty sentence-side fields.** Some notes have `Expression` blank (e.g., vocab-side only). `extract_bank.py` skips notes where both `sentence` AND `target_word` are empty.

**Subtitle-line concatenation.** subs2srs sometimes joins two adjacent subtitle lines into one note: `(line1)   (line2)`. The current extractor passes this through verbatim. When you build a card from such a note, clean the sentence by dropping the parenthesized chunk that doesn't contain the target word.

**Multiple media references per field.** Some banks have `[sound:foo.mp3][sound:bar.mp3]` in one field. The extractor captures all of them in `audio_files` but downstream picks the first one.

**HTML bolding.** Many vocab-side banks bold the target word: `今日は<b>同期</b>と飲みに行く`. The HTML strip in `extract_bank.py` removes the tags but keeps the content.

**Combining-mark filenames.** Drive sometimes stores filenames in NFD form (e.g., `ベアー` as `ヘ` + combining dakuten). `bank_id_from_path` NFC-normalizes the stem before slugifying, so `くまクマ熊ベアー` stays intact.
