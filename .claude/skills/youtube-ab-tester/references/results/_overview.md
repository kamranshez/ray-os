# A/B Results — Start Here (routing map + video index)

This folder holds the channel's title/thumbnail A/B evidence. This file is the map: it tells you **which doc answers which question** and **which file is which video**. Read it first.

## Which file do I read?

| File | Owns | Read it when |
|------|------|--------------|
| `_master-summary.md` | Winning patterns, formula rankings, key rules, title↔thumbnail division of labor, test mechanics, diagnosis logic. Starts with a 13-point **Durable Insights TL;DR** (a digest of the tables below it). Last reconciled 2026-07-07 (clean-room audit). | "What works?" / "Why did X win?" / picking frames |
| `_anti-patterns.md` | The never-do list + a Downgraded (judgment-call) section. The single source of truth for what to avoid. | Before generating any title/thumbnail — required reading |
| `_tests-still-worth-running.md` | Untested hypotheses worth a future round. | Planning what to test next |
| `YYYY-MM/YYYY-MM-DD-slug.md` | Raw per-video rounds (title text, thumbnail text, watch-share, rank). | Need the actual numbers for a specific video; read the latest 4–6 for current patterns |
| `_overview.md` (this file) | Routing + the authoritative video index. | First, and whenever a video number is ambiguous |

**Ownership rule:** each rule lives in ONE file. `_anti-patterns.md` owns avoidance rules; `_master-summary.md` owns winning patterns and diagnosis. SKILL.md holds operating procedure only and points here — it should never restate a rule. If you find the same rule in two files, the reference doc is canonical and SKILL.md is the stale copy.

## Read-order map (by task)

1. **Generating titles** → SKILL.md Part 1 dispatches a subagent that reads `_master-summary.md` + `_anti-patterns.md` + `_tests-still-worth-running.md` + the latest 4–6 `YYYY-MM/` files.
2. **Generating thumbnails** → SKILL.md Part 2 + `../matt-style.md` or `../nate-style.md` + `../../feedback.json`.
3. **Recording results** → SKILL.md Part 3 + the video's `thumbnails/v{N}-{slug}/uploaded.json`.
4. **"What works / why did X lose?"** → `_master-summary.md`, then drill into the per-video file.

## Video index (authoritative — # → date → file)

The number below is the source of truth. Some per-video files have a stale internal `## Video N` header (noted); trust this table, not the header.

| # | Date | File | Note |
|---|------|------|------|
| V1 | 2025-11-27 | `2025-11/2025-11-27-opus-prompting-tips.md` | |
| V2 | 2025-12-10 | `2025-12/2025-12-10-weekly-features-update.md` | |
| V3 | 2025-12-18 | `2025-12/2025-12-18-browser-control-update.md` | |
| V4 | 2026-01-02 | `2026-01/2026-01-02-ai-coding-workflow.md` | |
| V5 | 2026-01-08 | `2026-01/2026-01-08-subagents-update.md` | |
| V6 | 2026-01-19 | `2026-01/2026-01-19-planning-features.md` | |
| V7 | 2026-01-23 | `2026-01/2026-01-23-task-management.md` | |
| V8 | 2026-02-06 | `2026-02/2026-02-06-agent-swarms.md` | |
| V9 | 2026-02-21 | `2026-02/2026-02-21-worktrees-desktop-app.md` | |
| V10 | 2026-02-25 | `2026-02/2026-02-25-remote-control.md` | |
| V11 | 2026-03-03 | `2026-03/2026-03-03-60-claude-code-tips.md` | |
| V12 | 2026-03-04 | `2026-03/2026-03-04-skills-2.md` | |
| V13 | 2026-03-07 | `2026-03/2026-03-07-cron-scheduling.md` | |
| V14 | 2026-03-11 | `2026-03/2026-03-11-btw-fork-session.md` | |
| V15 | 2026-03-19 | `2026-03/2026-03-19-internal-skills-strategy.md` | |
| V16 | 2026-03-20 | `2026-03/2026-03-20-channels.md` | |
| V17 | 2026-03-21 | `2026-03/2026-03-21-cloud-scheduled-tasks.md` | |
| V18 | 2026-03-24 | `2026-03/2026-03-24-auto-dream.md` | |
| V19 | 2026-04-01 | `2026-04/2026-04-01-source-code-leak.md` | |
| V20 | 2026-04-06 | `2026-04/2026-04-06-ultra-plan.md` | |
| V21 | 2026-04-09 | `2026-04/2026-04-09-ultra-review.md` | |
| V22 | 2026-04-10 | `2026-04/2026-04-10-advisor-command.md` | same-day as V23 |
| V23 | 2026-04-10 | `2026-04/2026-04-10-monitor-tool.md` | same-day as V22 |
| V24 | 2026-04-15 | `2026-04/2026-04-15-interactive-artifacts.md` | |
| V25 | 2026-04-23 | `2026-04/2026-04-23-forked-subagents.md` | |
| V26 | 2026-05-05 | `2026-05/2026-05-05-codex-goal.md` | first Codex video |
| **V27** | 2026-05-22 | `2026-05/2026-05-22-workflow-tool.md` | the REAL V27. Docs may call it "V27-workflows" |
| V28 | 2026-05-29 | `2026-05/2026-05-29-dynamic-workflows.md` | re-cut of the workflow feature |
| V29 | 2026-06-01 | `2026-06/2026-06-01-codex-director.md` | |
| **V30** | 2026-06-09 | `2026-06/2026-06-09-wtf-are-loops.md` | ⚠️ internal header still says `## Video 27` — it is V30. Docs call it "V30-loops" |
| V31 | 2026-06-11 | `2026-06/2026-06-11-nested-subagents.md` | |
| V32 | 2026-06-21 | `2026-06/2026-06-21-anki-claude-code.md` | Anki + Claude Code; personal-workflow video, credential frame LOST |
| V33 | 2026-06-26 | `2026-06/2026-06-26-fable-return.md` | Fable 5 returning; R2 winner "Anthropic is Finally Bringing X Back (Get Ready Now)" 38.8%; "(Leak!)" tag lost; R3 urgency parenthetical DRAGS once headline strong; R4 "Anthropic Will... Differently" 37.8% — authority opener load-bearing (+10pp over passive "The Signs Say") |
| **V34** | 2026-07-06 | `2026-07/2026-07-06-code-with-claude.md` | Code with Claude event/insider video; payoff clause won ("Here's Their REAL Workflow" 38.1% vs payoff-free 27.4%). Same-day as V35 |
| **V35** | 2026-07-06 | `2026-07/2026-07-06-fable-sunset.md` | ⚠️ internal frontmatter says `v34` — it is V35. Docs call it "V35-fable-sunset". Deadline title won (38.2%); recycled V33 thumb won within-test but video threw subscriber-skip flag (rank 9/10) |
| **V36** | 2026-07-14 | `2026-07/2026-07-14-observer-agents.md` | Observer agents (gated CC feature). "Anthropic Just Dropped a New Kind of Subagent" won R1 (40.2%, 12.9pp) AND held R2 as control (35.7%, tight 4.1pp). Concrete named artifact > abstract benefit AND > vague superlative. R2: actor+verb opener rescues mechanism-description framing (-3pp, not V31's floor). Payoff-tail lever (A) still untested. Above-typical views; CTR/AVD are the soft spots |

**Numbering collisions (documented, not renamed):** (1) both `2026-05-22-workflow-tool.md` and `2026-06-09-wtf-are-loops.md` carry a `## Video 27` internal header — the workflow-tool file is correct; the loops file is actually V30 ("V27-workflows" / "V30-loops" in docs). (2) Both 2026-07-06 files self-label V34 — code-with-claude is the real V34; fable-sunset is V35 ("V35-fable-sunset" in docs). This table is the source of truth. Physical renumbers (headers + `thumbnails/` folders + `uploaded.json`) were deliberately deferred to avoid desync — keep using this table instead.
