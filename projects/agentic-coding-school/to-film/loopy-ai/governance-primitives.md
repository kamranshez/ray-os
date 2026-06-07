---
duration: "12-16 min"
batch: 2
order: 4
batch_name: "Foundations"
class: "loopy-ai"
chapter: "Governance Primitives"
status: stub
---

Stub for the L6 fundamentals segment. Teach the guardrails before the things they guard.

## Thesis

Most classes teach worker and discovery loops first and bolt governance on later. That's backwards. The first runaway loop teaches you why you needed governance from day one. This segment installs that day-one habit by teaching the four governance primitives before students build anything that needs them.

The rest of the class assumes you have these. When the L4 worker segment says "kill switch," it means the one we built here. When the L5 discovery segment says "token budget," it means this one.

## The four primitives

- **Token budgets.** Per loop, per fleet, per day. Hard cap, soft cap, and a daily report. If a loop spends two times its expected budget, it stops. No exceptions.
- **Kill switches.** A single file or env var that any loop in the fleet checks every iteration. Flip it, every loop exits cleanly at the next check. This is the brake, not the off switch.
- **Action log review.** Every loop writes a structured log of every action. A human reads the log on a cadence. If you can't bring yourself to read the log, you don't trust the loop, and you shouldn't.
- **Retirement.** A loop that hasn't produced anything useful in N days gets paused. Loops are cheap to start, expensive to leave running.

## Key beats

- The "thousand dollar overnight" story. The first runaway loop is when you learn this.
- Why governance is L6, not Ops. It operates on loops as the unit, not on artifacts.
- Why budgets must be enforced at the runtime, not the prompt. The model will lie about its remaining budget. The runtime will not.
- The diagnostic: if your loops can run forever without you noticing, you don't have governance.

## What this segment is *not*

Not a tour of every monitoring tool. Not a deep dive on observability platforms. The primitives are what every loop needs regardless of stack.

## Sources / refs

- Will pull from existing loopy-ai class notes on L6
- Pairs with [[strip-the-model-out]] (deterministic foundations) and [[mission-command]] (the L7 reframe)
- Sets up [[l4-workers]] and [[l5-discovery]] (they'll reference these primitives)

## TODO

- Demo: show a token budget config, show the kill switch file, show an action log, show a retirement rule.
- Image: a control panel with four toggles, each labelled with a primitive.
