---
title: The No-Rework Workflow for AI Coding Assistants
videoId: YcT7gjzj2TU
url: https://www.youtube.com/watch?v=YcT7gjzj2TU
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Write throwaway "learning tests" that actually run an opaque dependency and assert on its real output, so your design is grounded in observed behavior instead of docs that lie.**
Because docs and your own assumptions are the false inputs that force a two-phase-deep rewind, and a tiny running probe kills that risk before any real code exists.
VERDICT: net-new video available.

**2. Front-load the irreversible architecture decisions onto a cheap design-discussion doc, and iterate the doc (not the code) until you are aligned, because backtracking merged code is coding's single most expensive move.**
This is the whole "no-rework" thesis made concrete: decisions cost minutes and dominate outcomes, execution costs hours, so you move the human judgment call to the cheapest artifact.
VERDICT: next-step complement video available.

**3. Force the agent to plan in vertical slices (thin end-to-end cuts you can test each phase) instead of the horizontal layer-by-layer plan models default to.**
Horizontal planning buries twelve hundred untested lines before any feedback; vertical slicing lets you catch a wrong decision after two hundred lines, not two thousand.
VERDICT: next-step complement video available.

## Summary + counts

Vaibhav (BoundaryML/BAML) and Dexter (HumanLayer) live-build message queuing in their Claude Code harness Riptide, showing how upfront design, learning tests, and vertical planning eliminate rework.

Counts: 🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 — Learning tests / proofs against opaque dependencies

The claim: before designing against a closed-source or poorly documented dependency, write a disposable test that runs it under real conditions and asserts on the actual output, then feed those observations into the design. Most people treat the docs (or Claude's memory of them) as ground truth and start planning. The non-obvious move is that documentation is exactly the input most likely to be wrong or misread, and you will not discover it until you are "two phases into your implementation and then you're gonna have to go rewind and redo all of this work." The mechanism is a chain: an opaque SDK hides its true behavior, so any assumption you bake in carries hidden error; a learning test forces that behavior into the open ("the observed output from the test, which shows exactly how the state machine behaves"); with the behavior confirmed, "the design doc here is trivial." It generalizes cleanly beyond SDKs: probe a third-party API's real error codes, or a database's actual locking behavior, before committing to a schema. How it goes wrong: the test can be too narrow (their existing streaming test "uses a timeout and doesn't actually test that you can queue a message"), so a proof that asserts the wrong thing gives false confidence.

### Spine 2 — The design-discussion doc as the human decision gate

The claim: let the agent do everything up to the high-stakes architecture decision (read a hundred thousand lines, surface options A/B/C, ask sharp questions), then make the human choose on the doc before any code is written, and iterate the doc until aligned. The default this argues against is Claude's plan mode: "most people just hit straight enter, clear context, go onward" because "plans aren't designed to be read." The mechanism: decisions "take not a lot of time and have a lot of impact, whereas execution can take a lot of time"; a design doc is a two-hundred-line artifact you are not yet attached to, so re-steering it is cheap, whereas a merged thousand-line PR that needs twenty percent rework is "a huge mental and emotional burden on both the submitter and the reviewer." Aligning on the cheap artifact is what let Dexter one-shot a seventeen-thousand-line refactor. It generalizes to team review: send the design doc, not the finished PR, to the codebase owner. How it goes wrong: there is a sweet spot ("spend 10 minutes and get it 90 percent" beats "an hour to get 99 percent"), and over-planning past that point just burns time you could spend reading real code.

### Spine 3 — Vertical planning over horizontal planning

The claim: models "by default tend to want to do horizontal planning" (database, then service layer, then API, then frontend), which produces "the other side of twelve hundred lines of code and there's been nothing along the way for you to test." The fix is vertical planning: slice a thin cut through every layer so each phase is independently testable. Why it is non-obvious: a layered plan looks orderly and complete, so people approve it, not noticing that testability has been deferred to the very end. The mechanism: you cannot validate a decision you cannot test, so a horizontal plan concentrates all risk at the finish; a vertical slice lets you "click something in the UI and just go look that a thing was inserted into the database," surfacing a wrong decision after two hundred lines instead of two thousand. Dexter reorders the plan to build the endpoint first "because you can't test this until you have a way to send the messages in." It generalizes to any migration or large refactor. How it goes wrong: forcing verticality on genuinely sequential work (a serialization-layer rewrite) can add mocking overhead that a careful horizontal pass would avoid.

## 🎬 Proposed ACS videos

### 1. Learning Tests: Stop Trusting the Docs, Prove the Behavior

- HOOK: Your agent's biggest source of rework is not bad code, it is a confident wrong assumption about a library it never actually ran.
- THE PROMISE: For engineers wiring agents against closed-source SDKs and third-party APIs, one repeatable move that turns "I hope the docs are right" into "I have a test that proves it."
- THE SHAPE: (1) The rewind problem: a wrong assumption two phases deep costs a full redo. (2) Have Claude ripgrep node_modules for the real SDK types. (3) Write one learning test that runs the SDK under bypass permissions and asserts on the actual JSON it emits. (4) Feed the observed state-machine output back into the design doc. (5) Show the design collapse from "unknown" to "trivial" once behavior is confirmed.
- SPINE: 1
- SLOT: Context Engineering > new chapter "Grounding context in empirical proof" (net-new; the shipped class covers context construction but not empirically probing an opaque dependency).
- RELATIONSHIP: ❌ net-new. Nearest neighbor is the "build-it-twice" brief, but that throws away a whole feature build to learn; a learning test is a targeted empirical probe of one external dependency's behavior, a different demo and a different slot.
- PROOF TO REUSE: "the observed output from the test, which shows exactly how the state machine behaves"; the ripgrep-through-node_modules trick to read the minified SDK's types; the failure that their streaming test "uses a timeout and doesn't actually test that you can queue a message."

### 2. Iterate the Doc, Not the Code: The No-Rework Decision Gate

- HOOK: Everyone hits enter on Claude's plan without reading it, then spends a day rewinding the code it wrote. There is a cheaper place to be wrong.
- THE PROMISE: For anyone shipping non-trivial features with an agent, a workflow that concentrates your scarce human judgment on a two-hundred-line design doc so the implementation one-shots.
- THE SHAPE: (1) Why decisions beat execution: minutes of impact versus hours of typing. (2) Let the agent read the codebase and surface options A/B/C with tradeoffs. (3) Do "brain surgery on the model": make the architecture call on the doc, before any code. (4) The Ralph-Wiggum loop: prompt "what's inconsistent or missing" until the outline stops surfacing gaps. (5) Payoff: aligning on the cheap doc let a seventeen-thousand-line refactor one-shot.
- SPINE: 2
- SLOT: Techniques > planning-and-decisions chapter (alongside high-level-strategy-low-level-details).
- RELATIONSHIP: 🔗 complements "build-it-twice." That video teaches the opposite reflex, build a throwaway prototype and rebuild because you know least at the start; this video is its counterweight, the case where the architecture decision IS knowable and expensive to reverse, so you front-load it onto a doc instead of prototyping. The pair answers "when do I plan hard versus when do I build twice?" Do not re-teach the throwaway-prototype thesis; teach the decision gate.
- PROOF TO REUSE: "decisions take not a lot of time and have a lot of impact, whereas execution can take a lot of time"; "the idea of this design discussion doc is that it forces the human to do the high-stakes decision about the architecture"; the "great leaders are right a lot ... you move so much faster because you don't have to go back and fix your mistakes" framing.

### 3. Vertical Planning: Make Every Phase Testable

- HOOK: Your agent wrote twelve hundred clean lines and you could not test a single one until the end. That is a planning bug, not a coding bug.
- THE PROMISE: For engineers running large agent-built features, a way to restructure the plan so you catch a wrong decision after two hundred lines instead of two thousand.
- THE SHAPE: (1) Name the default failure: horizontal planning (DB, then service, then API, then UI) defers all testing to the finish. (2) Reshape the plan into a vertical slice through every layer. (3) Reorder to build the endpoint first so you can verify a row landed in the dev database. (4) Test and validate one piece at a time so you never debug the data layer and the UI at once. (5) Tie it to risk: each testable phase is a bet that lowers your probability of backtracking.
- SPINE: 3
- SLOT: Techniques > incremental-build chapter (alongside build-small-merge-big).
- RELATIONSHIP: 🔗 complements "build-small-merge-big" (currently Doing). That video is about building small, mergeable increments; this adds the missing upstream step, how to STRUCTURE the plan doc so the increments are vertical and testable rather than the horizontal layers models default to. It teaches the plan shape that makes small-merge-big possible.
- PROOF TO REUSE: "the models by default tend to want to do what I call horizontal planning ... before you know it you're at the other side of twelve hundred lines and there's been nothing to test"; "I want to be able to click something in the UI and just go look that a thing was inserted into the database"; "you want to optimize for finding surprises and finding incorrect things as early in the process as possible."

### Also film-able (not deep-dived)

- **Prune your skills to five to seven, treat them as products.** "prune prune prune prune prune that is the magic word"; kill low-adoption skills the way a PM kills features only ten percent of users touch, because compounding tooling returns need shared adoption. Slot: Skills class > maintaining-a-skill-library (net-new angle; the class covers building and chaining, not curation-by-adoption).
- **Keep the frontend dumb, consolidate logic on the backend to make it agent-friendly.** A preference-based API (queue/continue/interrupt/auto) that the backend resolves to the correct state dissolves race conditions. Slot: borderline scope (general architecture) with an agentic hook; hold unless paired with an agent-facing-API angle.

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BoundaryML/BAML) and Dexter (HumanLayer) live-build message queuing in their Claude Code harness Riptide, showing how upfront design, learning tests, and vertical planning eliminate rework.

### IDEAS
- Write throwaway learning tests that run an opaque SDK and assert on its actual observed output.
- Docs about closed-source libraries lie often, so prove real behavior empirically before baking design assumptions in.
- Backtracking is the most expensive move in coding; being right just means never rewinding merged work.
- Great leaders are right a lot because good upfront decisions let you skip costly correction loops.
- Decisions cost little time but huge impact; execution costs time, so invest thinking where leverage lives.
- Models default to horizontal planning: database, service, API, frontend, twelve hundred untested lines before any feedback.
- Vertical planning slices thin through every layer so each phase becomes testable long before final completion.
- Iterate the cheap design doc, not expensive code; align on a low-stakes artifact nobody's attached to.
- The design discussion doc forces the human to make high-stakes architecture calls before Claude writes code.
- AI reads a hundred thousand lines and surfaces options; you pick decisively between A, B, C.
- Most people hit enter on plan mode without reading, because plans aren't designed to be read.
- Plan, research, and design docs are throwaway; once shipped, code becomes the single source of truth.
- Ralph Wiggum the outline: repeatedly ask what's inconsistent or missing until the plan stops surfacing gaps.
- That single what's-inconsistent-or-missing prompt gave a claimed hundred percent hit rate on one-shotting large complex features.
- Keep the frontend dumb; consolidate state and business logic on the backend for reliably agent-friendly systems.
- A preference-based API (queue, continue, interrupt, auto) dissolves race conditions the backend resolves to correct state.
- One bad grep pattern amplifies; your codebase regresses toward the statistical mode of its existing patterns.
- Prune your skills to five or seven excellent ones everyone uses, killing the low-adoption long tail.
- Treat internal skills like products; a good PM cuts features only ten percent of users touch.
- Building all options in parallel still costs evaluation time; better to parallelize entirely different features instead.
- For V2 migrations, tell it to prefer V2, then verify the doc recorded that critical decision.
- Writing code is cheap now, so migrate V2 into a fresh package instead of entangling versions.

### INSIGHTS
- The scarce resource in agentic coding is correct early decisions, not typing speed or token budget.
- Every artifact exists to move the irreversible decision earlier, where changing your mind is still cheap.
- Empirical proof beats documentation because a running test cannot misremember or misdescribe the dependency's real behavior.
- Reviewing a two-hundred-line design artifact is far cheaper and safer than reviewing competing thousand-line pull requests.
- Human judgment concentrates at the architecture gate; everything upstream (reading, option-finding) is safely delegable to agents.
- A dumb frontend consolidates logic where even a weak agent can operate the entire backend correctly.
- Slop compounds over time: unread generated code reinforces bad patterns, making every subsequent generation strictly worse.
- Compounding tooling returns require shared adoption; scattered one-off skills never accumulate any meaningful team-wide engineering improvement.
- The single-process constraint eliminates network race conditions, letting queuing logic stay simple and fully deterministic locally.
- Time invested up front on the plan trades directly against your later probability of expensive backtracking.

### QUOTES
- "The more assumptions that you can bake in ahead of time and the more correct your design is, the more likely it is that your implementation will be correct." (Vaibhav)
- "Great leaders are right a lot ... when you are right, you move so much faster than any other competition because you don't have to go back and fix your mistakes." (Dexter)
- "Decisions take not a lot of time and have a lot of impact. Whereas execution can take a lot of time." (Vaibhav)
- "Plan files are throwaway." (Dexter)
- "As soon as it's shipped the code is the new source of truth." (Vaibhav)
- "If you want to know the truth read the code." (Dexter)
- "The models by default tend to want to do what I call horizontal planning." (Dexter)
- "You're basically Ralph Wiggum-ing your structure outline. You're just throw more tokens at the problem." (Vaibhav)
- "I actually one-shot the whole implementation. I never had to go edit this code again." (Dexter)
- "Keep your front end dumb. Keep your front end as dumb as possible." (Vaibhav)
- "Your codebase will always regress to the average of the best pattern and the worst pattern in the codebase." (Vaibhav)
- "One bad grep in your cloud code code research system is all it takes for your system to be bad." (Vaibhav)
- "Prune prune prune prune prune, that is the magic word." (Dexter)
- "You basically want to make decisions with the least amount of information." (Vaibhav)

### HABITS
- Kick off design jobs the morning before, then review the finished artifacts during the working session.
- Build a learning test whenever depending on a closed-source or poorly documented external library or SDK.
- Never check design or research docs into the repo; archive and forget them after merging code.
- Read the structured outline carefully rather than skimming every line of the full generated plan doc.
- Repeatedly prompt what's inconsistent or missing, discussing each surfaced design decision individually before updating the outline.
- Send complex design discussions to the codebase owner before implementing, not after finally opening the PR.
- Auto-advance through research loops; reserve scarce manual attention for the single high-stakes architecture decision gate only.
- Use Storybook to carve off the UI decisions the agent cannot develop good taste on itself.
- Run CodeRabbit CI to catch the bugs a one-shot implementation inevitably still leaves behind in code.

### FACTS
- The Claude Agent SDK's wrappers are open source, but the underlying Claude Code binary is minified.
- Dexter's proto migration PR added seventeen thousand lines and removed thirteen thousand across the entire codebase.
- That refactor took roughly eighteen separate commits spanning from two weeks down to five days ago.
- Riptide, the HumanLayer IDE, is closed source with an open public waitlist, working title still TBD.
- Riptide's message-queuing feature is built on the Claude Agent SDK's async prompting and session state machine.
- AI That Works airs live every Tuesday, co-hosted by Vaibhav of BoundaryML and Dexter of HumanLayer.
- The queuing architecture stores messages in a database that a daemon relays to Claude Code sessions.
- Local inter-process message delay is roughly one to two milliseconds, far below any network round-trip latency.

### REFERENCES
- AI That Works (weekly Tuesday podcast by BoundaryML), "No Vibes Allowed" live-build segment.
- BAML (BoundaryML) programming language for building AI pipelines.
- HumanLayer, and its IDE Riptide / "code layer" (working title TBD).
- Claude Code and the Claude Agent SDK (async prompting, bypass permissions, session state machine).
- The create-design-discussion skill.
- CodeRabbit (CI code review); Storybook (UI component development); Linear (issue tracking, autolink).
- Prior episodes referenced: interruptible agents / message queuing; agentic back pressure.
- Amazon leadership principle "Leaders are right a lot"; Google design-doc practice.
- The "Ralph Wiggum" iteration loop meme.
- Next episode teaser: PII redaction, designing the eval side and code side.

### ONE-SENTENCE TAKEAWAY
Front-load correctness into cheap design artifacts so implementation one-shots, because backtracking is coding's costliest move.

### RECOMMENDATIONS
- Before implementing against an opaque SDK, write a learning test asserting on its real message output.
- Restructure any horizontal, layer-by-layer plan into thin vertical slices you can test after every single phase.
- Iterate the design doc until fully aligned before coding; never rewind a costly half-built implementation instead.
- Actually read the whole plan; catching one wrong architectural decision saves you days of downstream rework.
- Run the what's-inconsistent-or-missing loop repeatedly on your structured outline until it stops surfacing any new gaps.
- Prune your team's skills to the five or seven everyone actually uses and actively maintains weekly.
- For V2 migrations, prefer a fresh package and verify the design doc recorded that critical decision.
- Design a preference-based API where the backend resolves queue, continue, or interrupt to the correct state.
