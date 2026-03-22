#!/usr/bin/env python3
"""YouTube data utility — transcripts, metadata, search, and thumbnails.

Usage:
    supadata.py transcript <video_id_or_url> [--out-dir DIR]
    supadata.py metadata <video_id_or_url>
    supadata.py search "<query>" [--max N]
    supadata.py thumbnail <video_id_or_url> [--out-dir DIR] [--quality QUALITY]
    supadata.py batch-thumbnails "<query>" [--max N] [--out-dir DIR]

Combines Supadata API (transcripts) with yt-dlp (metadata, search, thumbnails).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request


# ---------------------------------------------------------------------------
# Env loading
# ---------------------------------------------------------------------------

def _load_env():
    """Load .env file if SUPADATA_API_KEY not already set."""
    if os.environ.get("SUPADATA_API_KEY"):
        return
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]
    for env_path in env_paths:
        env_path = os.path.normpath(env_path)
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ.setdefault(key.strip(), val.strip())
            break


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_video_id(value: str) -> str:
    """Extract a YouTube video ID from a URL or return the value as-is."""
    patterns = [r"(?:v=|/v/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})"]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    if re.match(r"^[A-Za-z0-9_-]{11}$", value):
        return value
    print(f"Warning: '{value}' doesn't look like a valid video ID or URL", file=sys.stderr)
    return value


def slugify(name: str) -> str:
    """Convert a string to a filesystem-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


# ---------------------------------------------------------------------------
# Supadata API — Transcripts
# ---------------------------------------------------------------------------

def fetch_transcript(video_id: str) -> str:
    """Fetch transcript text from Supadata API. Handles async job polling."""
    api_key = os.environ.get("SUPADATA_API_KEY", "")
    if not api_key:
        raise RuntimeError("SUPADATA_API_KEY not set. Add it to your .env file.")

    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    url = f"https://api.supadata.ai/v1/transcript?url={urllib.parse.quote(yt_url)}&text=true&mode=auto&lang=en"
    req = urllib.request.Request(url, headers={
        "x-api-key": api_key,
        "User-Agent": "ray-os/1.0",
    })

    with urllib.request.urlopen(req, timeout=90) as resp:
        status = resp.status
        data = json.loads(resp.read().decode())

    # Handle async job (HTTP 202)
    if status == 202 and "jobId" in data:
        job_id = data["jobId"]
        print(f"  Transcript queued (job {job_id}), polling...", file=sys.stderr)
        for _ in range(120):
            time.sleep(1)
            job_url = f"https://api.supadata.ai/v1/transcript/{job_id}"
            job_req = urllib.request.Request(job_url, headers={"x-api-key": api_key})
            with urllib.request.urlopen(job_req, timeout=30) as job_resp:
                job_data = json.loads(job_resp.read().decode())
            if job_data.get("status") == "completed":
                return job_data["content"]
            elif job_data.get("status") == "failed":
                raise RuntimeError(f"Supadata job failed: {job_data.get('error', 'unknown error')}")
        raise RuntimeError("Supadata job timed out after 2 minutes")

    if "content" in data:
        return data["content"]

    raise RuntimeError(f"Unexpected Supadata response: {data}")


# ---------------------------------------------------------------------------
# yt-dlp — Metadata
# ---------------------------------------------------------------------------

def get_metadata(video_id: str) -> dict:
    """Fetch channel, title, and upload date for a video using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "%(channel)s|||%(title)s|||%(upload_date)s",
             "--skip-download", f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split("|||")
            if len(parts) == 3:
                channel, title, upload_date = parts
                if len(upload_date) == 8 and upload_date.isdigit():
                    upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                return {"channel": channel, "title": title, "date": upload_date, "video_id": video_id}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return {"video_id": video_id}


# ---------------------------------------------------------------------------
# yt-dlp — Search
# ---------------------------------------------------------------------------

def search_videos(query: str, max_results: int = 10) -> list[dict]:
    """Search YouTube for videos matching a query. Returns list of video info."""
    try:
        result = subprocess.run(
            ["yt-dlp", f"ytsearch{max_results}:{query}",
             "--print", "%(id)s|||%(title)s|||%(channel)s|||%(webpage_url)s",
             "--skip-download", "--no-warnings"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            videos = []
            for line in result.stdout.strip().split("\n"):
                parts = line.split("|||")
                if len(parts) == 4:
                    videos.append({
                        "video_id": parts[0],
                        "title": parts[1],
                        "channel": parts[2],
                        "url": parts[3],
                    })
            return videos
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"Search error: {e}", file=sys.stderr)
    return []


# ---------------------------------------------------------------------------
# yt-dlp — Thumbnails
# ---------------------------------------------------------------------------

THUMBNAIL_QUALITIES = ["maxresdefault", "hqdefault", "mqdefault", "default"]


def download_thumbnail(video_id: str, out_dir: str = ".", quality: str = "maxresdefault") -> str | None:
    """Download a video's thumbnail. Falls back through quality levels."""
    os.makedirs(out_dir, exist_ok=True)

    # Try requested quality first, then fall back
    qualities = THUMBNAIL_QUALITIES[THUMBNAIL_QUALITIES.index(quality):] if quality in THUMBNAIL_QUALITIES else THUMBNAIL_QUALITIES

    for q in qualities:
        url = f"https://img.youtube.com/vi/{video_id}/{q}.jpg"
        out_path = os.path.join(out_dir, f"{video_id}.jpg")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ray-os/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    data = resp.read()
                    # Skip tiny placeholder images (YouTube returns a small grey image for missing thumbnails)
                    if len(data) > 2000:
                        with open(out_path, "wb") as f:
                            f.write(data)
                        return out_path
        except Exception:
            continue

    print(f"  Could not download thumbnail for {video_id}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

def cmd_transcript(args):
    video_id = extract_video_id(args.video)
    text = fetch_transcript(video_id)
    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        out_path = os.path.join(args.out_dir, f"{video_id}.txt")
        meta = get_metadata(video_id)
        frontmatter = "---\n"
        if meta.get("title"):
            frontmatter += f'title: "{meta["title"]}"\n'
        if meta.get("date"):
            frontmatter += f'date: {meta["date"]}\n'
        frontmatter += f"video_id: {video_id}\n"
        if meta.get("channel"):
            frontmatter += f"channel: {slugify(meta['channel'])}\n"
        frontmatter += "---\n\n"
        with open(out_path, "w") as f:
            f.write(frontmatter + text)
        print(f"Saved to {out_path}")
    else:
        print(text)


def cmd_metadata(args):
    video_id = extract_video_id(args.video)
    meta = get_metadata(video_id)
    print(json.dumps(meta, indent=2))


def cmd_search(args):
    videos = search_videos(args.query, args.max)
    print(json.dumps(videos, indent=2))


def cmd_thumbnail(args):
    video_id = extract_video_id(args.video)
    out_dir = args.out_dir or "."
    result = download_thumbnail(video_id, out_dir, args.quality)
    if result:
        print(f"Saved: {result}")
    else:
        print(f"Failed to download thumbnail for {video_id}", file=sys.stderr)
        sys.exit(1)


def cmd_batch_thumbnails(args):
    out_dir = args.out_dir or "."
    print(f"Searching for: {args.query} (max {args.max})...")
    videos = search_videos(args.query, args.max)
    print(f"Found {len(videos)} videos")

    downloaded = []
    for v in videos:
        vid = v["video_id"]
        result = download_thumbnail(vid, out_dir)
        if result:
            print(f"  {v['title'][:60]} -> {result}")
            downloaded.append({"path": result, **v})

    # Write manifest
    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(downloaded, f, indent=2)
    print(f"\nDownloaded {len(downloaded)}/{len(videos)} thumbnails")
    print(f"Manifest: {manifest_path}")


def main():
    _load_env()

    parser = argparse.ArgumentParser(description="YouTube data utility")
    sub = parser.add_subparsers(dest="command", required=True)

    # transcript
    p = sub.add_parser("transcript", help="Fetch video transcript")
    p.add_argument("video", help="Video ID or URL")
    p.add_argument("--out-dir", help="Output directory (prints to stdout if omitted)")
    p.set_defaults(func=cmd_transcript)

    # metadata
    p = sub.add_parser("metadata", help="Get video metadata")
    p.add_argument("video", help="Video ID or URL")
    p.set_defaults(func=cmd_metadata)

    # search
    p = sub.add_parser("search", help="Search YouTube for videos")
    p.add_argument("query", help="Search query")
    p.add_argument("--max", type=int, default=10, help="Max results (default: 10)")
    p.set_defaults(func=cmd_search)

    # thumbnail
    p = sub.add_parser("thumbnail", help="Download video thumbnail")
    p.add_argument("video", help="Video ID or URL")
    p.add_argument("--out-dir", default=".", help="Output directory")
    p.add_argument("--quality", default="maxresdefault",
                   choices=THUMBNAIL_QUALITIES, help="Thumbnail quality")
    p.set_defaults(func=cmd_thumbnail)

    # batch-thumbnails
    p = sub.add_parser("batch-thumbnails", help="Search + download thumbnails")
    p.add_argument("query", help="Search query")
    p.add_argument("--max", type=int, default=10, help="Max results (default: 10)")
    p.add_argument("--out-dir", default=".", help="Output directory")
    p.set_defaults(func=cmd_batch_thumbnails)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
