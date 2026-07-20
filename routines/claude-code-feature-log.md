
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

## 2026-07-16 09:21 — v2.1.211 (upgraded from v2.1.210)

Classifier repaired from binary evidence before diffing: the main GrowthBook reader is now `et`, with `Fme`/`uM` structured reads, `pme`/`Vgt` refresh-aware reads, `hj`/`c1i` boolean eligibility checks, and `Jwi` per-model dynamic keys. Health check: 294 gate/config flags; the apparent `tengu_velvet_mallet` wired → present transition was rejected as a classifier artifact because its live gate now uses `et(Jwi(...))`. Official Anthropic changelog/release check was blocked because Exa MCP is unavailable; no announcement marker was advanced.

### 🔀 GrowthBook switches
- `tengu_shale_finch` — OFF → ON via GrowthBook. Removes `TodoWrite`, `TaskCreate`, `TaskGet`, `TaskUpdate`, and `TaskList` from non-teammate subagents after their toolset is resolved; code is wired and effective. The nearby output neutralizer is unconditional and is not controlled by this flag.
- `tengu_slate_harrier` — `off` → `compact` via GrowthBook. Enables the Opus 4.7 “investigate first” instruction that makes Claude perform brief read-only investigation before asking a clarifying question; code is wired and effective in compact mode, with `CLAUDE_CODE_INVESTIGATE_FIRST` taking precedence when set.
- `tengu_cowork_chrome_automode_default` — ON → OFF via GrowthBook. Supplies the default Chrome classifier-floor switch inside Auto Mode permission construction; code remains wired, but the floor is now off unless `CLAUDE_CHROME_CLASSIFIER_FLOOR` overrides it.
- `tengu_cloth_snorkel` — OFF → ON via GrowthBook. Enables Artifact MCP runtime capability declarations and connector summaries for published artifact frames; code is wired and effective, with `CLAUDE_CODE_ARTIFACT_MCP` taking precedence.
- `tengu_mcp_subagent_prompt` — OFF → ON via GrowthBook. Enables the stronger MCP large-result recovery prompt that tells subagents how to inspect saved JSON/text output completely rather than relying on the legacy truncation text; code is wired and effective, with `MCP_TRUNCATION_PROMPT_OVERRIDE` taking precedence.
- `tengu_velvet_hammer_opus_4_7` — OFF → ON in GrowthBook, but stripped from v2.1.211. Its last-known purpose is an Opus 4.7-specific bypass of the Edit tool's read-before-edit/stale-file guard; no call site survives, so the switch is a no-op.
- `tengu_velvet_hammer_sonnet_5` — OFF → ON in GrowthBook, but stripped from v2.1.211. Its last-known purpose is a Sonnet 5-specific bypass of the Edit tool's read-before-edit/stale-file guard; no call site survives, so the switch is a no-op.

### 🆕 New flags
- `tengu_media_byte_cap` — new numeric config `25165824` (24 MiB), wired and effective. During API message normalization it removes the oldest base64 image/document blocks until the request falls under the byte cap, replacing emptied content with `[media removed: request limit]` and emitting stripped-byte telemetry.

### 🧱 DCE switches
- `tengu_kairos_ready_nudge` — newly shipped (stripped → wired), but cached value is `null`, so it is inactive. Configures probability, impression count, and impression key for a Remote Control-ready push notification; the path additionally requires push-notification/Remote Control eligibility and suppresses itself in unsupported surfaces.

### ⚙️ Environment changes
- `CLAUDE_CODE_ENABLE_REFRESH_MCP_TOOLS` — added, opt-in boolean. When true it exposes the `RefreshMcpTools` tool, which re-queries already-connected MCP servers and reports tools added or removed; no related `tengu_*` gate is visible.
- `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` — added, opt-in boolean (also exposed as `--forward-subagent-text`). When true it forwards ordinary assistant/user text blocks from subagents alongside their tool events and avoids suppressing that text in noninteractive streaming; no related `tengu_*` gate is visible.
- `CLAUDE_CODE_GB_DISK_CACHE_WHEN_TELEMETRY_OFF` — added, opt-in boolean. Allows cached GrowthBook values on disk to remain usable when telemetry-backed GrowthBook initialization is otherwise unavailable; `DISABLE_GROWTHBOOK` still wins and disables the path.
- `CLAUDE_CODE_RESUME_INTERRUPTED_TURN_MAX_AGE_MS` — added, positive millisecond threshold used only with interrupted-turn resume. It suppresses automatic resubmission/synthetic continuation when the last meaningful message is at least this old; invalid positive input falls back to 3,600,000 ms, `0` disables the age check, and there is no related `tengu_*` gate.

## 2026-07-17 09:20 — v2.1.211

Classifier healthy at 294 gate/config flags. Repaired the tracker before diffing so numeric thresholds, probabilities, TTLs, byte limits, and string variants are treated as configuration payloads rather than boolean ON states; effective-only classifier changes can no longer create a false switch avalanche. Official Anthropic changelog/release checking was blocked because the required Exa MCP search/fetch tools are not registered in this runtime; `announcements-latest.json` remains absent and its marker was not advanced.

### 🔀 GrowthBook switches
- `tengu_auto_mode_config` — structured payload changed: the Sonnet 5 stage-1 hardening suffix was removed and per-model severity thresholds were added (`t1/t2`: Sonnet 5 `25/35`, Opus 4.8 `45/35`). This wired config controls Auto Mode's two-stage permission classifier; it is consumed only when Auto Mode runs and is not itself a standalone boolean enable.
- `tengu_russet_linnet` — OFF → ON. Enables Skill-tool description reframing before skills are injected, with `CLAUDE_CODE_SKILL_DESC_REFRAME` taking precedence; wired and effective via GrowthBook.
- `tengu_kairos_ready_nudge` — `null` → `{probability:0.25,maxImpressions:5,impressionKey:"v1"}`. Activates a wired Remote Control-ready push nudge for 25% of eligible events, capped at five impressions; push-notification and surface eligibility still gate delivery.
- `tengu_umber_kestrel` — OFF → ON. The surviving constant identifies the `EndConversation` tool, which lets comms-only agents end a turn explicitly; the flag is present but its read is indirect, so actual enablement cannot be proven from a literal gate call site.
- `tengu_lantern_spool` — OFF → ON. Adds `anthropic-usage-limit: extended` to eligible nested/subagent first-party API calls; wired and effective, but only for entitled first-party sessions and not auxiliary/compact calls.
- `tengu_rc_long_turn_nudge` — `null` → `{thresholdSec:10,probability:0.5,maxImpressions:5,impressionKey:"v1"}`. Activates the wired “Check in from your phone” Remote Control nudge after a 10-second turn for 50% of eligible sessions, capped at five; `CLAUDE_CODE_FORCE_RC_LONG_TURN_NUDGE` can force the test path.
- `tengu_cobalt_harbor` — OFF → ON. Makes Remote Control start automatically by default unless an explicit `remote_control_at_startup` setting overrides it; wired and effective, while OAuth, organization policy, provider, and entitlement checks still apply.

### 🆕 New flags
- `tengu_stone_shell` — new OFF, stripped. No string or implementation survives in this binary, so its behavior is unrecoverable and the cached value has no effect.
- `tengu_cobalt_thistle` — new OFF, wired. Gates an alternate shell-tool instruction set that relaxes the warning against using `cat`/`head`/`sed`/`awk`/`echo` and changes working-directory guidance; built but currently disabled.
- `tengu_cobalt_harbor_notice` — new ON, wired. Shows the “Keep working from anywhere” Remote Control auto-on notice, capped at three impressions, only when auto-on is active and Remote Control/policy eligibility passes.
- `tengu_juniper_vale` — new `{enabled:false,maxChars:500,autoDismissAfterMs:30000}`, stripped. The binary contains no call site or string, so the apparent text/auto-dismiss config is server-staged but ineffective here.
- `tengu_juniper_gantry` — new OFF, stripped. No surviving binary evidence reveals its purpose; the cached value is ineffective in this build.
- `tengu_rc_permission_nudge` — new `{afterPromptCount:2,probability:0.5,maxImpressions:3}`, wired. Offers “Approve tool calls from your phone” after two eligible permission prompts in a connected Remote Control session, at 50% probability and up to three times; `CLAUDE_CODE_RC_PERMISSION_NUDGE` can replace the payload.
- `tengu_ultrareview_git_init_recovery_enabled` — new OFF, stripped. Its name suggests Ultra Review git-init recovery, but no implementation survives, so purpose cannot be confirmed and the flag has no effect.

### 🧱 DCE switches
- `tengu_amber_quill` — retired from GrowthBook (wired → removed-from-growthbook). The binary still contains the contextual-tips classifier that inspects conversation/project context and can surface CLAUDE.md-aware tips, but its gate defaults OFF and has no environment override; removal from the live cache therefore leaves the feature disabled even though code remains.

### ⚙️ Environment changes
- No added or removed `CLAUDE_CODE_*` / `CLAUDE_*` controls.

## 2026-07-19 09:26 — v2.1.214 (upgraded from v2.1.211)

Classifier aliases were repaired from binary evidence before trusting the diff: 2.1.214 uses `uge`, `fO`, `Nbt`, `n3i`, `Jj`, `Bhe`, and `qVn` readers plus `YHi` model-suffixed keys and hoisted flag constants. Health check: 329 gate/config flags. This removed 12 bogus DCE transitions. The environment scanner also discarded 12 minified-string suffix/prefix artifacts and the non-env `CLAUDE_CODE_SKILL_DESCRIPTION` symbol. Official Anthropic changelog/release checking was blocked because the required Exa MCP search/fetch tools are not registered; `announcements-latest.json` remains absent and its marker was not advanced.

### 🔀 GrowthBook switches
- **Startup announcements** (`tengu_startup_announcements`) — the prior Fable 5 promotional card was removed (`[...]` → `[]`). This wired structured config selects startup cards with model and impression limits; the empty list is effective, so no startup announcement is shown.
- **Canary update pin** (`tengu_canary`) — `{}` → `{external: "2.1.214"}`. This wired installer config selects an external canary when it is newer than the latest allowed build; because the installed build is already 2.1.214, it does not trigger another upgrade.
- **Weekly-limit promo notice** (`tengu_rate_limit_promo_notices`) — `[]` → a seven-day-bar notice for “+50% weekly limits promo through Aug 19.” This wired config appends the notice beneath the `/usage` weekly bar, so the new message is user-visible when that bar is rendered.
- **EndConversation tool** (`tengu_umber_kestrel`) — ON → OFF. Gates the deferred `EndConversation` tool used by restricted comms/abuse-handling agents to end a turn explicitly; code remains wired, but the tool is now disabled and was additionally model-floor/entrypoint restricted when enabled.

### 🆕 New flags
- `tengu_mcp_claudeai_eligibility_gate` — new ON and wired. Enforces server entitlement on `claudeai-proxy` MCP integrations by marking ineligible servers unavailable; effective for this account, but actual access still depends on the server entitlement response.
- `tengu_thistle_grebe` — new value `"default"`, stripped. No string or implementation survives in 2.1.214, so behavior is unrecoverable and the server value has no effect in this build.
- `tengu_marl_cormorant` — new OFF, stripped. Codename only with no binary call site; purpose is unrecoverable and the flag is ineffective in this build.
- `tengu_gault_kestrel` — new OFF, stripped. Codename only with no binary call site; purpose is unrecoverable and the flag is ineffective in this build.

### 🧱 DCE switches
- `tengu_cobalt_heron` — code removed (wired → stripped). Previously gated a contextual tip suggesting that Pro users switch away from Opus after passing roughly 50% usage; it was already OFF, so removal does not change current behavior.
- `tengu_slate_moth` — code removed (wired → stripped). Previously suggested `/compact` when context exceeded roughly 300k tokens and stale-file context exceeded roughly 100k; it was already OFF, so removal is behaviorally inert.
- `tengu_team_discovery` — code removed (wired → stripped). Previously fetched daily-cached team usage from `/api/claude_code/discovery/team_usage` to recommend team-used skills and MCP servers; it also required `allow_team_discovery` and was OFF, so no live behavior was lost for this account.
- `tengu_stone_shell` — newly shipped (stripped → wired), currently OFF. Gates injection of the new `# auto memory` file-based-memory guidance when no explicit memory store, Cowork override, or project override applies; the code exists but is inactive.
- `tengu_juniper_vale` — newly shipped (stripped → wired), cached `{enabled:false,maxChars:500,autoDismissAfterMs:30000}`. Configures a post-feedback follow-up prompt and its text/auto-dismiss limits; disabled, so the new UI remains inactive.
- `tengu_juniper_relay` — newly shipped (stripped → wired), currently OFF. Gates a reviewable local `SendFeedback` draft queue for model-detected bugs or frustration; first-party/product-feedback eligibility is also required, and `CLAUDE_CODE_SEND_FEEDBACK=false` hard-disables it.
- `tengu_juniper_relay_config` — newly shipped (stripped → wired), cached `{}`. Supplies the `SendFeedback` tool description/config defaults but does not enable the tool independently; the parent relay gate remains OFF.

### ⚙️ Environment changes
- `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` — added. Positive integer cumulative subagent-spawn cap, minimum 1 and default 200; direct and effective with no GrowthBook gate.
- `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` — added. Positive integer cumulative WebSearch cap, minimum 1 and default 200; direct and effective with no GrowthBook gate.
- `CLAUDE_CODE_MEMORY_PUSH_DELETE_MODE` — added. Selects shared-memory deletion propagation: `corroborate` (default; two missing scans at least 30s apart), `immediate`, or `never`; overrides `tengu_mem_push_delete_mode`, while backend and safety eligibility still apply.
- `CLAUDE_CODE_NANKEEN_KESTREL` — added. Truthy value force-enables the native Windows sandbox ahead of `tengu_nankeen_kestrel`; false falls through to the gate, and the control is inert off Windows or when policy/dependencies block sandboxing.
- `CLAUDE_CODE_NO_MODEL_FALLBACK` — added. Truthy value collapses model fallback chains to the primary model and prevents compaction/Fable substitutions; direct with no GrowthBook gate, so primary-model policy or credit failures can surface instead of falling back.
- `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH` — added. Positive integer telemetry-only truncation cap in characters, default 61,440, further bounded by standard OTEL attribute/log/span limits; it does not enable exporting or bypass redaction.
- `CLAUDE_CODE_RESUME_SOURCE_ALIVE` — added internal transport value (`sessionId|ISO-boundary[|parentSessionId]`). Marks a concurrent source session alive so a resumed/forked child does not adopt source-owned file-history/checkpoint state; malformed values are ignored and there is no GrowthBook relationship.
- `CLAUDE_CODE_SEND_FEEDBACK` — added tri-state control, but only `false` is a hard kill switch. True or unset still requires wired `tengu_juniper_relay`, first-party/product-feedback eligibility, and a supported mode; the tool creates a reviewable draft and does not send automatically.
- `CLAUDE_CODE_USE_ANTHROPIC_GOOGLE_CLOUD` — added. Truthy value selects the `claude.googleapis.com` provider after higher-precedence gateway/Bedrock/Foundry/AWS choices; IAM, project, workspace, and model access still gate effectiveness.
- `CLAUDE_CODE_SKIP_ANTHROPIC_GOOGLE_CLOUD_AUTH` — added. Truthy value skips ADC only when the Anthropic Google Cloud provider is selected, enabling upstream/pre-signed authorization; it does not bypass service authorization.
- `CLAUDE_PID` — added internal child-process value overwritten with the parent Claude PID. The Linux `pkill` shim uses it to refuse matches that would terminate Claude's parent process; user-provided values are overridden.
- `CLAUDE_CODE_ENABLE_MORNING_BRIEF` — removed. Previously enabled the Cowork-only `/morning` brief; the live feature path is gone in 2.1.214.
- `CLAUDE_CODE_MORNING_BRIEF_PROMPT` — removed. Previously overrode the Cowork morning-brief prompt with a trimmed 500–50,000-character value; removal follows the feature's deletion.
- `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE` — removed schema-only residue. It was declaration/export/init DCE with no effective runtime read in 2.1.211, so removal is cleanup; current fast mode targets Opus 4.8 and remains entitlement/GrowthBook-gated.
- `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` — removed schema-only residue. It had no effective runtime read in 2.1.211, so no behavior was lost.
- `CLAUDE_CODE_MID_CONVERSATION_SYSTEM` — removed schema-only residue. It had no effective runtime read; the real positive lever `CLAUDE_CODE_FORCE_MID_CONVERSATION_SYSTEM` remains and can still be blocked in HIPAA contexts.
- `CLAUDE_CODE_PLAN_MODE_INTERVIEW_PHASE` — removed schema-only residue. It had no effective runtime read in 2.1.211, so removal is behaviorally inert.
- `CLAUDE_INTERNAL_WARM_RESUME_QA` — removed schema-only residue. It had no effective runtime read in 2.1.211, so removal is behaviorally inert.

## 2026-07-20 09:26 — v2.1.215 (upgraded from v2.1.214)

Classifier aliases were repaired from 2.1.215 binary evidence before trusting the diff: new readers are `dge`, `$bt`, `mO`, `u3i`, `Xj`, `Uhe`, and `WVn`, with `QHi` model-suffixed keys, optional client-data reads, and `$`-prefixed hoisted flag constants. Health check: 331 gate/config flags; the stricter helper boundary correctly excludes the telemetry call `oe("tengu_fleetview", {...})`. This suppressed 17 bogus wired→present transitions. The environment scanner also removed the concatenated artifacts `CLAUDE_CODE_SUPPRESS_SESSION_ATTRIBUTIONIS` and `CLAUDE_GATEWAY_LOG_LEVELI1`. Official Anthropic changelog/release checking was blocked because the required Exa MCP search/fetch tools are not registered; `announcements-latest.json` remains absent and its marker was not advanced.

### 🔀 GrowthBook switches
- **Canary update pin** (`tengu_canary`) — `{external:"2.1.214"}` → `{external:"2.1.215"}`. This wired updater config may replace the normal latest version with a newer external canary, subject to the configured maximum; because 2.1.215 is already installed, the new pin causes no further update now.
- **EndConversation tool** (`tengu_umber_kestrel`) — OFF → ON. Enables the deferred tool that lets abuse-handling agents explicitly end a conversation after warning the user; wired and effective only for qualifying CLI entrypoints and model floors (Opus 4.8+, Sonnet 5+, or Fable/Mythos 5+).
- **Subagent task-tool filtering** (`tengu_shale_finch`) — ON → OFF. When enabled it removes `TodoWrite`, `TaskCreate`, `TaskGet`, `TaskUpdate`, and `TaskList` from ordinary non-teammate subagents; the code remains wired, but the filter is now inactive.
- **Model task/todo blacklist** (`tengu_vellum_ash`) — `[]` → `["claude-opus-4-8","claude-sonnet-5","claude-fable-5"]`. This wired list disables task/todo tools, reminders, and rendering when the current model identifier matches an entry; it is now behaviorally effective on those three model families even though it is a structured config rather than a boolean gate.
- **Investigate-first prompt** (`tengu_slate_harrier`) — `compact` → `off`. Controls the Opus 4.7 instruction to perform brief read-only investigation before asking a clarifying question; wired but now disabled, with `CLAUDE_CODE_INVESTIGATE_FIRST` still able to override it.
- **Extended nested-call usage header** (`tengu_lantern_spool`) — ON → OFF. Adds `anthropic-usage-limit: extended` to eligible nested/subagent or compact requests on the first-party Anthropic endpoint; wired but now inactive, and server entitlement would still decide whether to honor it.
- **MCP large-result recovery prompt** (`tengu_mcp_subagent_prompt`) — ON → OFF. Selects strict JSON/text complete-inspection instructions after oversized MCP output is saved; wired but now falls back to the legacy offset/search guidance unless `MCP_TRUNCATION_PROMPT_OVERRIDE` forces the newer branch.
- **Remote Control auto-start default** (`tengu_cobalt_harbor`) — ON → OFF. Supplies the default for starting Remote Control automatically; wired but no longer auto-enables it, while an explicit `remote_control_at_startup` setting can still win and OAuth, provider, policy, and entitlement checks remain required.
- **Sonnet 5 Edit-guard variant** (`tengu_velvet_hammer_sonnet_5`) — server value ON → OFF, but the flag is stripped. Its last-known purpose is a Sonnet-5-specific bypass of the Edit tool's read-before-edit/stale-file guard; no call site survives in 2.1.215, so both values are runtime no-ops.

### 🆕 New flags
- `tengu_heron_tallow` — new OFF and stripped. No string, call site, or reliable historical evidence survives in the binary, so its behavior is unrecoverable and the cached value has no effect.

### 🧱 DCE switches
- `tengu_gault_kestrel` — newly shipped (stripped → wired), currently OFF. When enabled it relaxes the action-safety prompt by removing the instruction to surface contradictions or unowned targets before proceeding; `CLAUDE_CODE_GAULT_KESTREL` can force it on, and no entitlement gate is visible.
- `tengu_marl_cormorant` — newly shipped (stripped → wired), currently OFF. When enabled it adds an Exec-tool reminder that command output is shown to Claude, not reliably to the user; `CLAUDE_CODE_MARL_CORMORANT` can force it on, and no entitlement gate is visible.
- `tengu_thistle_grebe` — newly shipped (stripped → wired), cached `"default"`. Selects subagent steering: `default` keeps delegation nudges, `no_nudges` removes them, and `counter_steer` injects explicit anti-overdelegation guidance; precedence is env → client data → GrowthBook → default, so today's value preserves baseline behavior.

### ⚙️ Environment changes
- `CLAUDE_CODE_GAULT_KESTREL` — added force-ON boolean for `tengu_gault_kestrel`. Truthy removes the contradiction/unowned-target caution from the action-safety prompt; false does not override a true client-data or GrowthBook value, and it is currently unset.
- `CLAUDE_CODE_MARL_CORMORANT` — added force-ON boolean for `tengu_marl_cormorant`. Truthy adds the Exec output-visibility reminder; false does not override a true client-data or GrowthBook value, and it is currently unset.
- `CLAUDE_CODE_THISTLE_GREBE` — added enum override for `tengu_thistle_grebe`: `default`, `no_nudges`, or `counter_steer`. It has highest precedence and can explicitly restore `default`; it is currently unset, so the cached `default` applies.

Slack notification was attempted twice through the required `slackbot-message` script, but both escalated executions were rejected after the automatic permission review timed out. The complete message is preserved in the automation run output; delivery to `cc-feature-tracker` remains unresolved.
