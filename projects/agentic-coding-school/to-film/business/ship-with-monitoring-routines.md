---
duration: 6-10 min
batch: 2
order: 8
batch_name: Marketing Automation
class: business
chapter: Marketing Automation
status: filmed
---
# The Hook

"Coding agents made shipping 10x faster. Checking on what you shipped didn't. Here's how to close the loop in 30 seconds."
# The Problem

You add a new feature. You instrument it with PostHog events. You deploy. You move on.

Two weeks later the data is sitting in a dashboard you forgot you built, and you have no idea if the feature is working, ignored, or actively broken. The velocity gap between *shipping* and *learning-from-what-you-shipped* is where most startup instinct dies.

The old answer was "go check your dashboards every morning." That doesn't survive contact with a week where you ship 8 features.

![[images/ship-with-monitoring-routines/problem/1.jpg]]
# The Pattern

Every new feature gets three things, not two:

1. The code
2. The analytics events
3. **A monitoring routine with an expiration date**

The routine is a markdown file describing what to check (events, metrics, what counts as interesting) and a scheduled cron that runs it daily for a week, pushing the summary to Telegram or Slack.

After a week you either keep it (drop to weekly), kill it (feature is boring), or act on it (feature is broken).

![[images/ship-with-monitoring-routines/pattern/1.jpg]]
# What to Cover

1. **The velocity gap** — ship time ≪ learn time, and it's getting worse. Show the failure mode: a graveyard of instrumented-but-unread features.
2. **The three-part ship unit** — code + events + a time-boxed routine. The time-box is the key discipline: monitoring that never expires is just another dashboard nobody opens.
3. **Demo — build the loop for a real feature:**
   - Ship a small feature with PostHog events (e.g. a post-signup survey)
   - Write a `routines/feature-name.md` file: what to query, what counts as a signal, how to summarise
   - Use `/schedule` to create a daily cron agent that runs the routine and pushes to Telegram
   - Show the first morning's Telegram message landing on the phone
1. **Slack channel variant** — for team contexts, create a dedicated `#feature-xyz` Slack channel at ship time, point the cron at it, delete the channel when you're done watching. Same discipline, team-shaped.

![[images/ship-with-monitoring-routines/slack-variant/1.jpg]]
5. **Why Claude-driven and not a PostHog alert** — threshold alerts are for "metric X crossed Y." Agent-driven routines are for "here are the 3 interesting free-text answers this morning, here's what surprised me about the drop-off at step 2." Judgment, not thresholds.

![[images/ship-with-monitoring-routines/judgment-not-thresholds/1.jpg]]

6. **Expiring the routine** — the last step of a routine is a reminder to kill the routine. Force the cleanup; otherwise every ship leaks a standing cron.
7. 
![[images/ship-with-monitoring-routines/expiring-routine/3.jpg]]

### Key Tools

- Claude Code `/schedule` skill (remote cron agents, no local session needed)
- Telegram skill or a disposable Slack channel
- PostHog events (or any analytics source the agent can query)
- A `routines/` folder in the repo — the source of truth for what each cron runs
### The One-Liner

**"Every new feature ships with an expiration-dated monitoring routine."**
