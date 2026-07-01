---
title: BoundaryML "AI That Works" -> ACS content-gap index
source_channel: https://www.youtube.com/@boundaryml
podcast: AI That Works (Vaibhav Gupta / BoundaryML + Dexter Horthy / HumanLayer)
date: 2026-07-01
status: in-progress
episodes_analyzed: 30
---

## What this is

Every BoundaryML "AI That Works" episode run through the `wisdom-to-acs-gap` skill: one report per
episode (spine idea -> deep dive -> ranked ACS video pitches -> full wisdom). This index ranks the
film-able video ideas the channel implies and clusters the ones that recur across episodes.

**Progress:** 30 of 63 full episodes analyzed (~3 batches). Every episode cleared the gate (`posted`).
**Pitch tally:** 🔴 40 net-new | 🔗 40 complement | 🟡 2 partial | 82 total.

## Strongest signals: themes that recur across episodes

Recurrence across independent episodes is the best evidence an idea is worth its own video. Ranked by
how many distinct episodes hit it. Each bullet names the proposed video and its source episode.

### 1. Tool-call is ONE primitive; shape the schema the model was trained on  (8+ episodes)
Inline tools / MCP / bash / code-mode are swappable renderings of one primitive; models are RL'd onto a
specific tool schema; leverage = reshape your tools and data to match it, and prune the schema the agent
sees at runtime. Includes the "Skills or MCP or just write code" decision.
- Code Mode: Stop Calling Tools One at a Time (Bash Holding Agents Back)
- Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing (Bash Holding Agents Back)
- Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows (Context vs Harness)
- Match the Tool Shape or Pay the Compounding Tax (Outsmart the Model Makers)
- Design the Exact Tools Your Agent Sees (Give Your AI New Abilities)
- Skills or Subagents? The Two Questions That Decide (Agents, Subagents, Skills and Commands)
- Skills or MCP or Just Write the Code (Founding HumanLayer)

### 2. Design the feedback loop / back pressure FIRST  (7 episodes)
Give a taste-blind agent a deterministic, observable signal to self-correct against, designed before code.
Feature flags, profiling loops, visual unit tests, compilers/hooks, product-fuzzing, richer failure signal.
- Design the Back Pressure First (Agentic Backpressure)
- Give Your Agent Back Pressure It Doesn't Have Yet (Safely Ship to Production)
- Measure Before You Optimize (Performance Engineering)
- Unit Test Your UI: The Fastest Feedback Loop (Practical AI Assembly Line)
- Make Your Product Debug Itself (Self-Healing Loop)
- Feed the Loop Better: Give Your Fixing Agent the Whole Test (Building a Prompt Optimizer)

### 3. Determinism: if you know the steps, use code not a prompt  (3 episodes, strengthening)
Keep control flow in code; use typed structured outputs as the seams between LLM phases; do not push a
known workflow into one overloaded prompt.
- If You Know the Steps, Don't Use an Agent (12-Factor Coding Agent SDKs)
- Control Flow Belongs in Code, Not Your Prompt (Founding HumanLayer)
- Structured Output as the seam between phases (Prompting Is a Product Surface; Build Faster)

### 4. Evals without a golden dataset: invariant-based grading  (3 episodes)
Grade AI pipelines with structural invariants you already know must hold, then promote those checks into a
self-correcting online product. Ship at 97% instead of chasing a perfect prompt.
- Evals With No Answer Key (Multimodal Evals)
- Ship at 97%: Turning Eval Checks Into a Self-Correcting Product (Multimodal Evals)
- Testing Systems That Never Answer the Same Way Twice (Build Faster by Coding Slower)

### 5. Learning tests: prove the black box before you build  (3 episodes)
Have the agent write a throwaway probe that proves how a closed API / CLI / LLM actually behaves, so design
is grounded in observed behavior, not docs that lie.
- Learning Tests: Stop Trusting the Docs, Prove the Behavior (No-Rework Workflow)
- Prove It Before You Build It: Learning Tests for Black-Box APIs (Agentic Backpressure)
- Hide the Goal: Honest Research From an Agent (Claude Code Maxing)

### 6. Design-first: perfect the spec / iterate the doc, not the code  (3 episodes)
Front-load irreversible decisions onto a cheap doc, iterate the doc, let the agent one-shot the build; never
edit complex docs in place, rewrite them.
- Perfect the Spec, One-Shot the Build (Build Faster by Coding Slower)
- Iterate the Doc, Not the Code (No-Rework Workflow)
- Rewrite, Do Not Edit (Can an AI Out-Plan a Senior Engineer?)

### 7. Agent security is an architecture problem  (3 episodes)
- The Lethal Trifecta: One Email Away From Deleting Your Database (Prompt-Hackers)
- Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream (Prompt-Hackers)
- Scrub Your Secrets Before Claude Code Sends Them to Anthropic (Scrub Sensitive Data)
- Structured Output Is Your Injection Tripwire (Prompting Is a Product Surface)

### 8. Everything is a nested while loop  (2 episodes)
- Software Is Just Stacking While Loops (Outsmart the Model Makers)
- Agents, Sub-Agents, Orchestrators: It Is All One While Loop (Context vs Harness)

### New single-episode standouts worth filming (Batch 3)
- Ship AI Code Without Code Reviews: architecture guardrails + magnitude-gated sign-off (Claude Code Maxing)
- Make Your Agent Feel 10x Faster Without Touching the Model: latency is perception (Understanding Latency)
- Build Prefetch for Your Coding Agent: speculative read-only prefix via permission gating (Understanding Latency)
- Email Is Your Agent's Front Door + Build an Agent That Can Be Interrupted Mid Task (Email is All You Need)
- Build a Prompt Optimizer From Scratch: GEPA-style automated optimization (Building a Prompt Optimizer)
- The Manager Agent That Merges Your Parallel Worktrees For You (Git Worktrees + Agents)

---

## 🔴 Net-new video ideas (40)

| Proposed ACS video | Slot (class > chapter) | Source episode | Report |
|--------------------|------------------------|----------------|--------|
| Run a Fleet of Coding Agents Through One Issue Tracker | Claude Code > agent orchestration (near building-effective-agent-teams / self-modifying-claude-md) | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-07-01-self-healing-agent-loop.md) |
| Review Only What Changed From the Plan | techniques > Multi-Agent Orchestration / correction | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Point the Agent at the Source of Truth | Context Engineering > Grounding and Research | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Why New Models Rarely Change Everything | Techniques > Working With Model Releases | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-07-01-testing-claude-fable-5.md) |
| Build Your Own Private Model Benchmark | My Daily Workflows > Model Evaluation | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-07-01-testing-claude-fable-5.md) |
| Let Your Agent Ship to Prod Without Letting It Turn Things On | Master Claude Code > new Safe Production Rollouts chapter | How AI Agents Can Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| Make Your Agent Work in Any Language Without Forking Your Pipeline | Techniques > new "Normalize to Your Pipeline" pattern | How to Build AI Agents That Work in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| Code Mode: Stop Calling Tools One at a Time | Context Engineering > agent execution environments (or Bonus Techniques) | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-07-01-bash-holding-agents-back.md) |
| Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing | Context Engineering > foundational (or Master Claude Code > mcps and connectors) | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-07-01-bash-holding-agents-back.md) |
| Match the Tool Shape or Pay the Compounding Tax | Techniques > Harness Internals (new chapter) | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| The Harness Has No Moat (And Why That's Good for You) | Claude Code > agent-harness-concept (bare backlog title, no script) | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| Fight Slop With Slop: Disposable Tools That Make Great Docs | Techniques > Scaffolding: Tools That Build Your Work | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Make the Model Fight You: Surfacing the Design Decisions You Cannot See | Prompt Engineering > Make the Model Push Back | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows | Claude Code > agent-harness-concept (or new Designing Tools and MCPs chapter) | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Beat the Compiler: When to Override Claude Code (and When Not To) | Techniques > new decision-framework chapter | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Pure vs Wired: Architecting Your Codebase So Agents Can Actually Work | Context Engineering > codebase architecture for agents (adjacent to backlog designing-interfaces) | Building a Practical AI Assembly Line | [link](2026-07-01-practical-ai-assembly-line.md) |
| Streaming Is An Architecture, Not A Feature | Techniques > building agent products / real-time systems (new chapter) | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Steer A Running Agent: The Database Is Your Control Channel | Techniques > building agent products (sequel to pitch 1) | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Testing Systems That Never Answer the Same Way Twice | Techniques > new Evals for Agents chapter | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| Design the Exact Tools Your Agent Sees | Advanced Techniques > designing-interfaces | The Right Way to Give Your AI New Abilities | [link](2026-07-01-give-your-ai-new-abilities.md) |
| The Lethal Trifecta: Why Your Agent Is One Email Away From Deleting Your Database | DevBoxes (planned) or Claude Code > blast radius and security chapter | Prompt-Hackers are coming for your data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream | Techniques > agent-building | Prompt-Hackers are coming for your data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| Scrub Your Secrets Before Claude Code Sends Them to Anthropic | Claude Code class (enterprise rollout / DevBoxes) or Business | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| Skills or Subagents? The Two Questions That Decide | Claude Code > skills-vs-subagents | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| One Coordination Repo Beats Your Git Submodules | Claude Code > Workspace Organization | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| Learning Tests: Stop Trusting the Docs, Prove the Behavior | Context Engineering > Grounding context in empirical proof | The No-Rework Workflow for AI Coding Assistants | [link](2026-07-01-no-rework-workflow.md) |
| Automate 90%, Gate the One Way Doors | Claude Code > automation boundaries (new) | How to Automate Complex Workflows with Claude | [link](2026-07-01-automate-complex-workflows-claude.md) |
| Prove It Before You Build It: Learning Tests for Black-Box APIs | Context Engineering > Understanding the System | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Make the Other Mistake: Calibrating How Much to Plan | Techniques > developing instinct / Start Here | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Structured Output Is Your Injection Tripwire | Techniques > reliability/safety | Prompting Is Becoming a Product Surface | [link](2026-07-01-prompting-is-a-product-surface.md) |
| Build an Agent That Can Be Interrupted Mid Task | Techniques > core-agent-loop / closing-the-loop / designing-interfaces | Email is All You Need | [link](2026-07-01-email-is-all-you-need.md) |
| Email Is Your Agent's Front Door | Techniques (agent architecture); seeds Business > agent-mail | Email is All You Need | [link](2026-07-01-email-is-all-you-need.md) |
| Make Your Agent Feel 10x Faster Without Touching the Model | Techniques class > new chapter Designing Agentic UX | Understanding Latency | [link](2026-07-01-understanding-latency.md) |
| Build Prefetch for Your Coding Agent | Claude Code class > near blocking-risky-commands-with-hooks / background-hooks | Understanding Latency | [link](2026-07-01-understanding-latency.md) |
| Skills or MCP or Just Write the Code: The Decision That Ends the Confusion | Claude Skills class > foundations | Founding HumanLayer | [link](2026-07-01-founding-humanlayer.md) |
| Build a Prompt Optimizer From Scratch | Prompt Engineering > new chapter: Automated Prompt Optimization | Building a Prompt Optimizer | [link](2026-07-01-building-a-prompt-optimizer.md) |
| How to Ship AI Code Without Code Reviews | Techniques (or Context Engineering) | Claude Code Maxing - live coding | [link](2026-07-01-claude-code-maxing-live-coding.md) |
| If You Know the Steps, Don't Use an Agent | Techniques > new Agent Architecture chapter | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-07-01-12-factor-coding-agent-sdks.md) |
| Evals With No Answer Key: Grading AI When You Have No Labels | Techniques class > new Evaluating AI Pipelines chapter | Multimodal Evals | [link](2026-07-01-multimodal-evals.md) |
| Design the Data Shape First: Three Disjoint Pipelines, One Contract | Context Engineering class > new Designing the Data Contract chapter | Multimodal Evals | [link](2026-07-01-multimodal-evals.md) |

## 🔗 Complement video ideas (40)

| Proposed ACS video | Complements | Source episode | Report |
|--------------------|-------------|----------------|--------|
| Make Your Product Debug Itself With an Agent Loop | closing-the-loop | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-07-01-self-healing-agent-loop.md) |
| Stop Guessing Your Skill: Put Every Version in an Arena | simplify-skill | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-07-01-self-healing-agent-loop.md) |
| Why Your Agent Writes Bad Code (And the Design Split That Fixes It) | the-shifting-bottleneck | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Delete Your CLAUDE.md, Point to Architecture Files Instead | delete-your-readme | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| Measure Before You Optimize: Build the Agent's Feedback Loop | Closing the Loop | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-07-01-performance-engineering-human-judgment.md) |
| Catch the One Wrong Line: Human Judgment in Unfakeable Work | What Breaks If I Change This? | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-07-01-performance-engineering-human-judgment.md) |
| The First Thing to Do When a New Model Drops | goal-in-strategy-out | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-07-01-testing-claude-fable-5.md) |
| Give Your Agent Back Pressure It Doesn't Have Yet | closing-the-loop | How AI Agents Can Safely Ship Code to Production | [link](2026-07-01-safely-ship-code-to-production.md) |
| Your Output Schema Is Part of the Prompt | planned "structured-output" foundations | How to Build AI Agents That Work in Any Language | [link](2026-07-01-agents-in-any-language.md) |
| Why Your Agent Is Good at Bash and Bad at Sed | gravitational-pull-from-older-models | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-07-01-bash-holding-agents-back.md) |
| Software Is Just Stacking While Loops | test-time-compute | Can You Outsmart the Model Makers? | [link](2026-07-01-outsmart-the-model-makers.md) |
| Rewrite, Do Not Edit: Why Agents Wreck In-Place Doc Edits | Build It Twice | Can an AI Out-Plan a Senior Engineer? | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| Agents, Sub-Agents, Orchestrators: It Is All One While Loop | planned agent-harness-concept + core-agent-loop | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| Unit Test Your UI: The Fastest Feedback Loop for Coding Agents | closing-the-loop | Building a Practical AI Assembly Line | [link](2026-07-01-practical-ai-assembly-line.md) |
| A CLAUDE.md That One-Shots The Hard Thing | skills-as-team-knowledge-base / global-claude-md-personal-profile | Streaming Systems Masterclass | [link](2026-07-01-streaming-systems-masterclass.md) |
| Perfect the Spec, One-Shot the Build | build-it-twice | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| Give the Model Options, Not Orders | Prompt Engineering 01-steering-distributions | Build Faster by Coding Slower | [link](2026-07-01-build-faster-by-coding-slower.md) |
| The Only Time You Should Reach for MCP | clis-vs-mcps | The Right Way to Give Your AI New Abilities | [link](2026-07-01-give-your-ai-new-abilities.md) |
| Structured Output Won't Save You: The Validation That Turns Injections Into Errors | structured-output | Prompt-Hackers are coming for your data | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| The Checker Catches What the Builder Missed | closing-the-loop | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| Your Skills Are Bloating Context Just Like MCPs | clis-vs-mcps | Agents, Subagents, Skills and Commands | [link](2026-07-01-agents-subagents-skills-commands.md) |
| Iterate the Doc, Not the Code: The No-Rework Decision Gate | build-it-twice | The No-Rework Workflow for AI Coding Assistants | [link](2026-07-01-no-rework-workflow.md) |
| Vertical Planning: Make Every Phase Testable | build-small-merge-big | The No-Rework Workflow for AI Coding Assistants | [link](2026-07-01-no-rework-workflow.md) |
| Let the Agent Learn the Clicks, Then Bake Them | Claude CoWork 07 Browser Automation | How to Automate Complex Workflows with Claude | [link](2026-07-01-automate-complex-workflows-claude.md) |
| Claude Code as the Front End for Your CLIs | high-level-strategy-low-level-details | How to Automate Complex Workflows with Claude | [link](2026-07-01-automate-complex-workflows-claude.md) |
| Design the Back Pressure First | Closing the Loop | Agentic Backpressure Deep Dive | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| Let Your Users Design the Schema | Prompt Engineering Foundations 'structured-output | Prompting Is Becoming a Product Surface | [link](2026-07-01-prompting-is-a-product-surface.md) |
| Turn Your Inbox Into an Agent You Delegate To | Airtable Memory for Cloud Scheduled Tasks | Email is All You Need | [link](2026-07-01-email-is-all-you-need.md) |
| Order Your Prompt for the Cache, Not for Humans | the shipped Context Engineering class | Understanding Latency | [link](2026-07-01-understanding-latency.md) |
| Only Run the Tests Your Change Can Break | closing-the-loop | Founding Boundary | [link](2026-07-01-founding-boundary.md) |
| Delete Your Docs, Rebuild Context: The RPI Loop | Delete Your README | Founding HumanLayer | [link](2026-07-01-founding-humanlayer.md) |
| Control Flow Belongs in Code, Not Your Prompt | Boxing the Model In | Founding HumanLayer | [link](2026-07-01-founding-humanlayer.md) |
| Feed the Loop Better: Give Your Fixing Agent the Whole Test | closing-the-loop | Building a Prompt Optimizer | [link](2026-07-01-building-a-prompt-optimizer.md) |
| The Manager Agent That Merges Your Parallel Worktrees For You | the in-progress "worktrees" video | Git Worktrees + Agents | [link](2026-07-01-git-worktrees-plus-agents.md) |
| Fan Out Five Agents, Then Cherry-Pick The Best Answer | the planned stochastic-consensus-and-fan-out-fan-in / test-time-comput | Git Worktrees + Agents | [link](2026-07-01-git-worktrees-plus-agents.md) |
| Hide the Goal: How to Get Honest Research From an Agent | What breaks if I change this? | Claude Code Maxing - live coding | [link](2026-07-01-claude-code-maxing-live-coding.md) |
| Stop Writing Horizontal Plans | Build Small, Merge Big | Claude Code Maxing - live coding | [link](2026-07-01-claude-code-maxing-live-coding.md) |
| The Background Agent That Checks Your Work | subagent-verification-loops | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-07-01-12-factor-coding-agent-sdks.md) |
| The Diffable Architecture Map That Stops Vibe Rot | What Breaks If I Change This? | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-07-01-12-factor-coding-agent-sdks.md) |
| Ship at 97%: Turning Eval Checks Into a Self-Correcting Product | building-inner-and-outer-feedback-loops | Multimodal Evals | [link](2026-07-01-multimodal-evals.md) |

## 🟡 Partial (2)

| Proposed ACS video | Note | Source episode | Report |
|--------------------|------|----------------|--------|
| Your Prompt Has an Instruction Budget, Not Just an Information Budget | 🟡 fills gap in Context Engineering class | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| Treat the Model Like the Plus Operator | 🟡 fills gap in "structured-output" (Prompt Engineering foundations): adds resilient parsing of malformed/recursive output and the streaming dual-type problem | Founding Boundary | [link](2026-07-01-founding-boundary.md) |

---

## Per-episode index

| # | Episode | Spine (one line) | Verdict | Report |
|---|---------|------------------|---------|--------|
| B1 | The Self-Healing Agent Loop That Fixes Its Own Language | The self-healing product loop: point agents at your own product to manufacture the bug signal, then feed it back as issu... | 🔴1 🔗2 | [link](2026-07-01-self-healing-agent-loop.md) |
| B1 | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | Split the design phase into product, technical, and program design so architectural decisions land upstream where you ha... | 🔴1 🔗2 | [link](2026-07-01-why-ai-agent-writes-bad-code.md) |
| B1 | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | Performance engineering is really a data-driven feedback loop, and the same loop (workloads, standard deviations, JSON-s... | 🔴1 🔗2 | [link](2026-07-01-performance-engineering-human-judgment.md) |
| B1 | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | When a new model ships, test comprehension before completion: ask it to restate your architecture on your hardest LIVE p... | 🔴2 🔗1 | [link](2026-07-01-testing-claude-fable-5.md) |
| B1 | How AI Agents Can Safely Ship Code to Production | Feature flags manufacture back pressure where agents have none, turning unmeasurable UI/taste work into production metri... | 🔴1 🔗1 | [link](2026-07-01-safely-ship-code-to-production.md) |
| B1 | How to Build AI Agents That Work in Any Language | Normalize every language to one evaluable English pipeline wrapped with translation-in and translation-out units, instea... | 🔴1 🔗1 | [link](2026-07-01-agents-in-any-language.md) |
| B1 | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | Inline tools, MCPs, bash, and code mode are all just implementations of one primitive, the tool call, so stop arguing ab... | 🔴2 🔗1 | [link](2026-07-01-bash-holding-agents-back.md) |
| B1 | Can You Outsmart the Model Makers? | The harness has no moat: because the agent runs on your machine over an observable API, you can always reverse-engineer ... | 🔴2 🔗1 | [link](2026-07-01-outsmart-the-model-makers.md) |
| B1 | Can an AI Out-Plan a Senior Engineer? | Fight AI slop with slop: build throwaway, AI-generated internal tooling you never read as scaffolding that makes your re... | 🔴2 🔗1 | [link](2026-07-01-ai-outplan-senior-engineer.md) |
| B1 | Context Engineering vs Harness Engineering vs Software Engineering | Models are RL'd onto one specific tool schema (Claude Code learned old-string/new-string, Codex learned apply-patch), so... | 🔴2 🔗1 | [link](2026-07-01-context-vs-harness-vs-software-engineering.md) |
| B2 | Building a Practical AI Assembly Line | Give the coding agent an isolated render harness (Storybook) so it iterates on a single component's props instead of boo... | 🔴1 🔗1 | [link](2026-07-01-practical-ai-assembly-line.md) |
| B2 | Streaming Systems Masterclass | Streaming is a ground-up architectural decision, not a feature you bolt on later: model everything as yield and pass que... | 🔴2 🔗1 | [link](2026-07-01-streaming-systems-masterclass.md) |
| B2 | Build Faster by Coding Slower | Pour hours into the spec so the agent one-shots the entire build, because a 200-line spec becomes thousands of lines and... | 🔴1 🔗2 | [link](2026-07-01-build-faster-by-coding-slower.md) |
| B2 | The Right Way to Give Your AI New Abilities | MCP's only justifiable use is letting your product's users bring their own long-tail tools; everything you control shoul... | 🔴1 🔗1 | [link](2026-07-01-give-your-ai-new-abilities.md) |
| B2 | Prompt-Hackers are coming for your data | Prompt injection is an architecture problem, not a wording problem: an agent is exploitable only when untrusted input, p... | 🔴2 🔗1 | [link](2026-07-01-prompt-hackers-coming-for-data.md) |
| B2 | How to Scrub Sensitive Data Before it Reaches Your LLM | Stop sensitive data at a redaction proxy that intercepts the outbound request and runs a local detect-redact-restore pip... | 🔴1 🔗1 🟡1 | [link](2026-07-01-scrub-sensitive-data-before-llm.md) |
| B2 | Agents, Subagents, Skills and Commands | Context isolation and instruction modules are two orthogonal jobs; subagents were overloaded to do both, and skills fina... | 🔴2 🔗1 | [link](2026-07-01-agents-subagents-skills-commands.md) |
| B2 | The No-Rework Workflow for AI Coding Assistants | Write throwaway learning tests that actually run an opaque dependency and assert on its real output, so design is ground... | 🔴1 🔗2 | [link](2026-07-01-no-rework-workflow.md) |
| B2 | How to Automate Complex Workflows with Claude | Automate incrementally with STOP-for-human markers and permanently gate only the irreversible one-way doors (mass email,... | 🔴1 🔗2 | [link](2026-07-01-automate-complex-workflows-claude.md) |
| B2 | Agentic Backpressure Deep Dive | Learning tests: have the agent write a throwaway probe that proves how a black-box system (closed API, CLI, LLM) actuall... | 🔴2 🔗1 | [link](2026-07-01-agentic-backpressure-deep-dive.md) |
| B3 | Prompting Is Becoming a Product Surface | Expose the schema, not the prompt string, as the thing users configure, using a dynamic type system that escalates from ... | 🔴1 🔗1 | [link](2026-07-01-prompting-is-a-product-surface.md) |
| B3 | Email is All You Need | Design agents for async, interrupting inputs from day one: because you never own the UI, serialize each thread, defer ir... | 🔴2 🔗1 | [link](2026-07-01-email-is-all-you-need.md) |
| B3 | Understanding Latency | Latency is a perception problem, not a speed problem: you cannot beat competitors on raw model speed, so you win by maki... | 🔴2 🔗1 | [link](2026-07-01-understanding-latency.md) |
| B3 | Founding Boundary | When the test suite is too big to run per change, predict from the git diff which tests the change can affect and run on... | 🔴0 🔗1 🟡1 | [link](2026-07-01-founding-boundary.md) |
| B3 | Founding HumanLayer | Skills over MCP: use the file system plus bash plus a markdown skill as the substrate for connecting an agent to service... | 🔴1 🔗2 | [link](2026-07-01-founding-humanlayer.md) |
| B3 | Building a Prompt Optimizer | Prompt optimization is now a build-it-yourself commodity: point an automated GEPA-style optimizer at the prompts you wil... | 🔴1 🔗1 | [link](2026-07-01-building-a-prompt-optimizer.md) |
| B3 | Git Worktrees + Agents | Because worktrees share one git object database, a manager agent on main can continuously merge sibling worktree branche... | 🔴0 🔗2 | [link](2026-07-01-git-worktrees-plus-agents.md) |
| B3 | Claude Code Maxing - live coding | Ship AI code without code reviews by replacing per-line review with automated architecture guardrails (auto-generated de... | 🔴1 🔗2 | [link](2026-07-01-claude-code-maxing-live-coding.md) |
| B3 | Applying 12-Factor Principles to Coding Agent SDKs | If you know the workflow order, encode it as deterministic control flow, not a prompt, using typed structured outputs as... | 🔴1 🔗2 | [link](2026-07-01-12-factor-coding-agent-sdks.md) |
| B3 | Multimodal Evals | Evaluate a multimodal extraction pipeline with zero labeled data by encoding structural invariants you already know must... | 🔴2 🔗1 | [link](2026-07-01-multimodal-evals.md) |
