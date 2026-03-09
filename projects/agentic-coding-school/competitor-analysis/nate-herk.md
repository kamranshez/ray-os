---
tags: [competitor-analysis, gap-analysis]
date: 2026-03-09
---

## Nate Herk (AI Automation) - Gap Analysis

**Channel:** Nate Herk - AI Automation
**Videos Analyzed:**
1. "Master 95% of Claude Code in 36 Mins (as a beginner)" (36min)
2. "Turn Claude Code Into Your Executive Assistant in 27 Mins" (27min)
3. "From Zero to Your First Agentic Workflow in 26 Minutes" (26min)
4. "How I'd Teach a 10 Year Old to Build Agentic Workflows" (28min)
5. "How to Build $10K Agentic Workflows" (25min)

---

### Gaps Not Covered in Master Claude Code

- **[HIGH] Building a Personal Executive Assistant System End-to-End** -- Nate builds a complete Claude Code "executive assistant" in a dedicated project folder with structured context files: `context/me.md` (personal info), `context/work.md` (business details), `context/team.md` (team members), `context/current-priorities.md` (active focus areas), `context/goals-and-milestones.md` (quarterly goals), `decisions/log.md` (decision journal), `projects/` (individual project folders with readmes), `templates/`, `references/`, and `archives/`. The CLAUDE.md acts as a routing layer pointing to each file. He runs an interactive onboarding interview where Claude asks questions about the user to populate all context files. This becomes a persistent, growing knowledge system that gets smarter over time. Quote: "If you use this every day, a month from now, this thing is going to look crazy different -- there's going to be way more docs, way more decisions, way more skills." Ray has nothing covering this "executive assistant" or "personal OS" use case.

- **[HIGH] WAT Framework (Workflows, Agent, Tools)** -- Nate teaches a specific framework for structuring Claude Code projects: Workflows (markdown instruction files in a `/workflows` folder), Agent (Claude Code itself as coordinator), and Tools (Python scripts in a `/tools` folder that execute actions). This separation means workflows define *what* to do in natural language while tools handle *how* with actual code. Claude builds both. The self-improvement loop: when a tool fails, Claude reads the error, researches a fix, updates the tool, verifies it works, then updates the workflow so it never happens again. Ray doesn't present this specific organizational framework for building automation projects, though individual concepts overlap.

- **[HIGH] Non-Developer Audience Positioning: Building Automations Without Code** -- Nate consistently frames Claude Code as accessible to non-coders and positions it as a replacement/complement to n8n and Zapier for building business automations. He targets business owners, marketing agencies, and automation builders rather than developers. Examples include: competitor analysis PDFs, YouTube channel analytics, newsletter generation, job scraping to Excel, executive assistant tasks. Ray's course is developer-focused. This represents a significant audience gap -- non-technical users building business workflows. Quote: "Even if you don't know how to code and even if you've never touched an IDE before, you're in the right spot."

- **[HIGH] Branded PDF Report Generation as a Workflow Output** -- Nate shows a complete workflow that takes brand assets (logo PNG, brand guidelines), extracts colors/typography, and generates branded PDF reports using ReportLab with charts via matplotlib. The competitor analysis workflow creates a multi-page PDF with executive summary, competitor profiles, pricing analysis charts, strategic recommendations -- all in brand colors with the company logo. Ray covers no PDF generation or branded output workflows.

- **[HIGH] Newsletter Automation Workflow with AI Images** -- Nate builds a newsletter workflow that: (1) researches a topic via Perplexity API, (2) generates AI infographics using NanoBanana/Key.ai, (3) assembles branded HTML email with brand guidelines, (4) sends via Gmail, (5) archives to Google Sheets. The entire pipeline from "write me a newsletter about X" to delivered branded email with AI-generated images. This is a complete business-ready workflow that Ray doesn't cover.

- **[MEDIUM] Morning Coffee Skill / Day Planning from Connected Tools** -- Nate demonstrates a "morning coffee" skill that reads Google Calendar, project management tools (ClickUp), quarterly goals, video pipeline status, and current priorities -- then generates a prioritized daily schedule and offers to block off the calendar automatically. This is a practical daily-use skill that combines multiple data sources into actionable output. Quote: "If I don't have to have that decision fatigue of what should I do with my next 15 minutes... I'm way more productive."

- **[MEDIUM] Pulse Check on Team Progress** -- Nate shows a "pulse check" skill that reviews all current initiatives, checks task statuses across project management tools, compares against quarterly goals, and generates follow-up action items. This team management use case -- using Claude Code to monitor project health -- isn't covered in Ray's course.

- **[MEDIUM] Auto-Generated Social Media Content from Research** -- In the EA demo, Nate has Claude spin up a sub agent to research a topic (Claude Code voice feature), then simultaneously generate both a LinkedIn post in his tone of voice AND a Twitter-style carousel with 7 slides saved as markdown files in a dated folder. The multi-format content generation from a single research prompt is a practical workflow Ray doesn't demonstrate.

- **[MEDIUM] Firecrawl MCP for Web Scraping in Automation Workflows** -- Nate uses Firecrawl MCP server extensively for scraping competitor websites, job listings, and YouTube data. He walks through the full setup: installing the MCP server via Claude Code, storing the API key in `.env`, and then having Claude autonomously decide which Firecrawl tools (scrape, crawl, search, extract) to use based on the task. Ray covers MCP servers generally but doesn't show Firecrawl specifically or web scraping automation workflows.

- **[MEDIUM] YouTube Analytics Scraping Workflow with Slide Deck Output** -- Nate builds a workflow that scrapes YouTube channels in a niche, analyzes trending content and performance metrics, generates charts, creates a professional slide deck, and emails it via Gmail -- with Google Sheets tracking. Seven Python tools are auto-generated. This specific use case of competitive YouTube intelligence is not in Ray's course.

- **[MEDIUM] Cost Tracking and Budget Awareness for Workflows** -- Nate's workflows include cost breakdowns showing per-run costs (e.g., "$1.43 for this run"). He discusses caching strategies where subsequent runs cost less because business profiles and competitor data are cached. The plan mode also asks about "budget comfort level" with tiered options. Ray doesn't cover cost-awareness or caching strategies for recurring workflows.

- **[MEDIUM] Business Process Discovery / Selling Agentic Workflows** -- Nate devotes significant time to how to sell agentic workflows to businesses: value-based pricing (not hourly), the "doctor not pharmacist" analogy (diagnose problems before prescribing solutions), finding the business "clog" before building. A $5,000 build that saves $10,000/month. The freelancer-to-consultant-to-trusted-partner career path. While this isn't Claude Code-specific, it's a significant differentiator for his audience.

- **[MEDIUM] Perplexity API Integration as a Research Skill** -- Nate builds a dedicated research skill using the Perplexity API (Sonar model) that: loads business context (me.md, work.md, team.md, priorities), formulates multiple search queries based on that context, calls Perplexity, saves a detailed markdown report with sources to a dated folder, and presents a concise summary. He also creates a cheaper sub agent version using Haiku. Ray doesn't show Perplexity integration or context-aware research workflows.

- **[LOW] Interactive Onboarding Interview Pattern** -- Nate's executive assistant setup includes a structured multi-section interview: (1) personal info, (2) business details, (3) team, (4) priorities/goals/projects, (5) communication preferences, (6) recurring tasks. The agent won't move on until it has enough information per section. This conversational setup pattern for initializing a project with rich context is not covered by Ray.

- **[LOW] WAT Framework CLAUDE.md as Downloadable Template** -- Nate provides a standardized CLAUDE.md template for the WAT framework via his free community. This template includes: framework explanation, three-layer structure, self-improvement loop instructions, file structure rules, and how to operate. While Ray covers CLAUDE.md extensively, Nate's specific automation-focused template is a different angle.

- **[LOW] Deployment Path: Cloud Code to trigger.dev/Modal** -- Nate briefly mentions the path from building workflows in Claude Code to deploying them on trigger.dev or Modal for scheduled/webhook-triggered execution. The workflows and tools get pushed to GitHub and synced to these platforms. Ray covers VPS and headless mode but not these specific deployment platforms for automation workflows.

- **[LOW] Brand Assets Folder Pattern** -- Nate shows creating a `brand_assets/` folder with logos, fonts, brand guidelines that Claude can reference for any content generation task. The agent extracts colors and typography from image files and applies them consistently across outputs. While simple, this is a practical pattern for anyone generating branded content.

- **[LOW] Context Rot Warning and Clearing Best Practices** -- Nate explicitly warns about "context rot" -- the degradation of model performance as conversation history grows. He recommends clearing conversations when context usage exceeds ~60%. Quote: "The more and more you use one conversation, the worse the model kind of gets." Ray covers compacting vs clearing but not this specific practical threshold advice framed as "context rot."

- **[LOW] Self-Healing Distinction: Build-Time vs Deploy-Time** -- Nate makes an important distinction that self-healing only works while the agent is actively running (build-time). Once you deploy workflows as code to production (trigger.dev etc.), the agent isn't there to self-heal -- it behaves like traditional automation. Quote: "That self-healing piece is very, very real... while you're building and while you're iterating. But once you deploy that workflow to run on its own... the self-healing ability ultimately goes away." This nuanced distinction isn't covered by Ray.
