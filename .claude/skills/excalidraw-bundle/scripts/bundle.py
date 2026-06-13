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

# Vault-root flat images folder. Filename-only embeds (`![[name.png]]`) resolve
# here when they don't exist relative to the markdown file's directory.
VAULT_IMAGES = Path("/Users/ray/Desktop/ray-os/images")


def resolve_embed(rel: str, md_dir: Path) -> Path:
    """Resolve an embed path: absolute as-is, else relative to the md dir,
    else fall back to the vault-root images/ folder by basename."""
    if Path(rel).is_absolute():
        return Path(rel)
    local = (md_dir / rel).resolve()
    if local.exists():
        return local
    vault = (VAULT_IMAGES / Path(rel).name).resolve()
    if vault.exists():
        return vault
    return local


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
            resolved = resolve_embed(rel, md_dir)
            if resolved in seen:
                continue
            seen.add(resolved)
            out.append((current_title, resolved))
        for m in MD_IMG_RE.finditer(raw):
            rel = m.group(1).strip()
            resolved = resolve_embed(rel, md_dir)
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


def group_into_columns(panels):
    """Group panels into columns by placeholder base slug.

    Each placeholder produces several variation PNGs named `<base>-<N>.png`.
    Columns are ordered by first appearance in the document; within a column
    variations are ordered by their trailing number. Returns a list of
    (title, [path, path, ...]) in column (video) order.
    """
    cols = []
    index = {}
    for title, path in panels:
        base = re.sub(r"-\d+$", "", Path(path).stem)
        key = (title, base)
        if key not in index:
            index[key] = len(cols)
            cols.append((title, base, []))
        cols[index[key]][2].append(path)

    def vnum(p):
        m = re.search(r"-(\d+)$", Path(p).stem)
        return int(m.group(1)) if m else 0

    return [(title, sorted(paths, key=vnum)) for title, base, paths in cols]


def build_doc(panels, img_w=1200, img_h=675, gap_x=200, gap_y=120, title_height=50, title_gap=80):
    elements = []
    files = {}
    columns = group_into_columns(panels)
    elem_i = 0

    for col, (title, paths) in enumerate(columns):
        x = col * (img_w + gap_x)
        top = 0

        for row, png_path in enumerate(paths):
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

            y = top + row * (img_h + gap_y)
            elements.append({
                "id": rand_id(),
                "type": "image",
                "x": x,
                "y": y,
                "width": img_w,
                "height": img_h,
                "angle": 0,
                "strokeColor": "transparent",
                "backgroundColor": "transparent",
                "fillStyle": "solid",
                "strokeWidth": 4,
                "strokeStyle": "solid",
                "roughness": 1,
                "opacity": 100,
                "groupIds": [],
                "frameId": None,
                "index": f"a{elem_i}",
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
            elem_i += 1

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
