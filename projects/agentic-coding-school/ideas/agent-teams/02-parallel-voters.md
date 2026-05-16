---
status: stub
acs: []
mapping: workshop-original
day: 7
block: core
recording-needed: true
---
# Archetype 2: Parallel Voters

## What This Video Covers

Run the same task N times in parallel, then aggregate by vote or judge. This archetype exploits the fact that LLMs are stochastic: same prompt, slightly different answers each time. Averaging across many runs is one of the cheapest and most effective ways to raise accuracy without changing the model.

This is self-consistency sampling at the team-architecture level. Industry benchmarks show it often adds 10+ points of accuracy on reasoning tasks with zero model changes.

## Why This Matters

Voting works because individual errors are often uncorrelated. If agent A gets the wrong answer due to a particular hallucination, agent B (running independently) probably gets the wrong answer in a different way, or gets the right answer. The mode of many answers converges on correctness faster than any single answer can.

The retreat frames this as the simplest possible swarm:

> "Self-consistency sampling in LLM inference (generate N answers, take the majority) is the simplest possible swarm — one model, N rolls, convergence by voting."

The overlap with stochastic-multi-agent-consensus (already in the techniques folder): same underlying mechanism, different framing. That video focuses on using the distribution to find outlier ideas. This video focuses on using the distribution to raise accuracy on tasks with a single correct answer.

## The Pattern

```
        ┌─────────────┐
        │    TASK     │
        └──────┬──────┘
               │
     ┌─────────┼─────────┐
     ↓         ↓         ↓
  AGENT 1   AGENT 2   AGENT 3   ...  AGENT N
     ↓         ↓         ↓               ↓
   answer    answer    answer         answer
     │         │         │               │
     └─────────┼─────────┴───────────────┘
               ↓
        ┌─────────────┐
        │ AGGREGATOR  │ ← vote / judge / verifier
        └──────┬──────┘
               ↓
           final answer
```

The agents are independent. They do not see each other's work. The aggregator is a separate step.

## Three Ways to Aggregate

- **Majority vote** — works when the answer is discrete. "What is the correct SQL to answer this question?" with N candidates, keep the one that appears most often.
- **Judge agent** — an LLM whose only job is to pick the best candidate. Works for continuous outputs like code or text. Cheaper than re-running the task, and the judge can be a smaller model.
- **Verifier filter** — run the solo + verifier archetype N times in parallel. Keep only candidates that pass verification. Pick from survivors.

Each has a cost profile. Majority vote is cheapest but needs discrete answers. Judge is flexible but adds latency. Verifier filter gives the highest quality but needs a reliable verifier.

## Tuning the Swarm

The two knobs that matter:

1. **Temperature / diversity**. Too low and all N agents converge to the same wrong answer — correlated errors, no benefit from voting. Too high and you get noise that drowns out any signal. Sweet spot is usually moderate temperature with slight framing variations per agent.

2. **N (how many agents)**. Diminishing returns kick in fast. 5 to 10 is usually enough. 100 is almost always wasteful. If 10 don't give you a clear winner, the task is probably genuinely ambiguous and more samples won't fix it.

A small framing variation per agent helps: "conservative approach," "edge-case focused," "first-principles," "contrarian," "user-advocate." Same task, slightly different angles. The distribution of answers covers more of the solution space than N identical prompts would.

## When This Archetype Shines

- Tasks with a single correct answer that is hard to verify but easy to vote on (math, SQL, classification)
- Tasks where you want ideas from the full distribution, not just the most likely one (strategy, ideation)
- Tasks where you can afford the parallelism cost and want to trade tokens for accuracy

## When Not to Use It

- Tasks that are already well-solved by a single run (waste of tokens)
- Tasks where the output is creative / subjective (voting converges to the blandest average)
- Tasks that are expensive to run even once (research with 50K tokens of tool calls per agent)

## Connection to the Earlier Technique Video

The existing `stochastic-consensus-and-fan-out-fan-in.md` in techniques covers two specific flavors: consensus for outlier ideas, fan-out/fan-in for cost-efficient research. This video is the team-architecture framing: parallel voters as a general convergence pattern that those techniques are specific instantiations of.

## Key Concepts to Cover

- Stochasticity as a feature: same prompt, different answers
- Why independent errors don't compound the way correlated errors do
- The three aggregators: majority vote, judge agent, verifier filter
- Temperature as a diversity knob (too low = correlated errors, too high = noise)
- N with diminishing returns (5 to 10 is usually the sweet spot)
- Framing variation per agent (conservative, contrarian, edge-case focused)
- When this beats a single strong agent (benchmarks, 10+ accuracy points)
- When this wastes tokens (easy tasks, creative tasks, expensive tasks)
- The relationship to the existing stochastic-consensus technique

## Demo Plan

1. Run a reasoning task once. Show the answer.
2. Run the same task 10 times. Show the distribution — mode is correct, outliers are wrong.
3. Same task, 10 agents with slight framing variations. Show richer distribution.
4. Aggregate with majority vote. Show the winning answer.
5. Aggregate with a judge agent. Compare.
6. Aggregate with verifier filter. Compare.
7. Cost and accuracy math: 1 run vs 10 runs vs 10 runs + judge.

## Suggested Class Placement

Agent Teams — Video 3. Pairs with the existing `stochastic-consensus-and-fan-out-fan-in.md` video in techniques, which shows concrete instantiations of this general pattern.
