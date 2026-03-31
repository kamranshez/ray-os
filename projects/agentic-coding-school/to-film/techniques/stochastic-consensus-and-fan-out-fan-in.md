# Stochastic Multi-Agent Consensus + Fan-Out / Fan-In

## What This Video Covers

Two parallelization patterns that exploit the fact that LLMs are stochastic (same prompt → slightly different answers each time). Both spawn N agents in parallel and combine results, but for different purposes:

- **Stochastic Consensus:** Same question with slight framing variations per agent. Aggregate results by frequency (mode). High-frequency answers = high confidence. Low-frequency answers = potential outliers worth investigating.
- **Fan-Out / Fan-In:** Different research angles per agent. Cheap models (Sonnet/Haiku) do the research, expensive model (Opus) synthesizes. Model routing for cost savings.

## Why This Matters

**Consensus:** Instead of getting 3 ideas from one run, you get the FULL distribution of possible answers. If 8/10 agents suggest the same thing, it's high confidence. If 1/10 suggests something unique, it's either brilliant or hallucinated — but you'd never find it from a single run. This is how you systematically find outlier ideas.

**Fan-out/fan-in:** Reduces research time from 25 minutes (serial) to ~10 minutes (parallel). Uses cheaper models for the heavy lifting (60% cost savings). Keeps the synthesizer in the "zone of good" context-wise because it only receives summaries, not 100K tokens of raw research.

## The Statistics Behind It

LLMs are stochastic — due to temperature and sampling, the same prompt produces slightly different outputs each time. If you run 3 times:
- Run 1: ideas A, B, C
- Run 2: ideas A, B, D
- Run 3: ideas B, C, E

Single run gives you 3 ideas. Three runs give you 5 unique ideas (A, B, C, D, E). Ten runs with framing variations might give you 15-20 unique ideas spanning the full solution space.

The mode (most frequent answer) tells you what's statistically likely to be correct. The outliers tell you what's potentially brilliant but risky.

## How the Competitor Teaches It

**Consensus demo:**
- Creates a skill called "stochastic-multi-agent-consensus"
- Spawns 10 agents with different analytical framings: conservative, adventurous, first-principles, contrarian, user advocate, budget-conscious, etc.
- Demos on a real business problem (TikTok growth strategy)
- Shows the consensus report: consensus items, divergent items, outliers
- 119 raw ideas → 52 unique after deduplication

**Fan-out/fan-in demo:**
- Spawns 6 Sonnet researchers on different optimization axes for a codebase
- Each researcher works independently with its own clean context window
- Opus synthesizer integrates all summaries into a prioritized action plan
- Shows the architecture: parent → researchers (cheap) → synthesizer (expensive)

## Key Concepts to Cover

- Why stochasticity is a feature not a bug
- The search space visualization (pie chart — single run covers a sliver, N runs cover most)
- Slight framing variations per agent (conservative, edge-case finder, user advocate, contrarian)
- Statistical aggregation: mode (frequency), median, outliers
- Parallelization benefit: 10 agents = same wall-clock time as 1
- Fan-out: spawn N cheap researchers on DIFFERENT angles (not the same question)
- Fan-in: expensive synthesizer integrates summaries only (not raw research)
- Model routing: Sonnet/Haiku for research at $3/M, Opus for synthesis at $5/M
- Context isolation: each researcher has its own clean window → stays in "zone of good"
- Cost savings calculation (concrete math)
- Difference between consensus (same question, varied framing) and fan-out (different questions)
- When to use consensus (strategic decisions, ideation) vs fan-out (research, API evaluation)
- Practical demo on a real business/strategy decision

## Demo Plan

1. Show stochasticity: same prompt in 3 tabs → different answers
2. Build consensus: spawn 10 agents with varied framings on a strategy question
3. Show the consensus report (consensus, divergent, outlier categories)
4. Build fan-out: spawn 6 Sonnet researchers on different angles of a codebase optimization
5. Show Opus synthesizer combining results
6. Compare token costs and time: serial vs parallel

## Suggested Class Placement

Techniques — Advanced Techniques
