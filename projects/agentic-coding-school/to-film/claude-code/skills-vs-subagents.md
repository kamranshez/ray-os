---
duration: "5-9 min"
batch: 4
order: 4
batch_name: "Skills"
class: "claude-code"
chapter: "Skills"
---

# Skills vs Subagents

How they differ now

parallelisation

## Skills don't scale — subagents do

Beyond a certain number of skills (30-40+), it gets really messy. Claude struggles to reliably trigger the right one. The system prompt gets bloated with skill descriptions and trigger conditions, and Claude starts picking the wrong skill or ignoring them entirely. At that point, you're better off using subagents instead — give each subagent a focused subset of skills rather than loading everything into one agent. Specialized subagents with fewer, scoped tools are more reliable than one agent drowning in options.

[Claude](https://claude.ai/chat/8eeb9afe-eb3d-4254-be37-6c3ef3845458)
