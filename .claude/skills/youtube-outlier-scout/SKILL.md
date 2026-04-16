---
name: youtube-outlier-scout
description: |
  Daily niche scout that monitors a watchlist of YouTube channels for outlier videos
  and searches keywords for trending content in the AI/coding niche. Use this skill
  when the user says "run the scout", "outlier scout", "what's trending", "daily report",
  "check the watchlist", "any outliers today", or wants a broad view of what's
  performing in their YouTube niche. Also trigger when the user asks to add/remove
  channels or keywords from the watchlist.
argument-hint: [daily|watchlist-only|keywords-only|refresh-baselines]
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

Monitor a watchlist of YouTube channels and search niche keywords to surface
**recent** outlier videos and trending title patterns in Ray's content niche.

The daily report focuses on what's happening NOW -- videos published in the last
7 days that are already outperforming their channel's baseline.

## Arguments

`/youtube-outlier-scout [mode]`

- `$0` -- **mode** (optional): Which scan to run.
  - `daily` (default): watchlist recent scan + keyword discovery, combined report
  - `watchlist-only`: only scan watchlist channels, skip keyword discovery
  - `keywords-only`: only run keyword discovery, skip watchlist
  - `refresh-baselines`: full historical scan of all channels to update cached medians
  - `add <@handle>`: add a channel to the watchlist
  - `remove <@handle>`: remove a channel from the watchlist
  - `add-keyword <term>`: add a keyword to the search list
  - `remove-keyword <term>`: remove a keyword from the search list

## Configuration

**Watchlist file:** `watchlist.yaml` in this skill directory
**Baselines cache:** `baselines.yaml` in this skill directory
**Reports:** `reports/YYYY-MM-DD.md` in this skill directory

The watchlist contains:
- `channels:` -- list of YouTube handles to monitor
- `keywords:` -- list of search terms for niche discovery
- `min_multiplier:` -- outlier threshold (default 3x median)

## Data Access

**Primary tool: yt-dlp** (installed at `/opt/homebrew/bin/yt-dlp`)

### Channel baseline (full scan -- cached, refresh weekly)

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

### Recent videos only (daily scan -- fast)

Only pull the last 10 videos per channel to check for new outliers:

```bash
yt-dlp --flat-playlist --playlist-end 10 --print "%(id)s" \
  "https://www.youtube.com/@Handle/videos" 2>/dev/null | \
  xargs -P 10 -I {} sh -c \
  'yt-dlp --no-download --print "%(id)s|%(title)s|%(view_count)s|%(upload_date)s" \
  "https://www.youtube.com/watch?v={}" 2>/dev/null'
```

Then filter to videos from the last 7 days and compare against cached median.

### Keyword discovery (per keyword)

```bash
yt-dlp "ytsearch20:<keyword>" --no-download \
  --print "%(id)s|%(title)s|%(view_count)s|%(channel)s|%(upload_date)s" 2>/dev/null
```

Returns: `videoId|title|viewCount|channelName|uploadDate(YYYYMMDD)`

Filter to videos published within the last 48 hours.

## Process

### Step 0 -- Read Config + Check Baselines

Read `watchlist.yaml` and `baselines.yaml` from this skill's directory.

**baselines.yaml format:**
```yaml
last_refreshed: "2026-04-16"
channels:
  "@ColeMedin":
    median: 46398
    video_count: 110
  "@nicksaraev":
    median: 27232
    video_count: 99
  # ...
```

If `baselines.yaml` doesn't exist or `last_refreshed` is more than 7 days ago,
run a full baseline refresh first (Step 1a). Otherwise, skip to Step 1b.

### Step 1a -- Full Baseline Refresh (weekly, or first run)

Process all channels using subagents for parallelism. Spawn 5 subagents,
each handling 4-5 channels:

For each channel:
1. Pull ALL videos via yt-dlp two-step approach
2. Calculate median views
3. Store in baselines.yaml

**Important:** Use `timeout: 300000` for the batch yt-dlp commands. Large channels
(100+ videos) take 30-60 seconds each.

Each subagent writes results to `/tmp/outlier-scout-<handle>.tsv`

After all subagents complete, compile baselines.yaml with median + video_count
per channel and today's date as `last_refreshed`.

### Step 1b -- Daily Recent Scan (fast, ~1-2 minutes)

For each channel, only pull the **last 10 videos** and filter to the last 7 days:

```bash
CUTOFF=$(date -v-7d +%Y%m%d)
yt-dlp --flat-playlist --playlist-end 10 --print "%(id)s" \
  "https://www.youtube.com/@Handle/videos" 2>/dev/null | \
  xargs -P 10 -I {} sh -c \
  'yt-dlp --no-download --print "%(id)s|%(title)s|%(view_count)s|%(upload_date)s" \
  "https://www.youtube.com/watch?v={}" 2>/dev/null' | \
  awk -F'|' -v cutoff="$CUTOFF" '$4 >= cutoff'
```

Compare each recent video's views against the cached median from baselines.yaml.
Flag any video hitting min_multiplier (3x) or above.

**Parallelism:** Still use subagents (5 batches of 4-5 channels), but each
subagent only pulls 10 videos per channel instead of all. Much faster.

### Step 2 -- Keyword Discovery

For each keyword in the search list:

1. Run `yt-dlp "ytsearch20:<keyword>"` to get 20 results with view counts
2. Filter to videos published in the last 48 hours:
```bash
YESTERDAY=$(date -v-1d +%Y%m%d)
awk -F'|' -v yesterday="$YESTERDAY" '$5 >= yesterday'
```
3. Deduplicate across keywords (same video can match multiple terms)
4. For videos with high raw views (>10k in first 48h), note them as discoveries

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

Across ALL recent outliers (watchlist + discoveries), analyze:

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
- Which topics are trending this week vs. evergreen?
- Any new channels emerging in the niche?

### Step 5 -- Generate Report

Output to terminal AND save to file.

The report should focus on **what's new and actionable today**, not historical data.

**Report structure:**

```markdown
---
tags: [youtube, outlier-scout, daily]
date: YYYY-MM-DD
channels-scanned: N
keywords-searched: N
recent-outliers-found: N
discoveries-found: N
---

## Outlier Scout Report -- YYYY-MM-DD

### Trending Right Now (Last 48h)

Videos from keyword discovery that are gaining traction:
1. **"Title"** -- X views (Channel, date) -- keyword: term
2. ...

### Watchlist -- Recent Outliers (Last 7 Days)

Videos from tracked channels published in the last 7 days hitting 3x+ their median.

| # | Channel | Title | Views | Multiplier | Published |
|---|---------|-------|-------|------------|-----------|
| 1 | ...     | ...   | ...   | ...x       | ...       |

### Title Patterns This Week

**Cross-channel patterns (strongest signals):**
- [pattern] -- seen in N outliers across N channels

**Title formulas working right now:**
1. [formula with example]
2. [formula with example]

### Channels to Watch

New or small channels with breakout videos:
- @handle -- "Video Title" (Nx their usual, X views)

### Actionable Ideas for Ray

Title + topic ideas based on this week's outlier patterns:
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

### Step 7 -- Send Telegram Summary

After saving the report, send a condensed summary to Ray on Telegram using the
telegram-message skill's send script:

```bash
bash ~/.claude/skills/telegram-message/scripts/send-message.sh "<summary>"
```

The Telegram message should be concise (Ray reads on his phone) and include:
- Report date and channels/keywords scanned
- Top 5 trending videos (last 48h) with view counts
- Top title formulas with multipliers
- Top 5 biggest outliers with multipliers
- One line: "Full report saved to ray-os"

Keep it under ~1500 characters. No markdown formatting (plain text only for Telegram).

## Watchlist Management

When the user says `add @handle` or `remove @handle`:

1. Read `watchlist.yaml` from this skill's directory
2. Add/remove the handle from the channels list
3. Write back the updated file
4. Confirm the change

Same for `add-keyword` and `remove-keyword`.

## Performance Notes

**Daily scan (with cached baselines):**
- 22 channels x 10 recent videos = ~220 video lookups (vs ~1,500+ for full scan)
- 7 keywords x 20 results = 140 video lookups for keyword discovery
- **Total estimated runtime: 1-2 minutes** with parallel subagents
- Use `timeout: 120000` for daily scans

**Full baseline refresh (weekly or first run):**
- 22 channels with ~50-100 videos each = ~1,500-2,200 video lookups
- **Total estimated runtime: 5-8 minutes** with 5 parallel subagents
- Use `timeout: 300000` for baseline refresh

## Important Notes

- **NEVER use em or en dashes** in any output text. Use `--` instead.
- Title + thumbnail are a **pair** -- note when thumbnails complement or duplicate the title.
- Present title ideas as **numbered lists, not tables**.
- For feature announcements: lead with the feature, not meta/expose angles.
- If a watchlist channel has been deleted or made private, skip it and note in the report.
- Deduplicate: if a video appears in both watchlist results AND keyword discovery, only
  count it once (under watchlist).
- The first run in a new session always checks baselines.yaml age. If >7 days old,
  it auto-triggers a refresh before the daily scan.

## Integration with Other Skills

- Use `/youtube-outlier-titles @handle` for a deep-dive on any channel from the report
- Feed title patterns into `/youtube-ab-tester` for A/B test hypotheses
- Feed topic insights into `/youtube-scriptwriter` for content planning
