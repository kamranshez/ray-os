#!/usr/bin/env python3
"""Bundle a set of PNG images into a single .excalidraw file.

Two input modes:

1. Markdown mode (--md <file.md>):
   Parses `![[path/to/img.png]]` and `![](path/to/img.png)` embeds in order.
   Section title above each image comes from the most recent `## ` heading.
   Image paths resolved relative to the markdown file's directory.

2. Directory mode (--dir <root>):
   Walks each immediate subdirectory of <root> in alphabetical order. From
   each subdir picks the first PNG (by name). Subdir name becomes the title.

Output always lands in ~/Downloads/<stem>.excalidraw where <stem> is the
markdown filename or the root dir name. Override with -o.

Each image is embedded as base64 in the file's `files` map; the canvas
has one image element per input plus a centered title above it. Panels
flow left-to-right with a fixed gap so the user can pan/scroll through
them as a slideshow inside Excalidraw.
"""

import argparse
import base64
import hashlib
import json
import re
import secrets
import string
import sys
from pathlib import Path

ALPHABET = string.ascii_letters + string.digits + "_"

WIKILINK_RE = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


def rand_id(n=21):
    return "".join(secrets.choice(ALPHABET) for _ in range(n))


def title_case(slug):
    return slug.replace("-", " ").replace("_", " ").strip().title()


def collect_from_markdown(md_path: Path):
    """Return [(title, img_path), ...] in document order, one entry per embed."""
    out = []
    current_title = md_path.stem
    md_dir = md_path.parent
    seen = set()

    for raw in md_path.read_text().splitlines():
        h = HEADING_RE.match(raw)
        if h:
            current_title = h.group(1).strip()
            continue
        for m in WIKILINK_RE.finditer(raw):
            rel = m.group(1).strip()
            resolved = (md_dir / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
            if resolved in seen:
                continue
            seen.add(resolved)
            out.append((current_title, resolved))
        for m in MD_IMG_RE.finditer(raw):
            rel = m.group(1).strip()
            resolved = (md_dir / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
            if resolved in seen:
                continue
            seen.add(resolved)
            out.append((current_title, resolved))
    return out


def collect_from_dir(root: Path):
    """Return [(title, img_path), ...] from each immediate subdir."""
    out = []
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        pngs = sorted(sub.glob("*.png"))
        if not pngs:
            continue
        out.append((title_case(sub.name), pngs[0]))
    return out


def build_doc(panels, img_w=1200, img_h=675, gap_x=200, title_height=50, title_gap=80):
    elements = []
    files = {}
    for i, (title, png_path) in enumerate(panels):
        png_path = Path(png_path)
        if not png_path.exists():
            print(f"warn: missing {png_path}, skipping", file=sys.stderr)
            continue
        raw = png_path.read_bytes()
        file_id = hashlib.sha384(raw).hexdigest()
        if file_id not in files:
            files[file_id] = {
                "mimeType": "image/png",
                "id": file_id,
                "dataURL": "data:image/png;base64," + base64.b64encode(raw).decode("ascii"),
                "created": 1775543163208,
            }

        x = i * (img_w + gap_x)
        y = title_height + title_gap

        elements.append({
            "id": rand_id(),
            "type": "text",
            "x": x,
            "y": 0,
            "width": img_w,
            "height": title_height,
            "angle": 0,
            "strokeColor": "#1e1e1e",
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": f"a{2 * i}",
            "roundness": None,
            "seed": secrets.randbelow(2**31),
            "version": 1,
            "versionNonce": secrets.randbelow(2**31),
            "isDeleted": False,
            "boundElements": [],
            "updated": 1775543163208,
            "link": None,
            "locked": False,
            "text": title,
            "fontSize": 36,
            "fontFamily": 5,
            "textAlign": "center",
            "verticalAlign": "top",
            "containerId": None,
            "originalText": title,
            "autoResize": True,
            "lineHeight": 1.25,
        })
        elements.append({
            "id": rand_id(),
            "type": "image",
            "x": x,
            "y": y,
            "width": img_w,
            "height": img_h,
            "angle": 0,
            "strokeColor": "transparent",
            "backgroundColor": "#ffffff",
            "fillStyle": "solid",
            "strokeWidth": 4,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": f"a{2 * i + 1}",
            "roundness": None,
            "seed": secrets.randbelow(2**31),
            "version": 1,
            "versionNonce": secrets.randbelow(2**31),
            "isDeleted": False,
            "boundElements": [],
            "updated": 1775543163208,
            "link": None,
            "locked": False,
            "status": "saved",
            "fileId": file_id,
            "scale": [1, 1],
            "crop": None,
        })

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://app.excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "gridStep": 5,
            "gridModeEnabled": False,
            "viewBackgroundColor": "#ffffff",
            "lockedMultiSelections": {},
        },
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--md", type=Path, help="Markdown file: parse embeds in order")
    src.add_argument("--dir", type=Path, help="Directory: one PNG per immediate subdir")
    ap.add_argument("-o", "--output", type=Path, help="Output .excalidraw path (default: ~/Downloads/<stem>.excalidraw)")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=675)
    ap.add_argument("--gap", type=int, default=200)
    args = ap.parse_args()

    if args.md:
        panels = collect_from_markdown(args.md.resolve())
        stem = args.md.stem
    else:
        panels = collect_from_dir(args.dir.resolve())
        stem = args.dir.name

    if not panels:
        print("error: no images collected", file=sys.stderr)
        sys.exit(1)

    out = args.output or (Path.home() / "Downloads" / f"{stem}.excalidraw")
    out.parent.mkdir(parents=True, exist_ok=True)

    doc = build_doc(panels, img_w=args.width, img_h=args.height, gap_x=args.gap)
    out.write_text(json.dumps(doc))
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"wrote {out} ({size_mb:.1f} MB, {len(panels)} panels)")


if __name__ == "__main__":
    main()
