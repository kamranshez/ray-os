---
name: excalidraw-bundle
description: Bundle a set of section images into a single .excalidraw file (panels laid out left-to-right with section titles) and save it to ~/Downloads, ready to drag into excalidraw.com or the Obsidian Excalidraw plugin.
---

# excalidraw-bundle

Pair with [[excalidraw-codex]] / [[excalidraw-gemini]]: those skills *generate* per-section images, this one *combines* them into a single Excalidraw canvas you can pan through like a slide deck.

The output is always saved into `~/Downloads/` because that's where the user uploads it from into excalidraw.com.

## When to use

- The user has a markdown file (or directory of subfolders of images) and wants one Excalidraw canvas containing all the section images laid out in order.
- The user says things like "bundle these into an excalidraw", "make a slideshow", "give me one file I can import into Excalidraw".

## Two input modes

### Markdown mode (preferred)

Parses `![[path/to/img.png]]` and `![](path/to/img.png)` embeds **in document order**. Section title above each image is the most recent `## ` heading. Image paths are resolved relative to the markdown file's directory. Duplicate embeds are skipped.

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

- `--width` (default 1200) — image canvas width per panel
- `--height` (default 675) — image canvas height per panel (16:9-ish)
- `--gap` (default 200) — horizontal gap between panels

Defaults match the aspect ratio Codex's `image_gen` tool produces (~1672×941 → 1200×675 preserves the shape).

## File format

Excalidraw v2 JSON. Each PNG is base64-encoded into the document's `files` map under a sha384 fileId. Each panel is two elements: a 36pt Excalifont title above a positioned image. Files end up large (1-3 MB per embedded image is normal); don't be surprised by a 10-20 MB `.excalidraw`.

## After bundling

Tell the user the file is in Downloads and they can:
- Drag it into [excalidraw.com](https://excalidraw.com)
- Or import via the Obsidian Excalidraw plugin

Use `Shift+1` inside Excalidraw to fit-all and see every panel at once.
