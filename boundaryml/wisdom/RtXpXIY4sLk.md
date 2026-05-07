---
video_id: RtXpXIY4sLk
title: "🦄 Bash vs MCP for Coding Agents: ep #23"
url: https://www.youtube.com/watch?v=RtXpXIY4sLk
channel: BoundaryML
---

### SUMMARY

Dex and Vaibhav debate MCP versus bash for coding agents, exploring context window economics, tool descriptions, token waste, and engineering tradeoffs in agent design.

### IDEAS

- MCP servers function like package management for prompts, bundling tool descriptions developers cannot easily inspect or trim.
- Bloated package size only slows websites slightly, but bloated prompts directly destroy agent accuracy without warning.
- Claude Code renamed its task tool to general-purpose because tool naming materially affects model selection accuracy.
- Every word in MCP tool descriptions and field schemas becomes tokens consumed inside your context window.
- The GitHub MCP server alone can consume sixty thousand tokens before any user message arrives.
- Starting work at sixty percent context usage means you will never get good cloud code results.
- The useful working portion of any context window shrinks dramatically once system prompts and tools are loaded.
- Caching makes identical user messages and tool sets dramatically cheaper because nothing downstream must be recomputed.
- Changing only the user message busts only part of the cache, preserving system prompt and tool definitions.
- Bash trades token bloat for the model needing pretrained knowledge of CLIs like gh.
- Models are extensively trained on the GitHub CLI, making gh commands more reliable than custom MCP servers.
- Engineering effort narrows the distribution of model outputs, raising peak quality in your target domain.
- MCP shines for non-developers who want to connect tools without writing integration code themselves.
- Writing your own MCP servers works because you control and edit the prompts directly.
- Using other people's MCP servers is dangerous because their token costs and prompts remain hidden.
- Linear MCP tool naming like mcp_linear_list_cycles forces models to differentiate via verbose redundant prefixes.
- Browsers render redundant divs invisibly, but LLMs must process every redundant token computationally.
- The CLAUDE.md system message tells Claude to ignore CLAUDE.md unless specifically relevant, deliberately weakening user instructions.
- Anthropic deemphasizes CLAUDE.md inputs because most prompters are unskilled and rogue sentences tank performance.
- Skilled prompters should bypass CLAUDE.md and craft context windows dynamically using slash commands.
- A /ctx slash command can run make tasks that cat curated files into the context dynamically.
- Markdown front matter on files enables programmatic slicing and dicing for context selection.
- Context engineering blends deterministic code with non-deterministic LLM calls at the right boundaries.
- Models are improving so fast that today's forty percent context limit may soon become eighty percent.
- Always test models at their limits because rules of thumb decay rapidly with capability gains.
- Browser-style fifty nested divs cost nothing visually but fifty redundant tokens cost real accuracy.
- Streaming output rate is controlled by the API provider, never the model itself.
- Building reliable applications around single-token streaming chunks creates fragile dependencies on provider behavior.
- DSPy's premise that humans never want to read prompts is fundamentally flawed for the next year.
- Bootstrap failed as a design system because it lacked customizability, predicting prompt framework limitations today.
- ShadCN succeeds by giving full solution-space access with sane defaults instead of artificial interfaces.
- Good agent frameworks must let you reach into the box and customize everything without docs.
- Hierarchy of leverage means workflows used daily deserve heavy engineering investment over experimental MCP plugs.
- Cutting context window usage from seven to one percent cascades into massive team-wide accuracy improvements.
- Images often describe visual problems more efficiently than verbal explanations, especially for non-experts in CSS.
- Multimodal inputs work surprisingly well off the shelf for tasks like extracting structured data from screenshots.
- Writing the agent while loop yourself reveals that frameworks add little fundamental value beyond convenience.
- An MCP loop is just a tool registry, an agent call, and a dispatch on selected tool name.
- Debugging the code generator is slower than debugging the generated code, favoring simple bash scripts.
- The needle-in-haystack benchmark misleads because general performance drops off long before context fills.
- Tool descriptions like list_teams ship sorting and filter parameters consuming tokens for capabilities you never use.
- Reddit demanding multiple required MCP servers leaves a hundred thousand tokens of context already burned.
- Hand-tuning prompts will remain valuable for the next twelve to eighteen months minimum.

### INSIGHTS

- Token cost of tool definitions is the hidden tax that determines whether agents succeed.
- Naming differences between similar tools materially impact selection accuracy, justifying careful taxonomy work upfront.
- Context engineering is fundamentally about choosing which deterministic and non-deterministic boundaries to draw.
- The MCP versus bash debate reduces to who controls the bits entering the context window.
- Frameworks optimize for the eighty percent case, harming skilled users who need full configurability.
- The right abstraction provides sane defaults plus complete customizability, never one without the other.
- Engineering effort narrows performance distributions, sacrificing breadth for height in your target domain.
- Writing the agent loop yourself demystifies frameworks and exposes how little magic actually exists.
- Hidden prompts in third-party MCP servers create unbounded accuracy risks you cannot diagnose.
- Hierarchy of leverage dictates investment: high-frequency workflows deserve hand-tuned prompts over off-the-shelf MCP.
- Model capability gains may eventually erase context-engineering advantages, but not within the foreseeable horizon.
- Image inputs compress complex visual context into fewer tokens than equivalent verbal descriptions often require.
- Production systems should never depend on streaming behavior controlled by external API providers.
- Pretrained knowledge of common CLIs like gh makes bash inherently lower-token than custom integrations.
- Caching mechanics reward stable system prompts and tool sets across iterations of similar tasks.

### QUOTES

- "The more context you use, the worse results you will get across the board no matter what." — Jeff Huntley
- "Slowness is bad, but you can get around it. Accuracy is literally a user quality hit." — Vaibhav
- "Every single word you put into that MCP server is literally making it to the LLM." — Vaibhav
- "I am very happy to use MCP stuff that I have written, very unhappy to use stuff other people have written." — Vaibhav
- "If you load in fifty MCP tools, you are never ever going to get good results from cloud code." — Dex
- "Why do I have to know that I have to list teams? It's totally useless information." — Vaibhav
- "Bash is pretty good when you're using a coding agent, you don't really need more." — Dex
- "If you are using MCP, you don't get to control exactly what bits make it into your context window." — Vaibhav
- "If you're stuck debugging the thing that is generating the code for you, that is a much slower iteration loop." — Vaibhav
- "I just don't think prompts are in a world where eighty percent is good enough." — Vaibhav
- "If you're not using models for image processing, you're hurting yourself." — Vaibhav
- "This is the engineering part. You have to understand how context windows work." — Dex
- "The premise that you will never want to read and edit the prompt manually is fundamentally flawed." — Vaibhav
- "How fast can you know the code is working or not working determines everything." — Vaibhav
- "If you only change parts of it, then you get to reuse parts of the cache." — Dex
- "I would not build any amount of reliability ever in your application that depends on getting one token at a time." — Vaibhav
- "Most people don't know how to write a good CLAUDE.md, and over-steering is more harmful than under-steering." — Dex
- "Push in a hundred thousand tokens and see if it works and does what you want." — Vaibhav
- "We don't want a component library, we want a platform for building component libraries." — Dex
- "Crafting your context window is the bigger picture, and this matters as long as we're on transformer-based LLMs." — Dex

### HABITS

- Run a Docker reverse proxy that captures all Claude traffic and writes structured log files for analysis.
- Keep total context window usage below forty percent before letting the agent start its work.
- Have Claude do one thing, get it right, then start over with a fresh context window.
- Track cache_creation_input_tokens summed across sessions to measure real token usage in workflows.
- Avoid installing any MCP servers personally, defaulting to bash scripts the agent generates on demand.
- Use slash commands like /ctx to dynamically inject context rather than relying on static CLAUDE.md.
- Add YAML markdown front matter to files so context-selection scripts can slice by metadata.
- Pre-print key metrics, recent investor updates, and conversation summaries via cat into context windows.
- Test new models at their performance limits regularly rather than trusting old rules of thumb.
- Write your own agent while loops at least once to demystify framework abstractions.
- Use gh CLI commands instead of GitHub MCP because models are well-trained on it.
- Reach for images when describing visual UI bugs you cannot articulate in CSS terms.
- Allow and disallow specific MCP tools per sub-agent to control which definitions enter context.
- Wrap third-party APIs in custom CLIs that emit dense markdown rather than verbose JSON.
- Stream long tool outputs into ticket.md files so the model reads incrementally rather than entirely.

### FACTS

- Claude Code recently renamed its bash task tool to general-purpose for naming clarity reasons.
- The Linear MCP server adds approximately twelve thousand tokens to a Claude context window when loaded.
- The GitHub MCP server can consume around sixty thousand tokens of context window space.
- A typical Claude system prompt and small CLAUDE.md baseline together consume roughly six thousand tokens.
- Claude's effective working context is roughly one hundred sixty-eight thousand tokens after system overhead.
- Cloud code instructs the model to ignore CLAUDE.md content when not specifically relevant to the task.
- BAML uses an algorithm called SAP that parses malformed JSON outputs reliably across different model providers.
- BAML showed better tool-calling accuracy on GPT-5 than native function calling in their tests.
- MCP communication uses an OpenAPI-spec-like format describing tools as JSON schemas with descriptions.
- Models always generate exactly one token at a time regardless of streaming chunk size delivered.
- Memory MCP server adds approximately ten thousand tokens of context window overhead when installed.
- Claude Opus and Sonnet can both one-shot generating gh CLI commands for common GitHub operations.
- Cloud code's MCP tools get prefixed names like mcp_linear_list_cycles for routing dispatch purposes.
- Cache reuse requires identical user messages and identical sets of allowed tools across calls.
- DSPy and BAML produce best results when combined, according to a recent published study.

### REFERENCES

- BoundaryML AI That Works podcast (episode 23)
- Jeff Huntley (Geoff Huntley) blog post on MCP context costs
- BAML (Boundary's structured output library)
- Claude Code CLI by Anthropic
- Codex CLI by OpenAI
- AMP CLI
- Open Code CLI
- Linear MCP server
- GitHub MCP server
- Memory MCP server
- Reddit MCP requirements
- gh CLI tool
- MCP Inspector (npx tool)
- Manus paper (referenced in earlier caching episode)
- DSPy framework
- Bootstrap CSS framework
- ShadCN component library
- Tailwind CSS
- Replicated (Vaibhav's prior company)
- Streamyard (streaming software used in episode)
- Discord (chat for episode questions)
- BoundaryML Luma calendar for upcoming episodes

### ONE-SENTENCE TAKEAWAY

Engineer your context window deliberately because every MCP token silently degrades your coding agent's accuracy.

### RECOMMENDATIONS

- Audit your current MCP servers and count their token cost using cache_creation_input_tokens in JSON output.
- Replace the GitHub MCP with bash invocations of the gh CLI for most workflows.
- Write custom CLI wrappers around frequently-used APIs that emit dense markdown instead of verbose JSON.
- Keep your effective context window usage below forty percent before letting the agent work.
- Build a /ctx slash command that dynamically injects relevant files instead of static CLAUDE.md.
- Add YAML front matter to your knowledge files so scripts can slice them by metadata.
- Run a Docker reverse proxy capturing Claude traffic to inspect what actually enters your context.
- Disallow unused MCP tools per sub-agent to trim definitions out of the context window.
- Write your own agent while loop once to demystify how frameworks really work underneath.
- Test new models against their context limits regularly rather than relying on stale heuristics.
- Stream long tool outputs to disk files instead of returning them through the model context.
- Use images for visual UI bug descriptions when CSS vocabulary fails you.
- Reuse the exact same user message and tool set when iterating to maximize cache hits.
- Engineer prompts heavily for daily team workflows since one-percent accuracy gains cascade across users.
- Inspect any third-party MCP server's full tool list before installing to evaluate token cost.
- Pair BAML with DSPy for tool calling and structured output rather than choosing one alone.
- Bypass CLAUDE.md for skilled prompting and inject instructions through dynamic slash commands instead.
- Avoid building production reliability around streaming chunk sizes you do not control.
- Combine deterministic context-selection code with non-deterministic LLM calls at clear architectural boundaries.
- Push models to their limits regularly with hundred-thousand-token prompts to discover real performance ceilings.
