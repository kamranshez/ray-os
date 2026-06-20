#!/usr/bin/env python3
"""Extract markers from a Premiere Pro .prproj file as YouTube chapter timestamps.

A .prproj is gzip-compressed XML (or plain XML if the project was saved
uncompressed). Timeline/comment markers are stored as <DVAMarker> elements
whose body is a small JSON blob holding the marker name and its start time in
"ticks". Premiere uses a fixed 254016000000 ticks per second.

Usage: extract_timestamps.py <path-to.prproj>
Output: one chapter per line, sorted chronologically, in the format "MM:SS - Name".
"""
import sys
import gzip
import re
import json

TICKS_PER_SECOND = 254016000000


def fmt(seconds):
    """YouTube-style timestamp: MM:SS, or H:MM:SS once we cross an hour.

    Floor (don't round) the seconds: a chapter must never start *after* its
    content begins, or YouTube shows the previous chapter's frame for it.
    """
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def load_xml(path):
    with open(path, "rb") as f:
        magic = f.read(2)
    if magic == b"\x1f\x8b":  # gzip
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            return f.read()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_markers(xml):
    markers = []
    for match in re.finditer(r"<DVAMarker>(.*?)</DVAMarker>", xml, re.S):
        raw = match.group(1)
        raw = (raw.replace("&quot;", '"').replace("&amp;", "&")
                  .replace("&lt;", "<").replace("&gt;", ">").replace("&apos;", "'"))
        try:
            data = json.loads(raw)["DVAMarker"]
        except Exception:
            continue
        ticks = data.get("mStartTime", {}).get("ticks")
        if ticks is None:
            continue
        name = (data.get("mName") or "").strip()
        markers.append((int(ticks) / TICKS_PER_SECOND, name))
    markers.sort(key=lambda x: x[0])
    return markers


def main(path):
    markers = extract_markers(load_xml(path))
    lines = []
    # YouTube only enables chapters when the first one starts at 0:00, so seed an
    # Intro chapter unless a marker already sits at the very start.
    if not markers or markers[0][0] > 0.5:
        lines.append("00:00 - Intro")
    for sec, name in markers:
        lines.append(f"{fmt(sec)} - {name}" if name else fmt(sec))
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: extract_timestamps.py <path-to.prproj>")
    main(sys.argv[1])
