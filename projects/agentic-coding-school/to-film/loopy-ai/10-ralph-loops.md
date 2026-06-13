---
duration: "12-16 min"
batch: 4
order: 10
batch_name: "L3 Task Lifecycle"
class: "loopy-ai"
chapter: "Ralph Loops"
aliases: [ralph-loops]
status: stub
---

Stub — the Ralph loop. Run the same prompt in a fresh context window over and over until the goal is met. Cheap, dumb, surprisingly effective.

State lives in files on disk (`prd.json`, `progress.txt`, `AGENTS.md`). A *discipline* pattern: it works because you wrote the PRD and the quality gates up front.

## Key beats

- The in-window versus out-of-window variants. When to compact versus when to restart.
- The "/goal contract" anatomy (commit a6c99c4) — anchor for what state has to survive a restart.
- Why fresh context beats long context for repetitive deliverables.
- Failure modes: drift in the PRD, brittle outer loop, unclear exit condition.

## Sources / refs

- Pairs with [[autoresearch]] (eval-driven variant), [[goal]] (runtime variant), [[writing-effective-goals]], [[architecting-the-loop]] (the interfaces the Ralph runner needs).
