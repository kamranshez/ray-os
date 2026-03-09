---
status: filmed
---

## Source

- https://arxiv.org/abs/2509.04292 (Inverse IFEval, Oct 2025)

---

## The Problem

You've given the model the right context. You've kept your instructions minimal and relevant. And still — it fights you.

You tell it to follow your unconventional auth pattern. It "corrects" your approach back to the standard way. You tell it not to add comments. It adds comments anyway.

This is cognitive inertia.

---

## What Is Cognitive Inertia?

Cognitive inertia is the model's tendency to stick to patterns from training, even when you explicitly ask for something different.

The model has seen millions of examples. Those patterns are sticky. When your codebase does things differently, the model resists. It wants to pull you back toward convention.

If your codebase uses a non-standard pattern, the model may:

- Try to "fix" your approach
- Perform worse on follow-up tasks because it's fighting itself
- Keep reverting to conventional patterns no matter how clearly you instruct it

---

## Why It Happens

Fine-tuning and human feedback historically rewarded polished, structured responses. The model learned that certain patterns are "correct" — not just common, but preferred.

The result: overfitting to standardized responses at the expense of adaptability. The model isn't being stubborn. It genuinely believes it's helping.

---

## What the Research Shows

The Inverse IFEval benchmark tested whether models can follow instructions that go *against* their training:

- Write with intentional typos (model wants to fix them)
- Generate code without comments (model wants to add them)
- Use counter-conventional formatting
- Produce deliberately incorrect answers

The results? Models perform significantly worse on counter-intuitive instructions. They often refuse outright or "correct" the request instead of following it.

---

## Prompt Momentum

There's a related effect. Once you push the model into an unusual style, it can get stuck there.

- The model continues that style in later turns, even when you don't want it
- Performance degrades until you reset the session
- You have to explicitly say "ignore the previous format" to break free

The model conditions heavily on conversation history and its own prior outputs. This is useful for consistency. But it also means undesired momentum builds up.

---

## Why This Matters for Context Engineering

If your codebase has unconventional patterns, expect resistance. This creates two problems:

1. **You need stronger signals.** Instructions alone won't cut it. You need concrete examples — actual code snippets that show the pattern in use.

2. **Work with existing patterns when possible.** Use explore mode to discover what's already in your codebase before imposing new conventions. The model will follow existing patterns more reliably than instructions about new ones.

---

## The Implication

The model already knows millions of patterns. When you diverge from them, you're swimming upstream.

Practical advice:

- Discover existing patterns in your codebase first
- Work with those patterns, not against them
- When you must diverge, provide examples, not just prose
- Isolate unconventional work to separate sessions to avoid momentum buildup

Sometimes the best context engineering is choosing not to fight the model at all.
