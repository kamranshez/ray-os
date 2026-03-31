# Auto Research (Karpathy Loop)

## What This Video Covers

A framework for progressive autonomous improvement based on Andrej Karpathy's open-source auto-research repo. The agent runs in a continuous loop: hypothesize a change → execute the change → assess with a standardized metric → keep if improved, discard if not → repeat. Over hundreds of iterations, a system improves dramatically without human intervention.

## Why This Matters

This is the bridge between "agentic engineering" (human directs agent) and "independent research" (agent runs autonomously). Once set up, the agent just runs — you go to sleep and wake up to a better system. Toby Lutke (Shopify CEO) used this approach to get 53% faster parse+render time on Shopify Liquid and 61% fewer object allocations.

Applicable to anything with a measurable metric: website load speed, cold email reply rates, ad creative click-through, conversion rates, prompt quality scores, even AI model training itself.

## The 3 Requirements

Auto research only works when you have all three:

1. **A metric to optimize** — must be objective and standardized (e.g. Google Lighthouse score, email reply rate, conversion percentage)
2. **A change method** — a way to influence that metric (e.g. modifying website code, tweaking email copy, adjusting ad creative)
3. **An assessment** — a way to measure the result quickly (e.g. run Lighthouse test, check reply rate after 24h, measure CTR)

The faster the change method and assessment, the more iterations per day. If both take 30 seconds, you get 1,440 experiments per day. Even at 2% success rate, that's ~30 improvements/day → 1.01^30 = 34% improvement in one day.

## How the Competitor Teaches It

- Clones Karpathy's auto-research repo (`github.com/karpathy/auto-research`)
- Explains the three files: `prepare.py` (data setup), `train.py` (the thing being optimized), `program.md` (what the agent can modify)
- Sets up a Lighthouse page speed optimization loop on a real website
- Builds a live dashboard to watch experiments run and metrics improve
- Shows the actual score improving over time (LCP dropping from 1802ms to 8000ms improvement)
- Generalizes beyond websites: cold email, conversion rate, ad creative
- References the Shopify/Lutke case study as proof this works at scale

## Key Concepts to Cover

- The 3 requirements: metric, change method, assessment
- `program.md` — tells the agent what it can and cannot modify
- `train.py` — the actual system being optimized
- Setting up auto research on a real website (Lighthouse page speed)
- Building a dashboard to monitor experiments in real-time
- The math: iterations per day × success rate × improvement per success = compound gains
- Business applications beyond speed: cold email reply rates, conversion rate optimization, ad creative CTR
- The Shopify/Lutke case study (53% faster, 61% fewer allocations)
- How to scope what the agent can and cannot change (preventing it from breaking visual design while optimizing speed)
- The spectrum: vibe coding → agentic engineering → auto research → fully autonomous
- Relationship to the autoresearch skill already in the skills library

## Demo Plan

1. Clone Karpathy's repo into a workspace
2. Build a simple website (or use an existing one)
3. Set up the auto research loop targeting Lighthouse performance score
4. Configure program.md with constraints (don't change visual design)
5. Run the loop and watch the dashboard as metrics improve
6. Show the log of successful and failed experiments
7. Discuss business applications with concrete examples

## Suggested Class Placement

Claude Code — Advanced chapter, or a standalone video in Workflows
