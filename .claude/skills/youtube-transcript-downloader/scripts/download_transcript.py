#!/usr/bin/env python3
"""Download YouTube transcript(s) as plain text files, organized by channel.

Usage:
    python download_transcript.py <video_id_or_url> [video_id_or_url ...] [--out-dir DIR]

Transcripts are automatically saved into channel-name subfolders as <channel>/<video_id>.txt.
Uses the Supadata API for transcript fetching and yt-dlp for metadata.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.request
import urllib.parse
import json


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


def extract_video_id(value: str) -> str:
    """Extract a YouTube video ID from a URL or return the value as-is."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    # Assume it's already a video ID
    if re.match(r"^[A-Za-z0-9_-]{11}$", value):
        return value
    print(f"Warning: '{value}' doesn't look like a valid video ID or URL", file=sys.stderr)
    return value


def slugify_channel(name: str) -> str:
    """Convert a channel name to a filesystem-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[''']", "", slug)  # Remove apostrophes
    slug = re.sub(r"[^a-z0-9]+", "-", slug)  # Replace non-alphanumeric with hyphens
    slug = slug.strip("-")
    return slug


def get_video_metadata(video_id: str) -> dict:
    """Fetch channel, title, and upload date for a video using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "%(channel)s|||%(title)s|||%(upload_date)s", "--skip-download",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split("|||")
            if len(parts) == 3:
                channel, title, upload_date = parts
                # Format upload_date from YYYYMMDD to YYYY-MM-DD
                if len(upload_date) == 8 and upload_date.isdigit():
                    upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                return {"channel": channel, "title": title, "date": upload_date}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return {}


def fetch_transcript_supadata(video_id: str) -> str:
    """Fetch transcript text from Supadata API."""
    api_key = os.environ.get("SUPADATA_API_KEY", "")
    if not api_key:
        raise RuntimeError("SUPADATA_API_KEY not set. Add it to your .env file.")

    url = f"https://api.supadata.ai/v1/transcript?url={urllib.parse.quote(f'https://www.youtube.com/watch?v={video_id}')}&text=true&mode=auto&lang=en"
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
        print(f"  Transcript queued (job {job_id}), polling...")
        import time
        for _ in range(120):  # poll up to 2 minutes
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

    # Direct response
    if "content" in data:
        return data["content"]

    raise RuntimeError(f"Unexpected Supadata response: {data}")


def build_frontmatter(video_id: str, metadata: dict) -> str:
    """Build YAML frontmatter string from video metadata."""
    safe_title = metadata.get("title", "").replace('"', '\\"')
    lines = ["---"]
    if safe_title:
        lines.append(f'title: "{safe_title}"')
    if metadata.get("date"):
        lines.append(f'date: {metadata["date"]}')
    lines.append(f"video_id: {video_id}")
    if metadata.get("channel"):
        lines.append(f'channel: {slugify_channel(metadata["channel"])}')
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + "\n"


def download_transcript(video_id: str, out_dir: str) -> str:
    """Download transcript for a single video. Returns output path."""
    text = fetch_transcript_supadata(video_id)

    target_dir = out_dir
    metadata = get_video_metadata(video_id)
    channel = metadata.get("channel")
    if channel:
        slug = slugify_channel(channel)
        target_dir = os.path.join(out_dir, slug)
        print(f"  Channel: {channel} -> {slug}/")
    else:
        print(f"  Warning: couldn't fetch channel name, saving to root dir", file=sys.stderr)

    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, f"{video_id}.txt")
    frontmatter = build_frontmatter(video_id, metadata)
    with open(out_path, "w") as f:
        f.write(frontmatter + text)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Download YouTube transcripts")
    parser.add_argument("videos", nargs="+", help="Video IDs or YouTube URLs")
    parser.add_argument("--out-dir", default=".", help="Output directory (default: current dir)")
    args = parser.parse_args()

    _load_env()
    os.makedirs(args.out_dir, exist_ok=True)

    for value in args.videos:
        video_id = extract_video_id(value)
        print(f"Downloading transcript for {video_id}...")
        try:
            out_path = download_transcript(video_id, args.out_dir)
            print(f"  Saved to {out_path}")
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
