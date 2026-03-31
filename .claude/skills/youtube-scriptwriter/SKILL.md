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

**Use discovery framing, not announcement framing.** The top 3 all start from Ray's personal experience discovering or using the feature:
- Auto-dream (94k): "I was just doing some vibe coding and I noticed Claude Code did something really weird"
- btw/fork (39k): "Claude just dropped a feature I didn't even realize I wanted"

The mid-tier videos (25-35k) start with the announcement: "A few hours ago, Anthropic released..." / "I woke up and checked the updates." Discovery framing ("I stumbled onto this") makes viewers lean in. Announcement framing ("here's the news") makes them evaluate whether to stay.

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

### 8. Single CTA at End (last 30s)

One call to action, naturally connected to the topic. No mid-roll CTAs. The auto-dream script tied its CTA to "learn more about memory and context management in the masterclass."

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

## Pacing Guidelines (from improvements.md)

- Speak ~50% slower than typical AI tutorial pace
- Let visuals linger 2-3 seconds after referencing them
- Keep natural pauses — don't script out every breath
- Add clear section titles/breaks between segments
- Use progressive reveal over static slides where possible

## What NOT to Do

- **No feature roundups.** Focused single-feature videos average 25% more views. If the announcement has 5 features, pick the most interesting one.
- **No abstract intros.** Don't open with "In today's video we're going to..." — open with the hook.
- **No stacked CTAs.** One at the end. That's it.
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
