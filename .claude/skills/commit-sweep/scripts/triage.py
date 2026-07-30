#!/usr/bin/env python3
"""Classify a ray-os working tree ahead of a commit sweep.

Sorts everything git reports into junk / renames / hold / ready, and runs the
repo-specific checks that are easy to forget by hand: orphan images, images
outside the flat vault-root images/ folder, root-level strays, deletions of
tracked files, and the LFS payload a push would carry.

Renames are found by content, not by name: every deleted path is hashed from the
index and every untracked file from disk, so a file that moved is reported as one
rename instead of a deletion plus an unrelated addition. Files whose basename
survived but whose content changed are reported separately as move-plus-edit
candidates, since only a human can confirm those.

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


def blob_shas_index(root, paths):
    """path -> blob sha recorded in the index; works for files gone from disk."""
    want = set(paths)
    if not want:
        return {}
    found = {}
    for rec in sh("git", "-C", root, "ls-files", "-s", "-z").split("\0"):
        if "\t" not in rec:
            continue
        meta, path = rec.split("\t", 1)
        bits = meta.split()
        if len(bits) >= 2 and path in want:
            found[path] = bits[1]
    return found


def blob_shas_disk(root, paths):
    """path -> blob sha computed from the file as it sits on disk."""
    if not paths:
        return {}
    r = subprocess.run(
        ["git", "-C", root, "hash-object", "--stdin-paths"],
        input="\n".join(paths) + "\n",
        capture_output=True,
        text=True,
    )
    shas = [s for s in r.stdout.splitlines() if s]
    if len(shas) != len(paths):
        return {}  # a path vanished mid-run; fall back to reporting no renames
    return dict(zip(paths, shas))


def detect_renames(root, deleted, untracked):
    """Pair deletions with untracked files that hold the same content.

    Returns (renames, moved_edited): exact content matches, and same-basename
    pairs whose content differs. Both are pairs of (old_path, new_path).
    """
    old = blob_shas_index(root, deleted)
    new = blob_shas_disk(root, untracked)

    by_sha = defaultdict(list)
    for path, sha in new.items():
        by_sha[sha].append(path)

    renames, claimed = [], set()
    for o in deleted:
        sha = old.get(o)
        if not sha:
            continue
        free = [p for p in sorted(by_sha.get(sha, [])) if p not in claimed]
        if free:
            claimed.add(free[0])
            renames.append((o, free[0]))

    matched_old = {o for o, _ in renames}
    by_base = defaultdict(list)
    for path in new:
        if path not in claimed:
            by_base[os.path.basename(path)].append(path)

    moved_edited = []
    for o in deleted:
        if o in matched_old:
            continue
        free = [p for p in sorted(by_base.get(os.path.basename(o), [])) if p not in claimed]
        if free:
            claimed.add(free[0])
            moved_edited.append((o, free[0]))

    return renames, moved_edited


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

    # Pair moves before classifying, so a relocated file is one rename rather
    # than a deletion plus an unrelated addition.
    renames, moved_edited = detect_renames(
        root,
        [p for x, y, p in items if "D" in (x, y) and not JUNK.search(p)],
        [p for x, y, p in items if (x, y) == ("?", "?") and not JUNK.search(p)],
    )
    paired = {p for pair in renames + moved_edited for p in pair}

    for x, y, path in items:
        if path in paired:
            continue
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

    if renames or moved_edited:
        print("\nRENAMES — stage both paths so git records a move")
        print("-" * 22)
        for o, n in renames:
            print(f"  {o}\n    -> {n}")
        for o, n in moved_edited:
            print(f"  {o}\n    -> {n}   (same name, content CHANGED — confirm it is the same file)")
        print("  Stage the old and new path together in one commit. Staged apart,")
        print("  git records a delete plus an add and the connection is lost.")

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
        print("  Moves are already filtered out into RENAMES above, so these are")
        print("  real removals. Bulk pruning is routine in this vault: name the")
        print("  directories that went in a sentence, and skip the incident report.")
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
