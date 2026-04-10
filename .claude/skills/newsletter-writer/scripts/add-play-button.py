#!/usr/bin/env python3
"""
Overlay a YouTube-style play button on a thumbnail image and resize it for email.

Usage:
    python add-play-button.py <input_image> [output_image] [--max-width N] [--quality N]

Defaults:
    --max-width 1280  (resizes so the long edge is at most 1280px, preserving aspect ratio)
    --quality 80      (JPEG quality, ignored for PNG output)

If output_image is omitted, saves to <input_name>-play.<ext> in the same directory.

The defaults produce ~100KB JPEGs at 1280x720 from a 1920x1080 source, which is
a good fit for email clients. Override only if you need a specific size.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw


def add_play_button(
    input_path: str,
    output_path: str | None = None,
    max_width: int = 1280,
    quality: int = 80,
) -> str:
    """Add a YouTube-style play button overlay to a thumbnail image and resize it."""
    input_path = Path(input_path)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}-play{input_path.suffix}"
    else:
        output_path = Path(output_path)

    img = Image.open(input_path).convert("RGBA")

    # Resize BEFORE drawing the play button so the button stays sharp
    # and proportional to the final image.
    w, h = img.size
    if max_width and w > max_width:
        new_w = max_width
        new_h = int(h * (max_width / w))
        img = img.resize((new_w, new_h), Image.LANCZOS)
        w, h = img.size

    # Create overlay for the play button
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # --- Subtle dark gradient at bottom (like YouTube hover state) ---
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    gradient_height = int(h * 0.35)
    for y in range(gradient_height):
        progress = y / gradient_height
        alpha = int(80 * progress)  # max 80 alpha at the very bottom
        gradient_draw.line(
            [(0, h - gradient_height + y), (w, h - gradient_height + y)],
            fill=(0, 0, 0, alpha),
        )

    img = Image.alpha_composite(img, gradient)

    # --- Play button circle ---
    button_radius = int(min(w, h) * 0.075)
    cx, cy = w // 2, h // 2

    draw.ellipse(
        [cx - button_radius, cy - button_radius, cx + button_radius, cy + button_radius],
        fill=(0, 0, 0, 180),
    )

    # White triangle (play icon), offset slightly right for optical centering
    triangle_size = button_radius * 0.55
    offset_x = triangle_size * 0.15
    triangle = [
        (cx - triangle_size * 0.5 + offset_x, cy - triangle_size * 0.85),
        (cx - triangle_size * 0.5 + offset_x, cy + triangle_size * 0.85),
        (cx + triangle_size * 0.85 + offset_x, cy),
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 240))

    # Composite the play button overlay
    result = Image.alpha_composite(img, overlay)

    # Save: use JPEG quality for jpg/jpeg, leave PNG as-is
    if output_path.suffix.lower() in (".jpg", ".jpeg"):
        result = result.convert("RGB")
        result.save(str(output_path), quality=quality, optimize=True)
    else:
        result.save(str(output_path), optimize=True)

    print(f"Saved: {output_path} ({w}x{h})")
    return str(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", nargs="?", default=None, help="Output image path (optional)")
    parser.add_argument("--max-width", type=int, default=1280, help="Max width in pixels (default 1280)")
    parser.add_argument("--quality", type=int, default=80, help="JPEG quality 1-100 (default 80)")
    args = parser.parse_args()

    add_play_button(args.input, args.output, max_width=args.max_width, quality=args.quality)
