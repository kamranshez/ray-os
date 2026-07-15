
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

## 2026-06-30 — v2.1.196 (upgraded from v2.1.195)

*🔀 GrowthBook switches*
- **Cowork Chrome auto-mode default** (`tengu_cowork_chrome_automode_default`) — was OFF → now ON _(via GrowthBook)_. Gates the "chrome classifier floor" in Cowork's Claude-in-Chrome integration (`CLAUDE_CHROME_CLASSIFIER_FLOOR ?? it(...)`). With it on, Chrome browser actions in Cowork default to auto/permission mode driven by the permission classifier instead of prompting. Code still wired, so the flip is live for your account.

*🆕 New flags*
- `tengu_cobalt_plinth_putguard` — wired & ON. Part of the artifact-viewer/canvas module (sits next to `cobalt_plinth_fern`, `reader_persist`, `artifactViewerUrl`, `MAX_ARTIFACT_BYTES`). A guard on artifact PUT/persistence — write-protection when saving artifact state. _(wired, default on)_
- `tengu_plugin_binary_assets` — wired, OFF. Env `CLAUDE_CODE_PLUGIN_BINARY_ASSETS`. Lets plugins ship binary assets that get fetched and cached to a local `assetCacheDir`. _(wired/upcoming, gated off)_
- `tengu_mcp_path_scoped_permissions` — GB ON but stripped (no code). Path-scoped permissions for MCP tools (grant an MCP tool only within a path). Server-enabled but no call site this build → flipping is a no-op.
- `tengu_long_context_survey_probability` & `tengu_long_context_survey_trigger_mode` — present (data strings), effective off (gb=""). Part of the in-product micro-survey infra ("How is Claude doing this session?"). Control the sampling probability and the trigger condition for the long-context survey.
- `tengu_amber_packet`, `tengu_brass_sled` — stripped, OFF. Codenames reserved server-side; no binary code yet, behavior unknowable.
- `tengu_velvet_hammer_mythos_5`, `tengu_velvet_hammer_sonnet_4_6` — stripped, OFF. Per-model variants of the velvet_hammer Edit-tool string-match validation (Mythos / Sonnet 4.6). No code shipped for these model-specific variants.

*🧱 DCE switches*
- `tengu_report_findings_tool` — newly shipped (stripped → wired). Env `CLAUDE_CODE_REPORT_FINDINGS`. Structured "report findings" tool for review-style agents (tied to `/code-review` + reasoning-effort tiers); code now present, gated off by default.
- `tengu_russet_linnet` — newly shipped (stripped → wired). Env `CLAUDE_CODE_SKILL_DESC_REFRAME` ("skill_desc_reframe_arm_active"). Reframes/rewrites Skill tool descriptions before injection. Code now present, gated off.
- `tengu_lapis_anchor_budget` — newly shipped (stripped → wired). Env `CLAUDE_CODE_TOTAL_TOKENS_REMINDER_BUDGET`. The token-budget threshold companion to `tengu_lapis_anchor` (total-tokens reminder); now GB-configurable instead of hardcoded.
- `tengu_velvet_hammer` — gate retired (wired → present). Edit-tool fuzzy string-match validation pipeline (no_match/ambiguous/applies/lastRead). Gate call site removed; string survives only in the error-code telemetry list → behavior now unconditional.
- `tengu_velvet_mallet` — gate retired (wired → present). Write-tool read-before-write + subagent-md-report-block enforcement ("File has not been read yet"; "Subagents should return findings as text, not write report files"). Gate removed; behavior now unconditional.
- `tengu_event_watchdog_default_on` — code removed (wired → stripped). Defaulted an "event watchdog" on; string gone from this build, behavior retired.
- `tengu_slim_subagent_claudemd` — code removed (wired → stripped). Gave subagents a slimmed-down CLAUDE.md (reduced project-memory context for subagents); code gone this build.

## 2026-07-01 — v2.1.197 (upgraded from v2.1.196)

**🔀 GrowthBook switches**

- **Precompute compaction** (`tengu_sepia_moth`) — was ON → now OFF _(GrowthBook)_. Gates the `precomputeCompactionEnabled` behavior: precomputes the compacted conversation summary ahead of the compaction trigger so compaction is instant, and exposes a "Precompute compaction" toggle in settings. Code still wired; just gated off for your account now.
- **Auto-mode stage-1 classifier hardening** (`tengu_auto_mode_config`) — payload changed _(GrowthBook)_. Added `s1SuffixByModel` for `claude-sonnet-5` / `claude-sonnet-5[1m]`: the new stage-1 prompt suffix tells the auto-mode (YOLO) permission classifier to judge an action by its full effect (what it runs/sends/publishes/enables), block if ANY rule could apply, and NOT apply user-intent/ALLOW exceptions (stage 2 handles those). Wired; effective off for you (auto mode).
- **MCP root-combinator normalization** (`tengu_mcp_normalize_root_combinators`) — `["learningcommons.org"] → ["*"]` _(GrowthBook)_. Controls which MCP-server URL hostnames get root/OAuth-URL "combinator" normalization. Now applies to ALL hostnames (`*`) instead of one test domain. Wired.
- **Bridge attestation config** (`tengu_bridge_attestation_enforce_config`) — `accept_level: VERIFIED_KEYLESS_DEVICE → VERIFIED_BY_GATE` _(GrowthBook)_. Device/bridge attestation security policy; when the parent `tengu_bridge_attestation_enforce` gate is on, defines the accepted attestation level. Now accepts "verified by gate" instead of "verified keyless device". Wired but gated off for you.
- **Canary version stamp** (`tengu_canary`) — `{} → {external: "2.1.197"}` _(GrowthBook)_. Staged-rollout / canary marker tracking which build version is canaried; just bumped to the new version. Wired, effective off.
- **Feature of the week** (`tengu_lilac_loom`) — `{} → null` _(GrowthBook)_. The `feature_of_the_week` spotlight (24h-cached eligibility promo highlighting a CC feature). Config cleared to null for you. Present (string only, not gate-wired).

**🆕 New flags**

- `tengu_frame_publish_context` — wired gate, default OFF. Sits in the artifact/"frame" publishing path (slug/title/favicon/label, `artifactReadVersions`); probably gates including extra context when publishing an artifact/frame. _(wired/upcoming)_
- `tengu_saffron_credits_only_tiers` — wired gate; parses a list of plan tiers (default `["enterprise"]`) treated as "credits only" for billing/overage-consent logic. GB value `["enterprise"]`. _(wired)_
- `tengu_usage_overage_included_models` — list of model ids included in/covered by usage-overage billing; `Uda()` prefix-matches a model against it, tied to `isUsingOverage`/`overageStatus`. Empty list currently. _(present)_
- `tengu_startup_announcements` — config list of announcement messages shown at Claude Code startup, each optionally gated by `requiresModel` and tracked via impression counts. Empty currently. _(present/upcoming)_
- `tengu_velvet_hammer_sonnet_5` — stripped, no code this build. A Sonnet-5-specific variant of the "velvet hammer" edit-tool guard (forces a Read before an Edit/Write; blocks stale edits). Name only, no behavior yet. _(stripped)_

**🧱 DCE switches**

None.

## 2026-07-03 10:15 — v2.1.199 (from v2.1.197)

_Gate helper prefix drifted `it(`→`ot(` this release; regex patched in the routine. `velvet_mallet`/`velvet_hammer` present→wired were regex artifacts (wrapper `$st`→`Jat`, ends in `at`) and were dropped — both are wired read-guards in both versions._

**🔀 GrowthBook switches**
- Weekly plan rate-limit config (`tengu_saffron_lattice`) — OFF → ON _(GrowthBook, wired)_. Parses the plan/weekly usage-limit UI config; dropped `hideRateLimitsDescription`, now sets `planLimitsEndDate: 2026-07-08`. Surfaces the rate-limit description + end-date banner.
- Startup announcements (`tengu_startup_announcements`) — `[]` → Fable 5 promo _(config)_. Startup banner now carries "Fable 5 is back": up to 50% of weekly limit on Fable 5 until Jul 7, then usage credits. maxImpressions 100.
- Artifact publish context (`tengu_frame_publish_context`) — OFF → ON _(wired)_. Gates attaching artifact read-version context when publishing an Artifact/frame.
- Artifacts master gate (`tengu_cobalt_plinth`) — OFF → ON _(wired)_. Turns on the Artifact feature (publish HTML/MD to a hosted claude.ai page: `/api/frame/deploy/init`, `artifactViewerUrl`, FRAME_RUNTIME, MAX_ARTIFACT_BYTES). Now live for this account.
- Auto-mode classifier config (`tengu_auto_mode_config`) — payload expanded _(wired, mode still off)_. Two-stage `/auto` safety classifier gained `sameTurnSiblingContext`, `jsonlTranscript`, `editRemovalVisibility`, `editRemovalCap: 3000`.
- Overage-included models (`tengu_usage_overage_included_models`) — `[]` → `["Fable","Fable 5"]`. Models allowed to draw usage-credit overage past the plan cap (ties to the Fable 5 promo).
- Canary pin (`tengu_canary`) — `{external:"2.1.197"}` → `{}` _(wired)_. External canary-version pin cleared now that 2.1.199 is the release.

**🆕 New flags** (all name-only / stripped — no binary code yet)
- `tengu_velvet_tide` — zero binary presence; purpose unknown, watch next release.
- `tengu_md_artifact_styling` — likely styling/theming for Markdown Artifacts (pairs with cobalt_plinth). No code yet.
- `tengu_ide_rc_auto_enable` — likely auto-enabling an IDE release-candidate build/extension. No code yet.
- `tengu_plan_artifact` — likely publishing plan-mode output as an Artifact. No code yet.

**🧱 DCE switches**
- `tengu_amber_packet` — newly shipped (stripped → wired). Gates a background precompute-compaction path (`ot("tengu_amber_packet")&&!K$()`, feeds `Lba` alongside `precomputeCompactionEnabled`/`sepia_moth`) so a compaction is ready ahead of a stall.
- `tengu_slate_ibis` — newly shipped (stripped → present, default ON). Gates the Explore/Plan **coordinator + worker** multi-agent system (`getCoordinatorAgents`, `WORKER_AGENT`, worker/coordinator prompts; honors `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS`). Read via getFeatureValue, hence "present".
- `tengu_brass_sled` — newly shipped (stripped → wired). Gates injecting Windows toolchain detection into the shell system prompt (`kVa()`→`hks()` enumerates MSVC/VS-dev-shell tools on PATH).
- `tengu_gorse_fathom` — newly shipped (stripped → wired). Gates extra memory guidance near the `memory-types` skill: prompt to save a `feedback` memory when the user corrects how a repeatable step was run.
- `tengu_quartz_heron` — code removed (wired → stripped). Gated the built-in subagent default model (off → `"haiku"`, on → `"inherit"`). Removed → built-in agent model selection no longer haiku-gated.
- `tengu_amber_heron` — code removed (wired → stripped). Gated defaulting the Agent/Task tool to async/background execution (fed the `is_async` decision). Removed → async-subagent behavior no longer behind this gate.

## 2026-07-15 10:24 — v2.1.210 (upgraded from v2.1.199)

Classifier repaired from binary evidence before diffing: current GrowthBook reads use `Ze`, with `J1`/`vme`/`Xfe`/`dgt`/`S6n`/`Xq`/`IPi` wrappers and `bvi` context-derived keys. Health check: 286 gate/config call sites, 1,292 telemetry references, 1,633 `tengu_` strings. Environment baseline captured: 524 variables; no additions/removals reported. Official Anthropic changelog/release check blocked because Exa MCP was unavailable; no announcement marker was advanced.

### 🔀 GrowthBook switches
- `tengu_copper_fox` — effective ON → OFF. Enables fork-style subagents; the current build still contains the feature path, but the GrowthBook value is now off and no override is set.
- `tengu_orford_ness` — OFF → ON. Gates first-party error reporting, minimum-version checks, and related eligibility handling; current code is present and effective.
- `tengu_auto_mode_config` — payload expanded while effective state stayed OFF. Configures Auto Mode’s two-stage classifier, sibling context, JSONL transcript handling, edit-removal visibility/cap, and Git/outcome context; the code is wired but Auto Mode remains off for this account.
- `tengu_saffron_lattice` — plan-limit deadline moved Jul 8 → Jul 20 while enabled. Controls usage-overage/Fable entitlement behavior and plan-limit messaging; wired and effective.
- `tengu_slate_harrier` — `compact` → `off`. Controls Opus 4.7 “investigate first” prompting before questions/actions; wired but now disabled.
- `tengu_cedar_sundial` — OFF → ON, but code is stripped. Historical purpose was stale-read edit recovery; this flip is a no-op in 2.1.210.
- `tengu_shale_finch` — ON → OFF. Controls output/prompt-injection sanitization and disallowed-tool filtering; code is wired but disabled.
- `tengu_shoji_engine` — OFF → ON, but code is stripped. Historical settings/config-resolution engine behavior is gone from this build; no effect.
- `tengu_mcp_subagent_prompt` — ON → OFF. Controls guidance when MCP/blob results exceed output limits and are saved for inspection; wired but disabled.
- `tengu_ember_latch` — ON → OFF. Enables extra-usage and usage-credit admin-request flows; wired but disabled.
- `tengu_bridge_attestation_enforce` — OFF → ON. Enforces trusted-device attestation for Remote Control control requests; wired and effective.
- `tengu_cobalt_plinth_reader_persist` — OFF → ON. Persists Artifact/frame reader state and stored artifact versions; wired and effective.
- `tengu_startup_announcements` — Fable 5 promo payload replaced and max impressions 100 → 10. Selects/throttles startup announcements; wired, but the current announcement is not effective because the cached flag is false.
- `tengu_velvet_hammer_opus_4_8` — OFF → ON, but code is stripped. No current Opus-specific implementation survives, so the switch is a no-op.

### 🆕 New flags
- `tengu_rc_long_turn_nudge` — new, GB `null`, wired but unset. Likely controls a Remote Control upsell after a long turn, with threshold/probability/impression settings.
- `tengu_umber_kestrel` — new, OFF, wired but disabled. Controls availability of the `EndConversation` tool.
- `tengu_plugin_feedback_survey_config` — new, `{}`, wired. Configures plugin feedback-survey triggers, scopes, and cooldowns.
- `tengu_lapis_anchor_user_turn` — new, OFF, wired but disabled. Re-anchors token-reminder budgets after each user turn.
- `tengu_marbled_teal` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_zinc_harbor` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_rate_limit_promo_notices` — new, empty list, present. Configures notices shown around usage and rate limits; no active notices are supplied.
- `tengu_chrome_install_upsell` — new, OFF, wired but disabled. Controls Claude-in-Chrome installation/setup upsell UI.
- `tengu_slate_trellis` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_vellum_ash` — new, empty list, wired. Disables legacy todo/task tools when the current model matches configured entries.
- `tengu_deferred_stub_tool` — new, ON, wired and effective. Provides a deferred Document/Image stub tool for fallback loading.
- `tengu_quiet_reef` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_cobalt_plinth_osier` — new, OFF, wired but disabled. Kills/disables shared-scope Artifact listing.
- `tengu_fleet_needs_input_nudge` — new, ON, stripped. A Fleet input nudge is server-staged, but no implementation is present in this build.
- `tengu_wavy_light` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_salt_marsh` — new, OFF, wired but disabled. Adds memory-citation instructions to prompts when enabled.
- `tengu_dash_flame` — new, OFF, stripped. No surviving behavior or reliable purpose is recoverable from this binary.
- `tengu_bridge_system_init` — new, ON, wired and effective. Gates sending Remote Control bridge `system/init` data.
- `tengu_walnut_spire` — new, OFF, wired but disabled. An internal gate near model/review logic; the exact product surface is not named in surviving strings.
- `tengu_updater_range_resume` — new, OFF, stripped. No surviving updater-resume behavior is present.
- `tengu_haze_glass` — new, OFF, wired but disabled. Gates organization-memory discovery and synchronization.
- `tengu_kairos_ready_nudge` — new, GB `null`, stripped. No surviving ready-nudge behavior is present.
- `tengu_retire_chat_relay_artifact_backstop` — new, OFF, wired but disabled. Disables Artifacts in chat-relay/noninteractive contexts.
- `tengu_lantern_prism` — new, OFF, wired but disabled. Gates the Ultra/cloud-review path and can also be enabled through its environment override.
- `tengu_juniper_relay_config` — new, `{}`, stripped. No surviving relay-config behavior is present.
- `tengu_juniper_relay` — new, OFF, stripped. No surviving relay behavior is present.

### 🧱 DCE switches
- `tengu_ide_rc_auto_enable` — newly shipped (stripped → wired). Sends an IDE-side Remote Control auto-enable gate during session initialization.
- `tengu_fine_survey_transcript_ask_config` — newly shipped (present → wired). Configures transcript-sharing prompts for “fine” survey outcomes.
- `tengu_malort_pedway` — newly shipped (present → wired). Controls Computer Use enablement, pixel validation, clipboard safety, mouse animation, and coordinate mode.
- `tengu_cloth_snorkel` — newly shipped (stripped → wired). Gates Artifact MCP runtime capability declarations.
- `tengu_kairos_cron_durable` — newly shipped (present → wired). Controls whether scheduled tasks persist in `.claude/scheduled_tasks.json` across restarts.
- `tengu_sparrow_ledger` — code removed (wired → stripped). The prior verify-prompt/ledger behavior is absent from this build.
- `tengu_ccr_bundle_seed_enabled` — newly shipped (present → wired). Allows seeded bundles for eligible remote/background sessions.
- `tengu_cedar_sundial` — code removed (wired → stripped). Duplicate DCE entry; the stale-read edit-recovery behavior is absent.
- `tengu_bridge_min_version` — newly shipped (present → wired). Rejects Remote Control clients below the configured minimum version.
- `tengu_herring_clock` — code removed (wired → stripped). The prior memory-store behavior is absent; no current effect.
- `tengu_shoji_engine` — code removed (wired → stripped). Duplicate DCE entry; the historical settings engine is absent.
- `tengu_bridge_poll_interval_config` — newly shipped (present → wired). Configures bridge polling, heartbeat, reclaim, and keepalive intervals.
- `tengu_velvet_tide` — newly shipped (stripped → wired). Enables the simplified system-prompt path for supported models.
- `tengu_max_version_config` — newly shipped (present → wired). Sets updater maximum-version and forced-downgrade behavior.
- `tengu_slate_ibis` — newly shipped (present → wired). Enables coordinator, Explore, and Plan-agent tooling; it honors `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS`.
- `tengu_orchid_mantis_v2` — code removed (wired → stripped). The prior schedule-offer behavior is absent.
- `tengu_marble_lark` — code removed (wired → stripped). The prior memory-path behavior is absent.
- `tengu_silk_almanac` — code removed (wired → stripped). The prior team-memory multistore behavior is absent.
- `tengu_desktop_upsell` — newly shipped (present → wired). Configures desktop shortcut and contextual upsell tips.
- `tengu_version_config` — newly shipped (present → wired). Enforces a minimum Claude Code version and displays the update message.
- `tengu_good_survey_transcript_ask_config` — newly shipped (present → wired). Configures transcript-sharing prompts for “good” survey outcomes.
- `tengu_kairos_cron` — newly shipped (present → wired). Enables cron/scheduled-task tools and `/schedule`.
- `tengu_fleet_past_sessions` — newly shipped (stripped → wired). Enables Fleet past-session browsing, with `CLAUDE_CODE_FLEET_PAST_SESSIONS` as an environment override.
- `tengu_startup_announcements` — newly shipped (present → wired). Selects/throttles startup announcements; this is the same live path described in the GrowthBook switch above.
- `tengu_bridge_repl_v2_config` — newly shipped (present → wired). Configures Remote Control REPL v2, including minimum version and metadata.
- `tengu_orchid_mantis` — code removed (wired → stripped). The prior schedule-offer behavior is absent.
- `tengu_bad_survey_transcript_ask_config` — newly shipped (present → wired). Configures transcript-sharing prompts for “bad” survey outcomes.
- `tengu_velvet_hammer` — code removed (wired → stripped). The previous edit-tool validation path no longer survives in this build.
- `tengu_fleetview_onboarding_v2` — retired from GrowthBook (wired → removed-from-growthbook). No current flag string or gate remains, so its Fleet onboarding behavior is unrecoverable.
- `tengu_quartz_heron` — retired from GrowthBook (stripped → removed-from-growthbook). No current flag string or gate remains, so the historical behavior is unrecoverable.
