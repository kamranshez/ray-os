---
title: OpenAI Codex Masterclass — Vaibhav Srivastav & Katia Gil Guzman
video_url: https://www.youtube.com/watch?v=MhHEGMFCEB0
video_id: MhHEGMFCEB0
channel: AI Engineer
published: 2026-04-29
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**OpenAI Codex Masterclass — Vaibhav Srivastav & Katia Gil Guzman**](https://www.youtube.com/watch?v=MhHEGMFCEB0) - AI Engineer - uploaded 2026-04-29

> Three complement-tier ACS videos here: a custom Codex subagent fleet, letting Codex author its own config from your history, and guardian approvals. Code review and automations are already covered.

---

## 1. The ideas worth a video

**Spine 1 — Build a fleet of custom Codex subagent personas, each with its own model, permissions, and tools.**
This is the reframe the whole subagent section hangs off: the lever is not "spin up many agents" but matching model tier, sandbox mode, and MCP/skill access to each job's risk (review agents read-only, docs writers write-enabled, mini/spark for cheap parallel grunt work).
VERDICT: 🔗 next-step video available.

**Spine 2 — Have Codex read your own past sessions and author your reusable config (subagents, automations, skills).**
The meta-move VB repeats three times: you do not hand-design your automation library, you have the agent reverse-engineer it from what you already do.
VERDICT: 🔗 next-step video available.

**Spine 3 — Replace yolo mode with guardian approvals: a verifier subagent judges which privileged actions actually need you.**
Neither blanket yolo nor per-action approval scales once agents run unattended; the fix is an agent that gates the agent.
VERDICT: 🔗 next-step video available.

*(Also promoted: **code review as the mandatory first pass** — load-bearing for the video but ✅ already covered by ACS, so deep-dived below and excluded from the pitches.)*

**Also film-able (not deep-dived):**
- **Codex hooks (start / per-tool-use / stop) and the keep-going stop loop** — 🟡 the loop concept is covered by Loopy AI and Claude Code "Hooks", but a Codex-native hooks walkthrough (hooks.json, session lifecycle, keep_going script) is a natural, uncovered addition to Master Codex. One-liner pitch: "Codex Hooks: deterministic lifecycle automation" in Master Codex.

---

## 2. Summary + counts

OpenAI DevEx engineers Vaibhav Srivastav and Katia Gil Guzman demo Codex as a full software-engineering system: plugins, automations, subagents, code review, and bleeding-edge safety features.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 1 covered

---

## 3. 🔬 Deep dive

### Spine 1 — Right-size each subagent (model, permissions, tools) and dispatch a fleet

**The claim.** The real power of subagents is not parallelism itself but constraining each one: pick its model, its sandbox mode, and its exact tools per the job's risk. **Why it's non-obvious.** Most people treat subagents as identical clones of the main model, so they either over-permission everything (a "reviewer" that can write) or waste a frontier model on trivial parallel grunt work. **Why it's true.** Because a review or security agent that can execute is a live hazard, forcing read-only removes the entire class of "the reviewer changed my code" failures; and because short exploration tasks do not need frontier reasoning, routing them to mini/nano/Spark lets you fan out twenty agents at a fraction of the cost. The constraint IS the capability. **What it generalizes to.** The same discipline governs a CI pipeline: least-privilege service accounts per stage, cheap runners for lint, expensive ones for integration tests. **How it goes wrong.** Over-partitioning a task the main model could do in one pass adds coordination overhead; and concurrency caps (VB's setup capped at six) silently serialize a "twenty-agent" request.

### Spine 2 — Let Codex author its own reusable config from your session history

**The claim.** Instead of hand-crafting subagents, automations, and skills, point Codex at your own past sessions and have it propose the reusable primitives you should codify. **Why it's non-obvious.** The default mental model is that YOU are the architect of your tooling; here the agent mines your revealed behaviour and designs the tooling for you. **Why it's true.** Your session history is a dense log of the workflows you actually repeat, so a model reading it can detect recurrence a human would never bother to audit, then emit a concrete artifact (a TOML persona, an automation schedule) that captures the pattern. Because the artifact is generated from real traces rather than imagined needs, it fits your actual work instead of an idealized version. **What it generalizes to.** The same loop builds team runbooks from support-ticket history, or shell aliases from your bash history. **How it goes wrong.** It over-fits to noisy one-off sessions and proposes junk primitives; and it needs access to the raw session store (Codex keeps these in a sessions folder), which VB noted works cleanly from the CLI but not every surface equally.

### Spine 3 — Guardian approvals: an agent that gates the agent

**The claim.** Rather than yolo mode (unfettered access) or fatiguing per-action prompts, guardian approvals spin up a verifier subagent that decides, per privileged action, whether it genuinely needs a human. **Why it's non-obvious.** The industry frames safety as a binary toggle (ask vs skip); this reframes it as a judgment task you can delegate to a cheaper model. **Why it's true.** Because most privileged actions are routine (read a file, start a dev server) and only a few are dangerous (expose a file to the internet, remove a directory), a classifier can auto-approve the safe majority and escalate only the rare risky ones, which collapses approval fatigue without collapsing safety. The verifier runs on a fresh prompt per action, so its judgment is not poisoned by the main agent's momentum. **What it generalizes to.** This is exactly how a build system's policy engine gates deploys, or how a bank's fraud model auto-clears normal transactions and flags anomalies. **How it goes wrong.** A miscalibrated verifier waves through a genuinely destructive command, or over-escalates and reintroduces the fatigue it was meant to remove; it is experimental (/experimental) and unproven at scale.

### Spine 4 (✅ COVERED — deep-dive only, no pitch) — Code review as the mandatory first pass

**The claim.** Once you run many parallel agents you cannot read every line, so an automated reviewer that contextualizes the diff against the whole repo becomes required infrastructure, not a nicety. **Why it's non-obvious.** People treat AI review as a linting upgrade; VB's point is stronger — it is the only thing standing between parallel throughput and shipped breakage. **Why it's true.** Because Codex review reads the whole repo rather than just the diff, it catches second-order effects in modules the PR never touched; and because it is enforced by default (100% of OpenAI PRs, "including Greg"), it becomes a floor everyone clears rather than an optional step people skip under deadline. **What it generalizes to.** Any team gate: mandatory security scans, required test coverage thresholds. **How it goes wrong.** Blind trust in the reviewer replaces human judgment on architecture; and review-of-review loops can burn cost. **Why covered:** ACS already teaches this via `/code-review` (finder/verifier fan-out), `/code-review ultra`, and the `Codex CLI Plugin` for Claude Code (which is literally the "Claude Code plugin for Codex review" shown here). No new video needed.

---

## 4. 🎬 Proposed ACS videos

### 1. Build Your Own Codex Subagent Fleet

- **HOOK:** Codex ships three subagents. The pros run twenty, and every one is locked down differently.
- **THE PROMISE:** For Codex users past the basics: build a repo of custom subagent personas so you can fan out safe, cheap, parallel work on demand.
- **THE SHAPE:**
  1. The three defaults (fallback, worker, explorer) and why they are not enough.
  2. Anatomy of a persona TOML: name, description, model, reasoning effort, sandbox mode.
  3. The safety rule: reviewers and security agents in read-only; docs writers get write.
  4. Cost tiering: mini/nano/Spark for short parallel tasks vs frontier for the hard ones.
  5. Demo: "spin up 20 subagents to review all the personas," plan mode auto-partitioning files, concurrency caps.
  6. Give a subagent MCP access (Sentry, Linear) and skills.
- **SPINE:** 1
- **SLOT:** Master Codex → Codex App (new "Custom Subagents" beat alongside the existing "Subagents" video).
- **RELATIONSHIP:** 🔗 complements "Subagents" (Master Codex → Codex App), which teaches the built-in default/explorer/worker roles, reasoning effort, and parallel bounded tasks. This is the next step: authoring your OWN persona library with per-agent model, sandbox, and MCP/skill constraints. Do not re-teach what a subagent is.
- **PROOF TO REUSE:** the 45-persona repo review demo; "for a review agent you would almost always 100% want to use the review agent in read-only mode"; the six-concurrent-threads cap forcing batching; the PR-explorer persona on Spark, read-only.

### 2. Let Codex Write Its Own Subagents From Your History

- **HOOK:** Stop designing your agent setup by hand. Make Codex read what you already do and build it.
- **THE PROMISE:** For anyone with a messy pile of repeated workflows: have the agent mine your session history and hand you the reusable subagents and automations worth keeping.
- **THE SHAPE:**
  1. The problem: you repeat the same prompts weekly and never codify them.
  2. Where Codex stores sessions (the sessions folder) and how to point it at them.
  3. The prompt: "look through my past sessions and recommend subagents and automations."
  4. Triage the proposals; reject over-fit one-offs; keep the recurring winners.
  5. Codex writes the TOML / automation for you; you review and commit.
  6. Cross-tool note: the same move works in Claude Code.
- **SPINE:** 2
- **SLOT:** Master Codex → Codex App, or Advanced Techniques → Skills as Force Multipliers.
- **RELATIONSHIP:** 🔗 complements "/fewer-permission-prompts" (Master Claude Code → Niche Features), which mines prior transcripts for ONE narrow output — permission allow-rules. This generalizes the same "let the agent read your history and author config" move to your whole reusable toolkit (subagents, automations, skills). State that the existing video only does permission rules so Ray does not re-teach transcript-mining itself.
- **PROOF TO REUSE:** "the best thing that I like to do is to just ask Codex to look through my past sessions and recommend me certain automations, certain sub agents"; the CLI-scans-sessions Q&A answer; "you can actually ask codeex to create the skill for you as well."

### 3. Kill Yolo Mode With Guardian Approvals

- **HOOK:** You gave your agent unfettered access to do "literally whatever the hell it wants." Here is the safer default.
- **THE PROMISE:** For people running Codex unattended: swap blanket yolo for a verifier agent that only interrupts you on genuinely risky actions.
- **THE SHAPE:**
  1. The two bad extremes: yolo (unsafe) and per-action prompts (fatigue).
  2. Enable guardian approvals via /experimental.
  3. How it works: a fresh verifier subagent judges each privileged action.
  4. Demo the escalation: run a dev server (auto-approved) vs expose a file to the internet / rm a directory (escalated).
  5. Where it fits with sandbox modes and read-only subagents as layered defense.
- **SPINE:** 3
- **SLOT:** Master Codex → a Safety / Bleeding-Edge chapter.
- **RELATIONSHIP:** 🔗 complements "Auto Permission Mode" (Master Claude Code → The Fundamentals), which teaches the LLM-classifier-approves-or-blocks concept FOR CLAUDE CODE. This is the Codex-native equivalent plus the distinct mechanism — a fresh verifier subagent spun up per privileged action. Reference Auto Mode so Ray frames it as "same idea, Codex's version" rather than re-explaining classifier approvals from scratch.
- **PROOF TO REUSE:** "all of us including myself at some point were guilty of using yolo mode all the time"; "you by default give unfettered access to your coding agent to do literally whatever the hell it wants"; the per-action verifier-subagent description; the reduce-human-fatigue rationale.

---

## 5. 📚 Full wisdom (reference)

**SUMMARY** — OpenAI DevEx engineers Vaibhav Srivastav and Katia Gil Guzman demo Codex as a full software-engineering system: plugins, automations, subagents, code review, and bleeding-edge safety features.

**IDEAS**
- Codex is a software engineering agent, not just a coder: it runs commands, tests, explores codebases.
- A unified agent harness wraps tool execution, environment setup, and safety around the underlying foundation models.
- The team ships websockets giving 1.75x faster tokens, plus a fast mode adding another 2x throughput.
- Native git work trees let you run multiple features within one project without any context switching.
- Plugins bundle skills, apps, and MCP servers into one installable unit for reusable end-to-end coding workflows.
- Skills are reusable packaged instructions with scripts and resources; Codex can even author them for you.
- The game studio plugin used Image Gen for sprites and Playwright interactive to debug live gameplay.
- Playwright interactive gives Codex a headless browser to click, navigate, screenshot, and analyze its own app.
- Automations turn a successful chat workflow into a scheduled background job, much like a personal cron.
- Katia runs automations triaging Slack messages and Gmail daily, saving hours of manual inbox review work.
- Codex code review reads the whole repo, catching second-order effects far beyond the changed diff itself.
- Every single pull request across all OpenAI repos is reviewed by Codex code review by default.
- A new Claude Code plugin lets you invoke Codex review inside your Claude Code sessions directly.
- Subagents decompose one master task into parallel, independent subtasks that each report back once they finish.
- Each custom subagent can set its own model, reasoning effort, sandbox mode, MCP servers, and skills.
- Review and security subagents should always run read-only; docs writers get write access to produce output.
- Codex auto-detected the complex task, kicked off plan mode, then partitioned files across twenty separate reviewers.
- Guardian approvals spin up a verifier subagent to judge whether each privileged action needs human interruption.
- A stop hook running a keep-going script pushes long-running tasks to continue without any manual nudging.
- Codex currently supports three lifecycle hooks: at session start, after each tool use, and at stop.
- Best-of-n runs the same cloud task several times so you simply pick the single strongest output.
- You can ask Codex to scan your past sessions and recommend subagents and automations worth building.

**INSIGHTS**
- As you parallelize agents, reviewing every line becomes impossible, so automated review turns into non-negotiable infrastructure.
- The real subagent lever is matching model, permissions, and tools to each specific job's actual risk.
- Blanket yolo mode does not scale, and approval fatigue is solved by an agent judging actions.
- Model tiering matters: cheap fast mini and nano models suit short subagent tasks, saving real cost.
- The agent can bootstrap its own configuration by reading your session history and proposing reusable primitives.
- Codex review contextualizes the diff against the entire repo, surfacing breakage even in untouched dependent modules.
- Read-only enforcement is the single core safety primitive for any reviewing, security, or exploration-focused subagent role.
- Hooks convert vague CLAUDE-style reminders into deterministic, event-triggered behavior fired at session boundaries and tool calls.
- Codex spans surfaces (app, CLI, IDE, Slack, GitHub) so one same agent follows your entire workflow.

**QUOTES**
- "It's not just a coding agent... It can really do everything that a software engineer would do." — Katia Gil Guzman
- "Every time we make improvements, every time we have better models, Codex benefits from it." — Katia Gil Guzman
- "This is like saving me hours per day." — Katia Gil Guzman
- "In my own biased way, Codex code review is one of the best in the industry right now." — Vaibhav Srivastav
- "100% of pull requests across all OpenAI repos... including Greg... are reviewed by Codex code review by default." — Vaibhav Srivastav
- "All of us including myself at some point were guilty of using yolo mode all the time." — Vaibhav Srivastav
- "You by default give unfettered access to your coding agent to do literally whatever the hell it wants." — Vaibhav Srivastav
- "For a review agent you would almost always 100% want to use the review agent in read-only mode." — Vaibhav Srivastav
- "Sky is literally the limit — you can spin up as many agents as you want." — Vaibhav Srivastav
- "The best thing that I like to do is to just ask Codex to look through my past sessions and recommend me certain automations, certain sub agents." — Vaibhav Srivastav
- "Just last night we crossed the milestone of crossing 3 million weekly active users." — Vaibhav Srivastav

**HABITS**
- Vaibhav constantly pings Codex in Slack throughout the day to fix things or ask quick questions.
- Katia runs a daily 9am automation summarizing all Slack, bucketed per topic with time-sensitive urgent flags.
- She also runs a Gmail automation flagging legitimate, time-sensitive emails she should actually reply to today.
- Vaibhav always defaults review and security subagents to read-only so they can never execute anything themselves.
- He brainstorms new features by spinning up several subagents to explore distinct implementation approaches in parallel.
- He uses a stop hook to keep long-running tasks going, running one validating command per turn.
- He routinely asks Codex to review uncommitted changes before committing, spinning up a fresh review thread.
- Both presenters recommend creating your own custom subagents rather than relying only on the three defaults.

**FACTS**
- Codex crossed three million weekly active users, having more than tripled since January of this year.
- GPT-5.4 is currently the state-of-the-art Codex model, and a mini version was released only last week.
- The GPT-5.3 Codex Spark model was built in partnership with Cerebras for its blazing token speed.
- Codex now offers native Windows support with a native Windows sandbox, the first of its kind.
- Vaibhav's setup capped concurrent subagent threads at six, so the twenty requested reviewers ran in batches.
- The demo repo held roughly 45 curated subagent persona files, ranging from accessibility reviewer to architect.
- Codex ships three default subagent personas: a general fallback, an execution worker, and an explorer role.
- Updating one spreadsheet took Codex two minutes to analyze the codebase and write 57 event rows.
- Both presenters work on OpenAI's developer experience team, based in London, directly supporting developers using Codex.

**REFERENCES**
- Models: GPT-5.2, GPT-5.2 Codex, GPT-5.3 Codex, GPT-5.3 Codex Spark (with Cerebras), GPT-5.4, GPT-5.4 mini, GPT-5.4 Nano.
- Surfaces: Codex app, Codex CLI, IDE extension, Slack, GitHub.
- Features: unified agent harness, websockets, fast mode, git work trees, plugins, plugin creator, Skills, automations, code review, /review, best-of-n cloud runs, native Windows sandbox.
- Plugins/skills: game studio plugin, web app plugin, Playwright interactive, Image Gen, Google Drive plugin, Claude Code plugin for Codex review, Codex Security, Cloud Code plugin.
- Integrations: Figma, Linear, Notion, Slack, Gmail, MCP servers, Sentry, docs MCP server.
- Bleeding edge: guardian approvals (/experimental), hooks (hooks.json, session_start.py, keep_going_ui.py), personality/personalization settings.
- People: Vaibhav Srivastav (x.com/reach_vb), Katia Gil Guzman, colleague Dom, Greg (Brockman, referenced).

**ONE-SENTENCE TAKEAWAY** — Codex became a full engineering system: right-size subagents, automate review and approvals, and delegate everything.

**RECOMMENDATIONS**
- Build a dedicated repo of custom subagent personas, each with its own model, permissions, and tools.
- Set every reviewing or security subagent to strict read-only mode so it can never execute changes.
- Ask Codex to scan your past sessions and then propose reusable subagents and automations worth codifying.
- Turn any repeated daily workflow, such as Slack or email triage, into a scheduled Codex automation.
- Enable guardian approvals via /experimental to stop blindly running yolo mode on every privileged risky action.
- Install the Claude Code plugin to run state-of-the-art Codex review directly inside your Claude Code sessions.
- Use cheap mini and nano models for short subagent tasks to parallelize widely without heavy cost.
- Add a stop hook that tells Codex to keep going for unattended, long-running tasks running overnight.
- Have your review subagents contextualize diffs against the whole repo to catch second-order breakage much earlier.
