---
video_id: 9MFiATinGC0
title: "Streaming Systems Masterclass"
url: https://www.youtube.com/watch?v=9MFiATinGC0
channel: BoundaryML
---

## SUMMARY

Vibhav (Boundary/BAML) and Dex (HumanLayer) teach streaming system architecture, building a parallel async web-scraping agent with SSE, demonstrating real-time UI updates and incremental field streaming.

## IDEAS

- Streaming feels magical but reduces to basic system design with surprisingly minimal complexity once internalized.
- Most apps skip streaming because adding it later requires infinite plumbing through every existing function call.
- Deep Research and Perplexity feel premium because incremental progress dopamine keeps users engaged through long waits.
- Streaming exists at three layers: token-level, turn-level inspection, and parallel sub-agent fan-out coordination.
- Anything offering a stream API can be streamed, including bash commands, not just LLM outputs.
- Codex streams individual tokens while Claude Code streams entire tool calls only after JSON completion.
- The real reason for streaming is enabling user intervention, cancellation, and steering, not just observability.
- More automation pushes you toward streaming; less automation pushes you toward discrete turn-based workflows instead.
- Server-sent events use one-way long-running HTTP connections with named events and arbitrary data payloads attached.
- Never use WebSockets for long-running agent tasks because ephemeral connections create state race conditions everywhere.
- Use a database as single source of truth for bidirectional client-server agent communication patterns.
- Send a start event before any data so UIs can render pending states before items arrive.
- Assign IDs immediately so subsequent enrichment events can attach to the correct UI element later.
- A pending state visually differs from empty results, helping users distinguish processing from genuine emptiness.
- Stream key-value completion granularity is a contract decision between server and client per data structure.
- BAML's stream.notnull annotation guarantees fields complete before exposure, eliminating partial-render bugs at type level.
- Internal queues passed through async functions enable child coroutines to communicate progress to parent handlers.
- The bar for spinning up Next.js or Vite has risen significantly since Claude can write vanilla HTML quickly.
- A static index.html with JavaScript can be promoted to a framework later when actually needed.
- Type-safe shared event schemas across server and client make streaming systems dramatically more reliable to maintain.
- Architectural choices should minimize the chance teammates and Claude introduce bugs by accident through wrong abstractions.
- Cancellation works by checking database state at narrow control-flow points, accepting some race condition windows.
- Async queues in Python aren't generic, forcing untyped queue contents in modern streaming code unfortunately.
- Languages designed before async streaming patterns existed lack first-class primitives for today's agentic workloads.
- Python 3.4 added asyncio in 2014, before React, TypeScript, or modern streaming patterns matured significantly.
- Batch start events should announce upcoming work before doing it, enabling skeleton UIs ahead of completion.
- Streaming string deltas append to existing values while structured key-value pairs may stream atomically per pair.
- The same SSE connection multiplexes events for many parallel sub-tasks intermingled by ID-based routing logic.
- BAML can generate matching TypeScript types so frontend handlers stay type-safe with server-emitted event unions.
- Writing tests reframes incidents as missing contracts rather than someone breaking something they shouldn't have touched.
- Standalone HTML files can hit endpoints, append DOM nodes, and ship full streaming UIs without bundlers.
- Cursor streams bash output well; Claude Code historically did not, hurting feedback loops on long commands.
- Interrupting a sub-agent mid-task requires unidirectional database flow that streaming alone cannot provide cleanly.

## INSIGHTS

- Streaming is fundamentally an architectural decision at system inception, not a feature retrofitted onto existing call graphs.
- The dopamine of incremental progress determines whether users perceive an agent as fast or broken.
- Type systems eliminate entire classes of streaming bugs by encoding partiality and completion guarantees at compile time.
- Unidirectional data flow through a database beats bidirectional WebSocket gymnastics for any non-trivial agent system.
- Automation level inversely correlates with required user-facing checkpoints, determining whether streaming or workflows fit best.
- Knowledge artifacts like CLAUDE.md transform agent capability more than smarter prompts on naive setups ever do.
- Choose the simplest sound architecture so collaborators including AI assistants struggle to introduce subtle correctness regressions.
- Frameworks earned their dominance solving yesterday's pain; today's tooling makes vanilla approaches surprisingly viable again.
- Race conditions multiply with concurrent writers; centralizing writes through one API server simplifies the entire mental model.
- The ID-first event protocol decouples ordering from arrival, enabling robust UI assembly from intermingled async streams.

## QUOTES

- "Streaming is really cool. If you have not built streaming to your app..." — Vibhav
- "It's not the easy part. But go learn how to do the hard thing." — Vibhav
- "Anything worth doing is worth working for." — Vibhav
- "If you liked it, then you should have put a unit test on it." — Dex
- "Don't bet against Mitchell." — Vibhav
- "Don't use web sockets. If you're using web sockets, you're going to get screwed." — Vibhav
- "We don't read all our code anymore." — Vibhav
- "It's just software." — Vibhav
- "Streaming is the read-only part of it. But without streaming, you can't make the right part." — Vibhav
- "Adding it later is like an infinite amount of plumbing." — Vibhav
- "Choose the amount of reactivity and fluidness you want your app to have." — Vibhav
- "I'm not a shell boy anymore." — Vibhav
- "Most things that offer a stream API can be streamed." — Vibhav
- "It's the dopamine thing. It's why software has loaders." — Vibhav
- "Software is about how do I reduce bugs as much as possible." — Vibhav

## HABITS

- Write Claude MD instructions describing streaming patterns once so every new project inherits the institutional knowledge automatically.
- Run dev servers in separate terminal tabs to avoid hot-reload disruption during iterative agent code changes.
- Test streaming endpoints with curl quoted properly before assuming the browser rendering is the broken layer.
- Pass URL paths to a database for cancellation rather than propagating cancellation tokens through every layer.
- Default new frontends to a single index.html before deciding whether Next.js or Vite is genuinely warranted.
- Send a batch-start SSE event before processing batches so the UI can render skeletons immediately.
- Always emit a start event with empty payload as the very first message of any stream.
- Write evals as the primary code review mechanism when shipping at machine speed instead of human speed.
- Mark non-streamable fields explicitly so the type system blocks accidental partial exposure during incremental rendering.
- Use async-IO.as-completed and async-IO.gather plus careful failure isolation to prevent one task killing the entire batch.
- Group parallel sub-agent calls into batches of five to ten for tractable observability without losing concurrency.
- Read documentation aloud to coding agents instead of typing precise specifications when intent is clear enough.

## FACTS

- Python's asyncio module was added to the standard library in version 3.4, released around 2014 historically.
- TypeScript was barely on the stage in 2016 and felt like an obscure new tool to most developers.
- CoffeeScript saw active use around 2012 primarily because TypeScript did not yet exist as an option.
- Server-sent events are a one-way protocol where clients cannot send data back over the same connection.
- SSE specifies an event name and data field but the data payload itself need not be JSON formatted.
- Python's asyncio.Queue is not generic, preventing type-safe message contents inside async queues today.
- HTTP bodies are plain text once content-length headers indicate variable or unknown response length is acceptable.
- JSON-RPC is a message format that can run over SSE, stdio, or any persistent message-oriented transport.
- WebSockets are bidirectional but ephemeral, breaking when clients disconnect and reconnect during long-running background processes.
- Claude Code recently added bash output streaming after previously only returning results when commands fully completed.
- Codex CLI streams individual tokens during command output while Claude Code streams completed tool calls only.
- Python's async standard out has a mutex but the single-threaded event loop prevents simultaneous writers anyway.
- BAML provides stream-dot-notnull annotations that guarantee field completion before client exposure during incremental rendering.
- The Boundary CLAUDE MD lives at docs.boundaryml.com/agent.md and contains streaming patterns for any project.
- Datastar is a hypermedia framework by Bob using server-side rendering instead of client-side state logic.

## REFERENCES

- BAML (Boundary's programming language for nondeterminism)
- HumanLayer (Dex's company building context engineering tools)
- Boundary docs at docs.boundaryml.com/agent.md
- Cursor IDE
- Claude Code
- Codex CLI
- OpenAI Deep Research
- Perplexity agent
- Riptide (referenced for unidirectional data flow pattern)
- Datastar hypermedia framework by Bob
- Excalidraw (whiteboarding tool used during recording)
- Claude Agent SDK
- async-io Python module
- Server-sent events (SSE) protocol
- JSON-RPC over SSE
- MCP (Model Context Protocol)
- Next.js, Vite (frameworks discussed)
- jQuery, XHR (legacy comparison)
- The Unconference (upcoming live demo event)

## ONE-SENTENCE TAKEAWAY

Streaming is system design, not magic — type-safe events through SSE unlock reactive agents, cancellation, and intervention.

## RECOMMENDATIONS

- Copy the Boundary CLAUDE MD into your project so coding agents inherit streaming architecture patterns automatically.
- Build streaming into your agent system from day one to avoid massive future plumbing across function call graphs.
- Use server-sent events with named event types and ID-keyed payloads for parallel async sub-agent coordination.
- Reach for a database with unidirectional data flow before considering WebSockets for any agent application.
- Send a start event with empty data before any payload so the UI can render pending states immediately.
- Mark fields that must complete before exposure as non-streamable through your type system to prevent partial rendering bugs.
- Default new frontends to a single index.html with vanilla JavaScript before introducing Next.js or Vite frameworks unnecessarily.
- Group parallel sub-agent work into batches of five to ten with batch-start events announcing upcoming work.
- Stream bash command output to users so long-running tool calls give immediate feedback during agent execution.
- Pass cancellation through database state checked at narrow control points instead of plumbing tokens everywhere.
- Generate matching TypeScript types from your event schema so frontend handlers stay type-safe across the wire.
- Test streaming endpoints with curl using proper quoting before debugging suspected browser-side rendering or parsing issues.
- Pair every streamed string field with an empty-string default so partial deltas append cleanly to existing values.
- Write evals to enforce behavior contracts so future commits break loudly instead of silently regressing functionality.
- Use async-IO.gather with explicit error isolation per task so one failing sub-agent never kills a batch.
- Open an HTML file directly in your browser during early prototyping before standing up a full development server.
- Show batch contents up front so users can cancel or skip known-junk items before processing wastes resources.
- Build interruption capability into long-running agents through database flags rather than hoping users wait passively.
- Treat streaming UX as the foundation for steering agents, not merely as a passive observability decoration.
- Learn the hard architectural skills competitors avoid because mastery enables building things others fundamentally cannot.
