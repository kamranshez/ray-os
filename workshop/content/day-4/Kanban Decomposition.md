Sibling to [[Implementing Plans in Phases]]. Same question — *how do you slice a PRD?* — different answer for a different mode of work.

## Phases vs Kanban

- **Phases** — sequential, blocking, one big plan. Phase 2 starts when Phase 1 ends. Optimised for human-in-the-loop, where you want a clear narrative and one thing happening at a time.
- **Kanban** — independent vertical slices, parallelisable, any agent can grab the next ticket. Optimised for AFK and multi-agent work, where blocking dependencies kill throughput.

The shape of the work changes the shape of the plan. Don't force phases onto work that wants to be a board, and don't force a board onto work that has real ordering.

## What "vertical slice" means here

Each kanban ticket is a thin, end-to-end change that can ship independently:

- Touches the layers it needs (UI → API → DB) rather than "do all the DB first, then all the API."
- Is reviewable on its own. No "this only makes sense alongside ticket #7."
- Has its own acceptance criteria. The agent knows when it's done without reading the rest of the board.

A good kanban ticket is one a fresh agent could pick up cold. Bad tickets read like "Phase 2, Step 3" — they assume the rest of the plan in your head.

## When to pick which

- **Phases** when the work has real sequential dependencies, when you're driving it yourself, or when one wrong early decision invalidates later steps.
- **Kanban** when slices are genuinely independent, when you want to run agents in parallel, or when you'll be picking up tickets AFK and don't want to remember where you left off.

Most non-trivial features end up hybrid: a phased spine for the load-bearing decisions, a kanban board for the independent slices that follow.

## Where this sits in Day 4

Day 4 is planning. By this point students have PRDs and phases. Kanban is the second decomposition tool — the one that pays off later in the workshop when Day 8 (automation) and Day 9 (Ralph) need work units an agent can pull from a queue. The Ralph lessons can then *use* a kanban board as the backlog without having to teach the concept from scratch.
