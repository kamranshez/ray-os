---
tags: [workshop, idea, benchmarking, devops, evals]
date: 2026-05-04
aliases: [context-layer-benchmark]
---

## The idea

A generic benchmarking harness for *agent-side* changes. Same shape as CI, but instead of "did the code still pass tests," it answers "did this change to the agent's environment make it better at real tasks from this repo's history."

The variable can be anything that lives outside the codebase but affects how the agent behaves:

- **Model version** — Opus 4.6 vs 4.7, Sonnet vs Opus, a new release the day it drops
- **Context layer** — adding/removing CLAUDE.md or AGENTS.md files, restructuring the hierarchy
- **Skills** — installing a new skill, changing a skill's description, removing one
- **Hooks** — a new pre-tool-use hook, a different stop hook
- **System prompt or harness settings** — permissions, allowed tools, defaults
- **MCP servers** — adding a new one, swapping providers

Everything else is held constant. The codebase, the task, the scoring rubric — all fixed.

## The loop

1. Pick a real PR from the project's history (or a real ticket from the backlog).
2. Check out the **parent commit** — the state of the repo right before the PR landed.
3. Run the agent on the task description under **configuration A** (e.g. current setup).
4. Reset, run the same agent on the same task under **configuration B** (e.g. older context layer, or older model, or no skill X).
5. Score both implementations against the human PR as ground truth.
6. Record the delta. Over many PRs, the deltas become signal.

The PR is the eval. The agent-side configuration is the variable.

## Why this is "DevOps for agents"

Right now, every change to a CLAUDE.md, every new skill, every model upgrade is a vibe-based decision. We *think* it helps. We don't actually know.

This harness turns those decisions into something with a feedback loop:

- **Regression detection** — did the new model get worse at our specific codebase? CI for model upgrades.
- **Justification** — when someone asks "is this CLAUDE.md actually helping," we can show the curve.
- **Tuning** — try five variants of a context layer, keep the one that scored highest.
- **Onboarding agents** — when a new model drops, run the harness before adopting it.

Same conceptual move as load testing or canary deploys, but for the agent layer of the stack.

## What "side by side" means

- Diff locality (did the agent edit the right files?)
- Tests from the PR pass/fail
- Hallucinated imports, missing deps, dead code
- Did it discover the convention the human used, or invent its own?
- Tokens and turns to reach a working answer
- Final score: LLM-as-judge against the human diff, plus the mechanical signals above

## Architecture sketch

- **Task corpus** — a list of `{ pr_url, parent_sha, task_description, scoring_artifacts }` per repo
- **Configurations** — named bundles: model, context-layer git ref, skill set, hooks, settings
- **Runner** — checks out parent_sha, applies a configuration, runs the agent, captures the diff and trace
- **Scorer** — runs PR's own tests on the agent's diff, then LLM-as-judge against the human PR
- **Report** — config-vs-config table across the corpus, plus per-task drilldown

## Open questions

- How big does the corpus need to be before deltas are signal vs. noise? Probably 10–20 PRs minimum.
- How do we keep the corpus fresh as the repo evolves? Auto-mine recent merged PRs?
- Cost ceiling — running 20 PRs × 5 configs gets expensive fast. Sampling strategy?
- Configuration "rollback" — git tag each context-layer revision? Separate branch? Snapshot the whole `.claude/` dir?
- Does the harness itself need to be model-agnostic, or do we lock the *judge* to one model so scores are comparable across runs?

## Workshop framing

Pick a volunteer's repo on stage. Mine 5 recent PRs. Run them through the harness with two configs — "their current setup" vs "stripped-down baseline." Show the gap live. The demo *is* the value prop.
