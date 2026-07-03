---
title: "Ch 06: Planning -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "06"
pattern: "Planning"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 06: Planning** - Antonio Gulli

> Core plan-then-execute is deeply covered by ACS's whole Planning chapter; the one net-step available is building a Deep-Research-style plan -> iterative-gap-fill -> cited-report loop, complementing "Dynamic Workflows".

## The one idea worth a video

- **Planning = decompose a high-level goal into a sequence of interdependent, executable steps before acting.** This is the load-bearing idea the whole chapter reconstructs from; it subsumes decomposition, dependency ordering, and workflow orchestration. VERDICT: ✅ already covered (kept for context).
- **The choice to plan dynamically vs script a fixed workflow hinges on one question: does the "how" need to be discovered, or is it already known?** A distinct decision-heuristic video, but ACS teaches both sides. VERDICT: ✅ already covered (kept for context).
- **Deep Research is planning's advanced form: an agent drafts a research plan, gets it approved, then runs an iterative search-analyse-gap-fill loop that adapts and emits a cited report.** VERDICT: 🔗 next-step video available.

## Summary + counts

Planning lets agents decompose complex goals into ordered executable steps, adapt around obstacles, and choose dynamic planning only when the path must be discovered.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 2 covered

## 🔬 Deep dive

### Spine 1 - Plan-then-execute decomposition
THE CLAIM: an agent facing a multi-step goal should first formulate a coherent plan - an ordered set of sub-goals - then execute it, rather than react step by step. WHY IT'S NON-OBVIOUS: LLMs feel most natural reacting to the immediate prompt; the chapter argues foresight beats reactivity for "multifaceted requests that involve multiple steps and dependencies." WHY IT'S TRUE / MECHANISM: (1) decomposition converts one intractable objective into small tasks each within the model's reliable range; (2) an explicit ordering lets the system manage dependencies and orchestrate tools "in a logical order" instead of thrashing. Gulli notes "LLMs are particularly well-suited for this, as they can generate plausible and effective plans based on their vast training data," and that "explicitly prompting or designing tasks to require planning steps encourages this behavior." WHAT IT GENERALIZES TO: agentic coding - Plan Mode makes Claude Code explore the codebase, surface options, and write a plan before editing. HOW IT GOES WRONG: over-planning trivial edits wastes context; a stale plan followed rigidly ignores what execution reveals. This is thoroughly covered by ACS's Planning chapters.

### Spine 2 - Discover-vs-known: when to plan dynamically
THE CLAIM: dynamic planning is a specific tool, not a default - "when a problem's solution is already well-understood and repeatable, constraining the agent to a predetermined, fixed workflow is more effective." WHY IT'S NON-OBVIOUS: agent hype implies more autonomy is always better; Gulli argues the opposite for known problems, because fixing the workflow "limits the agent's autonomy to reduce uncertainty and the risk of unpredictable behavior, guaranteeing a reliable and consistent outcome." WHY IT'S TRUE / MECHANISM: (1) autonomy trades predictability for flexibility, so where the path is known you pay uncertainty for nothing; (2) the single deciding question is "does the how need to be discovered, or is it already known?" WHAT IT GENERALIZES TO: coding - a scripted deterministic workflow for a migration you have run 100 times, vs a planning agent for a novel feature. HOW IT GOES WRONG: scripting a genuinely novel task straitjackets the agent; letting it freely plan a routine, high-volume task invites nondeterministic drift. ACS covers both faces: the "let it discover" side and the "script it" side.

### Spine 3 - Deep Research as adaptive plan-review-execute
THE CLAIM: the mature form of planning is a long-running agent that deconstructs a prompt "into a multi-point research plan," presents it to the user for review, then runs an iterative "search-and-analysis loop" that "dynamically formulates and refines its queries," identifies knowledge gaps, corroborates, and emits a structured cited report. WHY IT'S NON-OBVIOUS: most people treat research as one query-response; Gulli frames it as "a managed, long-running process" that is async and "resilient to single-point failures." WHY IT'S TRUE / MECHANISM: (1) a human-approved plan aligns trajectory before expensive execution; (2) the gap-detection loop is what turns a flat search into comprehensive synthesis - "automating the iterative search-and-filter cycle, which is a core bottleneck in manual research." The OpenAI Deep Research API sharpens the coding angle: it "exposes all intermediate steps, including the agent's reasoning, the specific web search queries it executed, and any code it ran," and supports MCP to "connect the agent to private knowledge bases." WHAT IT GENERALIZES TO: building your own deep-research loop as a Claude Code skill / dynamic workflow. HOW IT GOES WRONG: no gap-check yields a shallow report; skipping the plan-approval gate wastes a long run on the wrong trajectory.

## 🎬 Proposed ACS videos

### 1. Build a Deep Research Loop: Plan, Approve, Gap-Fill, Cite
- **HOOK:** Deep Research isn't a product you buy - it's a plan-then-iterate loop you can build in Claude Code in an afternoon.
- **THE PROMISE:** For devs who want agent-driven research on their own sources: after this you can run a loop that drafts a research plan, waits for your approval, iteratively searches and closes gaps, then writes a cited markdown report.
- **THE SHAPE:** (1) Prompt the agent to deconstruct a question into a multi-point research plan and pause for approval; (2) fan out explore / web-search subagents per plan point; (3) add the gap-detection step - "what did we NOT answer?" - and loop back with refined queries; (4) synthesise into a structured report with inline source links; (5) show the transparent trace (queries run, reasoning) so the result is verifiable.
- **SPINE:** Spine 3.
- **SLOT:** Loopy AI -> Compounding Loops (a research loop), or Advanced Techniques -> Multi-Agent Orchestration.
- **RELATIONSHIP:** 🔗 complements "Dynamic Workflows" by being its next step - that video already teaches scripted JS orchestration with agent calls, schemas, conditionals, pipelines and even lists deep research as an example; this builds the deep-research loop itself, adding the plan-approval gate, the gap-detection cycle, and cited-report synthesis that a generic pipeline does not teach.
- **PROOF TO REUSE:** the plan-review gate ("deconstructing a user's prompt into a multi-point research plan... presented to the user for review and modification"); the gap-fill loop ("actively identifying knowledge gaps, corroborating data points, and resolving discrepancies"); the Deep Research API's transparency ("exposes all intermediate steps, including the agent's reasoning, the specific web search queries it executed") and MCP for private sources.

## 📚 Full wisdom (reference)

### SUMMARY
Gulli's Planning chapter shows agents decomposing complex goals into ordered executable steps, adapting around obstacles, and reserving dynamic planning for problems whose path must be discovered.

### IDEAS
- Planning is formulating a sequence of actions from an initial state toward a goal state.
- A planning agent is a specialist you delegate the "what" to, not the "how."
- The plan is created in response to the request, not known in advance.
- Adaptability is the hallmark: an initial plan is a starting point, not a rigid script.
- A capable agent registers new constraints, re-evaluates options, and formulates a new plan.
- Dynamic planning trades predictability for flexibility; it is a tool, not a universal solution.
- For well-understood, repeatable problems, a fixed workflow beats an autonomous planner.
- The deciding question: does the "how" need discovery, or is it already known?
- Planning decomposes a high-level objective into discrete, executable steps.
- Procedural automation uses planning to orchestrate workflows like employee onboarding.
- Robotics uses planning for state-space traversal optimizing time, energy, and constraints.
- Structured synthesis (research reports) plans phases: gather, summarize, structure, refine.
- LLMs generate plausible plans from vast training data.
- Explicitly designing tasks to require a plan step encourages planning behavior.
- CrewAI demo: one agent first drafts a bullet plan, then writes to it sequentially.
- Google Deep Research deconstructs a prompt into a plan presented for user review.
- Deep Research runs an async, iterative search-analyse loop resilient to single-point failures.
- OpenAI Deep Research API exposes reasoning, search queries, and code as intermediate steps.
- The API supports MCP to blend public web research with private knowledge bases.

### INSIGHTS
- Planning converts intractable goals into manageable tasks each within the model's reliable range.
- The real power of a planner is re-planning around obstacles, not the first plan.
- Autonomy is a cost, not a virtue: pay it only where the path is genuinely unknown.
- A human-approved plan aligns trajectory before you spend on expensive execution.
- Gap detection - "what did we miss?" - is what turns flat search into synthesis.
- Exposing intermediate steps makes an agent's output debuggable and verifiable.
- Planning is the bridge between human intent and automated execution of complex work.
- Comprehensiveness comes from processing more sources than a human can in the timeframe.

### QUOTES
- "planning is the ability for an agent or a system of agents to formulate a sequence of actions to move from an initial state towards a goal state." - Gulli
- "The plan is not known in advance; it is created in response to the request." - Gulli
- "An initial plan is merely a starting point, not a rigid script." - Gulli
- "the decision to use a planning agent versus a simple task-execution agent hinges on a single question: does the 'how' need to be discovered, or is it already known?" - Gulli
- "constraining the agent to a predetermined, fixed workflow is more effective... guaranteeing a reliable and consistent outcome." - Gulli
- "It begins by deconstructing a user's prompt into a multi-point research plan, which is then presented to the user for review and modification." - Gulli
- "the agent dynamically formulates and refines its queries based on the information it gathers, actively identifying knowledge gaps." - Gulli
- "the API exposes all intermediate steps, including the agent's reasoning, the specific web search queries it executed, and any code it ran." - Gulli

### HABITS / PRACTICES
- Define the objective and constraints (the "what"); let the agent chart the "how."
- Before committing, ask whether the solution path is known or must be discovered.
- Design tasks with an explicit "first make a plan, then execute" instruction.
- Present a generated plan to the user for review before running an expensive execution.
- Add a gap-detection step so the loop re-searches what it failed to answer.
- Inspect intermediate steps (queries, reasoning) to debug and verify agent output.

### FACTS
- Google Gemini Deep Research is an agent-based system for autonomous retrieval and synthesis.
- Deep Research can analyse hundreds of sources in a single async investigation.
- OpenAI Deep Research API used models o3-deep-research-2025-06-26 and o4-mini-deep-research-2025-06-26.
- The OpenAI Deep Research API supports the Model Context Protocol (MCP) for private data.
- The CrewAI example uses gpt-4-turbo via langchain_openai with a sequential process.

### REFERENCES
- CrewAI (Agent, Task, Crew, Process) framework
- LangChain / langchain_openai ChatOpenAI
- OpenAI Deep Research API (client.responses.create, web_search_preview, code_interpreter)
- Google Gemini Deep Research (gemini.google.com)
- Perplexity Deep Research
- Model Context Protocol (MCP)
- Models: gpt-4-turbo, o3-deep-research, o4-mini-deep-research

### ONE-SENTENCE TAKEAWAY
Planning turns reactive agents into strategists that decompose goals and adapt, but only discover paths worth discovering.

### RECOMMENDATIONS
- Reserve dynamic planning for novel tasks; script deterministic workflows for known, repeatable ones.
- Add an explicit plan-then-execute instruction to complex agent tasks.
- Build a research loop with a plan-approval gate and iterative gap-filling.
- Use an API that exposes intermediate reasoning and queries so results are verifiable.
- Connect research agents to private sources via MCP to blend proprietary and web data.
- Treat every plan as revisable; let the agent re-plan when it hits a constraint.
