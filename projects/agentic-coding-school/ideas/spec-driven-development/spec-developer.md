---
class: "spec-driven-development"
status: "idea"
aliases: [spec-developer]
---

The human-facing interview skill that produces a spec before any code is written.

## Models drift toward two possible truths if specs contain ambiguity

When a spec contains ambiguity — two plausible interpretations of how something should work — the model sees both and picks one at every downstream decision point. The picks are independent. So at one step it commits to interpretation A; at the next step it commits to interpretation B. The implementation becomes internally inconsistent in ways the human can't catch at code-generation speed. The fix is not to "clarify both options" — it's to *eliminate the ambiguity entirely* by removing the uncertain sections from the spec.

### Why "clarify" doesn't work
- Even with both options described, the model still picks one per decision
- Adding more text increases ambiguity surface area
- The model has no global consistency mechanism across long generations

### Why "remove" works
- A missing section forces a design discussion to surface it
- The discussion produces a single committed answer
- That single answer goes into the spec and propagates consistently

### How to apply
- When reading a spec, flag every "unknown" or "TBD" or hand-wave
- Don't fill them in with placeholders — *delete them*
- Let them resurface as questions in the next design pass
- Vibhav's principle: "if I'm not sure how to do something, I'd rather not have a bad version in the ticket"
- The two-pass workflow: first spec → design discussion → spec-two with everything resolved

### Surrounding context
This came up when Vibhav and Dex were reviewing the testing-feature ticket. Vibhav saw "unknown" placeholders in the report-types section and flagged them: "I see unknowns, don't really like that." Dex's response: "remove the things you're unsure about so they don't come into the model as pre-baked decisions." The two-sentence-to-big-design-discussion pattern works specifically *because* removing uncertainty forces the discussion. If you fill it in with a guess, you've stolen the option to discuss it.

The deeper point: a 200-line spec with one ambiguity becomes thousands of drifted lines. The cost of one wrong line in the spec is asymmetric.

## Auto-advancing through design without reading guarantees compounding mistakes

You can auto-advance the research and questions phases. You cannot auto-advance the design discussion. The design doc is roughly 200 lines of spec that turns into thousands of lines of code. One wrong line in the spec creates "two possible truths" the model can drift toward at any downstream step. That drift is unrecoverable at human-review speed because Claude writes code faster than you can read it. The design doc is your last deterministic checkpoint — skip reading it and you're rolling dice on a thousand-line implementation.

### Why this is the chokepoint
- Ambiguity in the spec → model drift during implementation
- Drift compounds: each subsequent decision branches on the wrong premise
- You cannot keep up with code-generation speed during implementation
- Once code is written wrong, your only recovery is nuking the branch
- Therefore the only place to stop drift is *before* code generation begins

### How to apply
- Auto-advance research and questions; pause at design
- Read the entire design doc end-to-end, not skim
- When you skim, flag every "this feels wrong" and resolve it before proceeding
- Eliminate "unknown" placeholders from the doc — they become drift seeds
- If something feels uncertain, *remove* it from the doc rather than commit a half-baked version (Dex's principle)
- The reread takes 12-30 minutes; a bad implementation costs hours of recovery

### Surrounding context
Vibhav: "I have to deterministically know that it's correct. That's my last check." He physically reads the entire ticket and design discussion, often disappearing for 20-30 minutes. The Riptide tool offers an "auto-advance through design" mode but he refuses to use it — and they joked about gating it behind "100 sessions completed" because it's so dangerous. The closures feature (16k lines, 36 hours) only worked because the design pass caught everything before code generation.

The compounding logic: 200 lines of spec × ambiguity = thousands of drifted lines. The leverage is enormous in both directions.
