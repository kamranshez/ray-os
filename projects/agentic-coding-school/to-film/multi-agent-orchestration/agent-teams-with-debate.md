# Agent Teams with Debate

## What This Video Covers

A comprehensive guide to Claude Code's agent teams feature, culminating in the debate pattern where teammates with adversarial personas argue back and forth to produce higher-quality conclusions. Covers: enabling teams, spawning, team lead architecture, teammate communication, the debate pattern with assigned personas, monitoring, token costs, and shutdown.

## Why This Matters

Agent teams are Claude Code's most powerful parallelization feature. Unlike subagents (which report back to a parent), teammates can communicate with EACH OTHER in real-time via a shared scratch pad. This enables debate — where agents with different perspectives challenge each other's assumptions and produce more nuanced, higher-quality conclusions than any single agent could.

The debate pattern is inspired by Generative Adversarial Networks (GANs) — adversarial tension produces better outputs. The competitor found insights from debate that did NOT emerge from independent consensus runs.

However, teams are expensive (7x token multiplier vs standard sessions). Understanding when to use them and when to shut them down is critical.

## Agent Teams vs Subagents

| Feature | Subagents | Agent Teams |
|---|---|---|
| Context | Own window, results return to parent | Own window, fully independent |
| Communication | Report to caller only | Can message each other directly |
| Coordination | Parent manages | Shared task list, self-coordination |
| Cost | Low (isolated calls) | High (7x multiplier, each teammate = full Claude instance) |
| Best for | Focused tasks, one result matters | Complex work requiring discussion and collaboration |

## The Debate Pattern

Spawn teammates with assigned adversarial personas:
- **Systems thinker** — looks at interconnections and second-order effects
- **Pragmatist** — focuses on what's actionable and realistic
- **Contrarian** — challenges every assumption, plays devil's advocate
- **Edge-case finder** — hunts for scenarios where the solution breaks
- **User advocate** — represents the end user's perspective

They share a conversation file and debate in round-robin turns. Each agent sees and responds to ALL other agents' arguments. Over multiple rounds, ideas get sharpened and refined.

## How the Competitor Teaches It

**Enabling:** Add experimental flag in settings.json (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)

**Design iteration demo:**
- Spawns 3 agents to design websites in parallel (Minimalist, Dark, Warm)
- Uses shift+up/down to monitor each agent
- Picks the winner, then spawns 3 more iteration agents with research (design principles, copywriting, competitor sites)
- Each iteration agent produces a new variant → picks best → iterates again

**Debate demo:**
- Spawns 10 scanner agents to audit an open-source codebase for security issues
- 4 documentation agents write up findings
- 2 debate agents: one argues findings are NOT real issues, other argues they ARE real
- Debate produces higher-confidence final assessment
- Shows $80+ token cost for this run

**Monitoring:** shift+up/down to navigate between agents, see each agent's token usage and idle time

**Shutdown:** Explicitly shut down teams to stop burning tokens. Shutdown isn't instant — agents finish current queries first.

## Key Concepts to Cover

- Enabling agent teams (experimental flag in settings.json)
- Team lead vs teammates architecture
- Spawning teams with specific instructions per member
- The shared scratch pad (how teammates communicate)
- The debate pattern: assigned personas, round-robin turns, adversarial tension
- Monitoring with shift+up/down (in-process mode)
- Split pane mode vs in-process mode
- Token cost reality check (7x multiplier, $80+ for big tasks)
- Shutting down teams to stop burning tokens (not instant)
- When teams beat subagents (complex work requiring discussion)
- When to avoid teams (simple parallelizable tasks — use subagents instead)
- The GAN analogy (adversarial tension → better outputs)

## Demo Plan

1. Enable agent teams in settings.json
2. Spawn 3 design agents for a website — show parallel creation
3. Monitor with shift+up/down, show token usage per agent
4. Pick winner, spawn iteration team with research agents
5. Spawn debate team: assign adversarial personas to discuss a strategy question
6. Show the conversation transcript — highlight insights that only emerged through debate
7. Show final token cost
8. Demonstrate shutdown

## Suggested Class Placement

Claude Code — Agent Teams (new chapter, expanding the existing "Subagent Teams" section)
