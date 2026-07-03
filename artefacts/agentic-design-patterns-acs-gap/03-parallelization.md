---
title: "Ch 03: Parallelization -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "03"
pattern: "Parallelization"
status: covered
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 03: Parallelization** - Antonio Gulli

> Already covered. Parallelization maps one-to-one onto ACS's mature subagents + worktrees + multi-agent-orchestration body (Async Tasks & Subagents, Quick Spawning Subagents, How I Use Worktrees, Multi Subagents for Hard Problems, Different Orderings). No net-new or next-step demo survives the gap-check.

## The one idea worth a video

- **Split a workflow into independent sub-tasks, run them at the same time, then synthesise the results into one answer.** This is the load-bearing idea: fan-out-then-merge subsumes the chapter's seven use cases and both code examples. VERDICT: ✅ already covered (kept for context).
- **A dedicated "merger" agent strictly grounded on the parallel outputs turns fan-out into a clean map-reduce.** De-merge candidate (a synthesis step, not just speed), but ACS already teaches the merge/converge half. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Parallelization runs independent LLM calls, tools, or sub-agents concurrently to cut latency, then merges their outputs; LangChain's RunnableParallel and Google ADK's ParallelAgent implement it.

🔴 0 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 2 covered

## 🔬 Deep dive

### Spine 1 - Fan-out independent sub-tasks
THE CLAIM: when a task decomposes into parts that do not depend on each other's outputs, run them concurrently instead of sequentially so total time approaches the slowest part, not the sum. WHY IT'S NON-OBVIOUS: the default agent loop is strictly sequential - plan, act, observe, repeat - so latency silently accrues even when steps are independent. WHY IT'S TRUE: the mechanism is I/O-bound waiting. Gulli is careful that "asyncio provides concurrency, not parallelism... a single thread using an event loop that intelligently switches between tasks when one is idle (e.g., waiting for a network request)." Because agent steps are dominated by network round-trips (model inference, search, DB), overlapping the waits collapses wall-clock time even under Python's GIL. WHAT IT GENERALIZES TO: agentic coding - spawning several read-only subagents to explore a repo, audit a diff, or research three approaches at once, then reading only their summaries. HOW IT GOES WRONG: Gulli's own key takeaway warns "a concurrent or parallel architecture introduces substantial complexity and cost, impacting design, debugging, and system logging"; and two subagents editing the same file collide, so fan-out only works on genuinely independent slices.

### Spine 2 - Merge/synthesis after the fan-out
THE CLAIM: parallel branches are worthless until a convergence step aggregates them; the ADK example ends with a `SynthesisAgent` whose instruction is "your entire response MUST be grounded *exclusively* on the information provided" in the parallel summaries. WHY IT'S NON-OBVIOUS: people picture parallelism as pure speed, but the hard, quality-determining work is the reduce step - combining possibly-conflicting outputs without hallucinating past them. WHY IT'S TRUE: independent workers produce fragments with no shared view; a grounded merger prompt both stitches them and acts as a guardrail against the synthesiser inventing connective tissue. WHAT IT GENERALIZES TO: ACS's "generate competing implementations then pick/merge the best" and "run subagents with different orderings then converge on ranked findings." HOW IT GOES WRONG: an ungrounded merger drifts into external knowledge; a merger fed contradictory summaries with no tie-break rule produces mush.

## 🎬 Proposed ACS videos

No pitches. Both spines are ✅ covered - the parallelization pattern is already taught end-to-end across ACS:

- **Fan-out for speed / background work** -> "Async Tasks & Subagents", "Quick Spawning Subagents" (Master Claude Code -> Subagents).
- **Parallel strategies, pick the convergent answer** -> "Multi Subagents for Hard Problems", "Different Orderings" (Advanced Techniques -> Multi-Agent Orchestration).
- **Fan-out + merge/synthesis** -> "Subagent Teams for Debugging", "Combining Skills & Subagents" (splits files across subagents, final type-check cleanup).
- **Parallel isolated work across worktrees** -> "How I Use Worktrees", "Worktrees", "Claude Code Desktop" (competing UI implementations in parallel across git worktrees).

The book's framing (LangChain RunnableParallel, ADK ParallelAgent) is framework-specific plumbing that does not translate into a distinct Claude Code / Codex demo beyond what these videos already show.

## 📚 Full wisdom (reference)

### SUMMARY
Gulli explains the Parallelization pattern: run independent agent sub-tasks concurrently to cut latency, then synthesise results, implemented via LangChain RunnableParallel and Google ADK ParallelAgent.

### IDEAS
- Parallelization executes multiple LLM calls, tools, or sub-agents concurrently rather than one after another.
- Identify workflow parts that do not depend on other parts' outputs; run those simultaneously.
- Total sequential time is the sum of task durations; parallel time approaches the slowest task.
- Parallelization pays off most when tasks wait on external I/O like APIs or databases.
- A research agent can search Source A and Source B at once, then summarise both concurrently.
- The final synthesis step is typically sequential, waiting for parallel branches to finish.
- LangChain LCEL runs a dictionary of runnables concurrently when passed downstream.
- RunnableParallel bundles independent chains and includes RunnablePassthrough to carry the original input forward.
- LangGraph enables parallel branches by defining multiple nodes reachable from one common node.
- Google ADK offers ParallelAgent and SequentialAgent primitives for concurrent then sequential orchestration.
- ADK sub-agents write results to session state via output_key for a later merger agent to read.
- A merger/synthesis agent should be grounded strictly on the parallel outputs, adding no external knowledge.
- asyncio gives concurrency, not true parallelism, switching tasks on a single GIL-bound thread.
- Use cases span research, data analysis, multi-API calls, content generation, validation, multi-modal, and A/B options.
- A/B testing generates multiple response variations in parallel to compare and select the best.
- Concurrent architecture adds real cost to design, debugging, and logging.
- ADK can also parallelise via LLM-driven delegation from a coordinator agent.
- Parallelization combines with chaining (sequential) and routing (conditional) for sophisticated control flow.

### INSIGHTS
- Latency, not compute, is the bottleneck parallelization attacks - overlap the waiting, not the thinking.
- The reduce/synthesis step is where quality lives; fan-out only buys speed.
- Grounding the merger prompt exclusively on inputs converts parallelism from a speed hack into a correctness guardrail.
- Concurrency (event-loop switching) is enough for I/O-bound agents; you rarely need true multi-core parallelism.
- Parallelism's cost is invisible until debugging - interleaved logs and nondeterministic ordering are the tax.
- Only genuinely independent sub-tasks parallelise; shared mutable state (same file) re-serialises them.
- Framework primitives (RunnableParallel, ParallelAgent) mostly hide the async plumbing so you design topology, not threads.

### QUOTES
- "Parallelization involves executing multiple components, such as LLM calls, tool usages, or even entire sub-agents, concurrently." - Gulli
- "The core idea is to identify parts of the workflow that do not depend on the output of other parts and execute them in parallel." - Gulli
- "Note that asyncio provides concurrency, not parallelism. It achieves this on a single thread by using an event loop that intelligently switches between tasks when one is idle." - Gulli
- "Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below." - Gulli (ADK merger prompt)
- "The adoption of a concurrent or parallel architecture introduces substantial complexity and cost, impacting key development phases such as design, debugging, and system logging." - Gulli
- "Use this pattern when a workflow contains multiple independent operations that can run simultaneously." - Gulli (Rule of thumb)

### HABITS / PRACTICES
- Decompose a workflow and mark which steps are independent before choosing sequential vs parallel.
- Bundle independent chains in RunnableParallel and pass the original input through with RunnablePassthrough.
- Store each parallel worker's output under a named key for a downstream merger to consume.
- Give the synthesis agent an explicit "use only provided inputs" instruction to prevent drift.
- Keep the final synthesis step sequential, gated on all parallel branches completing.

### FACTS
- LCEL uses `|` for sequential composition and dictionary/list constructs for concurrent execution.
- RunnableParallel is LCEL's construct for running multiple runnables side-by-side.
- Google ADK's ParallelAgent finishes only once all sub-agents complete and populate state.
- The LangChain example uses gpt-4o-mini; the ADK example uses gemini-2.0-flash.
- Python's GIL constrains asyncio to one executing thread despite apparent concurrency.

### REFERENCES
- LangChain / LangChain Expression Language (LCEL), RunnableParallel, RunnablePassthrough, ChatOpenAI, StrOutputParser.
- LangGraph (graph-topology parallel branches).
- Google Agent Developer Kit (ADK): LlmAgent, ParallelAgent, SequentialAgent, google_search tool.
- Python asyncio (asyncio.run, event loop, GIL).
- Models: gpt-4o-mini, gemini-2.0-flash.
- Docs: python.langchain.com/docs/concepts/lcel, google.github.io/adk-docs/agents/multi-agents, docs.python.org asyncio.

### ONE-SENTENCE TAKEAWAY
Run independent agent sub-tasks concurrently to cut latency, then merge their outputs into one grounded answer.

### RECOMMENDATIONS
- Audit an existing sequential agent for independent steps you can fan out.
- Build a fan-out-then-merge pipeline with RunnableParallel or ADK ParallelAgent + SequentialAgent.
- Add an explicitly grounded merger prompt so synthesis never invents beyond its inputs.
- Reserve parallelism for I/O-bound steps; measure wall-clock before and after.
- Budget extra effort for debugging and logging concurrent runs before adopting the pattern.
