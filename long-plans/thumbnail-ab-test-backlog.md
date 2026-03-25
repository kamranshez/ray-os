## Thumbnail A/B Test Backlog Plan

Generate 30 Nate Herk-style thumbnails for each of 16 videos (V11 already done), upload favorites as YouTube A/B tests, check results in 7 days.

**Total: 16 videos x 30 thumbnails = 480 thumbnails**

---

### Video List

| # | Video ID | Title | Views | Topic (for prompt adaptation) |
|---|----------|-------|-------|-------------------------------|
| V1 | `pb0lVGDiigI` | Anthropic Reveals How to Prompt Claude Code 10x Better | 28K | Prompting tips, Opus 4.5 |
| V2 | `IiA4Ku5viyg` | Anthropic Just Added These Features to Claude Code | 19K | Weekly features update |
| V3 | `rXTvax9pyhs` | Anthropic Just Connected Claude Code to Your Browser | 20K | Browser control, Chrome |
| V4 | `sy65ARFI9Bg` | My Claude Code Workflow for 2026 | 25K | Personal workflow, coding stack |
| V5 | `NmKdYlODC24` | Claude Code's Biggest Update in Months | 24K | Subagents update |
| V6 | `aF4QAHbNDrA` | Anthropic Just Added These Features to Claude Code | 19K | Planning features |
| V7 | `6omInQipcag` | Claude Code's New Task System Explained | 27K | Task management |
| V8 | `DWiYdXrxSwg` | Learn Claude Code Agent Teams in 12 Minutes | 21K | Agent swarms, multi-agent |
| V9 | `F_frSYyhzOE` | Anthropic Just Dropped 17 New Claude Code Features | 18K | Worktrees, desktop app |
| V10 | `y3xzYwxQuHc` | Anthropic Just Dropped the Feature Everyone Asked For | 35K | Remote control, phone coding |
| V11 | `AzmnaoVP8sk` | The Top 0.01% User's Guide to Claude Code | 18K | **DONE** (30 thumbnails generated) |
| V12 | `qXWz-V_XMOc` | Anthropic Just Dropped Claude Code Skills 2.0 | 44K | Skills 2.0, skill evals |
| V13 | **TBD** | Anthropic Just Dropped the Feature That Kills OpenClaw | ~38K | Cron scheduling, OpenClaw killer |
| V14 | `DqjBbAr3oTo` | Anthropic Just Dropped the Feature Nobody Knew They Needed | 38K | /btw, --fork-session, context pollution |
| V15 | `7PnF8qctDi8` | Anthropic Just Dropped Their Internal Skills Strategy | 10K | Skills guide, internal strategy |
| V16 | **TBD** | Claude Code Channels (Telegram/Discord) | ~20K | Channels, OpenClaw killer pt2 |
| V17 | `pOsGxVKYd3s` | Anthropic Just Revealed Where Coding Is Heading | 17K | Software factory, cloud tasks |

> **Action needed:** Find video IDs for V13 and V16 before starting those.

---

### 15 Nate Herk Style Variants

Each video gets all 15 variants x 2 each = 30 thumbnails.

| Variant | Style | Reference ID | Face? |
|---------|-------|-------------|-------|
| 1 | Folder + `/command` + pointing | `OUyfxhFtGCo` | Yes |
| 2 | Folder + `/command` + smiling | `X6EGzi9qm3E` | Yes |
| 3 | Icons on black + bold statement | `LrgfmZkl3nc` | No |
| 4 | Icons on black + short phrase | `Wu67lLD8bB0` | No |
| 5 | Old vs New comparison + face center | `pkSxISewcw8` | Yes |
| 6 | BASIC vs PRO? + shh face | `ZeJXI2MAhj0` | Yes |
| 7 | Holding prop/device + bold text | `T6_Ges4j1qY` | Yes |
| 8 | Feature grid on screen + face | `4Zaoo0YbYaw` | Yes |
| 9 | Whiteboard numbered list + face | `mpALXah_PBg` | Yes |
| 10 | Screen with flow arrows + face | `hem5D1uvy-w` | Yes |
| 11 | Retro game leaderboard/score | `l1jnOXc52NY` | Yes |
| 12 | CLI chat input + bold text overlay | `vFepZE_wrfg` | Yes |
| 13 | CLI chat input + "Game Over" style | `BlNJFa3Btm8` | Yes |
| 14 | Dark dashboard with stats | `NDnv16PY2XQ` | Yes |
| 15 | Folder + agent network diagram | `vDVSGVpB2vc` | Yes |

References already downloaded: `research/competitor-thumbnails/nateherk/`

---

### Execution Plan

#### Step 0: Prep (2 min)
- [ ] Find missing video IDs for V13 and V16
- [ ] Isolate `go-to-face.jpg` (move others to backup)
- [ ] Create all output directories

#### Steps 1-16: Generate per video (~4 min each, ~65 min total)

For each video:
1. Adapt all 15 prompts to the video's specific topic
2. Run **batch A** — 10 parallel generations (variants 1-5, 2 each)
3. Run **batch B** — 10 parallel generations (variants 6-10, 2 each)
4. Run **batch C** — 10 parallel generations (variants 11-15, 2 each)
5. Rename files with descriptive kebab-case names
6. Move to `output/<video-id>/`
7. Generate per-video HTML picker
8. Clean up temp directories
9. Mark step complete

**Processing order (highest views first = highest ROI):**

| Order | Video | Views | Est. Start |
|-------|-------|-------|------------|
| 1 | V12 — Skills 2.0 | 44K | 0 min |
| 2 | V14 — Feature Nobody Knew | 38K | ~4 min |
| 3 | V13 — OpenClaw Killer | ~38K | ~8 min |
| 4 | V10 — Feature Everyone Asked For | 35K | ~12 min |
| 5 | V1 — Prompt 10x Better | 28K | ~16 min |
| 6 | V7 — Task System | 27K | ~20 min |
| 7 | V4 — Workflow 2026 | 25K | ~24 min |
| 8 | V5 — Biggest Update | 24K | ~28 min |
| 9 | V8 — Agent Teams | 21K | ~32 min |
| 10 | V3 — Browser Control | 20K | ~36 min |
| 11 | V16 — Channels | ~20K | ~40 min |
| 12 | V6 — Planning Features | 19K | ~44 min |
| 13 | V2 — Weekly Features | 19K | ~48 min |
| 14 | V9 — 17 New Features | 18K | ~52 min |
| 15 | V17 — Software Factory | 17K | ~56 min |
| 16 | V15 — Internal Skills Strategy | 10K | ~60 min |

#### Step 17: Update Backfill Lab data.json (1 min)
- [ ] Mark each video as `generated` in `data.json` after thumbnails are created
- [ ] Backfill Lab auto-discovers thumbnails from `output/<video-id>/`

#### Step 18: Restore & Cleanup (1 min)
- [ ] Restore face photos from backup
- [ ] Remove all temp batch directories

#### Step 19: Agent Task — 7-Day Check (1 min)
- [ ] Create `/agent-tasks.yaml` with entry:
  ```yaml
  - task: check-thumbnail-ab-results
    description: Check YouTube Studio A/B test results for all 16 videos
    due: 2026-04-01  # 7 days from today (2026-03-25)
    videos: [V1-V10, V12-V17]
    action: |
      1. Open YouTube Studio analytics for each video
      2. Screenshot A/B test results
      3. Record winners in Backfill Lab (Results page)
      4. Update feedback.json with winning styles
  ```

#### Step 20: Commit & Push
- [ ] Commit all generated thumbnails + backfill app + agent task
- [ ] Push to remote

---

### Backfill Lab (Streamlit App)

**Location:** `.claude/skills/youtube-thumbnail-generator/backfill/`
**Launch:** `cd .claude/skills/youtube-thumbnail-generator/backfill && streamlit run app.py --server.port 8503`
**Data:** `backfill/data.json` — single source of truth for all state

**Pages:**
1. **Dashboard** — all videos as cards sorted by views, status badges, progress bar, export tools
2. **Review** — pick a video, see 30 thumbnails in variant pairs, click to shortlist up to 3, mark as uploaded
3. **Results** — record A/B test watch-time % and winners after 7 days, summary table

**Workflow:**
1. Generate thumbnails → status moves to `generated`
2. Ray shortlists 3 per video in Review page → status moves to `shortlisted`
3. Ray uploads to YouTube Studio, clicks "Mark as uploaded" → status moves to `uploaded`, sets 7-day due date
4. After 7 days, record results in Results page → status moves to `results_in`

---

### Settings

- **Parallel generations per batch:** 10
- **Face reference:** `go-to-face.jpg` only
- **Timeout per generation:** 180000ms (3 min)
- **Output:** `output/<video-id>/` per video
- **Naming:** `<style-description>-a.png`, `<style-description>-b.png`
