
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
