---
title: "Ch 01: Prompt Chaining -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "01"
pattern: "Prompt Chaining"
status: covered
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 01: Prompt Chaining** - Antonio Gulli

> Already covered. The "pipeline pattern" (decompose a task into a chain of focused prompts with structured handoffs and deterministic glue between steps) is the exact subject of ACS "Dynamic Workflows," which teaches it as runnable code rather than textbook theory.

## The one idea worth a video

- **Break one monolithic prompt into a sequence of focused sub-prompts where each step's output feeds the next.** This is the load-bearing idea; every use case in the chapter (report synthesis, OCR, code refinement, stateful chat) is a re-instantiation of it. VERDICT: ✅ already covered (kept for context).
- **A chain is only as reliable as the data passed between steps, so enforce structured output and insert deterministic (non-LLM) logic to validate and branch between model calls.** Distinct enough to consider separately, but the demo lives inside the same ACS video. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Prompt chaining decomposes complex tasks into a sequence of focused prompts, each output feeding the next, improving reliability through modularity, structured handoffs, and deterministic logic between steps.

🔴 0 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 2 covered

## 🔬 Deep dive

### Spine 1 - Decompose into a sequential chain
THE CLAIM: for multi-part tasks, a chain of small focused prompts beats one monolithic prompt. WHY IT'S NON-OBVIOUS: the intuitive move is to write one big instruction that lists everything you want ("summarize, extract data, draft an email"); the chapter argues this reliably fails. WHY IT'S TRUE: a single prompt raises cognitive load, producing "instruction neglect," "contextual drift," and "error propagation where early errors amplify" - Gulli's failure taxonomy. Splitting the task means "each step is simpler and less ambiguous, which reduces the cognitive load on the model," and you can assign a distinct role per step (Market Analyst, then Trade Analyst, then Documentation Writer). WHAT IT GENERALIZES TO: agentic coding. This is exactly scripted orchestration - a pipeline of agent calls where each has one job and hands off to the next, which is what ACS "Dynamic Workflows" builds in JavaScript (pipelines, agent calls, conditionals, loops, implement-review-fix). HOW IT GOES WRONG: over-decomposition adds latency and cost, and a chain has no way to recover if an early step silently degrades - failure propagates forward unless you gate each handoff.

### Spine 2 - Structured handoffs + deterministic glue
THE CLAIM: "the reliability of a prompt chain is highly dependent on the integrity of the data passed between steps," so force structured output (JSON/XML) and run plain code between model calls. WHY IT'S NON-OBVIOUS: people think the win is just "smaller prompts"; the sharper insight is that the *seams* between steps are where chains break, and the fix is deterministic, not more prompting. WHY IT'S TRUE: natural-language handoffs are ambiguous, so "the subsequent prompt may fail due to faulty input"; a JSON schema makes the payload "machine-readable and can be precisely parsed." Then you insert non-LLM logic - validation, conditional re-prompting when fields are missing, and offloading exact arithmetic to "an external calculator tool" because "a significant challenge for LLMs is performing precise mathematical calculations." WHAT IT GENERALIZES TO: coding agents that emit structured results consumed by the next agent or by a script - ACS "Dynamic Workflows" calls these "schemas for structured handoffs" with conditionals and budgets. HOW IT GOES WRONG: over-rigid schemas cause valid outputs to be rejected; and validation you never actually check gives false confidence.

## 🎬 Proposed ACS videos

No net-new or complement pitch. Both spines are substantially covered by **"Dynamic Workflows"** (Master Claude Code -> Subagents), which teaches prompt chaining as runnable scripted orchestration: pipelines, agent calls, schemas for structured handoffs, conditionals, loops, and examples like implement-review-fix and deep research. Related coverage: **"Long Context Failure"** (Techniques) already teaches the single-monolithic-prompt failure modes (context poisoning, distraction, confusion) that motivate decomposition, and **"Designing a Task Lifecycle"** (Loopy AI) chains multiple loops end-to-end. The chapter is a textbook framing of what ACS already films hands-on; nothing here becomes a distinct new demo.

## 📚 Full wisdom (reference)

### SUMMARY
Prompt chaining decomposes complex tasks into a sequence of focused prompts, each output feeding the next, improving reliability through modularity, structured handoffs, and deterministic logic between steps.

### IDEAS
- Prompt chaining is a divide-and-conquer strategy: break a daunting problem into smaller sequential sub-problems.
- Each sub-problem gets its own designed prompt; one prompt's output becomes the next prompt's input.
- Sequential processing introduces modularity and clarity, making each step easier to understand and debug.
- The dependency chain lets the model build on prior work and progressively approach the solution.
- Chains enable integration of external knowledge and tools - APIs, databases - at each step.
- Prompt chaining is foundational for building AI agents that plan, reason, and act.
- A single complex prompt causes instruction neglect, contextual drift, error propagation, and hallucination.
- Decomposing raises accuracy because each step carries lower cognitive load and less ambiguity.
- The model can be assigned a distinct role at each stage (Market Analyst, Trade Analyst, Writer).
- Reliability depends on data integrity between steps; ambiguous handoffs cause downstream failure.
- Structured output formats like JSON or XML make handoffs machine-readable and precisely parseable.
- Complex operations combine parallel processing for independent gathering with chaining for dependent synthesis.
- Data extraction uses conditional retries: validate fields, re-prompt for missing/malformed ones, repeat.
- Delegate precise arithmetic to external calculator tools since LLMs struggle with exact math.
- Chaining inserts deterministic logic between model calls for validation and conditional branching.
- Prompt chaining underpins stateful conversational agents by carrying entities across turns.
- Context Engineering builds a complete informational environment before generation, beyond query phrasing.
- Output quality depends more on context richness than on model architecture.

### INSIGHTS
- The seams between prompts, not the prompts themselves, are where chains most often break.
- Assigning a distinct persona per step focuses the model and raises per-step accuracy.
- Structured handoffs convert brittle natural-language passing into deterministic, parseable data flow.
- Deterministic code between model calls is where validation, branching, and tool offload belong.
- Real pipelines mix parallel independent gathering with sequential dependent synthesis.
- Chaining lets you swap unreliable LLM math for a reliable external tool call.
- Prompt chaining is the primitive from which planning, reflection, and multi-agent patterns are assembled.
- Context Engineering reframes the job from answering a question to building an operational picture.

### QUOTES
- "Rather than expecting an LLM to solve a complex problem in a single, monolithic step, prompt chaining advocates for a divide-and-conquer strategy." - Gulli
- "The output of one step acting as the input for the next is crucial." - Gulli
- "The reliability of a prompt chain is highly dependent on the integrity of the data passed between steps." - Gulli
- "This modularity is analogous to a computational pipeline where each function performs a specific operation before passing its result to the next." - Gulli
- "A significant challenge for LLMs is performing precise mathematical calculations." - Gulli
- "This approach also allows for the insertion of deterministic logic between model calls, enabling intermediate data processing, output validation, and conditional branching." - Gulli
- "Context Engineering is the systematic discipline of designing, constructing, and delivering a complete informational environment to an AI model prior to token generation." - Gulli

### HABITS / PRACTICES
- Break any multifaceted request into one prompt per distinct processing stage.
- Specify a structured output format (JSON/XML) for data passed between steps.
- Assign a distinct role to the model at each stage of the chain.
- Insert validation and conditional re-prompting between steps rather than trusting one pass.
- Delegate exact arithmetic and computation to deterministic external tools.
- Run independent extractions in parallel, then chain the dependent synthesis and review.

### FACTS
- The chapter cites a claim that 73% of consumers prefer brands using personal information for relevance.
- It cites that sales of products with ESG-related claims grew 28% over five years versus 20% without.
- LangChain provides linear-sequence abstractions; LangGraph adds stateful and cyclical computation.
- LangChain Expression Language (LCEL) uses the pipe operator to compose prompt-model-parser chains.

### REFERENCES
- LangChain / LangGraph (LCEL, StrOutputParser, ChatPromptTemplate, ChatOpenAI)
- Crew AI
- Google Agent Development Kit (ADK)
- Google Vertex AI prompt optimizer
- OpenAI, Google Gemini, Anthropic (as model providers)
- Prompt Engineering Guide - Chaining Prompts (promptingguide.ai)

### ONE-SENTENCE TAKEAWAY
Break complex tasks into a chain of focused prompts with structured, validated handoffs between each step.

### RECOMMENDATIONS
- Rewrite one failing monolithic prompt as a sequential chain and compare reliability.
- Enforce JSON output at each step so the next step parses instead of guesses.
- Add a validation-and-retry gate between extraction steps for unstructured documents.
- Offload any exact math in a chain to a calculator or code tool.
- Parallelize independent gathering, then chain the dependent synthesis and review stages.
- Build the linear LCEL two-step example, then extend it into a stateful LangGraph flow.
