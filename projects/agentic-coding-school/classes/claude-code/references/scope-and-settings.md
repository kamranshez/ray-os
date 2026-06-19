## Config Scopes

Precedence, highest to lowest:

1. **Managed** — server-managed / MDM / policy-level
2. **Command line arguments**
3. **Local** — `.claude/settings.local.json` (per-machine, gitignored)
4. **Project** — `.claude/settings.json` (shared, checked into source control)
5. **User** — `~/.claude/settings.json` (global personal defaults)

## All Config Files

| File                          | Purpose                                             |
| ----------------------------- | --------------------------------------------------- |
| `~/.claude/settings.json`     | User-wide defaults across all projects              |
| `.claude/settings.json`       | Shared repo/team settings (commit this)             |
| `.claude/settings.local.json` | Private per-machine overrides (auto-gitignored)     |
| `~/.claude.json`              | Global state — theme, OAuth, editor mode, MCP state |
| `.mcp.json`                   | Project MCP servers                                 |
| `CLAUDE.md`                   | Instructions/context, not JSON settings             |
## Override vs Merge

**Scalars override** — `model`, `language`, `outputStyle` → most specific scope wins.

**Arrays merge** — `permissions.allow`, `permissions.deny`, `permissions.ask`, sandbox paths, hook allowlists → concatenated and deduplicated across all scopes.

## Examples

### Simple override: `model`

```json
// ~/.claude/settings.json     → "claude-sonnet-4-6"
// .claude/settings.json       → "claude-opus-4-6"
// .claude/settings.local.json → "claude-haiku-4-5"
```

Effective result: `claude-haiku-4-5` (local wins).

### Arrays merge: `permissions.allow`

```json
// ~/.claude/settings.json     → ["Bash(npm run lint)"]
// .claude/settings.json       → ["Bash(npm run test *)"]
// .claude/settings.local.json → ["Read(~/.zshrc)"]
```

Effective result: all three rules combined.

### Conflict: allow in user, deny in project

```json
// ~/.claude/settings.json  → permissions.allow: ["Read(./.env)"]
// .claude/settings.json    → permissions.deny:  ["Read(./.env)"]
```

Result: blocked. The project deny wins over the broader user allow.

### Disabling hooks locally

```json
// .claude/settings.json       → hooks configured for team
// .claude/settings.local.json → { "disableAllHooks": true }
```

Hooks disabled for you only, teammates unaffected.

### User-wide default, project exception

```json
// ~/.claude/settings.json → { "language": "japanese" }
// .claude/settings.json   → { "language": "english" }
```

That repo: English. Everywhere else: Japanese.
## Realistic Pattern

```json
// .claude/settings.json (team)
{
  "model": "claude-sonnet-4-6",
  "outputStyle": "Explanatory",
  "permissions": {
    "deny": ["Read(./.env)", "Read(./secrets/**)"]
  }
}
```

```json
// .claude/settings.local.json (you)
{
  "outputStyle": "Concise",
  "permissions": {
    "allow": ["Bash(npm run dev)"]
  }
}
```

Effective: model stays sonnet, output becomes concise, team deny rules still apply, your extra allow gets added.

## Managed Settings — Where They Come From

The "Managed" scope (highest precedence) is the admin/IT-controlled layer. It can come from three places:

**1. Server-managed settings**
Pushed from Anthropic's servers via the Claude.ai admin console.

**2. MDM / OS-level policies**

| OS                      | Location                                                      |
| ----------------------- | ------------------------------------------------------------- |
| macOS                   | `com.anthropic.claudecode` managed preferences domain         |
| Windows                 | `HKLM\SOFTWARE\Policies\ClaudeCode` → `Settings` value (JSON) |
| Windows (user fallback) | `HKCU\SOFTWARE\Policies\ClaudeCode`                           |

**3. System-level files**

| OS | Path |
|----|------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux / WSL | `/etc/claude-code/managed-settings.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` |
