---
duration: "10-14 min"
batch: 2
order: 4
batch_name: "L1 On-Ramp"
class: "loopy-ai"
chapter: "L1 Essentials"
aliases: [l1-essentials]
status: stub
---

Stub for the on-ramp segment. Skip permissions, context management, subagents. The L1 housekeeping that makes everything above it usable.

## Thesis

L1 is the harness. Boring but necessary. Most of the "tips and tricks" content on the internet is L1 housekeeping dressed up as agent design. We cover it once, compactly, so it doesn't pollute the rest of the class.

Three things you actually need to know.

## Key beats

- **Skip permissions on the trusted path.** `--dangerously-skip-permissions` is the unlock for everything above L1. Without it, your loops stop every five seconds asking for confirmation. With it, you have to actually trust your loop. Aakash Gupta level 1.
- **Context management.** `/clear` between unrelated tasks. `/compact` when the same task drags on. Scratchpadding to survive resets. Subagent calls to keep tool noise out of your main thread. Aakash level 2 and 3.
- **Subagents as parallel context.** A subagent is a fresh window with its own context budget. Use them for "go and find" and "go and grade" tasks. Their tool output stays out of your main thread. The "go and grade" case is doing more than saving tokens. A subagent grades in a window that never watched the work get made, so it hasn't already committed to "this is done." That clean context is the seed of the verifier in [[closing-the-loop]] and the attacker in [[adversarial-reviewer-skill]]. As both of those segments stress, though, a fresh window only grades honestly if it also has a reason to disagree.
- The "main thread is precious" rule. Anything that produces a lot of tool output should go in a subagent.

## What this segment is *not*

Not a tour of every Claude Code feature. The point is to give students enough L1 to stop fighting the harness and start designing loops. If they want more, send them to the Claude Code class.

## Sources / refs

- Aakash Gupta's autonomy ladder, levels 1-3
- Pairs with [[strip-the-model-out]] (the loop primitives) and [[closing-the-loop]] (the first model-in-the-loop pattern)

## TODO

- Demo: three terminal windows. One showing skip permissions saving 80% of clicks. One showing /clear between two tasks. One showing a subagent grading something while the main thread keeps working.
- Image: a single L1 box with three sub-skills labelled inside it.
