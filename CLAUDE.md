# ray-os

Ray's centralised personal operating system — content, research, projects, and social media in one place.

## YouTube

- **Channel**: https://www.youtube.com/@RAmjad/videos

```

## Obsidian Vault

This repo doubles as an Obsidian vault. When working with markdown files:

- **No H1 titles** — Obsidian uses filename as title
- **Linking** — Use `[[Note Name]]` for internal links, `[[Note Name|Display Text]]` for aliases
- **Tags** — `#tag` inline or in YAML frontmatter
- **Never delete files without explicit user permission**

### Frontmatter

```yaml
---
tags: [tag1, tag2]
aliases: [alternate-name]
date: YYYY-MM-DD
---
```

## Conventions

- **kebab-case everything** — All file and folder names use `kebab-case`. No Title Case with spaces, no camelCase. Obsidian displays titles via frontmatter `title:` or `aliases:`.
- Date-prefix files as `YYYY-MM-` for chronological sorting
- `analysis/` folders contain research about *other* creators/posts
- `self-audit/` or `posts/` folders contain Ray's own content and performance data
- Images tracked via Git LFS (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`, `*.svg`)

## Images

Images are co-located with the note that uses them. There is no vault-root `images/` dump.

- **Location**: each note's images live in an `images/` folder next to that note: `<note-dir>/images/`. When a note moves, its `images/` folder moves with it, so embeds never break.
- **Grouping**: a multi-image lesson groups its files in a named subfolder, `<note-dir>/images/<note-slug>/<note-slug>-N.png` (e.g. `images/worktrees/worktrees-2.png`). A one-off image can sit directly in `<note-dir>/images/<descriptive-name>.png`.
- **Naming**: kebab-case and descriptive. Rename screenshots on import. Never keep tool-default names like `CleanShot 2026-05-17 at 16.09.13@2x.png`.
- **Embeds**: prefer filename-only wikilinks, `![[descriptive-name.png]]`, when the filename is unique across the vault. Use a path-qualified embed, `![[images/<group>/<file>.png]]`, when filenames could collide (e.g. generic `excalidraw_N.png` from excalidraw-gen). Obsidian resolves a path embed by unique path-suffix, so `![[images/<group>/<file>.png]]` keeps working after the folder is relocated.
- **LFS**: all image types are tracked via Git LFS (see Conventions). No extra setup per image.

## Timeouts

For image generation tasks (excalidraw-gen skill), use extended timeouts:
```bash
timeout: 180000  # 3 minutes per operation
```
When generating 5+ images, plan for 2-3 minutes total.

## Web Search

Use the Exa MCP (`mcp__claude_ai_Exa__web_search_exa`) as the default for all web searches. Do not dual-search with WebSearch unless explicitly asked to benchmark.