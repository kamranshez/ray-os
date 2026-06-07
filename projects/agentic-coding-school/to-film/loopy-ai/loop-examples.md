---
tags: [loopy-ai, class, examples]
aliases: [Loop Examples, Loop Patterns In The Wild]
date: 2026-06-07
status: draft
---

## Why this note exists

The taxonomy in [[loop-stack]] is abstract. This note grounds it in concrete loops, mostly from Ray's own stack, so the class can show real instances of L2 through L6 rather than hand-waving.

Each example below names the level, the boundary, and (most importantly) **what the engineering actually is**. The prompt is rarely the hard part. The control surface around the prompt is the work.

## L2 / L3 examples (loop design as craft)

### Self-tuning PR review loop

Every PR gets a review agent. It only posts findings above confidence X. Track which findings humans dismiss vs accept. If dismiss rate > 50% over the last 20 reviews, raise X. If accept rate is 95%+, lower X to catch more.

The loop tunes its own pickiness against human signal.

The skill is closing the feedback loop *on the loop itself*. Most people forget to instrument this and end up with loops that drift quietly until someone notices the noise.

### On-call triage pre-empter

When an alert fires, spawn an agent that pulls relevant logs, correlates with deploys in the last 6h, posts a triage comment **before the human reads the page**.

Hard constraints:
- Never say "I think it's fixed." Only describe what it found.
- Latency budget: 90 seconds, otherwise stay silent.
- False-positive cost is high (wrong diagnosis wastes oncall trust), so the loop is engineered around restraint.

The skill is knowing what the loop must *not* do.

### Closing-the-loop (the canonical L2)

Already covered in [[closing-the-loop]] and the filmed ACS video. Build -> test -> fix -> test. The lesson here is that this is the smallest unit of "real" loop and almost every higher-level loop nests one of these.

## L4 examples (continuous workers)

### Sentence-mining auto-feeder

Already partly built (see `~/.claude/skills/sentence-mining/`). Bank mode takes a target word list and processes it without further instruction. Promote it from "skill I invoke" to L4 by:
- Triggering automatically on a target word list file change
- Capping output at 20 cards / day so review burden stays sane
- Skipping any word already in deck (dedup across runs)
- Posting a daily summary to Telegram with reject / accept rate

### Dependabot auto-merge worker

Watches the dependency-update PR queue. For each PR: run tests, run a regression heuristic, merge if green and the diff matches the "minor / patch" pattern. Escalate majors to human.

Engineering: the threshold for "safe to auto-merge" is the entire design. Get it wrong in one direction and you ship breaks; wrong in the other and the loop is useless.

## L5 examples (discovery / problem finders)

### YouTube outlier scout

6am daily: scan watchlist for videos > 3x channel median.

Sounds simple. The engineering is what's not in that sentence:
- Dedup against anything already filed (don't re-surface yesterday's winner)
- Skip topics already in the publish pipeline
- Cap output at 5 / day so it doesn't become noise
- Track which surfaced items got clicked, raise threshold if click rate drops below 30%
- Token budget capped at $2 / day. If exceeded, post a "budget hit, here's what I skipped" line. Never silently truncate.

This is the canonical L5: the agent is not making videos, it's deciding what should *become* a video.

### Content idea factory

Generates 50 ideas / week from Twitter, HN, GitHub trending, YouTube comments. Scores them. Surfaces top 5.

The hard part is the scoring rubric, not the generation:
- "Aligned with skills class" vs "viral potential" vs "would I enjoy making this" are three different loops
- Novelty vs repeat-what-works ratio
- Track which surfaced ideas got made vs discarded *and* which discarded ones blew up for other creators. That gap is measurable taste, possibly for the first time.

### Thumbnail A/B reactor

When a test concludes, pull the winner, infer *why* it won, generate 3 follow-up hypotheses for the next video.

Hard parts:
- Distinguishing "this won because of contrast" from "this won because the topic was hot." Opposite next moves.
- Knowing when to stop iterating on a winning pattern before it fatigues
- Which losing variants were "right idea, wrong execution" (re-test) vs "wrong idea" (abandon)

## L6 examples (governance, loop-of-loops)

### Fleet health monitor

A meta-loop watching every other loop you run:
- Kills any loop spending > 2x expected daily tokens
- Pages you if output quality (judged by another agent against last week's baseline) drops 20%
- Lists loops that haven't surfaced anything actionable in 7 days as "candidates to retire"
- Weekly digest: total spend, per-loop cost, per-loop yield (in actions taken)

This is the org chart for the fleet. Once 20+ loops are running, this *becomes* the actual job.

### Loop discoverer

Watches your own behaviour over a week. Proposes new loops: "You manually triaged Slack DMs 12 times this week, want a loop?"

The taste question: when is a recurring task worth automating vs enjoyed manually? Not every repeat is a candidate for a loop. Some things you do because doing them keeps you close to the thing.

## Class arc through the examples

Open with closing-the-loop (familiar, L2). Then sentence-mining as an L4 they have probably seen. Then YouTube outlier scout as the L5 "aha" moment, because that's where the role of the human visibly changes. Close with fleet health monitor (L6) to make the "you need to govern this" point land before it becomes a fire.

The throughline: **the prompt is the easy part at every level. Budgets, thresholds, dedup, kill-switches, self-tuning, restraint, retirement, these are where the work lives.**

See also: [[loop-design-as-craft]] for the deeper "taste relocates" argument that all these examples are evidence for.
