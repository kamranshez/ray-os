---
title: Can an AI Out-Plan a Senior Engineer?
videoId: KCqsoXveqiI
url: https://www.youtube.com/watch?v=KCqsoXveqiI
date: 2026-07-01
status: posted
show: AI That Works (BoundaryML), Vaibhav (BAML) + Kevin Gregory (EvolutionIQ)
---

## The one idea worth a video

**Fight AI slop with slop: build throwaway, AI-generated internal tooling you never read, purely as scaffolding that makes your real deliverable (the design doc) high-quality.** It reframes internal tools from "code you own" to "means to an end," so the quality bar moves from the code to the workflow.
VERDICT: net-new video available.

**Make the model challenge your design: explicitly ask it what should be impossible but will actually happen, because LLMs are trained to trust you and will silently implement wrong assumptions.** It converts the model's agreeableness from a hidden failure mode into a design-time discovery tool.
VERDICT: net-new video available.

**For complex design docs, never edit in place: have the model rewrite a fresh V2 from scratch, because in-place edits degrade every time.** It is the "build it twice" thesis applied to documents, with its own mechanism (model editing degradation) and its own versioning discipline.
VERDICT: next-step video available (complements "Build It Twice").

The video's overarching frame, that design is where the work moved now that implementation one-shots, is already covered by "The Shifting Bottleneck" (start-here) and "Build It Twice" (techniques), so it is not pitched as its own new video.

## Summary

Boundary's Vaibhav and EvolutionIQ's Kevin show how they design complex features: build throwaway AI tooling, rewrite docs into clean V2s, and make models challenge assumptions.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1, Fight slop with slop.**
The claim: build disposable, AI-generated internal tooling you never read, purely to make your real deliverable easy to produce and review. Why it is non-obvious: most people apply their production code-quality bar to everything they build with AI, so they either avoid bespoke internal tools (too much effort) or agonize over the mess. The reframe is that internal, non-customer-facing tooling has a completely different bar: workflow-quality, not code-quality. Why it is true: because the tool is a means to an end, its correctness barely matters, only whether the workflow it enables is good. Since an agent can generate that tool in an afternoon and maintain it via Slack tags, the cost of bespoke tooling drops to near zero, which lets you shape tooling exactly around your real bottleneck (making design docs reviewable and in-sync). Better tooling then raises the quality of the actual deliverable. It generalizes to any internal glue: a data-cleaning script, a personal dashboard, a migration helper. How it goes wrong: the moment "internal" leaks to customers or becomes load-bearing infra, the slop bar becomes a liability, and debugging means "ask Claude" because nobody understands the code. As Vaibhav put it: "I don't even know what this code is. I don't care. Cuz this code is a means to an end."

**Spine 2, Make the model challenge your design.**
The claim: explicitly instruct the model to challenge what should be impossible in your design, because it defaults to trusting you and will implement wrong assumptions unquestioned. Why it is non-obvious: people treat the model as a code generator that just needs clear instructions, and miss that its compliance is itself the failure mode. It will not volunteer that your design is secretly impossible. Why it is true: LLMs are trained to assume the user holds context they lack and to be agreeable, so a stated assumption is treated as ground truth. That pushes the point where a design flaw surfaces to implementation time (expensive) instead of design time (cheap). Inviting adversarial pushback, "challenge what should not be possible but is going to actually be done here," moves discovery earlier. Kevin's concrete instance: a simple-sounding $5 cost-limit middleware forces thread-local storage underneath, a decision Vaibhav might never have surfaced alone. It generalizes to architecture reviews, security threat modeling, and product spec review, anywhere a confident human framing hides an unexamined constraint. How it goes wrong: the model can hallucinate objections or over-challenge trivial choices, so you still need taste to filter, and framing matters, "here's my thinking, what else?" beats a leading assertion.

**Spine 3, Rewrite complex docs into V2 instead of editing in place.**
The claim: for complex design docs, never let the model edit in place; have it write a fresh V2 from scratch, because in-place edits fail essentially every time. Why it is non-obvious: editing feels cheaper than rewriting (less to regenerate, preserves history), but that intuition is wrong for complex docs and models. Why it is true: a model editing a large doc behaves like a lazy human editor, making local patches without re-deriving global coherence, so contradictions and stale sections accumulate. Vaibhav claims 100% failure on complex docs. Rewriting forces the model to re-reason the whole structure, which is when it decides "the mental model is garbage, cut it," how the spawn doc shrank from 104KB to 62KB while getting clearer. This is the "Build It Twice" thesis applied to documents: "think about how much cleaner you would write it the second time." It generalizes to refactoring code, restructuring a README, or rewriting a messy migration, where the second pass is coherent because the shape is now known. How it goes wrong: you lose the review comment chain tied to V1 (hence their explicit versioning system), rewriting a huge doc costs tokens and time, and multiple versions in context confuse the model, so the active version must be isolated.

## 🎬 Proposed ACS videos

### 1. Fight Slop With Slop: Disposable Tools That Make Great Docs
- HOOK: The best way to produce a high-quality document is to build a garbage tool you will never read.
- THE PROMISE: For engineers who plan with AI, walk away able to spin up throwaway internal tooling that makes your real deliverable dramatically better.
- THE SHAPE: (1) The slop bar vs the ship bar. (2) Live-build a tiny CLI plus Claude skill that pulls and syncs your docs. (3) Never open the code, add features by tagging an agent in Slack. (4) Show how the tooling makes the doc reviewable, and that is the whole point. (5) When slop is a liability.
- SPINE: 1
- SLOT: Techniques class, new chapter "Scaffolding: Tools That Build Your Work"
- RELATIONSHIP: ❌ net-new. Adjacent to the filmed "Scrappy, Copy-First" technique, which teaches scrappy first drafts of the product; this is different, it is building disposable side-tooling around your real deliverable that you deliberately never read.
- PROOF TO REUSE: "This code is a means to an end." The open-source BEP dashboard plus BEP-pull Python CLI wrapped in a Claude skill. "I have never even opened Claude myself to add features into BEPs." Slack-as-notification-system instead of building notifications.

### 2. Make the Model Fight You: Surfacing the Design Decisions You Cannot See
- HOOK: The LLM will build exactly what you asked, even when what you asked is quietly impossible.
- THE PROMISE: For anyone designing systems with an agent, leave able to add one prompt move that surfaces hidden design decisions before they cost you an implementation.
- THE SHAPE: (1) Why models trust you by default and why that is dangerous. (2) The prompt: "challenge what should not be possible but will actually be done here." (3) Live demo: a $5 cost-limit that turns out to require thread-local storage. (4) The softer framing, "here's my thinking, what else?", and when to use each. (5) Filtering hallucinated objections with taste.
- SPINE: 2
- SLOT: Prompt Engineering class, new chapter "Make the Model Push Back"
- RELATIONSHIP: ❌ net-new. The "Clarifying Questions" correction has the model ask you questions; this is the inverse and stronger move, having the model adversarially attack your own stated design to expose constraints you did not know you assumed.
- PROOF TO REUSE: "LLMs will write every piece of code that you ask them to." Kevin: "it's going to assume you're correct because they've been trained to trust you." The cost-limit to thread-local-storage discovery. "I want you to challenge me with what should not be possible."

### 3. Rewrite, Do Not Edit: Why Agents Wreck In-Place Doc Edits
- HOOK: For a complex design doc, letting the model edit in place fails 100% of the time.
- THE PROMISE: For anyone maintaining living design docs with an agent, leave knowing exactly when to stop editing and force a clean V2 rewrite instead.
- THE SHAPE: (1) The lazy-editor failure mode, local patches, no global coherence. (2) Demo: same doc, edit-in-place vs fresh V2, watch coherence collapse then recover. (3) The 104KB to 62KB shrink that made the doc better, not worse. (4) Keeping versions on purpose, and why never exposing two versions to the model at once. (5) When editing is still fine (small, local docs).
- SPINE: 3
- SLOT: Techniques class, chapter "The First Build Is a Prototype" (alongside "Build It Twice")
- RELATIONSHIP: 🔗 complements "Build It Twice" by being its next step. "Build It Twice" teaches rebuilding code from scratch to buy knowledge; this applies the same coherence argument to documents, adds the model-specific in-place-edit degradation, and adds the versioning discipline (V2 files, never show the model multiple versions).
- PROOF TO REUSE: "Editing is a more hard exercise to be coherent in than rewriting from scratch." "For complicated design docs, I've seen this 100% of the time." "Models go nuts when they see multiple versions of something." The 104KB to 62KB reduction.

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's "AI That Works" (no-vibes-allowed) episode: Vaibhav (BAML language) and Kevin Gregory (EvolutionIQ) demo, live, how they design complex features using AI-built tooling and design docs.

### IDEAS
- Fight AI slop with slop: generate throwaway internal tools that make high-quality design documents really easy.
- Implementation is often one-shot when the design is phenomenally correct, but correct design is very hard.
- The Claude Code founder reportedly just perfects the plan, kicks it off, then starts another one.
- Hard problems split into four or five chunks that are each individually one-shot implementable after design.
- For complex design docs, models corrupt in-place edits every time; rewrite a fresh V2 from scratch.
- Editing is a harder exercise to stay coherent in than rewriting the whole thing from scratch.
- Ask the model to challenge what should be impossible in your design but will actually happen.
- A cost-limit middleware forced discovery that they needed thread-local storage, surfaced only by challenging the design.
- LLMs are trained to trust you, so they implement wrong assumptions unless you explicitly invite pushback.
- Build tooling so you never have to keep the whole design in your head at once.
- Structure design docs top-down: motivation, simplest form, then decisions, because models read them like humans do.
- Explicitly list what a design is NOT doing, so readers and models know its scope boundaries.
- Name folders with numbers plus names so an agent's LS reveals structure without reading any file.
- They record design-meeting Slack huddles, then paste the raw transcript into the model to reorganize docs.
- Move a doc from draft to proposed only after doing the legwork that guarantees it's readable.
- Frequent behaviors should be syntactically most convenient, without compromising correctness where correctness genuinely has to win.
- A Claude skill wraps a Python CLI that pulls BEP data and keeps local folders synced.
- They latched onto Slack as their notification system rather than building notifications into their own dashboard.

### INSIGHTS
- Since agents type the code, the human's real job becomes producing designs precise enough to one-shot.
- Slop tooling is fine precisely because it is internal and not customer-facing; the deliverable stays high-quality.
- Model in-place edits degrade like a lazy human editor; a full rewrite restores the global coherence.
- Building surfaces hidden design decisions earlier, so bugs get discovered during design rather than during implementation.
- Great engineers had better intuition; now AI research raises everyone's median design quality toward that intuition.
- The model surfaces prior art you'd never find, like .NET's Polly, enriching designs beyond your knowledge.
- Detailed worked examples in a design doc are where design bugs surface before expensive implementation begins.
- Versioning matters for both humans and agents, but exposing multiple versions simultaneously makes models go nuts.
- Small ergonomic tooling choices, like descriptive folder names, quietly steer an agent toward the correct behavior.
- You must be explicit teaching the model your learnings, or it invents its own possibly-wrong inferences.

### QUOTES
- "The real answer is build tooling so that you don't have to keep track of everything in your head.", Vaibhav
- "This is how you fight AI slop with slop.", Kevin
- "I worked to write this script. I don't even know what this code is. I don't care. Cuz this code is a means to an end.", Vaibhav
- "You generate slop code, don't really care what it does, as long as this workflow is good.", Vaibhav
- "Implementation can often be one shot if the design is phenomenally correct.", Vaibhav
- "Editing is a more hard exercise to be coherent in than rewriting from scratch.", Vaibhav
- "For complicated design docs, I've seen this 100% of the time.", Vaibhav
- "LLMs will write every piece of code that you ask them to.", Vaibhav
- "I want you to challenge me with what should not be possible in this design but is going to actually be done here.", Vaibhav
- "If you just tell the LLM something, it's going to assume you're correct because they've been trained to trust you.", Kevin
- "Now the job of hands-on keyboard typing code is kind of just been solved.", Kevin
- "Models go nuts when they see multiple versions of something.", chat question, read aloud

### HABITS
- They record every design meeting via Slack huddle transcription, then feed the transcript to the model.
- Vaibhav writes design docs and plans for almost all work now, roughly fifty percent of time.
- He creates a new V2 document rather than deleting V1, avoiding in-place edits on complex docs.
- He adds features to internal BEP tooling only by tagging coding agents in Slack, never manually.
- He asks Claude to check every implemented BEP for consistency instead of tracking it all mentally.
- He splits weak sections, like prior art, into dedicated subpages rather than bloating the main readme.
- He marks certain docs 'good for the LLM' so that new docs auto-pull them into context.
- He aggressively reduces doc verbosity, cutting one spawn spec from 104 kilobytes down to 62 kilobytes.

### FACTS
- EvolutionIQ, which builds disability insurance claims guidance systems, was acquired for around 730 million US dollars.
- BEP stands for BAML Enhancement Proposal, the mechanism for adding new features to the BAML language.
- Vaibhav spent almost four full days purely designing BAML's threading system before writing any actual code.
- The BAML BEP tooling is fully open source, living inside the BAML monorepo's own BEPs folder.
- The patterns BEP had seven versions, each one carrying its own comment chain and read-only history.
- Team members automatically join when their GitHub account carries a boundaryml email, unlocking elevated dashboard privileges.
- Async IO gives you concurrency, not parallelism, because it runs tasks interleaved on a single thread.
- Function coloring forces separate async and sync versions, propagating async upward through the entire call stack.
- Anyone can log into beps.boundaryml.com with a GitHub account and view Boundary's live in-progress design work.

### REFERENCES
- BAML programming language (BoundaryML / Boundary); BEPs (BAML Enhancement Proposals); beps.boundaryml.com
- BAML monorepo GitHub repo, BEPs folder (open source)
- "AI That Works" show, the monthly "no vibes allowed" live-coding episode
- EvolutionIQ (disability insurance claims guidance systems)
- Claude Code, Cursor, Claude skills
- Slack (huddles, threads, notifications), Granola (meeting transcription, broke mid-meeting)
- Google Drive / Google Docs (the "design.help" scattering problem)
- Async IO, function coloring; Go, Kotlin, Python, TypeScript, CPython, V8 (coroutines, virtual/OS threads)
- Go context/CTX cancellation, TypeScript AbortController, .NET Polly, Express middleware, Python decorators
- AI Engineer conference talk (fighting slop with slop, upcoming on YouTube)
- People: Akai (date-time BEP), Antonio, Aaron, Sam, Dex (prior episode)

### ONE-SENTENCE TAKEAWAY
Spend your effort designing; build disposable AI tooling and rewrite docs so agents one-shot implementation.

### RECOMMENDATIONS
- Build small throwaway internal tools with AI to make reviewing and sharing your design docs frictionless.
- When editing a complex doc fails, delete nothing; have the model write a fresh V2 instead.
- Add a prompt line asking the model to challenge what should be impossible in your design.
- Frame proposals as 'here's my thinking, what other ideas exist' rather than asserting your solution confidently.
- Write design docs top-down: motivation first, simplest example next, design decisions after, prior art in subpages.
- Name numbered folders with descriptive suffixes so that an agent's LS conveys structure before reading files.
- Explicitly document what a design excludes, listing out-of-scope items clearly so readers understand your deliberate boundaries.
- Record your design meetings, transcribe them, and paste the transcript in to reorganize the document's outline.
- Ask the model to research prior art from languages you don't know before finalizing a design.
