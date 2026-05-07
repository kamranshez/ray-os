---
video_id: zNZs19fIDHk
title: "No vibes allowed (AKA live coding with Claude and Code Layer): 🦄 #27"
url: https://www.youtube.com/watch?v=zNZs19fIDHk
channel: BoundaryML
---

### SUMMARY
Vaibhav (BoundaryML/BAML) and Dex (HumanLayer) live-code a timeout feature into BAML using research-plan-implement workflow, Claude Code, and intentional context engineering throughout.

### IDEAS
- Vibe coding works for hard maintainable problems, not just throwaway experimental code most engineers assume.
- Working backwards from documentation forces clarity before implementation begins on any new developer tooling feature.
- Specification correctness matters more than codebase familiarity when steering coding agents toward correct implementations.
- Frequent intentional compaction beats long context windows because models degrade significantly past forty percent utilization thresholds.
- Research phase produces ondemand updated codebase documentation that becomes obsolete after merging implementation patches.
- Reading every diff line is mandatory because skipping review tanks vibe coded projects fastest of all.
- A bad plan equals one hundred bad code lines because misunderstanding propagates through downstream implementation phases.
- Voice prompting injects more context than typing because speakers think less and elaborate more freely naturally.
- Phase design optimizes for incremental compilability so each segment produces verifiable working code before moving forward.
- Sub agents preserve parent context by handling parallel grep search and codebase analysis without polluting state.
- Opus reasons better over complex codebases despite Sonnet writing faster code for simpler isolated tasks.
- Restarting expensive research costs more than paying upfront for a higher quality reasoning model.
- Trajectory steering through interactive back-and-forth makes models check with users instead of running tools blindly.
- Pair programming with coding agents leverages downtime productively while solo work tempts engineers toward Twitter distraction.
- Architecture quality determines vibe coding success because well-designed codebases enable agents to add features predictably.
- Error compaction selectively shows past failures only when relevant tool calls trigger to avoid context pollution.
- Markdown specifications double as machine readable context and human readable documentation simultaneously without translation overhead.
- Test infrastructure quality matters most because models excel at fixing errors but struggle judging correctness.
- Incremental phase splits enable shipping partial features early without waiting for composite cases to complete.
- Codebase pattern finder agents locate existing conventions so new code matches established repository style guidelines.
- Saving research and plans in separate folders keeps them discoverable without polluting the main project repository.
- Rust compilation acts as cheap correctness proxy because passing builds usually indicate working logical implementations.
- Manual edits during agent iteration cycles get overwritten unless prompted explicitly to preserve user changes.
- Personal vibe checkers built through experience outperform formal eval systems for most practical prompting tasks.
- Engineering workflows resist homogenization because every developer uses tools through their own idiosyncratic personal style.
- Best engineers download entire codebases into their brain enabling rapid pinpointing of relevant change locations.
- Approval review gates per phase prevent compounding errors better than running entire implementations end to end.
- Speaking commands aloud feels weird initially but produces better results than typing once habits form.
- Continue command splits between clear and compact letting models generate handoff prompts before context resets.
- Test driven phase boundaries mean each segment has objective passing criteria before next agent picks up.

### INSIGHTS
- Context engineering is the actual skill behind vibe coding, not prompt magic or model selection alone.
- Working backwards from user-facing documentation produces specs that simultaneously serve humans and coding agents perfectly.
- The research-plan-implement loop trades model time for human reading time at roughly hundredfold leverage multiplier.
- Code review of agent output remains non-negotiable because correctness still belongs entirely to the human author.
- Phase granularity should match natural compilation checkpoints because partial working code beats complete broken systems.
- Intentional context compaction outperforms automatic compaction because humans choose what knowledge survives the boundary.
- Architecture investment pays exponential dividends when AI agents build atop predictable abstractions and consistent patterns.
- Vibes-driven tooling decisions often beat formal evals because eval infrastructure exceeds actual problem complexity routinely.
- Agent productivity scales with verification infrastructure because models fix what tests reveal but cannot self-judge.
- Knowing your codebase deeply remains valuable since steering requires recognizing when research output misses critical details.

### QUOTES
- "A bad line of code is a bad line of code. A bad part of a plan is a hundred bad lines of code." — Dex
- "If you don't read the code, you are going to be screwed." — Vaibhav
- "The less context you use, the better results you get." — Dex
- "If you're not using Opus, you're not going to get good results." — Dex
- "It's more expensive for you to have to stop and then start again if you get the wrong result." — Vaibhav
- "If you're not using voice, you're just slowing yourself down." — Vaibhav
- "Vibes are a big part of this. The best engineers I know, they don't use evals." — Dex
- "If it compiles, it probably works." — Vaibhav on Rust
- "Once a plan is approved, letting a model rip and run is so fast." — Vaibhav
- "I spent four hours automating a 10-minute task." — Vaibhav on overinvesting in eval infrastructure
- "Times you just have to learn to be happy with being a 100x faster." — Dex
- "Engineering is such a diverse medium that you usually don't have one thing that fits all." — Vaibhav
- "All dev tools should be built in Rust. I have a strong opinion on that." — Vaibhav
- "I'm still on the hook for the code working regardless of whether I wrote the code or not." — Vaibhav
- "The research basically gives you ondemand up-to-date codebase documentation in 10 minutes or so." — Dex
- "We're building our workflow around what I call frequent intentional compaction." — Dex
- "You'll be told that if AI should be able to do it. There's a top out where it's diminishing returns." — Dex
- "LLMs are bad at judging things, but they are good at reading errors and fixing them." — Dex

### HABITS
- Reads every diff line manually before accepting agent generated code into project repositories.
- Keeps Claude Code context window utilization under forty percent by aggressively starting fresh conversation sessions.
- Uses voice prompting through Super Whisper because typing slows down information density per minute significantly.
- Updates Super Whisper vocabulary with frequent codebase variable names and collaborator names for accurate transcription.
- Saves research and plans in separate Obsidian vault outside main codebase for clean version control.
- Reviews plans in Obsidian reader mode for cleaner reading separated from editor distraction context.
- Commits small logical chunks frequently using a custom split-into-files commit command for clean git history.
- Runs Claude Code directly on machine without sandbox since directory scoping prevents most malicious damage.
- Shims Python command in shell to redirect agents toward UV instead of bare Python execution.
- Switches between Opus for reasoning and Sonnet for fast execution based on task complexity assessment.
- Always opens new context window after spec approval so model receives clean slate without history.
- Uses interactive create-plan command without arguments to set conversational trajectory before describing the actual task.
- Tells coding agent how to run tests explicitly because incorrect test commands waste cycles repeatedly.
- Runs validation tests with UPDATE_EXPECT=1 environment variable to auto-regenerate expected error message snapshots.
- Drops detailed Slack messages with full spec context before starting any new pair programming session.
- Splits phases at natural compilation boundaries so partial work always produces verifiable buildable artifacts.
- Steers sub agents for pinpoint research instead of creating full new research documents for small questions.
- Uses /continue command for human-in-loop compaction generating handoff prompts before context limits hit.

### FACTS
- BAML is a programming language for building LLM applications and AI agents from BoundaryML company.
- HTTP status code 408 represents request timeout according to the standard HTTP specification documentation.
- The original GitHub issue for BAML timeouts was proposed on March 18th of the discussion year.
- Amazon promotes a working backwards methodology where teams write press releases before building actual products.
- BAML codebase contains roughly two hundred thousand lines of Rust plus two hundred thousand TypeScript.
- Cargo holds package-level locks preventing parallel sub-agent test execution within the same Rust workspace package.
- Rust lacks meaningful incremental compilation requiring full rebuilds when source files change in workspaces.
- Claude Code auto-compaction generates summaries of approximately thirty-five hundred words from full conversation history.
- The AI That Works podcast streams every Tuesday featuring shipping workflows that leverage AI productively.
- Anthropic models reportedly degraded when using million token context windows versus shorter context model variants.
- BAML supports retry policies, fallbacks, and round-robin client configurations for routing requests across providers.
- BAML cancellation feature was previously implemented before the timeout feature work began on stream.
- WASM environments cannot enforce timeouts in BAML because of platform-level execution constraints around scheduling.
- Code Layer is a CLI wrapper around Claude Code providing a prettier UI for navigation.
- Sonnet 4.5 was current at recording time being positioned as fast code writer alongside Opus.

### REFERENCES
- BAML programming language by BoundaryML
- HumanLayer (Dex's company)
- Claude Code by Anthropic
- Code Layer CLI wrapper
- Super Whisper voice transcription tool
- Obsidian markdown editor and vault
- Manus AI (referenced for context philosophy)
- Codex CLI by OpenAI
- Cursor AI editor
- Warp terminal
- VS Code editor
- AI That Works podcast
- Amazon's working backwards methodology
- GitHub issue 1630 for BAML timeouts
- Anthropic's recent context degradation post
- Tokyo async runtime for Rust
- yargs and clock CLI tools
- Slack messaging
- Vim keybindings reference

### ONE-SENTENCE TAKEAWAY
Research, plan, implement with intentional compaction beats vibe coding chaos for shipping production-quality complex feature work.

### RECOMMENDATIONS
- Write user-facing documentation first to specify any new developer tooling feature before implementation begins.
- Spawn research sub-agents to map relevant codebase regions before any planning agent attempts to write plans.
- Keep Claude Code context utilization below forty percent by starting fresh sessions between major workflow phases.
- Read every diff line agents produce because skipping review guarantees subtle bugs slip through unnoticed.
- Use Opus for reasoning over complex codebases reserving Sonnet for fast execution of well-specified tasks.
- Switch to voice prompting via Super Whisper because typing constrains how much context you can inject.
- Add frequent collaborator names and codebase variables to Super Whisper vocabulary for accurate voice transcription.
- Split implementation plans at natural compilation boundaries so each phase produces verifiable buildable working artifacts.
- Tell agents explicitly how to run tests because incorrect commands cause repeated wasted iteration cycles.
- Save research documents and plans in separate Obsidian vault outside the main project repository.
- Use create-plan without arguments interactively to set conversational trajectory before describing the implementation task.
- Steer sub-agents for pinpoint research questions instead of regenerating full research documents for small clarifications.
- Ship partial features early by splitting composite client work into separate phases after primitive client implementation.
- Invest in codebase architecture quality because well-designed abstractions multiply coding agent productivity dramatically over time.
- Build a personal vibe checker through repetition rather than over-engineering eval infrastructure for one-off prompting tasks.
- Pair program with another engineer on these workflows to use downtime productively for thinking and reviewing.
- Run UPDATE_EXPECT=1 environment variable when test snapshots change to regenerate expected outputs automatically in cargo.
- Shim dangerous shell commands like bare Python to redirect agents toward safer alternatives like UV.
- Inject error context selectively only when relevant tool calls happen rather than keeping all errors visible.
- Trust the research output approximately rather than perfectly because diminishing returns kick in past good-enough thresholds.
- Use codebase pattern finder agents to discover existing conventions before adding new code in unfamiliar areas.
- Compact context manually using continue command for human-in-loop handoff prompts before automatic compaction triggers.
