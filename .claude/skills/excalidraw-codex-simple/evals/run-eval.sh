#!/usr/bin/env bash
# Eval for excalidraw-codex-simple. Four cases, each targeting a specific
# failure mode of the predecessor skill.
set -u

OUT="${EVAL_OUT:-/tmp/excalidraw-simple-eval}"
GEN="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)/generate.sh"
mkdir -p "$OUT"

# CASE 1 — CLUTTER TRAP. Deliberately paste dense multi-idea prose, the way a
# user would if they ignored the skill's rule. Must still produce ONE simple
# diagram, not a poster.
cat > "$OUT/p-dense.txt" <<'EOF'
LAYER 3 — Judgment. Artifact on screen: a rubric, not a prompt. What it catches:
rows 13 and 14, the things that are real, expensive, and impossible to assert.
Is the error message useful. Is the feature discoverable. Does this look like the
rest of the product. Worth naming why it's a rubric and not "hey Claude is this
good": Qwen found that decomposing into structured dimensions took judge-human
agreement to a Spearman correlation around 0.9, and made different judge models
agree at Kendall tau above 0.93. How it goes blind: this is the first layer that
can be persuaded. Static judges got gamed by length: models learned to emit more
CSS and JavaScript because verbose output scored better. And the structural
problem: a judge calibrated against weak output cannot discriminate between two
strong outputs. It saturates.
EOF

# CASE 2 — ILLUSTRATION TRAP. Names people and agents explicitly. The old refs
# would render cute robots and human figures here.
cat > "$OUT/p-people.txt" <<'EOF'
An engineer hands a piece of work to an AI agent. The agent does the work and
hands it back. The engineer checks it only by looking at the finished result,
and never sees anything about how the agent actually got there.
EOF

# CASE 3 — BASELINE. A clean relational idea, stated as meaning.
cat > "$OUT/p-relation.txt" <<'EOF'
Two systems that look identical from the outside and produce the same output,
but one of them arrived there by a route that should worry you. From outside,
nothing distinguishes them.
EOF

# CASE 4 — WORD BUDGET FLAG. -w 4 must visibly tighten the text.
cat > "$OUT/p-wordcap.txt" <<'EOF'
Something is chased but never caught: as the pursuer advances, the target moves
away by exactly the same distance, so the gap never closes.
EOF

echo "eval start $(date +%H:%M:%S)"

( "$GEN" -p "$(cat "$OUT/p-dense.txt")"    -o "$OUT" -x "eval-dense"    -n 2 > "$OUT/dense.log" 2>&1 ) &
( "$GEN" -p "$(cat "$OUT/p-people.txt")"   -o "$OUT" -x "eval-people"   -n 2 > "$OUT/people.log" 2>&1 ) &
( "$GEN" -p "$(cat "$OUT/p-relation.txt")" -o "$OUT" -x "eval-relation" -n 2 > "$OUT/relation.log" 2>&1 ) &
( "$GEN" -p "$(cat "$OUT/p-wordcap.txt")"  -o "$OUT" -x "eval-wordcap"  -n 2 -w 4 > "$OUT/wordcap.log" 2>&1 ) &

wait

echo "=== TALLY $(date +%H:%M:%S) ==="
FAILED=0
for c in dense people relation wordcap; do
  n=$(ls "$OUT/eval-$c"-*.png 2>/dev/null | wc -l | tr -d ' ')
  echo "eval-$c: $n"
  if [ "$n" = "0" ]; then
    FAILED=1
    echo "  --- log ---"
    tail -5 "$OUT/$c.log"
  fi
done

echo
echo "Generation check: $([ "$FAILED" = "0" ] && echo PASS || echo FAIL)"
echo "Now inspect the images by eye against the four criteria:"
echo "  dense    — one simple diagram, NOT a summary of the pasted section"
echo "  people   — no characters/faces/robots despite the prompt naming people"
echo "  relation — clean baseline, one focal point"
echo "  wordcap  — visibly tighter text than the default budget"
exit $FAILED