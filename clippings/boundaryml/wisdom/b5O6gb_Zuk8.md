---
video_id: b5O6gb_Zuk8
title: "Agents, Subagents, Skills and Commands"
url: https://www.youtube.com/watch?v=b5O6gb_Zuk8
channel: BoundaryML
---

### SUMMARY
Dex (Human Layer) and Vibhav (Boundary) explain Claude Code's commands, sub agents, and skills, separating context isolation from instruction modules across coding workflows.

### IDEAS
- Sub agents exist primarily for context isolation, removing irrelevant tokens once a task returns its summary.
- Instruction modules and context isolation are orthogonal concepts; conflating them inside sub agents creates architectural mess.
- Slash commands originated as user-invoked prompt wrappers before sub agents and skills evolved later inside Claude Code.
- General purpose sub agents inherit standard tools while custom sub agents inject persistent userdefined instructions every invocation reliably.
- The slashcommand tool briefly bridged the gap, letting parent contexts inject instructions without forking new context windows.
- Skills replaced slash commands as dynamic, model-invocable instruction bundles loadable from parent or sub agent contexts.
- Skill instructions arrive as user messages, earning higher attention than tool results or background file reads.
- Every installed skill description still consumes instruction budget until tool search activates above ten thousand tokens.
- Sub agent quality depends entirely on parent prompt quality since each call resembles a single tool invocation.
- Forking sessions from earlier user messages predates sub agents and remains useful for cheap context resets.
- Pruning SQL query results after final answer lets models rerun cheap queries without polluting context windows.
- Playing house with backendengineer and frontendengineer sub agents fails because instruction modules masquerade as personas without value.
- Don't outsource thinking to agent teams; bottleneck remains design quality, not raw code generation throughput.
- Amazon now requires senior review for L1 to L3 AI generated code due to slop accumulation problems.
- Lights off software factories will collapse when 3am incidents hit code nobody has read recently.
- Monorepos dramatically simplify shared agent configuration; coordination repos with sim links offer pragmatic alternatives elsewhere.
- Git submodules consistently fail for agent navigation; sim linked source directories prove ergonomic for Claude Code.
- Disable model invocation flag hides slash commands from descriptions, reserving skills for explicit user invocation.
- Description hack "do not invoke unless asked by name" steers models toward conditional skill invocation.
- Code review products commoditize quickly because users buying context engineering can replicate prompts once leaked.
- Context engineering resembles app store purchases, not subscriptions, because copying prompts neutralizes any defensible moat.
- Anthropic faces tension between platform inference revenue and product surface like Claude Code competing internally.
- Max plan rules tighten because outside harnesses generate unoptimized inference traffic Anthropic cannot subsidize at scale.
- Cloud Agent SDK wraps the Claude Code binary, inheriting identical behavior whenever the right flags propagate through.
- Prescriptive workflows beat letting engineers innovate in seven half baked directions across a growing team.
- Lifting the median engineer outperforms supporting a few 50x outliers while everyone else flounders inconsistently.
- Coordination repo template uses additional directories permission to read across sibling repos without git submodules.
- Worktree based workflows separate research on main from writing inside per-task checkouts of relevant repos only.
- Open sourcing prompts beats walling them since paying users were never the leakers anyway long term.
- Throwing tokens at code review works, but Anthropic billing twenty bucks for self correction feels meme worthy.
- MCP servers exposing twenty seven tools each devastate context windows, motivating tool search lazy loading defaults.
- Cloud code can flip server side feature flags adjusting behavior, something open code competitors fundamentally cannot match.
- Sim linking open source repo into closed source repo simulates monorepo ergonomics without forcing organizational restructure.
- Skills bundle reference files enabling progressive disclosure while keeping initial descriptions short and instruction budget friendly.

### INSIGHTS
- Architecture matters more than personas; treat sub agents as context isolation primitives, not workplace org chart simulations.
- Models swappable inference plus token observability means prompt secrecy provides essentially zero durable competitive advantage.
- Bottleneck in AI assisted engineering remains design and review, never raw code emission speed.
- Instruction budgets are real; every always loaded sub agent or MCP tool steals user instruction attention.
- User messages outrank tool results for attention, so skills inject instructions as messages deliberately.
- Forking sessions remains the cheapest context reset trick, predating and complementing modern sub agent abstractions.
- Throw away wrong designs entirely rather than letting LLMs hack iterations atop fundamentally broken foundations.
- Surface area added by shipped features compounds maintenance burden; ship only when genuinely worth shipping.
- Consolidate workflows aggressively when teams scale; flexibility creates inconsistency that crushes median productivity over time.
- Tool descriptions function as advertisements; verbose ones poison context windows for marginal selection accuracy gains.
- Coordination repos with additional directories permission outperform git submodules for multi-repo agentic coding workflows reliably.
- Companies optimizing for token throughput while skipping human review will face catastrophic 3am production failures eventually.
- Caching and traffic shape determine subsidization economics, not just total inference volume across managed plans.
- Context engineering is a one-time purchase replicated easily; sustained moats require ongoing maintenance against new models.
- Removing irrelevant context as soon as possible mirrors human working memory hygiene during complex problem solving.

### QUOTES
- "Sub agents are just a really easy way to do that while coding." — Vibhav
- "Separate out instruction modules from context isolation. Like these are two orthogonal concepts." — Dex
- "Don't put your custom instructions in agents." — Dex
- "If it's shitty, it's just unmaintainable slop." — Dex
- "A lot of companies are going to die because they lean too hard into the lights off software factory." — Dex
- "Everybody wants AI that doesn't suck. We should call it AI that sucks." — Vibhav
- "Sub agents are good for context isolation." — Dex
- "Quality of the sub agent result is directly related to how good is the prompt the parent gave it." — Dex
- "Skills are dynamically loaded in as needed rather than preloaded in like slash commands." — Vibhav
- "You literally cannot work if you have downloaded the HubSpot MCP." — Dex
- "It's wrong architecturally. You're forced to do this almost." — Vibhav
- "It's way better to lift a median." — Vibhav
- "Everyone should do a monor repo." — Vibhav
- "Get submodules just is not ergonomic for the model." — Dex
- "Do not outsource the thinking." — Dex
- "Tokens, man. Thinking tokens. Before you code, you need to spend your own thinking tokens." — Vibhav
- "If you stop reading the code... eventually the models will be smart enough but in the next couple years a lot of companies are going to die." — Dex
- "We're all using the same models. If you can use cloud code to write the code then cloud code can review it." — Dex
- "Context engineering is a one-time purchase. It's not a permanent purchase." — Vibhav
- "You cannot build a company on a prompt because someone will figure out how to crack it." — Dex
- "If someone's paying the token bill they're going to find the prompt." — Dex
- "Tokens are low alpha long term." — Vibhav
- "Don't ship things just because you can. Make sure it's worth shipping because it adds surface area." — Dex
- "We've decided that we're going to live in a world where cloud code lives." — Vibhav
- "Make them want the new thing." — Dex

### HABITS
- Forking Claude Code sessions from prior user messages to reset context after long meandering tool exploration cheaply.
- Pulling GitHub PR comments via shell script and addressing them automatically inside Claude Code sessions routinely.
- Telling models to moo like a cow to detect when long contexts stop following instructions reliably.
- Adding "do not invoke unless asked by name" to skill descriptions to prevent unwanted automatic invocations.
- Running cloud code from coordination repos with additional directories rather than navigating into individual repos directly.
- Creating worktrees per task or branch using a workspace based on the task name.
- Pruning tool results from context after final answers when queries are cheap to rerun later.
- Using sim links between open source and closed source repos to fake monorepo ergonomics painlessly.
- Spending heavy thinking tokens before writing code rather than prompting features into existence prematurely always.
- Throwing away wrongly designed code entirely rather than iteratively patching foundationally broken implementations with LLMs.
- Reviewing code in a separate Claude Code context window before shipping pull requests consistently.
- Standardizing team workflows aggressively rather than supporting seven half baked individual approaches across engineers.
- Bundling reference files inside skills directories for progressive disclosure rather than front loading everything.
- Setting disable model invocation true on skills meant only for explicit slash command invocation.
- Avoiding git submodules entirely when configuring multi-repo agent workspaces because models navigate them poorly.

### FACTS
- Claude Code injects skill instructions as user messages, getting higher attention than tool result responses do.
- Tool search activates automatically once installed skill or tool descriptions exceed roughly ten thousand context tokens.
- Cloud Code historically used a "task" tool for sub agents which was renamed to "agent" recently.
- Amazon implemented a policy requiring senior engineer review for AI generated code from L1 to L3 engineers.
- Anthropic Max plan reportedly delivers around three thousand dollars of inference for two hundred dollars monthly.
- HubSpot MCP server exposes so many tools that installing it can break Claude Code productivity entirely.
- Settings.local.json is excluded from git commits while project level cloud configs are checked in normally.
- Cloud Agent SDK wraps the Claude Code binary directly, inheriting identical inference behavior with proper flags.
- Some founders building SaaS products on Cloud Agent SDK using Max plan triggered Anthropic terms updates.
- Theo released an open code competitor that excludes cloud code due to behavioral control concerns.
- Skills support a references subdirectory convention for bundling supplementary files alongside the main skill markdown.
- Custom sub agents must live in the root claude directory of the running directory, not nested paths.
- Cloud MD file injection happens automatically per project, with separate user level configuration in tilde claude.
- General purpose sub agents inherit standard read, write, edit, and bash tools by default automatically.
- MCP servers exposing 27 tools each cause every tool description to load into the context window.

### REFERENCES
- Human Layer (Dex's company solving complex codebase problems with coding agents)
- Boundary / BAML (Vibhav's programming language for agents)
- Claude Code by Anthropic
- Codex
- Open Code
- OpenClaw
- Cursor
- Riptide (workflow orchestration)
- Conductor (workflow orchestration)
- Tariq on the Claude Code team (Twitter source for disable_model_invocation tip)
- Kyle (Dex's co-founder)
- Bob's tweet about lights off software factories
- Dax's post about shipping too much AI generated code
- Jeff (inspiration for moo-like-a-cow context check)
- HumanLayer RPI commands (open source)
- Human Layer RPI coordination template repo
- Amazon internal AI code review policy news
- Theo's open code competitor product
- AI That Works podcast (Dex and Vibhav's show)
- HubSpot MCP server (cautionary example)
- Sentry (referenced in skill examples)
- Drizzle (migration rebasing skill)
- Playwright (sub agent example)

### ONE-SENTENCE TAKEAWAY
Separate context isolation from instruction modules; design carefully, review humans-in-the-loop, never outsource thinking entirely.

### RECOMMENDATIONS
- Use sub agents only for context isolation tasks, not for bundling reusable instructions across workflows ever.
- Replace persona based sub agents like backend engineer with skills invoked dynamically from any context.
- Fork Claude Code sessions from earlier user messages instead of letting bad exploration paths persist.
- Adopt monorepos when feasible; otherwise build coordination repos with additional directories permissions for agents.
- Avoid git submodules in agent driven workspaces because models cannot navigate them ergonomically reliably.
- Sim link related repos together when monorepos are organizationally impossible to ease agent navigation significantly.
- Add "do not invoke unless asked by name" to descriptions for skills you want explicit invocation only.
- Set disable_model_invocation true for skills meant exclusively as slash commands hidden from automatic selection.
- Bundle long instructions inside skill reference files for progressive disclosure keeping descriptions short and budget friendly.
- Audit installed MCP servers and skills regularly; remove anything inflating tool descriptions beyond useful threshold.
- Run a separate Claude Code review pass before shipping PRs catching common antipatterns the writer missed.
- Spend heavy thinking tokens designing features before letting agents generate code parallel to bad foundations.
- Throw away wrongly designed code entirely rather than asking LLMs to patch broken architectural decisions iteratively.
- Standardize team workflows prescriptively to lift median productivity over supporting individual half baked approaches everywhere.
- Use additional directories settings in cloud config to enable cross repo reads from coordination root sessions.
- Create per task worktrees inside coordination repos so research and writing live in separate clean checkouts.
- Avoid using Max plan inference inside competitor harnesses like open code or open claw to comply terms.
- Keep slash commands minimal wrappers; if it just runs a CLI, prompt the CLI directly instead now.
- Prune tool result tokens aggressively after final answers when underlying queries can rerun cheaply when needed.
- Treat tool descriptions as advertisements; keep them concise to preserve user instruction following budget meaningfully.
