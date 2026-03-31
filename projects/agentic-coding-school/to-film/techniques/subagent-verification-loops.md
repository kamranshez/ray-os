# Subagent Verification Loops (Implement → Review → Resolve)

Formal 3-agent pipeline: Implementer writes code → Reviewer (fresh context, zero bias) evaluates output → Resolver fixes issues. Implementer is biased by sunk cost; reviewer catches what implementer missed.

Build as a skill ("agent-review") that spawns subagents for correctness, edge cases, simplification, security. Demo on a real codebase — find issues the original builder couldn't see. Academic peer review analogy.

Partially covered by "Avoiding Code Bias" video but deserves dedicated treatment as a formal pattern.

**Source:** Coverage gaps from competitor transcripts (2026-03-31)
**Class:** Techniques — Advanced Techniques
