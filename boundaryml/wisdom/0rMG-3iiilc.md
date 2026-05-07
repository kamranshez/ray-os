---
video_id: 0rMG-3iiilc
title: "Build Faster by Coding Slower"
url: https://www.youtube.com/watch?v=0rMG-3iiilc
channel: BoundaryML
---

### SUMMARY
Vibhav and Dex from BoundaryML demonstrate designing a testing language feature for BAML using deep upfront design with Claude before any code generation.

### IDEAS
- Non-deterministic systems require scenario-grouped tests, aggregation metrics, and dynamic data loading from production logs.
- Spending hours iterating on design tickets enables one-shotting thousands of code lines without slop.
- Models are sycophantic and will obey any suggestion as a directive unless framed as optional.
- Junior engineers struggle with LLMs because their incorrect suggestions compound into massive coding mistakes downstream.
- Markdown design docs let you do brain surgery on the model's thinking before code generation.
- Testing scenarios should be string-named because variable names are arbitrary while strings describe intent.
- Global variables are evil because they make code hard to reason about and navigate.
- BDD nesting indents code thirty times before assertions, which makes test files painful to read.
- Before-each and before-all hooks encourage overgeneralization that hurts long-term test maintainability significantly.
- Rust's macro system eliminates the need for before-each hooks that plague other testing frameworks.
- Test runners should be lambdas that take a test and produce reports.
- Quorum runners enable executing a test multiple times and aggregating pass-fail across runs.
- Decorators preserving identity types let you wrap behavior without breaking the type system.
- Models bias heavily toward recent context, so old context loses influence but isn't truly forgotten.
- Long context works fine for document tasks but fails on multi-turn tool-calling feedback loops.
- Asking models if code is good produces praise; asking if bad produces criticism every time.
- Code Rabbit comments at the end add slop unless filtered through Claude summaries first.
- The cycle time for individual tasks matters more than total tickets in flight.
- Optimizing non-bottleneck stations makes the entire system less efficient by accumulating work-in-progress inventory.
- Restarting from scratch with a better ticket beats incrementally fixing thirty-percent-wrong implementations.
- Snapshot tests print serialized output to text files so humans can review during reviews.
- Boolean classifiers piped into deterministic scoring code beats asking models to evaluate quality directly.
- Files should mean almost nothing because agents constantly cat files across whole packages.
- Pre-collection of all test cases is required for true parallel execution to work properly.
- Two parallel hard tasks is the maximum before attention degrades and quality suffers.
- The dumb zone happens to humans at 11:30 PM just like it hits Opus.
- A million-context model lets you skip manual compaction in favor of letting it rip.
- Soundness checking beats correctness checking because correctness requires verifying every primary source.
- Show the model code snippets to bias future ticket-writing toward your preferred patterns.
- Every check or metric collector contributes to a final aggregation rather than failing individually.

### INSIGHTS
- Hours of design upfront converts directly into days of working autonomous code generation.
- Foundational bugs emerge when foundational design is sloppy, not when implementation has bugs.
- Context window position matters less than active human engagement holding long-term consistency in mind.
- Vertical slices and tracer bullets beat designing every layer simultaneously when working with coding agents.
- The faster the model writes, the more critical your design ticket quality becomes.
- Brainstorming options with Claude exceeds telling Claude what to do for novel decisions.
- Scenarios with named metrics replace boolean assertions when systems become probabilistic rather than deterministic.
- Suggesting softly to a model is the difference between exploration and obedience trap.
- Restart-from-scratch is faster than incremental repair once drift exceeds roughly thirty percent.
- Production data sampling makes evaluation a moving target that captures real user behavior changes.
- Bottleneck-focused optimization beats parallel-everything coding by reducing work-in-progress and inventory cost.
- Code rabbit slop at the final layer can destroy hours of careful upstream design work.
- Workflows are dynamic patterns of building blocks, not hardcoded automations you can fully script.
- Testing for non-deterministic systems is foundationally different from testing pure control-flow software.
- Hand-waving uncertain spec sections out keeps them from becoming pre-baked model decisions.
- Lazy coders win by only doing manual work when empirical evidence demands it.

### QUOTES
- "Do not outsource the thinking. If you let the model make decisions, you're rolling the dice." Dex
- "Models are extremely sycophantic. If I suggested something, it's going to listen to me." Vibhav
- "Tokens are cheap compared to the amount of effort you'll spend resteering the model down a bad path." Dex
- "I've had multiple 10,000 plus line PRs without me touching the implementation loop." Vibhav
- "The way I code now, I have two agents running in the background and I just play League while I code." Vibhav
- "I don't type code anymore. My models do that for me. Typing code is too 2024." Vibhav
- "Whatever the slowest thing in the workflow is, that is your constraint." Dex
- "If you are optimizing inefficiencies that are not bottlenecks, you are wasting time and adding no value." Dex
- "Files don't mean anything. In an agent-friendly world, you actually want files to mean almost nothing." Vibhav
- "Correctness requires too much work. I'm checking soundness, not correctness." Vibhav
- "There's no chance there's a BDD library in Rust because Rust is macro driven." Vibhav
- "Parallelism is impossible without pre-collection." Dex
- "I'd rather ship one thing in three days and the second thing in five days than ship two things in four days." Dex
- "Once you saw next, you're like oh shoot, this is actually useful in my current research task." Vibhav
- "These markdown docs are an opportunity to have the model dump everything it's thinking so you can do brain surgery." Vibhav
- "It's not the model is going to forget; it's that I will recognize the mistake." Vibhav
- "Lazy coders are extremely lazy and I am probably one of the laziest of all of them." Vibhav
- "Most people have probably never thought about evals in this approach from the very beginning." Vibhav
- "If you ask a model if the code is good, the model will be like oh yeah it's great." Dex
- "I just measure those two quality metrics and that gives me a really good idea if it's working." Vibhav

### HABITS
- Plays League of Legends in parallel while two coding agents run background tasks asynchronously.
- Reads ticket files completely in real time during long agent processing pauses without skimming.
- Auto-advances tickets through research and design phases while engaging only at decision points.
- Maintains personal repos of every major programming language for cross-language design research.
- Uses Riptide app to run multiple parallel coding sessions on the same feature branch.
- Goes to bed at 11:30 PM when brain enters dumb zone instead of pushing through.
- Copies completed PR content into new tasks to seed the next implementation cycle.
- Writes BAML in light mode despite preferring dark mode for everything else generally.
- Limits manual context compaction by trusting million-token windows to handle long sessions.
- Asks Claude to summarize Code Rabbit comments rather than reading raw automated review feedback.
- Splits compiler work into collection and execution phases for clean parallelism boundaries.
- Restarts entire branches from scratch when implementations drift more than thirty percent off target.
- Uses snapshot tests printing serialized output to text files reviewable during pull request reviews.
- Speaks technically and precisely to models so they receive less ambiguous instruction signals.
- Runs two design tasks in parallel but always prioritizes the primary task when unblocked.

### FACTS
- Face ID launched around 2017-2019, before transformer architecture became widely deployed in mobile devices.
- Google policy forbids using before-all and before-each hooks because they encourage overgeneralization in tests.
- The Goal book sold ten million copies and was originally written to sell supply-chain optimization software.
- Toyota lean Kanban inspired Western factory management after Japanese visits in the 1960s and 70s.
- BAML namespaces work like Go packages where files within a folder share scope automatically.
- Zig's testing syntax inspired BAML's ergonomic approach to scenario-driven test definitions.
- OLAP cubes historically restricted business intelligence to two dimensions plus one metric value.
- Million-context Claude models use yarn to extend input length without retraining model intelligence.
- Opus reportedly gets dumber around 2-3 PM Pacific time according to community observations.
- Vibhav implemented BAML closures in roughly 36 hours including two sleep periods between sessions.
- Closures generated 16,000 lines of working Rust code through fully auto-advanced agent workflows.
- BAML deletes the assert keyword in favor of a testing package with first-class functions.
- The original Scrum and Agile methodology comes from factory production line theory, not software.
- Chris on Twitter noted long context handles documents fine but breaks on multi-turn tool calls.
- BoundaryML hosted an unconference at YC's Dogpatch office on April 11th, a Saturday.

### REFERENCES
- BAML programming language by BoundaryML
- Riptide app for agentic engineering workflow management
- Code Rabbit automated PR reviewer
- The Goal by Eliyahu Goldratt about factory bottleneck theory
- Mitchell Hashimoto's talk on testing in Go
- Zig programming language testing ergonomics
- Go programming language defer keyword and package system
- Face ID as a case study for non-deterministic system testing
- Human Layer company by Dex
- YC office in Dogpatch San Francisco
- Anthropic's Opus model and million-context window
- Claude Code with custom agent skills
- The JP Morgan emails episode of AI That Works
- Karpathy's auto-research methodology
- LSP integration for custom code search tools
- Chef configuration management origin story
- SBF and the FTX startup scene reference
- Aaron, Vibhav's co-founder, who built much of the foundational research
- Kyle who built sync-degraded fallback infrastructure for Riptide
- Camila and other live audience participants asking questions

### ONE-SENTENCE TAKEAWAY
Spend hours making the design ticket flawless and the agent ships thousands of lines correctly.

### RECOMMENDATIONS
- Treat design tickets as the primary leverage point because tickets compound into thousands of code lines.
- Use markdown documents to externalize model thinking before letting it write any production code.
- Suggest options softly rather than commanding because models obediently amplify your incorrect hunches into bugs.
- Build named-metric scenarios instead of boolean assertions whenever your system has any non-deterministic component.
- Pre-collect all test cases before execution to enable true parallelism across the entire test suite.
- Make every test self-contained instead of using before-each hooks that hide setup logic away.
- Use string identifiers for test scenarios because variable names lose semantic meaning quickly over time.
- Restart branches from scratch when implementations drift more than thirty percent off the design.
- Run secondary tasks in parallel but always return to the primary task when unblocked.
- Optimize the bottleneck step rather than parallel-everything because work-in-progress inventory destroys cycle time.
- Print serialized snapshots to text files so reviewers can audit data structures during pull requests.
- Pipe Code Rabbit comments through Claude summarization rather than acting on raw automated review feedback.
- Maintain a personal repo of major programming languages for cross-language design pattern research.
- Use vertical slices and tracer bullets to ship end-to-end before adding feature breadth.
- Check for soundness rather than correctness because verifying every primary source consumes too much engagement.
- Remove uncertain ticket sections so they emerge fresh in design discussion rather than pre-baked.
- Sample one percent of last month's production logs as dynamic test cases for moving targets.
- Use lambdas and decorators that preserve identity types to wrap behavior without type system damage.
- Skip manual context compaction when using million-token models unless empirical evidence shows degradation.
- Frame Claude.md instructions with XML important-if blocks so the harness applies them only when relevant.
