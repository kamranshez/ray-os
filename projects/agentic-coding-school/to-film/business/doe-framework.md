# DOE Framework (Directive Orchestration Execution)

## What This Video Covers

A three-layer architecture for structuring AI agent workflows in a business context. Designed for non-developers who think in SOPs and checklists rather than code.

- **Directive layer:** Your workflows and SOPs stored as markdown checklists (what to do)
- **Orchestration layer:** The AI agent that reads directives, makes decisions, handles errors (how to do it)
- **Execution layer:** Scripts, API calls, browser actions that actually do the work (doing it)

This is the conceptual predecessor to Claude Code skills — same idea, more formal structure.

## Why This Matters

Most non-developers struggle with AI agents because they think they need to write code. DOE reframes it: you write CHECKLISTS, the AI follows them. The agent is just an employee who reads and executes your SOP.

This mental model makes AI agents accessible to business owners, marketers, consultants, and operations people. You don't need to know Python — you need to know how to write a good checklist.

Also maps directly to Claude Code skills: a skill.md IS the directive, Claude Code IS the orchestrator, the scripts/ folder IS the execution layer.

## The Three Layers

```
┌─────────────┐
│  DIRECTIVE   │  ← Markdown checklists, SOPs, process docs
│  (What)      │     "Step 1: Scrape leads. Step 2: Classify. Step 3: Email."
├─────────────┤
│ ORCHESTRATE  │  ← AI agent reads directives, makes decisions
│  (How)       │     Claude Code decides which tool to use, handles errors
├─────────────┤
│  EXECUTION   │  ← Scripts, API calls, browser actions
│  (Do)        │     Python scripts, MCP tools, Chrome automation
└─────────────┘
```

## How the Competitor Teaches It

- Introduces the three layers with clear definitions
- Builds a complete sales workflow end-to-end:
  1. Lead scraping directive (markdown checklist)
  2. Classification directive (LLM-based categorization)
  3. Proposal generation directive (auto-generate from template)
  4. Email outreach directive (personalized cold emails)
- Each step has its own directive file, scripts for execution, and Claude orchestrating between them
- Shows CRM integration (ClickUp via MCP) for tracking leads
- Shows Google Sheets output for lead lists
- Demonstrates how the orchestration layer handles errors (retry logic, fallback paths)

## Key Concepts to Cover

- The three layers: Directive, Orchestration, Execution
- Directives as markdown checklists (NOT code — business people can write these)
- How this maps to Claude Code skills:
  - skill.md = directive
  - Claude Code = orchestrator
  - scripts/ folder = execution
- Building a business workflow end-to-end using DOE
- The agent as "employee following the checklist"
- Error handling: what happens when a step fails (the orchestrator decides)
- CRM integration (ClickUp, HubSpot, Notion via MCP)
- Why this framing matters for non-developers
- The spectrum: manual checklist → DOE with AI → fully autonomous

## Demo Plan

1. Show a manual business process (lead scraping done by hand)
2. Write it as a markdown checklist (the directive)
3. Create the execution scripts (or have Claude create them)
4. Let Claude orchestrate: read the checklist, execute each step, handle errors
5. Show the end result: leads in a Google Sheet, classified, ready for outreach
6. Discuss scaling: same pattern for proposals, emails, reporting

## Suggested Class Placement

Business class (core framework — could be the conceptual intro to the entire class)
