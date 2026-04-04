---
name: x-article
description: >
  Write a long-form X/Twitter article from a YouTube video, transcript, topic, or
  agentic coding school content. Fetches the transcript, distills core ideas, and
  writes a platform-native article optimized for X's long-form format. Can combine
  multiple sources — school videos, external X posts, research — into a single
  cohesive article. Use this skill whenever the user wants to write an X article,
  turn a video into an X post, or says things like "write an X article",
  "X article from this video", "long-form X post", "write this up for X/Twitter".
  Also triggers on "article for X" or "post this on X" when long-form content is implied.
  Triggers on "combine insights" or "daily article from school" for scheduled runs.
---

# X Article Writer

You write long-form X articles from YouTube videos, topics, or combined sources.
The article should stand on its own — someone should read it, get value, and share
it even if they never watch a video. But it should also leave them wanting the
full depth that the source material provides.

## Step 1: Get the Source Material

**Mode A — YouTube video:**
If given a YouTube URL, use the `supadata` skill to fetch the transcript.
If given a video name, check `socials/youtube/videos/` first.

**Mode B — Agentic Coding School content:**
If given a topic or asked to write from school content:
1. Use `mcp__agentic-coding-school__search_videos` to find relevant completed videos
2. Use `mcp__agentic-coding-school__get_video` to fetch full transcript + agentContext
   for the top 1-3 most relevant videos
3. Combine insights from multiple videos into a single narrative — don't just
   summarize one video, synthesize across sources

**Mode C — Combined insights (the power mode):**
When combining school content with external sources (X posts, articles, research):
1. Pull school content via Mode B
2. If external URLs or pasted content provided, extract key claims and data points
3. Cross-reference: where does the school content confirm, contradict, or extend
   the external insights?
4. The article should feel like YOUR synthesis — not a summary of sources

**Mode D — Topic only:**
If given a topic directly (no video, no school search), work from that.

## Step 2: Extract Core Ideas

From the source material, identify:
- **The thesis** — the single main argument or insight (1 sentence)
- **3-5 key points** — the supporting ideas
- **The money shot** — the single most surprising/valuable moment
- **Quotable lines** — things Ray said or specific claims that work standalone
- **Cross-source tension** (combined mode only) — where sources disagree or
  complement each other. This creates the most interesting articles.

Target: 800-1,200 words. Cut 60-75% of the source content.
Keep what's new, specific, and actionable. Drop what's contextual or introductory.

When combining school content with external insights, the school content is YOUR
expertise — the external posts are the conversation you're joining. Frame it as
"here's what people are saying, and here's what I've found from actually teaching
this stuff."

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
**Source**: [YouTube URL / school video titles / "original"]
**Word count**: [count]
```

When sourced from school content, the CTA should point to agenticcoding.school
with the specific video or class URL. Example:
"The full walkthrough with live demos is at agenticcoding.school"

## Step 6: Save

Save to: `socials/x/articles/[slug]-YYYY-MM-DD.md`

```yaml
---
tags: [x-article, distribution]
date: YYYY-MM-DD
source: [YouTube URL, school video URLs, or "original"]
school-topic: [topic if from school content]
---
```

## Step 7: Deliver (scheduled runs only)

When running as a scheduled task, after saving the article:
1. Send the full article to Ray via Telegram using `mcp__plugin_telegram_telegram__reply`
2. Include the headline, article text, and source links
3. Ask "Post this? Edit first? Skip?" so Ray can approve before publishing

## References

See [references/example-articles.md] for 3 real X articles that got 69K-1M+ views.
Study their structure, pacing, and specificity before writing.

## Notes

- For Claude Code / AI dev topics, lean into technical specifics. Developers on X appreciate precision.
- The opening paragraph is everything. If the first two lines don't hook, they scroll past.
- This is a teaser — give 70% of the insight, make it clear the video has the rest.
- X articles get more engagement when they teach something concrete. "Here's exactly how" > "Thoughts on."
- When using school content, pick topics with the most specific/actionable agentContext.
  Generic "how to install" topics make boring articles. Pick hooks, skills, worktrees,
  sub-agents, debugging patterns — things with strong opinions and real workflows.
- Rotate topics: check `socials/x/articles/` for recent articles and avoid repeating
  the same school topic within 7 days.
