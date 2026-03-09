---
source: "The Only Claude Skills Guide You Need (Beginner to Expert)"
channel: Kenny Liao
video_id: 421T2iWTQio
date: 2025-10-24
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Skills as a context engineering solution — token efficiency framing** — Kenny frames skills primarily as a context engineering solution to the problem of loading all MCP tool schemas into the system prompt. He explains that an MCP with 20 tools might use 3,000 tokens in the system prompt, while a skill providing similar functionality only loads ~50 tokens initially (name + description). Quote: "At any given moment for the particular task at hand, you might use only a few tools or let's say less than 10% of the tokens that you actually loaded for all of those tool definitions." Ray covers skills extensively but may not frame them through this specific token-efficiency lens compared to MCPs.

- **[HIGH] Building a skill that invokes another AI CLI (Gemini) through bash** — Kenny's YouTube thumbnail skill calls the Gemini CLI via bash command, which is connected to the Nano Banana MCP server for image generation. This is a concrete example of a skill that orchestrates across multiple AI systems. Quote: "Claude Code can just run terminal commands. It can actually invoke the Gemini CLI and so it can run that agent which is connected to the Nano Banana MCP server." Ray doesn't seem to cover cross-CLI orchestration within skills.

- **[HIGH] Hierarchical context directory system for personal assistants** — Kenny shows a sophisticated context engineering setup with nested `context/` directories containing subdirectories for memory, projects, and tools, each with their own `claude.md` files. The agent traverses these progressively. Quote: "As the agent traverses these CloudMD files, it's going to get a little bit more context." This is a practical implementation of progressive disclosure beyond just skills — it's a full context architecture for a personal assistant.

- **[MEDIUM] Skills in the Claude web/desktop app (not just Claude Code)** — Kenny shows how to use skills in the Claude desktop/web app through Settings > Capabilities > Skills, including uploading zip files of skill folders. He demonstrates that skills are portable between Claude Code and the web app. Ray's course focuses on Claude Code but this cross-platform skill usage could be valuable.

- **[MEDIUM] Financial modeling skill (cohort analysis in Excel)** — Kenny demos a skill that takes transaction CSV data and builds a complete cohort analysis Excel model with formula-based cells, retention matrices, LTV calculations, and adjustable input parameters. The skill includes Python validation scripts to check for formula errors. This is a specific non-coding business use case for skills.

- **[MEDIUM] Skill that includes Python validation scripts** — Kenny's cohort analysis skill includes a `scripts/` folder with Python validation scripts the agent runs after building the Excel model to verify formula correctness. This pattern of embedding executable validation into skills is a specific technique.

- **[MEDIUM] YouTube thumbnail generation skill with design requirements docs** — Kenny's thumbnail skill has a `skill.md` with a table of contents pointing to required reading (design requirements, prompting guidelines) and optional assets (icons, headshots, templates). Some context files live outside the skill folder. This demonstrates skill architecture with external references and mandatory vs optional context.

- **[MEDIUM] Skills compounding: skills that leverage other skills** — Kenny mentions building an "Excel model builder" skill that leverages Anthropic's default Excel tool skill. Quote: "You can just kind of piece different skills together and build new, more powerful skills that leverage other skills." Ray covers combining skills and subagents but this specific skill-on-skill compounding pattern may be a gap.

- **[MEDIUM] Iteratively debugging and improving skills** — Kenny describes a specific workflow for improving skills that aren't working: tell Claude the skill failed because of X, show expected vs actual output, have it review the full skill, identify failure points, suggest fixes, and implement. Quote: "You can iteratively improve the skill and get it closer to what your expected output is." This is a practical debugging workflow for skills specifically.

- **[LOW] Skill creator skill from Anthropic** — Kenny mentions Anthropic's built-in "skill creator" skill that lets you prompt Claude to build new skills. You can see Anthropic's own best practices for skill creation by examining it.

- **[LOW] Why progressive disclosure isn't implemented for MCPs yet** — Kenny raises an interesting technical question: why doesn't Claude progressively disclose MCP tool schemas the same way it does with skills? He's done this in custom agents. This could be an interesting discussion topic.
