---
duration: "12-16 min"
batch: 3
order: 6
batch_name: "The Climb"
class: "loopy-ai"
chapter: "Governance Primitives"
status: stub
---

Stub for the L6 fundamentals segment. Teach the guardrails immediately before the loops that need them.

## Thesis

Governance can't be taught in the abstract — the four primitives only bite when there's something real to govern. So we sit this segment at the gate of The Climb, after L3 (Ralph, /goal, autoresearch) and immediately before L4 workers. By the time you walk in, you've already seen a Ralph loop bill $40 overnight and an autoresearch loop spend $12/day. The four primitives stop being plumbing and start being the brake you actually need.

The rest of the class assumes you have these. When the L4 worker segment says "kill switch," it means the one we built here. When the L5 discovery segment says "token budget," it means this one.

## What "fleet" actually means

Before the primitives: define **fleet** operationally. A fleet is the set of loops that share one budget, one kill switch, one log directory, and one retirement policy. The boundary is the shared governance, not the shared topic. Two loops doing very different work but governed by the same kill switch are one fleet. Two loops doing similar work with separate budgets and separate kill switches are two fleets.

This matters because the four primitives are scoped to the fleet, not to "all loops on your machine." If you don't draw the boundary, you can't enforce any of them.

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

## Is L6 itself a loop?

Yes — and saying so honors the Russian-doll framing from [[loop-stack]] without infinite regress. L6 wires up exactly as an L2:

- **builder** = the four primitives running their checks (budget tally, killswitch poll, log writer, retirement audit)
- **work artifact** = a fleet health report (spend, kills triggered, stale loops, retirement candidates)
- **verifier** = a human (you) on a Sunday cadence reading the report
- **exit condition** = the portfolio decision: keep, retire, reallocate, escalate to L7

L6 doesn't recurse forever because its verifier is human-cadence. That's the structural difference between L6 (the runtime watches the loops) and L7 (you decide which loops should exist at all). L7 isn't slow L6 — it integrates information that doesn't exist in the runtime: revenue, strategy, what you're trying to be. We come back to that in [[mission-command]] and [[loop-design-as-craft]].

## How to actually wire it

The four primitives need real mechanics, not just intent. Pick the stack now and commit.

- **Budgets.** Claude Agent SDK exposes `max_budget_usd` and `max_turns` per session — these are *client-side estimates* and can drift from the actual bill. Treat them as belt-and-braces, not the source of truth. The source of truth is `ccusage` tailing the JSONL transcript files, and the Anthropic Admin Usage & Cost API for the per-workspace number. The API has a 1–2 hour lag and no per-key attribution, so under about $X/day you're flying somewhat blind. Mitigation: per-loop workspaces or per-loop API keys, and a `ccusage` aggregator running as its own L2.
- **Kill switches.** A single file (`.fleet/KILL`) or env var that every loop checks at the top of each iteration. Claude Code's Stop hook is the cleanest enforcement point — it can read the file and abort. Don't trust the model to read its own kill switch.
- **Action logs.** Structured JSONL per loop, one line per action, with a timestamp, the tool call, and the artifact ref. Read the log on a cadence. If you can't bring yourself to read it, you don't trust the loop.
- **Retirement.** A loop that hasn't produced anything in the action log marked `useful=true` in N days gets paused. "Useful" is itself a verifier — pick it carefully, because retirement runs on this signal.

## What this segment is *not*

Not a tour of every monitoring tool. Not a deep dive on observability platforms. The primitives are what every loop needs regardless of stack.

## Sources / refs

- Will pull from existing loopy-ai class notes on L6
- Pairs with [[strip-the-model-out]] (deterministic foundations) and [[mission-command]] (the L7 reframe)
- Sets up [[l4-workers]] and [[l5-discovery]] (they'll reference these primitives)

## TODO

- Demo: show a token budget config, show the kill switch file, show an action log, show a retirement rule.
- Image: a control panel with four toggles, each labelled with a primitive.
