---
title: "No vibes allowed (live coding with Claude and Code Layer) #27"
videoId: zNZs19fIDHk
url: https://www.youtube.com/watch?v=zNZs19fIDHk
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1: Ship hard features by splitting the work into three passes, research then plan then implement, each run in a fresh context window that reseeds only the relevant spec ("frequent intentional compaction").** This is the backbone the whole session hangs off and it explains the fresh windows, the 40% rule, on-demand docs, resumable plans, and reading the plan over the code.
VERDICT: 🔗 next-step video available (complements the Context Engineering class + auto-compact-and-handoff).

**Spine 2: Write the feature's user-facing documentation first and hand that doc to the agent as the executable spec (Amazon "working backwards").** A distinct, film-able technique with its own demo: authoring and refining a doc before any code exists.
VERDICT: ❌ net-new video available.

**Spine 3 (LATENT): When building an agent, inject a tool's past errors into context only at the moment that tool is about to be called again, not always and not never.** Dexter's "third option" beyond the keep-it-all vs delete-it-all debate. Appears in one tangent, so the eventual video needs extra sourcing.
VERDICT: ❌ net-new video available.

---

## Summary + counts

BoundaryML's Vaibhav and HumanLayer's Dexter live-code a BAML timeouts feature with Claude Code, demonstrating a research, plan, implement pipeline built on frequent intentional context compaction.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Research, plan, implement in three fresh windows

**The claim.** Complex features ship reliably when you split the work into three passes, research then plan then implement, each in its own fresh context window that holds only the spec relevant to that step.

**Why it is non-obvious.** The default is one long chat where research, planning and coding pile up until the window bloats and quality silently degrades. The folk intuition that "more context is better" is exactly backwards here.

**Why it is true.** Because a research subagent first documents how the codebase handles the relevant area and writes it to a markdown file, the planning model opens a clean window already carrying a baked understanding, so it drafts the plan in the sweet spot of the window instead of burning tokens rediscovering code. The implementer then starts fresh again with only the approved plan, so it never sees the confusing history of spec revisions. Each boundary is a deliberate compaction: discard noise, reseed signal.

**What it generalizes to.** Onboarding a new engineer by handing them a written architecture doc rather than making them read the whole repo, or a data pipeline where each stage passes a clean artifact forward.

**How it goes wrong.** On a scratch, unarchitected codebase there is no structure for research to find, so the pipeline underperforms; and research chasing 100% accuracy hits diminishing returns fast.

### Spine 2 — Documentation as the executable spec

**The claim.** Before writing any code, write the feature's user-facing documentation, and treat that doc as the spec you hand the agent.

**Why it is non-obvious.** People describe a feature in a ticket or a prompt and assume docs come last. This flips it: Amazon's "working backwards" applied to AI coding means the doc comes first, and it is the artifact everything downstream reads.

**Why it is true.** Because the doc must state exactly how the user experience looks, the precise keys like connect_timeout_ms and their nesting under an http block, it forces you to resolve ambiguity a loose prompt would leave open. When Vaibhav realized arbitrary top-level keys would pollute the option namespace, editing the doc to nest everything under http instantly re-specified the entire build. The single doc is what the research and plan phases anchor to, so a fix there propagates automatically.

**What it generalizes to.** API design, where writing the reference page or OpenAPI first surfaces contract problems before implementation, or writing a CLI's help text before its flags.

**How it goes wrong.** The doc can be underspecified (that idle timeout only matters during streaming was missing), so a domain expert still has to augment it; and a doc-as-spec that is never pruned drifts from reality. Note the sharp contrast with the school's build-it-twice: that video says the cheapest spec is a thrown-away first build; this is the opposite move for when a throwaway build is too expensive.

### Spine 3 — Just-in-time error injection when building agents (LATENT)

**The claim.** When you build an agent, do not blindly keep or drop tool errors. Inject a tool's past failures into context only at the moment that same tool is about to be called again.

**Why it is non-obvious.** The public debate is binary: Manus says leave every error in so the model learns from it, while the token-saving instinct says delete them. Dexter proposes a third path, conditional just-in-time injection, that most people never consider.

**Why it is true.** Because errors from a past SQL generation are only useful when the model is about to generate SQL again, you separate the model's declaration "I want to run SQL" from the actual generation step, and inject the last few failures only in that window. Every unrelated step stays clean of irrelevant error noise, yet the model still relearns "that table does not exist" precisely when it matters.

**What it generalizes to.** Any retrieval agent that should surface a document's prior failed parses only when re-parsing it, or a coding agent that shows a file's past lint errors only when editing that file.

**How it goes wrong.** It requires controlling the tool boundary to intercept the declaration, which many harnesses do not expose; and mis-scoping which errors count as "relevant" reintroduces the exact noise you were trying to avoid. The source treats it thinly in one off-topic exchange, so a full video needs extra sourcing.

---

## 🎬 Proposed ACS videos

### 1. Write The Docs First: Turn A Feature Doc Into Your Agent's Spec
- HOOK: The best spec for an AI coding agent is the documentation you have not written yet.
- THE PROMISE: For anyone shipping features with Claude Code, you leave able to turn a feature into a doc the agent implements against, instead of a vague prompt.
- THE SHAPE: 1) Vague ticket vs a written doc. 2) Write the user-facing doc with exact keys and nesting. 3) Catch an ambiguity (top-level namespace pollution) and fix it in the doc. 4) Hand the doc in as spec.md and kick off research. 5) Show the doc doubling as subtle steering.
- SPINE: Spine 2.
- SLOT: Techniques, new chapter alongside "The First Build Is a Prototype" (documentation-as-spec / working-backwards).
- RELATIONSHIP: ❌ net-new. Sibling to build-it-twice and the-shifting-bottleneck (both mention "spec"), but neither teaches writing user-facing docs first as the executable spec; build-it-twice argues the opposite (a throwaway build is the spec), which makes a great contrast beat.
- PROOF TO REUSE: Vaibhav, "documentation is a great specification. We're saying exactly how the user experience should look." The Amazon working-backwards reference. The http-key nesting fix that re-specified the whole build in one edit.

### 2. Research, Plan, Implement: The Three-Window Workflow For Hard Features
- HOOK: Stop coding in one long chat. Ship hard features in three fresh windows instead.
- THE PROMISE: For engineers using Claude Code on real, large codebases, you leave able to run a research pass, a planning pass, and an implementation pass that each start clean, so quality stops degrading as the window fills.
- THE SHAPE: 1) /research with codebase-locator and analyzer subagents writes a codebase doc. 2) A domain expert reads and corrects it (catches the missing orchestrator.rs). 3) Fresh window, /create-plan produces a phased plan. 4) Read and reorder phases around the smallest compilable slices. 5) Fresh window, /implement-plan with resumable checkboxes.
- SPINE: Spine 1.
- SLOT: Context Engineering (or Claude Code, building on the auto-compact-and-handoff correction).
- RELATIONSHIP: 🔗 complements the Context Engineering class and the auto-compact-and-handoff correction, which teach the compaction principle. This adds the concrete three-pass pipeline: dedicated research subagents, research-as-compaction-boundary, and resumable phased plans as the move after understanding compaction.
- PROOF TO REUSE: "the plan gives you 10x leverage. The research gives you a 100x leverage." "a bad part of a plan is 100 bad lines of code." The under-40% context rule. On-demand codebase docs regenerated in ten minutes.

### 3. Just-In-Time Errors: Inject Tool Failures Only When The Model Needs Them
- HOOK: Manus says keep every error in context forever. Here is the smarter third option.
- THE PROMISE: For people building agents, you leave able to inject a tool's past failures only when that tool is called again, keeping the rest of the window clean.
- THE SHAPE: 1) The keep-everything vs delete-everything debate. 2) Split "declare intent" from "generate." 3) Inject the last N failures only at the generation call. 4) Show unrelated steps staying clean. 5) Generalize to retrieval and lint errors.
- SPINE: Spine 3 (latent; sourced thinly in one tangent, needs extra sourcing to fill a full video).
- SLOT: Business / agent-building, new topic (dynamic context injection / conditional error injection).
- RELATIONSHIP: ❌ net-new. Adjacent to the backlog items dynamic-context-injection-for-skills and core-agent-loop, but neither is filmed and neither covers conditional just-in-time tool-error injection.
- PROOF TO REUSE: Dexter's algorithm (inject SQL errors only when a new SQL generation is requested). The contrast with Manus's "leave it in." Vaibhav, "the LMs are bad at judging things ... but they are good at reading errors and fixing them."

---

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's Vaibhav and HumanLayer's Dexter live-code a BAML timeouts feature with Claude Code, demonstrating a research, plan, implement pipeline built on frequent intentional context compaction.

### IDEAS
- Timeouts for BAML clients get implemented live from scratch using a research, plan, then implement pipeline.
- "Frequent intentional compaction" means starting fresh context windows so each phase reseeds only the relevant spec.
- The research document is written to be read by the next agent in a clean window.
- Subagents like codebase-locator, analyzer, and pattern-finder do parallel grunt research so the main window stays lean.
- Documentation for the unbuilt feature is written first, then treated as the executable specification for implementation.
- Opus is preferred for reasoning over large codebases; Sonnet is faster but weaker on complex reasoning.
- Reading every diff line matters; skipping it is why earlier vibe-coding attempts produced worse, unmaintainable code.
- Reading the research and plan gives more leverage than reading generated code because they are outlines.
- Domain experts must review research because only they catch a missing file the agent skipped, orchestrator.rs.
- Phases are designed around the smallest compilable, testable increment, then reordered so primitives finish before composites.
- Rust's compiler is leveraged as a safety net: if it compiles, the implementation probably works correctly.
- Tests give the model objective ground truth; models fix errors far better than they judge code.
- Dexter's error-compaction algorithm injects past tool errors only when the relevant generation tool is next invoked.
- When debugging keep error history; once the flow works, delete errors and reseed only the success.
- Recurring manual corrections should move into infrastructure: your create-plan command and agents, not repeated ad-hoc prompts.
- On-demand research replaces stale docs: regenerate an accurate codebase picture in ten minutes rather than maintaining.
- Voice dictation beats typing for prompting because you speak more freely and inject far more context.
- Keeping context under forty percent is the target; fresh windows beat letting autocompact silently degrade quality.

### INSIGHTS
- A bad line in a plan equals a hundred bad lines of code downstream from it.
- Leverage tops out: research gives hundredfold, plans tenfold; chasing thousandfold automation makes simple things weirdly hard.
- The spec need not stay synced with code forever; it only must be correct while implementing.
- Misunderstanding which parts of a system are relevant tanks an entire project more than sloppy code.
- Reading for fuzzy approximate correctness, not perfection, is enough; diminishing returns make perfect research not worthwhile.
- Paying the expensive model tax upfront beats stopping and restarting after a cheap model's wrong result.
- Feeling good about the process matters; if it feels bad, you abandon vibe coding before finishing.
- Consistent, same-shaped review checkpoints reduce context switching, which is what actually makes parallel agent sessions manageable.
- Codebase architecture quality determines whether this workflow works; scratch vibe-coded projects lack the structure it needs.
- No single prompting workflow fits every engineer; forced homogeneity kills the enjoyment that makes people productive.
- Building an eval system for a one-day prompting problem costs more than the problem is worth.

### QUOTES
- "If you don't read the code, you are going to be screwed." (Vaibhav)
- "the less of your context you use the better." (Vaibhav)
- "the plan gives you 10x leverage. The research gives you a 100x leverage." (Dexter)
- "a bad line of code is a bad line of code. A bad part of a plan is a 100 bad lines of code." (Vaibhav)
- "if you're not using Opus, you're not going to get good results." (Dexter)
- "the LMs are bad at judging things if you ask me, but they are good at reading errors and fixing them." (Vaibhav)
- "if you're not using voice, you're just slowing yourself down." (Matt, via chat, endorsed by Vaibhav)
- "The best engineers I know ... they don't use evals. They just know what works better cuz they spend 70 hours a week talking to Claude." (Vaibhav)
- "if it compiles, it probably works." (Vaibhav, on Rust)
- "you always want to be pretty aggressive about the context." (Dexter)
- "the research basically gives you on-demand up-to-date codebase documentation in ... 10 minutes or so." (Vaibhav)
- "most prompting ... is all vibes. And the best thing you can do is build a really really good vibe checker in your own brain." (Vaibhav)

### HABITS
- They start a new context window whenever usage approaches forty percent to keep the model sharp.
- They always have a codebase expert read research to verify nothing relevant is missing or wrong.
- Dexter uses SuperWhisper voice dictation for prompting and adds project vocabulary so it transcribes names correctly.
- They keep research artifacts, plans, and specs outside the codebase as separate per-project files, not committed.
- Vaibhav shims Python in his shell to force UV, blocking the agent from the wrong interpreter.
- They read the plan top-to-bottom in Obsidian reader view before approving, treating it as subtle steering.
- They run create-plan with no arguments so the interactive three-phase back-and-forth sets a better prompting trajectory.
- Vaibhav validates end-to-end tests himself even when the model reports passing, staying accountable for serious code.
- They auto-approve tool calls once confident, letting long compilation and test cycles run unattended in background.

### FACTS
- The BAML timeouts GitHub issue was first proposed on March eighteenth before this live implementation session.
- The BAML codebase contains roughly two hundred thousand lines of Rust plus substantial Go and scripts.
- BAML currently hard-codes default timeouts of a ten-second connect and thirty-second read inside its HTTP clients.
- WASM environments disable timeouts entirely, and AWS clients require special handling in the BAML request stack.
- Time-to-first-token and idle timeouts only apply during streaming calls, not standard non-streaming BAML function invocations at all.
- The whole timeouts feature was built in about three hours live versus roughly two engineer-days normally.
- Rust lacks good incremental compilation, and cargo's system lock prevents running parallel subagents within one package.
- Claude Code's default system prompt references Python, which is why shimming the interpreter prevents accidental misuse.
- The autocompact summary generated by the CLI is roughly three thousand five hundred words of state.

### REFERENCES
- BAML (BoundaryML) programming language for LLMs and AI agents.
- Code Layer / CodeLayer, Dexter's UI wrapper around Claude Code.
- HumanLayer, Dexter's company; public repo with the research/plan/implement prompts and subagents.
- Claude Code (Anthropic); Claude Opus and Sonnet 4.5 models.
- SuperWhisper voice dictation (and "whisper floats" / Whisper Flow mentioned).
- Obsidian, used as a markdown reader for plans and research in reader view.
- Amazon "working backwards" (write the doc or blog post first).
- Manus, referenced for its "keep the errors in context" recommendation.
- Warp terminal; cloc ("clock") line-counting tool; UV Python package manager.
- VS Code and Cursor; Tokio async ("Tokyo select/pin") in Rust.
- Codex (OpenAI CLI), mentioned for better uptime during API errors.
- "AI That Works," BoundaryML and HumanLayer's weekly Tuesday livestream series.
- Subagents: codebase-locator, codebase-analyzer, codebase-pattern-finder.
- Commands: /research, /create-plan, /implement-plan, /continue.

### ONE-SENTENCE TAKEAWAY
Research, plan, then implement in fresh context windows, reading and steering each artifact you keep.

### RECOMMENDATIONS
- Split any feature into research, plan, and implement phases, each running in its own fresh window.
- Write the feature's user-facing documentation first and hand that document to the agent as your specification.
- Install codebase-locator, analyzer, and pattern-finder subagents so research fans out cheaply without bloating your main window.
- Read the generated research and plan yourself, correcting missing files and wrong assumptions before approving implementation.
- Keep working context under forty percent and start fresh windows rather than trusting silent autocompaction quietly.
- Design plan phases around the smallest independently compilable slice, then reorder to finish primitives before composites.
- Move any correction you repeat into your create-plan command or a subagent instead of retyping it.
- Give the model objective tests and update-expect snapshots so it can fix errors instead of guessing.
- Dictate prompts by voice with a tuned vocabulary so you inject more context than typing would.
- Use a handoff-compaction command that writes a resume prompt starting with implement-plan and the plan path.
