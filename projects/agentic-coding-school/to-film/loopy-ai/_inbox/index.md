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

- [[autonomy-ladder]] — Aakash Gupta's "6 levels of autonomous Claude Code" (skip-permissions -> context mgmt -> subagents -> Ralph -> AutoResearch -> VPS/OpenClaw 24/7). Strongest progression for the class arc.
- [[codex-goal-vs-ralph]] — the "pre-decomposable vs unfolding work" decision tree. Reuse as the conceptual core.

## What's in this inbox

- [[sources-x]] — first batch of X links (title-pass notes + workshop stubs), fetched and summarised
- [[sources-x-batch2]] — second batch, surfaced by the body-level note sweep (incl. Daniel San taxonomy, Weinbach, the Intercom talk)
- [[autonomy-ladder]] — the 6-levels spine, broken out
- [[sources-notes]] — what the Apple Notes actually contained across both passes
- [[workshop-migration]] — the existing workshop Day 9 stubs and assets to pull into this class

## Candidate class outline

On-ramp (Aakash levels 1-3): skip permissions, context management (/clear, /compact), subagents for parallel context.

Core loops:
- Ralph Loops
- /goal (anatomy + the state machine)
- Writing Effective Goals (Avi Chawla's 9-section template; Weinbach's "anchor on a theoretical max" tip; Ray's WatchLLM goal as the worked example)
- Closing the Loop / Verification loops (steipete's /review loop, Playwright write-test-fix, cursor's quality-review skill)
- Autoresearch (eval-driven mutation)
- Missions

Going long (Aakash levels 5-6): overnight runs + guardrails (Bootoshi), VPS/tmux/OpenClaw 24/7, Slack as agent transport.

Cross-cutting: "give agents problems, not tasks" (Intercom), scratchpadding to survive context resets, workflows that reset the context window between phases.
