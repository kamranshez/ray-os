#!/usr/bin/env bash
# Overlay Ray's transparent face PNG onto a generated faceless thumbnail.
# Usage: composite-face.sh <input.png> <output.png>
set -euo pipefail

INPUT="$1"
OUTPUT="$2"
FACE="/Users/ray/Desktop/ray-os/.claude/skills/youtube-ab-tester/references/rays-face/go-to-face.png"

W=$(magick identify -format '%w' "$INPUT")
H=$(magick identify -format '%h' "$INPUT")

magick "$INPUT" \
  \( "$FACE" -resize "${W}x${H}!" \) \
  -compose over -composite \
  "$OUTPUT"

echo "Composited: $OUTPUT (${W}x${H})"
