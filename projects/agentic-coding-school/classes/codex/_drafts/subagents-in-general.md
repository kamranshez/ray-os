---
duration: "10-12 min"
order: 4
class: "codex"
chapter: "Codex App"
status: "to-film"
tags: [course, script, codex, codex-app, subagents, parallel-agents]
lesson: "Subagents In General"
---
## The three agent types

Codex ships with three agent types out of the box. `default`, `explorer`, and `worker`. They are passed as the `agent_type` parameter when the main thread calls `spawn_agent`.

Use `default` for a generic delegated task. No specialization. It runs as a normal Codex side thread with the same general kind of capabilities as the parent thread. This is the right pick when you just want a side thread to handle something while you keep moving, and the task does not fit cleanly into "investigate" or "implement".

Use `explorer` when you need an answer before you edit. The role description in the codex source is literally "Use `explorer` for specific codebase questions. Explorers are fast and authoritative." This is your read-only investigator. Where is the password reset email generated. What does the auth flow look like. Which files import this helper. The discipline with explorers is to keep them narrow, run several in parallel for independent questions, and reuse existing explorers instead of spawning new ones for related follow-ups.

Use `worker` when the implementation is cleanly scoped and you can hand off ownership. A worker writes code. The codex guidance is explicit: clearly specify which files or modules the worker is responsible for, and tell it that other agents may be working in parallel so it does not revert their edits.

> IMG · three-agent-types.png

![[images/04-subagents-in-general/three-agent-types.png]]

---

## The parameters Codex sets

When the main thread calls `spawn_agent`, it fills in a handful of parameters that matter. Knowing what each does in practice is the difference between a useful subagent and a wasted one.

`agent_type`. The role. `default`, `explorer`, or `worker`. This is the first thing Codex picks, and it should match the shape of the task.

`message` or `items`. The task itself. `message` is plain text. `items` lets Codex pass structured input like file mentions or images. Whatever the subagent needs to know, it goes here, because once the agent starts running it cannot read your mind.

`fork_context`. This is the most important flag in the whole tool. When `fork_context` is true, the new agent starts with a copy of the parent thread's history. When it is false, the agent starts clean and only sees the `message` you gave it.

`model`. Optional override. Usually unset. Codex inherits the parent model unless the user specifically asks for a different one or the task clearly demands it.

`reasoning_effort`. Optional override. Same idea. You bump it up for harder side missions, leave it alone for routine ones.

Some Codex builds may expose extra fields, but do not build your mental model around them. The durable concepts are the role, the task, whether context is forked, and whether the model or reasoning effort is overridden.

> IMG · parameters.png

![[images/04-subagents-in-general/parameters.png]]

---

## Behind the scenes

Here is the practical version of what happens when `spawn_agent` runs. The source implementation can move around, but the flow is the same enough to reason about.

The handler reads your arguments, checks the depth limit so subagents cannot infinitely spawn more subagents, then calls into `agent_control.spawn_agent_with_metadata`. That function creates a fresh thread, attaches the role config, and starts the model running.

The branch that matters is `fork_context`. If you set it to true, the new thread gets a copy of the parent's conversation, decisions, and tool results. If you are forking the full history, you are saying "this agent is a continuation", so you should usually leave the model and reasoning effort alone unless you have a clear reason to override them.

If `fork_context` is false, the agent starts cold. Only your `message` and `items` are visible to it. This is the cleanest path for most side missions, because the subagent sees only the task you intentionally gave it.

What about the role itself. Look at `codex-rs/core/src/agent/role.rs`. Each role has a description string and an optional embedded TOML config loaded with `include_str!`. Today the explorer and worker built-in TOMLs are essentially empty, which means there is no hard tool allowlist or sandbox lockdown that physically prevents an explorer from writing files. The role is mostly a behavioral contract. The role description goes into the system prompt. The main thread is told, in its own instructions, that explorers should be treated as read-only and workers should be given file ownership.

That is worth saying out loud. The "read-only" nature of an explorer is enforced by prompt and convention, not by a sandbox flag. Codex trusts the orchestration layer to send explorers questions and send workers tasks. If you ask an explorer to write code, it will probably try.

Results come back to the main thread with the spawned thread id, a nickname when available, and the agent's final status. The main thread reads that result, decides what to do with the answer, and either keeps coordinating or spawns the next agent.

> IMG · spawn-agent-flow.png

![[images/04-subagents-in-general/spawn-agent-flow.png]]

---

## Coordination discipline

This is where most people break their subagent setup.

The main thread is the coordinator. Always. Subagents investigate. Subagents implement. They do not decide. They do not own the outcome. The main thread reads the results, picks what to trust, picks what to discard, and explains the final answer to the user.

There is one more practical constraint. In current Codex behavior, the model should spawn subagents only when the user explicitly asks for subagents, delegation, or parallel agent work. If the user simply asks for a fix, Codex should usually do the work in the main thread. If the user says "use subagents", "delegate this", or "run parallel agents", now the orchestration pattern in this lesson applies.

The clean pattern looks like this.

1. Split the work into clear sub-tasks before you spawn anything.
2. Give each subagent the exact context it needs, no more.
3. Keep ownership boundaries separate. Two workers should never share files.
4. Review every result in the main thread before integrating.
5. Throw away the parts you do not trust.

If you skip step 1, the rest collapses. Spawning an agent on a fuzzy task is how you get a confident, beautifully-formatted, completely wrong answer back five minutes later.

> IMG · coordination-discipline.png

![[images/04-subagents-in-general/coordination-discipline.png]]

---

## Good usage

Use an explorer when you need a specific answer before editing.

> Inspect the auth flow and tell me where password reset emails are generated. Do not edit any files. Return the exact file paths and line numbers.

Use a worker when the implementation is cleanly scoped.

> Update the settings panel copy in `src/settings/` only. Do not touch any other directory. Other workers may be editing the API layer in parallel, so do not revert their changes.

Use multiple agents when the work is genuinely parallel.

> We're adding a "saved filters" feature. Spawn one worker to add the API endpoint in `src/api/filters/` only. Spawn a second worker to add the settings UI in `src/components/filters/` only. Neither touches the other's directory. The main thread reviews both diffs before merging.

Each of these has the three things subagents need. A bounded task. A clear ownership line. And a reason the main thread cannot just do it inline.

> IMG · good-usage.png

![[images/04-subagents-in-general/good-usage.png]]

---

## Bad usage

Do not spawn a subagent because the task is important. Importance is not a reason to delegate. Bounded scope is.

Do not delegate the immediate blocker. If your main thread cannot move until that result comes back, you are not delegating. You are blocking yourself with extra steps. Just do it inline.

Do not give two workers overlapping file ownership. Codex does not lock files between agents. You will get merge pain and lost edits, and the main thread will have to clean it up.

Do not fork context when the side mission does not need the conversation. A fresh thread with a tight `message` runs faster, costs less, and produces cleaner output than a forked thread that drags the whole parent history along for no reason.

> IMG · good-vs-bad.png

![[images/04-subagents-in-general/good-vs-bad.png]]
