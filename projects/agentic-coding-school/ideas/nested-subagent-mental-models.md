---
status: "idea"
tags: [subagents, agents, mental-models, codex, claude-code]
date: 2026-05-08
---

Two complementary frames for thinking about nested subagent workflows. The full pattern catalog lives in `projects/agentic-coding-school/to-film/codex-app/nested-subagents.md`. This note captures the meta-frame those patterns hang off.

## The mechanical frame: subagents are functions, nesting is the call graph

A subagent is just a function call: take input, do work in a private scope, return a small answer to the caller. The whole tree is a call graph with parallelism layered on top.

This single frame explains every constraint that shows up in real workflows:

- **Siblings can't merge into a third layer.** Functions return to their caller, not to their siblings. There is no shared next stack frame where two children's outputs combine on their own. If you want results merged, the parent does it, or the parent spawns a fresh agent with the children's reports as input.
- **Depth past 2 or 3 hurts.** Deep call stacks are hard to reason about, in code or in agents. Same reason you flatten nested function calls during refactors.
- **The verifier is the killer pattern.** A verifier is a separate function call with a clean scope, like a unit test in a different file from the code it tests. Independence is what makes it useful.
- **Context isolation is the asset.** Each function has its own local variables. The parent's scope stays clean unless you explicitly forward the noise.
- **Compress on return.** Return values should be small. A function that returns its full local state pollutes the caller. A subagent that returns 4000 lines of log instead of "deploy failed at step 3, OOM" has not done its job.

## The strategic frame: spawning is committing to a decomposition

One level up from "agents are functions": **spawning a subagent is committing to a hypothesis about how the problem decomposes.**

Each pattern in the catalog is a named decomposition:

| Pattern | Decomposition |
|---|---|
| Map / Reduce / Verify | propose plus check |
| Divide and Conquer | spatial partition |
| Hypothesis Tree | candidate cause |
| Adversarial Pair | opposing perspective |
| Order Perturbation | attention frame (what gets read first) |
| Deploy with Embedded Debugger | happy path vs error path |
| Fallback Chain | source preference order |

The patterns aren't a menu of techniques to memorize. They're a checklist of decompositions to ask "is one of these the shape of my problem?" before spawning.

If you can't name the decomposition you're committing to, you're spawning on vibes.

## Two corollaries

**Compress on return.** Every subagent's job is to turn a big mess into a small clean answer. The whole tree is a cascade of compression. The deeper the tree, the more compression has to happen at each level for the root to receive something useful.

**Isolation is the point, not parallelism.** People reach for subagents because they want speed or specialization. Those are nice. The real asset is that the parent's context stays clean. If the parent ends up with all the child's tool noise anyway, you spent tokens for nothing.
