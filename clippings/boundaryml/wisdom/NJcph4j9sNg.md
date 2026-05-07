---
video_id: NJcph4j9sNg
title: "Claude for non-code tasks: 🦄 #20"
url: https://www.youtube.com/watch?v=NJcph4j9sNg
channel: BoundaryML
---

### SUMMARY
Both (BAML) and Dex (HumanLayer) demonstrate using Claude Code for non-coding tasks like CRM, release notes, daily reviews through context engineering and markdown.

### IDEAS
- Becoming a better agent user makes you a fundamentally better agent builder by surfacing missing UX patterns.
- Context engineering matters whether you build agents or only send the user message.
- Abstracting all internals from users hurts power users and lowers the achievable ceiling significantly.
- Markdown files plus front matter form a flexible knowledge graph rivaling SQL databases.
- The best context engineering gives the model the exact answer immediately, skipping reasoning.
- Second best is dumping maximally relevant data without filtering for noise reduction concerns.
- Third best is pruning noise so the model focuses on what actually matters.
- Front matter at file tops mirrors docstrings, helping agents skim before reading entire documents.
- Deterministic context packing via make scripts beats agentic searching for repeated workflows reliably.
- SOPs become reusable prompts encoding manual workflows like daily reviews and investor updates.
- Standups can be replaced by scripts diffing recent branches and summarizing PRs automatically.
- Agents versus workflows is the wrong frame; tolerance for inconsistency is the real axis.
- Software 3.0 sits between traditional code and ML, flexible but occasionally broken.
- Once a workflow stabilizes, bake it into a TypeScript script for speed and determinism.
- Performance engineering taught us to optimize bottlenecks, not every line of code.
- Context engineering similarly means optimizing critical sections, not perfecting every word everywhere.
- Cloud code's bash-only paradigm would work, but specialized tools let models think higher level.
- The Task tool prompt matters; calling subagents "tasks" yields better targeted prompting.
- Cloud MD content gets suffixed with "may not be relevant" reducing model attention significantly.
- Proxying Claude Code reveals system prompts and tool descriptions for deeper context engineering.
- Lossy outputs like meeting notes don't require perfection, just directional correctness for utility.
- The agent harness around the model matters as much as the model quality itself.
- Always be clearing or compacting; maintain external state files instead of relying on chat history.
- Linear MCP dumps too much JSON; wrapping it with custom scripts beats native integrations.
- Most tools are built incorrectly because median developers haven't yet learned context engineering.
- Cloud Code excels at non-coding tasks because it can write its own scripts dynamically.
- Caching saves money but you still pay output tokens for each model bash decision.
- Working backwards from desired weekly outputs clarifies which workflows deserve automation investment.
- Background tasks can't have dependencies in Claude Code; build your own loop if needed.
- Dynamically rewriting user context lifts the floor but lowers the ceiling for power users.
- The definition of engineering will evolve; today's prompting may be tomorrow's Python equivalent.
- Hard problems abandoned by humans for days got solved in seven hours via vibe coding.
- Generated code worked end-to-end but required cleanup passes to match design intent.
- Show me the prompt is the rallying cry of advanced users hitting abstraction walls.
- Tools should be small and specific, not god-tools requiring complex bash invocations always.
- IDE windows for deterministic context management may matter less as models improve dramatically.

### INSIGHTS
- Context engineering is universal; only the levers available differ between users and builders.
- Markdown plus front matter offers the lowest-friction database for prototyping agentic workflows quickly.
- The model's tolerance for noise inversely correlates with its ability to produce signal.
- Bake stable workflows into deterministic code; let LLMs handle ambiguity at the edges.
- Trust calibration, not architecture choice, determines when to use agents versus workflows.
- Composable building blocks beat monolithic systems; agents call workflows and vice versa freely.
- Tool design quality reflects whether the builder understands context engineering principles deeply.
- The agent harness, model, and prompt together determine capability; none alone suffices.
- Power users need transparency; novice users need abstraction; both serve different ceiling tradeoffs.
- Optimization should follow proven workflows, not precede them in agentic system design.
- External state files outperform chat logs as the source of truth for resumable work.
- Software's evolution has always redefined engineering; LLM-driven workflows continue that historical trend.

### QUOTES
- "I actually become a better agent builder by becoming a better agent user." — Both
- "LLMs are stateless functions; the only thing affecting answer quality is token quality." — Dex
- "It's almost your obligation as an agent builder to provide some insight to your users." — Both
- "Cloud Code runs our CRM." — Dex
- "If you give it the exact answer you want to spit out, it will spit it out." — Both
- "The next best thing is give it as little noise about what isn't relevant." — Both
- "Spend $2 just to run a make command." — Both
- "Don't make every single system perfectly engineered." — Both
- "It's allowed to be lossy." — Dex
- "I work backwards from the workflows." — Dex
- "I have never read the source code of the cat command." — Both
- "By taking over the user's context completely, you bring down the ceiling a lot." — Both
- "Show me the prompt." — Hussein (referenced)
- "We don't have one website to rule them all." — Dex
- "Always be compacting." — Both
- "MCPs are just API calls." — Both
- "The median right now is pretty bad." — Both
- "Tools that we use all the time have different patterns and different UX." — Dex
- "If thing is working, don't bother understanding it." — Both
- "It's an optimization spectrum." — Dex

### HABITS
- Dex runs a daily review SOP every morning brain-dumping calendar, meetings, and follow-up items.
- Generates nightly release notes via Claude Code combining PR data and Slack announcement posts.
- Compiles monthly investor updates by compacting accumulated daily reviews into structured summaries.
- Maintains a git repo specifically for non-technical work like CRM and journaling activities.
- Uses Opus model for everything despite higher per-call cost trade-offs in workflows.
- Writes design docs through Claude before writing implementation code on hard projects.
- Always tracks state in markdown files rather than relying on agent chat history persistence.
- Uses slash commands like /ctx to inject deterministic context bundles into Claude sessions.
- Wraps verbose MCPs like Linear with custom scripts that filter out unnecessary JSON noise.
- Allowlists specific scripts in permissions rather than broad bash command patterns globally.
- Reviews release notes morning after merges before publishing to trusted-tester Slack channels.
- Both writes design docs through Claude with file-link summaries for quick navigation later.
- Adds linting rules to enforce small files since Claude Code reads only first hundred lines.
- Both uses Obsidian as the source of truth for design docs and project notes.
- Compacts conversations using custom prompts listing files touched and broken next steps.

### FACTS
- Claude Code reads approximately the first 100 lines of long files when first encountering them.
- Cloud Code has at most four caching segments built in for prompt cache reuse.
- Adding cancellation to BAML produced roughly 35,000 lines of mostly generated code.
- Three engineers spent four days each previously failing to solve the BAML cancellation problem.
- Two engineers solved BAML cancellation plus WASM support in approximately seven hours together.
- Claude Code suffixes Cloud MD content with text instructing it may not be relevant.
- Karpathy described Software 1.0 as code, 2.0 as ML, and 3.0 as LLMs.
- Cloud Code's task tool launches subagents but is internally named "task" not "subagent."
- Generated PRs from agentic workflows often work end-to-end but need cleanup for design alignment.
- BAML is a programming language built specifically for structured LLM output and prompts.
- HumanLayer is Dex's company building tools for agentic coding workflows and collaboration.
- Cloud Code can be proxied to log all upstream Anthropic API requests for inspection.
- Linear's MCP server returns large JSON blobs that pollute agent context windows significantly.
- Code Layer is Dex's tool for parallelizing engineering work across multiple branches simultaneously.
- The AI That Works show provides about one hour weekly of practical advanced AI coding tips.

### REFERENCES
- BAML programming language by BoundaryML
- HumanLayer company and Code Layer tool by Dex
- Cloud Code by Anthropic
- Cursor IDE
- Obsidian markdown editor
- Linear project management
- Salesforce, Airtable CRM platforms
- Andrej Karpathy's Software 1.0/2.0/3.0 framing
- MRA's take on agents and workflows composability
- AI That Works weekly show repository
- Reveals (YC batch company example)
- Anthropic API and Opus model
- GitHub CLI (gh) for PR fetching
- Bun TypeScript runtime
- TypeScript scripting in tools/ directories
- Slack for trusted tester announcements
- Superhuman email client

### ONE-SENTENCE TAKEAWAY
Master context engineering by treating Claude as collaborator; markdown plus deterministic packing beats fancy databases.

### RECOMMENDATIONS
- Build a personal git repo for non-technical agentic workflows like CRM, journaling, and reviews.
- Use markdown with YAML front matter as your default database before reaching for SQL.
- Write SOPs as reusable prompts that encode your manual workflows step by step.
- Create make scripts that deterministically pack context instead of agentic file searching every time.
- Add slash commands like /ctx to inject baseline context bundles consistently across sessions.
- Wrap verbose MCPs with custom scripts that filter out JSON noise before reaching agents.
- Allowlist specific scripts in Claude permissions rather than broad bash patterns for safety.
- Replace standups with scripts that diff branches and summarize commits over recent days.
- Once a workflow stabilizes, convert it to a TypeScript script for speed and determinism.
- Always maintain external state files; treat chat logs as ephemeral working memory only.
- Proxy Claude Code traffic to inspect system prompts and tool descriptions during debugging sessions.
- Write design docs through Claude before implementation, especially for complex architectural changes.
- Add linting rules enforcing small files so Claude's first-100-lines heuristic stays useful.
- Compact context using custom prompts listing files touched, changes made, and next steps.
- Work backwards from desired weekly outputs to identify which workflows deserve automation investment.
- Use Opus for everything when accuracy matters more than per-call cost considerations significantly.
- Avoid Cloud MD for critical instructions since the suffix reduces model attention noticeably.
- Pick lossy tasks like meeting notes for early agentic experiments before tackling perfection-critical workflows.
- Build subagent prompts explicitly with how-to-prompt instructions to get clearer focused results back.
- Treat tool design as context engineering; small specific tools beat god-tools requiring bash invocations.
