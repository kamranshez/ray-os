---
name: youtube-outlier-titles
description: |
  Browse any YouTube channel, identify outlier videos (3x+ above channel average views),
  and analyze their titles for patterns. Use this skill whenever the user wants to find
  outlier videos on a channel, analyze what titles are working for another creator, scout
  title ideas, or says things like "find outliers on this channel", "what's working for
  [creator]", "analyze their titles", "outlier analysis", "title research", "scout this
  channel", or provides a YouTube channel URL/handle and wants to understand their
  best-performing content. Also trigger when the user shares a channel page screenshot
  with view counts and wants analysis.
argument-hint: <channel-handle-or-url> [min-multiplier]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - mcp__claude_ai_VidTempla__search_youtube
  - mcp__claude_ai_VidTempla__list_channels
  - mcp__claude_ai_VidTempla__get_channel
  - mcp__claude_ai_Exa__web_search_exa
---

# /youtube-outlier-titles -- YouTube Outlier Title Scout

Browse any YouTube channel, identify videos that massively outperform the channel average,
and extract title patterns worth stealing.

## Arguments

`/youtube-outlier-titles <channel> [min-multiplier]`

- `$0` -- **channel** (required): YouTube channel handle (e.g. `@TheAIAutomators`), channel ID
  (e.g. `UC...`), or full channel URL. If the user pasted a screenshot instead, extract the
  channel name from it.
- `$1` -- **min-multiplier** (optional): Minimum outlier threshold as a multiplier of channel
  median views. Defaults to `3` (i.e. 3x the median). Use `2` for broader results, `5` or
  `10` for only mega-outliers.

## Data Access

**Primary data source: yt-dlp** (installed at `/opt/homebrew/bin/yt-dlp`)

yt-dlp can pull video data for any public channel without API quota limits.
**Important**: `--flat-playlist` does NOT return view counts. Use a two-step approach:

**Step 1: Get video IDs (fast, ~2s)**
```bash
yt-dlp --flat-playlist --print "%(id)s" "https://www.youtube.com/@ChannelHandle/videos" 2>/dev/null
```

**Step 2: Batch-fetch view counts in parallel (10 at a time, ~30s for 88 videos)**
```bash
yt-dlp --flat-playlist --print "%(id)s" "https://www.youtube.com/@ChannelHandle/videos" 2>/dev/null | \
  xargs -P 10 -I {} sh -c 'yt-dlp --no-download --print "%(id)s|%(title)s|%(view_count)s|%(upload_date)s" "https://www.youtube.com/watch?v={}" 2>/dev/null' | \
  sort -t'|' -k3 -rn
```

Returns pipe-delimited rows sorted by views: `videoId|title|viewCount|uploadDate(YYYYMMDD)`
Use `timeout: 300000` for large channels.

**Thumbnails**: available at `https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg`
(fall back to `hqdefault.jpg` if maxres unavailable)

**Channel resolution** (if needed): use VidTempla `search_youtube` to find channel IDs
from handles. Ray's channel ID for auth: `UCLA7cJBnqr0nLF2bQBD9uUg`

## Process

### Step 1 -- Resolve Channel

If the user gave a `@handle`, construct the URL directly:
`https://www.youtube.com/@HandleName/videos`

If they gave a channel ID or ambiguous name, use VidTempla search to resolve:
```
mcp__claude_ai_VidTempla__search_youtube({
  channelId: "UCLA7cJBnqr0nLF2bQBD9uUg",
  q: "<channel name>",
  type: "channel",
  maxResults: 5
})
```

### Step 2 -- Pull All Videos via yt-dlp

```bash
yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(view_count)s|%(duration)s|%(upload_date)s" \
  "https://www.youtube.com/@ChannelHandle/videos" 2>/dev/null
```

Parse the output into a structured dataset. For very large channels (500+ videos),
this may take 10-20 seconds -- use `timeout: 60000`.

### Step 3 -- Calculate Outliers

From the parsed data, compute:

1. **Median views** (more robust than mean -- immune to outlier skew)
2. **Mean views** (for reference)
3. **Outlier multiplier** for each video: `video_views / median_views`
4. **Filter** to videos with multiplier >= threshold (default 3x)
5. **Sort** outliers by multiplier descending

Use inline bash arithmetic or a quick python snippet for the stats:
```bash
# Example: extract view counts and compute median
... | cut -d'|' -f3 | sort -n | awk '{a[NR]=$1} END {print a[int(NR/2)+1]}'
```

### Step 4 -- Analyze Title Patterns

For each outlier video title, examine:

**Structure:**
- Curiosity gaps ("You've been doing X wrong", "Here's What to Build Instead")
- Power words (UNLOCK, DEPLOY, COMPLETE, KEY, BEAST)
- Number usage ("10x", "800+", "5,000", "8 Modules")
- Question format vs statement format
- Parenthetical qualifiers ("(Full Guide)", "(Step by Step)", "(n8n)")
- Length (character count, word count)
- Name-dropping (people, companies, tools)

**Framing:**
- Problem-first vs solution-first
- "I did X" (personal) vs "How to X" (tutorial) vs "X Just Changed" (news)
- Negative framing ("Will Fail", "Not Enough") vs positive ("Game-Changer", "Smarter")
- Specificity level (vague "AI Agents" vs specific "Qwen3.5 Agent")

**Patterns across outliers:**
- Which title formulas repeat in the outlier set?
- Do outliers cluster around specific topics?
- Is there a correlation between title length and performance?
- Do recent outliers use different patterns than older ones?

### Step 5 -- Thumbnail Quick-Scan (Optional)

For the top 5 outliers, download and visually inspect thumbnails:
```
https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg
```

Note whether title + thumbnail are complementary or redundant.
This is secondary to title analysis but adds context.

### Step 6 -- Generate Report

Output a structured markdown report to the terminal:

```markdown
## Outlier Analysis: @ChannelName

**Channel Stats:** X subscribers, Y videos analyzed
**Median views:** Z | **Mean views:** W

### Outliers (>= Nx channel median)

| # | Title | Views | Multiplier | Duration | Published |
|---|-------|-------|------------|----------|-----------|
| 1 | ...   | ...   | ...x       | ...      | ...       |

### Title Formula Patterns
- [formula] -- used in N outliers, avg Mx multiplier
- [formula] -- used in N outliers, avg Mx multiplier

### What's Working
- [specific observations about title patterns that correlate with high performance]

### What's NOT Working
- [title patterns from non-outlier videos that underperform]

### Actionable Title Ideas for Ray
- [specific title formulas Ray could test, adapted to his content]
- [direct A/B test hypotheses based on outlier patterns]
```

### Step 7 -- Save Report (Optional)

If the user wants to keep the research, save to:
```
/Users/ray/Desktop/ray-os/socials/youtube/analysis/outliers/<channel-handle>.md
```

Use kebab-case filename. Add frontmatter:
```yaml
---
tags: [youtube, outlier-analysis, title-research]
date: YYYY-MM-DD
channel: "@HandleName"
videos-analyzed: N
outliers-found: N
median-views: N
---
```

## Important Notes

- **NEVER use em or en dashes** in any output text (Ray's preference). Use `--` instead.
- Title + thumbnail must be analyzed as a **pair** -- they work together, not independently.
  A great title with a redundant thumbnail is a missed opportunity.
- For channels with < 10 videos, lower the threshold to 2x automatically.
- If the user provided a screenshot with VPH (Views Per Hour) data, use VPH as an
  additional signal -- high VPH means a video is currently trending, not just lifetime views.
- Present title options as **numbered lists, not tables** (Ray's preference from feedback).
- For feature announcements: lead with the feature, not meta/expose angles.

## Multi-Channel Mode

If the user provides multiple channels, run them sequentially and add a comparative
summary at the end highlighting title patterns that appear across multiple channels.
Cross-channel patterns are the strongest signals.

## Integration with Other Skills

- Feed title patterns into `/youtube-ab-tester` for A/B test hypotheses
- Feed topic insights into `/youtube-scriptwriter` for content planning
- Use `/youtube-title-researcher` for broader niche research beyond a single channel
- Feed thumbnail observations into `/youtube-thumbnail-generator` for design inspiration
