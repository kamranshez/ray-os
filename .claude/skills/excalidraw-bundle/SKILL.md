---
name: excalidraw-bundle
description: Bundle a set of section images into a single .excalidraw file laid out as a grid — one column per section in document order, the section's variations stacked vertically — and save it to ~/Downloads, ready to drag into excalidraw.com or the Obsidian Excalidraw plugin.
---

# excalidraw-bundle

Pair with [[excalidraw-codex]] / [[excalidraw-gemini]]: those skills *generate* per-section images (typically N variations per section), this one *combines* them into a single Excalidraw canvas you can read like a storyboard.

The output is always saved into `~/Downloads/` because that's where the user uploads it from into excalidraw.com.

## Layout — grid

- **Columns = sections in document/video order** (left → right). The reader scans left to right to walk through the piece.
- **Rows = the variations of that section, stacked vertically** (`<slug>-1.png` at top, `-2`, `-3`, … below). Pick the best variation by scanning down a column.
- Variations are grouped automatically by stripping the trailing `-<N>` from each image's filename, so every `loopy-intro-loop-stack-1..5.png` lands in one column.
- **No title text** is drawn — images only. (Excalidraw dark theme inverts text/strokes oddly; the images carry their own labels.)

## When to use

- The user has a markdown file (or directory of subfolders of images) and wants one Excalidraw canvas containing all the section images laid out in order.
- The user says things like "bundle these into an excalidraw", "make a slideshow", "give me one file I can import into Excalidraw".

## Two input modes

### Markdown mode (preferred)

Parses `![[path/to/img.png]]` and `![](path/to/img.png)` embeds **in document order**. The most recent `## ` heading names each section (used only for column grouping, not drawn). Duplicate embeds are skipped.

**Image path resolution:** absolute paths are used as-is; otherwise the path is tried relative to the markdown file's directory, and if not found, falls back to the **vault-root `images/` folder by filename** (`/Users/ray/Desktop/ray-os/images`). This matches the vault convention where embeds are filename-only `![[slug-1.png]]` and all images live in one flat folder.

```bash
python3 .claude/skills/excalidraw-bundle/scripts/bundle.py \
  --md /abs/path/to/file.md
```

### Directory mode

Walks each immediate subdirectory of `<root>` alphabetically and picks the **first PNG** in each (sorted by filename). The subdirectory name becomes the panel title (kebab-case → Title Case).

```bash
python3 .claude/skills/excalidraw-bundle/scripts/bundle.py \
  --dir /abs/path/to/images-root
```

This is the right mode when image directories follow the [[excalidraw-codex]] convention of `images/<section-slug>/excalidraw_1.png` and you want the first variation from each.

## Output location

Defaults to `~/Downloads/<stem>.excalidraw` (stem = markdown filename or root dir name). Override with `-o`:

```bash
python3 .claude/skills/excalidraw-bundle/scripts/bundle.py \
  --md notes/talk.md \
  -o ~/Desktop/talk.excalidraw
```

Always tell the user where the file landed so they can drag it into Excalidraw.

## Layout knobs

- `--width` (default 1200) — image width per cell
- `--height` (default 675) — image height per cell (16:9-ish)
- `--gap` (default 200) — horizontal gap between columns (vertical row gap is fixed at 120)

Defaults match the aspect ratio Codex's `image_gen` tool produces (~1672×941 → 1200×675 preserves the shape).

## Dark background — CRITICAL

Set `viewBackgroundColor` to **`#ffffff`** (white) in the file, NOT a dark hex. Excalidraw's **dark app theme inverts the canvas for display**, so a white scene background renders dark on the user's screen, while a near-black `#0E1116` gets inverted to look *white*. Matching the user's reference (a plain white-background scene that appears dark in their dark-themed app) is the correct behavior. **Do not** paint a dark background rectangle — the user rejected that; rely on white `viewBackgroundColor` + their app theme.

## File format

Excalidraw v2 JSON. Each PNG is base64-encoded into the document's `files` map under a sha384 fileId. Each cell is a single positioned image element (no title text). Images use `backgroundColor: transparent`. Files end up large (1-3 MB per embedded image is normal); a full video deck of 10-25 images is routinely 20-50 MB.

## After bundling

Tell the user the file is in Downloads and they can:
- Drag it into [excalidraw.com](https://excalidraw.com)
- Or import via the Obsidian Excalidraw plugin

Use `Shift+1` inside Excalidraw to fit-all and see every panel at once.
