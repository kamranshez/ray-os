---
name: youtube-ab-tester
description: Generate A/B test title and thumbnail text options for Ray's YouTube videos, and record A/B test results. Use this skill whenever the user wants to brainstorm YouTube titles, generate thumbnail text ideas, record A/B test results, analyze title/thumbnail performance, or asks things like "suggest titles", "what titles should I test", "record these results", "what's working", "title ideas for my next video", "thumbnail text options", or "update the A/B test results". Also trigger when the user shares a screenshot of YouTube A/B test results and wants analysis or recording. Do NOT use for competitor title research (use youtube-title-researcher instead) or video scripting (use youtube-scriptwriter instead).
---

## What This Skill Does

You generate data-driven YouTube title and thumbnail text options for A/B testing, and record/analyze test results. Every suggestion is grounded in 16 videos worth of A/B test data with clear winning and losing patterns.

Before generating any titles or thumbnail text, read `references/ab-test-results.md` in this skill's directory. It contains all historical A/B test data, winning formulas, anti-patterns, and key learnings. This is your ground truth — never suggest something that contradicts the proven data.

## Generating Title Options

When the user asks for title ideas, provide 8-10 options organized by framing category. For each title, briefly note which proven pattern it uses or what untested hypothesis it explores.

### The Proven Formula Hierarchy

These are ranked by reliability based on actual test data. Lean heavily toward the top of this list:

1. **"Anthropic Just Dropped Their Internal [X] Strategy"** — insider framing, 49.4% all-time best (V15)
2. **"Anthropic Just Dropped the Feature Nobody Knew They Needed"** — negative social proof curiosity, 46.8% (V14)
3. **"The Top 0.01% User's Guide to [Tool]"** — statistical authority + resource framing, 44.6% (V11)
4. **"Anthropic Just Dropped the Feature Everyone Asked For"** — positive social proof curiosity, 42.3% (V10)
5. **"Anthropic Just Dropped [number] New [Tool] Features"** — specificity with count, ~37% (V9)
6. **"Anthropic Just Added [specific feature] to Claude Code"** — reliable workhorse, ~35-42% (V2, V6, V7)
7. **"[Tool]'s Biggest Update in [timeframe]"** — magnitude framing, ~37% (V5)

### Verb Hierarchy

When using the "Anthropic Just [verb]" formula:

- **"Dropped"** (strongest) — casual hype, consistently wins
- **"Added"** — reliable but weaker than Dropped
- **"Revealed"** — decent for insider/secret content
- **"Connected" / "Made"** — adequate but unremarkable
- **"Fixed"** — weak, no curiosity
- **"Completed"** — weak, passive

### Title Rules

Apply these rules to every title you generate:

1. **Include "Anthropic" authority framing** — titles without it consistently underperform (V10: 25.4% without vs 40.9% with). The only exception is statistical authority framing ("Top 0.01% User")
2. **Keep it short and clean** — one clear hook, not multiple
3. **Never list multiple features in the title** — kills performance every time (V5: 26%)
4. **Never use parentheticals** — proven negative signal (V1, V11 launch failure)
5. **Never use "Explained"** — educational framing consistently underperforms (~30%)
6. **Never use "How" prefix** — educational framing in disguise (V12: 29.3%, V15: 29.9%)
7. **Never use "Stop [doing X]"** — accusatory framing is the worst performer category (20-29%)
8. **Never use pipe format** — "| Here's What Changed" feels clickbaity (V9: 31.4%)
9. **Catchy terminology beats technical** — "Swarms" > "Multi-Agent Teams", "Dropped" > "Added"
10. **Specific tool names beat generic** — "Claude Code" > "AI Coding"
11. **Social proof curiosity is content-dependent** — works for mysterious/exciting features, fails for known/niche improvements like "skills update"
12. **"Internal" insider framing is content-dependent** — works when the content genuinely involves behind-the-scenes strategy
13. **Third-person social proof > second-person** — "Nobody" > "You" (V14: 40.8% vs 34.6%)
14. **"The" > "A" for definitive articles** — implies *the only* guide, not one of many (V11: 44.6% vs 26.1%)

### Ensure Frame Diversity

When generating options, include at least 3 genuinely different framing categories. If all options share the same frame, the A/B test can't find a winner (V11 launch failure — all 3 titles used reflective framing and all failed).

Good diversity example:
- Social proof curiosity: "...the Feature Nobody Knew They Needed"
- Cost contrast: "...a $5,000 Feature for $200"
- Competitive: "...the OpenClaw Killer"

Bad diversity example:
- "What 1,600 Hours Taught Me"
- "How I Use Claude Code After 1,600 Hours"
- "What 1,600 Hours Looks Like" ← all reflective, same frame

## Generating Thumbnail Text Options

When suggesting thumbnail text, follow these proven patterns:

### The Proven Hierarchy

1. **"How I [Verb] Now"** — dominant winner at 51.5% (V4), but only works for workflow/opinion videos, NOT news/announcement videos
2. **"[Feature] Changed"** — short, good at ~35% (V6)
3. **Version labels with question mark** — "Skills 2.0?" at 44.4% (V12), works when aligned with title
4. **Cost/percentage claims** — "It's 96% Cheaper!" at 38.3% (V13)

### Thumbnail Text Rules

1. **Shorter is better** — 2-3 words ideal
2. **Present tense "Now" beats year labels** — "How I Code Now" (51.5%) vs "My 2026 Workflow" (27.1%)
3. **Personal framing beats feature framing** — "How I..." > "How [Feature]..."
4. **Match the title's energy** — news title + personal thumbnail = mismatch (V12: "How I Make Them Now" flopped at 26.8% paired with news title)
5. **Never use vague time references** — "1 Year Later...", "A Lot Has Changed" = death (21.5%)
6. **Simple percentages > dollar comparisons** — less cognitive load at glance (V13: 38.3% vs 33.3%)

## Recording A/B Test Results

When the user shares A/B test screenshots or results:

1. Record them in `/Users/ray/Desktop/ray-os/socials/youtube/ab-tests/results.md` under the correct video section
2. Use the established format with markdown tables
3. Include timestamp in the round header: `### Title A/B Test Round N (YYYY-MM-DD)`
4. Write "Key takeaways" that reference specific data points from previous videos
5. End with a clear recommendation for the next round
6. Also update the reference copy in this skill's references/ directory to stay in sync

### Diagnosing Bottlenecks

When results are flat across title variants:
- If all titles share the same frame → the frame is the problem, test different frames
- If titles use diverse frames but all score the same (~0-2% spread) → the thumbnail is likely the ceiling, switch to thumbnail testing
- If a proven winner formula (e.g., "Nobody Knew They Needed" at 46.8%) suddenly scores ~33% → something external is capping it (thumbnail mismatch, audience fatigue, topic ceiling)

### When to Recommend What

- **Title testing first** — almost always start here. Titles have wider performance range (20-49%) than thumbnails
- **Switch to thumbnail testing** when 3+ diverse title frames produce identical results
- **Consider topic ceiling** when both title and thumbnail optimization plateau — some topics (niche power-user content) have hard ceilings regardless of packaging

## Anti-Patterns Quick Reference

Never suggest these. If you catch yourself writing one, delete it:

| Pattern | Why It Fails |
|---------|-------------|
| Parentheticals in titles | Visual clutter, afterthought feel |
| "Explained" / "Taught Me" / "Looks Like" | No urgency or curiosity |
| Personal framing without authority | "I/My" alone = no reason to click |
| "You Missed" / "You're Missing Out" | Accusatory, turns viewers off |
| Multiple features listed in title | Too much info, no single hook |
| Pipe format ("Here's What Changed") | Feels clickbaity |
| All-similar A/B test variants | Can't find a winner if all options share a frame |
| "Stop [doing X]" | Worst performer category (20-29%) |
| "Should Have" retrospective framing | Complaint without authority |
| Vague thumbnail time references | No value promise |
