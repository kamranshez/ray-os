#!/usr/bin/env python3
"""Scan collection.media for audio files whose extension doesn't match their
actual content (e.g. MP3 bytes saved as .wav, or M4A/AAC bytes saved as .mp3).

Why this matters: desktop Anki's bundled player decodes by content and never
notices a mismatch, but AnkiMobile/AnkiDroid trust the extension and silently
fail to play the file. This class of bug is invisible until someone studies on
their phone -- which is how a 9-card "saeko" import batch and one kotu.io
sentence-audio download went unnoticed until Ray flagged them in July 2026.

This is a standalone safety net on top of the write-time guard in
`_anki.store_media()` (which only protects audio this skill itself writes).
Run this periodically, or whenever cards from an EXTERNAL source (another
add-on, a manual import, a shared deck) enter the collection, since those
never go through store_media() at all.

Usage:
    python3 audit_media.py                  # report only, referenced files
    python3 audit_media.py --fix            # fix + update every referencing note
    python3 audit_media.py --include-orphans  # also list mismatches on files no note points to
"""
import argparse
import sys
from pathlib import Path

from _anki import anki_request, _sniff_audio_container, _RENAME_ONLY, _transcode_to_mp3


def media_dir() -> Path:
    return Path(anki_request("getMediaDirPath"))


def scan(mdir: Path, include_orphans: bool = False):
    """Returns [(path, actual_kind, referencing_note_ids)]. Orphaned mismatches
    (no note references the file -- e.g. a stale leftover from a previous fix)
    are skipped by default since they're inert and Anki's own Tools > Check
    Media > Delete Unused already handles them."""
    mismatches = []
    for f in mdir.iterdir():
        suffix = f.suffix.lower()
        if suffix not in (".wav", ".mp3"):
            continue
        actual = _sniff_audio_container(f)
        if not actual or _RENAME_ONLY.get(actual) == suffix.lstrip("."):
            continue
        nids = anki_request("findNotes", query=f'"{f.name}"')
        if nids or include_orphans:
            mismatches.append((f, actual, nids))
    return mismatches


def fix_one(f: Path, actual: str):
    """Returns (new_filename, new_path) after correcting the file on disk."""
    if actual in _RENAME_ONLY:
        new_path = f.with_suffix(f".{_RENAME_ONLY[actual]}")
        f.rename(new_path)
    else:
        new_path = _transcode_to_mp3(f)
        if new_path != f:
            f.unlink()
    return new_path.name, new_path


def update_referencing_notes(old_name: str, new_name: str):
    """Find every note referencing old_name in ANY audio-bearing field and swap
    the filename in place. Returns the list of (note_id, field) touched."""
    nids = anki_request("findNotes", query=f'"{old_name}"')
    touched = []
    if not nids:
        return touched
    for n in anki_request("notesInfo", notes=nids):
        updates = {}
        for field, data in n["fields"].items():
            if old_name in data["value"]:
                updates[field] = data["value"].replace(old_name, new_name)
        if updates:
            anki_request("updateNoteFields", note={"id": n["noteId"], "fields": updates})
            touched.append((n["noteId"], list(updates)))
    return touched


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true", help="Remux/transcode mismatches and update referencing notes")
    ap.add_argument("--include-orphans", action="store_true",
                    help="Also list mismatches on files no current note references")
    args = ap.parse_args()

    mdir = media_dir()
    mismatches = scan(mdir, include_orphans=args.include_orphans)

    if not mismatches:
        print("No extension/content mismatches found on any note-referenced audio.")
        return

    print(f"Found {len(mismatches)} mismatched file(s):")
    for f, actual, nids in mismatches:
        tag = f"{len(nids)} note(s)" if nids else "orphaned, no note references it"
        print(f"  {f.name}  (actually {actual}; {tag})")

    if not args.fix:
        print("\nRe-run with --fix to correct these and update every referencing note.")
        return

    print()
    for f, actual, _nids in mismatches:
        old_name = f.name
        new_name, new_path = fix_one(f, actual)
        touched = update_referencing_notes(old_name, new_name)
        if touched:
            for nid, fields in touched:
                print(f"  {old_name} -> {new_name}  (note {nid}: {', '.join(fields)})")
        else:
            print(f"  {old_name} -> {new_name}  (not referenced by any current note)")


if __name__ == "__main__":
    main()
