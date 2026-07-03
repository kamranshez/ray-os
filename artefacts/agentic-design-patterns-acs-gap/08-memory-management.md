---
title: "Ch 08: Memory Management -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "08"
pattern: "Memory Management"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 08: Memory Management** - Antonio Gulli

> Two film-able angles: a self-improving "Reflection" loop where Claude rewrites its own CLAUDE.md/skill from a finished session (next step beyond manual rule-adding), and a net-new build giving an agent an auto-populated long-term memory that persists and is searched across sessions. Short-term context management is already covered.

## The one idea worth a video

- **Procedural memory means an agent can rewrite its own instructions from experience -> a Reflection loop, not a human hand-editing rules.** This is the spine because it flips CLAUDE.md from a file you maintain into a file the agent maintains; it subsumes "add a rule after repeated mistakes" by automating the add. VERDICT: 🔗 next-step video available.
- **Long-term memory is a separate, persistent, searchable store the agent writes facts into and recalls across sessions -> not the context window, not a static config file.** Distinct spine: the demo is building the store and the write/recall loop, not editing instructions. VERDICT: ❌ net-new video available.
- **Short-term memory is the ephemeral context window; you manage it by summarizing/compacting, and it is lost at session end.** VERDICT: ✅ already covered (kept for context).

## Summary + counts

Agents need short-term (context window) and long-term (external, searchable) memory; ADK and LangGraph supply Session, State, MemoryService, and stores for semantic, episodic, procedural recall.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Procedural memory via Reflection (self-editing instructions)
THE CLAIM: an agent's core behavior lives in its instructions (system prompt / CLAUDE.md), and the agent itself can be prompted to reflect on a recent interaction and rewrite those instructions to do better next time. WHY IT'S NON-OBVIOUS: the default treats the system prompt as human-authored and fixed; the book instead calls it "procedural memory" and says "it's common for agents to modify their own prompts to adapt and improve." WHY IT'S TRUE / MECHANISM: (1) the failure signal already exists in the transcript - the model has the conversation plus its current instructions in context; (2) so a reflection node can "ask the LLM to reflect on the conversation and generate new, improved instructions," then persist them back to a store keyed under a namespace like `("instructions",)`. The next run loads the improved version. WHAT IT GENERALIZES TO: agentic coding - Claude Code finishes a task, you ask it to diff what went wrong against its own CLAUDE.md/skill and commit the fix as a durable rule. That is exactly ACS's "add a rule after repeated mistakes," but automated as a loop the agent runs on itself. HOW IT GOES WRONG: unconstrained self-rewrites drift, bloat the instruction budget, or overfit one session's quirk into a permanent rule - you need a human gate and a size cap.

### Spine 2 - Long-term memory as a persistent, searchable store across sessions
THE CLAIM: durable knowledge should live outside the context window in an external store the agent writes to and later queries by semantic similarity, so it survives session end and is shared across threads. WHY IT'S NON-OBVIOUS: with long-context models the tempting default is "just keep everything in the window," but Gulli warns context "is still ephemeral and is lost once the session concludes, and it can be costly and inefficient to process every time." WHY IT'S TRUE / MECHANISM: (1) memories are stored under a namespace + key (LangGraph) or extracted automatically (Vertex Memory Bank "asynchronously analyze[s] conversation histories to extract key facts and user preferences," then "consolidate[s] new data and resolve[s] contradictions"); (2) on a new session the agent does "a similarity search using embeddings" and injects only the relevant facts back into short-term context. WHAT IT GENERALIZES TO: agentic coding - give Claude Code a `memory/` directory or a memory MCP it appends durable facts to (your stack choices, past bug fixes, preferences) and greps/searches at session start, so it stops re-learning you every time. HOW IT GOES WRONG: stale or contradictory memories poison retrieval; without a consolidation/dedup step the store grows into noise the agent trusts blindly.

### Spine 3 - Short-term memory is the ephemeral context window (covered)
THE CLAIM: for LLM agents short-term memory just IS the context window - recent messages, tool results, reflections - with limited capacity, managed by "summarizing older conversation segments or emphasizing key details," and lost at session end. WHY IT'S NON-OBVIOUS to newcomers: they conflate "long context" with "memory," but a bigger window is still ephemeral working memory, not persistence. MECHANISM: capacity is finite, so relevance-ranking and summarization keep the useful bits resident; LangGraph persists this via a checkpointer so a thread can resume. WHAT IT GENERALIZES TO: agentic coding - this is precisely /compact, /context, /new, prompt-cache economics, and context-poisoning avoidance. HOW IT GOES WRONG: overstuffed windows degrade reasoning ("context poisoning, distraction, confusion, clash"). ACS already teaches this end to end, so no new pitch here - it grounds why the two long-term spines matter.

## 🎬 Proposed ACS videos

### 1. Give Your Agent a Long-Term Memory It Actually Recalls
- **HOOK:** Claude forgets everything the moment the session ends - so build it a memory that survives.
- **THE PROMISE:** For devs tired of re-explaining their stack and preferences every session, a persistent memory layer Claude writes to and reads back across sessions and projects.
- **THE SHAPE:** (1) Name the failure: long context is not memory - it dies at session end. (2) Stand up a `memory/` store (or a memory MCP) with a namespaced write path. (3) Have Claude, after solving a bug, append a durable fact ("we use pnpm, not npm"; "auth lives in x"). (4) New session: Claude searches memory first, pulls only relevant facts into context. (5) Add a consolidation pass that dedups and resolves contradictions so the store stays clean.
- **SPINE:** Spine 2.
- **SLOT:** Context Engineering (new chapter: Long-Term Agent Memory), or Techniques -> Session & Context Management.
- **RELATIONSHIP:** ❌ net-new. ACS covers CLAUDE.md as hand-curated project config and context-window management, but nothing on an auto-populated, searchable memory the agent grows and recalls across sessions.
- **PROOF TO REUSE:** Gulli's warning that context "is lost once the session concludes"; Vertex Memory Bank "extract[s] key facts and user preferences" then "consolidate[s] new data and resolve[s] contradictions"; the semantic/episodic/procedural taxonomy as the framing spine.

### 2. Let Claude Rewrite Its Own CLAUDE.md (Reflection Loop)
- **HOOK:** Stop hand-editing your rules file after every mistake - make the agent do it.
- **THE PROMISE:** For devs whose CLAUDE.md only improves when they remember to fix it, a reflection loop where Claude reviews a finished session and commits its own rule fix.
- **THE SHAPE:** (1) Finish a task where Claude made an avoidable mistake. (2) Prompt the reflection step: "here are your current instructions and this conversation - propose an improved rule." (3) Claude diffs against CLAUDE.md / a skill and drafts the edit. (4) Human-gate the change (accept/reject) and cap instruction budget. (5) Next session proves the rule now fires.
- **SPINE:** Spine 1.
- **SLOT:** Loopy AI (self-improving agent loop) or Master Claude Code -> CLAUDE.md.
- **RELATIONSHIP:** 🔗 complements "CLAUDE.md Best Practices" - that video teaches you to add rules manually only after repeated mistakes and keep the instruction budget lean; this is the next step: the agent runs that add-a-rule move on itself as a Reflection loop, with a human gate so it does not drift.
- **PROOF TO REUSE:** "it's common for agents to modify their own prompts to adapt and improve"; the `update_instructions` reflection node that asks the LLM to "generate new, improved instructions" and `store.put`s them back; procedural memory = "the memory of how to perform tasks."

## 📚 Full wisdom (reference)

### SUMMARY
Gulli explains agent memory as short-term (the ephemeral context window) plus long-term (external, searchable stores), demonstrated with Google ADK's Session/State/MemoryService and LangGraph.

### IDEAS
- Agent memory is the ability to retain and use information from past interactions and observations.
- Short-term memory is working memory living inside the LLM's limited context window.
- Long-context models only enlarge short-term memory; it stays ephemeral and dies at session end.
- Long-term memory persists outside the agent in databases, knowledge graphs, or vector stores.
- Vector databases enable semantic-similarity retrieval instead of exact keyword matching.
- Retrieval means query the store, pull relevant data, inject it into short-term context.
- ADK splits context into three concepts: Session, State, and Memory.
- Session is one chat thread logging Events plus temporary State.
- State is a key-value dictionary scoped by prefixes: none, `user:`, `app:`, `temp:`.
- Update State only via `output_key` or `EventActions.state_delta`, never by mutating the dict directly.
- MemoryService is the searchable long-term store, populated by `add_session_to_memory`.
- Long-term memory subdivides into semantic (facts), episodic (experiences), procedural (rules).
- Episodic memory is often implemented as few-shot examples of past successful task sequences.
- Procedural memory is the agent's instructions; Reflection lets it rewrite them.
- LangGraph stores memories as JSON under a namespace + key, searchable by similarity.
- Vertex Memory Bank auto-extracts facts, consolidates them, and resolves contradictions.
- LangChain's ConversationBufferMemory auto-injects a chat buffer into the prompt.
- `return_messages=True` gives chat models structured message objects instead of a string.
- Without memory, agents are stateless and limited to one-shot interactions.

### INSIGHTS
- A bigger context window is not persistence; it is just more expensive working memory.
- Persistence requires moving knowledge out of the model and into a searchable store.
- The strongest agentic move is procedural: the agent editing its own operating rules.
- Scoping memory (session/user/app/turn) is what makes personalization and multi-tenancy tractable.
- Automatic consolidation and contradiction-resolution are what separate a memory store from a junk drawer.
- Routing all writes through an event/append mechanism buys you history, persistence, and safe concurrency.
- Human memory's semantic/episodic/procedural split is a usable engineering taxonomy, not just analogy.

### QUOTES
- "For agents using large language models (LLMs), short-term memory primarily exists within the context window."
- "This context is still ephemeral and is lost once the session concludes, and it can be costly and inefficient to process every time."
- "It's common for agents to modify their own prompts to adapt and improve. An effective technique is 'Reflection,' where an agent is prompted with its current instructions and recent interactions, then asked to refine its own instructions."
- "The service uses Gemini models to asynchronously analyze conversation histories to extract key facts and user preferences."
- "This information is stored persistently... and intelligently updated to consolidate new data and resolve contradictions."
- "Direct modification of the `session.state` dictionary after retrieving a session is strongly discouraged as it bypasses the standard event processing mechanism."

### HABITS / PRACTICES
- Keep state simple: basic data types, clear key names, correct prefixes, avoid deep nesting.
- Always update state through the `append_event` process, never by direct mutation.
- Use `output_key` for simple text saves; `state_delta` for multi-key or scoped updates.
- Encapsulate state changes inside tools to co-locate logic and stay robust.
- Use in-memory services for testing, database/cloud services for production persistence.
- Set `return_messages=True` when wiring memory into chat models.

### FACTS
- ADK ships InMemory, Database, and VertexAi implementations for both Session and Memory services.
- InMemory services lose all data across application restarts.
- LangGraph short-term memory is persisted via a checkpointer, enabling thread resume.
- Vertex Memory Bank supports ADK, and via API also LangGraph and CrewAI.
- LangGraph memories are JSON documents keyed by namespace + key.
- `VertexAiRagMemoryService` exposes `similarity_top_k` and `vector_distance_threshold` knobs.

### REFERENCES
- Google Agent Developer Kit (ADK) - Session, State, MemoryService, Runner.
- LangChain - ChatMessageHistory, ConversationBufferMemory, LLMChain.
- LangGraph - InMemoryStore, BaseStore, checkpointer, namespaces.
- Vertex AI Agent Engine Memory Bank; VertexAiRagMemoryService; VertexAiSessionService.
- CrewAI (via Memory Bank API); Gemini models; RAG (cross-ref chapter 14).
- Docs: ADK Memory, LangGraph Memory, Vertex AI Memory Bank public preview.

### ONE-SENTENCE TAKEAWAY
Give agents an ephemeral context for now and an external, searchable store for lasting knowledge.

### RECOMMENDATIONS
- Split every agent's memory explicitly into short-term context and long-term external store.
- Scope long-term memories by user/app so personalization and tenancy stay clean.
- Add a consolidation step that dedups facts and resolves contradictions on write.
- Try a Reflection loop that lets the agent propose edits to its own instructions.
- Store episodic successes as retrievable few-shot examples for repeat tasks.
- Never mutate session state directly; route changes through the append-event mechanism.
