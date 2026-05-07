---
video_id: grGSFfyejA0
title: "Agentic Rag: Building a coding agent (no frameworks) 🦄 ep #28"
url: https://www.youtube.com/watch?v=grGSFfyejA0
channel: BoundaryML
---

### SUMMARY
Vaibhav (BAML) and Dexter (CodeLayer) build a from-scratch agentic RAG coding agent in three hours, debating tools, context engineering, and deterministic versus open-ended retrieval.

### IDEAS
- Agentic RAG defines the problem scope rather than prescribing a specific implementation pattern for retrieval.
- A traditional RAG pipeline injects context deterministically while agentic RAG lets models call retrieval tools.
- Most product workflows are too narrow to justify the unbounded cost of agentic retrieval loops.
- Tool implementation quality affects agent accuracy far more than tool definitions or system prompts do.
- Building from scratch teaches first principles better than reaching for an opinionated framework SDK immediately.
- Cursor wrote roughly seventy percent of this coding agent, mostly the user interface scaffolding code.
- Designing the iteration UI was harder than wiring the agent loop or writing tool prompts.
- Without a good debugging UI, identifying where tool implementations fail becomes practically impossible.
- The single terminating tool should be reply-to-user, with all other tools continuing the iteration loop.
- Max iteration limits prevent infinite spending without functionally constraining what reasonable agents can do.
- Scary tools like edit, write, and notebook-edit should be opt-in for read-only documentation agents.
- Returning relative paths instead of absolute paths from grep dramatically improved this agent's accuracy.
- Always pass current working directory into prompts using full paths, not relative paths, for reliability.
- Truncation messages should explicitly tell the model how to fetch the missing content using read.
- Writing oversized tool output to a file and returning the path beats inline truncation every time.
- Sub-agents are conceptually just fresh context windows spawned with a constrained subset of tools.
- Render tool calls as plain narrative text rather than raw JSON to keep context efficient.
- When the model produces malformed tool output, recover gracefully rather than retrying with error feedback.
- Temporary parsing-failure recovery messages should never persist into the canonical agent message history.
- Owning both the model and harness lets you reinforcement-learn the model on your tool format.
- Line numbers in file reads only work cleanly because models are RL-trained to ignore them semantically.
- Cloud Code hashes files on read so writes fail unless the model re-reads stale content first.
- Building a CLI first then upgrading to a TUI was essential for observing tool sequences clearly.
- Evaluating sequence of tool calls beats evaluating parameter values when iterating on agent behavior.
- The action-key discriminator pattern provides type safety over which tools an agent may legally use.
- Use ripgrep over grep because Rust developer tooling is ergonomically and operationally superior.
- BS4 with get_text strips HTML adequately for most fetch use cases without summarization overhead.
- A reference deterministic implementation gives you the AB baseline needed to measure agentic gains.
- Coding agents tolerate slow latency because typing the code yourself is always slower than waiting.
- Doc-search agents must be fast because users will not tolerate multi-minute response times.
- Hide an opt-in escape hatch button to upgrade deterministic queries into full agentic retrieval mode.
- Small models like GPT-5 Nano simply lack the capacity to follow complex multi-tool agent instructions.
- Cache invalidation matters less than getting the right tokens into the model context window.
- Anthropic and Cursor converge on identical tool formats because they observe each other's discoveries.
- Owning the model unlocks training on harness-specific tool patterns competitors cannot replicate cheaply.
- Claude removed the todo-read tool because models self-reinforce through the todo-write tool already.
- Compressing repeated file reads into a single summary keeps the context window small and useful.
- Every subprocess in tool implementations must have a built-in timeout to prevent runaway behavior.
- Limit directory searches and file reads to prevent agents from indexing root or huge files.
- Rendering directory and file labels separately helps thinking models reason about ls output efficiently.

### INSIGHTS
- Tool implementation quality dwarfs tool definition quality when optimizing agent reliability and end-user accuracy.
- Building agentic systems benefits from observability infrastructure long before benefits from clever prompt engineering tricks.
- The hardest engineering problem in agent loops is debugging UI, not orchestration logic itself.
- Context engineering is mostly about saving tokens per call, multiplied across hundreds of model invocations.
- Owning both model and tooling creates a moat through reinforcement learning on harness-specific output formats.
- Deterministic RAG should be the default because users tolerate slowness only when alternatives feel even slower.
- Frameworks save time on simple cases but obscure the system design tradeoffs you actually need.
- Recoverable parsing failures should be handled silently rather than surfaced as visible retries to users.
- File-system-backed truncation patterns generalize: write large outputs, return paths, let the agent decide.
- The reference implementation pattern in software engineering applies cleanly to agent system design and evaluation.
- Sub-agents are powerful precisely because their fresh context excludes the parent's accumulated noise and confusion.
- Type signatures on tool actions provide compile-time guarantees that scary tools cannot be silently invoked.
- Fast feedback loops outperform formal evals when you are still discovering what good behavior looks like.
- Convergent evolution among coding agents means model capacity matters more than harness implementation differences.

### QUOTES
- "If you can think it, you can build it. That's the whole idea." — Vaibhav
- "Most people should not build agentic RAG systems for their workflows." — Vaibhav
- "Almost all of it is pure UI stuff I have to build." — Vaibhav
- "I built the whole thing in three hours using Cloud Code." — Vaibhav
- "I love using scary tools." — Dexter
- "That's context engineering, dude. That's context engineering." — Dexter
- "Every single token counts. When your context gets long, when you save twenty tokens per call." — Dexter
- "I just wanted to learn it from first principles." — Vaibhav
- "Retrieval augmented generation doesn't have to use vectors. It doesn't have to use search." — Dexter
- "If you have accuracy, you actually want to say we're always going to do these three steps." — Dexter
- "The bulk of the time wasn't actually on tool definitions at all." — Vaibhav
- "Use ripgrep. If you're building a grep tool and you don't use ripgrep, incorrect." — Vaibhav
- "Sometimes our linear tool brings back way too much markdown content, so it just saves it." — Dexter
- "I I have a feeling this one's going to go more than an hour, which I'm super down for." — Vaibhav
- "Just write a fuck ton of code and you will probably get better at building this." — Vaibhav
- "Apache 2 license, go steal Vibhav's code and turn it into a company." — Dexter
- "Coding is different because the cost of me typing the code is always long." — Vaibhav
- "Small context gets better results." — Dexter
- "Try stuff, look at what happened, understand it, feel the vibes, look at the data." — Dexter
- "I would highly recommend that every single one of you actually go build something like this." — Vaibhav

### HABITS
- Build CLI tooling first, then upgrade to TUI once log noise overwhelms terminal readability immediately.
- Run the same test query repeatedly during development rather than constructing formal evaluation harnesses upfront.
- Inspect tool-call sequences for correctness instead of inspecting individual tool parameters during agent debugging.
- Copy battle-tested tool definitions from Claude Code rather than redesigning prompts from scratch every session.
- Always include subprocess timeouts when implementing any tool that shells out to external commands.
- Reach for the strongest available model first to eliminate model-capacity issues from the debugging surface.
- Disable directory-changing side effects on bash tools so the agent maintains predictable working-directory state.
- Pass full absolute paths in prompts rather than relative paths to avoid model path-resolution confusion.
- Strip scary tools (write, edit, notebook-edit) from read-only agents to prevent accidental file system writes.
- Render tool outputs as natural text rather than JSON inside the model's context window.
- Limit file reads to twenty thousand characters or five thousand lines, whichever truncates first.
- Hide parsing-failure recovery messages from end users to maintain perceived agent reliability.
- Keep temporary error-correction exchanges out of the canonical agent message history permanently.
- Use type-safe action discriminators to enforce which tools agents are legally allowed to invoke.
- Prefer file-write-then-read patterns over inline truncation when tool outputs exceed context budgets.

### FACTS
- Claude Code recently removed its todo-read tool because the model self-reinforces through todo-write alone.
- Ripgrep is a Rust rewrite of the silver searcher (ag), originally written in Perl with thread parallelism.
- OpenAI models heavily index on the system prompt's first tokens for instruction-following weight allocation.
- Cloud Code hashes files on read so concurrent modifications by humans force re-reads before writes.
- Context7 fetch tools accept a max-tokens parameter so models can request larger summarized payloads.
- BS4's get_text method strips HTML and returns plain text content suitable for model consumption.
- BAML is a programming language designed specifically for building reliable AI pipelines and agents.
- Code Layer is an IDE built around getting coding agents to solve hard codebase problems.
- Exa provides a Python SDK for web search that bypasses the need for MCP servers entirely.
- The Manus team advocates leaving errors in the context window so models avoid repeating mistakes.
- GPT-5 Mini failed to handle the research codebase prompt due to instruction density being too high.
- Cloud Code includes a CD tool letting it update working-directory state across bash invocations natively.

### REFERENCES
- BAML — programming language for AI pipelines (Vaibhav's company)
- Code Layer — IDE for coding agents on complex codebases (Dexter's product)
- Cloud Code (Anthropic) — referenced repeatedly as the gold-standard coding agent harness
- Cursor — IDE used to write 70% of the agent's code during the build
- Claude Agent SDK — explicitly avoided in favor of writing from scratch
- Crew AI — referenced for its prompt about not hallucinating tools
- Ripgrep / silver searcher (ag) — grep tool history and recommendation
- BS4 (BeautifulSoup) — used for HTML stripping in the web fetch tool
- Exa — web search SDK used for the agent's search tool
- GPT-5, GPT-5 Mini, GPT-5 Nano, Sonnet, Opus, Gemini 2.5 Pro — models discussed
- 12-factor agents — referenced for inner-loop versus outer-loop terminology
- Boundary Studio — Bob's evaluation tool for BAML pipelines
- Codex, AMP, Cursor agent — competing coding harnesses mentioned
- OpenRouter — used to swap GPT-OSS-120B into the Cloud Code harness during demo
- Riverside — recording platform used for the live podcast session
- BAML Bammy chat — production deterministic RAG agent compared to the new agentic one

### ONE-SENTENCE TAKEAWAY
Build agentic RAG from scratch to learn, but ship deterministic retrieval whenever your problem scope allows.

### RECOMMENDATIONS
- Build a coding agent from scratch rather than starting with the Claude Agent SDK or frameworks.
- Start with deterministic RAG and only escalate to agentic loops when narrow pipelines hit limits.
- Invest heavily in your TUI and event-rendering harness before optimizing tool prompts or definitions.
- Copy battle-tested tool prompts from Claude Code rather than designing tool definitions from scratch initially.
- Always render relative paths in tool outputs so models reason about file locations more accurately.
- Inject the current working directory at the top of every system prompt for reliable behavior.
- Add timeouts to every subprocess call in your tool implementations to prevent runaway resource consumption.
- Mark write, edit, and notebook tools as scary and exclude them from read-only documentation agents.
- Truncate large outputs by writing them to disk and returning the file path to the model.
- Use action-key discriminators on tool unions to get type-safe enforcement of allowed agent behaviors.
- Run the same test query repeatedly during iteration instead of building formal eval harnesses prematurely.
- Inspect tool-call sequences as your primary debugging signal, not individual tool parameter contents.
- Recover gracefully from malformed model output rather than feeding error messages back into context.
- Keep temporary error-correction exchanges out of the canonical agent message history to prevent contamination.
- Use ripgrep instead of grep when implementing search tools for any new agent today.
- Build a deterministic reference implementation before agentifying so you have a baseline AB comparison ready.
- Provide an opt-in UI escape hatch that upgrades deterministic queries to agentic retrieval on demand.
- Pass full absolute file paths in prompts rather than relative paths to avoid path-resolution failures.
- Limit file reads to twenty thousand characters or five thousand lines, with explicit truncation guidance.
- Render tool outputs as plain narrative text rather than JSON to save tokens across many calls.
