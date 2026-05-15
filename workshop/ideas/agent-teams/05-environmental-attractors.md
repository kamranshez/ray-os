# Archetype 5: Environmental Attractors

## What This Video Covers

The most powerful and least-built archetype. Instead of agents arguing with each other or voting on an answer, you design an environment where the correct answer is a stable state the system naturally drifts toward. Agents take actions, the environment accepts or rejects them, and over time the system converges on correctness without any single agent or critic driving the outcome.

This is how git plus CI already works for humans. The agent-native version has tighter loops, more granular verification, and agents that can detect when they are in a regression and back out.

## Why This Matters

From the retreat, the idea in its purest form:

> "A shared document that multiple agents edit, with a verifier that only accepts changes improving a fitness score. The document converges toward high fitness."

> "A work ledger where agents claim tasks, complete them, and get verified. Incorrect completions get rolled back; correct ones stick. The ledger converges toward correctness over time."

> "A codebase with a CI gate. Agents propose changes; only passing changes merge. The codebase converges toward a state where all tests pass."

This is the archetype that scales without linear supervision cost. You don't need a human in the loop, a critic, or a voting pool for every change. The environment does the selecting.

## The Pattern

```
 ┌──────────┐  ┌──────────┐  ┌──────────┐
 │ AGENT 1  │  │ AGENT 2  │  │ AGENT 3  │
 └────┬─────┘  └────┬─────┘  └────┬─────┘
      │ proposes    │ proposes    │ proposes
      │ change      │ change      │ change
      ↓             ↓             ↓
 ┌──────────────────────────────────────┐
 │         ENVIRONMENT / GATE           │
 │  (fitness function, CI, ledger)      │
 │                                      │
 │  accepts changes that improve state  │
 │  rejects / rolls back the rest       │
 └──────────────────────────────────────┘
                   │
                   ↓
        STATE DRIFTS TOWARD CORRECTNESS
```

No agent is told what the right answer is. Agents propose. The environment selects. The shape of the environment determines the attractor.

## The Three Requirements

For this archetype to work, you need:

1. **A fitness function** — something that tells "better" from "worse" without human judgment. Tests passing. Error rate dropping. Latency improving. Revenue going up. The function has to be cheap to evaluate (the environment runs it constantly).

2. **A rollback mechanism** — the environment has to be able to reject changes and return to the previous state. Without this, bad changes stick and the system drifts away from correctness.

3. **A work ledger** — some record of what was proposed, what was accepted, what was rejected, and why. Without this, you cannot debug non-convergence or detect regressions.

The retreat is explicit that most organizations lack these prerequisites:

> "Self-healing requires several foundations that most organizations lack: a clear ledger of every change, an operating system for agents with identity controls and permission boundaries, strong generic mitigation capabilities (rollback, feature flags) that work without code changes, fitness functions that define what 'healthy' means in terms agents can evaluate."

If you don't have those three things, you are not ready for this archetype. Build them first.

## Real-World Instances

- **CI-gated codebase**: agents open PRs, only passing PRs merge. Tests are the fitness function. `git revert` is the rollback. The git log is the ledger.
- **Feature flag ramp**: agents propose flag changes, metrics decide if they stick. If error rate spikes or a key metric drops, the flag rolls back automatically. Metrics are the fitness function.
- **Content pipeline with quality gate**: agents generate content, a scoring step accepts or rejects before publishing. The score is the fitness function, staying unpublished is the rollback, the queue is the ledger.
- **Self-healing infra**: agents make remediation changes to a system in an incident. Fitness is "is the SLO met now." Rollback is automatic if it isn't. This is where the retreat points toward "agent-assisted healing."

## The Gaming Failure Mode

The retreat's sharpest warning about this archetype:

> "An agent with access to a linter that enforced a 500-line file limit responded by making individual lines longer, technically satisfying the rule while violating the principle behind it."

If your fitness function is game-able, agents will game it. This is true of humans too (look at any goodhearted-metric story), but agents optimize faster and more literally. The design question: can the fitness function be satisfied only by the behavior you actually want?

Mitigations:
- Multiple fitness functions that are hard to satisfy simultaneously by gaming any single one
- Human spot-checks on a sample of accepted changes
- Fitness functions that measure outcomes (users retained, bugs found) rather than proxies (lines of code, tickets closed)

## The Multi-Agent Collision Problem

The retreat also flags this:

> "Multiple agents attempting to fix the same issue can create feedback loops where one agent's fix triggers another agent's correction, creating an escalating cycle. When multiple agents make different prioritization decisions about trade-offs, the system can oscillate rather than converge."

If two agents are both trying to optimize a fitness function with different local views, they can fight each other. The environment has to include some coordination mechanism: locks on contested resources, a queue that serializes decisions, or an explicit reconciler.

## Why This Archetype Is Where the Industry Is Heading

All of the earlier archetypes still require human design per task. You decide the decomposition, write the critic prompt, choose the aggregator. Environmental attractors do the selection at runtime without per-task human design. You build the environment once, agents operate in it indefinitely.

That is what makes this the pattern that scales. It is also what makes it the hardest to build. Most teams will not get here without first building out the lower-cost archetypes and discovering the need for better infrastructure.

## Key Concepts to Cover

- The pattern: agents propose, environment selects, state converges
- Fitness function, rollback, work ledger as the three prerequisites
- Git + CI as the proto-version that already exists for humans
- Real instances: CI-gated code, flag ramps, content gates, self-healing infra
- The gaming failure mode (500-line limit → longer lines)
- Mitigations: multiple fitness functions, spot checks, outcome-based metrics
- The multi-agent collision problem (oscillation, fighting agents)
- Why this is where durable advantage lives (no per-task human design)
- Why most teams are not ready (prerequisites missing)

## Demo Plan

1. Walk through git + CI as the everyday version of this archetype. Name the pieces.
2. Show an agent-native version: agents propose changes, a gate accepts or rejects automatically.
3. Fitness function example: agent proposes edits to a document, a judge accepts only changes that improve a score.
4. Gaming example: set up a fitness function an agent can game. Show the gaming happen. Show the fix.
5. Collision example: two agents optimizing against each other, system oscillates. Add a reconciler.
6. End with the prerequisites checklist: does your org have the three foundations yet?

## Suggested Class Placement

Agent Teams — Video 6. The capstone. The archetype where convergence stops being an event and becomes a property of the system itself.
