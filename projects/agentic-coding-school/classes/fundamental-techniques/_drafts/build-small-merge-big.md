---
class: "fundamental-techniques"
status: "scripted"
aliases: [build-small-merge-big]
---

# Build Small, Merge Big

## What This Video Covers

The technique of prototyping a feature in a clean, isolated project using a coding agent — getting it working and looking right — before porting it into your main codebase. It's the agentic version of the "spike" pattern from agile development, but adapted for how AI coding agents actually work.

## The Problem

When you ask a coding agent to build a new feature inside a large, existing codebase, three things go wrong:

1. **The agent gets confused by existing complexity.** It finds three ways to fetch data, two routing systems, legacy patterns alongside modern ones. It picks the wrong one, or worse, creates a fourth way. The "Reducing Agent Confusion" video covers diagnosing this — but what if you could avoid it entirely for the initial prototype?

2. **You can't see the feature clearly.** The new feature is tangled into existing components, shared state, and existing styles from the first commit. It's hard to evaluate the UX or the logic when you're also looking at everything else in the app.

3. **Iteration is slow and risky.** Every "try this instead" prompt risks the agent touching files it shouldn't. You want rapid, fearless iteration — "scrap this, try a completely different approach" — but in the main project, that's terrifying.

## The Pattern

**Phase 1 — Build small.** Create a new, empty project. Tell the agent: "Build me [feature] as a standalone [app/page/component]. No existing code to worry about. Just make it work." The agent operates in a clean room — no legacy patterns to get confused by, no shared state to accidentally break, no 200-file codebase to scan before writing line one.

This is where you iterate aggressively. Hate the UX? Scrap the whole thing and try again — it's 3 files, not 300. Want to try a completely different approach? Go for it. The blast radius is zero.

**Phase 2 — Merge big.** Once the prototype works and looks the way you want, open a new session in your main project. Point the agent at the prototype: "Here's a working implementation of [feature]. Integrate this into our codebase, following our existing patterns and conventions."

Now the agent's job isn't creative — it's mechanical. It's adapting known-good code to fit your architecture. This is the kind of structured, well-scoped task agents handle brilliantly.

## Why This Works With AI Agents Specifically

This isn't just the old spike pattern repackaged. It's specifically powerful with coding agents because of how they fail:

- **Context window pollution.** In a big project, the agent spends thousands of tokens just understanding the existing codebase before writing a single line. In a clean project, 100% of the context window goes toward the actual feature.
- **Pattern contamination.** Agents mimic what they see. In a codebase with old jQuery alongside modern React, the agent might produce Frankenstein code. In a clean project, it writes idiomatically.
- **Fearless iteration.** "Scrap this and try again" in a 3-file prototype takes 20 seconds. In a production codebase, it takes 5 minutes and you're praying nothing else broke. The speed of iteration directly determines how good the final feature gets.
- **Separate evaluation.** You can look at the prototype on its own, show it to someone, test it in isolation. The UX review is decoupled from the code review.

## When To Use This

- **New UI features** — especially when you're not sure what you want yet. Build a standalone page, iterate until the UX feels right, then port it.
- **Complex logic** — payment flows, multi-step wizards, state machines. Get the logic right in isolation, then wire it into your real data layer.
- **Unfamiliar territory** — trying a library or pattern you haven't used before. Let the agent experiment freely without risking your main project.
- **When the agent keeps getting confused** — if you've tried twice in the main project and the agent keeps touching the wrong files or using the wrong patterns, pull the feature out and build it clean.

## When NOT To Use This

- **Tightly coupled features** — if the feature inherently depends on existing state, auth, data models, etc., a standalone prototype won't teach you much.
- **Small, scoped changes** — fixing a bug, adding a field, tweaking a style. Just do it in the main project.
- **When integration IS the hard part** — if you already know what to build but the challenge is fitting it into the existing architecture, prototyping separately won't help.

## Demo Plan

1. Show the problem: ask Claude Code to build a feature in a real, complex project. Watch it get confused by existing patterns, touch wrong files, produce something mediocre.
2. New terminal, new folder. `mkdir prototype && cd prototype`. Ask for the same feature from scratch. Watch the agent move 5x faster with cleaner output.
3. Iterate aggressively — "I don't like this layout, try cards instead of a table." "Add drag and drop." "Scrap the sidebar, make it a modal." Each iteration takes seconds.
4. Once happy, open a new session in the main project. Use `/add-dir` to point at the prototype folder. "Integrate this working feature into our app, following our existing conventions."
5. Show the result — clean integration, existing patterns followed, feature works exactly like the prototype.

## The Relationship to Other Techniques

- **Designing Components** covers a narrower version of this — extracting a UI component into a standalone HTML file for design iteration. Build Small, Merge Big is the general principle that technique is an instance of.
- **Reducing Agent Confusion** diagnoses why agents fail in complex codebases. This technique is one solution: don't fight the complexity, sidestep it.
- **Worktrees** are about parallel execution on the same codebase. This is about building in a separate, simpler codebase entirely — different problem, different solution.

## Suggested Class Placement

Techniques — Fundamental Techniques
