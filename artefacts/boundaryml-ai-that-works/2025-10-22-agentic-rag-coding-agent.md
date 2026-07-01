---
title: "Agentic RAG: Building a coding agent (no frameworks) #28"
videoId: grGSFfyejA0
url: https://www.youtube.com/watch?v=grGSFfyejA0
channel: AI That Works (BoundaryML)
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Agent quality lives in how you implement tool OUTPUTS, not in tool prompts or definitions.** Vaibhav never touched a tool prompt after writing it once; every accuracy gain came from reshaping what the tools handed back.
VERDICT: 🔗 next-step video available (complements the Context Engineering class).

**2. Never truncate a big tool output. Write it to a file, hand the model the path, and let it read what it wants.** The filesystem becomes the agent's external memory instead of its context window.
VERDICT: 🔗 next-step video available (complements refactoring-to-save-on-context).

**3. Most people should NOT build agentic RAG. Ship a deterministic reference pipeline first, A/B against it, and add an opt-in escape hatch.** Agentic loops are slower and confuse users when they fail.
VERDICT: 🔗 next-step video available (complements the-ambiguity-line).

*Also film-able (not deep-dived):* **Build your own Claude-Code-style coding agent from scratch, no SDK, to actually learn agent design** — slot claude-code > agent-harness-concept / core-agent-loop; 🟡 partial (those briefs plan the loop concept, none teach the "clone Claude Code's tools in 3 hours" build).

---

## Summary

BAML's Vaibhav and HumanLayer's Dexter build a from-scratch coding agent in three hours, cloning Claude Code's tools, to explore when agentic RAG beats deterministic retrieval.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Tool outputs, not tool prompts, decide agent quality

**The claim.** When Vaibhav built a coding agent from scratch, the tool prompts and definitions he wrote once never changed; 100% of the quality improvement came from how each tool's OUTPUT was implemented.

**Why it's non-obvious.** The dominant story since 2024 is "the loop plus good tool definitions is the whole game." Dexter states it explicitly: the promise of agents was "bring your own tools" and the agent does anything. Vaibhav's lived result contradicts that: definitions were the easy, one-shot part; implementation of the returned strings was the crux.

**Why it's true.** The model only ever sees the tool's OUTPUT tokens, so the output IS the context. Grep returning absolute paths wastes ~20 tokens per call; across 30 calls in a long context that noise measurably degrades accuracy. Switch grep to relative paths, tag ls entries as dir/file, and the same model gets sharply better because every token now carries signal. Dexter's verdict: "that's context engineering, dude."

**What it generalizes to.** MCP server design. Any tool returning a blob (a Linear CLI, a database query) is really a context-engineering surface, not an API surface.

**How it goes wrong.** Micro-optimizing tokens on a weak model (GPT-5 nano failed regardless) or before you can observe the agent, so you tune blind.

### Spine 2 — Truncate is a trap: write to a file and hand back the path

**The claim.** Rather than truncating a long tool result, write the full output to a file, return the path, and let the model decide which parts to read.

**Why it's non-obvious.** The reflexive fix for oversized output is to cut it off with a "[truncated]" notice. That silently destroys information the model may need and gives it no way to recover.

**Why it's true.** A coding agent already has read, grep and bash tools. So an over-long web-fetch or search result does not need to live in the context window at all: persist it to disk, tell the model "written to {path}, use the read tool for the rest," and retrieval becomes on-demand and dynamic. The window stays small (small context gets better results), yet nothing is lost, because the model pulls exactly the slice it needs. Even a plain truncation notice should name the exact line range and the parameter to fetch more.

**What it generalizes to.** HumanLayer does this with their Linear CLI: overflowing markdown auto-saves to a file and returns "too long, it's here." Context7's fetch exposes a max-tokens parameter for the same reason.

**How it goes wrong.** An agent with no read/file tool cannot use the pattern, and extra file round-trips add latency.

### Spine 3 — Don't default to agentic RAG; build the deterministic pipeline first

**The claim.** Most software problems are not wide enough to justify an agentic RAG loop; build a deterministic retrieval pipeline first as a reference implementation, A/B the agentic version against it, and gate the agent behind an opt-in.

**Why it's non-obvious.** Agentic RAG is the exciting, general answer, so people reach for it by default. Vaibhav, having just built one, argues the opposite: "most people should not build agentic RAG systems for their workflows."

**Why it's true.** Deterministic RAG injects context via code every time, so it is fast and predictable; agentic RAG lets the model call tools in a loop, so it is unbounded, slow, and confusing when it fails. If you have no fixed baseline you cannot even tell whether the agent is better. Building the reference first gives you the A/B comparison, which Vaibhav finds more useful than a formal eval. Coding agents tolerate slow loops only because typing code by hand is always slower anyway; a docs chatbot does not get that excuse.

**What it generalizes to.** A tight classifier that routes to a slow expensive LLM only on "other" or a user "this is wrong" signal, i.e. the escape-hatch pattern.

**How it goes wrong.** Over-indexing on determinism caps the problem space; some genuinely open-ended questions need the loop.

---

## 🎬 Proposed ACS videos

### 1. Your Agent's IQ Is In Its Tool Outputs, Not Its Prompts

- HOOK: He built a coding agent and never touched a single tool prompt. Every gain came from somewhere else.
- THE PROMISE: For anyone building an agent or MCP server, learn to debug agent quality by reshaping tool outputs instead of endlessly rewriting prompts.
- THE SHAPE: (1) Ship a working agent with clean tool defs and watch it underperform. (2) Same model, swap grep from absolute to relative paths, show accuracy jump. (3) Tag ls output dir/file; add subprocess timeouts and file-count limits. (4) The 20-tokens-times-30-calls compounding argument. (5) Rule: the tool output IS the context.
- SPINE: 1
- SLOT: Context Engineering (class) > tool-response layer (new chapter)
- RELATIONSHIP: 🔗 complements the shipped Context Engineering class. That class teaches shaping the prompt and context window; this adds the layer almost nobody touches, the tool OUTPUT the agent reads back, where Vaibhav found 100% of his quality gains.
- PROOF TO REUSE: "the bulk of the time I spent wasn't on tool definitions at all"; grep relative-vs-absolute path fix; Dexter's "when you save 20 tokens per call and you grep 30 times, that makes a huge difference."

### 2. Stop Truncating: Write Tool Output To A File And Hand Back The Path

- HOOK: The right way to handle a giant tool result is to not put it in the context at all.
- THE PROMISE: For agent and tool builders, a single output pattern that keeps the context small without ever losing information.
- THE SHAPE: (1) The naive "[truncated]" notice and why it silently loses data. (2) Better: name the exact line range plus the read parameter to continue. (3) Best: write the full blob to disk, return the path, let the model read on demand. (4) Generalize to web-fetch, search, and CLI outputs. (5) The filesystem as the model's external memory.
- SPINE: 2
- SLOT: Context Engineering (class) > refactoring-to-save-on-context (adjacent new video)
- RELATIONSHIP: 🔗 complements refactoring-to-save-on-context (context-engineering backlog). That video prunes what is already in the window; this keeps big tool outputs OUT of the window entirely by handing back a file path.
- PROOF TO REUSE: "rather than truncating the output you should just write it to a file, tell the model where it is, and let the model decide which parts to read"; HumanLayer's Linear CLI auto-saving overflow to a file; Context7's max-tokens fetch parameter.

### 3. When NOT To Build An Agent: Deterministic First, Then A/B

- HOOK: The guy who just built an agentic RAG system live tells you most people should not build one.
- THE PROMISE: For anyone tempted to reach for an agent loop, a decision rule for when deterministic retrieval wins and how to prove it.
- THE SHAPE: (1) Deterministic RAG (code injects context) vs agentic RAG (model calls tools in a loop). (2) Why agentic is slower, unbounded, and confusing on failure. (3) Build the deterministic reference implementation first. (4) A/B the agentic version against that baseline instead of a formal eval. (5) The opt-in escape-hatch button that triggers the slow path only when needed.
- SPINE: 3
- SLOT: Techniques (class) > the-ambiguity-line (adjacent new video)
- RELATIONSHIP: 🔗 complements the-ambiguity-line. That video uses the deterministic-to-open-ended axis to ROUTE between existing CLIs; this applies the same axis to designing your OWN retrieval architecture, plus the reference-first + A/B + escape-hatch workflow.
- PROOF TO REUSE: "most people should not build agentic rag systems for their workflows"; the reference-implementation-first + A/B-comparison loop; the "does this look wrong?" button that opts into the agentic pipeline.

---

## 📚 Full wisdom (reference)

**SUMMARY** — BAML's Vaibhav and HumanLayer's Dexter build a from-scratch coding agent in three hours, cloning Claude Code's tools, to explore when agentic RAG beats deterministic retrieval.

**IDEAS**
- Vaibhav built an entire Claude-Code-style coding agent from scratch in three hours using Cursor, no framework.
- He deliberately skipped the Claude Agent SDK to learn every system-design tradeoff from first principles himself.
- Tool definitions and prompts, written once, never changed; all agent-quality gains came from tool-output implementation instead.
- Changing grep to return relative paths instead of absolute paths measurably improved the agent's accuracy dramatically.
- Rather than truncating long tool output, write it to a file and return the file path.
- Truncation notices should state exact line ranges and instruct the model how to read the rest.
- Most people should not build agentic RAG; most software problems are simply not that wide enough.
- Build a deterministic RAG reference implementation first, then A/B-compare the agentic version against that fixed baseline.
- Deterministic RAG injects context via code every time; agentic RAG lets the model call retrieval tools.
- He built a TUI before improving tools because a raw CLI made failures impossible to read.
- The agent emits events; CLI, TUI, and web all render the same underlying event stream cleanly.
- When the model returns plain text instead of a tool call, assume it meant to reply.
- Error-correction retries are injected as temporary states that never enter the permanent conversation history message array.
- Every subprocess and tool call has a guaranteed timeout to stop runaway loops from burning money.
- The agent loop tracks working directory as state so it can emit correct relative paths back.
- Owning both the model and the coding harness lets a lab RL the model's tool format.
- Scary tools like write, edit, and notebook-edit were removed so the reader agent couldn't mutate files.
- The read tool limits output to 20,000 characters or 5,000 lines to avoid overwhelming the context.

**INSIGHTS**
- Agentic RAG is defined by the problem's open-endedness, not by any specific vector-search implementation detail whatsoever.
- Tool prompts are commoditized; the durable engineering work is shaping what tool outputs feed back in.
- Twenty tokens saved per grep, across thirty calls, compounds into a materially better agent outcome overall.
- You cannot improve tools you cannot observe; build the observability UI before tuning the agent itself.
- Building from scratch, not using the SDK, is how you actually understand agent design tradeoffs deeply.
- Coding agents tolerate slow agentic loops because typing the code by hand is always slower anyway.
- The filesystem becomes the model's external memory: hand back paths, let it retrieve on demand itself.
- All coding agents converge on similar tool designs because they share the same underlying frontier models.
- Forgiving parsing beats strict retries: recognize the model's intent instead of rejecting the malformed tool calls.

**QUOTES**
- "If you are deciding whether or not you should build an agentic rag system or not, you should just build one. It's way easier than you think." — Vaibhav
- "most people should not build rag agentic rag systems for their workflows." — Vaibhav
- "that's context engineering, dude. That's context engineering. How do you make it more context efficient?" — Dexter
- "when you save 20 tokens per call and you're going to grep 30 times, that makes a huge difference in your outcome." — Dexter
- "rather than truncating the output for the model you should just write it to a file, tell the model where it is, and then let the model decide which parts of it it wants to read." — Vaibhav
- "the bulk of the time that I spent wasn't actually on tool definitions at all. almost all the time I spent was actually looking at how the tools were implemented." — Vaibhav
- "the inner loop versus the outer loop is what we'll talk about when we talk about 12 factor agents." — Dexter
- "go under the hood, do the janky weird thing, whatever it takes to get the right tokens into the model and every single token counts." — Dexter
- "I really want to learn it from first principles and I just find personally for myself writing the code helps me understand how it works." — Vaibhav
- "just write a ton of code and you will probably get better at building this kind of system." — Vaibhav

**HABITS**
- Vaibhav writes roughly 30% of code by hand and lets AI generate the remaining 70% instead.
- He reruns the same test prompt repeatedly, watching the tool-call sequence rather than building formal evals.
- When learning something new, Vaibhav writes the code himself rather than reaching for an existing abstraction.
- Dexter disables Claude Code's directory-persistence flag so the agent always returns to its original working directory.
- They inject the full absolute working-directory path into the prompt, never relying on relative paths alone.
- Vaibhav caps iterations with a max-loop limit to prevent the agent spinning forever and burning money.
- He always prompts for human-readable custom error messages on every tool the coding agent actually uses.
- They restrict tools from reading the root directory after watching the model attempt exactly that once.

**FACTS**
- Ripgrep is written in Rust and is faster than the Perl-based silver searcher, AG, it replaced.
- Claude Code's edit tool uses old-string new-string replacement rather than raw diffs or full file patches.
- Claude removed its to-do read tool because the model self-reinforces adequately using only to-do write now.
- Claude Code hashes files on read and blocks writes if the file changed since last read.
- Claude Code has a dedicated CD tool so it can track its own working directory state.
- OpenAI models heavily index on trusting system-prompt directory info far more than later message positions do.
- GPT-5 nano failed the agent tasks, lacking the capacity that the full GPT-5 model clearly has.
- The Manus team advocates leaving errors in context so the agent avoids repeating that same mistake.
- The entire coding agent is Apache-2.0 licensed and runnable via uv install plus uv run sync.

**REFERENCES** — BAML (Vaibhav's programming language); code layer (Dexter's ADE); HumanLayer / human-in-the-loop; Cursor; Claude Code; Claude Agent SDK; OpenAI Responses API; GPT-5, GPT-5 mini, GPT-5 nano; Gemini 2.5 Pro and 1.5 Pro; GPT-OSS-120B; OpenRouter; ripgrep (rg); AG / the silver searcher; BeautifulSoup (BS4); Exa web search Python SDK; Context7 fetch tool; crewAI prompt; 12-factor agents; Manus; Boundary Studio / BAML eval tool; Jupyter notebooks; Riverside; Apache 2.0 license.

**ONE-SENTENCE TAKEAWAY** — Agent quality lives in how you implement tool outputs, not in tool prompts or definitions.

**RECOMMENDATIONS**
- Build a small coding agent from scratch yourself to genuinely understand how agent loops actually work.
- Make grep and ls return relative paths and type tags to save the model tokens everywhere.
- Write oversized tool outputs to a file and hand the model the path, not a truncation.
- Build your observability UI before tuning tools so you can actually see agent failure modes clearly.
- Before building agentic RAG, ship a deterministic pipeline and A/B-compare to justify the added complexity first.
- Give every subprocess a hard timeout and cap iterations so runaway loops cannot burn your money.
- Inject the current absolute working directory into a user message, not the cache-busting system prompt itself.
- Handle malformed tool calls by inferring intent, injecting the correction as a discarded temporary state briefly.
- Add an opt-in escape hatch so users can trigger the slow agentic path only when needed.
