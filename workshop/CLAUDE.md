# Workshop

A 7-day live workshop being built by combining material across the Agentic Coding School catalogue (147-video Master Claude Code class, Codex, Techniques, Context Engineering, Prompt Engineering, Workflows). The workshop is the *distilled* version — the canonical path through the material, not a re-recording of every video.

## What a "stub" is (read this before touching content/)

Every file in `content/` is one of three things. The YAML frontmatter at the top of each file says which:

```yaml
---
status: stub
acs:
  - class: claude-code
    title: Spec Developer
  - class: claude-code
    title: Checking After Spec Developer
mapping: mapped         # mapped | mapped-partial | workshop-original
day: 1
block: core             # core | practice | deep-cut | n/a
---
```

Meanings:

- **`mapping: mapped`** — the stub is a *pointer* to one or more existing ACS videos. The body of the file should be short: enough framing to remind you what the topic is and which day it lives on, then a list of the ACS videos. **Don't expand these stubs into full notes** — the videos do the teaching. When fleshing out, you re-watch the named ACS videos and write the *workshop framing* (transitions, intro, post-watch discussion prompts), not a duplicate of what the video already says.
- **`mapping: mapped-partial`** — an ACS video covers part of the topic, but the workshop angle is bigger (more context, more recent thinking, a stronger frame). The body should capture *what the workshop adds past the video*. When fleshing out, expand the body with new framing; the video is supporting material.
- **`mapping: workshop-original`** — there is no matching ACS video. `acs: []` and `recording-needed: true`. These stubs *will* expand into full notes that drive a net-new recording. Day 7's archetype series, [[Status of Agents]], the long-context trio synthesis, etc.

The `acs:` field is a list of `(class, title)` pairs — these are the IDs the MCP uses (`mcp__claude_ai_Agentic_Coding_School__get_video` takes `classSlug` + `videoTitle`). To re-watch a video while fleshing out a stub: feed those pairs into `get_video` and the transcript comes back.

`day:` and `block:` are denormalised from `Class Structure.md` so each stub stands alone. If you move a topic between days, update both.