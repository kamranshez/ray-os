---
title: "From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work — Sandipan Bhaumik"
video_url: https://www.youtube.com/watch?v=2czYyrTzILg
video_id: 2czYyrTzILg
channel: AI Engineer
published: 2026-04-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**From Chaos to Choreography: Multi-Agent Orchestration Patterns That Actually Work — Sandipan Bhaumik**](https://www.youtube.com/watch?v=2czYyrTzILg) - AI Engineer - uploaded 2026-04-08

> Multiple net-new ACS videos available: this talk imports distributed-systems patterns that the catalog does not touch anywhere.

## The idea worth a video

**Spine 1: The moment you scale past one agent, your problem stops being the model and becomes distributed-systems coordination.** It subsumes the war story, the quadratic complexity curve, and the closing "build systems, not demos" argument. VERDICT: net-new video available.

**Spine 2: Choose choreography versus orchestration deliberately, using a workflow-complexity against autonomy matrix, not on instinct.** The single most film-able idea here: a decision framework plus a dual build. VERDICT: net-new video available.

**Spine 3: Agents should hand off immutable, versioned state snapshots with a validated data contract, never share mutable records.** The concrete fix for the race-condition war story. VERDICT: net-new video available.

**Spine 4 (also film-able): Wrap every agent call in a circuit breaker and give each agent a compensate method (saga rollback).** VERDICT: net-new video available.

## Summary + counts

Databricks Data and AI Tech Lead Sandipan Bhaumik shows why multi-agent systems fail as distributed systems and the coordination, state, and failure patterns that hold in production.

🔴 4 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: A multi-agent system is a distributed system

The claim: the moment you go from one agent to several, your hard problem stops being the model and becomes distributed-systems coordination. Why it is non-obvious: teams treat adding agents like adding features, a linear cost, and assume the database or framework quietly handles concurrency for them. Why it is true: every new agent adds handoffs, so n agents create roughly n-squared over two coordination edges, and each edge is a race condition, a stale read, or a state-sync failure waiting to happen. Sandipan's credit system proved it: the write to Postgres succeeded but the cache was never invalidated, so the risk agent read a stale 680 and approved customers who should have been flagged. As he puts it, "This is no longer an AI problem. This is a distributed system problem." What it generalizes to: this is identical to microservices, where the same coordination, idempotency, and observability problems dominate and the AI is incidental. How it goes wrong: over-engineering heavyweight infra for a two-agent toy, or, far more common, blaming the model and the prompts when the bug is purely architectural.

### Spine 2: Choreography versus orchestration is a deliberate choice

The claim: choose choreography (agents react to events on a shared bus, decentralized) versus orchestration (one central coordinator drives every call) deliberately, using a two-axis matrix of workflow complexity against required autonomy. Why it is non-obvious: most teams pick one on instinct, and many pick choreography because it "feels more agentic," then, in Sandipan's words, "spend months firefighting because they can't debug distributed event flows." Why it is true: choreography couples agents loosely and scales cleanly, but no component owns the trace, so failures become detective work (which agent failed to publish, was the event consumed twice); orchestration makes the coordinator the single source of truth that owns the execution graph, state, retries, and logs, which is exactly why regulated industries pick it despite losing autonomy. What it generalizes to: this is the classic event-driven versus request-driven tradeoff in microservice backends. How it goes wrong: the hard quadrant, a complex workflow that still needs autonomy, needs a hybrid (choreography with saga compensation), and choosing choreography without bulletproof observability, he warns, "will destroy you."

### Spine 3: Immutable versioned state and data contracts

The claim: agents should exchange immutable, versioned state snapshots through an append-only log, validating a data contract at every boundary, instead of writing to shared mutable records. Why it is non-obvious: engineers assume a modern database prevents lost updates by default; it does not unless you reach for explicit transactions, serializable isolation, or SELECT FOR UPDATE. Why it is true: with shared mutable state, two agents read 680, both write, and the last write silently erases the other (a lost update); with frozen snapshots that only ever insert a new version, concurrent modification is structurally impossible, and each handoff validates schema plus a confidence threshold so bad data is caught at the boundary rather than three agents downstream where it produces garbage. Versioning also buys lineage: "You can binary search through your state history to find where things went wrong." What it generalizes to: this is event sourcing, or a Git commit history, an immutable append-only ledger you can replay. How it goes wrong: the storage and latency cost of never updating in place, and contracts that exist but are not actually enforced still let garbage flow silently.

## 🎬 Proposed ACS videos

### 1. Choreography vs Orchestration: How to Wire Multiple Agents Without the Chaos
- **HOOK:** One flaky agent should not take down your whole workflow, and the fix starts with how your agents talk to each other.
- **THE PROMISE:** For anyone wiring more than two agents: pick the right coordination pattern on purpose, instead of choosing on instinct and firefighting for months.
- **THE SHAPE:** (1) the five-agent credit war story; (2) choreography demo on an event bus (research completed, analysis ready, report); (3) orchestration demo with a central coordinator owning the graph; (4) the complexity-versus-autonomy decision matrix; (5) the hybrid quadrant with saga compensation.
- **SPINE:** 2.
- **SLOT:** Loopy AI, new chapter "Multi-Agent Systems in Production." Note the existing Advanced Techniques > Multi-Agent Orchestration chapter is about Claude Code subagents for coding, a false friend, not agent-system topology.
- **RELATIONSHIP:** ❌ net-new. Every ACS multi-agent video is about spawning Claude Code subagents to help you code; nothing covers coordination topologies for agent systems you ship.
- **PROOF TO REUSE:** the "feels more agentic ... then months firefighting" quote; the event-bus publish/subscribe flow; the decision matrix he explicitly tells audiences to screenshot.

### 2. The State Handoff Pattern That Kills Agent Race Conditions
- **HOOK:** Two agents read the same record, both write, and one update silently vanishes; here is how to make that class of bug impossible.
- **THE PROMISE:** For engineers whose agents share data: hand off state between agents with zero race conditions and full replayability.
- **THE SHAPE:** (1) the lost-update demo (both read 680, last write wins); (2) frozen versioned snapshots in an append-only insert log; (3) a schema plus confidence contract validated at each handoff; (4) binary-searching the version history to find the bad step.
- **SPINE:** 3.
- **SLOT:** Loopy AI, "Multi-Agent Systems in Production" (state and contracts).
- **RELATIONSHIP:** ❌ net-new. No ACS video covers immutable versioned state, append-only handoffs, or data contracts between agents.
- **PROOF TO REUSE:** the frozen Python dataclass carrying version and creator; the confidence-below-0.7 rejected handoff; "binary search through your state history to find where things went wrong."

### 3. Your Multi-Agent System Is a Distributed System, Not an AI Problem
- **HOOK:** The bug that broke a production credit engine was not in the model or the prompt; it was in the architecture.
- **THE PROMISE:** For anyone scaling past one agent: diagnose coordination failures as distributed-systems problems and reach for the proven patterns instead of tuning the model.
- **THE SHAPE:** (1) one agent works, then product asks for five; (2) the n-squared complexity curve (25x, not 5x); (3) the cache-invalidation war story; (4) a map of the four pattern families (coordination, state, failure recovery, contracts) that the deeper videos each expand.
- **SPINE:** 1.
- **SLOT:** Loopy AI, intro to the "Multi-Agent Systems in Production" chapter (mindset and overview).
- **RELATIONSHIP:** ❌ net-new. ACS has no video reframing multi-agent work as distributed-systems engineering.
- **PROOF TO REUSE:** "This is no longer an AI problem. This is a distributed system problem."; "It gets 25 times more complex."; "Not bad AI, but bad architecture."

### Also film-able (not deep-dived)
- **Circuit Breakers and Saga Rollback for Agent Workflows** — wrap every agent call in a circuit breaker so one failing agent fails fast instead of cascading, and give each agent execute and compensate methods so the orchestrator can walk backward and undo partial failures. SPINE 4. SLOT: Loopy AI, "Multi-Agent Systems in Production" (failure recovery). ❌ net-new. Proof: the half-open breaker retrying after 60 seconds; the saga walk-backward compensate example that clears the draft recommendation and cached research.

## 📚 Full wisdom (reference)

**SUMMARY**
Databricks Data and AI Tech Lead Sandipan Bhaumik shows why multi-agent systems fail as distributed systems and the coordination, state, and failure patterns that hold in production.

**IDEAS**
- Moving from one agent to five agents means building a distributed system, not merely adding features.
- Coordination complexity grows exponentially: five agents create at least ten potential connections, each a failure point.
- A cache invalidation failure let the risk agent read a stale, wrong credit score of 680.
- The real race condition lived in the system architecture, not the database, the models, or prompts.
- Choreography means agents coordinate through events published on a message bus, staying decentralized and fully autonomous.
- Orchestration means one central coordinator calls each agent directly, and the agents never call each other.
- Choreography's real nightmare is debugging: you play detective guessing which agent failed to publish which events.
- Use a decision matrix: plot workflow complexity against autonomy to pick choreography, orchestration, or a hybrid.
- A simple workflow with high autonomy favors choreography; a complex workflow with low autonomy favors orchestration.
- The hardest quadrant, a complex workflow that still needs autonomy, calls for choreography plus saga compensation.
- Shared mutable state causes lost updates: two agents read 680, and the last write silently wins.
- Immutable versioned state snapshots, stored as an append-only insert log, eliminate concurrent modification and stale reads.
- In Python, a frozen dataclass makes each state object immutable, carrying a version number and creator.
- Data contracts validate the schema at each handoff, rejecting low-confidence output before it corrupts downstream agents.
- Versioned state gives lineage: binary search the history to locate exactly where the output went bad.
- The circuit breaker wraps every agent call: after five failures it opens and simply fails fast.
- After a timeout period the breaker goes half-open, testing one request before closing or reopening again.
- The saga pattern gives each agent execute and compensate methods, so every operation stays fully reversible.
- On failure the orchestrator walks the executed agents backward, calling compensate to restore the initial state.

**INSIGHTS**
- Multi-agent projects die from bad architecture, not bad AI: the model is rarely the real problem.
- Most teams pick choreography or orchestration instinctively, then regret that unexamined default once production load arrives.
- Autonomy feels agentic, but without strong tracing, distributed event flows become impossible to debug at scale.
- Regulated industries choose orchestration because auditability and rollback matter far more than raw agent autonomy does.
- Databases alone will not save you: default isolation levels quietly ship race conditions straight into production.
- Catching a bad handoff at the contract boundary beats discovering garbage output three agents further downstream.
- Circuit breakers prevent cascading failure, so one flaky agent no longer brings the whole workflow down.
- Compensation gives distributed agents transactional semantics: partial failures roll back cleanly instead of leaving stuck workflows.
- Graceful degradation, skipping an agent or using cached results, beats crashing the entire production workflow outright.
- Unsexy infrastructure work, not clever prompts, is precisely what separates reliable production systems from flashy demos.

**QUOTES**
- "This is no longer an AI problem. This is a distributed system problem." — Sandipan Bhaumik
- "Not bad AI, but bad architecture." — Sandipan Bhaumik
- "The race condition wasn't in the database. It was in the architecture." — Sandipan Bhaumik
- "It doesn't get just five times harder. It gets 25 times more complex." — Sandipan Bhaumik
- "Most teams pick one instinctively and regret it." — Sandipan Bhaumik
- "I've seen teams choose choreography because it feels more agentic more autonomous. Then they fi spend months firefighting because they can't debug distributed event flows." — Sandipan Bhaumik
- "The orchestrator is the single source of truth." — Sandipan Bhaumik
- "Agents are dumb. They just take the input, they do the work, they return the output." — Sandipan Bhaumik
- "You can binary search through your state history to find where things went wrong." — Sandipan Bhaumik
- "Circuit breakers are the single most important failure recovery pattern for multi-agent systems." — Sandipan Bhaumik
- "It is not sexy, but it's how production systems handle partial failures." — Sandipan Bhaumik
- "You don't get applause for implementing a circuit breaker." — Sandipan Bhaumik
- "Demos are easy. You use an LLM to show something cool, everyone can do it. These things don't work in production." — Sandipan Bhaumik
- "Be a systems engineer." — Sandipan Bhaumik

**HABITS**
- He plots every customer use case on the complexity-versus-autonomy matrix before choosing any agent coordination pattern.
- In financial services he uses orchestration almost exclusively, prizing its easy debugging and reliable rollback guarantees.
- He wraps every agent call in a circuit breaker and never leaves a single one unguarded.
- He stores every state version as an append-only insert, never updating an existing row in place.
- He validates the schema and a confidence threshold at each handoff before accepting any agent's output.
- He registers every agent's input and output schema in one central catalog, versioned and governed together.
- He traces every agent call: latency, inputs, outputs, and token usage, all through one observability layer.
- He logs every circuit breaker open and close transition to spot exactly when agents start flaking.
- He tells audiences to screenshot the decision matrix, fully expecting they will reference it repeatedly later.

**FACTS**
- Two agents have at least one connection, while five agents have at least ten potential connections.
- In that credit system, twenty percent of decisions had incorrect risk ratings within just three days.
- The risk agent read the cache 500 milliseconds after the write and got badly stale data.
- The first single agent ran two weeks in production with zero issues before four were added.
- It took the team two full days to find the cache invalidation race condition in production.
- A frozen dataclass in Python enforces immutability, blocking any later modification of that particular state object.
- A circuit breaker typically opens after five consecutive failures and moves to half-open after sixty seconds.
- The saga compensation pattern originates in distributed databases as a way to handle long-running distributed transactions.

**REFERENCES**
- Speaker: Sandipan Bhaumik, Data and AI Tech Lead at Databricks (prior: AWS, NHS, Tier 1 banks). LinkedIn: linkedin.com/in/sandipanbhaumik. Slides linked in the video description.
- LangGraph (orchestrator), Mosaic AI Agent Framework (Databricks), Agent Bricks.
- Unity Catalog (governance, lineage, agent/schema registration), Delta Lake (immutable versioned state storage), MLflow (per-agent tracing, LLM-as-judge, open/close transition logging).
- Databricks Model Serving / Function Serving and AI Gateway (circuit breaker style retries, timeouts, rate limits).
- Distributed-systems patterns: circuit breaker, saga / compensation, event sourcing, message bus, choreography vs orchestration, DAGs.
- Databases: PostgreSQL, serializable isolation, SELECT FOR UPDATE, explicit transactions, caching / cache invalidation.

**ONE-SENTENCE TAKEAWAY**
Scaling past one agent is a distributed systems problem; borrow proven patterns, not bigger models.

**RECOMMENDATIONS**
- Before adding more agents, map every connection and treat each one as a potential failure point.
- Pick choreography or orchestration deliberately using the complexity-versus-autonomy matrix, never by instinct or gut feel alone.
- Replace shared mutable state with immutable versioned snapshots, each stored in an append-only durable insert log.
- Define a data contract for every agent handoff and reject low-confidence output right at the boundary.
- Wrap every agent call in a circuit breaker so a single failure never cascades across everything.
- Give each agent execute and compensate methods so the orchestrator can roll back any partial failures.
- Instrument strong tracing before choosing choreography; without it, distributed event debugging will eventually just destroy you.
- Use explicit transactions, serializable isolation, or SELECT FOR UPDATE instead of trusting default database concurrency behavior.
- Design for failure upfront, because agents will time out, hit rate limits, and crash mid-workflow eventually.
