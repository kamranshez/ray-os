---
title: "Ch 15: Inter-Agent Communication (A2A) -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "15"
pattern: "Inter-Agent Communication (A2A)"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 15: Inter-Agent Communication (A2A)** - Antonio Gulli

> Net-new: a hands-on "expose your agent as an A2A server with an Agent Card" build, plus a complement to the MCP videos framing A2A vs MCP (agents-talk-to-agents vs agent-talks-to-tools). ACS multi-agent content is all in-process Claude Code subagents; the cross-framework HTTP protocol is absent.

## The one idea worth a video

- **A2A is an open HTTP/JSON-RPC standard that lets agents built in *different* frameworks discover and call each other via a published "Agent Card."** This is the spine: it subsumes discovery, task lifecycle, streaming, and security because all of them hang off the one move of publishing a machine-readable identity and speaking a shared wire protocol. VERDICT: ❌ net-new video available.
- **A2A and MCP are complementary layers, not competitors: MCP wires an agent to tools/data, A2A wires an agent to other agents.** Distinct explainer with its own decision framework and "which do I reach for" payoff. VERDICT: 🔗 next-step video available (complements the MCP videos).

## Summary + counts

Google's A2A protocol is an open HTTP/JSON-RPC standard letting agents from different frameworks discover, delegate, and collaborate via Agent Cards, complementing MCP's tool layer.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - A2A: publish an Agent Card, become a callable agent
THE CLAIM: any agent can be made interoperable with agents from other stacks by hosting a JSON "Agent Card" at a well-known URI and answering JSON-RPC 2.0 over HTTP(S). WHY IT'S NON-OBVIOUS: the default assumption is that multi-agent means spawning subagents *inside your own runtime* (Claude Code's Task tool, ADK sub-agents) - same vendor, same process. A2A argues the useful unit is a network-addressed, "opaque" remote agent the client never has to understand internally. WHY IT'S TRUE / MECHANISM: (1) the Agent Card declares identity, endpoint URL, skills, input/output modes, auth schemes and streaming/push capabilities, so a client can *discover* and bind at runtime instead of being hardcoded; (2) work is modelled as asynchronous Tasks with a state machine (submitted -> working -> completed) plus messages, parts and streamed artifacts, so long-running cross-org jobs survive polling, SSE, or webhooks. WHAT IT GENERALIZES TO: the ACS coding angle - wrapping a Claude Code / Codex agent in a thin Starlette+Uvicorn server (the chapter's `A2AStarletteApplication` example) so a teammate's LangGraph or CrewAI agent can call *your* specialist agent without importing your code. HOW IT GOES WRONG: unsecured `/.well-known/agent.json` endpoints leak capability maps; skipping mTLS/OAuth on the endpoint turns "opaque remote agent" into an open RPC surface.

### Spine 2 - A2A vs MCP: two protocols, two jobs
THE CLAIM: "A2A is a protocol that complements Anthropic's Model Context Protocol... MCP focuses on structuring context for agents and their interaction with external data and tools, A2A facilitates coordination and communication among agents." WHY IT'S NON-OBVIOUS: both are "agent protocols" backed by big labs, so devs assume they compete and must pick one. WHY IT'S TRUE / MECHANISM: (1) MCP standardizes the *downward* interface - an LLM reaching a database, an API, a file system as a tool; (2) A2A standardizes the *sideways* interface - a task-and-workflow protocol where one autonomous agent delegates to a peer and gets artifacts back. They stack: an A2A remote agent can itself use MCP tools internally (the chapter's calendar agent uses a Google `CalendarToolset` behind its A2A endpoint). WHAT IT GENERALIZES TO: ACS already teaches MCP heavily and shows Claude Code conversing with Codex over MCP; the missing mental model is *when a shared tool interface is not enough and you need a delegation protocol between whole agents*. HOW IT GOES WRONG: teams reach for A2A for what is really a tool call (over-engineering), or cram agent-to-agent delegation into MCP tool definitions and lose the task lifecycle/streaming.

## 🎬 Proposed ACS videos

### 1. Expose Your Agent as an A2A Server (Agent Card + HTTP)
- **HOOK:** Your subagents live and die inside one Claude Code session. What if another team's agent - built in a totally different framework - could call yours over HTTP?
- **THE PROMISE:** For devs who already run subagents: after this you can publish an Agent Card and stand up a minimal A2A endpoint so any A2A client can discover and invoke your specialist agent.
- **THE SHAPE:** (1) contrast in-process subagents vs network-addressed remote agents; (2) write a WeatherBot/Calendar-style Agent Card JSON - name, url, skills, capabilities, auth; (3) host it at `/.well-known/agent.json`; (4) stand up the Starlette+Uvicorn `A2AStarletteApplication` from the chapter and hit it with a `sendTask` JSON-RPC call; (5) add mTLS/OAuth and show why the discovery endpoint must be locked down.
- **SPINE:** Spine 1.
- **SLOT:** Advanced Techniques -> Multi-Agent Orchestration (new chapter entry, "Agents across frameworks").
- **RELATIONSHIP:** ❌ net-new. The Multi-Agent Orchestration chapter (Subagent Teams, Multi Subagents for Hard Problems, Refactoring with Subagents) is entirely in-process Claude Code delegation; there is no video on a cross-framework, network-addressed agent protocol, Agent Cards, or agent discovery.
- **PROOF TO REUSE:** the WeatherBot Agent Card JSON (streaming/skills/auth blocks); the `main()` calendar-agent example building `AgentCard` + `A2AStarletteApplication` + Uvicorn; the three discovery strategies (well-known URI, curated registries, direct config) and the "secure the card endpoint with mTLS" warning.

### 2. A2A vs MCP: When Agents Need to Talk to Agents
- **HOOK:** You've wired Claude Code to a dozen MCP tools. So why is Google shipping a *second* protocol - and when do you actually need it?
- **THE PROMISE:** A clean mental model: after this you can decide in seconds whether a job is an MCP tool call or an A2A agent delegation.
- **THE SHAPE:** (1) MCP = agent-to-tools (downward), A2A = agent-to-agents (sideways); (2) show the two stacking - an A2A remote agent that internally calls MCP tools; (3) map to ACS reality: Codex MCP Server already lets Claude Code converse with Codex over MCP - where would A2A change that; (4) a decision checklist (shared tool vs delegated task with its own lifecycle/streaming).
- **SPINE:** Spine 2.
- **SLOT:** Master Claude Code -> MCP Servers (or Advanced Techniques -> Multi-Agent Orchestration).
- **RELATIONSHIP:** 🔗 complements "Codex MCP Server" by being its next step. That video teaches Claude Code talking to Codex CLI over MCP to arbitrate reviews and reach consensus; this adds the *framework-agnostic delegation protocol* layer and the A2A-vs-MCP decision so Ray need not re-teach MCP setup or the Codex handshake.
- **PROOF TO REUSE:** the verbatim "A2A... complements Anthropic's Model Context Protocol" passage; the key-takeaway line that A2A manages "tasks and workflows between different agents" while MCP is "a standardized interface for LLMs to interface with external resources"; the calendar agent using an MCP-style toolset behind an A2A endpoint.

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** Google's A2A is an open HTTP/JSON-RPC protocol letting agents from different frameworks discover, delegate to, and collaborate with each other via published Agent Cards, complementing MCP.

**IDEAS**
- A2A is an open standard for communication between AI agents built on different frameworks.
- Interoperability across LangGraph, CrewAI, and Google ADK is A2A's primary goal.
- Three core actors: User, A2A Client (client agent), A2A Server (remote agent).
- The remote agent is "opaque" - clients need not know its internal operation.
- An Agent Card is a JSON file acting as an agent's digital identity.
- The card lists endpoint URL, version, skills, capabilities, input/output modes, and auth.
- Agent discovery uses well-known URIs, curated registries, or direct configuration.
- Communication is structured around asynchronous Tasks with a state machine.
- Tasks carry messages made of parts (text, files, structured JSON) plus metadata attributes.
- Agent outputs are "artifacts," which can be streamed incrementally as results arrive.
- All payloads travel over HTTP(S) using JSON-RPC 2.0.
- A server-generated contextId groups related tasks to preserve continuity.
- Four interaction modes: synchronous request/response, async polling, SSE streaming, push webhooks.
- A2A is modality-agnostic - text, audio, and video are all supported.
- Security rests on mTLS, audit logs, Agent Card auth declarations, and OAuth/API-key credentials.
- A2A complements MCP: A2A coordinates agents, MCP connects agents to tools/data.
- Specialized agents can run independently on different ports for scalability.
- Use cases: multi-framework collaboration, workflow orchestration, dynamic information retrieval.

**INSIGHTS**
- Discovery via a machine-readable card decouples clients from hardcoded agent endpoints.
- Treating the remote agent as opaque is what enables true cross-framework interoperability.
- Modelling work as stateful tasks (not calls) is what survives long-running, cross-org jobs.
- A2A and MCP are orthogonal layers that stack, not rivals competing for one slot.
- Streaming and push modes exist because agent tasks routinely outlast a single request.
- Securing the discovery endpoint matters as much as securing the task calls themselves.
- Broad industry backing (Microsoft, Salesforce, SAP) is what makes an open protocol viable.

**QUOTES**
- "The remote agent operates as an 'opaque' system, meaning the client does not need to understand its internal operational details." - Gulli
- "A2A is a protocol that complements Anthropic's Model Context Protocol (MCP)... While MCP focuses on structuring context for agents and their interaction with external data and tools, A2A facilitates coordination and communication among agents." - Gulli
- "An AgentCard serves as a digital identifier for an agent, allowing for automatic discovery and understanding of its capabilities by other agents." - the book
- "A2A encourages a modular architecture where specialized agents can operate independently on different ports." - the book

**HABITS / PRACTICES**
- Host the Agent Card at a standardized `/.well-known/agent.json` path for automatic discovery.
- Secure card endpoints with access control, mTLS, or network restrictions.
- Pass credentials (OAuth 2.0 tokens, API keys) via HTTP headers, never in URLs or bodies.
- Declare authentication requirements explicitly in the Agent Card.
- Use RFC3339 timestamps and inject the current date into agent instructions for temporal context.
- Keep audit logs of all inter-agent communications for accountability and debugging.

**FACTS**
- A2A is supported by Atlassian, Box, LangChain, MongoDB, Salesforce, SAP, and ServiceNow.
- Microsoft plans to integrate A2A into Azure AI Foundry and Copilot Studio.
- Auth0 and SAP are integrating A2A support into their platforms.
- The a2a-samples repo provides Java, Go, and Python examples under Apache 2.0.
- Synchronous requests use the `sendTask` / `tasks/send` method.
- Streaming requests use `sendTaskSubscribe` / `tasks/sendSubscribe`.
- The chapter's calendar agent runs on `gemini-2.0-flash-001` via Google ADK.

**REFERENCES**
- Google A2A protocol; Google Agent Development Kit (ADK); Model Context Protocol (Anthropic).
- Frameworks: LangGraph, CrewAI, AG2, Azure AI Foundry.
- Tools: Trickle AI (visualizing A2A comms); Starlette, Uvicorn, JSON-RPC 2.0.
- github.com/google-a2a/a2a-samples; a2a-protocol.org; adk-docs.
- Chen, B. (2025) "How to Build Your First Google A2A Project" (Trickle.so).
- O'Reilly Radar: "Designing Collaborative Multi-Agent Systems with the A2A Protocol."
- Companies: Atlassian, Box, MongoDB, Salesforce, SAP, ServiceNow, Microsoft, Auth0.

**ONE-SENTENCE TAKEAWAY:** A2A is an open HTTP protocol letting different-framework agents discover and delegate to each other via Agent Cards.

**RECOMMENDATIONS**
- Write an Agent Card for a specialist agent and host it at a well-known URI.
- Stand up a minimal A2A server (Starlette + Uvicorn) and call it with JSON-RPC.
- Pick the right interaction mode: sync for quick calls, SSE/webhooks for long tasks.
- Lock down discovery and task endpoints with mTLS and header-based credentials.
- Use MCP for tools and A2A for agent-to-agent delegation - stack, don't substitute.
- Explore the a2a-samples repo to see LangGraph, CrewAI, and ADK interoperate.
