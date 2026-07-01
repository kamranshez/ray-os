---
title: BoundaryML "AI That Works" -> ACS content-gap index
source_channel: https://www.youtube.com/@boundaryml
podcast: AI That Works (Vaibhav Gupta / BoundaryML + Dexter Horthy / HumanLayer)
date: 2026-07-01
status: in-progress
batches_done: 2
episodes_analyzed: 20
---

## What this is

Every BoundaryML "AI That Works" episode run through the `wisdom-to-acs-gap` skill: one report per
episode (spine idea -> deep dive -> ranked ACS video pitches -> full wisdom). This index ranks the
film-able video ideas the channel implies and clusters the ones that recur across episodes.

**Progress:** Batches 1-2 of 7 done (20 / 63 full episodes).
**Tally so far:** 🔴 29 net-new pitches | 🔗 26 complement | 🟡 1 partial | 55 total across 20 episodes. Every episode cleared the gate (`posted`).

---

## Strongest signals: themes that recur across episodes

Recurrence across independent episodes is the best evidence an idea is worth its own video. Ranked by
how many distinct episodes hit it.

### 1. Tool-call is ONE primitive; shape the schema the model was trained on  (7+ episodes)
The single biggest theme. Inline tools / MCP / bash / code-mode are swappable renderings of one
primitive; models are RL'd onto a specific tool schema; the leverage move is reshaping your tools and
data to match (or deliberately mismatch) it, and pruning the schema the agent sees at runtime.
- Code Mode: Stop Calling Tools One at a Time (Bash Holding Agents Back)
- Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing (Bash Holding Agents Back)
- Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows (Context vs Harness)
- Match the Tool Shape or Pay the Compounding Tax (Outsmart the Model Makers)
- Design the Exact Tools Your Agent Sees (Give Your AI New Abilities)
- The Only Time You Should Reach for MCP + Your Skills Are Bloating Context (Give Your AI New Abilities; Agents/Subagents/Skills)

### 2. Design the feedback loop / back pressure FIRST  (6 episodes)
Give a taste-blind agent a deterministic, observable signal to self-correct against, and design it
before writing code. Feature flags, profiling loops, visual unit tests, compilers/hooks, product-fuzzing.
- Design the Back Pressure First (Agentic Backpressure)
- Give Your Agent Back Pressure It Doesn't Have Yet (Safely Ship to Production)
- Measure Before You Optimize: Build the Agent's Feedback Loop (Performance Engineering)
- Unit Test Your UI: The Fastest Feedback Loop (Practical AI Assembly Line)
- Make Your Product Debug Itself With an Agent Loop (Self-Healing Loop)

### 3. Learning tests: prove the black box before you build  (3 episodes)
Have the agent write a throwaway probe that proves how a closed API / CLI / LLM actually behaves,
so design is grounded in observed behavior instead of docs that lie.
- Learning Tests: Stop Trusting the Docs, Prove the Behavior (No-Rework Workflow)
- Prove It Before You Build It: Learning Tests for Black-Box APIs (Agentic Backpressure)
- (grounds the Streaming Masterclass build too)

### 4. Design-first: perfect the spec / iterate the doc, not the code  (3 episodes)
Front-load the irreversible decisions onto a cheap doc, iterate the doc, and let the agent one-shot
the build; never edit complex docs in place, rewrite them.
- Perfect the Spec, One-Shot the Build (Build Faster by Coding Slower)
- Iterate the Doc, Not the Code (No-Rework Workflow)
- Rewrite, Do Not Edit (Can an AI Out-Plan a Senior Engineer?)

### 5. Everything is a nested while loop  (2 episodes)
- Software Is Just Stacking While Loops (Outsmart the Model Makers)
- Agents, Sub-Agents, Orchestrators: It Is All One While Loop (Context vs Harness)

### 6. Agent security is an architecture problem  (2 episodes, new in Batch 2)
- The Lethal Trifecta: One Email Away From Deleting Your Database (Prompt-Hackers)
- Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream (Prompt-Hackers)
- Scrub Your Secrets Before Claude Code Sends Them to Anthropic (Scrub Sensitive Data)

---

## 🔴 Net-new video ideas (all batches, theme-tagged)

Theme key: TOOLS, LOOP, PROBE, SPEC, HARNESS, SEC, MODEL, ORCH, LANG, UI, PLAN.

| Proposed ACS video | Theme | Slot (class > chapter) | Source episode | Report |
|--------------------|-------|------------------------|----------------|--------|
| Code Mode: Stop Calling Tools One at a Time | TOOLS | Context Engineering > agent execution environments | Bash Holding Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |
| Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing | TOOLS | Context Engineering > foundational | Bash Holding Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |
| Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows | TOOLS | Claude Code > agent-harness-concept | Context vs Harness vs SW Eng | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Match the Tool Shape or Pay the Compounding Tax | TOOLS | Techniques > Harness Internals (new) | Outsmart the Model Makers | [link](2026-07-01-outsmart-the-model-makers.md) |
| Design the Exact Tools Your Agent Sees | TOOLS | Advanced Techniques > designing-interfaces | Give Your AI New Abilities | [link](2026-07-01-give-your-ai-new-abilities.md) |
| Skills or Subagents? The Two Questions That Decide | TOOLS | Claude Code > skills-vs-subagents | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| Design the Back Pressure First | LOOP | Techniques > Closing the Loop | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Point the Agent at the Source of Truth | LOOP | Context Engineering > Grounding and Research | Performance Engineering | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Learning Tests: Stop Trusting the Docs, Prove the Behavior | PROBE | Context Engineering > Grounding in empirical proof | No-Rework Workflow | [link](2026-07-01-no-rework-workflow.md) |
| Prove It Before You Build It: Learning Tests for Black-Box APIs | PROBE | Context Engineering > Understanding the System | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Testing Systems That Never Answer the Same Way Twice | PROBE | Techniques > Evals for Agents (new) | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| Streaming Is An Architecture, Not A Feature | SPEC | Techniques > building agent products (new) | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Steer A Running Agent: The Database Is Your Control Channel | SPEC | Techniques > building agent products | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Pure vs Wired: Architecting Your Codebase So Agents Can Work | SPEC | Context Engineering > codebase architecture for agents | Practical AI Assembly Line | [link](2026-07-01-practical-ai-assembly-line.md) |
| The Lethal Trifecta: One Email Away From Deleting Your Database | SEC | DevBoxes / Claude Code > blast radius and security | Prompt-Hackers Coming for Your Data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream | SEC | Techniques > agent-building | Prompt-Hackers Coming for Your Data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| Scrub Your Secrets Before Claude Code Sends Them to Anthropic | SEC | Claude Code (enterprise / DevBoxes) or Business | Scrub Sensitive Data | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| The Harness Has No Moat (And Why That's Good for You) | HARNESS | Claude Code > agent-harness-concept | Outsmart the Model Makers | [link](2026-07-01-outsmart-the-model-makers.md) |
| Beat the Compiler: When to Override Claude Code (and When Not To) | HARNESS | Techniques > decision-framework (new) | Context vs Harness vs SW Eng | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Run a Fleet of Coding Agents Through One Issue Tracker | ORCH | Claude Code > agent orchestration | Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| One Coordination Repo Beats Your Git Submodules | ORCH | Claude Code > Workspace Organization | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| Automate 90%, Gate the One Way Doors | PLAN | Claude Code > automation boundaries (new) | Automate Complex Workflows with Claude | [link](2026-07-01-automate-complex-workflows-claude.md) |
| Make the Other Mistake: Calibrating How Much to Plan | PLAN | Techniques > developing instinct / Start Here | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Fight Slop With Slop: Disposable Tools That Make Great Docs | SPEC | Techniques > Scaffolding | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Make the Model Fight You: Surfacing Decisions You Cannot See | SPEC | Prompt Engineering > Make the Model Push Back | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Let Your Agent Ship to Prod Without Letting It Turn Things On | LOOP | Master Claude Code > Safe Production Rollouts (new) | Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| Make Your Agent Work in Any Language Without Forking Your Pipeline | LANG | Techniques > Normalize to Your Pipeline (new) | Build AI Agents in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| Why New Models Rarely Change Everything | MODEL | Techniques > Working With Model Releases | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |
| Build Your Own Private Model Benchmark | MODEL | My Daily Workflows > Model Evaluation | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |
| Review Only What Changed From the Plan | PLAN | Techniques > Multi-Agent Orchestration / correction | Why Your AI Coding Agent Writes Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |

## 🔗 Complement video ideas (next step beyond an existing ACS video)

| Proposed ACS video | Complements | Source episode | Report |
|--------------------|-------------|----------------|--------|
| Perfect the Spec, One-Shot the Build | build-it-twice | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| Iterate the Doc, Not the Code: The No-Rework Decision Gate | build-it-twice | No-Rework Workflow | [link](2026-07-01-no-rework-workflow.md) |
| Rewrite, Do Not Edit: Why Agents Wreck In-Place Doc Edits | build-it-twice | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Vertical Planning: Make Every Phase Testable | build-small-merge-big | No-Rework Workflow | [link](2026-07-01-no-rework-workflow.md) |
| Unit Test Your UI: The Fastest Feedback Loop for Coding Agents | closing-the-loop | Practical AI Assembly Line | [link](2026-07-01-practical-ai-assembly-line.md) |
| Measure Before You Optimize: Build the Agent's Feedback Loop | closing-the-loop | Performance Engineering | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Give Your Agent Back Pressure It Doesn't Have Yet | closing-the-loop | Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| Make Your Product Debug Itself With an Agent Loop | closing-the-loop | Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| The Checker Catches What the Builder Missed | closing-the-loop | Scrub Sensitive Data | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| Catch the One Wrong Line: Human Judgment in Unfakeable Work | what-breaks-if-i-change-this | Performance Engineering | [link](2026-07-01-performance-engineering-human-judgment.md) |
| The Only Time You Should Reach for MCP | clis-vs-mcps | Give Your AI New Abilities | [link](2026-07-01-give-your-ai-new-abilities.md) |
| Your Skills Are Bloating Context Just Like MCPs | clis-vs-mcps | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| Claude Code as the Front End for Your CLIs | high-level-strategy-low-level-details | Automate Complex Workflows | [link](2026-07-01-automate-complex-workflows-claude.md) |
| Let the Agent Learn the Clicks, Then Bake Them | Claude CoWork 07 Browser Automation | Automate Complex Workflows | [link](2026-07-01-automate-complex-workflows-claude.md) |
| A CLAUDE.md That One-Shots The Hard Thing | skills-as-team-knowledge-base | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Give the Model Options, Not Orders | 01-steering-distributions | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| Structured Output Won't Save You (validation vs injection) | structured-output | Prompt-Hackers Coming for Your Data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| Your Output Schema Is Part of the Prompt | structured-output | Build AI Agents in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| Software Is Just Stacking While Loops | test-time-compute | Outsmart the Model Makers | [link](2026-07-01-outsmart-the-model-makers.md) |
| Agents, Sub-Agents, Orchestrators: It Is All One While Loop | agent-harness-concept + core-agent-loop | Context vs Harness vs SW Eng | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Why Your Agent Writes Bad Code (design split) | the-shifting-bottleneck | Why Your AI Coding Agent Writes Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Delete Your CLAUDE.md, Point to Architecture Files Instead | delete-your-readme | Why Your AI Coding Agent Writes Bad Code | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| The First Thing to Do When a New Model Drops | goal-in-strategy-out | Testing Claude Fable 5 | [link](2026-07-01-testing-claude-fable-5.md) |
| Stop Guessing Your Skill: Put Every Version in an Arena | simplify-skill | Self-Healing Agent Loop | [link](2026-07-01-self-healing-agent-loop.md) |
| Why Your Agent Is Good at Bash and Bad at Sed | gravitational-pull-from-older-models | Bash Holding Agents Back | [link](2026-07-01-bash-holding-agents-back.md) |

## 🟡 Partial

| Proposed ACS video | Fills gap in | Source episode | Report |
|--------------------|--------------|----------------|--------|
| Your Prompt Has an Instruction Budget, Not Just an Information Budget | Context Engineering class | Scrub Sensitive Data | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |

---

## Per-episode index

| # | Episode | Spine (one line) | Verdict | Report |
|---|---------|------------------|---------|--------|
| B1 | The Self-Healing Agent Loop | Point agents at your own product to manufacture bug signal, then fix it with other agents | 🔴1 🔗2 | [link](2026-07-01-self-healing-agent-loop.md) |
| B1 | Why Your AI Coding Agent Writes Bad Code | Split design into product / technical / program so decisions land upstream | 🔴1 🔗2 | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| B1 | Why Performance Engineering Needs Human Judgment | Performance engineering is a data-driven feedback loop you also run on your agent | 🔴1 🔗2 | [link](2026-07-01-performance-engineering-human-judgment.md) |
| B1 | Testing Claude Fable 5 | Test comprehension before completion on your hardest live problem | 🔴2 🔗1 | [link](2026-07-01-testing-claude-fable-5.md) |
| B1 | How AI Agents Can Safely Ship to Production | Feature flags manufacture back pressure; split merge-to-prod from turn-it-on | 🔴1 🔗1 | [link](2026-07-01-safely-ship-code-to-production.md) |
| B1 | How to Build AI Agents in Any Language | Normalize every language to one English pipeline wrapped with translation units | 🔴1 🔗1 | [link](2026-07-01-agents-in-any-language.md) |
| B1 | Why Bash Might Be Holding AI Agents Back | Inline / MCP / bash / code-mode are one tool-call primitive; code mode wins | 🔴2 🔗1 | [link](2026-07-01-bash-holding-agents-back.md) |
| B1 | Can You Outsmart the Model Makers? | The harness has no moat; match the tool schema the model was post-trained on | 🔴2 🔗1 | [link](2026-07-01-outsmart-the-model-makers.md) |
| B1 | Can an AI Out-Plan a Senior Engineer? | Fight AI slop with disposable AI-built tooling that scaffolds your real doc | 🔴2 🔗1 | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| B1 | Context vs Harness vs Software Engineering | Models are RL'd onto one tool schema; reshape tools to match, do not fine-tune | 🔴2 🔗1 | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| B2 | Building a Practical AI Assembly Line | Give the agent an isolated render harness (Storybook) as a visual unit test | 🔴1 🔗1 | [link](2026-07-01-practical-ai-assembly-line.md) |
| B2 | Streaming Systems Masterclass | Streaming is a ground-up architecture (yield, not bolt-on); control via DB write-back | 🔴2 🔗1 | [link](2026-07-01-streaming-systems-masterclass.md) |
| B2 | Build Faster by Coding Slower | Pour hours into the spec so the agent one-shots the build | 🔴1 🔗2 | [link](2026-07-01-build-faster-by-coding-slower.md) |
| B2 | The Right Way to Give Your AI New Abilities | MCP only for user-brought tools; shape the exact tool schema at runtime | 🔴1 🔗1 | [link](2026-07-01-give-your-ai-new-abilities.md) |
| B2 | Prompt-Hackers Are Coming for Your Data | Prompt injection is architecture: kill one leg of the untrusted+private+outbound trifecta | 🔴2 🔗1 | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| B2 | How to Scrub Sensitive Data Before It Reaches Your LLM | Stop PII at a redaction proxy; scrubbing is a software-placement problem | 🔴1 🔗1 🟡1 | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| B2 | Agents, Subagents, Skills and Commands | Context isolation and instruction modules are orthogonal; skills finally separate them | 🔴2 🔗1 | [link](2026-07-01-agents-subagents-skills-commands.md) |
| B2 | The No-Rework Workflow for AI Coding Assistants | Learning tests + iterate the doc not the code + vertical-slice planning | 🔴1 🔗2 | [link](2026-07-01-no-rework-workflow.md) |
| B2 | How to Automate Complex Workflows with Claude | Automate incrementally; permanently gate only the irreversible one-way doors | 🔴1 🔗2 | [link](2026-07-01-automate-complex-workflows-claude.md) |
| B2 | Agentic Backpressure Deep Dive | Learning tests for black boxes + design the back pressure before code | 🔴2 🔗1 | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
