---
title: "Automating Large Scale Refactors with Parallel Agents - Robert Brennan, OpenHands"
video_url: https://www.youtube.com/watch?v=rcsliSIy_YU
video_id: rcsliSIy_YU
channel: AI Engineer
published: 2026-01-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Automating Large Scale Refactors with Parallel Agents - Robert Brennan, OpenHands**](https://www.youtube.com/watch?v=rcsliSIy_YU) - AI Engineer - uploaded 2026-01-08

> net-new ACS video available: the coexistence-scaffolding migration pattern is a genuine gap, plus two strong next-step complements.

## The one idea worth a video

**Spine 1 (framework): Agent orchestration is decomposing a too-big task into verifiable PR-sized batches, running parallel agents, and aiming for ~90% automation, not 100%.** It subsumes the "why big tasks aren't one-shottable," the git-branch accumulation workflow, the concurrency limits, and the CVE-remediation demo. VERDICT: 🔗 next-step video available.

**Spine 2 (technique): A refactor state machine over a dependency-graph of PR-sized batches, where a verifier flags problems and a full-agent fixer turns each node green.** Distinct central demo (Calvin's code-smell elimination), distinct build. VERDICT: 🔗 next-step video available.

**Spine 3 (technique): For a library migration, build ugly coexistence scaffolding so old and new run side by side, convert components one at a time with validation, then rip the scaffolding out.** VERDICT: ❌ net-new video available.

## Summary + counts

Robert Brennan (OpenHands CEO) and Calvin show patterns for orchestrating swarms of parallel agents, with a human in the loop, to automate large-scale refactors, migrations, and CVE remediation.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1 - Orchestration is decomposition plus verification, targeting 90%.** The claim: large refactors are not "tasks," they are hundreds of interconnected changes, so the win is not a smarter single agent but breaking the work into chunks each agent can one-shot, running them in parallel, and reviewing intermediate output. Non-obvious because everyone chases the autonomous one-shot; Brennan argues even a frozen model reshapes engineering for years purely through this operationalization. The mechanism: a single context window cannot hold a huge codebase, and errors compound over long trajectories, so a tiny early mistake repeats at every step; decomposing into commit-sized units caps both blast radius and context, and parallelism turns serial toil into concurrent throughput. It generalizes cleanly to CVE remediation: one client hit a 30x resolution speedup by auto-scanning repos and opening ready-to-merge PRs. How it goes wrong: agents get lazy ("I migrated three of your 100 services"), lack codebase intuition, and 100% automation is the wrong bar. Brennan targets 90%, "still an order-of-magnitude productivity lift."

**Spine 2 - The dependency-graph batch state machine.** The claim: to refactor at scale you render the repo as a dependency graph, batch files by directory so related code stays together, then drive a verify-then-fix loop until every node turns green. Non-obvious because most builder-verifier setups run one loop on one diff; here the loop is a traversal over the whole graph, processing leaf batches first so migrated utilities are ready before their dependents. The mechanism: batching bounds each agent's scope to PR size, which improves per-change performance and reviewability; a verifier (programmatic command for tests, or an LLM for subjective code smells) marks each node pass or fail; the most powerful fixer is a full agent with tools, not a single-shot call, so it can run tests and read docs before opening a tidy self-summarizing PR. It generalizes to type-annotation rollouts and dependency bumps. How it goes wrong: fixers must re-trigger verification, and a bad batching cut leaves cross-batch dependencies that stall progress.

**Spine 3 - Coexistence scaffolding for migrations.** The claim: rather than a big-bang cutover, have an agent build temporary scaffolding so the old and new libraries both work at once, then migrate one component at a time, validating the running app after each, then rip the scaffolding out. Non-obvious because the instinct is to convert everything then fix the breakage; Brennan calls the scaffolding "pretty ugly, not something you would actually want to do," yet it is the enabling trick. The mechanism: if both Redux and Zustand coexist, every component migration is independently testable, which is exactly what makes it safe to fan out one parallel agent per component and get real human feedback per step instead of only at the end. It generalizes to any framework or major-version migration (this is the strangler-fig pattern, agent-driven). How it goes wrong: the shim adds throwaway complexity and must be fully removed, and some libraries resist clean coexistence.

## 🎬 Proposed ACS videos

**1. TITLE: Migrate a Library Without a Big Bang: The Coexistence Scaffolding Trick**
HOOK: Stop converting your whole app at once and praying the tests come back green.
THE PROMISE: For solo devs facing a Redux-to-Zustand style migration, ship it one component at a time with the app working the whole way.
THE SHAPE: (1) Why big-bang library swaps fail with agents; (2) have Claude Code build a compatibility shim so old and new coexist; (3) fan out one agent per component; (4) validate the running app after each; (5) rip the scaffolding out and merge.
SPINE: 3.
SLOT: Advanced Techniques → Cleaning Up Legacy Code (adjacent to "The One-Pattern Rule for Agents").
RELATIONSHIP: ❌ net-new. ACS teaches parallel file migration ("Combining Skills & Subagents" does tRPC v10 to v11) but never the coexistence-shim pattern that makes incremental, validated, parallel migration safe.
PROOF TO REUSE: the Redux-to-Zustand scaffolding story; "allowed us to test the application as each individual component got migrated"; the rip-out-and-merge finish.

**2. TITLE: Turn a Repo Green: A Dependency-Graph Refactor Pipeline**
HOOK: Refactoring hundreds of files is not one task, it is a graph you turn from red to green.
THE PROMISE: For engineers cleaning tech debt across a large codebase, build a verify-then-fix pipeline that batches the repo and tracks progress node by node.
THE SHAPE: (1) Visualize the repo as a dependency graph; (2) batch files by directory into PR-sized chunks; (3) write a verifier (LLM for code smells, command for tests); (4) traverse leaf-first, spawning a full-agent fixer per red batch; (5) one tidy PR per batch until every node is green.
SPINE: 2.
SLOT: Advanced Techniques → Multi-Agent Orchestration (next to "Refactoring with Subagents").
RELATIONSHIP: 🔗 complements "Builder Verifier Pattern" (Loopy AI), which teaches a single builder plus separate verifier with adversarial rounds. This adds B: scaling that loop across an entire repo as a dependency-graph state machine with per-batch status, so Ray need not re-teach the base builder-verifier idea.
PROOF TO REUSE: Calvin's 380-file / 60k-line demo; "we just have to ensure that every single node on this batch graph turns green"; verifier-as-LLM vs verifier-as-command; fixer-as-agent-with-tools.

**3. TITLE: Run a Fleet of Agents to Clear Your Backlog (90 Percent, Not 100)**
HOOK: The top 1% of engineers are not writing better prompts, they are managing agent fleets.
THE PROMISE: For teams drowning in tech debt, learn to decompose, parallelize, and human-review a swarm so years of toil finish in weeks.
THE SHAPE: (1) Why huge tasks are not one-shottable (context, laziness, compounding errors); (2) decompose into one-shot, verifiable, parallelizable units; (3) the git-branch accumulation workflow with a micro-agent context file; (4) build the CVE demo: one scanner agent, then a parallel agent per vulnerability opening a PR; (5) why 90% automation is the real target.
SPINE: 1.
SLOT: Advanced Techniques → Multi-Agent Orchestration (or Loopy AI, higher chapter).
RELATIONSHIP: 🔗 complements "Combining Skills & Subagents," which films one parallel-agent migration. This adds B: the fleet-scale operating model (hundreds of agents, PR-per-team, repeatable CVE/modernization pipeline, the 90% bar) rather than a single job.
PROOF TO REUSE: the 30x CVE resolution client; "the goal is not to automate this process 100%. It's something like 90%"; the IC-to-manager reframe; the scanner-then-parallel-solver architecture.

**Also film-able (not deep-dived):**
- *Sharing context across a fleet of agents.* Pitch: the spectrum from share-everything (collapses to serial), to human-entered notes, to a shared agent.md agents PR into, to direct agent-to-agent messaging (bleeding edge, non-deterministic, the "zen perfection" loop). SLOT: Advanced Techniques → Multi-Agent Orchestration. Likely 🔗 complement to "Subagent Teams for Debugging."

## 📚 Full wisdom (reference)

**SUMMARY**
Robert Brennan (OpenHands CEO) and Calvin show patterns for orchestrating swarms of parallel agents, with a human in the loop, to automate large-scale refactors, migrations, and CVE remediation.

**IDEAS**
- Agent orchestration splits one huge task into PR-sized pieces that separate parallel agents each one-shot cleanly.
- Aim for ninety percent automation, not one hundred; that alone is still an order-of-magnitude productivity lift.
- One client cut CVE resolution time thirty-fold by auto-scanning repos and opening ready-to-merge remediation pull requests.
- Migrate front ends by scaffolding both old and new libraries to coexist, then converting components individually.
- Traverse the dependency graph from leaf nodes upward so migrated utilities are ready before their dependents.
- Visualize a repo as a graph, batch files by directory, then color each batch by status.
- A verifier can be a programmatic command or a language model scanning code for rule violations.
- The most powerful fixer is a full agent with tools, not merely a single-shot model call.
- Beginners should cap themselves at roughly three to five concurrent agents before their attention span breaks.
- At scale, teams run hundreds or thousands of agents sending pull requests to individual downstream teams.
- Cloud sandboxed agents beat local ones: no babysitting, no rm-rf risk, and massively more parallel runs.
- Errors compound over long agent trajectories: a tiny early mistake repeats across every single subsequent step.
- Agents hit the laziness problem: told to migrate a hundred services, they finish three then quit.
- Share context between agents via a shared agent.md file they can update themselves through pull requests.
- Two agents given direct messaging tools once looped forever, endlessly wishing one another serene zen perfection.
- Accumulate all agent work onto one branch, add temporary scaffolding, then rip it out before merging.

**INSIGHTS**
- Orchestration mirrors managing engineers: separable parallel tasks, clear dependency ordering, then collated results reviewed by humans.
- The bottleneck is decomposition, not agents: breaking work into verifiable one-shot chunks demands real human judgment.
- Human-in-the-loop must review intermediate outputs per agent, not merely the final collated merge landing into main.
- Orchestration pays off only for repeatable, verifiable, parallelizable tasks with clear dependencies, not everyday feature work.
- Choosing what a single agent can actually one-shot is itself a hard, skill-dependent decomposition judgment problem.
- Sharing every agent's context with every other collapses orchestration back into one slow serial agent again.
- Even frozen at today's capability, LLMs will keep reshaping software engineering for years purely through operationalization.
- Going from coding yourself to directing agent fleets feels like the jump from engineer to manager.
- Bridging scaffolding lets you validate and parallelize the migration instead of one single risky big-bang cutover.

**QUOTES**
- "pretty much every line of code that I write goes through an agent." - Robert Brennan
- "even if you froze large language models today... you would still see the job of software engineering changing very drastically over the next two to three years" - Robert Brennan
- "Okay, I migrated three of your 100 services. I need to hire a team of six people to do the rest." - Robert Brennan (voicing a lazy agent)
- "the goal is not to automate this process 100%. It's something like 90% automation." - Robert Brennan
- "there's nothing stopping the agent from doing rmrf slash trying to delete everything in your home directory" - Robert Brennan
- "it feels kind of like... the jump that I made when I went from being an IC to being a manager" - Robert Brennan
- "they just entered into a loop of wishing each other zen perfection." - Robert Brennan
- "you can do... ending your years of work in a in a couple weeks" - Robert Brennan
- "These are not tasks. They're sprawling interconnected changes that can touch hundreds of files." - Calvin
- "our strategy for ensuring that there are no code smells... is straightforward. We just have to ensure that every single node on this batch graph turns green." - Calvin

**HABITS**
- Start every large refactor on a fresh branch that accumulates each agent's work before final merge.
- Add a micro-agent markdown giving high-level context so agents know exactly which migration they are performing.
- Prefer the web UI, let agents push, then pull locally only when hands-on work truly matters.
- Point agents at documentation links and the SDK repo before asking them to write integration code.
- Run a trivial hello-world LLM call first to confirm keys and connectivity before doing real work.
- Run your agents inside a Docker agent-server container rather than directly on the local host machine.
- Pause a running agent with control-P, insert corrections, then type continue to resume its ongoing work.
- Have each fixer produce a tidy, self-summarizing pull request ready for quick human review and approval.

**FACTS**
- OpenHands is an MIT-licensed coding agent that began as OpenDevin right after Devin's launch demo video.
- OpenHands' core agent definition alone spans about 380 files and roughly sixty thousand lines of code.
- Devin and OpenDevin launched in early 2024, introducing autonomous agents that run and debug their code.
- One client remediates CVEs across thousands of repositories with tens of thousands of developers using OpenHands.
- OpenHands migrated its own front end from Redux to Zustand using parallel per-component agents and scaffolding.
- Brand-new OpenHands app users get a ten-dollar free LLM credit after registering an account at app.all-hands.dev.
- Contextual autocomplete like GitHub Copilot let models reference local variable and table names inside real codebases.
- Programmatic verifiers call shell commands running unit tests, linters, or type checks for objective pass signals.

**REFERENCES**
- OpenHands (formerly OpenDevin), MIT-licensed coding agent; the OpenHands agent SDK and refactor SDK.
- OpenHands CLI; app.all-hands.dev cloud (sandboxed agent server, $10 free credit, LLM proxy key).
- Devin (Cognition) fully-autonomous SWE agent launch demo.
- GitHub Copilot (contextual autocomplete).
- Redux and Zustand (React state management); Spark 2 to Spark 3; Java version migrations.
- Trivy (Docker image CVE scan), npm audit (package.json scanning).
- LiteLLM (litellm docs for provider model strings).
- Docker (agent server container), Kubernetes (fleet scale).
- OpenHands micro-agent / repo.md convention (.openhands microagent); agents.md.
- Slides: dub.sh/openhands-workshop; the openhands CVE demo repo.
- Speakers: Robert Brennan (co-founder/CEO), Calvin (coworker).

**ONE-SENTENCE TAKEAWAY**
Decompose huge refactors into verifiable PR-sized batches, run parallel agents, and target ninety percent automation.

**RECOMMENDATIONS**
- Pick tasks that are repeatable, parallelizable, and cheaply verifiable before attempting any multi-agent orchestration at scale.
- Break your refactor into commits a single agent can one-shot, then rubber-stamp and merge each quickly.
- Batch files by existing directory structure to keep semantically related code inside the same agent's scope.
- Build a dependency-graph view so you can process leaf batches first and track completion by color.
- Use an LLM verifier when checking subjective qualities like code smells rather than pass-fail unit tests.
- First build coexistence scaffolding when migrating libraries, then convert the components carefully, one at a time.
- Let a scanner agent detect the language and choose its own vulnerability-scanning tool for each repository.
- Give each fixer agent real tools so it can run tests and read docs iterating autonomously.
- Share hard-won solutions across a fleet through one shared file rather than duplicating every agent's context.
