---
tags: [agentic-coding-school, research, planning, context-engineering, program-design]
aliases: [WSFF Planning Pipeline, Dex Horthy Planning Deep Dive, Call Graph Planning]
date: 2026-07-23
source: "Dex Horthy, 'Harness Engineering Is Not Enough / Why Software Factories Fail' (AI Engineer World's Fair 2026 keynote) + 4-agent research sweep"
---

> Deep-dive on the planning pipeline from Dex Horthy's AIE World's Fair 2026 keynote: **product review, system architecture, program design, vertical slices**, plus the call-graph planning technique he cites from Dillon Mulroy. Built 2026-07-23 from a 4-agent research sweep (Dex/HumanLayer lineage, Dillon Mulroy call graphs, vertical slices history, program design discipline).

## TLDR

The talk's four planning docs are not four random artifacts. They are the same alignment work cut by **altitude**: product space (what and why), system space (how services talk), program space (the shape of the code), and time (what order, with what checks). The load-bearing claim underneath all of it: **maintainability is the one objective RL cannot reward**, because its cost function is measured in months, so no amount of harness engineering fixes it and humans have to inject design judgment upstream where it is cheapest. The most teachable single artifact in the whole space is Dillon Mulroy's call-graph plan, and we recovered his entire working session, including the exact prompt that produces it.

Key primary source: the talk is a living essay, `wsff.md` in the ACE-FCA repo (710 lines, currently flagged `PRE RELEASE - please don't share or post just yet -dex`). Full text preserved in `artefacts/wsff-planning-pipeline-sources/` alongside the ACE-FCA essay, the three HumanLayer prompts, and Dillon Mulroy's recovered session extracts; talk video at hlyr.dev/wsff-live. **Do not quote wsff.md publicly yet**; the talk itself is public.

## The thesis chain (why planning, not harnesses)

1. Coding models are RL-trained on SWE-bench-shaped tasks: binary reward for "did the hidden tests pass without breaking the old ones" (he walks through real task `fastlane__fastlane-19304`).
2. Verbatim: "there is no penalty for eroding codebase maintainability." Tests give feedback in seconds; "the cost function of bad architecture is measured in weeks, months, maybe even years." The reward signal cannot propagate back across that gap.
3. "If a model could reliably tell good code from bad, it might have written the good version to begin with, but maintainability has no fast oracle, so we can't reward for it during RL." LLM judges only raise the floor.
4. Claude Code won because "Anthropic RL'd the model inside the harness" - which is exactly why harness engineering alone cannot save third parties: the shortcoming is in the weights.
5. HumanLayer's own receipts: they went lights-off in July 2025. By the ~3rd incident in November, cofounder spent **two weeks typing every character by hand in VS Code** rebuilding the bones. Dex's public recantation (Qodo podcast): "In August we were like, stop reading the code... let the model cook... This code is terrible, and it's really hard to work in."
6. His redefinition of brownfield: "an agent-built codebase starts to struggle after maybe three to six months."
7. Empirical backup now exists: **SlopCodeBench** (arXiv 2603.24755) shows code erosion rises in 80% of agent trajectories and, crucially, "prompt-side interventions shift the intercept but not the slope" - anti-slop and plan-first prompts improve initial quality but degradation resumes at the same rate. That is the proof of "you can't prompt your way out of a training issue."

Closing advice verbatim: "1. Learn the constraints well. 2. Optimize systems within the arena of these constraints. 3. Seek leverage. 4. Read the dang code."

## How the pipeline evolved (context for everything below)

| Date | Artifact | State |
|---|---|---|
| Apr 2025 | 12-Factor Agents | Foundations: own your context (F3), own your control flow (F8) |
| Aug 2025 | ACE-FCA / "No Vibes Allowed" (601K views) | Research, Plan, Implement (RPI); "frequent intentional compaction"; "read the plans, not the code" |
| Mar 2026 | "Everything We Got Wrong About RPI" | RPI breaks at scale; split into CRISPY stages; "please please read the code" |
| Jun/Jul 2026 | WSFF keynote (the talk you watched) | The 4-doc pipeline: Product Review, System Architecture, Program Design, Vertical Slices |

Why RPI broke (the CRISPY talk, worth knowing because it explains the 4-doc split):

- **Instruction budget**: frontier models follow only ~150-200 instructions consistently; their `create_plan.md` monolith had 85+, so alignment steps got probabilistically skipped ~half the time.
- **Magic words**: users needed incantations to make plan mode interactive; "if a tool requires magic words for basic functionality, the tool itself is broken."
- **Plan-reading illusion**: "a thousand line plan tends to be about a thousand lines of code within 10% or so... this isn't leverage."

The fix was 12-Factor F8 applied to the workflow itself: many small stages, each under ~40 instructions: Questions, Research, Design, Structure, Plan, Implement, PR ("CRISPY"). The WSFF 4-doc pipeline is CRISPY's alignment stages re-cut by altitude rather than workflow step. Two mechanics worth stealing regardless:

- The **Questions stage hides the feature ticket from research** so research stays objective (documentarian, not advocate).
- The **Design discussion (~200 lines)** is where "you can do brain surgery on the agent before you proceed downstream" - and where he sends docs to his cofounder: "any of my bad decisions are headed off on a 200-line doc before I've gone and written the code and gotten it working and I'm attached to it."

The leverage ladder from ACE-FCA is still the best one-line justification: **"A bad line of code is a bad line of code. But a bad line of a plan could lead to hundreds of bad lines of code. And a bad line of research could land you with thousands of bad lines of code."**

## Phase 1: Product Review

A short doc pinning down what and why: "take two sentences or a long voice note ramble and turn it into something semi-structured."

- **Problem to solve**: the actual user pain, in the user's terms.
- **What success looks like**: "what can we read after shipping to decide the thing was worth building" (user outcome > error rate > "the support tickets about X stop").
- **Mockups over prose**: "I don't describe it - I mock it up. A rough HTML mockup of the actual screen settles an argument that three paragraphs would only prolong."
- Stay in product space; tech thoughts get jotted for later phases. If tech genuinely blocks product, commit what you have and go do prototype research.
- Review mechanic: author-opt-in reviews - you pick the person who would review the PR and walk them through the product/tech specs, async doc comments.

**Task-size routing (the 80/20)**: "~40% of tasks get oneshot or oneshot w/ 1-2 rounds of light feedback; for medium tasks, we do product/system design all in one plan document; for large things, we do all the steps." Copy tweaks, one-off scripts, obvious bugs: still just oneshot.

## Phase 2: System Architecture

"How the services, endpoints, schemas, queues, and stores talk to each other, without getting into the details of program design." Doc shapes he actually ships:

- Mermaid **sequence diagrams**
- **Contract/endpoint shapes** (literal `PUT /api/resources/:slug` request/response)
- **Data models as literal `CREATE TABLE` SQL** plus new query shapes

His own caveat: "Mermaid is fine here but it can sometimes be overkill and sometimes lure you into a false sense that you are aligned... it is insufficient to produce high-quality code." That insufficiency is exactly why phase 3 exists.

## Phase 3: Program Design (the underemphasized one)

"Most people assume that once the architecture is right, the model can just cook. You can go ahead and do this, but you might not like what you get back." Go one level down from architecture into the **shape of code**: types, method signatures, program layout, call stacks. Their first program-design skill "sucked... exhausting"; what they landed on is **light visualizations in pseudocode**:

1. **Call-stack trees** with diff syntax (`+ handleCreateResource` / `- legacyCreateFlow`) - credits Dillon Mulroy directly
2. **File-tree diffs** (`+ resource-client.ts # NEW`, `~ resource-route.ts # MODIFIED`) - "stay in touch with the layout of your codebase"
3. **Types and method signatures** - "the stuff that's too internal for an architecture doc but that an agent might still get wrong"

Money quote: "None of these take long to produce (the model drafts them, you argue with it), and every one of them is a decision you'd otherwise be making implicitly during code review - at the most expensive possible time to change your mind."

### The Dillon Mulroy call-graph method (full recovery)

The tweet Dex cited: [dillon_mulroy, May 28 2026](https://x.com/dillon_mulroy/status/2059985696148849025): "my 'plans' largely look like pseudo code composed of mostly types/interfaces, how they compose, and their boundaries. ive recently started including call stacks - been very helpful for both me and agents when implementing."

He then [shared the full pi session](https://x.com/dillon_mulroy/status/2060018957227061299) behind it, and the research agent recovered the entire thing (2,576 entries; project is `mulroy-control-plane`, a link shortener on Cloudflare Durable Objects + Effect-TS; model was GPT-5.5 in Mario Zechner's pi agent). Extractions preserved: all 55 of his prompts in `artefacts/wsff-planning-pipeline-sources/dillon-pi-user-messages.txt`, every spec iteration including the full 8-section plan in `dillon-pi-spec-outputs.txt` (full session re-derivable from the gist).

![[dillon-mulroy-call-graph-plan.jpg|500]]

![[dillon-mulroy-pi-session-summary.jpg|500]]

**The exact prompt that produces the plan** (his words, typos included):

> "outline the type apis callstacks seams and adapters using typescript pseudo to more concretecly (and concisely) outline the ideas for all four"

**His full loop, reconstructed:**

1. Architecture-review pass first: agent produces refactor recommendations tagged with strength (Strong / Worth exploring), category (ports and adapters, in-process, local-substitutable, mock), problem, solution, benefits framed as "locality" and "leverage" (straight Ousterhout vocabulary: "Deepen the Alias mutation module", "the storage seam is shallow").
2. The sauce prompt above: TypeScript-pseudo sketches of each idea, each with a `### Callstack` block.
3. **Annotation loop via [Plannotator](https://github.com/backnotprop/plannotator)**: he annotates the agent's message like a doc review, with surgical design feedback ("favor yield* Dependency/Service over parameter dependency injection"; "lets drop the entire mutation/outcome model... put it on the caller to orchestrate rollbacks"; pastes a preferred code pattern and asks "can we use a pattern closer to this").
4. Naming iteration ("what would be a better name for LinkCatalogWrites" -> `LinkCatalogCoordinator`), and every correction gets codified into AGENTS.md as a rule.
5. "output the full spec with that/those change(s)" -> the final 8-section spec.
6. Post-implementation audit, asked verbatim: "where did things deviate from the tech spec or where did you hit unknown unknowns and have to make decisions on your own."

**The 8-section plan doc** (verbatim headers): 1. Application-facing Link Catalog seam (service interface, full signatures, typed error channels). 2. Durable Object client seam (transport boundary as its own service). 3. Durable Object implementation. 4. LinkCatalogCoordinator (owns mutation serialization, write ordering, explicit compensation). 5. LinkCatalogStore: CRUD-shaped persistence seam (with a plain-text semantics block and an explicit "Delete from current model" list). 6. SQL executor module. 7. Memory composition (test adapter wired at the same seam). 8. **Final call graph** - and critically it contains **two** graphs, Production AND Tests, parallel structures with different layers at the same seams. Followed by a "Depth wins" bullet list. Almost no prose anywhere; the whole spec is TypeScript pseudo.

**Why call graphs specifically work** (synthesized):

- The call graph is the **composition contract**: it pins which module calls which, at what depth, through which adapter, in prod and in test. In Effect terms it doubles as the Layer dependency graph, so wiring mistakes (the #1 agent architecture failure) become diffable against one canonical picture. His session's top bug find was exactly a call-graph bug: the interface said Durable Object but production composition silently bound an in-memory implementation.
- An indented arrow list is close to the **densest possible encoding of architecture for a context window**: no prose ambiguity, trivially checkable after implementation.
- Best community articulation ([Srinivas Devaki QT](https://x.com/eightnoteight/status/2060051107288924354)): "controlling models purely on the boundaries means internally you are giving them full freedom to slopmaxx - controlling with low level contracts is the best way to minimise slop." And Michal Kvasnicak's reply: "essentially treating the agent as fast autocomplete of given interfaces."
- His own advice version ([Jul 7](https://x.com/dillon_mulroy/status/2074594303465447532)): "specs that focus on types, interfaces, input/output types, call stacks/data flow" + track what you keep correcting in review and feed it back into the spec or a review skill. "i have not cracked automating this process and is very manual, but i am more productive and it's gotten easier to steer."
- Fresh (posted 2026-07-23, today): his 72-min workflow video, "the next token" ep. 3: https://x.com/dillon_mulroy/status/2080118955100791290 - prime material to mine.
- The counter-position for tension: [dax's viral anti-planning tweet](https://x.com/thdxr/status/2052231563564228779) ("i never make plans i hate looking at markdown... i just plan by having it make changes to the code", 1.4K likes). Dillon's call-stack tweet is the fleshed-out rebuttal.

### Why the types-and-signatures layer matters to LLMs (three mechanisms)

1. **Constraint surface**: types shrink the generation search space before sampling. "The agent's job narrows from 'figure out what to build' to 'satisfy this contract'" (Benenson, [The Compiler Is the Harness](https://medium.com/@ashbenen/the-compiler-is-the-harness-why-agentic-coding-works-so-well-in-rust-730bca7faf8e)); types "turn open-ended synthesis into guided search" (Sae-Hwan Park).
2. **Compile errors are the only reward signal that always lands in time**: "An agent only fixes what it can see before it stops, and a compile error is the one signal that always lands in time... Type the infrastructure and a failure shifts left from a production incident to a compile error the agent fixes itself" ([Encore, Why AI coding agents love type errors](https://encore.dev/blog/type-errors-agents)). This is the in-loop miniature of the RL argument: maintainability has no fast oracle, but type errors do.
3. **Deep modules are now a hardware requirement, not a style preference**: the best essay found, [Khola, "Ousterhout Was Right. But the Game Has Changed"](https://www.khola.blog/p/ousterhout-was-right-but-the-game): "Deep modules were a cognitive convenience for human engineers. For autonomous agents, they are a hard architectural requirement... Its cognitive limit is a hardware constraint." Includes the brutal observed failure: "The shallow public API cost more tokens to satisfy than writing to the private array. So it wrote to the private array. That is the optimization function at work: minimize tokens, pass the tests, ship the diff."

Lineage in one paragraph: Ousterhout (deep modules, define errors out of existence, design it twice: "an hour or two considering alternatives... compared to the days or weeks implementing"); Naur's Programming as Theory Building (code is a lossy byproduct of the theory in heads; "LLM-generated code isn't just theory-less - it's nobody's theory" per Christian Ekrem; a program-design doc is the densest **serializable** fraction of a Naur theory you can hand a stateless agent); Wlaschin's type-driven domain modeling ("compile-time unit tests", make illegal states unrepresentable); Meyer's Design by Contract, now revived for agents ("DbC assumes memory. Stateless agents require that the contract itself be the memory" - HackerNoon). Empirical: The Specification Gap paper (arXiv 2603.24284) found integration pass rates drop 31pp as specs degrade to bare signatures, and the cliff is specifically **losing data-structure references** - behavioral description alone is not enough, which is precisely the program-design layer.

Best practitioner anecdote: Vaibhav Gupta (BAML) spent **four days designing a threading system before writing a line**, then split it into five chunks agents could implement without guidance. "The actual unlock is upstream. Four days of careful thinking can compress two weeks of implementation into an afternoon of agent dispatching."

## Phase 4: Vertical Slices

His verbatim framing: "Models love what I call 'horizontal plans' - doing things in stack-order: 1. Database Migrations 2. Service Layer 3. API 4. Frontend... there's no real way to 'touch' the solution as you're going." And from the CRISPY talk: "despite every single model and trying to prompt this out and eval the hell out of this, **we cannot get models to stop writing horizontal plans**... before you know it, you're on the other side of 1,200 lines of code and it's not working."

His pre-AI order (start in the middle, work outward), verbatim:

1. Create API contract and serve mock data, test with curl
2. Create frontend to consume mock data, iterate + polish in browser
3. Wire API to services layer (services serve mock data/behavior)
4. Add database migrations, wire services to database
5. Add a bunch of business logic
6. Add a bunch of error handling

...testing at each step. "Most frontier models won't design a plan like this without human steering... If I could outsource the thinking here, I would." Execution: "I'll send off a model to do 1-3 slices at a time, and review the code as I go... Checking 100-200 lines and resteering is a lot cheaper." Gates reserved for sensitive/hard/complex work - he does not ceremony-max everything.

### Why models go horizontal (the deeper story)

- **The bias predates LLMs.** Bill Wake, 2003, INVEST: "Developers often have an inclination to work on only one layer at a time (and get it 'right'); but a full database layer has little value to the customer if there's no presentation layer." Models learned the horizontal bias from the corpus of humans who have it.
- **AI removed the natural speed-brake.** Dan Vega: "Without AI, horizontal development is slow enough that you usually catch the problems... AI removes that. It can generate an entire horizontal layer in seconds. And because the code looks right, you keep going, adding more layers on top of an unverified foundation." He calls it "horizontal generation at machine speed."
- **Context-window mechanics add an agent-specific reason to slice** (Alex Lavaee's QRSPI writeup): "Horizontal layers defer integration to the end, where the agent is deep in a context window full of accumulated work and least equipped to handle integration complexity... each vertical slice can be a fresh session with clean context." Slice = fresh context + verification gate; horizontal = integration debugging at max context depth, in the dumb zone.

### Lineage (for teaching depth)

- **Tracer bullets** (Pragmatic Programmer, 1999): "one thin line of execution goes end to end... skeletally thin." Tracer code is kept, prototypes are thrown away ("a prototype is like a town in a western movie. It's all facade").
- **Walking skeleton** (Cockburn): "a tiny implementation of the system that performs a small end-to-end function... The architecture and the functionality can then evolve in parallel." Modern angle: it is an inverse Conway maneuver, forcing teams (or agents) to integrate from day one.
- **GOOS** (Freeman & Pryce, 2009): "the thinnest possible slice of real functionality that we can automatically build, deploy, and test end-to-end" - your first acceptance test forces the whole verification harness into iteration zero. Direct ancestor of "tests and checks between phases."
- **Bill Wake's layer cake** (2003): origin of the metaphor; "the best way is to slice vertically through the layers."
- **Jimmy Bogard's Vertical Slice Architecture** (2018) is the cousin, not the same thing: he slices the **codebase** ("couple along the axis of change; minimize coupling between slices, maximize coupling in a slice"); Dex slices the **work**. You can run vertical-slice plans against a horizontally layered codebase.
- Also: Shape Up ch. 11, Elephant Carpaccio (Kniberg and Cockburn), and Matt Pocock's Jan 2026 livestream covering the same technique as tracer bullets.

### The review interplay

The famous line ("The Agentic Review" podcast, May 2026): **"You actually don't have too many PRs. You have too many bad PRs."** Slices are what keep each reviewable unit at the "two, three, 400 line block" size with a runnable behavior change attached, so review is "does this thin path work and belong," not archaeology. Combined with plan-level alignment: "Code review is about a lot of things, but the most important part is mental alignment... I can't read 2,000 lines of Go every day, but I can sure as heck read 200 lines of an implementation plan." Supporting data: Faros AI measured +91% review time and +154% PR size on high-AI-adoption teams; Addy Osmani: "A diff a human can actually read is now a design constraint, not a courtesy."

The economics behind "30 minutes of planning saves hours of review" (from the `where-does-the-time-go` side-quest): even pre-AI, coding was only 25-50% of feature time, so AI-only-for-coding barely moves the needle. Rework curve: 2-min yolo prompt ~50% rework; principal-engineer 5-hour spec ~10%. `expected pain = P(change needed) x pain of change`, and "about 80% of the expected pain is gone in the first few minutes" - so the failure mode on the other side is real too: "What you don't want to do is spend 6 hours planning a task for which you could have eliminated 80% of the expected pain in the first 10 minutes."

### When horizontal is right (honest caveats)

- Infrastructure-heavy and deeply technical platform work (engines, specialized processing) is layer-shaped, not story-shaped.
- Migrations: even HumanLayer's own template orders DB work schema -> store -> logic -> API -> clients; expand-contract migration work is inherently layer-scoped.
- Parallelism: once sliced as thin as possible, you split remaining tasks horizontally across people/agents against agreed interfaces (Tech Lead Handbook); one HN practitioner runs 4 parallel Claude worktrees per layer precisely because layers parallelize, at the cost of becoming the merge bottleneck himself.
- Vertical slices' append-only property (new features add files rather than modify shared ones) is also why they suit parallel agent sessions: fewer merge conflicts.

## The maintainability benchmarks (what "better verifiers" looks like)

Dex's dream benchmark, verbatim (Qodo podcast): give a model 20 sequential features, then "hand that code base to a smaller, dumber model and see if that model can implement the 21st feature... does this code get worse over time?"

- **SWE-Marathon** (Abundant AI, arXiv 2606.07682): 20 ultra-long-horizon tasks (clone Slack, C compiler in Rust), expert estimates 40-400 hours; best config (Opus 4.8 + Claude Code) resolves 26%; longest rollout 877M tokens. 13.8% of rollouts contain exploit-shaped actions, 0 of 1,300 earned reward through one (multi-layer anti-cheat; Gemini's "C compiler" that shelled out to system gcc got zeroed).
- **DeepSWE** (Datacurve) - note: Dex's slide/DataFun summaries say "DeepSuite"; the real name is DeepSWE. 113 contamination-free tasks written from scratch; reference solutions average 668 LOC (5.5x SWE-Bench Pro); motivated by their audit finding SWE-Bench Pro verifiers have 8% false positives / 25% false negatives.
- **FrontierCode** (Cognition): first benchmark measuring **mergeability** ("would the maintainer actually merge this PR?") - correctness + test quality + scope discipline + style. Novel graders: reverse-classical tests (the agent's own tests must FAIL on the broken base commit, catching vacuous tests), automated scope checks, adaptive grading. Opus 4.8 gets 13.4% on the hardest set.
- **SlopCodeBench** (the one Dex says he follows closely, arXiv 2603.24755): code erosion under iterative spec refinement; no agent solves any problem end-to-end; erosion rises in 80% of trajectories; agent code 2.2x more verbose than maintained human repos; prompts shift the intercept, not the slope.
- **CodeThread** (arXiv 2606.21804, closest to Dex's dream): agents building on agent-written code resolve up to 13.1% fewer tasks than building on human code, and classical metrics (cyclomatic complexity) do not explain the gap.

## Reactions and tensions worth knowing

- **Addy Osmani, "Software Factories, Light and Dark"**: coins **"comprehension debt"** - "the widening gap between how much code exists and how much any human still understands. A dark factory doesn't pay it down; it takes it on as fast as it can, with the tests green the whole way."
- **The Great Loops Debate** (same event): Dex: "Kubernetes is built on control loops - but they're deterministic loops"; Geoffrey Huntley conceding loops are "frontier thinking" and worrying "this time next year... a whole bunch of folks saying our factories failed."
- **Kelsey Hightower** pushback thread: software factories are a remix of SDLC; compiler comparison.
- **Sean Goedecke on Naur + agents** (best balanced take): agents do visible theory-building in their logs but "they can't retain theories... forced to construct a theory of the software from scratch, every single time they're spun up." His numbers: rejects ~80% of agent output on sight; ~10% reaches a PR.
- Cost reality check: HumanLayer's team of three averages ~$12k/month on Opus.

## Ranked primary sources

1. `wsff.md` - the talk's canonical essay (PRE-RELEASE flagged, don't quote publicly yet): https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md (+ `side-quests/where-does-the-time-go.md`)
2. Live keynote video: https://www.youtube.com/live/htM02KMNZnk?t=27166 (hlyr.dev/wsff-live)
3. Dillon's pi session (full spec + prompts recovered): gist `dmmulroy/5ddc8747b98a80ad993c18e95270038e`; tweets [1](https://x.com/dillon_mulroy/status/2059985696148849025), [2](https://x.com/dillon_mulroy/status/2060018957227061299); his new 72-min workflow video (Jul 23): https://x.com/dillon_mulroy/status/2080118955100791290
4. CRISPY talk ("Everything We Got Wrong About RPI"): https://www.youtube.com/watch?v=YwZR6tc7qYg (full transcript: github.com/shanraisshan/claude-code-best-practice, videos folder)
5. ACE-FCA essay + the shipped prompts (`research_codebase.md`, `create_plan.md`, `implement_plan.md`): https://github.com/humanlayer/advanced-context-engineering-for-coding-agents + humanlayer/humanlayer `.claude/commands/`
6. Worked example docs (BAML episode, with/without-research plan contrast): https://github.com/ai-that-works/ai-that-works (2025-08-05 folder)
7. Qodo podcast (the recantation + maintainability-RL quote + dream benchmark): https://www.qodo.ai/podcasts/closing-the-gap-ai-agent-hype-and-production-reality/
8. Khola, "Ousterhout Was Right. But the Game Has Changed": https://www.khola.blog/p/ousterhout-was-right-but-the-game
9. SlopCodeBench: arXiv 2603.24755; FrontierCode: https://cognition.com/blog/frontier-code-1.1; SWE-Marathon: https://www.swe-marathon.org/
10. Encore, "Why AI coding agents love type errors": https://encore.dev/blog/type-errors-agents
11. Addy Osmani, "Software Factories, Light and Dark": https://addyosmani.com/blog/software-factories/
12. "No Vibes Allowed" (the RPI foundation, 601K views): https://www.youtube.com/watch?v=rmvDxxNubIg
13. Lineage: Bill Wake INVEST (https://xp123.com/invest-in-good-stories-and-smart-tasks/), Artima tracer-bullets interview, GOOS ch. 10, Bogard VSA (https://www.jimmybogard.com/vertical-slice-architecture/)
14. Plannotator (the annotation tool enabling Dillon's loop): https://github.com/backnotprop/plannotator
15. dax's anti-planning counter-position: https://x.com/thdxr/status/2052231563564228779

## Content angles (quick capture, not developed)

1. **"The prompt behind the most bookmarked planning tweet"**: Dillon's session is fully public; walk the exact loop live (architecture review -> sauce prompt -> Plannotator annotations -> call graph -> post-implementation deviation audit). Nobody has done this teardown; his own video dropped today, so timing is hot.
2. **"Plans vs no plans" (Dillon vs dax)**: the two viral tweets are direct counter-positions from respected practitioners; test both on the same feature.
3. **"Why your agent writes the database layer first"**: the horizontal-bias story (Wake 2003 -> models learned it from us -> Vega's speed-brake argument -> Lavaee's context-window argument), with a live demo of a model producing a horizontal plan unprompted.
4. **"The benchmark that can't exist yet"**: maintainability as the un-RL-able objective; SlopCodeBench's intercept-vs-slope finding is a genuinely counterintuitive, citable result.
5. **Skill idea**: a program-design skill that outputs Dillon's 8-section spec shape (seams -> coordinator -> store semantics -> memory composition -> dual prod/test call graph) for any feature. The pieces are all recovered; this is buildable now.
