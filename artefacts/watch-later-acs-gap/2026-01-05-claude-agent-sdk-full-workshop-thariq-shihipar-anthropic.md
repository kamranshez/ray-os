---
title: "Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic"
video_url: https://www.youtube.com/watch?v=TqC1qOfiVcQ
video_id: TqC1qOfiVcQ
channel: AI Engineer
published: 2026-01-05
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Claude Agent SDK [Full Workshop] — Thariq Shihipar, Anthropic**](https://www.youtube.com/watch?v=TqC1qOfiVcQ) - AI Engineer - uploaded 2026-01-05

> net-new ACS video available: build a real agent on the Claude Agent SDK, with two complements alongside.

## 1. The idea worth a video

- **Build a production agent on the Claude Agent SDK.** A deployed agent is mostly a Claude Code prototype plus a fifty-line runner, not a bespoke framework. VERDICT: ❌ net-new video available.
- **Bash is the universal agent tool, not a pile of bespoke tools.** One shell tool composes into unlimited actions, which is why Claude Code feels so capable. VERDICT: 🔗 next-step video available.
- **The file system, not the prompt, is the agent's memory.** Save tool results to files, return the path, and let files be ground truth for verification. VERDICT: 🔗 next-step video available.

## 2. Summary + counts

Thariq Shihipar's Anthropic workshop teaches building agents on the Claude Agent SDK: bash as the universal tool, the file system as memory, verification everywhere, prototype-then-productionize.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 3. 🔬 Deep dive

### Spine 1: Prototype in Claude Code, then productionize on the Agent SDK

The claim: a production agent is mostly a Claude Code prototype plus a fifty-line SDK runner, not a hand-built framework. Why it is non-obvious: most people assume productionizing means rebuilding the agent loop, tool routing, compaction, and permissions from scratch. Why it is true: Anthropic found they rebuilt those same parts over and over, so the Agent SDK packages the whole harness (loop, prompts, file system, sub-agents, memory, compacting). Because the harness is fixed, the real work moves into a CLAUDE.md and helper scripts you already tuned interactively. So you prototype in Claude Code until you have high conviction, summarize the working session into CLAUDE.md, keep the scripts, and write a tiny agent.ts that runs the query in the working directory. You deploy by pointing it at a sandbox, for example Cloudflare's sandbox.start plus bun agent.ts. It generalizes cleanly: the same shape produces a Slack issue-triage bot or a data-dashboard agent, not just coding tools. How it goes wrong: the sandbox container adds real overhead (Thariq's "React vs jQuery" tradeoff), and a thin CLAUDE.md leaves the agent guessing, once it wrote raw JavaScript instead of calling his API.

### Spine 2: Give the agent bash instead of building bespoke tools

The claim: the bash tool, not a library of custom tools, is the most powerful thing you can hand an agent. Why it is non-obvious: the intuitive design adds one structured tool per capability (search, lint, execute), which balloons context and confuses the model. Why it is true: bash is effectively the first "code mode." Because the agent can pipe, grep, store results to files, and call existing software like ffmpeg, git, npm, or LibreOffice, a single tool composes into unlimited actions, and it discovers capabilities at runtime via a help flag rather than spending context up front. An email agent that greps a search script's output and sums the prices beats one drowning in a hundred raw emails. The decision rule follows: keep real tools for atomic, irreversible actions (write file, send email) where you need approval and guarantees; use bash for composable exploration; use code generation for dynamic, flexible logic. It generalizes to any data agent, for instance converting a CSV to SQLite so the model queries via SQL. How it goes wrong: bash adds latency (discovery, linting) and demands the Swiss-cheese safety stack (AST parsing, sandboxing), because a shell is both powerful and dangerous.

### Spine 3: Use the file system as the agent's memory and verifier

The claim: the file system, not the context window, is where a robust agent stores memory, grounds itself, and verifies its work. Why it is non-obvious: people treat context engineering as prompt wording and try to keep everything inside the window. Why it is true: Thariq now saves every tool call result to a file and returns only the path, so the context stays small while the full data stays searchable and greppable later. Files become ground truth: the agent can cat a file to confirm it was actually created, re-read prices with line numbers to check its own math, and write memories to a folder. Skills exploit the same mechanic, they are folders the agent CDs into and reads on demand, which is progressive disclosure. It generalizes to scale: for a fifty-million-line codebase the same principle says skip a brittle semantic index and lean on good CLAUDE.md files plus a scoped starting directory. How it goes wrong: long outputs still leak into history when you forget to offload them, and the file-system-as-memory pattern only works when bash and files share one container.

## 4. 🎬 Proposed ACS videos

### 1. Turn a Claude Code Prototype Into a Deployed Agent With the Agent SDK
- **HOOK:** Your best agent is already running in Claude Code; productionizing it is about fifty lines away.
- **THE PROMISE:** For builders who prototype in Claude Code and want a real agent they can deploy to users.
- **THE SHAPE:** (1) prototype the task in Claude Code with an API plus a CLAUDE.md; (2) reach high conviction by reading transcripts; (3) summarize the working session into CLAUDE.md and keep the helper scripts; (4) write a ~50-line agent.ts on the Agent SDK; (5) deploy to a sandbox with Cloudflare sandbox.start plus bun agent.ts.
- **SPINE:** Prototype-then-productionize on the Agent SDK.
- **SLOT:** New "Agent SDK" chapter, most naturally in Advanced Techniques (or a new class stub).
- **RELATIONSHIP:** ❌ net-new. ACS has 164 Claude Code videos but nothing on building programmatically on the Claude Agent SDK; searches for the SDK only surface install, Slack, and subagent videos.
- **PROOF TO REUSE:** "building an agent should be simple ... but simple is not the same as easy"; the 50-line agent file; Cloudflare's sandbox.start plus bun agent.ts; the Pokemon agent built live from the Poke API.

### 2. Stop Building Tools, Give Your Agent Bash
- **HOOK:** One shell tool beats fifty bespoke tools, and it is exactly why Claude Code feels so capable.
- **THE PROMISE:** For anyone wiring tools into an agent who wants more capability with far less context bloat.
- **THE SHAPE:** (1) the tools vs bash vs code-generation tradeoff; (2) the atomic-action rule for when a real tool still wins; (3) an email or data demo that greps a script's output instead of a hundred raw results; (4) CSV to SQLite as a bonus interface trick; (5) the safety stack (AST parse, network and file-system sandbox).
- **SPINE:** Bash-first action layer.
- **SLOT:** Advanced Techniques, Tooling & Setup.
- **RELATIONSHIP:** 🔗 complements "Your Interaction Layer" (My Daily Workflows), which shows Claude using bash and general computer use to drive OBS, Premiere, and OS tasks. That video teaches that Claude can drive your apps; this adds the design principle, when to reach for an atomic tool vs bash vs code generation.
- **PROOF TO REUSE:** "the bash tool is the most powerful agent tool"; the grep-the-prices email example; Playwright help-flag discovery; the Swiss cheese defense and lethal trifecta framing.

### 3. Use the File System as Your Agent's Memory
- **HOOK:** The best place to store an agent's context is not the prompt, it is a folder on disk.
- **THE PROMISE:** For agent builders whose sessions bloat or forget, who want durable memory and built-in self-verification.
- **THE SHAPE:** (1) save every tool result to a file and return the path; (2) grep and cat as recall and ground truth; (3) check-your-own-math with line-numbered files; (4) skills as progressive disclosure; (5) the fifty-million-line corollary, CLAUDE.md plus a scoped directory beats a semantic index.
- **SPINE:** File system as memory.
- **SLOT:** Context Engineering class, new chapter on filesystem-as-memory.
- **RELATIONSHIP:** 🔗 complements "Context Window Management" (My Daily Workflows), which teaches when to compact, delegate, or restart a session. This is the next step: make the file system the durable external memory so context pressure never builds in the first place.
- **PROOF TO REUSE:** "whenever I have a tool call, I save the results ... and have the tool call return the path"; files-as-ground-truth verification; the claim that semantic search is "brittle."

### Also film-able (not deep-dived)
- **Give Your Agent Data It Already Understands (CSV to SQL):** transform awkward data into a representation the model has mastered (CSV into SQLite) so agentic search just works. SLOT: My Daily Workflows or Context Engineering. 🔗 complements "Data Analysis" (read-only DB access) by adding the format-translation move rather than just the access pattern.

## 5. 📚 Full wisdom (reference)

### SUMMARY
Thariq Shihipar (Anthropic) delivers a two-hour AI Engineer workshop on the Claude Agent SDK: agent theory, the harness, bash, context engineering, and live-coding a Pokemon agent.

### IDEAS
- The Agent SDK sits atop Claude Code because Anthropic kept rebuilding the same agent parts repeatedly.
- AI evolved from single LLM features to structured workflows to autonomous agents building their own context.
- Agents build their own context, decide their own trajectories, and work very autonomously without rigid pipelines.
- The harness wraps the model with tools, prompts, a file system, skills, sub-agents, memory, and compacting.
- The bash tool is the single most powerful agent tool, effectively the first programmatic code mode.
- Instead of fifty bespoke tools, the agent just runs grep, npm, or installs ESLint by itself.
- Bash lets the agent store tool results to files, pipe outputs, and compose Unix primitives freely.
- Code generation for non-coding means the agent writes scripts composing APIs to answer everyday user questions.
- An email agent using bash writes a Gmail search script, greps prices, then sums them accurately.
- The agent loop has three core parts: gather context, take action, then verify the completed work.
- Tasks you can verify make great agents; unverifiable tasks like research stay much harder to trust.
- Tools suit atomic, irreversible actions; bash suits composable actions; code generation suits dynamic, highly flexible logic.
- Claude Code writes files with a dedicated write tool, not bash, so users approve each change.
- Transforming a CSV into SQLite lets the agent query data through an interface it already masters.
- Skills are just progressive context disclosure: folders the agent CDs into, reads, then runs scripts from.
- Hooks fire as events for deterministic verification or injecting context, enforcing rules without retraining the model.
- A finished agent should be simple, roughly fifty lines, with CLAUDE.md and helper scripts doing work.
- Sub-agents preserve context by reading and summarizing separate spreadsheet sheets in parallel, then returning distilled results.
- The Swiss cheese defense layers model alignment, harness permissioning, bash AST parsing, and network sandboxing together.
- For fifty-million-line codebases, semantic search is brittle; good CLAUDE.md files and scoped starting subdirectories work better.

### INSIGHTS
- Context is not just the prompt; it includes the tools, files, and scripts the agent uses.
- General computer use beats bespoke tools because existing software already solves nearly every developer task well.
- The strength of an agent tracks the strength of its verification step more than anything else.
- Reading agent transcripts repeatedly is the core meta-skill for designing and steadily improving an agent loop.
- Because AI writes code tenfold faster, you should discard and rewrite agent code tenfold faster too.
- Startups win because they adopt current agent capabilities immediately, unlike incumbents stuck inside six-month release cycles.
- The file system is where agents naturally store memory, verify work, and ground their future actions.
- Verification should happen everywhere possible, not merely at the end, using rules and heuristics throughout execution.
- Keep tools atomic and reserve them for guaranteed, irreversible actions; let bash handle the composable exploration.
- Prototype an agent in Claude Code first, then productionize it only once you have high conviction.

### QUOTES
- "bash is what makes Claude Code so good" — Thariq Shihipar
- "one of the big opinions is the bash tool is the most powerful agent tool" — Thariq Shihipar
- "agents ... build their own context, like decide their own trajectories, are working very very autonomously" — Thariq Shihipar
- "we found that when we're building agents at Anthropic, we kept rebuilding the same parts over and over again" — Thariq Shihipar
- "building an agent loop, I think it's like really much very much like kind of an art or intuition" — Thariq Shihipar
- "the number one thing that the meta learning for designing an agent loop to me is just to read the transcripts over and over again" — Thariq Shihipar
- "if you can verify its work, it's like a great like candidate for an agent" — Thariq Shihipar
- "we can write code 10 times faster. You should throw out code 10 times faster as well" — Thariq Shihipar
- "building an agent should be simple ... but simple is not the same as easy" — Thariq Shihipar
- "the agent SDKs are like the React of agent frameworks to me" — Thariq Shihipar
- "any time you spend not solving these problems ... you're probably not delivering value to your users" — Thariq Shihipar
- "the great thing about the model is like it listens to feedback. It will read the error outputs" — Thariq Shihipar

### HABITS
- Thariq saves every tool call result to the file system, then returns the path for rechecking.
- He rewrites his own agent code roughly every six months as underlying model capabilities meaningfully shift.
- He always prototypes using Bun to avoid a TypeScript compile step the agent must otherwise remember.
- He logs every single tool call during prototyping so he can watch what the agent does.
- He designs all CLI scripts with a help flag so the model progressively discovers available subcommands.
- He starts every new agent build from the Agent SDK rather than assembling a harness manually.
- He gives agents broad database write access, then layers on specific guardrails and corrective feedback afterward.
- He creates temporary scoped API keys for agents, sometimes routing through proxies to prevent secret exfiltration.
- He summarizes a working prototype into CLAUDE.md, keeps the helper scripts, then writes a tiny runner.

### FACTS
- The Claude Agent SDK was formerly named the Claude Code SDK before Anthropic broadened its scope.
- Anthropic released skills roughly two weeks before this workshop and Claude Code around eight months prior.
- The Agent SDK ships to-do tools that maintain and check off tasks displayed as it runs.
- Anthropic runs an AST parser on every bash tool call to reliably know what commands do.
- The Agent SDK can sandbox both network requests and file system operations outside the working directory.
- Anthropic engineers, finance, data science, and marketing staff all began using Claude Code for non-coding tasks.
- People already build software reliability, security, incident triage, bug finding, and dashboard agents on the SDK.
- Cloudflare provides an Agent SDK example where sandbox.start and bun agent.ts deploy a working agent quickly.
- Pokemon Red is a heavily reverse-engineered ROM whose internal memory can be searched for party data.

### REFERENCES
- Claude Agent SDK (formerly Claude Code SDK), Claude Code, Anthropic platform docs.
- Bash and Unix primitives: grep, awk, tail, ffmpeg, LibreOffice, jq, git, npm, ESLint.
- SQLite, CSV, TypeScript, Bun, Node.js.
- Poke API, Smogon competitive data, a Node.js GBA emulator, Pokemon Red, "Claude Plays Pokemon."
- CLAUDE.md, skills (front-end design skill, docx skills), the plugin marketplace (/plugins).
- Anthropic reward hacking paper.
- Sandbox providers: Cloudflare (sandbox example and code-mode blog posts), Modal, AWS, DigitalOcean.
- Analogies and concepts: React, JSX, jQuery, Backbone; code mode / programmatic tool use; structured outputs; Swiss cheese defense; lethal trifecta.
- Playwright CLI / MCP; Thariq Shihipar (@trq212) and his AI Engineer talk.

### ONE-SENTENCE TAKEAWAY
Build agents on bash, the file system, and verification; prototype in Claude Code, then productionize.

### RECOMMENDATIONS
- Start any new agent from the Agent SDK instead of hand-building the tools, prompts, and compaction.
- Give your agent a bash tool before writing any bespoke tools for every new use case.
- Before building an agent, ask whether you can verify its output; if not, reconsider the task.
- Read your agent's transcripts repeatedly and continually ask where exactly you could help it do better.
- Save large tool outputs to files and return their paths so the agent can recheck work.
- Transform awkward data into a representation the model already masters, such as SQL, for reliable querying.
- Use hooks to enforce read-before-write and to force the agent to run scripts instead of guessing.
- Verify at every possible point, adding rule-based error feedback so that the agent self-corrects mid-task naturally.
- Prototype the whole agent inside Claude Code, then port it to a tiny SDK runner file.
- Scope agent API keys tightly and sandbox execution so a hijacked agent cannot exfiltrate your secrets.
