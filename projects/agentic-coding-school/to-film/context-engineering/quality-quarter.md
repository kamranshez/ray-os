---
class: "context-engineering"
chapter: "Advanced Techniques"
---

## The Thesis

Before you scale agents across a large codebase, you stop shipping features for a quarter and you clean.

That sentence will sound insane to most engineering managers. Three months without new features. No roadmap progress. No customer-facing wins. Just deletion, simplification, and the removal of things nobody is brave enough to remove.

This is the move Sentry made before going all in on AI. And it's the move you have to make too, because the codebase is the prompt. Whatever is in there gets fed to the agent. If it's full of dead flags, half-removed features, and "TODO fix this later" notes from 2019, that's what your agent is reasoning over.

You cannot prompt-engineer your way out of a messy codebase.

[IMAGE: dark chalkboard, two columns labeled "Before" and "After". Before column shows tangled wires labeled "any types, dead flags, stale TODOs, ghost components". After column shows clean parallel lines labeled "one pattern, named modes, current docs"]

![[images/quality-quarter/before-after.png]]

---

## The Problem

Sentry is fifteen years old. Around 400 engineers. About 100 pull requests merged every day. Roughly 100,000 organizations depend on the codebase functioning. If you go on vacation for two weeks, you come back to a different codebase than the one you left.

That's the environment Priscila Andre de Oliveira described in her AI Engineer talk. And in that environment, they did something most teams would never approve. They paused. Three months. No new features. The whole quarter went to:

- Removing every `any` type from TypeScript
- Killing dead feature flags that had outlived their purpose
- Deleting TODOs that had been there for years
- Removing components that had been "soft deprecated" but never actually removed
- Simplifying the patterns that had drifted across the codebase

They called it the **quality quarter**.

And only after that, they went all in on AI agents.

Most teams do this in the opposite order. They drop agents into a messy codebase, watch the agents produce slop, and conclude that agents are not ready. The agents are ready. The codebase is not.

---

## The Core Insight

Quality quarter is not a single-session cleanup. It is not a refactor sprint. It is a **scheduled ritual** that you do once, deliberately, before you trust agents with anything important.

The mechanics are not new. You already know how to delete a dead flag. You already know how to remove an `any` type. There are other videos in this class about [[asking-for-options]], [[reducing-agent-confusion]], and the [[one-pattern-rule]]. The mechanics are the easy part.

The hard part is the **decision to stop shipping for a quarter**. That is a strategic call, not a technical one. It requires telling your CEO that for three months, the only thing your team is producing is a smaller, cleaner codebase. No new revenue, no new features, no roadmap movement.

You make that call once. You do it before you scale agents. And you treat it the same way you would treat a security audit before going public. Non-negotiable, scheduled, blocking.

[IMAGE: a calendar with one quarter highlighted in red, labeled "Quality Quarter". The rest of the year is labeled "Feature work, but now with agents"]

![[images/quality-quarter/calendar.png]]

---

## What Actually Goes Away

When Priscila described the quarter, the items she listed were not glamorous:

- `any` types in TypeScript. Every one. No exceptions for "we'll fix it later."
- Dead feature flags. If the flag is permanently on or permanently off, the flag is dead. Remove the flag and inline the code.
- Old TODOs. If a TODO has survived more than six months, it is not a TODO. It is a load-bearing comment about a problem nobody is going to fix. Either fix it or delete it.
- Deprecated components that still have references. Either finish the deprecation or back it out.
- Lint rules that have been disabled with no comment explaining why.
- Tests that are skipped with no ticket attached.

None of this is exciting. None of it shows up in a demo. But every one of these is a piece of noise that your agent will inherit the moment you put it to work.

> The codebase is the prompt. Whatever is in there gets fed to the agent.

A flag that has been on for three years is a piece of context the agent has to reason about every time it touches that file. An `any` type is a sign the agent will read as "the types here are not trustworthy, do whatever." A TODO is a small unresolved thread that the agent will sometimes try to pull on and get distracted by.

You are not cleaning for humans. You are cleaning for the next ten thousand agent runs.

---

## Why Incremental Cleanup Fails

The objection is obvious. "Why a whole quarter? Can't we just clean as we go?"

Here is why incremental cleanup fails.

When you clean as you go, you clean only the files you touch. The files you do not touch stay dirty forever. And the files you do not touch are the majority of the codebase. So six months in, your codebase is still mostly dirty, but you have convinced yourself it is getting better because the parts you see are clean.

The agent does not see only the parts you see. The agent grep through everything. It reads files you have not opened in two years. It builds its mental model from the whole repo, not the parts you happen to be working in. So the agent inherits the messy 80%, not the clean 20%.

A quality quarter forces you to look at the whole thing. The directories nobody owns. The features marketing forgot existed. The libraries the founder wrote in 2011 that everyone is afraid to touch. You go through it. You remove what is dead. You document what is alive. And then you let the agent in.

---

## The Armin Ronacher Loop

Armin Ronacher, the creator of Flask and a former Sentry engineer, wrote this in his blog:

> When more and more people tell me they no longer know what code is in their own codebase, I feel like something is very wrong here.

This is the trap a quality quarter exists to prevent.

Without one, the codebase grows faster than any single human can track. Agents accelerate that, because agents will happily add files, rename functions, and introduce new patterns at a pace no human review can keep up with. Within a year, nobody on the team can tell you what is actually in there. The codebase becomes a black box even to its authors.

A quality quarter is the moment you reassert ownership. You go through the whole thing one more time as a team that still understands it. You remove what nobody can defend. And then you let the agents in, with the codebase in a shape you actually know.

If you skip this, you do not get to know your codebase again. The agents will only ever add. You will only ever forget.

---

## Demo

This is a one-week, single-engineer version of the quality quarter you can run today to feel the shape of it before pitching the real thing.

1. **Pick one directory.** Not the whole repo. A single directory you know well.
2. **Run a "what is dead here" prompt.** Ask Claude to grep for every flag reference, every TODO, every `any` type, every `@deprecated` annotation in that directory. Have it list each one with file and line.
3. **Triage in batches.** For each item, three buckets: delete, fix now, document as load-bearing.
4. **Delete the delete bucket.** No discussion. One PR per category.
5. **Re-run [[catch-me-up]] on the same directory.** Notice how much shorter and sharper the model's summary is now.
6. **Now scale.** If a single directory in a week produced this much signal, what does a quarter across the whole repo produce?

The demo is not the cleanup. The demo is the **before and after** of asking the agent to explain the directory. You film the model's response on day one. You film the model's response after the cleanup. The difference is the case for the quarter.

---

## Key Insight

> The codebase is the prompt. If you would not paste it into a chat window, you should not let an agent loose on it. A quality quarter is the one-time, scheduled investment that turns your repo from a noisy context into a clean one. Skip it and your agents inherit every shortcut your team has taken since 2011.

---

## Closing

You do not get to skip the cleanup. You can do it once, deliberately, as a quarter, before you scale agents. Or you can do it forever, in small panicked patches, every time the agents ship something stupid because they inherited a flag from 2018.

The first option is cheaper.

**See also:** [[catch-me-up]] only works well on a codebase that has been through this. [[self-instrumentation]] will tell you when your agents are actually struggling with codebase noise versus prompt noise.
