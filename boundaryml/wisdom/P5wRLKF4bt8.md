---
video_id: P5wRLKF4bt8
title: "Using MCP server with 10000+ tools: 🦄 Ep #7"
url: https://www.youtube.com/watch?v=P5wRLKF4bt8
channel: BoundaryML
---

### SUMMARY
Vaibhav (BAML) and Dexter (HumanLayer) demonstrate handling 10,000+ MCP tools by narrowing dynamically with embeddings while preserving prompt control and reliability.

### IDEAS
- MCP servers expose only two essential APIs: list tools and call tools.
- Reliability is the hardest engineering problem when scaling AI systems beyond toys.
- Most YC companies do not use MCP in production except for end-user integrations.
- MCP shines when non-coders drop integrations into Claude Desktop or cursor chatbots.
- Adding more tools widens coverage but reduces reliability per individual service path.
- Treating MCP servers as untrusted APIs prevents catastrophic prompt injection security failures.
- Append-only tool actions are safer than read-write actions exposed through MCP servers.
- Static tools offer stronger guarantees than dynamically loaded runtime tools from servers.
- Embedding text should differ from the description text passed into language models.
- A union type lets models pick exactly one structured object from many options.
- Aliasing internal tool names with prefixes prevents collision with arbitrary JSON fields.
- Hybrid systems blending deterministic code, LLM workflows, and MCP cover most scenarios.
- Sequencing tool calls is the developer's responsibility, not the language model's job.
- Sorting or filtering returned actions lets developers enforce business-critical execution ordering.
- Probes at narrowing and selection stages isolate failures into testable, fixable components.
- Lawyers must verify domain-specific tool selections that engineers cannot reasonably evaluate alone.
- Caching the tools list avoids sending megabytes of schema across networks repeatedly.
- Random tool selection still satisfies the narrowing function's signature contract perfectly.
- Models cannot pick correct tools that embedding filters never include in input.
- Open API specs convert cleanly into structured data models for prompt injection.
- Trying a thousand tools first reveals whether sophisticated filtering is genuinely necessary.
- Embedding model choice matters less than what content you feed into them.
- Self-hosting embeddings inside your VPC reduces latency dramatically below network roundtrip times.
- Format your chat history however you want, not just OpenAI's role-based JSON.
- Human message tools handle clarification gracefully when initial queries lack sufficient context.
- The god prompt with all tools breaks at scale just like classification.
- Race conditions in parallel tool calls become app developer concerns, not model concerns.
- Authorization concerns are spec problems, not interesting engineering problems worth dwelling upon.
- Robots.txt analogy shows MCP is just standardized service discovery for agents.
- A hundred tools roughly approaches the practical limit for current frontier models.

### INSIGHTS
- Coverage and reliability sit on opposite ends of the AI software design spectrum.
- Separation of concerns between embedding text and prompt text enables independent optimization.
- Building probes at every pipeline stage transforms opaque failures into isolated, fixable bugs.
- The MCP spec is fundamentally a REST API with two standardized agent endpoints.
- Trust boundaries around external MCP servers mirror traditional third-party API security thinking.
- Deterministic ordering belongs in code when sequence is known ahead of execution.
- Domain experts plus engineers iterating on probe outputs produces reliable specialized agents.
- Application-specific embedding strategies outperform generic descriptions copied straight from tool schemas.
- Hybrid architectures beat either pure deterministic or pure agentic approaches at scale.
- Easy fixes to embedding text should precede expensive embedding model fine-tuning attempts.
- Tool narrowing functions accept any implementation, enabling progressive refinement without architectural rewrites.
- Static plus dynamic tool blending preserves UI integration where reliability matters most.
- Reasoning trace length compounds the cost of poor tool selection at every step.
- Testable systems with hundred-case eval suites beat shooting in the dark.

### QUOTES
- "Unreliability is the hardest thing to deal with." — Vaibhav
- "Everything interesting happens at large scales." — Vaibhav
- "MCP just becomes another layer of SDK." — Vaibhav
- "If you already know what the right order is, you could have just written those five make commands in a bash script." — Dexter
- "There is no oneshot magic trick." — Vaibhav
- "MCP isn't that hard. It's just an API that does list a bunch of tools and let you call that tool." — Vaibhav
- "Don't tie yourself down because different models will have different behaviors." — Vaibhav
- "The MCP server is a black box to your application if you don't own it." — Vaibhav
- "It feels like that magic bullet, but it's not." — Vaibhav
- "Most people make the mistake of saying that I'm going to use this description as the thing that I pass into LLM and also the thing for embeddings. That is a mistake." — Vaibhav
- "If the embedding picked the wrong tool, then there's no way the LM can pick the right one because it's not even in your input." — Vaibhav
- "We live in this hybrid world where some tools are going to be defined dynamically and some tools are going to be defined statically." — Vaibhav
- "It's easier to teach non-engineering people a little bit of AI than it is to teach engineers a lot of business context." — Vaibhav
- "You should view them as the same way as using an API endpoint from anywhere that you don't trust." — Vaibhav
- "More tools is like cool, I'm going to write less code and I'm going to hope the LM can figure it out." — Dexter
- "Embeddings really just aren't that cool. But there are ways now where you can make them fast." — Dexter
- "You do not have to use the standard OpenAI JSON messages format." — Dexter
- "The fastest way to do it was go into the Chrome console and copy the requests and paste those into a model." — Dexter
- "These capabilities come with an unbounded amount of risk." — Vaibhav
- "Probably there are some companies with 10 users that are interesting." — Vaibhav

### HABITS
- Vaibhav builds CLI agents with default human clarification tools baked in from experience.
- Dexter copies Chrome console requests into models when API documentation proves inadequate.
- Caching tools list JSON locally avoids repeated network calls during development iterations.
- Running while-true loops with manual input tests agent behavior interactively before automation.
- Adding progress bars before long batch jobs prevents wasted waiting and frustration.
- Disabling open-mouth excitement, defaulting to subtle smirks, when expressing technical opinions publicly.
- Slicing test data first before running full ten-thousand item embedding generation jobs.
- Hosting small embedding models inside VPC for predictable sub-second response times.
- Aliasing tool name fields with dollar-sign prefixes to prevent JSON namespace collisions.
- Writing test suites with hundred examples to score pipeline changes against baseline performance.
- Filtering and sorting model-returned action lists deterministically before executing them sequentially.
- Building boilerplate code ahead of live demos to focus discussion on interesting parts.
- Polling audiences early in workshops to gauge familiarity with topics before diving deep.
- Keeping prompts simple initially, only adding complexity after measuring real failure modes.
- Treating MCP server descriptions as untrusted strings requiring validation before agent injection.

### FACTS
- Smithery is an MCP registry hosting thousands of community-contributed MCP servers.
- The transcript references 12-Factor Agents methodology for building reliable agentic systems.
- A GitHub MCP exploit was reported creating PRs containing personally identifiable information automatically.
- Roughly 30% of poll respondents currently ship MCP, while 25% never will.
- The example tools.json file contained roughly 11 megabytes spanning 300,000 lines.
- BAML supports both Python and TypeScript codebases for prompt and structured output engineering.
- Vaibhav previously worked on Face ID, hedge fund prediction systems, and Microsoft AR.
- Dexter founded HumanLayer focused on human-in-the-loop async orchestration for agents.
- OpenAI's GPT-4o handles roughly 100 tools effectively in a single tool selection prompt.
- Embedding API calls typically take between 50 milliseconds and 1 second per request.
- Vercel deployment promotion requires specific API invocations not obvious from public documentation.
- The agents.json proposal preceded MCP and is now being absorbed into the standard.
- Robots.txt is a semantic agreement scrapers honor, analogous to MCP for agents.
- BAML's TypeBuilder enables runtime data model construction for dynamically loaded tool schemas.
- AsyncIO gather enables parallel embedding generation using async OpenAI client invocations.

### REFERENCES
- BAML — prompt and structured output framework by BoundaryML
- HumanLayer — Dexter's async orchestration tool
- 12-Factor Agents methodology
- Smithery MCP registry
- Claude Desktop
- Cursor
- GitHub MCP server
- Vercel deployment APIs
- Notion API MCP
- Supabase MCP
- Browser Use / Browserbase
- Linear (PRD ticketing)
- agents.json (alternative proposal to MCP)
- robots.txt convention
- OpenAI embeddings API
- AWS Bedrock for hosted embeddings
- TQDM Python progress bars
- Episode 1: classification with 1000+ categories (BoundaryML series)

### ONE-SENTENCE TAKEAWAY
Narrow tools through testable probes before prompting; MCP is plumbing, not a magic reliability solution.

### RECOMMENDATIONS
- Build a narrow-tools function with a clean signature before optimizing its internal implementation.
- Cache MCP tool schemas locally instead of fetching multi-megabyte payloads on every request.
- Embed application-specific text rather than copying tool descriptions directly into vector representations.
- Add probes at narrowing and selection stages to isolate which component is failing.
- Treat third-party MCP servers as untrusted APIs requiring deterministic validation gateways before invocation.
- Prefer append-only or read-only MCP capabilities when exposing tools to end users.
- Alias internal tool name keys with reserved prefixes to avoid JSON namespace collisions.
- Try passing all thousand tools first to baseline whether filtering meaningfully improves accuracy.
- Self-host small embedding models inside your VPC for predictable low-latency tool retrieval.
- Sort returned action lists deterministically when sequence matters for application correctness.
- Combine static UI-aware tools with dynamic MCP tools to preserve critical user-facing reliability.
- Build a hundred-case test suite before claiming any optimization actually improves pipeline performance.
- Skip MCP entirely for known control flows where five bash commands suffice.
- Use union types to constrain model output to exactly one valid structured tool.
- Pair domain experts with engineers to verify tool selections in specialized industries like law.
- Inject explicit tool ordering instructions only after observing actual selection failures during evaluation.
- Build deterministic confirmation steps before sensitive read actions like accessing bank transactions.
- Filter LLM action arrays before execution to inject safety checks the model omitted.
- Cache embeddings to disk so reruns avoid recomputing identical content during development cycles.
- Slice tool datasets to fifty entries during development before scaling to ten thousand.
- Render request-clarification messages with distinct UI treatment versus regular agent response messages.
