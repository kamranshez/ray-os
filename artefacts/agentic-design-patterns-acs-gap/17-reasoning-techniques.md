---
title: "Ch 17: Reasoning Techniques -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "17"
pattern: "Reasoning Techniques"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 17: Reasoning Techniques** - Antonio Gulli

> Two next-step videos: an adversarial multi-agent DEBATE to settle a design call (beyond parallel voting), and a cost-optimal "small model + big thinking budget beats big model" measurement. CoT / ReAct / self-correction / self-consistency are already covered.

## The one idea worth a video

- **You buy agent accuracy with inference-time compute, and how you spend the "thinking budget" (deeper CoT, more candidates, more tool loops) matters more than raw model size.** This is the load-bearing idea: it subsumes CoT, ToT, self-correction, reasoning models, self-consistency, and Deep Research - they are all ways to spend more compute at inference. VERDICT: 🔗 next-step video available (economic model-size-vs-budget trade beyond "Reasoning Effort").
- **Move from a solitary agent to a council that ARGUES: agents present, critique, and rebut each other across rounds (Chain of Debates), reaching a validated consensus rather than one voice.** A distinct demo from independent parallel voting - the agents see and attack each other's reasoning. VERDICT: 🔗 next-step video available (adds cross-talk/rebuttal to "Multi Subagents for Hard Problems").
- ReAct (thought -> action -> observation loop) is the chapter's third pillar but is the definition of agentic coding and is thoroughly COVERED across the catalog. Kept for context, yields no pitch.

## Summary + counts

Advanced reasoning methods - CoT, ToT, self-correction, PALM, ReAct, multi-agent debate, MASS - make an agent's thinking explicit and trade inference-time compute for accuracy.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Buy accuracy with a thinking budget
THE CLAIM: "superior results can frequently be achieved from a comparatively smaller LLM by augmenting the computational investment at inference time." The chapter's Scaling Inference Law says performance tracks compute spent while generating, not just model size, and "a smaller model, when granted a more substantial 'thinking budget' during inference, can occasionally surpass the performance of a much larger model." WHY IT'S NON-OBVIOUS: it argues against "bigger is better" - the reflex to reach for the most expensive model. WHY IT'S TRUE / MECHANISM: (1) harder problems have a wider space of candidate solutions, so generating multiple candidates (self-consistency, beam search) and selecting the best strictly raises expected quality; (2) extended CoT lets a model self-correct and backtrack mid-trajectory, catching errors a single pass commits to. WHAT IT GENERALIZES TO: the ACS coding angle is a cost decision - run a cheap model with best-of-N or higher effort and measure whether it matches an expensive single pass on YOUR task, so you stop overpaying by default. HOW IT GOES WRONG: latency balloons; and past a point extra thinking adds tokens without accuracy (the law is a trade curve, not a free lunch), so you must find the knee.

### Spine 2 - A council that argues, not just votes
THE CLAIM: Chain of Debates (CoD) has "multiple, diverse models collaborate and argue," presenting ideas, critiquing each other's reasoning, and exchanging counterarguments - "an AI version of peer review." WHY IT'S NON-OBVIOUS: the default multi-agent move is to run agents independently and take a majority vote; here the agents actually read and rebut each other across rounds. WHY IT'S TRUE / MECHANISM: (1) independent samples share the same blind spots, so voting amplifies a common error; a rebuttal round forces each agent to defend claims against a specific counterargument, surfacing unsupported assumptions; (2) GoD extends this to a graph where arguments 'support'/'refute' each other and the winner is "the most robust and well-supported cluster," grounded in ground truth, search grounding, or model consensus. WHAT IT GENERALIZES TO: the coding angle is a two-agent architecture debate - one proposes an approach, a second attacks it with concrete failure cases, they iterate, and Ray adjudicates or a judge agent picks the surviving cluster. HOW IT GOES WRONG: agents can sycophantically converge (agreeing to agree), or debate forever without a stopping rule; you need an external verifier or ground-truth anchor.

## 🎬 Proposed ACS videos

### 1. AI Council: Make Two Agents Debate Your Architecture Decision
- **HOOK:** Parallel agents that vote share the same blind spots - make them argue instead.
- **THE PROMISE:** For anyone facing a reversible-but-expensive design call, run a structured debate that stress-tests both sides before you commit a line of code.
- **THE SHAPE:** (1) Frame a real decision (e.g. queue vs cron, monolith split); (2) spin up a Proposer agent and a Skeptic agent with a rebuttal loop - each must attack the other's last argument with a concrete failure case; (3) run 2-3 rounds; (4) a judge agent (or Ray) picks the surviving "most well-supported cluster"; (5) contrast with a plain majority vote to show what the debate caught.
- **SPINE:** Spine 2 (Chain of Debates / Graph of Debates).
- **SLOT:** Advanced Techniques -> Multi-Agent Orchestration.
- **RELATIONSHIP:** 🔗 complements "Multi Subagents for Hard Problems" by being its next step - that video runs independent strategy-analyzer subagents and implements the majority/convergent fix, with NO cross-talk between agents. This adds the rebuttal round where agents see and refute each other, plus a stopping/adjudication rule, which is exactly what independent voting misses.
- **PROOF TO REUSE:** "an AI version of peer review"; agents "critique each other's reasoning, and exchange counterarguments"; GoD's conclusion "by identifying the most robust and well-supported cluster of arguments."

### 2. Small Model, Big Thinking Budget: Beat the Expensive Model for Less
- **HOOK:** The most expensive model on max effort is often not the cheapest way to get a right answer.
- **THE PROMISE:** For cost-conscious devs, learn to trade model size against inference-time compute and MEASURE which combo wins on your task.
- **THE SHAPE:** (1) Pick a task with a checkable answer (a failing test, a math-heavy refactor); (2) baseline: expensive model, single pass; (3) challenger: cheaper model + higher reasoning effort and best-of-N/self-consistency; (4) score both on accuracy, latency, and token cost; (5) find the knee where extra thinking stops paying and pick the cost-optimal setting.
- **SPINE:** Spine 1 (Scaling Inference Law / thinking budget).
- **SLOT:** Techniques -> Session & Context Management (or Master Claude Code -> The Fundamentals, next to Reasoning Effort).
- **RELATIONSHIP:** 🔗 complements "Reasoning Effort" by being its next step - that video teaches turning one model's effort dial up or down for capability-vs-token-budget. This adds the cross-model economic experiment: swap DOWN to a smaller/cheaper model but spend the saved budget on more inference passes, and prove with numbers whether it matches the big model.
- **PROOF TO REUSE:** "a smaller model, when granted a more substantial 'thinking budget' during inference, can occasionally surpass... a much larger model"; the law balances "Model Size, Response Latency, Operational Cost"; "moving beyond a simple 'bigger is better' paradigm."

### Also film-able (not deep-dived)
- **Build your own Deep Research loop** (generate queries -> web research -> reflect on gaps -> refine -> synthesize with citations). Chapter details the gemini-fullstack-langgraph graph, but Loopy AI likely covers autonomous research loops; would need a Claude-Code-native framing to be net-new.

## 📚 Full wisdom (reference)

SUMMARY (25 words): Gulli surveys reasoning techniques - CoT, Tree-of-Thought, self-correction, PALM, ReAct, multi-agent debate, MASS - that make an agent's thinking explicit and trade inference-time compute for accuracy and reliability.

IDEAS:
- Advanced reasoning allocates more inference-time compute to raise accuracy, coherence, and robustness on hard problems.
- Chain-of-Thought decomposes a hard single-step problem into a transparent sequence of manageable sub-steps.
- "Think step by step" or few-shot exemplars both elicit CoT reasoning from a model.
- CoT's transparency aids debugging and gives auditable, steerable agent behavior in complex environments.
- Tree-of-Thought branches into multiple reasoning paths, enabling backtracking and exploration before finalizing.
- Self-correction is an internal critique loop that reviews and refines output before delivery.
- PALM offloads calculation and logic to executed code, combining LLM generation with deterministic computation.
- Reasoning models spend variable "thinking" time, producing long dynamic CoT thousands of tokens long.
- RLVR trains models on problems with known answers so they learn long-form reasoning unsupervised.
- ReAct interleaves Thought, Action, Observation, letting agents use tools and adapt to feedback.
- Chain of Debates has diverse models argue and critique like AI peer review.
- Graph of Debates models arguments as nodes linked by supports/refutes edges, non-linearly.
- MASS automates multi-agent design by optimizing prompts then topology then whole-system prompts.
- The Scaling Inference Law: performance predictably improves with more inference-time compute.
- A smaller model with a bigger thinking budget can beat a larger single-pass model.
- Deep Research agents take a time budget and iteratively search, reflect, and synthesize reports.
- Thought frequency is tunable - dense for fact-checking, sparse for many-action decision tasks.

INSIGHTS:
- Making reasoning explicit is the foundational capability for both autonomy and user trust.
- Inference-time compute is a design dial, not just model choice, for tuning quality.
- Independent parallel agents share blind spots; adversarial debate surfaces what voting hides.
- Verifiable-reward training lets models evolve reasoning without direct human supervision.
- Deterministic code execution rescues LLMs where symbolic accuracy and consistency fail.
- Optimize individual agents before composing them; then optimize their interaction topology.
- ReAct's observation feedback makes it more robust than linear CoT for dynamic environments.
- "Well-supported" reasoning rests on ground truth, search grounding, or model consensus.

QUOTES:
- "superior results can frequently be achieved from a comparatively smaller LLM by augmenting the computational investment at inference time." - Gulli
- "a smaller model, when granted a more substantial 'thinking budget' during inference, can occasionally surpass the performance of a much larger model." - Gulli
- "This iterative loop of 'Thought, Action, Observation, Thought...' allows the agent to dynamically adapt its plan." - Gulli
- "Chain of Debates (CoD) ... where multiple, diverse models collaborate and argue to solve a problem." - Gulli
- "Functioning as an AI version of peer review, this method creates a transparent and trustworthy record of the reasoning process." - Gulli
- "A conclusion is reached not at the end of a sequence, but by identifying the most robust and well-supported cluster of arguments within the entire graph." - Gulli

HABITS/PRACTICES:
- Prompt the model with an explicit numbered process (analyze, retrieve, synthesize, review, refine).
- Instruct the model to "think step by step" for multi-step reasoning tasks.
- Add a self-correction review step that checks output against original requirements before finalizing.
- Grant a time/compute budget for complex research rather than expecting instant answers.
- Optimize individual agent prompts before wiring them into a multi-agent topology.

FACTS:
- CoT markedly improves performance on arithmetic, commonsense, and symbolic reasoning tasks.
- Reasoning models' extended CoT can run thousands of tokens long.
- RLVR trains on problems with known correct answers (math, code) via trial and error.
- MASS optimized systems outperform manually designed and other automated MAS across tasks.
- Deep Research platforms include Perplexity AI, Google Gemini, and OpenAI ChatGPT functions.
- gemini-fullstack-langgraph-quickstart pairs a React frontend with a LangGraph backend under Apache 2.0.

REFERENCES:
- Papers: Wei et al. 2022 (CoT); Yao et al. 2023 (Tree of Thoughts); Gao et al. 2023 (PALM); Yao et al. 2023 (ReAct); Inference Scaling Laws 2024; Multi-Agent Design / MASS (arxiv 2502.02533).
- Frameworks/tools: Google ADK, LangGraph, Gemini 2.0/2.5, Gemma, Docker, Redis, Postgres, React, Vite, Tailwind, Shadcn UI, LangSmith.
- Concepts: CoT, ToT, PALM, RLVR, ReAct, CoD, GoD, MASS, Scaling Inference Law, Deep Research.

ONE-SENTENCE TAKEAWAY: Spend more compute at inference - decompose, explore, debate, and act - to buy agent accuracy.

RECOMMENDATIONS:
- Write agent prompts as explicit numbered reasoning-then-review processes.
- Add a self-correction pass that critiques a draft against its original requirements.
- Use code execution (PALM-style) for any symbolic or arithmetic step.
- Try a cheaper model with more inference budget before defaulting to the biggest model.
- Replace independent agent voting with a rebuttal round for contested decisions.
- Give research agents a time budget and let them iterate search-reflect-refine.
