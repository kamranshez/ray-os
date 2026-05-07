---
tags: [agentic-coding, multi-agent, validation, missions]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
---

### SUMMARY

Luke from Factory presents missions, a multi-agent framework using orchestrators, workers, and validators with structured handoffs that complete software engineering tasks autonomously over many days.

### IDEAS

- Software engineering's bottleneck has shifted from intelligence to human attention; models now outpace what humans supervise.
- A team of five engineers might handle ten work streams, missions could lift that to thirty.
- Tests written after implementation confirm decisions instead of catching bugs because the code shaped its assertions.
- A validation contract defines correctness independently of the implementation, written during planning before any code exists.
- Fresh-context validators discover bugs because the original implementing agent carries a cost bias toward its own work.
- Most of mission's wall-clock time is spent waiting for real-world execution, not generating tokens at all.
- Running features serially with internal parallelization on readonly operations dramatically reduces error rate as runs lengthen.
- Parallel coding agents conflict, duplicate work, and make inconsistent architectural decisions, eating up any throughput gains.
- Structured handoffs record what was completed, what was undone, commands run, exit codes, and discovered issues.
- Filesystem-based handoffs survive context windows, letting each new worker inherit a clean slate and working codebase.
- The user-testing validator behaves like a QA engineer, spawning the application and clicking through real flows.
- Scrutiny validators run lints, types, tests, and spawn dedicated code review agents for every completed feature.
- Putting orchestration logic in prompts means each model upgrade improves the system without any code rewrites overnight.
- Four sentences of prompt text can alter mission execution strategy more than hundreds of code lines.
- Direct agent-to-agent communication fragments state quickly because no central coordinator maintains a single source of truth.
- Negotiation works best when agents have positive sum trading opportunities, not adversarial conflicts over shared resources.
- Broadcast keeps long missions coherent by pushing shared constraints and status updates out to every active agent.
- The longest mission ran sixteen days continuously; the team believes thirty-day runs remain achievable with current architecture.
- Half of final code becomes tests and ninety percent gets covered when validation drives implementation correctly.
- Validation never succeeds first time in production missions, demonstrating that follow-up features pay for QA loops.
- A simple taxonomy of multi-agent patterns covers most systems: delegation, creator-verifier, direct communication, negotiation, broadcast.
- Verifier separation works because the implementing agent wants its code to succeed; verifiers want bugs found.
- Mission control replaces chat interfaces because long runs need progress visibility and budget burn at glance.
- Errors get caught at milestone boundaries where corrective work is scoped and the mission self-heals automatically.
- Open-weight models can run missions successfully because validation contracts and milestone checkpoints compensate for individual weakness.
- A clean codebase emerges from missions because the tests, skills, and structure help subsequent agents and humans.
- Forcing agents to write down completed and undone work prevents drift that hoping for memory cannot.
- Agents have cost bias toward their own implementations, mirroring why human code review needs separate reviewers.
- A verifier must answer narrow unambiguous questions; vague criteria like is-this-good fail entirely as useful gates.
- Coordination overhead from parallel agents eats speed gains while burning tokens, contradicting the simple parallelism intuition.

### INSIGHTS

- Adversarial validation by design beats friendly verification because separation of concerns prevents motivated reasoning in implementation.
- Long autonomous runs require external memory because hoping agents remember context produces drift, not coherent execution.
- Architectural choices in prompts compound with model improvements; choices in code create technical debt over time.
- Defining done before writing code is the only validation move that survives long autonomous execution windows.
- Sequential execution with targeted parallelization beats raw parallelism whenever shared state and architectural coherence matter most.
- Multi-agent systems need broadcast and shared state to maintain coherence across many days of continuous execution.
- Behavior validation through real application interaction matters more than test passing for genuine end-to-end correctness assurance.
- Cost bias is structural; reusing the implementing agent as verifier guarantees blind spots, regardless of intelligence.
- The bottleneck of human attention reframes engineering productivity around supervision capacity, not raw individual intelligence available.
- Structured handoffs convert agent communication from hopeful into auditable, making self-healing possible at milestone boundaries naturally.
- A multi-agent taxonomy clarifies design choices: every agent system implements some combination of the five named primitives.
- Filesystem state outperforms context-passing because it persists past compaction and survives any individual agent crashing entirely.
- Tests confirm what was built rather than catch bugs, unless written before any implementation satisfies them.

### QUOTES

- "The bottleneck in software engineering nowadays is not intelligence. It's now limited by human attention." — Luke
- "Today's models are smart enough to figure out all 50 of these tasks, but there's not enough uh just bandwidth to supervise their implementation." — Luke
- "What if a human decides what to build and then a system figures out how to do so" — Luke
- "An agent could just work for hours, for days, and you come back to finish work." — Luke
- "Tests written after implementation don't catch bugs. They confirm decisions." — Luke
- "If you rely on validation like that, your system will eventually drift." — Luke
- "It's written during planning before any code and it defines correctness independently of implementation." — Luke
- "Critically neither validator has seen the code before. They are not invested in the implementation and so validation is adversarial by design." — Luke
- "When a worker finishes a feature, it doesn't just say, 'I'm done.'" — Luke
- "Not by hoping that agents remember what happened, but by forcing them to write it down and then actually address issues." — Luke
- "Our longest mission ran for 16 days, which is much longer than a full sprint. And we believe that they can run for 30." — Luke
- "If you have 10 agents running at one point in time, then you have 10 times the throughput. But we tried that and it doesn't really work." — Luke
- "They step on each other's changes. They duplicate work. They make inconsistent architectural decisions." — Luke
- "It seems slower on paper, but the error rate drops dramatically." — Luke
- "Almost all of the orchestration logic is defined in prompts and skills um instead of like a hard-coded state machine." — Luke
- "Four sentences of this can alter the execution strategy pretty dramatically." — Luke
- "Missions sort of ensure the the discipline and the models provide the intelligence" — Luke
- "Notice how validation never succeeds on the first go." — Luke
- "Most of the mission's wall clock time is actually spent here waiting for this like real world execution to occur instead of generating tokens." — Luke
- "A fresh agent with fresh context is way more likely to find issues. And this is why we do code review as humans as well." — Luke
- "Hard to get right though because state fragments across conversations without that coordinator and there's no single source of truth." — Luke
- "It's a bit less uh flashy than the other ones, but it's critical for maintaining coherence over longunning tasks." — Luke
- "It kind of acts like a QA engineer. It spawns the application." — Luke
- "The codebase ends up cleaner than when you started." — Luke
- "You're only as strong as your weakest link." — Luke

### HABITS

- Write the validation contract during planning before any line of code gets implemented anywhere in production.
- Commit via git after every completed feature so the next worker inherits a clean working codebase reliably.
- Spawn fresh validator agents that have never seen the code being reviewed at any milestone boundary.
- Run features serially while parallelizing only readonly operations like codebase search and external API research tasks.
- Record exit codes alongside commands when documenting handoffs between workers, not just the natural language summary.
- Decompose features so each one maps to one or more validation contract assertions explicitly stated upfront.
- Use prompt caching aggressively whenever running long missions to offset the token cost of multi-day execution.
- Spawn dedicated code review subagents per completed feature instead of asking one agent to review everything.
- Use computer use or browser automation to interact with running applications during validation phases at boundaries.
- Argue with the orchestrator about scope before approving any plan to ensure requirements are understood properly.
- Approve a plan once and step away while missions execute autonomously over hours or days unattended.
- Block progress when handoff issues remain unaddressed rather than allowing the next worker to proceed regardless.
- Use mission control style dashboards instead of chat for any agent task that runs many hours.
- Define worker behavior through skills that the orchestrator selects per mission rather than rigid hardcoded templates.
- Keep deterministic logic thin and focused on bookkeeping while letting the model handle every meaningful decision.

### FACTS

- Goose started at Block about two-and-a-half years ago and now belongs to the Agentic AI Foundation officially.
- Goose is currently one of the leading open-source coding agents available in the developer ecosystem today.
- Factory's mission is bringing autonomy to the entire software development lifecycle, not just code writing tasks.
- Luke leads the core agent harness team at Factory, where he architected the missions framework presented.
- Around 700 lines of orchestration text govern how missions decompose features and handle failures during execution.
- About 60 percent of mission time and tokens are spent on the implementation phase, not validation.
- Tests typically comprise 50 percent of code lines after a successful mission completes its validation contract.
- Roughly 90 percent of code is covered by tests at the end of a successful mission.
- The longest production mission ran continuously for 16 days, longer than a typical engineering sprint cycle.
- Theo, an engineer at Factory, built the original missions prototype and chose default models for roles.
- A complex validation contract may include hundreds of assertions, each tied to one or more features.
- Factory's missions framework currently uses three roles: orchestrator, workers, and validators with distinct responsibilities and contexts.
- Five named multi-agent patterns exist in the literature: delegation, creator-verifier, direct communication, negotiation, and broadcast collectively.
- Missions can run on open-weight models because validation contracts effectively compensate for sub-frontier model capability gaps.
- A Slack clone was used as a public production demo for what missions can build end-to-end.

### REFERENCES

- Goose (open-source coding agent originated at Block, now Agentic AI Foundation)
- Block (Luke's previous employer)
- Factory (https://factory.ai) — Luke's current company
- Agentic AI Foundation (Goose's current home)
- Mission Control (Factory's UI for missions)
- Open Droid (Factory's CLI to run missions)
- Theo (Factory engineer who built the missions prototype)
- AGENTS.md and skills (primitives missions builds on)
- Slack clone example (publicly cited mission demo)

### ONE-SENTENCE TAKEAWAY

Define done before any code, separate implementation from validation, and put orchestration logic in prompts.

### RECOMMENDATIONS

- Stop using parallel coding agents on shared codebases; run features serially with internal readonly parallelization instead.
- Move orchestration logic out of state machines into prompts so model upgrades improve your system free.
- Write validation contracts during the planning phase, not after implementation has shaped the assertion choices already.
- Spawn separate validator agents that have never seen the implementation code to eliminate cost-bias verification failures.
- Build a user-testing validator that interacts with running applications via computer use, not just static checks.
- Persist handoffs to the filesystem rather than passing context, so workers inherit clean slates between iterations.
- Record exit codes, completed work, and undone work in every handoff to enable system self-healing reliably.
- Treat validation as adversarial by design, not collaborative; the verifier's job is finding bugs, not approving.
- Catch errors at milestone boundaries through scoped corrective work, allowing missions to self-heal back into spec.
- Approve a plan and walk away; the architecture should not need supervision for hours or days.
- Replace chat interfaces with a mission control dashboard for any agent run lasting longer than minutes.
- Customize default models for each role rather than relying on framework defaults from any single provider.
- Argue scope with the orchestrator before approving plans, treating it like a strategic sounding board partner.
- Block worker progress when previous handoff issues remain unaddressed rather than letting drift accumulate over iterations.
- Use prompt caching extensively to make multi-hour and multi-day agent runs remain economically sustainable at scale.
- Define each feature against specific validation contract assertions so the sum covers every required correctness property.
- Encode worker behavior through skills the orchestrator picks per mission, enabling deep customization without rewriting any code.
