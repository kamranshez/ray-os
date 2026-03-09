---
status: to-film
---

## Sources

- https://amplitude.com/blog/context-engineering
- https://www.linkedin.com/pulse/prompt-engineering-vs-context-reasoning-neeraj-kumar-singh-b
- https://waleedk.medium.com/give-claude-code-context-one-principle-many-implications
- https://www.anthropic.com/research/effective-context-engineering-for-ai-agents

---

## The Prompting Trap

You've probably done this. The model gives you a bad result, so you rewrite your prompt. Maybe you search online for "best Claude Code prompts." You add more detail. You try all caps. You rephrase the same instruction five different ways.

It still doesn't work.

So you keep tweaking. Convinced you're one clever phrase away from unlocking the model's potential.

This is the prompting trap.

![[images/02-the-prompt-isn-t-the-problem/prompting-trap.png]]

---

## Most Teams Overestimate What Prompt Engineering Can Do

Here's what the research shows: prompt engineering has diminishing returns.

Source: https://amplitude.com/blog/context-engineering

> "Most teams overestimate what prompt engineering can do. They tweak instructions, reformulate sentences, and write in all caps hoping that the model will suddenly become smarter. If your team has written and rewritten your prompt to the point of diminishing returns, you know what I mean."

Once you've got clear instructions and sufficient detail, additional prompt tweaking rarely moves the needle. If your system still fails after solid prompt work, the problem is almost never "I need a better prompt."

**It's usually that the model doesn't have the right information.**

![[images/02-the-prompt-isn-t-the-problem/diminishing-returns.png]]

---

## A Perfect Prompt Can't Fix Bad Context

This is the core insight: **prompts guide reasoning, but context ensures truth.**

Source: https://www.reddit.com/r/ClaudeAI/comments/prompt_engineering_vs_context_engineering

Think of it like pair programming. Your prompt is how you *talk* to your copilot. But context is what you *let it read.*

If you hide half the codebase from your pair programmer, they'll make wrong assumptions — no matter how clearly you explain the task. Conversely, giving them the right files and background means they can produce correct code even if your request is fairly simple.

The same applies to AI. You can craft the most elegant prompt in the world, and it will still produce wrong code if it can't see the relevant context.

This is fundamentally a signal-to-noise problem. We'll explore this deeper in [[03 - Signal to Noise]], but the short version: **you only get the behavior you load.** If the model doesn't see your patterns, it falls back to generic training defaults.

![[images/02-the-prompt-isn-t-the-problem/context-vs-prompt.png]]

---

## What the Prompt Actually Does

Your prompt doesn't directly produce the code. It produces the *plan.*

This is the key mental model:

**Prompt → Plan → Code**

If the plan is good, the code will be good. Current models are capable enough that solid plans lead to solid implementations.

Source: https://youtu.be/DW4a1Cm8nG4?t=1881 (Claude Code creator)

So when you're evaluating a prompt, don't ask: "Is this prompt perfect?"

Ask: **"Will this prompt lead to a good plan?"**

![[images/02-the-prompt-isn-t-the-problem/prompt-plan-code.png]]

---

## The Handful of Prompts That Actually Matter

Yes, there are a few prompting choices that have outsized impact:

1. **Keywords.** The right keywords help the model find the right files. If your codebase uses specific terminology — "workflow engine," "payment processor," "auth middleware" — use those terms in your prompt. They're search signals.

2. **Scope boundaries.** Tell the model what's in scope and what isn't. "Focus on the API layer, don't touch the database schema." This prevents wasted exploration.

3. **Constraints.** Hard requirements the model can't infer from code. "Don't break backwards compatibility." "This must work offline." These belong in the prompt because they won't show up in a grep search.

4. **Success criteria.** What does "done" look like? "The tests should pass." "The type errors should resolve." This gives the model a target to plan toward.

Beyond these? A "good enough" prompt with sufficient detail is satisfactory.

Why not just add more instructions to cover every edge case? Because models have hard limits on how many instructions they can follow simultaneously. Research shows even frontier models start dropping rules around 150 instructions. We'll cover this in [[05 - Instruction Following Limits]] — but the implication is clear: you can't brute-force your way to reliability with more rules.

![[images/02-the-prompt-isn-t-the-problem/keywords-that-matter.png]]

---

## The Right Question to Ask

Before you submit a prompt, ask yourself:

**"Does this prompt contain enough detail for Claude to explore the codebase effectively and find the right context?"**

If yes, the prompt is good enough. Ship it.

If no, add the missing detail. But don't wordsmith what's already there.

The leverage isn't in phrasing. It's in information.



![[images/02-the-prompt-isn-t-the-problem/right-question.png]]

---

## The Shift in Mindset

Stop thinking of prompting as an art of persuasion. It's not about finding magic words that unlock model intelligence.

Think of it as scoping a task for a new team member. You're not trying to trick them into doing good work. You're trying to give them enough context to succeed.

What files matter? What patterns should they follow? What constraints exist? What does success look like?

Answer those questions in your prompt, then trust the model to explore and plan.

![[images/02-the-prompt-isn-t-the-problem/shift-in-mindset.png]]

---

## When to Stop Tweaking

If your plan is bad, ask: **Is this a prompt problem or a context problem?**

Prompt problem signs:
- The model misunderstood what you wanted
- It's solving the wrong problem entirely
- Basic instructions weren't followed

Context problem signs:
- The model's approach is reasonable but uses wrong files
- It missed a critical dependency or pattern
- It made assumptions that contradict your architecture
- It "corrected" your unconventional approach back to standard patterns

These failures have root causes we'll examine: why search alone can't reliably find what it needs ([[04 - Why Search Isn't Enough]]), and why models resist your non-standard patterns even when instructed ([[06 - Cognitive Inertia]]).

If it's a context problem, no amount of prompt rewriting will fix it. You need to fix the context layer — what information is available and discoverable when the model goes exploring.

That's what the rest of this course is about.

![[images/02-the-prompt-isn-t-the-problem/prompt-vs-context-problems.png]]

---

## The Bottom Line

Prompt engineering matters, but it hits a ceiling fast.

Once you've included clear instructions, the right keywords, scope boundaries, constraints, and success criteria — you're done. Further tweaking is wasted effort.

If the results are still bad, look at the context. What is the model seeing? What is it missing? What can't it find?

**The prompt points the model in a direction. The context determines what it finds when it gets there.**

![[images/02-the-prompt-isn-t-the-problem/bottom-line.png]]
