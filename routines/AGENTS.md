# routines/ -- shared conventions for cloud routines

Every `*.md` here (and in `acs/`) is a **self-contained prompt for an unattended cloud
routine**: an isolated Claude Code session Anthropic's cloud spawns on a cron schedule. Shared
rules live here so routine files don't restate them -- rely on this file instead of re-deriving.

## Cloud execution contract

Runs in the cloud, NOT on Ray's Mac:

- **No local machine** -- only the git checkout; no local files, services, or binaries. `yt-dlp`
  is unavailable (and blocked from cloud IPs). Get data from **MCP connectors** (VidTempla for
  YouTube, PostHog, etc.), attached to the trigger.
- **Ephemeral checkout** -- freshly cloned each run; writes persist only via commit/PR.
  Report-only routines post to Slack and do NOT commit. Repo/app-changing routines open a PR on a
  `claude/*` branch, never push to main.
- **Zero prior context** -- the routine file must state everything: inputs, steps, tools,
  definition of done.

## Posting to Slack ("bot tags")

Plain-text posts use `$SLACK_BOT_TOKEN`, available **only in "Default with Bots"**
(`env_017zJzRHaWjfEM5xVDisLSMV`). Canonical snippet -- reference it, don't re-paste:

```bash
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data '{"channel": "#<channel>", "text": "<message>"}'
```

- **Empty token** (`echo $SLACK_BOT_TOKEN` blank): write the summary to stdout and stop -- it
  lands in the run log. Never silently no-op.
- **Redaction (any error output):** replace `$SLACK_BOT_TOKEN` and any
  `Authorization:`/`Bearer`/`xox…` string with `[REDACTED]` before printing or posting.
- `mrkdwn`: `*bold*` (single asterisks), `_italic_`, `<url|text>`. Keep posts under ~2500 chars
  (Ray reads on his phone).
- **Slack MCP instead** only for Block Kit, file uploads, channel create/resolve, or reading
  history (e.g. `oakhouse-tokyo-watcher`, the ACS question round). Attach the Slack connector
  then. Plain text -> bot-token curl (no connector needed).

Known channels: `#yt-outlier`, `#yt-performance-audit`, `#acs-gaps`, `#acs-friction`,
`#acs-questions`, `#acs-interesting-findings`, `#tokyo-apartments`. If a channel is missing,
create it (`conversations.create`) or post to `#general` prefixed `[<channel> missing]` -- never
fail silently.

## Writing style (Slack + any Ray-facing output)

- **No em or en dashes** -- use `--`. (Exception: the trigger pointer prompt matches the fleet's
  literal wording.)
- Lists as **numbered lists, not tables**. Feature announcements lead with the feature. Never
  fabricate a number -- "not answerable with this data" is a valid result.

## Registering a routine (`/schedule` -> `RemoteTrigger`)

`list` / `get` / `create` / `update` / `run` (no delete -- use https://claude.ai/code/routines).
Fleet shape:

- **Prompt = thin pointer**, kept in git not inlined:
  `Read and execute @routines/<path>.md from the `ray-os` repo. That file is your full, self-contained instructions — follow it exactly.`
- **Environment:** `env_017zJzRHaWjfEM5xVDisLSMV` (Default with Bots) for anything that Slacks.
  Others: `env_01E98nkCDvBMU63T4u2xpJ2V` (Default), `env_01HK8ySVEB7u5tsKiNxMhCLD` (Full Access).
- **Session:** `model` usually `claude-opus-4-8[1m]` (lighter routines use a smaller model);
  `sources` = `https://github.com/ray-amjad/ray-os`; `allowed_tools` typically
  `["Bash","Read","Write","Edit","Glob","Grep"]` (+ `WebFetch`/`WebSearch`/`Task` when needed).
- **Cron is UTC**, min interval 1h. Ray is Asia/Tokyo (UTC+9): 9am JST = `0 0 * * *`. Convert and
  confirm.

### Connector UUIDs (`mcp_connections`; `name` must be `[a-zA-Z0-9_-]`)

| name | connector_uuid | url |
|------|----------------|-----|
| VidTempla | `45610a0d-6e97-46e8-87e6-01719b49fa24` | https://www.vidtempla.com/api/mcp |
| Slack | `4d0e023a-093f-4a97-a987-71d9c7d1df96` | https://mcp.slack.com/mcp |
| PostHog | `30f014da-bd35-4339-bc96-23398d2b40bd` | https://mcp.posthog.com/mcp |
| Exa-Advanced | `5b91dcfa-2f77-4488-97f4-6dc81c61ad1a` | https://mcp.exa.ai/mcp |
| Agentic-Coding-School | `bafd344a-25fc-4c7a-b321-d4f2d493f658` | https://www.agenticcoding.school/api/mcp |
| Supadata | `329f4895-85e1-45fa-afd1-5e1f559d1729` | https://api.supadata.ai/mcp |
| Gmail | `365d40cf-749c-4b8d-9e11-6fd819281416` | https://gmailmcp.googleapis.com/mcp/v1 |
| Notion | `2db5c7fe-d151-4eea-a5c9-02984bd1be86` | https://mcp.notion.com/mcp |

Attach only the connectors a routine uses -- do not over-grant.

## Reference implementations

- **YouTube + Slack, VidTempla data:** `youtube-outlier-research.md`, `youtube-performance-audit.md`.
- **Slack Block Kit + state-in-Slack:** `oakhouse-tokyo-watcher.md`.
- **Thin file-reading routines:** most of `acs/*.md`.
