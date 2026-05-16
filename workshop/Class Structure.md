7-day live workshop. Day 0 is async pre-work. Each live day has three blocks:

- **Core watch-along** (~3-5 videos): screened together with pauses to discuss
- **Practice block** (~3-5 videos): demos a workflow attendees redo live
- **Deep cuts**: optional async pre/post-watch for hungry attendees

Class codes: **CC** = Master Claude Code, **CX** = Master Codex, **FT** = Fundamental Techniques, **AT** = Advanced Techniques, **CE** = Context Engineering, **PE** = Prompt Engineering, **WF** = My Daily Workflows, **FB** = For Business. *(NEW)* = needs net-new recording.

# Day 0 — Foundations & Setup *(async pre-work)*

Mechanics off the live track so Day 1 starts on concepts.

**Core**: Install CC (Mac + Windows) · Installing Warp · Install Codex CLI · Install Codex App · A Quick Build (CC + CX) · `/init` & `Claude.md` · `/init` & `AGENTS.md`

**Practice**: Terminal Commands · Git for Version Control

**Deep cuts**: VSCode Version · Cursor + Codex CLI · Ghostty · Resuming Sessions

**Mechanics moved here from live**: `/clear` · `/model` · `/status` · `/config` · `/context` · `/usage` · Permissions (3 videos) · Settings JSON

---

# Day 1 — Alignment

**Core**:
- Spec Developer · Checking After Spec Developer · Benefits of Spec Developer — CC
- Clarifying Questions — FT
- Customized Terminology for Better Prompts — FT *(maps to [[Glossaries]])*
- [[Status of Agents]] *(NEW)*

**Practice** (run a real planning session live):
- Planning Mode · Improved Plan Mode — CC
- Ask User Question Tool · Ask User Question Example — CC
- Starting in Plan Mode — FT

**Deep cuts**:
- Continuing Plan in New Context Window — CC *(sets up Day 3)*
- Artifact Planning — FT
- Multimodal Models for PRDs — FT
- Goal In, Strategy Out — PE
- /goal · Using /goal Effectively — CX
- Missions/Goals merge *(NEW — synthesises the three X threads currently in [[Missions]], [[Defining Good Goals]], [[goal]])*

---

# Day 2 — Steering

**Core**:
- Dealing with Syncophancy — FT
- Long Context Failure — FT
- Context Window Management — WF
- Opus 4.6's Context Window — WF
- /rewind — CC

**Practice** (steer a long-running task):
- /clear · Session Management — CC
- Auto Compact and Handoff · /handoff — CC
- /compact — CX

**Deep cuts**:
- Boxing the Agent In · Closing the Loop · Context Switching · Just Run It Again — FT
- Gravitational Pull from Older Models — AT
- Queuing vs Steering — CX
- [[Distribution Steering]] · [[Persona Vectors]] — PE
- High-Level Coherence, Low-Level Implementation — FT
- Cognitive Inertia — CE
- Getting Prompt Feedback · Multiple Proposals · Agent Introspection — FT
- Long-context trio merge *(NEW — synthesises [[long-context-demands-active-human-steering]] / [[recent-context-dominates-attention]] / [[long-context-inverts-dumb-zone-advice]])*

---

# Day 3 — Context Architecture

**Core**:
- Subagents · Quick Spawning Subagents — CC
- Forking Sessions · Forking Sessions vs /btw · /btw — CC
- [[Context Layer]] (Signal to Noise · Progressive Disclosure · Anatomy of a Node) — CE *(formally absorb 4-5 CE videos into core, not deep cuts)*

**Practice** (build a multi-subagent task live):
- Explore Subagent · Improving Explore Subagent — CC
- Async Tasks & Subagents · --agent — CC

**Deep cuts**:
- 1M Token Context · Different Orderings · Scout, Worker, Synthesizer · Starting Afresh · Simple Repetitive Tasks · Subagent Memories — CC
- Subagents · Forked Subagents · Nested Subagents · Creating Subagents — CX
- Why Search Isn't Enough · Instruction Following Limits · Example/Maintenance Build a Context Layer — CE
- [[Context Files]] family: Advanced CLAUDE.md · Hierarchical CLAUDE.md · Project & User Rules · Best Practices · Conditions · Cleanup · Memory.MD — CC
- Refactoring with Subagents · Multi Subagents for Hard Problems · Avoiding 'Code Bias' Caused Loops — AT
- [[Worktrees]] — CC + WF + CX *(real workflow primitive)*
- Multi Clauding — WF
- Combining CLIs & Models — AT *(maps to [[CLIs vs MCPs]])*
- [[Monitor Tool]] — CC

---

# Day 4 — Skills

ACS is *over*-covered here (14+ videos). Trim, don't pad.

**Core**:
- Claude Code Skills · Creating Skills · Types of Skills — CC
- Real World Skill Example 1 + 2 — CC

**Practice** (build a skill live, then chain it with a subagent):
- Arguments for Skills · Forked Contexts for Skills — CC
- Combining Skills & Subagents — CC
- Skills + Explore Subagents — AT

**Deep cuts**:
- Specifying Models · Allowed Tools · Disable Model-Invoked · Specifying Agents · How Models Switch · find-skills — CC
- Triggering Skills Reliably — CE
- Blog Post to Skill — AT
- Frontend Design Skill — CC
- Creating Skills (Codex parity) — CX
- The One-Pattern Rule for Agents — AT *(maps to [[Off-distribution]])*
- Delete Your README.md — FT *(maps to [[Markdown over architecture]])*
- Scaling Taste · Living Archetypes · Archetype Teams — PE
- [[Plugins]] · Official Plugin Marketplace · Claude MD Management Plugin — CC

---

# Day 5 — Automation & Workflows

**Core**:
- Hooks · Another Hook Example — CC
- Routines (aka Scheduled Tasks) — CC
- Remote Control · Connecting to Telegram — CC

**Practice** (wire up an actual automation live):
- Real World Example [Automation] — CC
- API Trigger Routines · Memory for Scheduled Tasks — CC
- Automatic Plan Reviewing with Other CLIs — CC
- Push Notifications (Desktop + Mobile) — CC

**Deep cuts**:
- Connecting to Discord · Creating a Custom Slack Bot · Claude Code for Slack · GitHub App — CC
- Make Claude Speak to You — CC
- [[Headless Mode]] · /loop · [[Monitor Tool]] — CC
- Custom Slash Commands — CC
- /autofix-pr — CC *(maps to [[Every PR]])*
- Mermaid Diagrams — CX · Git Diffs & Mermaid Diagrams — AT
- Automations · Thread Automations — CX
- Adding More Goal-Driven Events · Microsoft Clarity MCP — FB
- Multi Clauding — WF
- [[OpenAI Symphony]] *(NEW)*

---

# Day 6 — Verification

**Core**:
- Codex CLI Plugin · Codex Consult Skill · Codex MCP Server — CC
- /review — CX
- /security-review — CC

**Practice** (verify a real change end-to-end):
- /ultrareview — CC
- Automatic Plan Reviewing with Subagents — AT
- Closing the Loop — FT
- Mixing Models & Modes · Combining CLIs & Models — AT

**Deep cuts**:
- Quick Benchmarking — WF · Benchmarking Tools & MCPs — AT
- Planning Convergence — AT
- Understanding Agent Output · Logging · Bug Fixing Across Chats — FT
- /debug — CC
- Scoping APIs — FT
- /diff · /side — CX
- [[Languages]] + files-matter-less merge *(NEW)*

---

# Day 7 — Agent Teams & Loopy AI

Biggest gap day. Most workshop-original content lives here.

**Core**:
- Archetype Teams · Living Archetypes — PE *(frame for the 5 archetypes)*
- Subagent Teams for Debugging — CC
- Multi Subagents for Hard Problems — AT
- Ralph Loop — CC

**Practice** (run a real loop live):
- /loop · [[Headless Mode]] — CC
- Autoresearch Overview · Technical Example · Non-Technical Example — AT

**Deep cuts**:
- Refactoring with Subagents — AT
- Multi Clauding · Adding New Features — WF
- Task List Management · Plan Directory & Archiving · Archiving After Clear · Claude Code Guide Subagent — CC
- Just Run It Again · Bug Fixing Across Chats — FT
- Cloud Version · Thread Automations — CX
- [[Reverse Engineering]] — CC + FB
- **Workshop-original recordings**: convergence thesis + 5 archetypes *(NEW × 6)*
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

# Pricing
See [[Pricing Structure]].
