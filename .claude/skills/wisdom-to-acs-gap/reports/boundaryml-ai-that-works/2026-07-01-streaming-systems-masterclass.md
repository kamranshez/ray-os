---
title: Streaming Systems Masterclass
videoId: 9MFiATinGC0
url: https://www.youtube.com/watch?v=9MFiATinGC0
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1: Streaming is a ground-up architectural decision, not a feature you bolt on later.** Once you model your agent as functions that return values, retrofitting streaming means passing queues through every layer, an "infinite amount of plumbing," so you design for `yield` from day one.
VERDICT: net-new video available.

**Spine 2: Streaming is only the read-only half; the payload is steering a running agent job, and you get client-to-server control by writing to a database, not by opening WebSockets.** Cancel a branch, prune junk, or interrupt a sub-agent by writing to the DB and checking one cancellation checkpoint in the server's control flow.
VERDICT: net-new video available.

**Spine 3: A distributable domain CLAUDE.md turns a normally hard architecture into something the agent one-shots.** The whole streaming build went fast because Boundary's public agent.md encoded the streaming and async knowledge, so Claude avoided the classic mistakes without being told.
VERDICT: next-step video available.

## Summary

Boundary CEO Vibhav gives Human Layer's Dex a masterclass on architecting streaming agent systems, building a parallel scraper that streams SSE events into plain HTML.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: Design for streaming from the ground up

The claim: streaming is a fundamental architectural layer you commit to before writing the agent, because "if you don't design for it, adding it later is like an infinite amount of plumbing." Most people treat streaming as a UI polish item bolted on at the end. That is exactly backwards. The mechanism: a non-streaming function returns a value once; a streaming one must `yield` incrementally, and every caller up the stack must also yield rather than return. Because that inverts the shape of every function between the LLM call and the request handler, you either pass a queue (an in-memory structure the async coroutines write to and the top-level handler drains) through the whole system from the start, or you rewrite every layer later. Vibhav names the real axis: "the more automation you have, the more closer you are to streaming," so an autonomously-progressing map-reduce is effectively a stream whether or not you call it one. This generalizes cleanly beyond LLMs: any stream API can stream, and a long bash command is the obvious second domain most agents forget. It goes wrong when one parallel task fails and takes the run down, so failure points must be explicit.

### Spine 2: Streaming is the read-only half; steer a running job via a database, not WebSockets

The claim: the real product reason to stream is not observability, it is control, and enabling client-to-server control means writing to a database rather than opening a WebSocket. Most people reach for WebSockets the moment they need two-way communication. Vibhav's warning is blunt: "Don't use web sockets. If you're using web sockets, you're going to get screwed." The mechanism: SSE is one-directional by protocol, so the client cannot talk back over the same connection; instead the client writes its intent (cancel, prune, add) to the database, and the server checks that state at a single cancellation checkpoint inside its own control flow. Because there is one source of truth, you avoid the ephemeral-connection lifecycle and race conditions that WebSockets force on long-running background tasks. This is the Riptide pattern: all writes hit an API server, the database changes, and those changes stream down to subscribed clients. It generalizes to any interruptible pipeline, like a CI job you cancel mid-run. It goes wrong at the race boundary: past the checkpoint, a task cannot be cancelled, so you model "already started" explicitly.

### Spine 3: Ship a domain CLAUDE.md that encodes the hard architecture

The claim: the streaming build felt trivial only because a CLAUDE.md carried the team's hard-won knowledge, so "it's just having the knowledge base." When Vibhav asked why Claude one-shot the streaming code, the answer was that Boundary's agent.md at docs.boundaryml.com already spelled out how to do streaming, and "I think it just figured it out from here." Most people treat CLAUDE.md as project trivia (build commands, style) rather than as a distributable encoding of a genuinely hard technique. The mechanism: streaming has a small number of classic failure points (return-vs-yield, blocking-vs-async IO, queue plumbing, pending-vs-empty states); pre-loading those as instructions means the agent never rediscovers them by trial and error, collapsing a normally hard task into a five-prompt build. This generalizes to any domain where the mistakes are predictable and repeated, like a testing or migration playbook. It goes wrong when the knowledge base drifts from reality or is too generic to steer a specific decision, at which point the agent confidently applies stale patterns.

## 🎬 Proposed ACS videos

### 1. Streaming Is An Architecture, Not A Feature

HOOK: Why does no one build streaming? Because bolting it on later is infinite plumbing, so you design for yield first.
THE PROMISE: For engineers building agent products who want real-time UIs; after this you can architect a system that streams from day one instead of retrofitting it.
THE SHAPE: (1) Show the same scraper as return-only, then as yield-based, and count the plumbing difference. (2) Whiteboard the three streaming layers: per-token, per-turn, per-object. (3) Build a parallel web-scraper agent that emits SSE events with stable IDs. (4) Wire a plain index.html that appends to the DOM, no framework. (5) Add semantic streaming so title and URL complete while the summary streams token by token.
SPINE: 1.
SLOT: Techniques class, new chapter on building agent products / real-time systems.
RELATIONSHIP: net-new. The catalog has nothing on streaming, SSE, or real-time agent UIs. test-time-compute covers fanning subagents out for more compute, but never how to stream their progress to a user.
PROOF TO REUSE: "building streaming is actually a fundamental layer of your system that you think about from the ground up"; "you actually have to think of everything as a yield rather than as a return type"; the batch-of-five parallel scraper with a batch-start event.

### 2. Steer A Running Agent: The Database Is Your Control Channel

HOOK: Streaming is the read-only half. Want to cancel a branch or interrupt a sub-agent? Do not reach for WebSockets.
THE PROMISE: For engineers whose agents run long parallel jobs; after this you can build cancellation, pruning, and interruption without the WebSocket race-condition trap.
THE SHAPE: (1) Take the streaming scraper from video one. (2) Show the problem: SSE is one-directional, the client cannot talk back. (3) Add a cancel button that writes to the database. (4) Add one cancellation checkpoint in the server control flow that reads DB state. (5) Show the "already started" race and model it explicitly with a starting-entry write.
SPINE: 2.
SLOT: Techniques class, same building-agent-products chapter, as the sequel to video one.
RELATIONSHIP: net-new. Remote Control (Claude Code, filmed) is about controlling the coding agent remotely, not about architecting a steerable multi-agent product with unidirectional data flow. The speakers explicitly frame this as its own future episode.
PROOF TO REUSE: "Don't use web sockets. If you're using web sockets, you're going to get screwed."; the Riptide unidirectional-data-flow description; "streaming is the read-only part of it. But without streaming, you can't make the [write] part of it."

### 3. A CLAUDE.md That One-Shots The Hard Thing

HOOK: They built a streaming system in five prompts. The trick was not the prompts, it was a CLAUDE.md that already knew how.
THE PROMISE: For engineers who keep re-teaching Claude the same hard pattern; after this you can package a domain into a distributable CLAUDE.md the agent applies by default.
THE SHAPE: (1) Run a hard task (streaming) with no domain CLAUDE.md and watch Claude botch return-vs-yield and blocking IO. (2) Drop in the domain CLAUDE.md. (3) Re-run and watch it one-shot the same task. (4) Show how to distill the classic failure points into instructions. (5) Publish it so a team or the public can copy it.
SPINE: 3.
SLOT: Context Engineering class, or Business class next to skills-as-team-knowledge-base.
RELATIONSHIP: complements skills-as-team-knowledge-base and global-claude-md-personal-profile, which teach turning team knowledge into a reusable skill and a personal profile. This adds the specific move of encoding one genuinely hard architectural pattern so the agent avoids the predictable mistakes, and distributing it publicly like Boundary's agent.md.
PROOF TO REUSE: "why does this work? Well, because in our cloud MD, we actually have instructions of how to do streaming"; "it's just having the knowledge base ... once you know it, it's trivial"; the docs.boundaryml.com agent.md copy-paste.

Also film-able (not deep-dived): raise your framework bar. Dex's "one of my new favorite tactics" is to build the UI as a static index.html hitting an endpoint and appending to the DOM before adopting Next.js or React. This complements the filmed scrappy-copy-first technique with a concrete real-time-UI worked example.

## 📚 Full wisdom (reference)

### SUMMARY
Boundary CEO Vibhav gives Human Layer's Dex a masterclass on architecting streaming agent systems, building a parallel scraper that streams SSE events into plain HTML.

### IDEAS
- Streaming is a fundamental architectural layer designed from the ground up, never a feature bolted afterward.
- Once you skip designing for streaming, adding it later becomes an infinite amount of downstream plumbing.
- Streaming forces you to model every function as a yield, not a plain return value type.
- Multiple streaming layers exist: per-token deltas, per-turn agent-loop state, and per-object individual tool call event boundaries.
- Claude Code streams each turn but not each token; Codex now streams individual tokens as generated.
- Streaming is not only for LLMs; any stream API, like a long bash command, can stream.
- The real product reason to stream is control, not mere observability, which a background task provides.
- Streaming lets a human or agent prune junk websites, cancel branches, or add missed pages mid-run.
- SSE sends an event name plus a data field over one long-running, one-directional HTTP server connection.
- Give each streamed element a stable ID so the front end knows where to store data.
- Distinct UI states matter: pending, empty, and error must look different so users can read progress.
- Semantic streaming guarantees title and URL arrive complete while the longer summary streams token by token.
- A shared type system generating matching Python and TypeScript keeps front end and back end synchronized.
- For client-to-server control, write to a database; the server checks state, rather than using fragile WebSockets.
- Cancellation lives at one checkpoint in control flow; past that point the task cannot be cancelled.
- With Claude riffing out plain HTML, your bar for reaching for Next.js should be much higher.
- The streaming build worked fast because a CLAUDE.md encoded the team's hard-won streaming and async knowledge.

### INSIGHTS
- Streaming and discrete turn-based workflows sit on one axis: more automation pushes you toward continuous streaming.
- Whether you stream or batch, an automatically-progressing system is effectively streaming, even framed as a map-reduce.
- Streaming is the read-only half; without it you cannot build the write half, interruption and steering.
- Enforce dependencies with type systems and contracts that run before merge, since nobody reads all code.
- Good architecture is choosing the arrangement that makes accidental mistakes by teammates and agents least likely.
- WebSockets fail long-running agent tasks because ephemeral connections force fragile lifecycle and race-condition management on you.
- A single source of truth in the database beats multiple readers and writers fighting over state.
- The hard part of streaming is system design, not code; the coding agent writes the work.
- Encoding domain knowledge into a CLAUDE.md turns a normally hard technique into something the agent one-shots.
- Type-guaranteed streaming means the LLM never has to reason about which fields stream and which complete.

### QUOTES
- "building streaming is actually a fundamental layer of your system that you think about from the ground up" — Vibhav
- "if you don't design for it, adding it later is like an infinite amount of plumbing" — Vibhav
- "you actually have to think of everything as a yield rather than as a return type" — Vibhav
- "The real reason you want to do streaming is because oftentimes you want to have a user understand where failures are happening and how they can control and limit the map reduce system" — Vibhav
- "Don't use web sockets. If you're using web sockets, you're going to get screwed." — Vibhav
- "we don't read all our code anymore" — Vibhav
- "So, choose the simplest architecture that is most sound." — Dex
- "if you liked it, then you should have put a unit test on it" — Dex
- "streaming is the read-only part of it. But without streaming, you can't make the [write] part of it" — Vibhav
- "your bar for creating a Next.js app or a V app ... should be significantly higher than it used to be" — Dex
- "it's just having the knowledge base ... once you know it, it's trivial" — Vibhav
- "Choose the amount of reactivity and fluidness you want your app to have." — Vibhav

### HABITS
- They keep a CLAUDE.md encoding streaming and async patterns so the agent avoids classic mistakes automatically.
- They run the dev server in a separate terminal so hot reload does not fight edits.
- They batch parallel work into groups of five to ten rather than running everything fully unbounded.
- They design the SSE event contract first, then let Claude write the entire mechanical streaming implementation.
- They prototype UIs as a static index.html hitting an endpoint before ever reaching for a framework.
- They think about failure points explicitly so one failing parallel task does not collapse the run.
- Vibhav no longer writes code by hand, granting Claude unsafe edit permissions and flagellating it repeatedly.
- They push all demo code publicly so viewers can copy the streaming patterns and CLAUDE.md directly.

### FACTS
- Async IO was added to Python's standard library in version 3.4, first released back in 2014.
- Python's asyncio.Queue is not generic, so it cannot carry static type safety for its queued elements.
- Python's standard out has a mutex, but asyncio runs only one coroutine at a time anyway.
- SSE data fields need not be JSON; the protocol only requires the literal data keyword prefix.
- JSON-RPC and MCP both run message formats over SSE, and SSE can run over standard IO.
- Browsers cannot render streamed HTML blobs directly; SSE requires a data prefix plus a parsing receiver.
- The Claude Agent SDK does not stream bash output; you receive the whole result when done.
- Human Layer's Riptide uses unidirectional data flow: writes hit API server, database changes stream to clients.

### REFERENCES
- AI That Works (the show, hosted by Dex and Vibhav)
- Human Layer (Dex's company; context-engineering tools for coding agents)
- Boundary and BAML (Vibhav's company; a programming language for nondeterminism)
- Riptide (Human Layer's app using unidirectional data flow)
- docs.boundaryml.com (the agent.md / CLAUDE.md with streaming instructions)
- Claude Code, Codex, Cursor (coding agents)
- OpenAI Deep Research and Perplexity's agent (streaming UX examples)
- SSE (Server-Sent Events), JSON-RPC, MCP, WebSockets
- Datastar (a hypermedia framework raised by an audience member)
- Excalidraw, Next.js, Vite, React, jQuery, XHR, CoffeeScript, TypeScript
- The Unconference (event where the evals demo was promised)

### ONE-SENTENCE TAKEAWAY
Design agent systems for streaming from the ground up, or pay infinite plumbing costs later.

### RECOMMENDATIONS
- Copy Boundary's streaming CLAUDE.md from docs.boundaryml.com and paste it into your own coding agent project.
- Design your SSE event schema first, giving every element an ID before writing any streaming code.
- Model pending, empty, and error as distinct explicit states so the UI communicates real progress honestly.
- Use semantic streaming to guarantee some fields complete while others stream in token by token reliably.
- Handle client-to-server actions by writing to a database and checking that state, not opening fragile WebSockets.
- Batch parallel tasks in small groups and emit a batch-start event listing the upcoming work items.
- Build internal streaming UIs as a static index.html appending to the DOM before adopting a framework.
- Generate matching front-end and back-end types from one schema so events stay synchronized across the wire.
