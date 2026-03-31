# Workspace Organization (Business / Personal / Client)

## What This Video Covers

A complete system for organizing your Claude Code workspaces at scale. Separates business from personal. Within business, each client gets their own isolated subfolder with its own .env, skills, and CLAUDE.md. Uses an active/ folder as a dump zone instead of polluting root. Color-codes workspaces for instant visual identification. Includes periodic cleanup workflows.

## Why This Matters

Most people either dump everything in one giant folder (chaos) or create a new workspace for every tiny task (fragmentation). Neither scales.

This system lets you:
- Run an entire business from one workspace with organized client subfolders
- Keep personal projects separate but equally organized
- Cross-reference client skills from the business workspace
- Never lose files because everything has a designated location
- Know instantly which workspace you're in via color coding

The competitor runs a $4M+/year business entirely from this structure with no staff — just Claude Code skills organized this way.

## The Structure

```
business/
├── .claude/
│   └── skills/          ← business-wide skills
├── .env                 ← business API keys
├── claude.md            ← business-level instructions
├── active/              ← dump zone for generated files
│   ├── model-chat/      ← debate outputs
│   ├── research/        ← research outputs
│   └── tmp/             ← temporary files (hidden)
├── client-a/
│   ├── .env             ← client A's API keys
│   ├── .claude/skills/  ← client A's specific skills
│   └── claude.md        ← client A's context
├── client-b/
│   └── ...
└── client-c/
    └── ...

personal/
├── .claude/
│   └── skills/          ← personal skills
├── claude.md            ← personal context
├── health/              ← health tracking project
├── citizenship/         ← citizenship paperwork
└── ...
```

## How the Competitor Teaches It

- Walks through their actual Anti-Gravity setup live
- Shows business/ workspace with client A, B, C subfolders
- Demonstrates the active/ folder pattern: all generated files go here, not root
- Shows periodic cleanup: "clean up my active/ folder — anything loose goes into a subfolder or gets deleted"
- Shows personal/ workspace with health, citizenship as separate project folders
- Demonstrates color-coding: different VS Code settings.json per workspace changes header bar color
- Shows cross-workspace skill calling: referencing client skills from business/ CLAUDE.md
- Shows syncing claude.md with agents.md and gemini.md for model diversification

## Key Concepts to Cover

- The business/ workspace structure: .claude, active/, .env, claude.md
- Client subfolders with their own .env, .claude/skills, and claude.md
- The active/ folder as dump zone — NEVER pollute root with generated files
- Skill specs should define WHERE they dump output (e.g. active/model-chat/)
- personal/ workspace for non-business projects (health, hobbies, admin)
- Cross-workspace skill calling: one-liner in CLAUDE.md pointing to client skills
- Periodic cleanup: "clean up my active/ folder" prompt every few days
- Color-coding workspaces via VS Code settings.json (different header bar colors)
- Syncing claude.md with agents.md and gemini.md for fallback/diversification
- Duplicating workspace structure for Codex/Gemini as backup

## Demo Plan

1. Show a messy workspace (files everywhere in root)
2. Set up the business/ structure with client subfolders
3. Create the active/ folder and configure a skill to dump output there
4. Add a client subfolder with its own .env and skills
5. Show cross-workspace skill calling
6. Run a cleanup prompt to organize loose files
7. Set up color-coding for visual identification
8. Show the personal/ workspace alongside

## Suggested Class Placement

Claude Code — new section (could be in Advanced or a standalone chapter)
