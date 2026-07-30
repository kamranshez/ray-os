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

**Most valuable, but unranked: `entry-point-tracer`.** Enumerate every entry point (it found 88),
trace each hop by hop, and inspect the *joints between layers* rather than the layers. It reached
a class of cross-*system* seam defect (code versus Stripe, code versus Vercel's deploy ordering)
that a file-reading strategy cannot see by construction, and that is a real and distinctive
result. Its *rank* is not supported: see Caveats. It originally held first place on a count that
nobody audited and that was never graded on the shared ladder.

**Best on evidence, and the one result compute cannot inflate: `hostile-input-hunter`.** See
below. Given that confirmed-count turns out to correlate with compute spent at r=+0.82 while
proof-count does not correlate with it at significance, this is the entrant whose placement rests
on the soundest axis in the table.

**`hostile-input-hunter`.** Every one of its 20 confirmed findings carried an executable repro,
the only clean sweep in the field. Wins on evidence quality, loses on ceiling: you cannot fuzz
your way to "the reservation and the charge disagree about what a minute is."

**Third, and the run's biggest scoring casualty: `concurrency-hunter`.** 12 confirmed findings
on only 6 subagents, originally published as 3 because a transport failure ate its subagents'
results. It reached ~150 files with one broad mapper plus five narrow lenses, matching the
15-agent entrant's coverage, which is the clearest evidence in the run that fan-out *shape*
beats fan-out *count*.

**Worst: `mutation-survivor-hunter`.** Zero confirmed. Its thesis presupposes a test suite this
codebase lacks where it matters, so a surviving mutant carries no information and the signal
collapses. Ranked last on *fit*, not conduct: it executed cleanly and reported its own dry run
honestly rather than padding the scorecard. It also produced the run's most alarming single
result, which no scoring axis here could score — all 7 of its surviving mutants are money or
authorization enforcement points that the suite executes but never asserts on.

The practical recommendation is to keep **three**, not two, and to pick them for the axes they
cover rather than for their ranks: `entry-point-tracer` for cross-system seams, which nothing
else reached; `hostile-input-hunter` for executable proof, the one axis compute cannot inflate;
and `concurrency-hunter` for defects that need two things to happen at once, a class no amount
of careful reading finds. They fail in genuinely different directions and their overlap was low.

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
those two hunters' work, since both were stopped before writing their reports.
`invariant-hunter/own-sweeps-I1-I8/` holds its first eight sweeps, recovered on 2026-07-30 from
an ephemeral tmp scratchpad that would have been garbage-collected; they are the richest single
seam of unsynthesised findings in the archive and they were very nearly lost. The `verifiers/`
folder is where the inverted ladder did its job and several findings were downgraded or
overturned, though note it adjudicates one hunter's candidates only, so "the ladder worked"
generalises from that plus self-reports rather than from a clean sweep of all ten.

## Caveats

Two hunters (`entry-point-tracer`, `invariant-hunter`) never got their synthesis pass, so
their scorecard rows are reconstructed from subagent returns rather than self-reported.

**Corrected 2026-07-30.** Re-checking every row against the scorecard each hunter wrote at the
top of its own report turned up three errors, one of them material. `concurrency-hunter` was
published at 3 confirmed and is actually **12**, moving it from 7th to 3rd; a transport failure
had swallowed its six lens agents' results, and the scorecard was taken from the partial report
it wrote before recovering them. `mutation-survivor-hunter` is 0/3/7/20/4, not 0/1/6/15/3, and
`git-signal-hunter` proved 5 findings rather than 6. Details in `results/meta-analysis.md`.

That correction changes the reading of the experiment, not just the table. The run had
penalised a hunter for harness flakiness and presented it as a fact about its strategy, and
"concurrency bugs were rare in this codebase" was an artifact of the error rather than an
observation. They are not rare; they are the densest cluster in the run.

**The declared winner is not defensible and should be read as unranked.** `entry-point-tracer`'s
`~40` is the largest number in the table, no independent read of it exists, and it was assigned
by me to prose that was never graded on the shared ladder — none of its 13 subagent prompts
mention REFUTED or PLAUSIBLE, and its traces self-grade `confidence: high` instead. Two further
claims failed on checking: its redirect-loop lockout was independently found by
`invariant-hunter`'s I8 sweep at the same file and line, and the "highest unique-finding count"
was never tabulated by anyone. What survives is narrower and still worth keeping the strategy
for: entry-point tracing reached a class of cross-*system* seam defect that nothing else here
reached.

A correction published earlier in this note was itself wrong and is withdrawn: `invariant-hunter`
was *not* over-credited with other hunters' candidates. I1-I8 are its own sweeps, each candidate
carrying an explicit ownership tag, and what looked like misattribution was convergence. Its real
error is the agent count, which is at least 19 rather than 14.

**Ranks 5 to 10 are partly a resource-race outcome.** All ten hunters drew on one shared 20-slot
subagent pool while the four largest fan-outs alone wanted about 55. `oracle-hunter` lost its
entire verification wave, `subsystem-auditor` lost an angle and all but one verifier,
`spec-gap-hunter` received zero subagent output (which is the real cause of the synthesis failure
I attributed to it), and `mutation-survivor-hunter` had three spawns rejected outright. Read the
bottom half as one-directionally understated.

The findings themselves are about a live product. They were produced read-only, with no
network side effects and no production calls, and none of them have been fixed or filed yet.
The convergence index is the triage order.

Related: [[decision-surfaces]]
