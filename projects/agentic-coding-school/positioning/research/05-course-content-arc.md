# 05 — Course Content & Transformation Arc

**Source:** Agentic Coding School content MCP (classes, videos, transcripts). Pulled 2026-06-26.
**Why this file matters:** to write "agent engineer" copy *honestly*, we need what the curriculum actually teaches beyond tool basics. It backs the identity — the substance is real.

## Curriculum map — 9 classes
The two big "tool" courses are the on-ramp; the durable, identity-level material lives in the six smaller classes.

| Class | Slug | Videos | What it really is |
|---|---|---|---|
| Master Claude Code | `claude-code` | 158 | Tool fundamentals, zero-to-hero (on-ramp) |
| Master Codex | `codex` | 58 | Tool fundamentals for OpenAI Codex |
| Techniques | `fundamental-techniques` | 17 | Durable judgment: context mgmt, planning, debugging, hygiene |
| Advanced Techniques | `advanced-techniques` | 21 | Multi-model, multi-agent orchestration, legacy rewriting |
| **Loopy AI** | `loopy-ai` | 43 | **"Loop engineering" — flagship advanced class (L1→L7 ladder)** |
| Context Engineering | `context-engineering` | 11 | Building a "context layer" over large production codebases |
| Prompt Engineering | `prompt-engineering` | 13 | Aligning agents to intent, steering, personas/taste |
| My Daily Workflows | `workflows` | 15 | Ray's actual working setup |
| For Business | `for-business` | 7 | Non-technical/business use cases |

Real chapter spines: Loopy AI = "L1: Getting Started → L2: Builder & Verifier → L3: Task Lifecycle → L4 & L5: The Climb → Command & Control → Compounding Loops → L6: Governance → L7: Closing." Context Engineering = "Foundations → The Solution Paradigm → Build a Context Layer." Prompt Engineering = "Letting the Model Lead," "Seeding with You," "Personas and Archetypes."

## The advanced/durable skills (beyond "click these buttons")
- **Loop engineering** (Loopy AI, 43 lessons) — design self-running agent loops with explicit primitives (trigger, unit of work, completion check, exit condition, token/time cap, persistent state) so work continues after you close your laptop.
- **Builder/Verifier orchestration** — never let an agent grade its own work; separate-context verifier fails work back to the builder until a bar is met.
- **Verifier design** ("Don't Verify Against the Plan," "Real Verifiers Touch Reality," "Verifiers Go Stale," "Where to Set the Bar," "Sycophantic Attackers") — decide what to verify against; spot drift/rubber-stamping.
- **Context engineering / "context layer"** ("Progressive Disclosure," "The Context Layer," "Anatomy of a Node") — architect CLAUDE.md/AGENTS.md layer nodes at semantic boundaries + skills + hooks so a mediocre prompt yields senior-level output on a 2.5M-token codebase.
- **Multi-agent orchestration** — "Refactoring with Subagents," "Multi Subagents for Hard Problems," "Coverage Through Stochastic Starting Points," "Subagent Teams for Debugging," "Automatic Plan Reviewing with Subagents."
- **Parallelization / fan-out** — many subagents from stochastic starting points; parallel PR-review loops.
- **Planning** ("Starting in Plan Mode," "Artifact Planning," "High Level Coherence, Low Level Implementation," "Planning Convergence").
- **Context/session management** ("Long Context Failure," "Signal to Noise," "Cognitive Inertia," "Just Run It Again").
- **Steering / intent alignment** ("Goal In, Strategy Out," "Boxing the Agent In," "Distribution Steering," "Persona Vectors," "Scaling Taste").
- **Autonomy dial & command-and-control** ("The Autonomy Dial," "Decision Surfaces," "Slack as Your Command Center," "Mission Command").
- **Compounding / self-improving loops** ("The Self-Improvement Loop," "Teach the Agent How to Learn," "The Three Role Split (ACE)," "Echo Chamber Failure Mode").
- **Governance** ("Governance Primitives," "Skills as Code").
- **Legacy-code judgment** ("Gravitational Pull from Older Models," "The One-Pattern Rule for Agents").

## Transformation arc (from → to)
- From prompting a single agent + manually checking → to builder/verifier loops that converge automatically against reality.
- From writing longer prompts → to engineering a *context layer* so any mediocre prompt yields senior-level results.
- From one agent/one task/one session → to orchestrating teams of parallel subagents with adversarial review.
- From babysitting the loop → to running L4 worker loops off a backlog + L5 discovery loops that find their own work, you on the autonomy dial via Slack/Mission Command.
- From knowledge trapped in your head → to encoding senior judgment as context-layer/skills-as-code that raises a whole team's floor and compounds across model generations.

**One line a senior respects:** moves you from *operating* an AI coding tool to *engineering the systems* (loops, verifiers, context layers, agent teams, governance) that let agents do reliable work unattended at scale.

## "Loop engineering" specifically (the Loopy AI spine)
"Design AI loops that keep working when you close your laptop."
- **Primitives:** trigger (cron/event/human), unit of work, completion check, exit condition (incl. token/timeout caps), persistent state (Gmail tags, filesystem, GitHub issues, Supabase, Slack).
- **L1→L7 ladder:** L1 bare harness → **L2 builder/verifier** (separate-context verifier + adversarial review, stop criteria) → **L3 full task lifecycle** (spec→build→review→user-flow verify→PR→merge→post-deploy monitor, as a reusable skill) → **L4 worker loops** (pull from backlog) → **L5 discovery loops** (find new work) → **L6 governance** (skills as code) → **L7 command/taste/remove yourself as bottleneck.**
- **Toolbox:** slash commands, monitors, headless mode, local/cloud routines, routine memory, `/goal`.

## Best proof points (for copy)
- Add one line to a prompt → builder + verifier → visibly better output, agent does the click-around verification for you.
- **Ray ran a single goal for 19 hours that verified ~300 Chrome user flows** (241 passed, 66 partial, 16 failing surfaced) — and **Boris (Claude Code creator) replied "Nice."** Screenshot-backed. *(Ray's own result, not a student's — frame as "what the method makes possible.")*
- Build a context layer so adding a feature flag to a 2.5M-token codebase stops silently breaking prod.
- Ship a reusable L3 lifecycle skill: spec → merged PR + post-deploy monitoring + auto-hotfix.
- L4 backlog-burndown loops turn a pile of issues/PRs into reviewed, ready-to-merge work in parallel.
- A junior + a good context layer prompts simply and the agent writes at senior level → team floor rises.

## Caveats (honesty guardrails for copy)
- **Heavily Claude Code/Anthropic-centric** (158-video CC class; examples lean on Claude in Chrome, Cloud Routines, `/goal`, hooks). "Tool-agnostic agent engineering" is partly aspirational (Context Engineering does argue the layer is model/CLI-portable via AGENTS.md).
- **Loopy AI is still in production** — L1 has "(Still Editing...)" and many lessons `isCompleted: false`. Don't claim fully shipped if launch depends on it.
- Some titles have typos ("Gravitional," "Redunant," "Syncophancy") — don't quote verbatim.
- The 19hr/300-flow + "Nice" is **Ray's** result, not a student's.
- "Loop engineering" is Ray's framing for the **Loopy AI** class; no module is literally titled "Loop Engineering." Substance real; label is a positioning choice.
