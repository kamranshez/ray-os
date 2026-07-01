---
title: "Claude Code: Build Your Full AI Marketing Team (Agents + Claude Skills)"
video_url: https://www.youtube.com/watch?v=yLXLHnD4fco
video_id: yLXLHnD4fco
channel: Grace Leung
published: 2026-03-28
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Claude Code: Build Your Full AI Marketing Team (Agents + Claude Skills)**](https://www.youtube.com/watch?v=yLXLHnD4fco) - Grace Leung - uploaded 2026-03-28

> net-new ACS video available: one clean gap (task-board work queue plus phone remote) and two strong next-step complements.

## The one idea worth a video

**Spine A: Design your agents like an org chart, then route each step by whether it needs synthesis or is merely executional.** It is the reframe the whole build hangs off: skill per workflow, group non-overlapping skills into focused agents, wire routing into CLAUDE.md.
VERDICT: next-step video available (complements existing subagent and CLAUDE.md videos).

**Spine B: Author a skill by reverse-engineering a gold reference, then extend an official skill instead of writing from scratch.** Feed a template, have Claude emit an analysis report of its patterns, bolt that onto Anthropic's official skill.
VERDICT: next-step video available (complements existing skill-authoring videos).

**Spine D: Turn a shared Notion task board plus phone remote control into a pull-based, always-on teammate.** Agents pull pending tasks by priority and write status back; the phone dispatches to the local session.
VERDICT: net-new video available.

## Summary and counts

Grace Leung, a digital growth consultant, builds a full AI marketing team in Claude Code with five agents and twelve skills for a travel brand.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine A: Agents as an org chart, routed by synthesis vs execution

The claim: structure Claude Code like a company. Turn each recurring workflow into one skill, group non-overlapping skills into focused agents, and route work by whether a step needs synthesis or is merely executional. Why it is non-obvious: most people pile every skill into one chat and let a single generalist do everything. Grace argues "the more skills you pile into one conversation, the less focused cloud become. Just like one person trying to be your writer, analyst, and designer all at once." The mechanism, in steps: a generalist context holding twelve skills burns attention deciding which to use and drifts; partitioning skills into role-scoped agents gives each a narrow tool set and prompt, so each produces sharper work; a CLAUDE.md routing table then lets Claude pick deterministically, escalating to an agent only when a step "requires synthesizing" and using a bare skill when the step is "executional and straightforward." So the org structure, not a cleverer prompt, is what raises quality. It generalizes to any business function: a sales org (SDR agent, proposal skill) or a support desk (triage agent, macro skills). It goes wrong when roles overlap and agents collide, when routing rules are vague, or when you spawn agents for trivial one-shot work a skill would handle cheaper.

### Spine B: Reference-based skill authoring by extending an official skill

The claim: to make Claude reliably reproduce your brand, do not write a skill from scratch. Hand it a gold-standard template, have it emit a written analysis of that template's patterns, then extend an existing official skill with that analysis baked in. Why it is non-obvious: the instinct is to describe your brand in prose inside a skill. Grace's move is to let the model reverse-engineer the exemplar first, "have clause analyze this template first and to generate the analysis report," turning tacit design rules into an explicit artifact. The mechanism, in steps: a single reference plus a model-written analysis report converts fuzzy "make it on-brand" into concrete, inspectable pattern rules; extending Anthropic's official PowerPoint skill inherits robust deck-building machinery, so the custom skill only adds brand deltas rather than reimplementing rendering; the skill then carries assets plus the analysis as references, so every future deck follows "exactly the same brand presentation template." First run was "90% done." It generalizes to brand voice from a sample blog, email tone from past newsletters, or code style from an exemplar module. It goes wrong when the single reference is unrepresentative, when the analysis over-fits surface details (margins and charts still needed fixing), or when the official base skill fights your customization.

### Spine D: A shared task board plus phone remote as an always-on teammate

The claim: point your agents at a shared Notion Kanban so humans and AI drop tasks into one queue that agents pull from by priority, then attach mobile remote control so you can dispatch to the local session from anywhere. Why it is non-obvious: most agent usage is push, where you sit at the keyboard and prompt. This inverts it to pull: work waits on a board, and the agent will "scan the pending task on this notion board and assign an agent to do it and execute them according to priority," writing status and output paths back when done. The mechanism, in steps: a durable external board becomes shared state both teammates and agents read and write, so collaboration leaves the private chat; priority fields give the agent an execution order without re-explaining; the /remote-control command bridges the phone to the running session, so "everything you sent through your phone is immediately sync to your local Claude code session," making the desk optional. It generalizes to a GitHub issue queue, a Linear board, or a support inbox as the agent's work source. It goes wrong when you "rely on this one single connected session," when context fills and needs /clear, or when an unattended agent executes a mis-scoped board task with no review gate.

## 🎬 Proposed ACS videos

### 1. Give Claude a Task Board: Agents That Pull Work From Notion and Your Phone

HOOK: Stop prompting from your keyboard, let your agents pull the next job off a shared board while you are away.
THE PROMISE: For solo builders and small teams, you will run a Notion Kanban your agents work through by priority, and dispatch tasks from your phone.
THE SHAPE:
- Build a Notion Kanban with priority, title, details, and status columns
- Prompt Claude to scan pending tasks, route to an agent, and execute by priority
- Have the agent write status complete plus output file paths back to the board
- Activate /remote-control and open the link on your phone to dispatch remotely
- Cover the limits: single connected session, /clear when context fills, archive to save locally
SPINE: D
SLOT: Loopy AI, new chapter "Agents from a Task Queue" (alt: Master Claude Code, Other Forms of Claude Code)
RELATIONSHIP: ❌ net-new. "Claude.ai MCP Servers (Connectors)" only covers enabling the Notion connector; "Claude Code for Slack" covers Slack triggering, not a pull-based board; "Claude Code Desktop" explicitly excludes mobile remote. None teaches a shared Kanban work queue agents pull by priority, nor /remote-control from a phone.
PROOF TO REUSE: the David-inspired prompt "scan the pending task on this notion board and assign an agent to do it and execute them according to priority"; the sync line "everything you sent through your phone is immediately sync to your local Claude code session"; the Claude Cowork Dispatch equivalence; the "24 7 teammate" framing.

### 2. Clone Your Brand Into a Skill: Analyze a Template, Then Extend an Official Skill

HOOK: Do not describe your brand to Claude, hand it one perfect example and let it reverse-engineer the rules.
THE PROMISE: For anyone with a house style (decks, docs, posts), you will turn one gold template into a reusable skill that reproduces it on demand.
THE SHAPE:
- Drop a gold-standard reference (a branded deck) into a templates folder
- Ask Claude to analyze it first and emit a written analysis report of the patterns
- Extend an official Anthropic skill (PowerPoint) rather than authoring from scratch
- Store assets plus the analysis as skill references so every run follows the template
- Show the first run is "90% done" and where to fix the residue (margins, charts)
SPINE: B
SLOT: Master Claude Code, Skills (alt: Advanced Techniques, Skills as Force Multipliers)
RELATIONSHIP: 🔗 complements "Blog Post to Skill" and "Real World Skill Example 2", which author skills from articles and scattered notes. Those teach turning source text into a skill; this adds the reference-analysis-report method plus the extend-an-official-skill move for style fidelity, neither of which they cover.
PROOF TO REUSE: the "reference based method" name; the two requirements "the branded deck template and a detailed understanding of how that template works"; "have clause analyze this template first and to generate the analysis report"; "extend the official PowerPoint creation skill"; "it is 90% done."

### 3. Design Your Agents Like an Org Chart: When to Route to an Agent vs a Skill

HOOK: One Claude juggling twelve skills becomes a distracted generalist, so build a team with a routing rule instead.
THE PROMISE: For builders standardizing a whole function, you will decompose recurring work into skills, group them into focused agents, and route by synthesis vs execution.
THE SHAPE:
- Map your recurring workflows, turn each into one skill (one skill per workflow)
- Group non-overlapping skills into focused agent roles (analyst, content creator, researcher)
- Write agent-routing rules in CLAUDE.md so Claude picks the right agent
- Teach the rule: agent for steps needing synthesis, skill alone for executional steps
- Run one complex campaign task and watch the orchestrator route across agents and skills
SPINE: A
SLOT: For Business, new chapter "Design Your Agent Team" (alt: Advanced Techniques, Multi-Agent Orchestration)
RELATIONSHIP: 🔗 complements "Combining Skills & Subagents" (which combines the two on one tRPC migration) and "Hierarchical CLAUDE.md" (folder-scoped instruction loading). This adds the top-down org-design method and the explicit agent-vs-skill routing decision, which those videos do not cover.
PROOF TO REUSE: the four-step design framework (map function, skill per workflow, non-overlapping agents, connect as team); "the more skills you pile into one conversation, the less focused cloud become"; the routing rationale "for content creation that is really executional and straightforward skill should be enough"; the Go Travel five-agents-twelve-skills build.

## 📚 Full wisdom (reference)

### SUMMARY
Grace Leung, a digital growth consultant, builds a full AI marketing team in Claude Code with five agents and twelve skills for a travel brand.

### IDEAS
- Design your AI team in four steps: map function, skill per workflow, group agents, connect team.
- Turn every repeatable marketing task into a skill, ideally one focused skill per distinct repeatable workflow.
- Group similar non-overlapping skills into dedicated agent roles so each agent produces sharper, more focused work.
- Preload brand context first: your voice guide, style guide, product offerings, and core marketing strategy files.
- Separate reusable system folders (context, SOPs, templates) from working output folders like ads, pages, and presentations.
- Initialize the project with a CLAUDE.md file, then keep updating it, it is never a one-off.
- Install official Anthropic skills via the plugin marketplace, then extend them for your own branded project.
- Reference-based method: give Claude gold examples and templates, and it studies the underlying design patterns closely.
- Building a branded deck skill needs the template plus a detailed understanding of how it works.
- Have Claude analyze your template first and generate a detailed analysis report before creating the skill.
- Extend the official PowerPoint skill using the template and analysis report to make custom branded decks.
- First branded deck came back roughly 90% done, needing only minor margin, chart, and layout fixes.
- Connect skills to external MCP tools: the nano banana model generates on-brand social creative images reliably.
- Create a .mcp.json file in the project root to declare which external tools Claude can connect.
- Style references give Claude the vibe to follow, not an exact design to blindly copy directly.
- More skills piled into one conversation makes Claude less focused, like one person doing everything alone.
- Agents are specialized team members with roles and tools; skills are the shared playbook agents reuse.
- Create custom agents with /agents command; Claude generates the agent markdown file defining role, skills, responsibilities.
- The data analyst agent thinks in numbers and charts; content creator thinks in stories and headlines.
- Add agent-routing rules to CLAUDE.md so Claude knows explicitly when to delegate to each specific agent.
- On complex tasks Claude decides per step whether to use an agent or a skill alone.
- Use agents for steps needing synthesis; use skills alone for executional, straightforward, repeatable content creation steps.

### INSIGHTS
- Org structure, not a smarter prompt, is what most raises a multi-skill agent's output quality overall.
- Non-overlapping roles matter: overlap makes agents collide, so partition skills cleanly before assigning them to agents.
- Reverse-engineering a gold example beats describing your brand in vague written prose inside a skill definition.
- Extending an official skill inherits robust machinery, so you only add your brand-specific deltas on top.
- A written analysis report converts tacit design rules into explicit, inspectable, reusable pattern instructions for skills.
- Pull beats push: work waiting on a board lets agents self-assign the next task by priority.
- A durable external board becomes shared state humans and agents both read and write over time.
- Remote control bridges phone to local session, making your physical desk optional for dispatching new tasks.
- The agent-vs-skill routing rule is the real payload; the skills are just the executional muscle underneath.

### QUOTES
- "the more skills you pile into one conversation, the less focused cloud become." — Grace Leung
- "Just like one person trying to be your writer, analyst, and designer all at once." — Grace Leung
- "agents are specialized team members with their own roles and tools, and then skills are the shared playbook your agents can use." — Grace Leung
- "So you give Claude examples or templates of what goods look like And it studies the patterns" — Grace Leung
- "have clause analyze this template first and to generate the analysis report" — Grace Leung
- "it is 90% done." — Grace Leung
- "not just copying the design, but just the vibe." — Grace Leung
- "So Claude knows explicitly when to dedicate to this agent and it will make your system much more reliable." — Grace Leung
- "for content creation that is really executional and straightforward skill should be enough." — Grace Leung
- "everything you sent through your phone is immediately sync to your local Claude code session." — Grace Leung
- "if you're familiar with the Dispatch function from Claude Cowork, they are essentially the same thing." — Grace Leung
- "it really feels like a 24 7 teammate that works for you and get the work done." — Grace Leung

### HABITS
- Grace maps her own weekly marketing tasks first, then turns each repeatable one into a skill.
- She preloads her brand context files before building anything, so agents stay equipped about the brand.
- She keeps updating CLAUDE.md continuously rather than treating the initialization as a single one-off setup step.
- She stores gold templates in a dedicated folder so skills can reference them later for consistency.
- She separates reusable system folders from output working folders to keep agent inputs and deliverables organized.
- She restarts VS Code after editing .mcp.json so new MCP servers register for the project correctly.
- She clears context with clear conversation when a remote session's context becomes too full to continue.
- She archives remote sessions when done, saving all work locally even while away from her desk.

### FACTS
- Anthropic ships official prebuilt skills installable via a plugin marketplace GitHub repository inside Claude Code today.
- Claude Code runs three ways: desktop, an IDE like VS Code, or the full-power terminal option.
- The nano banana image model runs through an MCP server using a Gemini API key here.
- Claude Code now lets a mobile device connect remotely to a local running Claude code session.
- The /remote-control command generates a link opening a mobile chat into your local running session directly.
- Claude Cowork's Dispatch function is essentially the same mechanism as Claude Code's mobile remote control feature.
- The official Claude Code VS Code extension is published by Anthropic in the VS Code marketplace.
- Grace built five agents and twelve skills for a demo travel brand called Go Travel here.

### REFERENCES
- Claude Code (Anthropic); VS Code, Cursor, terminal as the three ways to run it
- Official Anthropic Skills marketplace and the document skills plugin
- Anthropic's official PowerPoint creation skill (extended into a branded deck skill)
- Nano banana MCP server (github.com/zhongweili/nanobanana-mcp-server) with a Gemini API key
- Notion (shared Kanban task board)
- Claude Cowork (Dispatch function)
- Claude mobile app and /remote-control
- HubSpot "The AI Toolkit I Use Every Week" (sponsor resource; covers Claude, ChatGPT, Gemini, Perplexity)
- Grace Leung's growth community and digital growth newsletter
- David, a marketer who suggested the task-board idea
- Go Travel, the demo travel brand

### ONE-SENTENCE TAKEAWAY
Decompose your work into skills, group them into routed agents, and let boards feed them.

### RECOMMENDATIONS
- Map every weekly workflow, then convert each repeatable one into a single focused reusable Claude skill.
- Preload your brand voice, style, offerings, and strategy into a context folder before building any skill.
- Give Claude one gold template, have it write an analysis report, then extend an official skill.
- Group your non-overlapping skills into focused agents so each agent produces sharper, more reliable work consistently.
- Write explicit agent-routing rules in CLAUDE.md so Claude reliably delegates to the correct agent every time.
- Route synthesis-heavy steps to agents; run executional, straightforward steps with a skill alone to save cost.
- Set up a Notion Kanban board so agents pull and execute pending tasks by priority autonomously.
- Activate /remote-control to dispatch tasks to your local Claude session from your phone anywhere you are.
- Never share your remote control link; it grants anyone full control of your running session entirely.
