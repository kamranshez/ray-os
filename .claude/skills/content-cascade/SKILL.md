---
name: content-cascade
description: >
  Orchestrator skill — takes a YouTube video and cascades it across platforms by
  calling other skills. Currently calls: x-article (for X long-form) and linkedin
  (for LinkedIn posts). Use this skill whenever the user wants to repurpose a video
  across multiple platforms at once, or says things like "cascade this video",
  "distribute this everywhere", "repurpose this", "content cascade", or "post this
  on X and LinkedIn". If the user only wants one platform, use that platform's skill
  directly instead.
---

# Content Cascade

You are an orchestrator. You take one YouTube video and cascade it across
multiple platforms by calling the appropriate skill for each platform.

## How It Works

### Step 1: Get the Video

Accept a YouTube URL or video name. If given a name, find the file in
`socials/youtube/videos/`.

Fetch the transcript once using the `supadata` skill — don't make each
downstream skill re-fetch it.

### Step 2: Extract Core Ideas (shared across all platforms)

From the transcript, distill:
- **The thesis** — single main argument (1 sentence)
- **3-5 key points** — supporting ideas
- **The money shot** — most surprising/valuable moment
- **Quotable lines** — standalone statements

This extraction is shared context — pass it to each skill so they don't
duplicate the analysis work.

### Step 3: Call Each Platform Skill

Run these in parallel where possible:

1. **X Article** — Invoke the `x-article` skill with the transcript and extracted ideas
2. **LinkedIn Post** — Invoke the `linkedin` skill (write post mode) with the same context

Pass each skill:
- The full transcript
- The extracted core ideas from Step 2
- The YouTube URL for CTA links

### Step 4: Collect and Present

Once all platform outputs are ready, present them together:

```
## Content Cascade: [Video Title]
Source: [YouTube URL]

---

### X Article
[output from x-article skill]

---

### LinkedIn Post
[output from linkedin skill]

---
```

### Step 5: Save

Save the combined output to: `socials/youtube/videos/[video-slug]-cascade.md`

```yaml
---
tags: [content-cascade, distribution]
date: YYYY-MM-DD
source-video: [YouTube URL]
platforms: [x-article, linkedin]
---
```

## Adding New Platforms

This skill is designed to be extensible. To add a new platform:
1. Create a standalone skill for that platform (like `x-article`)
2. Add it as a step in Step 3 above

Current platform skills:
- `x-article` — Long-form X/Twitter articles
- `linkedin` — LinkedIn posts (existing skill, generates 10 variations)

## Notes

- Always fetch the transcript once and share it. Don't make each skill re-fetch.
- Each platform's output should feel native to that platform. The cascade orchestrates — it doesn't homogenize.
- If the user only wants one platform, tell them to use that skill directly. The cascade is for "give me everything at once."
- The linkedin skill generates 10 variations. Let it do its thing — don't override its format.
