---
title: Event Driven Agent Loops #30
videoId: _VB9TT1Vus4
url: https://www.youtube.com/watch?v=_VB9TT1Vus4
date: 2026-07-01
status: posted
source: BoundaryML "AI that works" (Vaibhav / BAML + guest Anders / SageKit)
---

## The one idea worth a video

**Spine 1 — Model a complex agent as an append-only event log, and derive every view (UI, LLM context, control state) as a pure projection of that log, instead of mutating one central state object.** This single reframe subsumes queuing, interruptions, testability, forking, and persistence: they all fall out for free once events, not state, are the source of truth.
VERDICT: net-new video available.

**Spine 2 (de-merged) — Your LLM context window is a projection you compute from history, not a message list you append to.** The easy path (append role/content, feed the same list to UI and model) breaks once UI-truth and LLM-truth diverge; a projection function lets you decide exactly what the model sees while keeping the full log for audit.
VERDICT: next-step video available (complements the Context Engineering class).

## Summary

Vaibhav (BAML) and guest Anders (SageKit) whiteboard and code an event-driven agent architecture where an append-only event log, not mutable state, drives interactive chat systems.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — The agent as an event log

The claim: stop holding a mutable state object as the source of truth for a chat agent; keep an append-only array of typed events and recompute every piece of state as a pure function (a projection) of that array. Non-obvious because the default instinct is exactly the opposite: initialize one state object and mutate it as messages stream, queue, or get interrupted. That feels simpler, and for a plain back-and-forth bot it is. Why it is true: a rich agent needs three views that genuinely diverge, what the user sees, what the LLM sees, and what gets persisted. With one mutable object you must hand-synchronize all three, and Anders describes exactly how that "became very unwieldy" and drifted out of sync. If events are the only truth, each view becomes an independent read-only projection, so they cannot desync, and the backend can deterministically dictate what the frontend should render at any timestamp. Queuing becomes "push an event"; interrupt becomes "spawn a fresh event." It generalizes cleanly to multiplayer game netcode, where an authoritative server reconciles a lagging, "lying" client. It goes wrong two ways: it is real overkill for simple agents, and you must choose persistence timing deliberately (never mid-stream).

### Spine 2 — The context window is a projection

The claim: your LLM context window is not an append-only message list, it is one projection among several that you compute from the full event history by deciding precisely what the model should see. Non-obvious because the easy path is appending {role, content} to a list and feeding that same list to both the UI and the LLM. Vaibhav names the trap: "your context window is also really just a projection of this state," a function that turns the event array into a chat prompt. Why it is true: the raw log is full of stream chunks, interrupts, queued messages, tool-parse events, and OAuth states that are noise to the model. Feed them raw and you bloat and confuse context. By writing a projection that maps clean message state to role/content pairs, keeping only final responses, stripping interruptions, and reconstructing tool calls in Anthropic's internal XML, you control exactly what enters the window while the untouched log preserves full auditability. It generalizes to CQRS read models and RAG memory pipelines, where the write model and read model deliberately differ. It goes wrong when a wrong projection silently drops needed context, and you now own reconstructing formats the SDK used to hand you.

---

## 🎬 Proposed ACS videos (ranked)

### 1. Stop Mutating State: Build Your Agent as an Event Log

- HOOK: "The chat loop is so disgusting to maintain forever." Here is the architecture that kills that pain.
- THE PROMISE: For engineers building interactive agents (chat, coding, workflow), after this you can rebuild your agent so every view is a projection of one append-only event log, and queuing plus interrupts stop being special cases.
- THE SHAPE:
  1. The pain: mutable state desyncs across backend, frontend, and LLM as interactivity grows.
  2. Whiteboard the reactive loop: frontend sends events, backend appends to a DB, frontend listens for state.
  3. Show state as a projection: message state, UI state, and LLM-memory state all derived from one array.
  4. Demo how queuing and interrupts collapse into "push an event" / "spawn a fresh event."
  5. Show that testability and conversation forking fall out for free.
- SPINE: 1
- SLOT: Techniques (new agent-architecture chapter, positioned next to the backlog "core-agent-loop" topic).
- RELATIONSHIP: ❌ net-new. The nearest catalog item is the unfilmed backlog title "core-agent-loop" (Techniques), which would teach the standard while-loop / context-window agent loop; this is the alternative reactive, event-sourced model that sits beyond it, and no filmed ACS video covers event sourcing for agents.
- PROOF TO REUSE: "you don't keep the state object as your representation of truth, you have an event history"; "everything is just basically a pure function of the events that actually occurred"; the multiplayer-game "what you show the user is always some variation of a lie" analogy; queuing = one event pushed to the array, drained when the current action finishes.

### 2. Your Context Window Is a Projection, Not a Message List

- HOOK: You are appending messages to a list. That is exactly why your context is a mess.
- THE PROMISE: For anyone hand-building an agent loop, after this you can write a projection function that turns your full history into precisely the context the LLM should see, decoupled from your UI.
- THE SHAPE:
  1. The default: append {role, content} and feed the same list to both UI and LLM.
  2. Why it breaks: UI-truth and LLM-truth diverge as the agent gets complex.
  3. Build the LLM-memory projection: strip stream chunks, interrupts, and cruft; keep only final responses.
  4. Reconstruct tool calls in Anthropic's internal XML format so the model stays in sync.
  5. Side by side: the full event array versus the lean context the model actually receives.
- SPINE: 2
- SLOT: Context Engineering class (shipped, 13 videos).
- RELATIONSHIP: 🔗 complements the Context Engineering class. That class already teaches how to curate and compact context; this adds the architectural move of treating the context window as one projection among several derived from an event log, decoupled from UI state, so Ray does not re-teach general context curation.
- PROOF TO REUSE: "your context window is also really just a projection of this state... you turn it into a chat prompt"; "what you want to show on your UI is no longer the same as what you want to show to the LLM"; "everyone needs a different version of the truth"; mimic Anthropic's internal XML format for function calls.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BAML) and guest Anders (SageKit) whiteboard and code an event-driven agent architecture where an append-only event log, not mutable state, drives interactive chat systems.

### IDEAS
- You model your agent as an append-only array of events rather than one mutable state object.
- State becomes a pure function (projection) of the event history, recomputed every time you need it.
- Different consumers each need a different projection: the UI view differs from the LLM context view.
- "What you show the user is always some variation of a lie," never the raw truth.
- Queuing a message just pushes an event onto the array; the next finish handler drains it.
- Interrupts resemble queuing: you skip adding events and spawn a fresh event as if it restarted.
- Building agents resembles multiplayer video games: clients lag, so the server reconciles one authoritative world state.
- The event log makes agents testable: assert the interrupt button's availability given a specific event sequence.
- Fork any conversation by copying the event array up to a chosen point, then continuing onward.
- Your database is literally just one array of events stored in a single typed discriminated-union column.
- Persistence timing is a deliberate choice: don't save mid-stream or during invalid interrupted states; wait strategically.
- Claude Code's message queuing, unlike Cursor's cancel-and-resend, felt foundationally different, much like Amazon's subtle one-click checkout.
- Effect TS structures the streams-feeding-streams architecture, offering error handling, piping, and stream transformations for resilient TypeScript.
- An event bus lets services publish and subscribe, decoupling who produces from who perceives the events.
- The LLM's function calls use Anthropic's internal XML format, so mimic whatever the models use internally.
- The event paradigm mirrors database transactions: append logs that eventually reconcile into one consistent final state.

### INSIGHTS
- Event sourcing removes the desync between backend and frontend state that plagues traditional mutable-state chat systems.
- Interaction complexity, not chat length, justifies event sourcing; simple back-and-forth agents make it obviously complete overkill.
- The reactive queues-of-events model replaces the naive while-loop mental model most developers hold of an agent.
- Decoupling UI truth, LLM truth, and stored truth prevents the paradigm-mixing that makes chat loops unmaintainable.
- A deterministic backend-dictated frontend makes agent behavior unit-testable without manually running both ends together each time.
- Context engineering becomes explicit: you decide precisely which events project into the LLM's final context window.
- Preserving raw history while purging what the LLM sees keeps context clean without losing full auditability.
- Mid-run pipeline edits should diff against the running plan, not discard fifteen minutes of collected work.
- Like React's useState, the small upfront complexity of events pays off once interactivity grows sufficiently substantial.

### QUOTES
- "What you show to the user is always some variation of a lie." — Anders
- "It's not that you don't have a state object, it's that you don't keep the state object as your representation of truth. You have an event history." — Vaibhav
- "What if everything is just basically a pure function of the events that actually occurred." — Anders
- "The chat loop is so disgusting to maintain forever." — Vaibhav
- "Every agent task isn't actually a whole loop. It's actually a system that's just adding a new event through a massive like event log of what's happening." — Vaibhav
- "What you want the user to perceive is different from the truth and it's different from what you want the LLM to see." — Anders
- "Your context window is also really just a projection of this state. You take this state and you turn it into a chat prompt." — Vaibhav
- "The analogy that I've always personally found here is actually video games." — Vaibhav
- "Once you model the world in this way where it's just like a sequence of elements that are being collected, writing code for this is actually very simple." — Vaibhav
- "If you're building a simple back and forth chat agent, like this is completely overkill." — Anders

### HABITS
- Whiteboard the system architecture before writing any code, then get to coding as soon as possible.
- Delegate unfamiliar library code, like Effect TS, to Claude Code rather than struggling writing it yourself.
- Follow Claude Code's queuing model: accumulate queued messages, resolve them all together once the streaming finishes.
- Mimic Anthropic's internal XML function-call format when prompting Anthropic models to invoke their own tools reliably.
- Prototype a new architecture in a throwaway demo before touching the real production chat app first.
- Ban user input during specific windows when interruptions should not be allowed in the current flow.
- Debug state by hardcoding an initial condition, like React, then inspecting exactly how it actually renders.
- Commit the runnable demo code to the shared repo so viewers can run experiments themselves afterward.

### FACTS
- Magnitude, Anders's open-source browser agent, still ranks number one on benchmarks and trended on Hacker News.
- SageKit, Anders's YC S25 startup, is a chat-driven workflow automation platform, like ChatGPT meets Zapier essentially.
- Claude Code queued messages at launch; Cursor and everyone else later copied its interruption behaviors eventually.
- Multiplayer games favor the shooter: if your screen shows a hit, the server registers the kill.
- Effect TS is a TypeScript library for resilient systems: error handling, streams, piping, and data transformations.
- Amazon's one-click buy is cited as a subtle UI innovation that makes an enormous practical difference.
- AI that works streams live every Tuesday at 10am for roughly one hour, prioritizing coding quickly.
- The demo backend runs on Bun, uses bun.serve, and receives websocket connections from the frontend directly.

### REFERENCES
- BAML (Vaibhav's project / the show's host company)
- SageKit (Anders's YC S25 startup: chat-driven workflow automation)
- Magnitude (Anders's earlier open-source browser-agent project)
- "12-factor agents" / selecting a thousand tools from MCP (referenced prior episode)
- Effect TS (TypeScript library for resilient systems, streams, error handling)
- Bun / bun.serve (backend runtime for the demo)
- Claude Code (used live to write Effect persistence code; queuing model referenced)
- Cursor (contrasted interruption behavior)
- Reddit / r/LangChain (the demo scrape target); LangChain (complaint topic)
- Gemini (used in the demo pipeline to analyze complaints)
- Excalidraw (whiteboarding tool used live)
- Anthropic models (internal XML function-call format imitated)
- Amazon one-click buy (subtle UI innovation analogy)
- React / useState (state-debugging and complexity-payoff analogy)
- Hacker News, YC (S25 batch), BAML Discord, websockets

### ONE-SENTENCE TAKEAWAY
Model complex agents as an append-only event log; derive every view as a pure projection.

### RECOMMENDATIONS
- Replace your mutable chat-state object with an append-only event array as the single source of truth.
- Write projection functions that derive UI state, LLM context, and message state from one shared log.
- Implement queuing by pushing an event, then draining the queue when the current action fully finishes.
- Store all your events in a single discriminated-union database column, grouped by user and conversation ID.
- Write tests asserting expected UI affordances at each point given a specific sequence of recorded events.
- Add conversation forking and time-travel by copying the event array up to any chosen point instantly.
- Skip event sourcing for simple back-and-forth agents; reserve it only for genuinely complex multi-state interactive systems.
- Delegate Effect TS code to Claude Code and review the resulting git diff before accepting it.
- Diff mid-run pipeline edits against the running plan instead of discarding all in-progress collected work entirely.
