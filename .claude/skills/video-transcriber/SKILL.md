---
name: video-transcriber
description: "Transcribe MP4 videos into corrected plain-text transcripts for YouTube upload. Two-step pipeline: (1) AssemblyAI speech-to-text, (2) Gemini visual correction using the actual video. Use this skill whenever the user wants to transcribe a video, generate subtitles or captions, create a YouTube transcript, convert speech to text from a recording, or mentions AssemblyAI/Gemini transcription. Also trigger when the user has an MP4 and wants text output from it, even if they don't say 'transcribe' explicitly."
---

# Video Transcriber

Two-script pipeline that turns MP4 videos into accurate plain-text transcripts ready for YouTube upload.

## How it works

1. **`transcribe.py`** — Extracts audio via FFmpeg, uploads to AssemblyAI (Universal-3 Pro model), polls until done, saves raw transcript
2. **`correct.py`** — Uploads the entire video to Gemini's File API (gemini-2.5-flash), sends raw transcript for visual correction (cross-references on-screen text like slides, code, terminal output, names), outputs clean `.txt`

All outputs are saved to the `outputs/` folder inside this skill directory.

YouTube auto-syncs plain text to video timing, so no timestamps are needed.

## Prerequisites

- Python 3.10+ with venv at `.venv/` in this directory
- FFmpeg installed and on PATH
- API keys in `.env` file (see below)

## Setup

```bash
cd <skill-directory>
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

Add your API keys to the `.env` file in this skill's directory:
```
ASSEMBLYAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

## Usage

Always run scripts using the venv Python:

### Step 1: Transcribe with AssemblyAI

```bash
.venv/bin/python scripts/transcribe.py /path/to/video.mp4
```

Saves `<video-name>-raw.txt` to `outputs/`.

### Step 2: Correct with Gemini

```bash
.venv/bin/python scripts/correct.py /path/to/video.mp4 outputs/<video-name>-raw.txt
```

Saves `<video-name>.txt` to `outputs/` — ready to upload to YouTube.

## Why two scripts

Splitting the pipeline lets you re-run Gemini correction without re-transcribing (useful if you want to tweak the correction prompt or retry after a transient failure). It also means you can inspect the raw AssemblyAI output before spending Gemini credits on correction.

## Models used

- **AssemblyAI**: Universal-3 Pro (`universal-3-pro`) — highest accuracy for English, $0.21/hr
- **Gemini**: gemini-3-flash — fast, handles full video uploads via File API

## Key terms (word_boost)

The `word_boost` list in `transcribe.py` helps AssemblyAI correctly recognize domain-specific terms. Update this list if your videos frequently mention other terms that get misheard. Currently boosted: "Claude Code", "Anthropic", "Claude".

The Gemini correction prompt in `correct.py` also has a key terms section for the same purpose — keep both in sync.

## Learnings from first run

- AssemblyAI without `word_boost` consistently mishears "Claude Code" as "Claud Code", "cloud code", or "Claude cod" — the boost param set to "high" is essential
- Gemini 2.5 Flash handles full 7.5-minute / 355MB video uploads well with no chunking needed
- Gemini reliably fixes number misreadings (e.g. "890 minutes" → "8-9 minutes") and adds proper formatting for slash commands (`/memory`, `/dream`)
- The `google-generativeai` Python package is deprecated (EOL Nov 2025) — use `google-genai` with the `Client()` pattern instead
- AssemblyAI's `speech_model` (singular) parameter is deprecated — use `speech_models` (plural, array)
