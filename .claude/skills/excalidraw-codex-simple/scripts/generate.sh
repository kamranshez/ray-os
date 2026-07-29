#!/usr/bin/env bash
# Generate SIMPLE excalidraw-style idea diagrams via the headless Codex CLI.
#
# Differs from the excalidraw-codex skill in one decisive way: the prompt is
# an IDEA STATED AS MEANING, not source text passed verbatim. Passing text
# verbatim makes the model treat every sentence as a rendering requirement and
# it returns an exhaustive poster with no focal point. Here the wrapper adds a
# hard constraint set (one idea, no illustration, word budget, huge margins)
# and explicitly hands the geometry to the model rather than prescribing it.
#
# Wraps `codex exec --json` with these conveniences:
#   - Attaches the bundled assets/reference*.png as STYLE-ONLY examples.
#   - Asks the Codex CLI to produce N distinct variations inside ONE session.
#   - After codex finishes, collects every PNG that landed under
#     ~/.codex/generated_images/<thread_id>/ and copies them into the user's
#     output dir with kebab-case sequential filenames: <slug>-1.png ...
#
# Usage:
#   generate.sh -p "<idea stated as meaning>" -o /abs/out -n 3 [-w 10] [-a 16:9] [-r ref.png] [--no-default-refs]
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
MAX_WORDS=10
REFS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--prompt) PROMPT="$2"; shift 2 ;;
    -o|--output) OUT_DIR="$2"; shift 2 ;;
    -n|--count)  COUNT="$2";  shift 2 ;;
    -a|--aspect) ASPECT="$2"; shift 2 ;;
    -x|--name)   BASENAME="$2"; shift 2 ;;
    -w|--words)  MAX_WORDS="$2"; shift 2 ;;
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

# --- strip production timestamps from the prompt ------------------------------
# Section headers from video scripts often carry timecodes, e.g.
#   "### Don't waste the run on one leaf (7:55 - 9:25)".
# Left in the prompt, the model renders the timecode INTO the image (it showed
# up in a corner of generated diagrams). These are production directions, never
# visual content, so we scrub them here while leaving the rest verbatim:
#   * parenthesized ranges:   "(2:15 - 4:00)"  ->  ""
#   * bare ranges:            "7:55 - 9:25"    ->  ""
#   * lone parenthesized cue: "(0:00)"         ->  ""
# Handles -, en dash, and em dash as the separator.
PROMPT="$(printf '%s' "$PROMPT" | perl -CSAD -pe '
  s/\(\s*\d{1,2}:\d{2}\s*[-\x{2013}\x{2014}]\s*\d{1,2}:\d{2}\s*\)//g;
  s/\b\d{1,2}:\d{2}\s*[-\x{2013}\x{2014}]\s*\d{1,2}:\d{2}\b//g;
  s/\(\s*\d{1,2}:\d{2}\s*\)//g;
  s/[ \t]+$//;
')"
# -----------------------------------------------------------------------------

# --- codex version check -----------------------------------------------------
# REQUIRES codex 0.144.1+. History:
#   * 0.140.0-0.143.x shipped a regression (openai/codex#28422) where image_gen
#     produced a valid PNG but never persisted it to disk; fixed in 0.144.
#   * The old 0.139.0 pin is now ALSO broken (verified 2026-07-12): the account's
#     configured default model (gpt-5.6-terra in ~/.codex/config.toml) rejects
#     old CLIs with "requires a newer version of Codex", and the failure is
#     silent because this script's set -e kills the run before the error prints.
# Verified working: 0.144.1 (2026-07-12, real 1672x941 PNGs saved). Install:
#   npm install -g @openai/codex@latest
CODEX_VER="$(codex --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
case "$CODEX_VER" in
  0.14[4-9].*|0.1[5-9]*.*|0.[2-9]*.*|[1-9]*.*) : ;;  # 0.144.1+ known-good
  0.139.*|0.140.*|0.141.*|0.142.*|0.143.*)
    echo "WARNING: codex $CODEX_VER is active. This version is BROKEN for this skill:" >&2
    echo "         0.140-0.143 never save the PNG (openai/codex#28422); 0.139 is rejected by" >&2
    echo "         the account's default model (gpt-5.6-terra needs a newer CLI). Upgrade:" >&2
    echo "           npm install -g @openai/codex@latest" >&2
    ;;
  "") echo "WARNING: could not determine codex version; this skill requires codex 0.144.1+." >&2 ;;
  *)  echo "NOTE: codex $CODEX_VER is untested with this skill (verified on 0.144.1)." >&2 ;;
esac
# -----------------------------------------------------------------------------

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
read -r -d '' LANGUAGE <<'L_EOF' || true
VISUAL LANGUAGE — authentic Excalidraw. A genuinely hand-sketched vector look:
visibly wobbly, imperfect strokes with the doubled-back, slightly overshooting
line ends of a rough-sketch renderer. Rectangles do not quite close; circles are
a little lumpy. Near-black canvas. Excalidraw's own palette — white ink plus a
muted red, a muted blue, an amber and a green — with at most two colours used in
any one image. Fills are either transparent or a loose scribbled cross-hatch
that overshoots its own shape. Handwriting throughout, large and confident.
L_EOF

if [[ ${#REFS[@]} -gt 0 ]]; then
  STYLE_BLOCK="${LANGUAGE}

Match the attached reference images exactly for STYLE. Their subject matter is
irrelevant — do NOT reuse their shapes, labels or composition. Only their visual
grammar matters."
else
  STYLE_BLOCK="${LANGUAGE}"
fi

# The constraint set is the entire point of this skill. Passing source text
# verbatim makes the model treat every sentence as a rendering requirement, so
# it produces an exhaustive poster with no focal point. These rules force one
# idea per frame, and hand the geometry to the model instead of prescribing it.
read -r -d '' CONSTRAINTS <<C_EOF || true
This is ONE frame of a video, on screen for about 20 seconds, watched at 1080p
and often on a phone. It must be grasped in TWO SECONDS. Legibility beats
completeness; every extra element costs the viewer attention.

NON-NEGOTIABLE:
- ONE idea, drawn with the fewest possible marks. If an element can be removed
  and the idea still lands, remove it. Leaving things out is the goal.
- Abstract geometry and typography only. NO illustration: no characters, no
  robots, no faces, no objects drawn as little pictures, no scenery, no icons
  drawn as miniature illustrations.
- Labels are few and large, and sit as plain floating handwriting rather than
  being crammed inside shapes.
- Enormous negative space. Wide empty margins. The diagram is small in a big
  frame, not edge to edge.
- Exactly ONE focal point. The eye must know where to land first.
- No title bar, no header, no footer, no legend box, no quote panel, no
  numbered stage badges.
- ${MAX_WORDS} WORDS MAXIMUM in the entire image.

The geometry is yours to invent. Do not imitate any diagram you have seen —
solve the idea however this visual language wants to solve it.
C_EOF

WRAPPED_PROMPT=$(cat <<EOF
You are running headlessly. Do not load skills, do not read files, do not copy
or move outputs anywhere — just call the image_gen tool ${COUNT} time(s) in this
single turn to produce ${COUNT} distinct variations of the diagram described
below. Make the variations genuinely different solutions to the same idea, not
recolours of one layout.

${STYLE_BLOCK}

${CONSTRAINTS}

Aspect ratio: ${ASPECT}. Background: near-black (#0E1116) — solid, no gradients,
no textures. After all images are generated, your final message should just list
the saved file paths under \$CODEX_HOME/generated_images/<this-session>/.

THE IDEA TO EXPRESS — this is meaning, not a drawing spec. Express it; do not
transcribe it, and do not try to depict every sentence of it:

${PROMPT}
EOF
)

# Run codex exec, stream JSONL, capture thread_id.
TMP_LOG="$(mktemp)"
trap 'rm -f "$TMP_LOG"' EXIT

# `|| true`: with set -e + pipefail, a nonzero codex exit would kill the script
# HERE, before any error reporting below could run — that made auth expiry
# (401 turn.failed) fail silently with an empty log. Tolerate the exit code,
# then inspect the captured JSONL for what actually happened.
printf '%s' "$WRAPPED_PROMPT" | codex "${CODEX_ARGS[@]}" - 2>&1 | tee "$TMP_LOG" >/dev/null || true

# Surface fatal turn errors explicitly (auth expiry is the common one).
if grep -q '"type":"turn.failed"' "$TMP_LOG"; then
  echo "Codex turn FAILED. Error detail:" >&2
  grep -o '"turn.failed".*' "$TMP_LOG" | head -1 >&2
  if grep -q '401 Unauthorized' "$TMP_LOG"; then
    echo "" >&2
    echo "This is an AUTH failure: the codex CLI is logged out or its token expired." >&2
    echo "Check with:  codex login status" >&2
    echo "Fix with:    codex login   (interactive browser flow)" >&2
  fi
  exit 1
fi

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
