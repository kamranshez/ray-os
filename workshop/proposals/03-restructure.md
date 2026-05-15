# Restructuring proposal

A look at the ACS catalogue's *own* chapter clusters against A1's 7-day shape. Sourced from `list_videos` across all 8 classes (claude-code 147, codex 58, fundamental-techniques 23, advanced-techniques 21, context-engineering 11, prompt-engineering 8, workflows 14, for-business 7).

## Does A1 hold up?

**Confirmed by the catalogue**: Day 4 (Skills) maps almost 1:1 onto the 14-video `claude-code → Skills` chapter. Day 7 (Agent Teams + Loopy AI) is reinforced by `advanced-techniques`'s Multi-Subagents / Autoresearch trio / Combining CLIs & Models cluster plus `claude-code → Subagent Teams` and the `Advanced` chapter's Ralph / `/loop` / Monitor / Push Notifications / Headless / Auto Compact & Handoff. Day 6 (Verification) is reinforced by the `Connecting to Codex` chapter + Niche Features' `/security-review` and `/ultrareview`. Day 5 (Automation) maps onto `claude-code → Hooks` + `Automation` chapters cleanly.

**Strained or homeless content**: three big buckets have no clean A1 home.

1. **CLAUDE.md is missing from A1 entirely.** The `claude-code → CLAUDE.md` chapter is 8 videos (`/init`, Advanced, Hierarchical, Project & User Rules, Best Practices, Conditions, Cleanup, Memory.MD). This is the most basic taste-encoding mechanism in agentic coding and A1 has nowhere to put it. Day 4 (Skills) covers a more advanced form, Day 1 (Alignment) is conceptual, Day 3 (Context Architecture) is about runtime context flow. CLAUDE.md is the missing centre.

2. **Codex App is almost invisible.** The `codex → Codex App` chapter is 38 videos: `/goal`, threads vs chats, browser use, computer use, automations, mini windows, queueing vs steering, Codex subagents, forking, worktrees flow, agents.md & memories, chronicle, etc. A1 treats Codex only as a CLI verifier. If the workshop is "agentic coding" not "Claude Code only", Codex App deserves first-class billing — it's also the natural pair for the `claude-code → Connecting to Codex` chapter that already lives on Day 6.

3. **Context Engineering theory has no home.** The `context-engineering` class (Signal-to-Noise, Why Search Isn't Enough, Instruction Following Limits, Cognitive Inertia, Progressive Disclosure, The Context Layer, Anatomy of a Node, Maintenance) is theoretical groundwork that A1's Day 3 (mechanical: subagents/forks/CLIs vs MCPs) and Day 2 (behavioural: long-context/sycophancy) both implicitly assume but never teach.

Smaller homeless clusters: **Planning mechanics** (5 videos — Planning Mode, Improved Plan Mode, AskUserQuestion, Continuing Plan in New Context), **Multi-Clauding & Worktrees** (2 foundational team-workflow concepts spread across `workflows` and `claude-code → Advanced`), **Workflows class recipes** (Data Analysis, Extract Wisdom, Designing Components, Quick Benchmarking — concrete automation templates), **Plug Ins / Shortcuts / Niche Features ergonomics** (~25 videos of power-user moves with no curriculum home).

## Proposed restructure(s)

Three options ranging from least to most disruptive.

### Option A1-revised — still 7 days, additive shuffles

Keep A1's day titles and order. Plug the three biggest gaps by *adding* topics to existing days:

- Day 0 absorbs: Plug Ins chapter, Shortcuts chapter, ergonomic Niche Features (`/recap`, `/export`, Output Styles, Aliases, Custom Statusline, Fullscreen TUI, Sandboxing, Worktrees-as-basic-setup)
- Day 1 (Alignment) adds: `/init & CLAUDE.md`, Hierarchical CLAUDE.md, CLAUDE.md Conditions, Project & User Rules, Planning Mode, Improved Plan Mode, AskUserQuestion (Planning is part of getting aligned)
- Day 2 (Steering) adds: Cognitive Inertia, Instruction Following Limits, Long Context Failure (from fundamental-techniques)
- Day 3 (Context Architecture) adds: Signal-to-Noise, Progressive Disclosure, The Context Layer, Multi Clauding, Worktrees flow
- Day 4 (Skills) is unchanged (already complete)
- Day 5 (Automation & Workflows) adds: Multi Clauding-as-workflow, Data Analysis, Extract Wisdom, Designing Components, Quick Benchmarking, Frontend Design Skill, `/autofix-pr`
- Day 6 (Verification) adds: Codex MCP Server, Codex Consult Skill, Codex CLI Plugin, Planning Convergence, Automatic Plan Reviewing with Subagents
- Day 7 (Agent Teams & Loopy AI) adds: Subagent Teams for Debugging, Multi Subagents for Hard Problems, Refactoring with Subagents, Headless Mode, `/loop`, Monitor Tool, Push Notifications, Auto Compact & Handoff, `/handoff`, Task List Management, Archetype Teams, Living Archetypes

**Trade-off**: Day 1 and Day 3 get noticeably heavier. CLAUDE.md spread across Days 1 + 3 + 4 (Skills) means it never gets its own chapter — bad pedagogically since CLAUDE.md is *the* foundational mechanism most people are missing.

### Option A1-extended — 8 days, CLAUDE.md gets its own day

Promote CLAUDE.md from "spread across days" to "its own day". This is the cleanest fix.

- Day 1 — **Alignment**: Spec Developer, Prototypes, Glossaries, Status of Agents, Missions/Goals, Planning Mode + Improved Plan Mode + AskUserQuestion
- Day 2 — **Steering**: long-context trio, sycophancy, Cognitive Inertia, Instruction Following Limits, Rewinding, Ordering, Compaction, Just Run It Again
- Day 3 — **CLAUDE.md & The Context Layer**: `/init`, Hierarchical, Conditions, Best Practices, Cleanup, Project & User Rules, Memory.MD, Signal-to-Noise, Progressive Disclosure, Anatomy of a Node, Maintenance, agent-friendly languages
- Day 4 — **Subagents, Multi-Clauding, Context Architecture**: Subagents (basic + Explore + /batch + /simplify), Forked Subagents, Subagent Architectures, 1M Context (Scout/Worker/Synthesizer + Different Orderings), CLIs vs MCPs, Multi Clauding, Worktrees flow, Context Switching
- Day 5 — **Skills**: (unchanged from A1)
- Day 6 — **Automation & Workflows**: Hooks, Routines, Remote Control, Every PR, OpenAI Symphony, Mermaid Diagram Generator, Data Analysis, Extract Wisdom, Designing Components, Frontend Design Skill, Quick Benchmarking, `/autofix-pr`
- Day 7 — **Verification**: Languages, Verification Architectures, Verifying with Codex, Adversarial Reviewers, agent-benchmark-harness, security-review, ultrareview, Planning Convergence, Automatic Plan Reviewing with Subagents
- Day 8 — **Agent Teams & Loopy AI**: convergence thesis + 5 archetypes, Ralph, Autoresearch (overview + 2 examples), Subagent Teams for Debugging, Multi Subagents for Hard Problems, Headless Mode, `/loop`, Monitor Tool, Push Notifications, Auto Compact & Handoff, Archetype Teams, Living Archetypes, Removing Bottlenecks

**Trade-off**: 8 days = longer workshop = pricing implications (justifies $599 → $799?). But Day 3 (CLAUDE.md) is genuinely the day most students will remember, so it earns the slot. Day 8 stays packed but no worse than A1's Day 7.

### Option A1-extended-codex — 9 days, Codex App gets its own day

If you want the workshop to be "agentic coding" generally and not "Claude Code with Codex as a sidekick", give Codex App its own day. Same as A1-extended plus:

- Day 9 — **Codex App**: `/goal` + Using /goal Effectively, threads vs chats, mini windows, queueing vs steering, automations + thread automations, browser use + browser comments + Codex for Chrome, computer use, Codex subagents (basic + forked + nested + creating), worktrees flow, agents.md & memories, chronicle, MCP Servers, plugins, Paper Design MCP

**Trade-off**: 9 days is a big commitment to sell. Some students who already bought the `codex` class will feel double-charged (mitigated by your note that workshop buyers retain full class access). Big upside: positions Codex App as a *parallel platform*, not a verifier — which matches how it's actually being used in your daily workflow (per the `workflows` class showing Multi Clauding flows). This day could also be the "Day 7.5" optional add-on for a coaching tier.

## Migration map (chapter-level)

Sources annotated as `class → chapter`. Where a chapter splits, the split is noted.

| Workshop slot | ACS sources |
|---|---|
| Day 0 (async) | `claude-code → Set Up & Workflows`, `claude-code → Plug Ins`, `claude-code → Shortcuts`, `claude-code → Niche Features` (ergonomic subset: `/recap`, `/export`, Output Styles, Aliases, Custom Statusline, Fullscreen TUI, Sandboxing), `codex → Codex CLI → A Quick Build` |
| Day 1 Alignment | `claude-code → Spec Developer`, `claude-code → Planning`, `prompt-engineering → Goal In Strategy Out + Infusing Lived Experience`, `fundamental-techniques → Clarifying Questions + Customized Terminology + Multimodal Models for PRDs + Artifact Planning`, content stubs (Status of Agents, Missions trio, models-drift, auto-advancing-design) |
| Day 2 Steering | `fundamental-techniques → Long Context Failure + Dealing with Syncophancy + Just Run It Again`, `context-engineering → Cognitive Inertia + Instruction Following Limits + Signal to Noise`, `claude-code → Advanced → Auto Compact & Handoff`, content stubs (sycophancy, asking-for-options, long-context trio, Rewinding, Ordering, Compaction) |
| Day 3 CLAUDE.md & Context Layer *(extended only)* | `claude-code → CLAUDE.md` (all 8 videos), `context-engineering → Progressive Disclosure + The Context Layer + Anatomy of a Node + Example + Maintenance`, content stubs (files-matter-less, Markdown over architecture *moved up from Skills*) |
| Day 4 Subagents & Multi-Clauding | `claude-code → Subagents` (all 9 videos), `claude-code → 1M Context Window` (all 5), `workflows → Multi Clauding + How I Use Worktrees`, `advanced-techniques → Multi Subagents for Hard Problems + Refactoring with Subagents`, `fundamental-techniques → Context Switching + Reducing Agent Confusion`, content stubs (Subagent Architectures, CLIs vs MCPs, context-strategy) |
| Day 5 Skills | `claude-code → Skills` (all 14 videos), `advanced-techniques → Blog Post to Skill + Skills + Explore Subagents`, `prompt-engineering → Scaling Taste + Persona Vectors + Distribution Steering`, content stubs (Off-distribution, teach-models-like-your-engineers, Creating Skills, Types of Skills, Forked Contexts for Skills, Skills + Subagents) |
| Day 6 Automation & Workflows | `claude-code → Hooks` (all 4), `claude-code → Automation` (all 8), `claude-code → Connecting to Codex`, `workflows → Data Analysis + Extract Wisdom + Designing Components + Quick Benchmarking + Interactive HTML Artifacts`, `advanced-techniques → Git Diffs & Mermaid Diagrams`, `claude-code → Advanced → Frontend Design Skill + /autofix-pr`, content stubs (Workflows, Every PR, OpenAI Symphony, Automate Anything) |
| Day 7 Verification | `claude-code → Niche Features → /security-review + /ultrareview + /advisor + /team-onboarding`, `claude-code → Connecting to Codex → Codex Consult + Codex MCP Server`, `advanced-techniques → Planning Convergence + Automatic Plan Reviewing with Subagents + Benchmarking Tools & MCPs`, `fundamental-techniques → Logging + Understanding Agent Output + Agent Introspection`, content stubs (Languages, Verification Architectures, Adversarial Reviewers, agent-benchmark-harness) |
| Day 8 Agent Teams & Loopy AI | `claude-code → Subagent Teams`, `claude-code → Advanced → Headless Mode + /loop + Monitor Tool + Push Notifications + Ralph Loop + Task List Management + Plan Directory & Archiving + Claude Code Guide Subagent`, `prompt-engineering → Archetype Teams + Living Archetypes`, `advanced-techniques → Autoresearch Overview + Technical Example + Non-Technical Example + Mixing Models & Modes + Combining CLIs & Models`, content stubs (agent-teams archetypes, Ralph, Autoresearch, Removing Bottlenecks) |
| Day 9 Codex App *(codex variant only)* | `codex → Codex App` (all 38 videos), `claude-code → Connecting to Codex` (split — basic intro moves here, verifier flows stay on Day 7) |

## Trade-offs of each proposal

- **Pick A1 (status quo) if**: you want to ship the workshop fast and treat CLAUDE.md as something students learn in the class on their own. Lightest content load, but largest pedagogical gap.
- **Pick A1-revised if**: you want minimal disruption to the locked structure and are OK with Day 1 and Day 3 getting heavier. Best if you've already started recording Day 1 content.
- **Pick A1-extended (8 days) if**: you want the curriculum to match the ACS chapter shape and CLAUDE.md to be the day students remember. Best pedagogical fit. Requires re-pricing the workshop or accepting that some days will be shorter live sessions to keep total hours reasonable.
- **Pick A1-extended-codex (9 days) if**: you want to position the workshop as "agentic coding" not "Claude Code with Codex". Best if there's a clear coaching/$3k tier where the Codex App day lives as a bonus, OR if Codex App is genuinely where you spend most of your daily workflow time now and the workshop should reflect that.

My pick if forced: **A1-extended (8 days)**. CLAUDE.md getting its own day is the single biggest pedagogical win in this whole survey — the catalogue has 8 dedicated videos for it, students will recognise it from the start of the Master Claude Code class, and it gives the workshop a memorable "Day 3 changes everything" beat. Codex App can stay where A1 had it (sprinkled into Day 7 / Day 6) — promote it to its own day only if the Codex MCP changes the workshop's positioning.
