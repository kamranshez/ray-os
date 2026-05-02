# ray-os

Ray's centralised personal operating system — content, research, projects, and social media in one place.

<important if="you are about to call any MCP tool (mcp__*) — Stripe, PostHog, Exa, etc.">
**STOP.** First run `ls ./code-tools/<service>/` (e.g. `code-tools/stripe/`) to check for a local script that does this task. If a relevant script exists, use it via Bash instead of the MCP tool — these scripts are pre-built for common queries (aggregations, joins, formatting) that MCP tools handle poorly one-call-at-a-time.

Only fall back to the MCP tool if no matching script exists. Mention which path you took in your first user-facing sentence ("Using code-tools/<service>/..." or "No matching script, using MCP...").
</important>

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

## Web Search

Use the Exa MCP (`mcp__claude_ai_Exa__web_search_exa`) as the default for all web searches. Do not dual-search with WebSearch unless explicitly asked to benchmark.