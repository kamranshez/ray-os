---
tags: [agentic-coding, multi-agent, parallelism, coordination]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
status: "idea"
---

## What this video covers

The intuition that ten agents in parallel give you ten times the throughput is wrong for software tasks. This video explains why parallel coding agents conflict, why sequential execution with targeted internal parallelization wins, and where parallelism actually does pay off.

## Why this matters

Most people, the first time they hit a coding task that's too big for one agent, reach for parallelism. It feels like the obvious move. Luke's team tried it and found the opposite.

> "If you have 10 agents running at one point in time, then you have 10 times the throughput. But we tried that and it doesn't really work for tasks in the like software dev domain because agents conflict."

If you're going to run agents for hours, the error rate matters more than the wall-clock speedup. This video is about when to favor which.

## Sub-chapter 1: The intuition that fails

Run ten agents, get ten times the work done. Clean math, broken in practice.

> "Agents conflict. They step on each other's changes. They duplicate work. They make inconsistent architectural decisions."

Three failure modes from one sentence:
- **Stepping on each other's changes.** Agent A renames a function, Agent B is mid-flight using the old name.
- **Duplicating work.** Two agents independently solve the same subproblem two different ways.
- **Inconsistent architectural decisions.** Four agents each pick a different state-management approach for adjacent modules.

> "The coordination overhead ends up eating up the speed gains all the while you're burning tokens."

You spent the tokens. You did not get the speedup.

## Sub-chapter 2: Sequential with internal parallelization

Missions runs features serially. One worker or one validator at a time at the feature level.

> "There's only one worker or validator running at any given point in time."

But within a feature, parallelization is allowed for one specific class of operation: readonly.

> "Within a feature, we allow for parallelization on readonly operations. So you have something like searching through the codebase or researching APIs. All that gets parallelized."

The split is the whole insight: writes are serial, reads are parallel.

## Sub-chapter 3: Why readonly is safe

Readonly operations do not touch shared state. Two agents can search the codebase simultaneously and neither one's result invalidates the other's.

The same holds inside validators. Code review is readonly. You can spawn dedicated reviewer agents per feature in parallel without any of them stepping on each other.

> "Within validators, we also parallelize readonly operations such as code review."

This is the pattern: aggressive parallelism on the read side, strict serialization on the write side.

## Sub-chapter 4: The error rate trade

Sequential is slower on a single feature. But error rate compounds.

> "It seems slower on paper, but the error rate drops dramatically. And when you have tasks that run for many days, the correctness compounds."

A 5% error rate on each of ten parallel features is not 5% overall. The errors interact: feature B's bug surfaces because feature A made a conflicting assumption. Sequential keeps the codebase coherent feature by feature, so each new worker inherits a working baseline.

This is the real argument for going serial. Not "parallelism is bad" but "parallelism corrupts the substrate that the next agent works on."

## Sub-chapter 5: When parallel does work

Parallel works when:
- The agents touch disjoint state (different repos, different services, different files)
- The work is readonly (research, search, code review, evaluation)
- A coordinator merges results before any state is mutated

Parallel breaks when:
- Multiple agents write to the same codebase
- Architectural choices need to be consistent across the work
- Failures in one branch invalidate assumptions in another

If you can't put your task in the first list cleanly, default to sequential.

## Sub-chapter 6: Handoffs make sequential viable

The reason sequential doesn't lose context is that each worker writes a structured handoff before the next one starts. That's the next video. Without handoffs, sequential agents are just one agent over and over with amnesia. With handoffs, sequential agents are a relay race.

## Talking points for filming

- Lead with the failed intuition, name the three conflict modes
- The "writes serial, reads parallel" line is the soundbite
- Hammer the error-rate-compounds point for long-running missions
- Tease handoffs as the thing that makes sequential workable

## Key takeaway

Run features serially and parallelize only readonly work; the error rate drops dramatically as runs lengthen.
