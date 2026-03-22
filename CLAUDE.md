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

## Timeouts

For image generation tasks (excalidraw-gen skill), use extended timeouts:
```bash
timeout: 180000  # 3 minutes per operation
```
When generating 5+ images, plan for 2-3 minutes total.

## Benchmarking

Whenever you're told to do a web search online, spawn up two subagents, one to use the WebSearch tool and another to use the Exa MCP search tool in separate subagents, and then pass both of the results back to the main session. 

Once we have successfully implemented the task, add to a benchmark-search.md file that basically tells us which server was more useful for the optical job, whether it was the web search tool or the Exa MCP. 

Always include a table of which search results were missing what.