---
tags: [loopy-ai, inbox, sources, spine]
date: 2026-05-28
status: inbox
---

The single best spine candidate for the class, found on the second (body-level) Apple Notes pass in note "Auto research".

## Aakash Gupta — "6 levels of making Claude Code run autonomously"
https://x.com/aakashgupta/status/2035805431516246363 (275K views, Mar 22)

A clean difficulty ladder. Use it as the class progression; each rung is a segment.

- **Level 1 — Kill permission prompts.** `claude --dangerously-skip-permissions`. Stops the "can I edit this file?" interruptions.
- **Level 2 — Context window management.** 1M token window. `/clear` between tasks; `/compact` at ~60% usage instead of waiting for auto-compaction at 90% when the model is already forgetting instructions.
- **Level 3 — Subagents.** The reason it stops at 15 min is that everything shares one context window. Subagents run in separate contexts. A looping todo command runs each task in its own window; builds/tests/git never touch the main conversation. 2+ hours autonomous.
- **Level 4 — Ralph Wiggum loop.** Official Anthropic plugin. Claude works, tries to exit, a Stop hook blocks the exit and re-feeds the same prompt. Each iteration sees modified files + git history from previous runs. One dev: 27 hours straight, 84 tasks. Geoffrey Huntley ran one for three months and built a programming language with a working LLVM compiler.
- **Level 5 — Karpathy's AutoResearch.** Mar 7, a 630-line script, 100+ ML experiments overnight, 25K stars in five days. The difference from Ralph: structured **eval loops** — define a metric, run, measure, analyse failures, improve, repeat. One Claude Code port took accuracy 0.44 -> 0.78 R² across 22 autonomous experiments.
- **Level 6 — VPS + OpenClaw for 24/7.** Laptop lid closing kills everything; run Claude Code on a VPS inside tmux, detach, come back to a finished diff. OpenClaw (247K stars) goes further: a persistent gateway connecting LLMs to real tools 24/7 across messaging, email, git, calendars.

**The through-line (use as the class thesis):** "The unlock at every level is the same: give Claude a way to verify its own work."

This maps directly onto the existing [[codex-goal-vs-ralph]] framing and the loop taxonomy in [[sources-x-batch2]] (Daniel San). Levels 4-6 are the heart of "Loopy AI"; 1-3 are the on-ramp.
