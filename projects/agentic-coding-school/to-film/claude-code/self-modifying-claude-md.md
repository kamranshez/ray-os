# Self-Modifying CLAUDE.md

## What This Video Covers

A meta-instruction pattern where your CLAUDE.md tells the agent: "When the user corrects you or you make a mistake, immediately append a new numbered rule to the learned rules section at the bottom of this file." Over sessions, the rule set grows organically and the error rate drops toward zero — without you having to manually maintain the file.

## Why This Matters

This is the highest-ROI single pattern for anyone using AI agents. Without it, you repeat the same corrections across every session. With it, the agent accumulates a living document of your preferences, mistakes to avoid, and conventions to follow.

- Session 1: many errors, many corrections
- Session 2: fewer errors (previous corrections are now rules)
- Session 3: even fewer
- Session 5: near-zero errors for known patterns

It's platform-agnostic — works in CLAUDE.md, gemini.md, agents.md, or any system prompt file.

## The Meta-Prompt

Add this to the top of your CLAUDE.md (or equivalent):

```
Before we start any task, read this entire file.
This file contains a growing rule set that improves over time.

When the user corrects you or you make a mistake, immediately
append a new rule to the "Learned Rules" section at the bottom.

Rules are numbered sequentially and written as:
[Category] Never/Always do X because Y.
```

## How the Competitor Teaches It

- Shows the gemini.md file with the meta-prompt at top and empty "Learned Rules" section at bottom
- Builds a website — it comes out in dark mode
- Says "quit doing things in dark mode"
- Agent auto-appends rule: `#1 [Style] Never create applications in dark mode. User preference.`
- Opens a NEW session, asks for another website → no dark mode this time
- Shows the declining error rate as a graph over 5 sessions
- Notes that this will eventually need pruning if rules exceed ~1000

## Key Concepts to Cover

- The meta-prompt that enables auto-rule-writing (exact template)
- Rule format: numbered, category tag, imperative instruction, "because" clause
- When rules get added:
  - User explicitly corrects output
  - User rejects a file, approach, or pattern
  - Agent hits a bug caused by wrong assumption
  - User states a preference
- The declining error rate over sessions (draw the graph)
- Platform-agnostic: works in CLAUDE.md, gemini.md, agents.md — same pattern
- Pruning: when the rule list gets too long, ask Claude to consolidate overlapping rules
- Relationship to Claude Code's built-in auto-memory (memory.md) — this is more structured and persistent
- Combining with the global CLAUDE.md for rules that apply across ALL projects

## Demo Plan

1. Create a fresh CLAUDE.md with the meta-prompt
2. Ask Claude to build something
3. Correct it on 2-3 things (styling, naming convention, file structure)
4. Show the rules auto-appending to the file
5. Start a NEW session — show that previous corrections are remembered
6. Ask for something similar — show zero errors on the corrected patterns
7. Show the rule file growing over multiple sessions

## Suggested Class Placement

Claude Code — CLAUDE.md chapter
