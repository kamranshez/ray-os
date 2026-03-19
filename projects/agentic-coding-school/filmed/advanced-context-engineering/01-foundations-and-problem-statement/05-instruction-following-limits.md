---
status: filmed
---

## Source

- https://arxiv.org/abs/2507.11538 (IFScale Study, July 2025)
- https://arxiv.org/abs/2510.14842 (Elder et al., Oct 2025)
- https://arxiv.org/abs/2512.14754 (Dong et al., Dec 2025)

---

## The Intuition

You might think: if search isn't enough, I'll just write better instructions. I'll put everything the model needs to know in my CLAUDE.md.

This doesn't work either.

Models can only reliably follow so many instructions at once. The more you add, the less likely any single instruction will be followed. This isn't a bug. It's a fundamental limitation of how attention works.

---

## What the Research Shows

The IFScale benchmark (July 2025) measured how well models follow increasing numbers of simultaneous instructions.

Three patterns emerged:

1. **Threshold decay** — Best models (Gemini 2.5 Pro, o3) perform near-perfect until ~150 instructions, then fall off a cliff
2. **Linear decay** — Mid-tier models (GPT-4.1, Claude Sonnet 4) decline steadily across the board
3. **Exponential decay** — Smaller models degrade rapidly, then flatline at low accuracy

Even the best frontier models only hit 68% accuracy at 500 instructions.

## What This Looks Like in Practice

You write a detailed CLAUDE.md with all your coding standards, architectural patterns, and constraints. The model seems to follow most of it... most of the time.

Then one day it ignores a critical rule. No warning. No explanation. It just... didn't see it.

That's instruction decay in action. When you dump everything into one place:

- Instructions compete with each other
- Important rules get lost in the noise
- The model drops constraints silently
- Behavior becomes inconsistent across sessions

Sound familiar? It's the signal-to-noise problem again. Too many instructions = noise.

---

## The Implication

The goal isn't to tell the model everything. It's to tell it the right things at the right time.

This means:

- Keep your root CLAUDE.md minimal
- Use progressive disclosure — load instructions only when relevant
- Make constraints local, not global
- Prune regularly

If everything is important, nothing is.
