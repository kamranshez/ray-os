---
video_id: Xq8VxnGVStg
title: "Claude Code Maxing - live coding: 🦄 #42"
url: https://www.youtube.com/watch?v=Xq8VxnGVStg
channel: BoundaryML
---

## SUMMARY

Vaibhav and Dexter live-code BAML compiler work, demonstrating Riptide's research-plan-implement workflow for shipping complex Rust and WebAssembly code without manual coding.

## IDEAS

- BAML virtualizes file systems and network calls by passing language-native callbacks down through WebAssembly into the runtime.
- Splitting one giant prompt into smaller sequential prompts replaces prompting-for-control-flow with explicit control flow between steps.
- Research must remain objective and avoid implementation details so models do not bake assumptions into downstream work.
- The lazy RPI users get help by auto-generating objective research questions before the actual research phase begins.
- Architecture diagrams as SVG sit perfectly in LLM context windows because they are small, readable, and structurally meaningful.
- Codegen the dependency diagram from a stow tool that enforces namespace boundaries through CI/CD failures automatically.
- Transitive reduction strips redundant edges from architecture graphs, making them easier for both LLMs and humans to digest.
- Better naming emerges naturally when you visualize dependencies, because awkward arrows reveal where modules actually belong.
- Vibe engineering means shipping at the speed of thought while still doing rigorous design and human review.
- Pipelining tasks beats waiting; start the next process while reviewing prior outputs to maximize wall-clock progress.
- Forking chat threads in parallel for sub-questions would unlock map-reduce style exploration during single design sessions.
- Cargo Stow enforces architectural rules across crates so LLM slop cannot silently introduce bad cross-namespace dependencies.
- Performance tests with COSE block PRs unless humans manually approve regressions, replacing code reviews with automated gates.
- A magnitude-of-change gate can require human signoff only when diffs exceed thresholds, scaling review where it matters.
- Structured outlines beat thousand-line plans because humans should not double-review markdown they will review again as code.
- Phases should be testable units, neither too big to verify nor too small to be worth a checkpoint.
- The model should keep rejected design options in context, so future steps know what was explicitly avoided.
- Reading every plan line carefully prevents architectural mistakes from compounding into thousands of lines of unreviewable slop.
- Speed of typing is no longer the bottleneck; clarity of thought and architecture is the only remaining gap.
- Vertical, integration-testable phases beat horizontal layered plans because you can validate progress before exhausting context windows.
- File systems supporting multiple concurrent editors via CRDT-like merges would unlock safer parallel agent writes.
- Obsidian's reader-writer mode prevents accidental edits, letting models do all writing while humans only consume markdown.
- Compaction works fine for casual yolo coding but becomes dangerous when shipping thousands of dialed-in production lines.
- The autonomy slider concept lets humans approve a structured outline once, then agents rip until PR-ready.
- Asking the model "is there a better way to organize this?" after design produces tighter phase reorderings.
- Web searches that return zero production examples are strong signals not to attempt that pattern.
- Junior AI engineers tab-tab-tab through suggestions, forcing reviewers to assume zero thought went into any decision.
- Forking checkouts beats worktrees for some brains because git merge mental models stay simpler with separate clones.
- Speech-to-text breaks creator flow because narrating to viewers competes with typing context for the model.
- Ten-thousand line PRs can ship as multiple research files plus structured outlines split into independently shippable plans.
- Code references baked into research output dramatically reduce downstream context spent locating relevant lines later.
- Adding a web-search researcher into RPI catches external best practices the codebase researcher would never discover alone.
- Sequential numbering of artifacts (01-research, 02-design) reminds the engineer of the chronological order things happened.
- The cloud web-search researcher is shallower than ChatGPT deep research, so absence of results means uncommon patterns.
- Building custom CI/CD tools is now an hour-and-a-half investment instead of a multi-day infrastructure project.
- Safety through culture beats safety through systems when the team is small and high-trust.

## INSIGHTS

- The ceiling on task complexity scales directly with how much context engineering you invest before implementation begins.
- Objectivity in research is the load-bearing constraint; subjective research baked with intent corrupts every downstream decision.
- LLMs are equally capable at simple and complex code; the bottleneck is whether the model truly understands.
- Engineering velocity now depends on architectural clarity, not typing speed, because agents handle the mechanical translation.
- Visualizing system dependencies converts naming debates into geometry problems where bad names appear as awkward arrows.
- Splitting monolithic prompts into pipelined steps lets you context-engineer each stage independently for higher overall quality.
- Wall-clock time matters more than token cost because human attention degrades faster than budgets ever could.
- Plans should not require code review because they will be reviewed again when the actual code lands.
- Magnitude-aware quality gates outperform file-based ownership rules because change size predicts review value better than location.
- The hardest part of AI engineering is having focus to read every line carefully when scrolling tempts you.
- Models should always preserve rejected alternatives in design docs, so future agents and humans see explicit decisions.
- Phase boundaries should align with verifiable checkpoints; otherwise the agent flies blind through unbounded uncertainty.
- Forking conversations for sub-research is the missing primitive in coding agents for high-context exploration tasks.
- Tools that enforce architectural invariants in CI prevent agentic codebases from collapsing under accumulated naming and dependency slop.
- The best teams replace synchronous code review with asynchronous architectural enforcement plus performance and binary-size gates.

## QUOTES

- "We're just going to ship until me and Vaibhav are exhausted, basically." Dexter
- "I don't think I've written a single line of code by hand." Vaibhav
- "Vibe coding means you don't give a fuck about the code." Vaibhav
- "It's engineered. We've done heap allocators. We've done all sorts of things." Vaibhav
- "We don't do code reviews at all and we ship a pretty complex system." Vaibhav
- "The research must remain objective because you don't want the model to know about what we're building." Dexter
- "There's no shortcut to that." Vaibhav
- "I'm literally shipping as much code as possible at the speed of thought." Vaibhav
- "Don't make humans read any more markdown than they have to." Dexter
- "Complex is not necessarily bad. Complicated is like complex and unsafe basically." Dexter
- "If you're just going to accept everything that the AI chooses, then you're not doing the thinking." Dexter
- "The clarity of your thoughts and your architecture is really the only gap." Vaibhav
- "We're only optimizing for wall clock time, not for token time." Vaibhav
- "I will refrain from and hold myself back and not do this." Vaibhav
- "It's basically like safety through culture rather than through systems that enforce stuff." Dexter
- "I have never read this much in my life." Vaibhav
- "Bash configured considered harmful." Dexter
- "We're not going to pass raw bytes because we are not animals." Vaibhav
- "There are no real zero production examples of anyone doing this." Vaibhav
- "It's not just about the final artifacts that we create." Vaibhav
- "You can't actually test anything until it's done." Dexter
- "How can we reorder the phases so that each of these chunks is independently shippable?" Dexter
- "I get distracted and now I'm off doing my own thing." Vaibhav
- "There's just not enough concept here." Vaibhav

## HABITS

- Always read the full design document, never trust the chat summary as a sufficient review.
- Pipeline aggressively; kick off the next agent task while reading the previous output for review.
- Switch Obsidian to reader mode while reviewing to prevent accidental edits during agent-driven document work.
- Use voice input for ticket descriptions to capture context faster than typing during ambiguous task framing.
- Numerically prefix artifact filenames so chronological creation order is preserved across the agent workspace.
- Maintain four separate repo checkouts instead of git worktrees when worktree mental models feel too heavy.
- Skim research documents only for foundational gaps, trusting the objectivity constraint to catch most details.
- Queue all answers to design questions in a single message rather than answering one by one.
- Save every design discussion artifact to disk so context can be rebuilt from documents after compaction.
- Cancel and restart processes immediately when prompts contain mistakes rather than trying to recover mid-flow.
- Keep clipboard history enabled because parallel multitasking with agents requires juggling many text snippets simultaneously.
- Run COSE performance tests on every PR with mandatory human approval for any detected regression.
- Reset context windows by reloading saved documents rather than relying on auto-compaction for serious work.
- Never review the chat summary alone; always open the full markdown file before answering questions.
- Ask Claude to suggest better names for systems whose dependency arrows look architecturally awkward in diagrams.

## FACTS

- BAML now contains a custom heap allocator, garbage collector, FFI bridges, and instruction bytecode like JVM.
- Tokio breaks WebAssembly builds because async behavior diverges across language runtimes in subtle dependency ways.
- JSPI is an emerging V8 standard letting WebAssembly code interoperate with JavaScript promises more natively.
- The BAML team's architecture diagram lives as a 719-line SVG that fits in any LLM context.
- Cargo Stow is BoundaryML's namespace enforcement tool inspired by Rails monorepo ingress and egress rule packages.
- Wasm-bindgen is the standard Rust crate for bridging WebAssembly modules to JavaScript callable interfaces.
- Semi-space garbage collection is an alternative to generational GC that BoundaryML implemented for the BAML runtime.
- A 20,000 line PR was shipped using three structure outlines split into four separately implementable plans.
- Mermaid uses Graphviz under the hood for diagram layout but lacks customization needed for publication-quality output.
- The "AI That Works" podcast streams every Tuesday at approximately 10:10 AM with weekly live coding episodes.
- BoundaryML built a 4,000-line memory-safe garbage collector entirely through agentic coding without writing manual code.
- The new BAML runtime is called Beex Engine, the BAML execution engine analogous to V8.
- BoundaryML rebuilt their entire coding agent harness called Riptide from the ground up over months.
- CRDT systems like YJS power Google Docs by maintaining deterministically mergeable operation logs across collaborating clients.
- A 10,000 line single-plan PR fails because plan reading alone consumes too much context window space.

## REFERENCES

- BAML compiler and runtime (Beex Engine, Beex VM)
- Riptide (BoundaryML's experimental new coding agent harness)
- Cargo Stow (custom Rust dependency enforcement tool)
- Wasm-bindgen
- Tokio (Rust async runtime)
- JSPI (JavaScript Promise Integration for WebAssembly)
- Graphviz / Mermaid
- COSE (performance testing tool)
- Obsidian
- 12 Factor Agents for Coding Agents (prior episode)
- Claude Code
- Simon Willison and the term "vibe engineering"
- Cursor (plan-to-implement comparison)
- The HumanLayer RPI prompts repository
- YJS / CRDTs
- Zen of Python
- ChatGPT Deep Research
- AI That Works podcast and GitHub repo
- Cloudflare Workers
- WASI runtime
- Producer Kevin (show automation)

## ONE-SENTENCE TAKEAWAY

Speed of thought beats speed of typing when architectural clarity replaces typing as the engineering bottleneck.

## RECOMMENDATIONS

- Split your monolithic RPI prompt into research-questions, research, design, structured-outline, and plan as discrete pipelined stages.
- Generate an SVG architecture diagram and feed it to LLMs instead of text-based codebase descriptions whenever possible.
- Build a namespace enforcement tool that fails CI when LLM-introduced cross-crate dependencies violate architectural rules.
- Add a magnitude-of-change CI gate requiring manual human approval for diffs exceeding a thousand lines.
- Run performance regression tests on every PR with mandatory signoff for any detected slowdown above threshold.
- Save every research, design, and plan artifact to disk with sequential numbered prefixes for context recovery.
- Pipeline your agent work; start the next stage while reviewing the previous to maximize wall-clock throughput.
- Ask the model to reorganize structured outlines into independently shippable phases before committing to implementation work.
- Use Obsidian's reader mode while reviewing agent-generated documents to prevent accidental edits during human review.
- Force the design phase to preserve rejected options so downstream steps understand explicit architectural decisions made.
- For tasks above ten thousand lines, write multiple research files and split plans across phases.
- Configure your coding agent to auto-generate objective research questions before any actual research begins.
- Add a web-search researcher to your RPI loop for external best practices not found in your codebase.
- Cancel and restart agent processes immediately when prompts contain mistakes rather than recovering mid-flow.
- Build code reference extraction into research output so downstream agents waste less context locating relevant lines.
- Skip code reviews on small changes but enforce architectural and performance gates through automated CI checks.
- Treat zero-result web searches for a coding pattern as a strong signal to choose a different approach.
- Use voice input for ambiguous ticket descriptions to capture nuance faster than careful typing typically allows.
- Build cultural norms around quality so trusted teams can skip mandatory reviews without sacrificing codebase health.
- Stop reading thousand-line plans line-by-line; refactor your workflow to use shorter structured outlines for human alignment.
