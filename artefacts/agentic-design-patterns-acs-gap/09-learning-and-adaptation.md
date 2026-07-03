---
title: "Ch 09: Learning and Adaptation -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "09"
pattern: "Learning and Adaptation"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 09: Learning and Adaptation** - Antonio Gulli

> Three next-step (complement) videos: an autonomous benchmark-gated self-improving loop (SICA), an evolutionary code optimizer (OpenEvolve/AlphaEvolve), and an LLM overseer that kills stuck loops.

## The one idea worth a video

- **A coding agent can improve itself by editing its own tooling and keeping only the versions that score higher on a benchmark.** This is the chapter's headline (the SICA case study) and it subsumes "learning from experience", "archive of past versions", and "self-modification" into one film-able loop. VERDICT: 🔗 next-step video available (complements "Improving the Loop").
- **An evolutionary loop -> generate many code variants, score each with a fitness function, keep and mutate the winners -> discovers optimizations a single agent would not.** Distinct demo (population + generations, not self-editing), distinct slot. VERDICT: 🔗 next-step video available (complements "Quick Benchmarking").
- **An unattended loop needs a second LLM "overseer" watching its callgraph for stagnation and loops, with authority to halt it.** Distinct reliability demo, distinct "thing you can do after". VERDICT: 🔗 next-step video available (complements "Primitives of a Loop").

## Summary + counts

Agents improve autonomously via reinforcement, preference, and memory-based learning; SICA self-edits its code and AlphaEvolve evolves algorithms, both driven by benchmark-scored iteration.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - Benchmark-gated self-improving agent (SICA)
THE CLAIM: an agent equipped with only basic file/shell tools can autonomously edit its own codebase and get measurably better at coding benchmarks. WHY IT'S NON-OBVIOUS: the default mental model is that one agent trains another, or that improvement requires fine-tuning weights; SICA "acts as both the modifier and the modified entity", improving with no training paradigm at all. WHY IT'S TRUE / MECHANISM: (1) SICA keeps an archive of past versions plus their benchmark scores; (2) it selects the highest-scoring version using "a weighted formula considering success, time, and computational cost"; (3) that version edits its own tools, is re-benchmarked, and the result is appended to the archive - so selection pressure, not gradient descent, drives improvement. Concretely SICA evolved a plain file-overwrite tool into a "Smart Editor", then a "Diff-Enhanced Smart Editor" with AST-based diff minimization, and an "AST Symbol Locator" for navigation. WHAT IT GENERALIZES TO: Ray's world of Claude Code skills and slash-commands - point a loop at its own `.claude/skills` or agent scripts, run a benchmark, keep only edits that raise the score. HOW IT GOES WRONG: the chapter flags that getting the LLM to "propose novel, innovative, feasible" changes is hard (it stagnates), and self-editing needs Docker isolation because it runs shell commands.

### Spine 2 - Evolutionary code optimization (AlphaEvolve / OpenEvolve)
THE CLAIM: an LLM inside an evolutionary loop - generate variants, auto-evaluate, select, repeat for hundreds of iterations - discovers faster/novel code that a single prompt does not. WHY IT'S NON-OBVIOUS: we treat the model as a one-shot code generator; here the model is the mutation operator inside a population search, and the intelligence is in the outer loop. WHY IT'S TRUE / MECHANISM: (1) an ensemble generates a wide range of proposals (AlphaEvolve uses Gemini Flash for breadth, Pro for depth); (2) an automated evaluator scores each against predefined criteria; (3) scores feed selection, so good variants survive and get mutated. AlphaEvolve cut Google data-center compute 0.7%, sped a Gemini kernel 23%, and found a 4x4 complex matrix-mult using 48 scalar multiplications. WHAT IT GENERALIZES TO: OpenEvolve is an open-source, OpenAI-compatible clone with a five-line Python API (`evolve.run(iterations=1000)`) that evolves whole files - Ray can point it at a hot function with a timing evaluator and film the fitness curve climbing. HOW IT GOES WRONG: needs a cheap, gameable-resistant evaluator and many iterations (cost); a weak fitness function optimizes the wrong thing.

### Spine 3 - The asynchronous overseer
THE CLAIM: an autonomous agent should be watched by a second, concurrent LLM whose only job is to spot pathological behavior and stop it. WHY IT'S NON-OBVIOUS: reliability is usually framed as deterministic guards (token caps, timeouts); the chapter adds a *semantic* watcher that reasons about the trace. WHY IT'S TRUE / MECHANISM: (1) SICA's overseer "runs concurrently with the main agent"; (2) it receives "a callgraph and an event stream of LLM messages, tool calls, and responses"; (3) from that it detects loops, stagnation, or repeated work and can "intervene by sending notifications or even cancelling the agent's execution". A dumb timeout cannot tell productive work from a spin; an LLM reading the callgraph can. WHAT IT GENERALIZES TO: any Loopy-AI unattended run - a cheap Haiku overseer reads the main loop's log/session and kills it when it detects the same edit reverted three times. HOW IT GOES WRONG: overseer false-positives (halting good work) or misses subtle stalls; adds cost and latency.

## 🎬 Proposed ACS videos

### 1. Build a Self-Improving Skill Loop (Benchmark-Gated)
- **HOOK:** What if your Claude Code skill rewrote itself overnight and only kept the versions that scored higher?
- **THE PROMISE:** For loop-builders: a loop that edits its own tooling, benchmarks each version, and archives only improvements - so it gets better while you sleep.
- **THE SHAPE:** (1) pick a target skill + a scored benchmark (e.g. "pass this test suite in fewest tokens"); (2) archive current version + score; (3) loop: select best-scoring version, let it edit its own skill file, re-run benchmark, append to archive; (4) show the score climbing across generations like SICA's Smart Editor -> Diff Editor; (5) sandbox it in Docker because it runs shell.
- **SPINE:** Spine 1.
- **SLOT:** Loopy AI -> L3: Task Lifecycle (sits right after "Improving the Loop").
- **RELATIONSHIP:** 🔗 complements "Improving the Loop" by being its next step -> that video has a human compare improvement variants and apply feedback from completed sessions by hand; this removes the human, gates every edit on a benchmark score, and keeps a versioned archive so improvement is autonomous and reversible.
- **PROOF TO REUSE:** SICA "acts as both the modifier and the modified entity"; the "weighted formula considering success, time, and computational cost"; the Smart Editor -> Diff-Enhanced Smart Editor -> AST Symbol Locator progression; the Docker-isolation requirement.

### 2. Evolve Your Code with an LLM Fitness Loop (OpenEvolve)
- **HOOK:** One prompt writes one function. An evolutionary loop writes a thousand and keeps the fastest - here is how to run it.
- **THE PROMISE:** For devs with a hot function: point an evolve-and-score loop at it and let a fitness function discover an optimization you would not have written.
- **THE SHAPE:** (1) take a slow function + a timing/correctness evaluator; (2) wire OpenEvolve's `initial_program`, `evaluator.py`, `config.yaml`; (3) `evolve.run(iterations=1000)`; (4) watch the population's best score climb and diff the winner against your original; (5) discuss Flash-for-breadth / Pro-for-depth ensemble and where the evaluator can be gamed.
- **SPINE:** Spine 2.
- **SLOT:** Advanced Techniques -> new chapter "Evolutionary Optimization" (or Loopy AI L2, builder+verifier framing).
- **RELATIONSHIP:** 🔗 complements "Quick Benchmarking" by being its next step -> that video times a single proposed optimization to judge if it is worth it; this wraps benchmarking in a population + selection loop so the optimization is *discovered* automatically over generations, not hand-proposed once.
- **PROOF TO REUSE:** the OpenEvolve five-line snippet and `evolve.run(iterations=1000)`; AlphaEvolve's 0.7% datacenter and 23% Gemini-kernel wins; the 4x4 complex matrix-mult in 48 multiplications; "evolve entire code files, rather than being limited to single functions".

### 3. Add an Overseer That Kills Your Stuck Loops
- **HOOK:** Your unattended agent has been reverting the same file for an hour. A timeout won't catch it - a second LLM will.
- **THE PROMISE:** For anyone running unattended loops: a cheap overseer that reads the main agent's trace and halts it on stagnation, before it burns your budget.
- **THE SHAPE:** (1) run a main Loopy-AI loop; (2) spawn a concurrent Haiku overseer that periodically reads the session log / callgraph; (3) give it a rubric for "loop, stagnation, repeated work"; (4) let it notify or cancel the run; (5) contrast with deterministic token/time caps and show a case each guard catches.
- **SPINE:** Spine 3.
- **SLOT:** Loopy AI -> L1/reliability (next to "Primitives of a Loop").
- **RELATIONSHIP:** 🔗 complements "Primitives of a Loop" by being its next step -> that video covers deterministic exit conditions and token/time caps; this adds a *semantic* guard - an LLM that reasons over the callgraph to catch pathological spins a fixed cap cannot distinguish from productive work.
- **PROOF TO REUSE:** SICA's overseer "runs concurrently with the main agent"; it receives "a callgraph and an event stream of LLM messages, tool calls, and responses"; it can "intervene by sending notifications or even cancelling the agent's execution".

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** Agents improve autonomously via reinforcement, preference, and memory-based learning; SICA self-edits its code and AlphaEvolve evolves algorithms, both driven by benchmark-scored iterative refinement.

**IDEAS:**
- Learning changes an agent's thinking, actions, or knowledge from new experience and data.
- Adaptation is the visible behavior change that results from that learning.
- Reinforcement learning rewards good outcomes and penalizes bad ones to learn optimal behavior.
- Supervised, unsupervised, few-shot, online, and memory-based learning each fit different agent needs.
- LLM agents adapt fast via few-shot and zero-shot prompting with minimal examples.
- PPO makes small clipped policy updates inside a trust region to avoid collapse.
- DPO aligns LLMs directly on preference data, skipping a separate reward model.
- Reward models can be "hacked" by the LLM to score bad responses highly.
- SICA is both the modifier and the modified - it edits its own source.
- SICA selects its highest-scoring past version by success, time, and compute cost.
- Self-improvement came as concrete tools: Smart Editor, Diff-Enhanced Editor, AST Symbol Locator.
- Sub-agents (coding, problem-solving, reasoning) decompose tasks and manage context length.
- An asynchronous overseer LLM watches the callgraph and can halt the agent.
- Context-window structure (system, core, assistant messages) drives efficiency and cost.
- AlphaEvolve pairs Gemini Flash (breadth) and Pro (depth) with an evaluator loop.
- OpenEvolve is an open-source evolutionary coder that evolves entire files.
- RAG can hold a dynamic knowledge base of proven strategies for adaptation.

**INSIGHTS:**
- Selection pressure over a versioned archive can replace gradient-based training for improvement.
- The intelligence in evolutionary coding lives in the outer scoring loop, not the model.
- Benchmark-scored archives make self-modification safe: bad edits simply are not selected.
- A semantic overseer catches failure modes deterministic timeouts and caps cannot distinguish.
- DPO's simplicity comes from collapsing a two-stage RL pipeline into one optimization.
- Self-editing agents demand sandboxing precisely because their power is running shell commands.
- Open-ended novelty (proposing genuinely new improvements) is the current bottleneck, not execution.
- Context-window organization is a first-class performance lever, not an afterthought.

**QUOTES:**
- "SICA acts as both the modifier and the modified entity, iteratively refining its code base." (Gulli)
- "This clipping acts like a safety brake, ensuring the agent doesn't take a huge, risky step that undoes its learning." (Gulli, on PPO)
- "DPO skips the reward model entirely... using a mathematical relationship that directly links preference data to the optimal policy." (Gulli)
- "The LLM might find a loophole and learn to 'hack' the reward model to get high scores for bad responses." (Gulli)
- "An asynchronous overseer, another LLM, monitors SICA's behavior, identifying potential issues such as loops or stagnation." (Gulli)
- "A key aspect of OpenEvolve is its capability to evolve entire code files, rather than being limited to single functions." (Gulli)

**HABITS/PRACTICES:**
- Keep an archive of past agent versions with benchmark scores; iterate from the best.
- Score improvements on a weighted formula: success, time, and computational cost.
- Run self-editing agents inside a dedicated Docker container for host isolation.
- Attach a concurrent overseer LLM to unattended runs to detect stagnation.
- Structure the context window deliberately (system / core / assistant) to cut cost.
- Record file changes as diffs and periodically consolidate them.

**FACTS:**
- AlphaEvolve reduced Google's global compute resource usage by 0.7%.
- AlphaEvolve gave a 23% speed improvement in a core Gemini-architecture kernel.
- AlphaEvolve found up to 32.5% optimization of low-level GPU FlashAttention instructions.
- AlphaEvolve found a 4x4 complex matrix multiplication using 48 scalar multiplications.
- AlphaEvolve rediscovered state-of-the-art on 75% of 50+ open problems, improved 20%.
- PPO paper: Schulman, Wolski, Dhariwal, Radford, Klimov (arXiv:1707.06347).
- SICA paper: Robeyns, Aitchison, Szummer, 2025 (arXiv:2504.15228v2).

**REFERENCES:**
- People: Antonio Gulli; Maxime Robeyns, Laurence Aitchison, Martin Szummer (SICA); John Schulman et al. (PPO).
- Algorithms/methods: PPO, DPO, reinforcement/supervised/unsupervised/online/memory-based learning, few-shot/zero-shot.
- Systems: SICA, AlphaEvolve (Google/Gemini Flash + Pro), OpenEvolve (codelion).
- Concepts/tools: reward model, AST parsing, Smart Editor, AST Symbol Locator, Docker, RAG, callgraph/event bus.
- Books: Sutton & Barto, Reinforcement Learning; Goodfellow et al., Deep Learning; Mitchell, Machine Learning.
- Repos: github.com/MaximeRobeyns/self_improving_coding_agent; github.com/codelion/openevolve.

**ONE-SENTENCE TAKEAWAY:** Agents get better by scoring their own attempts and keeping only what wins.

**RECOMMENDATIONS:**
- Clone OpenEvolve and evolve one slow function against a timing evaluator.
- Give an unattended loop a benchmark and a versioned archive of its tooling.
- Add a cheap overseer LLM to any long autonomous run you leave alone.
- Prefer DPO over PPO-plus-reward-model when aligning on preference data.
- Sandbox any self-editing or shell-running agent in Docker before trusting it.
- Read SICA's paper for a concrete self-improvement architecture with sub-agents.
