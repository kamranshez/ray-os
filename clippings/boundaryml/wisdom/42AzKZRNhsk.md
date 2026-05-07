---
video_id: 42AzKZRNhsk
title: "Advanced context engineering for coding agents: 🦄#17"
url: https://www.youtube.com/watch?v=42AzKZRNhsk
channel: BoundaryML
---

## SUMMARY

Vaibhav (BAML) and Dexter discuss advanced context engineering for coding agents, focusing on Claude Code workflows, sub-agents, intentional compaction, and spec-first development practices.

## IDEAS

- Rust for core systems plus Python bindings represents the optimal approach for builder-focused tools today.
- Claude Code success depends entirely on understanding what fills the 200k token context window every turn.
- Bad research lines lead to thousand bad code lines through cascading downstream amplification effects.
- Sub-agents exist solely for context control, not for anthropomorphizing roles or playing organizational house.
- Reading what models output matters more than reading the actual generated code afterward.
- Intentional manual compaction beats slash compact because trajectory matters as much as captured information.
- Target maximum 50% context utilization for reliable coding agent performance across complex multi-step tasks.
- Distinguished engineers sign off on designs, not implementations, mirroring how AI workflows should function.
- Naming consistency across codebases matters more than ever because models cannot disambiguate inconsistent terminology.
- Code review's primary purpose is mental alignment among teammates, not finding bugs or correctness issues.
- Tests should be written first because TDD is the only reliable AI-generated code methodology.
- Reading research before passing plans to colleagues is non-negotiable workflow hygiene for AI development.
- Three-phase workflow research, planning, implementation creates checkpoints that prevent uncontrolled scope creep dramatically.
- Compressed markdown files representing prior context outperform raw conversation history for cross-thread continuation.
- Tools requiring permission like bash interrupt agent flow, so steer toward read/glob/grep instead.
- Builder framework choices like page.tsx everywhere structurally prevent agents from navigating codebases efficiently.
- Smaller repos and monorepos massively reduce friction for coding agents working across boundaries.
- Symlinks confuse Claude search tools because gitignored paths skip traversal during recursive operations.
- Hooks and plan-embedded shell commands beat CLAUDE.md instructions because relevance disclaimers dilute system messages.
- Practice with motorcycles in parking lots beats running marathons faster on foot indefinitely.
- Spec process produces 200-line plans easier to review than chronologically-jumbled GitHub PR diffs.
- Custom MCP wrappers compress noisy JSON responses into context-efficient markdown for repeated tool usage.
- Question placement second in prompts empirically yields better results than question first for Dexter.
- Auto-accept implementation works when plans are written by experts knowing the codebase intimately.
- Six PRs shipped Thursday without opening non-markdown files in editor for over a month.
- Failing tests written before implementation give models verification harnesses for hands-off iteration toward correctness.
- Architecture-impacting changes require pulling down branches and using daily before merge approval.
- Disk fragmentation analogy explains why occasional defragging context yields dramatically better space allocation.
- Allison's 300-line research markdown command coordinates parallel sub-agents researching different codebase parts.
- Linear board states track research progress separately from planning and implementation lifecycle stages.

## INSIGHTS

- Context engineering is leverage hierarchy where prompt quality affects research, plans, then thousands of code lines.
- Model performance depends on context window density, not capability, so compression is the real optimization frontier.
- Sub-agents purely manage context windows, not personality, despite recent industry framing toward agent personas.
- Specification reviews replace code reviews because human attention should target highest-leverage decision points only.
- Tribal knowledge encoded as consistent vocabulary becomes machine-readable infrastructure that AI agents navigate predictably.
- Test-driven development becomes mandatory rather than optional once humans stop reading generated implementation code.
- Onboarding documentation and context engineering converge: both teach fresh entities how to navigate systems efficiently.
- Reps and intuition matter more than tool selection because principles transfer across coding agent platforms.
- Builder tools should expose internals because abstraction prevents users from maximizing system performance through engineering.
- Process discovery never ends because learning how to learn is the perpetual software engineering meta-skill.

## QUOTES

- "Anyone that isn't writing Rust code for core systems is doing it wrong." — Vaibhav
- "Sub agents are not for playing house. They are for exactly one thing, which is context control." — Dexter
- "I haven't opened a non-markdown file in an editor in over a month." — Dexter
- "Words are more important than ever before." — Vaibhav
- "Hoping is a really really bad strategy." — Vaibhav
- "Do not make a plan and send it to your co-workers if you didn't read it yet." — Dexter
- "A bad line of research can lead you to a thousand bad lines of code." — Dexter
- "TDD is the only way to write AI generated code." — Dexter
- "If you have your code across seven different repos and you're not using a monorepo, you will have a hard time." — Vaibhav
- "The most important thing about code review is mental alignment." — Dexter
- "You should be doing your compaction manually." — Dexter
- "Don't forget to read everything the model outputs because the research is super high leverage." — Dexter
- "Manage your context window because the smaller you can keep it, the better performance you will get." — Dexter
- "Models can't do the right thing if you have seven different ways to refer to it." — Vaibhav
- "Use the right tools." — Vaibhav
- "Some people are about to get passed by people riding motorcycles." — Dexter (paraphrasing Jeff)
- "If you tell Claude to think deeply you get the thinking tokens. This can backfire." — Dexter

## HABITS

- Use slash clear instead of slash compact for fresh context window with same instructions.
- Read every research output before handing implementation plans to teammates or coding agents.
- Open Claude Code inside VS Code integrated terminal to gain LSP error access automatically.
- Turn on Python type checking in VS Code because it remains disabled by factory default.
- Run Cargo test, Cargo check, and linters automatically because Rust's TDD culture demands it.
- Try Claude Code for ten minutes; revert to old methods if no happy path emerges.
- Spend more review time on research and plans than reviewing the actual generated implementation code.
- Always include "use a sub agent and prompt it like this" inside user messages explicitly.
- Write failing tests as first phase of implementation plans before fixing underlying code issues.
- Add architecture-impacting tools to teammates' machines for daily use before merging fundamental changes.
- Maintain Linear board states for research, planning, and implementation lifecycle separately for visibility.
- Steer agents toward read, glob, grep, and never bash to avoid permission prompt interruptions.
- Pull down branches and use new versions personally before approving foundational infrastructure modifications.
- Keep markdown plan files using path-and-line-number references rather than embedded code searches.
- Sample alternative prompt orderings frequently to discover empirical wins like question-second placement.

## FACTS

- Claude Code's context window holds approximately 200,000 tokens including system, tools, MCP, and user messages.
- The task tool existed in Claude long before sub-agents launched as a marketed feature recently.
- OpenAI's new OSS model uses Rust runtime with Python bindings compiled on top of it.
- BAML hit 5,000 GitHub stars recently as a community milestone for the team.
- Claude appends a relevance disclaimer after CLAUDE.md content telling models to ignore irrelevant context.
- BAML had a bug open since December where double-at assertions silently failed without warnings.
- Claude Code Grep tool is fast pattern search based on ripgrep underneath the hood.
- Sonnet lacks attention quality required for prompts that work effectively with Opus models.
- Ultrathink mode pays attention to higher conversation entries but sometimes overrides newer user instructions.
- Human Layer is building open-source terminal UI for managing many concurrent Claude Code instances.
- Linear MCP responses contain noisy JSON that wastes context tokens on every tool invocation.
- Aaron auto-merged the BAML PR without knowing he was being recorded as a demonstration.
- Dexter coined the term "context engineering" back in April according to Swix's attribution.

## REFERENCES

- BAML codebase and BoundaryML company
- Claude Code by Anthropic, including Opus 4 and Sonnet 4 models
- Twelve Factor Agents methodology referenced repeatedly throughout the show
- Human Layer GitHub repository with open-source coding workflow commands
- Allison, contributor to research prompt commands
- Blake Smith's article on code review fundamentals
- Jeff at Sourcegraph AMP, article on coding LLMs being instruments
- Linear MCP server for issue tracking integration
- Jeff's marathon-versus-motorcycle metaphor for AI adoption urgency
- Cursor IDE, Vim, VS Code as alternative editors
- Turbo build system for TypeScript monorepos
- Next.js framework page.tsx file naming pattern critique
- GPT OSS model with Rust runtime and Python bindings
- Sonnet 3.7 era Twitter Spaces vibe-checking session
- Swix for context engineering term attribution

## ONE-SENTENCE TAKEAWAY

Manage your context window aggressively through specs, sub-agents, and intentional compaction to maximize coding agent performance.

## RECOMMENDATIONS

- Adopt three-phase workflow: research, planning, implementation, with human review checkpoints between each distinct stage.
- Write 300-line markdown commands that orchestrate parallel sub-agents researching different codebase areas independently together.
- Target fifty percent maximum context utilization to preserve attention quality across long coding sessions.
- Replace slash compact with manual markdown progress files including exact paths and line numbers referenced.
- Standardize codebase vocabulary so attributes, blocks, and entities have one canonical name everywhere consistently.
- Open Claude Code inside VS Code's integrated terminal and install the extension for LSP errors.
- Turn on Python type checking and select correct interpreter so models receive proper type information.
- Build custom MCP wrappers that compress responses into markdown instead of consuming JSON token budgets.
- Practice Claude Code on personal projects when work environments restrict access to advanced AI tooling.
- Use git worktrees and parallel directories to run multiple implementation plans simultaneously for comparison studies.
- Write failing tests first then fix code, giving agents verification harnesses for autonomous iteration cycles.
- Steer sub-agents to read, glob, and grep only, avoiding bash to prevent permission prompts.
- Add additionalDirectories to settings.json so Claude works across related repos without per-session permission grants.
- Pull architectural changes locally and use them daily before merging fundamental infrastructure or tooling decisions.
- Read every research document and reject plans where files, tests, or vocabulary appear incorrect.
- Convert symlinks to hard links so Claude search tools traverse directories that gitignore would otherwise skip.
- Restructure folders so files starting with letters before "p" appear ahead of repeated page.tsx entries.
- Spend ten minutes trying Claude Code; if no happy path emerges, revert and try again later.
- Sample alternative prompt structures regularly, swapping question and context positions to discover empirical performance wins.
- Run sub-agents in parallel by explicitly instructing the parent agent to launch them concurrently together.
