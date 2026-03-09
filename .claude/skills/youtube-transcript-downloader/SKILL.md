---
name: youtube-transcripts
description: Download YouTube video transcripts as plain text files. Use when the user asks to download, fetch, or save transcripts/captions/subtitles from YouTube videos. Accepts video IDs or full YouTube URLs.
---

# YouTube Transcripts

Download YouTube transcripts using `scripts/download_transcript.py`. Uses the Supadata API for reliable transcript fetching. Transcripts are automatically organized into channel-name subfolders.

## Usage

```bash
python3 <skill-dir>/scripts/download_transcript.py <video_id_or_url> [more...] [--out-dir DIR]
```

- Accepts YouTube video IDs (`pb0lVGDiigI`) or full URLs (`https://youtube.com/watch?v=pb0lVGDiigI`)
- Automatically organizes transcripts into channel-name subfolders via `yt-dlp`
- Default output directory is the current working directory
- Reads `SUPADATA_API_KEY` from environment or `.env` file in project root

## Examples

Single video:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI --out-dir transcripts/
```

Output:
```
transcripts/
└── ray-amjad/
    └── pb0lVGDiigI.txt   # includes YAML frontmatter (title, date, video_id, channel)
```

Multiple videos:
```bash
python3 scripts/download_transcript.py pb0lVGDiigI mZzhfPle9QU --out-dir transcripts/
```

Output:
```
transcripts/
├── ray-amjad/
│   └── pb0lVGDiigI.txt
└── john-kim/
    └── mZzhfPle9QU.txt
```

## Requirements

- Python 3 (no pip packages needed — uses stdlib `urllib` for Supadata API)
- `yt-dlp` (for channel name lookup)
- `SUPADATA_API_KEY` environment variable (set in `.env`)
