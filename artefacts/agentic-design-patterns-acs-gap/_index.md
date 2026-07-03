---
title: "Agentic Design Patterns (Gulli) -> ACS content-gap index"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
author: Antonio Gulli
date: 2026-07-03
status: complete
chapters_analyzed: 24
tags: [acs-gap, agentic-design-patterns, book, index]
---

## What this is

Every chapter of Antonio Gulli's *Agentic Design Patterns* run through the [[wisdom-to-acs-gap]]
skill: one report per chapter (spine idea -> deep dive -> ranked ACS video pitches -> full wisdom).
This index ranks the film-able video ideas the book implies for the Agentic Coding School and clusters
the ones that recur across chapters. The book is a conceptual/textbook treatment (framed around Google
ADK, LangChain, CrewAI); the value here is translating its patterns into hands-on agentic *coding* videos.

**Coverage:** 24 of 24 units analyzed (21 pattern chapters + 3 coding-relevant appendices: A Advanced
Prompting, E Agents on the CLI, G Coding Agents). Appendices B/C/D were out of scope (GUI / framework-survey).
**Post gate:** 21 of 24 cleared the gate (`posted`). 3 chapters were fully `covered` by the existing catalog.
**Spine tally:** 🔴 15 net-new · 🔗 23 complement · 🟡 0 partial · ✅ 24 covered.
**37 film-able ACS video ideas** across the 21 post-worthy chapters.

The book's altitude is *design patterns*, not *keystrokes* - so most spines land as 🔗 complements (the
next step beyond an existing practical ACS video) rather than 🔴 net-new. The 🔴 net-new cluster below is
where the book genuinely reaches ground ACS has not filmed.

---

## The biggest gaps: 🔴 net-new territory (film these first)

Ranked by how absent the area is from the 300+ video catalog and how buildable the demo is.

### 1. Agentic RAG / retrieval grounding - the single richest gap ([Ch 14](14-knowledge-retrieval-rag.md))
The only chapter that came back **3/3 net-new**. ACS teaches agentic search *of a codebase* but has no
end-to-end retrieval-grounding track: chunk -> embed -> retrieve -> **fact-check its own sources** ->
cite. Three distinct videos here: an agentic RAG that verifies its own retrievals, a docs-grounded Q&A
bot shipped end to end (For Business), and GraphRAG for multi-hop questions.

### 2. Evaluating agents: LLM-as-judge, goldsets, trajectory scoring ([Ch 19](19-evaluation-and-monitoring.md), [Appendix A](A-appendix-advanced-prompting.md), [Appendix E](E-appendix-agents-on-the-cli.md))
Recurs across three units and lands net-new each time. ACS has *quick benchmarking* but no "Evaluating
Agents" chapter: grade output with an LLM judge, score the **trajectory** not just the final answer,
and auto-tune a prompt against a goldset. A whole new Advanced Techniques chapter.

### 3. Build your OWN tools: MCP servers + A2A ([Ch 05](05-tool-use.md), [Ch 10](10-model-context-protocol.md), [Ch 15](15-inter-agent-communication.md))
ACS teaches *consuming* MCP connectors; the book's altitude is *authoring* them. Net-new: build an MCP
server in 15 min with FastMCP, expose your agent as an A2A server (agent card + HTTP), and the A2A-vs-MCP
"when do agents talk to agents" explainer.

### 4. Long-term agent memory ([Ch 08](08-memory-management.md))
Net-new: a persistent, searchable memory store that survives across sessions (semantic/episodic/procedural),
distinct from the ephemeral context window. Pairs with the procedural-memory complement (let Claude rewrite
its own CLAUDE.md).

### 5. Reliability & fallbacks ([Ch 12](12-exception-handling-and-recovery.md), [Ch 16](16-resource-aware-optimization.md))
Net-new: fallback chains that always return *something*, and fallback *models* so an agent never hard-fails.
A "Resilient Agent Design" chapter that does not exist yet.

### 6. Deterministic routing & a co-scientist discovery loop ([Ch 02](02-routing.md), [Ch 21](21-exploration-and-discovery.md))
Net-new: route with a rule/embedding *before* reaching for an LLM classifier; and a co-scientist loop that
hunts your codebase for the bugs nobody filed.

---

## Strongest signals: themes that recur across chapters

Recurrence across independent chapters is the best evidence an idea deserves its own video. Ranked by how
many distinct chapters hit each theme.

### 1. Multi-agent orchestration: choose the topology before you spawn  (~5 chapters)
The book's repeated move: decomposition is easy, the design decision is the *structure*. A "pick the shape
first" framework video plus concrete demos (debate, tournament, dispatch).
- Picking the Right Subagent Topology - the choose-before-you-spawn decision map ([Ch 07](07-multi-agent-collaboration.md))
- Build a Triage Router That Dispatches to Your Specialists ([Ch 02](02-routing.md))
- AI Council: Make Two Agents Debate Your Architecture Decision ([Ch 17](17-reasoning-techniques.md))
- Tournament of Fixes: Rank and Evolve, Don't Just Pick One ([Ch 21](21-exploration-and-discovery.md))
- Expose Your Agent as an A2A Server ([Ch 15](15-inter-agent-communication.md))
- **Slot:** Advanced Techniques -> Multi-Agent Orchestration (the chapter this cluster most feeds)

### 2. Reliability engineering: fallbacks, overseers, stopping conditions  (~4 chapters)
A taste-blind agent needs graceful failure designed in. The book keeps returning to it; ACS barely touches it.
- Fallback Chains for Agents (Always Return Something) ([Ch 12](12-exception-handling-and-recovery.md))
- Fallback Models So Your Agent Never Hard-Fails ([Ch 16](16-resource-aware-optimization.md))
- Add an Overseer That Kills Your Stuck Loops ([Ch 09](09-learning-and-adaptation.md))
- Making a Reflection Loop Know When to Stop - the convergence signal + iteration cap ([Ch 04](04-reflection.md))
- **Slot:** a new Advanced Techniques (or Loopy AI) chapter "Resilient Agent Design / Reliability & Recovery"

### 3. Evaluation & benchmarking: LLM-judge, goldsets, trajectory  (~4 chapters)
- Grading Your Agent with an LLM Judge; Scoring the Trajectory, Not Just the Answer ([Ch 19](19-evaluation-and-monitoring.md))
- Stop Guessing Which Agent Is Best - Benchmark Them ([Appendix E](E-appendix-agents-on-the-cli.md))
- Auto-Tune an Agent Prompt Against a Goldset ([Appendix A](A-appendix-advanced-prompting.md))
- Build a Self-Improving Skill Loop (Benchmark-Gated) ([Ch 09](09-learning-and-adaptation.md))
- **Slot:** Advanced Techniques -> new chapter "Evaluating Agents"

### 4. Author your own tools: MCP servers + A2A  (~3 chapters)
- Build Your Own MCP Server in 15 Minutes with FastMCP ([Ch 10](10-model-context-protocol.md))
- Build Your Own MCP Server to Give Claude Code a Custom Tool ([Ch 05](05-tool-use.md))
- A2A vs MCP: When Agents Need to Talk to Agents ([Ch 15](15-inter-agent-communication.md))
- **Slot:** Master Claude Code -> MCP Servers (authoring, not consuming)

### 5. Self-improving & optimization loops  (~4 chapters)
- Evolve Your Code with an LLM Fitness Loop (OpenEvolve) ([Ch 09](09-learning-and-adaptation.md))
- Let Claude Rewrite Its Own CLAUDE.md (Reflection Loop) ([Ch 08](08-memory-management.md))
- A Co-Scientist Loop for Your Codebase ([Ch 21](21-exploration-and-discovery.md))
- Auto-Tune an Agent Prompt Against a Goldset ([Appendix A](A-appendix-advanced-prompting.md))
- **Slot:** Loopy AI -> L3: Task Lifecycle (the improve-the-loop rung)

### 6. Routing & model tiering: pick the cheapest thing that works  (~3 chapters)
- Route Deterministically Before You Reach for an LLM ([Ch 02](02-routing.md))
- Auto-Routing Tasks to the Cheapest Model That Works ([Ch 16](16-resource-aware-optimization.md))
- Which CLI Agent For Which Job - A Routing Cheat Sheet ([Appendix E](E-appendix-agents-on-the-cli.md))
- **Slot:** Techniques -> Routing & Dispatch / Advanced Techniques -> Multi-Model & Multi-CLI Workflows

### 7. Safety, guardrails & human checkpoints  (~2 chapters)
- Build a Cheap-Model Input Firewall for Your Agents ([Ch 18](18-guardrails-safety-patterns.md))
- Build a Human Escalation Checkpoint Into Your Loop ([Ch 13](13-human-in-the-loop.md))
- **Slot:** Loopy AI -> new chapter "Input Guardrails / Reliability"

### 8. Hooks: commit-on-green & staged-diff review  (~2 chapters)
- The Commit-On-Green Loop: An Aider-Style Safety Net in Claude Code ([Appendix E](E-appendix-agents-on-the-cli.md))
- A Git Pre-Commit Hook That Reviews Your Staged Diff ([Appendix G](G-appendix-coding-agents.md))
- **Slot:** Master Claude Code -> Hooks

---

## Every chapter at a glance

| Ch | Pattern | Status | 🔴 / 🔗 / ✅ | Top pitch |
|----|---------|--------|-------------|-----------|
| [01](01-prompt-chaining.md) | Prompt Chaining | ✅ covered | 0 / 0 / 2 | (covered: sequential chains + deterministic glue) |
| [02](02-routing.md) | Routing | 🟢 posted | 1 / 1 / 0 | Route Deterministically Before You Reach for an LLM |
| [03](03-parallelization.md) | Parallelization | ✅ covered | 0 / 0 / 2 | (covered: fan-out + map-reduce merge) |
| [04](04-reflection.md) | Reflection | 🟢 posted | 0 / 1 / 1 | Making a Reflection Loop Know When to Stop |
| [05](05-tool-use.md) | Tool Use | 🟢 posted | 0 / 1 / 1 | Build Your Own MCP Server for a Custom Tool |
| [06](06-planning.md) | Planning | 🟢 posted | 0 / 1 / 2 | Build a Deep Research Loop: Plan, Approve, Gap-Fill, Cite |
| [07](07-multi-agent-collaboration.md) | Multi-Agent Collaboration | 🟢 posted | 0 / 1 / 2 | Picking the Right Subagent Topology |
| [08](08-memory-management.md) | Memory Management | 🟢 posted | 1 / 1 / 1 | Give Your Agent a Long-Term Memory It Actually Recalls |
| [09](09-learning-and-adaptation.md) | Learning and Adaptation | 🟢 posted | 0 / 3 / 0 | Build a Self-Improving Skill Loop (Benchmark-Gated) |
| [10](10-model-context-protocol.md) | Model Context Protocol | 🟢 posted | 1 / 1 / 1 | Build Your Own MCP Server in 15 Minutes with FastMCP |
| [11](11-goal-setting-and-monitoring.md) | Goal Setting and Monitoring | ✅ covered | 0 / 0 / 2 | (covered: goal specs + monitoring) |
| [12](12-exception-handling-and-recovery.md) | Exception Handling & Recovery | 🟢 posted | 1 / 1 / 1 | Fallback Chains for Agents (Always Return Something) |
| [13](13-human-in-the-loop.md) | Human-in-the-Loop | 🟢 posted | 0 / 1 / 1 | Build a Human Escalation Checkpoint Into Your Loop |
| [14](14-knowledge-retrieval-rag.md) | Knowledge Retrieval (RAG) | 🟢 posted | 3 / 0 / 0 | Build an Agentic RAG That Fact-Checks Its Own Sources |
| [15](15-inter-agent-communication.md) | Inter-Agent Communication (A2A) | 🟢 posted | 1 / 1 / 0 | Expose Your Agent as an A2A Server |
| [16](16-resource-aware-optimization.md) | Resource-Aware Optimization | 🟢 posted | 1 / 1 / 1 | Fallback Models So Your Agent Never Hard-Fails |
| [17](17-reasoning-techniques.md) | Reasoning Techniques | 🟢 posted | 0 / 2 / 1 | AI Council: Make Two Agents Debate a Decision |
| [18](18-guardrails-safety-patterns.md) | Guardrails / Safety | 🟢 posted | 0 / 1 / 2 | Build a Cheap-Model Input Firewall for Your Agents |
| [19](19-evaluation-and-monitoring.md) | Evaluation and Monitoring | 🟢 posted | 2 / 1 / 0 | Grading Your Agent with an LLM Judge |
| [20](20-prioritization.md) | Prioritization | 🟢 posted | 0 / 1 / 1 | Encode a Prioritization Rubric as a Skill |
| [21](21-exploration-and-discovery.md) | Exploration and Discovery | 🟢 posted | 1 / 1 / 1 | A Co-Scientist Loop for Your Codebase |
| [A](A-appendix-advanced-prompting.md) | Appendix A: Advanced Prompting | 🟢 posted | 2 / 0 / 1 | Auto-Tune an Agent Prompt Against a Goldset |
| [E](E-appendix-agents-on-the-cli.md) | Appendix E: Agents on the CLI | 🟢 posted | 1 / 2 / 0 | Stop Guessing Which Agent Is Best - Benchmark Them |
| [G](G-appendix-coding-agents.md) | Appendix G: Coding Agents | 🟢 posted | 0 / 1 / 1 | A Git Pre-Commit Hook That Reviews Your Staged Diff |

**Fully covered (no new video, kept for reference):** Ch 01 Prompt Chaining, Ch 03 Parallelization,
Ch 11 Goal Setting & Monitoring. These are foundational patterns the ACS catalog already teaches well;
their reports keep a deep dive for context but produced no pitch.

---

## How this was built

`pdftotext` split the 424-page book into 24 chapter/appendix text files. An `ultracode` workflow fanned out
one deep-analysis agent per unit (24 agents, parallel), each running the full wisdom-to-acs-gap pipeline -
extract wisdom, promote 1-3 spine ideas, deep-dive each in prose, gap-check every spine against the live ACS
catalog via `search_videos`, and pitch the buildable videos - then writing its own report here. This index
synthesizes the 24 structured summaries. Total: ~1.66M subagent tokens, 24/24 clean, ~14 min wall-clock.
