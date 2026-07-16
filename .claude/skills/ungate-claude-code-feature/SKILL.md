---
name: ungate-claude-code-feature
description: >-
  Enable a gated, experimental, or staged-rollout Claude Code feature on your own
  machine by finding its GrowthBook feature flag in the binary and force-enabling
  it through a Proxyman interception rule (with an optional disk-cache fast-path).
  Use this skill whenever the user wants to ungate, unlock, force-enable, or "turn
  on" a Claude Code feature hidden behind a flag — phrasings like "ungate the X
  feature", "enable ultrareview", "unlock [feature name]", "turn on [feature]",
  "enable the workflow/agent tool", "this feature won't show up even with the env
  var", "force-enable a tengu_ flag", "flip the flag for X", "intercept the feature
  flag", "unlock a beta Claude Code feature", or any case where a Claude Code
  feature is gated and the user wants it on. Also trigger when the user references
  a specific tengu_ flag name, or the existing "GrowthBook Flag Enabler" Proxyman
  rule, or wants to add another flag to it. For the user's own Claude Code install
  and account.
---

# Ungate a Claude Code feature

Claude Code ships many features behind **GrowthBook feature flags** (`tengu_*`)
so Anthropic can roll them out gradually. A flag-gated feature stays invisible on
your machine until Anthropic enables the flag for your account — even if you set
the feature's opt-in env var. This skill flips the flag locally by intercepting
Claude Code's flag-fetch request with Proxyman, and optionally seeding the local
disk cache so the feature is live on the very first read.

It works on **your own machine and your own authenticated account**. Gated
features are often gated because they are unstable or token-heavy — treat
anything you ungate as beta. Do not use this to misrepresent paid entitlements.

## How feature gating works — the three tiers

Before touching anything, work out **which tier** is blocking the feature. Only
one of the three can be unlocked client-side.

### Tier 1 — Compile-time Dead Code Elimination (DCE)
- `feature()` from `bun:bundle` strips code at build time:
  `if (feature('KAIROS')) { ... }` — if false at build, the block is gone.
- **Cannot be unlocked.** The code literally does not exist in the binary.

### Tier 2 — Runtime GrowthBook flags
- `getFeatureValue_CACHED_MAY_BE_STALE('<flag>', <default>)` (minified, e.g.
  `lT("<flag>", null)`). Server evaluates flags via
  `POST https://api.anthropic.com/api/eval/sdk-<clientKey>`; values cache to
  `~/.claude.json` under `cachedGrowthBookFeatures`.
- **CAN be unlocked** — this skill targets exactly this tier.

### Tier 3 — Server-side enforcement
- Some features make a server call *after* the flag check (e.g.
  `/v1/ultrareview/quota`). If the server rejects, no client trick fixes it.
- **Partially unlockable** — the UI/command appears, but the backend call may fail.

### Ant-only overrides (do not work for you)
`CLAUDE_INTERNAL_FC_OVERRIDES` and `growthBookOverrides` are guarded by
`process.env.USER_TYPE === 'ant'`. External users must use Proxyman interception,
which is what this skill does.

## The 30-second runtime model

At startup Claude Code POSTs to a GrowthBook remote-eval endpoint and caches the
result. A gated feature's `isEnabled()` is usually an AND of two things:

    isEnvVarSet(CLAUDE_CODE_<FEATURE>)  AND  flagLookup("tengu_<feature>", <default>)

- The flag lookup reads the cached GrowthBook value, or returns `<default>` if the
  flag is unknown or GrowthBook is disabled.
- Many flags **default to `true`** — Anthropic ships the flag only to *disable* the
  feature for accounts outside the rollout. That detail is why the alternate
  methods (block the endpoint / disable GrowthBook) work at all.
- If the feature has an env-var gate, **forcing the flag alone is not enough** —
  the env var must also be set in the Claude Code process (Phase 3).

Full mechanics — endpoint, request/response schema, env-var behaviour, the local
cache file — are in `references/growthbook-internals.md`. Read it when you need
detail or something does not match what you see.

## Workflow

Five phases. Phases 1, 2 and 5 change per feature; 3 and 4 are mechanical.

### Phase 1 — Identify the gate

You need three facts about the target feature: its **env-var gate** (if any), its
**GrowthBook flag name**, and its **user-visible surface** (a slash command or
tool to look for, to confirm success).

Spawn a subagent to reverse-engineer the Claude Code binary — the
**`claude-binary-explorer`** skill is built for exactly this (it knows Claude
Code's mangled variable conventions; fall back to `binary-explorer` only if that
is unavailable). Tell it to find:

- The feature's gate: an env check `process.env.CLAUDE_CODE_<FEATURE>` AND a flag
  lookup `someFn("tengu_<feature>", <default>)`, plus tool/command registrations
  with an `isEnabled` that calls that gate.
- The exact `tengu_*` flag string and its coded default value.
- What the user sees when it is on — a `/command`, a tool name, a menu entry.

Minified symbol names rotate every release, so have the subagent **search by the
stable string literals**: `tengu_`, `/api/eval/`, `CLAUDE_CODE_`, `growthbook`,
and the feature's marketing name.

Locating the binary: `which claude` is often a wrapper (e.g. cmux). Resolve the
real one — usually `~/.nvm/.../node_modules/@anthropic-ai/claude-code/bin/claude.exe`
or the npm global install. Re-resolve every run; the path changes with each version.

### Phase 2 — Assess feasibility and report

Map what Phase 1 found onto the three tiers and give the user a verdict **before**
doing any work:

| Check | Finding |
|-------|---------|
| Code in binary (survived DCE)? | Yes/No — what substantial code was found |
| GrowthBook flag | `<flag_name>` + expected shape (boolean, or object + field) |
| Server-side calls after the flag? | Yes/No — which endpoints |
| **Verdict** | **Unlockable / Partially / No** |

- **No** (Tier 1 / code stripped): stop here. Explain that the code isn't in the
  binary and what would need to change. Do not proceed to Proxyman.
- **Partially** (Tier 3): warn that the command/UI will appear but the server call
  may fail with "not enabled for your account", then proceed if the user wants the
  surface anyway.
- **Unlockable** (pure Tier 2): proceed.

Determine the **forced value shape** from the flag check:
- `cfg?.enabled === true` → object, force `{ "enabled": true }`
- `cfg?.someField` → object, force `{ "someField": <value> }`
- `value === true` → boolean, force `true`

### Phase 3 — Force the flag with Proxyman

Default method: a Proxyman **scripting rule** that rewrites the flag-fetch
response. It persists across sessions, re-applies on every fetch, and is visible
on camera.

1. Confirm Proxyman is up and the cert is trusted: `get_proxy_status`,
   `get_certificate_status`.
2. Ensure `api.anthropic.com` is in the SSL-decrypt list (`get_ssl_proxying_list`;
   add with `toggle_ssl_proxying_domain` or `enable_ssl_proxying` if missing).
3. Find the flag-forcer rule: `list_rules` with `rule_type: "scripting"`, look for
   one whose URL contains `/api/eval/` (usually named "GrowthBook Flag Enabler").
   - **If it exists:** read its script at
     `~/Library/Application Support/com.proxyman.NSProxy/scripts/<RULE_ID>.js`,
     add the new flag to the `FORCED` map, push the full script back with
     `update_scripting_rule`.
   - **If it does not exist:** create it with `create_scripting_rule`, URL
     `https://api.anthropic.com/api/eval/*`, script body from
     `assets/flag-forcer-rule.js`.
   - **If the existing rule is in an older hand-coded form** (per-flag `if` blocks
     rather than a `FORCED` map): replace it with `assets/flag-forcer-rule.js`,
     carrying over **every** flag it was already forcing, then add the new one.
4. `FORCED` keys are flag names; values are the forced value — a boolean for a
   simple on/off gate, an object for a config flag (objects merge into the
   server's value so timeouts/limits survive). See the asset's comments.

Two alternatives (detail in `references/growthbook-internals.md`): blocking the
eval endpoint, and `DISABLE_TELEMETRY=1`. Both rely on the flag's default and flip
*every* defaulted flag, not just yours. Mention them, but use the scripting rule
unless the user asks otherwise.

**Optional disk-cache fast-path.** The Proxyman rule only takes effect after the
next eval fetch. To have the feature live on the *first* read of a fresh session,
also seed `~/.claude.json` (back it up first — the CLI guards and periodically
overwrites this file):

```bash
python3 -c "
import json, shutil
shutil.copy2('$HOME/.claude.json', '$HOME/.claude.json.backup')
with open('$HOME/.claude.json') as f: data = json.load(f)
cached = data.get('cachedGrowthBookFeatures', {})
cfg = cached.get('<FLAG>', {})
if isinstance(cfg, dict): cfg['<FIELD>'] = <VALUE>   # object config
else: cfg = <VALUE>                                   # boolean flag
cached['<FLAG>'] = cfg
data['cachedGrowthBookFeatures'] = cached
with open('$HOME/.claude.json','w') as f: json.dump(data, f, indent=2)
print('Patched. Backup at ~/.claude.json.backup')
"
```

The Proxyman rule is the durable mechanism; the cache patch is just a head-start.

### Phase 4 — Run Claude Code through the proxy

The interception only fires for a Claude Code process pointed at the proxy. Give
the user this for a fresh terminal:

    export HTTP_PROXY="http://127.0.0.1:9090"
    export HTTPS_PROXY="http://127.0.0.1:9090"
    export NO_PROXY="localhost,127.0.0.1"
    export NODE_EXTRA_CA_CERTS="$HOME/Library/Application Support/com.proxyman.NSProxy/app-data/proxyman-ca.pem"
    export CLAUDE_CODE_<FEATURE>=1     # the feature's own env-var gate, if it has one
    claude

Alternatively, open a Proxyman-injected terminal for them with
`mcp__proxyman__inject_terminal` (`terminal_app: "apple_terminal"`) and have them
run `claude` there — same effect, the env vars are injected for you.

Do **not** set `DISABLE_TELEMETRY=1` here — it suppresses the flag-fetch request
entirely, so the Proxyman rule has nothing to intercept.

### Phase 5 — Verify

Confirm at two layers:

1. **HTTP** — with a session running through the proxy, capture the flow:
   `filter_flows` for url containing `/api/eval/sdk-`, then `export_flows` that
   flow id to a `.har`. Run
   `python3 scripts/check_flag_in_har.py <har-file> <flag-name>` — it decodes the
   base64/gzip response body and reports the flag's presence and value. A forced
   flag shows `source:"force"` and `ruleId:null`; the server's own forced flags
   carry a real `ruleId:"fr_..."`.
2. **UX** — the feature's user-visible surface from Phase 1 appears: the
   `/command` shows up, the tool is callable, the menu entry is there. **This is
   the real proof.** Note: an internal filter keeps some tools out of *subagent*
   tool-lists, so verify in the **main** interactive session, not a subagent.

## Report

Summarize: the **feature** unlocked, the **flag** name, the **injected value**,
the **Proxyman rule ID** (for future management), any **server-side caveats**, and
**persistence** — the rule survives across sessions, but Claude Code must always
be launched from a proxy-pointed terminal.

## Known flags and their shapes

Flags already reverse-engineered. `TBD` = shape not yet confirmed; verify in the
binary before forcing.

| Flag | Force value | Server-side calls | Status |
|------|-------------|-------------------|--------|
| `tengu_workflows_enabled` | `true` (boolean) | None | Unlockable — Workflow tool + `/workflows` |
| `tengu_review_bughunter_config` | `{ "enabled": true }` | `/v1/ultrareview/quota` | Partially — `/ultrareview` |
| `tengu_kairos_brief_config` | `{ "enable_slash_command": true }` | None (entitlement via `isBriefEntitled()`) | Unlockable |
| `tengu_kairos_brief` | `true` (boolean) | None | Unlockable |
| `tengu_onyx_plover` | `{ "enabled": true }` | None (also `autoDreamEnabled` in settings.json) | Unlockable |
| `tengu_session_memory` | `true` (boolean) | None | Unlockable |
| `tengu_chomp_inflection` | TBD | None | Unlockable |
| `tengu_slate_heron` | TBD | None | Unlockable |
| `tengu_passport_quail` | TBD | None | Unlockable |
| `tengu_destructive_command_warning` | TBD | None | Unlockable |

## Adding more flags later

The `FORCED` map is cumulative. Ungating a second feature is just Phase 1 (find
its flag) plus one new entry in the map — the existing forced flags stay put.

## Troubleshooting

- **Feature still not showing**: confirm Claude Code was launched from the proxied
  terminal — `env | grep HTTPS_PROXY` should show port 9090 — and that the
  feature's `CLAUDE_CODE_<FEATURE>` env var (if any) is set.
- **Proxyman not intercepting**: verify SSL proxying is enabled for
  `api.anthropic.com` and the scripting rule is active (`list_rules`,
  `toggle_rule`).
- **Cache keeps reverting**: the rule isn't matching the response shape — run
  `get_flow_detail` on the `/api/eval/sdk-` flow to see the actual JSON and adjust.
- **"Not enabled for your account"**: a Tier 3 server-side entitlement check is
  failing — this cannot be bypassed via proxy.
