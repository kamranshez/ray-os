#!/usr/bin/env bash
# Build a throwaway git repo that mimics a messy ray-os working tree, with a
# local bare remote so a push can be verified without touching anything real.
#
#   ./make-fixture.sh /path/to/fixture-dir
#
# The tree deliberately contains one instance of every case the skill has to get
# right: a clean split between tooling and the content it generated, junk that
# must never be committed, a stray at repo root, an orphan image, and a deletion
# of a tracked file that needs a human decision.
set -euo pipefail

DEST="${1:?usage: make-fixture.sh <dir>}"
rm -rf "$DEST"
mkdir -p "$DEST"
DEST="$(cd "$DEST" && pwd)"

REMOTE="$DEST/remote.git"
WORK="$DEST/vault"

git init -q --bare "$REMOTE"
git init -q -b main "$WORK"
cd "$WORK"
git config user.name "Ray Amjad"
git config user.email "r@rayamjad.com"
git config commit.gpgsign false
git remote add origin "$REMOTE"

png() { printf '\211PNG\r\n\032\n%s' "$(head -c 2000 /dev/urandom | base64)" > "$1"; }

# ---------- committed baseline ----------
cat > .gitattributes <<'EOF'
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
EOF
cat > .gitignore <<'EOF'
.DS_Store
scratchpad/
EOF
mkdir -p .claude/skills/old-skill/references .obsidian notes images
echo "colour tokens for the old skill" > .claude/skills/old-skill/references/palette.md
echo "layout notes for the old skill"  > .claude/skills/old-skill/references/layouts.md
printf '{"activeLeaf":"one"}\n' > .obsidian/workspace.json
cat > notes/existing-note.md <<'EOF'
An existing note that was already committed.
EOF

# The vault's own conventions live in the repo, exactly as ray-os keeps them in
# CLAUDE.md. Both eval configurations can read this, so the comparison measures
# the skill's workflow rather than whether one side was handed the house rules.
cat > CLAUDE.md <<'EOF'
# fixture-vault

A personal Obsidian vault. Content lives in notes/; the repo doubles as a vault.

<important if="you are adding, embedding, or moving images in notes">
All images live in a single vault-root `images/` folder. There are no co-located
per-note image folders.

- **Location**: every image goes directly in `images/<descriptive-name>.png`. No subfolders.
- **Naming**: kebab-case, descriptive of the image's content, globally unique.
  Never keep tool-default names like `screenshot.png` or `CleanShot 2026-05-17.png`.
- **Embeds**: filename-only wikilinks, `![[descriptive-name.png]]`.
- **No orphans**: only keep images that a note actually references. Unreferenced
  images are deleted.
- **LFS**: all image types (`*.png`, `*.jpg`) are tracked via Git LFS.
</important>

<important if="you are creating new files or folders, or naming anything in the vault">
- **kebab-case everything** — all file and folder names use `kebab-case`.
- **Never delete files without explicit user permission.**
</important>
EOF
git add -A
git -c commit.gpgsign=false commit -q -m "vault: initial state"
git push -q origin main
git branch -q --set-upstream-to=origin/main main 2>/dev/null || true

# ---------- the mess ----------

# 1. Generated media, properly named and referenced by a new note.
for i in 1 2 3; do png "images/fixture-pipeline-$i.png"; done

# 2. The note that embeds them. Meaningless apart from the images.
cat > notes/pipeline-explainer.md <<'EOF'
---
tags: [fixture]
---

How the pipeline fits together.

![[fixture-pipeline-1.png]]
![[fixture-pipeline-2.png]]
![[fixture-pipeline-3.png]]
EOF

# 3. A new reusable skill. Must NOT share a commit with the images above —
#    tooling and generated content have different lifetimes.
mkdir -p .claude/skills/diagram-maker/scripts
cat > .claude/skills/diagram-maker/SKILL.md <<'EOF'
---
name: diagram-maker
description: Draw pipeline diagrams.
---
Draw one idea per diagram.
EOF
echo 'print("draw")' > .claude/skills/diagram-maker/scripts/draw.py

# 4. Junk. Never committed.
mkdir -p notes/scripts/__pycache__
printf '\x00compiled' > notes/scripts/__pycache__/helper.cpython-314.pyc
echo "def helper(): pass" > notes/scripts/helper.py

# 5. Stray at repo root with a generic name. Wrong place, wrong name.
png "screenshot.png"

# 6. Orphan image: correct folder and name, but no note references it.
png "images/fixture-unused-panel.png"

# 7. Deletion of a tracked file. A human decides whether this ships.
rm .claude/skills/old-skill/references/layouts.md

# 8. Obsidian UI churn.
printf '{"activeLeaf":"two"}\n' > .obsidian/workspace.json

echo "fixture ready"
echo "  work repo : $WORK"
echo "  bare remote: $REMOTE"
