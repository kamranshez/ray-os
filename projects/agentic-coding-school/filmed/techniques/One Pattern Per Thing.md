---
status: filmed
---

Agents don't have taste. If your codebase has two ways to do the same thing — two error handling styles, two data-fetching patterns, two component structures — the agent picks whichever it encounters first, or invents a third.

This is the "gravitational pull" effect. Early code (often written by weaker models or under time pressure) becomes the template for everything that follows, even when better patterns exist elsewhere in the same repo. The agent doesn't evaluate which pattern is better. It just copies the first one it sees.

![[images/gravitational-pull.png]]

---

## Two patterns means the agent is fighting itself

If your CLAUDE.md says "use Result types for error handling" but half the codebase uses try/catch, the agent is getting contradictory signals. It hedges, mixes approaches, or just ignores the instruction entirely — because the code is a stronger signal than the doc.

This kills predictability. Run the agent 5 times on a consistent codebase and you get 5 similar results. Run it 5 times on an inconsistent one and you get 5 different approaches. You end up reviewing every line manually, which defeats the purpose.

![[images/agent-fighting-itself.png]]

---

## Find where it hurts

You don't need to audit everything at once. Start with the area where the agent misbehaves most. If it keeps generating inconsistent API handlers, that's your first target. If it mixes component patterns, start there.

Spawn an Explore subagent with a "why" that frames the problem:

> "Using many explore subagents, find conflicting patterns (eg, data fetching, error handling, rate limiting) in this codebase and save them into a markdown file with locations, because it'd be better to consolidate inconsistent patterns to improve your reliability."

The "why" filters results. "Find data fetching patterns" returns everything. Adding "because it'd be better to consolidate inconsistent patterns" focuses the subagent on surfacing the conflicts — where two patterns exist for the same job, which files use which, and what the differences actually are.

![[images/find-where-it-hurts.png]]

## Pick the winner and build a task list

Once you know the competing patterns, pick which one wins. Then have the agent generate a task list of every file in the codebase that uses the losing pattern. This is your migration backlog.

You don't need to refactor everything in one session. The task list gives you a concrete, file-by-file list you can work through over time. Each file you migrate is one fewer place the agent can copy the wrong pattern from.

![[images/pick-winner-build-task-list.png]]

## Let the code be the documentation

Here's the key: once the losing pattern is gone from the code, you don't need to document the winning pattern in your CLAUDE.md. The agent is biased toward whatever code it sees. If every file in the codebase uses the same approach, the agent will follow it without being told. The code _is_ the instruction.

You only need a CLAUDE.md line if you can't fully eliminate the losing pattern yet (e.g. a third-party dependency forces a different style in one module). In that case, a single constraint line bridges the gap until you can finish the migration.

![[images/code-is-the-documentation.png]]

Each file you clean up makes every future agent run more predictable. The codebase converges, and the agent converges with it. Consistency is a form of constraint, and constraints make agents predictable.
