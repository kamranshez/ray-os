---
title: "WF2026: Autoresearch & Keynotes ft. Anthropic, Google DeepMind, Amazon AGI, Sonar, Arena, Recursive (Day 2)"
video_url: https://www.youtube.com/watch?v=4sX_He5c4sI
video_id: 4sX_He5c4sI
channel: AI Engineer
published: 2026-07-02
status: posted
date: 2026-07-04
tags: [acs-gap, wf2026]
---

[**WF2026: Autoresearch & Keynotes ft. Anthropic, Google DeepMind, Amazon AGI, Sonar, Arena, Recursive (AI Engineer World's Fair 2026, Day 2)**](https://www.youtube.com/watch?v=4sX_He5c4sI) - AI Engineer - uploaded 2026-07-02

> 1 complement (surface your unknown unknowns, the next step beyond The Context Layer) plus 1 spine-level partial gap (verification loop / evals-as-CI). Autoresearch spine already covered by the catalog.

## The one idea worth a video

- **With Mythos-class models the bottleneck moves to you: systematically use Claude to surface your unknown unknowns before and during the build (Anthropic's field guide to Fable).** This is the load-bearing idea of the day's opening Anthropic keynote: capability overhang means the harness and the prompter are what contain the model, so Tariq's entire toolkit (blind spot pass, divergent prototypes, interview-me, references-as-maps, implementation notes, post-run quizzes) plus the 80%-smaller system prompt and context-not-constraints guidance all become predictable once you accept that matching your mental map to the codebase territory is the new job. Each technique is a beat of one filmable workflow, not a separate video.
  VERDICT: 🔗 next-step video available
- **Auto research is the new agentic workflow: freeze the harness, define a verifiable score, expose one small editable surface, and let an agent propose-test-keep-or-revert overnight. Anything you can write as text and score, you can optimize.** This single loop pattern makes most of the day predictable: Prime Intellect's Codex/Claude Code speedrun agents, W&B's Arya running 200+ experiments, Wiko's Aiden winning an OpenAI hiring competition, Jina's overnight embedding-program search, GPU kernel tuning, Supercell's village-policy optimization, and GEPA/optimize-anything are all the same while-loop with different scoreboards. It also carries the failure lore (80% of proposals are bad, reward hacking like disabling CUDA graphs, Pareto pools vs greedy local optima, small policy surfaces). GEPA's GSkill (optimizing a repo's agent skills cheaply and transferring them to frontier models) is the most directly filmable ACS instance.
  VERDICT: ✅ covered: Autoresearch Overview + Autoresearch Technical Example (Loopy AI > Compounding Loops). Kept for understanding; excluded from pitches.
- **Agent velocity only survives if zero-trust, multi-layered verification is baked into the loop itself: guide with context plus constraints, verify algorithmically and agentically, and treat evals as the new CI.** Four independent talks converge on this: Sonar's AC/DC cycle with its 44%-fewer-outages and 92%-issue-reduction data, Meta's 'benchmarks measure capability, production measures behavior' eval pyramid, W&B's tasks-as-YAML with LLM judges running nightly as go/no-go gates, and Arize's agent-as-a-judge Signal that mines traces and opens fix PRs. It explains why the Carnegie Mellon 3-5x velocity boost dissipates in three months without it, and why clean codebases cut agent token use. Distinct demo (building a verification loop around a coding agent) and distinct ACS slot from spine 2's optimization loop: one hill-climbs a score, this one gates what ships.
  VERDICT: 🟡 partial gap: "Automatic Plan Reviewing with Subagents" already covers pre-implementation review with specialized agents; this adds continuous production verification gates throughout the shipping loop and evals-as-CI infrastructure to sustain agent velocity at scale.

**Summary:** AI Engineer World's Fair 2026 Day 2 keynotes: Anthropic, Sonar, DeepMind, Amazon, and startups on Fable, auto research loops, verification, evals, memory, and agent economics.

🔴 0 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 1 covered

## 🔬 Deep dive

### Surface your unknown unknowns

**Claim:** With Mythos-class models the model is no longer the bottleneck; you are, so the new job is systematically using Claude to surface your own unknown unknowns before and during the build.

**Why it's non-obvious:** the default instinct is to write ever-tighter specs and bigger prompts, but Anthropic went the other way, removing 80% of Claude Code's system prompt because "the examples tend to constrain it because it's actually more imaginative than the examples we give it."

**Mechanism:** because capability now overhangs the harness, every unspecified decision point becomes a place the model guesses; because "the map is not the territory," your mental map of the codebase, not the model's ability, determines which guesses go wrong; therefore the leverage move is running the model against your map first via a blind spot pass, an interview that prioritizes architecture-changing questions, and divergent prototypes that surface preferences you didn't know you held.

**Generalizes to:** Tariq applies the same blind spot pass to non-code domains like color grading his own videos, i.e. any project brief or client onboarding.

**Failure modes:** answering 40 interview questions on a task too small to warrant it, and skipping the closing quiz so you ship a PR you can't defend.

### Auto research as a discipline (covered, no pitch)

**Claim:** Auto research is not a new capability, it is a discipline: freeze the harness, define a verifiable score, expose one small editable surface, and let an agent propose-test-keep-or-revert overnight. As the Prime Intellect speaker put it, "In actuality, it's really just a while loop."

**Why non-obvious:** Most people assume overnight agents need smarter models or elaborate scaffolding. The talks argue the opposite bottleneck: roughly 80% of what the loop proposes is bad, so the leverage lives entirely in the scoreboard and the revert, not in the proposals.

**Mechanism:** Because the score is automatic, bad proposals cost nothing but compute; because the harness and metrics are frozen while only a small policy surface is editable, the agent cannot game the evaluation (Supercell's pattern), so accepted diffs are real gains, and gains compound run over run. Keeping a Pareto pool instead of only the current best (GEPA's move) prevents greedy dead ends.

**Generalizes to:** GSkill on your own repo: optimize agent skills with GPT-5-mini (24% to 93% issue resolution), then transfer them to Sonnet for ~100% at half the execution time.

**How it goes wrong:** Reward hacking (agents disabling CUDA graphs or testing tiny contexts to fake speedups) unless you write explicit do-not rules, and harness drift, where letting the agent touch the metric turns optimization into fiction.

### Verification as the survival condition for agent velocity

**The claim:** agent velocity only compounds if zero-trust verification is baked into the loop itself: context plus constraints going in, algorithmic plus agentic checks coming out, and evals running as the new CI gate on what ships.

**Why it's non-obvious:** most teams treat review as an afterthought and assume the speed boost is permanent. Carnegie Mellon found the 3-5x velocity gain from coding agents dissipates within roughly three months. The mechanism: unverified agent output compounds technical debt, a messier codebase inflates the agent's token consumption and error rate, so this week's velocity is borrowed against next month's slowdown. Verification is what keeps the codebase legible enough for agents to stay fast, which is why Sonar's split of guidance into context vs constraints alone cut tokens 30%+, and its multi-layer verify customers saw 44% fewer AI-derived outages. Layering matters because a single-model reviewer inherits that model's biases; you pair algorithmic checks with a different-model judge.

**It generalizes** straight to agent products: W&B encodes behaviors as YAML tasks with LLM judges running nightly as go/no-go gates, because "tasks and evals are the new world of CI" and "benchmarks measure model capability. Production measures system behavior."

**How it goes wrong:** judges drift without weekly human trace-review calibration, and over-heavy gates strangle the very velocity they protect.

## 🎬 Proposed ACS videos (ranked)

### 1. Claude Knows What You Don't Know. Ask It First

- **HOOK:** Anthropic deleted 80% of Claude Code's system prompt, because the bottleneck is no longer the model. It is what you forgot to tell it.
- **THE PROMISE:** For anyone starting a build in unfamiliar territory: run a repeatable pre-build workflow that surfaces your unknown unknowns before the first prompt, then keeps you in the loop until you can defend the PR.
- **THE SHAPE:** The framing: 'the map is not the territory'. Draw the 2x2 unknowns matrix and show why every unspecified decision point is where Fable guesses → Demo 1, blind spot pass: 'I'm adding a new auth provider I know nothing about in this codebase, do a blind spot pass to find my relevant unknown unknowns and help me prompt better', pointed at git history for gotchas → Demo 2, interview mode: have Claude ask questions about the spec with the instruction 'prioritize questions that would change the architecture' → Demo 3, unknown knowns: 'make me an HTML page with four wildly different design directions so I can react', taste surfaces by reaction not specification → Close the loop: implementation notes logging every unknown Fable hits mid-run, then a post-run quiz so you can defend the merged PR
- **SPINE:** With Mythos-class models the bottleneck moves to you: systematically use Claude to surface your unknown unknowns before and during the build.
- **SLOT:** context-engineering / The Solution Paradigm
- **RELATIONSHIP:** 🔗 Complement: 'The Context Layer' already teaches externalizing discovered unknowns into a persistent harness; this video adds the pre-build workflow for discovering those unknowns in the first place, using Claude as the probe.
- **PROOF TO REUSE:** "The map is not the territory." (Tariq Shihipar, Anthropic) | "We recently removed 80% of the system prompt for Claude Code" because "the examples tend to constrain it because it's actually more imaginative than the examples we give it" | "luckily you can use Claude, you can use Fable to find your unknowns"

### 2. Why Agent Speed Dies in 3 Months (Build the Verification Loop That Saves It)

- **HOOK:** Carnegie Mellon found your 3 to 5x coding agent boost evaporates in about three months. Here is the loop the teams who kept it are running.
- **THE PROMISE:** For engineers shipping with coding agents daily: leave able to wrap a zero-trust, two-layer verification gate plus a nightly eval suite around their agent so velocity compounds instead of decaying.
- **THE SHAPE:** The trap: unverified agent output compounds debt, debt inflates the agent's own token use and error rate, and the CMU 3-5x gain quietly dies → Guide: split your guidance into two artifacts, context (semantic map of the codebase) and constraints (allowed deps, standards, intended architecture); Sonar measured 30%+ token reduction from this alone → Verify in layers: demo bolting algorithmic checks (secrets, data flows, known patterns) plus an agentic reviewer on a different model onto a Claude Code run, because every model has biases → Evals as CI: encode behaviors as YAML tasks with two LLM judges plus a rule-based judge, cluster into a nightly suite that gates promotion (W&B shipped on 73% candidate vs 72% prod) → Keep humans as calibrators: weekly best/worst trace review, and the explain-it-or-don't-ship-it rule
- **SPINE:** Agent velocity only survives if zero-trust, multi-layered verification is baked into the loop itself.
- **SLOT:** advanced-techniques + multi-agent-orchestration
- **RELATIONSHIP:** 🟡 Partial: "Automatic Plan Reviewing with Subagents" covers pre-implementation plan review; this fills the after-the-code gap, continuous layered verification gates and evals-as-CI that decide what actually ships.
- **PROOF TO REUSE:** "tasks and evals are the new world of CI" | "benchmarks measure model capability. Production measures system behavior" | Sonar customers with multi-layered verification report 44% fewer AI-derived production outages; one large bank hit 92% issue reduction with guide-verify-solve

**Also film-able (not deep-dived):** Agents are repo-bound amnesiacs: Polygraph-style meta-harnesses build one dependency graph across all your repos and capture resumable, shareable agent sessions so one explanation replaces seven. [Context-engineering / command-and-control class (multi-repo agent memory)] · The log is the agent: treat the append-only event log as the agent's identity (save-file analogy), enabling resume, replay, and portability across runtimes and models. [Context-engineering class (session/state design chapter)] · Own the verdict: Addy Osmani's alpha-and-decay career math, cognitive debt, cognitive surrender, and orchestration tax, the outer-loop skills that survive every model release. [Business class / engineer-mindset video] · HTML is the agent's native visual medium: stop fighting canvases and have Claude generate decks, docs, and even videos as divs, then render to PDF. [Techniques class (deliverables/artifacts chapter)] · Cost engineering for agents: input tokens dominate long-running task cost, so compare cache-hit prices not list prices, and match task archetype (ceiling vs no-ceiling) to model tier. [Business class (agent economics video)] · Memory recall policy as a first-class metric: Sakana's ladder (no memory → RAG → ranked decision ledger → oracle) shows ranked ledgers beat vector RAG and bad memory costs more than none. [Context-engineering class (memory harness design)] · Agent recipes: version your taste into a git repo. Failure patterns become judges, repeated behaviors become skills, user frustrations become harness extensions (Introspection's pi.recipes pattern). [Skills class (self-improving skill systems)] · Classic engineering discipline for agentic systems: giant prompts are god-classes. Decompose into skills, schemas, scripts, and subagents; code for determinism, agents for judgment, humans for authority. [Agentic-coding fundamentals / techniques class] · Simulation-first specs: Resonate has agents build a deterministic simulated implementation as 'executable design' before writing the concrete spec and production system. Agents moving upstream into design. [Techniques class (spec-driven development chapter)]

## 📚 Full wisdom (reference)

### SUMMARY

AI Engineer World's Fair 2026 Day 2 keynotes: Anthropic, Sonar, DeepMind, Amazon, and startups on Fable, auto research loops, verification, evals, memory, and agent economics.

### IDEAS

- Anthropic removed eighty percent of Claude Code's system prompt because examples constrain the newest models' imagination.
- Tariq's blind spot pass asks Claude to surface unknown unknowns in unfamiliar modules before prompting begins.
- Ask Fable for four wildly different HTML design prototypes so you can react, revealing unknown knowns.
- Giving Claude reference code or an HTML mockup as a map beats writing detailed specs yourself.
- Sonar's AC/DC cycle surrounds generation with guide, verify, and solve loops, treating verification as preemptive discipline.
- Separating context from constraints when guiding agents cut Sonar customers' token consumption by over thirty percent.
- Amazon's perception agents read the rendered screen, letting agents verify their own work without backend APIs.
- Annotation extensions let you point at page elements instead of writing long lossy textual change descriptions.
- DeepMind proposes new programming languages designed for models, strongly typed, unreadable by humans, enforcing correctness structurally.
- Open-ended compression benchmarks force models toward inventing novel algorithms because the loss function never fully saturates.
- Arize's Signal agent reads production traces, discovers subtle failure patterns, then opens pull requests with fixes.
- Prime Intellect's Claude Code agent quit every ten hours declaring records unbeatable; Codex almost never idled.
- Autonomous speedrun agents beat human records by combining papers, yet discovered no genuinely novel optimizer mechanisms.
- Weights and Biases writes tasks as YAML unit tests with LLM judges running nightly eval suites.
- Wiko's Aiden agent won seven leaderboard records using only four percent of the competition's total compute.
- Your eval is the loss function; your codebase abstraction is the architecture biasing agent search direction.
- GEPA's reflective optimization doubled GRPO's gains from twenty-five thousand rollouts using just three training examples alone.
- Optimized skills took a GPT-5-mini agent from twenty-four to ninety-three percent on Go repository issue resolution.
- Cheaply optimized skills transferred to Claude Sonnet, hitting one hundred percent resolution while halving execution time.
- Polygraph builds one dependency graph across thousands of repos, creating the illusion of one big codebase.
- Captured agent sessions resume on coworkers' machines with different agents, sharing memory like Star Trek transporters.
- Amnara argues the agent is its append-only event log, not the model or the runtime environment.
- Introspection's agent recipes version taste into git repos: failure patterns become judges, repeated behaviors become skills.
- Nori renders decks, docs, and videos as HTML because language, not canvas, is models' native medium.
- Artificial Analysis shows agentic task costs are dominated by input tokens, making cache-hit input pricing decisive.

### INSIGHTS

- Capability overhang means models get smarter in spiky ways; harnesses and prompts are the real constraint.
- The map is never the territory; every unspecified decision point becomes an unknown Claude must navigate.
- Coding was solved first because code is verifiable; reliability appears wherever answers can be checked automatically.
- Velocity gains from coding agents evaporate within months unless verification controls the compounding technical debt created.
- Auto research succeeds when humans supply ideas and taste while agents supply relentless execution and search.
- Freezing the harness and exposing only a small policy surface prevents optimization loops from reward hacking.
- Keeping a Pareto pool of candidates beats greedy loops that quickly get stuck in local optima.
- Production telemetry outranks benchmarks; every real interaction becomes evaluation data for agents behaving in live workflows.
- Memory harnesses only pay off when tasks exceed context; otherwise they add pure cost without capability.
- Agents are constrained in space and time: they see one repo and forget every previous session.
- The inner loop is capability, the outer loop is agency: deciding, verifying, approving, and owning outcomes.
- Cognitive debt grows as generated repositories outpace human understanding; explain the change or don't ship it.
- Use code for determinism, agents for judgment, humans for authority when architecting any agentic software system.
- Giant prompts are the new god-class code smell; decompose into skills, schemas, scripts, and focused subagents.
- Token prices fall tenfold yearly per intelligence level, yet cost per task rises as horizons lengthen.

### QUOTES

- "The models are grown, not designed." (Tariq Shihipar, Anthropic)
- "We recently removed 80% of the system prompt for Claude Code." (Tariq Shihipar, Anthropic)
- "The map is not the territory." (Tariq Shihipar, Anthropic)
- "The only way to prove that agents work is to do the best work of our lives faster than ever before." (Tariq Shihipar, Anthropic)
- "AI slop is everywhere." (Tariq Shakat, Sonar CEO)
- "Code is provable, but when you start dealing with large code bases, software is not." (Tariq Shakat, Sonar CEO)
- "We're now in a world where writing code is free or nearly free." (Benoit Schillings, Google DeepMind)
- "I think that 80% of the new code added to GitHub today is machine generated." (Benoit Schillings, Google DeepMind)
- "What if the best way to evaluate an agent was actually with an agent?" (Aparna Dhinakaran, Arize)
- "In reality, execution is mostly the bottleneck." (Junya, Wiko/Aiden)
- "If you can write it as text and score it, GEPA can optimize it." (Lakshya Agrawal, GEPA)
- "Stop thinking like a user. Think like the model." (Amol, Nori Agentic)
- "The agent can follow your runbook, but it can't inherit the consequences." (Addy Osmani)
- "Your cognitive bandwidth does not parallelize." (Addy Osmani)
- "Search is test time compute. So don't reach for bigger model. Do more search at inference instead." (Han Xiao, Jina/Elastic)

### HABITS

- Tariq asks Claude to interview him, prioritizing questions that would change the architecture before building anything.
- He asks Fable to log implementation notes whenever it hits unknowns, reviewing the deviations after runs.
- After completing work, he has Fable quiz him so he can represent the merged PR confidently.
- Tariq runs blind spot passes on unfamiliar domains, recently color grading for his own video editing.
- Weights and Biases teams manually review their best and worst traces together on a weekly board.
- Victor resumes coworkers' Polygraph sessions locally instead of asking them questions, interrogating their captured agent traces.
- Stefania runs multi-day evals on a fan-cooled M3 Ultra Mac, controlling it from her phone remotely.
- The kernel engineer profiles with NSight first, then tells auto research which top method is dumb.
- Amole builds entire board decks from his phone during subway commutes using agents with company data.
- Tariq made his conference deck with Fable in four hours on the night before presenting it.

### FACTS

- METR shows Mythos-class models complete eighteen-hour tasks at fifty percent success, three-hour tasks at eighty percent.
- Carnegie Mellon found three-to-five-x velocity boosts from coding agents typically dissipate within roughly three months entirely.
- Sonar customers using multi-layered verification report forty-four percent fewer AI-derived production outages than customers who don't.
- One large bank achieved ninety-two percent issue reduction applying guide-verify-solve inside its own agentic coding loops.
- Keller Jordan's modded nanoGPT community cut GPT-2 training from ninety minutes to under two minutes total.
- Arize runs over one hundred million evals monthly; top teams run over 3,800 different evaluators simultaneously.
- Aiden's PR H-index reached ten in the OpenAI-reviewed competition while the best human managed only seven.
- Databricks tuned GPT-OSS-120B with GEPA to outperform Claude Opus while running ninety times cheaper in production.
- Open-weights models have trailed the proprietary frontier by a consistent three-to-nine-month gap for three straight years.
- Arena collected one million agentic traces in its first month, with Fable 5 ranking first overall.
- OpenAI's internal Codex traffic shows essentially one hundred percent of output tokens now come from agents.
- The AI Engineer World's Fair 2026 drew a record seven thousand attendees across eighteen simultaneous tracks.

### REFERENCES

- Fable / Mythos-class models, Claude Code, AskUserQuestion tool, plan mode, HTML reports (Tariq Shihipar, Anthropic)
- "On the Biology of a Large Language Model" (Anthropic paper)
- Sonar, Sonar Vortex, AC/DC agent-centric development cycle, Sonar 2026 developer survey
- METR task-horizon benchmarks; Carnegie Mellon productivity study
- Amazon AGI Lab perception agents: open-source annotation Chrome extension + design.md verification harness; Bee wearable; "From RL to IRL" talk (Gaurav Mishra)
- Google DeepMind: Project Pitchfork (Google X), AlphaZero, SWE-bench critique, compression evals, Jeff Dean (Benoit Schillings)
- Arize: Alex agent, agent-as-a-judge, Signal trace-mining agent (Aparna Dhinakaran)
- OpenGov OG Assist: Effect (TypeScript), effect-ai package, LangGraph (migrated off), A2A protocol, agent cards, human-in-the-loop tool approval, sandboxing
- Recursive.com Eureka machine, nanochat, nanoGPT speedrun, CUDA kernel discovery, you.com, Karl Popper, Marc Andreessen's Techno-Optimist Manifesto
- Meta Superintelligence Labs production evals (Nishant Gupta): scenario-driven evals, SRE mindset, evaluation pyramid
- Jina/Elastic (Han Xiao): Jina embeddings v5 nano, ColBERT late interaction, DataRoom, SearchBox, Knowledge Graph projects, Noam Brown test-time-compute result
- Resonate durable execution (Dominic Tornow): abstract spec → simulation implementation → concrete spec → implementation; NATS.io / Synadia
- Sakana AI memory harness (Stefania): XBench, Spider V2, Qwen-27B 4-bit, DeepSeek V4 Flash, Coinbase local-model cost tweet
- Story mapping / analyst toolkit talk (Bas): user stories, business model canvas, value-architecture-design
- Prime Intellect speedrun agents (Elie): Karpathy's autoresearch, goal.md, Slurm sbatch, Codex GPT-5.5, Claude Code Opus 4.8, Kimi K2.7, GLM, AlphaEvolve, verifiers/prime-rl training libraries
- Weights & Biases Arya (Tim Sweeney): Launch, Weave, CoreWeave sandboxes, tasks-as-YAML, LLM-judge signals, iOS app
- Character AI / Hello History / Companion open-source persona framework; InCharacter benchmark
- Wiko Aiden (Junya): OpenAI Parameter Golf hiring challenge, MLE-bench, gated attention (Qwen paper), H-index over PRs
- GEPA / optimize-anything / GSkill (Lakshya Agrawal): GRPO comparison, AMD NPU XDNA2 case, ARC-AGI agent discovery, Databricks and Snorkel results, learning-fast-and-slow paper
- Recursive language models (Alex Zhang, Omar Khattab, MIT), recursivecodingagents.com (Raymond, OpenProse)
- GPU kernel autoresearch (Tis): NSight profiler, CuTe DSL, CUDA graphs reward hacking, FlashInfer, CUTLASS, bare-metal BIOS/overclock tweaks
- Polygraph meta-harness (Victor, trypolygraph.com); Context7 comparison
- Amnara "the log is the agent" (Ean)
- Introspection (Roland, ex-xAI): pi harness, Harbor evals, pi.recipes, OODA loops, OpenClaw/Clawbot car-buying loop
- Machinecraft 36-agent factory brain (Rushabh): RAG + graph memory, agent pantheon (Athena, Prometheus, Memnon corrections guard)
- Supercell AI innovation lab Project Paradox (Arina, Arnav Manikandan): controlled scenarios, behavioral scorecards, policy-surface optimization
- Nori Agentic (Amol): Simon Willison's pelican-on-a-bicycle SVG test, HTML-as-medium decks/docs/videos
- Mobile cloud sandboxes talk (Zion): 30-second VM boots, designer/QA agent iteration
- Addy Osmani: Boris Cherny role taxonomy, Paul Graham on taste, Mitchell Hashimoto taste definition, Wharton borrowed-confidence study, Homer Simpson automation gag
- Artificial Analysis (George Cameron, Micah Hill-Smith): Intelligence Index v4.1, AA Briefcase agentic knowledge-work eval, GPQA Diamond, cache-hit pricing analysis
- Arena (Wei-Lin Chiang): Chatbot Arena, LLM-as-a-judge, Agent Arena, RCT evaluation methodology, arena.ai leaderboard
- Google DeepMind gen-media panel: Nano Banana 2 Light, Gemini Omni Flash APIs, Veo 3 joint audio-video, "video models are zero-shot learners and reasoners" paper
- Karpathy's LLM wiki (agent memory layer), relocation-scout agent design talk
- Decoding AI second-brain / AI research OS segment (Obsidian, Readwise, NotebookLM)

### ONE-SENTENCE TAKEAWAY

Agentic coding's frontier is loops: verifiable metrics, small editable surfaces, baked-in verification, and human verdicts.

### RECOMMENDATIONS

- Before big builds, run a blind spot pass asking Claude which unknowns would change your prompt.
- Have Claude interview you about specs, explicitly prioritizing questions whose answers would change the system architecture.
- Pass reference code or HTML mockups as maps instead of writing every specification detail out yourself.
- Write a design markdown file so agents can verify visual work against your own explicit rules.
- Encode each desired agent behavior as a YAML task with judges, then run the evals nightly.
- Annotate roughly fifty production traces, then let GEPA learn an LLM-judge prompt for your specific domain.
- Optimize your repository's agent skills with cheap models, then transfer them to stronger frontier models freely.
- When running improvement loops, freeze the harness, score behavior, and revert changes that fail your scorecards.
- Give kernel-writing agents hardware context files; they will hallucinate architectures and quietly reward hack without them.
- Compare cache-hit input prices, not list prices, when estimating what long-running agentic tasks will actually cost.
- Generate slides, documents, and videos in HTML; agents reason in structure, not in pixels and coordinates.
- Adopt the explain-it-or-don't-ship-it rule: someone must understand every agent change well enough to defend it confidently.
