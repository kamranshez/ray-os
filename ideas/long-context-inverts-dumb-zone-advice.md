---
tags: [agentic-coding, context-windows, long-context]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Long context models invert dumb-zone advice

## The idea
The conventional wisdom — "stay under 100k tokens, the dumb zone will eat you" — is a rule of thumb for people without intuition. With million-token context models and active human steering, you can comfortably push to 800k+ tokens on certain tasks. The middle of the window is still under-weighted, but if the human is actively steering and re-injecting the things that matter into recent messages, you compensate for the model's forgetting. The "dumb zone" rule assumes a passive operator. An engaged operator inverts it.

## The mechanism
- Middle context loses influence, not information
- Active operators reiterate critical points naturally as conversation continues
- The model attends most to recent messages — which the human is shaping in real time
- Long context becomes a *cache of everything explored* rather than a liability

## When it works vs. doesn't
**Works:**
- Heavy design discussions where you're actively reading and responding
- Tasks where you'd otherwise lose valuable exploration
- When you want to avoid re-establishing context in a fresh chat

**Doesn't work:**
- Multi-turn tool-calling loops (model spins out, per Chris on Twitter)
- Tasks where the operator is disengaged or batch-processing
- When you can't tell whether forgotten context is biting you

## How to apply
- Match context strategy to engagement level, not to a token-count rule
- If you're highly engaged → use bigger context, let it rip, you're the safety net
- If you're disengaged / running in background → keep context small, let the model make fewer mistakes
- Recognize the rule is "correlated with engagement," not absolute

## Surrounding context
Vibhav: "If you want to be highly engaged in the process, go further. If you want to be highly disengaged to background tasks, you probably don't want to go as far." He hits 800k tokens regularly on BAML work. Dex pushes back: "if you're going to pretend the middle doesn't impact you, why not just start a new one?" Vibhav: "convenience — and it's not that it doesn't impact you, it has less influence." This is the active-steering thesis: the human's job in long context is to keep dragging important state forward into recent turns.

## Open questions to explore
- What does "active steering" look like as a teachable skill?
- Are there models where this strategy fails harder than others?
- Can you build tooling that auto-injects forgotten-but-important state back into recent context?
- Is there a measurable point where steering effort exceeds the cost of just starting fresh?
