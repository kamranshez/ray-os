---
tags: [agentic-coding, multi-agent, handoffs, filesystem]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
status: "idea"
---

## What this video covers

How to pass context between workers without losing it. Specifically: structured handoff documents written to the filesystem at every worker boundary, recording what was completed, what wasn't, what commands ran, and what issues turned up. This is the unglamorous load-bearing piece that lets multi-day missions stay coherent.

## Why this matters

Validation catches bugs. Handoffs catch drift. Different problems, both fatal if ignored.

> "For a system that runs for many days, you also need to make sure that context isn't lost between the agents."

The temptation is to just pass the previous agent's transcript to the next agent. That's the failure mode this whole pattern exists to prevent.

## Sub-chapter 1: "I'm done" is not a handoff

The bad pattern: worker finishes, says "feature complete," next worker starts with nothing but the codebase diff.

> "When a worker finishes a feature, it doesn't just say, 'I'm done.' It fills out a structured handoff."

If the only artifact is the diff, the next worker rediscovers everything: which approaches were tried and rejected, which commands failed, which tests are flaky, which assumptions the previous worker made about the orchestrator's procedures. That rediscovery is where drift compounds.

## Sub-chapter 2: What goes into a handoff

Luke lists the fields explicitly:

> "Detailing what was completed, what was left undone, what commands were run throughout that agent loop, and what were the exit codes of those commands. What issues were discovered and did it abide by the procedures that the orchestrator defined for that worker."

Six things, every time:
- **Completed work.** Not the diff, the *list of intended outcomes that were achieved.*
- **Undone work.** What the worker tried and didn't finish, or chose to defer.
- **Commands run.** The exact shell commands or tool calls.
- **Exit codes.** Whether each command succeeded. Critical for distinguishing "I ran the tests" from "I ran the tests and they passed."
- **Issues discovered.** Surprises, broken invariants, things downstream workers should know.
- **Procedure adherence.** Did the worker follow the orchestrator's defined procedures? If not, why?

The exit code field is the one most people skip. Don't.

## Sub-chapter 3: Why filesystem, not main context

Handoffs go in files. Not the orchestrator's context, not a follow-up message.

Reasons:
- **Survives compaction.** Long missions blow through context windows. Files don't compact.
- **Survives crashes.** If a worker dies mid-task, the previous handoffs are still on disk.
- **Auditable.** You can `git log` the handoffs alongside the code. The mission becomes inspectable after the fact.
- **Cheap to read selectively.** A worker can grep for "exit code != 0" across all prior handoffs without loading them all.

This is the pattern of "filesystem is shared state." The orchestrator coordinates, but the truth lives on disk.

## Sub-chapter 4: Self-healing at milestone boundaries

Structured handoffs aren't just bookkeeping. They're the mechanism by which the system corrects course.

> "That's how we catch issues and how the system self-heals. The errors get caught at milestone boundaries. Corrective work gets scoped and the mission sort of pulls itself back on track."

The orchestrator reads the handoffs at each milestone. If a worker reported undone items, the orchestrator scopes a follow-up feature. If a worker reported a discovered issue, the orchestrator decides whether to fix it now or defer.

> "Not by hoping that agents remember what happened, but by forcing them to write it down and then actually address issues."

That second clause is the load-bearing one. Writing things down is necessary but insufficient. The orchestrator has to actually consume the handoffs and act on them. A handoff log nobody reads is just an expensive form of journaling.

## Sub-chapter 5: Block progress on unaddressed issues

The discipline that makes this work: don't let the next worker start until prior handoff issues are addressed or explicitly deferred.

> "Stuff like running validation and ensuring that progress is blocked when there are some handoff issues that are not addressed."

This is what stops drift. A worker reports "I couldn't get the tests to pass on this module." If the next worker starts anyway, two features later you have a codebase nobody can run. If the orchestrator blocks progress, the issue gets scoped and resolved before it compounds.

## Sub-chapter 6: What this looks like on disk

Concrete: missions stores handoffs in `handoffs.jsonl` (per the architecture diagram). One JSON object per worker, append-only.

Co-located in shared state alongside `features.json` and `validation-contract.md`. The orchestrator reads all three to make decisions. Workers write their own handoff entry and read previous ones as needed.

The file system is the bus. Agents are the writers. The orchestrator is the conductor.

## Talking points for filming

- "I'm done" vs the six-field handoff: lead with the contrast
- Emphasize exit codes specifically (most-skipped field)
- Filesystem-as-shared-state is the through-line
- End on self-healing: handoffs aren't reports, they're how the mission stays on track

## Key takeaway

Structured filesystem handoffs convert agent communication from hopeful into auditable, making self-healing possible at every milestone.
