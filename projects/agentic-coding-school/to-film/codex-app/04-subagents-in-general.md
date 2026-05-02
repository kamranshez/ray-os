---
duration: "10-12 min"
order: 4
class: "codex-app"
chapter: "Codex App"
status: "to-film"
tags: [course, script, codex, codex-app, subagents, parallel-agents]
lesson: "Subagents In General"
---
Subagents in Codex are not magic extra brains. They are a way for the main thread to delegate a bounded piece of work, get a result back, and keep going.

If you take one thing from this video, take this. Subagents are delegation, not decoration. You use them when the work splits cleanly. You do not use them because the task feels important.

[IMAGE: chalkboard. main thread in the center as a brain. three smaller brains branching off labeled default, explorer, worker. arrows return back to center labeled "result"]

![[images/04-subagents-in-general/the-mental-model.png]]

---

## The tool is `spawn_agent`

Every subagent in Codex starts the same way. The model calls a tool named `spawn_agent`. That tool is defined in the codex source at `codex-rs/tools/src/agent_tool.rs`. It exists in two versions, v1 and v2, but the shape is the same.

You hand it a task. You pick a role. You decide whether the new agent inherits your conversation history. Codex spins up a new thread, runs the model on that task, and hands the result back to you.

The description Codex gives the model in v1 is exactly this: "Spawn a sub-agent for a well-scoped task." That phrase is the whole game. Well-scoped. If you cannot describe the side mission in one or two sentences, you are not ready to spawn an agent. You are ready to think more.

---

## The three agent types

Codex ships with three agent types out of the box. `default`, `explorer`, and `worker`. They are passed as the `agent_type` parameter when the main thread calls `spawn_agent`.

Use `default` for a generic delegated task. No specialization. The agent gets the same tools you have. This is the right pick when you just want a side thread to handle something while you keep moving, and the task does not fit cleanly into "investigate" or "implement".

Use `explorer` when you need an answer before you edit. The role description in the codex source is literally "Use `explorer` for specific codebase questions. Explorers are fast and authoritative." This is your read-only investigator. Where is the password reset email generated. What does the auth flow look like. Which files import this helper. The discipline with explorers is to keep them narrow, run several in parallel for independent questions, and reuse existing explorers instead of spawning new ones for related follow-ups.

Use `worker` when the implementation is cleanly scoped and you can hand off ownership. A worker writes code. The codex guidance is explicit: clearly specify which files or modules the worker is responsible for, and tell it that other agents may be working in parallel so it does not revert their edits.

[IMAGE: three columns, dark background. column 1 "default" with a generic agent icon. column 2 "explorer" with a magnifying glass and a "read only" tag. column 3 "worker" with a wrench and a "owns: src/auth/" tag]

![[images/04-subagents-in-general/three-agent-types.png]]

---

## The parameters Codex sets

When the main thread calls `spawn_agent`, it fills in five parameters that matter. Knowing what each does in practice is the difference between a useful subagent and a wasted one.

`agent_type`. The role. `default`, `explorer`, or `worker`. This is the first thing Codex picks, and it should match the shape of the task.

`message` or `items`. The task itself. `message` is plain text. `items` lets Codex pass structured input like file mentions or images. Whatever the subagent needs to know, it goes here, because once the agent starts running it cannot read your mind.

`fork_context`. This is the most important flag in the whole tool. When `fork_context` is true, the new agent starts with a copy of the parent thread's history. When it is false, the agent starts clean and only sees the `message` you gave it.

`model`. Optional override. Usually unset. Codex inherits the parent model unless the user specifically asks for a different one or the task clearly demands it.

`reasoning_effort`. Optional override. Same idea. You bump it up for harder side missions, leave it alone for routine ones.

In v2 of the tool there are two extra parameters. `task_name`, a short identifier the user sees. And `fork_turns`, which lets you fork only the last N turns of history instead of the whole thread. That last one is useful when the parent conversation is long and most of it is irrelevant to the side mission.

---

## Behind the scenes

Here is what actually happens when `spawn_agent` runs. This is not lore. It is in the codex source under `codex-rs/core/src/tools/handlers/multi_agents/spawn.rs` and `codex-rs/core/src/agent/control.rs`.

The handler reads your arguments, checks the depth limit so subagents cannot infinitely spawn more subagents, then calls into `agent_control.spawn_agent_with_metadata`. That function creates a fresh thread, attaches the role config, and starts the model running.

The branch that matters is `fork_context`. If you set it to true, Codex picks a path called `SpawnAgentForkMode::FullHistory`. The new thread gets a copy of the parent's conversation, decisions, and tool results. Codex also rejects any model or reasoning effort overrides on this path. The reason is simple. If you are forking the full history, you are saying "this agent is a continuation". Switching the model midway would corrupt that context. So Codex blocks it.

If `fork_context` is false, no fork mode is set. The agent starts cold. Only your `message` and `items` are visible to it. This is also the path where model and reasoning overrides are allowed, because there is no history to break.

What about the role itself. Look at `codex-rs/core/src/agent/role.rs`. Each role has a description string and an optional embedded TOML config loaded with `include_str!`. Today the explorer and worker built-in TOMLs are essentially empty, which means there is no hard tool allowlist or sandbox lockdown that physically prevents an explorer from writing files. The role is mostly a behavioral contract. The role description goes into the system prompt. The main thread is told, in its own instructions, that explorers should be treated as read-only and workers should be given file ownership.

That is worth saying out loud. The "read-only" nature of an explorer is enforced by prompt and convention, not by a sandbox flag. Codex trusts the orchestration layer to send explorers questions and send workers tasks. If you ask an explorer to write code, it will probably try.

Results come back through an event called `CollabAgentSpawnEndEvent`. That event carries the spawned thread id, the nickname, the model, and the status. The main thread reads it, decides what to do with the answer, and either keeps coordinating or spawns the next agent.

[IMAGE: sequence diagram. parent thread on the left calls spawn_agent. arrow to "fork_context check". two branches. top branch "true: copy full history, freeze model". bottom branch "false: empty thread, message only, model override allowed". both meet at "child runs". arrow back labeled "CollabAgentSpawnEndEvent: thread_id, nickname, status"]

![[images/04-subagents-in-general/spawn-agent-flow.png]]

---

## Coordination discipline

This is where most people break their subagent setup.

The main thread is the coordinator. Always. Subagents investigate. Subagents implement. They do not decide. They do not own the outcome. The main thread reads the results, picks what to trust, picks what to discard, and explains the final answer to the user.

The clean pattern looks like this.

1. Split the work into clear sub-tasks before you spawn anything.
2. Give each subagent the exact context it needs, no more.
3. Keep ownership boundaries separate. Two workers should never share files.
4. Review every result in the main thread before integrating.
5. Throw away the parts you do not trust.

If you skip step 1, the rest collapses. Spawning an agent on a fuzzy task is how you get a confident, beautifully-formatted, completely wrong answer back five minutes later.

---

## Good usage

Use an explorer when you need a specific answer before editing.

> Inspect the auth flow and tell me where password reset emails are generated. Do not edit any files. Return the exact file paths and line numbers.

Use a worker when the implementation is cleanly scoped.

> Update the settings panel copy in `src/settings/` only. Do not touch any other directory. Other workers may be editing the API layer in parallel, so do not revert their changes.

Use multiple agents when the work is genuinely parallel.

> Spawn one explorer to map the API contract. Spawn one worker to update the UI copy. The main thread reviews both before merging.

Each of these has the three things subagents need. A bounded task. A clear ownership line. And a reason the main thread cannot just do it inline.

---

## Bad usage

Do not spawn a subagent because the task is important. Importance is not a reason to delegate. Bounded scope is.

Do not delegate the immediate blocker. If your main thread cannot move until that result comes back, you are not delegating. You are blocking yourself with extra steps. Just do it inline.

Do not give two workers overlapping file ownership. Codex does not lock files between agents. You will get merge pain and lost edits, and the main thread will have to clean it up.

Do not fork context when the side mission does not need the conversation. A fresh thread with a tight `message` runs faster, costs less, and produces cleaner output than a forked thread that drags the whole parent history along for no reason.

[IMAGE: split panel. left side "good" green checkmark, an explorer with "find me X, do not edit" and a worker with "owns: src/billing/". right side "bad" red x, two workers both labeled "owns: src/" overlapping, and one agent with "this is important!!!" as its only instruction]

![[images/04-subagents-in-general/good-vs-bad.png]]

---

## Watching subagents in the app

The Codex App makes the side missions visible. While the main thread is coordinating, every subagent it spawns shows up as its own entry you can click into.

Click any subagent and a dropdown opens up with the live thread. You can see exactly what it is doing right now. The tool calls it is making, the files it is reading, the output it is producing. No guessing about whether the agent is stuck or making progress.

You are not locked out of it either. You can send a follow-up prompt directly to that subagent from inside the dropdown. Nudge an explorer toward a file it missed. Tell a worker to narrow its scope. The main thread keeps coordinating, and you keep a side channel into any agent that needs a course correction.

This is the part that turns subagents from a black box into something you can actually steer. You see the fanout. You see each agent in flight. And you can intervene without killing the run.

[IMAGE: codex app screenshot mockup. main thread on the left. on the right a list of subagents, one expanded into a dropdown showing live tool calls and a follow-up prompt input at the bottom]

![[images/04-subagents-in-general/subagent-dropdown.png]]

---

## Demo

Here is what the camera shows.

1. Open Codex on a real repo. Ask the main thread, "Spawn an explorer to find every place we send transactional email, and a second explorer to map the queue retry logic. Do not edit anything yet."
2. Watch Codex emit two `spawn_agent` tool calls in parallel, both with `agent_type: "explorer"` and `fork_context: false`. Show the JSON tool call inline.
3. Open the second agent's thread in the Codex App and show it has no parent history. Just the message you gave it.
4. Both explorers return. The main thread reads both results, picks the relevant files, and writes a one-paragraph plan.
5. Now ask the main thread, "Spawn a worker to add retry logging in `src/queue/` only. Do not touch the email module." Watch Codex call `spawn_agent` with `agent_type: "worker"` and a clear ownership line in the `message`.
6. The worker finishes. The main thread reviews the diff, accepts it, and explains what changed.
7. To close the loop, ask, "Now spawn a worker on the same files." Watch Codex push back, because the ownership boundary is gone. Show the model declining or asking for a narrower scope.

The whole demo lives or dies on one thing. The main thread is doing the coordinating. The agents are doing the side missions. You can see the discipline on the screen.

---

## Key insight

> Subagents are delegation, not decoration. Use them when the work splits cleanly and the main thread can keep moving while the side mission runs.

---

After this video, you should never spawn a subagent because something feels big. You spawn one because you can name the side mission in one sentence, hand it the exact context it needs, and trust the main thread to integrate the result. Anything else is theater.
