---
source: "10 Crazy Claude Code Tips That Give You An Unfair Advantage"
channel: AI LABS
video_id: TmsH-RIHvas
date: 2026-02-11
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] /insights command — analyzing past sessions to improve workflow** — AI LABS describes a new Anthropic command: "It analyzes all your past claude code sessions over a certain time period and generates a report. The report analyzes your working style, roasts your working patterns, highlights what you were doing right and what you weren't." They use the insights to add rules to CLAUDE.md (e.g., preventing agent teams from polling indefinitely). Ray doesn't cover this command.

- **[HIGH] Experimental MCP CLI mode to eliminate MCP context bloat** — They enable a flag that removes all MCP tool schemas from the context window: "all the MCPs that were showing up in the context disappeared and no context window was taken up by the MCP tools." Instead of loading schemas upfront, Claude uses `mcp-cli info` and `mcp-cli calls` as bash commands on demand. This is a significant context optimization technique not in Ray's course.

- **[HIGH] Hook with exit code 2 to block test file modifications (TDD enforcement)** — They create a pre-tool-use hook that checks if Claude is trying to modify test files and blocks it with exit code 2. "If the path it's trying to work on is a test directory or contains the word test, it shows an error message saying modifications to test folders are not allowed and returns exit code too." This prevents Claude from cheating on tests by modifying them. Ray covers hooks but not this specific TDD enforcement pattern.

- **[HIGH] Adversarial parallel agents (researcher + fact-checker)** — They set up two agents: one researching and one fact-checking the research agent's output. "one agent does the task while the other critically analyzes it, giving them an adversarial way of working." The fact-checker found many inaccuracies the research agent produced. They note this works for development too: "one agent implements a feature and another reviews the implementation against the plan." Ray covers multi-subagents but not this specific adversarial verification pattern.

- **[HIGH] Vercel Agent Browser as context-efficient verification tool** — They compare three browser testing tools and recommend Vercel's Agent Browser CLI over Claude Chrome extension and Puppeteer MCP: "it uses the accessibility tree where each element has a unique reference. This compacts the full DOM from thousands of tokens down to around 200 to 400 tokens." They add CLAUDE.md instructions to prefer agent browser over MCP-based testing. Ray doesn't cover this tool.

- **[HIGH] User stories as a testing and implementation framework** — They write user stories before implementation that define acceptance criteria for each feature: "Each story features a specific aspect of the app, its priority and the acceptance criteria for the agent to test against." Stories cover best case and edge cases, and Claude implements them one by one. Ray doesn't cover user-story-driven development with Claude Code.

- **[MEDIUM] Four-document project documentation structure (PRD, architecture.md, decision.md, feature.json)** — They generate four specific documents for project context:
  1. PRD — project requirements and scope
  2. architecture.md — data formatting, file structure, APIs
  3. decision.md — decisions Claude made during creation as future reference
  4. feature.json — all features in token-efficient JSON with completion criteria and pass/fail tracking
  Ray covers planning and specs but not this specific four-document structure, especially the token-efficient feature.json format.

- **[MEDIUM] Predictive failure analysis prompt** — They ask Claude to "check the implementation and identify areas where the app could fail" — proactively finding bugs through pattern matching against known failure modes. "found 18 issues that could have been harmful in production, but our testing processes didn't catch them." Ray doesn't cover this specific prediction-based testing approach.

- **[MEDIUM] TypeScript strict mode as an agent error reduction strategy** — They always enable `strict: true` in tsconfig, arguing: "Agents don't have a built-in way to catch runtime errors. Strict mode minimizes the chance of runtime failures and makes sure the compiler handles these issues instead." This is a language-level configuration tip specifically for improving agent reliability. Ray doesn't cover this.

- **[MEDIUM] Worktrees over branches for parallel agents** — They explain why worktrees are preferred: "Branches aren't preferred because they cause conflicts. Agents have difficulty checking out different branches since branches share the same working directory but work trees don't." Ray doesn't cover worktrees.

- **[MEDIUM] Context7 MCP for latest library documentation** — They use Context7 MCP to give Claude access to current library docs: "It has documentation for all the libraries and frameworks and gets updated frequently so that agents can pull the latest docs and fill the gap between what the model knows and what actually the current update." While Ray covers MCP Search Tool, Context7 as a specific documentation MCP for preventing dependency mismatches may not be covered.

- **[LOW] Hook exit codes explained (0 = success, 2 = blocking error, other = non-blocking)** — The specific exit code system for hooks is a technical detail that helps users build more sophisticated hooks. Ray covers hooks but may not detail these exit codes.
