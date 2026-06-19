---
class: "multi-agent-orchestration"
status: "idea"
aliases: [designing-codebases-ai-loves]
---

Sits next to [[Context Layer]]. Same goal — make the repo legible to an agent — different surface. The Context Layer is the docs-level surface (CLAUDE.md hierarchies, AGENTS.md, glossaries). Codebase shape is the code-level surface (folders, modules, interfaces). Both feed the agent's context window.

## The frame: your codebase is context

Every file the agent reads is context it has to hold. A shallow module with a fat interface forces the agent to pull in 800 lines to make one change. A deep module with a simple interface lets it pull in 80. Same feature, ten times the headroom.

Ousterhout's "A Philosophy of Software Design" landed before AI agents existed, but it reads like it was written for them:

- **Deep modules** — small interface, large implementation. The cost of using the module is the interface; the value is everything it hides.
- **Shallow modules** — fat interface, thin implementation. Cost ≈ value. These are the modules that bloat agent context for no payoff.

Deep modules are good for humans. Deep modules are *necessary* for agents.

## What this looks like in practice

- **One concept per module.** If the file name has "and" in it, split it.
- **Interfaces that read like sentences.** `archivePost(id)` not `updatePostStatusByIdWithOptions(id, { status: 'archived' })`.
- **Hide the implementation aggressively.** The agent reads the export list first. If everything is exported, you've told it nothing matters more than anything else.
- **Co-locate related code.** Tests next to source, types next to functions, fixtures next to tests. Less navigation = less context.
- **Predictable folder names.** `routes/`, `services/`, `db/` beats `lib/`, `utils/`, `helpers/`. The agent shouldn't have to guess.

## Why this earns its place on Day 5

By Day 5 students understand context windows, subagents, and the Context Layer. Codebase shape is the next layer of the same idea: *physical* legibility on top of *documentation* legibility. Once you see it this way, "refactor for the agent" stops feeling like premature optimisation and starts feeling like the same skill as writing good prompts.

The worked example — [[The Improve My Codebase Skill]] — lives on Day 6 as a skill-building exercise. This stub teaches the principle; that one teaches the tool.

## The PRD link

[[Plans to PRDs]] gets a small update on Day 4: PRDs should name the modules they touch and respect existing module boundaries. A PRD that says "add an archive feature" without naming the module it lives in tells the agent nothing about the seam to cut along. Module-aware PRDs prevent the "AI sprawled the change across six files" failure mode.
