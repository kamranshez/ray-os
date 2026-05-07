---
video_id: NMhH5_ju3-I
title: "Human as Tools: 🦄 Ep #8"
url: https://www.youtube.com/watch?v=NMhH5_ju3-I
channel: BoundaryML
---

### SUMMARY
Vaibhav and Dexter from BoundaryML demonstrate human-in-the-loop agent architecture using email, BAML, and twelve-factor agent principles applied to production-grade AI workflows.

### IDEAS
- Building AI agents differs little from software engineering principles refined over the past thirty years.
- Humans become a new software surface area, similar to touchscreens reshaping iPhone and iPad apps.
- Agents over email enable asynchronous interaction patterns where responses may take hours or days.
- Email links historically pulled users back into apps; LLMs let users respond from anywhere naturally.
- Apps where users configure once and then interact externally are increasingly successful with founders.
- Natural language approval increases error rates slightly compared to deterministic button clicks for sensitive actions.
- Anthropic's elicitation API lets agents present users specific deterministic options instead of free text.
- Thread state can be any serializable object, not just OpenAI-style message chains being passed.
- Adding timestamps to UUID filenames dramatically speeds debugging by avoiding endless scrolling through identifiers.
- Storage backend choice between Redis, SQL, file system, or iceberg matters less than persisting thread state.
- The agent inner loop is just prompt, switch statement, code execution, and looping until exit.
- The outer loop returns control to humans whose responses re-enter the inner loop with appended context.
- Safe tools execute inline; scary tools force exit to outer loop for explicit human approval.
- Code-enforced approval requirements make prompt injection mathematically incapable of bypassing human gatekeeping decisions.
- Long-running tools should checkpoint to database and trigger separate workflows rather than spinning indefinitely.
- Workflow systems either store context externally or pass entire context windows back upon completion.
- Mailto links demonstrate state-encoding-in-URL versus database templates as alternative persistence patterns for workflows.
- Treat agent state management exactly as you would build email-based software in regular databases.
- Custom switch statements over structured outputs give you more control than generic tool-call mappings.
- Adding new tools requires only defining another data model the LLM has access to.
- BAML tests let you assert agent intent like request_more_information versus process_refund deterministically.
- Code-level assertions on output structure (length, format) handle cases prompting alone cannot reliably enforce.
- Forking threads per agent enables multi-agent systems without abandoning the unified thread state pattern.
- Unifying execution state with business state creates a single object with multiple specialized views.
- Duplication beats wrong abstractions especially in fast-changing AI where flexibility outweighs DRY principles.
- Multi-agent black-box frameworks prevent stopping loops mid-execution which kills your debugging and observability.
- Most developers don't write multi-threaded code, so high-quality single-loop agents serve ninety-five percent of needs.
- LLMs are functions taking input and returning typed output; treat them as implementation details.
- Magic happens when LLMs convert unstructured data into JSON your existing code can consume.
- Sprinkle LLM capabilities into existing software rather than rebuilding from scratch as agent systems.
- Successful AI founders making six figures plus ship code that's mostly traditional software with sprinkled AI.
- Human approval flips the workflow so agents work in background and surface only when needed.
- Trust in agent autonomy grows over time, mirroring the gradual acceptance of mobile check deposits.
- Threshold-based approvals (refund over ten dollars needs manager) create graduated trust models for risky actions.
- Communicating with humans through Slack, email, Discord, Teams should be commodity infrastructure nobody rewrites.
- The agent-to-human protocol should be open source so everyone benefits from shared interface conventions.
- BAML deliberately avoids enforcing chat roles since some LLMs need them and others don't.

### INSIGHTS
- Software has always specialized at edges while keeping cores generic; AI agents follow the same architectural pattern.
- Human-in-the-loop is fundamentally a control flow problem, not an AI problem requiring novel frameworks or vocabulary.
- Owning your agent loop unlocks transitions, observability, and customization that black-box frameworks fundamentally cannot provide you.
- Deterministic code wrapping nondeterministic LLM calls produces guaranteed safety properties impossible through prompting alone reliably.
- Surface area expansion (email, Slack, CLI) lets agents meet users where they are, not vice versa.
- The valuable LLM work happens at the boundary between unstructured input and structured output your code consumes.
- Async agent architectures must serialize state and trigger workflows because humans operate on day-long timescales.
- Trust in autonomous systems builds through demonstrated reliability over time, not through capability improvements alone.
- Treating LLMs as typed functions rather than magical entities lets standard software engineering patterns apply directly.
- Test cases derived from production traces close the feedback loop between observed behavior and prompt iteration.
- Multi-agent systems often add complexity without justification; simpler single-loop designs serve most actual use cases.
- Shipping fast with twenty percent failure beats shipping perfectly nine months later for product iteration speed.

### QUOTES
- "A lot of these principles when building with AI agents are not that different than software engineering principles." (Vaibhav)
- "There's very little AI involved in actually adding a human in the loop." (Vaibhav)
- "Software is all about surface areas." (Vaibhav)
- "I build all my agents to work over email." (Dexter)
- "It's only valuable in that synchronous use case." (Dexter)
- "It gives you a way to deploy your software to where your users already are." (Dexter)
- "We increase our error rate a little bit by giving the user the convenience of responding in natural language." (Vaibhav)
- "The fact that it's an AI is just an implementation detail." (Vaibhav)
- "I just exit to a database." (Vaibhav)
- "There's no prompt injection ever possible that breaks that." (Vaibhav)
- "Duplication is better than the wrong abstraction." (Dexter quoting Ruby community)
- "Code you own is better than code you don't own." (Vaibhav)
- "If the only benefit you're getting is just running the while loop, just write the damn while loop." (Dexter)
- "LLMs are just functions." (Vaibhav)
- "The number one concept that LLMs are really good at is turning unstructured data into JSON." (Vaibhav)
- "The best LLM apps are mostly just code anyway." (Vaibhav)
- "It might be better to ship in two days with twenty percent failure rate than nine months perfectly." (Vaibhav)
- "You should build an object that you control and create different views into it." (Dexter)
- "We're trying to give you a canvas to paint on." (Dexter)
- "Type systems usually solve most problems." (Dexter)

### HABITS
- Use trivially simple toy tools like add and divide for unambiguous demonstrations of agent behavior.
- Build all agents to work over email as the most asynchronous interface possible to design.
- Add human-readable timestamps to UUID-based filenames so debugging finds latest threads instantly without scrolling.
- Store thread state as both JSON source-of-truth and human-readable text serializations side by side.
- Maintain control over the inner loop so prompt iteration directly determines accuracy and value delivered.
- Serialize agent state to database and trigger separate workflows for any long-running or human-dependent task.
- Write deterministic code assertions checking LLM output structure rather than relying on prompt instructions alone.
- Convert observed production traces directly into BAML test cases asserting expected agent intents and behavior.
- Sprinkle LLM capabilities into existing software incrementally rather than rebuilding entire products as agents from scratch.
- Use threshold-based human approvals so trivial actions auto-approve while risky ones require explicit clicks.
- Build canvases not frameworks so users can paint custom logic at the most important boundaries.
- Run BAML tests during development to verify intent classification stays correct across prompt and model changes.
- Fork threads per sub-agent in multi-agent systems while keeping unified state object pattern intact.
- Default to file system or simplest backing store first, then upgrade to Redis or SQL only when needed.
- Prefer code duplication over premature abstractions especially when LLM tooling and patterns evolve weekly.

### FACTS
- Slack runs as an Electron app consuming approximately seventy gigabytes of RAM in typical user installations.
- Anthropic published a Model Context Protocol specification including an elicitation API for structured user prompts.
- The twelve-factor agents framework documents principles like unifying execution state with business state explicitly.
- Go programming language was designed around channels for fast easy data passing between concurrent threads.
- Mailto links can pre-fill subject and body fields encoded directly in the URL without database storage.
- AWS SQS and similar workflow systems support pausing execution and resuming via webhook callbacks asynchronously.
- Temporal and Cadence are workflow orchestration tools supporting checkpointing and resuming long-running jobs reliably.
- LangGraph offers checkpointing capabilities for agent workflows but couples developers to its specific framework abstractions.
- Credit card companies historically texted approval requests for every swipe before adopting threshold-based notifications.
- Amazon often auto-approves small refunds without manual review because investigating costs more than the refund value.
- BAML treats LLM calls as functions returning union types, ignoring underlying chat role conventions entirely deliberately.
- Person-on-events mode in PostHog reflects property values at ingestion time, not the person's current value.
- Human Layer is open source software for managing human-in-the-loop interactions across Slack, email, and Teams.
- Dexter's email agent uses Gmail webhooks delivering conversation.created objects containing from, to, subject, message fields.
- The twelve-factor agents methodology was developed and published openly by Dexter at Human Layer for community use.

### REFERENCES
- BAML (BoundaryML's prompt language and framework)
- Twelve-Factor Agents (https://github.com/humanlayer/12-factor-agents)
- Human Layer (https://humanlayer.dev)
- Anthropic Model Context Protocol (MCP) and elicitation API
- LangGraph
- Temporal and Cadence workflow engines
- AWS SQS
- Vercel AI SDK
- Gmail API and webhooks
- Slack API
- Microsoft Teams
- Discord
- Redis, SQL, Iceberg cold storage
- Go programming language channels
- The Ruby community quote: "Duplication is better than the wrong abstraction"
- VS Code, Cursor IDE
- AI That Works podcast (Episode 8)
- Vaibhav Gupta and Dexter Horthy as hosts

### ONE-SENTENCE TAKEAWAY
Treat humans as just another asynchronous tool, owning the loop yourself with deterministic code-enforced safety boundaries.

### RECOMMENDATIONS
- Build your first agent over email to force asynchronous design thinking from day one of development.
- Define an explicit thread object you fully own rather than passing OpenAI-formatted message chains around.
- Use deterministic switch statements over structured output, not generic tool-call dispatchers from frameworks you don't own.
- Add timestamp prefixes to UUID-based debug files so finding the latest thread takes zero search time.
- Serialize agent state to database before any long-running tool, then trigger separate completion workflows asynchronously.
- Enforce sensitive tool approvals in code, never trusting prompts to prevent destructive actions like refunds reliably.
- Convert real production agent traces directly into BAML test cases for fast prompt iteration cycles afterward.
- Add code-level assertions on LLM output structure rather than relying on prompt instructions to enforce constraints.
- Use threshold-based approval flows so cheap actions auto-execute and only expensive ones require explicit human clicks.
- Start with file system storage before reaching for Redis or SQL backends in your initial agent prototypes.
- Sprinkle LLM JSON conversion into existing apps rather than rewriting your product as a multi-agent rebuild.
- Default to single-loop agents unless you have explicit need and capacity for multi-threaded coordination complexity.
- Watch the twelve-factor agents talks before designing any production AI system relying on long-running workflows.
- Ship with twenty percent failure rate in two days rather than perfecting for nine months without feedback.
- Build your own observability and debug UIs since framework-provided ones rarely match your specific debugging needs.
- Treat the LLM call as one typed function inside otherwise normal software, not the architectural center.
- Adopt Human Layer or similar SDKs to avoid rebuilding Slack, email, and Teams notification plumbing yourself.
- Fork threads per sub-agent rather than building separate state systems when expanding to multi-agent designs.
- Create graduated trust models that loosen approval requirements as the agent demonstrates reliability over time.
- Demo your agents with toy tools like add and divide so observers can clearly see architectural patterns.
