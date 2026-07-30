#!/usr/bin/env python3
"""Classify a ray-os working tree ahead of a commit sweep.

Sorts everything git reports into junk / hold / ready, and runs the repo-specific
checks that are easy to forget by hand: orphan images, images outside the flat
vault-root images/ folder, root-level strays, deletions of tracked files, and the
LFS payload a push would carry.

Read-only. Never stages, commits, or deletes anything.
"""

import os
import re
import subprocess
import sys
from collections import defaultdict

JUNK = re.compile(
    r"(^|/)(__pycache__|node_modules|\.venv|venv|\.pytest_cache|\.mypy_cache"
    r"|\.ruff_cache|\.DS_Store|[^/]+\.egg-info)(/|$)|\.pyc$|\.pyo$"
)
MEDIA = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
WIKILINK = re.compile(r"!?\[\[([^\]|#]+)")


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout


def repo_root():
    root = sh("git", "rev-parse", "--show-toplevel").strip()
    if not root:
        sys.exit("not inside a git repository")
    return root


def entries(root):
    """(index_status, worktree_status, path) for everything git reports.

    Untracked directories are expanded to their files so a whole tree of junk
    doesn't hide behind a single line.
    """
    out = sh("git", "-C", root, "status", "--porcelain", "-uall", "-z")
    items, parts = [], out.split("\0")
    i = 0
    while i < len(parts):
        p = parts[i]
        if len(p) < 4:
            i += 1
            continue
        x, y, path = p[0], p[1], p[3:]
        # renames carry a second NUL-separated path; skip the origin
        if "R" in (x, y):
            i += 1
        items.append((x, y, path))
        i += 1
    return items


def linked_names(root):
    """Every wikilink target referenced by any note in the vault."""
    names = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", "node_modules", "__pycache__")
        ]
        for fn in filenames:
            if not fn.endswith((".md", ".html", ".canvas")):
                continue
            try:
                with open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore") as fh:
                    for m in WIKILINK.finditer(fh.read()):
                        names.add(m.group(1).strip())
            except OSError:
                pass
    return names


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def section(title, rows):
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("  (none)")
    for r in rows:
        print(f"  {r}")


def main():
    root = repo_root()
    items = entries(root)
    if not items:
        print("Working tree is clean — nothing to sweep.")
        return 0

    junk, hold, ready = [], [], []
    media_paths = []
    deleted_paths = []
    linked = None

    for x, y, path in items:
        status = f"{x}{y}".strip() or "??"
        untracked = (x, y) == ("?", "?")
        deleted = "D" in (x, y)
        base = os.path.basename(path)
        stem, ext = os.path.splitext(base)
        ext = ext.lower()

        if JUNK.search(path):
            junk.append(f"[{status}] {path}")
            continue

        if deleted:
            deleted_paths.append(path)
            ready.append((status, path))
            continue

        reasons = []
        if ext in MEDIA:
            media_paths.append(path)
            in_images = path.startswith("images/") and path.count("/") == 1
            if not in_images:
                where = "repo root" if "/" not in path else os.path.dirname(path)
                reasons.append(f"media outside vault-root images/ (in {where})")
            elif untracked:
                if linked is None:
                    linked = linked_names(root)
                if base not in linked and stem not in linked:
                    reasons.append("orphan: no note references it")
            if not KEBAB.match(stem):
                reasons.append("filename is not kebab-case")
        elif "/" not in path and untracked:
            reasons.append("new file at repo root; content usually lives in a subfolder")

        if reasons:
            hold.append(f"[{status}] {path}  — " + "; ".join(reasons))
        else:
            ready.append((status, path))

    groups = defaultdict(list)
    for status, path in ready:
        top = path.split("/")[0] if "/" in path else "(root)"
        if top == ".claude" and path.startswith(".claude/skills/"):
            top = "/".join(path.split("/")[:3])
        groups[top].append((status, path))

    print(f"commit-sweep triage — {len(items)} entries in {root}")

    section("NEVER COMMIT — junk", junk)
    section("HOLD — needs a human decision", hold)

    print("\nREADY — grouped by area")
    print("-" * 22)
    if not groups:
        print("  (none)")
    for top in sorted(groups):
        rows = groups[top]
        print(f"  {top}  ({len(rows)} file{'s' if len(rows) != 1 else ''})")
        for status, path in rows[:6]:
            print(f"      [{status}] {path}")
        if len(rows) > 6:
            print(f"      … and {len(rows) - 6} more")

    if deleted_paths:
        n = len(deleted_paths)
        print(f"\nDELETIONS — {n} tracked file{'s' if n != 1 else ''} removed from disk")
        print("-" * 22)
        print("  Included in READY above: commit these, grouped by area, like any")
        print("  other change. The content stays recoverable from history.")
        print("  Before committing, check each one is a real removal and not half of")
        print("  a rename — if the content reappeared elsewhere, stage both paths so")
        print("  git records a rename instead of a delete plus an add.")
        if n >= 25:
            print(f"  {n} at once is a lot. Say so plainly in the report, and name the")
            print("  directories that vanished, so Ray can spot collateral damage.")

    payload = 0
    for p in media_paths:
        fp = os.path.join(root, p)
        if os.path.isfile(fp):
            payload += os.path.getsize(fp)
    print("\nLFS PAYLOAD")
    print("-" * 11)
    if media_paths:
        n = len(media_paths)
        print(f"  {n} media file{'s' if n != 1 else ''}, {human(payload)}")
        print("  Report this to Ray before pushing — LFS bandwidth is spent on every")
        print("  future clone, so trimming is cheap now and permanent after the push.")
    else:
        print("  (no media)")

    print("\nNext: group the READY files into separately-revertable commits.")
    print("Keep reusable tooling (skills, scripts) apart from the content it generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
