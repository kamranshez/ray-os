# routines/ -- shared conventions for cloud routines

Each `*.md` file here (and under `acs/`) is a **self-contained prompt for an unattended cloud
routine** -- an isolated Claude Code (CCR) session that Anthropic's cloud spawns on a cron
schedule. This file holds the conventions ALL routines share so individual routine files do not
each re-derive them. When writing or editing a routine, rely on what is documented here instead
of restating it.

## The cloud execution contract (read before writing any routine)

A routine runs in Anthropic's cloud, NOT on Ray's Mac. Therefore:

- **No local machine access** -- no local files outside the git checkout, no local services, no
  local env vars except what the environment provides (see `$SLACK_BOT_TOKEN` below).
- **No local binaries** -- `yt-dlp` and other locally-installed tools are NOT available (and
  yt-dlp is blocked from cloud IPs regardless). Get data from **MCP connectors** instead
  (VidTempla for YouTube, PostHog, Stripe, etc.). A routine that needs a service must have that
  connector attached to its trigger (see "Registering a routine").
- **Ephemeral checkout** -- the repo is freshly cloned each run. Writes only persist if the
  routine commits/opens a PR. Report-style routines that just post to Slack should NOT commit;
  routines that change the repo/app open a PR on a `claude/*` branch and never push to main.
- **Self-contained** -- the session starts with zero prior context. The routine file must say
  everything: inputs, steps, tools, and definition of done.

## Posting to Slack -- the canonical idiom ("bot tags")

Simple text posts use the `SLACK_BOT_TOKEN` env var, available **only in the "Default with
Bots" environment** (`env_017zJzRHaWjfEM5xVDisLSMV`). This is the single source of truth for the
snippet -- routine files should reference it, not paste their own variant:

```bash
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data '{"channel": "#<channel>", "text": "<message>"}'
```

- **Fallback:** if `echo $SLACK_BOT_TOKEN` is empty, write the summary to stdout and stop -- it
  lands in the run log. Never silently no-op.
- Slack `mrkdwn` is supported (`*bold*`, `_italic_`, `<url|text>`). Keep phone-friendly posts
  under ~2500 chars.
- **When to use the Slack MCP instead:** only if the routine needs Block Kit blocks, file
  uploads, channel resolution, or reading history (e.g. Oakhouse's per-listing cards, the ACS
  question-round canvas). Then attach the Slack connector and use `slack_*` tools. For plain
  text, prefer the bot-token curl -- it needs no connector.

Known channels: `#yt-outlier`, `#yt-performance-audit`, `#acs-questions`, `#acs-infra`,
`#tokyo-apartments`. Resolve a channel by name if unsure; if missing, post to `#general`
prefixed `[<channel> missing]` rather than failing.

## Writing style (applies to Slack posts and any Ray-facing output)

- **Never use em or en dashes** in Ray-facing content -- use `--`. (The one exception is the
  trigger's pointer prompt, which matches the existing fleet's literal wording; see below.)
- Present idea/title lists as **numbered lists, not tables**.
- Feature announcements lead with the feature, not a meta/expose angle.
- Never fabricate a number. "Not answerable with this data" is a valid, useful result.

## Registering a routine (the trigger)

Triggers are managed with the **`/schedule` skill** (which drives the `RemoteTrigger` tool:
`list` / `get` / `create` / `update` / `run`). You cannot delete via the tool -- use
https://claude.ai/code/routines. The whole fleet follows one shape:

- **Prompt = thin pointer.** The trigger's message is almost always:
  `Read and execute @routines/<path>.md from the `ray-os` repo. That file is your full, self-contained instructions — follow it exactly.`
  Keep the logic in the routine file (versioned in git), not inlined in the trigger. (Inlining
  the whole prompt, like the old "YouTube Format Scout" did, means editing it lives outside git
  and rots when files move.)
- **Environment:** `env_017zJzRHaWjfEM5xVDisLSMV` ("Default with Bots") for anything that Slacks
  via bot token. Others: `env_01E98nkCDvBMU63T4u2xpJ2V` ("Default"),
  `env_01HK8ySVEB7u5tsKiNxMhCLD` ("Full Access").
- **Session context:** `model` defaults across the fleet to `claude-opus-4-8[1m]` (or
  `claude-opus-4-8`); light routines use `claude-sonnet-4-6` / `claude-haiku-*`. `sources` =
  `https://github.com/ray-amjad/ray-os` (add the app repo if the routine touches it).
  `allowed_tools` is typically `["Bash","Read","Write","Edit","Glob","Grep"]` (+ `WebFetch`/
  `WebSearch`/`Task` when needed).
- **Cron is UTC**, minimum interval 1 hour. Ray is Asia/Tokyo (UTC+9): 9am JST = `0 0 * * *`.
  Always convert and confirm the local<->UTC mapping.

### Common connector UUIDs (for `mcp_connections`)

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

The `name` must match `[a-zA-Z0-9_-]` only (no dots/spaces). Attach only the connectors a
routine actually uses -- do not over-grant.

## Reference implementations

- **YouTube + Slack, bot-token, VidTempla data:** `youtube-outlier-research.md`,
  `youtube-performance-audit.md`.
- **Slack Block Kit + state-in-Slack:** `oakhouse-tokyo-watcher.md`.
- **Read-a-file thin routines:** most of `acs/*.md`.
