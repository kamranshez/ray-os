---
tags: [claude-code, coordinator-mode, fleet, orchestration, gated-features, reverse-engineering]
date: 2026-07-12
aliases: [coordinator-mode, cc-coordinator, delegation-only-mode]
---

Self-contained description of Claude Code's **Coordinator Mode**, reverse-engineered from the shipped binary v2.1.207 (build `bc512d5`) on 2026-07-12. Gated/experimental at time of writing. See [[README]] for the discovery routine; sibling deep-dive: [[observer-agents]].

## One-line summary

Coordinator Mode turns a Claude Code session into a **delegation-only orchestrator**: its own toolset is stripped down to spawning and steering worker subagents (`Agent`, `SendMessage`, `TaskStop`, plus `StructuredOutput`/`Workflow`), so it cannot touch the codebase directly — it can only direct workers to do the research/implementation/verification and then synthesize their results.

## Why it exists

It's the "manager" half of Claude Code's Fleet/multi-worker story. A normal session both plans and executes, which muddies context and makes it easy for one agent to rabbit-hole. Coordinator mode enforces separation of concerns structurally: the coordinator keeps a clean, high-altitude view and never gets its hands dirty, while workers (spawned via `Agent`) hold the messy execution context. It pairs naturally with [[observer-agents]] (supervision) and the background daemon (persistence).

## Rollout & gating — the catch

Activation is **pure env-var logic** — no GrowthBook flag, no entitlement gates entry. The gate is `lk()` / `isCoordinatorMode()` (exported as `Dee`):

```js
function lk(){
  if(!ct(process.env.CLAUDE_CODE_COORDINATOR_MODE)) return false;
  if(c1() && !Zs() && !ct(process.env.CLAUDE_CODE_REMOTE)) return false;
  return true
}
```

- `ct(e)` — truthy-env parser: accepts `1`, `true`, `yes`, `on` (case-insensitive, trimmed).
- `c1()` = `Pt.isInteractive` — true in a real terminal.
- `Zs()` = `Pt.caps.workspace === "remote"` — true only inside a cloud / CCR / teams sandbox, **false** on a local machine.

**The gotcha:** setting `CLAUDE_CODE_COORDINATOR_MODE=1` alone does nothing in a normal terminal. Walking the second line for a local interactive session: `c1()`=true, `!Zs()`=true, `!ct(REMOTE)`=true → the whole condition is true → `return false`, and the session silently falls back to normal. You must **also** set `CLAUDE_CODE_REMOTE=1` (spoofing the "I'm a remote session" signal) to get past it. In a non-interactive/headless (`--print`) invocation, `c1()` is false so the second line short-circuits and `CLAUDE_CODE_REMOTE` isn't needed.

Session-resume auto-toggle (`IZh`/`matchSessionMode`): resuming a session recorded in coordinator mode re-sets the env var and re-checks `Dee()`; if the gate still blocks (plain terminal) it silently deletes the var again. It only prints `"Entered coordinator mode to match resumed session."` / `"Exited coordinator mode to match resumed session."` when the mode actually changes.

### Activation recipe (local, watchable)

```bash
CLAUDE_CODE_COORDINATOR_MODE=1 CLAUDE_CODE_REMOTE=1 claude
# add tools back into the stripped set:
CLAUDE_CODE_COORDINATOR_MODE=1 CLAUDE_CODE_REMOTE=1 CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS=Bash,Read claude
```

Note `CLAUDE_CODE_REMOTE=1` is a side door — that var normally travels with `CLAUDE_CODE_REMOTE_SESSION_ID` / `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` in genuine cloud sessions. Forcing it locally just to satisfy the gate works, but you're spoofing the remote-session check, not using a documented path.

## What changes when it's active

**1. The system prompt swaps** (`DZh`/`getCoordinatorSystemPrompt`, fired via `we("coordinator_mode_start")`):

> "You are Claude Code, an AI assistant that orchestrates software engineering tasks across multiple workers.
> ## 1. Your Role
> You are a **coordinator**. Your job is to: Help the user achieve their goal · Direct workers to research, implement and verify code changes · Synthesize results and communicate with the user · Answer questions directly when possible — don't delegate work that you can handle without tools.
> ## 2. Your Tools — **Agent** (Spawn a new worker) · **SendMessage** (Continue an existing worker) · **TaskStop** (Stop a running worker)"

**2. The tool list collapses** — the biggest visible tell. The hard-coded coordinator allowlist (`A9i`) is exactly: **`Agent`, `TaskStop`, `SendMessage`, `StructuredOutput`, `Workflow`**. Everything else — `Bash`, `Read`, `Edit`, `Write`, `Grep`, `Glob`, `WebFetch`, `WebSearch`, most MCP tools — is stripped by `D7p()` / `applyCoordinatorToolFilter`. If Claude can no longer read or run anything and only delegates, you're in coordinator mode.

**3. Worker semantics** — `Agent` calls are narrated as spawning "workers"; results arrive as `<task-notification>` XML wrapped in **user-role** messages (not inline tool results). The prompt tells the model: *"After launching agents, [briefly tell the user what you launched] and end your response. Never fabricate or predict agent results... results arrive as separate messages."*

**4. Cosmetic panel** — `tengu_coordinator_panel` (GrowthBook, default **true**, no-op in non-interactive) suppresses killed-worker status lines from the transcript (they live in a persistent worker panel instead) and reserves footer width for a worker-count indicator. This flag only affects rendering, not activation.

## `CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS`

A comma-separated allowlist of tool names added back into the stripped set, parsed inside `D7p()` (which only runs when `isCoordinatorMode()` is true): `new Set((env.CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS ?? "").split(",").map(trim).filter(Boolean))`. Use it to let the coordinator also, say, `Read` or run `Bash` itself.

Other keep-conditions in `D7p()`: `subscribe_pr_activity`/`unsubscribe_pr_activity` always kept; MCP tools with `mcpInfo.role==="comms"` kept; and if `CLAUDE_CODE_BRIEF` is set, `SendUserMessage`/`SendUserFile` are kept too. The CCR-comms path (`isCcrCoordinator()`) is **dead code in this build** — `function kZh(){return Dee() && !1}` always false — so remote-comms tools are unreachable; the local `EXTRA_TOOLS` route is the way to broaden the toolset.

## Verify it worked

1. Ask Claude to list its tools, or run `/context` — should show only `Agent`, `SendMessage`, `TaskStop`, `StructuredOutput`, `Workflow` (+ `subscribe_pr_activity`/`unsubscribe_pr_activity`, + anything from `EXTRA_TOOLS`). No `Bash`/`Read`/`Edit`.
2. Ask "what is your role" — it self-describes as a coordinator directing workers.
3. Any task it takes on is delegated to "workers," with results arriving as separate messages.

Telemetry/labels: `tengu_coordinator_mode_switched`, `is_coordinator` tag in `tengu_init`, session mode saved as `"coordinator"` vs `"normal"`.

## Ungatability & video angle

- **Ungatable: yes (env only)** — `CLAUDE_CODE_COORDINATOR_MODE=1` + `CLAUDE_CODE_REMOTE=1`, no flag or entitlement needed. No server call gates entry; the stripped toolset is what bounds what the coordinator can do (no separate publish gate).
- **Video-worthiness:** strong as part of a multi-agent story ("Claude that only manages, never codes — it delegates everything to a fleet of workers"), and the toolset-collapse is a clean on-camera demo. Pairs with [[observer-agents]] and the daemon for a full "autonomous fleet" narrative.

## Open/unconfirmed

- Whether `Zs()` (`Pt.caps.workspace==="remote"`) can be satisfied by anything other than `CLAUDE_CODE_REMOTE` in a real cloud session.
- Exact worker default agent type and `maxTurns` for coordinator-spawned workers.
- Whether the dead `isCcrCoordinator()` path is slated to re-enable comms tools in a later build.

Source strings: `/Users/ray/.claude/cache/binary-strings/2.1.207.txt` (coordinator module ~offset 16.01M).
