---
duration: "1-4 min"
batch: 1
order: 1
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Commands"
---

# Scheduled Tasks — Set-and-Forget Cron Jobs

Claude Code can create scheduled background tasks that run on a cron — no external scheduler needed. Give it a prompt, pick a frequency, and it runs autonomously in the background. Think of it as cron jobs that understand your whole codebase.

### Examples

- **Email bug triage** — Check your emails every few hours for bug reports, enrich them with context in Sentry, and add them as tasks to your todo list.
- **Vercel log monitor** — Every 12 hours, pull Vercel logs, identify any errors, figure out the fix, open a PR, and send you a Telegram so you wake up to a fix instead of a fire.
- **Competitor ad/video tracker** — Use an MCP to monitor what ads competitors are running or what videos they just uploaded, and surface anything relevant.
- **PR babysitter** — Watch all your open PRs, auto-fix broken builds, and use worktree agents to address review comments — you come back to green checks.
- **Overnight codebase cleanup** — Review your codebase while you sleep for dead code, tech debt, and refactoring candidates — report waiting in the morning.
- **Weekly release automation** — Every Friday: update changelog, bump version, regenerate API docs, run tests, tag the release, push. Replaces a 45-minute manual process.

![[images/scheduled-tasks/excalidraw_3.png]]
