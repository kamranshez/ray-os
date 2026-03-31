---
tags: [agentic-coding-school, planning, coverage-gaps]
date: 2026-03-31
---

## Coverage Gaps: Topics from Video Transcripts Not Yet in Agentic Coding School

These topics were extracted from 5 video transcripts (Advanced Claude Code, AI Agents, Agentic Workflows for Business, Claude Code for Beginners, AI Agents extended) and confirmed as NOT covered by searching the Agentic Coding School MCP. Each entry includes what the topic is, why it matters, how the competitor teaches it, and a suggested class placement.

---

### 1. Auto Research (Karpathy Loop)

**What it is:** A framework for progressive autonomous improvement based on Andrej Karpathy's open-source auto-research repo. The agent runs in a loop: hypothesize a change → execute the change → assess with a metric → keep or discard → repeat. Over hundreds of iterations, a system improves dramatically without human intervention.

**Why it matters:** This is the bridge between "agentic engineering" (human directs agent) and "independent research" (agent runs autonomously). Toby Lutke (Shopify CEO) used this to get 53% faster parse+render on Shopify Liquid. Applicable to website speed, cold email copy, ad creative, conversion rates, prompt optimization — anything with a measurable metric.

**How the competitor teaches it:** Full walkthrough of cloning Karpathy's repo, setting up a Lighthouse score optimization loop on a website, building a live dashboard to watch experiments, then generalizing the 3 requirements (metric + change method + assessment). Runs the loop live and shows incremental improvement over time.

**Key concepts to cover:**
- The 3 requirements: metric to optimize, change method, assessment
- program.md (what the agent can modify) and train.py (the thing being optimized)
- Setting up auto research on a real website (Lighthouse page speed)
- Building a dashboard to monitor experiments
- Business applications beyond speed (cold email, conversion rate, ad creative)
- The Shopify/Lutke case study
- How to scope what the agent can and cannot change

**Suggested class:** Techniques (Advanced Techniques) or a new standalone video in Workflows

---

### 2. Stochastic Multi-Agent Consensus

**What it is:** Spawning N agents (typically 5-10) with slight prompt framing variations to independently analyze the same problem, then aggregating results by statistical consensus (mode/frequency). Exploits the fact that LLMs are stochastic — same prompt gives slightly different answers each time — to traverse a much larger solution space.

**Why it matters:** Instead of getting 3 ideas from one run, you get all possible ideas across the entire distribution. Consensus items (suggested by 8/10 agents) are high-confidence. Outliers (suggested by 1/10) are either brilliant or hallucinated — but you find ideas you'd never get from a single run.

**How the competitor teaches it:** Creates a skill called "stochastic-multi-agent-consensus" that spawns 10 agents with different analytical framings (conservative, adventurous, first-principles, contrarian, etc.). Demos it on a real business problem (TikTok growth). Shows the consensus report with consensus items, divergent items, and outliers.

**Key concepts to cover:**
- Why stochasticity is a feature not a bug (same prompt → different answers)
- The search space visualization (pie chart of all possible answers)
- Slight framing variations per agent (conservative, edge-case finder, user advocate)
- Statistical aggregation: mode (frequency), outliers, consensus vs divergence
- Parallelization benefit (10 agents in parallel = same wall-clock time as 1)
- Practical demo on a business/strategy decision
- When to use this vs just asking once

**Suggested class:** Techniques (Advanced Techniques) or Skills class

---

### 3. Agent Debate / Chat Rooms (Model Chat)

**What it is:** Spawning multiple agents with assigned personas (systems thinker, pragmatist, contrarian, edge-case finder, user advocate) who share a conversation file (chat.json) and debate back and forth in round-robin turns. Unlike consensus (independent parallel), debate agents see and respond to each other's arguments, producing more nuanced and spiky conclusions.

**Why it matters:** Debate produces higher quality results than independent consensus because agents challenge each other's assumptions. They carve out the "nooks and crannies" of an idea. Similar to generative adversarial networks (GANs) in machine learning — the adversarial tension produces better outputs.

**How the competitor teaches it:** Builds a skill called "model-chat" that spawns 5 Claude instances in a shared room. Demos on the same TikTok growth problem. Shows the actual conversation transcript where agents disagree. Highlights insights that ONLY emerged through debate (not from consensus).

**Key concepts to cover:**
- Difference from stochastic consensus (debate = sequential + interactive, consensus = parallel + independent)
- Persona assignment and why personality variation matters
- The shared chat.json file as communication medium
- Round-robin turns with parallel execution within rounds
- How to read and use the synthesis report
- When debate beats consensus (nuanced strategy vs broad ideation)

**Suggested class:** Techniques (Advanced Techniques) or Skills class

---

### 4. Multi-Agent Chrome (Parallel Browser Automation)

**What it is:** Spawning multiple Claude Code agents, each with their own Chrome DevTools MCP instance, to perform the same browser action across many targets simultaneously. Example: 10 agents each filling out contact forms on different websites at the same time.

**Why it matters:** Single-agent browser automation takes 2-3 minutes per target. With 10 parallel agents, you do 10 targets in the same time. At 50 agents, you can process 1000 targets in 40 minutes. This is the pattern for automated outreach, lead scraping on JS-heavy sites, form submissions, and data collection at scale.

**How the competitor teaches it:** Builds a skill called "multi-agent-chrome" that orchestrates parallel Chrome instances. Each agent has its own MCP server, its own CLAUDE.md, and communicates via a centralized chat file. The orchestrator checks the chat every 30 seconds. Demos it on apartment hunting (Craigslist, Kijiji, PadMapper simultaneously).

**Key concepts to cover:**
- Why single-agent browser automation is slow
- The architecture: orchestrator + N Chrome agents + centralized chat
- Each agent gets its own Chrome DevTools MCP instance
- Prompt contracts before launching (define constraints, targets, format)
- Real demo: lead outreach via contact forms OR rental searching
- Anti-detection considerations (fingerprinting, rate limiting)
- When to use this vs HTTP requests vs computer use

**Suggested class:** Claude Code (Skills or Advanced) or Business class

---

### 5. Self-Modifying CLAUDE.md / System Prompt

**What it is:** A meta-instruction in your CLAUDE.md (or Gemini.md / agents.md) that tells the agent: "When the user corrects you or you make a mistake, immediately append a new numbered rule to the learned rules section at the bottom of this file." Over sessions, the rule set grows and error rate drops toward zero.

**Why it matters:** This is the highest-ROI single pattern for beginners. Instead of the user having to remember their preferences and re-state them every session, the agent accumulates a living document of rules. First session: many errors. Fifth session: near-zero errors. Works across all platforms (Claude, Gemini, Codex).

**How the competitor teaches it:** Shows the gemini.md pattern with YAML-like rule format (category: never/always do X because Y). Demos building a website, getting corrected on dark mode, then watching the rule auto-append. Next session, dark mode is never used again. Shows the error rate declining over sessions.

**Key concepts to cover:**
- The meta-prompt that enables auto-rule-writing
- Rule format: numbered, category, imperative instruction, because clause
- When to add rules (user corrects, user rejects approach, bug from wrong assumption, user states preference)
- The declining error rate over sessions (graph)
- Platform-agnostic (works in Claude.md, gemini.md, agents.md)
- Pruning: when the rule list gets too long

**Suggested class:** Claude Code (CLAUDE.md chapter) or Techniques (Fundamental)

---


---

### 7. Video-to-Action Pipeline

**What it is:** Teaching agents to learn from YouTube videos instead of text alone. Feed a YouTube URL → Claude sends it to Gemini API → Gemini extracts step-by-step instructions at 1fps → structured steps return to Claude → Claude executes each step using browser/MCP tools. The agent replicates what the video teaches.

**Why it matters:** Most human learning is through video, but agents historically could only learn from text. This bridges the gap. You can point an agent at any YouTube tutorial and have it replicate the workflow — building N8N flows, Blender models, Figma designs, etc.

**How the competitor teaches it:** Creates a skill called "video-to-action" that downloads the video, sends to Gemini, extracts hyperdetailed steps. Demos on a 21-minute N8N lead scraping tutorial. The agent builds the entire N8N flow by watching the video, including clicking buttons, configuring nodes, and testing.

**Key concepts to cover:**
- Why video learning matters (most knowledge is in video, not docs)
- The pipeline: YouTube URL → download → Gemini API → step extraction → Claude execution
- Gemini's 1fps tokenization rate for video
- How to write the extraction prompt for maximum detail
- Practical demo: replicating a workflow from a video
- Combining with Chrome DevTools MCP for browser execution
- Spencer Sterling's Blender donut tutorial as inspiration

**Suggested class:** Techniques (Advanced) or Skills class

---

### 8. Prompt Contracts

**What it is:** Before implementing any non-trivial task, the agent generates a structured 4-section contract: Goal (what done looks like), Constraints (technical limits), Format (output structure), Failure (what would make it wrong). The user approves the contract before work begins.

**Why it matters:** Vague tasks are the #1 cause of poor agent output. "Build me a Netflix" fails because there's no definition of done. Prompt contracts force both user and agent to agree on scope before building — like a freelance scope of work.

**How the competitor teaches it:** Builds a skill called "prompt-contract" that auto-generates the 4 sections. Demos on "build me a beautiful site for leftclick.ai" — the contract specifies: single page, smooth scroll animations, under 500 lines, failure if it looks like Bootstrap. Then chains it with reverse prompting.

**Key concepts to cover:**
- The 4 sections: Goal, Constraints, Format, Failure
- Why vague prompts fail (no definition of done)
- Analogy to freelance scopes of work
- Building it as a skill that triggers before non-trivial tasks
- Chaining with reverse prompting for even better results
- Demo on a real build task

**Suggested class:** Techniques (Fundamental) or Prompt Engineering

---

### 9. Workspace Organization (Business/Personal/Client)

**What it is:** A complete workspace organizational system: business/ workspace at top level with .claude, active/, .env, and client subfolders. Each client gets their own .env, .claude/skills, and claude.md. Separate personal/ workspace for health, citizenship, etc. Color-coded VS Code themes per workspace. Periodic cleanup with Claude.

**Why it matters:** Most people dump everything in one folder and it becomes chaos. This system scales to multiple clients, separates business from personal, keeps workspaces clean, and allows cross-workspace skill calling. The competitor runs a $4M/year business entirely from this structure.

**How the competitor teaches it:** Walks through their actual Anti-Gravity setup showing business/ with client A, B, C subfolders. Shows the active/ folder pattern (dump generated files there, not root). Shows periodic cleanup prompts. Shows personal/ workspace with health, citizenship projects. Demonstrates color-coding with VS Code settings.

**Key concepts to cover:**
- business/ workspace: .claude, active/, .env, claude.md
- Client subfolders with their own .env, skills, claude.md
- active/ folder as dump zone (not root)
- personal/ workspace for non-business projects
- Cross-workspace skill calling (referencing client skills from business)
- Periodic cleanup prompts ("clean up my active/ folder")
- Color-coding workspaces (VS Code settings for different header colors)
- Syncing claude.md with agents.md and gemini.md for diversification

**Suggested class:** Claude Code (new section) or Business class

---

### 10. Agent Harness Concept

**What it is:** An explanation of what an "agent harness" is — the code wrapping around an LLM that turns it from a text-in/text-out model into something that can control a computer. Claude Code IS the harness. The harness includes: system prompt, hooks, tools, parameters (context compaction limits, token limits, message limits), and memory.

**Why it matters:** Understanding that Claude Code is a harness (not just a chat interface) changes how you think about AI agents. The LLM is the brain; the harness is everything else. This is why different harnesses (Claude Code, Droid, Pi, Codex) can wrap the same LLM and get different results.

**How the competitor teaches it:** Uses analogies (dog sled harness, gun barrel directing gunpowder, Space Invader in a house). References Anthropic's Nov 2025 blog post "Effective Harnesses for Long-Running Agents." Compares Claude Code to alternatives (Droid, Pi, CrewAI, Paperclip). Explains that skills and subagents are just "different ways of organizing markdown files."

**Key concepts to cover:**
- Definition: harness = everything wrapping the LLM (system prompt, tools, hooks, memory, parameters)
- The gun barrel analogy (same gunpowder, different accuracy)
- Why Claude Code is the dominant harness today
- Skills and subagents are both "organized markdown files" — same idea, different shape
- Anthropic's "Effective Harnesses" blog post as foundational reading
- Brief comparison to alternatives (Droid, Pi, CrewAI) without going deep

**Suggested class:** Claude Code (Introduction or Advanced) or Techniques

---

### 

### 13. Fan-Out / Fan-In with Model Routing

**What it is:** A formal parallelization pattern where a parent agent (Opus) spawns N researcher sub-agents (Sonnet/Haiku) to investigate different aspects of a problem, then synthesizes all results in a single Opus pass. The researchers "fan out" to explore, the synthesizer "fans in" to integrate. Different from consensus because researchers investigate DIFFERENT angles, not the same question.

**Why it matters:** Reduces research time from 25 minutes (serial) to ~10 minutes (parallel). Uses cheaper models for research (60% cost savings). Keeps the synthesizer in the "zone of good" context-wise because it only receives summaries, not raw research.

**How the competitor teaches it:** Demos on "find best APIs for a feature" — spawns 6 Sonnet researchers on different optimization axes, waits for all to finish, then runs Opus synthesis. Shows the architecture diagram with parent → researchers → synthesizer. Explains the model routing (cheap research, expensive synthesis).

**Key concepts to cover:**
- Fan-out: spawn N cheap researchers on different angles
- Fan-in: expensive synthesizer integrates summaries only
- Model routing: Sonnet/Haiku for research, Opus for synthesis
- Context isolation: each researcher has its own clean window
- Cost savings calculation (research at $3/M vs synthesis at $5/M)
- Difference from consensus (different angles vs same question)
- Practical demo on a real problem

**Suggested class:** Techniques (Advanced) or Claude Code

---

### 14. Deploying Skills to the Cloud (Modal / Netlify)

**What it is:** Taking locally-built skills, websites, and API endpoints and deploying them to the internet so they run independently. Modal for serverless functions (API endpoints, webhook handlers, scheduled tasks). Netlify for static sites. The agent sets everything up — you just provide API keys.

**Why it matters:** Everything built locally is useless if you can't access it from your phone, share it with clients, or trigger it from other tools. Modal lets you create a URL in seconds that runs your skill. Netlify lets you push a website live in minutes.

**How the competitor teaches it:** Full walkthrough: sign up to Modal ($5 free credits), copy config JSON, Claude installs it, deploy a birthday-check endpoint (accessible via browser). Then deploys the lead scraping skill as a web form — fill out the form, get a CSV. Also shows Netlify deployment for the proposal generator app.

**Key concepts to cover:**
- Why deploy: accessibility, sharing, webhook triggers, scheduling
- Modal: serverless functions, $5 free credits, fast setup
- Deploying a simple endpoint (hello world / birthday check)
- Deploying a skill as a web form (lead scraper accessible via URL)
- Netlify: static site deployment for websites/apps
- Environment variables and API key management in production
- Integration with no-code tools (N8N, Make.com) via webhooks

**Suggested class:** Claude Code (Advanced) or Business class
### 21. Computer Use (Mouse/Keyboard Control)

**What it is:** Claude Desktop's computer use feature that literally controls your mouse and keyboard. Unlike browser automation (which manipulates JavaScript), computer use can do ANYTHING on your computer — move files, click menu items, navigate Finder, interact with native apps. Very slow and expensive but universally capable.

**Why it matters:** Computer use is the "nuclear option" — it works on everything but costs a lot. It's the third tier of the automation gradient: HTTP requests (fast/cheap/fragile) → browser automation (medium) → computer use (slow/expensive/universal). Understanding when to use each tier is critical.

**How the competitor teaches it:** Opens Claude Desktop, asks it to find and rename a file in Downloads. Shows the agent literally moving the mouse, typing search terms, scrolling through Finder. Notes it took much longer than manual but works for any task.

**Key concepts to cover:**
- What computer use is (mouse + keyboard control, not just browser)
- The automation gradient: HTTP → browser → computer use
- When to use each tier (tradeoffs: speed, cost, generality)
- Practical demo in Claude Desktop (file management task)
- Cost implications (many tokens for screenshots at every step)
- Current limitations and where this is heading

**Suggested class:** Claude Code (Advanced) or Business class

### 23. Agent Teams Full Tutorial

**What it is:** A comprehensive guide to Claude Code's agent teams feature: enabling it (experimental flag in settings.json), spawning teams, the team lead pattern, teammate communication (shared scratch pad), split pane vs in-process mode, monitoring with shift+up/down, token costs (7x multiplier), shutting down teams.

**Why it matters:** Agent teams are the most powerful parallelization feature but also the most expensive. The existing ACS video (Subagent Teams for Debugging) is narrow and focused on one use case. The transcripts cover the full feature: enabling, multiple design patterns, cost management, and multiple real demos.

**How the competitor teaches it:** Enables agent teams via settings.json. Spawns 3 agents to design websites in parallel. Uses shift+up/down to monitor. Spawns research teams. Demos security audit on OpenClaw with 10 scanner agents + debate agents. Shows $80+ token cost. Demonstrates /shutdown.

**Key concepts to cover:**
- Enabling agent teams (experimental flag in settings.json)
- Team lead vs teammates architecture
- Spawning teams with specific instructions per member
- Monitoring with shift+up/down (in-process mode)
- Split pane mode (multiple terminals)
- Token cost reality check (7x multiplier, $80+ for big tasks)
- Shutting down teams to stop burning tokens
- When teams beat subagents (complex work requiring discussion)
- When to avoid teams (simple parallelizable tasks)

**Suggested class:** Claude Code (Subagent Teams chapter — expand existing)

---

### 24. DOE Framework (Directive Orchestration Execution)

**What it is:** A three-layer architecture for wrapping AI agents in business workflows. Directive layer: workflows and SOPs stored as markdown checklists. Orchestration layer: the AI agent that reads directives and makes decisions. Execution layer: scripts, API calls, browser actions that actually do the work. The predecessor to Claude Code skills — same concept, more formal.

**Why it matters:** This is the business-person's mental model for AI agents. Instead of thinking in code, you think in SOPs and checklists. The agent is just the person who follows the checklist. This framing makes AI agents accessible to non-developers.

**How the competitor teaches it:** Builds a complete sales workflow: lead scraping → classification → proposal generation → email outreach. Each step has a directive (markdown checklist), the agent orchestrates (decides what to do next), and execution happens via scripts/APIs. Shows CRM integration, Google Sheets output, Stripe payments.

**Key concepts to cover:**
- The three layers: Directive, Orchestration, Execution
- Directives as markdown checklists (not code)
- How this maps to Claude Code skills
- Building a business workflow end-to-end
- CRM integration (ClickUp, HubSpot via MCP)
- The self-annealing concept (workflows that improve over time)

**Suggested class:** Business class (core framework)

---

### 25. Self-Annealing Workflows

**What it is:** The process of progressively improving AI workflows over time, inspired by metallurgical annealing (heating metal to find lowest-energy crystal state). Start with a rough workflow → run it → measure results → make small adjustments → repeat. Over many iterations, the workflow becomes highly optimized. Related to auto research but applied to business processes, not code metrics.

**Why it matters:** Most people build a workflow once and never improve it. Self-annealing turns every workflow into a continuously improving system. The competitor applies this to cold email sequences, proposal generation, lead scoring — any repeatable business process.

**How the competitor teaches it:** Explains the annealing metaphor (molecules finding lowest energy state = workflow finding optimal configuration). Shows how to add measurement points to workflows. Emphasizes the loop: run → measure → adjust → run. Notes the safety considerations (adding guardrails before giving agents more autonomy).

**Key concepts to cover:**
- The annealing metaphor (heating → cooling → crystal lattice)
- Applied to business workflows (not just code)
- Adding measurement points to any workflow
- The improvement loop: run → measure → adjust → repeat
- Difference from auto research (business processes vs code metrics)
- Safety guardrails as workflows become more autonomous
- Examples: cold email optimization, proposal quality, response rates

**Suggested class:** Business class or Techniques

---

### 28. Global CLAUDE.md with Personal Profile

**What it is:** Inserting personal context about yourself (role, revenue, team, goals, communication style, reasoning strategies) into your global CLAUDE.md so every conversation across all workspaces understands who you are. This prevents Claude from making irrelevant suggestions (like recommending the cheapest option when money isn't the bottleneck).

**Why it matters:** Without personal context, Claude defaults to generic advice. With it, Claude tailors everything to your specific situation. The competitor includes: revenue breakdown, team members, YouTube stats, Instagram goals, reasoning strategies.

**How the competitor teaches it:** Shows their actual global CLAUDE.md with sections: profile (age, role, revenue), businesses owned, team members (editor, LinkedIn person, AI agents), YouTube goals, Instagram goals. Explains why each section changes Claude's recommendations.

**Key concepts to cover:**
- What goes in global CLAUDE.md (personal context, not project context)
- Profile section: role, revenue, goals, constraints
- Why this changes Claude's recommendations (money vs time tradeoffs)
- Reasoning strategies section (your personal decision-making frameworks)
- Token conservation strategies section
- Where to find your global CLAUDE.md file (~/.claude/CLAUDE.md)
- Keep it concise (bullet points, not essays)

**Suggested class:** Claude Code (CLAUDE.md chapter)

---

### 31. The Core Agent Loop (Observe → Think → Act)

**What it is:** The foundational loop that ALL AI agents run: Observe (read context, files, tool results), Think (reason about what to do next), Act (call tools, edit files, run commands). Repeats until "definition of done" is reached. Context grows with each loop iteration.

**Why it matters:** This is the conceptual foundation for everything else. Understanding this loop explains why context management matters, why planning saves time, and why verification loops work. It's the "first principles" of AI agents.

**How the competitor teaches it:** Draws the loop diagram. Shows Codex CLI going through observe → think → act in real-time (with the grayed-out thinking section visible). Explains the definition of done concept. Shows how context grows with each iteration.

**Key concepts to cover:**
- The three steps: Observe, Think, Act
- Context accumulation per loop iteration
- Definition of done (when the loop stops)
- Why this matters for context management
- The thinking/reasoning panel as visibility into the "Think" step
- How different tools (Claude Code, Codex, Gemini) all run this same loop

**Suggested class:** Techniques (Fundamental — could be Intro or first video) or Business class intro

---

### 32. Subagent Verification Loops (Implement → Review → Resolve)

**What it is:** A formal 3-agent pipeline: Agent 1 (Implementer) writes code → Agent 2 (Reviewer, fresh context, zero bias) evaluates the output → Agent 3 (Resolver, also fresh context) fixes issues identified by the reviewer. The implementer is biased by sunk cost; the reviewer catches what the implementer missed because it has no context about the journey.

**Why it matters:** One agent reviewing its own work is inherently biased. This pattern is the AI equivalent of academic peer review. The competitor runs it on a real app (Splinter) and finds 22 issues that Gemini (the original builder) couldn't see.

**How the competitor teaches it:** Builds a skill called "agent-review" that spawns subagents to review for correctness, edge cases, simplification, and security. Runs it on an existing codebase. Shows the 22 issues found. Demonstrates the fix process.

**Key concepts to cover:**
- Why one agent can't review its own work (sunk cost bias, context pollution)
- The 3-agent pipeline: implement → review → resolve
- Fresh context = zero bias for reviewer
- The 4 review axes: correctness, edge cases, simplification, security
- Building it as a skill
- Demo on a real codebase
- Academic peer review analogy

**Suggested class:** Techniques (Advanced) — partially covered by existing "Avoiding Code Bias" video but deserves dedicated treatment
