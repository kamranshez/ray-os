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
| DAEMON + BRIDGE_MODE | /remoteControlServer | DCE'd out |
| HISTORY_SNIP | /force-snip | Stubbed (`isEnabled:()=>!1`) |
| WORKFLOW_SCRIPTS | /workflows | DCE'd out |
| KAIROS_GITHUB_WEBHOOKS | /subscribe-pr | DCE'd out |
| TORCH | /torch | DCE'd out |
| UDS_INBOX | /peers | DCE'd out |
| FORK_SUBAGENT | /fork | DCE'd out (fork telemetry exists but no command) |
| *(runtime)* | /ultrareview | In binary, GrowthBook-gated (`tengu_review_bughunter_config.enabled`) |

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