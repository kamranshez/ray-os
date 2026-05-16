---
status: stub
acs: []
mapping: workshop-original
day: 4
block: deep-cut
recording-needed: true
---

## The idea

Steal Roblox's playbook: teach the agent to think like the team's senior engineers by mining the PR review history that team has already produced. Not a new model, not a fancier prompt — institutional memory turned into automated guardrails.

Roblox went from ~30% to over 60% AI suggestion acceptance across a 10,000-PR set, and pushed an agentic cleanup project from 46% to over 90% accuracy. The unlock wasn't capability. It was context.

Source: https://about.roblox.com/newsroom/2026/01/doubled-ai-code-acceptance-teaching-models-think-like-roblox-engineers

## Why this matters for the workshop

Most teams already have the raw material sitting in their git history:

- Years of merged PRs
- Thousands of code review comments where senior engineers explain *why* something is wrong
- Commit messages, design docs, post-incident write-ups

That corpus is where the team's actual standards live. CLAUDE.md files written from scratch are a guess at what those standards are. Mining the review history is the receipts.

## The pipeline (Roblox's version, generalized)

1. **Pull every code review comment** from the repo's history.
2. **Strip the noise** — drop praise, typo nits, "lgtm", anything non-actionable.
3. **Embed and cluster** the remaining comments to find recurring themes ("we always do X here", "never call Y in a loop", "this pattern is banned in service Z").
4. **LLM-refine each cluster** into a single reusable rule with the *what* and the *why*, plus citations to the original PR comments so the rule stays grounded.
5. **Rank candidates** by frequency × number of distinct reviewers who flagged it. Recurring + cross-reviewer = real norm, not personal preference.
6. **Have a human curate** the top candidates into a knowledge base — CLAUDE.md entries, skill rules, hook checks, whatever the harness supports.
7. **Run it forward**: every new agent task is checked against the curated rules.

The point is the **shape**: noisy human feedback → embedded → clustered → refined → ranked → curated → enforced.

## Negative signals are training data too

Roblox treats every rejected AI suggestion, failed refactor, and reverted merge as a high-value signal. They label it, embed it, and have the agent semantically search it before generating new output so it doesn't repeat the same mistake.

For us this means: when we reject one of Claude's suggestions, that rejection should be captured *with the reasoning*, not just thrown away. Build a "rejected patterns" index the agent searches before proposing changes.

## What the workshop deliverable could look like

A small tool that:

- Takes a GitHub repo
- Pulls the last N PRs and their review comments via the GitHub API
- Runs the cluster + refine + rank pipeline
- Outputs a draft `CLAUDE.md` (or a set of skill rules) full of *real* guardrails sourced from that repo's actual review history, each one citing the PR comments it came from

Then point the agent benchmark harness ([[agent-benchmark-harness]]) at it: replay old PRs with and without the mined rules, show the acceptance-rate delta. Roblox's claim becomes something the room can reproduce on their own repo in an hour.

## Pairs naturally with the benchmark harness

These two ideas are the same loop from different ends:

- This skill **generates** new agent-side context (mined exemplars).
- The benchmark harness **measures** whether that context actually helps.

Together they're a closed loop: mine → curate → benchmark → keep what wins.

## Open questions

- How many PRs do we need to mine before clusters are real signal? Roblox had 700K PRs over 3 years; most teams have far less.
- For solo creators / small repos, is there enough review history to mine? Probably need to fall back to commit messages + issue threads.
- Curation step is the bottleneck — can we make it a 10-minute weekly review instead of a one-time sprint?
- Does the rule format matter? Plain CLAUDE.md lines vs. structured skill rules vs. hook checks — which actually changes agent behavior most?
- How do rules decay? A norm from 2020 may not apply anymore. Auto-detect when a "rule" is being violated in recent merged PRs and flag it for re-review.

## Workshop framing

"You already wrote your team's coding standards. They're in your PR review comments. Let's extract them and turn them into something the agent actually obeys."

Live demo: pick a public repo on stage, run the pipeline on its last 200 PRs, show the top 10 mined rules with citations, drop them into a CLAUDE.md, and run the benchmark harness to show the lift.
