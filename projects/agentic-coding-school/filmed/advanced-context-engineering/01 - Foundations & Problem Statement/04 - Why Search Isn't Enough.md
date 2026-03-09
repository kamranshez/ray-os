---
status: filmed
---

## Source

- https://www.intent-systems.com/learn/context-is-your-constraint#agentic-search

---

## The Promise of Agentic Search

Modern AI agents can search your codebase. They grep for keywords, read files, follow imports, and explore until they find what they need.

In theory, this should solve the context problem. Let the agent find what it needs.

In practice, it doesn't work reliably.

---

## How Search Adds Noise

Every exploration step adds tokens. And most exploration steps don't find signal — they find noise.

**Examples of noise from search:**

- Random files from grepping a keyword that appears everywhere
- Outdated documentation that contradicts current code
- Verbose comments that restate what code already says
- Test fixtures and mock data unrelated to the task
- Dead ends that seemed promising but weren't

By the time the agent finds what it actually needs, the context window is polluted. The signal is buried.

---

## Scale Makes It Worse

The larger your codebase, the worse this gets.

In a small codebase, the agent can explore thoroughly and usually finds the relevant code. But even then, it misses things that aren't in the code — architectural decisions, historical context, the "why" behind patterns.

In a large codebase, complete exploration is impossible. The agent will miss critical files. It has no concept of enforcement boundaries or "what must never happen." The search becomes a slot machine — maybe it finds the right files, maybe it doesn't.

---

## What About Explore Agents?

Explore agents (like Claude Code's subagents) do help. They run in a separate context window and return only a summary, filtering out the noise.

But they have their own limitations:

- **Too little context:** The explore agent may not gather enough to establish all the patterns required.
- **Gathers too much information**: Subagents also have a context window and they have to identify the signal too. If they fill up the context window because the codebase is so big, they lose it.
- **Missing information:** There's context that isn't in the codebase at all — architectural decisions, tribal knowledge, historical constraints
- **Wrong information:** The agent may fetch the wrong files if naming conventions are misleading or architecture isn't obvious.
- **Summarization loss:** When the subagent summarizes, nuance gets lost

Explore agents are better than raw search, but they're still searching blind. They don't know what they don't know.

---

## The Core Limitation

The fundamental problem isn't the tools. It's that **code doesn't capture intent, history, or tribal knowledge.**

**Example:** Your database has a `users` table with a column called `legacy_id`. It's nullable. No foreign keys reference it. It's not used anywhere in the current codebase.

To an agent, this looks like dead code. Safe to remove in a cleanup refactor.

But here's what the code doesn't show: Partner X's integration depends on that column through an undocumented API. Dropping it breaks a $2M/year contract.

That constraint isn't in the code. It's in a Slack thread from 2022 and the head of partnerships' memory. Until you externalize it, the agent will never know.

---

## Implication

Search isn't useless. It's just not enough on its own.

The agent will still explore your codebase. That's fine. But you can guide where it looks and what it prioritizes. You can tell it which files matter, which patterns to follow, which constraints exist.

Think of it this way: search is the agent fumbling in the dark. Context engineering is handing it a map.

The map doesn't replace exploration — but it makes exploration dramatically more effective. The agent spends less time on dead ends and more time on signal.

This is what we'll build: a context layer that lives alongside your code and captures what the code alone cannot express.
