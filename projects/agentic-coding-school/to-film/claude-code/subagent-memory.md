---
duration: "1-4 min"
batch: 1
order: 10
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Subagents"
---

# Subagent Memory

Subagents can now have persistent memory across runs using the `memory` frontmatter key (user, project, or local level). Claude injects a `memory.md` file into the subagent each time it runs, so it can remember what it did last time. Combine with `background: true` for self-improving background agents.
