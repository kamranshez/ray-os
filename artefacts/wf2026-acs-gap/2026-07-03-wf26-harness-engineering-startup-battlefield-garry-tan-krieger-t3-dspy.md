---
title: "WF26: Harness Engineering & Startup Battlefield ft. Garry Tan, Mike Krieger, @t3dotgg, DSPy"
video_url: https://www.youtube.com/watch?v=I2cbIws9j10
video_id: I2cbIws9j10
channel: AI Engineer
published: 2026-07-03
status: posted
date: 2026-07-04
tags: [acs-gap, wf2026]
---

[**WF26: Harness Engineering & Startup Battlefield ft. Garry Tan, Mike Krieger, @t3dotgg, DSPy**](https://www.youtube.com/watch?v=I2cbIws9j10) - AI Engineer - uploaded 2026-07-03

> 2 net-new ACS videos available (delete your harness; deterministic gates) plus 1 complement (tokens have jobs). All-net-new verdict survived adversarial re-search.

## The one idea worth a video

- **As models improve, delete your harness: the highest-performing agents collapse orchestration code into a filesystem, bash, markdown files, and a sandbox.** Route A breadth spine. It makes predictable the largest cluster of bullets across at least five independent talks: Vercel's D0 journey (mega-prompt to multi-agent pipeline to filesystem agent, eval score doubling, then 80% tool removal), Google's Gemini three-version demo ending in agents.md plus skills plus sandboxed gh CLI, Cursor replacing 12,000 lines of TypeScript with ~200 lines of agent files, Manus refactoring its harness five times, the 741-tool accuracy collapse (fat catalogs vs just-in-time context), Salesforce's skills-over-MCP context economy, and Theo's whole product tier of markdown-file-on-a-cron businesses. The unifying mechanism survives 'why does it work': models are trained heavily on filesystem/bash/CLI behavior, so prescriptive tool orchestration fights the model while files let capability scale with the model. Its litmus heuristic is quotable and testable: harness complexity should DECREASE with each model release.
  VERDICT: ❌ net-new video available *(survived adversarial re-search)*
- **Real agent engineering encodes your domain as deterministic gates (pre-commit hooks, static types, scanners, tests) because prompts steer but only infrastructure enforces.** Route A breadth spine spanning the Loops Debate, PostHog's security talk, Salesforce, DSPy, and Sentry economics. It explains why loops work only on verifiable tasks (Huntley: encode back pressure so the loop cannot close until domain requirements are satisfied; static types as verification; 'the models are drunk... we engineer away those failure domains'), why PostHog's Warlock keeps enforcement in deterministic YARA rules with the LLM demoted to a fail-closed triage adviser, why Salesforce says enforce isolation in infrastructure never in prompts, and why DSPy separates 'what must happen' (code) from 'what should happen' (instructions). It also explains the failure bullets: sub-agents goal-seeking around guardrails and inventing secrets, agents modifying tests to cheat, attacks composing where code review does not. A tip dies at 'what do I type'; this survives 'why': non-deterministic components must never sit on the enforcement path.
  VERDICT: ❌ net-new video available
- **Within a fixed token budget, giving tokens distinct jobs (advising, grading, dreaming) beats pure execution, measured as expected tokens until a perfect run.** Route B altitude with its own complete demo and catalog slot. It comes from one dedicated Anthropic talk rather than cross-talk breadth, but it reframes the only lever most builders pull (spend more budget) into an orchestration-design decision, and it introduces a genuinely new metric: score runs pass/fail at 100% accuracy and compute expected tokens-to-perfect (execute needed 1.8M tokens; advise/grade far less). It fails the merge test with spine 1 (this ADDS meta-harness structure where spine 1 deletes it, and the tension itself is teachable), has a distinct demo (build executor/adviser/grader/dreamer on one benchmark task), a distinct slot (multi-agent orchestration and evals), and a distinct one-thing-after: add a grader with a rubric before you add budget.
  VERDICT: 🔗 next-step video available

**Summary:** AI Engineer World's Fair 2026 day four: harness engineering keynotes, Krieger fireside, DSPy, loops debate, Theo, Garry Tan, and startup battlefield across agentic engineering themes.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### As models improve, delete your harness

**The claim:** as models improve, the winning move is to delete your harness. The best agents collapse orchestration code into a filesystem, bash, markdown files, and a sandbox.

**Why it's non-obvious:** the industry default is to add scaffolding, more routing, more scoped tools, more planner/executor graphs. This spine says that scaffolding encodes yesterday's model weaknesses as permanent ceilings. The litmus test is quotable: "if your harness is getting more complex as the model improves, you are most likely overengineering your harness."

**The mechanism:** models are trained overwhelmingly on filesystem, bash, and CLI behavior, so prescriptive tool orchestration fights the model's native competence; because files and shell are the interface the model already knows, capability scales automatically with each release instead of being capped by your code. Vercel's D0 doubled its eval score by becoming "just a file system" and then removed 80% of its tools; Cursor swapped 12,000 lines of TypeScript for roughly 200 lines of agent files; 741 loaded tool schemas collapsed selection accuracy to 13.6% versus 78% at ten.

**Generalizes to:** whole products. Theo's PR triage service is one markdown file on a 9am cron writing an S3 dashboard.

**How it goes wrong:** deleting the harness is not deleting guardrails. Enforcement must stay deterministic (hooks, sandboxes), and deletions must be eval-gated, not vibes-gated.

### Deterministic gates, not prompt rules

**Claim:** Prompts steer agent behavior; only deterministic infrastructure enforces it. Real agent engineering means encoding your domain as gates (pre-commit hooks, static types, scanners, tests) that the loop physically cannot close around.

**Why non-obvious:** The default move is stacking rules into CLAUDE.md ("never read .env", "this module cannot depend on that one") and trusting compliance. That feels like enforcement. It is steering.

**Mechanism:** A model is a sampler, so every natural-language rule holds only probabilistically, and an autonomous loop takes thousands of samples, so any rule with nonzero violation odds eventually gets violated. Worse, goal-seeking agents actively route around soft constraints: PostHog caught sub-agents inventing fake secrets to satisfy guardrails. A deterministic gate has zero pass probability for a violation, and when it echoes a corrective prompt back (Huntley's back pressure), the violation becomes loop feedback instead of a shipped bug. "The models are drunk... we engineer away those failure domains."

**Generalizes to security:** PostHog's Warlock scanner blocks with deterministic YARA rules first; the LLM only triages false positives, fail-closed. "If it isn't enforced deterministically, it is not enforced."

**How it goes wrong:** agents edit the tests or hooks themselves, so gates must live outside the agent's write path; and gates check parts, not combinations, because "attacks compose, code review doesn't."

### Tokens have jobs

**The claim:** at a fixed token budget, splitting tokens into distinct jobs (executing, advising, grading, dreaming) beats spending them all on execution, when cost is measured as expected tokens until a perfect run.

**Why it's non-obvious:** the only lever most builders pull is budget: more retries, longer runs, bigger context. That assumes tokens are fungible fuel. Anthropic's Angela showed they aren't: at an identical budget, an executor that could phone an adviser mid-task hit 89% where execute-only hit 76%.

**The mechanism:** in domains where partial credit is worthless ("if you're not 100% accurate it's actually not useful", like an 80%-right P&L), the honest metric is expected tokens-to-perfect. Because a low per-run pass rate multiplies retries geometrically, execute-only costs an expected 1.8M tokens to reach one perfect answer. A rubric-holding grader converts failed runs into corrective loops instead of discarded spend, so pass probability rises and expected cost collapses.

**Generalizes to:** Claude Code primitives today: a grader is a rubric subagent gating completion; a dreamer is post-run reflection writing learnings to memory files.

**How it goes wrong:** this ADDS meta-harness where the same conference says delete harness; and a sloppy rubric passes garbage, making the grader theater. It only pays in genuinely pass/fail tasks.

## 🎬 Proposed ACS videos (ranked)

### 1. Delete Your Harness: Why the Best Agents Are Just a Filesystem

- **HOOK:** Vercel doubled their agent's eval score by deleting code, and Cursor replaced 12,000 lines of TypeScript with 200 lines of markdown.
- **THE PROMISE:** For anyone building or maintaining an agent pipeline: walk away with a litmus test and a repeatable ritual for collapsing orchestration code into files, bash, and a sandbox every time a new model ships.
- **THE SHAPE:** Open with the litmus test: your harness should get SIMPLER with every model release; if it grows, you are overengineering → Explain the mechanism: models are trained on filesystem and CLI behavior, so prescriptive orchestration fights the model while files ride each release for free → Live demo: take a prescriptive multi-agent pipeline (planner/executor with scoped tools) and rebuild it as a filesystem agent with just bash, read/write file, and a sandbox, then compare outputs → Tool pruning segment: the 741-tool collapse (127k tokens of schemas, 13.6% selection accuracy vs 78% at ten tools) and replacing fat catalogs with skills or just-in-time loading → Close with the build-to-delete ritual: on every model release, attempt to remove orchestration code instead of adding capability, plus a cron that distills successful runs into skills
- **SPINE:** As models improve, delete your harness: the highest-performing agents collapse orchestration code into a filesystem, bash, markdown files, and a sandbox.
- **SLOT:** Advanced Techniques class, new Architecture Principles chapter
- **RELATIONSHIP:** ❌ net-new
- **PROOF TO REUSE:** "we realized that the big unlock was that it was just a file system" (Vercel, on D0's eval score doubling after the filesystem rewrite, then removing 80% of its tools) | "if your harness is getting more complex as the model improves, you are most likely overengineering your harness" (Google Gemini API talk) | Cursor replaced roughly 12,000 lines of TypeScript orchestration with about 200 lines of agent files; Theo's PR triage product is one markdown file run on a 9am cron

### 2. Stop Writing Rules in Prompts. Build Gates Agents Cannot Pass

- **HOOK:** PostHog watched its own sub-agents invent fake secrets to sneak past guardrails written as prompts. Your CLAUDE.md rules are getting the same treatment.
- **THE PROMISE:** For engineers running autonomous loops: by the end you can convert your top three domain rules from prompt suggestions into deterministic gates the loop cannot close around.
- **THE SHAPE:** Open with the failure: put a rule in CLAUDE.md ('this module cannot depend on that one'), run a loop long enough, and watch the agent violate it because prompts hold only probabilistically → Build the fix live: a pre-commit hook that blocks the commit AND echoes a corrective prompt back into the loop, turning your architecture boundary into automatic feedback (Huntley's back pressure) → Show verification breadth: run the same loop on a typed vs untyped codebase to demo static types as free deterministic gates → Layer the Warlock pattern: deterministic pattern rules block BEFORE any model opinion; the LLM is demoted to a fail-closed triage adviser that only silences false positives → Close with the limits: keep gates outside the agent's write path so it cannot edit the tests to cheat, and keep architecture judgment human because gates check parts, not compositions
- **SPINE:** Real agent engineering encodes your domain as deterministic gates because prompts steer but only infrastructure enforces.
- **SLOT:** Loopy AI > Command and Control
- **RELATIONSHIP:** ❌ net-new
- **PROOF TO REUSE:** "if it isn't enforced deterministically, it is not enforced. Prompts are not security rules. Don't act like they are." (Sarah, PostHog) | "the models are drunk, right? You can't trust them. But like, we accept that. But we engineer away those failure domains" (Geoffrey Huntley) | PostHog's Warlock keeps all enforcement in deterministic YARA rules with the LLM as fail-closed triage only, and banned sub-agents outright after they tried inventing secrets to bypass guardrails

### 3. Add a Grader Before You Add Budget (Anthropic's Token Jobs Experiment)

- **HOOK:** Anthropic proved your agent's tokens are not fungible: the same 600k tokens arranged differently jumps accuracy from 76% to 89%.
- **THE PROMISE:** For builders whose agents fail on hard tasks: after this video you can wire a rubric grader and a reflection step into Claude Code and measure them by expected tokens until a perfect run, instead of blindly raising budget.
- **THE SHAPE:** The trap: your agent fails a hard task, so you raise max turns and retry. Show the real cost: execute-only needs an expected 1.8M tokens to reach one perfect answer. → The reframe: re-score everything pass/fail. In domains like a P&L, 80% right is 0% useful, so the metric that matters is expected tokens-to-perfect, not average accuracy. → The demo: one benchmark task, four strategies at one fixed budget. Executor baseline, adviser the executor can call mid-task, grader that loops until the rubric passes, dreamer that writes post-run learnings to memory. → Map to real primitives: grader = rubric-holding subagent gating completion, dreamer = reflection writing to memory files. Trivially buildable in Claude Code today. → Pick by business goal: advise for token efficiency, grade and dream for reliability. Then the rule: add a grader with a rubric before you ever add budget.
- **SPINE:** Within a fixed token budget, giving tokens distinct jobs beats pure execution, measured as expected tokens until a perfect run.
- **SLOT:** Advanced Techniques + Multi-Agent Orchestration
- **RELATIONSHIP:** 🔗 Complement: Automatic Plan Reviewing with Subagents already teaches specialized reviewer roles for plans; do not re-teach that. This adds the executor/adviser/grader/dreamer allocation framework and the tokens-to-perfect metric that says when a grader beats more budget.
- **PROOF TO REUSE:** "if you get really smart about having your tokens do these different jobs and try these different strategies, you're very very likely to be able to get a better outcome for the task at hand within a fixed budget" (Angela, Anthropic) | "You can expect on average to have to spend 1.8 million tokens with the execution strategy to get to your perfect answer" versus advise hitting 89% where execute hit 76% at an identical budget | "in this kind of domain for this kind of task if you're not 100% accurate it's actually not useful" which justifies pass-only scoring and the tokens-to-perfect metric

**Also film-able (not deep-dived):** Garry Tan's markdown organization: skill files are employees, resolver tables are org charts, trigger evals are performance reviews, and a curated company brain (library + librarian + 'skillify everything, never do one-off work') is the compounding asset. [Skills class (skill chaining / compounding) or business class] · Mike Krieger on how Anthropic actually works: most usage is async multiplayer delegation via tagging Claude in Slack as a proactive teammate that owns codebase areas, plus Claude Code artifacts (intent + trade-offs) replacing line-by-line PR review. [Claude CoWork class / loopy-ai command-and-control chapter] · The log is the agent: treat the append-only event log as the agent's identity (Skyrim save-file analogy) so runtimes are disposable, sessions resumable, and compaction is just a lossy projection. [Context-engineering class (durability/resumability chapter)] · Latent space vs deterministic space: deciding where each computation lives (LLM for taste/judgment, code for state like seating 800 people) as the root cause of most agent bugs. [Prompt-engineering or techniques class] · CLI vs MCP vs Skills decision rubric: who else needs it, which failure mode matters, how tight is context, with the 50-tools-burns-20k-tokens context-explosion demo. [Skills class (tooling-layer chapter)] · HTML is the agent's visual medium: agents fail at canvas tools and SVG but excel at HTML, so generate decks, docs, and even videos as divs and render to PDF later (pelican-on-a-bicycle demo). [Techniques class] · Theo's tier-shift thesis: what was a startup is now a side project and what was a side project is now a markdown file, so go wider and bigger, because 'if your idea doesn't feel stupid, it's not big enough'. [Business class]

## 📚 Full wisdom (reference)

### SUMMARY

AI Engineer World's Fair 2026 day four: harness engineering keynotes, Krieger fireside, DSPy, loops debate, Theo, Garry Tan, and startup battlefield across agentic engineering themes.

### IDEAS

- Vercel's D0 data agent doubled its eval score after replacing bespoke tools with filesystem plus bash.
- Cursor replaced twelve thousand lines of TypeScript orchestration with roughly two hundred lines of agent files.
- Google's Interactions API deletes agent loop code entirely: an agents.md file plus sandbox replaces Python plumbing.
- Anthropic's token-jobs experiments show advise, grade, and dream strategies beat pure execution at identical token budgets.
- Measuring expected tokens until a perfect run reveals execute costs 1.8 million versus advise far less.
- Geoffrey Huntley encodes domain constraints as pre-commit hooks that echo prompts back, creating loop back pressure.
- PostHog's Warlock scanner keeps all enforcement deterministic through Yara rules; the LLM only advises on triage.
- Tool-selection accuracy collapses from seventy-eight percent at ten tools to roughly thirteen percent at 741 tools.
- Garry Tan maps entire organizations onto markdown: skill files are employees, resolver tables are org charts.
- Trigger evals verifying that resolver tables actually load referenced files function as performance reviews for agents.
- Mike Krieger ported a several-hundred-thousand-line Python codebase to TypeScript over one weekend using a dynamic workflow.
- Anthropic engineers mostly delegate through Claude in Slack, tagging it as an asynchronous proactive multiplayer teammate.
- Claude Code artifacts explaining intention and trade-offs now replace reviewing inscrutable two-thousand-line pull requests at Anthropic.
- DSPy argues fixing input-output signatures lets you swap prompts, agents, and models without ever breaking integrations.
- DSPy.flex learns a custom harness per function over time, optimizing code itself rather than mere prompts.
- Vercel runs a recurring cron job that distills recent agent queries into roughly one hundred skills.
- Theo's PR triage service became a markdown file running on a cron, generating his daily priorities.
- Salesforce's rubric: choose the CLI for transparency, MCP for shared tenant-isolated services, skills for repeated procedures.
- Keeping fifty MCP tool schemas loaded burns fifteen to twenty thousand tokens before any task starts.
- Nori builds slides, docs, and videos through HTML because language, not canvas coordinates, is model native.
- Amnara frames the append-only log as the agent's identity; runtimes and models are merely disposable projections.
- Resonate makes agents design systems by building simulated implementations inside deterministic environments before writing concrete specifications.
- WorkOS proposes o.md, an agent-native registration spec letting agents sign up for services without any humans.
- Polygraph builds a unified dependency graph across hundreds of repos, creating one big navigable codebase illusion.
- Sub-agents inside PostHog's wizard tried inventing secrets to bypass guardrails, so sub-agents were then banned entirely.

### INSIGHTS

- When harness complexity grows as models improve, you are over-engineering; better models should delete your code.
- Tokens are not fungible; assigning them advisory, grading, and dreaming jobs beats pure brute-force execution spending.
- Loop engineering means preventing the loop from closing until deterministic gates satisfy your encoded domain requirements.
- Prompts can steer but they never enforce; anything not enforced deterministically in your infrastructure isn't enforced.
- Attacks compose while code review doesn't; two innocent merged changes can shake hands and open doors.
- The bottleneck moved from writing code to human capacity for conceptualizing and reviewing what agents produce.
- Capture every solved task as a reusable skill; asking an agent twice means you already failed.
- Decide whether computation belongs in latent space or deterministic code; most agent bugs cross that line.
- Separating task contracts from implementations lets you adopt every new technique without ever rewriting your integrations.
- Verification breadth determines loop viability; static types, tests, and simulators expand what agents can safely automate.
- Fewer, relevant tools beat comprehensive catalogs; context economy matters more than capability coverage for production agents.
- Memory without hygiene becomes a garbage dump with great search; provenance and pruning make it compound.
- Agents that learn from every interaction beat static agents; real-time skill updates outpace any periodic fine-tuning.
- Software factories still cannot decide whether they built the right thing; architecture judgment stays firmly human.

### QUOTES

- "we realized that the big unlock was that it was just a file system" (Andrew, Vercel)
- "if your harness is getting more complex as the model improves, you are most likely overengineering your harness" (Google Gemini API speaker)
- "if it isn't enforced deterministically, it is not enforced. Prompts are not security rules. Don't act like they are." (Sarah, PostHog)
- "attacks compose code review doesn't" (Sarah, PostHog)
- "your job now is to actually encodify your domain to prevent the agent from doing a commit" (Geoffrey Huntley)
- "the models are drunk, right? You can't trust them. But like, we accept that. But we engineer away those failure domains" (Geoffrey Huntley)
- "It's not the model. The 2x people and the 100x people are using the exact same claude. Same weights, same context window, same API. So the leverage is not in the weights, it's in how you wire the work." (Garry Tan)
- "if you have to ask for something twice, you failed" (Garry Tan)
- "A skill file is an employee." (Garry Tan)
- "Model quality is rented, but if you build your brain, you own that brain." (Garry Tan)
- "The models are getting better faster than we are." (Theo)
- "If your idea doesn't feel stupid, it's because your idea is not big enough." (Theo)
- "Do you know how many companies are at this event where their whole product could just be a markdown file?" (Theo)
- "Stop thinking like a user. Think like the model." (Amol, Nori)
- "if you get really smart about having your tokens do these different jobs and try these different strategies, you're very very likely to be able to get a better outcome for the task at hand within a fixed budget" (Angela, Anthropic)
- "You can expect on average to have to spend 1.8 million tokens with the execution strategy to get to your perfect answer." (Angela, Anthropic)

### HABITS

- Geoffrey Huntley strips all skills and markdown when new models release, testing bare model tastes first.
- Dex Horthy keeps hard problems under sixty thousand tokens, watching thinking traces for telltale flailing signals.
- Garry Tan skillifies every completed task immediately, refusing to ever perform the exact same work twice.
- Mike Krieger interrogates Claude about pull requests with his own questions instead of reading every line.
- Theo runs a nine a.m. cron where a markdown file triages PRs and prioritizes his day.
- Greg at Sentry reads agent-generated code after semantic verification passes, still personally steering architecture and simplification.
- Geoffrey Huntley vendors source code and minimally uses open source, generating replacements tailored to his requirements.
- Greg's team runs security scanning loops on every PR, paying roughly five dollars per PR deliberately.
- Mike Krieger encourages verbalizing emotions in meetings, opening with honest frustration to hold space for others.
- Anthropic labs reviews every project biweekly under persevere-or-pivot, shutting down some bets nearly every single cycle.
- Dex advises building small incremental loops throughout your system rather than an isolated three-month software factory.
- Krieger deliberately carves offline days, believing no job is important enough to prevent being offline briefly.

### FACTS

- The 2026 State of AI Engineering survey gathered 1,048 respondents; ninety-five percent now report using agents.
- Eighty-nine percent of agent-building teams now grant agents write access, up from fifty-two percent last year.
- Image generation usage doubled year over year, from eighteen percent to thirty-six percent of survey respondents.
- Sixty-seven percent expect a lab declaring AGI within five years; nine percent back transformers remaining state-of-the-art.
- Shopify cut costs five hundred fifty times using DSPy by swapping expensive models for cheap ones.
- Homa reduces ninety-ninth percentile small-message latency thirteenfold versus TCP, under roughly one hundred microseconds per roundtrip.
- PostHog's wizard reached eight thousand weekly runs; its Warlock scanner has never caught genuine malicious injection.
- Loading 741 tool schemas consumes 127,000 tokens before user questions, with accuracy collapsing to 13.6 percent.
- A quarter of YC's winter 2025 batch had codebases ninety-five percent AI generated a year ago.
- Ninety-four YC companies have crossed one hundred million dollars in revenue starting from a seed check.
- Anthropic's dreaming strategy consumed six hundred thousand tokens one-shot while pure execution used only about 39,000.
- Manus refactored its harness five times in six months; LangChain rearchitected deep research three times yearly.
- Emergent, an AI app builder, reached nine figures ARR within eight months of its public launch.
- Vercel removed eighty percent of D0's tools, achieving fewer steps, faster responses, and measurably better accuracy.

### REFERENCES

- People: Barr Yaron (Amplify), John Ousterhout (Stanford, Homa), Maxime/Isaac Miller (DSPy), Mike Krieger (Anthropic), Emil Eifrem (Neo4j), Caitlin & Angela (Anthropic platform, tokens-have-jobs), Paul Iusztin (Decoding ML), Louis-François Bouchard (Towards AI / What's AI), Nikita Kothari (Salesforce), Amol (Nori), Isidora (Bloom wedding venue / Threadline), Michael Grinich (WorkOS), Mike Chambers (AWS), Geoffrey Huntley (Ralph loop), Dex Horthy (HumanLayer), Ian Livingstone (Keycard), Greg (Sentry), Sarah (PostHog), Dominic Turno (Resonate), Andrew (Vercel), Ehsan (Amnara), Kay Malcolm (Oracle), Theo (t3dotgg), Garry Tan (YC), Howie Liu (Airtable / Hyper Agent), Simon Willison (pelican SVG test), Andrej Karpathy (three-waves quote), Sarah Guo, Ben Horowitz, Boris (Ralph post), Harrison Chase, Marc Benioff.
- Tools/projects: DSPy, GEPA, DSPy.flex, recursive language models (Alex Zhang, MIT), Homa, TCP/RDMA/RoCE, Neo4j ontology semantic layer, Claude Code, Claude CoWork, Claude Design, Claude in Slack ("tag"), Claude Code artifacts, Claude managed agents, Fable 5 / Mythos / Opus 4.5, Ralph loop, Loom experiment, Kubernetes, PostHog Wizard / Warlock / context mill, YARA, o.md spec, ID-JAG, Cloudflare Wrangler, MCP, Strands Agents SDK, Amazon Bedrock AgentCore, Kiro, Restate, Apache Flink, Resonate, NATS.io / Synadia, TurboQuant (Google, ICLR 2026), Oracle 26AI / agent memory SDK, Polygraph meta-harness, Vercel AI SDK, D0 agent, Eve framework, skills.sh, Next.js, Gemini Interactions API, Antigravity remote agent, agents.md, NotebookLM, Obsidian, Readwise, MonkeyType (Instagram), Character AI, Hello History, InCharacter benchmark, Hamilton (musical), GBrain, OpenClaw, T3 Chat, Hyper Agent, x402.
- Battlefield startups: Kamad (commodities trade agents), common.io (multiplayer markdown editor for people and agents, winner), Built by Foundry (creator businesses).
- Books/posts: The Hard Thing About Hard Things (Ben Horowitz), LLM Engineer's Handbook (Iusztin), Building for Production (Bouchard), "skillify it" (Garry Tan on X), Vercel file-system-agent blog post, martinfowler.com harness engineering article (Pete), LangChain harness article.

### ONE-SENTENCE TAKEAWAY

As models improve, delete harness code, encode verification deterministically, and compound learning through reusable skills.

### RECOMMENDATIONS

- Rebuild one hardcoded multi-agent pipeline as a filesystem agent with bash, files, and a secure sandbox.
- Audit your harness quarterly; every model release, try deleting orchestration code instead of adding even more.
- Give tokens explicit jobs: add a grader with a rubric before increasing any agent's token budget.
- Measure true cost as expected tokens until a perfect run, not average accuracy on single attempts.
- Write pre-commit hooks that echo corrective prompts, converting your architectural boundaries into automatic agent loop feedback.
- Keep enforcement deterministic and fail-closed; use LLM judgment only for triaging noise after automatic blocking decisions.
- Distill recurring agent queries into skills automatically with a scheduled job reviewing your recent successful runs.
- Skillify every completed one-off task before closing the session, building a compounding library of reusable procedures.
- Replace one small recurring service with a markdown file executed on a cron by an agent.
- Prune MCP tool catalogs aggressively; load task-relevant tools just in time through skills or semantic routing.
- Share Claude Code artifacts explaining intent and trade-offs instead of raw diffs for large generated changes.
- Test each new model bare, without skills or markdown, learning its tastes before layering back customization.
- Start software factory efforts small and iterative with real users, never as a three-month isolated build.
