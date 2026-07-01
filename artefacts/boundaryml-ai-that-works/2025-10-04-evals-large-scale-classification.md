---
title: "Evals for large scale classification #24"
videoId: 5Fy0hBzyduU
url: https://www.youtube.com/watch?v=5Fy0hBzyduU
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works
---

## The one idea worth a video

**Spine 1 (the pipeline is free, the eval view is the work): stage your AI task into narrowing filters with a breakpoint at each stage, then build a dense visual eval harness that shows exactly which stage lost the right answer.**
Why it is the spine: it subsumes the whole architecture beat (embeddings to 100, LLM to 50, LLM select), the "add intermediate steps to get more knobs" idea, and the JSON to tree to table UI evolution. Building the classifier took Kevin a couple of hours; nailing the eval view took days, and that is where every decision came from.
VERDICT: net-new video available.

**Spine 2 (your evals are lying to you): before you touch a prompt, read every failure by hand, because most "wrong" answers are subjective ground-truth disagreements, and the fix is redefining what correct means, not the model.**
Why it is the spine: it stands on its own altitude (Route B). It reframes an aggregate 79% accuracy number as a problem-specification problem, and it drives distinct moves (lenient scoring dropdown, ground-truth-as-array, "did you mean" secondary category) that a pipeline-architecture video would never film.
VERDICT: net-new video available.

**Spine 3 (a two-tier codebase): treat the eval harness and UI as permanent throwaway scaffolding you vibe-code freely, keep only the core pipeline production-grade, and for un-testable visual work flip research-plan-implement into plan-implement-research.**
Why it is the spine: it is the explicit "how we actually built this" workflow beat (Vibhav: "vibe code the UIs, the evals, the testing harness, but keep the core code good"; Dex: RPI does not work for visual work). It is the next step beyond the school's existing throwaway-prototype lesson.
VERDICT: next-step (complement) video available.

---

## Summary

AI That Works episode 24: Vibhav, Dex, and Kevin dissect a production hardware-store classification pipeline, its staged narrowing, and the visual eval harness debugging it.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: The pipeline is free, the eval view is the real engineering

The claim: once you stage a classification task into narrowing filters (embed 1,400 down to 100, LLM down to 50, LLM selects one) with a probe at each boundary, the scarce skill is not building the pipeline but rendering its results so densely that the failing stage jumps off the page. What most people get wrong is treating the pipeline as the deliverable: as Kevin put it, "anyone here on the call could probably build this within a week," and Vibhav agreed it is "almost free." The mechanism is a two-step chain. First, each breakpoint turns one opaque wrong answer into a locatable failure: you can see whether the correct category dropped out at embedding, at LLM filter, or at final selection. Second, that per-stage attribution is only usable if the display is dense enough to act on, which is why the JSON blob and the NetworkX tree both failed (the tree "collapsed at 100 and you cannot command-F it") and the sortable table with one column per stage won. This generalizes cleanly to routing thousands of MCP tools: a tool call is a classification, and the same narrow-then-select staging applies. It goes wrong when you add vanity columns: Kevin's latency column was pure distraction because "you will not make a different decision" from it.

### Spine 2: Your evals are lying to you, so read every case

The claim: an aggregate accuracy score hides that "correctness" is a product decision, not a fact, and only case-by-case review reveals that most failures are subjective disagreements or polluted ground truth, not model errors. The default this argues against is the engineer's instinct that "this has all the information I need, so why look case by case?" The mechanism: when Kevin opened individual failures, the pipeline had picked "gas ranges" where ground truth said "double oven gas ranges", and the panel spent twenty minutes realizing either answer is fine depending on the product's UX. Switching to a lenient definition (right subtree, one level off is acceptable) moved measured accuracy from 79% to 85% without touching a prompt. Going further, "if we looked at 100% of the failure cases, all of them are actually not failures. It is a problem-specification problem." The generalization is direct to conversational chatbot evals: you cannot score them zero-or-one, so you tie them to an end business metric (copy-paste rate, returns) and spot-check. It goes wrong when leniency hides real regressions, so the scoring definition itself becomes something you must review and defend.

### Spine 3: A two-tier codebase, and flipping RPI for visual work

The claim: the eval harness, the UI, and the notebooks are permanent throwaway scaffolding you should vibe-code freely, while only the core pipeline earns production-grade discipline, and for visual work the usual research-plan-implement order fails. Vibhav is explicit: "make sure your core code is good and vibe code the rest, vibe code the UIs, the evals, the testing harness, but do vibe code them, do not skip those parts." The mechanism has two parts. First, the harness never reaches customers, so its only jobs are running fast and being adaptable by Claude Code, which means it can stay scrappy like a Jupyter cell you delete on ship. Second, deterministic tests cannot validate whether a UI "makes the signal jump off the page," so Dex reorders the loop: plan, implement, then research, iterating loosely by screenshot until it looks right, then handing that screenshot to an expert to rebuild production-grade. This generalizes to any hard-to-validate surface (a Streamlit dashboard, a Figma-substitute prototype). It goes wrong if the throwaway code quietly becomes load-bearing, or if you skip the harness entirely and only build the shippable app.

---

## 🎬 Proposed ACS videos

### 1. Build an AI Pipeline You Can Actually Debug

TITLE: Build an AI Pipeline You Can Actually Debug
HOOK: The classifier took two hours. The dashboard that told us what to fix took two days, and that was the real work.
THE PROMISE: For anyone shipping an LLM classification or routing task, you will leave able to stage your pipeline with probes and build a dense eval view that points at the exact stage to fix.
THE SHAPE:
1. Stage the task: embeddings narrow 1,400 to 100, an LLM narrows to 50, a final LLM selects one, with a probe at every boundary.
2. Add an intermediate "beef up the categories" step to show how new breakpoints create new knobs to turn.
3. Show the failed displays first: raw JSON, then a NetworkX tree that collapses at 100 categories and cannot be searched.
4. Build the winning sortable table, one column per stage, and watch the failing stage sort to the top.
5. Delete the latency column on camera to make the point that a dashboard shows only what changes a decision.
SPINE: 1
SLOT: Context Engineering (new chapter: Evals and Observability) or Techniques
RELATIONSHIP: ❌ net-new. The catalog has no evals, classification, or eval-dashboard video. Closest neighbour is Techniques "closing-the-loop", which gives the agent a test-based feedback loop; this is the inverse, giving the human a visual feedback loop over a probabilistic pipeline.
PROOF TO REUSE: the 1,400-to-100-to-50-to-1 hardware-store pipeline; "there is a lot of breakpoints or probes"; the NetworkX-tree-does-not-scale demo; "metrics you will not act on are just distracting."

### 2. Your Evals Are Lying to You

TITLE: Your Evals Are Lying to You
HOOK: The system scored 79%. Then we read every failure and found almost none of them were actually failures.
THE PROMISE: For anyone who trusts an eval number, you will leave knowing to read failures by hand, spot polluted ground truth, and fix the scoring definition instead of the prompt.
THE SHAPE:
1. Open the aggregate view: 79% correct, and resist the urge to go tune the prompt.
2. Drop into the test-case view and walk a "wrong" answer where general-versus-specific was genuinely ambiguous.
3. Flip the lenient-correctness dropdown live and watch accuracy jump to 85% with zero prompt changes.
4. Show a case where the ground truth itself was wrong, labelled by non-experts, and reframe it as a specification problem.
5. Make the fix an eval change plus a UI change: ground truth becomes an array, and the product surfaces a "you might have also meant this" secondary category.
SPINE: 2
SLOT: Context Engineering (new chapter: Evals and Observability) or Prompt Engineering (error analysis)
RELATIONSHIP: ❌ net-new. Nothing in the catalog covers error analysis, subjective ground truth, or scoring-definition design. It is a distinct lesson from Spine 1: that video builds the view, this one teaches what to distrust when you read it.
PROOF TO REUSE: "gas ranges" versus "double oven gas ranges"; the 79%-to-85% lenient flip; "a problem-specification problem much more so than a failure"; "sometimes the source of truth is not a source of truth."

### 3. Two Tiers of Code: Production Core, Throwaway Everything Else

TITLE: Two Tiers of Code: Production Core, Throwaway Everything Else
HOOK: Vibe-code the evals, the UI, the whole harness. Just never let the throwaway code touch what ships.
THE PROMISE: For engineers building AI systems, you will leave knowing which code to keep production-grade, which to treat as disposable scaffolding, and how to build visual tools an agent cannot test.
THE SHAPE:
1. Draw the line: the core pipeline is production code; the eval harness, UI, and notebooks are throwaway scaffolding you vibe-code and delete on ship.
2. Show why the harness only needs to run fast and be Claude-adaptable, not be clean, like a Jupyter cell.
3. Explain why research-plan-implement fails for visual work: there is no deterministic test for "does this dashboard read well."
4. Demo the flip: plan, implement, then research, iterating loosely by screenshot until it looks right.
5. Hand the screenshot to an expert (or a fresh production build) to turn the scrappy version into the real thing.
SPINE: 3
SLOT: Techniques (chapter: The First Build Is a Prototype)
RELATIONSHIP: 🔗 complements "build-it-twice" (Techniques). That video teaches that the first build of a feature is a throwaway prototype you rebuild from the learnings, reset not refactor. This is the next step beyond it: some code is permanently two-tier (throwaway harness around a production core), and the plan-implement-research reorder is the specific workflow for un-testable visual surfaces that build-it-twice does not cover.
PROOF TO REUSE: "vibe code the UIs, the evals, the testing harness, but do vibe code them"; "you do not know the right thing to build until you build the wrong thing"; Dex's plan-implement-research reorder; "the best way to lint a Jupyter notebook is to run it."

---

## 📚 Full wisdom (reference)

### SUMMARY
AI That Works episode 24: Vibhav, Dex, and Kevin dissect a production hardware-store classification pipeline, its staged narrowing, and the visual eval harness debugging it.

### IDEAS
- Classify 1,400 categories by narrowing through staged filters: embeddings to 100, LLM to 50, then select.
- Each pipeline stage is a breakpoint showing exactly where the correct answer dropped out of contention.
- Naive single-LLM approaches give few levers; adding intermediate stages multiplies the knobs you can actually turn.
- Insert an intermediate step that rewrites terse categories into descriptive paragraphs before the LLM narrows them.
- Building the pipeline is nearly free now; ingesting results into actionable signal is the hard part.
- The eval UI evolved from raw JSON to a NetworkX tree to a final sortable table.
- Tree-and-node graphs looked cool at 20 categories but collapsed at 100, and were unsearchable by command-F.
- A sortable table with one column per filter stage packs the same information far more densely.
- Removing the latency column mattered: metrics you won't act on are distraction, not diligence, on dashboards.
- Case-by-case review revealed most 'failures' were subjective disagreements over general-versus-specific categories, rather than real system errors.
- A lenient correctness definition (right subtree, one level off) jumped measured accuracy from 79% to 85%.
- Digging into every failure case showed the ground truth itself was polluted by non-expert human labelers.
- Fix the eval definition, not just the prompt: make ground truth an array of acceptable answers.
- Upgrading from GPT-4o to GPT-5 barely moved accuracy; the categories, not the model, were the bottleneck.
- Kevin built the whole system in roughly two days, mostly Claude-coded: pipeline hours, eval UI longest.
- Tool-calling with thousands of MCP tools is classification: narrow candidates before asking the model to choose.
- Start with 20 categories, not 1,400: shrink the problem first so the iteration loop stays fast.

### INSIGHTS
- Breakpoints between pipeline stages convert an opaque wrong answer into a locatable, fixable, single-stage failure you see.
- The scarce skill is not building pipelines but displaying results so the next action is obvious.
- Eval dashboards should show only decision-relevant data; latency and other vanity metrics actively obscure the signal.
- Correctness is a product decision, not a fixed fact; scoring definitions should encode acceptable user outcomes.
- Aggregate metrics hide subjectivity; only case-by-case review reveals that many failures are specification disagreements, not bugs.
- When a model swap doesn't help, the bottleneck is your data or definitions, not raw intelligence.
- Eval and UI harness code is throwaway scaffolding; only the core pipeline needs production-grade quality maintained.
- For visual work, research-plan-implement fails; iterate loosely to learn the target, then rebuild it properly afterward.
- Shrinking the problem to 20 categories buys a fast iteration loop before any UI complexity matters.
- Tie ambiguous evals to an end business metric; without one you cannot converge on anything meaningful.

### QUOTES
- "Building this pipeline is not hard. What's hard [is] figuring out how to ingest the information in a way that's helpful and tells you what to do." (host)
- "The real art and engineering comes into figuring out what gives me the information I care about in the densest way that makes it jump right off the page." (Kevin)
- "You don't always know the right thing to build to visualize it until you build the wrong thing." (Kevin)
- "[The latency numbers] shouldn't be here at all. It's just honestly it's just distracting." (Kevin)
- "If we actually looked at 100% of the failure cases, all of them are actually not failures. It's a problem specification problem much more so than a failure." (Vibhav)
- "Sometimes the actual source of truth is not a source of a truth as you think it is." (host)
- "Make sure your core code is good and vibe code the rest of it. Vibe code the UIs, vibe code the evals, vibe code the testing harness. But do vibe code them. Don't skip those parts." (Vibhav)
- "The most important thing you have to think about is actually not finances. It's actually not latency. It's can you make it work?" (Vibhav)
- "A tool call is the same as a classification." (host)
- "The best way to lint a Jupyter notebook is actually to run it." (Vibhav)

### HABITS
- Always show the final result first, then work backwards to explain how you actually got there.
- Look at the raw data first, because inspecting individual cases is always the clearest starting point.
- Throw away notebook-style eval UIs, like Jupyter cells, once the finished project actually ships into production.
- Use Streamlit over React for internal eval UIs when you know Python and iteration speed matters.
- Roast the prompt: have a colleague with strong LLM intuition critique it almost token by token.
- Always collect real representative data from actual users, not merely synthetic or family-generated sample search queries.
- Spot-check chat logs repeatedly before building formal evals, and tie every check to real business metrics.
- Grow the problem along two dimensions in parallel: more rules and more data, stepping up gradually.

### FACTS
- The example used over 1,400 hardware-store categories, resembling those found on lowes.com or homedepot.com online today.
- Medical billing uses ICD codes with roughly 80,000 entries, including separate codes for each individual toe.
- Adding a full GitHub MCP server's tools can consume 60,000 tokens of tool definitions, tanking performance.
- Marty Cagan's book 'Inspired,' from roughly twenty years ago, codified modern product management around learning fast.
- Replit's agent is reportedly used as a product-management tool to prototype and validate real customer demand.
- E-commerce search categorization has been researched for many years, including one older paper cited from 2020.
- The original AI That Works classification episode aired March 31st, covering schemas, embeddings, and RAG probes.
- Jupyter notebooks have no linter; the only reliable way to check one is to run it.
- The panelists estimate these e-commerce classification problems are worth hundreds of millions of dollars to retailers.

### REFERENCES
- BAML (BoundaryML) programming language; the BAML/family test CLI run via uvx ("llm-cli-test", "family cli test").
- HumanLayer (Dex's company); Evolution IQ (Kevin's employer, claims-guidance systems for disability and personal insurance).
- AI That Works show; the March 31st first classification episode; episode 5 on evals; the "policy to prompts" episode; the voice-agent episode.
- Tools and libraries: Streamlit, NetworkX, Matplotlib, React, Jupyter notebooks, Playwright, ML Flow.
- Models and APIs: GPT-4o, GPT-4o mini, GPT-5, GPT-5 mini, o3, GPT-5 max thinking, OpenAI Responses API.
- Coding agents: Claude Code, Cursor, Cursor's new CLI.
- Marty Cagan, "Inspired" (book); Amjad Masad and Replit / Replit agent (via Lenny's Podcast, roughly nine months ago).
- Jeff Huntley (talk on GitHub MCP tool bloat); a 2020 e-commerce search paper (shared by Nick); a Hacker News post on an MCP server injecting thousands of tools with narrowing.
- ICD medical billing codes; lowes.com, homedepot.com, Amazon; Riverside; Discord.

### ONE-SENTENCE TAKEAWAY
Building AI pipelines is cheap; the real work is dense evals revealing what to change.

### RECOMMENDATIONS
- Add intermediate breakpoints to your classification pipeline to see exactly where each wrong answer drops out.
- Build a sortable eval table, one column per stage, instead of tree diagrams that don't scale.
- Strip every metric from your dashboard that won't change a decision, including those tempting latency numbers.
- Before fixing prompts, read every failure case to check whether your ground truth itself is wrong.
- Make your ground truth an array of acceptable answers when categories legitimately overlap or nest inside.
- Add adjustable correctness definitions like strict and lenient so you can score by real user impact.
- Ship the shortest path that works first, then engineer down cost and latency only once needed.
- Vibe-code the eval harness and disposable UI freely, but keep the core pipeline production-grade and clean.
- For hard-to-validate visual work, iterate loosely first, then hand the resulting screenshot to an expert engineer.
- Collect real user data behind a feature flag rather than delaying launch to train models upfront.
