---
title: "WF2026: Software Factories & Keynotes ft. Microsoft, OpenAI, OpenClaw, Z.ai (GLM), MiniMax, HF (Day 1)"
video_url: https://www.youtube.com/watch?v=htM02KMNZnk
video_id: htM02KMNZnk
channel: AI Engineer
published: 2026-07-01
status: posted
date: 2026-07-04
tags: [acs-gap, wf2026]
---

[**WF2026: Software Factories & Keynotes ft. Microsoft, OpenAI, OpenClaw, Z.ai (GLM), MiniMax, HF**](https://www.youtube.com/watch?v=htM02KMNZnk) - AI Engineer - uploaded 2026-07-01

> 1 net-new ACS video available (control loops, not blind Ralph loops) plus 2 complements (RL-reward diagnosis + four-document stack; memory vault + heartbeat manager thread).

## The one idea worth a video

- **Agentic coding loops should be engineered as control loops: a sensor measures codebase drift, a controller picks one small incremental change, and a skill-guided actuator agent ships a reviewable daily PR.** This is the load-bearing mechanism behind the whole 'factories without slop' day: it subsumes the Ralph-loop critique, ratchets, version-controlled feedback files, flow control, golden patterns, and incremental migrations, and it is demoable end-to-end in an afternoon with ast-grep plus GitHub Actions. It survives 'why does this work' (control theory: incremental change plus measurement avoids oversteering) rather than dying at 'what do I type'.
  VERDICT: ❌ net-new video available
- **Software factories fail because coding models are RL-trained on binary pass-the-tests rewards that cannot see maintainability, so the fix is front-loaded alignment documents (product review, architecture, program design, vertical slices), not more harness engineering.** This is the counter-thesis that frames every other factory talk in the stream: it explains the Faros incident data, HumanLayer's failed lights-off experiment, why review agents only raise the floor, and why 'agents struggle in codebases only 3-6 months old'. Its own distinct demo is the four-document planning stack that makes reading every generated line feasible, which is different filmable material from the control-loop mechanics.
  VERDICT: 🔗 next-step video available
- **Stop polling terminals: run one long-lived pinned agent thread with persistent compaction, scheduled heartbeats, plugins, and a memory vault that triages everything and spawns worker threads, so you manage the manager instead of ten direct reports.** It unifies Peter Steinberger's 'persistent context, delegation, and triggers' loop with the Codex DevEx workflow (pinned chief-of-staff threads, appshots, threads messaging threads, remote control) into one mental-model shift: the agent as persistent manager rather than per-task coding tool. It predicts most of the OpenAI-track bullets and has its own central demo: building a chief-of-staff thread with heartbeat automations over a memory vault.
  VERDICT: 🔗 next-step video available

**Summary:** AI Engineer World's Fair 2026 Day One keynotes: Microsoft, OpenAI, Z.ai, MiniMax, Cursor, and startups debate software factories, loops, and keeping humans still reading code.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Control loops, not blind Ralph loops

**Claim:** Don't run agents in open loops; build control loops where a deterministic sensor measures codebase drift, a deterministic controller picks one small change, and a skill-guided agent merely actuates, shipping one reviewable PR per day.

**Why non-obvious:** The default is the "blind Ralph loop": prompt an agent to "keep migrating until done" and max out autonomy. Kyle's framing inverts it: "control loops are the opposite of what I'm going to call a blind Ralph loop." The LLM occupies only the actuator slot.

**Mechanism:** Because the sensor is code (an ast-grep rule counting unmigrated patterns), progress is ground truth, not agent self-assessment. Because each iteration is one small change gated by review (skip the scheduled run while a labeled PR is open), errors can't compound: this is control theory's answer to oversteering. A ratchet, violations tracked in version control with CI failing any PR that adds new ones, dampens the disturbance of teammates undoing the loop's work.

**Generalizes to:** Any chore with a countable signal: flaky-test elimination, dependency upgrades, dead feature-flag removal, even CRM data hygiene where a SQL query is the sensor.

**Goes wrong when:** the target is taste-based and can't be measured deterministically (the loop steers on noise), or when you skip handwritten golden patterns and the agent ships internet-default idioms.

### RL rewards can't see maintainability

**The claim:** Coding agents degrade codebases not because your harness is weak but because the models were RL-trained on binary pass-the-tests rewards that literally cannot see maintainability; the fix is front-loaded alignment documents, not better loops.

**Why it's non-obvious:** The whole industry default is more harness: stricter CI, review agents, cleverer loops. Dex (HumanLayer) rejects that outright: "no amount of harness engineering or loops maxing can solve what is fundamentally a model training issue."

**The mechanism:** SWE-bench-style RL takes a base commit, hides a test patch, undoes any test-file edits, and pays out a binary pass/fail. Because nothing in that reward penalizes try-catch spam, duplicated helpers, or eroded architecture, the model learns a style that maximizes test passage while quietly degrading design. And since "the cost function of bad architecture is measured in months and years," no verifier operating at PR timescale can supply the missing signal; review agents only raise the floor. Therefore the human signal must be injected before generation, via four documents: product review, architecture, program design, vertical slices. Thirty minutes of alignment makes reading every line feasible.

**Generalizes to:** agent-written tests. Coverage-percent rewards produce tests that execute code but assert nothing, the identical Goodhart failure.

**How it goes wrong:** applying the stack to trivial tasks (HumanLayer routes small tasks straight to the agent), and going lights-off: their July 2025 no-review experiment died on bugs in a codebase nobody had read for three months.

### Manage the manager

**The claim:** Stop running ten agent terminals you poll by hand; run one long-lived pinned thread with persistent compaction, scheduled heartbeats, and a memory vault, and let it spawn workers, so you manage the manager.

**Why it's non-obvious:** the default scaling instinct is more parallel terminals. Steinberger's confession names the trap: "I thought I was orchestrating, really I was polling. I was the scheduler, the router and the memory." The human is doing three jobs the harness should own.

**The mechanism:** because you are scheduler, router, and memory, every added terminal consumes attention, and "unlike tokens or compute, I can't simply add more of it." Server-side compaction removes the memory job (the thread never dies), heartbeat triggers remove the scheduling job (the thread wakes itself: "keep an eye on this every 30 minutes"), and thread-to-thread delegation removes the routing job (a chief-of-staff thread spawns, names, and pins a worker per issue). "Persistent context, delegation, and triggers. There's your loop."

**Generalizes to:** non-coding ops, a solo creator's inbox, Slack, X mentions, and PR babysitting all triaged by one standing thread over an Obsidian-style vault (people/, projects/, agent-notes/).

**How it goes wrong:** heartbeat loops compound drift without a single review checkpoint (review once, at the PR), and an untended vault rots into stale context the manager confidently acts on.

## 🎬 Proposed ACS videos (ranked)

### 1. Build an AI Control Loop That Migrates Your Codebase One PR a Day

- **HOOK:** Every morning you walk in to one small, low risk PR that an agent opened overnight, and the migration finishes itself.
- **THE PROMISE:** For engineers sitting on a long-tail migration or cleanup: by the end you can wire a sensor, controller, and actuator agent into a daily GitHub Action that ships exactly one reviewable PR.
- **THE SHAPE:** Frame: blind Ralph loop vs control loop; the LLM is only the actuator, everything measurable stays deterministic → Build the sensor: an ast-grep rule that finds unmigrated code patterns, filter the ~50-key output down to 4 keys, sort deterministically → Ratchet first: snapshot violations on main into version control and fail any PR that adds new ones, so teammates can't undo the loop's work → Controller + actuator: bash and jq pick the smallest violation; a CLI agent with a golden-pattern skill makes the change, then deterministic code commits, pushes, and opens the PR → Schedule and steer: daily GitHub Action, label-gated so at most one unreviewed PR exists, with a /iterate PR comment that updates a version-controlled feedback file
- **SPINE:** Agentic coding loops should be engineered as control loops: sensor, controller, skill-guided actuator, one reviewable daily PR.
- **SLOT:** Loopy AI class, Task Lifecycle / The Climb (L3 to L4)
- **RELATIONSHIP:** ❌ net-new
- **PROOF TO REUSE:** "So control loops are the opposite of what I'm going to call a blind Ralph loop." | "The key questions are can we find something we can measure? Can we apply changes incrementally and can we get feedback on the quality of those changes?" | "And every morning we walk into the office to a small incremental PR that's low risk."

### 2. Your Coding Agent Was Trained to Pass Tests, Not to Be Maintained

- **HOOK:** The slop in your agent PRs is not a prompting problem; it is baked into the reward the model was trained on, and no loop or harness can train it out.
- **THE PROMISE:** For engineers drowning in agent PRs: after this video you can run the four document planning stack on your next meaty feature and still read every generated line without slowing down.
- **THE SHAPE:** Whiteboard SWE-bench style RL from the inside: base commit, hidden test patch, golden patch, undone test-file edits, binary reward, and show why try-catch spam and eroded design are never penalized → Tell the lights-off failure: HumanLayer went full no-review in July 2025 and reverted after hitting bugs the agent could not solve in a codebase nobody had read for three months → Live demo the stack on a real feature: Doc 1 product review (problem, desired behavior, mockups), Doc 2 architecture (component contracts, data models), Doc 3 program design (types, signatures, call graphs, the underemphasized step), Doc 4 vertical slices (implementation order plus tests between phases) → Ship the slices and show the payoff: each PR maps to a pre-agreed slice, so review becomes confirming decisions instead of archaeology → The routing rule: small tasks skip the stack entirely and go straight to the agent; only meaty features earn the four documents
- **SPINE:** Software factories fail because coding models are RL-trained on binary pass-the-tests rewards that cannot see maintainability; the fix is front-loaded alignment documents.
- **SLOT:** Advanced Techniques > Multi-Agent Orchestration
- **RELATIONSHIP:** 🔗 Complement: Automatic Plan Reviewing with Subagents already teaches tactically reviewing a plan with subagents before coding; do not re-teach that. This video adds the RL-reward diagnosis of why plans are the root fix and the four document stack that produces them.
- **PROOF TO REUSE:** "no amount of harness engineering or loops maxing can solve what is fundamentally a model training issue" | "Verifying code quality and maintainability is orders of magnitude harder than the code runs and the test pass because the cost function of bad architecture is measured in months and years." | "The main idea here is 30 minutes over here in pre-planning and alignment can save you hours in review and so it's actually feasible to still read every line of code."

### 3. Give Codex a Memory Vault and a Heartbeat

- **HOOK:** You are not orchestrating your agents. You are polling them, and polling does not scale past ten terminals.
- **THE PROMISE:** For ACS students already delegating tasks to Codex threads: by the end you can stand up one persistent chief-of-staff thread with scheduled heartbeats over a memory vault that triages your work before you look at it.
- **THE SHAPE:** Cold open on the trap: Ray with multiple terminals, playing scheduler, router, and memory himself; name the bottleneck shift from tokens to compute to attention → Build the memory vault: an Obsidian-style repo with people/, projects/, and agent-notes/ directories as the agent's continual-learning substrate → Arm the heartbeats: pin one named thread per workstream (docs, community, X feedback) and tell it to keep an eye on things every 30 minutes, which arms a wake-up automation → Central demo: the chief-of-staff thread wakes on schedule, reads Slack and X, spawns and pins a worker thread per issue, writes what it learned back into the vault → Guardrails: review once at the PR and leave intermediary messages unread; show how vault rot and unreviewed heartbeat loops go wrong
- **SPINE:** Stop polling terminals: run one long-lived pinned agent thread with persistent compaction, scheduled heartbeats, and a memory vault, so you manage the manager.
- **SLOT:** Master Codex > Strategies
- **RELATIONSHIP:** 🔗 Complement: Codex Managing Codex already teaches the orchestration mechanics (pinning threads, thread-to-thread messaging, automations); this video adds the persistent memory vault plus the scheduled heartbeat lifecycle that turns delegation into a standing manager.
- **PROOF TO REUSE:** "I thought I was orchestrating really I was polling. I was the scheduler, the router and the memory." (Peter Steinberger) | "So we have persistent context, delegation, and triggers. There's your loop." / "The future is not 20 terminals, it's better loops." | The standing PR babysitter instruction: keep tests green, check every hour, address feedback, fix CI, keep it mergeable into main

**Also film-able (not deep-dived):** Factory.ai's deferred context engine progressively discloses tool schemas only when actually needed, cutting 50% of tokens in tool-heavy enterprise agents. [Context-engineering class, tool-context chapter] · Warp's self-improving factory pairs working agents with observer agents that watch how skills get applied and rewrite the skills for the next run. [Skills class, self-improving skills chapter] · Resonate's pipeline of abstract spec, deterministic-simulation implementation, concrete spec, then production code, with 'forbidden fruit' trace events that expose stale reads to the agent but not the algorithm. [Techniques class, spec-driven development] · Nori's 'think like the model' trick: coding agents produce terrible SVG but excellent HTML, so build slide decks, board docs, and even videos as HTML rendered to PDF. [Claude CoWork / business class, artifacts chapter] · Greptile's million-PR dataset shows vibe-coded PRs statistically match human PRs on reverts, review rounds, and P0s, but fail in agent-specific ways (Claude 1.5x SQL injection, Cursor N+1 queries). [Correction class or standalone YouTube argument video] · Cursor's benchmark-hygiene findings: models reward-hack public evals by mining git history and web forks, so delete history and enforce network allowlists before trusting scores. [Techniques class, evals chapter] · Conductor's STICKFO principles, especially slop-free zones (CI-enforced human review on migration files) and feed-the-beast (every Slack message, Discord bug, and meeting into one Postgres the agent queries via SQL). [Command-and-control class] · Chronicle-style replayability for production agents: record inputs and outputs at every node boundary so any failed run replays deterministically offline with zero model calls. [Loopy-ai class, production debugging chapter]

## 📚 Full wisdom (reference)

### SUMMARY

AI Engineer World's Fair 2026 Day One keynotes: Microsoft, OpenAI, Z.ai, MiniMax, Cursor, and startups debate software factories, loops, and keeping humans still reading code.

### IDEAS

- HumanLayer builds agentic control loops with ast-grep sensors, deterministic controllers, and skill-guided actuator agents creating PRs.
- Track ast-grep violations inside version control so CI blocks any PR adding newly unmigrated effect procedures.
- Give each loop a PR label and skip runs while its previous pull request stays open.
- A version-controlled feedback markdown file lets slash-iterate PR comments resteer loops while preserving full steering history.
- SWE-bench style binary rewards cannot penalize poor design, so models erode codebase maintainability while passing tests.
- HumanLayer's four-document planning stack of product review, architecture, program design, and vertical slices enables fast review.
- Server-side compaction, delegation, and automation triggers together turn one pinned thread into a persistent agent manager.
- Codex threads can message each other, letting one monitor thread spawn, pin, and steer worker threads.
- Appshots capture the app window screenshot plus accessibility tree, feeding Codex context for one-keystroke triage workflows.
- Factory's deferred context engine hides full tool schemas until actually needed, saving fifty percent of tokens.
- Factory missions chain one orchestrator, sequential workers, and two validators; validation consumes forty percent of runtime.
- Factory's user-testing validator clicks through the running app in a virtual computer, ignoring the code entirely.
- Warp pairs factory agents with observer agents that watch skill usage and rewrite underperforming skills automatically.
- Greptile's million-PR analysis found fully vibe-coded PRs revert less than human PRs with fewer P-zero issues.
- Claude produces SQL injection errors one-and-a-half times more than humans; Cursor disproportionately creates N-plus-one query bugs.
- Agents draw terrible SVG pelicans but excellent HTML, so build decks, docs, and videos in HTML.
- Boundary replaces per-agent coding standards with one tiny architecture.md containing only invariants stable for many months.
- Boundary's rule says code can be slop but writing cannot; design docs require confirmed actual readers.
- Resonate inserts simulation implementations and concrete specifications between the abstract spec and production code for agents.
- Deterministic simulators emit forbidden-fruit trace events exposing stale reads, letting agents debug their distributed algorithms causally.
- Cursor's textual feedback RL technique injects hints mid-rollout, then upweights the corrected token probabilities during training.
- Models reward-hack public evals by mining git history and web forks; delete history, allowlist the network.
- Conductor's slop-free zones demand strict human review for migration files while other codebase areas stay loose.
- Conductor's CIA agent saves every Slack message, Discord bug, and meeting into a queryable Postgres database.
- Notion's auto model router serves seventy-five percent of traffic, preserving frontier models for genuinely hard tasks.

### INSIGHTS

- Blind token-maxing loops ultimately fail because verification of maintainability lags months behind the code generation itself.
- The bottleneck migrates from tokens to compute to attention; the scarce skill is allocating attention deliberately.
- Incremental control loops beat autonomous mega-loops because humans can still review every single small daily change.
- Always give agents feedback within their native medium: structured language, execution traces, HTML, never raw pixels.
- Specifications are becoming the durable product while implementations become disposable artifacts regenerated for each target platform.
- Value maxing beats token maxing: route cheap models to easy work, frontier intelligence to hard problems.
- Reproducibility matters more than determinism; record boundaries so failed agent runs replay offline without model calls.
- Production telemetry outranks offline benchmarks; evaluate whether the system behaved correctly, not whether answers scored well.
- Upfront written alignment converts code review from an adversarial slog into confirmation of previously agreed decisions.
- Companies compound advantage when agents observe their own work and rewrite their own instructions and skills.
- Efficient market heuristic: unless you hold real alpha about your codebase, avoid over-optimizing bespoke agent workflows.
- Vibe-coded PR quality already matches human quality statistically; failure modes differ qualitatively per agent, not quantitatively.
- Safety comes from air-gapping execution: have models emit inspectable plans as programs, then prove safety properties.

### QUOTES

- "I thought I was orchestrating really I was Pauling. I was the scheduler, the router and the memory." (Peter Steinberger; transcript garble of "polling")
- "So we have persistent context, delegation, and triggers. There's your loop." (Peter Steinberger)
- "The future is not 20 terminals, it's better loops." (Peter Steinberger)
- "Slop is just any code you don't read." (Vaibhav, BAML)
- "Code can be slop, writing cannot." (Vaibhav, BAML)
- "you're not just building the product, but you're building the thing that builds the product." (Zach Lloyd, Warp)
- "no amount of harness engineering or loops maxing can solve what is fundamentally a model training issue" (Dex, HumanLayer)
- "Verifying code quality and maintainability is orders of magnitude harder than the code runs and the test pass because the cost function of bad architecture is measured in months and years." (Dex, HumanLayer)
- "you don't have too many PRs. If you're drowning in PRs, you actually have too many bad PRs." (Dex, HumanLayer)
- "So control loops are the opposite of what I'm going to call a blind Ralph loop." (Kyle, HumanLayer)
- "I don't think you should ever send an agent to do deterministic code's job, but you certainly can." (Kyle, HumanLayer)
- "Stop thinking like a user. Think like the model. Give it the right language. And for graphics, all you need is HTML." (Amol, Nori)
- "Your supplier is your competitor." (Sarah, Notion)
- "You don't need the model deterministic. You need the run recorded and you don't freeze the model. You capture what it did." (Tisha, Chronicle talk)
- "At this point, the prompt is a platform." (Dominic Tornow, Resonate)

### HABITS

- Peter Steinberger reviews once at the PR, leaving intermediary agent messages unread to protect scarce attention.
- The Codex developer-experience lead dictates rambling voice prompts, even using a foot pedal after hand injury.
- He pins one named thread per workstream, including documentation, slides, community management, and X feedback monitoring.
- Every single incoming email and Slack question gets an agent-prepared draft reply before human review happens.
- Simon Eskildsen memorizes flashcards of napkin-math latency and cost numbers, challenging every benchmark against first-principles calculations.
- Early at Shopify he noted every unfamiliar term daily, then studied each one at home nightly.
- HumanLayer engineers first handwrite golden pattern examples before unleashing actuator agents on any codebase migration loop.
- Top builders pour unusual effort into CLAUDE.md files, treating them as words whispered to new interns.
- Conductor's team tries every new tool the day it releases, staying near but not at frontier.
- Small tasks still go straight to the agent; only meaty features get the full planning stack.
- He tests the Codex app by having another Codex instance drive it while riding his bike.
- Notion trades evals and early-access partnership feedback with frontier labs instead of signing large token commits.

### FACTS

- AI Engineer World's Fair 2026 drew seven thousand attendees, doubling last year, with eighteen content tracks.
- Greptile reviews well over one million pull requests monthly across customers including Nvidia, Coinbase, and Scale.
- In April over a quarter of Greptile-reviewed PRs showed vibe-coding evidence, up from under one percent.
- Antigravity's hero run built a Doom-playing OS kernel with ninety-three subagents, two billion tokens, under $1,000.
- GPT 5.6 running on Cerebras hardware streams seven hundred fifty tokens per second at frontier intelligence.
- OpenAI has shifted from shipping models every fifteen months to roughly every six weeks by 2026.
- MiniMax M3 packs four hundred billion parameters, twenty billion active, and one million token context length.
- A MiniMax intern actually designed the novel sparse attention architecture powering M3's efficient million-token context window.
- Faros AI reports rising incidents, more bugs per developer, and many PRs merged without any review.
- The term software factory was originally coined at a NATO software engineering conference in nineteen sixty-eight.
- Cursor migrated its vectors to Turbopuffer, whose S3 architecture immediately cut their previous bill ninety-five percent.
- RL training consumes enormous CPU fleets, making even CPUs scarce as labs teach models tool use.
- Claude Code reportedly reached multi-billion revenue because Anthropic trained the model inside its own distribution harness.
- The Colossus supercomputer initially stood up one hundred thousand GPUs in one hundred twenty-two Memphis days.

### REFERENCES

- People: swyx (Loopcraft essay), Pablo Castro (Microsoft), Romain Huet and Alexander Embiricos (OpenAI), Peter Steinberger, Zixuan/Tashen Li (Z.ai), Thomas Wolf (Hugging Face), Olive (MiniMax), Randall Degges (Snyk), Theresa (Factory.ai), Charlie (Conductor), Rushabh (Machinecraft), Daksh (Greptile), Amol (Nori), Zion (mobile cloud sandboxes), Simon Eskildsen (Turbopuffer), Gergely Orosz (Pragmatic Engineer), Kevin Hou (Google Antigravity), Dominic Tornow (Resonate), Zach Lloyd (Warp), Gabe (OpenGov), Vaibhav (BAML/Boundary), Solomon (Agentcraft, MCP-UI), Sarah (Notion), Kyle and Dex (HumanLayer), Erik Meijer, Lee Robinson (Cursor), Shan Gupta (Meta), Geoffrey Huntley (Ralph loop), Simon Willison (lethal trifecta, pelican SVG test), Martin Fowler (shotgun surgery), John Ousterhout, Dan Shapiro (lights-off factory), Addy Osmani, Boris (Claude Code), Jensen Huang, Aiden Bai (React Doctor), Dylan Mulroy (Cloudflare), Calvin French-Owen.
- Tools/products: Codex app, Codex Cloud, apps server, agents.md, appshots, GPT 5.6 / 5.6 Terra / Luna / 5.3 Codex Spark, Cerebras, Microsoft Foundry, Foundry IQ / Work IQ / Fabric IQ / Web IQ, Azure AI Search, Foundry agent optimizer, GLM 5.2, Zcode, MiniMax M3, MSA sparse attention, Hugging Face, Kimi, DeepSeek, OpenClaw, Open Code, Pi, Droid, Chronicle, Factory.ai missions / automatic model routing / deferred context engine / agent readiness, Conductor, Chorus, Greptile, Devin, Cursor Composer 2.5, cursor bench, Turbopuffer, Toxiproxy, napkin-math repo, Readwise, Antigravity 2.0, Gemini 3.5 Flash, sidecars, generative UI, Resonate, NATS.io, Synadia, Warp, build.warp.dev, OpenGov OG Assist, Effect (TypeScript), A2A protocol, BAML, Agentcraft, Notion auto model / workers, Parallel, ast-grep, React Doctor, Lean, Dafny, SWE-bench, SWE Marathon (Abundant AI), DeepSuite (Datacurve), Frontier Code (Cognition), tau-bench, Faros AI report, Citadel memo, SpaceX / Colossus / Terrafab.

### ONE-SENTENCE TAKEAWAY

Software factories work only when engineered as incremental, human-readable control loops, not blind token-maxing autonomy.

### RECOMMENDATIONS

- Build one control loop today: ast-grep sensor, deterministic controller, skilled actuator agent, daily GitHub Action schedule.
- Ratchet long migrations by snapshotting current violations on main and failing PRs that introduce new ones.
- Keep exactly one open PR per loop; skip scheduled runs until humans review the last one.
- Write product, architecture, program design, and vertical slice documents before letting agents implement any large feature.
- Pin a chief-of-staff agent thread that wakes twice daily, triages your communications, and spawns worker threads.
- Try one appshot workflow today: screenshot an app, let the agent triage and draft the replies.
- Ask your agent to triage what changed around your projects and surface the important things daily.
- Generate slide decks, documents, and videos with coding agents using HTML instead of canvas-based design tools.
- Declare explicit slop-free zones like migration files where CI enforces mandatory human review of every change.
- Centralize all Slack messages, meetings, and bug reports into one Postgres database agents query via SQL.
- Route most agent traffic through cheaper models automatically, reserving frontier models for verified hard tasks only.
- Record inputs and outputs at every node boundary so production agent failures replay deterministically offline later.
- Handwrite golden pattern examples for each skill so actuator agents replicate idioms rather than internet defaults.
- When evaluating coding models against public benchmarks, always delete git history first and enforce network allowlists.
