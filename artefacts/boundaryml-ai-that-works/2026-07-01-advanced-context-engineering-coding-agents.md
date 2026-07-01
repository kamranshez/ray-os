---
title: "Advanced context engineering for coding agents #17"
videoId: 42AzKZRNhsk
url: https://www.youtube.com/watch?v=42AzKZRNhsk
date: 2026-07-01
status: posted
source: BoundaryML "AI That Works" (Vaibhav, BAML) with Dexter (HumanLayer)
---

## The one idea worth a video

**Spine 1 (flagship): Intentional compaction.** You manage the context window as a scarce budget by hand-writing your working state into a markdown file (with file plus line pointers), clearing the thread, and resuming, targeting under fifty percent utilization, because /compact preserves the information but keeps the polluting trajectory.
VERDICT: 🔗 next-step video available (complements the shipped 1M context video).

**Spine 2: The research, plan, implement workflow with read-only research sub-agents.** Split coding into three checkpointed phases and make research its own cited artifact, produced by read-only sub-agents and reviewed by a human before any plan exists.
VERDICT: 🟡 partial (the core workflow is already covered; only the research-as-a-reviewed-phase angle is missing, so no new pitch).

**Spine 3: The error-cost leverage hierarchy, so review the research and plan, not the code.** A bad line of research becomes a thousand bad lines of code, so put human attention at the top of the funnel and treat code review as mental alignment, not bug hunting.
VERDICT: 🔗 next-step video available (complements the blast-radius verification idea on a different axis).

---

## Summary and counts

Vaibhav (BAML) and Dexter (HumanLayer) demo context-engineering for Claude Code: intentional compaction, read-only research sub-agents, and a research, plan, implement workflow where you review specs, not code.

🔴 0 net-new · 🔗 2 complement · 🟡 1 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: Intentional compaction

The claim: treat the context window as a budget you actively manage by hand-compacting your own working state into a markdown file, clearing the thread, and resuming, aiming to stay under fifty percent utilization. Most people do one of two things: let a single thread grow forever, or reach for /compact. Dexter argues /compact "sucks" for high performance because "it's not just the information in the prompt, it's also the trajectory." The mechanism has two steps. First, every user message and tool call resends the entire window, so as the thread grows, stale searches and dead ends dilute the density of "what is the right next step" signal. Second, because the model attends over all of it, that noise degrades the next action, so compressing to a hand-written progress file (path plus line number, never full file dumps) and starting fresh restores signal density. He frames it as defragging a fragmented disk. This generalizes to any long-running LLM pipeline, for example their custom tool that pulls a noisy Linear ticket into compact markdown in one call. It goes wrong if you over-compact and drop a constraint the next thread needed, and it is manual labor that demands judgment about what to keep.

### Spine 2: The research, plan, implement workflow

The claim: separate coding into three checkpointed phases, and make research a first-class artifact produced by read-only sub-agents and reviewed by a human before a plan is written. The default is a single thread that reads, searches, and fixes all at once. The reframe is that discovery is a separate deliverable, and sub-agents are "not for playing house, they are for exactly one thing, which is context control." A read-only sub-agent burns its search calls inside a throwaway window and returns a tight answer naming the exact files and lines. The mechanism: a research document that names files and line numbers reduces the next agent's job to "read this file at these line numbers," which Dexter calls "ten times less work," and the explicit checkpoints stop scope creep ("oh, I'll fix this too"). Dexter ran a with-research plan and a no-research plan in parallel worktrees and compared the PRs. This generalizes to onboarding a human engineer, where the research doc is exactly the twenty-minute codebase walkthrough. It goes wrong because research can be flat wrong (his first pass claimed there was no bug), it needs steering against a known-true axiom, and a huge research pass can push the window past eighty percent and wreck the plan.

### Spine 3: The error-cost leverage hierarchy

The claim: errors compound upward through the artifact stack, so human review belongs at the top, not on the code. A bad line of code is one bad line, a bad line in a plan is ten to a hundred, a bad line of research is roughly a thousand, and a bad core prompt is roughly a hundred thousand. Everyone reviews the diff, but by the time bad code exists the expensive mistake already happened upstream. Dexter's team has Linear columns for research-in-review and plan-in-review, reads the research and plan closely, and "barely" reads implementation code, gating instead on well-designed passing tests. The mechanism: because each upstream artifact multiplies into the layer below, a misunderstanding in research (where functionality lives) misroutes the plan, which misroutes hundreds of code lines, so the marginal minute of attention returns far more spent on research. Per Blake Smith, code review's real job is "mental alignment, keeping people on the same page about how the system is changing," and a two-hundred-line spec is easier to grok than an out-of-order PR. This generalizes to any org where a distinguished engineer signs off on the design, not every line. It goes wrong if tests are untrustworthy, if the reviewer never actually reads the research (most people throw it away), or on algorithmically complex code that still needs human eyes.

---

## 🎬 Proposed ACS videos

### 1. Why I Never Let Claude Code Pass 50% Context

- TITLE: Why I Never Let Claude Code Pass 50% Context
- HOOK: The slash-compact command is quietly making your agent dumber on long tasks. Here is the manual move that beats it.
- THE PROMISE: For anyone whose long Claude Code sessions get worse over time. After this you can hand-compact your own context and keep the agent sharp on big features in large codebases.
- THE SHAPE: (1) show a proxy trace where 99 percent of the window is system, tools, and instructions; (2) show every tool call resending the whole window and diluting signal; (3) the defrag-the-disk metaphor; (4) write a progress file with file plus line pointers, not dumps; (5) /clear and resume from that file, targeting under 50 percent, and explain why /compact keeps the polluting trajectory.
- SPINE: 1
- SLOT: Context Engineering > (new) Managing the Working Window (neighbour of Claude Code > 1M Context Window and the auto-compact-and-handoff correction).
- RELATIONSHIP: 🔗 complements "12-1m-context-window", which teaches wide ingest, distill into artifacts, then execute in narrow windows using the 1M window. That video already teaches the intake-versus-working-memory split and scout, worker, synthesizer. This adds the everyday manual discipline for the ordinary 200K thread: deliberate mid-task compaction targeting 50 percent, and why /compact loses the trajectory rather than just information.
- PROOF TO REUSE: the captured proxy trace showing 99 percent of the window is not your prompt; "compact... I personally think it sucks... it's also the trajectory"; the disk-defragmentation analogy; "we try to target maximum like 50% context utilization."

### 2. Review the Research, Not the Code

- TITLE: Review the Research, Not the Code
- HOOK: You are reviewing the wrong artifact. The expensive mistake happened three steps before the code was written.
- THE PROMISE: For engineers drowning in AI-generated diffs. After this you know exactly where to spend limited review attention so the costliest errors get caught early, and when passing tests are enough.
- THE SHAPE: (1) draw the four-layer cost pyramid (code is 1, plan is 10 to 100, research is ~1000, core prompt is ~100,000); (2) show the Linear board with research-in-review and plan-in-review gates before any code; (3) skim a 120-line research doc and catch the wrong file; (4) read the tests, not the implementation, to trust the code; (5) reframe code review as mental alignment, citing Blake Smith.
- SPINE: 3
- SLOT: Code Review (ideas/code-review) or Fundamental Techniques.
- RELATIONSHIP: 🔗 complements "blast-radius-proportional-verification", which tiers verification by business blast radius (internal, external, safety-critical). This adds an orthogonal axis: tier your review by artifact altitude and move human attention up the funnel to research and plan, plus the mental-alignment purpose of review. Do not re-teach the risk-tiering taxonomy; this video is about which artifact to read, not which code tier deserves rigor.
- PROOF TO REUSE: the 1 / 10-100 / 1000 / 100,000 leverage hierarchy; "everybody reviews the research... research in progress, research in review before... ready to plan"; "the most important thing about code review is not... finding bugs... it's mental alignment"; "you have to read the [stuff] that the model spits out."

(Spine 2 produces no pitch: the research, plan, implement workflow and its sub-agents are already substantially covered by 12-1m-context-window (scout, worker, synthesizer) and the spec-driven-development idea set. The only missing angle is research as its own explicitly reviewed phase, which is folded into Pitch 2.)

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BAML) and Dexter (HumanLayer) show how to engineer Claude Code's context window: intentional compaction, read-only research sub-agents, a three-phase workflow, and reviewing specs over code.

### IDEAS
- Ninety-nine percent of Claude Code's context window is system prompt, tools, and instructions, not your message.
- Every new user message resends the whole context window, so longer threads dilute the useful-signal density.
- Intentional compaction means hand-writing progress into a markdown file, then clearing the thread and resuming fresh.
- The slash-compact command loses the reasoning trajectory, not just information, which is why Dexter avoids it.
- They target maximum fifty percent context utilization because that is generally plenty for any good task.
- Progress files store path plus line number, not dumps, to avoid refilling the window with noise.
- Sub-agents exist for context control, a fresh window whose bulky search calls never reach the parent.
- Read-only research sub-agents return a tight answer naming the exact files and lines to touch next.
- A three-phase workflow separates research, planning, and implementation with human checkpoints between each intentional stage boundary.
- Errors compound upward: bad code is one line, bad research is roughly a thousand bad lines.
- A bad core prompt can produce a hundred thousand bad lines across everything it later generates.
- Their Linear board tracks research-in-progress, research-in-review, and ready-to-plan columns well before any implementation code is written.
- Dexter ran a with-research and a no-research plan in parallel worktrees, then compared the resulting PRs.
- TDD is presented as the only sane way to write AI-generated code with agents reliably today.
- Test commands must be trivial for the model to run, or the whole TDD loop breaks.
- Consistent nomenclature matters: a model cannot act correctly if one concept has seven different names everywhere.
- CLAUDE.md gets injected with a caveat saying it may not be relevant, weakening its instructions considerably.
- Open Claude Code in the integrated terminal with the VS Code extension to get LSP errors.

### INSIGHTS
- Understanding how the context window is assembled is what lets you deliberately engineer and hack it.
- Human attention is scarce, so spend it upstream where a single mistake multiplies most expensively downstream.
- Code review's real purpose is mental alignment about system evolution, not finding bugs or correctness issues.
- A short spec is far easier to review and grok than an out-of-order pull request diff.
- Well-designed passing tests give enough confidence to skip line-by-line review of the implementation code entirely today.
- Compaction is like defragging a disk: reorganize what you send so the allocation becomes efficient again.
- Discovery solved upfront means the implementation agent does ten times less work per tool call afterward.
- Naming your files and folders well is itself a context-engineering act that shapes model comprehension directly.
- The principles transfer across tools: clearing context and adding a research step apply even in ChatGPT.

### QUOTES
- Dexter: "I haven't opened a nonmarkdown file in an editor in over a month."
- Dexter: "sub aents are not for playing house... They are for exactly one thing, which is context control."
- Dexter: "A bad line of research... can lead you to a thousand bad lines of code."
- Vaibhav: "words are more important than ever before."
- Dexter: "You have to read the [ __ ] that the model spits out."
- Dexter: "The most important thing about code review is not design or correct or finding bugs... it's mental alignment."
- Dexter: "we try to target maximum like 50% context utilization because that's that's generally plenty to do anything."
- Vaibhav: "if you're just like vibing it fully, don't do it... hoping is a really really bad strategy."
- Dexter: "compact... I personally think it sucks um because it's not just the information in the prompt, it's also the trajectory."
- Dexter: "the only way you can take advantage of this technique was actually to stop the thread and start a new thread."

### HABITS
- They review the research and the plan closely, but barely read the implementation code itself afterward.
- Dexter always writes a failing test first before letting the agent write any other real code.
- He always reads the research document rather than blindly making a plan from it himself first.
- They keep a journal of failed research runs and reuse it to steer later attempts better.
- He forces agents to use read, glob, and grep only, never bash, to avoid permission prompts.
- They run two implementation approaches in parallel worktrees and then compare the resulting pull requests afterward.
- Vaibhav asks himself what could be better every single time he uses any AI tool now.
- Dexter puts critical instructions directly in the prompt or plan rather than trusting CLAUDE.md alone here.
- They try changing their process ten percent of the time to keep discovering better prompting habits.

### FACTS
- Claude Code's default context window is 200,000 tokens shared across system, tools, and user messages combined.
- The task tool existed in Claude long before the official sub-agents feature launched weeks ago publicly.
- The BAML bug being fixed had stayed open on GitHub since December, failing tests silently throughout.
- OpenAI's new open-source model uses a Rust runtime and compiles Python bindings on top of it.
- Micro-compaction, which discards tool calls specifically, shipped in Claude Code only the day before recording here.
- Dexter shipped six pull requests in one Thursday using this specification-driven Claude Code workflow of his.
- The reviewed research document for the BAML fix was roughly one hundred twenty lines long total.
- Their research prompt, mostly written by a colleague named Allison, is around three hundred lines long.

### REFERENCES
- Claude Code, Claude Opus 4 and Sonnet 4, and the Claude Code SDK.
- BAML (BoundaryML) and its GitHub repo (around 5,000 stars).
- HumanLayer and its open-source terminal UI for managing many Claude Code instances at once.
- The 12-factor agents methodology (referenced repeatedly).
- Blake Smith's article on code review as mental alignment.
- Jeff (works on the AMP coding CLI), June article: coding with LLMs is like an instrument.
- Swix, who credited Dexter with coining the term "context engineering" in April.
- Linear and its MCP server, plus their custom context-optimized ticket-to-markdown tool.
- Rust and Cargo, Turbo, Go, TypeScript, Python type checking, VS Code extension and LSP.
- The "AI That Works" weekly series, including an earlier episode on 10,000-plus tools and classification.
- settings.json additionalDirectories, ultrathink thinking tokens, symlinks versus hard links for search traversal.

### ONE-SENTENCE TAKEAWAY
Engineer the context window, review the research and plan, and let tests verify the code.

### RECOMMENDATIONS
- Reverse-engineer a Claude request with a proxy to see exactly what fills up your context window.
- Write your current progress into a markdown file with exact file paths and line numbers included.
- Keep every working session under fifty percent context by compacting intentionally instead of using slash-compact blindly.
- Delegate read-only codebase searches to sub-agents so their bulky tool output never bloats your window again.
- Split real work into research, plan, and implementation phases with a review gate between each stage.
- Spend your review time on research and the plan, then trust the well-designed passing tests afterward.
- Make your test commands trivially easy so the model can run them without any friction whatsoever.
- Use one consistent name per concept across the codebase so the model assigns meaning correctly everywhere.
- Put critical instructions directly in your prompt or plan, not only in the CLAUDE.md file itself.
- Open Claude Code inside the integrated VS Code terminal so it receives LSP diagnostic errors automatically.
