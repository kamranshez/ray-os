#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""
Prep Ray's profile picture: square-center-crop, downscale, mask to circle, write transparent PNG.
Run once; result lands at ../assets/profile.png and is reused across renders.

Usage:
  uv run scripts/prep_profile.py [--source PATH] [--size 512]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

DEFAULT_SOURCE = Path(
    "/Users/ray/Library/Mobile Documents/com~apple~CloudDocs/Profile Pictures/6 Large.jpeg"
)


def make_circular(src: Path, dst: Path, size: int = 512) -> None:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)

    # Antialiased circular mask: render at 4x then downscale.
    scale = 4
    mask_big = Image.new("L", (size * scale, size * scale), 0)
    ImageDraw.Draw(mask_big).ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask_big.resize((size, size), Image.LANCZOS)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG")
    print(f"wrote {dst} ({size}x{size})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument(
        "--dest",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "assets" / "profile.png",
    )
    args = ap.parse_args()
    if not args.source.exists():
        raise SystemExit(f"source not found: {args.source}")
    make_circular(args.source, args.dest, args.size)


if __name__ == "__main__":
    main()
