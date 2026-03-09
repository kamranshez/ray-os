#!/usr/bin/env python3
"""
Image cleanup tool for Obsidian vaults.

Finds unreferenced images, deletes them, flattens subfolder structures,
renames files based on their section/subfolder name, and updates markdown references.
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path


IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}
IMAGE_REF_PATTERN = re.compile(
    r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp))\]\]', re.IGNORECASE
)


def find_md_files(folder):
    return list(Path(folder).rglob("*.md"))


def find_image_files(folder):
    images = []
    images_dir = Path(folder) / "images"
    if images_dir.exists():
        for f in images_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
                images.append(f)
    return images


def extract_image_refs(md_files):
    """Extract all ![[...]] image references from markdown files.
    Returns dict: {ref_string: [(md_file, line_num)]}
    Skips references inside fenced code blocks (``` or ~~~).
    """
    refs = {}
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            in_code_block = False
            for line_num, line in enumerate(f, 1):
                stripped = line.strip()
                if stripped.startswith('```') or stripped.startswith('~~~'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                for match in IMAGE_REF_PATTERN.finditer(line):
                    ref = match.group(1)
                    if ref not in refs:
                        refs[ref] = []
                    refs[ref].append((md_file, line_num))
    return refs


def resolve_ref_to_file(ref, folder, image_files):
    """Resolve an Obsidian ![[ref]] to an actual file path."""
    # Try as relative path from folder
    candidate = Path(folder) / ref
    if candidate.exists():
        return candidate
    # Try filename-only match (Obsidian resolves by filename alone)
    ref_name = Path(ref).name
    for img in image_files:
        if img.name == ref_name:
            return img
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Clean up unreferenced images in Obsidian vault folders'
    )
    parser.add_argument('folder', help='Target folder to clean up')
    parser.add_argument(
        '--execute', action='store_true',
        help='Actually perform changes (default: dry run)'
    )
    parser.add_argument(
        '--no-flatten', action='store_true',
        help='Skip flattening/renaming — only delete unreferenced images'
    )
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.exists():
        print(f"Error: Folder {folder} does not exist")
        sys.exit(1)

    # Discover files
    md_files = find_md_files(folder)
    image_files = find_image_files(folder)

    if not md_files:
        print(f"No markdown files found in {folder}")
        sys.exit(0)

    if not image_files:
        print(f"No image files found in {folder}/images/")
        sys.exit(0)

    print(f"Found {len(md_files)} markdown file(s)")
    print(f"Found {len(image_files)} image file(s)")
    print()

    # Extract references from markdown
    refs = extract_image_refs(md_files)
    print(f"Found {len(refs)} unique image reference(s) in markdown")
    print()

    # Resolve each reference to an actual file
    referenced_files = set()
    ref_to_file = {}
    unresolved_refs = []

    for ref in refs:
        resolved = resolve_ref_to_file(ref, folder, image_files)
        if resolved:
            referenced_files.add(resolved.resolve())
            ref_to_file[ref] = resolved
        else:
            unresolved_refs.append(ref)

    # Find unreferenced images
    unreferenced = [
        img for img in image_files if img.resolve() not in referenced_files
    ]

    # --- Report ---

    if unresolved_refs:
        print("BROKEN REFERENCES (image file missing):")
        for ref in unresolved_refs:
            locations = refs[ref]
            for md_file, line_num in locations:
                rel_md = md_file.relative_to(folder)
                print(f"  ! {ref}  (in {rel_md}:{line_num})")
        print()

    if unreferenced:
        total_size = 0
        print(f"UNREFERENCED IMAGES ({len(unreferenced)} to delete):")
        for img in sorted(unreferenced):
            size = img.stat().st_size
            total_size += size
            rel = img.relative_to(folder)
            print(f"  - {rel} ({size / 1024:.1f} KB)")
        print(f"  Total: {total_size / 1024 / 1024:.2f} MB")
        print()
    else:
        print("No unreferenced images found.")
        print()

    # --- Flatten + rename plan ---

    rename_plan = {}   # {old_path: new_path}
    ref_updates = {}   # {old_ref: new_ref}

    if not args.no_flatten and ref_to_file:
        images_dir = folder / "images"
        used_names = set()

        for ref, file_path in sorted(ref_to_file.items()):
            rel = file_path.relative_to(folder)
            parts = rel.parts  # e.g., ('images', 'two-room-office', 'excalidraw_6.png')

            if len(parts) == 3 and parts[0] == 'images':
                # Has subfolder — rename using subfolder name
                subfolder_name = parts[1]
                extension = file_path.suffix
                new_name = f"{subfolder_name}{extension}"

                # Handle duplicates (multiple kept images from same subfolder)
                if new_name in used_names:
                    counter = 2
                    while f"{subfolder_name}-{counter}{extension}" in used_names:
                        counter += 1
                    new_name = f"{subfolder_name}-{counter}{extension}"

                used_names.add(new_name)
                new_path = images_dir / new_name

                if file_path.resolve() != new_path.resolve():
                    rename_plan[file_path] = new_path
                    new_ref = f"images/{new_name}"
                    ref_updates[ref] = new_ref

            elif len(parts) == 2 and parts[0] == 'images':
                # Already flat — keep as-is
                used_names.add(parts[1])

        if rename_plan:
            print(f"FLATTEN + RENAME PLAN ({len(rename_plan)} files):")
            for old, new in sorted(rename_plan.items()):
                old_rel = old.relative_to(folder)
                new_rel = new.relative_to(folder)
                print(f"  {old_rel}  →  {new_rel}")
            print()

    # --- Dry run gate ---

    if not args.execute:
        print("DRY RUN — no changes made. Pass --execute to apply.")
        return

    # --- Execute ---

    # 1. Delete unreferenced images
    deleted_count = 0
    for img in unreferenced:
        img.unlink()
        deleted_count += 1
    if deleted_count:
        print(f"Deleted {deleted_count} unreferenced image(s)")

    # 2. Rename/flatten referenced images
    if rename_plan:
        for old_path, new_path in rename_plan.items():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(new_path))
        print(f"Renamed/moved {len(rename_plan)} image(s)")

    # 3. Update markdown references
    if ref_updates:
        updated_files = 0
        for md_file in md_files:
            content = md_file.read_text(encoding='utf-8')
            modified = False
            for old_ref, new_ref in ref_updates.items():
                old_embed = f"![[{old_ref}]]"
                new_embed = f"![[{new_ref}]]"
                if old_embed in content:
                    content = content.replace(old_embed, new_embed)
                    modified = True
            if modified:
                md_file.write_text(content, encoding='utf-8')
                updated_files += 1
        print(f"Updated references in {updated_files} markdown file(s)")

    # 4. Remove broken references from markdown
    if unresolved_refs:
        for md_file in md_files:
            content = md_file.read_text(encoding='utf-8')
            modified = False
            for ref in unresolved_refs:
                old_embed = f"![[{ref}]]"
                if old_embed in content:
                    # Remove the embed and any trailing newline
                    content = content.replace(old_embed + "\n", "")
                    content = content.replace(old_embed, "")
                    modified = True
            if modified:
                md_file.write_text(content, encoding='utf-8')
        print(f"Removed {len(unresolved_refs)} broken reference(s) from markdown")

    # 5. Clean up empty subdirectories
    images_dir = folder / "images"
    if images_dir.exists():
        for dirpath in sorted(images_dir.rglob("*"), reverse=True):
            if dirpath.is_dir() and not any(dirpath.iterdir()):
                dirpath.rmdir()
                print(f"Removed empty directory: {dirpath.relative_to(folder)}")

    print("\nDone!")


if __name__ == '__main__':
    main()
