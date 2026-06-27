
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
