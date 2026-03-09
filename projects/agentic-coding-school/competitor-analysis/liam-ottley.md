---
source: "How to Automate Your Life & Work w/ Claude Code: Ultimate Beginner's Guide"
channel: Liam Ottley
video_id: 2bsfQThGXxc
date: 2026-02-12
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Workspace template for non-code productivity automation**: Liam provides a full workspace template with folders for commands, skills, context, outputs, plans, and reference scripts -- designed for business automation, not coding. He breaks context into four documents: business context, personal info, priorities/strategy, and communication style. This "personal assistant workspace" pattern is distinct from coding project setups. Quote: "When you are thinking about setting up claude code to be your personal assistant to automate parts of your work, you need to create a workspace for it to operate within."

- **[HIGH] Context stacking diagram -- layered context management**: Liam presents a visual framework for context management: CLAUDE.md at the bottom, then context documents, then commands/skills layer, then the task layer on top. He teaches this as a mental model for how context flows. Quote: "I think of it in layers. Like we need to start with the CLAUDE.md file... then on top of that..." Ray covers context engineering concepts but not this specific layered stacking visual/framework.

- **[HIGH] Using Apify MCP for real-time data scraping in workflows**: Liam demonstrates connecting Claude Code to Apify via MCP to scrape YouTube channel data (views, engagement, video details for the 20 most recent videos) and then generating competitor analysis reports and PowerPoint presentations from that data. This specific MCP integration for business intelligence is not covered by Ray.

- **[HIGH] Background research agent (deep research mode in Claude Code)**: Liam triggers what he calls a "background research agent" that does comprehensive web research in the background while Claude continues other tasks. He uses this for competitor analysis. Quote: "I want to trigger one of these background research agents which will go on the web to find all the links of the podcast background information." Ray covers subagents and background tasks but not this specific deep research agent pattern.

- **[HIGH] End-to-end automation demo: competitor analysis to PowerPoint**: Liam demonstrates a complete workflow: `/analyze competitor Lenny's Podcast` triggers deep research, Apify YouTube scraping, markdown report generation, and automatic PowerPoint creation using a PPTX skill. This is a compelling real-world business automation that Ray doesn't replicate.

- **[MEDIUM] Priming sessions with context -- explicit "/prime" command pattern**: Liam emphasizes creating a priming command that you run every time you start a new Claude Code session to load context. He treats this as a critical best practice. Quote: "We want to be priming our session every single time when we spin it up. We want to be using new sessions of Claude Code as often as possible rather than chatting away non-stop." Ray covers session management but not this explicit priming-on-startup pattern.

- **[MEDIUM] Four biggest mistakes beginners make (framework)**: Liam structures his content around four specific mistakes:
  1. Not providing enough context (no CLAUDE.md, no context docs)
  2. Not using plan mode to think before acting
  3. Not managing context window properly (200K limit awareness)
  4. Not using commands/skills to automate recurring workflows
  Ray covers all these topics individually but doesn't frame them as a "biggest mistakes" list.

- **[MEDIUM] Shell aliases for quick Claude Code launch modes**: Liam sets up shell aliases like `cc` for standard launch, `ccy` for YOLO mode with auto-accept, and priming aliases. Quote: "We have the shells alias here which you need to copy and paste... quick access to the sort of yolo mode and priming setup." Ray doesn't cover shell aliases for Claude Code launch configurations.

- **[MEDIUM] Storing API keys in .env file within workspace for skill access**: Liam demonstrates using a .env file in the workspace to store API keys (Apify, etc.) so skills can access them persistently across sessions. Quote: "In this .env file is where you can put your tokens. And this is going to be a sort of persistent place for you to store all your API keys so that your claude code agent can grab the information from there." Ray doesn't cover this .env pattern for skill API key management.

- **[MEDIUM] Skills Marketplace (skillsmpp.com) for downloading pre-built skills**: Liam shows browsing and downloading skills from a Claude Skills Marketplace, specifically downloading the PPTX/PowerPoint skill from Anthropic. Ray covers the plugin marketplace but not this specific skills marketplace.

- **[LOW] Using MCP integration skill to teach Claude how to use MCPs**: Liam has a meta-skill called "MCP integration" that teaches Claude Code when and how to use MCP connections. This is a skill about skills. Ray doesn't cover this meta-pattern.

- **[LOW] Outputs folder pattern for organized command results**: Liam's workspace template includes a dedicated "outputs" folder where commands automatically save their results (e.g., competitor-analysis/lenny-podcast/report.md). This organizational pattern isn't covered by Ray.
