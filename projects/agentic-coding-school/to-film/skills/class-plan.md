---
class: skills
title: "From Prompt to Product"
tagline: "Build a complete AI operating system — one skill at a time."
total_videos: 29
status: planning
created: 2026-03-31
---

# From Prompt to Product — Skills Class Plan

One continuous project across the entire class. The viewer builds a complete AI operating system for a real business, adding one layer per chapter. By the end, they have a working system they can use or sell.

## Audience

Primary: business owners, solopreneurs, marketers, consultants, operators who use Claude Code or Co-work but haven't gone beyond basic prompting.

Secondary: developers who've seen the Skills chapter in the Claude Code class but want the full picture on building production skill systems.

## What makes this different from competitors

| Competitor | Their angle | Our differentiation |
|---|---|---|
| Chase (10min masterclass) | What skills are, how to trigger, skill creator | Surface-level, no architecture, no evals |
| Brock (15 skills giveaway) | Practical demos of individual skills, Co-work focused | No progressive disclosure, no structure, no optimization |
| 7 Levels guy | Deep architecture, evals, self-improvement | Theory-heavy, no continuous build project |
| 1% framework guy | Anti-bloat manifesto, curated > massive | Good principles but no class structure |
| Solopreneur AI employees | CEO framework, chaining, selling to enterprises | Business framing but no technical depth |

| Lenny (non-coder home improvement) | Interrogate skill, project briefs, milestones | Great patterns but no skill architecture, no optimization |
| Elliot (brand applicator) | Brand skills from real assets, profile setting hack | Good demos but no progressive disclosure, no evals |
| Designer (front-end design) | Visual output skills, Figma integration | Niche audience, no system building |
| Brand DNA + research guy | Reference file splitting, with/without comparison | Solid fundamentals but single-session scope |

**Our angle**: You build ONE complete system across the class. Every video produces something tangible. We teach the architecture (progressive disclosure, 200-line rule, reference files) through the build, not as standalone theory. And we go further than anyone — evals, self-improvement, chaining, and selling.

---

## Chapter 1: The Blank Slate (3 videos)

### 1.1 — Why Skills Change Everything
- **Duration**: 7-10 min
- **Status**: NEW — class intro
- **Core concept**: "Claude Code without skills is like a smartphone without apps." Skills make Claude do a specific thing in a specific way, every time. Not just chat — actual labor.
- **What to show**: Side-by-side of Claude with vs without the front-end design skill. Side-by-side of a generic contract review vs one with an encoded legal skill (Zack Shapiro example from encoding-your-expertise brief).
- **Key line**: "Skills aren't prompts you save. They're employees you train once."
- **Business pain framing (Miessler)**: Open with the $50T stat — worldwide knowledge worker compensation, most of it producing inconsistent output. SOPs decay, get stuck in people's heads, conflict with each other. Skills are SOPs that execute themselves — they can't forget, can't skip steps, can't produce inconsistent output. The bar AI is competing with is not excellence — it's chaos.
- **Human 3.0 framing (Miessler)**: Address the elephant in the room early — "am I replacing myself?" The capability stack: Knowledge → Understanding → Intelligence → Creativity → Subjective Experience → Desire. AI has the first three. Humans uniquely have the bottom two plus creativity. Your role is deciding WHAT to build, WHY, and for WHOM. Skills handle the HOW. You're not the row in the Excel sheet — you're the person who decides what the spreadsheet should calculate.
- **The control hierarchy** (frame early): There are three layers of control over Claude's behavior:
  1. **Global instructions** (Settings → Profile) — affects everything, always loaded
  2. **Project-level CLAUDE.md / Agent.md** — affects this project/folder
  3. **Skills** — triggered on specific tasks, loaded on demand
  Skills are the third layer, and they're most powerful when the first two are set up properly. This hierarchy is what separates "I told Claude once" from "Claude always knows."
- **Cross-platform note**: Skills work everywhere — Co-work desktop, Claude chat on the web, mobile app. Build once, available across your entire Claude ecosystem. No reinstalling per platform.
- **Cross-link**: [[Types of Skills]] (claude-code class) covers workflow vs knowledge gap — reference but don't repeat

### 1.2 — How Skills Actually Work Under the Hood
- **Duration**: 7-10 min
- **Status**: NEW — this is the "how does it load" explanation nobody does well
- **Core concept**: Progressive disclosure applied to skills. Three tiers:
  - Tier 1: YAML front matter (name + description) — ALWAYS loaded, ~100 tokens per skill
  - Tier 2: skill.md body (the process) — loaded only when skill activates
  - Tier 3: references/scripts/assets — loaded only when a specific step needs them
- **What to show**: The /context command before and after a skill triggers. Show token usage jumping when tier 2 loads, then again when a reference file loads. Make the invisible visible.
- **Key numbers**: 15,000 character limit for total skill descriptions (tier 1). This is why 500 skills kills you.
- **Cross-link**: [[Progressive Disclosure]] (context-engineering class) covers the general principle — this video is the skill-specific application
- **Cross-link**: [[Forked Contexts for Skills]] (claude-code class) — mention but cover in Ch 6

### 1.3 — Set Up Your Workspace
- **Duration**: 5-7 min
- **Status**: NEW
- **Core concept**: Get the tools in place before building. Install Skill Creator. Understand user-scope vs project-scope vs repo-scope. Pick your business/project for the class build.
- **What to show**:
  - Install Skill Creator from /plugin marketplace
  - Show ~/.claude/skills/ (user) vs .claude/skills/ (project) folder structure
  - /reload plugins after install
  - CLI install pattern: `npx skills add <repo> -d-skill <name>`
- **The global profile setting hack**: Go to Settings → General → Profile and add: *"Always consider using the most appropriate skill when answering a query or responding."* This one line tells Claude to actively check skills on every request. Without it, skills "just sit there." Two separate creators independently flag this as critical for activation rates. Do this BEFORE building any skills.
- **Zip packaging note**: Simple skills are just a .md file you upload. Skills with scripts/ or assets/ folders need to be compressed into a zip file first before uploading to Co-work. Quick gotcha that trips up non-technical users.
- **Key decision**: "Do I need this everywhere (user scope) or just here (project scope)?" — the first question for every skill install. Think about compounding: skills should be reusable across projects, not one-offs. If you build a research skill for one project, make it general enough to use everywhere (user scope).
- **Cross-link**: [[Creating Skills]] (claude-code class) — covers the mechanics, this video is purely setup

---

## Chapter 2: Your First Skill (5 videos)

### 2.1 — The Interrogate Skill (Your First Build)
- **Duration**: 8-10 min
- **Status**: NEW — the simplest, highest-ROI skill anyone can build
- **Core concept**: Before building anything complex, build the skill that makes EVERYTHING better: the interrogate skill. This is a meta-skill that forces Claude to interview you exhaustively before doing any work. "Walk down each branch of the decision tree." It solves the #1 non-coder problem: giving Claude bad/incomplete input and getting bad output.
- **Why this is first**: It's pure text. No scripts, no references, no assets. Just a skill.md file with instructions like "Before executing any task, ask the user at least 5 clarifying questions. Explore edge cases. Walk down each branch of the decision tree. Only proceed when you have enough context." This is the easiest possible first build — and the one they'll use every single day.
- **What to show**:
  - Write the skill.md by hand (it's ~30 lines — perfect for understanding the format)
  - Test it: ask Claude to "help me plan a marketing campaign" — without the skill it jumps straight to output. With the skill, it interviews you first.
  - Show the difference in output quality: shallow generic plan vs deeply contextualized plan
- **Key line from competitor**: "That's really where the hard work is — giving it the information it needs so that going forward it has everything to be the best helper it can possibly be."
- **Bridge to next video**: "Now that you've built the simplest skill by hand, let's use Skill Creator to build something more complex."

### 2.2 — Building a Research Skill with Skill Creator
- **Duration**: 10-12 min
- **Status**: NEW — flagship Skill Creator build video
- **Core concept**: Use Skill Creator to build a research/summarizer skill. The viewer's first Skill Creator experience. Show the full flow: describe what you want → answer clarifying questions → skill gets drafted → skill gets tested.
- **What to show**: Live Skill Creator session. "I want a skill that researches any topic and gives me a TLDR brief with key facts, pros/cons, and sources." Skill Creator spins up sub-agents, asks questions, drafts the skill. Then test it on a real topic.
- **Key insight from competitors**: Chase showed Skill Creator running 6 test cases (3 with, 3 without). Show this benchmarking step — it's the "wow" moment.
- **Competitor gap**: Nobody shows the iterative feedback loop properly. Show: first output is 70-80%, give feedback ("make the sources section shorter, add a bottom-line verdict"), Claude updates the skill, re-test.
- **Bonus**: You can also have Claude help you BUILD skills conversationally without Skill Creator — just say "help me build a skill that does X" and it will interview you and draft it. Skill Creator is better for complex skills with evals, but conversational building works great for simple ones.

### 2.3 — Anatomy of a Well-Built Skill
- **Duration**: 7-10 min
- **Status**: NEW — the architecture video
- **Core concept**: Dissect the skill we just built. Explain the folder structure: skill.md (process) + references/ (knowledge) + scripts/ (execution) + assets/ (templates).
- **The 200-line rule**: skill.md should be max 200 lines. It's a table of contents that points to reference files, not a dump of everything. Anything beyond process instructions goes into references/.
- **Point-don't-dump**: The skill.md says "for content templates, see references/content-templates.md" — Claude loads that file only during the step that needs it, then can unload it.
- **The guardrails section**: Every well-built skill.md should end with 3-5 explicit rules that prevent Claude from overthinking or going off-script. Standard guardrails:
  1. "Only load relevant reference files for the current step"
  2. "If guidelines are unclear or information is missing, ask before proceeding"
  3. "Keep responses concise — don't over-explain unless asked"
  4. "If the task doesn't match this skill's purpose, say so instead of forcing a fit"
  These rules are the difference between a skill that works reliably and one that drifts. Multiple creators include them as a distinct section — make it part of the template.
- **What to show**: Take a bloated 400-line skill.md from a marketplace skill. Refactor it live into <200 lines + reference files. Show the 60% reduction. Then add the guardrails section.
- **Key numbers**: The Reddit post — developer had CloudFlare skill at 1,131 lines, Shadcn at 850, Next.js at 900. Loading 5-7K lines every activation. Context window exploded.
- **The visual comparison**: Show a 500-line single-file skill loading into memory vs a 100-line skill.md with separate reference files. "When you split context into reference files, Claude only loads what it needs. Creating a social media post? It loads your voice guidelines but skips your visual style guide."

### 2.4 — Writing Descriptions That Actually Trigger
- **Duration**: 5-7 min
- **Status**: NEW — the activation rate problem
- **Core concept**: 20% activation rate for marketplace skills with bad descriptions. Three-part framework:
  1. **Trigger**: "triggers on: research, trending, what's new in..."
  2. **Not-trigger**: "does NOT trigger for: general web browsing, simple URL fetching"
  3. **Outcome**: "produces: a research brief with TLDR, key facts, pros/cons, sources"
- **What to show**: Take our research skill, show it with a vague description ("helps with research") — run 5 prompts, count how many times it triggers. Then optimize the description with the 3-part framework — run same 5 prompts, count again. Show the jump from ~2/5 to ~4-5/5.
- **The three invocation modes**: Vague ("let's research this") → explicit ("use the research skill") → forced (/research-skill). Know when to use each. Multiple creators recommend defaulting to /slash invocation: "I find the best way to get around all that is just to use the slash command so there's not that confusion of the AI trying to decide."
- **Callback to Ch 1.3**: Remind viewers about the global profile setting ("Always consider using the most appropriate skill"). That one-line fix + good descriptions + /slash invocation = three layers of trigger reliability.
- **Cross-link**: [[Triggering Skills Reliably]] (context-engineering class) covers layer-node tricks to boost trigger rates to 95%

### 2.5 — The Skill You Already Have (Blog Post → Skill)
- **Duration**: 5-8 min
- **Status**: CROSS-LINK candidate from [[Blog Post to Skill]] (techniques class)
- **Core concept**: You don't always build from scratch. Take an article, a blog post, a documentation page you already reference, and turn it into a skill. The "You Might Not Need an Effect" example from the existing video. Or a Zack Shapiro-style "take your firm's playbook and encode it."
- **Decision**: Either cross-link the existing video (it's developer-focused with React useEffect) or re-record with a business example (take a sales playbook PDF → skill). Recommend RE-RECORD for this class's audience.
- **What to show**: Take a real business document (proposal template, review checklist, client brief format) and use Skill Creator to turn it into a skill. Show output with vs without.

---

## Chapter 3: Make It Yours (3 videos)

### 3.1 — Adding Your Brand Context
- **Duration**: 10-12 min
- **Status**: NEW — the personalization video
- **Core concept**: A skill without your business context is a commodity. Add voice profile, ICP, positioning, brand guidelines as reference files. This is what takes output from "sounds like AI" to "sounds like me."
- **What to show**:
  - Create a shared `brand-context/` folder with three reference files:
    - `voice-tone.md` — how you communicate (conversational, confident, uses real examples not theory)
    - `visual-style.md` — color palette, font choices, imagery style (can include actual brand asset files: logos, fonts, PDFs)
    - `messaging-pillars.md` — 3-4 core messages everything should tie back to
  - Add a "context needs" section to the research skill's skill.md that points to these files
  - Run the same research prompt with and without brand context — show the difference
- **The brand applicator approach** (from Elliot's video): You can also build this as a standalone "brand identity guardian" skill that any OTHER skill can invoke. Point Co-work at a folder with your actual brand assets (logos, fonts, brand guideline PDF). Claude extracts colors, typography, pairings, and usage rules, then builds the skill automatically. The result is way deeper than text descriptions — it knows exact hex codes, approved color pairings, logo placement rules, etc.
- **Key quote from competitor**: "An AI SEO skill that knows your brand voice, your product offering, your audience, your content pillars, your competitors, and your positioning will produce content that will both rank and bring you traffic for relevant queries."
- **Draws from**: [[encoding-your-expertise-into-skills]] brief — the Zack Shapiro legal framework. "The gap between 'AI is a toy' and 'AI changed my practice' lives in the quality of your instructions."

### 3.2 — Refactoring a Marketplace Skill
- **Duration**: 8-10 min
- **Status**: NEW
- **Core concept**: Most marketplace skills are badly built — everything in one giant skill.md, no references, no progressive disclosure. But the content is often good. Show how to take a popular marketplace skill, diagnose the problem, and refactor it.
- **What to show**:
  - Find a popular skill from skills.mpp.com or skillhub.com (e.g., the Cory Haynes AI SEO skill at 400 lines)
  - Install it, run /context to see how much it loads
  - Use Skill Creator to refactor: "take this skill, keep skill.md under 200 lines, move all reference info into references/"
  - Show before/after: 400 → 148 lines. 4 new reference files. 60% reduction.
  - Run /context again — show the difference in token usage
- **Key insight**: "The actual content is often really good. The business logic is solid. It's just the structure that's the problem."

### 3.3 — Encoding Your Expertise
- **Duration**: 10-15 min
- **Status**: ADAPT from [[encoding-your-expertise-into-skills]] brief
- **Core concept**: "Templates are commodities, judgment isn't." Your 5/10/20 years of expertise is exactly the asset that AI makes more valuable, not less. Encode it.
- **What to show**:
  - Take a professional workflow the viewer does weekly (proposal review, client brief, contract review)
  - Build a skill that encodes YOUR analytical framework, preferred format, voice, and judgment
  - The before/after: generic prompt ("review this contract") vs skill-encoded prompt (severity-rated, counter-language for each high-severity issue)
- **Live build**: Contract reviewer skill with red flags, yellow flags, missing terms, negotiation suggestions — all encoded from a real professional's judgment
- **Key line**: "Experienced practitioners have the biggest advantage. If you've spent 10 or 20 years developing judgment in your practice area, you are sitting on exactly the asset that AI makes more valuable, not less."

### 3.4 — The Articulation Gap
- **Duration**: 10-12 min
- **Status**: NEW — from Miessler "AI WILL Replace Knowledge Workers"
- **Core concept**: The gap between human expertise and AI expertise isn't the model — it's that nobody has written their expertise down. 3.3 encodes YOUR expertise. 3.4 extracts expertise from OTHER PEOPLE — the "Cliff" who never documented anything.
- **What to show**:
  - Build a knowledge capture interview skill that asks structured questions: "Walk me through how you do X. What do you check first? What are the red flags? What does everyone get wrong?"
  - The skill captures answers into a draft skill skeleton: process steps, decision points, edge cases, common mistakes, quality criteria
  - Demo: interview yourself about something you know well but haven't documented — show how much gets captured
  - "The Cliff exercise": Think of the person at your company everyone calls when things break. Imagine they're retiring in 30 days. This skill is how you capture what's in their head.
- **Key line (Miessler)**: "The expertise gap between humans and AI is actually the failure so far of us to articulate all the different chaos things — all those random pieces of knowledge inside of people's brains."
- **Connects to Ch 7.2**: This knowledge capture is part of the $15K service — walk into a company, interview domain experts, build skills from their knowledge.

---

## Chapter 4: Build Your AI Employees (5 videos)

### 4.1 — The Morning Briefing Employee
- **Duration**: 8-10 min
- **Status**: NEW
- **Core concept**: Build a skill that runs every morning and gives you everything you need to start your day: calendar, urgent emails, industry news, to-dos. This is the skill that demonstrates the "AI employee" concept most viscerally.
- **What to show**:
  - Build the morning briefing skill with Skill Creator
  - Connect it to Gmail, Google Calendar via connectors
  - Show the HTML dashboard output (calendar, emails to respond to, suggested replies)
  - Turn it into a scheduled task (daily at 7am)
- **The bookend — the Update skill**: The morning briefing starts your day. The update skill ends it. After you do real-world work (meetings, calls, progress on a project), you run the update skill and it syncs all relevant project files, briefs, and trackers. "I went through the first milestone this weekend, here's what happened" → skill updates the project brief, marks milestones complete, flags what's next. This is the feedback loop from real-world execution back into your AI system. Without it, your system drifts out of sync. Build both in this video — they're natural complements.
- **Connectors intro**: Skills are 10x more powerful with connectors. Show the connectors panel in Co-work. Gmail, Calendar, Notion, Slack, etc.
- **Zapier MCP hack**: For apps not in the native connector list — Zapier MCP server with 8,000+ apps

### 4.2 — The Content Director
- **Duration**: 10-12 min
- **Status**: NEW
- **Core concept**: Chain multiple skills into one workflow. The "content director" from the solopreneur video: ideation → scripting → calendar, all from one command.
- **What to show**:
  - Build an ideation skill (research trending topics, competitor analysis, view multiplier calculation)
  - Build a scriptwriting skill (your voice, your format, your pacing)
  - Show how Claude auto-routes: "plan my next batch of videos" → ideation skill kicks in → script skill takes over → calendar skill organizes
  - Key point: you don't manually say "use skill A then B then C" — Claude reads the task and picks the right skills automatically
- **Visual output demo**: Don't just show text output. Include at least one visual skill in the chain — a slide deck builder or branded proposal generator. Some of the most viral skill demos are visual: "I built this entire slideshow with one prompt." Show the content director producing a script AND a presentation deck for the same video, using the brand context from Ch 3. This demonstrates range beyond text/data and makes the output feel real.
- **Skills calling sub-skills**: The humanizer gate pattern — before saving any written content, pass it through a humanizer skill to strip AI patterns
- **Cross-link**: [[Combining Skills & Subagents]] (claude-code class) — the technical mechanics of skill chaining

### 4.3 — The Operations Manager
- **Duration**: 8-10 min
- **Status**: NEW
- **Core concept**: Build operational skills: receipt scanner, invoice generator, expense tracker. The boring stuff that eats your time.
- **What to show**:
  - Receipt scanner: drop receipts into a folder → skill categorizes, generates spreadsheet + dashboard
  - Invoice generator: "generate an invoice for Bob, $75K AI contracting" → formatted PDF with your business details pre-filled
  - Turn receipt scanner into a scheduled task (every Friday at 5pm)
- **Key insight**: "I'd rather build 5 apps than spend 30 minutes looking at a spreadsheet. So I built a financial reporting skill instead."

### 4.4 — The Marketing Director
- **Duration**: 8-10 min
- **Status**: NEW
- **Core concept**: LinkedIn posts, email drafts, SEO content — all with your positioning and ICP baked in.
- **What to show**:
  - LinkedIn skill: generates 10-12 post ideas based on trending topics + your positioning → writes 2 variations of each → organizes into posting calendar
  - Email drafter: connected to Gmail, summarizes inbox, drafts responses
  - All pulling from the shared brand-context/ folder created in Ch 3
- **Key number from competitor**: "$4,500/month on help (copywriter $2,500, creative director $1,000, freelancers $1,000) → $100/month Claude Max. 97.8% reduction."
- **Cross-link with Kanban items**: [[social-media-content-engine]], [[linkedin-via-claude-mcp]], [[lead-research-and-outreach]]

### 4.5 — Skills vs Subagents: When to Use What
- **Duration**: 5-8 min
- **Status**: ADAPT from [[skills-vs-subagents]] brief + existing [[Combining Skills & Subagents]] video
- **Core concept**: Skills = consistent, repeatable process. Subagents = autonomy, parallelization, scale. Beyond 30-40 skills, give subagents focused subsets instead of loading everything into one agent.
- **What to show**:
  - Same task done with a skill vs a subagent — show the difference in consistency and autonomy
  - The "specialist subagent" pattern: subagent with 3-5 scoped skills > one agent with 50 skills
  - When to use `context: fork` to isolate a skill's execution
- **Cross-link**: [[Forked Contexts for Skills]] (claude-code class)

---

## Chapter 5: Quality Control (5 videos)

### 5.1 — Evaluating Your Skills
- **Duration**: 10-12 min
- **Status**: NEW — this is the key differentiator from all competitors
- **Core concept**: Stop guessing if your skills work. Use Skill Creator's eval/benchmarking feature. Define criteria, run 5 tests, get assertion pass rates.
- **What to show**:
  - Take the research skill from Ch 2
  - Define 3-5 criteria: "Does it include a TLDR? Does it cite sources? Does it assess pros/cons? Does it give a bottom-line verdict?"
  - Run 5 tests with the skill — see pass rates, time, tokens
  - Run 5 tests WITHOUT the skill — compare baseline
  - Show the benchmark dashboard: assertion pass rate, token cost, time
- **Key insight**: "Up until now it was completely vibes based whether your skills gave high quality output or not."

### 5.2 — A/B Testing Reference Files
- **Duration**: 7-10 min
- **Status**: NEW
- **Core concept**: Not all reference files improve quality. Some just cost tokens. A/B test them: run the same task with and without specific reference files, compare benchmark scores.
- **What to show**:
  - Take the AI SEO skill with 4 reference files
  - A/B test: remove content-type-optimization.md, run 5 tests with and 5 without
  - Result might be: same 93% pass rate but significantly fewer tokens without it → remove it
  - Or: pass rate drops from 93% to 70% → keep it
- **Key line**: "Can we take away some reference files without compromising quality? That's where the A/B test becomes essential."

### 5.3 — Self-Improving Skills (Feedback Loops)
- **Duration**: 8-10 min
- **Status**: NEW — nobody else teaches this
- **Core concept**: Skills should learn from every interaction. Add a learnings.md file that accumulates what works and what doesn't. Add a wrap-up skill that captures session feedback automatically.
- **What to show**:
  - Add a `rules` section to a skill.md that reads from learnings.md
  - Run the skill, notice something good ("articles that open with a direct answer rank faster in AI search") → add to learnings
  - Build a wrap-up skill that runs at end of session, auto-captures feedback into learnings.md per skill
  - Show output quality improving over 3 iterations without manual eval runs
- **Key caveat**: Keep learnings files under control. Prune every week. Too much history = its own context bloat problem.

### 5.4 — The Auto-Improvement Skill (Your System Tells You What to Build Next)
- **Duration**: 7-10 min
- **Status**: NEW — the growth loop
- **Core concept**: Different from 5.3 (where a skill improves ITSELF). This is a meta-skill that looks back on everything you've done across all your skills and suggests NEW skills to build. "Here are some other skills we can build that will help speed things up." It's the growth loop that keeps your system evolving after the class ends.
- **What to show**:
  - Build an "auto-improve" skill that reviews recent sessions and identifies:
    - Repetitive tasks you're still doing manually (→ should be a skill)
    - Steps in existing workflows that could be broken into sub-skills
    - Gaps in your system (e.g., "you have content creation but no content distribution skills")
  - Run it on the system we've built across the class — show what it suggests
  - Pick one suggestion and build it live using Skill Creator
- **Key line from competitor**: "It looks back on everything we've done and says, 'Hey, here are some things we can do better. Here are some other skills maybe that we can build.' This is one way to sort of self-improve your processes going forward."
- **Why this matters**: The class teaches you to build 15-20 skills. But your system should grow to 30-50+ over time. This skill is how that happens without you having to audit your own workflow.

### 5.5 — The Customizer Pattern
- **Duration**: 5-7 min
- **Status**: NEW
- **Core concept**: A meta-skill that customizes other skills. Download someone's skill, run /customize, answer questions about your brand/preferences, get a personalized version.
- **What to show**:
  - Take any skill from the class (or a marketplace skill)
  - Use a customizer skill: "What skill do you want to customize?" → "What's most important?" → "What's your brand voice?"
  - Show before/after: generic slide deck skill → Swiss-design-branded version with your colors
- **Why this matters for sharing**: You can share one plugin with your team and each person customizes it to their context

### 5.6 — Business Metrics for Skills
- **Duration**: 7-10 min
- **Status**: NEW — from Miessler "AI WILL Replace Knowledge Workers"
- **Core concept**: 5.1 measures skills technically (assertion pass rates, tokens). This video measures them in dollars, hours, and consistency — the metrics business people care about.
- **What to show**:
  - Cost per execution vs human equivalent (e.g., content director: $0.12 tokens vs $150 for 2hrs human work)
  - Consistency test: same input to a skill 5 times — near-identical outputs. Same task to 5 different humans — wildly different (the "Sarah vs Jim" problem from Miessler)
  - Quality blind test: skill output vs human output, reviewed blind
  - Build a metrics dashboard meta-skill that tracks cost, time, quality across all skills with weekly rollups
- **The vendor test (Miessler)**: "Now a vendor doesn't come with a steak dinner. We show them our metrics. What are YOUR ratings? What are YOUR cost numbers?"
- **Connects to**: 6.4 (each graph node gets these metrics), 7.2 (business metrics are the proof when pitching)

---

## Chapter 6: Wire It All Together (4 videos)

### 6.1 — Chaining and Stacking Skills
- **Duration**: 10-12 min
- **Status**: NEW — the synthesis video
- **Core concept**: There are two ways skills work together, and most people only know about one:
  - **Chaining** (sequential): Skill A finishes → skill B starts → skill C finishes. A pipeline. "Plan and script my next batch of videos" → ideation → scripting → calendar → humanizer gate.
  - **Stacking** (parallel): Multiple skills active simultaneously on the same task. "I can have my dashboard skill + writing-in-my-voice skill + brand applicator skill + output format skill all at the same time." They layer on top of each other like filters.
- **What to show**:
  - **Chaining example**: "Plan and script my next batch of videos" → ideation skill → script skill → calendar skill → humanizer gate. Show the sequential handoff.
  - **Stacking example**: "Create a client proposal" → brand applicator + voice skill + proposal template skill all active at once. Show /context to see multiple skills loaded simultaneously.
  - **Combined**: "Process this week's finances" → receipt scanner → expense categorizer (chain) with brand applicator stacked on top for consistent visual output.
  - The auto-routing mechanism: Claude reads all active skill descriptions and picks which ones apply. You don't manually orchestrate.
- **Key architectural point**: Skills calling sub-skills is how you build depth without bloating any single skill. Chaining = departments (sequential pipeline). Stacking = layers (parallel enrichment).

### 6.2 — Scheduling Skills as Autonomous Agents
- **Duration**: 7-10 min
- **Status**: CROSS-LINK candidate with [[Scheduled Tasks]] (claude-code class, not yet filmed)
- **Core concept**: Any skill can become a scheduled task. Morning briefing at 7am. Receipt scanner every Friday. Competitor monitor weekly. The skill runs without you.
- **What to show**:
  - Take the morning briefing → schedule it daily
  - Take the receipt scanner → schedule it weekly
  - Show the scheduled tasks dashboard — all your "employees" and when they run
  - Show Slack/Telegram delivery: the output arrives on your phone
- **Decision**: If [[Scheduled Tasks]] is filmed first for the claude-code class, cross-link. Otherwise, this is the canonical video.

### 6.3 — Mapping Your System
- **Duration**: 7-10 min
- **Status**: NEW
- **Core concept**: Visualize your complete AI operating system. Use a workflow visualizer skill to generate an interactive HTML dashboard showing all your skills, how they chain, what's scheduled, what connectors are used.
- **What to show**:
  - Run the workflow visualizer on the system we've built across the class
  - Interactive dashboard: click on each skill to see what it does, when it runs, what it connects to
  - "This is not a tool. This is a content director / operations manager / marketing department."
- **Key number**: "My entire operation runs on Claude Max — $100/month. That's $1,200/year versus $54,000/year for human equivalents."

### 6.4 — Companies Are Graphs of Algorithms
- **Duration**: 10-12 min
- **Status**: NEW — from Miessler "AI WILL Replace Knowledge Workers"
- **Core concept**: 6.3 maps your personal system. 6.4 goes enterprise — every company process is a node in a graph, each with metrics (cost, quality, time), each either human, automated, or hybrid. Skills are the implementation layer for each node.
- **The Lattice Architecture (Miessler)**: A hierarchy where company → department → team → individual each have SOPs, metrics, goals, budget, work, quality. Each tier broadcasts APIs — queryable up, down, and across.
- **What to show**:
  - Map a real business process as a graph (e.g., lead → qualification → proposal → contract → onboarding)
  - Identify which nodes are skill candidates vs human-only vs hybrid
  - Build an interactive HTML graph — color-coded green (automated), yellow (hybrid), red (human-only)
  - Click any node to see its metrics from 5.6
  - The vendor test: "What are your ratings? What are your cost numbers?"
- **Key line (Miessler)**: "You can't optimize what you don't understand. You can't optimize what you don't see."
- **The visibility pitch**: CEOs/CFOs spend months and hundreds of thousands of dollars (McKinsey, KPMG) just to get visibility into what their company is doing. This graph provides it instantly.
- **Connects to**: 7.2 — this graph IS the deliverable for the enterprise engagement

---

## Chapter 7: Ship It (2 videos)

### 7.1 — Sharing Skills with Your Team
- **Duration**: 7-10 min
- **Status**: ADAPT from [[skills-as-team-knowledge-base]] brief
- **Core concept**: Package skills for distribution. Git repos for technical teams. Plugin bundles for non-technical teams. managed-settings.json for enterprises.
- **What to show**:
  - Commit skills to a shared repo — anyone who clones gets the skills
  - Create a plugin bundle (zip of skills) that installs with one click
  - The Zack Shapiro insight: "Knowledge that takes years of mentorship to transmit is now an instruction file that works from the first draft."
  - Show: two Claude instances, same skill, same input → consistent output. vs blank Claude → wildly different output.
- **Cross-link**: Kanban items [[skills-as-team-knowledge-base]], [[managed-settings-json-for-enterprises]]

### 7.2 — Selling AI Operating Systems
- **Duration**: 8-10 min
- **Status**: NEW — the business case closer
- **Core concept**: The system you just built is what businesses pay $15K+ for. How to productize and sell it.
- **What to show**:
  - The pitch: "I'll build an AI operating system that replaces 3-4 employees for your business for a one-time fee"
  - Real numbers: solopreneur video guy working with 3 clients at $15K average deal size
  - The delivery: skill plugin + onboarding + customization session
  - The recurring angle: monthly retainer for skill maintenance, updates, new skills as business evolves
- **Key insight**: "Anyone can go and install 280,000 generic skills. But building one that's tailored to a specific business with years of knowledge and context — that's where the real value is."
- **This is the closer**: The class started with "build skills for yourself." It ends with "sell skills to others."

---

## Cross-Link Map

These existing videos from other classes should be referenced (not re-recorded) at specific points:

| Existing Video | Class | Reference Point |
|---|---|---|
| Creating Skills | claude-code | Ch 1.3 — mechanics of creating |
| Types of Skills | claude-code | Ch 1.1 — workflow vs knowledge gap |
| Arguments for Skills | claude-code | Ch 4.2 — dynamic input to chained skills |
| Allowed Tools for Skills | claude-code | Ch 4.5 — scoping skill permissions |
| Specifying Models for Skills | claude-code | Ch 2.1 — using Haiku for simple skills |
| Real World Skill Example 1 & 2 | claude-code | Ch 3.3 — encoding expertise |
| Blog Post to Skill | techniques | Ch 2.4 — alternative source |
| Skills + Explore Subagents | techniques | Ch 4.5 — parallel skill application |
| Combining Skills & Subagents | claude-code | Ch 4.5, Ch 6.1 — chaining mechanics |
| Forked Contexts for Skills | claude-code | Ch 4.5 — context isolation |
| Triggering Skills Reliably | context-engineering | Ch 2.3 — layer-node boost to 95% |
| Progressive Disclosure | context-engineering | Ch 1.2 — general principle |
| MCP Servers | claude-code | Ch 4.1 — connectors setup |
| Claude Connectors with OAuth | claude-code | Ch 4.1 — OAuth connectors |

## Recording Priority

**Phase 1 — Foundation (record first, highest standalone value)**
- Ch 1: 1.1, 1.2, 1.3
- Ch 2: 2.1, 2.2, 2.3, 2.4

**Phase 2 — The Build (record second, needs Phase 1 as prereq)**
- Ch 2: 2.5
- Ch 3: 3.1, 3.2, 3.3
- Ch 4: 4.1, 4.2, 4.3, 4.4, 4.5

**Phase 3 — Advanced + Ship (record last)**
- Ch 5: 5.1, 5.2, 5.3, 5.4, 5.5
- Ch 6: 6.1, 6.2, 6.3
- Ch 7: 7.1, 7.2

## Video Count Summary

| Chapter | Videos | New | Cross-link/Adapt |
|---|---|---|---|
| 1. The Blank Slate | 3 | 3 | 0 |
| 2. Your First Skill | 5 | 4 | 1 (re-record Blog Post to Skill for business audience) |
| 3. Make It Yours | 4 | 3 | 1 (adapt encoding-your-expertise brief) |
| 4. Build Your AI Employees | 5 | 4 | 1 (adapt skills-vs-subagents brief) |
| 5. Quality Control | 6 | 6 | 0 |
| 6. Wire It All Together | 4 | 3 | 1 (cross-link or co-film with Scheduled Tasks) |
| 7. Ship It | 2 | 1 | 1 (adapt skills-as-team-knowledge brief) |
| **Total** | **29** | **24 new** | **5 adapted/cross-linked** |

### Miessler-sourced additions (2026-03-31)
- 1.1: Added $50T business pain framing + Human 3.0 "where humans fit" intro
- 3.4: The Articulation Gap — extracting OTHER people's expertise into skills
- 5.6: Business Metrics for Skills — dollars/hours/consistency vs technical evals
- 6.4: Companies Are Graphs of Algorithms — enterprise process mapping with the Lattice architecture
