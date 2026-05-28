---
status: idea
---

**The pre-mortem prompt.** Before letting the model execute a plan, ask: *"assume this plan fails. What's the most likely reason?"*

The trick is that you're giving the model permission to find fault. By default, once the model has proposed a plan, it's locked into defending it. Sycophancy plus consistency bias means it won't volunteer the failure modes it can already see. Pre-mortem flips the frame: now its job is to find the crack, not protect the plan.

Works especially well right before a destructive action: migrations, deletes, refactors that touch many files. Ask for the pre-mortem, then decide.

The deeper move: bake it into the workflow so you never skip it. Plan, pre-mortem, then execute. Three steps, not two.
