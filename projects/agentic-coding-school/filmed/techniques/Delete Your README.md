---
status: filmed
---

The core problem with a README.md isn't that it goes stale (though it does). It's that it creates **multiple sources of truth** in your project.

You already have a CLAUDE.md that tells the agent how your project works — conventions, patterns, commands, boundaries. And you have the code itself. The README is a third voice saying potentially different things. When the agent lands in your repo, it reads all of them, and now it has to reconcile conflicting information. The CLAUDE.md says one thing, the README says another, the code says a third. The agent can't tell which one is current.

![[images/multiple-sources-of-truth/excalidraw_1.png]]

---
## The multiple sources of truth problem

A README describes the project. A CLAUDE.md describes the project. The code _is_ the project. That's three sources of truth for the same information, and they drift at different rates.

Your CLAUDE.md stays relatively fresh because you feel the pain when it's wrong — the agent misbehaves, you fix the instruction, behaviour improves. There's a feedback loop. The code is always current by definition — it's the thing that actually runs.

The README has no feedback loop. Nobody notices when it's wrong because nobody depends on it for anything that breaks visibly. It just sits there, confidently describing a version of the project that no longer exists, and the agent reads it first because it's at the root.

The more sources of truth you have, the more the agent hedges. It doesn't know which document to trust, so it tries to satisfy all of them, or picks one at random. This is the same problem as having two patterns for the same thing in your code — see [[One Pattern Per Thing]].

![[images/readme-has-no-feedback-loop/excalidraw_1.png]]

---
## The fix: delete it, generate on demand

Delete the README. When you need documentation — for a new teammate, for yourself, for any reason — spawn an Explore subagent pointed at the actual codebase and ask it to summarise whatever you need.

The subagent reads the real imports, the real config files, the real directory structure. It gives you what actually exists right now. The cost of generating is trivial — a few seconds. The cost of acting on stale context is hours of debugging the wrong thing.

This is the principle of **just-in-time context**: don't pre-load stale information, generate fresh context at the moment you need it. One source of truth (the code), one set of constraints (the CLAUDE.md), nothing else competing for the agent's attention.

![[images/just-in-time-context/excalidraw_7.png]]