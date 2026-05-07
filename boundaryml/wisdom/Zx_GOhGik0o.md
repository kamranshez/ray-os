---
video_id: Zx_GOhGik0o
title: "Agentic Backpressure Deep Dive: 🦄 #44"
url: https://www.youtube.com/watch?v=Zx_GOhGik0o
channel: BoundaryML
---

### SUMMARY
Vibhav (Boundary/BAML) and Dexter (HumanLayer/Riptide) discuss learning tests, agentic backpressure, and deterministic feedback loops that help AI coding agents check their own work.

### IDEAS
- Learning tests probe black-box systems by writing code that demonstrates and asserts assumed behavior empirically.
- Backpressure means giving models deterministic feedback channels so they can detect and fix mistakes autonomously.
- You can accidentally steer a model with prompts but never accidentally steer a deterministic type checker.
- Print debugging beat GDB because printing values is fundamentally a learning test about runtime behavior.
- Hello world programs are humanity's first learning test, demonstrating system behavior through concrete observable example.
- Three identical type-system algorithms across streaming, compiler, and non-streaming reveal architectural design problems requiring redesign.
- Reading external SDK docs is insufficient because subtle behaviors hide in long comprehensive parameter reference pages.
- Curling new APIs before integration is a learning test most developers already do unconsciously today.
- Documenting library contracts as failing-when-broken tests catches breaking changes between dependency version upgrades automatically.
- Database setup precheck tests are a familiar form of learning tests guarding flaky external dependencies.
- Make-the-other-mistake heuristic: overshoot deliberately in both directions to binary-search the optimal range faster.
- Agentic coding requires variable techniques per problem, unlike human typing where consistent technique works fine.
- Most engineers struggle with AI because they pick wrong technique for each problem they encounter.
- Goats of software engineering have intuition for which planning depth fits which specific problem.
- Stressed teams cannot learn AI coding because cognitive load already maxes out finishing assigned work.
- Backpressure mechanisms need not be binary, only observable as tokens the model can consume.
- LLM-as-judge often fails because builder and manager use the same model with same biases.
- Same model asked "is this good" versus "what's wrong" produces dramatically different yet equally confident answers.
- Best AI engineers spend three days designing backpressure harnesses before writing any implementation code whatsoever.
- Twenty thousand lines of working code emerges when backpressure design eliminates human-in-the-loop verification entirely.
- Pre-commit hooks, type checkers, and stop hooks all create deterministic feedback the model can consume.
- Visual dependency matrices reveal architectural violations faster than reading code line by line manually.
- High-leverage files like Cargo.toml deserve manual review since errors cascade into hundreds of downstream issues.
- The hardest part is doing learning tests early enough that wrong assumptions don't poison implementation phases.
- Models testing models with role prompts is mostly cargo-culting; collapse roles into single comprehensive prompt.
- Running two repos in parallel with different strategies explores bug state-space twice as fast.
- User token has stronger bias than system token because of prompt-injection training in frontier models.
- Professionals like doctors and lawyers spend twenty hours weekly on craft beyond their actual job.
- Plans are flexible documents; reviewer agents catching mid-phase deviations help maintain implementation accuracy honestly.
- Codex 5.3 plus Opus planning in parallel multiplies exploration speed across solution-space dimensions simultaneously.
- Performance engineering is essentially perpetual learning tests: write code, inspect assembly, iterate empirically forever.
- Fuzz testing the input range of black-box APIs is penetration testing applied to behavior discovery.

### INSIGHTS
- Determinism is the load-bearing property of backpressure; opinions and probabilities cannot replace verifiable pass-fail signals.
- Learning tests externalize assumptions so wrong models of the world fail loudly before implementation amplifies them.
- The constraint that distinguishes elite engineers is meta-judgment: choosing planning depth proportional to problem complexity.
- Variability of technique is mandatory in agentic coding; consistency was a luxury affordable only to human typists.
- Front-loading backpressure design pays compound interest: every hour invested removes dozens of human review cycles later.
- Models, like humans, ship slop because code itself was designed expecting deterministic feedback loops to catch mistakes.
- Documentation completeness lies; only executable assertions tell you what an external system actually does today.
- Binary-searching skill via deliberate overshooting develops faster instincts than incremental adjustment toward perceived ideal.
- Reviewer-agent patterns work only when same conversational context is preserved, not as detached judging system prompts.
- The interesting questions in software now concern harness design, not implementation; harnesses unlock autonomous code generation.
- High-leverage chokepoints in codebases deserve manual rather than automated review precisely because errors propagate widely.
- Observable-not-binary backpressure means any signal injectable into context counts: stdout, screenshots, types, hooks alike.
- Honing craft requires deliberate hours beyond paid work; agentic coding accelerates this if cognitive bandwidth permits.

### QUOTES
- "You can accidentally steer a model. You cannot accidentally steer a type checker." Vibhav
- "Code humans created this for humans. We wanted back pressure." Dexter
- "Last night at 2:45 a.m." Vibhav, on discovering a wrong baked-in assumption
- "Learning tests, the problem is that this phrase has terrible SEO." Vibhav
- "We're proving the system works in the way that we think it does." Dexter
- "Focus on the highest leverage parts of your pipeline." Dexter
- "External fuzzy libraries." Vibhav, naming the category being tested
- "It's a feedback loop for the AI." Dexter, defining backpressure
- "The back pressure mechanism doesn't have to be binary. It just needs to be observable." Vibhav
- "If you apply everything everywhere you will just be the slowest engineer in the world." Vibhav
- "That's why most people suck at AI coding." Vibhav
- "Make the other mistake." Dexter, on binary-searching skill ranges
- "Anyone that tells you that they're oneshotting everything is lying or producing totally garbage code." Vibhav
- "Doctors and lawyers don't clock off and then go home and watch TV." Dexter
- "Steer the models to the things you want." Vibhav
- "They had designed the back pressure mechanism so they didn't have to be in the loop." Dexter
- "I just had to completely throw that out in terms of our implementation detail." Vibhav

### HABITS
- Use Zed editor for fast markdown viewing and writing because it opens nearly instantly.
- Pull external SDK docs into research folders before any implementation planning starts on features.
- Write learning tests as the third step after reading code and reading external documentation.
- Maintain roughly a hundred documented learning tests covering contracts with uncontrolled external dependencies systematically.
- Run learning tests manually on demand, not in CI, similar to how evals are triggered.
- Generate visual dependency matrices from codebase to spot architectural boundary violations during reviews.
- Open two repository clones simultaneously to explore competing implementation strategies in parallel sessions.
- Kick off Codex 5.3 implementation while running Opus planning session concurrently for the same task.
- Enforce manual code review specifically on Cargo.toml and other high-leverage configuration files.
- Add stop hooks that run type checks deterministically whenever the model believes it has finished.
- Use pre-commit hooks via the pre-commit framework to inject deterministic backpressure into git workflows.
- Document AGENTS.md with exact commands the model should run for type checking each package.
- Spend three days designing backpressure harnesses before writing any implementation for hard problems.
- Read manual verification steps in plans and convert them into automated tests where possible.
- Vibe out small problems first to develop instinct for when planning is unnecessary.

### FACTS
- BAML generates two type systems: a partial type for streaming and a full type for completion.
- BAML's Rust compiler implements nearly identical type algorithms three times across streaming, compiler, non-streaming.
- Claude Agent SDK TypeScript wrapper translates options into flags before invoking the underlying claude CLI binary.
- Claude SDK v1 to v2 changed default session-resume behavior, requiring explicit forkSession=true parameter passing.
- Michael Feathers coined "learning tests" in his book Working Effectively With Legacy Code.
- Cargo Storm is BoundaryML's internal tool that auto-generates dependency matrix diagrams from Rust codebases.
- AI That Works is Boundary and HumanLayer's weekly podcast, with episode 50 marking an SF unconference.
- Jeff Huntley publishes diagrams illustrating spec-driven development loops with continuous backpressure feedback.
- The August 5th episode covered advanced context engineering for coding agents on this same podcast.
- Claude Agent SDK exposes allowed-tools and disallowed-tools options that behave non-obviously despite documentation.
- Node child_process and crypto HMAC libraries have non-obvious edge cases worth documenting via learning tests.
- Premium Codex 5.3 runs slower than Opus but enables productive parallel solving while planning elsewhere.
- Uncle Bob advocates forty-five hours weekly for employer plus twenty hours weekly for craft development.
- The "twenty-five-minute black-box API" interview question tests fuzz-testing and exploratory penetration approaches.

### REFERENCES
- BAML programming language by Boundary
- Riptide tool by HumanLayer (Dexter's company)
- Claude Agent SDK (TypeScript)
- Claude CLI
- OpenAI Responses API
- Codex 5.3
- Opus model for planning
- Zed editor
- Cursor and VS Code editors
- Working Effectively With Legacy Code by Michael Feathers
- Jeff Huntley's spec-driven backpressure diagram
- Pre-commit framework
- Cargo Storm internal dependency-matrix tool
- Ralph Wiggum episode of AI That Works
- August 5th episode: Advanced Context Engineering for Coding Agents
- Uncle Bob (Robert C. Martin) on professional development hours
- Linus Torvalds, git creators, Anders Hejlsberg as software "goats"
- Michael Feathers' learning-tests concept
- Context7 for documentation lookup
- BAML playground for prompt iteration

### ONE-SENTENCE TAKEAWAY
Design deterministic backpressure harnesses first; let learning tests verify assumptions before implementation amplifies wrong models.

### RECOMMENDATIONS
- Write a learning test before integrating any third-party SDK whose source you cannot fully read.
- Convert manual verification steps in implementation plans into automated tests on isolated ports.
- Add stop hooks running type checks so models receive deterministic completion feedback automatically.
- Document external library contracts as on-demand tests that fail visibly when upstream behavior changes.
- Spend three days designing backpressure before writing implementation code for genuinely hard problems.
- Generate dependency matrix visualizations of your codebase to spot architectural boundary violations quickly.
- Restrict imports between sensitive modules using lint rules rather than relying on review vigilance.
- Open two repos in parallel and try competing implementation strategies to explore bug space faster.
- Skip planning entirely on small problems to develop instinct for when planning is unnecessary.
- Overshoot deliberately into too-much and too-little planning to binary-search your optimal range faster.
- Replace LLM-as-judge with deterministic checks like compilers, type systems, and unit test runners.
- Curl new APIs and inspect raw responses before writing wrapping abstractions in your codebase.
- Treat user-token instructions as higher-priority than system-token in modern frontier models for steering.
- Add pre-commit hooks injecting linter and formatter feedback directly into model context windows.
- Manually review high-leverage configuration files like Cargo.toml because errors cascade widely downstream.
- Reserve twenty hours weekly outside paid work for honing your craft and experimenting deliberately.
- Maintain documented learning-test suites of around a hundred tests covering external contract surface areas.
- Use parallel Codex implementation alongside Opus planning to multiply exploration across solution dimensions.
- Build pretty renderers for tools like Claude Code so debugging output stays readable for humans.
- Update the model's context with hook failures rather than expecting it to discover errors itself.
