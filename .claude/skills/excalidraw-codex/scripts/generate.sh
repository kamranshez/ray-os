#!/usr/bin/env bash
# Generate excalidraw-style images via the headless Codex CLI (`codex exec`).
#
# Wraps `codex exec --json` with these conveniences:
#   - Attaches the bundled reference images from assets/ by default. The
#     wrapper prompt tells codex they are STYLE EXAMPLES ONLY so it copies
#     the aesthetic without reusing their subject matter.
#   - Asks the Codex CLI to produce N variations inside ONE session.
#   - After codex finishes, collects every PNG that landed under
#     ~/.codex/generated_images/<thread_id>/ and copies them into the user's
#     output dir with kebab-case sequential filenames: excalidraw_1.png ...
#
# Usage:
#   generate.sh -p "<verbatim prompt>" -o /abs/path/to/out -n 5 [-a 16:9] [-r ref1.png -r ref2.png] [--no-default-refs]
#
# Notes:
#   - Each codex exec call writes images to a fresh session UUID dir.
#   - Asking for >5 in a single call can be slow; for big batches, run multiple
#     parallel invocations of this script (each gets its own session UUID).
#   - Output filenames auto-increment if files already exist in -o.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS_DIR="$SKILL_DIR/assets"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

PROMPT=""
OUT_DIR=""
COUNT=5
ASPECT="16:9"
BASENAME="excalidraw"
USE_DEFAULT_REFS=1
REFS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--prompt) PROMPT="$2"; shift 2 ;;
    -o|--output) OUT_DIR="$2"; shift 2 ;;
    -n|--count)  COUNT="$2";  shift 2 ;;
    -a|--aspect) ASPECT="$2"; shift 2 ;;
    -x|--name)   BASENAME="$2"; shift 2 ;;
    -r|--ref)    REFS+=("$2"); shift 2 ;;
    --default-refs) USE_DEFAULT_REFS=1; shift ;;
    --no-default-refs) USE_DEFAULT_REFS=0; shift ;;
    -h|--help)
      sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$PROMPT" || -z "$OUT_DIR" ]]; then
  echo "Required: -p <prompt> and -o <output_dir>" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"

if [[ $USE_DEFAULT_REFS -eq 1 ]]; then
  for f in "$ASSETS_DIR"/reference*.png; do
    [[ -f "$f" ]] && REFS+=("$f")
  done
fi

CODEX_ARGS=(exec --skip-git-repo-check --json)
for r in "${REFS[@]+"${REFS[@]}"}"; do
  CODEX_ARGS+=(-i "$r")
done

# Wrap the user's prompt with strict directives:
#   * Generate exactly N images (variations of the same concept) in this call.
#   * Describe the excalidraw aesthetic in words (refs are off by default
#     because attaching prior concept diagrams caused subject-matter bleed).
#   * Don't copy files anywhere, don't run sips/find/git — just generate.
if [[ ${#REFS[@]} -gt 0 ]]; then
  STYLE_BLOCK="The reference images attached are STYLE EXAMPLES ONLY. Match their
hand-drawn excalidraw aesthetic — do NOT reuse their subject matter, diagrams,
labels, or composition. Your image's subject is defined entirely by the Image
content section below."
else
  STYLE_BLOCK="Excalidraw hand-drawn aesthetic in DARK MODE: chalk-style off-white
sketchy outlines on a near-black charcoal background (#0E1116), slight imperfect
lines, handwritten-style light labels, soft glowing accent colors only. When
people or avatars are needed, draw a small cute light-blue robot character (round
head, antenna, glowing blue eyes, simple smiling face, two short arms)."
fi

WRAPPED_PROMPT=$(cat <<EOF
You are running headlessly. Do not load skills, do not read files, do not copy
or move outputs anywhere — just call the image_gen tool ${COUNT} time(s) in this
single turn to produce ${COUNT} distinct variations of the image described below.

${STYLE_BLOCK}

Aspect ratio: ${ASPECT}. Background: near-black dark charcoal #0E1116 (dark mode)
— solid, no gradients, no textures. After all images are generated, your final message should just list
the saved file paths under \$CODEX_HOME/generated_images/<this-session>/.

Image content (verbatim, do not summarize):

${PROMPT}
EOF
)

# Run codex exec, stream JSONL, capture thread_id.
TMP_LOG="$(mktemp)"
trap 'rm -f "$TMP_LOG"' EXIT

printf '%s' "$WRAPPED_PROMPT" | codex "${CODEX_ARGS[@]}" - 2>&1 | tee "$TMP_LOG" >/dev/null

THREAD_ID=$(grep -m1 -o '"thread_id":"[^"]*"' "$TMP_LOG" | head -1 | sed 's/.*"thread_id":"\([^"]*\)".*/\1/')
if [[ -z "$THREAD_ID" ]]; then
  echo "Could not extract thread_id from codex output. Log:" >&2
  cat "$TMP_LOG" >&2
  exit 1
fi

SESSION_DIR="$CODEX_HOME/generated_images/$THREAD_ID"
if [[ ! -d "$SESSION_DIR" ]]; then
  echo "Codex session dir missing: $SESSION_DIR" >&2
  exit 1
fi

# Copy each PNG into OUT_DIR as "<BASENAME>-<N>.png", no overwrite.
next_index() {
  local i=1
  while [[ -e "$OUT_DIR/${BASENAME}-${i}.png" ]]; do i=$((i+1)); done
  echo "$i"
}

COPIED=0
for src in "$SESSION_DIR"/*.png; do
  [[ -f "$src" ]] || continue
  idx=$(next_index)
  dst="$OUT_DIR/${BASENAME}-${idx}.png"
  cp "$src" "$dst"
  echo "$dst"
  COPIED=$((COPIED+1))
done

if [[ $COPIED -eq 0 ]]; then
  echo "No PNGs found in $SESSION_DIR" >&2
  exit 1
fi

echo "Copied $COPIED image(s) into $OUT_DIR (session $THREAD_ID)" >&2
