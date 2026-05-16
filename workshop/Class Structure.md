7-day live workshop. Day 0 is async pre-work. Each live day has three blocks:

- **Core watch-along** (~3-5 videos): screened together with pauses to discuss
- **Practice block** (~3-5 videos): demos a workflow attendees redo live
- **Deep cuts**: optional async pre/post-watch for hungry attendees

Class codes: **CC** = Master Claude Code, **CX** = Master Codex, **FT** = Fundamental Techniques, **AT** = Advanced Techniques, **CE** = Context Engineering, **PE** = Prompt Engineering, **WF** = My Daily Workflows, **FB** = For Business. *(NEW)* = needs net-new recording.

# Day 0 — Foundations & Setup *(async pre-work)*

Mechanics off the live track so Day 1 starts on concepts.

**Core**: Install CC (Mac + Windows) · Installing Warp · Install Codex CLI · Install Codex App · A Quick Build (CC + CX) · `/init` & `Claude.md` · `/init` & `AGENTS.md` · **Custom Slash Commands** (CC) *(promoted from Day 5 — load-bearing across Days 1/2/5/6/7 per dependency hunt)* · **Scope & Settings.json** (CC) · Creating Projects & Files (CX) · Referencing Files & Folders (CX)

**Practice**: Terminal Commands · Git for Version Control

**Deep cuts**: VSCode Version · Cursor + Codex CLI · Ghostty · Resuming Sessions · Where Codex Works (CX) · /approvals (CX) · /fewer-permission-prompts (CC) · Aliases (CC) · Ultrathink (CC) · Fullscreen TUI & Focus (CC) · Claude Environment Variables (CC) · /teleport (CC) · Git Features (CX) · MCP Servers (CX) · Exa MCP (WF) · [[Codex App vs Claude Code]]

**Mechanics moved here from live**: `/clear` · `/model` · `/status` · `/config` · `/context` · `/usage` · Permissions (3 videos) · Settings JSON

---

# Day 1 — Alignment

**Core** *(play in this order)*:
1. [[Status of Agents]] *(NEW)*
2. Customized Terminology for Better Prompts — FT *(maps to [[Glossaries]])*
3. Clarifying Questions — FT
4. Ask User Question Tool · Ask User Question Example — CC *(must precede Spec Developer per dep hunt)*
5. Spec Developer — CC
6. Benefits of Spec Developer — CC

*(**Checking After Spec Developer** moved to Day 6 — assumes Subagents knowledge from Day 3, lands naturally as the "verify against the spec" beat)*

**Practice** (run a real planning session live):
- Planning Mode · Improved Plan Mode — CC
- Starting in Plan Mode — FT
- [[HTML Artifacts]] live demo (Interactive HTML Artifacts — WF) *(artifact-as-spec)*

**Deep cuts**:
- Continuing Plan in New Context Window — CC *(sets up Day 3)*
- Artifact Planning — FT
- Multimodal Models for PRDs — FT
- Goal In, Strategy Out — PE
- /goal · Using /goal Effectively — CX
- Channel HTML Artifacts — WF
- Infusing Lived Experience — PE
- /advisor — CC *(plan-review mechanic)*
- Reducing Agent Confusion in Growing Projects — FT *(under [[Glossaries]] umbrella)*
- Missions/Goals merge *(NEW — synthesises the three X threads currently in [[Missions]], [[Defining Good Goals]], [[goal]])*

---

# Day 2 — Steering

**Core** *(play in this order)*:
1. Long Context Failure — FT *(sets the why)*
2. Context Window Management — WF · Opus 4.6's Context Window — WF
3. Dealing with Syncophancy — FT
4. /rewind — CC *(after attendees have seen /clear + /compact in pre-work)*

**Practice** (steer a long-running task):
- /clear · Session Management — CC
- Auto Compact and Handoff · /handoff — CC
- /compact — CX

**Deep cuts**:
- Boxing the Agent In · Context Switching · Just Run It Again — FT *(Closing the Loop moved to Day 7 Practice — required prerequisite for Autoresearch per dep hunt)*
- Gravitational Pull from Older Models — AT
- Queuing vs Steering — CX
- [[Distribution Steering]] · [[Persona Vectors]] — PE
- High-Level Coherence, Low-Level Implementation — FT
- Cognitive Inertia — CE
- Getting Prompt Feedback · Multiple Proposals · Agent Introspection — FT
- Chats vs Threads (CX) · Compaction & Monothreading (CX) *(Codex App primitives)*
- /new (CX) · /recap (CC) · Stashing Prompts (CC)
- Economising with Prompt Cache — AT
- Long-context trio merge *(NEW — synthesises [[long-context-demands-active-human-steering]] / [[recent-context-dominates-attention]] / [[long-context-inverts-dumb-zone-advice]])*

---

# Day 3 — Context Architecture

**Core** *(play in this order — internal dep chains enforced)*:
1. Subagents — CC *(foundation)*
2. Quick Spawning Subagents — CC
3. Forking Sessions — CC → /btw — CC → Forking Sessions vs /btw — CC
4. *5-minute Skills primer* — required before Context Layer videos. Progressive Disclosure assumes Skills knowledge per dep hunt. Either insert primer here OR swap Days 3 ↔ 4. **OPEN CALL — see Findings section.**
5. [[Context Layer]]: Signal to Noise → Progressive Disclosure → Anatomy of a Node — CE

**Practice** (build a multi-subagent task live):
- Explore Subagent · Improving Explore Subagent — CC
- Async Tasks & Subagents · --agent — CC
- [[Memory]] (unified note: Memory.MD · Subagent Memories — CC; Agents.MD & Memories — CX)

**Deep cuts**:
- 1M Token Context · Different Orderings · Scout, Worker, Synthesizer · Starting Afresh · Simple Repetitive Tasks — CC
- Subagents · Forked Subagents · Nested Subagents · Creating Subagents — CX
- Mini Windows (CX) · Forking (CX) · Symlinking (CX) *(Codex App primitives)*
- Why Search Isn't Enough · Instruction Following Limits · Example/Maintenance Build a Context Layer — CE
- [[Context Files]] family: Advanced CLAUDE.md · Hierarchical CLAUDE.md · Project & User Rules · Best Practices · Conditions · Cleanup — CC
- Refactoring with Subagents · Multi Subagents for Hard Problems · Avoiding 'Code Bias' Caused Loops — AT
- [[Worktrees]] — CC + WF + CX *(real workflow primitive)*
- Multi Clauding — WF · Cmux — CC
- Combining CLIs & Models — AT *(maps to [[CLIs vs MCPs]])*
- Using Public GitHub Repos — AT
- --add-dir (CX) · /batch (CC)
- [[Monitor Tool]] — CC

---

# Day 4 — Skills

ACS is *over*-covered here (14+ videos). Trim, don't pad.

**Core**:
- Claude Code Skills · Creating Skills · Types of Skills — CC
- Real World Skill Example 1 + 2 — CC

**Practice** (build a skill live, simplify it, chain it with a subagent):
- Arguments for Skills · Forked Contexts for Skills — CC
- Combining Skills & Subagents — CC *(uses skill-creator — install first)*
- Skills + Explore Subagents — AT
- [[Simplify Pass]] (`/simplify` — CC; Tackling Redunant Code — AT) *(post-build clean-up beat)*

**Deep cuts**:
- Specifying Models · Allowed Tools · Disable Model-Invoked · Specifying Agents · How Models Switch · find-skills — CC
- Triggering Skills Reliably — CE
- Blog Post to Skill — AT
- [[Real World Skills]] umbrella: Frontend Design Skill (CC) · Designing Components (WF) · Extract Wisdom (WF) · Data Analysis (WF) · Blog Post to Skill (AT)
- Creating Skills (Codex parity) — CX
- The One-Pattern Rule for Agents — AT *(maps to [[Off-distribution]])*
- Delete Your README.md — FT *(maps to [[Markdown over architecture]])*
- Unrestraining LLMs for Rewrites — AT
- Scaling Taste — PE
- [[Plugins]] (CC + CX) · Official Plugin Marketplace · Claude MD Management Plugin — CC
- [[Design Context MCPs]]: Refero Design (WF) · Paper Design MCP (CX)

---

# Day 5 — Automation & Workflows

**Core** *(play in this order — Hooks before Another Hook Example; Routines before Memory + API Trigger)*:
1. Hooks — CC
2. Another Hook Example — CC
3. Routines (aka Scheduled Tasks) — CC
4. Remote Control — CC
5. Connecting to Telegram — CC

**Practice** (wire up an actual automation live):
- Real World Example [Automation] — CC
- API Trigger Routines · Memory for Scheduled Tasks — CC
- Automatic Plan Reviewing with Other CLIs — CC
- Push Notifications (Desktop + Mobile) — CC

**Deep cuts**:
- Connecting to Discord · Creating a Custom Slack Bot · Claude Code for Slack · GitHub App — CC
- Make Claude Speak to You — CC
- [[Headless Mode]] · /loop · [[Monitor Tool]] — CC
- *(Custom Slash Commands moved to Day 0 — load-bearing across days)*
- /autofix-pr — CC *(maps to [[Every PR]])*
- Mermaid Diagrams — CX · Git Diffs & Mermaid Diagrams — AT
- Automations · Thread Automations — CX
- Browser Use (CX) · Computer Use (CX) · Codex for Chrome (CX)
- Custom Prompts (CX) *(Codex parity for slash commands)*
- Chrome Javascript Tool — CC
- Adding More Goal-Driven Events · Microsoft Clarity MCP · Follow Ups on Features · LinkedIn + Claude in Chrome — FB
- Managing API Keys for Agents — AT
- Multi Clauding — WF
- [[OpenAI Symphony]] *(NEW)*

---

# Day 6 — Verification

**Core** *(play in this order — Consult Skill before CLI Plugin per dep hunt; Plugin video opens by referencing Consult Skill)*:
1. Codex Consult Skill — CC
2. Codex CLI Plugin — CC
3. Codex MCP Server — CC
4. /security-review — CC
5. /review — CX
6. **Checking After Spec Developer** — CC *(moved from Day 1 — the "verify against the spec" beat lands here now that Subagents is in scope)*

**Practice** (verify a real change end-to-end):
- /ultrareview — CC
- Automatic Plan Reviewing with Subagents — AT
- Mixing Models & Modes · Combining CLIs & Models — AT
- Data Analysis — WF *(verify-the-numbers demo)*

**Deep cuts**:
- Quick Benchmarking — WF · Benchmarking Tools & MCPs — AT
- Planning Convergence — AT
- Understanding Agent Output · Logging · Bug Fixing Across Chats — FT
- /debug — CC
- Scoping APIs — FT
- /diff · /side · Browser Comments — CX
- Using Reliable Packages — FT
- [[Languages]] + files-matter-less merge *(NEW)*

---

# Day 7 — Agent Teams & Loopy AI

Biggest gap day. Most workshop-original content lives here.

**Core** *(play in this order)*:
1. Convergence thesis *(NEW)*
2. Archetype Teams · Living Archetypes — PE 🚨 *(both videos appear unfilmed in ACS — MCP returns null transcript/duration. Either record them as part of the workshop, or replace with the 5 archetype videos directly. **OPEN CALL — see Findings.**)*
3. Subagent Teams for Debugging — CC
4. Multi Subagents for Hard Problems — AT
5. The 5 archetype videos *(NEW × 5)* — solo + cheap verifier · parallel voters · generator + adversarial critic · decomposed swarm · environmental attractors

**Practice** (run a real loop live — **Closing the Loop is the bridge** per dep hunt):
1. Closing the Loop — FT *(prereq for Autoresearch)*
2. Ralph Loop — CC
3. Autoresearch Overview · Technical Example · Non-Technical Example — AT
4. /loop · [[Headless Mode]] — CC

**Deep cuts**:
- Refactoring with Subagents — AT
- Multi Clauding · Adding New Features — WF
- Task List Management · Plan Directory & Archiving · Archiving After Clear · Claude Code Guide Subagent — CC
- Just Run It Again · Bug Fixing Across Chats — FT
- Cloud Version · Thread Automations · Chronicle — CX
- [[Reverse Engineering]] — CC + FB
- [[Removing Bottlenecks]] *(NEW)*

---

# Recording plan (net-new content)

Topics with no ACS counterpart that need to be recorded for the workshop. Ranked by load-bearing-ness:

**Must-record (workshop spine)**:
1. **Day 7 archetype series** — convergence thesis + 5 archetypes (6 videos). This is the workshop's signature IP.
2. **Day 1 — Status of Agents** — the libraries-vs-products mental model. 1 video.
3. **Day 2 — long-context trio synthesis** — single video covering the three AI-That-Works observations together.
4. **Day 1 — Missions/Goals merge** — synthesises the three X threads into one explainer.

**Should-record (round out the day)**:
5. **Day 6 — Languages** — one explainer on language choice + flat-file layout for agent verifiability.
6. **Day 7 — Removing Bottlenecks** — reflection-style: "look at last week's transcripts, find the bottleneck."
7. **Day 5 — OpenAI Symphony** — or cut from the workshop and leave as a deep-cut note.

**Topics that may need to be cut** (no ACS coverage, stub is one line, hard to justify recording):
- [[Verification Architectures]] — one-line stub, no clear video angle. Cut or fold into [[Verifying with Codex]] day-of.
- [[Workflows]] (the root stub) — generic three-approaches list; consider folding into Day 2 ([[Compaction]]) + Day 7.

---

# Stub triage (follow-up pass)

The comprehensive proposal flags ~17 stubs to slim to one-line pointers (ACS video covers them fully) and ~8 to expand past their video (workshop angle is bigger). Holding this for a focused follow-up pass — see `proposals/02-comprehensive.md` for the full list.

**Retire (slim to pointer)**: Spec Developer · Compaction · Subagents · Forked Subagents · 1M Context · Creating Skills · Types of Skills · Forked Contexts for Skills · Skills + Subagents · Hooks · Routines · Remote Control · Mermaid Diagram Generator · Verifying with Codex · ultrareview · security-review · Autoresearch.

**Expand past video**: Glossaries · Prototypes as specs · Rewinding · Ordering · Off-distribution · Markdown over architecture · Every PR · Adversial Reviewers · agent-benchmark-harness · Ralph.

---

# Merges (still valid)

- **Goals trio** → [[Missions]] + [[Defining Good Goals]] + [[goal]]
- **Long-context trio** → the three Day 2 long-context idea-notes
- **Adversarial overlap** → [[Adversial Reviewers]] ↔ [[03-generator-plus-adversarial-critic]]
- **Subagent split** → [[Subagent Architectures]] = wiring, [[Verification Architectures]] = what to verify
- **Languages pair** → [[Languages]] + [[files-matter-less-in-agent-friendly-languages]]

# Findings from 2nd-pass curation (need Ray's call)

Three parallel agents ran a second pass — edge-class gap hunt (`proposals/04-edges.md`), dependency hunt (`proposals/05-dependencies.md`), and ACS-ID backfill (`proposals/06-backfill-summary.md`). Most findings are applied inline above. These five need decisions:

1. **🚨 Archetype Teams + Living Archetypes (PE) appear unfilmed** — `get_video` returns null transcript and duration for both. They're currently Day 7 Core "frame for the 5 archetypes." If unfilmed, Day 7 needs +2 more recordings (or just film the 5 archetypes + thesis and drop the PE intros).
2. **Progressive Disclosure ↔ Skills cross-day dependency** — PD (Day 3 Core) assumes Skills (Day 4) knowledge. Options: (a) 5-min Skills primer in Day 3 before PD, (b) swap Days 3 ↔ 4 entirely, (c) move PD to Day 4. Currently the plan assumes (a).
3. **Stub: `Workflows.md`** — backfill agent flagged this is a thin pointer. Comprehensive proposal already recommended retiring it. Cut or fold into [[Compaction]] + Day 7?
4. **Stub: `Subagent Architectures.md`** — backfill flagged it could live on Day 7 (Agent Teams) instead of Day 3 (Context). Move?
5. **Stub: `Ordering.md`** — placed on Day 2 deep-cut currently, but Day 3 (Context Architecture) is arguably the better home. Move?
6. **Stub: `Verification Architectures.md`** — comprehensive + backfill both flagged it as one-line, no clear angle. Cut?

# Day-0 absorption candidates (from dep hunt)

Beyond Custom Slash Commands (already promoted): **Settings JSON editing**, **Reasoning Effort / Ultrathink**, and **`/agents`** are load-bearing across multiple live days. Settings JSON + Ultrathink already on Day 0 — call out as load-bearing. `/agents` not yet on Day 0; either pull in or cover briefly with Subagents on Day 3.

# Edge additions not applied inline

The edge-scan proposal recommends ~50 specific video additions. The highest-leverage ones are applied above. For the full per-day add list (especially the Codex App primitives, Workflows class videos, and post-2026-03-01 additions), see `proposals/04-edges.md`. Treat unapplied items as candidates for the next pass rather than gaps.

# Pricing
See [[Pricing Structure]].
