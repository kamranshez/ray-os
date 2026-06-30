
## 2026-06-21 14:11 — v2.1.185 (upgraded from v2.1.183)

**🔀 GrowthBook switches**
- Skills health dashboard (`tengu_skills_dashboard_enabled`) — was ON → now OFF _(via GrowthBook)_. Gates the `GET /api/claude_code/skills` health fetch that surfaces per-skill good/warn/poor status. Code still wired; just gated off for Ray's account now.

**🆕 New flags**
- None.

**🧱 DCE switches**
- `tengu_chert_bezel` — **code removed** (wired → stripped). The flag string no longer appears anywhere in the binary this build.
- `tengu_kairos_brief` — **retired from GrowthBook** (was wired). The "Brief" concise-output mode; the code remains in the binary, now reachable only via the `CLAUDE_CODE_BRIEF` env var.
- `tengu_kairos_brief_config` — **retired from GrowthBook** (was wired). Config payload for Brief mode; residual code still present.
- `tengu_neapolitan` — **retired from GrowthBook** (was wired). A git-state gate (checks cwd/HEAD, skips when CLAUDE_CODE_REMOTE); code still present (~2 hits), just no longer server-gated.

## 2026-06-21 14:50 — v2.1.185

No changes.

## 2026-06-26 16:45 — v2.1.193 (upgraded from v2.1.186)

> Note: the in-binary gate helper was renamed `ct(`→`it(` and telemetry `j(`→`G(` since the routine was written. GB-value switches + present/stripped DCE detection are unaffected and verified; wired-vs-present granularity was reconstructed manually via `it(`.

**🔀 GrowthBook switches**
- Artifacts publish (`tengu_cobalt_plinth`) — OFF → ON _(GrowthBook)_. Gates Claude Code artifact publishing: render an HTML artifact and publish it to a shareable URL (eligibility-gated; sibling flags do the direct/inline upload lane + read-version persistence). Wired.
- Fullscreen TUI default (`tengu_ochre_hollow`) — OFF → ON _(GrowthBook)_. Makes the new fullscreen, flicker-free TUI the default render mode (revert with `/tui default`). Wired.
- Review workflow routing (`tengu_review_workflow_routing`) — OFF → ON _(GrowthBook)_. Routes `/review`/`/code-review` through the workflow/ultra path with a local-effort fallback ("Running a local {effort} review and applying its findings") when cloud ultra isn't available. Wired.
- Claude-in-Chrome in-product permissions (`tengu_cfc_in_product_permissions`) — OFF → ON _(GrowthBook)_. In-product permissions UI for the Chrome extension; enumerates per-OS browser profile/data paths (macOS, Windows Roaming) to manage Claude-for-Chrome perms inside CC. Wired.
- Chrome auto-enable (`tengu_chrome_auto_enable`) — OFF → ON _(GrowthBook; env `CLAUDE_CODE_ENABLE_CFC`)_. Auto-offers/enables the Claude-in-Chrome extension when a paired browser/device is detected (shows chrome_auto_enable_prompt). Wired.
- 1h prompt-cache scope (`tengu_prompt_cache_1h_config`) — config changed (effective-off). Removed `"compact"` from the 1-hour prompt-cache allowlist; compaction no longer uses the extended 1h cache TTL.
- Bridge attestation level (`tengu_bridge_attestation_enforce_config`) — config changed (effective-off). Accepted device-attestation tier moved `VERIFIED_BY_GATE` → `VERIFIED_KEYLESS_DEVICE` for bridge attestation enforcement.

**🆕 New flags**
- `tengu_rewind_first_message` — GB **true / effective ON**, wired. Lets `/rewind` jump back to the first message via a persisted anchor even with no preceding assistant turn (persistAnchor vs precedingAssistantUuid).
- `tengu_ccr_delta_rehydrate` — GB **true / effective ON**, wired. CCR (remote/cloud) "delta rehydrate": incrementally rehydrates remote session state over the `/worker/events/stream` websocket.
- `tengu_team_discovery` — wired, off. Team/org MCP server auto-discovery ("allow_team_discovery") — surfaces MCP servers your org recommends via `/mcp`. (Also a newly-shipped DCE.)
- `tengu_fleetview_onboarding_v2` — wired, off. v2 onboarding for FleetView (the daemon/multi-agent "hand off a bigger task" column view).
- `tengu_amber_quill` — wired, off. Gates contextual tips (the allow_context_tips system that reads CLAUDE.md and surfaces inline tips).
- `tengu_cowork_chrome_automode_default` — wired, off. Defaults Claude-in-Chrome "auto mode" on in cowork (override `CLAUDE_CHROME_CLASSIFIER_FLOOR`).
- `tengu_cobalt_plinth_reader_persist` — wired, off. Persists artifact "read versions" (artifactReadVersions).
- `tengu_cobalt_plinth_direct` — wired, off. Artifact direct-upload lane: inline signed, no-auth publish (override `CLAUDE_CODE_ARTIFACT_DIRECT_UPLOAD`); falls back to signed lane.
- `tengu_fine_survey_transcript_ask_config` — config (prob 0.5), present. "Fine"-rated tier of the post-session survey that asks permission to share your transcript (sibling of bad_/good_); 50% ask rate.
- `tengu_long_context_survey_threshold` / `tengu_long_context_survey_question_variant` — config, present (defaults: threshold 5000, variant prob 0.2). Drive a long-context "How is Claude doing this session?" survey: when to ask + question wording.
- Stripped (name only, no code yet): `tengu_slate_meridian`, `tengu_tense_pond`, `tengu_lumen_thicket_q7`, `tengu_xq7_marble_zephyr`, `tengu_quartz_meadow`, `tengu_riverbed_lantern`, `tengu_copper_meadow`, `tengu_mcp_normalize_root_combinators` (last likely normalizes root-level JSON-schema combinators—anyOf/allOf/oneOf—in MCP tool schemas; not wired yet).

**🧱 DCE switches**
- `tengu_team_discovery` — newly shipped (stripped → present, wired). Team/org MCP discovery (see above).
- `tengu_silk_almanac` — newly shipped (stripped → present, wired). Team-memory **multistore** conflict handling (partitions, remoteHashes, team_memory_multistore_conflict, manifest-changed-mid-pull) for syncing shared team memory across stores.
- `tengu_cobalt_heron` — newly shipped (stripped → present, wired). Contextual tip: warns Pro users they're burning their weekly limit ~2× faster on Opus and suggests `/model`.
- `tengu_slate_moth` — newly shipped (stripped → present, wired). Contextual tip: when context >300k tokens with >100k stale-file tokens, suggests `/compact` to stop re-sending stale files.
- `tengu_orford_ness` — newly shipped (stripped → present). Org/enterprise managed-settings + error-tracking path ("your organization requires remote managed settings to load", Datadog error ingestion, subscription-switch).
- `tengu_billiard_aviary` — **code removed** (present → stripped). Was the remote-memory-directory selector (override `CLAUDE_CODE_REMOTE_MEMORY_DIR`); gone from the binary this build.
- `tengu_slate_fern` — **code removed** (present → stripped). Was the plugin/marketplace update nudge (returned a {days, sessions} reminder cadence for plugin marketplace updates); gone this build.

## 2026-06-28 16:40 — v2.1.195 (upgraded from v2.1.193)

NOTE: gate helper renamed `it(` → `at(` this build (telemetry now `j(`/`f_(`). Routine regex updated to match. Reclassified cleanly after a first buggy pass; counts below are correct.

### 🔀 GrowthBook switches
- **Artifact publishing** (`tengu_cobalt_plinth`) — ON → OFF. Gates the Artifacts feature (render an HTML page and publish/deploy it; CLAUDE_CODE_ARTIFACT, /api/frame/deploy). Team/enterprise-only behind `allow_cobalt_plinth`. Code still wired, gated off for Ray's account.
- **Artifact direct-upload lane** (`tengu_cobalt_plinth_direct`) — OFF → ON. Uploads the rendered artifact directly (inline lane) instead of via a signed URL. Wired. env CLAUDE_CODE_ARTIFACT_DIRECT_UPLOAD.
- **Precomputed compaction** (`tengu_sepia_moth`) — OFF → ON. Pre-warms the auto-compact summary ahead of time (`precomputeCompactionEnabled`) so compaction is ready when context fills. Wired.
- **Auto-compact token threshold** (`tengu_amber_redwood3`) — "1000000" → "" (cleared). Token count at which auto-compaction triggers (1M); now empty, falls back to redwood2/default. Wired.
- **Investigate-first clarifying questions** (`tengu_slate_harrier`) — "off" → "compact". Opus-4-7 only: whether Claude asks a clarifying question / investigates before acting (modes additive/compact/off). Wired. env CLAUDE_CODE_INVESTIGATE_FIRST.
- **Malformed tool-use clean retry** (`tengu_malformed_tool_use_clean_retry`) — OFF → ON. Retries a malformed tool_use block cleanly instead of erroring. Wired.
- **MCP large-output truncation prompt** (`tengu_mcp_subagent_prompt`) — OFF → ON. New MCP tool-result truncation/format-instructions prompt (Plain text / JSON-with-schema). Wired. env MCP_TRUNCATION_PROMPT_OVERRIDE.
- **Tool-list filtering** (`tengu_shale_finch`) — OFF → ON. Filters a specific subset of built-in tools out of the resolved toolset under certain conditions. Wired.
- **MCP root-combinator normalization** (`tengu_mcp_normalize_root_combinators`) — [] → ["learningcommons.org"]; ALSO newly wired (see DCE). Per-host allowlist that normalizes MCP server root URLs by hostname. Wired.
- **Bridge min client version** (`tengu_bridge_min_version`) — minVersion 2.1.70 → 2.1.139. Minimum CLI version for the remote-control "bridge" (CCR/remote driving); older clients refused. Config payload.
- **Long-context survey threshold** (`tengu_long_context_survey_threshold`) — "800000" → "" (cleared). Token count at which the "How is Claude doing this session?" survey fires. Off for Ray now.
- **Long-context survey question variant** (`tengu_long_context_survey_question_variant`) — "instruction_following" → "" (cleared). Which question variant that survey shows.

### 🆕 New flags
- **Shoji engine** (`tengu_shoji_engine`) — wired, off. New settings/config-resolution engine producing an "effective config + sources" view (touches usage accounting). Real code, gated off. env CLAUDE_CODE_SHOJI_ENGINE.
- **Per-model read-before-edit guard** (`tengu_velvet_hammer_opus_4_8`/`_opus_4_7`/`_opus_4_6`/`_fable_5`) — model-specific variants of `tengu_velvet_hammer`, which relaxes the "file must be Read before Edit" enforcement. Built at runtime via `${flag}_${model}`, so no literal string (classified "stripped") but functionally live via the base flag's per-model lookup. Per-model rollout scaffolding.
- **Per-model read-before-write guard** (`tengu_velvet_mallet_opus_4_8`/`_opus_4_7`/`_opus_4_6`/`_fable_5`) — same mechanism for the Write tool (relaxes "must Read before overwrite").
- **Report-findings tool** (`tengu_report_findings_tool`) — GB-only, stripped (no code yet). Name suggests an agent tool to report findings (review/bug-hunt). Upcoming, off.
- `tengu_slate_ibis` — GB value ON but no code in this build (stripped); purpose unrecoverable from binary, flipping is a no-op here.
- `tengu_linen_osprey`, `tengu_russet_linnet` — codename-only, stripped, off. No code/strings; purpose unrecoverable.

### 🧱 DCE switches
- **MCP root-combinator normalization** (`tengu_mcp_normalize_root_combinators`) — newly shipped (stripped → wired). Per-host MCP URL-normalization allowlist; also got its first host value (see switches).
- `tengu_velvet_cascade` — retired from GrowthBook (was wired). Per-model gate for the condensed "simple_system_prompt" (checks model against a `.models` list). Code still present in 2.1.195; now driven only by managed `simple_system_prompt` settings, not a server gate.
- `tengu_ladder_mq7`, `tengu_satin_quoll` — retired from GrowthBook (both already stripped/no code). Names gone server-side and no code in the binary; nothing changes, last purpose unrecoverable.

## 2026-06-29 — v2.1.195 (no version change)

### 🔀 GrowthBook switches
- **Default-async subagents** (`tengu_amber_heron`) — OFF → ON (via GrowthBook). In the Agent tool's launch path, this is one of the OR-terms that sets `is_async`: with it ON, a subagent spawned **without** an explicit `run_in_background` (and not a teammate) now defaults to running **asynchronously in the background** — the tool returns an `async_launched` status and notifies on completion instead of blocking the main loop. Code is wired, so the flip changes real behavior. Still overridden by `run_in_background:false`, teammate context, and `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`.

### 🆕 New flags
- `tengu_lapis_anchor_budget` — GB value **15000000** (15M), stripped (literal key not in this binary). Companion to `tengu_lapis_anchor`, which controls the injected `<total_tokens>…tokens left</total_tokens>` reminder (modes off/infinite/fixed/countdown; env `CLAUDE_CODE_TOTAL_TOKENS_REMINDER`). The `_budget` value is almost certainly the token budget used in "fixed" mode (binary's hardcoded fixed default is `Nwm=5000000` = 5M). Server-side config staged ahead of the code that reads it — no direct call site this build, so flipping it is a no-op here.
- `tengu_fleet_past_sessions` — GB false, stripped. Name ties to **FleetView** (the multi-agent fleet UI: `mountFleetView`, `FleetViewScreen`, `fleet_view_dispatch`). Probably gates a "past / historical sessions" view in the fleet manager. No direct call site in this build → upcoming/server-staged, off.
- `tengu_gorse_fathom` — GB false, stripped. Codename-only; no strings or code in the binary, purpose unrecoverable from this build. Off, no-op.

### 🧱 DCE switches
None.
