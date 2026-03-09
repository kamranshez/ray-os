---
status: to-film
---

## How I Think

I like to see the big picture before diving into details. This video gives you that big picture—the core idea of the entire course in ten minutes.

---

## The Premise

**Prompt engineering will only take you so far.**

You can rewrite your prompt a hundred times. Add more detail. Try all caps. Search online for "best Claude prompts." And still get mediocre results.

The bottleneck isn't your prompt. It's context.

**The right context takes you dramatically further.** When the model has the information it needs—the patterns, the constraints, the "why" behind your architecture—it produces good plans. And once the plan is good, the code is good.

![[images/01-context-engineering-in-10-minutes/premise.png]]

---

## What This Course Covers

We start with **fundamental ideas**—the constraints that explain why naive approaches fail:

- Why prompt tweaking has diminishing returns
- Why agentic search fills your context with noise before finding signal
- Why models drop rules when you give them too many instructions
- Why models fight your unconventional patterns

These aren't arbitrary limitations. They're fundamental to how attention works. Once you understand them, everything else clicks.

![[images/01-context-engineering-in-10-minutes/fundamentals.png]]

---

## The Context Layer

Then we introduce the solution: **a context layer** over your codebase.

The layer has three components:

- **Layer nodes** (CLAUDE.md, AGENTS.md) — Files that explain each area of your system. They load automatically when an agent works in that directory.
- **Skills** — Reusable capabilities that activate only when relevant. Framework patterns, complex workflows, domain knowledge.
- **Hooks** — Automation that triggers at specific points. Inject context, run validation, enforce standards.

Together, they capture what code alone cannot express:

- Architectural decisions and their rationale
- Historical constraints and tribal knowledge
- Patterns the model should follow
- Invariants that must never be violated
- Concrete examples that anchor behavior

The agent gets exactly the context it needs—nothing more, nothing less.

![[images/01-context-engineering-in-10-minutes/context-layer.png]]

---

## What It Looks Like

Here's the structure:

```
your-project/
├── CLAUDE.md              ← Always loaded (system overview)
├── services/
│   ├── CLAUDE.md          ← Loaded when working in services/
│   ├── payment/
│   │   └── CLAUDE.md      ← Loaded when working in payment/
│   └── billing/
│       └── CLAUDE.md      ← Loaded when working in billing/
└── frontend/
    └── CLAUDE.md          ← Loaded when working in frontend/
```

When an agent touches a file in `payment/`, it automatically loads:
1. The root CLAUDE.md (system overview)
2. The services CLAUDE.md (service patterns)
3. The payment CLAUDE.md (payment-specific context)

It doesn't load billing or frontend context. That's noise for this task.


![[images/01-context-engineering-in-10-minutes/hierarchy.png]]

---

## The Result

Your AI agents stop behaving like confused newcomers grepping through unfamiliar code.

They start behaving like **senior engineers who know where the bodies are buried**.

- They find relevant files on the first try
- They follow your patterns, not generic training defaults
- They respect constraints that aren't visible in the code
- They make fewer mistakes that require correction

The context layer is how you bridge the gap between what AI can do and what you're currently getting.


![[images/01-context-engineering-in-10-minutes/result.png]]

---

That's the big picture.

Let's get started.
