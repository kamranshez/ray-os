---
tags: [claude-code, observer-agents, reverse-engineering, gated-features]
date: 2026-07-12
aliases: [observer-agents, agent-observer, watchdog-agents]
---

Full self-contained description of Claude Code's **Observer Agents** feature, reverse-engineered from the shipped binary v2.1.207 (build `bc512d5`) on 2026-07-12. Gated/experimental at time of writing.

## One-line summary

An **observer agent** is a second agent paired to a running ("observed") agent that receives a read-only digest of the observed agent's activity after each turn, can **report** on it, and can sit on the **permission gate** to allow / deny / defer the observed agent's actions — separating *doing* the work from *supervising* it into two agents with independent contexts.

## Core idea

Normally one agent both does a task and is responsible for not doing anything unsafe. That self-policing is weak: the same context motivated to finish is the one judging safety, so it rationalizes ("I need to force-push to fix this"). Observer agents split those roles. The worker just works; a separate observer — fresh context, single job — watches and can intervene. Crucially the observer isn't only advisory: it's wired into the permission system, so it can structurally block an action, not just comment on it.

## Rollout & gating

- **Flag:** `tengu_observer_agents_enabled` (GrowthBook). Default appears ON in this build, but it is still guarded and paired with an env opt-in.
- **Env opt-in:** `CLAUDE_CODE_EXPERIMENTAL_OBSERVER_AGENTS=1`.
- **Status:** experimental. The "EXPERIMENTAL" env name and the flag guard both signal it is not GA.

## How you declare it

Observer pairing is declared in the **observed agent's** definition (a `.claude/agents/<name>.md` file), via an `observer:` frontmatter field naming another agent type:

```yaml
---
name: observed-demo
description: ...
observer: watchdog-demo      # <-- names the observer agent type
tools: Read, Bash, Grep, Glob
---
```

The named observer (`watchdog-demo`) is itself an ordinary agent definition. When the observed agent is spawned, Claude Code resolves the `observer` name against available agent types (`let o = t.find(i => i.agentType === n)`); if it matches, the observer is auto-spawned. If it does not match, it logs `… which does not match any available agent type — unobserved` and the agent runs normally.

Binary evidence: `if (!e?.observer) return;` (the definition carries an `observer` property), `observerAgentType`, `declaredObserverType`, `[observer auto-spawn] Watch agent <X> and report via ObserverReport.`

## Lifecycle

1. **Auto-spawn.** Spawning an agent whose definition declares an `observer` triggers `[observer auto-spawn] Watch agent X and report via ObserverReport`.
2. **Arm.** The observer becomes `armed`. Arming runs a permission check with a mode (`armingPermissionMode` / `persistedArmingMode`, values `default` or `bypassPermissions`); if denied: `[agentObserver] arm-time permission denied for observer 'X' on 'Y'`.
3. **Observe.** After each of the observed agent's turns, the observer receives a **read-only activity digest** (see below). Steady state is silence.
4. **Act (optional).** The observer may emit an `ObserverReport` and/or exercise the permission gate.
5. **Retire.** States seen: `armed`, `blocked`, `retired`, `stopped`, plus an `observer tombstone` marker on teardown.
6. **Resume re-arm.** Observers persist across session resume: `reattachObserverTaskId`, `priorObserverTaskId`, `[agentObserver] resume re-arm failed for '…'` — on resuming a session the observer is re-attached to its observed task.

Bookkeeping fields tracking the pair: `observedTaskId` / `observerTaskId`, `observedAgentType` / `observerAgentType`, `observedKey`, `observedName`, `observedEnvelopeName`, `observedIsObserver`.

## What the observer receives

Per the observer's own system prompt (verbatim from the binary):

> "You are a background observer paired with the agent "<name>". After each of its turns you will receive a read-only activity digest wrapped in <…>. **The expected steady state is silence: most digests warrant no response at all.**"

The digest is assembled from the observed agent's event stream. Event/message kinds present in the observer envelope: `agent`, `tool_call`, `tool_result`, `assistant` (and user/turn boundaries). So the observer sees what tools the worker called, what came back, and what it said — read-only.

## What an observer can do

**1. Report — `ObserverReport` tool.** The observer's channel to surface something. In practice: a one-line assessment ("clean: read 2 files, ran ls, no risky actions" / "flag: attempted rm outside task"). Designed to be used sparingly (silence is the default).

**2. Gate permissions.** The observer is wired into the permission system for the observed agent's actions:
- `permission_mode` outcomes: `allow` / `deny` / `defer` (plus `default`).
- `observer-gate-` prefixed decisions, `permissionBehavior`, `safetyCheck`, `updatedInput` (it can even rewrite the action's input).
- `preventContinuation` — the observer can stop the observed agent from continuing.
- Batches of pending actions are evaluated; on error the batch is dropped fail-safe: `[agentObserver] permission gate errored (batch dropped)`.
- Sits alongside Claude Code's existing dangerous-command detection (`Dangerous rm operation`, `Dangerous rmdir operation`).

This is the load-bearing difference from a plain "reviewer" — the observer can veto in real time.

## Constraints & guarantees

- **No chaining.** An observer cannot itself be observed: `[agentObserver] ignoring observer declaration on observer agent '<X>' (no chaining)`. Prevents infinite observer towers.
- **Arm-time permission check.** Installing an observer is itself permission-gated; it can be denied before it ever watches.
- **`allowedAgentTypes`.** There is a notion of which agent types are permitted as observers.
- **Read-only digest.** The observer sees a digest, not a live mutable handle — it watches, it doesn't run inside the worker's thread.
- **Fail-safe.** Gate errors drop the batch rather than silently allowing.

## How to experiment (working demo)

Two agent files in `.claude/agents/`:

- `observed-demo.md` — a worker that makes several visible tool calls; frontmatter declares `observer: watchdog-demo`.
- `watchdog-demo.md` — the observer; watches the stream and calls `ObserverReport` on anything risky/off-track.

Run:
```bash
cd /Users/ray/Desktop/ray-os
CLAUDE_CODE_EXPERIMENTAL_OBSERVER_AGENTS=1 claude --debug
```
Then: "Use the observed-demo agent to list images/, read CLAUDE.md, and grep for kairos in artefacts." The watchdog auto-spawns and reports. Debug lines to look for: `[observer auto-spawn] …`, `[agentObserver] Agent 'observed-demo' declares observer 'watchdog-demo'`. To see the gate fire, give the worker a mildly destructive step and watch the observer deny/defer it.

(This build's flag is force-enabled locally via the Proxyman GrowthBook rule `B3AD68CE` + `~/.claude.json` cache seed.)

## Why it matters / use cases

- **Guardrail for unattended/autonomous agents** — the safety partner to persistent loops + the background daemon ("runs while you sleep"). An independent watchdog that can halt a runaway before it deletes the wrong dir or force-pushes over main.
- **Real-time quality gate** — flags drift as it happens ("wrong file", "test skipped not fixed", "reading a secret") instead of at post-hoc review.
- **Loop / stuck detection** — a cheap model watching an expensive one, ready to interrupt a spin.
- **Independent audit trail** — an objective record of what the worker actually did.
- **Context hygiene** — supervision concerns live in the observer's context, not the worker's; neither pollutes the other.

## Open/unconfirmed

- The exact frontmatter key is `observer:` (inferred from the `observer` property access + confirmed empirically by the demo firing); a plural/alternate alias was not found.
- Whether the digest is every event or a summarized rollup per turn — the prompt says "activity digest," implying some summarization.
- Whether observer gate decisions require the observer agent to have specific tools/permissions granted, beyond arm-time approval.

Source strings: `/Users/ray/.claude/cache/binary-strings/2.1.207.txt`, observer module ~offset 6.03M and 6.26M.
