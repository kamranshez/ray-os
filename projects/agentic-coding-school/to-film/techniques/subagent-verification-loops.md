# Subagent Verification Loops (Implement → Review → Resolve)

## What This Video Covers

A formal 3-agent pipeline for producing higher-quality code (or any output). Agent 1 (Implementer) builds the thing. Agent 2 (Reviewer) evaluates the output with ZERO context about how it was built — pure objective review. Agent 3 (Resolver) fixes issues the reviewer identified. The key insight: the implementer is biased by sunk cost; the reviewer catches what the implementer missed because it has no context about the journey.

## Why This Matters

One agent reviewing its own work is inherently biased. It spent 200K+ tokens reasoning through approaches, hitting dead ends, making design decisions. All that history creates "sunk cost bias" — it believes its approach is correct because it invested so much in getting there.

A fresh reviewer agent sees ONLY the output. No reasoning history, no dead ends, no emotional attachment. It evaluates the code the same way it would evaluate a random snippet from the internet. This objectivity catches issues that the implementer is blind to.

The competitor demos this on a real app and finds 22 issues that the original builder (Gemini) couldn't see — even when explicitly asked to self-review.

This is the AI equivalent of academic peer review or code review in professional development.

## The Pipeline

```
Agent 1: IMPLEMENTER
  ↓ writes code
  ↓ (biased by 200K tokens of reasoning history)
  
Agent 2: REVIEWER (fresh context, zero bias)
  ↓ evaluates output only — no access to reasoning
  ↓ reviews for: correctness, edge cases, simplification, security
  ↓ if issues found → lists them
  ↓ if no issues → approved ✓
  
Agent 3: RESOLVER (fresh context)
  ↓ receives issues list + original code
  ↓ fixes each issue
  ↓ testing/verification
  
Result: higher quality output
```

## How the Competitor Teaches It

- Builds a skill called "agent-review" that spawns subagents
- The skill reviews on 4 axes:
  1. **Correctness** — does the code do what it's supposed to?
  2. **Edge cases** — what inputs/scenarios would break it?
  3. **Simplification** — can this be done in fewer lines or simpler logic?
  4. **Security** — any vulnerabilities? (SQL injection, XSS, auth bypass)
- Runs it on an existing app (Splinter) built by Gemini
- Finds 22 issues: some critical, some high, some medium, some low
- The original builder (Gemini) couldn't find these even when asked "are there any issues?"
- Then fixes the issues using a separate resolver agent
- Emphasizes: don't use the same agent for both building and reviewing

## Key Concepts to Cover

- Why one agent can't review its own work:
  - Sunk cost bias (invested 200K tokens in this approach → believes it's correct)
  - Context pollution (dead ends and reasoning history cloud judgment)
  - Confirmation bias (looks for evidence the code works, not evidence it doesn't)
- The 3-agent pipeline: implement → review → resolve
- Fresh context = zero bias for the reviewer (ONLY sees the output)
- The 4 review axes: correctness, edge cases, simplification, security
- Building this as a reusable skill ("agent-review")
- The reviewer should use a DIFFERENT model or at minimum a fresh session
- Academic peer review analogy: the author can't review their own paper
- How this differs from existing "Avoiding Code Bias" video:
  - That video: using a different model/chat to get a fresh perspective
  - This video: formalizing it as a 3-agent PIPELINE with a reusable skill
- When to use: after any non-trivial implementation (features, refactors, new modules)
- When NOT to use: trivial changes (rename a variable, update a string)

## Demo Plan

1. Build something with Claude Code (a feature or small app)
2. Ask the SAME agent to review its own work — show it finds nothing
3. Run the agent-review skill — spawn fresh reviewer subagent
4. Show the reviewer finding issues the implementer missed
5. Show the resolver fixing the issues
6. Run the reviewer again on the fixed code — show clean pass
7. Compare: self-review (0 issues found) vs peer review (22 issues found)

## Suggested Class Placement

Techniques — Advanced Techniques (partially covered by "Avoiding Code Bias" but deserves dedicated treatment as a formal pattern with a reusable skill)
