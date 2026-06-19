---
status: "idea"
acs: []
mapping: workshop-original
day: 7
block: core
recording-needed: true
---
# Archetype 4: Decomposed Swarm with Independent Errors

## What This Video Covers

Instead of running one agent through a ten-step task, split the task so different agents handle independent sub-problems. The errors then stay local instead of compounding. One agent's 5% failure rate does not multiply across a chain of dependencies.

This is the archetype where sequential thinking hurts the most. The instinct is: "decompose into steps, execute in order." The better move is: "decompose into pieces that do not depend on each other, execute in parallel, merge at the end."

## Why This Matters

The math that justifies the archetype:

- One agent doing a 10-step sequential task at 95% per step → end-to-end accuracy ≈ 60%.
- Ten agents each doing an independent 1-step task at 95% each → you get 9.5 out of 10 correct, and you can identify which one failed and regenerate just that one.

Sequential errors compound multiplicatively. Parallel errors stay additive. That is the whole game.

From the retreat, on the mental block that stops this:

> "The first barrier to effective swarming is mental, not technical. Engineers trained in sequential decomposition struggle to conceptualize parallel agent work."

## The Pattern

```
           ┌────────────┐
           │   TASK     │
           └─────┬──────┘
                 │
         decompose into independent sub-tasks
                 │
     ┌───────────┼────────────┐
     ↓           ↓            ↓
  AGENT A     AGENT B      AGENT C
  (job X)     (job Y)      (job Z)
     │           │            │
     └───────────┼────────────┘
                 ↓
          ┌────────────┐
          │ MERGER /   │ ← combines sub-results
          │ AGGREGATOR │
          └────────────┘
```

The hard part is the decomposition. The sub-tasks must be genuinely independent. If A's output feeds B's input, their errors correlate and the pattern collapses into sequential.

## Independence Tests

Before you commit to a decomposition, ask:

1. **Does B need A's output to do its job?** If yes, they are not independent. Reconsider.
2. **Can A and B run in different sessions, on different machines, at different times, and still produce equivalent results when merged?** If yes, they are independent.
3. **If A fails, does B still produce something useful?** If yes, independent. If no, correlated.

Independence is often a spectrum. The more independent, the more the pattern works. Some real systems have "weakly coupled" sub-tasks where one feeds the other with a narrow interface. That is closer to a pipeline than a swarm, and worth naming as such.

## Where This Archetype Lives

- **Research / information gathering**: ten agents researching ten different aspects of a question, merged into one report. The retreat's "patrol workers on loops" pattern.
- **Content analysis**: classify a batch of 100 videos, one agent per video. Perfectly embarrassingly parallel.
- **Multi-file code changes**: different sub-agents on different files or different modules, with a merge / integration step at the end.
- **Data processing pipelines**: the boring, high-volume work. ETL, enrichment, deduplication, validation. Each agent does one narrow thing on one record.
- **Competitor monitoring**: one agent per competitor, running on its own loop, feeding a central ledger. Exactly the monitoring pattern you already have.

## What Makes This Different From Fan-Out / Fan-In

The existing `stochastic-consensus-and-fan-out-fan-in.md` video in techniques covers fan-out / fan-in: cheap researchers on different angles, expensive synthesizer combines them. That is one instantiation of this archetype (decomposition by research angle, merge by synthesis).

This archetype is more general: the sub-tasks don't have to be research, the merger doesn't have to be expensive, and the dimension of decomposition can be anything (files, records, competitors, time windows, customer segments).

## The Merger Is the Hard Part

Decomposition is usually straightforward. Merging is where the design effort goes.

- **Concatenation merge**: sub-results are independent data points. Stack them. Trivial.
- **Reconciliation merge**: sub-results overlap or contradict. Need a rule to resolve conflicts. Hard.
- **Synthesis merge**: sub-results need to be integrated into a unified artifact. Usually requires an expensive model with good judgment. Hardest.

If your merge is trivial, the archetype is basically free. If your merge is hard, the merge is where the leverage lives and where most of your engineering goes.

## Detecting Failed Independence

Warning signs that your "independent" sub-tasks are actually coupled:

- The same error keeps appearing across multiple sub-agents. Their inputs or prompts are correlated.
- One sub-agent's output contradicts another's, and you have no way to resolve. The task wasn't actually decomposable.
- The merge step is rewriting more than it is combining. Decomposition was artificial.

When you see these, rethink the decomposition before throwing more compute at it.

## Connection to Patrol Workers

The retreat specifically calls out the unsexy version of this archetype:

> "Most enterprise agent orchestration will not look like swarming at all. The more common pattern is 'patrol workers on loops': agents running well-defined ETL transforms, data quality checks and business process monitors on continuous cycles."

Patrol workers are this archetype at steady state. Each worker has a narrow job. They run continuously. Errors stay local. The merger is usually just a database or a dashboard. Most production agent value is going to look like this, not like dramatic generative swarms.

## Key Concepts to Cover

- The compounding math: sequential errors multiply, parallel errors add
- Why sequential decomposition feels natural and is often wrong
- Independence tests (does B need A? can they run separately? does A's failure break B?)
- Three kinds of merger: concatenation, reconciliation, synthesis
- Merge as the hard part (where the engineering goes)
- Embarrassingly parallel tasks as the easiest starting point (research, classification, per-record processing)
- "Patrol workers on loops" as the steady-state version of this archetype
- Warning signs that sub-tasks are secretly coupled
- Difference from fan-out/fan-in (same mechanism, broader framing)

## Demo Plan

1. Sequential agent on a 10-step task. Show the compounding failure.
2. Same task, decomposed into 10 independent sub-tasks, parallel agents. Show 9 correct, 1 failure, regenerate the one.
3. A reconciliation merge: two agents produce overlapping results, show the conflict-resolution step.
4. A synthesis merge: six researchers, one synthesizer. Same as fan-out/fan-in but framed as an instance of this pattern.
5. A patrol workers example: three continuous loops monitoring different data sources, writing to a shared ledger.
6. A failed independence example: two "independent" agents that share a hidden assumption and both get it wrong together.

## Suggested Class Placement

Agent Teams — Video 5. The archetype most relevant to production ops work. Pairs with `stochastic-consensus-and-fan-out-fan-in.md` and with Ray's own competitor-monitor routine as a real-world example.
