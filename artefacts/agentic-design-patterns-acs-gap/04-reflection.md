---
title: "Ch 04: Reflection -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "04"
pattern: "Reflection"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 04: Reflection** - Antonio Gulli

> The producer-critic separation is already deeply covered across ACS review videos. The one fresh angle is the loop's exit mechanism: how a generate-critique-refine loop KNOWS to stop (sentinel token + iteration cap + diminishing-returns) before it burns tokens and blows the context window. That is a next-step complement to Loopy AI's loop-design videos.

## The one idea worth a video

- **A separate critic agent beats an agent reviewing its own work, because the fresh persona removes the "cognitive bias" of grading your own homework.** This is the load-bearing idea of the whole chapter (Producer-Critic / Generator-Critic). VERDICT: ✅ already covered (kept for context).
- **Reflection is a LOOP, not a step - and a real loop needs an explicit stopping condition (a `CODE_IS_PERFECT` sentinel plus a max-iteration cap) or it over-refines, bloats context, and racks up cost.** Distinct DEMO (building the exit condition), distinct SLOT (Loopy AI convergence). VERDICT: 🔗 next-step video available.

## Summary + counts

An agent evaluates its own output and iteratively refines it; a separate producer-critic pair yields more objective, higher-quality results at added cost.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Producer-Critic separation
THE CLAIM: splitting reflection into two roles - a Producer that generates and a Critic that evaluates - "prevents the 'cognitive bias' of an agent reviewing its own work." WHY IT'S NON-OBVIOUS: the intuitive move is to ask one agent to "check your work," but a model grading its own output tends to rubber-stamp it; the default assumption that self-review is enough is exactly what the pattern argues against. WHY IT'S TRUE / MECHANISM: (1) the Critic gets a distinct system prompt and persona ("You are a senior software engineer," "a meticulous fact-checker"), so it approaches the output with no commitment to defend it; (2) it is instructed only to find flaws and emit structured feedback (the ADK example returns a `{status, reasoning}` dict), which the Producer then consumes as a guide. WHAT IT GENERALIZES TO: agentic coding - fresh-context subagents auditing a diff, or a second CLI reviewing a plan, is the same separation-of-concerns move. HOW IT GOES WRONG: the Critic can hallucinate problems in already-correct code, or be too lenient if its criteria are vague; and it doubles cost. This is squarely ACS territory - `/simplify` runs "three fresh-context review agents," `/code-review` fans out finder and verifier stages, and "Automatic Plan Reviewing with Subagents" spins up security/architecture/performance critics. COVERED.

### Spine 2 - The reflection loop and its stopping condition
THE CLAIM: reflection's real power is iterative (generate -> critique -> refine -> repeat), and a working loop needs an explicit exit: the chapter's critic emits the sentinel `CODE_IS_PERFECT` to break, guarded by `max_iterations = 3`. WHY IT'S NON-OBVIOUS: people picture "reflection" as one review pass; the chapter insists "true iterative reflection typically involves more complex orchestration" and that termination is a first-class design problem, not an afterthought. WHY IT'S TRUE / MECHANISM: (1) without a convergence signal the loop either stops arbitrarily (fixed N) or never stops; a sentinel token lets the Critic itself declare done. (2) Every extra cycle appends the draft, critique, and refinement to history, so the chapter warns the pattern is "memory-intensive" with "higher risk of exceeding the model's context window or being throttled." So the exit condition is also a cost and context-budget control. WHAT IT GENERALIZES TO: unattended coding loops - a builder-reviewer loop that must decide "clean enough to stop" vs "iterate again," which is Loopy AI's whole world. HOW IT GOES WRONG: a critic that never says perfect loops to the cap and ships mediocre work; one that says perfect too early ships bugs; diminishing returns mean iteration 3 often costs a full LLM call for nothing.

## 🎬 Proposed ACS videos

### 1. Making a Reflection Loop Know When to Stop
- **HOOK:** Your generate-critique-refine loop works, but when does it STOP? Fixed 3 passes wastes tokens; no cap runs forever.
- **THE PROMISE:** For anyone building a self-correcting agent loop -> after this you can design a convergence-and-exit mechanism (critic sentinel + iteration cap + diminishing-returns check) so the loop stops at "good enough" instead of over-refining or blowing context.
- **THE SHAPE:** (1) Show a naive fixed-N refine loop wasting a full pass on already-clean code. (2) Add a critic that emits a clean sentinel ("CODE_IS_PERFECT" / a PASS verdict) to break early. (3) Add a max-iteration guard as the safety cap. (4) Show the context/cost blow-up: history grows every cycle, so exiting early is a budget control, not just a nicety. (5) Wire it into a Loopy-AI builder-reviewer loop and watch it converge.
- **SPINE:** Spine 2 (the reflection loop and its stopping condition).
- **SLOT:** Loopy AI -> L3: Task Lifecycle (convergence / exit design).
- **RELATIONSHIP:** 🔗 complements "Testing the Loop" and "Designing a Task Lifecycle" by being their next step - those videos build the builder/verifier/reviewer loop and chain its stages, but assume the loop terminates; this adds the specific convergence signal and iteration cap that decide WHEN the loop exits, plus the cost/context reason it must.
- **PROOF TO REUSE:** The `CODE_IS_PERFECT` sentinel + `max_iterations = 3` pattern from the LangChain example; the chapter's warning that reflection is "memory-intensive... higher risk of exceeding the model's context window or being throttled"; the rule of thumb "use Reflection when quality... matters more than speed and cost."

### Also film-able (not deep-dived)
- **Single-agent self-critique as a lightweight in-session move** ("critique your own last output against these criteria before I accept it") - but this is largely covered by "Agent Introspection" and "Understanding Agent Output," which already teach treating self-reflections as hypotheses, not proof. Not pitched.

## 📚 Full wisdom (reference)

**SUMMARY:** Gulli explains the Reflection pattern: an agent evaluates and iteratively refines its own output, most robustly via a separate producer-critic pair, trading cost for quality.

**IDEAS:**
- Reflection is a feedback loop where an agent examines its output and refines it.
- It differs from chaining (pass-through) and routing (path choice) by looping back.
- The cycle is execution, evaluation/critique, reflection/refinement, optional iteration.
- Evaluation checks accuracy, coherence, style, completeness, or instruction adherence.
- The Producer-Critic (Generator-Critic) model splits generation and evaluation into two roles.
- A separate critic prevents the "cognitive bias" of an agent grading itself.
- The Critic gets a distinct persona and system prompt to find flaws objectively.
- Structured critic output (bulleted list, or status/reasoning dict) guides the next refinement.
- A single reflection step fits in LCEL; true iteration needs stateful orchestration like LangGraph.
- A sentinel phrase ("CODE_IS_PERFECT") plus a max-iteration cap terminates the loop.
- Conversation history is fed back each cycle so critique has full context.
- Memory turns reflection cumulative: each cycle learns from past critiques, avoiding repeat errors.
- Reflection intersects with goal-setting/monitoring: goals are the benchmark, reflection the corrector.
- The pattern is memory-intensive; history expands with every iteration.
- Reflection raises latency and cost because each loop is another LLM call.
- Google ADK does reflection via a SequentialAgent pipeline writing to shared state keys.
- An alternative ADK implementation uses a LoopAgent for iteration.

**INSIGHTS:**
- Objectivity is architectural: separating producer from critic buys unbiased evaluation cheaply.
- Termination is a first-class design problem, not an afterthought to the loop.
- Reflection adds meta-cognition, moving agents from executors to self-correcting problem-solvers.
- The context window is the hidden budget: iteration bloats history toward throttling and overflow.
- Reflection only pays off when quality matters more than speed and cost.
- A generalist producer misses specialized flaws a persona-scoped critic is built to catch.
- Memory converts one-shot reflection into a learning process across cycles.

**QUOTES:**
- "The Reflection pattern involves an agent evaluating its own work, output, or internal state and using that evaluation to improve its performance." (Gulli)
- "This separation of concerns is powerful because it prevents the 'cognitive bias' of an agent reviewing its own work." (Gulli)
- "Without memory, each reflection is a self-contained event; with memory, reflection becomes a cumulative process where each cycle builds upon the last." (Gulli)
- "Use the Reflection pattern when the quality, accuracy, and detail of the final output are more important than speed and cost." (Gulli)
- "Reflection adds a layer of meta-cognition to agentic systems, enabling them to learn from their own outputs and processes." (Gulli)

**HABITS/PRACTICES:**
- Give the critic a distinct persona and explicit review criteria, not "check this."
- Have the critic emit a machine-readable sentinel or verdict to control the loop.
- Cap iterations so a never-satisfied critic cannot loop forever.
- Pass full conversation history into both generate and critique stages.
- Reserve reflection for high-stakes outputs; skip it for time-sensitive tasks.

**FACTS:**
- The LangChain example uses OpenAI's GPT-4o at temperature 0.1 for deterministic output.
- The example loop runs a maximum of 3 iterations.
- The critic returns either a bulleted critique or the phrase "CODE_IS_PERFECT."
- The ADK example uses SequentialAgent with generator and reviewer LlmAgents sharing state keys.
- The ADK reviewer returns a dict with "status" (ACCURATE/INACCURATE) and "reasoning" keys.

**REFERENCES:**
- LangChain, LangChain Expression Language (LCEL), LangGraph, langchain-openai, langchain-community
- Google Agent Developer Kit (ADK): SequentialAgent, LlmAgent, LoopAgent
- Crew.AI
- OpenAI GPT-4o; also cited: Google Gemini, Anthropic as LLM options
- "Training Language Models to Self-Correct via Reinforcement Learning" (arxiv.org/abs/2409.12917)

**ONE-SENTENCE TAKEAWAY:** Loop an agent through generate-critique-refine, ideally with a separate critic, to trade cost for quality.

**RECOMMENDATIONS:**
- Build a producer-critic pair with two distinct system prompts before trusting single-agent self-review.
- Add a critic sentinel token plus an iteration cap to control loop termination.
- Watch context growth across cycles; exit early to avoid overflow and throttling.
- Use reflection for polished long-form content, code debugging, and detailed plans.
- Pair reflection with memory so the agent stops repeating critiqued errors.
