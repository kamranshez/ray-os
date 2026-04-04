---
name: next-up
description: Show what to work on next by reading the Dashboard and following links to project boards and corrections. Use this skill whenever the user asks "what should I work on", "what's next", "show me my queue", "what's in progress", or wants a quick view of active tasks across all projects. Also triggers on /next-up.
---

# /next-up — What to Work On

Show Ray what's in progress, what's next, and what corrections need attention
across all active projects. This is the "ground-level" view — not analytics
or briefings, just the work queue.

## Instructions

### Step 1: Read the Dashboard

Read `Dashboard.md` at the vault root. It's a router — a table of projects
with their status, board link, and corrections link.

Filter to rows where Status = `active`. Ignore parked projects entirely.

### Step 2: For each active project, follow the links

**Board file** (the kanban):
- Read the linked board file (e.g., `projects/agentic-coding-school/board.md`)
- Extract items from the `## Doing` section — these are in-progress tasks
- Extract items from the `## To Do` section — these are queued next
- Ignore `## Backlog` and `## Done`

**Corrections file** (if present):
- Read the linked corrections file (e.g., `projects/agentic-coding-school/corrections.md`)
- Extract unchecked items (`- [ ]`) — these are corrections to published videos
- Checked items are done, skip them

### Step 3: Read each task note for context

For every item in Doing and To Do (not Backlog), the kanban links to a note
via `[[note-name]]`. Try to read each linked note to get a one-line summary
of what the task involves. Notes live in the project's `to-film/` subfolders,
organized by class (e.g., `to-film/claude-code/`, `to-film/business/`).

If a note doesn't exist yet, that's fine — just show the title.

For corrections, similarly try to read each linked note from `to-film/correction/`.

### Step 4: Present the queue

Format the output like this:

```
DOING ([count])
- [task name] — [class tag] — [one-line context from note]
- ...

NEXT UP ([count])
- [task name] — [class tag] — [one-line context from note]
- ...

CORRECTIONS ([count])
- [task name] — [one-line context from note]
- ...

[Optional: "No corrections pending" if all are checked off]
```

### Guidelines

- Keep it scannable. One line per task, no paragraphs.
- The class tag comes from the kanban item's `#tag` (e.g., `#claude-code`, `#business`).
- If a task note has a `## Brief` or `## Script` section, pull the first sentence as context.
- If a task note is empty or missing, just show the task name and tag.
- Don't make priority recommendations — just show the state. Ray decides what to do.
- Don't show the Backlog. That's for planning sessions, not daily work.
- End with: "Run `/gm` for your full morning briefing with calendar and tasks."
