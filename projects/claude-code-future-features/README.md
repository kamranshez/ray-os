---
tags: [claude-code, reverse-engineering, gated-features, feature-flags, growthbook]
aliases: [claude-code-future-features, cc-future-features, gated-feature-tracker]
date: 2026-07-12
---

Tracking Claude Code's **unreleased / gated / hidden features** across versions — what exists behind flags and env vars, how each works, whether it can be unlocked locally, and which are worth a video.

This is a recurring local routine (see [[reference_cc_gated_feature_scan]]). Each new Claude Code release, re-run the scan, diff against the last version's catalogue, and log what's new.

## Folder layout

- `by-version/<version>.md` — full per-release catalogue of gated features, grouped by cluster, with a rollout-state legend. Diff consecutive versions to see what landed / shipped / disappeared.
- `features/<feature>.md` — self-contained deep-dives on individual features (e.g. `observer-agents.md`). Written when a feature is interesting enough to demo or make a video about.
- `flag-registry/<version>-*.{json,tsv,txt}` — raw evidence captured from the live GrowthBook eval response + binary, so findings are reproducible:
  - `*-eval-response.json` — the full decoded `/api/eval/sdk-<key>` response (every flag + its evaluated on/off/value for this account).
  - `*-gated-off.tsv` — just the flags evaluated OFF, with value shape.
  - `*-env-candidates.txt` — candidate `CLAUDE_CODE_*` env-var gates from the binary.

## How the two gating mechanisms work

Claude Code hides features two ways, often AND-ed together:

1. **GrowthBook feature flags** (`tengu_<colour>_<noun>` underscore codenames). Read at startup via a `POST https://api.anthropic.com/api/eval/sdk-<clientKey>`; the evaluated result caches to `~/.claude.json` under `cachedGrowthBookFeatures`. In the binary they're read via minified helpers `Qe(key,default)` / `w1` / `Ype` / `uG`.
2. **Env vars** (`CLAUDE_CODE_<FEATURE>`). A local opt-in the process reads directly. Many features gate on `envVarSet AND flagOn`.

Rollout state is read from the predicate shape:
- `return !1` (hardcoded false) = **dark** — not even flag-flippable; the switch is compiled shut.
- `Qe("tengu_x", false)` with no server call = **gated** — server-flippable, unlockable via Proxyman.
- `Qe(...) || CLAUDE_CODE_...` = an env var is a local override.
- A server call *after* the flag (e.g. `/v1/ultrareview/quota`) = **server-enforced** — UI may appear but the backend can still reject.

## The scan routine (per version)

1. **Extract strings:** `bash .claude/skills/binary-explorer/scripts/extract-claude.sh` → `~/.claude/cache/binary-strings/<version>.txt`.
2. **Capture the live flag registry (ground truth):** with Proxyman running (port 9090, cert trusted, `api.anthropic.com` SSL-decrypted), run a `claude` session through the proxy, then `filter_flows` for `/api/eval/sdk-`, `export_flows` to a HAR, and decode the response body → `flag-registry/<version>-eval-response.json`. This tells you exactly which flags exist and which are OFF for your account.
3. **Triage the OFF codenames against the binary:** most `tengu_*` names are opaque. Fan out subagents (haiku triage → sonnet explain) to classify each as a real *feature* vs model-routing / infra / experiment noise, and to describe how the real ones work.
4. **Cross-reference env vars:** grep `CLAUDE_CODE_*` in the strings; map each to the feature it gates and its paired flag.
5. **Write it up:** update `by-version/<version>.md`; promote anything demo-worthy to `features/`.

## Unlocking (for testing / demos)

See the `ungate-claude-code-feature` skill. The durable mechanism is the Proxyman scripting rule **`B3AD68CE`** ("GrowthBook Flag Enabler") at
`~/Library/Application Support/com.proxyman.NSProxy/scripts/B3AD68CE.js` — add a flag key to its `FORCED` map, push via `update_scripting_rule`, optionally seed `~/.claude.json` (back up first), then launch `claude` from a proxied terminal with the feature's `CLAUDE_CODE_*` env var set. Verify via `filter_flows` on `/api/eval/sdk-` (forced flags show `source:"force"`, `ruleId:null`).

## Confirmed working ungates (v2.1.207)

- **Kairos** brief/loop family — launched, slash command surfaces.
- **Observer agents** (`CLAUDE_CODE_EXPERIMENTAL_OBSERVER_AGENTS=1`) — confirmed working; the demo pair and its rig now live outside the vault at `~/Desktop/observer-demo/` (`.claude/agents/implementer.md` + `watchdog.md`, alongside the `tax.py` rig). Deep-dive: `features/observer-agents.md`.
- **Coordinator mode** (`CLAUDE_CODE_COORDINATOR_MODE=1`) — delegation-only orchestrator.

## Index

- [[2.1.209]] — **2.1.207 → 2.1.209 diff** (`by-version/2.1.209.md`): 34 flags added / 21 removed, 5 new env vars. Headline: **Artifact MCP** (`CLAUDE_CODE_ARTIFACT_MCP` — published claude.ai pages can call your MCP connectors at runtime). Also: Remote-Control "follow on your phone" nudges, memory self-rating write-back, Anthropic remote-override of official-plugin prompts, teleport branch guard. Kairos morning-brief and the Edit staleness flags (cedar_sundial/velvet_hammer) shipped and lost their gates.
- [[2.1.207-gated-flag-map]] — **full flag+env map** (`by-version/2.1.207-gated-flag-map.md`): 63 gated feature-flags + 36 env-var gates, ranked by video-worthiness, each with binary evidence and how to unlock. Built from the live GrowthBook eval capture.
- [[2.1.207-env-impact-map]] — **env-var impact ranking** (`by-version/2.1.207-env-impact-map.md`): all 402 `CLAUDE_CODE_*` vars triaged; 163 behavior-changers grouped major / moderate / minor by how big a change each makes.
- [[2.1.207]] — earlier narrative catalogue (`by-version/2.1.207.md`)
- [[observer-agents]] — observer/watchdog deep-dive (`features/observer-agents.md`)
- [[coordinator-mode]] — delegation-only orchestrator deep-dive (`features/coordinator-mode.md`)
