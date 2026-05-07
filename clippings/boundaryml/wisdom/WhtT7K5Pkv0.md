---
video_id: WhtT7K5Pkv0
title: "Building Animation Pipelines: 🦄 #32"
url: https://www.youtube.com/watch?v=WhtT7K5Pkv0
channel: BoundaryML
---

### SUMMARY
Dexter Horthy and Vaibhav from BoundaryML demonstrate building Excalidraw animation pipelines using Claude Code, custom tools, and AI-assisted workflows for conference talks.

### IDEAS
- Excalidraw animations export to webm by recording browser screen captures using clever headless browser automation hacks.
- Object timestamps in Excalidraw JSON files determine animation render order, enabling programmatic reordering through edit tricks.
- Cutting and pasting elements regenerates their timestamps, providing a janky but effective animation reordering mechanism.
- Wrapping bash scripts in Claude commands buys mental freedom from remembering syntax, even when slower mechanically.
- Claude designs its own CLI syntax when building tools, freeing humans from learning command-line argument structures entirely.
- LLMs excel at converting unstructured human words into structured JSON parameters for downstream tools.
- The valuable shift is realizing token cost is negligible compared to mental overhead of remembering workflows.
- Coding agents pipe outputs between tool calls automatically, eliminating manual file path tracking between commands.
- Recording animations works by literally screen-sharing a browser tab while it draws, then converting to webm.
- About two of three AI-script attempts fail, but successful ones permanently eliminate manual workflow steps.
- Markdown summaries plus jq commands let models manipulate large JSON without reading the entire structure.
- Constraining Excalidraw diagrams to non-recursive simple shapes makes AI manipulation tractable and predictable.
- Putting critical instructions at the very end of prompts increases adherence as the most-recent token.
- Sonnet forgets multi-step instructions around step three; Opus follows long-horizon instructions reliably across context.
- Coding agents have two orthogonal dimensions: prompt and tool harness versus the underlying model.
- Speed of Sonnet often beats Opus quality because faster iteration matters more than first-pass correctness.
- The xkcd "my code is compiling" meme returned as agents work, distracting humans from later review quality.
- Pairing during AI generation maintains engagement; solo coding leads to Twitter checks and worse final review.
- Three levels of plan wrongness: 95% polish in cursor, 85% iterate same session, 60% restart.
- Vibes about model behavior matter more than cross-tool optimization; pick one tool and build deep intuition.
- Building incremental compilers mirrors what rust-analyzer and Astral's UV/Ruff toolchains do internally.
- Custom snapshot diff tools with color-coded syntax compress weeks of manual debugging into instant visual feedback.
- Insta library snapshot testing creates .snap.new files that LLMs use to detect changes between iterations.
- Six-month compiler work compresses to two months when leveraging AI plus internal tooling investment.
- Performance tests in CI/CD guarantee compiler speed regressions cannot ship to production silently.
- Voice dictation hits 200 words per minute easily; typing caps even fast humans around 130.
- The skill cap shifted from typing speed to thinking speed, exhausting brains previously throttled by keyboards.
- AI assistants make code fast but only good when humans bring taste, design judgment, and engagement.
- Maximum parallel coding agents tops out at two for focused work, four only on dedicated weekends.
- Detail-oriented engineers shine at release checklists where less detail-focused people fail predictably.
- Research-plan-implement workflow: have Claude research first, then plan with the user, then build.
- Linear bash automation through Claude beats writing bash directly because adapting workflows on-the-fly stays trivial.

### INSIGHTS
- Token cost is invisible compared to the mental tax of remembering command-line incantations across rare workflows.
- The real productivity unlock from AI is offloading workflow memorization, not raw code generation speed.
- Plans must be directionally perfect, not exhaustively correct, because final-mile fixes are cheap inline.
- Vibes-based tool selection beats minmaxing across coding agents because intuition compounds with single-tool reps.
- Two-person AI coding sessions outperform solo because human engagement during agent downtime determines output quality.
- Pre-existing tool knowledge constrains what AI workflows you can imagine; exposure to libraries unlocks possibilities.
- Constraining input domains (no recursive structures, simple diagrams) makes general AI manipulation tractable in practice.
- Building internal tooling around AI agents compounds; teams expecting AI changes which tools they invest in.
- Long-horizon instruction following separates Opus from Sonnet more meaningfully than coding-specific benchmarks reveal.
- Recovery from a doomed agent trajectory wastes more tokens than restarting with lessons learned.
- Snapshot testing infrastructure provides the feedback loop AI needs to iterate without humans visually checking everything.
- Recognizing wrongness levels (60/85/95 percent) prevents wasted effort on plans needing complete restart.
- The mind-shift from script-writing to slash-command-running represents a developer identity change, not just tool adoption.
- Final tokens in prompts carry more weight; structuring instructions around recency improves adherence dramatically.
- Internal tools built with AI for AI workflows form a flywheel where capability grows compounding weekly.

### QUOTES
- "Start with the end in mind." — Dexter Horthy
- "I don't even know the syntax of this. Like Claude designed the syntax of this and built it for itself." — Dexter Horthy
- "What you're really buying here is you bought time to not have to think about a task." — Vaibhav
- "The valuable thing that LLMs can do is turn human words into JSON unstructured data into structured data." — Dexter Horthy
- "It's abstracting away a way of thinking that you don't have to think about anymore." — Vaibhav
- "Don't outsource the thinking. You need to bring your taste and your craft." — Dexter Horthy
- "Talking is way more engaging and arguing and debating how which library to use." — Dexter Horthy
- "If your plan is 95% of the way there, go fix it in cursor yourself." — Dexter Horthy
- "It's vibes and you just have to put in the reps to get the sense of that." — Dexter Horthy
- "I have never felt skill capped in producing code. My skill cap has been the rate at which I can type." — Vaibhav
- "If something is broken, nothing works, which is a fine way to write the first version of the compiler." — Vaibhav
- "If you're going to build a thing that you want to last a hundred years, you need a good foundation." — Vaibhav
- "Anything you're going to build is going to benefit from a plan." — Dexter Horthy
- "There's no shortcut for any of this stuff along the way." — Vaibhav
- "Get good. I don't know what else to tell you." — Dexter Horthy
- "Half the battle here is honestly just about knowing about the right tools to be able to use." — Vaibhav
- "The minute you recognize that it's doing something wrong, it's like doomed effectively." — Dexter Horthy
- "JSON must be summarized by bash or scripts and JSON must be written by programs, not by models." — Dexter Horthy
- "I'm not what I would say a crazy fast typer." — Vaibhav
- "We just need them directionally perfect." — Vaibhav

### HABITS
- Use start-with-the-end-in-mind diagramming on a whiteboard before architecting any new pipeline workflow.
- Save Excalidraw files to disk and pass paths directly to Claude rather than describing diagrams verbally.
- Run pipelines in bypass-permissions mode for trusted personal automation to avoid constant interruption prompts.
- Add the magic-words instruction to prompts: work back-and-forth, start with open questions, then plan.
- Place most important instructions at the prompt's end since recent tokens carry highest attention weight.
- Use Sonnet for speed-prioritized iteration tasks; reserve Opus for long-horizon multi-step instruction following.
- Pair-program during AI generation phases to maintain engagement and prevent quality degradation from distraction.
- Cap parallel coding agents at two on weekdays; allow four only during distraction-free Saturday sessions.
- Save Whisper-based voice dictation as primary input; switch tools rarely to preserve workflow muscle memory.
- Constrain Excalidraw diagrams to non-recursive simple shapes for predictable AI manipulation downstream.
- Run research-plan-implement as three discrete phases rather than collapsing them into single ambiguous prompts.
- Include unit-test-per-phase instructions explicitly because models default to dumping tests at plan ends.
- Use Obsidian for markdown thoughts and plans rather than custom thoughts-tool CLIs or other systems.
- Snapshot-test infrastructure first; build the testing harness before building the system being tested.
- Write performance tests into CI/CD pipelines to guarantee compiler speed regressions never ship silently.

### FACTS
- Excalidraw stores all element data including timestamps as JSON exportable as .excaladraw files.
- Excalidraw-Animate is an open-source project that animates Excalidraw exports based on element creation timestamps.
- WebM is a web video format functionally similar to MP4 used for animations uploadable to YouTube.
- Insta is a Rust snapshot testing library used by Astral for UV and Ruff toolchains.
- Salsa is a Rust library providing caching infrastructure for compilers and abstract-syntax-tree work.
- Rust-analyzer uses incremental parsing to avoid regenerating autocomplete on every keystroke in VS Code.
- TypeScript's compiler isolates syntax errors so unrelated code keeps working during edits.
- Whisper Flow tracks user words-per-minute leaderboards showing dictation typically reaches 200+ wpm.
- Fast typists max around 120-130 words per minute, well below voice dictation throughput.
- AI Engineer Code Summit in New York hosts MCP debates with Dexter Horthy and Ian arguing.
- Excalidraw exports include Unix timestamps on every element tracking creation and modification times.
- Cutting and pasting Excalidraw elements regenerates their timestamps, enabling reordering through clipboard tricks.
- Reading 200 lines of JSON consumes roughly 3-4% of a typical Claude context window.
- Riverside is the recording platform BoundaryML upgraded to before adding a dedicated video editor.
- BAML is BoundaryML's compiler, currently being rewritten with incremental parsing capabilities.

### REFERENCES
- Excalidraw — open-source diagramming tool
- Excalidraw-Animate — Hacker News project for animating Excalidraw exports
- Claude Code — Anthropic's coding agent
- Codex — OpenAI's coding agent
- Cursor — AI-powered code editor
- 12 Factor Agents — Dexter's framework on LLM workflow design
- jq — command-line JSON processor
- Whisper / Super Whisper / Whisper Flow — voice transcription tools
- Obsidian — markdown knowledge management application
- Salsa — Rust library for incremental computation
- Insta — Rust snapshot testing library
- Rust-analyzer — Rust language server
- UV / Ruff — Astral's Python tooling built in Rust
- AI Engineer Code Summit — New York conference
- MCP (Model Context Protocol) — Anthropic protocol being debated
- Linear — issue tracking platform
- Riverside — podcast recording platform
- BAML — BoundaryML's domain-specific compiler
- Human Layer — Dexter's company and YouTube channel

### ONE-SENTENCE TAKEAWAY
Wrapping deterministic scripts in Claude commands buys freedom from remembering syntax, compounding over time massively.

### RECOMMENDATIONS
- Fork Excalidraw-Animate and build a headless browser version for fully automated webm generation pipelines.
- Use Claude to design CLI syntax for tools you build, then never memorize the arguments yourself.
- Pass file paths to Claude commands instead of copy-pasting content to preserve context window space.
- Constrain your Excalidraw diagrams to flat non-recursive structures for tractable AI-driven manipulation later.
- Place the most critical instruction at the end of every prompt since recency dominates attention weighting.
- Pick one coding agent and build deep vibes-level intuition rather than minmaxing across multiple tools.
- Use Sonnet when speed beats accuracy; switch to Opus only for long multi-step instruction-following workflows.
- Pair on AI coding sessions to maintain engagement during agent downtime instead of drifting to Twitter.
- Cap parallel agent sessions at two during focused work; reserve four-way parallelism for weekend sprints.
- Recognize three wrongness levels: polish in cursor at 95%, iterate at 85%, restart at 60%.
- Throw out doomed agent trajectories immediately rather than burning tokens trying to recover bad starts.
- Build snapshot testing infrastructure before the system itself so AI gets fast iteration feedback loops.
- Add performance tests to CI/CD when building anything speed-sensitive to prevent silent regressions shipping.
- Add the prompt suffix: work back and forth, ask open questions, outline phases before writing plans.
- Use jq to manipulate large JSON files instead of having models read entire structures into context.
- Invite both BoundaryML founders to do a free lunch-and-learn with your engineering team.
- Watch the AI-That-Works episodes recorded every six weeks where they pair-code for three hours.
- Have Claude write summarization scripts for JSON data so it never reads entire files directly.
- Ignore token costs for personal automation; mental overhead saved dwarfs API spending in practice.
- Build internal tooling around your AI workflows; expect AI to write the tools that accelerate AI.
