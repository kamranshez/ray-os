You are checking which hidden/unreleased Claude Code features have changed status. Use the binary-explorer skill to extract and search the current Claude Code binary.

**Step 1: Extract the binary**
Run: `bash /Users/ray/.claude/skills/binary-explorer/scripts/extract.sh`

**Step 2: Check each feature's status**
Search the extracted strings file for these feature-gated commands and determine if they're now registered, enabled, or still stripped:

| Feature Flag | Command | Last Known Status |
|---|---|---|
| KAIROS_BRIEF | /brief | In binary, GrowthBook-gated OFF (`tengu_kairos_brief_config` default `enable_slash_command: false`) |
| PROACTIVE | /proactive | DCE'd out — not in binary |
| KAIROS | /assistant | DCE'd out — not in binary |
| BRIDGE_MODE | /bridge | Partial — `bridge-kick` internal only |
| *(runtime)* | /daemon | Registered (type:local-jsx). Desc: "Manage background services: assistants, scheduled tasks, and remote control" |
| HISTORY_SNIP | /force-snip | DCE'd out — not in binary |
| tengu_workflows_enabled | /workflows | Registered (type:local-jsx), gated by `tengu_workflows_enabled` (GB default ON) + `CLAUDE_CODE_WORKFLOWS` env. Desc: "Browse workflow history (running and completed)" |
| KAIROS_GITHUB_WEBHOOKS | /subscribe-pr | DCE'd out |
| TORCH | /torch | DCE'd out (telemetry refs exist but no command) |
| UDS_INBOX | /peers | DCE'd out |
| FORK_SUBAGENT | /fork | Registered command ("Spawn a background agent that inherits the full conversation"), gated by `tengu_copper_fox` (GB) + `CLAUDE_CODE_FORK_SUBAGENT` env var + internal 'ant' source, default OFF |
| *(runtime)* | /ultrareview | In binary, GrowthBook-gated (`tengu_review_bughunter_config.enabled`) |
| *(runtime)* | /ultraplan | In binary, GrowthBook-gated (`tengu_ultraplan_config.enabled`), remote plan refinement |
| SEDGE_LANTERN | /recap | In binary, GrowthBook-gated ON by default (`tengu_sedge_lantern`), session recap + away summary |
| *(none)* | /background | Registered (alias /bg), always enabled. Desc: "Send this session to the background and free the terminal" |
| *(runtime)* | /advisor | Registered. Desc: "Configure the Advisor Tool to consult a stronger model for guidance at key moments during a task" |
| *(runtime)* | /autofix-pr | Registered, requires GitHub App installed. Desc: "Monitor and autofix any issues with the current PR" |
| tengu_velvet_static | /radio | Registered but hidden, gated OFF. Desc: "Listen to Claude FM lo-fi radio" |
| *(disabled)* | /loops | Registered but isEnabled:false. Desc: "List, create, and delete recurring loops and stop-hooks" |
| allow_remote_sessions | /teleport | Registered, gated by allow_remote_sessions. Desc: "Resume a Claude Code session from claude.ai" |

For each one:
- `grep -c 'name:"<command>"' <strings_file>` to check if registered
- `grep 'isEnabled.*!1\|isEnabled.*!0\|isEnabled.*false\|isEnabled.*true' <strings_file>` near the command for gating
- Check for new GrowthBook config keys (`tengu_*`) that weren't there before

**Step 3: Report changes only**
Compare against the "Last Known Status" column. If anything has changed (newly appeared, gating relaxed, new config keys), that's news. If nothing changed, say so.

**Step 4: Send via Telegram**
  Use the telegram-message skill to send findings. Run:

  ```bash
  bash ~/.claude/skills/telegram-message/scripts/send-message.sh "<message>"

  If changes found:
  🔔 Claude Code Feature Update (v{version})

  🟢 NEW: /command — now in binary, gated by X
  🔄 CHANGED: /command — was stubbed, now enabled
  ⚪ Still locked: /brief, /torch, etc.

  If no changes:
  ⚪ Claude Code v{version} — no feature flag changes since last check