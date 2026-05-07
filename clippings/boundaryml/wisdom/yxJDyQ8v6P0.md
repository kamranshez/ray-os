---
video_id: yxJDyQ8v6P0
title: "🦄 Building a 12 Factor Agent - EP #4"
url: https://www.youtube.com/watch?v=yxJDyQ8v6P0
channel: BoundaryML
---

### SUMMARY
Vibe (BAML) and Dex (HumanLayer) walk through twelve principles for building production agents, live-coding a TypeScript calculator agent demonstrating tool calls, context ownership, and reasoning.

### IDEAS
- An LLM is essentially a smart goto statement that picks the next code path.
- Agents are just prompts that determine the next step from current state.
- Tool calling is structured output; the model never actually calls anything itself.
- The full prompt includes serialization, instructions, schema, and history, not just system text.
- Owning the loop, switch, and context window is the core engineering work.
- Frameworks hide the prompt; reverse-engineering their prompts is unavoidable at scale.
- Magical AI experiences live at the boundary of what models can consistently do.
- Models will always have a moat-free ceiling; engineering around them differentiates products.
- Unifying execution state and business state simplifies debugging across long-running workflows.
- A context window doubles as a database row for pause-resume async workflows.
- Stateless agents become trivially horizontally scalable like normal stateless functions.
- Errors appended to context windows let the model self-correct on the next iteration.
- Small focused agents with narrow tool sets reliably outperform sprawling generalist agents.
- More engineering effort tightens the agent reliability distribution into a taller, wider curve.
- Meet users where they are: email, Slack, not just chat windows.
- Multiple human-contact intents (clarification, final answer) need distinct tool types.
- Models trained on markdown often output code better in markdown than forced JSON.
- JSON.parse on raw model output is genuinely bad without a tolerant custom parser.
- BAML extracts structured data from unrestricted markdown-like outputs without JSON constraints.
- Reasoning prompts with simple structures (dot-dot-dot) elicit reasoning behavior from non-reasoning models.
- Each token of whitespace, quote, or comma in serialization burdens the model's comprehension.
- XML-like serialization can be dramatically more token-efficient than JSON for context windows.
- Test-driven prompt engineering: assertions on intent and parameters replace brittle eval frameworks.
- Changing serialization format requires re-running tests to confirm behavior preservation.
- Agents decoupled from UX plug into CLI, web hooks, Slack, or email identically.
- Notebook LM team: magic equals models pushed to their boundary, executed consistently.
- Cursor and Claude Code use identical Sonnet models; UX engineering creates the difference.
- Same database, different views: agents differ only in interface and engineering choices.
- MCP feels like an app store for Anthropic-built UIs, not yet beautiful code.
- Helm beat Google's better Kubernetes solutions purely through earlier momentum and adoption.
- Most MCP servers are actually clients running locally that call real remote servers.
- Beautiful code matters; React felt beautiful, LangChain and MCP do not yet.
- The agent loop is just while-not-done with switch on next-step intent.
- Treating humans as one of several specialized tools improves user experience dramatically.
- Switch statement ownership lets you inject summarization, judges, or pauses anywhere.
- The model only knows what you tell it through tokens passed into the context window.
- Larger LLMs as gotos: tool descriptions matter more than which provider trained them.

### INSIGHTS
- Control over the prompt string is the single highest leverage point in agent engineering.
- Statelessness plus context-window-as-state collapses agents into ordinary stateless functions.
- The prompt is everything tokenized and sent, not just the system message developers usually mean.
- Engineering effort, not model selection, defines the reliability distribution of any agent product.
- Tool calling abstractions obscure that models only emit structured tokens others execute.
- Owning the loop unlocks pause-resume, errors-as-context, judges, and async webhooks naturally.
- Unified state simplifies multiplayer-game-like systems where many views render one source of truth.
- Forcing JSON wastes tokens on escapes and constrains the model's natural output distribution.
- Tests asserting intent and parameters give faster, cheaper signals than full LLM-as-judge evals.
- Decoupling agents from interfaces enables identical code across CLI, web, Slack, and email.
- Frameworks should expose control knobs rather than hiding prompt construction behind abstractions.
- Reasoning emerges from minimal structural prompts; prescribed few-shot reasoning is often unnecessary.
- Serialization format choice can shift token count and model comprehension by orders of magnitude.
- Beautiful code in frameworks predicts adoption durability better than feature-completeness or backing.
- Adoption momentum locks protocols in regardless of subsequent superior technical alternatives appearing.

### QUOTES
- "An LLM is really just a really really smart goto statement." — Vibe
- "I actually think the concept of tool use is harmful." — Dex
- "Own the loop. Own the loop. That's it. It's not that hard." — Vibe
- "Every model is a tool calling model." — Dex
- "LLMs are stateless. The only state is basically this context window." — Dex
- "If you don't own the serialization, you're really not making life easy for yourself." — Vibe
- "We just need something that scaffolds everything out for you with some good opinions." — Dex
- "What we need is shadcn for agents." — Dex
- "There's no moat in saying I'm going to use the best model." — Vibe
- "Make a better product anyway. And do that with engineering." — Vibe
- "Don't ask the model to output JSON and JSON.parse it. That is bad." — Vibe
- "The only way to create magical AI experiences is to find the boundary of what models can do." — Dex
- "Chat GPT is the geocities era of AI UX." — Dex
- "Beauty is really important in code, especially for frameworks and systems." — Vibe
- "I don't know what's better, but I know you want to be able to try everything." — Dex
- "When I look at LangChain, it doesn't feel beautiful." — Vibe
- "Cursor versus Claude Code, they're both using Sonnet 3.7. There's no difference." — Vibe
- "The agent is decoupled from the UX so you can plug it into multiple interfaces." — Dex
- "Conceptually the agent's going to figure out the ifs and the logic for me." — Dex
- "MCP is a REST service with a query that says tell me all your other services." — Dex

### HABITS
- Hold weekly live-coding sessions to reveal real engineering tradeoffs publicly with peers.
- Open source every line of code from public sessions for community learning together.
- Run npx baml-cli test on every prompt change to catch regressions immediately.
- Commit after each refactor chapter so diffs reveal exactly what each principle changed.
- Turn on BAML debug logs while iterating to inspect the actual rendered prompt.
- Hide internal reasoning tokens from end users while still letting models reason naturally.
- Add new test cases whenever a model behavior surprises you in development.
- Use solarized terminal themes when ANSI color output matters for tooling readability.
- Write assertions on tool intent and parameters rather than full output strings.
- Serialize context windows as readable formats so humans can debug them visually.
- Decouple agent loops from UX layers from day one of any new project.
- Coin-flip between TypeScript and Python to keep skills sharp across both ecosystems.
- Hackathon with collaborators to seed long-running ideas like the 12-factor framework.
- Never deploy fully automated releases; insist on human approval for liability-bearing actions.
- Survey audiences after each season to tune the next batch of content.

### FACTS
- BAML and HumanLayer are both YC-funded companies founded by Vibe and Dex respectively.
- Vibe was a YC Winter 23 founder before co-creating BAML.
- The 12-factor agent post emerged from a hackathon Vibe and Dex held in October or November.
- LangChain became hyped early but engineering constraints exposed limitations at production scale.
- LangGraph is considered more thought-through than LangChain in agent engineering circles.
- Notebook LM defined magical AI as operating consistently at a model's capability boundary.
- Helm won Kubernetes packaging despite Google later releasing technically superior alternatives.
- GPT-4o handled the calculator agent reasoning while GPT-4o-mini reportedly fails on it.
- O3-mini 2025-01-31 was used live in the demonstration to swap models trivially.
- Most MCP servers run locally as clients calling real remote servers, not actual servers.
- DAG orchestrators like Prefect, Airflow, and Dagster predate agent frameworks structurally.
- LangGraph maintains separate graph state and business state objects, complicating debugging significantly.
- BAML uses a custom unrestricted parser instead of JSON.parse for model outputs.
- AI That Works wrapped season one after four episodes and returned three weeks later.
- BFCL (Berkeley Function Calling Leaderboard) benchmarks BAML extraction performance against alternatives.

### REFERENCES
- 12-Factor Agents blog post by Dex (Dexter)
- BAML by BoundaryML
- HumanLayer
- LangChain
- LangGraph
- CrewAI
- Prefect, Airflow, Dagster (DAG orchestrators)
- Notebook LM team statement on AI magic
- Anthropic SDK and OpenAI SDK
- Model Context Protocol (MCP)
- GPT-4o, GPT-4o-mini, O3-mini
- Helm and Kubernetes ecosystem comparison
- React (cited as example of beautiful code)
- shadcn/ui (analogy for desired agent tooling)
- Berkeley Function Calling Leaderboard (BFCL)
- Cursor and Claude Code (cited as same-model competitors)
- "Goto Considered Harmful" essay
- OpenAI tokenizer web tool
- Luma event signup platform
- AI That Works podcast and YouTube channel

### ONE-SENTENCE TAKEAWAY
Own your prompt, loop, and context window because engineering effort, not model choice, differentiates production agents.

### RECOMMENDATIONS
- Build agents incrementally from existing software rather than greenfield rewrites with frameworks.
- Sprinkle LLM calls into deterministic code at high-leverage points instead of replacing everything wholesale.
- Write the agent loop yourself: a switch, a for loop, and prompt construction.
- Unify execution state and business state to simplify debugging and pause-resume workflows.
- Store context windows in your database so async webhooks can resume long-running agents.
- Append tool errors back into the context window and let the model retry intelligently.
- Keep agents small and focused; expand scope only as engineering and models mature together.
- Decouple your agent from its interface so you can ship CLI, web, and Slack identically.
- Test prompts with assertions on intent and parameters before reaching for LLM-as-judge evals.
- Try multiple serialization formats (JSON, XML, markdown) and measure token counts and accuracy.
- Treat humans as differentiated tool types: clarification requests versus final-answer announcements.
- Prefer markdown code blocks over forced JSON when models must output substantial code.
- Customize reasoning prompts with minimal structure rather than prescribing few-shot reasoning examples.
- Run agent tests after every prompt change to catch behavioral regressions before merge.
- Turn on debug logging during development to inspect the literal prompt being sent.
- Avoid frameworks that hide the final prompt string from your direct inspection and edits.
- Read 12-factor agents post and the linked blog explaining BAML's parser behavior thoroughly.
- Add human approval gates for risky tool calls regardless of agent reliability metrics.
- Build differentiated UX assuming competitors have access to identical underlying foundation models.
- Measure agent quality as a distribution curve and engineer to widen and heighten it.
