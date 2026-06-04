# Bank Mode

Source: a **list of target words** (or a single word). For each word, find a natural example sentence inside Ray's locally-indexed subs2srs `.apkg` banks, reuse the bank's original audio + screenshot when present, and produce a draft card per word.

When this mode triggers:
- Ray pastes a list of Japanese words and says anything like "make cards", "mine these", "find sentences for", "leech these"
- Ray says "what's left in <show>" or "pull i+1 from my <show> bank" (a future variant — currently word-list only)
- Ray writes `/sentence-mining` with no URL and a list of words

If Ray gives a URL → that's [video-mode](video-mode.md), not bank mode.

## Why bank mode exists

Video mode is great when Ray has a *specific clip* he wants to mine. But often the trigger is the other direction: "I keep forgetting `同期`, give me a card." Bank mode answers that — it searches a corpus of Japanese sentences Ray already has indexed and pulls a sentence that uses the word in context, with the original native audio when the bank shipped one.

Cards built this way are tagged `claude-sentence-bank` (vs. `claude-sentence-mining` for video-sourced cards) and additionally `bank:<bank-id>` so you can filter by source show.

## Prerequisites

1. **At least one `.apkg` indexed** — see [setup](#one-time-setup-indexing-banks) below.
2. **AnkiConnect running** (port 8765) — same as video mode.
3. **GEMINI_API_KEY** in the skill's `.env` — only needed when a bank lacks audio for a chosen sentence (we synthesize via Gemini TTS).

## One-time setup: indexing banks

Banks live in `~/Library/CloudStorage/.../subs2srs/{Imported,Not Yet Imported}/` on Drive. **Don't copy the `.apkg` files locally** — the Imported folder alone is ~76 GB. Instead, extract them in place into local JSON indexes:

```bash
python3 <skill-dir>/scripts/extract_bank.py \
    "/Users/ray/Library/CloudStorage/GoogleDrive-the.rehman.amjad@gmail.com/My Drive/Projects/Japanese/Anki/subs2srs/Imported/"
# Or point at a single file:
python3 <skill-dir>/scripts/extract_bank.py "/path/to/specific.apkg"
```

Output lands in `~/Downloads/sentence-mining/banks/index/`:
- `<bank-id>.notes.json` — searchable index (1 record per note: sentence, audio refs, image refs, meaning)
- `<bank-id>.media/` — extracted audio+image with original filenames

The `<bank-id>` is derived from the source filename (NFC-normalized, alnum + Japanese + dash + underscore preserved). See [bank-formats.md](bank-formats.md) for known notetypes and the [apkg-schema.md](apkg-schema.md) for the underlying ZIP/SQLite layout.

**Re-extraction is safe** — `cp -n` semantics for media; JSON is overwritten. Run it again when Ray adds new banks.

**Big banks are slow.** A 1GB audiobook bank is mostly mp3s; extraction copies all of them. For audiobook/Terrace House sized banks, consider running with `--skip-media` (TODO — not yet implemented) and rehydrating per-card as needed.

## Step 1: Intake — collect the word list

Words can come in as:
- Comma-separated in chat: `同期, 西暦, 和暦`
- A file path Ray pastes
- A leech export Ray pastes (one word per line, possibly with reading/meaning columns — keep just the first column)

Normalize to a plain list of strings. Deduplicate preserving order.

## Step 2: Search banks

```bash
python3 <skill-dir>/scripts/search_banks.py \
    --words "同期,西暦,和暦" \
    --top-per-word 3 \
    --output ~/Downloads/sentence-mining/banksearch.json
```

For each word, the script scans every `<bank-id>.notes.json`, finds notes whose sentence contains the word as a literal substring, and ranks hits by:

| signal | points |
|---|---|
| Bank has audio for this note | +6 |
| Bank has image for this note | +4 |
| target_word field exactly equals the search word | +5 |
| Sentence length 15–50 chars (sweet spot for review) | +3 |
| Sentence length 8–14 or 51–80 chars (OK) | +1 |
| Word appears at a clean boundary (punctuation or end) | +2 |

Ties break by shorter sentence.

The script also records `bank_meaning` (English translation if the bank ships one), useful for sanity-checking the sense matches the one Ray wanted.

### Known limitation: literal substring matching

Current search is substring-only. `言う` won't match a sentence with `言って`. To handle inflected forms, mecab-tokenize the bank sentences at index time and store per-note lemma sets, then match lemma-to-lemma. Not done yet.

## Step 3: Curate — pick which hits become cards

Inline, look at the top hits per word and pick. Heuristic:

- **Prefer the one with audio + image** even if the sentence is slightly less elegant. A card with native audio + screenshot is a vastly better study artifact than a text-only one.
- **Clean obvious noise.** If the sentence is `(line1) (line2)` (subs2srs concatenated two subtitle frames), drop the chunk that doesn't contain the target word.
- **Drop dupes vs. Ray's existing cards.** Query AnkiConnect for `wordForm:<lemma> (deck:"Ray's Sentence Cards" OR deck:"Ray's Sentence Mining Deferred")` and skip any word that already has a card. **This step is currently a manual check** — automate it in `search_banks.py` next.
- **For zero-hit words**, tell Ray and ask. He may want to (a) index more banks, (b) accept a synthetic Claude-written example sentence with Gemini TTS, or (c) skip.

For each kept candidate, set `deck` to `Ray's Sentence Cards`. (Bank mode doesn't use the `Deferred` deck — these aren't i+2+ by definition since they're hand-selected.)

## Step 4: Generate explanations

Same as video-mode Step 4 — read [explanation-prompt.md](explanation-prompt.md), produce one `explanation` field per candidate inline using the prompt template (Japanese only, ~200–250 chars, no English).

If a candidate's audio comes from a bank's actual show (e.g., the Tokyo Ghoul subtitle audio), feel free to reference the source context in the explanation when natural — but don't overload the card with show-specific lore the next viewer won't know.

## Step 5: Generate media (bank-mode)

```bash
python3 <skill-dir>/scripts/generate_media_bank.py \
    --candidates ~/Downloads/sentence-mining/banksearch.json \
    --output ~/Downloads/sentence-mining/bank.draft.json
```

For each candidate:
- If `existing_audio` resolves to a real file → copies it to `<anki-media>/sm_bank_<bank-id>_<note-id>_sentence.<ext>` (preserves extension; `.ogg` files work in Anki natively).
- Else → calls Gemini TTS on the sentence text → `<anki-media>/sm_bank_<bank-id>_<note-id>_sentence_tts.mp3`.
- If `existing_image` resolves → copies it as `<anki-media>/sm_bank_<bank-id>_<note-id>_image.<ext>`. Else leaves picture field blank (no placeholder).
- Always runs Gemini TTS on the `explanation` text → `<anki-media>/sm_explain_bank_<bank-id>_<note-id>.mp3`.

This script differs from video-mode's `generate_media.py` in two ways: it never invokes ffmpeg for clipping (the bank already did that), and it skips screenshots entirely (the bank either shipped one or there isn't one).

## Step 6: Preview + approval

Same as video mode — print a summary and wait for Ray's confirmation. Distinguishing bits to surface:

```
Mined N bank cards (word list: <words>):

  1. 同期 [tokyo_ghoul_season_1] 🔊🖼
     "同期では二人 二人共 聡明で強い意思を持った女性でした"
  2. 西暦 [legend_of_the_galactic_heroes_eng_jp]
     "西暦2166年には 木星の衛星 イオに" (sentence TTS synthesized; no image)

  Misses: 和暦 (no hit across 10 indexed banks)
```

Always list misses explicitly so Ray can choose to add more banks or accept synthetic fallback.

## Step 7: Push

Same `push.py` as video mode — the script detects `source == "bank-search"` in the draft and applies the `claude-sentence-bank` permanent tag (vs. `claude-sentence-mining`). Cards also get `bank:<bank-id>` and `auto-mined:YYYY-MM-DD` tags.

Bank cards always land in `Ray's Sentence Cards` (no Deferred routing — see Step 3).

## Gotchas specific to bank mode

- **Substring match misses inflections.** Already mentioned; a real fix needs mecab at index time.
- **No AnkiMorphs known-check.** Ray might already know a word he sent; bank mode pushes a card anyway. Pre-flight check is on the TODO list.
- **Tag pollution from `bank:<bank-id>`.** If a bank-id has Japanese characters they'll be in the tag (`bank:くまクマ熊ベアー_1-300`). Anki handles this but tag autocomplete may behave oddly.
- **`Migaku Japanese` Audio field is often empty even though the notetype declares it.** The detector says the bank "has audio" structurally, but resolution at media-gen time falls back to TTS. This is the right behavior — the structural signal is still useful for ranking — but Ray may be surprised that a "Migaku" bank produces synthesized audio.
