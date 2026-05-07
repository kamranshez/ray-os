---
video_id: z5inaSXkiTU
title: "The Right Way to Give Your AI New Abilities"
url: https://www.youtube.com/watch?v=z5inaSXkiTU
channel: BoundaryML
---

### SUMMARY

Vaibhav and Dexter on AI That Works podcast debate MCP, context engineering, dynamic tool discovery, auth design, and skills versus protocols for agents.

### IDEAS

- MCP behaves all-or-nothing where agents either accept every tool or none whatsoever
- Context windows are zero-sum, so adding tools costs intelligence the agent could otherwise use
- Three competitive alphas exist: better agent performance, distribution, or burnable VC funding
- Long tail tools belong in user-bringable extensions, not first-class application features by default
- Popular MCP usage signals which integrations deserve promotion to first-class engineered support
- GitHub MCP famously consumed sixty thousand tokens just by being loaded into context
- Google Cloud SDKs already discovered tools dynamically before MCP was even invented as concept
- MCP tries replacing SDKs but should instead enable user-extensibility in pre-built agent harnesses
- Every function definition is an instruction competing for the model's limited attention budget
- Tree shaking minifies JavaScript bundles but no equivalent exists for shaving down MCP servers
- Closures over tool schemas let you hide irrelevant parameters based on user authentication state
- The ninety-ninth percentile rule: design defaults assuming most users will not engineer carefully
- Claude Code stopped pushing MCPs and pivoted toward skills because MCP was insufficient
- Skills only function meaningfully when the agent has bash access to execute commands
- Tool search introduces extra round trips compared with keeping common tools always available
- The jagged frontier of model capability extends with both new releases and context engineering
- MCP cannot solve auth because credentials must propagate through chained server invocations
- Plaid-style middleman authentication would be required to make MCP secure across nested servers
- REST endured because headers enabled extension like OAuth without redesigning the underlying protocol
- Protocol bars exceed package bars; MCP fails the protocol bar by needing constant retrofit
- Rich authorization JWTs could let humans deterministically scope agent actions to specific verbs
- GitHub and Stripe lead in fine-grained tokens because granular API auth is genuinely hard work
- Browser agents exist because websites lack programmatic auth, forcing agents to impersonate users wholesale
- Don't pass directories or sources to tools when the system can inject deterministically itself
- Agent harnesses lack platform definitions because they evolve faster than they can codify boundaries
- Vercel's bash sandbox emulation hints at safer ways to give agents executable powers
- Educate users to disable unused MCPs rather than letting them silently degrade their own agent
- Audit highly frequent tools mercilessly for parameter and description bloat that wastes tokens
- The same context rot afflicts CLIs through bash; transport choice doesn't determine context efficiency
- Wrapping MCP with another MCP just leaks how authentication must propagate to every layer
- Open Code calls grep but executes ripgrep underneath, hiding implementation from confused agent
- Reasoning models help build first; optimize prompts for cheap models only after proving usefulness

### INSIGHTS

- Architectural simplicity loses to competitors who context-engineer aggressively for one or five percent gains
- The right MCP use case is user-supplied long tail, not engineering-team-owned core integrations
- Tool design quality matters more than transport protocol for context efficiency outcomes
- Default-to-fail patterns matter when most engineers reach for the easiest available implementation choice
- Determinism beats agent reasoning whenever the surrounding system can inject context without ambiguity
- Protocols must extend gracefully through composition, not require redefinition for each new requirement
- Granular authorization needs deterministic scoping per action, not long-lived broadly-scoped session tokens
- Closures encapsulate user state into tool signatures, removing dimensions the model would otherwise overthink
- Frontier expansion happens twice: through model releases and through deliberate context engineering effort
- Education through application UI prevents users from blaming you for performance they degraded themselves
- Platform ecosystems require stable APIs which fast-moving agent harnesses cannot yet credibly provide
- Trust boundaries collapse when authentication credentials must traverse multiple unaudited intermediate servers
- The bitter lesson cuts both ways: engineering effort compounds alongside frontier model capability gains

### QUOTES

- "MCP's kind of like an all or nothing game. You get the MCP or you don't get the MCP." — Vaibhav
- "In terms of alpha, there's only two alphas in today's world." — Vaibhav
- "MCP does not cause context rot." — Kyle (via Dexter)
- "It's the way you design the tools that is most important more so than the actual protocol." — Dexter
- "Don't use MCP to talk to GitHub. Literally just have Claude code use the GitHub CLI." — Vaibhav
- "Every single function definition in an MCP server is an instruction." — Dexter
- "The minute you add an MCP that you're not trusting, you've consumed a certain amount of the model's intelligence." — Vaibhav
- "Claude is just the laziest engineer out there that just happens to be really fast at typing code." — Vaibhav
- "Don't let users shoot themselves in the foot." — Vaibhav
- "It seems like it's tailored to how you want like the agent to be." — Evan
- "We're RLing the model on a way smaller set of tools." — Vaibhav
- "Skills only work if you have a bash tool." — Dexter
- "Technical purity is not correctness here." — Dexter
- "MCP cannot withstand the test of time because it tries to live up to the bar of a protocol." — Vaibhav
- "REST is so freaking good because we haven't had to extend update it." — Vaibhav
- "MCP is really a poor man's attempt of trying to build an app store-like ecosystem." — Vaibhav
- "Old man yelling at clouds." — Dexter
- "Please don't do fraud." — Vaibhav
- "You have an instruction budget for every model." — Dexter
- "If your customer needs an MCP integration to make it work, go ship the damn thing." — Dexter

### HABITS

- Audit highly frequent tool calls for unnecessary parameters and bloated description text routinely
- Track tool call frequency in agents to know which surfaces deserve careful context engineering
- Use slash context in Claude Code to inspect token consumption across MCPs and skills
- Fight aggressively against adding new tools that only one percent of users genuinely need
- Build OAuth directly into applications rather than forwarding credentials through agent intermediaries
- Show users which MCPs they haven't called recently and suggest temporarily disabling them
- Default to closures over tool functions to inject deterministic state out of the model
- Reach for SDK calls in source code rather than MCP whenever functionality is statically known
- Promote popular user-installed MCPs into first-class engineered integrations once usage trends emerge
- Use bash with CLI tools instead of MCP when context efficiency matters most for performance
- Validate every parameter exposed to a model rather than letting Claude write tools naively
- Visualize the jagged frontier of capability when planning where to invest engineering effort
- Inspect MCP servers using NPX MCP inspector before integrating them into production agents
- Run Tuesday recurring AI conversations to externalize and stress-test architectural beliefs publicly
- Hold quarterly unconferences in San Francisco where attendees vote and present talks day-of

### FACTS

- GitHub MCP server consumes approximately sixty thousand tokens just by being loaded into context
- HubSpot API similarly bloats context, pushing combined GitHub plus HubSpot past one hundred thousand tokens
- Google Cloud SDKs dynamically build function trees at import time by calling schema endpoints
- Boto3 lacks autocomplete by default because all AWS function types are determined at runtime
- Twitter REST in 2011 first abandoned PUT and DELETE methods, simplifying down to GET and POST
- Stripe and GitHub are notable for offering fine-grained scoped API tokens with checkbox permissions
- Plaid acts as authenticated middleman so banking websites never see user banking credentials directly
- JWTs combined with rich authorization specs enable signed one-time agent action approvals
- Vercel released a sandboxed bash emulation environment for safer agent code execution capabilities
- VS Code became powerful through its extension SDK ecosystem, similar to iPhone app store dynamics
- Claude Code's documentation moved from MCP focus toward skills as primary extensibility path
- Open Code routes grep tool calls through ripgrep underneath without exposing the substitution
- April eleventh AI That Works unconference was scheduled live in San Francisco for builders
- The OAuth specification originally required browser-based flows that broke under nested server contexts
- Last quarter's San Francisco unconference hosted approximately forty attendees for audience-driven talks

### REFERENCES

- Boundary (programming language Panel) — Vaibhav's company
- Human Layer — Dexter's company
- AI That Works podcast — weekly Tuesday show
- MCP (Model Context Protocol)
- Claude Code
- LangChain, CrewAI — early agent frameworks with imported tool definitions
- Google Cloud SDK, Boto3 (AWS SDK)
- MCP Inspector (npx mcp-inspector)
- Linear MCP, GitHub MCP, HubSpot MCP, Jira MCP
- Zod (TypeScript schema library)
- Plaid (banking authentication middleman)
- Vercel bash sandbox
- VS Code extensions, iPhone App Store
- OpenCode, Codex
- Open AI O1, O3, GPT-4o mini
- YubiKey, Face ID passkeys
- Rich Authorization Requests (OAuth extension)
- JWT specification
- April 11 AI That Works Unconference, San Francisco

### ONE-SENTENCE TAKEAWAY

Reserve MCP for user-supplied long-tail extensions; engineer first-class tools yourself for everything performance-critical.

### RECOMMENDATIONS

- Use SDKs in source code whenever functionality is statically known to your application
- Reserve MCP for letting end users bring custom integrations to your harness
- Promote popular user-installed MCPs into first-class engineered integrations once trends emerge
- Audit every tool description and parameter for token bloat before shipping to production
- Build closures around tool definitions to inject deterministic context the model shouldn't reason about
- Skip exposing source parameters when the user has authenticated only one viable backend choice
- Implement OAuth directly in your application rather than chaining credentials through MCP servers
- Show users token consumption per MCP and prompt them to disable unused integrations
- Keep frequently-used tools always available rather than hiding them behind tool search lookups
- Optimize prompts for cheap models only after proving the use case on reasoning models
- Use NPX MCP inspector to audit any MCP server before integrating into production agents
- Wrap MCP servers when necessary to filter or whitelist functions before exposing to agents
- Invest in fine-grained scoped API tokens following GitHub and Stripe patterns wherever feasible
- Explore JWT-based rich authorization for deterministic per-action agent approval workflows
- Treat agent platforms like VS Code: define stable extension boundaries before locking in protocols
- Reach for bash plus CLI patterns when context efficiency matters more than security boundaries
- Ship features users need today even when underlying protocols are imperfect technically
- Watch frontier capability expansion in two dimensions: new model releases and your engineering effort
- Run weekly conversations with collaborators to externalize and stress-test architectural beliefs publicly
