---
title: Anthropic Just Dropped a Masterclass on Building Agent Harnesses (for Large Codebases)
video_url: https://www.youtube.com/watch?v=efRIrLXoOVA
video_id: efRIrLXoOVA
channel: Cole Medin
published: 2026-05-20
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Anthropic Just Dropped a Masterclass on Building Agent Harnesses (for Large Codebases)**](https://www.youtube.com/watch?v=efRIrLXoOVA) - Cole Medin - uploaded 2026-05-20

> Two buildable ACS videos here: a self-improving Stop hook (next step beyond existing Hooks videos) and an org-level AI-layer rollout strategy (net-new).

## 1. The idea worth a video

- **Spine A: A Stop hook that runs a headless Claude to reflect on the finished session and propose CLAUDE.md edits, so your rules never silently go stale.** It is the one component in the video that turns the whole harness from static config into a self-maintaining system. VERDICT: 🔗 next-step video available.
- **Spine B: Treat the AI layer as shared org infrastructure a small champion team builds during a quiet investment period, then rolls out, instead of every dev evolving their own.** The strategy that decides whether any of the techniques actually stick across a team. VERDICT: ❌ net-new video available.
- **Spine C (load-bearing, covered): The harness beats the model. Your repo now has a third layer beyond code and tests: the AI layer.** The umbrella thesis the whole video hangs off. VERDICT: ✅ already covered across the CLAUDE.md, Skills, Subagents chapters and the Context Engineering class (kept for understanding, not pitched).

## 2. Summary + counts

Cole Medin unpacks Anthropic's large-codebase playbook, building each harness component (the AI layer) into a demo repo: layered rules, self-improving hooks, scoped skills, LSP, subagents.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 3. 🔬 Deep dive

### Spine A — The self-improving Stop hook

The claim: a Stop hook that spawns a throwaway headless Claude to reflect on the just-finished session and propose CLAUDE.md edits keeps your rules from silently going stale. Why it is non-obvious: most teams treat hooks purely as guardrails (block dangerous commands, auto-format on save), so the highest-leverage use, self-maintenance, goes unused. Cole is blunt that "it's really really bad when your claw.md goes stale." Why it is true: because the model re-reads CLAUDE.md every turn, one stale rule quietly degrades every future session; but immediately after a session the diff and the reasoning are still fresh, so a hook firing on Stop can launch a separate headless Claude, compare the changes against current rules, and write suggested edits to a markdown review file. Because it fires automatically, maintenance happens continuously instead of never. It generalizes cleanly to a test suite that proposes its own missing cases, or an incident runbook that updates itself after each outage. How it goes wrong: the reflection can propose noisy or flat-wrong edits, so it must suggest into a review file for human approval rather than auto-commit, and running a full Claude session on every Stop adds latency and token cost.

### Spine B — The AI layer as an org asset

The claim: treat the AI layer as shared infrastructure that a small champion team builds during a quiet investment period and then rolls out, rather than letting everyone grow their own. Why it is non-obvious: the default is bottom-up, where each dev accretes personal rules and skills, which feels productive but quietly fragments the org and leaves newcomers with a weak first experience. Why it is true: because first impressions gate adoption, a dev who tries the agent with no harness gets mediocre results and churns, whereas a pre-built standard layer produces consistent results faster, so adoption compounds instead of stalling. And because the layer is versioned in the repo, an improvement one team makes propagates to everyone automatically. It generalizes to the internal platform or developer-experience team that owns CI, linters, and templates so product teams simply inherit them. How it goes wrong: a central team can over-standardize and ossify, ignoring local needs, so the layer must stay lean and let subdirectories override it; and a long quiet period with no shipping risks building the wrong standard in isolation.

### Spine C — The harness beats the model (covered, load-bearing)

The claim: the harness (the context and tools you wrap around the model, the AI layer) matters as much as the model, and is now a first-class third part of every codebase alongside code and tests. Why it is non-obvious: benchmark culture pushes people to chase the next model, assuming capability lives in the model. Why it is true: because Claude Code navigates via agentic search (grep, folder walking) with no index, its output is bounded by the starting context it is handed; curate that context (rules, skills, LSP, subagents) and the same model performs dramatically better on the same repo, so investment shifts from waiting for a smarter model to engineering the layer you own. It generalizes to context engineering broadly, and mirrors how a senior engineer's value is their map of the codebase, not raw IQ. How it goes wrong: over-building the layer (thousand-line rule files) backfires and hurts performance, so the harness must stay lean and progressively disclosed. Gap-check: ✅ COVERED. ACS already teaches all seven components across the CLAUDE.md, Skills, Subagents, and MCP chapters plus the entire Context Engineering class, so this framing is load-bearing for the video but not a new video. Excluded from the pitches and the post gate.

## 4. 🎬 Proposed ACS videos (ranked)

### Pitch 1 — Make Your CLAUDE.md Maintain Itself: a Self-Improving Stop Hook

- **HOOK:** Your rules go stale the moment your codebase moves, and stale rules quietly wreck every session after.
- **THE PROMISE:** For anyone with a living CLAUDE.md, wire a Stop hook that proposes rule updates automatically after every session, so your rules maintain themselves.
- **THE SHAPE:** 1) show a rule going stale right after a code change; 2) build the Stop hook in settings.json; 3) it spawns a headless Claude to diff the session against current rules; 4) read the generated "claude markdown review" suggestions; 5) approve and action them in a fresh session.
- **SPINE:** A.
- **SLOT:** Master Claude Code / Hooks (sits after "Hooks" and "Automatic Plan Reviewing with Other CLIs").
- **RELATIONSHIP:** 🔗 complements "Hooks" (which already teaches Stop/PostToolUse events, blocking dangerous commands, and auto-formatting) and "Automatic Plan Reviewing with Other CLIs" (a hook that spawns a headless reviewer CLI) by aiming that same machinery at self-maintaining rules, the move after you know hooks exist. Do not re-teach hook basics; the new payload is the reflect-and-propose loop against CLAUDE.md.
- **PROOF TO REUSE:** Cole's live stop-hook demo; the "claude markdown review" markdown output; "it's really really bad when your claw.md goes stale"; the billing-service example where a bigger change triggered a real rule-update recommendation.

### Pitch 2 — The AI Layer Is Infrastructure: How One Small Team Rolls It Out to Your Whole Org

- **HOOK:** When every dev grows their own rules and skills, your org fragments and newcomers bounce off a weak setup.
- **THE PROMISE:** For team leads adopting Claude Code, build one standard AI layer with a champion team, then roll it out, so everyone gets consistent results fast.
- **THE SHAPE:** 1) the fragmentation and first-disappointment problem; 2) name the small champion team; 3) the quiet investment period building rules, skills, hooks, and the LSP-MCP; 4) version the whole layer in the repo; 5) a staged rollout so newcomers inherit the standard instead of rebuilding it.
- **SPINE:** B.
- **SLOT:** For Business (adoption) or My Daily Workflows.
- **RELATIONSHIP:** ❌ net-new. The closest existing video is "/team-onboarding" (which generates an onboarding.md from recent usage), but that is a tool, not the org-adoption strategy. Latent spine: the source treats this in roughly two minutes at the end, so the video needs extra sourcing beyond this transcript.
- **PROOF TO REUSE:** "you start with a quiet investment period"; the avoid-fragmentation and avoid-first-disappointment arguments; Cole's stated enterprise-training experience building AI layers for organizations.

**Also film-able (not deep-dived):**
- Path-scoped skills: use the skill `path` parameter so a skill only activates inside the relevant directory. 🟡 partial. The Skills chapter covers many frontmatter params (allowed-tools, model, agent, forked context) but not path-scoping. Rough slot: Master Claude Code / Skills. Narrow feature, better as a short than a full video.

## 5. 📚 Full wisdom (reference)

**SUMMARY:** Cole Medin unpacks Anthropic's large-codebase playbook, building each harness component (the AI layer) into a demo repo: layered rules, self-improving hooks, scoped skills, LSP, subagents.

**IDEAS**
- The harness around the model, not the model itself, decides how well large codebases get handled.
- Claude Code uses agentic search with grep and folder structure, never a synced semantic codebase index.
- Every codebase now gains a third part beyond just code and tests: the AI layer harness.
- Global rules run the entire session, so they deserve the most context-curation effort of all components.
- Nested CLAUDE.md files load automatically whenever Claude edits inside that folder, layering conventions progressively like skills.
- Initializing Claude Code inside a subdirectory pins its working directory, so it stays in that scope.
- Claude walks up the directory tree loading every parent CLAUDE.md, so root context is never lost.
- A stop hook reflects on the finished session and proposes CLAUDE.md edits while context is fresh.
- That reflection runs a separate headless Claude session that outputs suggested changes to a markdown file.
- A session-start hook can inject dynamic context like git status, recent commits, or team Confluence docs.
- Skills accept a path parameter so they only activate inside the relevant part of the repo.
- Cole's rule: global rules are the conventions to follow; skills are the workflows you actually run.
- An MCP server can expose LSP tools, giving Claude go-to-definition and find-references beyond plain grep search.
- Past six-digit line counts, grep turns slow and token-inefficient, so symbol-level search becomes the better default.
- Subagents split exploration from editing, keeping huge research token counts out of the primary context window.
- You can spawn built-in explorer subagents ad hoc without defining any custom subagent files up front.
- A champion team should build the AI layer during a quiet investment period, then roll out.

**INSIGHTS**
- Model benchmarks obsession misleads teams; the surrounding ecosystem of context and tools drives real coding outcomes.
- Progressive disclosure is the unifying principle: load conventions, skills, and searches only where they actually matter.
- Agentic search removes index sync pain but demands you curate starting context so Claude finds targets.
- Stale rules quietly poison sessions; automating rule maintenance matters as much as writing the rules originally.
- Hooks are misunderstood as guardrails; their higher-value use is continuous, automatic improvement of the whole setup.
- The rules-versus-workflows split clarifies otherwise overlapping tools: CLAUDE.md holds the conventions, skills hold the repeatable procedures.
- Context economy is the through-line: every technique here exists to protect a finite context window budget.
- Standardizing one organizational AI layer prevents fragmentation and stops newcomers being disappointed by weak first setups.
- Giving any repo to Claude and asking it to explain strategies is the fastest adoption path.

**QUOTES**
- "The harness matters as much as the model." — Cole Medin
- "if you think your code base is too complex for Claude code, you are wrong." — Cole Medin
- "There are actually studies out there that prove that that can hurt your coding agent performance" — Cole Medin
- "most teams think of hooks as scripts that prevent Claude from doing something wrong... But their more valuable use is continuous improvement." — Cole Medin
- "global rules are your conventions... Your skills are the workflows." — Cole Medin
- "grep by itself is going to be slow and really token inefficient" — Cole Medin
- "we want to use subagents to split exploration from editing." — Cole Medin
- "it's really really bad when your claw.md goes stale" — Cole Medin
- "you give Claude the same navigation that a developer has in their IDE." — Cole Medin
- "you start with a quiet investment period." — Cole Medin

**HABITS**
- Cole keeps his global rule files lean, resisting the urge to write thousand-line comprehensive instruction documents.
- He puts a directory-structure map in global rules so Claude can discover the right slice itself.
- He initializes Claude directly in a subdirectory when a ticket clearly scopes the relevant work area.
- He uses subagents liberally, often spawning three at conversation start for database, backend, and frontend research.
- He scopes tests and lint commands per subdirectory and ignores build artifacts from agent reading entirely.
- He runs a self-reflection stop hook constantly in the background, actioning its suggestions only when ready.
- He plans, implements, and validates through a fuller process before trusting any real production code changes.
- He tells Claude which search tool to use, or bakes that guidance into his global rules.

**FACTS**
- Anthropic reports Claude Code running across multi-million-line monorepos and decades-old legacy systems at large enterprise scale.
- Claude Code performs no codebase indexing and runs no traditional RAG or semantic search underneath it.
- Anthropic's blog post lists seven AI-layer components, each mapping to one large-codebase strategy for coding agents.
- Studies cited by Anthropic show overly long rule files can degrade coding agent performance quite measurably.
- Language server protocols power IDE features like go-to-definition, hover hints, and reference highlighting by default everywhere.
- Cole's demo MCP server exposed three search tools, returning one definition and two references in repo.
- The plugin installs via slash plugin marketplace add, pointing at a locally cloned repository folder path.
- The example helpline repo bundles the stop hook, explorer subagent, LSP-MCP server, and a scoped skill.

**REFERENCES**
- Anthropic blog post: "How Claude Code works in large codebases" (claude.com/blog).
- Cole Medin's helpline demo repo: github.com/coleam00/helpline (every component built and validated).
- Claude Code (Anthropic) and Codex (OpenAI); features: CLAUDE.md, skills, hooks, subagents, MCP servers, LSP, plugins.
- JetBrains Academy AWS Skill Paths (sponsor).
- Dynamous community and second brain course.
- Tools mentioned: Confluence, Jira, GitHub issues, VS Code, grep, headless Claude sessions.

**ONE-SENTENCE TAKEAWAY:** Invest in the harness around your model, because the AI layer beats raw model power.

**RECOMMENDATIONS**
- Split your bloated CLAUDE.md into nested files scoped to the subdirectories where each convention actually applies.
- Add a stop hook that runs headless Claude to propose rule updates after each finished session.
- Add a session-start hook that injects git status and team docs into every new coding session.
- Scope repeatable skills to their directory using the path parameter so they activate only where relevant.
- Stand up an MCP-wrapped LSP once your codebase passes roughly one hundred thousand lines of code.
- Dispatch web research and codebase exploration to subagents so editing starts with a clean context window.
- Initialize Claude inside the exact subdirectory a ticket targets to keep its edits tightly scoped there.
- Assign a small champion team to build the organization's AI layer before a wider team rollout.
- Hand any complex repo to Claude and ask it to explain and apply these harness strategies.
