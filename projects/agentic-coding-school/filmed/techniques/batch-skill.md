---
duration: "1-4 min"
batch: 1
order: 20
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Skills"
---
## The Problem: Sequential Bottleneck

When you need to apply the same kind of change across dozens of files — a migration, a rename, a pattern replacement — doing it sequentially is painfully slow. The agent works through files one at a time, and by file 15 it's running low on context, forgetting conventions it followed in file 3, and making inconsistent changes.

You could do it manually file-by-file, but that defeats the purpose of having an agent.

![[images/sequential-bottleneck/excalidraw_5.png]]

## The Solution: One Coordinator, Many Workers

`/batch` turns a single instruction into a parallel operation. You say "replace all uses of lodash with native equivalents" and it:

1. **Researches the scope** — launches Explore agents to find every file, pattern, and call site that needs to change
2. **Decomposes into 5–30 independent units** — each unit is scoped to a directory or module, independently mergeable, and can't conflict with sibling units
3. **Spawns one worker per unit** — all running in parallel, each in an isolated git worktree so they can't step on each other
4. **Each worker autonomously**: implements the change, runs `/simplify` to clean up, runs tests, does e2e verification, commits, and opens a PR
5. **Tracks progress** — renders a status table that updates as workers complete, showing PR links

The key architectural decision: **git worktree isolation**. Each worker gets its own copy of the repo, so 20 agents can edit the same codebase simultaneously without merge conflicts during implementation. The conflicts (if any) only surface when merging PRs, where they're much easier to resolve.

![[images/coordinator-worker-fanout/excalidraw_3.png]]


## When to Use It

- Migrations: React to Vue, lodash to native, class components to hooks
- Codebase-wide renames or pattern replacements
- Adding type annotations, tests, or documentation across many files
- Any change where the instruction is uniform but the scope is large
- Translating content across many files (the literal example from the prompt)

## What Makes It Smart

- **Mandatory e2e verification** — the coordinator figures out how workers can verify their changes end-to-end (browser automation, curl, test suite) *before* spawning them. If it can't figure it out, it asks you.
- **Workers run /simplify** — each worker reviews its own changes before committing, so you don't get 20 PRs of sloppy code
- **Plan approval gate** — you see the full decomposition before any work starts. You can adjust unit boundaries, merge trivial units, or split large ones.
- **Self-contained worker prompts** — each worker gets the full context it needs (codebase conventions, e2e recipe, exact file list) so it doesn't have to rediscover anything

## The Full Prompt

```
# Batch: Parallel Work Orchestration

You are orchestrating a large, parallelizable change across this codebase.

## User Instruction

<the user's instruction gets interpolated here>

## Phase 1: Research and Plan (Plan Mode)

Call the `EnterPlanMode` tool now to enter plan mode, then:

1. **Understand the scope.** Launch one or more Explore agents (in the foreground — you need their results) to deeply research what this instruction touches. Find all the files, patterns, and call sites that need to change. Understand the existing conventions so the migration is consistent.

2. **Decompose into independent units.** Break the work into 5–30 self-contained units. Each unit must:
   - Be independently implementable in an isolated git worktree (no shared state with sibling units)
   - Be mergeable on its own without depending on another unit's PR landing first
   - Be roughly uniform in size (split large units, merge trivial ones)

   Scale the count to the actual work: few files → closer to 5; hundreds of files → closer to 30. Prefer per-directory or per-module slicing over arbitrary file lists.

3. **Determine the e2e test recipe.** Figure out how a worker can verify its change actually works end-to-end — not just that unit tests pass. Look for:
   - A `claude-in-chrome` skill or browser-automation tool (for UI changes: click through the affected flow, screenshot the result)
   - A `tmux` or CLI-verifier skill (for CLI changes: launch the app interactively, exercise the changed behavior)
   - A dev-server + curl pattern (for API changes: start the server, hit the affected endpoints)
   - An existing e2e/integration test suite the worker can run

   If you cannot find a concrete e2e path, use the `AskUserQuestion` tool to ask the user how to verify this change end-to-end. Offer 2–3 specific options based on what you found (e.g., "Screenshot via chrome extension", "Run `bun run dev` and curl the endpoint", "No e2e — unit tests are sufficient"). Do not skip this — the workers cannot ask the user themselves.

   Write the recipe as a short, concrete set of steps that a worker can execute autonomously. Include any setup (start a dev server, build first) and the exact command/interaction to verify.

4. **Write the plan.** In your plan file, include:
   - A summary of what you found during research
   - A numbered list of work units — for each: a short title, the list of files/directories it covers, and a one-line description of the change
   - The e2e test recipe (or "skip e2e because …" if the user chose that)
   - The exact worker instructions you will give each agent (the shared template)

5. Call `ExitPlanMode` to present the plan for approval.

## Phase 2: Spawn Workers (After Plan Approval)

Once the plan is approved, spawn one background agent per work unit using the `Agent` tool. **All agents must use `isolation: "worktree"` and `run_in_background: true`.** Launch them all in a single message block so they run in parallel.

For each agent, the prompt must be fully self-contained. Include:
- The overall goal (the user's instruction)
- This unit's specific task (title, file list, change description — copied verbatim from your plan)
- Any codebase conventions you discovered that the worker needs to follow
- The e2e test recipe from your plan (or "skip e2e because …")
- The worker instructions below, copied verbatim:

After you finish implementing the change:
1. **Simplify** — Invoke the `Skill` tool with `skill: "simplify"` to review and clean up your changes.
2. **Run unit tests** — Run the project's test suite (check for package.json scripts, Makefile targets, or common commands like `npm test`, `bun test`, `pytest`, `go test`). If tests fail, fix them.
3. **Test end-to-end** — Follow the e2e test recipe from the coordinator's prompt (below). If the recipe says to skip e2e for this unit, skip it.
4. **Commit and push** — Commit all changes with a clear message, push the branch, and create a PR with `gh pr create`. Use a descriptive title. If `gh` is not available or the push fails, note it in your final message.
5. **Report** — End with a single line: `PR: <url>` so the coordinator can track it. If no PR was created, end with `PR: none — <reason>`.

Use `subagent_type: "general-purpose"` unless a more specific agent type fits.

## Phase 3: Track Progress

After launching all workers, render an initial status table:

| # | Unit | Status | PR |
|---|------|--------|----|
| 1 | <title> | running | — |
| 2 | <title> | running | — |

As background-agent completion notifications arrive, parse the `PR: <url>` line from each agent's result and re-render the table with updated status (`done` / `failed`) and PR links. Keep a brief failure note for any agent that did not produce a PR.

When all agents have reported, render the final table and a one-line summary (e.g., "22/24 units landed as PRs").
```
