---
name: image-cleanup
description: Clean up unreferenced images in Obsidian vault folders. Deletes unused images, flattens subfolder structures, renames files by section name, and updates markdown references. Also sorts images into per-note subfolders (images/{note-slug}/{name}.png). Use when the user wants to clean up images after picking favorites from excalidraw-gen batches, sort images by note, or whenever they want to tidy up image references in a folder. Triggers on "clean up images", "delete unused images", "flatten images", "tidy up images", "sort images by note", "move images into their own folder", or "/image-cleanup".
---

## What This Skill Does

After excalidraw-gen creates 10 images per section and the user picks their favorite(s), this skill:

1. **Finds unreferenced images** — scans all `.md` files in the target folder for `![[...]]` image embeds, cross-references against actual files in `images/`
2. **Deletes unused images** — removes any image file not referenced by any markdown file
3. **Flattens + renames** — moves referenced images from `images/subfolder/excalidraw_N.png` to `images/subfolder-name.png` (flat structure, descriptive names)
4. **Updates markdown references** — rewrites all `![[...]]` embeds to match the new paths
5. **Removes broken references** — strips `![[...]]` embeds that point to non-existent files
6. **Cleans up empty directories** — removes leftover empty subfolders

### Before → After

```
Before:
images/two-room-office/excalidraw_1.png    ← unreferenced
images/two-room-office/excalidraw_2.png    ← unreferenced
images/two-room-office/excalidraw_6.png    ← referenced in markdown
images/thin-waist/excalidraw_3.png         ← unreferenced
images/thin-waist/excalidraw_9.png         ← referenced in markdown

After:
images/two-room-office.png                 ← renamed, flattened
images/thin-waist.png                      ← renamed, flattened
```

Markdown updates accordingly:
```
![[images/two-room-office/excalidraw_6.png]]  →  ![[images/two-room-office.png]]
```

---

## How to Run

The skill always operates on a **target folder** provided by the user.

### Step 1: Dry Run (always do this first)

```bash
python3 /Users/ray/Desktop/Obsidian/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/target/folder"
```

This prints a full report without changing anything:
- Unreferenced images to delete (with sizes)
- Broken references to remove
- Rename/flatten plan

**Show the user the dry run output** so they can review before executing.

### Step 2: Execute (after user confirms)

```bash
python3 /Users/ray/Desktop/Obsidian/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/target/folder" --execute
```

### Optional: Skip flattening

If the user only wants to delete unreferenced images without restructuring:

```bash
python3 /Users/ray/Desktop/Obsidian/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/target/folder" --execute --no-flatten
```

---

## Workflow

1. **Ask the user which mode they want:**
   - **Cleanup** — delete unreferenced images, flatten/rename subfolder images, update markdown refs
   - **Sort by note** — move images from ad-hoc locations into `images/{note-slug}/` subfolders
   - **Both** — run sort-by-note first, then cleanup
2. User provides a target folder (or you infer it from context, e.g., the file they're working on). If none provided, ask.
3. Run the **dry run** for the chosen mode(s) first — always
4. Show the user the report
5. Ask for confirmation before running with `--execute`
6. Report results

---

## Important Notes

- **Always dry run first.** Never run `--execute` without showing the user what will happen.
- **Scope is one folder.** The script processes all `.md` files and `images/` subdirectories within the target folder recursively.
- **Duplicate handling.** If multiple images from the same subfolder are referenced (user kept 2 favorites), they get numbered: `section-name.png`, `section-name-2.png`.
- **Already-flat images are left alone.** Images already at `images/name.png` (no subfolder) aren't touched.
- **No dependencies.** Pure Python 3 stdlib — no pip install needed.

---

## Sort by Note (sort-by-note.py)

Reorganizes images into per-note subfolders: `images/{note-slug}/{image-name}.png`

Use this when:
- Images are in a flat `images/` folder shared across notes
- Images are in ad-hoc locations (e.g., `Boxing the Model In/core-concept.png`)
- You want a clean, predictable structure tied to each note

### Before → After

```
Before:
images/core-concept.png          ← referenced by "Boxing the Model In.md"
images/best-of-5-intro.png       ← referenced by "Best of 5.md"
Boxing the Model In/why.png      ← referenced by "Boxing the Model In.md"

After:
images/boxing-the-model-in/core-concept.png
images/boxing-the-model-in/why.png
images/best-of-5/best-of-5-intro.png
```

### Step 1: Dry Run

```bash
python3 /Users/ray/Desktop/Obsidian/.claude/skills/image-cleanup/scripts/sort-by-note.py "/path/to/folder"
```

### Step 2: Execute

```bash
python3 /Users/ray/Desktop/Obsidian/.claude/skills/image-cleanup/scripts/sort-by-note.py "/path/to/folder" --execute
```

### Slug format

Note filename → slug: lowercase, non-alphanumeric runs become hyphens, trimmed.
- `Boxing the Model In` → `boxing-the-model-in`
- `Best of 5` → `best-of-5`
- `High Level Strategy, Low Level Details` → `high-level-strategy-low-level-details`
