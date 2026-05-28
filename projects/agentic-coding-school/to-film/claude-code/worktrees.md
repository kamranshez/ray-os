---
duration: "5-9 min"
batch: 1
order: 9
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Advanced"
---

# Worktrees

## The Problem

When you run two Claude sessions on the same codebase at the same time, they share the same files. If both agents touch the same file — even accidentally — they corrupt each other's work. You might not notice until the code is broken and you can't tell who broke it.

Git worktrees solve this. One repo, multiple working directories, each on its own branch. It's not a Claude thing — it's a Git primitive that Claude Code has added built-in support for.

![[two-sessions-one-codebase-problem.png]]
## What Worktrees Actually Do

Each agent gets its own isolated copy of the working directory on a separate branch. They can edit files, run builds, and test independently without touching each other. When they're done, you merge the branch back in.

The Claude Code Desktop app has had built-in worktree support for a while. Now subagents support it too — so when Claude spawns parallel tasks, each one can operate in its own worktree automatically.

![[isolated-worktrees-parallel-agents.png]]
## When They're Worth It

Boris Cherny (Claude Code engineer) uses subagent worktrees mainly for large batch changes — codebase-wide code migrations, things that would previously require a custom Python harness or a multi-step plan that rarely executes cleanly in one shot.

One reply from the thread nailed it: *"each subagent gets clean isolation, no conflict drama, then you just review the diff. the 1-shot part is the killer feature — sequential edits across 50 files is where things used to fall apart."*

The pattern: one orchestrator session spawns up to 8 subagents, each in its own worktree, all running in parallel. Real speed, no conflicts.
![[subagent-worktrees-parallel-execution.png]]
## When They Don't Help: Agent Teams

Here's a subtlety worth understanding. If you're using agent teams — where multiple agents are collaborating on the same high-level task — worktrees don't actually help much. The problem is coordination, not file conflicts. Agents that need to share context, read each other's output, or build on each other's work need to operate on the same state. Splitting them into isolated worktrees just makes that harder.

Worktrees are for **truly independent** workstreams. Think: migrate 50 files where each file is self-contained, or run the same refactor across 10 separate modules. If the agents need to talk to each other, stay on the same branch.

![[agent-teams-vs-independent-workstreams.png]]
## The Honest Tradeoffs

The team behind Claude Code is roughly 50/50 on worktrees. Half use them. Half prefer multiple git checkouts or just opening multiple tabs in the Desktop app.

The friction is real:
- You need to reinstall dependencies in each worktree
- You need to clean up after
- Merge conflicts still happen — you just deferred them
- Different agents handle things their own way, which creates drift

For small, tight changes? Some people just skip worktrees entirely and run two sessions on the same branch. If the scope is small enough that they won't touch the same files, it works fine.

The longer-term take from some in the thread: worktrees are a stepping stone. The real direction is lightweight cloud VMs — a fresh, pre-prepared environment per session. Worktrees are the best current solution, not the permanent one.

![[worktree-friction-and-future-direction.png]]
## How to Use Them

You don't need to touch git directly. Claude Code has a built-in `--worktree` flag:

```bash
claude --worktree feature-auth    # named worktree
claude -w bugfix-123              # short form
claude --worktree                 # auto-generates a name like "bright-running-fox"
```

This creates an isolated directory at `<repo>/.claude/worktrees/<name>/` on a new branch and starts Claude there. When the session ends with no changes, the worktree and branch are automatically removed. If there are changes, Claude asks whether to keep or clean up.

For subagents, add `isolation: worktree` to their frontmatter and each one gets its own worktree automatically.

![[worktree-flag-and-subagent-isolation.png]]
## Setting Up the Environment Automatically

Fresh worktrees don't have your gitignored files — no `.env`, no `node_modules`. This is the friction people complain about. Claude Code solves it with two hooks: `WorktreeCreate` and `WorktreeRemove`.

`WorktreeCreate` fires when a worktree is being set up and **replaces the default git logic entirely** — so you can run `npm install`, copy `.env` files, spin up Docker, whatever the project needs. Your script receives the worktree path and branch as JSON and prints the final path back to stdout.

```json
{
  "hooks": {
    "WorktreeCreate": [
      { "type": "command", "command": "\".claude/hooks/setup-worktree.sh\"" }
    ],
    "WorktreeRemove": [
      { "type": "command", "command": "\".claude/hooks/cleanup-worktree.sh\"" }
    ]
  }
}
```

There's also `.worktreeinclude` — a file in your project root listing gitignored files you want auto-copied into every new worktree (like `.env` or `config/secrets.json`). Only gitignored files matching the list get copied; tracked files are never duplicated.

`WorktreeRemove` fires on cleanup — useful for teardown tasks like dealloc resources or logging, but failures don't block the removal.

![[worktreecreate-hooks-automated-setup.png]]
## References
- Boris Cherny's announcement thread: https://x.com/bcherny/status/2025117826412106216
- 50 Tips video tip: *"Use worktrees so parallel sessions don't interfere with your main project"*
- [[subagent-teams]] — note: worktrees don't help much when agents share the same high-level task, only when they're truly independent
