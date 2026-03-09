---
source: "Every Claude Code Concept Explained for Normal People"
channel: Simon Scrapes
video_id: ZlDnsf_DOzg
date: 2026-02-28
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Agent Teams as a distinct concept from sub-agents** — Simon explains "agent teams" as a newer Claude Code feature where teammates can communicate directly with each other and share a task list, contrasting it with the hub-and-spoke sub-agent model where everything flows through the main agent. Quote: "Instead of that hub and spoke model where everything goes through one central point, teammates can actually communicate directly with each other and they share a task list." Ray covers subagents extensively but doesn't seem to cover this agent teams / teammate concept as a separate paradigm.

- **[MEDIUM] Deny list in settings.json to block Claude from accessing sensitive files** — Simon explains how to add deny rules to settings.json so Claude cannot read env files, secrets folders, or credentials — even if you ask it to directly. Quote: "Claude won't even discover these files. It won't include them in search results and can't read them even if you ask them to directly." Ray covers permissions but may not specifically cover the deny list / file blocking approach.

- **[MEDIUM] Worktrees for parallel isolated development** — Simon explains the `-w` / `--worktree` flag to create isolated working directories with their own branches, plus sub-agents working in separate worktrees that auto-cleanup when done. Quote: "Three claudes working on completely different tasks in completely separate copies of my code." Ray doesn't appear to have a video specifically on worktrees in the course outline.

- **[MEDIUM] Context rot concept explained with token thresholds** — Simon explains context rot as a named phenomenon with a specific mental model: "As we increase the number of input tokens, our reliability on the output gets less, to the point where if we're actually putting in 10,000 tokens or around 7,500 words, we lose 50% of the context." While Ray covers context-related topics, explicitly naming and quantifying "context rot" as a concept for non-technical users could be a gap.

- **[LOW] CLI mode (formerly headless mode) explained for non-technical users** — Simon explains the `-p` flag for non-interactive execution in very accessible terms, positioning it as a stepping stone to Ralph loops. Ray covers headless mode but Simon's framing for non-coders is different.

- **[LOW] Cost comparison: Claude Max subscription vs API pay-as-you-go** — Simon breaks down the Pro ($20), Max ($100/$200) pricing tiers vs API token-based pricing, recommending fixed subscriptions for active builders. Ray likely covers this but Simon's decision framework is worth noting.

- **[LOW] Launch flags overview as "session settings"** — Simon covers `--model`, `--allowed-tools`, `--verbose`, and `--dangerously-skip-permissions` as launch-time configuration flags. Ray covers these individually but not as a unified "flags" concept.
