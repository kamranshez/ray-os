---
title: "Ch 05: Tool Use (Function Calling) -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "05"
pattern: "Tool Use (Function Calling)"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 05: Tool Use (Function Calling)** - Antonio Gulli

> Consuming tools via MCP is already covered wall-to-wall in ACS. The gap is the OTHER half of this chapter: authoring your own tool -> wrapping your internal function/API/DB as a small MCP server so Claude Code can call it. That is a 🔗 complement to the existing "MCP Servers" videos.

## The one idea worth a video

- **A tool is just a well-described function: give the model a name, a purpose, and typed parameters, and it decides when to call it.** This is the load-bearing idea of the chapter (the `@tool` decorator demo) and it subsumes routing, calculation, retrieval and action-taking. In ACS terms, *consuming* tools is covered; *authoring* one (writing your own MCP server) is the gap. VERDICT: 🔗 next-step video available.
- **"Tool calling" is broader than "function calling": a tool can be an API, a database, a code interpreter, or even another specialized agent.** The agent becomes an orchestrator across a diverse resource ecosystem. VERDICT: ✅ already covered (subagents + MCP + code-execution native to Claude Code) (kept for context).

## Summary + counts

Tool Use, implemented via function calling, lets an LLM decide when to call described external functions, emit structured arguments, execute them, and fold results back into its response.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - A tool is a described function; authoring one is the gap
THE CLAIM: an agent gains real-world power the moment you describe an external function to it (name, purpose, typed parameters) and let the model decide when to emit a structured call. WHY IT'S NON-OBVIOUS: the instinct is that "giving an agent a tool" is a heavy integration job; the chapter shows it is mostly *writing a good docstring* - the `search_information` and `get_stock_price` demos are ten-line functions whose docstrings ("Use this tool to find answers to phrases like 'capital of France'") ARE the interface the model reasons over. WHY IT'S TRUE / MECHANISM: (1) the framework serialises the function signature + docstring into the tool schema sent to the LLM; (2) the LLM, seeing the user request beside that schema, generates JSON naming the tool and extracting arguments; (3) an orchestration layer executes the real function and returns the observation. The description quality, not the code, drives whether the right tool fires. WHAT IT GENERALIZES TO: in agentic *coding*, the analog of the book's `@tool` is writing your own MCP server - wrapping your internal REST API, a Postgres query, or a CLI so Claude Code can call it. ACS teaches *installing* MCP servers thoroughly, but not *building* one. HOW IT GOES WRONG: vague or overlapping docstrings make the model pick the wrong tool or hallucinate arguments; the CrewAI demo's fix - raise a `ValueError` instead of returning a string - shows error shape also teaches the agent how to recover.

### Spine 2 - Tool calling generalizes past functions to APIs, code, and agents
THE CLAIM: "tool" should be read expansively - a traditional function, an API endpoint, a database query, a sandboxed code interpreter, or a call to another specialized agent all count, turning the primary agent into an orchestrator. WHY IT'S NON-OBVIOUS: "function calling" sounds like invoking local Python; the chapter argues the same mechanism delegates a data-analysis task to an "analyst agent" or runs code in a sandbox (ADK's `built_in_code_execution`). WHY IT'S TRUE / MECHANISM: (1) from the model's view every tool is the same schema-plus-observation contract, so the callee's *implementation* is irrelevant; (2) that uniformity means an agent, an API, and an interpreter are interchangeable behind one interface, which is exactly how multi-agent orchestration composes. WHAT IT GENERALIZES TO: Claude Code already lives this - Bash is a code-execution tool, subagents are agents-as-tools, MCP servers are API-as-tool. HOW IT GOES WRONG: Gulli notes a real distinction - Vertex extensions auto-execute, while function calls require manual execution by the client, so blurring "tool" can hide who actually runs the code and with what permissions.

## 🎬 Proposed ACS videos

### 1. Build Your Own MCP Server to Give Claude Code a Custom Tool
- **HOOK:** You know how to install MCP servers. But when the tool you need does not exist, you write one - and it is smaller than you think.
- **THE PROMISE:** For anyone who has an internal API, script, or DB query they keep pasting into Claude Code: after this you can wrap it as a real MCP tool the agent calls on its own.
- **THE SHAPE:** (1) Start from a plain Python function - a stock/price/inventory lookup, mirroring the book's `get_stock_price`. (2) Wrap it in a minimal MCP server, writing the docstring/description AS the tool's interface. (3) `claude mcp add` it and confirm it shows in `/mcp`. (4) Prompt Claude Code so it decides to call the tool and folds the result back. (5) Break the docstring on purpose to show the model picking the wrong tool, then fix it - the description is the product.
- **SPINE:** Spine 1.
- **SLOT:** Master Claude Code -> MCP Servers (new video, sits right after "MCP Servers" install video).
- **RELATIONSHIP:** 🔗 complements "MCP Servers" by being its next step. That video teaches `claude mcp add`, adding Exa with an API key, scopes, and `/mcp` inspection - all on the CONSUMING side. This video is the AUTHORING side: writing the server that exposes your own function so the agent can call it. Ray should not re-teach install/scopes; open on "now you write one."
- **PROOF TO REUSE:** The chapter's six-step Tool Use loop (definition -> LLM decision -> structured call -> execution -> observation -> processing); the `@tool` docstring "Use this tool to find answers to phrases like 'capital of France'"; the CrewAI refactor lesson "raise a ValueError ... The agent is equipped to handle exceptions and can decide on the next action."

## 📚 Full wisdom (reference)

### SUMMARY
Gulli explains the Tool Use pattern: function calling lets an LLM decide when to invoke described external functions, emit structured arguments, execute them, and use results, demoed in LangChain, CrewAI, and Google ADK.

### IDEAS
- Tool Use, via function calling, lets agents interact with external APIs, databases, services, and code.
- The LLM decides when and how to use a tool from the request.
- A tool definition supplies name, purpose, and typed, described parameters to the model.
- The model emits structured JSON naming the tool and its arguments.
- An orchestration layer intercepts that JSON and executes the real function.
- Tool results are returned to the agent as an observation.
- The LLM folds the observation into a final answer or next step.
- Function calling breaks the limits of static training data with live information.
- "Tool calling" is broader: a tool can be an API, DB, or another agent.
- A primary agent can delegate work to a specialized "analyst agent."
- LangChain, LangGraph, and Google ADK provide tool-definition and binding support.
- LangChain's `@tool` decorator turns a Python function into a bound tool.
- `create_tool_calling_agent` plus `AgentExecutor` form LangChain's runtime.
- Returning clean data or raising errors beats returning strings from tools.
- Raised exceptions let the agent decide on a recovery action.
- ADK ships pre-built tools: Google Search, code execution, Vertex AI Search.
- `built_in_code_execution` gives the agent a sandboxed Python interpreter.
- Code execution supplies deterministic logic outside probabilistic generation.
- Vertex extensions auto-execute; function calls require manual client execution.
- Tool Use turns a text generator into an agent that senses, reasons, and acts.

### INSIGHTS
- The tool's docstring, not its code, is the real interface the model reasons over.
- Description quality determines whether the correct tool fires reliably.
- Uniform schema-plus-observation contract makes functions, APIs, and agents interchangeable.
- Error shape teaches the agent how to recover, not just that it failed.
- Code execution injects deterministic precision where language generation is unreliable.
- Auto-execution vs manual execution is the key control/permission boundary.
- Framing tools broadly reframes the agent as an orchestrator, not a caller.
- Tool Use is the bridge from reasoning to real-world action.

### QUOTES
- "The Tool Use pattern, often implemented through a mechanism called Function Calling, enables an agent to interact with external APIs, databases, services, or even execute code." - Gulli
- "Thinking in terms of 'tool calling' better captures the full potential of agents to act as orchestrators across a diverse ecosystem of digital resources and other intelligent entities." - Gulli
- "The tool now returns raw data (a float) or raises a standard Python error. This makes it more reusable and forces the agent to handle outcomes properly." - Gulli
- "The key difference between extensions and function calling lies in their execution: Vertex AI automatically executes extensions, whereas function calls require manual execution by the user or client." - Gulli
- "Tool Use is what transforms a language model from a text generator into an agent capable of sensing, reasoning, and acting in the digital or physical world." - Gulli

### HABITS / PRACTICES
- Define each tool with a clear name, purpose, and typed parameter descriptions.
- Write the docstring as the model-facing interface, with example trigger phrases.
- Return clean typed data from tools; raise specific errors rather than returning error strings.
- Write task descriptions that tell the agent how to handle success and failure.
- Check for the API key before running the agent to avoid runtime errors.
- Configure logging to debug and track tool calls during execution.

### FACTS
- LangChain's `@tool` decorator and `create_tool_calling_agent`/`AgentExecutor` build tool-using agents.
- Google ADK ships pre-built Google Search, code execution, and Vertex AI Search tools.
- ADK's `built_in_code_execution` provides a sandboxed Python interpreter.
- Vertex AI extensions are auto-executed by Vertex; function calls are executed by the client.
- The example uses `gemini-2.0-flash` and `gpt-4o` as tool-calling models.

### REFERENCES
- Frameworks: LangChain, LangGraph, Google Agent Developer Kit (ADK), CrewAI.
- Models: Gemini series (gemini-2.0-flash / -exp), OpenAI series (gpt-4o).
- Google tools: Google Search tool, `built_in_code_execution`, Vertex AI Search (VSearchAgent), Vertex AI extensions, Code Interpreter.
- Libraries: `langchain_google_genai`, `crewai`, `google.adk`, asyncio, nest_asyncio.
- Docs: LangChain Tools, Google ADK Tools, OpenAI Function Calling, CrewAI Tools.

### ONE-SENTENCE TAKEAWAY
Describe an external function to an LLM and it will decide when to call it.

### RECOMMENDATIONS
- Wrap an internal function or API as a tool and let the agent invoke it.
- Invest in tool docstrings and typed parameters before touching the logic.
- Return typed data and raise specific errors so agents recover gracefully.
- Give the agent a sandboxed code interpreter for deterministic calculation tasks.
- Note who executes each tool (auto vs manual) to manage permissions.
- Think in "tool calling," letting agents delegate to APIs, databases, or other agents.
