---
name: competitor-monitor
description: Monitor competitor YouTube channels for new Claude Code videos and compare their topics against your known gaps. Use Chrome browser automation to check each channel's recent uploads, extract video titles/dates, and flag topics that overlap with your blind spots. Triggers on "check competitors", "what are competitors posting", "monitor competitors", "competitor scan", "what's new from competitors", "any new competitor videos", or "/competitor-monitor".
---

# Competitor Monitor

Scan competitor YouTube channels for recent uploads, compare topics against your gap analysis, and surface what you should pay attention to.

## Workflow

### 1. Load Context

Read these files to understand the competitive landscape:

- `projects/agentic-coding-school/competitor-analysis/_MASTER-GAPS.md` — your blind spots and gap themes
- `.claude/skills/competitor-monitor/references/channels.md` — the channel list to monitor
- `.claude/skills/competitor-monitor/references/scan-history.md` — previous scan results (to avoid re-flagging old videos)

### 2. Scan Channels via Chrome

Use `mcp__claude-in-chrome__tabs_context_mcp` first to get browser state.

For each channel in `references/channels.md`:

1. Create a new tab with `mcp__claude-in-chrome__tabs_create_mcp`
2. Navigate to the channel's Videos tab: `https://www.youtube.com/@{handle}/videos`
3. Use `mcp__claude-in-chrome__read_page` to extract the video list
4. Record **all videos from the last 30 days** (title, date, view count if visible)
5. Close the tab before moving to the next channel

**Parallelization:** Process channels sequentially (one tab at a time) to avoid overwhelming Chrome. Each channel should take ~10 seconds.

**Rate limiting:** If YouTube shows a CAPTCHA or rate limit page, stop scanning, report what you have so far, and note which channels remain.

### 3. Download Transcripts

For every new video found (not already in scan-history.md), download its transcript using the youtube-transcript-downloader skill's script. Extract the video ID from the YouTube URL.

```bash
python3 /Users/ray/Desktop/ray-os/.claude/skills/youtube-transcript-downloader/scripts/download_transcript.py <video_id> --out-dir /Users/ray/Desktop/ray-os/projects/agentic-coding-school/competitor-analysis/transcripts/
```

**Parallelization:** Batch transcript downloads — run up to 5 in parallel using background Bash tasks, then wait for all to complete before the next batch.

Transcripts auto-organize into channel subfolders:
```
competitor-analysis/transcripts/
├── indydevdan/
│   └── abc123.txt
├── cole-medin/
│   └── def456.txt
```

If a transcript fails (no captions available), note it in the report and move on.

### 4. Compare Against Your Course (via MCP)

For each new video, extract 3-5 key topics/techniques from the competitor transcript, then search your actual course content using the agentic-coding-school MCP:

```
mcp__agentic-coding-school__search_videos(query: "<topic from competitor video>")
```

Run multiple searches per video to cover different angles (e.g., if a competitor covers "TDD with hooks", search for "TDD", "testing", "hooks test", etc.).

Based on search results, classify each video:

- **GAP** — You have zero matching content in your course. The competitor is teaching something you don't cover at all.
- **THIN** — You touch on it briefly (mentioned in passing, or covered as part of another topic) but the competitor goes deeper or has a dedicated video.
- **COVERED** — You already have substantial content on this topic. No action needed.
- **IRRELEVANT** — Not related to Claude Code / agentic coding.

For GAP and THIN classifications, include:
- What specifically the competitor covers (key techniques/quotes from their transcript)
- What your course currently has (or doesn't) based on the MCP search results
- How big the gap is (did they do a full 30-min deep dive on something you never mention?)

### 5. Report

Output a summary table to the user:

```
## Competitor Scan: YYYY-MM-DD

### New Videos Found: N

| Channel | Title | Views | Age | Classification |
|---------|-------|-------|-----|----------------|
| ... | ... | ... | ... | GAP |

### Gaps (they teach it, you don't)
[For each GAP video: what they cover, what MCP search returned (nothing), key techniques/quotes from their transcript]

### Thin Coverage (you touch it, they go deep)
[For each THIN video: what they cover in depth, what your course has (with video title from MCP), and what's missing]

### Trend Watch
[Note if multiple competitors are converging on the same topic — that's a signal]

### Key Techniques / Workflows Spotted
[Pull specific actionable techniques from transcripts that are new or different from what you teach]

### Channels with No New Content
[List channels that haven't posted in 30+ days]
```

### 6. Save Results

Append the scan results to `.claude/skills/competitor-monitor/references/scan-history.md` with the date and video IDs, so future scans skip already-seen videos.

## Important Notes

- **Always download transcripts** — titles alone aren't enough to know what competitors are actually teaching. The transcript reveals the real content.
- **Flag trends** — If 3+ competitors post on the same topic in the same month, call it out prominently.
- **Pull actionable intel** — Don't just classify. Extract specific techniques, workflows, or tools from transcripts that could inform your content.
- **Transcript storage** — All transcripts go to `projects/agentic-coding-school/competitor-analysis/transcripts/` organized by channel subfolder.
