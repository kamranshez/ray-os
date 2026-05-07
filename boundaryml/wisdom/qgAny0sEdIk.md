---
video_id: qgAny0sEdIk
title: "Applying 12-Factor Principles to Coding Agent SDKs:🦄 #40"
url: https://www.youtube.com/watch?v=qgAny0sEdIk
channel: BoundaryML
---

## SUMMARY

Dex (HumanLayer) and Vaibhav (BAML) discuss applying 12-factor agent principles to coding SDKs, with guest Mike demonstrating structured Ralph Wiggum workflows.

## IDEAS

- Only two levers exist for improving agent systems: fewer steps or more accurate step selection.
- Knowing the workflow order means you probably do not need an agent at all.
- Bash scripts beat agents whenever the execution sequence is already deterministic and well understood.
- Reading and reviewing teammates' agent threads is the highest-leverage coaching tool for engineering leaders.
- Compounding accuracy across 50 steps quickly drops a 99% reliable system below 60% reliability.
- Variance handling and consistency are inverse curves you trade off when designing agent autonomy.
- Looping back to LLM steps on errors lets agents wiggle out of unpredicted failure modes.
- Control flow via prompt accumulates instructions until you reinvent a brittle deterministic script imperfectly.
- Embedded workflows inside single prompts hide nodes that should be made explicit and structured.
- Models can only attend to roughly 150 to 200 instructions before reliability degrades significantly.
- Capitalized warnings like CRITICAL and NEVER consume attention budget without proportional reliability gains.
- Editing a long generated plan is harder than regenerating it because trajectory dominates attention weights.
- Feedback given late in context windows applies inconsistently across earlier sections of the plan.
- Short early back-and-forths steer trajectory more efficiently than corrections deep in context.
- Structured outputs let deterministic harness code orchestrate transitions between agent loops cleanly.
- Background research agents can inject discoveries into ongoing design conversations as ambient context.
- Mission-critical human-in-the-loop workflows benefit from background agents validating assumptions proactively.
- Code reviews exist to artificially slow entropy injection into shared codebases through process checkpoints.
- Coding agent workflows mirror task management diversity: no single style works across teams universally.
- The more you codify a workflow, the less other people want to adopt your codification.
- Subtrees beat submodules because they avoid commit locking while sharing repository content cleanly.
- Build steps must run warning-free because warnings compound context bloat across every agent run.
- SVG architecture diagrams enable diffable dependency review and image-based agent comprehension simultaneously.
- Pre-commit hooks enforcing dependency boundaries prevent vibe-coded abstraction leaks before they spread.
- Plans suck to review because they are too long; structure outlines compact mental alignment artifacts better.
- Design docs survive outside codebases because code evolves faster than design intent ever does.
- Markdown files need a sharable commenting experience that coding agents can also edit deterministically.
- Junior engineers achieve consistency through robust step sequences rather than generic vibe-coded agents.
- The smart-dumb line marks where context window depth degrades model attention and decision quality.
- Classifiers handling common cases with LLM escape hatches give consistency, speed, and rare-case coverage.
- Style guides reduce onboarding questions; coding agent workflows function similarly for new engineers.
- Stateful cloud sandboxes like sprites enable closing laptops while parallel feature agents complete work.
- Frontier model harnesses are now reinforcement-learned, making agentic loops finally usable in production.

## INSIGHTS

- Agent reliability collapses geometrically with step count; reduce steps before improving per-step accuracy.
- Determinism and autonomy form a spectrum where every application must consciously pick its position.
- Composition of small consistent loops within larger loops yields both variance tolerance and reliability.
- Compaction is lossy; deliberate context resets between phases preserve intent better than autocompaction.
- Structured outputs serve as the connective tissue between deterministic harnesses and generative subagents.
- The highest-leverage human moments shift upstream from PR review to design decision checkpoints.
- People prefer building their own platform-as-a-service over adopting somebody else's, including workflows.
- Background validation agents resolve the speed-versus-correctness tension better than synchronous quality gates.
- Visual codebase diagrams compound value because they enable both human review and agent comprehension.
- Forcing intentional compaction between workflow phases prevents trajectory lock-in within long context windows.
- Process checkpoints reduce downstream entropy without requiring AI in the validation loop itself.
- Design artifacts and code artifacts have different lifecycles and should remain orthogonal systems.
- Coaching engineers via reading their agent threads scales mentorship faster than traditional pair programming.
- Markdown collaboration tooling is the missing primitive between agents that edit and humans that comment.
- Workflow codification feels universal to its author but feels constraining to every other practitioner.

## QUOTES

- "The only two things you can do is have fewer steps or have a more accurate step selection system." — Dex
- "If you know the workflow order, you probably do not need an agent." — Dex
- "Models give us a way to loosely have state transitions that are undefined." — Vaibhav
- "Editing with consistency is a much harder task than creating with consistency." — Vaibhav
- "You just want to reduce the number of things the model has to think about." — Dex
- "Frontier thinking can follow about 150 to 200 instructions before losing track." — Dex
- "Not everything is a good task for an agent." — Dex
- "This is basically just software engineering." — Vaibhav
- "Plans suck to review. They are actually too long." — Dex
- "It makes the default thing the correct thing instead of them having to learn." — Dex
- "Designs are designed to checkpoint your codebase at some point in time." — Vaibhav
- "Generic cloud code will produce slop unless you know what you are doing." — Vaibhav
- "The more I codified it, the less other people wanted to do it." — Vaibhav
- "Compaction is lossy and you lose intent." — Mike
- "How do you move the SDLC upstream and automate as much as possible?" — Dex
- "No one has fun building a design doc." — Dex
- "I want checkpoints that are stable and well understood." — Vaibhav
- "Code evolves much faster than design." — Vaibhav
- "Don't use prompts for control flow; use control flow for control flow." — Dex

## HABITS

- Rotate between Claude Code, Cursor, and Anti-Gravity rather than committing to one coding tool.
- Pick the most recently used model in Cursor instead of overthinking model selection daily.
- Read teammates' AMP agent threads as a primary engineering coaching mechanism every week.
- Spawn parallel agent tasks and discard the worse one rather than steering bad runs.
- Restart from zero with deterministic workflow when first vibe-coded attempt produces wrong output.
- Force intentional compaction between research, planning, and implementation phases of coding work.
- Generate SVG dependency diagrams of the codebase and review their diffs in pull requests.
- Enforce pre-commit hooks that block cross-package dependencies between abstraction layers automatically.
- Run all build steps warning-free to prevent context bloat across every agent invocation.
- Export design discussions to file system folders so coding agents can edit them.
- Use cargo over make for dependency management and reproducible build orchestration in Rust projects.
- Invite users into design discussions early before models commit to high-token plan trajectories.
- Spin up ephemeral cloud sandboxes per feature, then shut them down when PRs land.
- Validate every PR comment was addressed via automated AI review before requesting human signoff.
- Manage tasks via simple Notion checkbox lists rather than heavyweight Jira or Linear systems.

## FACTS

- Sonnet 3.5 was a meaningful capability jump over Sonnet 3 for coding agent reliability.
- LangChain published a cognitive architectures graph mapping autonomy against determinism for AI workflows.
- Frontier models around April 2025 could only follow roughly 150 to 200 instructions reliably.
- A 99% accurate step compounded across 20 steps yields roughly 80% end-to-end reliability.
- Ralph Wiggum is a community pattern for running coding agents in deterministic bash loops.
- Sprites by Fly.io launched as stateful cloud sandboxes for parallel coding agent execution.
- Mike manages 25 engineers learning agentic coding at his company using AMP for coaching.
- Mike maintains 20-plus Elixir packages as git subtrees rather than git submodules in monorepos.
- Git subtrees differ from submodules by not locking content to specific commits across repos.
- BAML is a programming language designed to make AI systems more reliable through structured outputs.
- HumanLayer helps companies use coding agents to solve hard problems in complex codebases.
- Claude Code SDK supports built-in structured output schema validation for agent final responses.
- Reinforcement learning on the agent harness was the key 2024 breakthrough for production usability.
- A typical create-plan prompt produced plans averaging 5 to 10 percent of context window.
- Kyle wrote a popular blog post studying how many instructions models can reliably follow.

## REFERENCES

- 12 Factor Agents (Dex's framework and talk)
- BAML programming language by Boundary
- HumanLayer (Dex's company)
- Claude Code SDK (Anthropic)
- AMP coding agent
- Cursor IDE
- Anti-Gravity coding tool
- LangChain cognitive architectures graph
- Kyle's blog post on writing a good plan.md
- Ralph Wiggum looping pattern (October discussion)
- Make, Cargo, Just build tools
- Sprites.dev by Fly.io (stateful cloud sandboxes)
- Mike's open-source GTO project and Wreckit CLI
- Ryan Carson's PRD.json approach
- Ben Swerdlow at Freestyle (burrito SaaS benchmark)
- Notion, Linear, GitHub Issues, Jira (task management)
- AI Engineer World's Fair (June meetup)
- Episode 85 of AI That Works (advanced context engineering)

## ONE-SENTENCE TAKEAWAY

Use control flow for control flow and prompts for variance; codify what you actually know.

## RECOMMENDATIONS

- Audit any agent prompt over 100 instructions and split it into structured workflow phases.
- Replace control-flow-via-prompt with deterministic harness code wrapping smaller agent loops between transitions.
- Define structured output schemas for each workflow phase so deterministic code can orchestrate transitions.
- Force intentional compaction by exiting Claude Code contexts at natural workflow phase boundaries.
- Generate SVG dependency diagrams of your codebase and commit them for diffable agent review.
- Add pre-commit hooks blocking cross-layer dependencies before vibe-coded abstraction leaks accumulate.
- Run every build step warning-free to prevent compounding context bloat across agent runs.
- Spawn parallel agent runs on important tasks and discard the worse trajectory rather than steering.
- Restart from a deterministic workflow when first vibe attempts fail rather than mid-flight correcting.
- Build background validation agents that ping when assumptions diverge from in-flight design decisions.
- Replace plan-review with structure-outline-review since long plans exceed effective human attention budgets.
- Coach engineers by reading their agent threads instead of only reviewing their finished pull requests.
- Use git subtrees for sharing code across monorepos to avoid submodule commit-locking pain.
- Stand up ephemeral cloud sandboxes per feature so parallel agents can run while you sleep.
- Avoid building agents for any workflow whose step order you can already enumerate explicitly.
- Move design docs out of the codebase since their lifecycles diverge from code evolution.
- Provide structured exports of design discussions so coding agents can edit alongside humans collaboratively.
- Default new engineers to opinionated coding agent workflows rather than generic Claude Code freedom.
- Treat plans as ten percent of context budget and front-load decisions before generation begins.
- Combine cheap classifiers for common cases with expensive LLM escape hatches for rare cases.
