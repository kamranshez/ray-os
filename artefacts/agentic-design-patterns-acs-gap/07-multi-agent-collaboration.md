---
title: "Ch 07: Multi-Agent Collaboration -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "07"
pattern: "Multi-Agent Collaboration"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 07: Multi-Agent Collaboration** - Antonio Gulli

> The core pattern (specialized-role decomposition, critic-reviewer, debate) is already well-covered by ACS's Multi-Agent Orchestration and Subagents chapters. The one thing missing: the book's explicit topology-selection map (single -> network -> supervisor -> supervisor-as-tool -> hierarchical -> custom) -> a complement decision-framework video.

## The one idea worth a video

- **Split a task across specialized agents, each with a role, tools, and a communication protocol, and the ensemble beats any single agent.** This is the load-bearing spine that subsumes handoffs, parallelism, hierarchy, and expert teams. VERDICT: ✅ already covered (kept for context).
- **The interrelationship structure (network / supervisor / supervisor-as-tool / hierarchical / custom) is itself the key design decision, each with distinct failure modes.** Distinct from any single how-to demo: this is the map for choosing among them. VERDICT: 🔗 next-step video available.
- **A second group of agents critiques the first group's output (policy, security, correctness) before it ships.** The critic-reviewer loop that reduces hallucinations. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Multi-agent collaboration decomposes complex tasks across specialized agents that communicate via defined protocols and topologies, producing synergistic outcomes no single agent could reach.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 2 covered

## 🔬 Deep dive

### Spine 1 - Specialized-role decomposition (the core pattern)
THE CLAIM: a monolithic agent hits a ceiling on multi-domain tasks, so you structure the system as "a cooperative ensemble of distinct, specialized agents" whose "collective performance surpasses the potential capabilities of any single agent." WHY IT'S NON-OBVIOUS: the intuitive move is to make one agent smarter (more tools, longer prompt); the book argues the opposite - divide the objective into sub-problems and give each to the agent "best suited for that task." WHY IT'S TRUE / MECHANISM: (1) each specialist carries a smaller, cleaner context and tool surface, so it reasons better in its lane; (2) failure of one agent "does not necessarily cause a total system failure," giving modularity and robustness the monolith lacks. WHAT IT GENERALIZES TO: agentic coding - Claude Code's Explore/Plan/implement subagents, a researcher + writer crew, or read-only auditor subagents each starting from a different file. HOW IT GOES WRONG: without "a standardized communication protocol and a shared ontology" the handoffs corrupt; and over-decomposition adds coordination overhead that swamps the benefit. ACS already teaches this end-to-end (Nested Subagents, Quick Spawning, Combining Skills & Subagents), so it is covered.

### Spine 2 - Choosing the collaboration topology (the decision, not the demo)
THE CLAIM: "the choice of interrelationship and communication model for a multi-agent system is a critical design decision," and the book lays out a spectrum - single, network, supervisor, supervisor-as-a-tool, hierarchical, custom - each with named tradeoffs. WHY IT'S NON-OBVIOUS: most practitioners reach for whatever their tool does by default (usually a flat supervisor spawning workers) and never ask whether a peer network, a resource-providing supervisor-as-tool, or a multi-layer hierarchy fits better. WHY IT'S TRUE / MECHANISM: (1) a supervisor "introduces a single point of failure and can become a bottleneck if overwhelmed by a large number of subordinates"; (2) a network "fosters resilience" but pays in "communication overhead and ensuring coherent decision-making," so the right structure depends on task complexity, agent count, and acceptable overhead. WHAT IT GENERALIZES TO: agentic coding - deciding, for a real Claude Code job, between fan-out parallel subagents, an orchestrator that delegates, peer subagents that pass findings mid-run, or a supervisor that just exposes shared tools/skills. HOW IT GOES WRONG: picking a network for a task that needs one authority produces incoherent output; picking a lone supervisor for a huge fan-out bottlenecks it. ACS demos each structure individually but has no single "here's the map, here's how to pick" video - that is the gap.

### Spine 3 - Critic-Reviewer loop
THE CLAIM: one group of agents produces plans/drafts/answers; "a second group of agents then critically assesses this output for adherence to policies, security, compliance, correctness, quality" and the creator revises. WHY IT'S NON-OBVIOUS: teams assume a single strong generator is enough; the book insists on a structurally separate reviewer, "particularly effective for code generation." WHY IT'S TRUE / MECHANISM: (1) a fresh reviewer without the generator's commitment bias catches errors the author is blind to; (2) separating create-from-critique yields "a reduced likelihood of hallucinations or errors." WHAT IT GENERALIZES TO: agentic coding - exactly what /code-review, /simplify, and the ExitPlanMode review-agent hook do. HOW IT GOES WRONG: reviewer and generator sharing context collapses the independence; endless critique loops without a "final agent revises" stop condition. ACS covers this thoroughly (Automatic Plan Reviewing with Subagents, /code-review, Multi Subagents for Hard Problems), so it is covered.

## 🎬 Proposed ACS videos

### 1. Picking the Right Subagent Topology
- **HOOK:** You default to "spawn a few subagents" for everything - but flat fan-out, a supervisor, a peer network, and a hierarchy fail in completely different ways.
- **THE PROMISE:** For Claude Code power users - after this you can look at a task and deliberately pick the orchestration structure (and know the failure mode you're buying) instead of always reaching for the same one.
- **THE SHAPE:** (1) Lay out the book's spectrum - single, network, supervisor, supervisor-as-tool, hierarchical, custom; (2) map each to a concrete Claude Code job (flat parallel refactor, orchestrator that delegates, peer subagents passing findings mid-run, multi-layer nested delegation); (3) show the named failure of each - supervisor bottleneck/single point of failure, network communication overhead and incoherence; (4) demo one task solved two ways (flat vs supervisor) to show the tradeoff live; (5) give a one-line rule of thumb per structure.
- **SPINE:** Spine 2 (choosing the collaboration topology).
- **SLOT:** Advanced Techniques -> Multi-Agent Orchestration (capstone / decision-framework episode).
- **RELATIONSHIP:** 🔗 complements "Subagent Teams for Debugging" and "Nested Subagents" by being their next step - those two each demonstrate ONE structure (a peer team; a multi-layer hierarchy) executed well; this video steps back and teaches how to CHOOSE among all the structures before you spawn, so Ray should not re-teach how to build a peer team or nest agents - only when each wins.
- **PROOF TO REUSE:** "the choice of interrelationship and communication model... is a critical design decision"; the supervisor "introduces a single point of failure and can become a bottleneck"; a network "fosters resilience" but struggles with "communication overhead and ensuring coherent decision-making"; and the distinctive "Supervisor as a Tool" idea - a supervisor that "provides resources, guidance, or analytical support" rather than command-and-control (maps cleanly to a coordinator exposing shared skills/MCP tools instead of dictating).

## 📚 Full wisdom (reference)

### SUMMARY
Gulli's chapter presents Multi-Agent Collaboration: decompose complex tasks across specialized, communicating agents whose synergy and topology choice produce outcomes no single agent achieves.

### IDEAS
- A monolithic agent is constrained on complex, multi-domain tasks; decomposition into specialists lifts the ceiling.
- Task decomposition assigns each sub-problem to the agent best suited by tools, data, or reasoning.
- Efficacy depends less on division of labor and more on inter-agent communication mechanisms.
- A standardized communication protocol and shared ontology let agents exchange data and coordinate coherently.
- Distributed architecture buys modularity, scalability, and robustness against single-agent failure.
- Collaboration forms: sequential handoffs, parallel processing, debate/consensus, hierarchy, expert teams, critic-reviewer.
- Sequential handoffs pass one agent's output to the next, like a pipeline.
- Parallel processing runs agents on different sub-problems simultaneously, then combines results.
- Debate and consensus have agents with varied perspectives discuss to reach an informed decision.
- Hierarchical structures use a manager agent that delegates to workers and synthesizes results.
- Critic-reviewer agents assess output for policy, security, correctness before a final revision ships.
- A multi-agent system needs role delineation, communication channels, and an interaction protocol.
- Interrelationship models span a spectrum: single, network, supervisor, supervisor-as-tool, hierarchical, custom.
- A network is decentralized peer-to-peer, resilient but prone to communication overhead and incoherence.
- A supervisor centralizes coordination but is a single point of failure and bottleneck.
- Supervisor-as-a-tool provides resources and guidance rather than issuing top-down commands.
- Hierarchical stacks multiple supervisor layers over operational agents for scalable decomposition.
- Custom models hybridize or invent structures tuned to a problem's dynamics and metrics.
- Frameworks like Crew AI and Google ADK provide structures for agents, tasks, and interactions.
- Agent-as-a-tool lets a higher-level agent invoke another agent like a function call.

### INSIGHTS
- The bottleneck in agent systems is coordination and communication, not raw individual intelligence.
- Choosing the communication topology is the load-bearing design decision, not an afterthought.
- Robustness is architectural: isolating specialists means one failure doesn't collapse the whole system.
- Every topology trades control for resilience; supervisors centralize risk, networks distribute it.
- Separating creation from critique is what structurally reduces hallucination, not a smarter single agent.
- A shared ontology and protocol are prerequisites; without them decomposition corrupts at the seams.
- Supervisor-as-a-tool inverts control - the coordinator serves capability rather than dictating action.
- Synergy is the goal: the ensemble should exceed, not merely sum, individual agent capabilities.

### QUOTES
- "The collaboration allows for a synergistic outcome where the collective performance of the multi-agent system surpasses the potential capabilities of any single agent." (Gulli)
- "The efficacy of such a system is not merely due to the division of labor but is critically dependent on the mechanisms for inter-agent communication." (Gulli)
- "A second group of agents then critically assesses this output for adherence to policies, security, compliance, correctness, quality, and alignment with organizational objectives." (Gulli)
- "The choice of interrelationship and communication model for a multi-agent system is a critical design decision." (Gulli)
- "It introduces a single point of failure (the supervisor) and can become a bottleneck if the supervisor is overwhelmed." (Gulli)
- "The AgentTool acts as a bridge, allowing one agent to use another agent as a tool." (Gulli)

### HABITS / PRACTICES
- Give each agent a defined role, specific goal aligned to the objective, and scoped tools.
- Establish explicit communication channels and an interaction protocol before wiring agents together.
- Use sequential context passing (output_key -> session state) so one agent's output feeds the next.
- Add a separate critic-reviewer group for code, research, and logic before shipping output.
- Wrap a specialist agent as a tool (AgentTool) so a parent can invoke it like a function.
- Separate actions from reasoning: expose core capabilities as function tools, not agent instructions.
- Bound iterative loops with a max_iterations cap and an explicit stop condition.

### FACTS
- Crew AI and Google ADK are frameworks engineered to specify agents, tasks, and interactions.
- The chapter's Crew AI example uses the "gemini-2.0-flash" model in a sequential process.
- Google ADK provides LlmAgent, BaseAgent, SequentialAgent, ParallelAgent, LoopAgent, and AgentTool primitives.
- ADK's LoopAgent runs sub-agents repeatedly until a condition escalates or max_iterations (e.g. 10) is hit.
- ADK's ParallelAgent runs sub-agents concurrently, each writing to a distinct session-state output_key.
- The referenced survey "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" is arXiv 2501.06322.

### REFERENCES
- Crew AI (framework) - Agent, Task, Crew, Process primitives.
- Google ADK (framework) - LlmAgent, BaseAgent, SequentialAgent, ParallelAgent, LoopAgent, AgentTool.
- LangChain / langchain_google_genai (ChatGoogleGenerativeAI).
- Gemini 2.0 Flash / gemini-2.0-flash-exp models.
- "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" - arXiv 2501.06322.
- "Multi-Agent System - The Power of Collaboration" - Aravindakumar (Medium).

### ONE-SENTENCE TAKEAWAY
Decompose hard tasks across specialized, communicating agents, and choose the topology deliberately - the structure is the design.

### RECOMMENDATIONS
- List a task's sub-problems, then assign each to a purpose-built agent with scoped tools.
- Pick your topology on purpose: match single/network/supervisor/hierarchical to task complexity and agent count.
- Add a structurally separate critic-reviewer pass before merging generated code.
- Wrap frequently-reused specialists as callable agent-tools to keep the orchestrator's context clean.
- Cap iterative agent loops with a max-iteration ceiling and an explicit completion signal.
- Try a supervisor-as-a-tool structure: have the coordinator expose shared skills rather than micromanage workers.
