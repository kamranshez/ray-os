#!/usr/bin/env python3
"""
Overlay a YouTube-style play button on a thumbnail image.

Usage:
    python add-play-button.py <input_image> [output_image]

If output_image is omitted, saves to <input_name>-play.<ext> in the same directory.
"""

import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw


def add_play_button(input_path: str, output_path: str | None = None) -> str:
    """Add a YouTube-style play button overlay to a thumbnail image."""
    input_path = Path(input_path)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}-play{input_path.suffix}"
    else:
        output_path = Path(output_path)

    img = Image.open(input_path).convert("RGBA")
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
        gradient_draw.line([(0, h - gradient_height + y), (w, h - gradient_height + y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, gradient)

    # --- Play button circle ---
    # Size the button relative to image dimensions (roughly 15% of the shorter side)
    button_radius = int(min(w, h) * 0.075)
    cx, cy = w // 2, h // 2

    # Semi-transparent dark circle
    draw.ellipse(
        [cx - button_radius, cy - button_radius, cx + button_radius, cy + button_radius],
        fill=(0, 0, 0, 180),
    )

    # White triangle (play icon) - offset slightly right for optical centering
    triangle_size = button_radius * 0.55
    offset_x = triangle_size * 0.15  # nudge right so it looks centred
    triangle = [
        (cx - triangle_size * 0.5 + offset_x, cy - triangle_size * 0.85),
        (cx - triangle_size * 0.5 + offset_x, cy + triangle_size * 0.85),
        (cx + triangle_size * 0.85 + offset_x, cy),
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 240))

    # Composite the play button overlay
    result = Image.alpha_composite(img, overlay)

    # Convert back to RGB for JPEG output
    if output_path.suffix.lower() in (".jpg", ".jpeg"):
        result = result.convert("RGB")

    result.save(str(output_path), quality=95)
    print(f"Saved: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add-play-button.py <input_image> [output_image]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    add_play_button(input_file, output_file)
