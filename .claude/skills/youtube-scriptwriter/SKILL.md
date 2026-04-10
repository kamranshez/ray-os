---
name: youtube-scriptwriter
description: "Turn feature announcements, changelogs, or release notes into view-optimized YouTube video outlines. Use when the user pastes a changelog, feature announcement, release notes, or describes a new feature and wants help planning how to structure a YouTube video script. Also use when the user asks to write a script, outline a video, plan video structure, or says things like 'let's make a video about X', 'script this', 'how should I structure this video', or 'turn this into a video'. Use this skill even when the user just shares a feature/tool and seems to be brainstorming content ideas."
---

# YouTube Scriptwriter

Write scripts for Ray's YouTube channel (@RAmjad) — Claude Code tutorials and AI tooling content aimed at developers and increasingly non-developers.

## Before writing anything

1. Read the reference scripts in `references/` — these are Ray's proven hits. Study their structure before drafting:
   - `auto-dream-script.md` — 90k views in 2 days (gold standard)
   - `skills-2.0-script.md` — 40k views in 2 days
   - `btw-and-fork-script.md` — 30k views in 1 day
2. Read `socials/youtube/improvements.md` in the project root — active production improvements. Apply any that are relevant.
3. If the video topic relates to an existing script in `socials/youtube/videos/`, read it for context on what's already been covered.

## The Meta-Pattern (what all 3 hits share)

These three scripts look different on the surface — one's about memory, one's about testing, one's about context management. But they share a deep structure that explains why they all broke out. This is the formula.

### 1. Name the Invisible Problem

All three scripts start by naming something the viewer *feels* but can't articulate:
- Auto-dream: "Your memory files are full of stale, contradictory notes" (everyone noticed this but nobody named it)
- btw/fork: "Context pollution" — coined a term for attention degradation mid-session
- Skills 2.0: "Building a skill was pure vibes" — named the lack of testing

The pattern: find the pain that has no name yet, and name it. This is why people share the video — they finally have vocabulary for their frustration.

**Coin a term.** The data here is stark: the only 3 videos that coined a memorable term ("context pollution", "capability uplift vs encoded preference", "sleep-deprived agent") are the top 3 by views. None of the next 7 top performers coined anything. Every script should try to create at least one phrase viewers will screenshot and reuse. "Context pollution" is the kind of term that spreads beyond the video.

### 2. Human Analogy as Structural Backbone (not decoration)

Every hit maps the technical concept to a human experience, and the analogy isn't a throwaway line — it's the organizing principle of the entire video:
- Auto-dream: Memory consolidation = REM sleep. Every section references sleep/dreaming.
- btw/fork: Context window = your desk. /btw = asking without putting paper on it. Fork = second desk. Rewind = clearing the mess.
- Skills 2.0: Evals = teacher grading an exam. Capability vs preference = two types of knowledge.

Ask yourself: "What does this feature do that humans also do?" Build the video around that mapping. If the analogy only appears once, it's not doing enough work.

### 3. 3-Beat Hook (first 20-30 seconds)

**Use discovery framing, not announcement framing.** March 2026 confirmed this pattern hard. Every March video that opened with personal discovery beat its peers:
- Auto Dream (97K views): "I was just doing some vibe coding and I noticed something weird"
- /btw (39K views): "Claude Code added a feature I didn't even realize I needed"
- Kills OpenClaw (30K, **$13,776 — best revenue of the month**): "I woke up a few minutes ago and checked the changelog"

Mid-tier March videos that opened with "Anthropic Just Dropped X" verbally (even when the title used that phrase) averaged 30–60% fewer views than the discovery-framed ones. The title can say "Anthropic Just Dropped X" — the spoken opening cannot. Discovery framing ("I stumbled onto this") makes viewers lean in. Announcement framing ("here's the news") makes them evaluate whether to stay.

Every script opens with three beats:
- **Discovery or novelty signal** — frame it as something Ray found, not something Anthropic announced
- **What it actually is** — one concrete sentence explaining the feature
- **The analogy/reframe that makes it click** — connect to the human experience or name the problem

### 4. The Problem Before the Solution (30s - 2min)

Before explaining how the feature works, make the viewer feel the pain it solves. Use second person — "you've probably run into this." Be brutally specific about the failure mode, not abstract:
- Auto-dream: stale memory files, contradictory notes, relative dates that decay
- btw/fork: noise in conversation, off-topic messages degrading all future outputs
- Skills 2.0: "try it a few times, go 'yeah that seems to work,' and move on"

Concrete details build trust. Vague problems feel like filler.

**Use the Problem → Old Workaround → New Solution triple.** The top performers don't just show the problem and the solution — they add a middle step showing Ray *already tried* to solve it the hard way. This builds credibility and makes the new solution feel like relief:
- btw/fork: Problem (interrupting pollutes context) → Old workaround (--fork-session, "clunky") → New solution (/btw)
- Remote control (36k): Problem (can't use Claude from phone) → Old workaround (tmux + Tailscale + Terminus, "a hassle") → New solution (claude rc)
- Kills OpenClaw (31k): Problem (remote was passive) → Old workaround (OpenClaw) → New solution (/loop cron)

Three acts inside the problem section. The "old workaround" step is what separates 30k+ videos from 15k ones — it proves Ray lives in the problem, not just reports on it.

### 5. Single Feature Deep Dive (2min - 6-7min)

One feature, explained thoroughly. Show the actual internals — real prompts, real code, real terminal output, real benchmark tables. All three hits do this:
- Auto-dream: the literal system prompt, the three phases, the trigger conditions
- btw/fork: the actual CLI flags, the tradeoff matrix
- Skills 2.0: real benchmark tables with pass rates and token counts

Structure in numbered phases or clear comparison sections. People need scaffolding to follow technical content.

**Concept-first, not demo-first.** The 40k+ videos explain the feature through analogies and show real internals (prompts, tables) but don't do live building. The 25-35k tier videos (remote control, kills OpenClaw, subagents) have extended live-coding sequences — setting up Telegram bots, SSHing into servers. Live demos are fine but they cap out around 30k. The videos that break 40k lead with the *idea*, not the tutorial. If there's a demo, narrate over it rather than building live.

### 6. The "Ray Thinks Deeper" Move

All three scripts have a moment where Ray goes beyond the announcement and adds original analysis:
- Auto-dream: connects to Mastra's Observational Memory (broader industry trend)
- btw/fork: "btw is the inverse of a subagent" (original insight not in the docs)
- Skills 2.0: "Anthropic kind of buries the lede" + the insurance claim example showing A/B is the wrong question for procedural skills

This is the section that makes people subscribe. It shows Ray isn't just parroting release notes — he's thinking about what the feature *means*. Every script needs one of: a broader trend connection, an original insight not in the docs, or a critique/gap the announcement missed.

### 7. Practical Takeaway (brief)

Brief, actionable. Where to enable it, what to configure, what it means for their workflow. Keep it short — the value was already delivered.

### 8. The Pitch Layer (separate from content structure)

Content structure is optimized for *views*. The pitch layer is optimized for *revenue*. They are different systems and must be planned separately. March 2026 data settled this:

| Pitch tactic | With | Without | Delta |
|---|---:|---:|---:|
| Masterclass CTA in first 90 seconds | $11,687 avg | $4,692 avg | **+149%** |
| Urgency + price escalation language | $13,776 (Mar 7) | $5,880 avg | **+134%** |
| "Best at their company" social proof | $12,142 (Skills 2.0) | $6,064 avg | **+100%** |
| Newsletter-first closing | $4,601 avg | $8,489 avg | **−46%** |

**The old "single CTA at end, no mid-roll CTAs" rule was costing revenue.** Auto Dream followed that rule on 97K views and made only $6,029. Kills OpenClaw broke it (mid-video soft anchor + closing urgency pitch) and made $13,776 on 30K views.

**Apply the Mar 7 template to every regular video:**

**Soft anchor at 1:30–2:00** (after the hook lands, before the deep dive):
> "Before we continue — this video is sponsored by myself and my Claude Code Masterclass. Over 1,500 engineers from companies like [X] have taken it and many are now the best Claude Code user at their company. The lifetime plan retires [date] and the price is going up after that. Link below."

**Closing urgency pitch** (tied to the video topic):
> "So [feature summary]. If you want to go deeper on this, the Masterclass covers [specific deliverable]. The lifetime plan is gone after [date] and the price goes up. Link below."

**Rules:**
- Never newsletter-first on videos with a live masterclass deadline (March penalty: −46%)
- Always include a concrete deadline + price escalation, not a vague "check it out"
- Tie the closing pitch to a specific deliverable the video hinted at
- One pitch system at a time. If newsletter is the goal, skip the masterclass pitch entirely rather than stacking both weakly (Auto Dream's mistake)
- If a video crosses 30K views in 48 hours and the pitch was weak, **add a pinned comment with urgency + masterclass link**. Auto Dream would have captured ~$14K more with this single action.

## Adapting the Formula by Scope

The three hits show the formula scales to different video lengths:

| Video | 48hr Views | D1 Subs | D1 Avg Watch | Retention @50% | Has Broader Trend? |
|-------|-----------|---------|-------------|----------------|-------------------|
| Auto-dream | 86,662 | 1,113 (1.90%) | 2:52 | 36% | Yes (Mastra) |
| Skills 2.0 | 37,635 | 343 (1.21%) | 4:06 | 30% | Yes (eval=skill future) |
| btw/fork | 34,495 | 383 (1.45%) | 2:50 | 33% | No |

- **8-10 min (tight)**: Skip the full demo. Use the broader trend OR the original insight, not both. btw/fork is the template.
- **10-12 min (standard)**: Include the broader trend section AND either a demo or a deeper original analysis. Auto-dream is the template.
- **12+ min (deep)**: Full demo walkthrough + broader trend + original critique. Skills 2.0 is the template.
- **30-45 min (pillar)**: Lifestyle storytelling opening, no single-feature anchor, compress multiple techniques into one "how I actually use Claude Code" narrative. **Mar 2 Top 0.01% (41:31) is the template — it had a 3.16% site click-through rate, 4–5x any single-feature video in March, and produced $10K revenue on only 20K views.** Open with memorable lifestyle stories (Claude Code reverse-engineered a dating app API, script to auto-reconnect to Starbucks WiFi). Use for ~1 in 5 videos — it's the highest-converting format the channel has.

## Pacing Guidelines (from improvements.md)

- Speak ~50% slower than typical AI tutorial pace
- Let visuals linger 2-3 seconds after referencing them
- Keep natural pauses — don't script out every breath
- Add clear section titles/breaks between segments
- Use progressive reveal over static slides where possible

## What NOT to Do

- **No feature roundups.** Focused single-feature videos averaged 45K views in March vs 17K for thesis/leak/pillar formats — **a 2.6x gap.** If the announcement has 5 features, pick the most interesting one.
- **No "Anthropic Just Dropped X" spoken openings.** The title can use that framing; the first spoken line cannot. Every March video with an announcement-style verbal opening underperformed the discovery-framed peers on the same week by 30–60%.
- **No abstract intros.** Don't open with "In today's video we're going to..." — open with the discovery beat.
- **No repeated title templates within 60 days.** "Nobody Knew They Needed" was used twice in March (/btw Mar 11 at 39K → Auto Dream Mar 24) and once in Feb. Reuse compresses the novelty signal. Track recent titles before proposing a new one.
- **No newsletter-first closings on videos with a live masterclass deadline.** March penalty: −46% revenue. Newsletter-first averaged $4,601 per video; masterclass-first averaged $8,489.
- **No stacking 3 uploads in 3 days.** Mar 19/20/21 combined drove $8,500 across 5 unique days — less than the single Mar 11 /btw upload ($8,788 on its own). Overlapping 3-day windows cannibalize each other.
- **No slides-first approach.** Write the script first, plan visuals second. The verbal explanation carries the video; visuals support it.

## Output Format

Write the script as a markdown document with:
- Timestamp ranges for each section (estimated)
- Section headers matching the formula above
- Actual spoken words (not bullet points — write what Ray will say)
- `*Italicized stage directions*` for screen content and visuals
- Save to `socials/youtube/videos/<kebab-case-title>.md` with frontmatter:

```yaml
---
tags: [youtube, script, claude-code]
status: draft
date: YYYY-MM-DD
---
```

## Title Generation

Generate 3 title options using different formulas:
1. Bold claim + anthropomorphism/personification
2. Bold claim + specificity
3. Curiosity gap + exclusivity

Present them in a table at the top of the script, like the auto-dream reference does.
