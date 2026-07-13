---
tags: [decision-surfaces, agentic-coding, meta, hci]
aliases: [Rich Decision Surfaces, Decision Surfaces]
date: 2026-07-10
---

*Fleshing out the "rich decision surfaces" idea: as models get better, the human becomes the bottleneck, and the quality of the interface where decisions get made becomes the quality ceiling of the whole system. Grounded in the 11-paradigm mockup sweep in `hyperwhisper-public/plans/mockups/`.*

> "The wrong way to understand a system is to talk about it, to describe it. The right way to understand it is to get in there and model it and explore it. And you can't do that in words."
> Bret Victor, The Humane Representation of Thought (2014)

## 1. The claim, stated precisely

Agentic coding has quietly inverted its bottleneck. It used to be generation: the model couldn't write the code, so the human's job was production. Now the model produces faster than the human can judge, so the scarce resource is **decision throughput**: how many high-stakes judgments per hour you can make *without degrading their quality*. Taste, product sense, and "is this what I actually meant" are exactly the things that stay human longest, because they are preferences, not capabilities. A model can get better at inferring your taste, but it cannot own it.

So the leverage point is no longer the model or the harness. It is the **decision surface**: the artifact the model hands you at the moment it needs a judgment. If that artifact is a 400-line markdown plan, you skim it, feel vaguely informed, and type "looks good." The decision got made, but not by you; it got made by whatever the model defaulted to in the parts you didn't really read. That is the failure mode this whole idea attacks: **approval without comprehension**.

The human-factors literature has a name for the role you're drifting into: supervisory control. Operators who monitor mostly-autonomous systems reliably develop automation complacency; the better the system, the worse the vigilance. Aviation solved this not with willpower but with instruments: cockpits, checklists, and displays engineered so that the state of the system is *perceivable at a glance* and anomalies pop out. That is the correct frame. You are not "reading plans," you are instrument-rating your own cockpit.

## 2. Why prose fails as a decision surface

A markdown plan fails for structural reasons, not laziness:

- **Serial access.** Prose forces one reading order. You can't get the gestalt first and drill in second; you must traverse.
- **Structure is described, not shown.** "There are two branches, cloud and BYOK, which rejoin at the keyboard step" is a sentence you parse and reconstruct mentally. Drawn as two colored lanes that fork and rejoin, the same fact costs zero effort and is impossible to misread.
- **Decisions are buried inside exposition.** The 5 things the model actually needs from you sit interleaved with 40 things it already decided. Nothing distinguishes "FYI" from "your call."
- **No write-back channel.** Even when you do spot a problem, your feedback re-enters the loop as more prose, lossy and unanchored to the thing it critiques.

Notice that all four failures are properties of the *medium*, and none of them improve as models improve. That matters for the [[bitter-lesson-harness-audit]] test: is this structure compensating for a model limitation (depreciating, delete it later) or for a durable requirement? Decision surfaces compensate for a **human** limitation: fixed reading speed, fixed working memory, vision system optimized for spatial pattern-matching over text parsing. Humans do not scale with compute. This is one of the few places where investing in elaborate scaffolding is *not* a bet against model progress; it is the piece that stays load-bearing at every capability level short of full autonomy, and it is precisely what makes higher autonomy safe to grant.

## 3. What the mockup sweep already proved

The `ios-onboarding-redesign` folder is more interesting than any single file in it: eleven paradigms of the *same plan* (linear storyboard, blueprint, review board, dual-lane, diff explorer, canvas, scrollytelling, simulator, RFC, deck, metro map). That is a design-space sweep of decision-surface formats, the same move as thumbnail A/B testing pointed at your own tooling. Worth keeping as a standing method: when a surface underperforms, fork the paradigm, not the content.

What the three inspected versions showed:

- **v1 (linear storyboard)** is a presentation. Good first read, but it enforces sequential thinking, branches stay implicit, and you can never see the whole plan at once.
- **v4 (dual-lane)** adds rigor: UI, frontend diffs, and backend diagram as parallel lanes, plus a cumulative "component ledger" of every file touched. But it needs a huge monitor, and branching still lives in your head. This is the "Dolaney" readability failure: density without spatial structure just moves the skimming problem around.
- **v6 (canvas)** is the phase change. One 6800x4550 world, pan/zoom, fit-to-view. Branches are geometry: the cloud lane and BYOK lane visibly fork and rejoin, the skip path is a labeled dashed arc you cannot miss. Colored zones chunk the world ("TODAY: THE DEAD END" in red, the changeset in slate). A minimap kills disorientation. Double-click drops a sticky note *at the location it critiques*, with resolve/delete states and a Copy JSON export.

The generalizable grammar hiding in v6:

1. **Whole before parts.** Fit-to-view gives the gestalt in one glance; zoom is the drill-down. Overview first, detail on demand.
2. **Spatial encoding of structure.** Forks, rejoins, skips, and groupings rendered as geometry and color, not sentences.
3. **Zones as chunking.** Labeled background regions carry meaning persistently, even mid-pan.
4. **Multi-speed navigation.** Arrow keys for sequential reviewers, number-key jumps for targeted ones, pan/zoom for explorers, F for the big picture. One surface, several cognitive modes.
5. **Annotations are spatial and exportable.** A sticky pinned to card 5 is worth ten lines of chat feedback, because position *is* the reference.
6. **An embedded machine-readable spec**, so the artifact itself can be re-ingested by a fresh session and iteration continues without re-explaining.

And what v6 still lacks defines the roadmap: no persistence (reload wipes stickies), no freehand drawing, no automatic write-back (Copy JSON is manual), no multi-surface queue, mobile/tablet hostile.

## 4. Anatomy of a good decision surface

Beyond the canvas grammar, principles that should hold for *any* surface, not just plans:

- **Surface the decisions, not the document.** Open questions, options, and tradeoffs are first-class objects with affordances (approve, reject, pick A/B, annotate), visually distinct from everything the model already decided. The reviewer's job is triage, not archaeology.
- **Declare decision provenance.** Every element tagged: model-decided (glance and move on), model-recommends-but-flags (skim), needs-your-call (stop here). Without this tiering the conveyor belt becomes decision fatigue with prettier packaging.
- **Lossless round-trip.** Every annotation, sticky, stroke, and checkbox must flow back to the agent machine-readably and anchored to what it references. A surface without a write-back channel is a brochure.
- **Consistent grammar across surfaces.** If every plan renders in the same visual language (same zone colors, same wire semantics, same sticky mechanics), your eye trains on the format and per-surface comprehension cost drops toward zero. This is why cockpits are standardized.
- **Honest at every altitude.** A polished mockup manufactures false confidence; the render is not the implementation. Keep the "under the hood" strips and the changeset ledger so beauty never substitutes for truth.
- **Disposable to produce.** Surfaces are generated per decision and thrown away. The *grammar* is the asset; any individual artifact is not.

### Keeping the surface honest: verify by construction, then by cross-check

A wrong instrument is worse than no instrument, because you trust it. The map is not the territory, and a misdrawn wire on the canvas is a confident lie: you approve the plan the diagram shows, not the plan that exists. There are exactly two gaps where lies enter:

1. **Spec vs reality.** The embedded plan JSON claims something false about the code ("this screen already exists", "these branches rejoin here").
2. **Render vs spec.** The drawing misrepresents its own spec: a Mermaid edge missing, a wire pointing the wrong way, a zone containing the wrong cards.

Attack them differently. Gap 2 should be closed **by construction**: derive the render deterministically from the spec (spec is the single source of truth, wires and zones are compiled from it, never hand-drawn by the model in a second pass). What is generated from the spec cannot disagree with it. That collapses the problem to gap 1, which is where **cheap verifier agents** earn their keep: fan out one small agent per load-bearing claim in the spec, each grepping the codebase to confirm or refute it, plus optionally a vision pass that screenshots the rendered surface and diffs it against the spec as a belt-and-braces check on the compiler. Verified claims get a badge on the surface ("checked against `OnboardingView.swift:41`"); unverifiable claims get flagged as assertions. Pilots are taught instrument cross-check precisely because any single instrument can fail; the surface should wear its cross-check visibly.

The prior art for this is double-entry bookkeeping: a representation with a *built-in* verifier. Every transaction is written twice, and the books must balance; the redundancy is not waste, it is the error detector. A decision surface should have the same property: enough redundancy between spec, render, and reality that a lie shows up as an imbalance somewhere.

## 5. The maturity ladder

- **Stage 0: prose plan.** Where everyone starts. Skim-and-LGTM failure mode.
- **Stage 1: rich HTML artifact.** Storyboards, lanes, diffs. Done (artifact-planner).
- **Stage 2: spatial canvas with in-place annotation.** v6, plus the artifact-planner-canvas skill. Mostly done; missing persistence and automatic write-back.
- **Stage 3: the annotate-and-return loop.** The surface becomes bidirectional. Serve the HTML from the session instead of a static file; stickies, checkboxes, and freehand ink POST to a JSON file the agent watches. Add a drawing layer (an embedded tldraw or Excalidraw canvas pinned to world coordinates) so an iPad + pencil works: circle a card, scrawl "no, three steps max," hit send. Ink that can't be parsed structurally gets screenshotted and read multimodally; models are already good at reading annotated screenshots. No app store, no native build: a local server plus a tablet browser gets 90% of the iPad-app vision this week.
- **Stage 4: mission control.** The conveyor belt. Multiple agents working in the background, each surfacing decision requests into a queue. You stand at a board of pending surfaces: zoom in, inspect, annotate, dispatch, next. Real-time in both directions: the agent re-renders as you draw. This is management-by-exception, and it is plausibly what senior engineering *is* once generation is free: an air-traffic controller whose instruments are decision surfaces.

The honest framing of stage 4: it is not a stepping stone to full autonomy that later gets deleted. Preferences never fully transfer. Even at very high autonomy, someone owns taste, and that person needs instruments.

## 6. Prior art worth stealing from

- **Code review** is the one decision surface software already perfected: the diff, inline comments anchored to lines, resolve states, approve/request-changes. The whole idea can be described as "generalize the PR review loop beyond code diffs to plans, designs, and strategies."
- **tldraw / Excalidraw** for the ink layer and canvas mechanics; tldraw's "Make Real" already demonstrated the draw-then-AI-ingests loop in reverse.
- **Figma comments** for spatial annotation with threads and resolution, multiplayer included.
- **Miro/FigJam** for zones, wires, and facilitation grammar.
- **Bret Victor** (Media for Thinking the Unthinkable, Dynamicland) for the underlying thesis: representations do the thinking; upgrade the representation and you upgrade the thinker.
- **Tufte**: small multiples for option comparison (your 11-paradigm sweep *is* a small-multiples move), data-ink ratio as a check on decorative canvas bloat.
- **Control-room and cockpit design** (ecological interface design): make system state perceivable, make anomalies pop out, standardize the instrument panel.

## 7. The lineage: representations that upgraded thinking

The Bret Victor point ("representations do the thinking") is not a metaphor; it is one of the most repeated patterns in intellectual history. Ken Iverson's Turing Award lecture was literally titled *Notation as a Tool of Thought*. The lineage worth keeping in your head:

- **Arabic numerals vs Roman.** Try long division in Roman numerals. The medieval merchants who adopted Hindu-Arabic notation didn't get smarter; their representation started doing the arithmetic's structural work for them. Whitehead: "By relieving the brain of all unnecessary work, a good notation sets it free to concentrate on more advanced problems."
- **Feynman diagrams.** Perturbation calculations that took Schwinger pages of algebra became pictures a graduate student could manipulate. Same physics, different surface, order-of-magnitude more practitioners able to make correct judgments. This is the target: plans that currently require a senior engineer's full attention becoming glanceable.
- **John Snow's cholera map and Nightingale's rose diagrams.** Decisions (remove the pump handle, reform army hospitals) made *by* a representation, where the same data as a table had persuaded no one. And Anscombe's quartet is the proof from the other side: four datasets with identical summary statistics and wildly different shapes. Some truths are literally invisible in text form.
- **Beck's London Underground map.** Geographically wrong on purpose. Beck realized riders decide *which line and where to change*, not *how far*, so he distorted toward the decision and threw away fidelity that didn't serve it. A decision surface should not mirror the system 1:1; it should distort toward the judgment being asked. (The v6 canvas making branch topology huge and code detail tiny is exactly Beck's move.)
- **The periodic table.** Mendeleev's arrangement made *gaps* visible; the representation predicted elements nobody had found. A good surface does the same for plans: the open-questions header is the row of gaps, and an empty zone should feel as loud as a filled one.
- **Double-entry bookkeeping.** The self-verifying representation (see section 4). Also the reason firms could scale: owners could *inspect state at a glance* instead of trusting narrative reports from below. That is precisely the multi-agent situation.
- **Hutchins' *Cognition in the Wild*.** A ship is navigated not by any one mind but by a cockpit of instruments, charts, and roles; the cognition lives in the system. Mission control for agents is this, deliberately built.
- **Programming's own history.** Assembler to high-level languages, printf to debuggers to flame graphs, and above all the **diff**: nobody reviews code by rereading both files. The entire craft keeps winning by inventing representations that make the relevant judgment cheap.

The common shape: the breakthrough is rarely new information, it is old information re-represented so the human perceptual system can do the work that deliberate reasoning was straining at. Chess masters don't calculate more than novices; they *see* more. The surface is how you buy that seeing.

## 8. What to build next, concretely

1. **Extract the v6 grammar into the canvas skill as a spec**, not an example: zones, wires, cards, stickies, provenance tags, embedded plan JSON. Every future plan renders in this one language, and the render is *compiled from* the spec so it cannot misdraw it.
2. **Add the fidelity pass**: after generation, fan out cheap verifier agents (one per load-bearing spec claim) to check the spec against the codebase, badge verified claims on the surface, and flag unverified assertions. Optionally a vision agent screenshots the render and diffs it against the spec.
3. **Add the write-back loop**: a tiny local server (or even a file-watcher on a JSON the page writes via a download shim) so "Copy JSON" becomes automatic. The session blocks on `decisions.json`, you annotate on any device on the LAN, the agent resumes with your annotations in context. This single step converts the artifact from brochure to instrument.
4. **Add a decision header to every surface**: N open questions, each with options and a recommended default, rendered as the first thing fit-to-view shows. Measure yourself: are you answering the questions, or scrolling past them?
5. **Then the ink layer** (embedded tldraw pane or stroke capture + screenshot ingestion), which unlocks the iPad workflow without a native app.
6. **Only after 2-5 work: the queue.** Multiple sessions publishing surfaces into one inbox page. Do not build mission control before the single-surface round-trip is proven, or you get a beautiful backlog of unmade decisions.

## 9. Tensions to keep in view

- **The surface can lie, two ways.** Aesthetically (polish manufactures confidence; enforce the under-the-hood strips) and factually (a misdrawn diagram is a confident falsehood; close it with render-by-construction plus the cheap-verifier fidelity pass from section 4).
- **Fatigue scales with queue depth, not surface quality.** Without provenance tiers and auto-approve thresholds for low-stakes calls, better surfaces just let agents generate decision debt faster than you can pay it.
- **Grammar lock-in.** The visual language should be versioned and pruned like any other harness structure; the *human-facing* purpose is durable, any *specific* encoding is not.
- **Latency.** A surface that takes 10 minutes to generate changes what it gets used for. Cheap-and-instant beats rich-and-slow for most decisions; keep a fast plain tier.
