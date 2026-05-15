# Comprehensive curation

A fuller mapping of existing ACS videos onto A1's 7-day workshop. Sized so each live day has enough material for a 3-4h session: a **Core watch-along** block (3-5 videos teacher screens and pauses to discuss), a **Practice block** (2-3 videos that demo a workflow which attendees then redo), and **Deep cuts** (optional async pre-work or homework for hungry attendees who want the long tail).

Class codes used below: **CC** = Master Claude Code, **CX** = Master Codex, **FT** = Fundamental Techniques, **AT** = Advanced Techniques, **CE** = Context Engineering, **PE** = Prompt Engineering, **WF** = My Daily Workflows, **FB** = For Business.

---

## Day 0 — Foundations & Setup *(async pre-work)*

**Core watch-along** *(everyone watches before Day 1)*:
- Install Claude Code (MacOS) — CC
- Install Claude Code (Windows) — CC
- Installing Warp (for MacOS) — CC
- Installing Codex CLI — CX (Codex CLI chapter)
- Installing for MacoS [Codex App] — CX
- A Quick Build — CC
- A Quick Build [Codex CLI] — CX

**Practice block**:
- Terminal Commands (for Beginners) — CC
- Using Git for Version Control — CC
- /init & Claude.md — CC
- /init & AGENTS.md — CX

**Deep cuts (optional)**:
- VSCode Version — CC
- Using Cursor Alongside Codex CLI — CX
- Ghostty Terminal — CC
- Resuming Sessions — CX

---

## Day 1 — Alignment

**Core watch-along**:
- Spec Developer — CC (Spec Developer chapter)
- Checking After Spec Developer — CC
- Benefits of Spec Developer — CC
- Clarifying Questions — FT
- Customized Terminology for Better Prompts — FT *(maps to [[Glossaries]])*

**Practice block** (run a real planning session live):
- Planning Mode — CC
- Improved Plan Mode — CC
- Ask User Question Tool — CC
- Ask User Question Example — CC
- Starting in Plan Mode — FT

**Deep cuts**:
- Continuing Plan in New Context Window — CC *(sets up Day 3)*
- Artifact Planning — FT *(maps to [[Prototypes as specs]])*
- Multimodal Models for PRDs — FT
- Goal In, Strategy Out — PE *(use to frame Missions/Goals merge)*
- /goal — CX
- Using /goal Effectively — CX

**Stub overlap notes**:
- [[Spec Developer]] stub → ACS has 3 videos that cover this fully. **Use the videos, retire the stub** (or shrink the stub to a one-line "see Spec Developer chapter in Master CC").
- [[Glossaries]] → "Customized Terminology for Better Prompts" + "Reducing Agent Confusion in Growing Projects" (FT) together cover this. **Use the videos, expand the stub past them** with the Grok glossary example already in the note.
- [[Prototypes as specs]] → "Artifact Planning" (FT) is the closest match but doesn't fully cover Theo's scrappy-copy-first. **Expand the stub past the video**.

---

## Day 2 — Steering

**Core watch-along**:
- Dealing with Syncophancy — FT *(maps to [[sycophantic-models-suggestions-as-commands]])*
- Long Context Failure — FT *(part of the long-context merge)*
- Context Window Management — WF (Feb 2026)
- Opus 4.6's Context Window — WF (Feb 2026)
- /rewind — CC *(maps to [[Rewinding]])*

**Practice block** (demo steering a long-running task):
- /clear — CC
- Session Management — CC
- Auto Compact and Handoff — CC *(maps to [[Compaction]])*
- /handoff — CC
- /compact — CX

**Deep cuts**:
- Boxing the Agent In — FT
- Closing the Loop — FT
- Context Switching — FT
- Just Run It Again — FT
- Gravitional Pull from Older Models — AT
- Queuing vs Steering — CX
- Distribution Steering — PE
- Persona Vectors — PE
- High Level Coherence, Low Level Implementation — FT
- Cognitive Inertia — CE
- Getting Prompt Feedback — FT
- Multiple Proposals — FT *(maps to [[asking-for-options-preserves-judgment]])*
- Agent Introspection — FT

**Stub overlap notes**:
- [[Compaction]] → "Auto Compact and Handoff" + "/handoff" + "/compact" (CX) cover it. **Use the videos, retire the stub** beyond a one-liner pointing to them.
- [[Rewinding]] → "/rewind" (CC) covers the mechanic; the stub's "don't change intent too often" point is the *why* that deserves to stay. **Expand the stub past the video** with the intent-stability framing.

---

## Day 3 — Context Architecture

**Core watch-along**:
- Subagents — CC
- Quick Spawning Subagents — CC
- Forking Sessions — CC *(maps to [[Forked Subagents]])*
- Forking Sessions vs /btw — CC
- /btw — CC

**Practice block** (build a multi-subagent task live):
- Explore Subagent — CC
- Improving Explore Subagent — CC
- Async Tasks & Subagents — CC
- --agent — CC

**Deep cuts**:
- 1M Token Context — CC *(maps to [[1M Context]])*
- Different Orderings — CC *(maps to [[Ordering]])*
- Scout, Worker, Synthesizer — CC
- Starting Afresh — CC
- Simple Repetitive Tasks — CC
- Subagent Memories — CC
- Subagents — CX
- Forked Subagents — CX
- Nested Subagents — CX
- Creating Subagents — CX
- Signal to Noise — CE
- Why Search Isn't Enough — CE
- Instruction Following Limits — CE
- Progressive Disclosure — CE
- The Context Layer — CE
- Anatomy of a Node — CE
- Example [Build a Context Layer] — CE
- Maintenance [Build a Context Layer] — CE
- /init & Claude.md — CC *(if not already covered Day 0)*
- Advanced CLAUDE.md — CC
- Hierarchical CLAUDE.md — CC
- Project & User Rules — CC
- CLAUDE.md Best Practices — CC
- CLAUDE.md Conditions — CC
- CLAUDE.md Cleanup — CC
- Memory.MD — CC
- Refactoring with Subagents — AT
- Multi Subagents for Hard Problems — AT
- Avoiding 'Code Bias' Caused Loops — AT
- Multi Clauding — WF (Feb 2026)
- Combining CLIs & Models — AT *(maps to [[CLIs vs MCPs]])*
- MCP Servers — CC *(if not Day 0)*

**Stub overlap notes**:
- [[Subagents]] / [[Forked Subagents]] → fully covered by CC chapters + CX chapters. **Use the videos, retire the stubs** beyond a pointer.
- [[Ordering]] → "Different Orderings" + Carlini quote in stub. Carlini story is the *why*. **Expand the stub past the video**.
- [[1M Context]] → "1M Token Context" + "Scout, Worker, Synthesizer" cover this. **Use the videos, retire the stub**.
- **Context Engineering class (all 11 videos)** is essentially a built-in Day 3.5 module. Strongly consider folding 4-5 of them into Day 3 core (Signal to Noise, Progressive Disclosure, The Context Layer, Anatomy of a Node) rather than as deep cuts — they teach the *frame* that subagents + CLAUDE.md hang off.

---

## Day 4 — Skills

**Core watch-along**:
- Claude Code Skills — CC
- Creating Skills — CC
- Types of Skills — CC
- Real World Skill Example 1 — CC
- Real World Skill Example 2 — CC

**Practice block** (build a skill live, then chain it with a subagent):
- Arguments for Skills — CC
- Forked Contexts for Skills — CC
- Combining Skills & Subagents — CC *(maps to [[Skills + Subagents]])*
- Skills + Explore Subagents — AT

**Deep cuts**:
- Specifying Models for Skills — CC
- Allowed Tools for Skills — CC
- Disable Model Invoked Skills — CC
- Specifying Agents for Skills — CC
- How Models Switch with Skills — CC
- find-skills Skill — CC
- Triggering Skills Reliably — CE
- Blog Post to Skill — AT
- Frontend Design Skill — CC
- Creating Skills — CX *(Codex's version, for parity)*
- The One-Pattern Rule for Agents — AT *(maps to [[Off-distribution]])*
- Delete Your README.md — FT *(maps to [[Markdown over architecture]] thematically)*
- Scaling Taste — PE
- Living Archetypes — PE
- Archetype Teams — PE

**Stub overlap notes**:
- [[Creating Skills]] / [[Types of Skills]] / [[Forked Contexts for Skills]] / [[Skills + Subagents]] → all four stubs map 1:1 onto existing CC Skills chapter videos. **Use the videos, retire the stubs** beyond a pointer to the chapter.
- [[Off-distribution]] → "The One-Pattern Rule for Agents" (AT) is the closest match. **Expand the stub past the video** with the Javascript-classes example from the stub.
- [[Markdown over architecture]] → "Delete Your README.md" (FT) is thematically close but the stub's claim ("skills replace code") is bigger. **Expand the stub past the video**.

---

## Day 5 — Automation & Workflows

**Core watch-along**:
- Hooks — CC
- Another Hook Example — CC
- Routines (aka Scheduled Tasks) — CC
- Remote Control — CC
- Connecting to Telegram — CC

**Practice block** (wire up an actual automation live):
- Real World Example [Automation] — CC
- API Trigger Routines — CC
- Memory for Scheduled Tasks — CC
- Automatic Plan Reviewing with Other CLIs — CC
- Push Notifications (Desktop + Mobile) — CC

**Deep cuts**:
- Connecting to Discord — CC
- Creating a Custom Slack Bot — CC
- Claude Code for Slack — CC
- GitHub App — CC
- Make Claude Speak to You — CC
- Headless Mode & Background Workflows — CC
- /loop — CC
- Monitor Tool — CC
- Custom Slash Commands — CC
- /autofix-pr — CC *(maps directly to [[Every PR]])*
- Mermaid Diagrams — CX *(maps to [[Mermaid Diagram Generator]])*
- Git Diffs & Mermaid Diagrams — AT
- Automations — CX
- Thread Automations — CX
- Adding More Goal-Driven Events — FB
- Microsoft Clarity MCP — FB
- Multi Clauding — WF

**Stub overlap notes**:
- [[Hooks]] / [[Routines]] / [[Remote Control]] → all three map 1:1 onto CC chapter videos. **Use the videos, retire the stubs**.
- [[Every PR]] → "/autofix-pr" (CC) is the literal feature; "Hooks" gives the gating mechanism. **Expand the stub past the videos** with the @aidenybai philosophy ("system to run on every PR").
- [[Mermaid Diagram Generator]] → CX "Mermaid Diagrams" + AT "Git Diffs & Mermaid Diagrams". **Use the videos, retire the stub**.
- [[OpenAI Symphony]] → no direct ACS video. **Net-new content needed** (see "Where the catalogue is thin").

---

## Day 6 — Verification

**Core watch-along**:
- Codex CLI Plugin — CC
- Codex Consult Skill — CC
- Codex MCP Server — CC
- /review — CX
- /security-review — CC

**Practice block** (verify a real change end-to-end):
- /ultrareview — CC
- Automatic Plan Reviewing with Subagents — AT
- Closing the Loop — FT
- Mixing Models & Modes — AT
- Combining CLIs & Models — AT

**Deep cuts**:
- Quick Benchmarking — WF *(maps to [[agent-benchmark-harness]])*
- Benchmarking Tools & MCPs — AT
- Planning Convergence — AT
- Understanding Agent Output — FT
- Logging — FT
- Bug Fixing Across Chats — FT
- /debug — CC
- Scoping APIs — FT
- /diff — CX
- /side — CX

**Stub overlap notes**:
- [[Verifying with Codex]] → fully covered by "Codex CLI Plugin" + "Codex Consult Skill" + "Codex MCP Server" + "/review" (CX). **Use the videos, retire the stub**.
- [[Adversial Reviewers]] → "Automatic Plan Reviewing with Subagents" (AT) is the live demo. Stub adds the Edge Case Hunter persona. **Expand the stub past the video**.
- [[ultrareview]] / [[security-review]] → 1:1 with CC videos. **Use the videos, retire the stubs**.
- [[agent-benchmark-harness]] → "Quick Benchmarking" (WF) + "Benchmarking Tools & MCPs" (AT). **Use the videos, expand the stub** with the eval-first framing.
- [[Languages]] → no direct ACS video. **Net-new** (the stub itself is one line).

---

## Day 7 — Agent Teams & Loopy AI

**Core watch-along**:
- Archetype Teams — PE *(maps to [[convergence-over-perfection-thesis]] + sets up the 5 archetypes)*
- Living Archetypes — PE
- Subagent Teams for Debugging — CC
- Multi Subagents for Hard Problems — AT
- Ralph Loop (aka Ralph Wiggum) — CC *(maps to [[Ralph]])*

**Practice block** (run a real loop live):
- /loop — CC
- Autoresearch Overview — AT *(maps to [[Autoresearch]])*
- Autoresearch Technical Example — AT
- Autoresearch Non-Technical Example — AT
- Headless Mode & Background Workflows — CC

**Deep cuts**:
- Refactoring with Subagents — AT
- Multi Clauding — WF
- Adding New Features — WF
- Task List Management — CC
- Plan Directory & Archiving Plans — CC
- Archiving Plans After Clear Context — CC
- Claude Code Guide Subagent — CC
- Just Run It Again — FT
- Bug Fixing Across Chats — FT
- Combining CLIs & Models — AT
- Cloud Version — CX
- Thread Automations — CX

**Stub overlap notes**:
- [[Ralph]] → "Ralph Loop (aka Ralph Wiggum)" (CC) is the literal video. **Use the video, expand the stub** with the /goal contract anatomy + in-window vs out-of-window framing.
- [[Autoresearch]] → 3 AT videos (Overview / Technical / Non-Technical) form a complete sub-module. **Use the videos, retire the stub**.
- [[convergence-over-perfection-thesis]] + the 5 archetypes → no direct ACS video; PE's "Archetype Teams" / "Living Archetypes" are the closest. **Expand the archetype notes past the PE videos** — these are workshop-original IP.
- [[Removing Bottlenecks]] → no direct video. **Net-new content needed** (stub is one line: "Get it to analyse previous transcripts").

---

## Day 0 additions

Beyond install + Quick Build, push these into pre-work so they don't burn live time:

- /clear — CC
- /model — CC
- /status & /config — CC
- /context — CC
- /usage — CC
- Permissions / Tab Accept Permissions / Auto Permission Mode — CC *(3 short videos)*
- Settings Json — CC
- /init & Claude.md — CC
- /init & AGENTS.md — CX
- Using Git for Version Control — CC

Rationale: these are mechanics, not concepts. Live time should not be burned on "here is what /clear does." Move them to async so Day 1 starts on alignment, not buttons.

---

## Topics that need a new stub

These appear in the comprehensive plan above but have no workshop content note yet. Add as Title Case stubs in `content/`:

- `Plan Mode.md` — covers Planning Mode, Improved Plan Mode, Continuing Plan in New Context Window (Day 1 practice block). Distinct from [[Spec Developer]].
- `Ask User Question.md` — the AUQ tool + example (Day 1 practice block, also feeds [[Spec Developer]]).
- `CLAUDE.md.md` — the canonical "how to write a CLAUDE.md" note for Day 3. Wraps Advanced CLAUDE.md, Hierarchical CLAUDE.md, Project & User Rules, Best Practices, Conditions, Cleanup, Memory.MD. (Filename collision with the workshop's own CLAUDE.md is annoying — name it `CLAUDE-md.md` or `Context Files.md`.)
- `Context Layer.md` — wraps the Context Engineering class's 11 videos into a single workshop topic for Day 3. Big idea: progressive disclosure + node anatomy.
- `Signal to Noise.md` — alternatively, leave the Context Layer split into 2-3 notes; this is the "why" framing for Day 3.
- `Goal In Strategy Out.md` — PE concept worth its own note. Day 1 (Alignment) or as part of the [[Missions]] merge.
- `Persona Vectors.md` — PE concept, fits Day 2 (Steering) as the deep mechanism behind sycophancy/distribution drift.
- `Distribution Steering.md` — same chapter as Persona Vectors, Day 2.
- `Plugins.md` — Plug Ins, Official Plugin Marketplace, Claude MD Management Plugin (CC). Day 4 (Skills) — plugins are skills' distribution channel.
- `Worktrees.md` — Worktrees (CC) + How I Use Worktrees (WF) + Worktrees Flow (CX). Day 3 or Day 5. Real workflow primitive.
- `Monitor Tool.md` — CC video, deserves its own note since it pairs with [[CLIs vs MCPs]] (streaming) and Day 5 automation.
- `Headless Mode.md` — Headless Mode & Background Workflows + /loop. Day 7 (Loopy AI) primitive.
- `Reverse Engineering.md` — "How to Reverse Engineer Claude Code" (CC) + "Reverse Engineering Mobile APIs" + "Reverse Engineering Binaries" (FB). Optional Day 7 deep cut / advanced theme.

---

## Where the catalogue is thin

Days where ACS doesn't quite carry the live session and Ray will need net-new content:

**Day 1 — Alignment**: ACS has Spec Developer + Plan Mode + Clarifying Questions, but no video covers [[Status of Agents]] (the "where agents are good/bad" mental model with the libraries-vs-products diagram). **Net-new**: one explainer video. Same for the [[Missions]] / [[Defining Good Goals]] / [[goal]] merge — the closest is PE "Goal In, Strategy Out" but the merge synthesises three X threads that aren't yet on ACS.

**Day 2 — Steering**: the long-context trio merge ([[long-context-demands-active-human-steering]] / [[recent-context-dominates-attention]] / [[long-context-inverts-dumb-zone-advice]]) is built from a single AI That Works podcast and has no ACS counterpart beyond FT's "Long Context Failure." **Net-new**: one synthesis video covering all three observations together.

**Day 4 — Skills**: solidly covered by ACS — the catalogue is *not* thin here. The risk is the opposite: too much material. Trim the deep cuts list before Day 4 rather than padding it.

**Day 5 — Automation**: [[OpenAI Symphony]] has no ACS video. **Net-new** (or cut it from the workshop and leave it as a deep-cut note). [[Workflows]] stub is generic ("three approaches: continue+compact, subagents, Ralph") and could be folded into [[Compaction]] (Day 2) + Day 7 rather than standing alone — *consider retiring*.

**Day 6 — Verification**: [[Languages]] + [[files-matter-less-in-agent-friendly-languages]] merge has no ACS video. **Net-new** (1 video). [[Verification Architectures]] stub is one line — needs either a video or to be cut from the curriculum.

**Day 7 — Agent Teams**: this is the biggest gap. The 6 archetype notes ([[convergence-over-perfection-thesis]] + 5 archetypes) are workshop-original. PE's "Archetype Teams" + "Living Archetypes" videos cover the *frame* but not the 5 specific archetypes. **Net-new**: 5-7 videos, one per archetype + the thesis. This is the workshop's signature IP and worth recording properly.

**Day 7 — Loopy AI**: [[Removing Bottlenecks]] has no ACS video. **Net-new** (probably a workshop-format reflection rather than a tool video — "look at your last week's transcripts, find the bottleneck").

---

## Summary deltas vs A1

The comprehensive view doesn't change A1's days, but it surfaces:

1. **Day 0 should swallow more mechanics** (permissions, /clear, /model, settings) so live time stays on concepts.
2. **Day 3 should formally absorb 4-5 Context Engineering videos** — they're already a built-in module that maps directly. Currently A1 mentions [[CLIs vs MCPs]] and [[1M Context]] but no Context Layer / Progressive Disclosure notes.
3. **Day 4 has the most ACS coverage** — 14 Skills videos plus AT skill content. Trim aggressively.
4. **Day 7 has the least ACS coverage** — most workshop-original content lives here. Budget recording time accordingly.
5. **~12 workshop stubs can be retired** (kept as one-line pointers to ACS videos) because the videos fully cover the topic: Spec Developer, Compaction, Subagents, Forked Subagents, 1M Context, Creating Skills, Types of Skills, Forked Contexts for Skills, Skills + Subagents, Hooks, Routines, Remote Control, Mermaid Diagram Generator, Verifying with Codex, ultrareview, security-review, Autoresearch.
6. **~8 stubs need expansion past their ACS counterpart** because the workshop angle is bigger than the video: Glossaries, Prototypes as specs, Rewinding, Ordering, Off-distribution, Markdown over architecture, Every PR, Adversial Reviewers, agent-benchmark-harness, Ralph.
7. **~6 topics need net-new recording**: Status of Agents, long-context trio, OpenAI Symphony, Languages, the 5 agent-team archetypes + thesis, Removing Bottlenecks.
