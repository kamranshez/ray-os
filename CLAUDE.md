# ray-os

Ray's centralised personal operating system — content, research, projects, and social media in one place. The repo doubles as an Obsidian vault.

<important if="you are working with markdown notes in the vault (creating, editing, linking, tagging)">

- **No H1 titles** — Obsidian uses filename as title
- **Linking** — Use `[[Note Name]]` for internal links, `[[Note Name|Display Text]]` for aliases
- **Tags** — `#tag` inline or in YAML frontmatter
- **Never delete files without explicit user permission**
</important>

<important if="you are adding or editing frontmatter on a note">

```yaml
---
tags: [tag1, tag2]
aliases: [alternate-name]
date: YYYY-MM-DD
---
```
</important>

<important if="the user asks you to open a file in Obsidian, or you want to surface a note for the user to look at">

Use the official Obsidian CLI. Do not use `open -a Obsidian` or the `obsidian://` URI scheme — the CLI opens the file in the active vault and reports what it opened.

```bash
# By filename (resolves like a wikilink — works when the name is unique in the vault)
obsidian open file=<note-name>

# By full vault-relative path (required when filenames collide)
obsidian open path=projects/.../note.md
```

Obsidian must already be running; the first invocation launches it. CLI ships inside Obsidian.app 1.12.7+ at `/usr/local/bin/obsidian`. Docs: https://help.obsidian.md/cli
</important>

<important if="you are creating new files or folders, or naming anything in the vault">

- **kebab-case everything** — All file and folder names use `kebab-case`. No Title Case with spaces, no camelCase. Obsidian displays titles via frontmatter `title:` or `aliases:`.
- Date-prefix files as `YYYY-MM-` for chronological sorting
- `analysis/` folders contain research about *other* creators/posts
- `self-audit/` or `posts/` folders contain Ray's own content and performance data
</important>

<important if="you are adding, embedding, or moving images in notes">

Images are co-located with the note that uses them. There is no vault-root `images/` dump.

- **Location**: each note's images live in an `images/` folder next to that note: `<note-dir>/images/`. When a note moves, its `images/` folder moves with it, so embeds never break.
- **Grouping**: a multi-image lesson groups its files in a named subfolder, `<note-dir>/images/<note-slug>/<note-slug>-N.png` (e.g. `images/worktrees/worktrees-2.png`). A one-off image can sit directly in `<note-dir>/images/<descriptive-name>.png`.
- **Naming**: kebab-case and descriptive. Rename screenshots on import. Never keep tool-default names like `CleanShot 2026-05-17 at 16.09.13@2x.png`.
- **Embeds**: prefer filename-only wikilinks, `![[descriptive-name.png]]`, when the filename is unique across the vault. Use a path-qualified embed, `![[images/<group>/<file>.png]]`, when filenames could collide.
- **LFS**: all image types (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`, `*.svg`) are tracked via Git LFS.
</important>

<important if="you are running excalidraw-gen or any image-generation operation">

Use extended timeouts: `timeout: 180000` (3 minutes) per operation. When generating 5+ images, plan for 2-3 minutes total.
</important>

<important if="you are about to do a web search">

Use the Exa MCP (`mcp__claude_ai_Exa__web_search_exa`) as the default. Do not dual-search with WebSearch unless explicitly asked to benchmark.
</important>

<important if="you are working on YouTube content, scripts, or analytics">

Channel: https://www.youtube.com/@RAmjad/videos
</important>
