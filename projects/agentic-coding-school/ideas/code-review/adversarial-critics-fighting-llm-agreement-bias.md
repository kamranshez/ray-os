---
class: "code-review"
status: "idea"
aliases: [adversarial-critics-fighting-llm-agreement-bias]
---

# Adversarial Critics: Fighting LLM Agreement Bias

## What This Video Covers

LLMs have a well-documented failure mode: they are trained toward helpfulness, which bleeds into agreement. Ask "is this code correct?" and you will usually get "yes, with these caveats." Ask "does this plan have holes?" and you will usually get "looks solid overall."

The fix is not "be more critical when you ask." The fix is structural: you write prompts that assume flaws exist and make the agent hunt for them. Done well, this turns a critic agent into something that actually catches problems instead of validating them.

This video covers the technique: how to write adversarial prompts, when to use them, and how to chain them into generator / critic pipelines that converge on correctness.

## Why This Matters

From the retreat, on why human incident commanders are hard to replace with LLMs:

> "Human incident commanders challenge assumptions, push back on comfortable hypotheses and maintain situational awareness. LLMs tend toward positive reinforcement and agreement."

And the suggested fix:

> "Train 'angry agents' that are specifically designed to challenge the dominant hypothesis."

This is a general pattern, not just an incident response pattern. Any time you want an agent to catch its own (or another agent's) mistakes, you are fighting the agreement bias. The prompt structure is the lever.

## The Core Problem

Three prompts that look similar but produce wildly different behavior:

1. "Is this code correct?" → agreement. The agent will say yes and add mild caveats.
2. "Review this code." → polite review. The agent will find stylistic nits and low-severity issues.
3. "Find three bugs in this code. Assume the author missed something important." → adversarial. The agent will find three things, and often they are real.

Notice prompt 3 works even when there are no real bugs. That is both the feature and the trap. You get high recall on real issues, but you also get false positives when the code is genuinely clean. A critic agent alone is not a verifier. It needs a loop back to the generator that either fixes the issue or defends the code.

## The Technique: Presuppose the Flaw

Instead of asking whether a flaw exists, assume it does and ask what kind. Compare:

- Weak: "Does this plan have any issues?"
- Strong: "This plan has at least one unstated assumption that will fail in production. What is it?"

- Weak: "Review this code for security."
- Strong: "A security reviewer has flagged this code. Find the vulnerability they saw. Do not tell me the code is fine."

- Weak: "Is the architecture sound?"
- Strong: "Name the three decisions in this architecture that will be regretted in 12 months, and why."

The presupposition is doing the work. The agent accepts the frame and hunts.

## Specialized Critics

Different flaws live in different places. A single critic prompt is a blunt instrument. Better: multiple critics with narrow, specialized remits:

- **Security critic**: "Find the injection, auth-bypass, or secret-leak risk."
- **Performance critic**: "Find the query that will be slow at 10x load, or the N+1."
- **Correctness critic**: "Find the off-by-one, the null case, the race condition."
- **Edge-case critic**: "Name the three inputs the author did not test for."
- **Simplicity critic**: "Find the three lines that could be deleted without changing behavior."

Each runs in its own clean context. Their outputs merge into a single critique list. The generator then has to address or defend each item.

## The Generator / Critic Loop

The full shape:

```
GENERATOR writes code / plan / text
    ↓
CRITIC (fresh context, adversarial prompt) finds issues
    ↓
If critic finds substantive issues:
    GENERATOR addresses each one (fix or defend)
    ↓ loop back to CRITIC
If critic runs out of substantive objections:
    DONE
```

Two design points that matter:

1. **The critic must have fresh context**. If the critic is the same session as the generator, it inherits the generator's biases and sunk cost. Fresh session, ideally different model.

2. **The generator must be allowed to defend, not just capitulate**. If every critique forces a change, you are just making the code longer. Sometimes the right answer is "the critic is wrong, here is why." A good loop has both modes.

## When Adversarial Prompts Backfire

- **Creative writing**: aggressive criticism flattens voice. Use lightly.
- **Truly clean code**: the critic will still find "issues," which will be false positives. Need a verifier step to filter.
- **Early exploration**: if you are still figuring out what you want, adversarial critique kills the brainstorm. Use after you have a candidate, not before.

The rule of thumb: adversarial critics work best when the output is supposed to converge on a single correct artifact. They work worst when the output is supposed to diverge into possibilities.

## Key Concepts to Cover

- LLM agreement bias as a trained-in failure mode, not a prompt mistake
- Three versions of "review this" and how prompt strength scales with presupposition
- The presupposition pattern: assume the flaw exists, ask what kind
- Specialized critics with narrow remits (security, performance, correctness, edge-cases, simplicity)
- Why the critic needs fresh context (not the same session as the generator)
- The full generator / critic loop, including the "defend" branch
- Why adversarial prompts cause false positives on clean work (and how to filter)
- When NOT to use adversarial prompts (creative work, brainstorming, early exploration)
- The connection to swarms: adversarial critics are one archetype of convergence architecture
- The connection to verification loops: the critic is a verifier, the generator is a producer

## Demo Plan

1. Show a plan. Ask "any issues?" — agent says no.
2. Same plan. Ask "find the unstated assumption that will fail." — agent finds it.
3. Show the full generator / critic loop on a real code task with specialized critics.
4. Show the generator defending a critique instead of capitulating.
5. Show a false-positive case where the critic "finds" an issue that isn't real.

## Suggested Class Placement

Techniques — Advanced Techniques (pairs with subagent-verification-loops as the prompt-craft side of the same pattern. This video: how to write the critic prompt. That video: how to pipeline implementer → reviewer → resolver.)
