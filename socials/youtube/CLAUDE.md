# YouTube

Ray's YouTube channel data and research.

- `ab-tests/` — Ray's own title and thumbnail A/B test results
- `research/` — Competitor video transcript analysis (hooks, structure, retention patterns)
- `performance/` — Ray's own videos audited against competitor research findings
- `improvements.md` — **Living doc**: active production improvements, per-video experiment notes, and viewer feedback log. Check this before scripting or editing any video.
- `transcripts/` — Downloaded video transcripts organized by channel

## Video Frontmatter

All video scripts in `videos/` should include YouTube stats in their frontmatter. Fetch data from VidTempla using `get_video` and update the frontmatter in this format:

```yaml
---
youtube-id: dQw4w9WgXcQ
youtube-title: "The Actual YouTube Title"
published: 2026-03-11
duration: "7:57"
views: 39199
likes: 1001
comments: 88
status: uploaded
fetched: 2026-04-09
---
```

- `fetched` is the date the stats were last pulled — stats go stale, so update periodically
- Keep any existing frontmatter fields (tags, source, date) alongside the YouTube fields
- Only add YouTube stats for videos that have been uploaded (match by YouTube ID or publish date)

## A/B Test Logging

When recording A/B test results, include a timestamp on each round:

```markdown
### Title A/B Test Round N (YYYY-MM-DD HH:MM)
```

This tracks when results were captured so we can see how quickly tests converge and how much time passed between rounds.
