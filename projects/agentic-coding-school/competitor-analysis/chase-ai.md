---
source: "567 Hours of Claude Code Lessons in 20 Minutes"
channel: Chase AI
video_id: rVEoyx349Hk
date: 2026-03-01
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Agent Teams — experimental feature with coordinating team leader** — Chase describes agent teams as distinct from regular subagents: "in agent teams, they talk to one another. So the guy that's doing the UI and the guy that's doing the blog and the guy that's doing authentication, they all speak to one another and they even have a team leader coordinating all their actions." He shows how to enable it via documentation prompt and use it with explicit invocation: "use agent teams to do A, B, C, and D." Ray covers subagents extensively but agent teams as a coordinated, communicating system with a team leader is a distinct feature not covered.

- **[MEDIUM] Claude Code frameworks (GSD, BMAD) as "mods"** — Chase introduces the concept of third-party frameworks layered on top of Claude Code: "think of them as like mods for cloud code. It's still cloud code doing everything, but if I use something like GSD on top of cloud code, it sort of just changes the logic for how it approaches certain problems." He specifically mentions GSD's context window management and subagent approach. Ray doesn't cover third-party frameworks/methodologies.

- **[MEDIUM] Worktrees for parallel feature development** — Chase explains worktrees as an alternative to branches for parallel agent work: "work trees allows us to do the same thing [as agent teams], but they work in different git branches" using `claude --worktree feature-dark-mode`. He contrasts this with regular branches and explains how to merge afterward. Ray doesn't appear to cover worktrees.

- **[MEDIUM] Context rot / degradation at ~50-60% context usage** — Chase explains the concept of context rot with specific numbers: "when we hit about 100,000, so the halfway mark... the effectiveness of our AI system drops drastically, right? It begins to nose dive." He uses this to argue for proactive context management. While Ray covers compacting and clearing, the specific "context rot" framing with the danger zone threshold is a useful mental model.

- **[LOW] "Yes, clear context and bypass permissions" as the standard plan execution command** — Chase shows that after plan mode produces a plan, the recommended execution command is "yes, clear context and bypass permissions" to start fresh. This specific workflow step connects plan mode to context management.

- **[LOW] Asking "What am I not thinking about?" as a debugging/planning prompt** — Chase recommends proactive prompts: "What am I not thinking about? Is this the best way forward? What would someone who is an expert in whatever you're trying to build, what would they be doing in this scenario?" While Ray covers clarifying questions, this specific set of meta-prompts is a useful addition.

- **[LOW] Web search for latest best practices during UI design** — Chase demonstrates: "use your web search to look up best practices for UI design in 2026" as a way to overcome knowledge cutoff. Ray covers web search via MCP but this specific pattern of combining web research with implementation prompts is worth noting.
