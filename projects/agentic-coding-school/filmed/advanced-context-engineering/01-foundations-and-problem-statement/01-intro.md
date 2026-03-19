---
status: filmed
---

## Sources
- https://www.intent-systems.com/learn/ai-adoption-roadmap
	- https://archive.md/YwXpO
- https://www.youtube.com/watch?v=DW4a1Cm8nG4

---

## The Gap

You've probably seen it online: someone using the exact same model as you, solving complex engineering problems in their codebase. Huge refactors. Debugging obscure issues. One-shotting features end-to-end.

And you're wondering — why can't I do that?

You're using the same model. You're giving it reasonable prompts. But the results aren't even close.

---

## The Capability Is Already There

Here's what most people don't realize: with recent models like Opus 4.5 and GPT-5.2, the capability is already there. These models can reason through complex problems, understand intricate codebases, and produce production-quality code.

The bottleneck isn't intelligence. It's context.

The only thing preventing you from tapping into that capability is whether the model has the right information when it needs to make a decision.

---

## What This Class Will Teach You

This class is about context engineering — the skill of curating what information an AI model sees when working on a task.

By the end, you'll know how to make AI work reliably on *your* codebase. Not toy examples. Not greenfield projects. Your actual code, with all its history, quirks, and constraints.

You'll understand why some approaches fail and others succeed. And you'll have a systematic way to set up any codebase for effective AI collaboration.

---

## The Core Thesis

The creator of Claude Code put it simply: once the plan is good, the code is good.
- https://youtu.be/DW4a1Cm8nG4?t=1881

Current models are so capable that if the plan is solid, the implementation will be solid too.

The question becomes: **what prevents a plan from being good?**

1. **Missed critical context.** The agent followed a path through your codebase but missed something important.
2. **Confusing patterns.** It didn't understand part of your codebase due to unconventional structure.
3. **Unknown constraints.** It didn't know about a requirement you had in place.

All three come down to the same thing: the model didn't have the right context.

---

## The Junior vs Senior Engineer

Think about the difference between onboarding a junior engineer versus a senior engineer.

When you bring a junior onto a new team, you give them small, scoped tasks. Edit this one file. Fix this one bug. You wouldn't hand them an ambiguous, multi-system problem on day one.

But a senior engineer? You can give them large, ambiguous tasks. They'll figure out what files to touch, what patterns to follow, what constraints to respect. They've accumulated context over years of working with the codebase and the team.

We want our AI agents to behave like senior engineers. And the way we do that is by giving them the context that a senior engineer would have.

---

## Why Foundations Matter

Before we show you solutions, you need to understand why this is hard.

If you don't understand the underlying constraints, the techniques will feel arbitrary. You'll apply them mechanically without knowing when to adapt.

This chapter covers fundamental limitations that explain why naive approaches fail:
- Why the model can't just search for what it needs
- Why you can't just write more instructions
- Why the model fights your unconventional patterns

Once you understand these, the solutions will click.
