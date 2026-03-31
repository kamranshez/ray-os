# Multi-Agent Chrome (Parallel Browser Automation)

## What This Video Covers

Spawning multiple Claude Code agents, each with their own Chrome DevTools MCP instance, to perform the same browser action across many targets simultaneously. Instead of one agent slowly filling out one form at a time, 10 agents fill out 10 forms at the same time.

## Why This Matters

Single-agent browser automation is SLOW — 2-3 minutes per target (launch browser, navigate, screenshot, identify form, fill fields, submit). For 1,000 targets, that's 30+ hours.

With 10 parallel agents: 1,000 targets in ~3 hours. With 50 parallel agents: 1,000 targets in ~40 minutes.

This is the pattern for: automated lead outreach (filling contact forms), scraping JS-heavy sites that don't have APIs, data collection at scale, apartment/rental searching, and any browser task that needs to hit many different websites.

## Architecture

```
User
  ↓
Orchestrator Agent (Opus)
  ↓ spawns
┌──────────┬──────────┬──────────┐
│ Chrome   │ Chrome   │ Chrome   │ ... (N agents)
│ Agent 1  │ Agent 2  │ Agent 3  │
│ + MCP 1  │ + MCP 2  │ + MCP 3  │
└────┬─────┴────┬─────┴────┬─────┘
     ↓          ↓          ↓
  centralized chat.json
     ↓
Orchestrator checks chat every 30s
```

Each agent has:
- Its own Chrome DevTools MCP instance
- Its own CLAUDE.md context
- Access to the centralized chat file for reporting status/issues

The orchestrator:
- Determines how many agents needed
- Launches all Chrome instances
- Resets the chat file
- Monitors progress via the chat file
- Collects results

## How the Competitor Teaches It

- Builds a skill called "multi-agent-chrome"
- Each sub-agent has its own MCP server, its own instructions
- All communicate through a centralized chat file
- Orchestrator checks the chat every 30 seconds for status updates
- **Demo 1:** Contact form outreach — agents navigate to different business websites, find contact forms, fill in personalized messages, submit
- **Demo 2:** Apartment hunting — 4 parallel Chrome agents scraping Craigslist, Kijiji, PadMapper, and liv.rent simultaneously with location/budget filters
- Notes anti-detection considerations (browser fingerprinting, rate limiting)

## Key Concepts to Cover

- Why single-agent browser automation is slow (2-3 min per target)
- The math: 10 agents = 10x throughput, 50 agents = 50x throughput
- The architecture: orchestrator + N Chrome agents + centralized chat
- Each agent gets its own Chrome DevTools MCP instance
- The centralized chat.json as coordination mechanism
- Prompt contracts before launching (define constraints, targets, output format)
- Real demo: lead outreach via contact forms across multiple websites
- OR real demo: apartment/rental searching across multiple listing sites
- Anti-detection considerations (fingerprinting, rate limiting, terms of service)
- When to use this vs HTTP requests (faster but fragile) vs computer use (slower but universal)
- Cost considerations (each agent burns tokens independently)

## Demo Plan

1. Show single-agent Chrome automation speed (2-3 min per form)
2. Build the multi-agent-chrome skill
3. Spawn 4 Chrome agents targeting different rental sites
4. Show all 4 browsers navigating simultaneously
5. Watch them filter, scroll, click, and extract data in parallel
6. Collect results into a unified list
7. Discuss scaling to 10, 50, 100 agents

## Suggested Class Placement

Claude Code — Advanced or Skills chapter
