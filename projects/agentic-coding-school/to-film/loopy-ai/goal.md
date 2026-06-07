---
duration: "12-16 min"
batch: 3
order: 3
batch_name: "The Climb"
class: "loopy-ai"
chapter: "/goal Mode"
status: stub
---

Stub — /goal mode. Keep the context alive, fight drift with structure. The runtime owns the loop, the model can't cheat it.

State machine in the runtime: objective, optional token budget, auto-continuation, a completion audit, "budget exhaustion is not completion." An *infrastructure* pattern, in contrast to Ralph's discipline pattern.

## Key beats

- The state machine: objective, completion audit, auto-continuation.
- Why "budget exhaustion is not completion" matters.
- When to pick /goal versus Ralph: pre-decomposable work versus unfolding work.
- Failure modes: vague objectives, no completion audit, audits that defer to the model.

## Sources / refs

- https://x.com/jarrodwatts/status/2052372045829382430
- https://x.com/kingbootoshi/status/2052510026535936157
- Pairs with [[ralph-loops]] (the discipline variant), [[writing-effective-goals]] (how to write the objective), [[mission-command]] (the L7 reframe of "goal").
