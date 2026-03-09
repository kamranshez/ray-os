---
source: "Every Level of Claude Code Explained in 39 Minutes"
channel: Simon Scrapes
video_id: Y09u_S3w2c8
date: 2026-02-07
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] GSD Framework for project planning and execution** — Simon demos the "GSD" (Get Stuff Done) framework extensively as a structured alternative to Ralph loops. It breaks large projects into individual phases, each with its own plan, execute, and user acceptance testing loop. He shows `.planning/` folder structure with roadmap, state tracking, and phase-level documents with wave/task breakdowns. Quote: "GSD is a planner and an executor... when you need a larger project to be broken down into a really comprehensive plan." Ray covers Ralph Loop and planning convergence but not this specific phased framework with UAT verification at each stage.

- **[HIGH] Full content creation pipeline demo using Air Table MCP** — Simon walks through a complete end-to-end workflow: connecting Air Table via MCP, reading a content calendar, pulling specific ideas by date, feeding them into a slash command to generate LinkedIn posts, then writing the output back into the Air Table record. This is a concrete non-coding business use case with a real MCP integration. Ray covers MCP Servers generally but doesn't show this specific Air Table content pipeline workflow.

- **[HIGH] Running multiple parallel terminals with different sub-agents on the same content pipeline** — Simon opens 3-4 terminal panes simultaneously, each running the same content creation workflow pulling different ideas from Air Table, demonstrating how to compress a 15-minute sequential process into 5 minutes. He tracks timing across each terminal. Ray covers subagents and parallelism conceptually but not this specific multi-terminal operational workflow pattern.

- **[MEDIUM] Brand voice hook that auto-checks banned words** — Simon creates a hook that automatically scans every piece of output content for banned words/phrases (e.g., "game-changer," "dive into," "delve") and reports results after each write action. Quote: "No band words found in the output draft. So it gives us peace of mind." Ray covers hooks generally but not this specific brand-voice enforcement use case.

- **[MEDIUM] Content creation system built progressively across all 7 levels** — Simon uses a single use case (social media content creation) and builds on it at each level: basic prompting > CLAUDE.md rules > slash commands > skills > MCP connections > sub-agent teams > Ralph loops. This "progressive build" teaching approach across levels is a pedagogical gap — showing how the same workflow improves at each skill tier.

- **[MEDIUM] Skills vs Commands vs Hooks mental model summary** — Simon provides a clear distinction: "Skills is how Claude thinks... hooks are what happens automatically after Claude Code acts... commands are stuff we trigger manually." While Ray covers each individually, this comparative mental model in one concise framing is a gap.

- **[LOW] PRD.json format for Ralph loop with user stories and acceptance criteria** — Simon shows structuring Ralph loop input as JSON with user stories, each having description and acceptance criteria that Claude self-verifies against. Different from the typical markdown PRD approach.

- **[LOW] Using /mcp add command to set up MCP servers** — Simon shows the built-in `/mcp` slash command to add MCP servers interactively rather than manually editing mcp.json. Quote: "You can just use the command /mcp which is built in, add air table, and it will start setting up this mcp.json file for us."

- **[LOW] Linking Air Table personal access token with specific scopes** — Simon shows the exact flow of getting an Air Table token at airtable.com/create/token/new, selecting read/write record scopes, and granting base-level access. This is a very specific MCP setup walkthrough.
