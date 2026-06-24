# Title + Format Analysis Framework

(Absorbed from the former `youtube-title-researcher` skill. Two jobs: classify
**titles** and classify **formats**, then ground both against Ray's own channel.)

## Metrics to Collect Per Video

| Field | How to Get It |
|-------|---------------|
| Title | From search results / yt-dlp |
| Channel | From search results / yt-dlp |
| Views | From metadata |
| Subscriber count | `%(channel_follower_count)s` via yt-dlp, or vidIQ overlay |
| Views/Sub ratio | Calculate: views / subscribers -- the key normalization metric |
| Channel-median multiplier | views / channel median (the scout's primary outlier metric) |
| VPH (views per hour) | From vidIQ overlay if available -- means trending NOW |

**Two complementary outlier metrics -- use BOTH:**

1. **Channel-median multiplier** (`views / channel median`) -- "is this video an
   outlier *for this channel*?" Good for watchlist monitoring.
2. **Views/Sub ratio** (`views / subscriber count`) -- "is this video an outlier
   *for the channel's size*?" Better cross-channel signal. This is the metric that
   flags the small-channel-huge-video case (e.g. 13.3k subs, 736k views = 55x).

**Views/Sub ratio benchmarks:**
- **> 5.0x** = Mega outlier (the packaging/format is doing enormous work -- study it)
- **1.0x - 5.0x** = Viral outlier
- **0.3x - 1.0x** = Strong performer
- **0.1x - 0.3x** = Average for niche
- **< 0.1x** = Underperforming (channel size carried it)

Always surface the small-channel-big-views cases explicitly. A 10k-sub channel with
a 700k-view video is the single strongest "they are doing something we are not"
signal, because subscriber base cannot explain it -- only packaging and format can.

## Title Pattern Categories

Classify each title into one or more of these patterns:

### Authority Patterns
- **Credential authority**: "How I Use X (Job Title/Company)"
- **Brand authority**: "Anthropic Just [verb]..." -- company name as source
- **Expert framing**: "Pro Tips", "Advanced", "Master"

### Emotional Hook Patterns
- **Negative hook**: "You're Using X Wrong", "Stop Doing X"
- **Superlative claims**: "Insane", "Crazy", "Mind-Blowing"
- **Outcome promises**: "10x Your Productivity", "Unfair Advantage"
- **Third-person reaction**: "His/Their Workflow Is Insane"
- **Regret hook**: "I Wish I Knew From the Start"

### Structural Patterns
- **Number lists**: "10 Tips", "8 Use Cases", "5 Features"
- **Time-constrained**: "in 7 Minutes", "in 13 Mins"
- **Definitive**: "The Only Tutorial You Need"
- **News/update**: "Just Added", "Just Dropped", "New"
- **How-to**: "How to Use X", "How I Use X"

### Underperforming Patterns (avoid)
- **ALL CAPS hype**: "Just Changed EVERYTHING" -- feels overdone
- **Curiosity gap**: "Nobody's Talking About" -- too vague in this niche
- **Explained/educational**: "X Explained" -- consistently underperforms
- **Trailing ellipsis**: "The BEST FEATURE is..." -- cliffhanger fatigue
- **Pipe format**: "Title | Subtitle" -- underperforms clean titles
- **Repeated/templated titles**: reusing the same title shell ("Anthropic Just
  Dropped the Feature Nobody Knew They Needed") trains the algorithm and audience
  that videos are interchangeable. Strong negative signal -- flag when Ray does it.

## Format Categories (the axis titles miss)

Two videos can share a title pattern but be completely different *formats*. Format is
about what the video structurally IS. Classify every outlier into one:

- **News / update** -- "here's what shipped." Caps near sub base, decays in ~72h.
- **Test / battle / head-to-head** -- "X vs Y, which wins?" Evergreen, searchable,
  shareable. Strong curiosity gap. (The Pat Simmons Opus-vs-Fable case.)
- **Review / verdict** -- "is X actually good? (honest)." Opinion + judgment.
- **Build / demo** -- "I built X with Y." Visual payoff carries retention.
- **Tutorial / how-to** -- "how to do X." Evergreen, search-driven.
- **Transformation / outcome** -- "I did X for N and here's what happened."
- **List / roundup** -- "N tools/features/tips."
- **Reaction / commentary** -- responding to a trend or another creator.

For each format, note: is it evergreen or perishable? Does it pull beyond the
creator's subscriber base (high views/sub)? Is it visually demonstrable?

## Ray's channel grounding

Cross-reference findings against Ray's own data before recommending anything:

- **A/B history**: per-test files under
  `.claude/skills/youtube-ab-tester/references/results/YYYY-MM/` -- tag each title pattern
  as PROVEN (won an A/B test), NEW (untested), or UNDERPERFORMING (lost a test).
- **Ray's format mix**: pull his own recent videos (channel ID
  `UCLA7cJBnqr0nLF2bQBD9uUg`) and classify each into the format categories above to
  get his current distribution. His default is heavily **news**; his outliers
  (331k Anki how-to, 54k Replit review) are non-news formats. The gap between the
  formats winning for OTHERS and the formats he actually PUBLISHES is the core output.

## Search Queries to Use

Filtered to **"This month"** + **"Videos"** (browser) or `ytsearch20:` (yt-dlp):

1. `"claude code" tips workflow`
2. `"claude code" new update features`
3. `"claude code" tutorial beginner`
4. `claude code agent teams`

Sort by relevance, not raw view count (relevance surfaces niche-relevant results;
raw view count gets polluted by large general channels).
