#!/usr/bin/env bash
# Lists videos from a YouTube channel as JSON, filtered by minimum duration.
# Usage: list-channel.sh <channel-url-or-handle> [--min-duration MINUTES] [--max-videos N]
# Output: JSON array of {video_id, title, duration_sec, url} sorted newest-first.

set -euo pipefail

channel=""
min_duration=20
max_videos=0

while [ $# -gt 0 ]; do
  case "$1" in
    --min-duration) min_duration="$2"; shift 2 ;;
    --max-videos)   max_videos="$2"; shift 2 ;;
    *)              channel="$1"; shift ;;
  esac
done

if [ -z "$channel" ]; then
  echo "error: channel URL or @handle required" >&2
  exit 2
fi

# Normalise: a bare @handle gets the youtube.com/<handle>/videos URL.
case "$channel" in
  @*) channel="https://www.youtube.com/${channel}/videos" ;;
  http*) ;;
  *)  channel="https://www.youtube.com/@${channel}/videos" ;;
esac

min_seconds=$((min_duration * 60))

raw=$(yt-dlp --flat-playlist --dump-json "$channel" 2>/dev/null)

if [ "$max_videos" -gt 0 ]; then
  echo "$raw" | jq -s --argjson min "$min_seconds" --argjson cap "$max_videos" '
    map({video_id: .id, title: .title, duration_sec: .duration, url: .url})
    | map(select(.duration_sec >= $min))
    | .[0:$cap]
  '
else
  echo "$raw" | jq -s --argjson min "$min_seconds" '
    map({video_id: .id, title: .title, duration_sec: .duration, url: .url})
    | map(select(.duration_sec >= $min))
  '
fi
