---
name: image-cleanup
description: Clean up unreferenced images in Obsidian vault folders. Deletes unused images, renames excalidraw files with descriptive names based on image content (using vision), and moves everything to vault root images/ folder. Use after picking favorites from excalidraw-gen batches. Triggers on "clean up images", "delete unused images", "tidy up images", "image cleanup", or "/image-cleanup".
---

## What This Skill Does

After excalidraw-gen creates 10 images per section and the user picks their favorite(s), this skill:

1. **Deletes unreferenced images** — scans `.md` files for `![[...]]` embeds, cross-references against actual image files, removes anything not referenced
2. **Renames images descriptively** — Claude reads each remaining image with vision and gives it a descriptive filename based on what the image actually shows
3. **Moves to vault root** — all images go to `images/` at the vault root (`/Users/ray/Desktop/ray-os/images/`), organized as `images/{note-slug}/descriptive-name.png`
4. **Updates markdown references** — rewrites all `![[...]]` embeds to match the new paths
5. **Cleans up** — removes empty directories and old local `images/` folders

### Before → After

```
Before (in socials/youtube/videos/):
images/two-room-office/excalidraw_1.png    ← unreferenced
images/two-room-office/excalidraw_2.png    ← unreferenced
images/two-room-office/excalidraw_6.png    ← referenced
images/thin-waist/excalidraw_9.png         ← referenced

After (at vault root):
images/my-video-name/two-room-office-analogy.png
images/my-video-name/thin-waist-architecture.png
```

Markdown updates:
```
![[images/two-room-office/excalidraw_6.png]]  →  ![[images/my-video-name/two-room-office-analogy.png]]
```

---

## Workflow

1. User provides a **target folder** (or you infer it from context). If none provided, ask.
2. Run the **dry run** to find unreferenced images:
   ```bash
   python3 /Users/ray/Desktop/ray-os/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/target/folder" --no-flatten
   ```
3. **Show the user the dry run output** so they can review.
4. After confirmation, **delete unreferenced images**:
   ```bash
   python3 /Users/ray/Desktop/ray-os/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/target/folder" --no-flatten --execute
   ```
5. **Read each remaining image** using the Read tool (vision) and propose descriptive filenames based on what the image actually depicts. Present the rename plan to the user.
6. After confirmation, **rename + move** images to vault root:
   - Create subfolder `images/{note-slug}/` at vault root if it doesn't exist
   - Move and rename each image
   - Update all `![[...]]` references in the markdown files
   - Remove the old local `images/` directory
   - Remove any empty directories left behind

---

## Image Destination Rules

**All images live at the vault root: `/Users/ray/Desktop/ray-os/images/`**

- **Multi-image notes** → `images/{note-slug}/descriptive-name.png`
  - e.g., `images/anthropic-skills-playbook/skill-shifts-distribution.png`
- **Single-image notes** → `images/{note-slug}/descriptive-name.png` (same pattern)
  - e.g., `images/using-cc-in-wsl/claude-code-in-wsl.png`
- **Note slug** = filename → lowercase, non-alphanumeric runs become hyphens
  - `Anthropic Skills Playbook` → `anthropic-skills-playbook`
  - `1M Context Window` → `1m-context-window`

**Never create local `images/` folders** inside project subdirectories. Everything goes to vault root.

---

## Naming Images

**Use vision, not folder names.** Read each image with the Read tool and name it based on what it actually shows:

- Use the image's title/heading if visible (e.g., "How a Skill Shifts the Distribution" → `skill-shifts-distribution.png`)
- Use the core concept if no title (e.g., image showing a before/after comparison of prescriptive vs flexible prompts → `prescriptive-vs-flexible-prompt.png`)
- Keep names concise but descriptive (3-5 words slugified)
- Use hyphens, all lowercase

**Do NOT** use the excalidraw number, the subfolder name alone, or generic names.

---

## Important Notes

- **Always dry run first.** Never delete images without showing the user what will happen.
- **Always show rename plan.** Present the proposed names before executing.
- **Vault root is sacred.** `images/` at `/Users/ray/Desktop/ray-os/images/` is the single source of truth for all images.
- **Markdown references use vault-root paths.** All refs should look like `` — Obsidian resolves these from the vault root.
- **No dependencies.** The cleanup.py script is pure Python 3 stdlib. Renaming and moving is done by Claude directly.

---

## Helper Scripts

### cleanup.py — Delete unreferenced images

Always use with `--no-flatten`. Only use this for deleting unreferenced images.

```bash
# Dry run
python3 /Users/ray/Desktop/ray-os/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/folder" --no-flatten

# Execute
python3 /Users/ray/Desktop/ray-os/.claude/skills/image-cleanup/scripts/cleanup.py "/path/to/folder" --no-flatten --execute
```

### rename-by-context.py — Fallback rename tool

Only use if you cannot read images with vision. Renames excalidraw files using subfolder names or surrounding markdown context.

```bash
python3 /Users/ray/Desktop/ray-os/.claude/skills/image-cleanup/scripts/rename-by-context.py "/path/to/folder"
```
