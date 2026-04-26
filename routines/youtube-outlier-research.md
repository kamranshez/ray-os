Run /youtube-outlier-scout.

Read the watchlist and baselines from .claude/skills/youtube-outlier-scout/, scan the last 10 videos per channel using yt-dlp, filter to last 7 days, compare against cached medians, run keyword discovery filtered to last 48h, save the report to .claude/skills/youtube-outlier-scout/reports/YYYY-MM-DD.md.

Then send the report to the Slack channel #yt-outlier with the Slack message skill.

If baselines.yaml is >7 days old, refresh them first.