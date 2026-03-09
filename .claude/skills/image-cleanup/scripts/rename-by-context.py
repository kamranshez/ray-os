#!/usr/bin/env python3
"""
rename-by-context.py — rename generic image filenames using surrounding context.

Strategy:
1. For images with generic names (excalidraw_N.png, img_N.png, timestamp filenames):
   a. If the image is in a descriptive subfolder (not just "images"), use the subfolder name.
   b. Otherwise, use the nearest heading or bold text above the image embed in markdown.
2. Already-descriptive names are left alone.
3. Collision-safe: appends -2, -3, etc. if destination exists.

Usage:
    python3 rename-by-context.py "/path/to/folder"           # dry run
    python3 rename-by-context.py "/path/to/folder" --execute # apply changes
"""

import os
import re
import sys
import shutil
from pathlib import Path
from collections import defaultdict

GENERIC_PATTERN = re.compile(
    r'^(excalidraw_\d+|img_\d+|image_\d+|screenshot_\d+|'
    r'excalidraw_\d+\s+\d{2}-\d{2}-\d{2}-\d+)'
    r'\.(png|jpg|jpeg|gif|webp|svg)$',
    re.IGNORECASE
)

EMBED_PATTERN = re.compile(r'!\[\[([^\]]+)\]\]')
HEADING_PATTERN = re.compile(r'^#{1,6}\s+(.+)$')
BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')
NUMBERED_TIP_PATTERN = re.compile(r'^\d+\.\s+\*\*(.+?)\*\*')


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text[:60]  # cap length


def is_generic_name(filename):
    return bool(GENERIC_PATTERN.match(filename))


def is_descriptive_folder(folder_name):
    """Returns True if the folder name encodes meaningful context."""
    generic_folders = {'images', 'img', 'assets', 'media', 'files'}
    return folder_name.lower() not in generic_folders and not re.match(r'^\d+$', folder_name)


def get_context_from_markdown(md_path, image_ref):
    """Find the nearest heading or tip text above the image embed in the markdown."""
    try:
        lines = Path(md_path).read_text(encoding='utf-8').splitlines()
    except Exception:
        return None

    # Find the line with this image reference
    target_line = None
    for i, line in enumerate(lines):
        if image_ref in line:
            target_line = i
            break

    if target_line is None:
        return None

    # Walk backwards from the image line looking for context
    for i in range(target_line - 1, max(target_line - 10, -1), -1):
        line = lines[i].strip()
        if not line:
            continue

        # Numbered tip: "1. **The only limit is your imagination**"
        m = NUMBERED_TIP_PATTERN.match(line)
        if m:
            return slugify(m.group(1))

        # Heading: "## Setup & Environment"
        m = HEADING_PATTERN.match(line)
        if m:
            return slugify(m.group(1))

        # Bold text
        m = BOLD_PATTERN.search(line)
        if m:
            return slugify(m.group(1))

    return None


def find_md_files(root):
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs and skill dirs
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(Path(dirpath) / f)
    return md_files


def collect_renames(root):
    """
    Returns list of (old_abs_path, new_abs_path, md_file, old_ref, new_ref)
    """
    root = Path(root)
    md_files = find_md_files(root)

    renames = []
    # Track destination names to avoid collisions
    dest_counts = defaultdict(int)

    for md_path in sorted(md_files):
        try:
            content = md_path.read_text(encoding='utf-8')
        except Exception:
            continue

        for m in EMBED_PATTERN.finditer(content):
            ref = m.group(1)
            # Strip any display text after |
            ref = ref.split('|')[0].strip()

            # Resolve relative to the markdown file's directory first, then root
            img_path = md_path.parent / ref
            if not img_path.exists():
                img_path = root / ref
            if not img_path.exists():
                continue

            filename = img_path.name
            if not is_generic_name(filename):
                continue

            ext = img_path.suffix.lower()
            parent_folder = img_path.parent.name

            # Strategy A: use descriptive subfolder name
            if is_descriptive_folder(parent_folder):
                base_slug = slugify(parent_folder)
            else:
                # Strategy B: use surrounding markdown context
                context = get_context_from_markdown(md_path, ref)
                if context:
                    base_slug = context
                else:
                    continue  # can't determine context, skip

            # Collision avoidance
            dest_key = str(img_path.parent / (base_slug + ext))
            dest_counts[dest_key] += 1
            count = dest_counts[dest_key]
            if count == 1:
                new_name = base_slug + ext
            else:
                new_name = f"{base_slug}-{count}{ext}"

            new_abs = img_path.parent / new_name
            if new_abs == img_path:
                continue  # already named correctly

            new_ref = str(Path(ref).parent / new_name)

            renames.append({
                'old_path': img_path,
                'new_path': new_abs,
                'md_file': md_path,
                'old_ref': ref,
                'new_ref': new_ref,
            })

    return renames


def print_plan(renames):
    if not renames:
        print("Nothing to rename — all images already have descriptive names.")
        return

    by_note = defaultdict(list)
    for r in renames:
        by_note[r['md_file'].name].append(r)

    total_size = 0
    for note, items in sorted(by_note.items()):
        print(f"\n  {note}:")
        for r in items:
            size = r['old_path'].stat().st_size if r['old_path'].exists() else 0
            total_size += size
            print(f"    {r['old_ref']}")
            print(f"      → {r['new_ref']}")

    print(f"\nTotal: {len(renames)} rename(s) across {len(by_note)} note(s)")


def apply_renames(renames, root):
    root = Path(root)
    # Group all renames by md file so we can do one pass per file
    by_md = defaultdict(list)
    for r in renames:
        by_md[r['md_file']].append(r)

    renamed_files = set()
    errors = []

    # Rename files on disk first
    for r in renames:
        old = r['old_path']
        new = r['new_path']
        if old in renamed_files:
            continue
        if old == new:
            continue
        try:
            if new.exists() and new != old:
                print(f"  SKIP (dest exists): {old.name} → {new.name}")
                continue
            old.rename(new)
            renamed_files.add(old)
            print(f"  Renamed: {old.name} → {new.name}")
        except Exception as e:
            errors.append(f"  ERROR renaming {old}: {e}")

    # Update markdown references
    for md_path, items in by_md.items():
        try:
            content = md_path.read_text(encoding='utf-8')
            for r in items:
                if r['old_path'] not in renamed_files:
                    continue
                content = content.replace(
                    f"![[{r['old_ref']}]]",
                    f"![[{r['new_ref']}]]"
                )
            md_path.write_text(content, encoding='utf-8')
            print(f"  Updated refs in: {md_path.name}")
        except Exception as e:
            errors.append(f"  ERROR updating {md_path}: {e}")

    for e in errors:
        print(e)

    print(f"\nDone: {len(renamed_files)} file(s) renamed.")


def main():
    if len(sys.argv) < 2:
        print("Usage: rename-by-context.py <folder> [--execute]")
        sys.exit(1)

    root = sys.argv[1]
    execute = '--execute' in sys.argv

    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Scanning: {root}")
    renames = collect_renames(root)

    if execute:
        print(f"\nEXECUTING {len(renames)} rename(s)...\n")
        apply_renames(renames, root)
    else:
        print(f"\nRENAME PLAN ({len(renames)} image(s)):")
        print_plan(renames)
        print("\nDRY RUN — no changes made. Pass --execute to apply.")


if __name__ == '__main__':
    main()
