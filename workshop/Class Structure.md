A 7-day live workshop. Day 0 is async pre-work — install, basics, get-to-Quick-Build. Days 1–7 are the live curriculum. Structure follows option A1 (Layered, one concept per day, Skills and Automation each get their own day).

# Day 0 — Foundations & Setup *(async pre-work, not live)*
Self-paced videos people watch before Day 1 so live time isn't burned on installs.
- Install Claude Code (MacOS / Windows)
- Install Codex
- Terminal basics, Git basics
- [[Using the MCP]]
- A Quick Build — ship one thing end-to-end before Day 1

# Day 1 — Alignment
Getting agent + human pointed at the same target before any code runs.
- [[Spec Developer]]
- [[Status of Agents]]
- [[Prototypes as specs]]
- [[Glossaries]]
- [[auto-advancing-design-destroys-implementations]]
- [[models-drift-toward-two-possible-truths]]
- [[Missions]] + [[Defining Good Goals]] + [[goal]]  *(merge — see below)*

# Day 2 — Steering
Keeping the run on-rails. Long-context behaviour, intent drift, sycophancy.
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
- [[1M Context]]

# Day 4 — Skills
Encoding your taste so you don't have to repeat yourself.
- [[Off-distribution]]
- [[Markdown over architecture]]
- [[teach-models-to-think-like-your-engineers]]
- [[Creating Skills]]
- [[Types of Skills]]
- [[Forked Contexts for Skills]]
- [[Skills + Subagents]]

# Day 5 — Automation & Workflows
Removing yourself from the loop on everything that isn't taste.
- [[Workflows]]
- [[Every PR]]
- [[OpenAI Symphony]]
- [[Mermaid Diagram Generator]]
- [[Automate Anything and Everything]]
- [[Hooks]]
- [[Routines]]
- [[Remote Control]]

# Day 6 — Verification
Proving the agent stayed in shape.
- [[Languages]] + [[files-matter-less-in-agent-friendly-languages]]  *(merge)*
- [[Verification Architectures]]
- [[Verifying with Codex]]
- [[Adversial Reviewers]]
- [[agent-benchmark-harness]]
- [[security-review]]
- [[ultrareview]]

# Day 7 — Agent Teams & Loopy AI
Multi-agent systems and self-running loops.
- [[convergence-over-perfection-thesis]]
- [[01-solo-plus-cheap-verifier]]
- [[02-parallel-voters]]
- [[03-generator-plus-adversarial-critic]]
- [[04-decomposed-swarm-independent-errors]]
- [[05-environmental-attractors]]
- [[Ralph]]
- [[Autoresearch]]
- [[Removing Bottlenecks]]

---

# Merges

- **Goals trio** → merge [[Missions]], [[Defining Good Goals]], [[goal]] into one "Goals & Missions" note. Same atom, three angles.
- **Long-context trio** → merge [[long-context-demands-active-human-steering]], [[recent-context-dominates-attention]], [[long-context-inverts-dumb-zone-advice]] into one "How long context actually behaves" note.
- **Adversarial overlap** → [[Adversial Reviewers]] and [[03-generator-plus-adversarial-critic]] cover the same pattern. Keep the archetype version in Day 7; Day 6 links to it instead of duplicating.
- **Subagent overlap** → [[Subagent Architectures]] = *how to wire them*, [[Verification Architectures]] = *what to verify with them*. Split cleanly.
- **Languages pair** → merge [[Languages]] + [[files-matter-less-in-agent-friendly-languages]].

# Separations

- Skills (Day 4) and Verification (Day 6) get their own days instead of being collapsed together.
- Automation (Day 5) is its own day, not folded into Workflows or Loops.
- Agent Teams + Loopy AI share Day 7 but stay logically distinct sections.

# Open questions

- Is Day 5 (Automation) reachable before Day 6 (Verification)? Argument against: you automate things you can't yet trust. Argument for: most Day 5 automation is *humans-in-the-loop* (PR gates, scheduled runs to phone), so trust is less load-bearing.
- Day 7 packs 6 archetypes + 3 loop topics — may need to drop one or split if pacing dies.

# Pricing
See [[Pricing Structure]].
