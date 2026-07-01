---
title: BoundaryML "AI That Works" -> ACS content-gap index
source_channel: https://www.youtube.com/@boundaryml
podcast: AI That Works (Vaibhav Gupta / BoundaryML + Dexter Horthy / HumanLayer)
date: 2026-07-01
status: in-progress
batches_done: 1
episodes_analyzed: 10
---

## What this is

Every BoundaryML "AI That Works" episode run through the `wisdom-to-acs-gap` skill: one report per
episode (spine idea -> deep dive -> ranked ACS video pitches -> full wisdom). This index ranks the
film-able video ideas the channel implies, best first, each linking to its full brief.

**Progress:** Batch 1 of 7 done (10 / 63 full episodes). Counts below are Batch 1 only.

**Batch 1 tally:** 🔴 15 net-new pitches | 🔗 13 complement pitches | 28 total across 10 episodes. Every episode posted (all cleared the gate).

---

## Strongest signals: themes that recur across episodes

These reframes showed up as a spine in more than one episode. Recurrence across independent episodes
is the strongest evidence an idea is worth a video.

1. **The tool-call is one primitive; match the schema the model was RL'd on.** (Ep: Bash Holding Agents Back, Context vs Harness vs SW Eng) The move is reshaping your tools/data to mimic primitives the model already masters, not fine-tuning. Two episodes land this independently.
2. **Code mode: let the agent write one script that calls many tools.** (Ep: Bash Holding Agents Back; echoed in the harness episodes) Beats one-call-at-a-time by shaping output and capping round-trips.
3. **Everything is a nested while loop.** (Ep: Outsmart the Model Makers, Context vs Harness vs SW Eng) Agents, sub-agents, harnesses, orchestrators are one primitive; "always build the next loop."
4. **Manufacture the feedback signal the agent lacks.** (Ep: Self-Healing Loop, Performance Engineering, Safely Ship to Prod) Feature flags / product fuzzing / profiling loops all give a taste-blind agent a metric to self-correct against.

---

## 🔴 Net-new video ideas (ranked, best first)

| # | Proposed ACS video | Slot (class > chapter) | Source episode | Report |
|---|--------------------|------------------------|----------------|--------|
| 1 | Code Mode: Stop Calling Tools One at a Time | Context Engineering > agent execution environments | Why Bash Might Be Holding AI Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |
| 2 | Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing | Context Engineering > foundational | Why Bash Might Be Holding AI Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |
| 3 | Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows | Claude Code > agent-harness-concept | Context vs Harness vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| 4 | Match the Tool Shape or Pay the Compounding Tax | Techniques > Harness Internals (new) | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| 5 | The Harness Has No Moat (And Why That's Good for You) | Claude Code > agent-harness-concept | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| 6 | Beat the Compiler: When to Override Claude Code (and When Not To) | Techniques > decision-framework (new) | Context vs Harness vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| 7 | Run a Fleet of Coding Agents Through One Issue Tracker | Claude Code > agent orchestration | The Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| 8 | Fight Slop With Slop: Disposable Tools That Make Great Docs | Techniques > Scaffolding | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| 9 | Make the Model Fight You: Surfacing Decisions You Cannot See | Prompt Engineering > Make the Model Push Back | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| 10 | Let Your Agent Ship to Prod Without Letting It Turn Things On | Master Claude Code > Safe Production Rollouts (new) | How AI Agents Can Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| 11 | Make Your Agent Work in Any Language Without Forking Your Pipeline | Techniques > Normalize to Your Pipeline (new) | How to Build AI Agents That Work in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| 12 | Point the Agent at the Source of Truth | Context Engineering > Grounding and Research | Why Performance Engineering Still Requires Human Judgment | [link](2026-07-01-performance-engineering-human-judgment.md) |
| 13 | Review Only What Changed From the Plan | Techniques > Multi-Agent Orchestration / correction | Why Your AI Coding Agent Keeps Writing Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| 14 | Why New Models Rarely Change Everything | Techniques > Working With Model Releases | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |
| 15 | Build Your Own Private Model Benchmark | My Daily Workflows > Model Evaluation | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |

## 🔗 Complement video ideas (next step beyond an existing ACS video)

| Proposed ACS video | Complements | Source episode | Report |
|--------------------|-------------|----------------|--------|
| Why Your Agent Writes Bad Code (And the Design Split That Fixes It) | the-shifting-bottleneck | Why Your AI Coding Agent Keeps Writing Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Delete Your CLAUDE.md, Point to Architecture Files Instead | delete-your-readme | Why Your AI Coding Agent Keeps Writing Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Software Is Just Stacking While Loops | test-time-compute | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| Agents, Sub-Agents, Orchestrators: It Is All One While Loop | agent-harness-concept + core-agent-loop | Context vs Harness vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Make Your Product Debug Itself With an Agent Loop | closing-the-loop | The Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| Stop Guessing Your Skill: Put Every Version in an Arena | simplify-skill | The Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| Measure Before You Optimize: Build the Agent's Feedback Loop | closing-the-loop | Why Performance Engineering Still Requires Human Judgment | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Catch the One Wrong Line: Human Judgment in Unfakeable Work | what-breaks-if-i-change-this | Why Performance Engineering Still Requires Human Judgment | [link](2026-07-01-performance-engineering-human-judgment.md) |
| The First Thing to Do When a New Model Drops | goal-in-strategy-out | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |
| Give Your Agent Back Pressure It Doesn't Have Yet | closing-the-loop | How AI Agents Can Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| Your Output Schema Is Part of the Prompt | structured-output (PE Foundations) | How to Build AI Agents That Work in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| Why Your Agent Is Good at Bash and Bad at Sed | gravitational-pull-from-older-models | Why Bash Might Be Holding AI Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |
| Rewrite, Do Not Edit: Why Agents Wreck In-Place Doc Edits | build-it-twice | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |

---

## Per-episode index (Batch 1)

| Episode | Spine (one line) | Verdict | Report |
|---------|------------------|---------|--------|
| The Self-Healing Agent Loop | Point agents at your own product to manufacture bug signal, then fix it with other agents | 🔴1 🔗2 | [link](2026-07-01-self-healing-agent-loop.md) |
| Why Your AI Coding Agent Writes Bad Code | Split design into product / technical / program so decisions land upstream | 🔴1 🔗2 | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Why Performance Engineering Needs Human Judgment | Performance engineering is a data-driven feedback loop you also run on your agent | 🔴1 🔗2 | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Testing Claude Fable 5 | Test comprehension before completion on your hardest live problem | 🔴2 🔗1 | [link](2026-07-01-testing-claude-fable-5.md) |
| How AI Agents Can Safely Ship to Production | Feature flags manufacture back pressure; split merge-to-prod from turn-it-on | 🔴1 🔗1 | [link](2026-07-01-safely-ship-code-to-production.md) |
| How to Build AI Agents in Any Language | Normalize every language to one English pipeline wrapped with translation units | 🔴1 🔗1 | [link](2026-07-01-agents-in-any-language.md) |
| Why Bash Might Be Holding AI Agents Back | Inline / MCP / bash / code-mode are one tool-call primitive; code mode wins | 🔴2 🔗1 | [link](2026-07-01-bash-holding-agents-back.md) |
| Can You Outsmart the Model Makers? | The harness has no moat; match the tool schema the model was post-trained on | 🔴2 🔗1 | [link](2026-07-01-outsmart-the-model-makers.md) |
| Can an AI Out-Plan a Senior Engineer? | Fight AI slop with disposable AI-built tooling that scaffolds your real doc | 🔴2 🔗1 | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Context vs Harness vs Software Engineering | Models are RL'd onto one tool schema; reshape tools to match, do not fine-tune | 🔴2 🔗1 | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
