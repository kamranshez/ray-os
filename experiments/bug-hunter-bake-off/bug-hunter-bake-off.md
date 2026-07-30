---
tags: [experiment, bug-hunting, skills, evaluation, agentic-coding]
aliases: [bug-hunter-bake-off, 10-way bug hunter comparison]
date: 2026-07-29
---

Ten independently designed bug-hunting skills, run in parallel against the same real
codebase, under identical rules, each spawning its own nested subagents. Roughly 85 agents
total on Opus 5.

The point was not to find bugs in HyperWhisper. It was to answer a methodological question:
**when there is no diff to anchor on, which hunting strategy actually finds real defects?**
The bugs are the measuring instrument, not the product.

## Why this experiment exists

Code review tooling is overwhelmingly diff-shaped, and that shape carries a hidden
assumption: the interesting defects are in what just changed. Off-diff, on a codebase that
already exists, that assumption breaks and two new problems appear.

- **The recall bias inverts.** On a diff, guessing generously is correct, since the change
  is small and a false positive costs one comment. On a whole codebase, generous guessing
  produces unbounded plausible-looking findings, and 200 maybes is indistinguishable from
  noise.
- **Coverage stops being self-bounding.** A diff tells you where it ends. A codebase does
  not, so every claim has to be paired with what was *not* examined, or "we looked at 14
  files" silently reads as "the codebase is clean."

So the ten skills were written to attack the same problem from ten different angles, and
this run is the head-to-head.

## The answer

**Best: `entry-point-tracer`.** Enumerate every entry point (it found 88), trace each hop by
hop, and inspect the *joints between layers* rather than the layers. It produced the two most
severe findings in the run and the highest unique-finding count, and several of its findings
are cross-*system* seams (code versus Stripe, code versus Vercel's deploy ordering) that a
file-reading strategy cannot see by construction.

**Runner-up: `hostile-input-hunter`.** The only 100% proof rate in the field, 20 of 20. Wins
on evidence quality, loses on ceiling: you cannot fuzz your way to "the reservation and the
charge disagree about what a minute is."

**Worst: `mutation-survivor-hunter`.** Zero confirmed. Its thesis presupposes a test suite
this codebase lacks where it matters, so every mutant survives and the signal is uniformly
zero. Ranked last on *fit*, not conduct: it executed cleanly and reported its own dry run
honestly rather than padding the scorecard.

The practical recommendation is to keep the top two **as a pair**. They fail in opposite
directions, one producing architectural arguments and the other executable demonstrations,
and their overlap was low.

## What transferred beyond the ranking

- **The inverted ladder is the load-bearing idea.** Default verdict REFUTED; CONFIRMED
  requires a named file, line, caller, and a reaching input. Verifiers killed a large share
  of what finders proposed, including several compelling-looking ones: a "dead" validator
  that was live, a Stripe version mismatch that was a typing artifact, a credit bug whose
  exposure proved bounded and self-correcting. Under diff-review defaults every one of those
  ships as a comment.
- **Convergence is the best available proof.** The `sanitizeReturnTo` open redirect was found
  four times by four unrelated strategies, each verifying it by *running* the URL parser. The
  `/usage` cache-poisoning was found six times. Independent rediscovery beats any single
  agent's confidence rating.
- **Coverage honesty predicted quality better than volume did.** The strategies worth trusting
  turned out to be the ones whose refuted lists were longer than their candidate lists.
- **Synthesis is a real stage, not a formality.** `spec-gap-hunter` initially reported 2
  findings while its own subagents had returned far more, and `oracle-hunter`'s finished
  report beat my reconstruction of it from its raw subagent returns. Fan-out is not the
  hard part; folding the results back in is.

## Layout

| Path | What it holds |
|---|---|
| `bake-off-comparison.html` | The visual comparison. Open this first. |
| `results/meta-analysis.md` | Full write-up: scoring, convergence index, pros and cons of all ten. |
| `results/reports/` | The 8 hunters that wrote their own reports, verbatim. |
| `method/shared-brief.md` | Rules of engagement every hunter read first. This is the control. |
| `method/scope-files.txt` | The 210-file arena, the denominator for every coverage claim. |
| `skills-under-test/` | The 10 `SKILL.md` files being compared. |
| `raw-subagent-output/` | 34 nested-subagent returns, renamed from task hashes. |

`raw-subagent-output/entry-point-tracer/` and `.../invariant-hunter/` are the only record of
those two hunters' work, since both were stopped before writing their reports. The
`verifiers/` folder is worth reading on its own: it is where the inverted ladder actually
did its job, and where several findings were downgraded or overturned.

## Caveats

Two hunters (`entry-point-tracer`, `invariant-hunter`) never got their synthesis pass, so
their scorecard rows are reconstructed from subagent returns rather than self-reported. The
top spot is safe by a wide enough margin, but the middle of the table could reorder on a
clean rerun.

The findings themselves are about a live product. They were produced read-only, with no
network side effects and no production calls, and none of them have been fixed or filed yet.
The convergence index is the triage order.

Related: [[decision-surfaces]]
