---
title: "Ch 16: Resource-Aware Optimization -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "16"
pattern: "Resource-Aware Optimization"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 16: Resource-Aware Optimization** - Antonio Gulli

> Two film-able videos: a net-new "fallback model chains / graceful degradation on rate-limit" video, plus a complement to /model that builds an automatic complexity-router instead of choosing models by hand.

## The one idea worth a video

- **Build an automatic router that classifies each request's difficulty and dispatches it to the cheapest model that can still do the job.** This is the load-bearing idea of the chapter - the Router Agent, the Critique-Agent feedback loop, and dynamic model switching all hang off it. VERDICT: 🔗 next-step video available (complements manual /model selection).
- **Wire a fallback chain so the system silently drops to a backup model when the primary is overloaded, throttled, or rate-limited - graceful degradation instead of a hard failure.** Distinct demo (fallback config, forced failure, recovery) and distinct "one thing after," so it de-merges from the router. VERDICT: ❌ net-new video available.
- **Cut token cost by pruning and summarizing the context you carry between steps.** Real but ACS already teaches this thoroughly. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Resource-Aware Optimization lets agents monitor compute, time, and money mid-run, routing simple queries to cheap models, complex ones to powerful models, with fallback for reliability.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Automatic complexity router
THE CLAIM: instead of one model for everything, a Router Agent should classify each incoming request's complexity and forward it to the cheapest model that can still succeed. WHY IT'S NON-OBVIOUS: the default is to pick one good model and pay its price on every call, including the trivial ones; the chapter argues the *classification* itself is worth a cheap LLM call because it saves far more downstream. WHY IT'S TRUE: Gulli's example routes a factual-recall query to Gemini Flash and a deep-analysis query to Gemini Pro, using either a crude metric ("query length") or a real classifier that returns `simple / reasoning / internet_search`. Because most real traffic is skewed toward easy requests, routing collapses average cost while preserving quality on the hard tail. A Critique Agent then watches outputs and feeds "this Flash answer was inadequate" back into the router, so the boundary self-corrects over time. WHAT IT GENERALIZES TO: agentic coding - Claude Code and Codex already expose model choice per session (/model), per skill, and per subagent (Explore on Haiku vs Sonnet). The next step is a *declarative router*: a skill or router subagent that reads the task and picks Haiku for boilerplate, Sonnet for features, Opus for gnarly debugging - no human toggling. HOW IT GOES WRONG: a mis-tuned classifier sends a hard query to the cheap model and ships a wrong answer; and the classifier call itself adds latency and cost if the threshold is set badly.

### Spine 2 - Fallback chains and graceful degradation
THE CLAIM: a production agent should specify a hierarchical list of models so that when the primary "fails to respond due to service unavailability, rate-limiting, or content filtering," the system re-routes to the next model automatically. WHY IT'S NON-OBVIOUS: most developers treat model choice as a single fixed string and let the whole run crash on a 429 or an overload; the chapter reframes availability as a resource to manage, not an assumption. WHY IT'S TRUE / MECHANISM: OpenRouter's `models: [primary, backup]` array tries each in sequence until one succeeds, and the returned metadata tells you which one actually ran and what it cost. Because the fallback is silent, the user sees continuity ("maintaining service continuity instead of failing completely") rather than an error - degraded quality beats zero output. WHAT IT GENERALIZES TO: agentic coding under real usage limits - Claude Code exposes a fallback model on overload, Codex hits rate limits, and OpenRouter/LiteLLM let you chain providers. This is a concrete, demo-able config you can force-fail and watch recover. HOW IT GOES WRONG: a silent downgrade can mask a real outage you needed to know about, and a cheaper fallback can quietly produce worse code that slips through if nothing flags the switch.

### Spine 3 - Contextual pruning for cost (covered)
THE CLAIM: strategically summarize and drop history to "minimize the prompt token count and reduce inference costs" without losing the relevant signal. WHY IT'S TRUE: token count drives both cost and latency linearly, so trimming stale turns compounds across a long session. WHAT IT GENERALIZES TO: this is squarely ACS's existing territory - "Economising with Prompt Cache," "Context Window Management," "Long Context Failure," /compact and /context all teach exactly this trade-off for Claude Code sessions. No net-new video here; kept for completeness because it is one of the chapter's four headline optimizations.

## 🎬 Proposed ACS videos

### 1. Fallback Models So Your Agent Never Hard-Fails
- **HOOK:** You hit the rate limit mid-run and the whole agent dies - here's how to make it silently drop to a backup instead.
- **THE PROMISE:** For anyone running agents under real usage limits: after this you can configure a fallback chain that degrades gracefully instead of crashing on overload or 429s.
- **THE SHAPE:** (1) Show a run dying on an overload / rate-limit error. (2) Configure Claude Code's fallback-on-overload model. (3) Show the OpenRouter `models: [primary, backup]` sequential-fallback pattern and how the response tells you which model actually ran. (4) Force the primary to fail and watch the backup catch it. (5) Add a log line so the silent switch is still visible to you.
- **SPINE:** Spine 2 (fallback chains and graceful degradation).
- **SLOT:** Advanced Techniques -> new chapter "Reliability & Fallbacks" (or Loopy AI, since unattended loops most need this).
- **RELATIONSHIP:** ❌ net-new. Catalog searches for "fallback model when primary unavailable / rate limited" surfaced /model and context videos but nothing on fallback chains or graceful degradation on overload.
- **PROOF TO REUSE:** OpenRouter's "Sequential Model Fallback" description ("service unavailability, rate-limiting, or content filtering"); the `{"models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"]}` snippet; Gulli's framing "maintaining service continuity instead of failing completely."

### 2. Auto-Routing Tasks to the Cheapest Model That Works
- **HOOK:** Stop paying Opus prices to rename a variable - let a router pick the model for each task automatically.
- **THE PROMISE:** For devs burning limits on trivial work: after this you can build a router skill/subagent that sends boilerplate to Haiku, features to Sonnet, hard debugging to Opus - no manual /model toggling.
- **THE SHAPE:** (1) Recap manual /model and per-skill model choice as the baseline. (2) Build a lightweight classifier prompt that labels a task simple/reasoning/complex. (3) Route each label to a different model via skill frontmatter or a router subagent. (4) Add a critique check that flags when the cheap model under-delivered, tightening the threshold. (5) Compare cost across a mixed task batch.
- **SPINE:** Spine 1 (automatic complexity router).
- **SLOT:** Advanced Techniques -> "Multi-Model & Multi-CLI Workflows" (sits next to "Combining CLIs & Models").
- **RELATIONSHIP:** 🔗 complements "/model" (Master Claude Code) by being its next step - "/model" teaches choosing Opus vs Sonnet by hand for hard vs easy work; this adds the automatic classifier that makes that choice per-task without you touching it. Also builds on "How Models Switch with Skills" (per-skill model switching) by adding the difficulty-classification layer that decides which skill/model to invoke. Do not re-teach manual model selection or the skills model-switch mechanics.
- **PROOF TO REUSE:** The three-way `simple / reasoning / internet_search` classifier and its system prompt; the travel-planner split (Pro plans, Flash executes tool calls); the Critique Agent's role in "identifying suboptimal routing choices ... which informs adjustments that improve resource allocation."

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** Resource-Aware Optimization lets agents monitor compute, time, and money mid-run - routing simple queries to cheap models, complex ones to powerful models, with fallback for reliability.

**IDEAS:**
- Resource-Aware Optimization manages computational, temporal, and financial resources dynamically during operation, beyond simple action sequencing.
- Agents choose between accurate-but-expensive models and faster-cheaper ones based on budget and time.
- A Router Agent classifies incoming request complexity, then forwards it to the most suitable model.
- Crude routing uses query length; sophisticated routing uses an LLM/ML classifier of nuance.
- Fallback mechanisms safeguard against a preferred model being overloaded or throttled.
- Graceful degradation switches to a default or cheaper model to keep service running.
- A Critique Agent evaluates responses, feeding back to refine routing logic over time.
- Critique feedback indirectly manages budget by catching mis-routed simple/complex queries.
- Hierarchical agents use a powerful planner and cheap models for repetitive tool calls.
- Travel-planner example: Gemini Pro plans the itinerary, Gemini Flash runs the web lookups.
- OpenRouter offers one API for hundreds of models with automated failover and cost-optimization.
- OpenRouter "Automated Model Selection" (openrouter/auto) routes based on prompt content.
- OpenRouter "Sequential Model Fallback" tries a hierarchical model list until one succeeds.
- Prompt tuning and fine-tuning the router LLM improve routing accuracy over time.
- Additional levers: adaptive tool selection, contextual pruning, proactive resource prediction.
- Contextual pruning and summarization minimize prompt token count and inference cost.
- Learned resource allocation policies adapt strategy from feedback and performance metrics.
- Energy-efficient deployment matters for edge devices with limited battery.
- Parallelization and distributed-computing awareness raise throughput across machines.
- The core tension is a quality-vs-resource trade-off with no free lunch.

**INSIGHTS:**
- Availability is a resource to manage, not an assumption; fallback chains encode that.
- The classifier call is worth its cost because most traffic is trivial.
- Silent degradation preserves user trust better than a hard failure.
- Routing intelligence can live in a cheap model that guards an expensive one.
- A critique loop turns routing from static config into a self-correcting policy.
- Hierarchical agents naturally separate expensive reasoning from cheap execution.
- Cost, latency, and energy are distinct budgets that can each drive model choice.
- Optimization is inseparable from evaluation - you tune what you measure.

**QUOTES:**
- "Resource-Aware Optimization enables intelligent agents to dynamically monitor and manage computational, temporal, and financial resources during operation." - Gulli
- "To ensure graceful degradation, the system automatically switches to a default or more affordable model, maintaining service continuity instead of failing completely." - Gulli
- "A Router Agent can direct queries based on simple metrics like query length, where shorter queries go to less expensive models and longer queries to more capable models." - Gulli
- "Should this primary model fail to respond due to any number of error conditions - such as service unavailability, rate-limiting, or content filtering - the system will automatically re-route the request to the next specified model in the sequence." - the book (OpenRouter)
- "While not directly managing the budget, the Critique Agent contributes to indirect budget management by identifying suboptimal routing choices." - Gulli

**HABITS/PRACTICES:**
- Classify each request's complexity before choosing a model.
- Reserve powerful models for planning/reasoning; use cheap models for repetitive tool calls.
- Specify a hierarchical fallback list so overload never hard-fails.
- Run a critique pass to catch and correct mis-routed queries.
- Prune and summarize context to hold down token spend.

**FACTS:**
- Google's ADK supports multi-agent architecture, model flexibility, and LLM-driven routing.
- LiteLLM lets ADK integrate models beyond Gemini.
- The OpenAI example routes to gpt-4o-mini (simple), o4-mini (reasoning), gpt-4o (search).
- OpenRouter exposes hundreds of models behind one endpoint with a token-production leaderboard.
- The chapter's code example is MIT-licensed, authored by Mahtab Syed, on GitHub.

**REFERENCES:**
- Google Agent Development Kit (ADK) - https://google.github.io/adk-docs/
- Gemini 2.5 Pro and Gemini 2.5 Flash - https://aistudio.google.com/
- OpenRouter (openrouter/auto, sequential fallback, rankings) - https://openrouter.ai/docs/quickstart
- LiteLLM (model integration layer)
- OpenAI models: gpt-4o, gpt-4o-mini, o4-mini
- Google Custom Search API / CSE
- Mahtab Syed - 21-Agentic-Patterns GitHub repo

**ONE-SENTENCE TAKEAWAY:** Classify each task's difficulty, route it to the cheapest capable model, and fall back gracefully when that model is unavailable.

**RECOMMENDATIONS:**
- Add a complexity classifier in front of your agent to route cheap vs expensive.
- Configure a fallback model chain so rate limits degrade instead of crash.
- Split hierarchical agents so a strong planner delegates cheap execution tasks.
- Log which model actually served each request to audit routing decisions.
- Add a critique pass and use its verdicts to retune routing thresholds.
- Prune and summarize carried context to cut token cost on long runs.
