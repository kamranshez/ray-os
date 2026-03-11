---
duration: "5-9 min"
batch: 1
order: 6
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Setup"
---

# Compound Engineering

Your CLAUDE.md, skills, hooks, and settings aren't just personal config — they're intellectual property. When you commit them to the repo, every improvement one person makes compounds for the entire team. This is compound engineering.

## Prep
- Watch John Kim's video for context on the term: https://www.youtube.com/watch?v=mZzhfPle9QU (tip #4 and #10)
- Dan Shipper coined the term — skim his writing on it

## What to Cover

### 1. The Problem
- Most people treat CLAUDE.md as a personal scratchpad
- Knowledge stays siloed — one person figures out a great prompt pattern, nobody else benefits
- New team members start from zero

### 2. What to Commit (and What Not To)
- **Commit**: project CLAUDE.md, shared skills, hooks, slash commands, `.claude/settings.json`
- **Don't commit**: personal CLAUDE.md (`~/.claude/CLAUDE.md`), absolute paths, machine-specific config
- Show the difference between project-level and user-level config

### 3. The Compound Effect
- Week 1: one person adds a skill for running tests
- Week 3: someone else improves it to also check coverage
- Week 6: another person adds a hook that auto-runs it on commit
- Each layer builds on the last — like compound interest for your engineering workflow

### 4. Demo: From Personal to Shared
- Start with a useful skill or CLAUDE.md rule you've been using locally
- Clean it up: remove personal paths, make it project-generic
- Commit it, show a teammate (or fresh clone) picking it up automatically
- Show how `claude init` bootstraps a new contributor instantly

### 5. Keeping Quality High
- Treat CLAUDE.md like code — review it in PRs
- Remove stale rules that no longer apply
- Keep it focused: if it's longer than ~50 lines, you're probably over-specifying

### Key Insight
> The best teams won't just be writing better code — they'll be writing better instructions for the AI that writes their code. And those instructions will compound.
