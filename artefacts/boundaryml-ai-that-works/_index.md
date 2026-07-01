---
title: BoundaryML "AI That Works" -> ACS content-gap index
source_channel: https://www.youtube.com/@boundaryml
podcast: AI That Works (Vaibhav Gupta / BoundaryML + Dexter Horthy / HumanLayer)
date: 2026-07-01
status: in-progress
episodes_analyzed: 63
---

## What this is

Every BoundaryML "AI That Works" episode run through the `wisdom-to-acs-gap` skill: one report per
episode (spine idea -> deep dive -> ranked ACS video pitches -> full wisdom). This index ranks the
film-able video ideas the channel implies and clusters the ones that recur across episodes.

**Progress:** 63 of 63 full episodes analyzed (~7 batches). Every episode cleared the gate (`posted`).
**Pitch tally:** 🔴 80 net-new | 🔗 92 complement | 🟡 4 partial | 176 total.

## Strongest signals: themes that recur across the whole channel

The full 63-episode sweep. Recurrence across independent episodes is the best evidence an idea is worth
its own video. Clusters are ranked by how many distinct episodes hit them; each names the proposed video
and its source episode. **The top 6 clusters are the channel's real "definitely film this" signals.**

### 1. The tool-call is ONE primitive; shape the schema the model was trained on  (~9 episodes)
The channel's single most-repeated argument. Inline tools / MCP / bash / code-mode are swappable renderings
of one primitive; models are RL'd onto a specific tool schema; bash and a custom CLI you own beat MCP
because every schema word is tokens that degrade accuracy; the leverage move is reshaping tools and pruning
the schema the agent sees at runtime (including aliasing names and routing 1000+ tools via retrieval).
- Code Mode: Stop Calling Tools One at a Time (Bash Holding Agents Back)
- Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing (Bash Holding Agents Back)
- Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows (Context vs Harness)
- Match the Tool Shape or Pay the Compounding Tax (Outsmart the Model Makers)
- Design the Exact Tools Your Agent Sees (Give Your AI New Abilities)
- Why I Deleted My MCPs and Wrote Bash Instead (Bash vs MCP for Coding Agents)
- Skills or Subagents? / Skills or MCP or Just Write the Code (Agents Subagents Skills; Founding HumanLayer)
- Route 1000 MCP Tools With One LLM Function + The Text You Embed Is Not the Text the LLM Sees (Large Scale Classification)

### 2. Decompose the black box into typed, tunable stages; offload work off the LLM  (~8 episodes)
Never one giant model call. Split into extract/resolve/enrich (or research/plan/implement) typed functions,
each swappable for a heuristic / small model / big model, with a hard per-stage guarantee. Build probe
points you can unit-test. Deterministic glue between focused prompts.
- Stop Looping the LLM on Errors: Build a Coding Agent as Deterministic Glue (Building a Coding Bot)
- Stop Writing One Giant Prompt: Turn Extraction Into Typed Functions (Entity Extraction)
- Build Probe Points Into Your LLM Pipeline (Large Scale Classification)
- If You Know the Steps, Don't Use an Agent (12-Factor Coding Agent SDKs)
- Why Your Actor Checker Loop Costs 10x Too Much (Reasoning Models vs Prompts)

### 3. Design the feedback loop / back pressure FIRST; deterministic signals over LLM-judge  (~8 episodes)
Give a taste-blind agent a deterministic, observable signal to self-correct against, and design it before
writing code. Feature flags, profiling loops, visual unit tests, compilers/hooks, probe points, product-fuzzing.
- Design the Back Pressure First (Agentic Backpressure)
- Give Your Agent Back Pressure It Doesn't Have Yet (Safely Ship to Production)
- Measure Before You Optimize (Performance Engineering)
- Unit Test Your UI: The Fastest Feedback Loop (Practical AI Assembly Line)
- Make Your Product Debug Itself (Self-Healing Loop)
- Feed the Loop Better: Give Your Fixing Agent the Whole Test (Building a Prompt Optimizer)

### 4. The schema/data model IS the prompt; reshape the schema, not the prose  (~7 episodes)
Field names silently steer the model; an enum forces self-classification and kills a hallucination class;
when a field underperforms, change the schema (string -> string[]) rather than reword. Design the data shape
first and keep pipelines disjoint. Output as a deterministic intermediate representation software finishes.
- Change the Schema, Not the Prompt (Getting Tone Right with LLMs)
- Design the Data Shape First: Three Disjoint Pipelines, One Contract (Multimodal Evals)
- Your Output Schema Is Part of the Prompt (Build AI Agents in Any Language)
- Let Your Users Design the Schema (Prompting Is a Product Surface)
- Stop Asking the Model to Compute. Ask It for a Blueprint. (Dates, Times, and LLMs)

### 5. Context is a projection you render, not a log you append; engineer memory deliberately  (~7 episodes)
The context window is a projection computed from history (write a projection function); model the agent as an
append-only event log; memory = decaying resolution + stateful per-tenant tools; author context retroactively
by deleting failed turns; pack context deterministically instead of trusting agentic search or a static CLAUDE.md.
- Stop Mutating State: Build Your Agent as an Event Log (Event Driven Agent Loops)
- Decaying Resolution Memory: Teach Your Agent To Forget On Purpose (Context & Memory Deep Dive)
- Stateful Tools Are Your Agent's Memory And Its Security Boundary (Context & Memory Deep Dive)
- Lie to Your Agent: Rewrite Its History So Every Failure Disappears (Building a Coding Bot)
- Deterministic Context Packing: make print-context Beats Agentic Search (Claude for Non-Code Tasks)
- Why Claude Ignores Your CLAUDE.md, and What To Do Instead (Bash vs MCP / Claude for Non-Code Tasks)

### 6. Evals: invariant-based grading, golden cases from real runs, no answer key  (~6 episodes)
Grade AI pipelines with structural invariants you already know must hold; capture one real run as a golden
case and iterate the prompt in isolation (synthetic data is the worst input); ship at 97% via self-correction
instead of chasing a perfect prompt; for conversations, a green/red on-track timeline is the KPI.
- Evals With No Answer Key + Ship at 97% (Multimodal Evals)
- Testing Systems That Never Answer the Same Way Twice (Build Faster by Coding Slower)
- Turn Real Runs Into Golden Test Cases (YouTube to Email/X)
- The Only Voice-Agent Eval That Matters: A Green-and-Red Timeline (Voice Agents)

### 7. Design-first: build the harness / spec before the AI; iterate the doc, not the code  (~6 episodes)
Front-load irreversible decisions onto a cheap doc, iterate the doc, let the agent one-shot the build; build
the whole product harness first and bolt the AI on last; never edit complex docs in place, rewrite them;
reuse a verified diff as the next spec.
- Perfect the Spec, One-Shot the Build (Build Faster by Coding Slower)
- Iterate the Doc, Not the Code (No-Rework Workflow)
- Build the Harness Before You Touch the AI (YouTube to Email/X)
- Rewrite, Do Not Edit (Can an AI Out-Plan a Senior Engineer?)
- Your Best Spec Is Last Week's Diff (No Vibes Allowed #33)

### 8. Async / interruptible / event-driven agents; steer a running job out of band  (~5 episodes)
You never own the UI, so design for async interrupting inputs from day one; supervisor threading re-steers a
live agent by rewriting its context; control a running job via DB write-back and one cancellation checkpoint.
- Build an Agent That Can Be Interrupted Mid Task + Email Is Your Agent's Front Door (Email is All You Need)
- The Supervisor Thread: Re-Steer an Agent That Went Off the Rails (Voice Agents)
- Steer A Running Agent: The Database Is Your Control Channel (Streaming Systems Masterclass)

### 9. Agent security is an architecture problem  (~4 episodes)
- The Lethal Trifecta: One Email Away From Deleting Your Database (Prompt-Hackers)
- Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream (Prompt-Hackers)
- Scrub Your Secrets Before Claude Code Sends Them to Anthropic (Scrub Sensitive Data)
- Structured Output Is Your Injection Tripwire (Prompting Is a Product Surface)

### 10. Latency is perception; hide it with optimistic execution and prefetch  (~3 episodes)
- Make Your Agent Feel 10x Faster Without Touching the Model + Build Prefetch for Your Coding Agent (Understanding Latency)
- Start Talking Before You Think: The Latency Trick From Voice Agents (Voice Agents)
- Pipeline Your LLM Stream: Start Work Before Generation Finishes (Generative UIs)

### Also strong: model routing, reasoning-as-behavior, nested while loops, Claude-as-general-agent
- Route Every Step to the Cheapest Model That Works (Building a Coding Bot); You Do Not Need a Reasoning Model (Reasoning Models vs Prompts)
- Software Is Just Stacking While Loops (Outsmart); It Is All One While Loop (Context vs Harness)
- Run Your Company on Markdown: Claude Code as Your CRM and Back Office (Claude for Non-Code Tasks)
- Ship AI Code Without Code Reviews: architecture guardrails + magnitude-gated sign-off (Claude Code Maxing)

---

## 🔴 Net-new video ideas (80)

| Proposed ACS video | Slot (class > chapter) | Source episode | Report |
|--------------------|------------------------|----------------|--------|
| Run a Fleet of Coding Agents Through One Issue Tracker | Claude Code > agent orchestration (near building-effective-agent-teams / self-modifying-claude-md) | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-06-26-self-healing-agent-loop.md) |
| Review Only What Changed From the Plan | techniques > Multi-Agent Orchestration / correction | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-06-19-why-ai-agent-writes-bad-code.md) |
| Point the Agent at the Source of Truth | Context Engineering > Grounding and Research | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-06-12-performance-engineering-human-judgment.md) |
| Why New Models Rarely Change Everything | Techniques > Working With Model Releases | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-06-13-testing-claude-fable-5.md) |
| Build Your Own Private Model Benchmark | My Daily Workflows > Model Evaluation | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-06-13-testing-claude-fable-5.md) |
| Let Your Agent Ship to Prod Without Letting It Turn Things On | Master Claude Code > new Safe Production Rollouts chapter | How AI Agents Can Safely Ship Code to Production | [link](2026-06-05-safely-ship-code-to-production.md) |
| Make Your Agent Work in Any Language Without Forking Your Pipeline | Techniques > new "Normalize to Your Pipeline" pattern | How to Build AI Agents That Work in Any Language | [link](2026-06-05-agents-in-any-language.md) |
| Code Mode: Stop Calling Tools One at a Time | Context Engineering > agent execution environments (or Bonus Techniques) | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-06-01-bash-holding-agents-back.md) |
| Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing | Context Engineering > foundational (or Master Claude Code > mcps and connectors) | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-06-01-bash-holding-agents-back.md) |
| Match the Tool Shape or Pay the Compounding Tax | Techniques > Harness Internals (new chapter) | Can You Outsmart the Model Makers? | [link](2026-05-11-outsmart-the-model-makers.md) |
| The Harness Has No Moat (And Why That's Good for You) | Claude Code > agent-harness-concept (bare backlog title, no script) | Can You Outsmart the Model Makers? | [link](2026-05-11-outsmart-the-model-makers.md) |
| Fight Slop With Slop: Disposable Tools That Make Great Docs | Techniques > Scaffolding: Tools That Build Your Work | Can an AI Out-Plan a Senior Engineer? | [link](2026-05-04-ai-outplan-senior-engineer.md) |
| Make the Model Fight You: Surfacing the Design Decisions You Cannot See | Prompt Engineering > Make the Model Push Back | Can an AI Out-Plan a Senior Engineer? | [link](2026-05-04-ai-outplan-senior-engineer.md) |
| Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows | Claude Code > agent-harness-concept (or new Designing Tools and MCPs chapter) | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-04-27-context-vs-harness-vs-software-engineering.md) |
| Beat the Compiler: When to Override Claude Code (and When Not To) | Techniques > new decision-framework chapter | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-04-27-context-vs-harness-vs-software-engineering.md) |
| Pure vs Wired: Architecting Your Codebase So Agents Can Actually Work | Context Engineering > codebase architecture for agents (adjacent to backlog designing-interfaces) | Building a Practical AI Assembly Line | [link](2026-04-20-practical-ai-assembly-line.md) |
| Streaming Is An Architecture, Not A Feature | Techniques > building agent products / real-time systems (new chapter) | Streaming Systems Masterclass | [link](2026-04-13-streaming-systems-masterclass.md) |
| Steer A Running Agent: The Database Is Your Control Channel | Techniques > building agent products (sequel to pitch 1) | Streaming Systems Masterclass | [link](2026-04-13-streaming-systems-masterclass.md) |
| Testing Systems That Never Answer the Same Way Twice | Techniques > new Evals for Agents chapter | Build Faster by Coding Slower | [link](2026-04-06-build-faster-by-coding-slower.md) |
| Design the Exact Tools Your Agent Sees | Advanced Techniques > designing-interfaces | The Right Way to Give Your AI New Abilities | [link](2026-03-30-give-your-ai-new-abilities.md) |
| The Lethal Trifecta: Why Your Agent Is One Email Away From Deleting Your Database | DevBoxes (planned) or Claude Code > blast radius and security chapter | Prompt-Hackers are coming for your data | [link](2026-03-23-prompt-hackers-coming-for-data.md) |
| Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream | Techniques > agent-building | Prompt-Hackers are coming for your data | [link](2026-03-23-prompt-hackers-coming-for-data.md) |
| Scrub Your Secrets Before Claude Code Sends Them to Anthropic | Claude Code class (enterprise rollout / DevBoxes) or Business | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-03-09-scrub-sensitive-data-before-llm.md) |
| Skills or Subagents? The Two Questions That Decide | Claude Code > skills-vs-subagents | Agents, Subagents, Skills and Commands | [link](2026-03-16-agents-subagents-skills-commands.md) |
| One Coordination Repo Beats Your Git Submodules | Claude Code > Workspace Organization | Agents, Subagents, Skills and Commands | [link](2026-03-16-agents-subagents-skills-commands.md) |
| Learning Tests: Stop Trusting the Docs, Prove the Behavior | Context Engineering > Grounding context in empirical proof | The No-Rework Workflow for AI Coding Assistants | [link](2026-03-02-no-rework-workflow.md) |
| Automate 90%, Gate the One Way Doors | Claude Code > automation boundaries (new) | How to Automate Complex Workflows with Claude | [link](2026-02-23-automate-complex-workflows-claude.md) |
| Prove It Before You Build It: Learning Tests for Black-Box APIs | Context Engineering > Understanding the System | Agentic Backpressure Deep Dive | [link](2026-02-16-agentic-backpressure-deep-dive.md) |
| Make the Other Mistake: Calibrating How Much to Plan | Techniques > developing instinct / Start Here | Agentic Backpressure Deep Dive | [link](2026-02-16-agentic-backpressure-deep-dive.md) |
| Structured Output Is Your Injection Tripwire | Techniques > reliability/safety | Prompting Is Becoming a Product Surface | [link](2026-02-09-prompting-is-a-product-surface.md) |
| Build an Agent That Can Be Interrupted Mid Task | Techniques > core-agent-loop / closing-the-loop / designing-interfaces | Email is All You Need | [link](2026-01-26-email-is-all-you-need.md) |
| Email Is Your Agent's Front Door | Techniques (agent architecture); seeds Business > agent-mail | Email is All You Need | [link](2026-01-26-email-is-all-you-need.md) |
| Make Your Agent Feel 10x Faster Without Touching the Model | Techniques class > new chapter Designing Agentic UX | Understanding Latency | [link](2026-01-12-understanding-latency.md) |
| Build Prefetch for Your Coding Agent | Claude Code class > near blocking-risky-commands-with-hooks / background-hooks | Understanding Latency | [link](2026-01-12-understanding-latency.md) |
| Skills or MCP or Just Write the Code: The Decision That Ends the Confusion | Claude Skills class > foundations | Founding HumanLayer | [link](2025-12-29-founding-humanlayer.md) |
| Build a Prompt Optimizer From Scratch | Prompt Engineering > new chapter: Automated Prompt Optimization | Building a Prompt Optimizer | [link](2025-12-22-building-a-prompt-optimizer.md) |
| How to Ship AI Code Without Code Reviews | Techniques (or Context Engineering) | Claude Code Maxing - live coding | [link](2026-02-02-claude-code-maxing-live-coding.md) |
| If You Know the Steps, Don't Use an Agent | Techniques > new Agent Architecture chapter | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-01-19-12-factor-coding-agent-sdks.md) |
| Evals With No Answer Key: Grading AI When You Have No Labels | Techniques class > new Evaluating AI Pipelines chapter | Multimodal Evals | [link](2025-12-08-multimodal-evals.md) |
| Design the Data Shape First: Three Disjoint Pipelines, One Contract | Context Engineering class > new Designing the Data Contract chapter | Multimodal Evals | [link](2025-12-08-multimodal-evals.md) |
| Never Let the Model Read Your JSON | Context Engineering > handling large structured data | Building Animation Pipelines | [link](2025-11-25-building-animation-pipelines.md) |
| Treat the Model Like a User: One Timezone, Zero Timezone Bugs | context-engineering (new video in shipped class) | Dates, Times, and LLMs #31 | [link](2025-11-12-dates-times-and-llms.md) |
| Stop Mutating State: Build Your Agent as an Event Log | Techniques > new agent-architecture chapter (next to backlog core-agent-loop) | Event Driven Agent Loops #30 | [link](2025-11-05-event-driven-agent-loops.md) |
| Ralph Wiggum: The Dumbest Way To Build Software That Actually Works | Techniques > Multi-Agent Orchestration (new "Unattended Loops" chapter) | Ralph Wiggum under the hood: Coding Agent Power Tools #29 | [link](2025-10-29-ralph-wiggum-power-tools.md) |
| Run It In Reverse: Migrate Any Codebase By Generating Specs First | Techniques > Multi-Model & Multi-CLI Workflows (Migrations & Ports) | Ralph Wiggum under the hood: Coding Agent Power Tools #29 | [link](2025-10-29-ralph-wiggum-power-tools.md) |
| Write The Docs First: Turn A Feature Doc Into Your Agent's Spec | Techniques > documentation-as-spec / working-backwards | No vibes allowed (live coding with Claude and Code Layer) #27 | [link](2025-10-16-no-vibes-live-coding-code-layer.md) |
| Just-In-Time Errors: Inject Tool Failures Only When The Model Needs Them | Business / agent-building > dynamic context injection | No vibes allowed (live coding with Claude and Code Layer) #27 | [link](2025-10-16-no-vibes-live-coding-code-layer.md) |
| How to tell if the model actually got dumber (and what to do about it) | Loopy AI > Command and Control (or new Running-AI-in-Production chapter) | Anthropic Post Mortem #26 | [link](2025-10-16-anthropic-post-mortem.md) |
| The Dumping Ground Field: Stop Fighting the Model, Give It Somewhere to Put the Junk | Prompt Engineering > PE Foundations | Dynamic Schemas #25 | [link](2025-10-04-dynamic-schemas.md) |
| Build an AI Pipeline You Can Actually Debug | Context Engineering > Evals and Observability (new chapter) | Evals for large scale classification #24 | [link](2025-10-04-evals-large-scale-classification.md) |
| Your Evals Are Lying to You | Context Engineering > Evals and Observability (new chapter) / Prompt Engineering error analysis | Evals for large scale classification #24 | [link](2025-10-04-evals-large-scale-classification.md) |
| The Only Voice-Agent Eval That Matters: A Green-and-Red Conversation Timeline | Techniques > Multi-Agent Orchestration (or new Evals chapter) | Voice Agents and Supervisor Threading #21 | [link](2025-09-06-voice-agents-supervisor-threading.md) |
| Start Talking Before You Think: The Latency Trick From Voice Agents | Techniques > Multi-Agent Orchestration | Voice Agents and Supervisor Threading #21 | [link](2025-09-06-voice-agents-supervisor-threading.md) |
| Run Your Company on Markdown: Claude Code as Your CRM and Back Office | My Daily Workflows (or Business) > Run Ops on Claude Code | Claude for non-code tasks #20 | [link](2025-08-28-claude-for-non-code-tasks.md) |
| Show Me the Prompt: Proxy Claude Code and Why Your CLAUDE.md Gets Ignored | Context Engineering > Understanding the System | Claude for non-code tasks #20 | [link](2025-08-28-claude-for-non-code-tasks.md) |
| A Second Model That Watches Your Agent and Steers It | Techniques > next to subagent-verification-loops / closing-the-loop | Interruptible agents #19 | [link](2025-08-20-interruptible-agents.md) |
| Mask, Don't Remove: Change an Agent's Tools Without Breaking the Cache | Context Engineering (advanced) / Advanced Techniques > Multi-Agent Orchestration | Context Engineering lessons from Manus #18 | [link](2025-08-16-context-engineering-lessons-manus.md) |
| Vibe Eval: Build a Model Comparison Dashboard in Under an Hour | Techniques > Evals / comparing models (new chapter) | Evals: How to compare models #16 | [link](2025-08-02-evals-how-to-compare-models.md) |
| Push the Model to Its Limit: A Ritual for Every New Release | Techniques > working-with-new-models | Evals: How to compare models #16 | [link](2025-08-02-evals-how-to-compare-models.md) |
| How vision models actually see (it is all tokens, and you should own the pixels) | Techniques > Working with vision and multimodal models (new chapter) | PDFs, Multimodality, Vision Models: Part 1 #15 | [link](2025-07-27-pdfs-multimodality-vision-models.md) |
| Why your agent silently fails: the compounding-accuracy trap | Context Engineering / Techniques > foundational reliability concept | PDFs, Multimodality, Vision Models: Part 1 #15 | [link](2025-07-27-pdfs-multimodality-vision-models.md) |
| Steal the Architecture: Solve New AI Problems With Old Engineering | Techniques > backlog (new technique) | Implementing Decaying-Resolution Memory #14 | [link](2025-07-16-decaying-resolution-memory.md) |
| Decaying Resolution Memory: Teach Your Agent To Forget On Purpose | Context Engineering > Agent Memory (new chapter) | Context Engineering and memory deep dive #13 | [link](2025-07-09-context-memory-deep-dive.md) |
| Stateful Tools Are Your Agent's Memory (And Its Security Boundary) | Context Engineering > tool design (or for-business, building agents) | Context Engineering and memory deep dive #13 | [link](2025-07-09-context-memory-deep-dive.md) |
| Generate the Content, Then Generate the Email: The Two-Pass Prompt | Prompt Engineering > Core Techniques | Getting Tone Just Right with LLMs #12 | [link](2025-07-04-getting-tone-right-with-llms.md) |
| Build the Harness Before You Touch the AI | Advanced Techniques > build-order principle (or Start Here) | n/a | [link](2025-06-27-youtube-to-email-x-posts.md) |
| Build a Self-Updating Entity Database Your AI Pipeline Can Trust | Business > LLM Data Pipelines | Entity extraction from LLMs - extracting, deduping, enriching #10 | [link](2025-06-20-entity-extraction-dedup-enrich.md) |
| Stop Writing One Giant Prompt: Turn Extraction Into Typed Functions | Techniques > LLM App Engineering | Entity extraction from LLMs - extracting, deduping, enriching #10 | [link](2025-06-20-entity-extraction-dedup-enrich.md) |
| Write the Damn While Loop: Why I Do Not Use Agent Frameworks | Techniques > core-agent-loop / agent-harness-concept (backlog) or Context Engineering | Humans as Tools #8 | [link](2025-06-10-humans-as-tools.md) |
| Exit to a Database: How to Survive a Five-Day Human Wait | Techniques or Context Engineering > durable/resumable agents | Humans as Tools #8 | [link](2025-06-10-humans-as-tools.md) |
| 1000 MCP Tools, One Agent: How to Not Blow Up Your Context Window | Claude Code > new MCP / agent-building chapter | Using MCP server with 10000+ tools #7 | [link](2025-05-28-mcp-server-10000-tools.md) |
| Every MCP Server You Install Is Untrusted Code | Claude Code > security | Using MCP server with 10000+ tools #7 | [link](2025-05-28-mcp-server-10000-tools.md) |
| Read the Data First: How to Build an Eval You Can Actually Trust | Prompt Engineering (or new Evals mini-class) > new Evals chapter | LLMs to analyze Enron Emails #6 | [link](2025-05-21-llms-analyze-enron-emails.md) |
| The Cheap Proxy Pass: Profile Your Data Before You Spend a Single Token | Techniques > new chapter on cost-aware LLM pipelines | LLMs to analyze Enron Emails #6 | [link](2025-05-21-llms-analyze-enron-emails.md) |
| Vibe Eval First: How To Go From Zero Evals To Good Evals | Techniques > new Evals chapter | Evals, Evals, Evals #5 | [link](2025-05-13-evals-evals-evals.md) |
| Catch The LLM Lying: Deterministic Runtime Evals | Techniques > Evals chapter | Evals, Evals, Evals #5 | [link](2025-05-13-evals-evals-evals.md) |
| Route Every Step to the Cheapest Model That Works | Techniques > Multi-Model & Multi-CLI Workflows | Building a coding bot #3 | [link](2025-04-16-building-a-coding-bot.md) |
| Why Your Actor Checker Loop Costs 10x Too Much | Techniques > Multi-Agent Orchestration | Reasoning models vs reasoning prompts #2 | [link](2025-04-08-reasoning-models-vs-prompts.md) |
| Route 1000 MCP Tools With One LLM Function | Techniques > large-scale-classification / routing at scale | Large scale classification #1 | [link](2025-04-02-large-scale-classification-ep1.md) |
| The Text You Embed Is Not the Text the LLM Should See | Prompt Engineering > Foundations (few-shot / structured-output neighbor) | Large scale classification #1 | [link](2025-04-02-large-scale-classification-ep1.md) |

## 🔗 Complement video ideas (92)

| Proposed ACS video | Complements | Source episode | Report |
|--------------------|-------------|----------------|--------|
| Make Your Product Debug Itself With an Agent Loop | closing-the-loop | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-06-26-self-healing-agent-loop.md) |
| Stop Guessing Your Skill: Put Every Version in an Arena | simplify-skill | The Self-Healing Agent Loop That Fixes Its Own Language | [link](2026-06-26-self-healing-agent-loop.md) |
| Why Your Agent Writes Bad Code (And the Design Split That Fixes It) | the-shifting-bottleneck | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-06-19-why-ai-agent-writes-bad-code.md) |
| Delete Your CLAUDE.md, Point to Architecture Files Instead | delete-your-readme | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | [link](2026-06-19-why-ai-agent-writes-bad-code.md) |
| Measure Before You Optimize: Build the Agent's Feedback Loop | Closing the Loop | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-06-12-performance-engineering-human-judgment.md) |
| Catch the One Wrong Line: Human Judgment in Unfakeable Work | What Breaks If I Change This? | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | [link](2026-06-12-performance-engineering-human-judgment.md) |
| The First Thing to Do When a New Model Drops | goal-in-strategy-out | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | [link](2026-06-13-testing-claude-fable-5.md) |
| Give Your Agent Back Pressure It Doesn't Have Yet | closing-the-loop | How AI Agents Can Safely Ship Code to Production | [link](2026-06-05-safely-ship-code-to-production.md) |
| Your Output Schema Is Part of the Prompt | planned "structured-output" foundations | How to Build AI Agents That Work in Any Language | [link](2026-06-05-agents-in-any-language.md) |
| Why Your Agent Is Good at Bash and Bad at Sed | gravitational-pull-from-older-models | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | [link](2026-06-01-bash-holding-agents-back.md) |
| Software Is Just Stacking While Loops | test-time-compute | Can You Outsmart the Model Makers? | [link](2026-05-11-outsmart-the-model-makers.md) |
| Rewrite, Do Not Edit: Why Agents Wreck In-Place Doc Edits | Build It Twice | Can an AI Out-Plan a Senior Engineer? | [link](2026-05-04-ai-outplan-senior-engineer.md) |
| Agents, Sub-Agents, Orchestrators: It Is All One While Loop | planned agent-harness-concept + core-agent-loop | Context Engineering vs Harness Engineering vs Software Engineering | [link](2026-04-27-context-vs-harness-vs-software-engineering.md) |
| Unit Test Your UI: The Fastest Feedback Loop for Coding Agents | closing-the-loop | Building a Practical AI Assembly Line | [link](2026-04-20-practical-ai-assembly-line.md) |
| A CLAUDE.md That One-Shots The Hard Thing | skills-as-team-knowledge-base / global-claude-md-personal-profile | Streaming Systems Masterclass | [link](2026-04-13-streaming-systems-masterclass.md) |
| Perfect the Spec, One-Shot the Build | build-it-twice | Build Faster by Coding Slower | [link](2026-04-06-build-faster-by-coding-slower.md) |
| Give the Model Options, Not Orders | Prompt Engineering 01-steering-distributions | Build Faster by Coding Slower | [link](2026-04-06-build-faster-by-coding-slower.md) |
| The Only Time You Should Reach for MCP | clis-vs-mcps | The Right Way to Give Your AI New Abilities | [link](2026-03-30-give-your-ai-new-abilities.md) |
| Structured Output Won't Save You: The Validation That Turns Injections Into Errors | structured-output | Prompt-Hackers are coming for your data | [link](2026-03-23-prompt-hackers-coming-for-data.md) |
| The Checker Catches What the Builder Missed | closing-the-loop | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-03-09-scrub-sensitive-data-before-llm.md) |
| Your Skills Are Bloating Context Just Like MCPs | clis-vs-mcps | Agents, Subagents, Skills and Commands | [link](2026-03-16-agents-subagents-skills-commands.md) |
| Iterate the Doc, Not the Code: The No-Rework Decision Gate | build-it-twice | The No-Rework Workflow for AI Coding Assistants | [link](2026-03-02-no-rework-workflow.md) |
| Vertical Planning: Make Every Phase Testable | build-small-merge-big | The No-Rework Workflow for AI Coding Assistants | [link](2026-03-02-no-rework-workflow.md) |
| Let the Agent Learn the Clicks, Then Bake Them | Claude CoWork 07 Browser Automation | How to Automate Complex Workflows with Claude | [link](2026-02-23-automate-complex-workflows-claude.md) |
| Claude Code as the Front End for Your CLIs | high-level-strategy-low-level-details | How to Automate Complex Workflows with Claude | [link](2026-02-23-automate-complex-workflows-claude.md) |
| Design the Back Pressure First | Closing the Loop | Agentic Backpressure Deep Dive | [link](2026-02-16-agentic-backpressure-deep-dive.md) |
| Let Your Users Design the Schema | Prompt Engineering Foundations 'structured-output | Prompting Is Becoming a Product Surface | [link](2026-02-09-prompting-is-a-product-surface.md) |
| Turn Your Inbox Into an Agent You Delegate To | Airtable Memory for Cloud Scheduled Tasks | Email is All You Need | [link](2026-01-26-email-is-all-you-need.md) |
| Order Your Prompt for the Cache, Not for Humans | the shipped Context Engineering class | Understanding Latency | [link](2026-01-12-understanding-latency.md) |
| Only Run the Tests Your Change Can Break | closing-the-loop | Founding Boundary | [link](2026-01-05-founding-boundary.md) |
| Delete Your Docs, Rebuild Context: The RPI Loop | Delete Your README | Founding HumanLayer | [link](2025-12-29-founding-humanlayer.md) |
| Control Flow Belongs in Code, Not Your Prompt | Boxing the Model In | Founding HumanLayer | [link](2025-12-29-founding-humanlayer.md) |
| Feed the Loop Better: Give Your Fixing Agent the Whole Test | closing-the-loop | Building a Prompt Optimizer | [link](2025-12-22-building-a-prompt-optimizer.md) |
| The Manager Agent That Merges Your Parallel Worktrees For You | the in-progress "worktrees" video | Git Worktrees + Agents | [link](2025-12-15-git-worktrees-plus-agents.md) |
| Fan Out Five Agents, Then Cherry-Pick The Best Answer | the planned stochastic-consensus-and-fan-out-fan-in / test-time-comput | Git Worktrees + Agents | [link](2025-12-15-git-worktrees-plus-agents.md) |
| Hide the Goal: How to Get Honest Research From an Agent | What breaks if I change this? | Claude Code Maxing - live coding | [link](2026-02-02-claude-code-maxing-live-coding.md) |
| Stop Writing Horizontal Plans | Build Small, Merge Big | Claude Code Maxing - live coding | [link](2026-02-02-claude-code-maxing-live-coding.md) |
| The Background Agent That Checks Your Work | subagent-verification-loops | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-01-19-12-factor-coding-agent-sdks.md) |
| The Diffable Architecture Map That Stops Vibe Rot | What Breaks If I Change This? | Applying 12-Factor Principles to Coding Agent SDKs | [link](2026-01-19-12-factor-coding-agent-sdks.md) |
| Ship at 97%: Turning Eval Checks Into a Self-Correcting Product | building-inner-and-outer-feedback-loops | Multimodal Evals | [link](2025-12-08-multimodal-evals.md) |
| Order Your Plan by What You Can Prove, Not by Layer | Ultra Plan | No Vibes Allowed #33 | [link](2025-12-02-no-vibes-allowed-33.md) |
| Your Best Spec Is Last Week's Diff | Build It Twice | No Vibes Allowed #33 | [link](2025-12-02-no-vibes-allowed-33.md) |
| Keep Research Objective: Never Let It Plan While It Reads | What Breaks If I Change This | No Vibes Allowed #33 | [link](2025-12-02-no-vibes-allowed-33.md) |
| Build the Tool You Never Have to Think About Again | task-shaped-wrappers | Building Animation Pipelines | [link](2025-11-25-building-animation-pipelines.md) |
| How Wrong Is It? The Recovery Ladder for Agent Output | build-it-twice | Building Animation Pipelines | [link](2025-11-25-building-animation-pipelines.md) |
| Stop Asking the Model to Compute. Ask It for a Blueprint. | structured-output | Dates, Times, and LLMs #31 | [link](2025-11-12-dates-times-and-llms.md) |
| Your Context Window Is a Projection, Not a Message List | Context Engineering class | Event Driven Agent Loops #30 | [link](2025-11-05-event-driven-agent-loops.md) |
| Back Pressure: Design The Harness Before You Let The Agent Cook | Closing The Loop | Ralph Wiggum under the hood: Coding Agent Power Tools #29 | [link](2025-10-29-ralph-wiggum-power-tools.md) |
| Your Agent's IQ Is In Its Tool Outputs, Not Its Prompts | the shipped Context Engineering class | Agentic RAG: Building a coding agent (no frameworks) #28 | [link](2025-10-22-agentic-rag-coding-agent.md) |
| Stop Truncating: Write Tool Output To A File And Hand Back The Path | refactoring-to-save-on-context | Agentic RAG: Building a coding agent (no frameworks) #28 | [link](2025-10-22-agentic-rag-coding-agent.md) |
| When NOT To Build An Agent: Deterministic First, Then A/B | the-ambiguity-line | Agentic RAG: Building a coding agent (no frameworks) #28 | [link](2025-10-22-agentic-rag-coding-agent.md) |
| Research, Plan, Implement: The Three-Window Workflow For Hard Features | Context Engineering class + auto-compact-and-handoff | No vibes allowed (live coding with Claude and Code Layer) #27 | [link](2025-10-16-no-vibes-live-coding-code-layer.md) |
| Stop maxing out your context window | 1M Context Window | Anthropic Post Mortem #26 | [link](2025-10-16-anthropic-post-mortem.md) |
| Your evals are useless if they don't span the distribution | Building Inner and Outer Feedback Loops | Anthropic Post Mortem #26 | [link](2025-10-16-anthropic-post-mortem.md) |
| The wall every no-code agent builder hits (also film-able, not deep-dived) | structured-output foundation | Anthropic Post Mortem #26 | [link](2025-10-16-anthropic-post-mortem.md) |
| Let the Model Write the Schema: Dynamic Extraction for Data You Have Never Seen | Structured Output | Dynamic Schemas #25 | [link](2025-10-04-dynamic-schemas.md) |
| Two Tiers of Code: Production Core, Throwaway Everything Else | build-it-twice | Evals for large scale classification #24 | [link](2025-10-04-evals-large-scale-classification.md) |
| Why I Deleted My MCPs and Wrote Bash Instead | mcps-connectors-that-i-use | Bash vs MCP for Coding Agents #23 | [link](2025-10-04-bash-vs-mcp-coding-agents.md) |
| Why Claude Ignores Your CLAUDE.md, and What To Do Instead | dynamic-context-injection-for-skills | Bash vs MCP for Coding Agents #23 | [link](2025-10-04-bash-vs-mcp-coding-agents.md) |
| Type-Safe Streaming: Stop Writing Render Guards in Your AI App | Prompt Engineering "structured-output" foundations brief | Generative UIs and Structured Streaming #22 | [link](2025-09-10-generative-uis-structured-streaming.md) |
| Pipeline Your LLM Stream: Start Work Before Generation Finishes | test-time-compute / stochastic-consensus-and-fan-out-fan-in | Generative UIs and Structured Streaming #22 | [link](2025-09-10-generative-uis-structured-streaming.md) |
| The Supervisor Thread: How to Re-Steer an Agent That Went Off the Rails | closing-the-loop | Voice Agents and Supervisor Threading #21 | [link](2025-09-06-voice-agents-supervisor-threading.md) |
| Deterministic Context Packing: A make print-context Command Beats Agentic Search | the shipped Context Engineering class | Claude for non-code tasks #20 | [link](2025-08-28-claude-for-non-code-tasks.md) |
| Build an Agent You Can Interrupt Mid-Run | core-agent-loop | Interruptible agents #19 | [link](2025-08-20-interruptible-agents.md) |
| Design Your Prompt Around the Cache | Forked Subagents | Context Engineering lessons from Manus #18 | [link](2025-08-16-context-engineering-lessons-manus.md) |
| Give Your Agent a Restore Button: Compaction Without Losing Anything | Progressive Disclosure | Context Engineering lessons from Manus #18 | [link](2025-08-16-context-engineering-lessons-manus.md) |
| Why I Never Let Claude Code Pass 50% Context | 12-1m-context-window | Advanced context engineering for coding agents #17 | [link](2025-08-06-advanced-context-engineering-coding-agents.md) |
| Review the Research, Not the Code | blast-radius-proportional-verification | Advanced context engineering for coding agents #17 | [link](2025-08-06-advanced-context-engineering-coding-agents.md) |
| Don't Swap the Model: Define Accuracy Before You Evaluate | scaling-taste | Evals: How to compare models #16 | [link](2025-08-02-evals-how-to-compare-models.md) |
| The 110% guarantee: deterministic runtime evals that self-heal your pipeline | closing-the-loop | PDFs, Multimodality, Vision Models: Part 1 #15 | [link](2025-07-27-pdfs-multimodality-vision-models.md) |
| Give Your Agent a Memory That Never Forgets (But Stays Small) | The Context Layer | Implementing Decaying-Resolution Memory #14 | [link](2025-07-16-decaying-resolution-memory.md) |
| Break the Chat Format to Stop Prompt Injection | Loopy AI Goal Mode's untrusted-objective tag | Implementing Decaying-Resolution Memory #14 | [link](2025-07-16-decaying-resolution-memory.md) |
| The Flexibility Dial: When to Hardcode Instead of Handing It to the Agent | Boxing the Model In | Getting Tone Just Right with LLMs #12 | [link](2025-07-04-getting-tone-right-with-llms.md) |
| Change the Schema, Not the Prompt | Structured Output | Getting Tone Just Right with LLMs #12 | [link](2025-07-04-getting-tone-right-with-llms.md) |
| Turn Real Runs Into Golden Test Cases | Building Inner and Outer Feedback Loops | n/a | [link](2025-06-27-youtube-to-email-x-posts.md) |
| Dynamic Few-Shot: Make the Model Know It's Just an Example | Few-Shot Prompting | n/a | [link](2025-06-27-youtube-to-email-x-posts.md) |
| Your Schema Is a Prompt: Make the Model Reason Through Its Output Type | structured-output | Entity extraction from LLMs - extracting, deduping, enriching #10 | [link](2025-06-20-entity-extraction-dedup-enrich.md) |
| Stop Making the Model Type: Emit an Index, Rebuild in Code | 07 Structured Output | Cracking the prompting interview #9 | [link](2025-06-13-cracking-prompting-interview.md) |
| Why Strict JSON Makes Your Code Worse (and What to Do Instead) | 07 Structured Output | Cracking the prompting interview #9 | [link](2025-06-13-cracking-prompting-interview.md) |
| RTFP: Read the Prompt Your Framework Actually Sends | 10 Iterative Refinement | Cracking the prompting interview #9 | [link](2025-06-13-cracking-prompting-interview.md) |
| Make Your Agent Ask Permission (And Make It Impossible to Skip) | blocking-risky-commands-with-hooks | Humans as Tools #8 | [link](2025-06-10-humans-as-tools.md) |
| MCP Is Just Two API Calls: Own Your Agent Loop | core-agent-loop | Using MCP server with 10000+ tools #7 | [link](2025-05-28-mcp-server-10000-tools.md) |
| Your Schema Is the Prompt: Structured Output as a Reasoning Scaffold | boxing-the-model-in | LLMs to analyze Enron Emails #6 | [link](2025-05-21-llms-analyze-enron-emails.md) |
| Stop Scoring 1 to 10: Categorical Evals And LLM As Judge | Prompt Engineering structured-output | Evals, Evals, Evals #5 | [link](2025-05-13-evals-evals-evals.md) |
| Own the Loop: Build an Agent Without a Framework | The Core Agent Loop | Building a 12 Factor Agent #4 | [link](2025-04-23-building-a-12-factor-agent.md) |
| Stop Calling Tools: Treat the LLM as a Stateless Function | Structured Output | Building a 12 Factor Agent #4 | [link](2025-04-23-building-a-12-factor-agent.md) |
| Unit-Test Your Agent: Evals Without an LLM Judge | 5.1 Evaluating Your Skills" and loopy-ai "Generator Evaluator | Building a 12 Factor Agent #4 | [link](2025-04-23-building-a-12-factor-agent.md) |
| Stop Looping the LLM on Errors: Build a Coding Agent as Deterministic Glue | closing-the-loop | Building a coding bot #3 | [link](2025-04-16-building-a-coding-bot.md) |
| Lie to Your Agent: Rewrite Its History So Every Failure Disappears | the Context Engineering class | Building a coding bot #3 | [link](2025-04-16-building-a-coding-bot.md) |
| You Do Not Need a Reasoning Model | 06-chain-of-thought.md | Reasoning models vs reasoning prompts #2 | [link](2025-04-08-reasoning-models-vs-prompts.md) |
| Route to a Specialist, Not a Genius | 01-steering-distributions.md | Reasoning models vs reasoning prompts #2 | [link](2025-04-08-reasoning-models-vs-prompts.md) |
| Build Probe Points Into Your LLM Pipeline | closing-the-loop | Large scale classification #1 | [link](2025-04-02-large-scale-classification-ep1.md) |

## 🟡 Partial (4)

| Proposed ACS video | Note | Source episode | Report |
|--------------------|------|----------------|--------|
| Your Prompt Has an Instruction Budget, Not Just an Information Budget | 🟡 fills gap in Context Engineering class | How to Scrub Sensitive Data Before it Reaches Your LLM | [link](2026-03-09-scrub-sensitive-data-before-llm.md) |
| Treat the Model Like the Plus Operator | 🟡 fills gap in "structured-output" (Prompt Engineering foundations): adds resilient parsing of malformed/recursive output and the streaming dual-type problem | Founding Boundary | [link](2026-01-05-founding-boundary.md) |
| JSON Schema Is Costing You Accuracy: Why Concise Code Beats It 4 to 1 | 🟡 fills gap in Structured Output | Dynamic Schemas #25 | [link](2025-10-04-dynamic-schemas.md) |
| Review the Diagram, Not the 300 Lines of Markdown | 🟡 fills gap in high-level-strategy-low-level-details / goal-in-strategy-out / Ultra Plan (V20): they teach reviewing the plan, not using a diagram as the review medium for AI-generated architecture | Interruptible agents #19 | [link](2025-08-20-interruptible-agents.md) |

---

## Per-episode index

| # | Episode | Spine (one line) | Verdict | Report |
|---|---------|------------------|---------|--------|
| B1 | The Self-Healing Agent Loop That Fixes Its Own Language | The self-healing product loop: point agents at your own product to manufacture the bug signal, then feed it back as issu... | 🔴1 🔗2 | [link](2026-06-26-self-healing-agent-loop.md) |
| B1 | Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt) | Split the design phase into product, technical, and program design so architectural decisions land upstream where you ha... | 🔴1 🔗2 | [link](2026-06-19-why-ai-agent-writes-bad-code.md) |
| B1 | Why Performance Engineering Still Requires Human Judgment \| No Vibes Allowed | Performance engineering is really a data-driven feedback loop, and the same loop (workloads, standard deviations, JSON-s... | 🔴1 🔗2 | [link](2026-06-12-performance-engineering-human-judgment.md) |
| B1 | Testing Claude Fable 5: Why New AI Models Rarely Change Everything | When a new model ships, test comprehension before completion: ask it to restate your architecture on your hardest LIVE p... | 🔴2 🔗1 | [link](2026-06-13-testing-claude-fable-5.md) |
| B1 | How AI Agents Can Safely Ship Code to Production | Feature flags manufacture back pressure where agents have none, turning unmeasurable UI/taste work into production metri... | 🔴1 🔗1 | [link](2026-06-05-safely-ship-code-to-production.md) |
| B1 | How to Build AI Agents That Work in Any Language | Normalize every language to one evaluable English pipeline wrapped with translation-in and translation-out units, instea... | 🔴1 🔗1 | [link](2026-06-05-agents-in-any-language.md) |
| B1 | Why Bash Might Be Holding AI Agents Back \| Rhys Sullivan | Inline tools, MCPs, bash, and code mode are all just implementations of one primitive, the tool call, so stop arguing ab... | 🔴2 🔗1 | [link](2026-06-01-bash-holding-agents-back.md) |
| B1 | Can You Outsmart the Model Makers? | The harness has no moat: because the agent runs on your machine over an observable API, you can always reverse-engineer ... | 🔴2 🔗1 | [link](2026-05-11-outsmart-the-model-makers.md) |
| B1 | Can an AI Out-Plan a Senior Engineer? | Fight AI slop with slop: build throwaway, AI-generated internal tooling you never read as scaffolding that makes your re... | 🔴2 🔗1 | [link](2026-05-04-ai-outplan-senior-engineer.md) |
| B1 | Context Engineering vs Harness Engineering vs Software Engineering | Models are RL'd onto one specific tool schema (Claude Code learned old-string/new-string, Codex learned apply-patch), so... | 🔴2 🔗1 | [link](2026-04-27-context-vs-harness-vs-software-engineering.md) |
| B2 | Building a Practical AI Assembly Line | Give the coding agent an isolated render harness (Storybook) so it iterates on a single component's props instead of boo... | 🔴1 🔗1 | [link](2026-04-20-practical-ai-assembly-line.md) |
| B2 | Streaming Systems Masterclass | Streaming is a ground-up architectural decision, not a feature you bolt on later: model everything as yield and pass que... | 🔴2 🔗1 | [link](2026-04-13-streaming-systems-masterclass.md) |
| B2 | Build Faster by Coding Slower | Pour hours into the spec so the agent one-shots the entire build, because a 200-line spec becomes thousands of lines and... | 🔴1 🔗2 | [link](2026-04-06-build-faster-by-coding-slower.md) |
| B2 | The Right Way to Give Your AI New Abilities | MCP's only justifiable use is letting your product's users bring their own long-tail tools; everything you control shoul... | 🔴1 🔗1 | [link](2026-03-30-give-your-ai-new-abilities.md) |
| B2 | Prompt-Hackers are coming for your data | Prompt injection is an architecture problem, not a wording problem: an agent is exploitable only when untrusted input, p... | 🔴2 🔗1 | [link](2026-03-23-prompt-hackers-coming-for-data.md) |
| B2 | How to Scrub Sensitive Data Before it Reaches Your LLM | Stop sensitive data at a redaction proxy that intercepts the outbound request and runs a local detect-redact-restore pip... | 🔴1 🔗1 🟡1 | [link](2026-03-09-scrub-sensitive-data-before-llm.md) |
| B2 | Agents, Subagents, Skills and Commands | Context isolation and instruction modules are two orthogonal jobs; subagents were overloaded to do both, and skills fina... | 🔴2 🔗1 | [link](2026-03-16-agents-subagents-skills-commands.md) |
| B2 | The No-Rework Workflow for AI Coding Assistants | Write throwaway learning tests that actually run an opaque dependency and assert on its real output, so design is ground... | 🔴1 🔗2 | [link](2026-03-02-no-rework-workflow.md) |
| B2 | How to Automate Complex Workflows with Claude | Automate incrementally with STOP-for-human markers and permanently gate only the irreversible one-way doors (mass email,... | 🔴1 🔗2 | [link](2026-02-23-automate-complex-workflows-claude.md) |
| B2 | Agentic Backpressure Deep Dive | Learning tests: have the agent write a throwaway probe that proves how a black-box system (closed API, CLI, LLM) actuall... | 🔴2 🔗1 | [link](2026-02-16-agentic-backpressure-deep-dive.md) |
| B3 | Prompting Is Becoming a Product Surface | Expose the schema, not the prompt string, as the thing users configure, using a dynamic type system that escalates from ... | 🔴1 🔗1 | [link](2026-02-09-prompting-is-a-product-surface.md) |
| B3 | Email is All You Need | Design agents for async, interrupting inputs from day one: because you never own the UI, serialize each thread, defer ir... | 🔴2 🔗1 | [link](2026-01-26-email-is-all-you-need.md) |
| B3 | Understanding Latency | Latency is a perception problem, not a speed problem: you cannot beat competitors on raw model speed, so you win by maki... | 🔴2 🔗1 | [link](2026-01-12-understanding-latency.md) |
| B3 | Founding Boundary | When the test suite is too big to run per change, predict from the git diff which tests the change can affect and run on... | 🔴0 🔗1 🟡1 | [link](2026-01-05-founding-boundary.md) |
| B3 | Founding HumanLayer | Skills over MCP: use the file system plus bash plus a markdown skill as the substrate for connecting an agent to service... | 🔴1 🔗2 | [link](2025-12-29-founding-humanlayer.md) |
| B3 | Building a Prompt Optimizer | Prompt optimization is now a build-it-yourself commodity: point an automated GEPA-style optimizer at the prompts you wil... | 🔴1 🔗1 | [link](2025-12-22-building-a-prompt-optimizer.md) |
| B3 | Git Worktrees + Agents | Because worktrees share one git object database, a manager agent on main can continuously merge sibling worktree branche... | 🔴0 🔗2 | [link](2025-12-15-git-worktrees-plus-agents.md) |
| B3 | Claude Code Maxing - live coding | Ship AI code without code reviews by replacing per-line review with automated architecture guardrails (auto-generated de... | 🔴1 🔗2 | [link](2026-02-02-claude-code-maxing-live-coding.md) |
| B3 | Applying 12-Factor Principles to Coding Agent SDKs | If you know the workflow order, encode it as deterministic control flow, not a prompt, using typed structured outputs as... | 🔴1 🔗2 | [link](2026-01-19-12-factor-coding-agent-sdks.md) |
| B3 | Multimodal Evals | Evaluate a multimodal extraction pipeline with zero labeled data by encoding structural invariants you already know must... | 🔴2 🔗1 | [link](2025-12-08-multimodal-evals.md) |
| B4 | No Vibes Allowed #33 | Order your implementation plan's phases by what you can independently verify, biggest unknown first, not by architecture... | 🔴0 🔗3 | [link](2025-12-02-no-vibes-allowed-33.md) |
| B4 | Building Animation Pipelines | Wrap a linear workflow in a Claude slash command the model builds and owns for itself, buying you out of ever thinking a... | 🔴1 🔗2 | [link](2025-11-25-building-animation-pipelines.md) |
| B4 | Dates, Times, and LLMs #31 | Put a deterministic intermediate representation between the LLM and the answer: the model classifies fuzzy intent into a... | 🔴1 🔗1 | [link](2025-11-12-dates-times-and-llms.md) |
| B4 | Event Driven Agent Loops #30 | Model a complex agent as an append-only event log and derive every view (UI, LLM context, control state) as a pure proje... | 🔴1 🔗1 | [link](2025-11-05-event-driven-agent-loops.md) |
| B4 | Ralph Wiggum under the hood: Coding Agent Power Tools #29 | Run a coding agent in a bash while-loop forever, feeding one tiny prompt that does a single bounded task then exits, so ... | 🔴2 🔗1 | [link](2025-10-29-ralph-wiggum-power-tools.md) |
| B4 | Agentic RAG: Building a coding agent (no frameworks) #28 | Agent quality lives in how you implement tool OUTPUTS, not in tool prompts or definitions; Vaibhav never touched a tool ... | 🔴0 🔗3 | [link](2025-10-22-agentic-rag-coding-agent.md) |
| B4 | No vibes allowed (live coding with Claude and Code Layer) #27 | Ship hard features by splitting work into three passes, research then plan then implement, each in a fresh context windo... | 🔴2 🔗1 | [link](2025-10-16-no-vibes-live-coding-code-layer.md) |
| B4 | Anthropic Post Mortem #26 | Use the least context that fully represents your problem, because a bigger context window trades accuracy for capacity a... | 🔴1 🔗2 | [link](2025-10-16-anthropic-post-mortem.md) |
| B4 | Dynamic Schemas #25 | Meta-programming with LLMs: have the model author the schema first, then run that schema to extract the data for inputs ... | 🔴1 🔗1 🟡1 | [link](2025-10-04-dynamic-schemas.md) |
| B4 | Evals for large scale classification #24 | Stage your AI task into narrowing filters with a probe at each boundary, then build a dense visual eval harness that sho... | 🔴2 🔗1 | [link](2025-10-04-evals-large-scale-classification.md) |
| B5 | Bash vs MCP for Coding Agents #23 | For any tool you touch daily, bash and a custom CLI you own beat MCP, because every word of an MCP schema is tokens the ... | 🔴0 🔗2 | [link](2025-10-04-bash-vs-mcp-coding-agents.md) |
| B5 | Generative UIs and Structured Streaming #22 | Reflect your UX in the type system: declarative per-field streaming annotations make partial LLM output type-safe, repla... | 🔴0 🔗2 | [link](2025-09-10-generative-uis-structured-streaming.md) |
| B5 | Voice Agents and Supervisor Threading #21 | Supervisor threading: a background agent snapshots the frozen conversation, classifies its state, and re-steers the live... | 🔴2 🔗1 | [link](2025-09-06-voice-agents-supervisor-threading.md) |
| B5 | Claude for non-code tasks #20 | Claude Code is a general-purpose agent: run your whole back office (CRM, release notes, standups) on interlinked markdow... | 🔴2 🔗1 | [link](2025-08-28-claude-for-non-code-tasks.md) |
| B5 | Interruptible agents #19 | Make an agent's workflow cleanly cancellable and resumable at any point, keeping work already done, via an in-progress f... | 🔴1 🔗1 🟡1 | [link](2025-08-20-interruptible-agents.md) |
| B5 | Context Engineering lessons from Manus #18 | Design around the KV cache: because caching is purely prefix-continuous, pin the system prompt and push every dynamic va... | 🔴1 🔗2 | [link](2025-08-16-context-engineering-lessons-manus.md) |
| B5 | Advanced context engineering for coding agents #17 | Intentional compaction: manage the context window as a budget by hand-writing progress to a markdown file (file:line poi... | 🔴0 🔗2 🟡1 | [link](2025-08-06-advanced-context-engineering-coding-agents.md) |
| B5 | Evals: How to compare models #16 | The eval IS a vibe-coded, throwaway, domain-specific dashboard that renders model outputs side by side, not an automated... | 🔴2 🔗1 | [link](2025-08-02-evals-how-to-compare-models.md) |
| B5 | PDFs, Multimodality, Vision Models: Part 1 #15 | Multimodality never changes the architecture, it is still just tokens, so an image is a grid of tokens whose resolution,... | 🔴2 🔗1 | [link](2025-07-27-pdfs-multimodality-vision-models.md) |
| B5 | Implementing Decaying-Resolution Memory #14 | Before building a novel AI system, find the known engineering primitive it maps to and copy that architecture (caches, m... | 🔴1 🔗2 | [link](2025-07-16-decaying-resolution-memory.md) |
| B6 | Context Engineering and memory deep dive #13 | Decaying Resolution Memory: never make an agent remember everything; make it remember what matters by summarizing at fal... | 🔴2 🔗0 🟡1 | [link](2025-07-09-context-memory-deep-dive.md) |
| B6 | Getting Tone Just Right with LLMs #12 | Getting tone right is a data-assembly problem, not a prompting problem: get the factual data (links, titles, dates, summ... | 🔴1 🔗2 ✅1 | [link](2025-07-04-getting-tone-right-with-llms.md) |
| B6 | n/a | Build the whole product harness (glue code, real-time DB, UI, typed contracts, job system) first, then bolt on and itera... | 🔴1 🔗2 | [link](2025-06-27-youtube-to-email-x-posts.md) |
| B6 | Entity extraction from LLMs - extracting, deduping, enriching #10 | Entity resolution is not one model call: decompose it into extract, resolve, and enrich, each a swappable type signature... | 🔴2 🔗1 | [link](2025-06-20-entity-extraction-dedup-enrich.md) |
| B6 | Cracking the prompting interview #9 | Never make the model generate long, meaningless token sequences; emit the shortest semantically meaningful pointer (inde... | 🔴0 🔗3 | [link](2025-06-13-cracking-prompting-interview.md) |
| B6 | Humans as Tools #8 | Enforce human approval for dangerous tools inside your own loop's switch statement, not in the prompt, so no injection c... | 🔴2 🔗1 | [link](2025-06-10-humans-as-tools.md) |
| B6 | Using MCP server with 10000+ tools #7 | When a tool catalog outgrows the context window, put a narrow_tools(query, tools) function between the tools and the mod... | 🔴2 🔗1 | [link](2025-05-28-mcp-server-10000-tools.md) |
| B6 | LLMs to analyze Enron Emails #6 | A trustworthy eval starts by reading one real row by hand, then freezing that exact case into a deterministic golden tes... | 🔴2 🔗1 | [link](2025-05-21-llms-analyze-enron-emails.md) |
| B6 | Evals, Evals, Evals #5 | Evals are a journey you bootstrap from production data, not a golden dataset you build up front. | 🔴2 🔗1 | [link](2025-05-13-evals-evals-evals.md) |
| B6 | Building a 12 Factor Agent #4 | An agent is just four pieces of ordinary code you write and own (a prompt, a switch statement, a context-string builder,... | 🔴0 🔗3 | [link](2025-04-23-building-a-12-factor-agent.md) |
| B7 | Building a coding bot #3 | Build the coding agent as small deterministic glue between focused prompts, giving each stage a hard guarantee and offlo... | 🔴1 🔗2 | [link](2025-04-16-building-a-coding-bot.md) |
| B7 | Reasoning models vs reasoning prompts #2 | Reasoning is a behavior you architect into any model (prompt it to note what is hard first), not a model tier you buy; b... | 🔴1 🔗2 | [link](2025-04-08-reasoning-models-vs-prompts.md) |
| B7 | Large scale classification #1 | A black-box LLM gives you one lever (the prompt) that worsens as the system grows; decompose it into independently tunab... | 🔴2 🔗1 | [link](2025-04-02-large-scale-classification-ep1.md) |
