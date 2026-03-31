---
duration: "5-8 min"
order: 16
class: "skills"
chapter: "Build Your AI Employees"
status: "adapt"
adapts: "skills-vs-subagents"
---

## Skills vs Subagents: When to Use What

The decision framework for when a skill is enough and when you need subagents.

### The Core Distinction

- **Skills** = consistent, repeatable process. Same output quality every time. Best for: SOPs, formatting, reviews, reporting.
- **Subagents** = autonomy, parallelization, scale. Can fix side issues, work in parallel. Best for: large-scale tasks, exploration, multi-file operations.

From the skills-vs-subagents brief: "Beyond 30-40+ skills, it gets really messy. Claude struggles to reliably trigger the right one. The system prompt gets bloated with skill descriptions, and Claude starts picking the wrong skill or ignoring them entirely."

### The Specialist Subagent Pattern

"At that point, you're better off using subagents instead — give each subagent a focused subset of skills rather than loading everything into one agent. Specialized subagents with fewer, scoped tools are more reliable than one agent drowning in options." (skills-vs-subagents brief)

Pattern: subagent with 3-5 scoped skills > one agent with 50 skills.

### Context Forking

When to use `context: fork` to isolate a skill's execution:
- Skill runs multiple commands or reads many files
- You only care about the final result, not the intermediate steps
- You want to preserve main session context for other work

### What to Show

1. Same task done with a skill vs a subagent — show the difference in consistency and autonomy
2. The specialist pattern: subagent with focused skills
3. `/context` before and after a forked skill vs non-forked

### Cross-Links

- [[Forked Contexts for Skills]] (claude-code class) — context isolation
- [[Combining Skills & Subagents]] (claude-code class) — parallel workflows
- [[Skills + Explore Subagents]] (techniques class) — parallel skill application
- [[Allowed Tools for Skills]] (claude-code class) — scoping permissions
