---
status: filmed
---

Most agent failures aren't execution failures. The agent clicks the wrong button, gets lost in a loop, or forgets what it was doing three steps ago. The root cause is almost always the same: **planning and doing are tangled together in one context window**, and the context gets overwhelmed.

Plan-and-Act fixes this by splitting the agent into two roles: a **Planner** that thinks strategically and an **Executor** that does the grunt work. The Planner never touches a button. The Executor never decides strategy. They communicate through a narrow interface — short task specs, not raw tool output.

![[images/high-level-strategy-low-level-details.png]]

---

## Why one agent can't do both

When a single agent plans _and_ acts, its context fills up with low-level noise — HTML dumps, click confirmations, error traces, DOM snapshots. By step 15 of a 30-step task, the original goal is buried under pages of execution debris. The agent starts making decisions based on whatever's most recent in context, not what actually matters.

This is the **context explosion problem**. The more actions you take, the worse your planning gets. The more you plan inline, the less room you have for action context. It's a zero-sum fight for the same window.

Separating the two roles means neither has to compromise. The Planner keeps a clean, short context: goal, constraints, current plan, what's been accomplished. The Executor gets a messy, disposable context: raw page content, tool outputs, retry logs. When the Executor finishes a step, it sends back a one-line summary. The mess stays contained.