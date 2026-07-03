---
title: "Ch 10: Model Context Protocol (MCP) -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "10"
pattern: "Model Context Protocol (MCP)"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 10: Model Context Protocol (MCP)** - Antonio Gulli

> Consuming MCP servers is heavily covered by ACS, but AUTHORING one (write a FastMCP server, expose your own functions, plug Claude Code in) is net-new, and the chapter's "wrap-vs-redesign" warning is a sharp complement to the existing MCP Servers video.

## The one idea worth a video

- **MCP is a universal client-server standard that lets any agent dynamically discover and call any compliant tool, replacing per-vendor function-calling glue.** This is the load-bearing frame the whole chapter reconstructs from - discovery, resources/tools/prompts, transports. VERDICT: ✅ already covered (kept for context).
- **You can flip from MCP consumer to MCP producer: expose your own functions as a server with FastMCP so Claude Code (or any client) can call them.** Distinct demo (author a server, not install one), distinct "one thing after". VERDICT: ❌ net-new video available.
- **An MCP wrapper is only as good as the API beneath it: wrapping a legacy API 1:1 makes agents slow and wrong; add deterministic filtering/sorting and agent-friendly formats (Markdown, not PDF).** Distinct design demo. VERDICT: 🔗 next-step video available.

## Summary + counts

MCP is an open client-server standard letting LLMs discover and call external tools, resources, and prompts uniformly, with FastMCP and ADK making servers and clients easy.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - MCP as a universal discovery standard (COVERED)
THE CLAIM: MCP is "a universal connection mechanism" - an open client-server protocol where servers expose resources (static data), tools (executable functions), and prompts (templates), and any compliant client can dynamically discover and call them. WHY IT'S NON-OBVIOUS: it argues against the default of per-provider function calling, where "tool integrations are often tightly coupled with the specific application and LLM being used" and every integration is bespoke. WHY IT'S TRUE / MECHANISM: (1) a client queries a server's manifest at runtime ("just-in-time discovery"), so capabilities can be added without redeploying the agent; (2) standardizing the transport (JSON-RPC over STDIO locally, Streamable HTTP/SSE remotely) means one server serves Gemini, GPT, Claude alike, so "any compliant tool can be accessed by any compliant LLM." WHAT IT GENERALIZES TO: the ACS coding world - installing Exa, Notion, PostHog into Claude Code or Codex, and the /mcp discovery flow. HOW IT GOES WRONG: too many servers blow up the context window (hence tool-search). This is thoroughly taught: "MCP Servers" (Claude Code), "MCP Servers" (Codex), "Claude.ai MCP Servers (Connectors)", and "MCP Search Tool" all cover discovery, scope, and toggling - so no new pitch here.

### Spine 2 - Author your own MCP server with FastMCP (NET-NEW)
THE CLAIM: with FastMCP you turn a plain Python function into an MCP tool using a single `@mcp_server.tool` decorator - "automatic schema generation intelligently interprets Python function signatures, type hints, and documentation strings" so the docstring becomes the tool description the LLM reads. WHY IT'S NON-OBVIOUS: ACS (and most devs) treat MCP as a consumer act - you install servers other people wrote. The chapter shows the inverse: you are the publisher, exposing "specialized internal functions or proprietary systems... in a standardized, easily consumable format, without needing to modify the LLM." WHY IT'S TRUE / MECHANISM: (1) FastMCP abstracts the protocol boilerplate, so `mcp_server.run(transport="http", ...)` makes the function "available as a network service"; (2) because the schema is derived from the signature, the same server is instantly consumable by any client (ADK, Claude Code) via URL - one authored server, many agents. WHAT IT GENERALIZES TO: the ACS dev wraps their own repo scripts, internal API, or DB helper as a local MCP server that Claude Code then calls by name. HOW IT GOES WRONG: no auth/authz (the chapter flags security as mandatory), or vague docstrings that mislead the model into wrong calls.

### Spine 3 - The MCP wrapper is only as good as the API beneath it (COMPLEMENT)
THE CLAIM: "MCP is a contract for an agentic interface, and its effectiveness depends heavily on the design of the underlying APIs it exposes" - wrapping a legacy API unchanged is often suboptimal. WHY IT'S NON-OBVIOUS: teams assume MCP magically makes any API agent-ready; the chapter insists "agents do not magically replace deterministic workflows; they often require stronger deterministic support to succeed." WHY IT'S TRUE / MECHANISM: (1) if a ticketing API only fetches tickets one-by-one, an agent summarizing high-priority tickets "will be slow and inaccurate at high volumes" - so you add deterministic filtering and sorting so the non-deterministic agent does less work; (2) format matters: a server returning PDFs is "mostly useless if the consuming agent cannot parse PDF content," so return Markdown "which the agent can actually read." WHAT IT GENERALIZES TO: how ACS devs should design the tools they expose (spine 2) - shape outputs and add server-side filters for the agent. HOW IT GOES WRONG: over-wrapping (rebuilding the whole backend) or shipping token-bloated raw payloads.

## 🎬 Proposed ACS videos

### 1. Build Your Own MCP Server in 15 Minutes with FastMCP
- **HOOK:** You have installed a dozen MCP servers into Claude Code. Now write one - and expose your own scripts to any agent.
- **THE PROMISE:** For the dev who consumes MCP but has never published it: after this you can turn any Python function or internal API into an MCP server Claude Code calls by name.
- **THE SHAPE:** (1) `pip install fastmcp`, write a `greet`-style tool with `@mcp_server.tool` and a real docstring; (2) `mcp_server.run(transport="http", host, port)` and hit localhost:8000; (3) `claude mcp add` the server and watch Claude discover it via `/mcp`; (4) add a second, genuinely useful tool (query your repo/db) and a `tool_filter`; (5) note auth as the production gate.
- **SPINE:** Spine 2.
- **SLOT:** Master Claude Code -> MCP Servers chapter (sits right after "MCP Servers" and "MCP Search Tool" as the authoring companion).
- **RELATIONSHIP:** ❌ net-new. The existing "MCP Servers" video teaches installing and toggling servers others wrote (claude mcp add, scope, /mcp, reconnect); none of the catalog shows AUTHORING a server, the FastMCP decorator, or schema-from-docstring - this is the producer side.
- **PROOF TO REUSE:** The FastMCP `greet` example and `@mcp_server.tool` decorator; "automatic schema generation... interprets Python function signatures, type hints, and documentation strings"; "the docstring becomes the tool's description for the LLM."

### 2. Make Your Tools Agent-Ready: Filtering, Sorting, and Markdown Over PDF
- **HOOK:** MCP does not make a bad API good. Wrap a legacy endpoint 1:1 and your agent gets slow and wrong.
- **THE PROMISE:** For devs exposing internal APIs to agents: after this you know the two fixes - server-side deterministic filters and agent-readable formats - that make a tool actually usable.
- **THE SHAPE:** (1) show the failure: a tool that returns tickets one-by-one, agent asked to "summarize high-priority tickets" thrashes; (2) add deterministic filtering/sorting server-side so the agent does less; (3) show a tool returning PDFs and the agent choking; (4) refactor to return Markdown; (5) principle: "agents require stronger deterministic support to succeed."
- **SPINE:** Spine 3.
- **SLOT:** Master Claude Code -> MCP Servers chapter (pairs with video 1), or Context Engineering as a tool-design lesson.
- **RELATIONSHIP:** 🔗 complements "MCP Servers" by being its next step. That video teaches how to add and use a server; it does not teach how to DESIGN the tool so the agent uses it well - this adds the API-shaping half (filtering, sorting, Markdown-not-PDF) that the chapter argues is where MCP effectiveness actually lives.
- **PROOF TO REUSE:** "MCP is a contract for an agentic interface... depends heavily on the design of the underlying APIs"; the one-by-one ticketing example; "creating an MCP server for a document store that returns files as PDFs is mostly useless"; "agents do not magically replace deterministic workflows."

## 📚 Full wisdom (reference)

SUMMARY: MCP is an open client-server standard letting LLMs discover and call external tools, resources, and prompts uniformly; FastMCP and ADK make servers and clients easy.

IDEAS:
- MCP is a universal adapter letting any LLM plug into any external system without custom integration.
- It standardizes how Gemini, GPT, Mixtral, and Claude talk to external apps and data.
- MCP uses a client-server architecture exposing resources, prompts, and tools.
- A resource is static data; a tool is an executable function; a prompt is a template.
- Clients dynamically discover a server's capabilities via a queried manifest, just-in-time.
- MCP fosters interoperability, composability, and reusability across systems and vendors.
- Wrapping legacy services in an MCP interface modernizes them without costly rewrites.
- Function calling is proprietary, one-to-one; MCP is an open, discoverable framework.
- MCP effectiveness depends on the design of the underlying APIs it exposes.
- Wrapping a legacy API unchanged is often suboptimal for a non-deterministic agent.
- Add deterministic filtering and sorting so agents work efficiently at high volume.
- Return agent-friendly formats like Markdown, not PDFs the agent cannot parse.
- Local servers use JSON-RPC over STDIO; remote use Streamable HTTP and SSE.
- FastMCP turns a Python function into a tool via one decorator with auto schema.
- ADK's MCPToolset consumes existing MCP servers via Stdio or HTTP parameters.
- npx and uvx run community MCP servers without global installation.
- tool_filter restricts which server tools an agent can actually use.
- Security (auth/authz) and error handling are mandatory considerations, not optional.

INSIGHTS:
- Standardization is the payload: one server, once written, serves every compliant LLM.
- Discovery-at-runtime lets agents gain capabilities without being redeployed.
- MCP does not enforce data quality; the wrapper is only as good as the API.
- Agents need MORE deterministic scaffolding, not less, to succeed reliably.
- Publishing a server inverts the usual consumer relationship - you expose your systems.
- Docstrings and type hints are the interface contract the model reads.
- Function calling suffices for fixed toolsets; MCP wins when the toolset evolves.

QUOTES:
- "Imagine a universal adapter that allows any LLM to plug into any external system, database, or tool without a custom integration for each one." - Gulli
- "MCP is a contract for an 'agentic interface,' and its effectiveness depends heavily on the design of the underlying APIs it exposes." - Gulli
- "Agents do not magically replace deterministic workflows; they often require stronger deterministic support to succeed." - Gulli
- "Creating an MCP server for a document store that returns files as PDFs is mostly useless if the consuming agent cannot parse PDF content." - Gulli
- "The docstring becomes the tool's description for the LLM." - Gulli
- "For simple applications, specific tools are enough; for complex, interconnected AI systems that need to adapt, a universal standard like MCP is essential." - Gulli

HABITS/PRACTICES:
- Replace the placeholder path with an absolute directory before running a filesystem server.
- Filter exposed tools with tool_filter to limit an agent to what it needs.
- Prefer a local server for sensitive data speed/security; remote for shared scalable access.
- Write clear docstrings and type hints so FastMCP generates a correct schema.

FACTS:
- npx ships with npm 5.2.0 and later and runs Node packages without global install.
- Community MCP servers are commonly distributed as Node.js packages run via npx.
- uvx uses uv to run Python tools in a temporary isolated environment.
- FastMCP HTTP servers default to listening on localhost:8000.
- Anthropic and FastMCP offer SDKs that abstract MCP boilerplate.
- The chapter lists nine key MCP use cases.

REFERENCES:
- Model Context Protocol (MCP) and its documentation.
- FastMCP (github.com/jlowin/fastmcp).
- Google ADK (Agent Development Kit), MCPToolset, StdioServerParameters, HttpServerParameters.
- MCP Toolbox for Databases; Google BigQuery.
- MCP Tools for Genmedia Services: Imagen, Veo, Chirp 3 HD, Lyria.
- @modelcontextprotocol/server-filesystem; npx; uvx; mcp-google-sheets.
- LLMs named: Gemini, GPT, Mixtral, Claude.
- Transports: JSON-RPC, STDIO, Streamable HTTP, Server-Sent Events.

ONE-SENTENCE TAKEAWAY: MCP is the universal standard letting agents discover and call any tool - and you can publish one.

RECOMMENDATIONS:
- Install a community MCP server (filesystem) via npx and drive it from your agent.
- Write a FastMCP server exposing one real internal function and connect Claude Code.
- Audit an API before wrapping it: add filtering/sorting and return Markdown.
- Use tool_filter and add auth before exposing any server beyond localhost.
- Choose function calling for fixed toolsets; adopt MCP when capabilities evolve.
