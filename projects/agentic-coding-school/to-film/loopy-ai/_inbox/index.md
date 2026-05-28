---
tags: [loopy-ai, class, inbox, research, agentic-coding-school]
aliases: [Loopy AI Inbox]
date: 2026-05-28
status: inbox
---

Gathered context for the new **Loopy AI** class. This replaces the old Day 9 "Loopy AI" block from the [[workshop]] (we are moving away from the workshop and folding this material into a standalone class).

## The thesis

Having AI run in **loops** to achieve better results and stay productive for longer on the tasks you actually care about. Instead of one prompt and one turn, you set an objective and let the agent keep working across turns, fresh contexts, or eval cycles until the goal is genuinely met, not just vibe-met.

Three families of loop sit under this:

1. **Ralph loops** — run the same prompt in a fresh context window over and over until done. Cheap, dumb, state lives in files on disk (`prd.json`, `progress.txt`, `AGENTS.md`). A *discipline* pattern: it works because you wrote the PRD and the quality gates up front.
2. **`/goal` (Codex) / goal mode** — keep the context alive, fight drift with structure. A state machine baked into the runtime: objective, optional token budget, auto-continuation between turns, a completion audit, and "budget exhaustion is not completion." An *infrastructure* pattern: the runtime owns the loop, the model can't cheat it.
3. **Autoresearch / eval-driven loops** — run a skill, score the output against binary evals, mutate the prompt, keep improvements. Karpathy-style. The loop optimises the *prompt*, not just the work.

Core framing already written up: [[codex-goal-vs-ralph]] (the "pre-decomposable vs unfolding work" decision tree). Reuse that as the spine.

## What's in this inbox

- [[sources-x]] — every X/Twitter link from Apple Notes plus the two from the workshop stubs, fetched and summarised
- [[sources-notes]] — what the Apple Notes actually contained (links, the WatchLLM goal example, screenshots)
- [[workshop-migration]] — the existing workshop Day 9 stubs and HTML assets to pull into this class

## Candidate class outline (rough, from workshop Day 9)

- Ralph Loops
- Closing the Loop
- Autoresearch
- /goal (anatomy + the state machine)
- Writing Effective Goals (the 9-section prompt template)
- Missions
- Overnight / long-running runs + guardrails (new, from Bootoshi)
- Loops for review (steipete's /review loop, cursor's quality-review skill)
