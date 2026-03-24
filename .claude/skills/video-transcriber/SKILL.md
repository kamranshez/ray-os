---
name: video-transcriber
description: "Transcribe MP4 videos into corrected plain-text transcripts for YouTube upload. Two-step pipeline: (1) AssemblyAI speech-to-text, (2) Gemini visual correction using the actual video. Use this skill whenever the user wants to transcribe a video, generate subtitles or captions, create a YouTube transcript, convert speech to text from a recording, or mentions AssemblyAI/Gemini transcription. Also trigger when the user has an MP4 and wants text output from it, even if they don't say 'transcribe' explicitly."
---

# Video Transcriber

Two-script pipeline that turns MP4 videos into accurate plain-text transcripts ready for YouTube upload.

## How it works

1. **`transcribe.py`** — Extracts audio via FFmpeg, uploads to AssemblyAI, polls until done, saves raw transcript
2. **`correct.py`** — Uploads the entire video to Gemini's File API, sends raw transcript for visual correction (cross-references on-screen text like slides, code, terminal output, names), outputs clean `.txt`

YouTube auto-syncs plain text to video timing, so no timestamps are needed.

## Prerequisites

- Python 3.10+
- FFmpeg installed and on PATH
- API keys in `.env` file (see below)

## Setup

```bash
cd <skill-directory>
pip install -r scripts/requirements.txt
```

Add your API keys to the `.env` file in this skill's directory:
```
ASSEMBLYAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

## Usage

### Step 1: Transcribe with AssemblyAI

```bash
python scripts/transcribe.py /path/to/video.mp4
```

This extracts audio, uploads to AssemblyAI, and saves `video-raw.txt` in the current directory.

### Step 2: Correct with Gemini

```bash
python scripts/correct.py /path/to/video.mp4 video-raw.txt
```

This uploads the full video to Gemini, cross-references the transcript against what's actually said and shown on screen, and saves `video.txt` — ready to upload to YouTube.

## Why two scripts

Splitting the pipeline lets you re-run Gemini correction without re-transcribing (useful if you want to tweak the correction prompt or retry after a transient failure). It also means you can inspect the raw AssemblyAI output before spending Gemini credits on correction.
