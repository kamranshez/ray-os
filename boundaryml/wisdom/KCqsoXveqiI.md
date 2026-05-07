---
video_id: KCqsoXveqiI
title: "Using Sloppy Code to Build Perfect Plans"
url: https://www.youtube.com/watch?v=KCqsoXveqiI
channel: BoundaryML
---

### SUMMARY
Vaibhav (BoundaryML) and Kevin Gregory (Evolution IQ) demonstrate building design docs for complex features like BAML threading using AI-generated internal tooling and slop.

### IDEAS
- Fight AI slop with slop by generating throwaway internal tooling that produces high quality documents.
- Implementation can often be one-shot if the design document is phenomenally correct first time around.
- Phenomenally correct design is extremely hard, requiring days of pure thinking before any code gets written.
- Build tooling so you don't have to keep track of everything in your head while designing.
- GitHub does not work well for sharing massive amounts of markdown design files across teams collaboratively.
- Latch onto Slack as a notification system rather than building your own notification infrastructure from scratch.
- Members tagged via GitHub email auto-join the system, granting different privileges than random external wild users.
- Internal tooling code can be pure AI slop because it's not customer-facing and just needs to work.
- Export design docs as zip files so Claude can edit them locally outside the website backend.
- A CLI tool syncs local folders with the web UI, detecting drift and pulling changes via Claude.
- Function coloring is a legacy pain point because concurrency wasn't on day one for most languages.
- Call-site determines concurrency rather than function definition, avoiding async-await coloring problems entirely.
- Spawning returns a future type that can be awaited multiple times idempotently with same response.
- Frequent behaviors should be syntactically most convenient without compromising correctness in language design philosophy.
- Cancellation as a panic, with explicit catching required, prevents accidentally hiding cancel signals via wildcards.
- Recording Slack huddle transcriptions feeds raw context into the model for restructuring design docs comprehensively.
- Models mess up complicated design docs when editing in place rather than rewriting from scratch.
- Editing is a harder cognitive exercise than rewriting from scratch even for humans, not just models.
- Sunk cost fallacy keeps people editing when major rewrites would yield much cleaner results faster.
- Naming folders with numbers plus names lets ls reveal context without the model reading files.
- Models read design docs like humans, so layered top-down approaches help comprehension dramatically.
- Spawn doc subpages separate prior art from main motivation to reduce cognitive load for skimmers.
- Challenge the LLM to find what should not be possible rather than just trusting your assumptions.
- LLMs trained to trust user context will implement wrong things rather than push back on assumptions.
- Median engineer quality rises dramatically when AI handles edge case discovery during design phase exploration.
- Best engineers have less skill issue problems because better intuition produces better implementations naturally.
- Discovery of design bugs shifts from implementation phase to design phase, saving massive rework cost.
- Cost limits in middleware require thread-local storage, a discovery only made by writing exhaustive examples.
- Versioning design docs linearly rather than via git allows richer per-version comment chains and tooling.
- Older versions become read-only with comment history preserved, exported into agent-context markdown for retrieval.
- Spending 50%+ of engineering time on design docs because hands-on-keyboard typing has been largely solved.
- Beep stands for BAML Enhancement Proposals, modeled after PEP for governing language feature additions.
- Granola transcription tools captured 2.5-hour meetings became raw input for restructuring complex design proposals.

### INSIGHTS
- The bottleneck has shifted from typing code to articulating design decisions explicitly enough for models to execute.
- Sloppy internal tooling beats polished tooling when the goal is producing high-quality customer-facing artifacts faster.
- Design quality compounds: better docs make better code, which validates better designs, which produces better intuition.
- Model behavior mirrors human cognitive limits, so the same readability principles apply to both audiences identically.
- Implicit decisions in meetings must be extracted into explicit document decisions for one-shot implementability later.
- Linear versioning beats git when you need rich tooling around comments, drafts, and per-version state machines.
- Forcing exhaustive examples reveals architectural requirements like thread-local storage that hand-waving would miss entirely.
- Notification systems should be borrowed not built when adjacent platforms already solve the social coordination problem.
- The cost of an LLM API call now matters, making cancellation semantics a first-class application developer concern.
- Code becomes a means to an end when the workflow it enables is the actual product being optimized for.
- Splitting prior art into separate subpages preserves linear motivation flow while keeping nuance accessible to readers.
- Asking models to challenge your assumptions counteracts their training to defer to user-provided context blindly.
- One-shot implementability emerges from breaking hard problems into four or five individually shippable design chunks.
- Tooling that auto-pulls related design docs into context eliminates manual consistency checking across feature boundaries.

### QUOTES
- "This is how you fight AI slop with slop, you're using slop to build internal tools." — Kevin
- "The real answer is build tooling so that you don't have to keep track of everything in your head." — Vaibhav
- "Implementation can often be one-shot if the design is phenomenally correct." — Vaibhav
- "Phenomenally correct design is very hard to do." — Vaibhav
- "I haven't even started coding yet. It's pure designing for 4 days." — Vaibhav
- "We've decided as a society that asyncio is more convenient than threading." — Vaibhav
- "Frequency is really important. We don't want to make it harder to do the right thing." — Vaibhav
- "If you replace in place for design docs models will often just mess up." — Vaibhav
- "Editing is a more hard exercise to be coherent in than rewriting from scratch." — Vaibhav
- "I have a lot more time to write these design docs and it's so much more important to do that." — Kevin
- "LLMs will write every piece of code that you ask them to." — Vaibhav
- "Now everyone's median kind of rises and your median is so much better than it used to be." — Vaibhav
- "It will just assume what you're saying is correct and then it'll implement it when it may not be." — Kevin
- "I have never even opened claude myself to add features into beeps because it's not worth it." — Vaibhav
- "It's a tool use. Yeah, it's a tool. Exactly. It's money." — Kevin and Vaibhav
- "Get good. But the real answer is not get good. The real answer is build tooling." — Vaibhav
- "If your design doc is really good, a lot of times claude code cursor can get it in one shot." — Vaibhav

### HABITS
- Spawn coding agents via Slack tags to add features rather than opening Claude directly yourself.
- Record Slack huddle transcriptions and feed full transcripts back into models for design doc restructuring.
- Spend four full days on pure design before writing any implementation code for complex language features.
- Allocate over 50% of engineering time to writing design documents and iterating on plans actively.
- Always rewrite complex design docs from scratch in V2 rather than editing V1 in place repeatedly.
- Force exhaustive code examples in design docs to surface hidden architectural requirements early always.
- Tag design docs explicitly as good-for-LLM so other working agents auto-pull them as context.
- Read every design doc end-to-end personally before promoting it from draft to proposed status.
- Ask the LLM to challenge what should not be possible in your design before implementing.
- Name BEP folders with numbers plus descriptive names so ls reveals context without reading files.
- Cross-check new BEPs against every previously implemented BEP for consistency and syntactic correctness automatically.
- Export full beep history with versions, comments, and discussions baked into agent-context.md before handoffs.
- Split prior art into separate subpages instead of weaving it through main motivation sections.
- Use Slack threads as the notification layer for design doc comments rather than building custom systems.
- Auto-link GitHub email accounts to grant team members elevated privileges in the internal review tool.
- Promote drafts only after personally doing the legwork to verify the document is genuinely ready.

### FACTS
- Evolution IQ was acquired for 730 million dollars approximately a year and a half before this recording.
- Async/await creates function coloring where async context cannot freely call sync functions and vice versa.
- TypeScript has fetch.JSON await chains requiring double awaits because metadata and payload arrive separately.
- Go uses ctx parameter passed through every function layer for explicit cancellation token propagation.
- 99.99% of TypeScript code never uses AbortController, leaving most APIs uncancelable by default in practice.
- Python uses implicit cancellation semantics rather than explicit cancel tokens like Go's ctx pattern.
- BAML's threading BEP shrunk from 104 kilobytes to 62 kilobytes after rewriting and restructuring it.
- Goroutines and Kotlin coroutines are virtual threads, lighter than OS threads but heavier than async-await.
- BEPs.boundaryml.com is the public-facing URL for browsing BoundaryML's enhancement proposals interactively.
- The BAML repository contains the beeps folder as fully open source, written entirely by AI agents.
- BAML infers error types per function automatically rather than requiring explicit error type annotations everywhere.
- Threading BEP V2 covers spawn semantics, futures, awaits, cancellation, middleware, retries, and circuit breakers.
- Granola transcription tool broke during a 2.5-hour design meeting, capturing only partial recording sadly.
- Polly is a .NET library implementing middleware patterns for retries, timeouts, fallbacks, and circuit breakers.
- Spawned futures in BAML start immediately upon spawn rather than waiting for explicit start calls.

### REFERENCES
- BAML programming language by BoundaryML
- Async.io concurrency model
- Go programming language goroutines and ctx pattern
- Kotlin coroutines
- CPython concurrency model
- V8 JavaScript engine
- TypeScript fetch and AbortController
- Python decorators for middleware
- Express.js middleware
- Polly .NET middleware library
- Cloud Code (Claude Code) founder's plan-iteration workflow
- Cursor coding agent
- Granola meeting transcription tool
- Slack as notification platform
- Google Docs and Google Drive
- GitHub pull requests and issues
- BEPs.boundaryml.com (public BEP browser)
- Evolution IQ disability insurance claims systems
- AIN conference talk on fighting slop with slop
- Kai's BAML datetime BEP
- Antonio's earlier threading BEP version
- Sam's suggestion on naming BEP folders
- Dex from previous AI That Works episode
- PEP (Python Enhancement Proposals) as inspiration for BEPs

### ONE-SENTENCE TAKEAWAY
Build sloppy internal tooling so you can spend your real effort writing phenomenally correct design documents.

### RECOMMENDATIONS
- Build internal markdown sharing tools with Slack integration rather than relying on GitHub for design review.
- Force coding agents to add features to your tooling via Slack tags rather than direct invocation.
- Record all design meetings with transcription tools and feed raw transcripts back into models afterward.
- Rewrite complex design docs from scratch in numbered V2 files rather than editing V1 in place.
- Split prior art and design rationale into separate subpages from the main motivation document section.
- Force exhaustive code examples in every design proposal to surface hidden architectural requirements early on.
- Ask LLMs explicitly to challenge what should not be possible in your design before implementing it.
- Name folders with numbers plus descriptive labels so ls reveals context without reading file contents.
- Auto-pull related design documents into agent context to eliminate manual cross-feature consistency checking work.
- Export design docs as zip files with full version history baked into agent-context.md for handoffs.
- Spend over 50% of engineering time on design documents now that typing code is largely solved.
- Break extremely hard problems into four or five individually one-shot implementable design chunks deliberately.
- Use linear versioning rather than git for design docs to enable richer per-version commenting tooling.
- Make older document versions read-only with preserved comments rather than allowing destructive edits across history.
- Auto-link GitHub email accounts to your review system to grant team members elevated privileges automatically.
- Tag design docs as good-for-LLM so other working agents pull them into context automatically.
- Promote design docs from draft to proposed only after personally verifying they are ready to read.
- Prefer call-site concurrency decisions over function-level async coloring when designing new language threading models.
- Treat cancellation as a panic with explicit catching required to prevent wildcards hiding cancel signals.
- Discover design bugs during exhaustive example writing rather than waiting until implementation reveals them.
