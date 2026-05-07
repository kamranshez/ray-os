---
video_id: fF3GssyaTcc
title: "No Vibes Allowed: 🦄 #33"
url: https://www.youtube.com/watch?v=fF3GssyaTcc
channel: BoundaryML
---

### SUMMARY
Dex (Human Layer founder) and Vaibhav (BAML creator) live-code three features into the Code Layer desktop app, contrasting opinionated context engineering against fast vibe coding workflows.

### IDEAS
- Context switching for humans is expensive, just like context switching is expensive across threads in software systems.
- Light mode beats dark mode when reading specs because eyes need carefully traversing words instead of glossing.
- Markdown files lack the syntax-highlight contrast that makes dark mode great for reading actual program code.
- Research phase prompts should stay strictly objective so models explain how systems work before proposing implementations.
- Mixing implementation suggestions into research causes models to lock onto the first nondeterministic choice they generate.
- Planning works best as iterative back-and-forth conversation, not single-shot generation against a giant research document.
- You cannot outsource thinking to the model; come with strong opinions or accept whatever it picks.
- Force the model to outline phases before writing the plan to preserve attention budget for steering.
- Put your biggest unknowns as phase one so failure happens cheaply with minimal accumulated code.
- Vertical slices wired end-to-end beat horizontal layers because they enable real validation against curl or shell.
- Models are very bad at evaluating whether code is correct; they tell you what you want hearing.
- Boolean flags about email properties beat asking models to score on a one-to-ten scale.
- Use deterministic code for the workflow you already understand and let models write tested correct code.
- Forking a Claude Code session preserves earlier context while letting you redirect after a wrong turn.
- Keeping context window under fifty percent before plan generation matters more than people typically appreciate.
- Reading code in markdown plans gives less leverage than reading it inside a proper editor.
- Prove the unknown bash one-liner works before planning around it; don't let the model assume capabilities.
- Few-shot prompting past titles requires distinguishing AI-generated from user-edited rows or you bias the system wrong.
- Multiplexing four parallel research sessions across models beats perfecting a single prompt for ambiguous explorations.
- Verifiable git diffs of completed features generalize better than plans when scaffolding similar future features.
- Snapshot tests producing per-case diff files let models inspect exactly which assertion broke and self-repair.
- Naming test phases sequentially helps models infer that fixing phase one likely unblocks later phase failures.
- The strangler pattern lets teams migrate Go demons to TypeScript by routing new endpoints through the new stack.
- Background goroutines for AI title generation hide latency from users while still updating UI via SSE events.
- Storing AI titles in a separate database column from user titles preserves manual-edit precedence cleanly.
- Detecting consecutive affirmative responses could let tooling auto-inject yes when models repeatedly ask to proceed.
- Discontinuous innovation tools require workflow changes; continuous tools just speed up your existing habits.
- When new model versions ship, reset expectations and probe the upper boundary of what becomes newly possible.
- Building developer tooling on today's model capability locks in features that become obsolete within months.
- Hot reload that doesn't restart the Go process actively undermines agent-driven UI iteration loops.
- Test harnesses that incrementally accept new cases scale better than vertical end-to-end debugging in complex systems.
- Pick one dimension weekly (tools, models, context level) and evaluate while locking the others constant.

### INSIGHTS
- Context engineering effort should scale with feature complexity; overkill on small features wastes time, underkill yields garbage plans.
- Validate vertically through every layer at each phase rather than horizontally completing layers before any integration test.
- Models default to nondeterministic first choices, so brainstorm explicitly during research to surface alternatives before locking.
- Human attention and model attention are both finite budgets; spend the first half steering, not generating.
- Architectural fallback logic belongs wherever business decisions live, but display logic legitimately belongs on the client.
- Discontinuous innovation requires explicit workflow re-annealing; continuous tools merely accelerate existing patterns developers already trust.
- Building tools forward-projected two years prevents shipping features made obsolete by the next model release.
- Test scaffolding earns compounding returns by making every subsequent regression cheaper to localize and fix.
- Strong opinions about codebase architecture beat asking models open-ended how questions during planning conversations.
- Workflow speed often matters more than workflow optimality; lowest-friction tools win against superior but unfamiliar alternatives.

### QUOTES
- "You cannot outsource the thinking, man." — Dex
- "If you don't come with opinions, the model will not." — Dex
- "If you know what you want, just tell the model what you want." — Dex
- "My opinions are correct opinions." — Vaibhav
- "Light mode has been shown to be significantly better at reading large reading specs." — Vaibhav
- "Context switching is the most expensive thing you do in your software." — Vaibhav
- "Implementation details. And what I like to do during research is just tell it the parts of the codebase that are going to matter without telling it what we're building." — Dex
- "The whole point of the planning prompt is to work back and forth quite a bit." — Dex
- "Models are very bad at evaluating whether code is correct. They just want to tell us what we want to hear." — Dex
- "You want to keep the model objective as long as possible because it's very good at explaining what's there." — Dex
- "Don't obsess too much over getting the plan 100% right." — Dex
- "Put your biggest unknowns as the first phase." — Dex
- "Speed is my actual number one alpha." — Vaibhav
- "If the AI generates a bad title, then you want to differentiate." — Vaibhav
- "I let it do is I let three or four models produce similar outputs." — Vaibhav
- "Get a bunch of reps and figure out which one is right." — Dex
- "TDD: red, green, refactor, iterate." — Vaibhav
- "Make it work and then figure out your test loop and then refactor." — Dex
- "If you do not pick a time to relax and recharge, your body will pick it for you." — Dex
- "Vacation work's really important." — Vaibhav
- "I freaking love code of all kind. It doesn't even matter what it is." — Vaibhav
- "If I ever lock that in into what developers can build today, we will build a feature that is pointless." — Vaibhav
- "Pick a dimension and then eval across that dimension for your own intuition." — Dex
- "When new models come out, I actually just reset all expectations." — Vaibhav

### HABITS
- Open a fresh research session per feature rather than reusing context-loaded sessions for new investigations.
- Keep small one-off bash proof-of-concepts before investing planning time on assumed-working external commands.
- Title every Claude Code session immediately so parallel work streams stay distinguishable across hours.
- Use Haiku for sub-agents because speed matters more than marginal quality on bounded research tasks.
- Run four parallel research processes across different models when exploring ambiguous architectural questions cheaply.
- Stash implementation ideas in a text file during research, surfacing them only during planning phases.
- Always read sub-agent prompts via the focus-and-inspect keybinding to verify what was actually delegated.
- Fork sessions before sending corrections rather than continuing forward through bad context accumulations.
- Prefer light mode in Obsidian when reading long specs; reserve dark mode for syntax-highlighted code.
- Take real vacation time and resist letting fascinating coding problems eat into recharge windows.
- Reset workflow assumptions whenever new model versions ship to discover newly unlocked capabilities quickly.
- Group related research, planning, and implementation sessions under one task rather than under projects.
- Always include integration tests in early phases so wiring failures surface before hundreds of lines accumulate.
- Default to the lowest-friction tool already open rather than context-switching to theoretically better alternatives.
- Skim plans rather than reading line-by-line; trust phase ordering to surface real bugs cheaply.

### FACTS
- Code Layer routes web app traffic through CLLD (Code Layer Demon), which proxies to HLD (Human Layer Demon).
- The Human Layer Demon is currently written in Go but actively migrating to TypeScript via strangler pattern.
- Sub-agents in Claude Code are hardcoded to use Sonnet via the agent header configuration.
- Obsidian's URI scheme requires files to live inside an existing vault; arbitrary file paths fail silently.
- The macOS open command with -a Obsidian and a directory path opens that directory as a vault.
- Claude Code Go is a wrapper library invoking the Claude CLI binary on the system path.
- Claude Code sessions can inherit Claude Max subscription credentials instead of consuming Anthropic API keys.
- BAML development began in mid-2023, making the codebase roughly two years old at recording time.
- Cursor's research agents panel currently cannot spawn sub-agents the way Claude Code's harness does.
- Hot reload in Code Layer's current Go process does not actually restart the demon during file changes.
- The term "context engineering" was coined publicly by Dex but emerged from extensive Vaibhav conversations.
- BAML snapshot tests generate per-case diff files on disk for failed assertions to enable model self-repair.
- SSE (Server-Sent Events) is used sparingly in Code Layer because async title updates are uncommon currently.
- Phased-implement is a new Claude Code command that delegates per-phase work to dedicated sub-agents.
- Tower is the Rust backend of the Code Layer desktop app; the WUI is a Vite frontend application.

### REFERENCES
- BAML (Boundary Markup Language) — language for reliable LLM pipelines
- Code Layer — Human Layer's coding agent desktop app
- Human Layer — company building tooling for coding agents
- Claude Code — Anthropic's CLI coding agent
- Claude Code Go library — Go wrapper around Claude CLI
- Claude Code TypeScript SDK
- Cursor — AI coding editor
- OpenAI Codex — competing CLI agent
- Obsidian — markdown editor used for plans/specs
- VS Code — referenced as a default editor option
- Warp terminal
- Ghosty terminal (by Mitchell Hashimoto)
- Atuin / oxide-style shell history tools
- TanStack DB — replacing Zustand in Code Layer frontend
- SQLite — Code Layer local database
- 12-Factor Agents methodology
- Crossing the Chasm — discontinuous innovation framing
- AI That Works podcast (this show)
- Strangler Fig migration pattern
- Red-Green-Refactor (TDD)
- Open API spec / generated SDK types
- Server-Sent Events (SSE)

### ONE-SENTENCE TAKEAWAY
Strong opinions, vertical slices, and ruthless context budgeting let small teams ship hard agent features fast.

### RECOMMENDATIONS
- Start research prompts strictly objective; forbid implementation suggestions until you reach a separate planning conversation.
- Force phase outlines before plan writing so steering happens before consuming significant context window budget.
- Place your largest unknowns as phase one so wiring failures surface against minimal accumulated code volume.
- Add integration tests inside early phases that exercise external CLIs without mocking the critical interfaces.
- Store AI-generated titles in a separate column from user titles so manual edits always win cleanly.
- Run background goroutines for slow AI calls during session creation so users see no perceptible latency.
- Fork Claude Code sessions when correcting course rather than appending more messages to derailed context.
- Keep plan files under ten percent of context window; iterate phases before writing the markdown out.
- Use Haiku aggressively for sub-agents and research; reserve Opus only for genuinely complex reasoning steps.
- Build snapshot test harnesses that create per-case diff files models can read to localize failures.
- Name test cases sequentially so models infer dependency ordering when multiple assertions fail simultaneously.
- Multiplex three or four parallel research sessions across models when exploring ambiguous architectural questions cheaply.
- Switch into light mode whenever reading specs; reserve dark mode for syntax-highlighted source code reading.
- Reset workflow assumptions whenever a new model version ships and probe its newly expanded capability surface.
- Pick one workflow dimension per week and evaluate variations while locking other variables constant.
- Build developer tooling toward what models will do in two years, not what they do today.
- Validate external commands manually in shell before letting plans depend on assumed-working capabilities like Obsidian URIs.
- Detect repeated affirmative answers and auto-advance models past redundant confirmation prompts during background runs.
- Reuse verified git diffs as feature scaffolds rather than reusing markdown plans whose intent may drift.
- Take real vacation time; coding problems will still be fascinating after you actually recharge properly.
