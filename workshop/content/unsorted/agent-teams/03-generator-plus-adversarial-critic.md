---
status: stub
acs: []
mapping: workshop-original
day: 7
block: core
recording-needed: true
---
# Archetype 3: Generator + Adversarial Critic

## What This Video Covers

A two-agent team where one writes and one attacks. The generator produces a candidate. The critic, with a fresh context and an adversarial prompt, hunts for flaws. The generator then either fixes each issue or defends against it. The loop runs until the critic runs out of substantive objections.

This archetype is different from parallel voters (archetype 2) because the critic plays a different role, not just a second opinion. It is different from solo + verifier (archetype 1) because the critic produces a nuanced critique, not a yes/no.

## Why This Matters

From the retreat, the failure mode this archetype is built to fight:

> "Human incident commanders challenge assumptions, push back on comfortable hypotheses and maintain situational awareness. LLMs tend toward positive reinforcement and agreement. Building an effective agent incident commander requires solving this behavioral mismatch. One suggestion: train 'angry agents' that are specifically designed to challenge the dominant hypothesis."

Without deliberate adversarial structure, critic agents default to being polite reviewers who find minor nits. With the right prompt structure, they find real problems. The design of the critic is the lever.

This video focuses on the team architecture. The companion video in techniques (`adversarial-critics-fighting-llm-agreement-bias.md`) focuses on the prompt-craft side.

## The Pattern

```
┌───────────────┐
│  GENERATOR    │ ← writes code / plan / text
│   produces X  │
└───────┬───────┘
        ↓
┌─────────────────────────────┐
│  CRITIC (fresh context)     │ ← adversarial prompt
│  "find the flaw that exists"│
└───────┬─────────────────────┘
        ↓
  ┌─────┴─────────────┐
  │                   │
flaws found      no substantive flaws
  ↓                   ↓
GENERATOR           DONE
  fixes OR defends
  ↓
 loop back to CRITIC
```

Two things that make this work:

1. **Fresh context for the critic**. If the critic shares a session with the generator, it inherits the generator's sunk cost and biases. Fresh session, ideally different model.

2. **Defend as a valid response**. Not every critique is correct. The generator has to be allowed to push back. If every critique forces a change, you just make the code longer.

## Specialized Critics

A single critic prompt is blunt. Better: multiple critics with narrow remits, running in parallel:

- **Security critic**: "Find the injection, auth-bypass, or secret-leak risk."
- **Performance critic**: "Find the query that will be slow at 10x load, or the N+1."
- **Correctness critic**: "Find the off-by-one, the null case, the race condition."
- **Simplicity critic**: "Find the three lines that could be deleted without changing behavior."
- **Edge-case critic**: "Name three inputs the author did not test for."

Each produces a narrow critique. Merge them. The generator addresses the combined list. This is a small swarm of critics feeding one generator, which is its own interesting structure.

## Difference From Solo + Verifier

Solo + verifier (archetype 1) asks yes/no. The verifier is narrow and cheap. Good for well-defined correctness.

Generator + critic is nuanced. The critic produces a critique, not a pass/fail. Good for artifacts where correctness has many dimensions (code quality, security, performance, edge cases) and where the critique itself is useful information even when the code could ship.

A common production setup combines both: solo + verifier to confirm the thing works at all, generator + critic to make it actually good.

## Difference From Parallel Voters

Parallel voters (archetype 2) run the same task N times and aggregate. Each agent is playing the same role. The "wisdom" comes from averaging.

Generator + critic has asymmetric roles. The critic is not a second attempt at the task, it is a different job. You can't swap them. This is the key structural difference.

## Where This Archetype Fits

- **Code review**: the pattern at its most natural. Generator writes, critic reviews, generator responds.
- **Plan review**: before executing a plan, have an adversarial critic find the unstated assumption that will fail.
- **Writing / editing**: draft writer plus a skeptical editor. The critic is specifically tasked with finding weak arguments.
- **Spec review**: the retreat notes this is where rigor is moving. Generator writes spec, critic asks "what requirement is missing."

## Watch Out For

- **The critic hallucinates flaws in clean work.** Adversarial prompts cause false positives when the work is genuinely good. Need a verifier step or a "defend" mode to filter.
- **The generator capitulates too easily**. If every critique forces a rewrite, outputs get bloated. The defend option has to be real.
- **The loop doesn't terminate**. Without a stopping condition ("critic has no substantive new objections"), the loop can run forever. Define done.
- **Context pollution**. Long critic/generator exchanges bloat context. Each round should summarize and reset, not accumulate.

## Connection to Subagent Verification Loops

The existing `subagent-verification-loops.md` video in techniques describes a three-agent pipeline: implementer → reviewer → resolver. That is a specific instantiation of this archetype, where the reviewer role is split from the resolver role. This video is the general pattern; that one is a concrete pipeline inside it.

## Key Concepts to Cover

- Generator and critic as asymmetric roles (unlike voters)
- Fresh context for the critic as non-negotiable
- The defend branch as equal to the fix branch
- Specialized critics with narrow remits (security, performance, correctness, edge-case, simplicity)
- Difference from archetype 1 (verifier is yes/no, critic is nuanced)
- Difference from archetype 2 (voters are same role, critic is different role)
- False-positive failure mode on clean work
- Loop termination (define done)
- Context pollution across long loops
- Relationship to subagent-verification-loops as a specific instantiation

## Demo Plan

1. Single generator writes a feature. Show it ships with subtle issues.
2. Generator + single critic loop. Show the critic finding issues, generator fixing them.
3. Add a defend case: critic raises a false concern, generator pushes back with reasoning.
4. Specialized critic swarm (security + performance + correctness in parallel). Show merged critique.
5. Show termination: critic runs out of substantive objections, loop exits.
6. Show context pollution problem and how to reset between rounds.

## Suggested Class Placement

Agent Teams — Video 4. Pairs with the techniques videos `subagent-verification-loops.md` (concrete pipeline) and `adversarial-critics-fighting-llm-agreement-bias.md` (prompt craft).
