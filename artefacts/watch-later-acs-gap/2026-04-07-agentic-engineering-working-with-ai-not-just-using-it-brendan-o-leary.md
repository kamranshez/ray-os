---
title: "Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary"
video_url: https://www.youtube.com/watch?v=BEKc4P87XKo
video_id: BEKc4P87XKo
channel: AI Engineer
published: 2026-04-07
status: covered
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary**](https://www.youtube.com/watch?v=BEKc4P87XKo) - AI Engineer - uploaded 2026-04-07

> already covered by ACS: a strong synthesis of fundamentals the school already teaches deeply

Brendan O'Leary (Kilo Code) gives a polished overview talk, but it is a greatest-hits of core agentic-coding fundamentals rather than a source of a new buildable video. Every load-bearing idea gap-checks to COVERED.

- Working with AI, not using it (the confidently-wrong junior-developer mental model): a framing, not a distinct filmable video with its own central demo; the tactics beneath it are what ACS films, and they are covered below.
- Context engineering (persist, select, compress, isolate; the ~50% "dumb zone"; disabling unused MCP servers to save tokens): COVERED by the entire Context Engineering class plus "Long Context Failure" (context poisoning/distraction/clash), "/context", "Context Window Management", "Opus 4.6's Context Window" (the softened 50-60% rule), "Forked Contexts for Skills", and the two "MCP Servers" videos.
- Research, plan, implement with read-only modes and a fresh session per phase: COVERED by "Starting in Plan Mode", "Planning Mode", "Improved Plan Mode", and especially "Continuing Plan in New Context Window" (implement from a clean window on just the plan file, cheaper model for execution).
- agents.md (always-on) vs skills.md (on-demand), and isolate-then-review-as-a-PR with frequent commits: COVERED by the Skills chapters, "The One-Pattern Rule for Agents" (local CLAUDE.md/AGENT.md), "Using Git for Version Control", and "Git Diffs & Mermaid Diagrams".

Only near-gap: the brief beat on feeding an agent your internal platform API docs (OpenAPI spec / convert to markdown / live reference URL / custom MCP). "Scoping APIs" covers prototyping against unfamiliar APIs but not documenting a private internal API for agents. This is a minor, thinly-treated angle, not spine-level, so it does not clear the post gate.
