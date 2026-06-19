---
tags: [agentic-coding, validation, code-review, cost-bias]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
status: "idea"
---

## What this video covers

Why the agent that wrote the code cannot be the one that verifies it. The structural reason: cost bias. The implementing agent has spent thousands of tokens committing to its approach and is going to defend it. A fresh agent with no investment in the implementation finds bugs the original agent literally cannot see.

This is why human code review works, and why the same property has to be designed into agent systems explicitly.

## Why this matters

Most agent systems today fail at this. They ask the same agent to write code and then verify it. The agent writes a passing test, declares victory, and moves on. The bug ships.

Adversarial validation is the design pattern that fixes this. It is not optional for long-running work.

## Sub-chapter 1: Cost bias is structural

The cleanest framing of the problem:

> "The agent that implemented the code has some cost bias, right? It wants that code to work. A fresh agent with fresh context is way more likely to find issues. And this is why we do code review as humans as well."

Cost bias is not a model weakness you can prompt your way out of. It's a property of the conversation. Every token the agent generated committing to an approach is now in its context, biasing every subsequent token toward defending that approach.

You cannot tell an agent "be objective about your own work." It will agree it is being objective and continue defending its work.

## Sub-chapter 2: Fresh context, fresh eyes

The fix: spawn a new agent. New conversation. No memory of the implementation. It reads the diff and the validation contract and asks the only question that matters: does this code satisfy these assertions?

> "Critically neither validator has seen the code before. They are not invested in the implementation and so validation is adversarial by design."

"Adversarial by design" is the key phrase. The validators aren't trying to be helpful collaborators. They're trying to find what's wrong. That's their entire job.

Implementing agents and validating agents have different goals on purpose. One wants to ship. The other wants to find bugs. The system works because they pull in opposite directions.

## Sub-chapter 3: Mirroring human code review

The same pattern in human teams:

> "This is why we do code review as humans as well."

Why don't engineers self-review? Because they have cost bias. Why don't reviewers also write the code? Because then they'd have cost bias too. The two-role split exists for the same structural reason in humans and in agents.

If you've ever done a "let me just review my own PR" and missed the bug that was obvious to a colleague the next morning, you've experienced cost bias firsthand.

## Sub-chapter 4: Designing adversarial agents

What goes into a validator's prompt:

- The validation contract (what to check against).
- The diff or the running application (what to check).
- An explicit framing: your job is to find bugs, not to approve.
- No history of the implementation conversation.

What does *not* go in:

- The implementing agent's reasoning.
- Justifications for design choices.
- "The implementer thought this was fine."

Sharing the implementation context corrupts the verifier. Adversarial design means starving the verifier of the implementer's reasoning so it cannot inherit the implementer's blind spots.

## Sub-chapter 5: Dedicated subagents per feature

For code review specifically, missions spawns one reviewer per feature, in parallel.

> "It runs the test suite, type checking, lints and critically it spawns dedicated code review agents for each completed feature within the milestone."

Why per-feature instead of one big reviewer:

- **Scope is bounded.** A reviewer assigned to feature 7 can hold all of feature 7's diff in context. A single reviewer for the whole milestone can't.
- **Parallel.** Code review is readonly, so per-feature reviewers run in parallel without conflict.
- **Better signal.** A focused reviewer finds more bugs than a generalist reviewer skimming a giant diff.

This is the only place in missions where parallelism is aggressive. It's safe because each reviewer reads only; none of them write.

## Sub-chapter 6: The verifier needs a narrow question

Connecting back to the validation contract: an adversarial verifier only works if the question it's answering is narrow and unambiguous.

"Is this code good?" is not a verifier question. The agent will say yes; you can't fault its reasoning. "Does this code's behavior satisfy assertion #47 of the validation contract?" is a verifier question. There's a right answer and a wrong answer, and the validator can be graded.

This is why the validation contract video is the prerequisite for this one. Without a contract, "adversarial validation" is just two agents arguing about subjective code quality. With a contract, it's a test you can pass or fail.

## Talking points for filming

- Open with the human-code-review analogy; everyone has the lived experience
- Emphasize cost bias is structural, not a "bad agent" problem
- Show the two prompts side by side: implementer vs validator
- Per-feature reviewer parallelism as the practical implementation detail

## Key takeaway

Reusing the implementing agent as verifier guarantees blind spots; adversarial validation requires fresh context and a separate goal.
