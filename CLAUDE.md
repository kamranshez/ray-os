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

All images live in a single vault-root `images/` folder. There are no co-located per-note `images/` folders.

- **Location**: every image goes directly in the vault-root `images/` folder: `images/<descriptive-name>.png`. No subfolders.
- **Naming**: kebab-case and descriptive of the image's *content*, and globally unique across the whole folder (the flat layout means a generic name like `excalidraw_1.png` or `1.jpg` will collide). Rename screenshots on import; never keep tool-default names like `CleanShot 2026-05-17 at 16.09.13@2x.png`. If a name would collide, extend it with more content detail (or a `-2` suffix as a last resort).
- **Embeds**: use filename-only wikilinks, `![[descriptive-name.png]]`. Because every image is unique and in one folder, filename-only links resolve regardless of where the note lives, so notes can move freely without breaking embeds. Obsidian image sizing is preserved as `![[descriptive-name.png|400]]`.
- **No orphans**: only keep images that a note actually references. Unreferenced images are deleted.
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
