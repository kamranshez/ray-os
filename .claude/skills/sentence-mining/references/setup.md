# Setup mode — write `config.json` for this user

Goal: produce `<skill-dir>/config.json` so every script knows this user's note
type, fields, decks, known-word sources, and sentence banks. This is what makes
the skill shareable — a friend runs `/sentence-mining setup` and is mining on
their own collection minutes later, with nothing about anyone else hardcoded.

Route here when the user says "setup" / "set up sentence mining", or whenever a
mining request arrives and `config.json` does not exist yet.

`config.json` is git-ignored. Never commit it; never copy one user's into another's.

## Step 1 — Probe the environment

```bash
python3 <skill-dir>/scripts/setup.py --probe
```

This prints JSON with: AnkiConnect reachability + version; every note type and its
field names; the deck list; which CLI tools (`yt-dlp`, `ffmpeg`, `mecab`) and
Python packages are present; which API keys are set; and the current config if any.

If AnkiConnect is unreachable, tell the user to open Anki (and install the
AnkiConnect add-on, code `2055492159`) and stop. If tools/packages/keys are
missing, surface exactly which, with the install commands from SKILL.md's "required
env" section. Don't proceed to write config until at least AnkiConnect + the field
choices are resolvable.

## Step 2 — Interview (use AskUserQuestion)

Drive these with `AskUserQuestion`, pre-filling smart defaults from the probe so
the user mostly confirms rather than types.

1. **Note type** — the model new cards are created on. List `note_types` from the
   probe; let them pick. If they don't have one, point them at `note-type.md` and
   offer to help create one, or pick an existing close match.

2. **Field mapping** — map the skill's internal roles onto that note type's actual
   field names. Propose a mapping by matching field names (e.g. a field called
   `sentence`/`Expression` → `sentence`; `wordForm`/`Vocab`/`Word` → `word`) and
   ask them to confirm/adjust. Roles:
   - `word` (**required**) — the target lemma
   - `sentence` (**required**) — the example sentence
   - `reading`, `sentence_audio`, `picture`, `explanation`, `explanation_audio`,
     `source_url` (all optional — leave blank to skip; only mapped roles get written)

3. **Decks** — `main` (i+1 cards, daily review) and optionally `deferred`
   (i+2/i+3). Pick from the probe's deck list or name new ones (created on first
   push). If `deferred` is blank it falls back to `main`.

4. **Known-word sources** — see [known-words.md](known-words.md). Ask which decks/
   note types hold Japanese they've already studied; build a `sources` entry per
   answer as `{ "query": "note:\"X\"" | "deck:\"Y\"", "field": "<jp field>" }`.
   At minimum include their sentence-mining deck's sentence field. If they're
   coming from AnkiMorphs, offer to import its note filters from
   `addons21/<id>/meta.json` (`config.filters`). Confirm `interval_threshold`
   (default 21).

5. **JPDB priority CSV** (optional) — path to a frequency list for ranking
   unknowns. Blank is fine (ranking falls back to source order).

6. **Sentence banks** — ask: *"Do you have any sentence banks (subs2srs `.apkg`
   files) you'd like to fall back on for words not found in videos?"* If yes, get
   the folder path → set `banks.source_dir`. Offer to index now (Step 4).

## Step 3 — Write `config.json`

Write the file directly (Write tool) using the shape in `config.example.json`.
Only include roles the user mapped. Then validate:

```bash
python3 <skill-dir>/scripts/setup.py --validate
```

Fix anything it flags (missing field on the note type, etc.). A `decks.*` "does
not exist yet" warning is fine — decks are created on first push.

## Step 4 — Index banks (if they have them)

```bash
python3 <skill-dir>/scripts/extract_bank.py          # uses config.banks.source_dir → index_dir
# or a single file: extract_bank.py "/path/to/One Show.apkg"
```

Large libraries take a while (one `.apkg` per show). Report bank_id + note counts
per bank. After this, bank mode is ready.

## Step 5 — Confirm and continue

Summarize what was written (note type, decks, # known-sources, # banks indexed),
then proceed with the user's original request (or tell them they can now mine a
video URL or a word list).
