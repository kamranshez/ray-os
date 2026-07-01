---
title: "Claude Code Maxing - live coding"
videoId: Xq8VxnGVStg
url: https://www.youtube.com/watch?v=Xq8VxnGVStg
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works (Vaibhav Gupta + Dexter Horthy)
---

# The one idea worth a video

**1. Ship AI code without code reviews by replacing per-line review with automated architecture guardrails plus magnitude-gated human sign-off.** They ship a garbage collector and a compiler with zero code reviews because a custom CI tool (cargo stow) fails the build the moment an LLM draws an invalid dependency arrow, and only large or complex diffs demand a human to sign off.
VERDICT: ❌ net-new video available

**2. Run the research phase with the goal deliberately withheld, so the model compresses the truth of the system instead of biasing toward a solution.** A separate step turns the ticket into objective questions, then a fresh context window answers them with the "what we are building" stripped out, keeping research unbiased and reusable.
VERDICT: 🔗 next-step video available (complements "What breaks if I change this?")

**3. Order the plan as vertical, independently verifiable slices sized to one context window, not horizontal layers you can only test at the end.** The structured outline stays high-level for human alignment; each phase gives the model a feedback loop instead of 2,000 untestable lines.
VERDICT: 🔗 next-step video available (complements "Build Small, Merge Big")

---

## Summary

Vaibhav (BoundaryML) and Dexter (HumanLayer) live-code a WebAssembly bridge in BAML, demonstrating enhanced research-plan-implement workflow, objective research, architecture-boundary CI enforcement, and shipping without code reviews.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Architecture guardrails replace code review

**The claim.** You can ship large volumes of AI-generated code with no code reviews if you replace per-line review with automated architecture enforcement plus a human gate keyed to change magnitude.

**Why it is non-obvious.** The reflexive assumption is that removing code review yields slop. Vaibhav argues the reverse: reviews are the wrong tool for LLM velocity, because an agent can produce a thousand plausible lines faster than a human can read them. The failure you actually fear is structural, not stylistic.

**Why it is true.** Three mechanisms compound. First, the architecture is a canonical auto-generated dependency diagram (a transitive-reduced SVG), so "correct shape" is a checkable artifact, not tribal knowledge. Second, cargo stow encodes namespace and crate boundary rules and fails CI the instant an LLM adds a forbidden dependency arrow, catching slop before it compounds. Third, a magnitude gate (over a thousand changed lines, a CodSpeed performance regression, a binary-size jump) forces an explicit human sign-off, so scarce attention lands only where risk concentrates.

**What it generalizes to.** Any monorepo: Rails packwerk ingress/egress rules, or a TypeScript workspace enforcing import boundaries in CI.

**How it goes wrong.** Boundary rules need upkeep; magnitude is a proxy, since a five-line change can still be catastrophic; and, as Dexter notes, it runs on trust and culture, not just tooling.

### Spine 2 — Objective research: withhold the goal

**The claim.** Run your research phase with the objective deliberately hidden, so the model compresses the current truth of the codebase rather than reaching for a solution.

**Why it is non-obvious.** Almost everyone hands the researcher the ticket: "here is what I am building, go research it." Dexter's point is that this poisons the output. The model "focuses more on information about how to solve the ticket" and bakes in premature implementation details, which is just the model picking the next likely token instead of pulling the human in to decide.

**Why it is true.** They split one step into two: a step that turns the ticket into objective questions, and a fresh context window that answers only those questions with the input query deleted. Because the researcher cannot see the goal, it stays objective, its output is reusable across attempts, and it emits code references that make downstream grep cheap.

**What it generalizes to.** Incident investigation or literature review, where "what is true" must be separated from "what we hope to conclude."

**How it goes wrong.** Pure objectivity can drop goal-relevant context; Vaibhav admits the input query is "sometimes useful," so a human still skims research for foundational misses.

### Spine 3 — Vertical, verifiable phase slicing

**The claim.** Order your plan into vertical phases that are each independently verifiable and sized to fit one context window, rather than horizontal architectural layers.

**Why it is non-obvious.** Coding agents default to horizontal plans: database layer, then services, then API, then UI. Dexter's warning is that "you can't actually test anything until it's done," so you discover the break at line 2,000 with no idea where it lives.

**Why it is true.** They separate a high-level structured outline (used for human mental alignment and cheap to reorder) from the detailed plan generated later. Ordering steps so each ends at a unit or integration checkpoint mirrors how a human codes: write fifty lines, run a test, write a hundred more, run the CLI. The phase-sizing rule follows: big enough to be worth verifying, small enough for one context window.

**What it generalizes to.** Any large multi-module feature; a 20,000-line PR shipped as three outlines split across four independently shippable plans.

**How it goes wrong.** Not every problem has a clean integration test; over-slicing induces artificial phases and slop; and for trivial tasks you should just tell the model to rip the whole plan.

---

## 🎬 Proposed ACS videos

### 1. Ship Without Code Review (net-new)

- **TITLE:** How to Ship AI Code Without Code Reviews
- **HOOK:** BoundaryML ships a whole garbage collector with zero code reviews. Here is the machinery that makes that safe.
- **THE PROMISE:** For engineers letting agents write at volume: replace line-by-line review with guardrails a human can actually trust.
- **THE SHAPE:**
  1. The problem: agents out-type any reviewer, so per-line review is the wrong gate.
  2. Make architecture a checkable artifact: auto-generate a transitive-reduced dependency diagram.
  3. Enforce it in CI: a boundary tool (cargo stow) fails the build on any invalid dependency arrow.
  4. Gate humans on magnitude: over a thousand lines, a perf regression, or a binary-size jump forces explicit sign-off.
  5. The culture caveat: guardrails plus trust, not one or the other.
- **SPINE:** 1
- **SLOT:** Techniques (backlog: sits beside subagent-verification-loops, closing-the-loop) or Context Engineering
- **RELATIONSHIP:** ❌ net-new. Closest neighbor is "What breaks if I change this?", which teaches asking the agent to draw the blast radius once before a change; this video is the continuous-enforcement sibling: the diagram becomes a CI gate and review is keyed to change magnitude, which no current ACS video covers.
- **PROOF TO REUSE:** "we don't do code reviews at all and we ship a pretty complex system"; cargo stow failing CI on bad namespace arrows; CodSpeed performance-regression gate requiring manual approval; "if someone made like a thousand line change, have them at least manually approve."

### 2. Keep Your Research Honest (complements "What breaks if I change this?")

- **TITLE:** Hide the Goal: How to Get Honest Research From an Agent
- **HOOK:** The fastest way to ruin agent research is telling it what you are building.
- **THE PROMISE:** For anyone running a research-then-build loop: get a map of the system that is not already contaminated by your intended solution.
- **THE SHAPE:**
  1. The default failure: hand the ticket to the researcher and it bakes in implementation bias.
  2. Split it: one step writes objective questions, a fresh context answers them.
  3. Delete the input query so the researcher cannot see the goal.
  4. Why this pays off: objective, reusable research with code references that cut downstream grep.
  5. The limit: skim for foundational misses, because sometimes the goal was useful context.
- **SPINE:** 2
- **SLOT:** Context Engineering (chapter: Understanding the System, next to "What breaks if I change this?")
- **RELATIONSHIP:** 🔗 complements "What breaks if I change this?" by being its next step. That video teaches getting the agent to map the system before you change it; this adds the discipline of running the research phase itself with the goal withheld so the map stays unbiased. Ray should not re-teach "make the agent draw the system"; this video is purely about de-biasing the research context.
- **PROOF TO REUSE:** "the goal of research is really to like compress truth to compress the state of the world today"; "you don't want the model to know about what we're building"; the two-phase questions-then-research split; "this code references... makes graping for the model so much easier in downstream processes."

### 3. Vertical Plans (complements "Build Small, Merge Big")

- **TITLE:** Stop Writing Horizontal Plans
- **HOOK:** Most agent plans build the database, then services, then UI, and you cannot test any of it until line 2,000.
- **THE PROMISE:** For anyone planning a big multi-module change: order the work so the model gets a feedback loop at every phase.
- **THE SHAPE:**
  1. The horizontal trap: layers you cannot verify until the end.
  2. Vertical slices: each phase ends at a testable or shippable checkpoint.
  3. Structured outline first (high-level, for human alignment), detailed plan later.
  4. Phase sizing: big enough to be worth checking, small enough for one context window.
- **SPINE:** 3
- **SLOT:** Techniques (chapter alongside build-small-merge-big, which is currently in Doing)
- **RELATIONSHIP:** 🔗 complements "Build Small, Merge Big" by being its planning-time counterpart. That video teaches shipping small increments and merging big; this adds how to order the plan's phases as vertical, independently verifiable slices before any code is written. Ray should not re-teach small-PR hygiene; this is about phase ordering and sizing.
- **PROOF TO REUSE:** "you can't actually test anything until it's done"; "the phase should not be so big that the model can't complete it in one context window and it should not be so small that there's nothing to verify at the end"; the 20,000-line PR split into three outlines and four plans.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BoundaryML) and Dexter (HumanLayer) live-code a WebAssembly bridge in BAML, demonstrating enhanced research-plan-implement workflow, objective research, architecture-boundary CI enforcement, and shipping without code reviews.

### IDEAS
- They split the monolithic research-plan-implement prompt into smaller staged prompts, each solving one distinct planning part.
- Research generates objective questions first; the researcher never learns what you're actually building, avoiding solution bias.
- A separate step turns the ticket into objective research questions before any codebase research even begins.
- Deleting the input query from research keeps the model from baking in premature implementation detail assumptions.
- The architecture is an auto-generated SVG dependency diagram that fits entirely inside an LLM context window.
- Transitive reduction removes redundant dependency arrows, showing only the minimal graph humans and models easily digest.
- Cargo Stow enforces namespace boundary rules in CI, failing builds when LLMs add invalid crate dependencies.
- They routinely ship complex Rust systems, including a whole garbage collector, without doing any code reviews.
- Gate CI on change magnitude: over a thousand lines requires manual human approval before merging it.
- Structured outlines stay high-level and concise, used for team alignment; the detailed plan comes later separately.
- Order plan phases vertically so each is independently testable, not horizontal layers testable only at end.
- Each phase should be big enough to be worth verifying, small enough for one context window.
- Optimize for wall-clock time, not token cost; pipeline the next step while reviewing the previous output.
- Number workflow artifacts sequentially: 01 research questions, 02 research, 03 design, preserving the working order automatically.
- Skim research for missing foundations rather than reading deeply; the design discussion surfaces any gaps later.
- The complexity ceiling of a solvable task scales with context-engineering and design effort you invest upfront.
- Reading the plan line-by-line catches architectural bugs that granular workflows surface but fast skimming would miss.

### INSIGHTS
- Research must compress the current truth of the system, staying objective, not proposing how to solve.
- Withholding the goal prevents the model from picking likely tokens instead of surfacing decisions for humans.
- Clarity of your architecture, conveyed simply, is the real gap when vibe coding large complex systems.
- Complexity is fine if the model understands it; the LLM finds all approaches roughly equally complex.
- Enforce quality through systems and culture, not mandatory reviews; reserve human sign-off for large risky changes.
- The diagram exposed real bugs: a compiler depending on the VM revealed a misplaced type crate.
- Human time dwarfs token cost; distraction and context-switching are worse than paying for extra model tokens.
- Plan-to-implement suffices for simple tasks; large multi-module changes need the fuller research-plan-implement investment to actually succeed.
- Accepting every AI suggestion forces reviewers to re-check everything, since no human thought was ever applied.
- Keeping rejected options documented lets humans and models see decisions were deliberate, enabling later reasoned discussion.

### QUOTES
- "the clarity of your thoughts and your architecture is really the only gap" — Vaibhav
- "the goal of research is really to like compress truth to compress the state of the world today" — Dexter
- "we're all just shipping as much code as possible at the speed of thought" — Vaibhav
- "you don't want to make a pull request that is like a pain in the ass to review" — Dexter
- "I don't actually care about complexity when I go write things ... The only question is does it understand it?" — Vaibhav
- "safety through culture rather than through systems that enforce stuff" — Dexter
- "We're only optimizing for wall clock time, not for token time." — Vaibhav
- "in the last three or four months ... I don't think I've written a single line of code by hand" — Vaibhav
- "the ceiling goes up with how much of this context engineering and design that you're willing to do" — Dexter
- "it's very easy to scroll through this file be like yep yep yep and not catch this line" — Vaibhav
- "Vibe coding means you don't give a [expletive] about the code ... I think it's just software engineering." — Vaibhav

### HABITS
- Vaibhav uses voice and speech-to-text for most agent prompts, narrating intent instead of typing detailed written instructions.
- He always reads the summary first but never answers questions without reading the full document too.
- He reads all markdown inside Obsidian reader mode, which prevents him from accidentally editing model-owned documents.
- He queues all answers to the design questions in one message rather than replying to each individually.
- He pipelines aggressively, kicking off the next step while he is still reviewing the previous output.
- When a pipeline goes bad, he simply kills the process and the context and restarts completely fresh.
- He keeps multiple clipboards and several separate repo checkouts, admitting he still cannot learn git worktrees.
- The team copies design discussion documents to teammates so they gain context and can review them.
- They run performance tests through CodSpeed in CI, failing PRs on any substantial performance regression detected.
- Vaibhav reads plans in full despite Dexter recommending against it, and finds real bugs inside them.

### FACTS
- Tokio is a Rust library for multiprocessing and async workflows that behaves poorly under WebAssembly compilation.
- WebAssembly is sandboxed by design, lacking default access to both the file system and network interfaces.
- JSPI is the WebAssembly JavaScript Promise Integration API from V8, not yet widely available across browsers.
- BAML compiles source into its own bytecode instruction set, similar to how JVM and Python work.
- SVG files are LLM-friendly because they are small text; a 719-line diagram fits a context window.
- CRDTs, the technology powering Google Docs, use an operation log that merges deterministically across concurrent editors.
- Graphviz uses the dot language, and its layout APIs are either too low-level or too brittle.
- A semispace garbage collector differs from generational collection; BAML implemented one, roughly four thousand generated lines.
- GitHub CODEOWNERS is file-based, making it too heavy for enforcing rules based on change magnitude alone.
- One recent PR shipped roughly 20,000 lines using three structured outlines split across four separate plans.

### REFERENCES
- BAML and BoundaryML (the DSL, compiler, and company)
- Beex, the BAML execution engine (their "V8 alternative")
- The CIS crate (system-call bridging across languages)
- cargo stow (their custom namespace/crate boundary enforcement tool)
- Code Layer / Riptide (their rebuilt RPI tool that powers the VS Code extension)
- RPI (Research-Plan-Implement) and the canonical HumanLayer repo prompts
- The "12-factor agents for coding agents" episode
- Obsidian (markdown reading, reader/writer mode)
- Excalidraw (architecture sketching on stream)
- Graphviz / dot and Mermaid (layout engines)
- wasm-bindgen and wasm-bindgen-futures (Rust WASM crates)
- Tokio (Rust async runtime) and the WASI runtime
- JSPI (V8 WebAssembly JavaScript Promise Integration)
- CodSpeed (CI performance testing)
- CRDT / YJS (concurrent document editing)
- Claude Code (compaction, worktrees, forking a chat thread)
- Cloudflare Workers
- Simon Willison and the term "vibe engineering"
- Prisma (cited for Rust-to-WASM boundary performance problems)
- GitHub CODEOWNERS
- Protobuf and JSON serialization
- "AI That Works" weekly show (Vaibhav Gupta and Dexter Horthy), producer Kevin

### ONE-SENTENCE TAKEAWAY
Invest in staged, objective context engineering upfront; the hardest task you can solve scales accordingly.

### RECOMMENDATIONS
- Separate research-question generation from research, and strip the goal so your research phase stays fully objective.
- Have your agent auto-generate a transitive-reduced dependency diagram small enough to fit its whole context window.
- Enforce namespace and dependency boundary rules during CI so bad LLM-introduced architecture automatically fails the builds.
- Gate mandatory human review on change magnitude, requiring explicit sign-off only for large or complex diffs.
- Order your plan into vertical phases, each independently verifiable, instead of untestable horizontal architectural layers only.
- Size each implementation phase to fit one context window while still leaving something concrete worth verifying.
- Number your workflow files sequentially so their order reveals how you actually worked through the task.
- Optimize for wall-clock time by paying for tokens freely and pipelining steps to keep your momentum.
- Preserve rejected design options in your documents so future context shows choices were deliberate, not accidental.
- Read plans and code with real focus; scrolling past one bad line ships architectural slop downstream.
