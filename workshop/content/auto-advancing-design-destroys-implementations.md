---
tags: [agentic-coding, design-process, ticket-writing]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Auto-advancing through design without reading guarantees compounding mistakes

## The idea
You can auto-advance the research and questions phases. You cannot auto-advance the design discussion. The design doc is roughly 200 lines of spec that turns into thousands of lines of code. One wrong line in the spec creates "two possible truths" the model can drift toward at any downstream step. That drift is unrecoverable at human-review speed because Claude writes code faster than you can read it. The design doc is your last deterministic checkpoint — skip reading it and you're rolling dice on a thousand-line implementation.

## Why this is the chokepoint
- Ambiguity in the spec → model drift during implementation
- Drift compounds: each subsequent decision branches on the wrong premise
- You cannot keep up with code-generation speed during implementation
- Once code is written wrong, your only recovery is nuking the branch
- Therefore the only place to stop drift is *before* code generation begins

## How to apply
- Auto-advance research and questions; pause at design
- Read the entire design doc end-to-end, not skim
- When you skim, flag every "this feels wrong" and resolve it before proceeding
- Eliminate "unknown" placeholders from the doc — they become drift seeds
- If something feels uncertain, *remove* it from the doc rather than commit a half-baked version (Dex's principle)
- The reread takes 12-30 minutes; a bad implementation costs hours of recovery

## Surrounding context
Vibhav: "I have to deterministically know that it's correct. That's my last check." He physically reads the entire ticket and design discussion, often disappearing for 20-30 minutes. The Riptide tool offers an "auto-advance through design" mode but he refuses to use it — and they joked about gating it behind "100 sessions completed" because it's so dangerous. The closures feature (16k lines, 36 hours) only worked because the design pass caught everything before code generation.

The compounding logic: 200 lines of spec × ambiguity = thousands of drifted lines. The leverage is enormous in both directions.

## Open questions to explore
- What's a checklist for "is this design doc actually ready to ship"?
- Can you train a model to find ambiguity in design docs better than humans?
- Is there value in a second-pair-of-eyes reviewer (human or model) before implementation?
- How do you teach the discipline of "remove uncertain sections" vs. "fill in placeholder"?
- What's the right cadence for full-read vs. diff-read of evolving design docs?
