---
name: hook-writer
description: >
  Generate 5 video hook variations using the data-backed 3-beat formula, each with
  spoken script, visual direction, and text overlay. Use this skill whenever the user
  wants hooks for a video — "write hooks for X", "hook me", "write the opening",
  "give me hook options", "3-beat hook for X", "what should I say in the first 30
  seconds", or "write the intro". Also triggers when the user is about to film and
  needs the opening nailed down, or says "I need a hook" in any context.
---

# Hook Writer

You write the most important 20-30 seconds of Ray's videos. A great hook is the
difference between someone watching for 10 minutes and someone clicking away.
Everything here is grounded in data from Ray's outlier research — not generic
YouTube advice.

## Before You Start

Read these files:

1. **`socials/youtube/research/2026-02/master-research.md`** — Specifically the 3-Beat Hook Formula section and the outlier patterns
2. **`socials/youtube/improvements.md`** — Check current hook-related experiments
3. **`socials/youtube/performance/2026-02.md`** — Performance gaps, especially the "visual hook in first 10s" gap (0% of Ray's videos have this vs 100% of outliers)

Also check if there's an ideation file for this topic in `socials/youtube/research/ideation-*.md` — if so, use its angle and desire mapping.

## The 3-Beat Hook Formula

This comes from analyzing every outlier video (18.8x, 8.7x, 5.1x views/sub ratio).
100% of outliers use this pattern. 0% of Ray's current videos do. It's the single
highest-leverage improvement available.

### Beat 1: Empathy / Relatability
Connect with a frustration, aspiration, or experience the viewer already has.
Makes them think "this person gets it."

**Examples from outliers:**
- "If Claude has ever felt dumb to you..."
- "I used to mass-highlight and copy code into ChatGPT..."
- "Most people use Claude Code like a fancy autocomplete..."

**What NOT to do:**
- "This is HUGE!" / "This is INSANE!" (hype openers underperform — 0.05x views/sub)
- "Hey guys, welcome back to my channel" (dead air)
- "So today we're going to talk about..." (no emotional hook)

### Beat 2: Provocative Claim
A bold, specific statement that creates a knowledge gap. The viewer needs to keep
watching to understand how this claim could be true.

**Examples from outliers:**
- "I'm not writing code anymore"
- "6 months of lessons compressed into 27 minutes"
- "One feature that changed everything about how I work"

**The key**: specificity beats hyperbole. "50 tips" is more compelling than "INSANE tips"
because it's concrete and promises density.

### Beat 3: Clear Scope
Tell the viewer exactly what they'll get. This is the commitment device — it
converts curiosity into a decision to watch.

**Examples from outliers:**
- "50 tips from 6 months of daily use"
- "The 6 core features most people miss"
- "From zero to deployed app in one session"

## The Visual Hook (First 10 Seconds)

Separate from the spoken hook. While Beat 1 is being spoken, the screen should
show the RESULT — the finished thing, the impressive output, the "wow" moment.

100% of outlier videos do this. 0% of Ray's current videos do.

**Pattern**: Show the end result first, THEN explain how to get there.
- Terminal showing a complex multi-file diff being applied
- A deployed app running smoothly
- A side-by-side before/after
- Revenue dashboard, analytics, something with numbers

The visual hook answers: "Why should I care?" before the viewer even processes the words.

## Generating Hooks

For each video topic, produce **5 hook variations**. Each variation should take a
genuinely different approach — not just rewording the same hook.

### Hook Format

```markdown
## Hook [N]: [Strategy name — e.g., "The Confession", "The Impossible Claim", "The Data Drop"]

### Spoken (15-25 seconds)
> [Beat 1 — Empathy/Relatability]
> [Beat 2 — Provocative Claim]
> [Beat 3 — Clear Scope]

### Visual Direction
[What's on screen during the spoken hook. Be specific — "terminal showing X" not "relevant visuals"]

### Text Overlay (optional, mainly for short form)
[If this were a short/reel, what text appears on screen in the first 3 seconds?]

### Why This Works
[1-2 sentences connecting this hook to specific outlier patterns or performance data]
```

### The 5 Variation Strategies

Aim for a mix from these approaches:

1. **The Confession** — Start with what you used to do wrong. "I used to [common mistake]... then I discovered [thing]"
2. **The Impossible Claim** — Make a bold specific claim that sounds too good. "I built [impressive thing] in [short time] with [tool]"
3. **The Data Drop** — Lead with a surprising number. "[Specific stat] — and here's exactly how"
4. **The Empathy Play** — Name the pain the viewer is feeling. "If you've ever [common frustration]..."
5. **The Reframe** — Challenge a common assumption. "Everyone thinks [common belief], but [contrarian truth]"
6. **The Tease** — Show the result, withhold the method. "This [impressive output] took me [short time]. The trick is [vague hint]..."
7. **The Authority Stack** — Lead with credentials/proof. "[Time period] of doing [thing] taught me [number] lessons"

Pick 5 that are most appropriate for the specific topic. Don't force strategies that
don't fit.

## Quality Checks

Before presenting hooks, verify each one:

- [ ] All three beats are present and distinct
- [ ] Beat 2 is specific, not hyperbolic (numbers > adjectives)
- [ ] Visual direction is concrete and shows a result
- [ ] The hook could stand alone as a short-form opening
- [ ] It sounds like Ray talking, not a generic YouTuber (casual, direct, slightly self-deprecating)
- [ ] No "Hey guys" / "Welcome back" / "In this video" / "So today"
- [ ] No hype words: INSANE, HUGE, CRAZY, GAME-CHANGER, MIND-BLOWING

## Save Output

Save to the video's file in `socials/youtube/videos/[video-slug].md` under a `## Hooks` section.

If the video file doesn't exist yet, create it with frontmatter:
```yaml
---
tags: [video, hooks]
date: YYYY-MM-DD
status: hooks-written
---
```

## Voice Notes

Ray's speaking style is:
- Casual and direct — talks like he's explaining to a friend
- Uses "right?" as a verbal punctuation
- Occasionally self-deprecating ("not to toot my own horn but...")
- Avoids corporate/formal language
- Says "like" and "so" naturally — hooks should sound spoken, not written
- Gets to the point fast — no warming up

The hooks should read like something Ray would actually say out loud, not something
that sounds good on paper but awkward when spoken.
