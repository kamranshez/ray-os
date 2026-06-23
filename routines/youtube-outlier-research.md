Run /youtube-outlier-scout for today.

This is an unattended scheduled run. Apply these overrides:

# Resilience
- Do NOT spawn subagents -- they fail with "Prompt is too long" in this environment. Run yt-dlp directly via Bash with run_in_background: one parallel loop for the 22 watchlist channels, one sequential loop for the 7 keywords, both writing to /tmp/outlier-scout and /tmp/outlier-scout-kw.
- If any single tool call returns a transient error (permission stream closed, network blip, rate limit), retry once. Only abort the run if the same call fails twice in a row.
- On resume from any interruption, check /tmp/outlier-scout and /tmp/outlier-scout-kw for cached .tsv files first. If present and non-empty, continue from there -- do NOT restart the scan.
- If the system says "Continue from where you left off" with no new user task, treat that as an instruction to resume the scheduled run, not a no-op. Keep going until done.

# Definition of done
The run is complete only when BOTH:
  1. reports/YYYY-MM-DD.md exists with today's date
  2. The slackbot-message skill has posted the summary to #yt-outlier
Until both are true, do not stop and do not return a summary.

# Inputs
- Watchlist + keywords: .claude/skills/youtube-outlier-scout/watchlist.yaml
- Cached medians: .claude/skills/youtube-outlier-scout/baselines.yaml
- If baselines.last_refreshed is >7 days old, refresh first.

# Scope
- Watchlist: last 10 videos per channel, filter to last 7 days, flag anything >= 3x channel median.
- Keyword discovery: 20 results per keyword, filter to last 48h, dedupe against watchlist.
- Auto-add (Step 3a/3b in SKILL.md): for each newly-discovered channel not already on the
  watchlist, evaluate the `auto_add` bars (min_subscribers, min_outliers, on-niche). Channels
  that clear ALL bars get appended to watchlist.yaml automatically; near-misses go to
  auto_add_rejected. List any auto-adds in the report AND the Slack summary. This mutates
  watchlist.yaml in the repo -- that's expected, no approval gate.
- Title-pattern analysis across all flagged videos.
- **Format-Gap Analysis (Step 4b in SKILL.md) -- REQUIRED, this is the headline.** For
  every outlier compute views/sub ratio (not just channel-median multiplier) and classify
  its format. Spotlight any small-channel-big-views case (views/sub > 5x, e.g. a 10k-sub
  channel with 700k views) by name -- those are the strongest "they're doing something we
  aren't" signals. Pull Ray's own recent videos (channel ID UCLA7cJBnqr0nLF2bQBD9uUg),
  classify their formats, compute his mix, and report which winning formats he under-uses.
  Cross-reference socials/youtube/ab-tests/results.md to tag ideas PROVEN/NEW. Package the
  top 3-5 bangers as concrete video ideas (format + title options + thumbnail concept).

# Output
Save to .claude/skills/youtube-outlier-scout/reports/YYYY-MM-DD.md, then post a <2500-char
Slack-mrkdwn summary to #yt-outlier via the slackbot-message skill. **Lead the Slack post
with the Format Gap section** (the bangers + what we're doing differently), then the
trending/outlier lists and any auto-adds.
