#!/usr/bin/env python3
"""
Mine on-screen text from a video to seed AssemblyAI key terms.

Extracts scene-change + periodic frames, OCRs them with tesseract, and prints a
frequency-ranked candidate word list. OCR of a screen recording is NOISY, so
this does NOT write the final keyterms file directly — the caller (Claude)
reviews the candidates and writes a curated keyterms.txt (proper nouns, product
names, people, rare tech terms). Boosting common English words is pointless;
only ambiguous/rare terms help AssemblyAI.

Requires: ffmpeg, tesseract on PATH.

Usage:
  python extract_keyterms.py <video> [--out candidates.txt] [--min-count 2]
"""

import sys
import os
import argparse
import subprocess
import tempfile
import re
from collections import Counter
from pathlib import Path


def extract_frames(video: str, frames_dir: str) -> int:
    # Scene-change frames (slide transitions) ...
    subprocess.run(
        ["ffmpeg", "-y", "-i", video,
         "-vf", "select='gt(scene,0.3)',scale=1280:-1", "-vsync", "vfr", "-q:v", "3",
         os.path.join(frames_dir, "scene_%04d.jpg")],
        check=True, capture_output=True,
    )
    # ... plus a periodic grid so nothing static is missed.
    subprocess.run(
        ["ffmpeg", "-y", "-i", video,
         "-vf", "fps=1/6,scale=1280:-1", "-q:v", "3",
         os.path.join(frames_dir, "grid_%04d.jpg")],
        check=True, capture_output=True,
    )
    return len([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])


def ocr_frames(frames_dir: str) -> str:
    chunks = []
    for f in sorted(os.listdir(frames_dir)):
        if not f.endswith(".jpg"):
            continue
        out = subprocess.run(
            ["tesseract", os.path.join(frames_dir, f), "stdout", "--psm", "11"],
            capture_output=True, text=True,
        )
        chunks.append(out.stdout)
    return "\n".join(chunks)


def rank_words(ocr_text: str, min_count: int) -> list[tuple[str, int]]:
    tokens = re.findall(r"[A-Za-z][A-Za-z.+#]*[A-Za-z]", ocr_text)
    counts = Counter(t.lower() for t in tokens if len(t) >= 3)
    return [(w, n) for w, n in counts.most_common() if n >= min_count]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--min-count", type=int, default=2)
    args = ap.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: file not found: {args.video}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as frames_dir:
        n = extract_frames(args.video, frames_dir)
        print(f"Extracted {n} frames. Running OCR...")
        ocr_text = ocr_frames(frames_dir)

    ranked = rank_words(ocr_text, args.min_count)
    lines = [f"{n}\t{w}" for w, n in ranked]
    body = "\n".join(lines)

    if args.out:
        Path(args.out).write_text(body + "\n")
        print(f"Wrote {len(ranked)} candidates to {args.out}")
    print("\n# Top OCR candidate terms (count<TAB>word) — curate into keyterms.txt:")
    print("\n".join(lines[:150]))


if __name__ == "__main__":
    main()
