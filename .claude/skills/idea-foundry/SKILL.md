---
name: idea-foundry
description: >-
  Mine 60 to 150 fresh ideas on any topic, concept, project, video, class, or
  research question by fanning out ~20 parallel agents across web search
  (Exa), X discourse (via the x-search skill), and 8 pure-reasoning angles
  (economics, analogies, failure modes, cross-domain, dark side, first
  principles, anti-patterns, provocations). Synthesizes the raw pool, dedups,
  ranks by novelty, and renders to a self-contained dark-theme HTML idea
  bank with selectable cards, a floating "Copy selected (N)" button, filter
  chips, search, and keyboard shortcuts. Use this skill whenever the user
  wants to brainstorm widely before narrowing, mine angles on a topic,
  explore the design space, generate ideas, build an idea bank, research a
  concept from many sides, stage ideas to curate later, prep for a video
  series, prep for a class, or kick off a new project with a rich raw
  material pool. Trigger on phrases like "mine ideas for X", "brainstorm Y",
  "idea bank for", "generate ideas about", "what could I do/say/build/write
  about X", "give me angles on", "explore the design space for", "20 ways to
  think about Z", "ideate on", "spitball for me", "stage ideas on", or any
  time the user signals they want more ideas than a single agent could
  produce in one shot. Use it proactively at the start of any new project,
  class, video series, product launch, essay, or creative effort where a
  wide first-pass brainstorm beats a narrow first draft. Distinguished from
  `idea-triage` (which RANKS existing ideas) and `extract-wisdom` (which
  PULLS ideas out of a fixed source). This skill GENERATES ideas from many
  angles at once. Costs about 1.5M output tokens and 25 minutes; always
  warn the user up front and confirm before launching.
---

# Idea Foundry

Heavy multi-angle brainstorm. Twenty parallel agents hit a topic from three source types, then one synthesis agent dedups + ranks + polishes, then one render agent writes a curated HTML idea bank Ray can browse, filter, select from, and paste back.

The engine is the `idea-foundry` workflow at `~/.claude/workflows/idea-foundry.js`. This skill is the front door: it gathers the arguments, warns about cost, and invokes the workflow.

## When NOT to use

- Single-source brainstorm (the user only wants ideas from one specific document, transcript, or person). Use a regular conversation or [[extract-wisdom]] instead.
- The user wants to RANK or pick from an existing list. Use [[idea-triage]].
- Quick one-shot ideation (under 30 ideas, under 5 minutes). The cost overhead is not worth it. Just brainstorm inline.
- Sensitive or private topic where running searches on Exa and X would leak signal. Confirm first.

## Step 1: Warn about cost and confirm

Before doing anything else, tell the user:

> This will spawn about 22 agents in parallel, costing roughly 1.5M output tokens and running for around 25 minutes. The output is a curated HTML idea bank with 60 to 150 ranked ideas you can filter and select from. Want me to launch it?

Wait for confirmation. If the user wants a cheaper variant, offer:
- "lite" (drop the 4 x-search agents and the 8 reasoning agents, run only the 8 Exa angles; ~10 min, ~600k tokens)
- "no web" (drop the 8 Exa angles; useful when the topic is private or when fresh web signal does not matter)

Pass these by overriding `xQueries: []` or `extraExaAngles: []` etc. in the workflow args, or by editing the workflow inline.

## Step 2: Gather the args

Ask only the questions you cannot answer from the conversation context. Required:

- **topic** (string) — the headline topic. Short enough to drop into Exa and X queries. Examples: "agentic loops and AI orchestration", "thumbnail design for AI YouTube creators", "personal CRM tools 2026".
- **slug** (string) — short kebab-case identifier used in output filename. Default: derive from topic. Example: "agentic-loops", "thumbnail-design".
- **purpose** (string) — one sentence on why the user wants these ideas. Shapes the synthesis voice and ranking. Example: "Ray is planning a 6-video YouTube series on this", "Ray is deciding whether to build a SaaS in this space".
- **alreadyCovered** (string) — bullet list of concepts the user has already covered or wants explicitly excluded. Critical for avoiding obvious-to-them ideas. If unsure, ask: "what should I avoid regenerating?" If the user is mining for a class or project that has existing files, OFFER to read those files yourself and build the exclusion list. For class projects in `projects/agentic-coding-school/to-film/`, scan the .md files and bullet their existing themes.
- **recentDate** (YYYY-MM-DD) — used as the `--since` cutoff for x-search. Default: 14 days before today. Compute from `currentDate` in the user's CLAUDE.md / memory if available, otherwise ask.
- **outputPath** (string) — defaults to `/tmp/<slug>-ideas.html`. Offer to write directly into a project folder if one is obvious (e.g. the class folder's `_inbox/`).

Optional (skip if no signal):

- **xQueries** (array of `{key, query, desc}`) — if the user knows specific X handles or queries that would surface domain experts, accept them. Otherwise the workflow uses two generic ones (topic phrase + thought-leader handles). Override is high-leverage when the topic has known commentators.
- **extraExaAngles** (array of `{key, prompt}`) — appended to the 8 built-in Exa angles when the user has a specific source type in mind.
- **extraReasoningAngles** (array of `{key, prompt}`) — appended to the 8 built-in reasoning angles.
- **voiceNote** (string) — overrides the synthesis voice. Defaults to "Direct, plain, no fluff, no Oxford fancy words. Ray talks like a smart practitioner explaining to a peer, not a TED speaker." Change for non-Ray contexts.

## Step 3: Launch the workflow

```
Workflow({
  name: 'idea-foundry',
  args: {
    topic: '<topic>',
    slug: '<slug>',
    purpose: '<one sentence>',
    alreadyCovered: '<bullet list as string>',
    recentDate: '<YYYY-MM-DD>',
    outputPath: '<absolute path>',
    xQueries: [...],          // optional
    extraExaAngles: [...],    // optional
    extraReasoningAngles: [...], // optional
    voiceNote: '<...>'        // optional
  }
})
```

The workflow is a background task. You will be notified when it completes. Do not poll. The result returns `{count, path, slug, topic}`.

## Step 4: After the run

The render agent writes the HTML inside the workflow, so it is already on disk when the notification arrives.

1. **Verify** the file exists and has zero em or en dashes:
   ```bash
   wc -c <outputPath>
   python3 -c "import sys; s=open('<outputPath>',encoding='utf-8').read(); print('em:', s.count('—'), 'en:', s.count('–'))"
   ```
2. **Open** in browser: `open <outputPath>`.
3. **Offer to move** to a project folder if the file was written to `/tmp/`. For class projects, the natural destination is the class's `_inbox/` directory.
4. **Summarize**: report the count, file size, runtime, and where it ended up. Two sentences.

## Step 5: When the user pastes back

After the user clicks through, selects cards, and clicks "Copy selected (N)", they will paste a markdown blob with H2 titles, explanations, and metadata footers. Treat that blob as their curated short list. Common follow-ups:

- "now write scripts for these" → invoke [[class-script-writer]] per idea or batch.
- "now pick the best 5" → respond directly, no skill needed.
- "expand idea #3" → respond directly with a longer treatment.

## Reference: built-in angles

**Exa (8):** thought-leaders, research, postmortems, comparisons, hn-reddit, podcasts, case-studies, critical-takes.

**X-search (2 default):** topic phrase, thought-leader handles. Override via `xQueries` for sharper targeting.

**Reasoning (8):** economics, analogies, failure-modes, cross-domain, dark-side, first-principles, anti-patterns, provocations.

Total default: 18 agents in phase 1 + 1 synthesis + 1 render = 20 agents. Add custom angles via `extraExaAngles` / `extraReasoningAngles`.

## Reference: HTML output spec

The render agent produces a self-contained file with:

- Dark theme: bg `#0a0a0a`, text `#e8e8e8`, accent amber `#f59e0b`
- Sticky filter bar: category chips, level chips, novelty chips, search input
- Stats line: "X/Y ideas, Z selected"
- Responsive grid (1/2/3 col)
- Click card to toggle selection (amber border + filled check)
- Fixed top-right "Copy selected (N)" button, amber when N>0
- Cmd+Shift+C copies, Esc clears
- "Clear selection" link inline with count
- Zero external CDN/fonts/JS
- Zero em or en dashes anywhere

The user has loved this UX across two runs already (loopy-ai-ideas v1 and v2). Do not redesign it on each invocation; if the user wants visual changes, edit the render prompt in the workflow script directly.

## Cost and runtime, calibrated

Based on the two real runs so far:

| Run | Angles | Agents | Tokens | Wall clock | Ideas out |
|---|---|---|---|---|---|
| loopy-ai v1 | 10 | 12 | ~800k | 18 min | 48 |
| loopy-ai v2 | 20 | 22 | 1.56M | 25 min | 191 |

So per-agent cost is roughly stable at ~70k output tokens and ~75 seconds. Use this to estimate variants:

- 10-agent lite run: ~700k tokens, ~15 min
- 30-agent heavy run: ~2.1M tokens, ~35 min

If the user has a budget directive (`+500k`, `+1M`), scale the angle count to fit.
