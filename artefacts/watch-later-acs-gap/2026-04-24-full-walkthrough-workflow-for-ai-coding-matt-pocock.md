---
title: "Full Walkthrough: Workflow for AI Coding — Matt Pocock"
video_url: https://www.youtube.com/watch?v=-QFHIoCo-Ko
video_id: -QFHIoCo-Ko
channel: AI Engineer
published: 2026-04-24
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Full Walkthrough: Workflow for AI Coding — Matt Pocock**](https://www.youtube.com/watch?v=-QFHIoCo-Ko) - AI Engineer - uploaded 2026-04-24

> Three film-able spines: two net-new ACS videos plus one complement. Vertical slices and TDD-anti-cheat are genuine gaps.

## 1. The ideas worth a video

**Slice work vertically, not horizontally, so the agent gets integrated feedback after slice one.** Matt shows AI defaults to building layer by layer (all schema, then all API, then all UI), which means no working path exists until the end. VERDICT: ❌ net-new video available.

**Codebase architecture is a prompt-engineering surface: deep modules make repos testable, and feedback-loop quality is the ceiling on AI output.** Bad codebases make bad agents. VERDICT: 🔗 next-step video available (beyond "Reducing Agent Confusion in Growing Projects").

**Make the agent do TDD red-green-refactor so it cannot cheat its own tests.** Writing the failing test first instruments the code before it exists. VERDICT: ❌ net-new video available.

## 2. Summary + counts

Matt Pocock's two-hour AI Engineer workshop walks the full agentic coding lifecycle: grill for alignment, slice work vertically, run AFK agents, and design testable codebases.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 3. 🔬 Deep dive

### Spine 1 — Vertical slices / tracer bullets for agents

The claim: force agents to build thin vertical slices that cross every layer at once, never horizontal layers built one at a time. Why it is non-obvious: the tidy instinct, and the agent's own instinct, is to finish all the schema, then all the API, then all the UI. It feels organized. Why it is true: you only get an integrated, testable path once the top layer lands, so horizontal building leaves the agent "coding blind" until phase three, whereas a vertical slice closes the feedback loop at the end of slice one, letting both agent and human course-correct immediately. Matt borrows the pragmatic programmer's tracer-bullet image: a glowing round every sixth shot so you can see where you are aiming. It generalizes cleanly to data pipelines, where you wire a single record end to end before scaling breadth. How it goes wrong: agents revert to horizontal even when told to slice vertically (Matt had to correct the model mid-demo when it proposed building the gamification service alone), and a slice that grows too fat stops being a fast feedback unit.

### Spine 2 — Design deep modules so agents can code well (feedback-loop ceiling)

The claim: the architecture of your repo sets the ceiling on how well agents perform, because module depth decides how cleanly you can draw test boundaries, and feedback-loop quality is the ceiling on AI output. Why it is non-obvious: people reach for prompting and model choice as the levers; Matt argues the codebase itself is the surface, and "bad code bases make bad agents." Why it is true: deep modules (John Ousterhout) expose a small interface over a lot of functionality, so a single test boundary wraps meaningful behavior; shallow modules scatter tiny files with tangled dependencies the agent cannot navigate and cannot test without brittle mocking, so its feedback loops are weak, so its output is weak. It generalizes to refactoring a service-heavy backend into fewer deep services before pointing agents at it. How it goes wrong: unaided agents naturally emit shallow modules, so you must direct them, and over-deep "god" modules hide too much. The trick that keeps you sane: design the interfaces yourself, delegate the guts as gray boxes, and keep your mental map of the codebase.

### Spine 3 — TDD red-green so the agent cannot cheat its tests

The claim: making the agent follow red-green-refactor, writing a failing test first, confirming red, then implementing to green, is the highest-leverage move for trustworthy output, because it stops the agent gaming its own tests. Why it is non-obvious: most people add tests after implementation, or let the agent write code and tests together. Why it is true: Matt observes agents cheat exactly when they write the whole implementation and then the whole test layer just beneath it; writing the failing test first instruments the code before it exists, so the test encodes intent independently and the agent must satisfy a target it cannot trivially fake. It also seeds the repo with genuinely good tests, which raises the feedback-loop quality that caps everything else. It generalizes to any crisp signal, such as a type-check loop that caught a real error in the demo. How it goes wrong: front-end is hard to TDD because it is multimodal and needs human eyes, and TDD only works where you can express a sharp failing check.

## 4. 🎬 Proposed ACS videos

### 1. Why Your AI Codes Blind: Vertical Slices for Agents

- **HOOK:** Your agent builds all the schema, then all the API, then the UI, and gets zero feedback until the very end.
- **THE PROMISE:** For engineers planning agent work, learn to shape each issue as a thin end-to-end slice so the first slice already runs and can be QA'd.
- **THE SHAPE:** (1) Show an agent proposing a horizontal "build the whole service first" slice. (2) Explain the tracer-bullet metaphor and why feedback timing matters. (3) Rewrite the issue as a vertical slice ("award points for lesson completion, visible on dashboard"). (4) Run it and QA a working path immediately. (5) Rule of thumb for slice size.
- **SPINE:** Spine 1 (vertical slices).
- **SLOT:** Techniques (fundamental-techniques) → Working with the Codebase; alt Loopy AI backlog/planning chapter.
- **RELATIONSHIP:** ❌ net-new. Closest is Loopy AI "Don't Pre-Sequence the Backlog," which is about dynamic ordering of issues, not the vertical shape of each individual slice, so nothing teaches slice geometry for feedback.
- **PROOF TO REUSE:** The anti-aircraft tracer-bullet image; the mid-demo correction where the agent proposed a horizontal gamification-service slice; "you don't get feedback on your work until you've really started or completed phase three."

### 2. Stop Your Agent Cheating Its Tests: TDD for Coding Agents

- **HOOK:** Agents cheat tests, and they cheat them precisely because they write the implementation first and the tests second.
- **THE PROMISE:** For engineers running autonomous agents, learn to enforce red-green-refactor so tests encode intent before code exists and the agent cannot game them.
- **THE SHAPE:** (1) Demo an agent writing a passing-but-hollow test after the fact. (2) Introduce a red-green-refactor skill. (3) Watch the agent write a failing test, confirm red, implement to green. (4) Show the type-check feedback loop catching a real error. (5) Note where TDD breaks down (front-end).
- **SPINE:** Spine 3 (TDD red-green).
- **SLOT:** Techniques (fundamental-techniques) → new "Feedback Loops & TDD" chapter; alt Loopy AI L2: Builder & Verifier.
- **RELATIONSHIP:** ❌ net-new. Loopy AI "Builder Verifier Pattern" separates a builder from a verifier agent, but does not teach the red-green-refactor process inside the builder as an anti-cheating instrument, so the TDD mechanism is uncovered.
- **PROOF TO REUSE:** "it tends to try to cheat at the tests because it's sort of doing it in layers"; the red-green-refactor skill in the demo repo; the 284-tests result; "the quality of your feedback loops influences how good your AI can code. Essentially, that is the ceiling."

### 3. Design a Codebase Your Agent Can Actually Test

- **HOOK:** You keep blaming the model, but the ceiling on your agent's output is the shape of your repo.
- **THE PROMISE:** For engineers on maturing codebases, learn to convert shallow scattered modules into deep testable ones so agents get stronger feedback loops.
- **THE SHAPE:** (1) Contrast deep vs shallow modules (Ousterhout) with the test-boundary problem. (2) Run an improve-codebase-architecture skill to find shallow clusters worth deepening. (3) Wrap one deep module in a single test boundary. (4) The gray-box trick: design interfaces, delegate the guts, keep your map.
- **SPINE:** Spine 2 (deep modules / feedback ceiling).
- **SLOT:** Context Engineering → new "Designing Codebases for Agents" chapter; alt Advanced Techniques.
- **RELATIONSHIP:** 🔗 complements "Reducing Agent Confusion in Growing Projects" (Techniques → Working with the Codebase), which audits confusing architecture so agents stop editing the wrong areas. That video fixes comprehension; this adds the design principle, module depth for testability, that raises the feedback-loop ceiling on code quality. Do not re-teach the confusion audit.
- **PROOF TO REUSE:** "bad code bases make bad agents"; deep vs shallow module diagram; the video-editor module wrapped end to end for testing ("night and day"); "design the interface for these modules, but then delegate the implementation."

### Also film-able (not deep-dived)

- **Push vs pull for coding standards** (🟡 partial): implementers pull standards via skills, reviewers get them pushed in. Slot: Prompt Engineering → Aligning to Your Intent. Uncovered as a distinct framing.

Note: the grill-me / alignment-first thesis is already covered by "Clarifying Questions" (Prompt Engineering), the Spec Developer chapter, and "Don't Verify Against the Plan" (Loopy AI); the smart-zone / dumb-zone constraint by "Long Context Failure"; fresh-context review by "/simplify" and "Avoiding 'Code Bias' Caused Loops"; and kanban / parallel AFK loops by the Loopy AI L4/L5 backlog videos. None promoted as pitches.

## 5. 📚 Full wisdom (reference)

**SUMMARY**
Matt Pocock's two-hour AI Engineer workshop walks the full agentic coding lifecycle: grill for alignment, slice work vertically, run AFK agents, and design testable codebases.

**IDEAS**
- LLMs have a smart zone and a dumb zone starting past roughly 100k context tokens today.
- Attention relationships scale quadratically; every added token strains a model like adding teams to a league.
- Treat LLMs like the guy from Memento: they forget everything, so prefer clearing context over compacting.
- The grill-me skill interviews you relentlessly, one question at a time, until you reach shared understanding.
- Reject the specs-to-code movement; the code is your real battleground, so you must keep understanding it.
- Split tasks into human-in-the-loop versus AFK; planning alignment must stay human, implementation can go fully autonomous.
- A PRD is just a destination document summarizing the design concept; do not obsess over it.
- Do not read the whole PRD; once aligned you are only testing the model's summarization ability.
- AI loves to code horizontally, layer by layer, so it gets no feedback until phase three.
- Slice work into thin vertical tracer bullets that cross every layer and produce something visible immediately.
- Build a kanban board of independently grabbable issues so multiple agents parallelize instead of running sequentially.
- A numbered multi-phase plan is really just a loop; collapse it into phase-n running until complete.
- The Ralph loop caps all issues into context, grabs recent commits, and runs Claude in Docker.
- TDD red-green-refactor forces the agent to write failing tests first, making it much harder to cheat.
- Feedback-loop quality is the ceiling on AI code; bad loops guarantee bad agent output every time.
- Review in a fresh context; reviewing inside the implementation session means reviewing from the dumb zone.
- Deep modules expose a small interface over lots of functionality, making one clean test boundary possible.
- Shallow modules scatter tiny files with tangled dependencies that AI cannot easily navigate or test cleanly.
- Bad codebases make bad agents; garbage in the repo simply guarantees garbage out of the agent.
- Design module interfaces yourself but delegate implementation, treating modules as gray boxes to retain codebase understanding.
- Push versus pull: implementers pull coding standards via skills, while reviewers get standards pushed into context.
- Doc rot is real; keeping old PRDs around later misleads future agents, so Matt closes them.
- Own your whole planning stack; without observability over frameworks you cannot fix them when they break.

**INSIGHTS**
- Software engineering fundamentals from twenty-year-old books map almost perfectly onto working effectively with today's coding agents.
- Alignment, not documentation, is the true deliverable of planning; the shared design concept matters most here.
- Feedback speed governs everything: vertical slices, TDD, and testable modules all exist purely to accelerate feedback.
- Context is a scarce budget; the whole workflow exists to keep agents inside the smart zone.
- Codebase architecture is now a prompt-engineering surface: module depth directly determines how well your agents perform.
- Delegating implementation while owning interfaces lets you move fast without losing your mental map of code.
- Parallelizing agents requires independence: only a dependency graph, not a sequential plan, unlocks truly concurrent work.
- QA is where humans inject taste; fully automating every stage produces working but soulless, low-quality slop.
- More delegation means more review; delegating coding inevitably shifts the human bottleneck onto QA and review.

**QUOTES**
- "when you're working with LLMs, they have a smart zone and a dumb zone" — Matt Pocock
- "LLM are kind of like the guy from Momento, right? They just continually forget." — Matt Pocock
- "the code is your battleground" — Matt Pocock
- "I needed to reach a shared understanding. I didn't need an asset. I didn't need a plan." — Matt Pocock
- "I don't look at these. The reason I don't look at these is because what am I testing at this point?" — Matt Pocock
- "AI loves to code horizontally. So it loves to code layer by layer." — Matt Pocock
- "if your codebase doesn't have feedback loops you're never ever ever going to get decent AI decent output out of AI" — Matt Pocock
- "bad code bases make bad agents" — Matt Pocock
- "We're not producing slop here." — Matt Pocock
- "the reviewer will be dumber than the thing that actually implemented it" — Matt Pocock
- "if you take one thing away from this session... buy a ton of those old books" — Matt Pocock

**HABITS**
- Matt starts nearly every single coding task by clearing context and invoking the grill-me skill first.
- He watches the token status line constantly to know exactly how close he is to dumbness.
- He usually dictates to the AI rather than typing, keeping himself in the loop between questions.
- He always prefers clearing context over compacting so the starting state stays identical and predictably clean.
- He always runs his AFK agent loops inside a Docker sandbox rather than exposing the host machine.
- He always manually QAs features himself because that is where he imposes his taste and opinions.
- He closes finished PRDs and issues rather than keeping them, deliberately avoiding documentation rot in repos.
- He uses Sonnet for implementation and Opus for reviewing, deliberately reserving the smarter model for review.

**FACTS**
- Matt's own course video manager repo holds around 744 closed issues containing PRDs and implementation tickets.
- Dex, who runs a company called Human Layer, originated the smart-zone and dumb-zone framing Matt uses.
- Matt marks roughly 100k tokens as today's practical smart-zone boundary regardless of the advertised context window.
- Claude Code shipped a one-million-token context window the same day Matt launched his Claude Code course.
- The grill-me skill has reportedly asked Matt's students up to a hundred questions in one session.
- A grilling session in the demo answered twenty-two of its own questions using roughly 25k tokens.
- The demo repository had accumulated 284 tests after the agent completed just one gamification feature slice.
- An explore subagent burned about 94k Opus tokens while barely raising Matt's own main context usage.
- Matt built Sand Castle, a TypeScript library that runs parallel agent loops in git-worktree Docker containers.

**REFERENCES**
- Dex (Human Layer) — smart zone / dumb zone framing
- Ralph Wiggum as a software practice — the phase-n loop
- Frederick P. Brooks, "The Design of Design" — the shared design concept
- Martin Fowler, "Refactoring" — do not bite off more than you can chew
- "The Pragmatic Programmer" — tracer bullets / vertical slices
- John Ousterhout, "A Philosophy of Software Design" — deep vs shallow modules
- Claude Code (Matt uses it but is lukewarm on it)
- Skills used: grill-me, write-a-PRD, PRD-to-issues, red-green-refactor, improve-codebase-architecture
- Sand Castle — Matt's TypeScript library for parallel AFK agent loops
- AI Hero — Matt's website, home of the token status-line article
- Slido — live audience Q&A voting
- Cucumber — language for writing user stories
- Beads framework (Steve) — kanban/issue management, untested by Matt
- Memento — the film, metaphor for LLM forgetting
- Playwright MCP / agent browser — front-end tooling Matt finds immature
- SQLite, tRPC, npm, Docker — stack elements in the demo

**ONE-SENTENCE TAKEAWAY**
Twenty-year-old software engineering fundamentals, applied deliberately, are what make autonomous coding agents actually ship well.

**RECOMMENDATIONS**
- Add a live token status line to every coding session so you always see dumb-zone proximity.
- Grill yourself with a dedicated skill before planning so you reach alignment instead of a document.
- Slice every feature vertically so the very first slice already produces something visible and testable end-to-end.
- Turn plans into kanban dependency graphs so independent issues can be grabbed by many parallel agents.
- Make the agent use TDD red-green-refactor so tests get written before implementation, largely preventing test cheating.
- Always clear context before reviewing so the reviewer works in the smart zone, not the dumb.
- Run an improve-codebase-architecture skill on your repo to find shallow modules worth deepening for better testability.
- Design your module interfaces yourself, then delegate the implementation inside those gray-box modules entirely to agents.
- Sandbox your AFK agent loops in Docker, and buy old software-engineering books to mine into prompts.
</content>
</invoke>
