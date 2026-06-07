---
tags: [loopy-ai, class, inbox, research, agentic-coding-school]
aliases: [Loopy AI Inbox]
date: 2026-05-28
status: inbox
---

Gathered context for the new **Loopy AI** class. This replaces the old Day 9 "Loopy AI" block from the [[workshop]] (we are moving away from the workshop and folding this material into a standalone class).

## The thesis

Having AI run in **loops** to achieve better results and stay productive for longer on the tasks you actually care about. Instead of one prompt and one turn, you set an objective and let the agent keep working across turns, fresh contexts, or eval cycles until the goal is genuinely met, not just vibe-met.

The unifying line (from Aakash Gupta's ladder): **the unlock at every level is the same, give the agent a way to verify its own work.**

A clean way to open (Daniel San's taxonomy): every loop is just a different answer to "what makes the agent take another turn?"
- **/goal** waits for an outcome
- **/loop** waits for the clock
- **Stop hooks** wait for your script
- **Normal chat** waits for you

Three families of loop sit under this:

1. **Ralph loops** — run the same prompt in a fresh context window over and over until done. State lives in files on disk (`prd.json`, `progress.txt`, `AGENTS.md`). A *discipline* pattern: it works because you wrote the PRD and the quality gates up front.
2. **`/goal` (Codex) / goal mode** — keep the context alive, fight drift with structure. A state machine in the runtime: objective, optional token budget, auto-continuation, a completion audit, "budget exhaustion is not completion." An *infrastructure* pattern: the runtime owns the loop, the model can't cheat it.
3. **Autoresearch / eval-driven loops** — run a skill, score against binary evals, mutate the prompt, keep improvements. Karpathy-style. The loop optimises the *prompt*, not just the work.

## Spine candidates

- [[autonomy-ladder]] — Aakash Gupta's "6 levels of autonomous Claude Code" (skip-permissions -> context mgmt -> subagents -> Ralph -> AutoResearch -> VPS/OpenClaw 24/7). Strongest *difficulty* progression for the class arc.
- [[loop-stack]] — the L0 to L7 *scope* taxonomy (inference, harness, builder/verifier, task lifecycle, worker, discovery, governance, strategic). Opens the class by giving people vocabulary to point at things precisely. Pairs with the autonomy ladder rather than competing.
- [[codex-goal-vs-ralph]] — the "pre-decomposable vs unfolding work" decision tree. Reuse as the conceptual core inside L3.
- [[loop-design-as-craft]] — closing argument: taste relocates from single judgments into rubrics. Use as the class outro.
- [[loop-examples]] — concrete L2 to L6 loops from Ray's own stack. Each major class segment can lean on one of these as the worked example.
- [[borrowed-verifiers]] — the unlock for any L2 / L3 loop: stop self-grading, hunt for an external oracle (React Doctor, Lighthouse, axe, Ahrefs, codex review, real CTR). Pairs with [[../automation/auto-research-for-non-technical-work]] which is the L4 / L5 version with experiment tables. Wire into CI so every commit is one iteration.

## What's in this inbox

- [[sources-x]] — first batch of X links (title-pass notes + workshop stubs), fetched and summarised
- [[sources-x-batch2]] — second batch, surfaced by the body-level note sweep (incl. Daniel San taxonomy, Weinbach, the Intercom talk)
- [[autonomy-ladder]] — the 6-levels spine, broken out
- [[sources-notes]] — what the Apple Notes actually contained across both passes
- [[workshop-migration]] — the existing workshop Day 9 stubs and assets to pull into this class

## Class outline (Structure D, locked 2026-06-07)

Restructured around two claims. One: idea #6 from the loop bank — teach verification and governance *before* the climb, not after. Two: each high-signal idea deserves its own segment, not a paragraph inside another script.

Two acts. The Climb teaches you to *build* loops. Compounding Loops teaches you to *improve* loops. Mission Command then teaches you to *run a fleet of them.*

**Chapter 1 — Setup**
1. [[../intro]] — Boris's "I write loops," the vocabulary trap
2. [[../loop-stack]] — L0 to L7 (the map, not the syllabus)
3. [[../strip-the-model-out]] — build a fully deterministic loop with cron + bash + a static rubric. No model. Hands-on opener so students separate loop-design from model-behaviour. (Idea #6.)

**Chapter 2 — Foundations** (verification and governance, before the climb)
4. [[../closing-the-loop]] — the L2 pattern. Builder, verifier, exit condition.
5. [[../borrowed-verifiers]] — external oracles. Three categories, the hunt, wiring it in, CI on every commit.
6. [[../adversarial-reviewer-skill]] — pair every creator skill with an attacker skill. The L2 building block of a Reflector. (Idea #2.)
7. [[../governance-primitives]] — token budgets, kill switches, action-log review, retirement rules. L6 fundamentals taught now so everything above can hang guardrails on them.
8. [[../architecting-the-loop]] — the interface layer. What tools the agent needs (perceive, act, check, remember, stop) before the prompt is even written. Voice-agent worked example. (New, from 2026-06-07 conversation.)

**Chapter 3 — The Climb** (with verifier + governance + interface already in hand)
9. [[../l1-essentials]] — skip permissions, context management, subagents. The on-ramp, compressed.
10. [[../ralph-loops]] — discipline pattern, fresh windows, PRD-driven.
11. [[../goal]] — runtime owns the state machine.
12. [[../writing-effective-goals]] — Avi's 9-section, Weinbach's theoretical-max anchor, WatchLLM example.
13. [[../autoresearch]] — eval-driven mutation, optimising the prompt itself.
14. [[../l4-workers]] — Stop hooks, queues, sentence-mining as worked example.
15. [[../l5-discovery]] — Boris's 200 Claudes, YouTube outlier scout, anomaly detection.

**Chapter 4 — Compounding Loops** (the second act)
16. [[../ace-three-role-split]] — Stanford ACE. Generator does, Reflector reviews, Curator updates the playbook. Taste files survive model swaps. (Idea #1.)
17. [[../bug-triage-loop]] — Rippling's pipeline. The highest-leverage loop because it compounds on every other loop. L4 + L5 + L2 composed. (Idea #3.)
18. [[../echo-chamber]] — the named failure mode of compounding loops. Exogenous signal injection and rubric drift detection as the two antidotes. (Idea #5.)
19. Also reference: [[../automation/auto-research-for-non-technical-work]] as the operator-grade L4/L5 version of borrowed-verifiers with experiment tables.

**Chapter 5 — Closing**
20. [[../mission-command]] — Auftragstaktik as the L7 operating model. Intent docs, not prompts. (Idea #4.)
21. [[../loop-design-as-craft]] — where taste went. Old taste in single judgments, new taste in rubrics. The terminal role is "loop curator for X."

Cross-cutting: "give agents problems, not tasks" (Intercom), scratchpadding to survive context resets, workflows that reset the context window between phases, Missions.

### Status

- Written: intro, loop-stack, borrowed-verifiers, loop-design-as-craft (4 of 21)
- Stubbed: everything else (17 of 21)
- Filming order: not yet decided. Suggested writing order for full scripts: strip-the-model-out → adversarial-reviewer-skill → governance-primitives → architecting-the-loop → closing-the-loop → ace-three-role-split → bug-triage-loop → echo-chamber → mission-command. Then the remaining Climb segments fill in.
