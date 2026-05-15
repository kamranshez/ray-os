A 5-day intensive built from the ACS material. Pre-work covers tooling; each day is one coherent mental model.

> [!note] Proposed structure — see [Merges](#merges) and [Open questions](#open-questions) at the bottom.

# Pre-work — Fundamentals
Short async videos before Day 1. Not a "day".
- Using Claude Code — basic commands; point at the rest of the class for depth
- Using Codex — basic commands; point at the rest of the class for depth
- [[Using the MCP]]

# Day 1 — Alignment
Getting the agent and the human pointed at the same target before any code runs.
- [[Spec Developer]]
- [[Status of Agents]]
- [[Prototypes as specs]]
- [[Glossaries]]
- [[auto-advancing-design-destroys-implementations]]
- [[models-drift-toward-two-possible-truths]]
- [[Missions]] + [[Defining Good Goals]] + [[goal]]  *(merge — see below)*

# Day 2 — Steering
Keeping the agent on-rails once it's running. Long-context behaviour, intent drift, sycophancy.
- [[sycophantic-models-suggestions-as-commands]]
- [[asking-for-options-preserves-judgment]]
- [[long-context-demands-active-human-steering]] + [[recent-context-dominates-attention]] + [[long-context-inverts-dumb-zone-advice]]  *(merge)*
- [[Rewinding]]
- [[Ordering]]
- [[Compaction]]

# Day 3 — Context Architecture
How context flows between sessions, subagents, and tools.
- [[Subagents]]
- [[Forked Subagents]]
- [[Subagent Architectures]]
- [[CLIs vs MCPs]]
- [[context-strategy-correlated-with-engagement]]
- [[Workflows]]

# Day 4 — Skills & Verification
Two halves of one idea: teach the model your shape (skills), then prove it stayed in shape (verification).

**Skills**
- [[Off-distribution]]
- [[Markdown over architecture]]
- [[teach-models-to-think-like-your-engineers]]
- [[Every PR]]
- [[Automate Anything and Everything]]

**Verification**
- [[Languages]] + [[files-matter-less-in-agent-friendly-languages]]  *(merge)*
- [[Verification Architectures]]
- [[Verifying with Codex]]
- [[Adversial Reviewers]]
- [[agent-benchmark-harness]]

# Day 5 — Agent Teams & Loopy AI
Multi-agent systems and self-running loops. The "what does this look like at scale" day.

**Agent Teams**
- [[convergence-over-perfection-thesis]]
- [[01-solo-plus-cheap-verifier]]
- [[02-parallel-voters]]
- [[03-generator-plus-adversarial-critic]]
- [[04-decomposed-swarm-independent-errors]]
- [[05-environmental-attractors]]

**Loopy AI**
- [[Autoresearch]]
- [[Ralph]]
- [[Removing Bottlenecks]]
- [[OpenAI Symphony]]
- [[Mermaid Diagram Generator]]

---

# Merges

- **Goals trio** → merge [[Missions]], [[Defining Good Goals]], [[goal]] into a single "Goals & Missions" note. All three are the same atom from different angles; splitting them dilutes the lesson.
- **Long-context trio** → merge [[long-context-demands-active-human-steering]], [[recent-context-dominates-attention]], [[long-context-inverts-dumb-zone-advice]] into one "How long context actually behaves" note.
- **Adversarial overlap** → [[Adversial Reviewers]] and [[03-generator-plus-adversarial-critic]] cover the same pattern. Keep the archetype version in Day 5 and have Day 4 link to it instead of duplicating.
- **Subagent overlap** → [[Subagent Architectures]] and [[Verification Architectures]] both describe orchestrator/critic shapes. Split cleanly: Subagent Architectures = *how to wire them*, Verification Architectures = *what to verify with them*.
- **Languages + agent-friendly languages** → merge [[Languages]] and [[files-matter-less-in-agent-friendly-languages]]. Same point: pick a language with strong verification + flat file layout.

# Separations

- **Pull Skills out of "Verifying"** — currently buried under Day Verifying in the old draft, but Skills is its own mental model and deserves equal weight on Day 4.
- **Agent Teams gets its own slot** — was implicit before. The 6 archetype notes + thesis are enough material for a full half-day.
- **Spec Developer ≠ Prototypes as specs** — related but distinct: spec developer is the human-facing interview, prototypes-as-specs is the artifact. Keep separate on Day 1.

# Open questions

- Should Day 3 (Context) come *before* Day 2 (Steering)? Steering relies on knowing what a context window is.
- Is Day 5 too packed? Could split into Day 5 = Agent Teams, Day 6 = Loopy AI for a 6-day class (justifies the $299 → $599 jump).
- `cohort-pivot-strategy.md` is meta/business, not class content — move out of `workshop/ideas/`.

# Pricing
See [[Pricing Structure]].
