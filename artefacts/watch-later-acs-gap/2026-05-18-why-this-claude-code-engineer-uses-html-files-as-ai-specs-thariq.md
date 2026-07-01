---
title: "Why this Claude Code engineer uses HTML files as AI specs | Thariq Shihipar (Anthropic)"
video_url: https://www.youtube.com/watch?v=Qrpm7E80wQ0
video_id: Qrpm7E80wQ0
channel: How I AI
published: 2026-05-18
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Why this Claude Code engineer uses HTML files as AI specs | Thariq Shihipar (Anthropic)**](https://www.youtube.com/watch?v=Qrpm7E80wQ0) - How I AI - uploaded 2026-05-18

> Two next-step ACS videos available: authoring plans/specs in HTML, and a portable design-system.html that travels with the repo.

## The one idea worth a video

- **Spine 1 (headline): HTML is the new markdown for plans and specs.** Because agents now emit thousand-line plans nobody reads, moving the plan into a rendered HTML medium is what pulls the human back into the loop, and staying in the loop is what determines output quality. It subsumes brainstorm-in-HTML, plan-in-HTML, weekly-updates-in-HTML, and the compute-allocator "why." VERDICT: 🔗 next-step video available.
- **Spine 2: build throwaway micro-UIs to edit one module of your plan.** When a section is awkward to edit in the terminal, have Claude build a disposable custom app for exactly that module and paste the structured output back. VERDICT: ✅ covered (deep-dived for context, no pitch).
- **Spine 3: a living design system as one portable HTML file that travels with the repo.** Encode colors, typography, spacing, radius, and components in a single design-system.html Claude references in every new project, doubling as a marketer-ready component gallery. VERDICT: 🔗 next-step video available.

## Summary + counts

Anthropic Claude Code engineer Thariq Shihipar tells Claire Vo why he replaced markdown with HTML for plans, specs, brainstorms, and design systems traveling with code.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 — HTML is the new markdown for plans and specs

The claim: author plans, PRDs, and specs in HTML rather than markdown, because a richer visual medium pulls you back into reading and editing, and being in the loop is what raises quality. Why it is non-obvious: most people assume plan format is cosmetic and that a capable model reads markdown fine, so why bother. Thariq flips the audience, the format is not for the model, it is for you. The mechanism runs in two steps. Because agents now run for an hour and emit thousand-line plans, people stop reading them ("I honestly have stopped reading them"); because they stop reading, they stop steering, and quality quietly drops. HTML renders mockups, diagrams, and scrollable structure, so the human actually engages, which uplevels the spec, which produces a better build. The compute-allocator frame supplies the stakes: an eight-hour run is roughly $500, so the leverage lives in deciding what to spend it on, and that decision happens in the spec. It generalizes to weekly status updates: Claude reads Slack and emits an HTML report a manager will actually read. How it goes wrong: HTML costs more tokens, plans can bloat with scaffolding you did not ask for (his scripted the whole podcast), and prettiness can mask a weak plan.

### Spine 2 — Throwaway micro-UIs to edit one plan module (covered)

The claim: when one module of your plan is awkward to edit, have Claude build a throwaway custom UI for exactly that module, edit it visually, then paste the structured output back. Why it is non-obvious: the instinct is to iterate in chat ("I don't like it, change it") or hand-edit markdown; the move is to spend tokens building single-use software to kill a one-off friction. The mechanism: a bespoke interface ("design the ideal interface for this problem") matches the shape of the data, for example a decision-rules table, far better than free text, so edits are precise and fast; the UI emits markdown to copy back, closing the loop without terminal ping-pong. Claire's frame: "micro software on top of micro software." It generalizes to any structured sub-artifact: pricing tables, state machines, config matrices, prioritization grids. How it goes wrong: the copy-paste round trip is manual, and disposable tools accumulate if you never toss them. This spine is load-bearing for understanding the video, so it keeps its deep dive, but it gap-checks to ✅ COVERED, so it is excluded from the ranked pitches and does not count toward the post gate.

### Spine 3 — A living design system as a portable HTML file

The claim: encode your design system as a portable design-system.html that lives in the repo and travels to every new project, instead of design.md. Why it is non-obvious: teams treat the design system as a doc or a Figma file kept separate from code; Thariq keeps it as one self-contained HTML file that both renders the system and follows the code. The mechanism: you point Claude at a folder or an existing repo and have it extract the design system (colors, typography, spacing, radius, components) into a single HTML file; because it is HTML it renders the actual components with knobs to vary padding and border, so the file is simultaneously the spec and a live preview; dropping it into a new project gives Claude a compressed, referable source of truth in one mention. It generalizes into a marketer and designer workflow: a component-visualization page shows the components "in action and interactable," so a marketer can export a real-looking transparent PNG for a deck or a video. How it goes wrong: the file drifts from the real components if it is never regenerated, and a small system fits one file while a large one may need splitting.

## 🎬 Proposed ACS videos

### 1. Stop Writing Markdown Plans: Put Your Specs in HTML So You Actually Read Them

- **HOOK:** Your thousand-line markdown plans went unread, so you quietly stopped steering; rendered HTML pulls you back in.
- **THE PROMISE:** For solo builders and PMs: brainstorm, plan, and spec in HTML so you stay in the loop and ship better.
- **THE SHAPE:**
  1. The compute-allocator framing: an eight-hour run is roughly $500, so planning is where you allocate the money.
  2. Prompt "brainstorm eight ideas in an HTML file with mockups," then scroll the rendered visual guide.
  3. Have Claude interview you, then "create an HTML plan with excerpts, mockups, code, whatever is needed for maximum context."
  4. Read and edit the rendered plan; upload it as a shareable link so colleagues actually read it.
- **SPINE:** 1.
- **SLOT:** My Daily Workflows (new HTML-planning entry) or Techniques > Planning Before Implementing.
- **RELATIONSHIP:** 🔗 complements "Interactive HTML Artifacts" and "Channel HTML Artifacts" (both in My Daily Workflows, April 2026), which teach making artifacts interactive and feeding browser comments back to Claude Code. This video moves one step upstream: authoring the plan, PRD, or spec itself in HTML instead of markdown, plus the compute-allocator argument for why roughly 99% of your tokens should go to planning, not production code. Do not re-teach the click-to-comment loop; that is already filmed.
- **PROOF TO REUSE:** "the plans are so long, I honestly have stopped reading them and this was honestly a mistake"; the eight-idea HTML brainstorm demo; "whatever is needed to give me maximum context"; the ~1% of tokens going to production code.

### 2. Your Design System Should Be an HTML File That Travels With the Repo

- **HOOK:** design.md cannot render. A single design-system.html shows every component and follows you into any new project.
- **THE PROMISE:** For builders and designers: keep one portable HTML design system Claude references in every repo, doubling as a marketer-ready component gallery.
- **THE SHAPE:**
  1. Point Claude at an existing repo and have it extract colors, typography, spacing, radius, and components into one HTML file.
  2. Add knobs to vary padding and border, so the file is both the spec and a live preview.
  3. Drop design-system.html into a new project and reference it with a single mention.
  4. Build a component-visualization page so marketers export real-looking transparent PNGs for decks and videos.
- **SPINE:** 3.
- **SLOT:** My Daily Workflows or Loopy AI (design chapter).
- **RELATIONSHIP:** 🔗 complements "Example: Design Source of Truth" (Loopy AI, L2), which produces a design source of truth from messy UI via builder-review loops. This video adds encoding that system as a single portable HTML file that lives in the repo, travels across projects, and serves marketers via a real-looking component gallery. It also extends "Designing Components" (throwaway per-component HTML) into a persistent, reusable file.
- **PROOF TO REUSE:** the living design system demo (colors, typography, spacing, radius, core components); Claude Design extracting a system from a linked GitHub repo; the marketer transparent-PNG component gallery Claire describes as a source of truth for videos.

## 📚 Full wisdom (reference)

**SUMMARY** — Anthropic Claude Code engineer Thariq Shihipar tells Claire Vo why he replaced markdown with HTML for plans, specs, brainstorms, and design systems traveling with code.

**IDEAS**
- Markdown plans now run thousands of lines, so Thariq stopped reading them and just asks Claude.
- HTML renders mockups and diagrams directly, so Claude stops drawing crude ASCII wireframes inside markdown plans.
- Telling Claude to run eight hours really means authorizing roughly five hundred dollars of compute spend.
- Everyone is becoming a compute allocator, deciding through spec and planning what work deserves the money.
- He prompts Claude to brainstorm eight demo ideas directly inside one HTML file with visual mockups.
- After brainstorming, he has Claude interview him to surface unknown unknowns before writing the implementation plan.
- The plan prompt asks for excerpts, mockups, and code, whatever is needed for maximum planning context.
- Overbuilt skills labeling Claude an expert planner usually outsource and constrain too much, degrading its results.
- He builds a throwaway custom HTML app to edit arbitrary decision rules, copying markdown back afterward.
- This is micro software on micro software, zooming into one plan module with bespoke custom interfaces.
- A living design system lives as one HTML file holding colors, typography, spacing, radius, and components.
- Point Claude at a folder, extract the design system, then pass the HTML around new projects.
- Component visualization pages let marketers quickly grab real looking transparent PNGs for their decks and videos.
- You can add comment and annotation UIs to plans, then submit fixes back to Claude Code.
- HTML plans upload to AWS as shareable links, so busy colleagues actually read your implementation plan.

**INSIGHTS**
- Format choice targets the human, not the model; engagement with the spec is what raises quality.
- When reading collapses, steering collapses; unreadable plans quietly remove the human from the whole decision loop.
- Strong prompting balances specifying exactly what you need against leaving Claude an out to improvise freely.
- The interface boundary matters: choose types and tests as the layer where you engage with Claude.
- Types plus success criteria form bookends; everything between those two given constraints becomes negotiable implementation gravy.
- Cheap content flips old rules: stop obsessing over one single blessed source of truth and format.
- Verification is not testing; rubrics, synthetic data, and recorded videos now count as valid modern checks.
- Beautiful working artifacts keep humans engaged, and that engagement plausibly propagates into a better final product.

**QUOTES**
- "the plans are so long, I honestly have stopped reading them and this was honestly a mistake." — Thariq Shihipar
- "you heard it here first. HTML is the new markdown." — Claire Vo
- "when you say okay cloud can run for eight hours what you're really saying is cloud can spend like 500 bucks" — Thariq Shihipar
- "I'm going to say you're a compute allocator, babe. That's the job now." — Claire Vo
- "whatever is needed to give me maximum context is like my way of saying like, hey, Claude, like I trust you here." — Thariq Shihipar
- "This is like micro software on top of micro software." — Claire Vo
- "the amount of tokens I produce that go into production code like extremely small. It's like 1% or something." — Thariq Shihipar
- "test verification is not testing." — Thariq Shihipar
- "design.md is dead. Long lived design.html." — Claire Vo

**HABITS**
- He always starts sessions by brainstorming with Claude as a partner before requesting any concrete plan.
- He refuses to read outputs longer than one Claude Code screen, so mockups aid his scanning.
- He ends prompts with I trust you, not make no mistakes, deliberately inviting Claude's own judgment.
- Every week he sends his manager an HTML status update Claude generates by reading his Slack.
- For technical work he specifies type interfaces, editing those rather than the underlying implementation code details.
- He keeps synthetic data and runs a CLI against it to catch previously broken edge cases.
- He never yells at Claude, preferring friendly prompts since emotional charge activates different internal model features.
- He deliberately avoids reading Claude's thinking traces, giving the model privacy like a trusted human employee.

**FACTS**
- Code with Claude was Anthropic's first developer conference, held in San Francisco, where this was filmed.
- Anthropic announced a SpaceX partnership to bring more compute online at the Code with Claude event.
- Anthropic said it is thinking about orbital data centers, which Thariq called incredibly sci-fi but plausible.
- Recent Anthropic research shows emotional charge in prompts activates different internal features inside the Claude models.
- The Claude desktop application ships three tabs, and Thariq names the code tab his personal favorite.
- Claude Design extracts a design system automatically when you link an existing GitHub repository to it.
- Jevons paradox describes how cheaper resources increase, rather than decrease, total consumption of that given resource.
- Anthropic recently announced outcomes, a goal-oriented feature focused on achieving a defined result by any means.

**REFERENCES**
- Tools: Claude Code, Claude Design (claude.ai/design), AWS, Figma, GitHub.
- Anthropic features/news: "outcomes" (goal-oriented), the SpaceX compute partnership, orbital data centers, Code with Claude event.
- People: Thariq Shihipar (X @trq212, thariq.io, GitHub ThariqS); Claire Vo (ChatPRD, clairevo.com); Cat and Boris (colleagues); Nate (Claude Design GitHub extraction).
- Companies/examples: Stripe team's internal vibe-coding platform for design/spec review; Databricks, PayPal, Ollipop (sponsor read); Brex, Figma, Etsy, Twilio, Lithic, Skyfire (sponsor read).
- Concepts: Jevons paradox; compute allocator; just-in-time documentation; verification vs testing.
- Models referenced: Opus 4, Opus 4.5, Opus 4.7, Claude 3.5.
- Show/blog: How I AI podcast (howiaipod.com); ChatPRD "How I AI" blog post on replacing markdown with HTML.

**ONE-SENTENCE TAKEAWAY** — Author plans, specs, and design systems in HTML so you stay engaged and steer quality.

**RECOMMENDATIONS**
- Ask Claude to brainstorm your next feature ideas inside an HTML file with rendered visual mockups.
- Have Claude interview you about a chosen idea before it writes any implementation plan at all.
- End planning prompts with whatever is needed for maximum context, giving Claude a deliberate escape hatch.
- When a plan section annoys you, ask Claude to build a custom editing UI for it.
- Encode your design system as one portable HTML file and reference it across every new project.
- Build a component gallery page so marketers can export real looking transparent PNGs for marketing assets.
- Specify type interfaces plus test criteria as your bookends, then let Claude fill everything in between.
- Upload HTML plans to a shareable link so colleagues actually read and comment on them directly.
