# Tools: VidTempla + Supadata

This skill leans on two MCP servers. Load what you need in one `ToolSearch` call, e.g.:

```
ToolSearch select:mcp__claude_ai_VidTempla__list_videos,mcp__claude_ai_VidTempla__list_comment_threads,mcp__claude_ai_VidTempla__search_youtube,mcp__claude_ai_VidTempla__get_video,mcp__claude_ai_Supadata__supadata_transcript,mcp__claude_ai_Supadata__supadata_metadata
```

## Channel-id resolution

Most VidTempla tools accept a handle, channel id, or URL directly in `channelId`. If you only have a
channel name, resolve it first with `search_youtube` (`type: "channel"`, `q: "<name>"`) and take the
`channelId`. Cache it. Known: Theo (t3.gg) = `UCbRP3c757lWg9M-U7TyEkXA` (`@t3dotgg`).

## Discovery — prefer `list_videos`

`list_videos` works for **public, unowned** channels (it fetches from the YouTube API) and for the
user's own channels (from VidTempla's DB). It paginates with a `cursor` and does **not** cost the
100-unit search quota that `search_youtube` does. This is the primary discovery path.

```
list_videos({ channelId: "@t3dotgg", sort: "publishedAt:desc", limit: 100 })
# -> { videos: [...], cursor: "..." }   keep calling with cursor until exhausted or past the date window
```

Filter to a date window client-side by `publishedAt`. If the user wants "all time", page to the end.
Capture per video: `videoId`, `title`, `url` (`https://www.youtube.com/watch?v=<id>`), `publishedAt`,
and `description`/`viewCount` if present (don't invent them).

Fallback discovery (only if `list_videos` fails for a channel): `search_youtube` with
`filterChannelId=<id>`, `type="video"`, `sort="date"`, `maxResults=50`, `publishedAfter=<since>`,
paginate via `pageToken`. An empty `q` is usually accepted; if rejected, sweep several broad topic
queries and dedupe by `videoId`. Note `search.list` does not return `viewCount`.

## Mining a single video — pull all three signals

**Transcript** (the content):
```
supadata_transcript({ url: "<video url>", text: true })
# large videos may return a jobId -> supadata_check_transcript_status; if so, fall back to
# description + comments and mark transcriptFound=false rather than blocking.
```

**Description + original sources** (the primary artifacts):
```
supadata_metadata({ url: "<video url>" })   # returns title, description, tags, date, stats
```
Parse the description for a "SOURCES"/"LINKS" block and capture those URLs. These are the original
blog posts / papers / tweets the creator was reacting to — the most valuable output of this skill.
`get_video({ id })` (VidTempla) is an alternative source of the description for owned channels.

**Top comments** (the audience demand signal):
```
list_comment_threads({ videoId: "<id>", order: "relevance", maxResults: 60 })
```
Read comments for: explicit requests ("please make a video on X", "how do you do Y"), points of
confusion (what people didn't get), disagreement/corrections, and links commenters share. Distill a
few recurring "audience signals" per video — these tell you which ideas have proven demand and which
follow-up videos people are literally asking for. `order: "relevance"` surfaces the most-liked/most-
discussed threads, which is what you want; use `order: "time"` only if you specifically need recency.

Comments are public-readable, so `channelId` can be omitted (it reads with any connected channel's
token). If comment reading fails for a video, continue without it and note it; don't abort the video.

## Optional: performance ranking

For owned channels you can rank or filter the shortlist by real performance with
`get_video_analytics({ id, metrics: "views", startDate, endDate })`. For unowned channels you usually
cannot get reliable view counts cheaply, so rank by novelty + source-traceability and **say so** in
the report's caveats rather than implying a performance-based ranking.

## Following links

Don't judge an idea from a title. Open the SOURCES links, the article behind a referenced story, and
links commenters share — fetch them (`mcp__claude_ai_Exa_Advanced__web_fetch_exa` or `WebFetch`) and
read the actual content before deciding an idea is worth surfacing, and trace each insight to its
true primary source.
