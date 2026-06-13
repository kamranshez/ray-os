#!/usr/bin/env python3
"""Turn a markdown script/note into Loom teleprompter-ready text chunks.

Loom's teleprompter (the on-screen script you read while recording) caps a
single script at ~5000 characters and silently refuses a paste that's over.
So a full video script has to go in as several chunks. This script:

  1. strips YAML frontmatter,
  2. removes things you don't read aloud — image embeds (![[...]] and
     ![](...)) and [IMAGE: ...] / [VISUAL: ...] stage directions,
  3. keeps the spoken prose, headings, and fenced code blocks,
  4. splits the result into chunks under the limit, preferring `## ` section
     boundaries (and falling back to paragraph / hard splits if a single
     section is itself too long),
  5. writes each chunk to <outdir>/<stem>-notes-partN.txt, and
  6. optionally opens them in TextEdit.

The TextEdit step exists because the shell that runs this is often sandboxed:
`pbcopy` there writes to a session pasteboard that never reaches the GUI
clipboard, so a programmatic copy looks like it worked but Cmd+V pastes
nothing. Opening the files in a real GUI window lets the user copy reliably
with Cmd+A / Cmd+C.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)


def strip_for_speech(md_text: str) -> str:
    """Remove frontmatter, image embeds, and stage directions; keep prose."""
    text = FRONTMATTER_RE.sub("", md_text, count=1)
    kept = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("![[") or s.startswith("!["):   # wikilink / md image embeds
            continue
        if s.startswith("[IMAGE:") or s.startswith("[VISUAL:"):  # stage directions
            continue
        kept.append(line)
    out = "\n".join(kept)
    out = re.sub(r"\n{3,}", "\n\n", out)  # collapse runs of blank lines
    return out.strip()


def _hard_split(s: str, limit: int):
    """Last resort: cut an oversized blob on whitespace near the limit."""
    parts = []
    while len(s) > limit:
        cut = s.rfind("\n", 0, limit)
        if cut <= 0:
            cut = s.rfind(" ", 0, limit)
        if cut <= 0:
            cut = limit
        parts.append(s[:cut].strip())
        s = s[cut:].strip()
    if s:
        parts.append(s)
    return parts


def _split_oversized_section(section: str, limit: int):
    """A section bigger than the limit: split on blank-line paragraphs,
    then hard-split any paragraph still too large."""
    chunks, cur = [], ""
    for para in section.split("\n\n"):
        if len(para) > limit:
            if cur:
                chunks.append(cur.strip())
                cur = ""
            chunks.extend(_hard_split(para, limit))
            continue
        candidate = f"{cur}\n\n{para}" if cur else para
        if len(candidate) > limit:
            chunks.append(cur.strip())
            cur = para
        else:
            cur = candidate
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def chunk_text(text: str, limit: int):
    """Group `## ` sections into chunks under `limit`, preserving order."""
    # Keep the heading attached to its section by splitting *before* each `## `.
    sections = re.split(r"(?=^## )", text, flags=re.M)
    chunks, cur = [], ""
    for sec in sections:
        if not sec.strip():
            continue
        if len(sec) > limit:
            if cur.strip():
                chunks.append(cur.strip())
                cur = ""
            chunks.extend(_split_oversized_section(sec.strip(), limit))
            continue
        candidate = f"{cur}{sec}" if cur else sec
        if cur and len(candidate) > limit:
            chunks.append(cur.strip())
            cur = sec
        else:
            cur = candidate
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="Markdown file to convert")
    ap.add_argument("--limit", type=int, default=4800,
                    help="Max characters per chunk (default 4800, safely under Loom's ~5000 cap)")
    ap.add_argument("--outdir", type=Path, default=Path.home() / "Downloads",
                    help="Where to write the chunk files (default ~/Downloads)")
    ap.add_argument("--open", dest="do_open", action="store_true", default=True,
                    help="Open the chunks in TextEdit (default on)")
    ap.add_argument("--no-open", dest="do_open", action="store_false",
                    help="Don't open the chunks in TextEdit")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    speech = strip_for_speech(args.input.read_text())
    if not speech:
        print("error: nothing left after stripping — is this an empty/all-image file?", file=sys.stderr)
        sys.exit(1)

    chunks = chunk_text(speech, args.limit)
    args.outdir.mkdir(parents=True, exist_ok=True)
    stem = args.input.stem

    paths = []
    if len(chunks) == 1:
        p = args.outdir / f"{stem}-notes.txt"
        p.write_text(chunks[0] + "\n")
        paths.append(p)
        print(f"{len(chunks[0])} chars (fits in one teleprompter paste) -> {p}")
    else:
        for i, c in enumerate(chunks, 1):
            p = args.outdir / f"{stem}-notes-part{i}.txt"
            p.write_text(c + "\n")
            paths.append(p)
            print(f"part{i}: {len(c)} chars -> {p}")

    if args.do_open:
        subprocess.run(["open", "-a", "TextEdit", *map(str, paths)], check=False)
        print(f"opened {len(paths)} file(s) in TextEdit — Cmd+A, Cmd+C in each, paste into Loom in order")


if __name__ == "__main__":
    main()
