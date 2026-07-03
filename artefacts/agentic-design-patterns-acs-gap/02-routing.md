---
title: "Ch 02: Routing -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "02"
pattern: "Routing"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 02: Routing** - Antonio Gulli

> Two buildable videos: a triage router that classifies an incoming request and dispatches it to the right specialist (next step beyond ACS's subagent/skill auto-routing), and a "route deterministically before you reach for an LLM" mechanism-choice lesson that ACS has nowhere.

## The one idea worth a video

- **A routing agent first classifies intent, then dispatches control to a specialized path instead of running one fixed sequence.** This classify-then-dispatch coordinator is the load-bearing idea; every use case in the chapter (support triage, document pipelines, multi-agent dispatch) is the same move with different destinations. VERDICT: 🔗 next-step video available (ACS covers the destinations and Claude's built-in auto-routing, not building the router).
- **The routing decision can be made four ways -> LLM prompt, rule/switch, embedding similarity, or a trained classifier -> and the cheapest deterministic one that works is usually right.** Distinct video: it argues against defaulting to an LLM call for every branch. VERDICT: ❌ net-new video available.

## Summary + counts

Routing adds conditional logic to agents: classify the input, then dynamically direct flow to the right tool, sub-agent, or chain instead of one fixed path.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - The classify-then-dispatch coordinator
THE CLAIM: an adaptive agent should first classify an incoming request, then route control to a specialized handler, rather than forcing every input down one deterministic chain. WHY IT'S NON-OBVIOUS: prompt chaining (Ch 1) trains you to think in fixed linear pipelines; routing argues the first step of a good pipeline is often a decision, not an action. WHY IT'S TRUE / MECHANISM: (1) a single prompt cannot serve booking, info, and technical-support intents well, so quality drops as input variety grows; (2) inserting a router that emits one label ("booker"/"info"/"unclear") lets you attach a purpose-built specialist per label, and each specialist can carry its own tools, model, and instructions. The chapter's LangChain demo is literally `router_chain | RunnableBranch`; the ADK demo achieves the same via `sub_agents=[...]` and Auto-Flow. WHAT IT GENERALIZES TO: agentic coding intake. An unattended loop that ingests GitHub issues, Slack messages, or support tickets needs a triage router that reads each item and dispatches to a bug-fix subagent, a docs subagent, or a human-escalation path. HOW IT GOES WRONG: an over-eager router that never emits "unclear" mis-routes ambiguous requests silently; the chapter deliberately includes an `unclear_handler` fallback, and the ADK note admits its coordinator "doesn't explicitly use it" -> a real failure mode.

### Spine 2 - Choose the routing mechanism deliberately
THE CLAIM: routing can be done with an LLM prompt, predefined rules, embedding similarity, or a fine-tuned classifier -> and these trade flexibility against cost, latency, and determinism. WHY IT'S NON-OBVIOUS: the reflex is "ask the model to decide," but the chapter states rule-based routing "can be faster and more deterministic than LLM-based routing," and ML-model routing "is not a generative model executing a prompt at inference time" -> the decision lives in learned weights or a switch statement, not a token stream. WHY IT'S TRUE / MECHANISM: (1) every LLM routing call adds a full inference round-trip and its variance to the critical path; (2) for stable, keyword-shaped inputs a regex/switch is O(1), free, and never hallucinates a label, while embedding routing gives semantic matching without a generation call. WHAT IT GENERALIZES TO: Claude Code hooks. A `UserPromptSubmit` hook can cheaply pattern-match your request and deterministically inject the right skill, pick Haiku vs Opus, or block-and-redirect -> no LLM classifier needed. HOW IT GOES WRONG: rules are "less flexible for handling nuanced or novel inputs"; picking rules for genuinely fuzzy intent creates a brittle wall of `if` statements that silently mis-routes edge cases.

## 🎬 Proposed ACS videos

### 1. Route Deterministically Before You Reach for an LLM
- **HOOK:** You do not need a model call to decide where a request goes -> a five-line rule router is faster, free, and never hallucinates the label.
- **THE PROMISE:** For anyone wiring intake into an agent loop: after this you can pick the right routing mechanism (rule vs embedding vs LLM) on purpose instead of defaulting to a model call every time.
- **THE SHAPE:** (1) show the naive version -> an LLM classifies every incoming prompt/issue; (2) measure the cost + latency + a mis-classification; (3) rebuild the hot path as a deterministic `UserPromptSubmit` hook that pattern-matches and dispatches (inject skill / pick model / redirect); (4) show where rules break and you escalate to an embedding or LLM router for the fuzzy tail; (5) the rule of thumb -> cheapest deterministic mechanism that handles the input wins.
- **SPINE:** Spine 2.
- **SLOT:** Techniques (fundamental-techniques) -> new "Routing & Dispatch" beat, or Loopy AI intake.
- **RELATIONSHIP:** ❌ net-new -> ACS teaches "add deterministic guardrails" (Agent Introspection) and skill auto-invocation, but no video frames routing-mechanism choice or builds a rule-based dispatcher as an alternative to an LLM call.
- **PROOF TO REUSE:** The four-mechanism taxonomy (LLM / rule / embedding / ML classifier); the exact quote that rule-based routing "can be faster and more deterministic than LLM-based routing, but is less flexible"; the ML-routing point that the decision is "encoded within the fine-tuned model's learned weights," not a prompt.

### 2. Build a Triage Router That Dispatches to Your Specialists
- **HOOK:** Stop hand-picking which subagent to run -> build a coordinator that reads the request, classifies intent, and delegates to the right specialist automatically.
- **THE PROMISE:** For people running multi-subagent or unattended loops: after this you can build an explicit router that triages incoming work to a bug-fix agent, a docs agent, or a human, with an "unclear" fallback.
- **THE SHAPE:** (1) frame the coordinator pattern from the chapter -> classify -> branch -> specialist; (2) build a router skill/slash-command that labels an incoming issue or prompt; (3) wire each label to a purpose-built subagent (own tools, own model); (4) add the `unclear` escalation path so ambiguous work goes to a human instead of the wrong handler; (5) run it on a queue of mixed requests and watch each land on the right specialist.
- **SPINE:** Spine 1.
- **RELATIONSHIP:** 🔗 complements "Nested Subagents" and "Disable Model Invoked Skills" by being their next step -> those videos teach that Claude auto-delegates to subagents and auto-invokes skills from their descriptions (and how to suppress that). This video has you build the router explicitly: a classify-then-dispatch coordinator with your own labels, destinations, and an unclear fallback, so Ray does not re-teach how built-in auto-routing works.
- **PROOF TO REUSE:** The customer-inquiry routing walkthrough (order-status / product-info / technical-support / unclear); the LangChain `coordinator_router_chain | RunnableBranch` structure; the ADK admission that the coordinator "doesn't explicitly use" its `unclear_handler` -> the exact gap to fix on camera.

## 📚 Full wisdom (reference)

SUMMARY: Routing adds conditional logic to agents. The agent classifies an input, then dynamically directs control to the most appropriate tool, sub-agent, or chain instead of one fixed sequence.

IDEAS:
- Prompt chaining handles linear deterministic flows but cannot adapt to contingent, variable inputs.
- Routing introduces conditional logic, shifting an agent from a fixed path to dynamic selection.
- A router first classifies intent, then directs the query to a specialized destination.
- Customer inquiries route by intent: order status, product info, technical support, or clarification.
- LLM-based routing prompts the model to emit a single category label the system reads.
- Rule-based routing uses if-else/switch on keywords -> faster and more deterministic, less flexible.
- Embedding-based routing compares the query vector to route vectors for semantic matching.
- ML-model routing uses a fine-tuned classifier whose logic lives in learned weights, not a prompt.
- Routing can occur at task outset, at intermediate chain steps, or when selecting a tool.
- LangGraph's state-based graph suits routing contingent on accumulated system state.
- Google ADK routes by defining discrete tools/sub-agents and letting the framework match intent.
- A default "unclear" fallback path handles requests the router cannot confidently classify.
- Document pipelines use routing to classify and distribute emails, tickets, and payloads.
- Multi-agent systems use a router as a high-level dispatcher assigning tasks to suitable agents.
- An AI coding assistant routes by language and intent -> debug, explain, or translate.
- Routing transforms a static executor into a dynamic, context-aware decision-making system.

INSIGHTS:
- The first step of a robust pipeline is often a decision, not an action.
- Adding a router lets each destination carry its own tools, model, and instructions.
- Deterministic mechanisms beat LLM routing on cost and latency for stable inputs.
- Flexibility, cost, latency, and determinism trade off across the four routing mechanisms.
- An explicit "unclear" branch is what stops silent mis-routing of ambiguous input.
- ADK hides the router inside the framework; LangGraph makes states and transitions explicit.
- Routing is the control-flow primitive that makes multi-agent delegation possible.
- Semantic routing decides on meaning, not keywords, without a generation call.

QUOTES:
- "Routing introduces conditional logic into an agent's operational framework, enabling a shift from a fixed execution path to a model where the agent dynamically evaluates specific criteria to select from a set of possible subsequent actions." (Gulli)
- "This can be faster and more deterministic than LLM-based routing, but is less flexible for handling nuanced or novel inputs." (Gulli, on rule-based routing)
- "The routing logic is encoded within the fine-tuned model's learned weights." (Gulli, on ML-model routing)
- "Use the Routing pattern when an agent must decide between multiple distinct workflows, tools, or sub-agents based on the user's input or the current state." (Gulli, Rule of Thumb)

HABITS/PRACTICES:
- Always include a default/unclear fallback branch in a router.
- Classify intent to a single canonical label before dispatching.
- Match the routing mechanism to input stability -> rules for stable, LLM/embedding for fuzzy.
- Give each routed destination its own purpose-built handler, tools, and instructions.

FACTS:
- LangChain's `RunnableBranch` routes on a router chain's string output.
- Google ADK enables LLM-driven delegation (Auto-Flow) automatically when `sub_agents` are defined.
- The chapter's demos use gemini-2.5-flash (LangChain) and gemini-2.0-flash (ADK) at temperature 0.
- Embedding-based routing is cross-referenced to RAG in Chapter 14.

REFERENCES:
- LangChain, LangGraph, Google Agent Developer Kit (ADK).
- Google Generative AI (Gemini 2.5-flash, 2.0-flash); `langchain-google-genai`, `google-adk`, pydantic.
- Code author: Marco Fago (MIT-licensed examples).
- LangGraph docs (langchain.com), ADK docs (google.github.io/adk-docs).

ONE-SENTENCE TAKEAWAY: Classify the input first, then dispatch control to the right specialized path instead of one fixed sequence.

RECOMMENDATIONS:
- Build a coordinator that classifies requests and delegates to specialist handlers.
- Add an explicit "unclear" escalation path before shipping any router.
- Prefer a rule or embedding router over an LLM call when inputs are stable.
- Use LangGraph when routing depends on accumulated state; ADK for discrete tool sets.
- Route incoming tickets/emails/issues to per-type workflows in automated pipelines.
