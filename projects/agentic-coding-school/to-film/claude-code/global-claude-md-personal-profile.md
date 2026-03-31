# Global CLAUDE.md with Personal Profile

## What This Video Covers

Inserting personal context about yourself — role, revenue, team, goals, communication style, reasoning strategies — into your global CLAUDE.md (~/.claude/CLAUDE.md) so that EVERY conversation across ALL workspaces understands who you are. This prevents Claude from giving generic advice and ensures tailored, relevant recommendations.

## Why This Matters

Without personal context, Claude defaults to generic suggestions. Ask "what's the best solution for X?" and it recommends the cheapest option. But if it knows you make $300K/month and value time over money, it recommends the fastest option instead.

The global CLAUDE.md is injected at the top of EVERY session, in EVERY workspace. It's your persistent identity across all projects. Unlike the local CLAUDE.md (project-specific), this is about YOU.

## What Goes In It

The competitor includes these sections:

**Profile:**
- Age, personality type, location
- Revenue breakdown (which businesses, how much each)
- Team members (editor, LinkedIn person, AI agents)
- Current priorities and constraints

**Goals:**
- YouTube growth targets
- Instagram conversion goals
- Business revenue targets

**Reasoning Strategies:**
- Personal decision-making frameworks
- Communication style preferences
- How they want Claude to present options

**Token Conservation:**
- "Don't over-explain — I can read the diff"
- "Use one write call instead of many sequential edits"
- "Fetch API docs before attempting to use unfamiliar tools"

## How the Competitor Teaches It

- Opens their actual global CLAUDE.md and walks through each section
- Shows a conversation WITHOUT personal context: Claude recommends the cheapest option
- Shows the SAME conversation WITH personal context: Claude recommends the fastest option (because it knows money isn't the bottleneck)
- Explains that high-level reasoning strategies and conventions go in global (applied everywhere)
- Project-specific knowledge goes in local CLAUDE.md (only for that workspace)
- Uses /insights to discover what should be added to global CLAUDE.md
- Emphasizes: manually review before adding to global (compound probability: AI reviewing AI reviewing AI = errors compound)

## Key Concepts to Cover

- What goes in global CLAUDE.md (personal context) vs local (project context)
- Where to find it: ~/.claude/CLAUDE.md (Mac: users/[name]/.claude/)
- How to access the hidden .claude folder (Shift+Cmd+Period on Mac)
- Profile section: role, revenue, goals, constraints, team
- Why this changes Claude's recommendations (the money vs time example)
- Reasoning strategies section: your personal decision-making frameworks
- Token conservation strategies section: rules that apply to ALL projects
- Combining with /insights: use insights to discover global patterns
- The human-in-the-loop requirement for global updates (compound probability argument)
- Keep it concise: bullet points, not essays (every token here is injected in EVERY session)
- Don't duplicate what the model already knows (don't say "use encryption for passwords")

## Demo Plan

1. Show ~/.claude/CLAUDE.md (empty or minimal)
2. Ask Claude something — show generic advice
3. Add personal profile (role, revenue, goals, constraints)
4. Ask the SAME question — show tailored advice
5. Add reasoning strategies and token conservation rules
6. Show the difference in output quality and relevance
7. Discuss what NOT to put in (project-specific stuff, things the model already knows)

## Suggested Class Placement

Claude Code — CLAUDE.md chapter
