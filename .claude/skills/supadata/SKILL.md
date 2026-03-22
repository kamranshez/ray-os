---
name: supadata
description: YouTube data utility — fetch transcripts, metadata, thumbnails, and search for videos. Wraps the Supadata API and yt-dlp into a single CLI tool. Use whenever you need YouTube data like transcripts, video metadata, thumbnail images, or need to search YouTube for videos matching a query. Triggers on any YouTube data fetching need from other skills or direct user requests.
---

## Overview

A reusable YouTube data utility that combines:
- **Supadata API** for transcript fetching (handles async/queued jobs)
- **yt-dlp** for metadata, search, and thumbnail downloads

Other skills (youtube-transcript-downloader, youtube-thumbnail-generator, competitor-monitor) should call this script rather than reimplementing YouTube data logic.

## CLI Usage

```bash
python3 .claude/skills/supadata/scripts/supadata.py <command> [args]
```

### Commands

#### `transcript` — Fetch video transcript
```bash
python3 .claude/skills/supadata/scripts/supadata.py transcript <video_id_or_url> [--out-dir DIR]
```
Returns plain text transcript. Handles Supadata's async job polling automatically.

#### `metadata` — Get video metadata
```bash
python3 .claude/skills/supadata/scripts/supadata.py metadata <video_id_or_url>
```
Returns JSON: `{"channel": "...", "title": "...", "date": "YYYY-MM-DD", "video_id": "..."}`.

#### `search` — Search YouTube for videos
```bash
python3 .claude/skills/supadata/scripts/supadata.py search "<query>" [--max N]
```
Returns JSON array of `{"video_id", "title", "channel", "url"}` objects. Default max: 10.

#### `thumbnail` — Download video thumbnail
```bash
python3 .claude/skills/supadata/scripts/supadata.py thumbnail <video_id_or_url> [--out-dir DIR] [--quality maxresdefault|hqdefault|mqdefault]
```
Downloads the highest quality thumbnail available. Saves as `<video_id>.jpg`.

#### `batch-thumbnails` — Search + download thumbnails in one shot
```bash
python3 .claude/skills/supadata/scripts/supadata.py batch-thumbnails "<query>" [--max N] [--out-dir DIR]
```
Searches YouTube for videos matching the query, then downloads all their thumbnails. Useful for competitive thumbnail research.

## Requirements

- `SUPADATA_API_KEY` in project `.env` file (for transcripts)
- `yt-dlp` installed (for metadata, search, thumbnails)

## Notes

- Transcript fetching handles both sync (HTTP 200) and async (HTTP 202 with job polling, up to 2 min)
- Thumbnail quality falls back gracefully: maxresdefault -> hqdefault -> mqdefault -> default
- Search uses yt-dlp's `ytsearch` extractor
