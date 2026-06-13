Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. It doesn't save something every session — it decides what's worth remembering based on whether the information would be useful in a future conversation.

Auto memory requires Claude Code v2.1.59 or later. Check your version with `claude --version`.

## Enable or disable auto memory

Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings:

```json
{
  "autoMemoryEnabled": false
}
```

You can also disable it via environment variable by setting `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

![[directory-structure-git-worktrees-configuration.png]]
## Storage location

Each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. The `<project>` path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.

To store auto memory in a different location, set `autoMemoryDirectory` in your user or local settings:

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

This setting is accepted from policy, local, and user settings. It is not accepted from project settings (`.claude/settings.json`) to prevent a shared project from redirecting auto memory writes to sensitive locations.

The directory contains a `MEMORY.md` entrypoint and optional topic files:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

`MEMORY.md` acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using `MEMORY.md` to keep track of what's stored where. Auto memory is machine-local — all worktrees and subdirectories within the same git repository share one auto memory directory, but files are not shared across machines or cloud environments.

[[images/storage-location/excalidraw_1.png]]
![[session-history-directory-storage-structure.png]]
![[memory-organization-session-history-index.png]]
![[claude-memory-default-vs-custom-config.png]]
![[claude-memory-storage-structure-scope.png]]

## How it works

The first 200 lines of `MEMORY.md`, or the first 25KB (whichever comes first), are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.

This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.

Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.

Claude reads and writes memory files during your session. When you see "Writing memory" or "Recalled memory" in the Claude Code interface, Claude is actively updating or reading from `~/.claude/projects/<project>/memory/`.

![[images/how-it-works/excalidraw_1.png]]
![[images/how-it-works/excalidraw_2.png]]
![[images/how-it-works/excalidraw_3.png]]
![[images/how-it-works/excalidraw_4.png]]
![[images/how-it-works/excalidraw_5.png]]

## Audit and edit your memory

All auto memory files are plain markdown you can edit or delete at any time. Run `/memory` to browse and open memory files from within a session.

![[memory-files-before-after-organization.png]]
![[memory-files-markdown-editable-management.png]]
![[memory-organization-before-after-workflow.png]]
![[memory-management-filing-workflow.png]]
![[auto-memory-toggle-disable-methods.png]]

## View and edit with `/memory`

The `/memory` command lists all CLAUDE.md and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.

When you ask Claude to remember something — like "always use pnpm, not npm" or "remember that the API tests require a local Redis instance" — Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly (e.g. "add this to CLAUDE.md") or edit the file yourself via `/memory`.

![[memory-system-command-interface.png]]
![[memory-command-configuration-workflow.png]]
![[memory-instruction-management-paths.png]]
![[memory-command-auto-memory-adding.png]]
![[memory-system-learning-feedback.png]]
