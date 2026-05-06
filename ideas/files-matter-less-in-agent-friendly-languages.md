---
tags: [agentic-coding, language-design, code-organization]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Files matter less in agent-friendly languages

## The idea
Agents `cat` files indiscriminately. They don't navigate path semantics the way humans do — they don't think "this is in `auth/middleware/`, so it must be auth middleware." They just read everything. So in an agent-friendly language, file boundaries should mean almost nothing. Namespaces and packages — explicit grouping constructs in the language itself — should dominate. This is closer to Go's model (everything in a package shares scope across files) than to TypeScript's model (each file is its own module with its own imports).

## Why path semantics fail for agents
- Agents read whole files, not directory trees
- Path-based meaning requires the reader to navigate hierarchy mentally
- Agents have weak intuition about "what kind of code lives where" without explicit signals
- Explicit `package` / `namespace` declarations are visible inside the file the agent is reading

## Implications for language design
- Prefer Go-style package scope over TypeScript-style file modules
- Use explicit namespace declarations (BAML uses `NS`-prefixed folders)
- Don't encode meaning in the path that isn't also encoded in the code
- Path should provide *grouping* but minimal *semantics*

## Implications for codebase design (existing languages)
- Don't rely on "the file it's in" to convey meaning to an agent
- Add explicit module/package docstrings that an agent will see when it cats the file
- Repeat critical context inside files rather than relying on directory structure
- Be skeptical of "you can tell what this does by where it lives" arguments

## Surrounding context
Vibhav, while designing BAML's testing feature, was deciding between per-file, per-namespace, and per-package test registration. He landed on per-file chained into per-package, and articulated this principle in the process: "in an agent-friendly world, you actually want files to mean almost nothing. You want minimal impact from the path meaningfulness. You want some grouping level from the path." This is also why BAML namespaces use folder prefixes (`NS_`) — making the grouping signal explicit and visible inside the code, not just implied by the directory.

## Open questions to explore
- Does this generalize to file naming conventions (kebab-case vs. semantic-case)?
- How should existing TypeScript/Python codebases adapt without a full restructure?
- Is there a tooling layer that could "flatten" path semantics into in-file annotations?
- Do agents perform measurably worse on path-semantic codebases vs. flat-package ones?
- What does this mean for monorepo structure when agents are primary readers?
