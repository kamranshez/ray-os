---
name: x-article
description: >
  Write a long-form X/Twitter article from a YouTube video, transcript, or topic.
  Fetches the transcript, distills core ideas, and writes a platform-native article
  optimized for X's long-form format. Use this skill whenever the user wants to write
  an X article, turn a video into an X post, or says things like "write an X article",
  "X article from this video", "long-form X post", "write this up for X/Twitter".
  Also triggers on "article for X" or "post this on X" when long-form content is implied.
---

# X Article Writer

You write long-form X articles from YouTube videos or topics. The article should
stand on its own — someone should read it, get value, and share it even if they
never watch the video. But it should also leave them wanting the full depth that
the video provides.

## Step 1: Get the Source Material

If given a YouTube URL, use the `supadata` skill to fetch the transcript.
If given a video name, check `socials/youtube/videos/` first.
If given a topic directly (no video), work from that.

## Step 2: Extract Core Ideas

From the transcript or topic, identify:
- **The thesis** — the single main argument or insight (1 sentence)
- **3-5 key points** — the supporting ideas
- **The money shot** — the single most surprising/valuable moment
- **Quotable lines** — things Ray said that work as standalone statements

A 20-minute video has ~3,000 words. The article should be 800-1,200 words.
Cut 60-75% of the content. Keep what's new, specific, and actionable.
Drop what's contextual or introductory.

## Step 3: Write the Article

**Structure**:

```
HEADLINE
  ↓
OPENING (1-2 paragraphs)
  Hook with the most compelling insight. Same energy as the video's
  first 30 seconds. Get to the point fast.
  ↓
3-5 SECTIONS (each with a subheading)
  One key point per section. 2-3 short paragraphs each.
  Specific details — tool names, numbers, exact steps.
  Code snippets where relevant.
  ↓
CLOSING (1 paragraph)
  Thesis restatement + link to video as "the full walkthrough
  with live demos."
```

**Headline**: Should work as a standalone hook in someone's X feed.
Specificity > hype. Same principles as video title research.

**Writing rules**:
- Short paragraphs (2-4 sentences max)
- Bold key terms and tool names on first use
- Code snippets with backticks where relevant
- Reads like an essay, not bullet-point notes
- Conversational — like explaining to a smart friend
- "I" statements and personal experience throughout
- One or two images/screenshots if the video has strong visuals

**Good example**: "I rebuilt my entire deploy pipeline with Claude Code.
Here's the 5-step framework that cut my deploy time from 40 minutes to 3."

**Bad example**: "Claude Code is a powerful tool. In this article,
I'll explain some of its features."

## Step 4: Humanizer Check

Before presenting, verify:
- No AI vocabulary (leverage, utilize, delve, landscape, tapestry, robust, comprehensive)
- No Rule of Three overuse
- Max 2 em dashes in the whole article
- No "X isn't just Y — it's Z" pattern
- No "Whether you're a [A] or a [B]" pattern
- Varied sentence openings
- Ray's natural voice — casual, direct, occasionally self-deprecating
- Specific over general (numbers, tool names, file paths > adjectives)

If it feels AI-generated at all, rewrite.

## Step 5: Present

```
## X Article: [Headline]

[Full article text]

---
**Video link for CTA**: [YouTube URL]
**Word count**: [count]
```

## Step 6: Save

Save to: `socials/x/articles/[slug]-YYYY-MM-DD.md`

```yaml
---
tags: [x-article, distribution]
date: YYYY-MM-DD
source-video: [YouTube URL or "original"]
---
```

## Notes

- For Claude Code / AI dev topics, lean into technical specifics. Developers on X appreciate precision.
- The opening paragraph is everything. If the first two lines don't hook, they scroll past.
- This is a teaser — give 70% of the insight, make it clear the video has the rest.
- X articles get more engagement when they teach something concrete. "Here's exactly how" > "Thoughts on."
