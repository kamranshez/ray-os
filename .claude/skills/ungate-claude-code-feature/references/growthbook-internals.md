# GrowthBook feature-flag internals (Claude Code)

Everything the `ungate-claude-code-feature` skill needs about how Claude Code
gates features. Verified against CLI 2.1.147 (May 2026). Minified symbol names
rotate every release — **search the binary by the stable string literals**, not
by symbol names.

## Contents
- The flag service (endpoint, request, response)
- How a gate resolves
- The three ungate methods
- The local flag cache
- Verifying

## The flag service

Claude Code uses **GrowthBook in remote-eval mode against Anthropic's own API** —
not `cdn.growthbook.io`, and not Statsig. (`cdn.growthbook.io` appears in the
binary only as the SDK's unused default; no traffic goes there.)

- Endpoint: `POST https://api.anthropic.com/api/eval/sdk-<clientKey>`
  `<clientKey>` is a hardcoded literal in the binary (e.g. `sdk-zAZezfDKGoZuXXKe`).
  Grep the binary for `sdk-` to get the current one.
- Request body: `{attributes, forcedVariations, forcedFeatures, url}`. `attributes`
  carries deviceId, sessionId, platform, organizationUUID, accountUUID, userType,
  subscriptionType, appVersion, email. No specific flags are requested — the
  endpoint returns every feature evaluated for those attributes.
- Auth header is the user's own session credential (OAuth `Authorization: Bearer`
  or `x-api-key`). Proxyman will display it — that is the user's own token.
- Response: JSON with a top-level `features` map keyed by **plaintext** flag names:

      { "features": {
          "tengu_workflows_enabled": {
            "source": "force", "experiment": null, "on": true,
            "ruleId": "fr_...", "off": false, "value": true,
            "experimentResult": null
          }, ...
      } }

  The payload is plaintext — the CLI does not pass a GrowthBook `decryptionKey`,
  so there is no `encryptedFeatures` blob. If a future build adds one, plaintext
  rewriting stops working and you would need the key.

## How a gate resolves

The flag accessor returns, from the cached features:

    "value" in entry ? entry.value : entry.defaultValue

…or the **`default`** argument passed by the caller if the flag is unknown or
GrowthBook is disabled. Forcing a flag means making the response contain
`features[flag]` with the `value` (or `defaultValue`) you want.

A feature's `isEnabled()` is usually an AND of:

1. **An env-var opt-in** — `process.env.CLAUDE_CODE_<FEATURE>` must be truthy.
   Checked first, no network component. If the feature has one, it must be set in
   the Claude Code process environment; forcing the flag alone is not enough.
2. **The GrowthBook flag** — `flagLookup("tengu_<feature>", <default>)`.

Many gated features have a coded **default of `true`**; Anthropic ships the flag
only to *disable* the feature for accounts outside the rollout. That is why
methods 2 and 3 below work at all.

Subagent note: an internal filter keeps some tools out of *subagent* tool-lists so
only the top-level orchestrator can use them. A successful ungate still surfaces
the feature in the **main** interactive session — that filter is not part of the
flag gate, so do not let it confuse verification.

## The three ungate methods

All three still require the feature's env-var opt-in, if it has one.

### 1. Proxyman scripting rule (default)
Rewrite the response so `features[flag]` is forced on. Persistent, visible,
surgical — other flags untouched. This is what `assets/flag-forcer-rule.js` does.

### 2. Block the eval endpoint
Blacklist the exact path `https://api.anthropic.com/api/eval/sdk-*` (Proxyman
block-list, or map to a 4xx). The fetch fails, the features cache stays empty, and
the lookup returns each flag's `default`. Simple, but it flips *every* defaulted
flag, and only works for flags whose default is `true`. Never block all of
`api.anthropic.com` — that kills the model API.

### 3. DISABLE_TELEMETRY env var
`DISABLE_TELEMETRY=1` (also `DO_NOT_TRACK=1`,
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, `DISABLE_GROWTHBOOK=1`) makes
`isGrowthBookEnabled()` false. GrowthBook never initialises, so the lookup returns
every flag's `default`. One env var, no Proxyman. Same caveat as method 2 —
defaults only — and the `/api/eval/` request never fires, so there is nothing for
a Proxyman demo to show.

## The local flag cache

After a successful fetch the features are cached in the CLI config file —
`~/.claude.json` (or `$CLAUDE_CONFIG_DIR/.claude.json`) under
`cachedGrowthBookFeatures`. You can edit it directly, but the CLI overwrites it
after the next successful fetch (~every 6h) and guards writes to that file — back
it up first. The Proxyman rule is more reliable because it re-applies on every
fetch.

## Verifying

Confirm at two layers:

- **HTTP** — capture the `/api/eval/sdk-*` flow and check the flag with
  `scripts/check_flag_in_har.py`. A forced flag shows `source:"force"` and
  `ruleId:null`; the server's own forced flags carry a real `ruleId:"fr_..."`.
- **UX** — the feature's user-visible surface appears: a slash command, a tool, a
  menu entry. This is the real confirmation that the gate opened.
