---
name: youtube-outlier-scout
description: |
  Daily niche scout that monitors a watchlist of YouTube channels for outlier videos
  and searches keywords for trending content in the AI/coding niche. Use this skill
  when the user says "run the scout", "outlier scout", "what's trending", "daily report",
  "check the watchlist", "any outliers today", or wants a broad view of what's
  performing in their YouTube niche. Also trigger when the user asks to add/remove
  channels or keywords from the watchlist.
argument-hint: [daily|watchlist-only|keywords-only]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - mcp__claude_ai_Exa__web_search_exa
---

# /youtube-outlier-scout -- Daily Niche Outlier Scout

Monitor a watchlist of YouTube channels and search niche keywords to surface outlier
videos and trending title patterns in Ray's content niche. Runs daily.

## Arguments

`/youtube-outlier-scout [mode]`

- `$0` -- **mode** (optional): Which scan to run.
  - `daily` (default): full watchlist + keyword scan, generates combined report
  - `watchlist-only`: only scan watchlist channels, skip keyword discovery
  - `keywords-only`: only run keyword discovery, skip watchlist
  - `add <@handle>`: add a channel to the watchlist
  - `remove <@handle>`: remove a channel from the watchlist
  - `add-keyword <term>`: add a keyword to the search list
  - `remove-keyword <term>`: remove a keyword from the search list

## Configuration

**Watchlist file:** stored in this skill directory at `watchlist.yaml`
**Reports:** stored in this skill directory at `reports/YYYY-MM-DD.md`

The watchlist contains:
- `channels:` -- list of YouTube handles to monitor
- `keywords:` -- list of search terms for niche discovery
- `min_multiplier:` -- outlier threshold (default 3x median)

## Data Access

**Primary tool: yt-dlp** (installed at `/opt/homebrew/bin/yt-dlp`)

### Watchlist scan (per channel)

Two-step approach -- flat-playlist is fast but doesn't return view counts:

```bash
# Step 1: Get video IDs (fast, ~2s per channel)
yt-dlp --flat-playlist --print "%(id)s" \
  "https://www.youtube.com/@Handle/videos" 2>/dev/null

# Step 2: Batch-fetch metadata in parallel (10 at a time)
yt-dlp --flat-playlist --print "%(id)s" \
  "https://www.youtube.com/@Handle/videos" 2>/dev/null | \
  xargs -P 10 -I {} sh -c \
  'yt-dlp --no-download --print "%(id)s|%(title)s|%(view_count)s|%(upload_date)s" \
  "https://www.youtube.com/watch?v={}" 2>/dev/null' | \
  sort -t'|' -k3 -rn
```

Returns: `videoId|title|viewCount|uploadDate(YYYYMMDD)`

### Keyword discovery (per keyword)

```bash
yt-dlp "ytsearch20:<keyword>" --no-download \
  --print "%(id)s|%(title)s|%(view_count)s|%(channel)s|%(upload_date)s" 2>/dev/null
```

Returns: `videoId|title|viewCount|channelName|uploadDate(YYYYMMDD)`

Filter to videos published within the last 24 hours using the upload_date field.

## Process

### Step 0 -- Read Watchlist

Read `watchlist.yaml` from this skill's directory:
```
.claude/skills/youtube-outlier-scout/watchlist.yaml
```

Parse the channels list, keywords list, and min_multiplier.

### Step 1 -- Watchlist Scan

Process all 22 channels using subagents for parallelism. Spawn 5 subagents,
each handling 4-5 channels:

For each channel:
1. Pull all videos via yt-dlp two-step approach
2. Calculate median views for the channel
3. Identify videos >= min_multiplier threshold
4. Collect outliers with: title, views, multiplier, upload date, video ID

**Important:** Use `timeout: 300000` for the batch yt-dlp commands. Large channels
(100+ videos) take 30-60 seconds each.

Each subagent writes results to `/tmp/outlier-scout-<handle>.tsv`

### Step 2 -- Keyword Discovery

For each keyword in the search list:

1. Run `yt-dlp "ytsearch20:<keyword>"` to get 20 results with view counts
2. Filter to videos with upload_date = today (YYYYMMDD)
3. Deduplicate across keywords (same video can match multiple terms)
4. For videos with high raw views (>10k), note them as discoveries

**Date filtering:**
```bash
TODAY=$(date +%Y%m%d)
# Filter: only keep rows where upload_date field = today
awk -F'|' -v today="$TODAY" '$5 == today'
```

For daily runs, also include yesterday to catch videos uploaded late in the day:
```bash
YESTERDAY=$(date -v-1d +%Y%m%d)
awk -F'|' -v today="$TODAY" -v yesterday="$YESTERDAY" '$5 >= yesterday'
```

### Step 3 -- Cross-Reference Discoveries

For keyword discoveries that look promising (high views, recent):
- Check if the channel is already on the watchlist (skip if so -- already covered)
- For new channels: quick yt-dlp pull of their last 10 videos to get a baseline median
- Calculate if the discovered video is an outlier for its channel

```bash
# Quick baseline for a new channel (last 10 videos only)
yt-dlp --flat-playlist --playlist-end 10 --print "%(id)s" \
  "https://www.youtube.com/@NewChannel/videos" 2>/dev/null | \
  xargs -P 10 -I {} sh -c \
  'yt-dlp --no-download --print "%(view_count)s" \
  "https://www.youtube.com/watch?v={}" 2>/dev/null' | \
  sort -n | awk '{a[NR]=$1} END {print a[int(NR/2)+1]}'
```

### Step 4 -- Analyze Title Patterns

Across ALL outliers (watchlist + discoveries), analyze:

**Structure:**
- Curiosity gaps ("You've been doing X wrong", "Here's What to Build Instead")
- Power words (UNLOCK, DEPLOY, COMPLETE, KEY, BEAST)
- Number usage ("10x", "800+", "5,000")
- Question format vs statement format
- Parenthetical qualifiers ("(Full Guide)", "(Step by Step)")
- Name-dropping (people, companies, tools)

**Framing:**
- Problem-first vs solution-first
- Personal ("I did X") vs tutorial ("How to X") vs news ("X Just Changed")
- Negative framing vs positive framing

**Cross-channel patterns:**
- Which title formulas appear in outliers across MULTIPLE channels? (strongest signal)
- Which topics are trending today vs. evergreen?
- Any new channels emerging in the niche?

### Step 5 -- Generate Report

Output to terminal AND save to file.

**Report structure:**

```markdown
---
tags: [youtube, outlier-scout, daily]
date: YYYY-MM-DD
channels-scanned: N
keywords-searched: N
outliers-found: N
discoveries-found: N
---

## Outlier Scout Report -- YYYY-MM-DD

### Watchlist Outliers

Videos from tracked channels hitting {min_multiplier}x+ their channel median.

| # | Channel | Title | Views | Multiplier | Published |
|---|---------|-------|-------|------------|-----------|
| 1 | ...     | ...   | ...   | ...x       | ...       |

### Keyword Discoveries

Trending videos in the niche from the last 24 hours (not on watchlist).

| # | Channel | Title | Views | Est. Multiplier | Published | Keyword |
|---|---------|-------|-------|-----------------|-----------|---------|
| 1 | ...     | ...   | ...   | ...x            | ...       | ...     |

### Title Patterns Today

**Cross-channel patterns (strongest signals):**
- [pattern] -- seen in N outliers across N channels

**Trending topics:**
- [topic] -- N videos, avg Nx multiplier

**Title formulas working right now:**
1. [formula with example]
2. [formula with example]

### Channels to Watch

New or small channels with breakout videos today:
- @handle -- "Video Title" (Nx their usual, X views)

### Actionable Ideas for Ray

Title + topic ideas based on today's outlier patterns:
1. [specific title idea]
2. [specific title idea]
3. [specific title idea]
```

### Step 6 -- Save Report

Save to this skill's reports directory:
```
.claude/skills/youtube-outlier-scout/reports/YYYY-MM-DD.md
```

Use today's date. If a report already exists for today, append `-v2`, `-v3`, etc.

## Watchlist Management

When the user says `add @handle` or `remove @handle`:

1. Read `watchlist.yaml` from this skill's directory
2. Add/remove the handle from the channels list
3. Write back the updated file
4. Confirm the change

Same for `add-keyword` and `remove-keyword`.

## Performance Notes

- 22 channels with ~50-100 videos each = ~1,500-2,200 video lookups
- At 10 parallel yt-dlp processes, ~3-5 minutes for the full watchlist scan
- 7 keywords x 20 results = 140 video lookups for keyword discovery
- **Total estimated runtime: 5-8 minutes for a full daily scan**
- Use subagents to parallelize channel processing (4-5 channels per subagent)
- Use `timeout: 300000` (5 min) for long-running bash commands

## Important Notes

- **NEVER use em or en dashes** in any output text. Use `--` instead.
- Title + thumbnail are a **pair** -- note when thumbnails complement or duplicate the title.
- Present title ideas as **numbered lists, not tables**.
- For feature announcements: lead with the feature, not meta/expose angles.
- If a watchlist channel has been deleted or made private, skip it and note in the report.
- Deduplicate: if a video appears in both watchlist results AND keyword discovery, only
  count it once (under watchlist).

## Integration with Other Skills

- Use `/youtube-outlier-titles @handle` for a deep-dive on any channel from the report
- Feed title patterns into `/youtube-ab-tester` for A/B test hypotheses
- Feed topic insights into `/youtube-scriptwriter` for content planning
