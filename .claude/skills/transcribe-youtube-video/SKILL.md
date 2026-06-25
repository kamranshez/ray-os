---
name: transcribe-youtube-video
description: "Transcribe audio or video into a clean .txt + timestamped .srt + YouTube chapter timestamps. Re-encodes any WAV/MP4 to a small MP3 before upload, mines on-screen text with OCR to seed AssemblyAI key terms, runs AssemblyAI Universal-3 Pro speech-to-text, then generates punchy chapter markers from the SRT. Use whenever the user wants to transcribe a video or audio file, generate subtitles/captions or an SRT, create a YouTube transcript or chapters, or convert a recording to text. Also trigger when the user has a WAV/MP4/MOV and wants text out of it, even without saying 'transcribe'."
---

# Video / Audio Transcriber

Single-pass pipeline: any audio/video file in; a clean `.txt`, a timestamped `.srt`, and a YouTube `.chapters.txt` out — ready for upload. On-screen text is OCR'd first to boost recognition of names, products, and rare technical terms.

## How it works

1. **`extract_keyterms.py`** (optional, when a video is available) — extracts scene-change + periodic frames, OCRs them with tesseract, and prints a frequency-ranked candidate word list. Claude curates this noisy list into a clean `keyterms.txt` (proper nouns, product/people names, rare tech terms — not common English words).
2. **`transcribe.py`** — re-encodes the input to a small mono 64k MP3 (a 200 MB WAV becomes ~5 MB on the wire), uploads to AssemblyAI (Universal-3 Pro), boosts the key terms via `keyterms_prompt`, then saves the plain `.txt` and the `.srt`.
3. **Chapters (Claude step)** — Claude reads the `.srt`, finds the topic transitions, and writes `<basename>.chapters.txt` in the **Punchy Keywords** style (see below). No extra API or model key; AssemblyAI's `auto_chapters` is deliberately NOT used (it forces a downgrade off `universal-3-pro` and emits verbose sentence summaries, not short labels).

YouTube auto-syncs plain text to video timing, and the `.srt` carries real timestamps for captions/chapters.

## Prerequisites

- Python 3.10+ with venv at `.venv/` in this directory
- `ffmpeg` and `tesseract` installed and on PATH
- `ASSEMBLYAI_API_KEY` in the `.env` file in this skill's directory

## Setup

```bash
cd <skill-directory>
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

`.env`:
```
ASSEMBLYAI_API_KEY=your_key_here
```

## Usage

Always use the venv Python.

### Step 1 (optional, video only): mine on-screen key terms

```bash
.venv/bin/python scripts/extract_keyterms.py /path/to/video.mp4 --out /tmp/candidates.txt
```

Review the printed candidate list and write a curated `keyterms.txt` — one term per line. Keep only terms that speech-to-text is likely to mishear: model/product names, people, rare jargon. Skip common words.

### Step 2: transcribe

```bash
# audio or video input; --out sets the output basename; --keyterms is optional
.venv/bin/python scripts/transcribe.py "/path/to/Audio.wav" \
  --out "/path/to/my-video" \
  --keyterms /tmp/keyterms.txt
```

Saves `my-video.txt` and `my-video.srt`. If `--out` is omitted, outputs land in this skill's `outputs/<input-stem>.{txt,srt}`.

### Step 3: generate chapters (always)

After transcribing, Claude reads `<basename>.srt` and writes `<basename>.chapters.txt` — YouTube chapter markers in the **Punchy Keywords** style. This is a Claude reasoning step (semantic topic detection + short labeling), not a script.

How to build them:
1. Read the `.srt` and scan for topic transitions (new subject, demo start, sponsor/class plug, caveats section, outro).
2. Pick ~8–13 chapters for a 10–15 min video. The **first chapter must be `00:00`** (YouTube requirement) and chapters must be ≥10s apart and in ascending order.
3. Use the timestamp of the *first* SRT cue where the new topic begins, formatted `MM:SS` (or `HH:MM:SS` past an hour).
4. Title each chapter in **Punchy Keywords** style and write one per line.

**Punchy Keywords style (the format to use):**
- 1–3 words per label, Title Case, no trailing punctuation.
- Plain noun phrases or the proper noun that defines the segment (a person/product/concept name beats a generic word).
- Use `&` for "and"; use `x` for "times/multiplied by" (e.g. `Impact x Opportunity`).
- First label is `Intro`, last is `Outro`.
- No em or en dashes anywhere; the line separator is a plain `" - "` (hyphen).

Format and worked example (an 11-min video):
```
00:00 - Intro
00:56 - The Mistake
01:15 - The Carlini Method
01:50 - Sweep & Score
03:11 - Impact x Opportunity
04:49 - Demo
07:16 - The Class
08:00 - Root Cause
09:21 - Caveats
10:05 - Build the Machine
10:47 - Outro
```

## Models / settings

- **AssemblyAI**: Universal-3 Pro (`universal-3-pro`), `language_detection` on, `keyterms_prompt` for boosting.
- The input is always re-encoded to mono 64k MP3 first to minimize upload size — works for WAV, MP4, MOV, etc.

## Key terms

`BASE_KEYTERMS` in `transcribe.py` (`Claude Code`, `Anthropic`, `Claude`) are always boosted. Per-video terms from `extract_keyterms.py` are merged on top, de-duped, base terms first.

## Learnings

- AssemblyAI without key-term boosting mishears "Claude Code" as "Claud Code"/"cloud code"; `keyterms_prompt` fixes it. OCR-seeded terms also nail product/people names (e.g. "Fable 5", "Nicholas Carlini", "AgentStack", "Excalidraw").
- OCR of a full screen recording is noisy (browser chrome, URLs). Frequency-rank and let Claude curate — don't feed raw OCR straight into `keyterms_prompt`.
- Re-encoding to mono 64k MP3 cuts a ~200 MB WAV to ~5 MB with no measurable accuracy loss.
- AssemblyAI's `speech_model` (singular) is deprecated — use `speech_models` (plural array).
- The `/transcript/{id}/srt` endpoint returns ready-to-use SRT; no local timing math needed.
- AssemblyAI `auto_chapters` is INCOMPATIBLE with `universal-3-pro` (400 error) and only runs on the older `universal` model, and its output is verbose sentence gists. So chapters are generated by Claude from the SRT instead — better style, no accuracy downgrade, no second pass.
