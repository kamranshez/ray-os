---
name: youtube-miner
description: >-
  Mine a YouTube creator's entire back catalogue (or a date-bounded slice) for reusable ideas,
  content angles, and insights, tracing each insight to the original source it came from (blog,
  paper, tweet, changelog) and surfacing what the audience keeps asking for in the comments.
  Built on VidTempla (channel video listing + comment threads) and Supadata (transcripts +
  descriptions). Use this skill WHENEVER the user wants to go through a channel's videos in bulk
  to extract ideas, not just look up one video: "mine Theo's videos", "go through every video on
  this channel", "what video ideas can I pull from <creator>", "analyze <channel> for content
  angles", "what is <creator>'s audience asking for", "find the best insights across <creator>'s
  last year", "scan <competitor>'s channel for gaps", "turn this creator's catalogue into a list
  of ideas". Trigger even when the user names a creator/handle/URL and says "find me ideas" without
  saying "mine" or "skill". Produces a ranked, source-traceable markdown report plus an interactive
  HTML picker the user can click through to select the ideas worth pursuing. Default framing is
  "ideas that could become Agentic Coding School videos", but the goal is parameterizable for any
  channel or purpose. Do NOT use for single-video transcript lookups (just fetch the transcript),
  for competitor TITLE research (use youtube-title-researcher), or for outlier/trend scouting
  across many channels (use youtube-outlier-scout).
---

# YouTube Miner

Turn a creator's body of work into a curated, **selectable** list of ideas. The unit of work is
"a whole channel (or a slice of it)", not "one video". The output is two things:

1. A ranked **markdown report** of the strongest ideas, each traced to its **original source** and
   annotated with how it relates to the user's existing work and what the **audience is asking for**.
2. An interactive **HTML picker** the user clicks through to choose which ideas to act on, then
   pastes their selection back.

This is what turned the Theo → Ptacek → "Carlini Loop" chain into a class video: a Theo video was
*reacting to* an original blog post, and that blog post was the real teachable artifact. The job of
this skill is to find those chains at scale.

## When the heavy engine vs. the light path

- **Big catalogue (roughly 30+ candidate videos, or "go through everything")** → use the bundled
  **Workflow engine** (`assets/mine-workflow.js`). It fans out: discover → triage → mine (transcript
  + description sources + comments) → synthesize. This is token-heavy and runs in the background, so
  it is opt-in: only launch it when the user has asked for breadth (or used "ultracode").
- **Small/targeted (a handful of named videos, or "just the last 5")** → skip the Workflow and do it
  inline: list the videos, then for each one read the transcript + top comments and pull the ideas
  yourself. Same stages, no orchestration.

When unsure which the user wants, ask once: "Mine the whole catalogue (heavy, backgrounded) or just
the recent N?"

## The pipeline (what each stage does and why)

Read `references/vidtempla-and-sources.md` for exact tool calls and channel-id resolution before you
start. The stages:

1. **Discover** — enumerate the creator's videos with VidTempla `list_videos` (it paginates *public,
   unowned* channels straight from the YouTube API, with no per-call search quota cost — far cheaper
   and more complete than `search_youtube`). Bound by a publish-date window if the user gave one.
   Report honestly whether coverage is complete.
2. **Triage** — for a large catalogue, cheaply score each video's relevance to the user's goal from
   its title + description, and only deep-mine the top slice. Always **log what you dropped** — a
   silent cap reads as "covered everything" when it did not.
3. **Mine (per video)** — the heart of it. For each kept video pull three signals:
   - **Transcript** (Supadata) — the actual content and the claims worth teaching.
   - **Description sources** (Supadata metadata) — creators like Theo list their references in a
     "SOURCES" section; this is where the *original* blog/paper/tweet lives. Follow those links.
   - **Top comments** (VidTempla `list_comment_threads`, `order: relevance`) — the audience tells
     you what they didn't understand, what they want explained, what they disagree with, and what
     they're literally requesting. This is demand signal you cannot get from the video alone.
4. **Relate to existing work** (optional) — if the user has a curriculum/back-catalogue MCP (e.g.
   Agentic Coding School), check whether each idea is already covered and frame it as new ground,
   a sequel, or a contrast. Prefer ideas that open new ground.
5. **Synthesize** — rank by a blend of novelty and clean source-traceability. Produce the report
   (see `references/report-format.md`) plus a picker-ready JSON.
6. **Build the picker** — run `scripts/build_picker.py` on the picker JSON to emit the clickable
   HTML. Never hand-write that HTML; the script bundles the styling and the "links don't toggle the
   card" behaviour.

## Running the heavy engine

The engine reads parameters from the Workflow `args` (so the script itself never needs editing).
Compute the values first (especially the `since` date — workflow scripts cannot call `Date.now()`),
then launch:

```
Workflow({
  scriptPath: ".claude/skills/youtube-miner/assets/mine-workflow.js",
  args: {
    channel: "@t3dotgg",                 // handle, channel id, or URL
    since: "2025-06-21T00:00:00Z",        // null = all-time
    today: "2026-06-21",
    goal: "insights that could become Agentic Coding School videos (a course on agentic coding / AI dev tools). Bias toward insights that trace to an original blog/paper/tweet, like a creator reacting to a primary source.",
    mineCap: 80,
    useComments: true,
    curriculumHint: "Use mcp__claude_ai_Agentic_Coding_School__search_videos to check what is already taught and add a 'Relates to' note."   // or null
  }
})
```

It returns `{ report, picker, stats }`. Then:

1. Write `report` to a vault note (kebab-case filename, no H1, frontmatter — see the repo's image/
   note conventions). A good home is `projects/agentic-coding-school/ideas/<slug>/`.
2. Save `picker` to a temp JSON and run the picker builder:
   ```bash
   python3 .claude/skills/youtube-miner/scripts/build_picker.py <picker.json> <out.html>
   ```
3. Open both for the user (`obsidian open path=...` for the note, `open -a "Google Chrome" <out.html>`).

If the run dies or you edit the engine, resume with `Workflow({scriptPath, resumeFromRunId})` — the
unchanged prefix of agents returns cached results.

## Output conventions (match the user's repo)

- **No em dashes or en dashes** in written output — this is a firm style rule for Ray's content. The
  picker builder and the synthesis prompt already strip them; keep it that way if you edit them.
- Notes are kebab-case, date-prefixed (`YYYY-MM-`), no H1 (Obsidian uses the filename), with
  `tags`/`date` frontmatter.
- Always state coverage caveats: how many videos were found, mined, and dropped, and whether ranking
  used view data (the public YouTube search endpoint does not return view counts).

## Reference files

- `references/vidtempla-and-sources.md` — exact VidTempla + Supadata calls, channel-id resolution,
  comment mining, fallbacks when a tool is unavailable.
- `references/report-format.md` — the report template and the picker JSON shape.
- `assets/mine-workflow.js` — the parameterized Workflow engine.
- `scripts/build_picker.py` — generates the interactive HTML picker from a JSON of ideas.
