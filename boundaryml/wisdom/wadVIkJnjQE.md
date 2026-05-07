---
video_id: wadVIkJnjQE
title: "Understanding Latency:🦄 #39"
url: https://www.youtube.com/watch?v=wadVIkJnjQE
channel: BoundaryML
---

### SUMMARY
Vaibhav (BoundaryML) and Dex (HumanLayer) discuss latency optimization in agentic LLM applications, covering bottlenecks, caching strategies, streaming patterns, and prompt design.

### IDEAS
- Performance engineering hardest problem is identifying where to optimize, not actually making code faster.
- Decouple components aggressively because parallelism becomes possible only after meaningful separation between concerns exists.
- Prefetch LLM requests after user pauses typing for several seconds to mask latency.
- Treat write tools as blocked during prefetch, allowing only idempotent read operations to execute speculatively.
- Going from sixty to thirty seconds barely matters; sixty to ten radically changes user expectations.
- Treat LLM prompts as append-only buffers because changing prefixes blows the provider cache.
- Anthropic skips prompt caching below 1024 tokens, so padding to 1024 sometimes goes faster.
- Fire one cache-warming request first, then parallelize remaining requests sharing that cached prefix afterward.
- Put dynamic schemas after static user context in system message to preserve cache prefix integrity.
- Reasoning tokens you cannot see still count against latency, sometimes seventy percent of total time.
- Reasoning summaries are worse than nothing because they generate additional tokens before output begins.
- Model providers hide reasoning traces partly to prevent competitors from training distilled reasoning models cheaply.
- Latency is mostly about feelings, not actual speed; identical networks serve everyone underneath.
- Stream meaningful semantic chunks rather than tokens; render numbers atomically not digit-by-digit refinement.
- AGUI two-step process: stream JSON first, then generate matching React component to swap in.
- Prefetching breaks when streamed strings remain invalid until completion forces business logic complications.
- Type systems should reflect streaming completeness so frontend code stays simple and deterministic.
- Triplet state problem: present-but-unset, set-to-empty, or absent — streaming creates this mess everywhere.
- Letting Claude write your prompts just regurgitates training data instead of high-leverage customization.
- Replace example JSON with type-system schemas; models understand structured types faster than prose examples.
- Use field aliases to shorten tokens fed to the model while keeping verbose internal code names.
- Reducing four-thousand-token prompts to four hundred provides the single biggest latency win observed.
- Cursor tab complete must stay sub-200ms because slower autocomplete breaks typing flow entirely.
- The semi-async valley of death describes apps where waiting kills productivity but completion isn't fast.
- Show thinking tokens, ghost components, or skeleton UIs to make slow apps feel responsive.
- Windows file copy dialogue jumping zero to sixty percent demonstrates how loaders manipulate user perception.
- Honey and Turbotax fake searching for coupons longer than necessary because users feel better waiting.
- Cache the read tool results when prefetching so subsequent matched requests resolve instantly from memory.
- Lazy invalidation: keep old autocomplete result if user keystrokes still match its prefix path.
- Force LLMs to use chain-of-thought within main prompt to recover reasoning visibility on summary-only providers.
- Reasoning tokens lack safety guardrails; jailbreak DeepSeek by manipulating reasoning before final response.
- Setting reasoning effort to none or minimal can drop response from six seconds to two seconds.
- Use literal common keys at start of tool schema enabling switch statements during streaming.
- A typed array with five sentence elements outputs better than asking for five sentences in prose.
- Latency design is choosing where on the productivity-versus-delegation graph each user task lives.

### INSIGHTS
- Performance optimization is fundamentally a measurement problem disguised as an engineering problem requiring discipline first.
- Perceived latency dominates real latency because feelings drive abandonment thresholds more than actual milliseconds.
- Cache-aware prompt architecture inverts intuitive prompt design, placing static context before dynamic schema definitions.
- Streaming should respect semantic atomicity, not token granularity, because partial values create invalid intermediate states.
- Type systems are compression tools for LLM communication, encoding constraints in fewer tokens than natural language.
- Decoupling generation from rendering enables both parallelism and graceful degradation when components arrive out of order.
- Reasoning tokens have become opaque latency taxes that providers protect as competitive moats against distillation.
- Idempotency boundaries determine which operations can be speculatively prefetched without corrupting user-visible state.
- Letting models write their own prompts collapses customization into training-data echoes lacking specific leverage.
- The biggest latency wins always come from prompt reduction first, optimizations second, infrastructure third.
- Streaming UI patterns trade visible-progress feedback against confusion from invalid intermediate states the user sees.
- Different workflow modes have wildly different latency tolerances, from sub-200ms autocomplete to multi-minute research.

### QUOTES
- "It's actually not about making your code faster. It's about knowing where you want to make your code faster." — Vaibhav
- "If you just let Claude slop out all your prompts, you'll end up with information already in the training set." — Dex
- "The best way you can do for latency is decouple stuff as much as possible." — Vaibhav
- "Think of your LLM prompt as a write-only buffer. It's an append-only array." — Vaibhav
- "Latency isn't actually about making your app faster, only about making your app feel faster." — Vaibhav
- "Feelings are a lot more important than the actual latency." — Vaibhav
- "You're just doing the compute twice in the hope that the user won't change it." — Dex
- "Math is pointless unless it's done." — Vaibhav
- "Autocomplete cannot take one second. It has to be like sub 200 milliseconds." — Dex
- "I'm willing to trade time for higher intelligence." — Dex
- "It's the semi-async valley of death." — Dex
- "Be deterministic about the things that are deterministic, then let the LLM do what the LLM is good at." — Dex
- "Reading the prompt and then just trying to condense out the things that actually matter." — Dex
- "We'll use control flow for control flow." — Dex
- "Auditability is better than latency for them." — Vaibhav

### HABITS
- Always run coding agents with maximum thinking tokens at thirty-two thousand for important tasks.
- Hit stop in ChatGPT and switch to faster auto model when waiting feels excessive.
- Read entire prompts manually to identify and remove redundant tokens before shipping changes.
- Measure SSE streams directly with curl to verify reasoning token counts versus visible output.
- Design tool schemas with a literal common key first to enable streaming switch statements.
- Default coding agents to using max thinking tokens because being wrong wastes more time.
- Multitask during long agent runs by kicking off requests then returning minutes later.
- Inspect cache-hit boundaries deliberately when restructuring prompts rather than trusting intuition about ordering.
- Test streaming behavior at scale to catch fringe stalls happening mid-token in production traffic.
- Prefer type-system schemas over few-shot JSON examples when communicating output structure to models.
- Use ChatGPT only occasionally for deep research tasks that take twenty minutes anyway.
- Verify reasoning token consumption by setting effort to none and comparing output token counts.
- Block all write-tool permissions during prefetch sessions while permitting only safe read operations.
- Maintain Redis caches indexed by event-buffer signatures rather than relying on LLM provider caches.
- Watch for thinking-and-reasoning indicators in Cursor as a deliberate latency-perception design pattern.

### FACTS
- Anthropic does not cache prompts shorter than 1024 tokens at all in production.
- OpenAI Responses API defaults to reasoning enabled, secretly burning tokens you cannot see or control.
- Cursor tab complete operates under a sub-200-millisecond budget to avoid breaking typing flow.
- Going from 4000-token prompts to 400 tokens delivers the largest measurable latency improvement consistently.
- A reasoning model running 1400 reasoning tokens plus 400 output tokens spent seventy percent invisibly.
- Setting reasoning effort to minimal dropped one example from 548 output tokens to 34 tokens.
- That reasoning reduction changed total response time from approximately six seconds to two-point-three seconds.
- Anthropic prompt caching requires explicit cache-control breakpoints rather than automatic content-based caching like OpenAI.
- Go's standard library treats unset environment variables identically to empty strings in os.Getenv calls.
- Electric SQL is an open-source sync engine designed to sit in front of Postgres databases.
- Firebase and Convex implement sync architectures where UIs read from databases rather than polling servers.
- The 12-Factor Agents paper was published in April before Claude Code gained early momentum two months later.
- Honey and TurboTax intentionally extend coupon-search animations beyond technical necessity to improve perceived value.
- Windows file copy dialogues historically jumped from zero to sixty percent before stalling near completion.
- DeepSeek reasoning tokens lack the safety guardrails applied to final response tokens in production.

### REFERENCES
- HumanLayer (Dex's company building tools for coding agents in large codebases)
- BoundaryML (Vaibhav's company making AI more reliable and deterministic)
- Excalidraw (whiteboarding tool used during the recording)
- Electric SQL (open-source Postgres sync engine)
- Firebase, Convex (sync architecture providers)
- Anthropic prompt caching documentation
- OpenAI Responses API documentation
- Cursor (coding IDE referenced for tab complete and reasoning UX)
- Replit (referenced for async wait patterns)
- Claude Code (Anthropic's coding agent)
- Cloud Code SDK / Claude Agent SDK
- 12-Factor Agents paper (Dex, April)
- Manus paper (referenced for tool-call schema placement)
- LangGraph (jokingly disavowed)
- Swix's productivity-versus-delegation diagram
- DeepSeek (referenced for reasoning-token jailbreak example)
- ChatGPT auto mode and reasoning models
- Honey, TurboTax, Gmail, Instagram, YouTube (perceived-latency design examples)
- IDE meme (referenced YC party encounter)

### ONE-SENTENCE TAKEAWAY
Reduce tokens, decouple components, respect cache boundaries, and stream semantically — feelings beat raw speed.

### RECOMMENDATIONS
- Audit your current prompts and aggressively cut tokens before pursuing any infrastructure-level latency optimizations.
- Decouple agent generation from UI rendering so components can stream and parallelize independently.
- Prefetch LLM responses after user pauses, blocking write tools while allowing read operations.
- Place static user context first in system messages and dynamic schemas in subsequent cache blocks.
- Pad small prompts to exceed Anthropic's 1024-token cache threshold when serving repeated traffic.
- Warm shared prefix cache with one request before fanning out parallel requests sharing identical prefixes.
- Stream numbers and structured values atomically; never render partial digits or incomplete units to users.
- Build skeleton placeholders, ghost components, and progress indicators to mask unavoidable waiting periods convincingly.
- Set reasoning effort to none or minimal whenever auditability matters less than user-visible response time.
- Replace few-shot JSON examples with type-system schemas using aliases to compress prompt token counts.
- Stop letting Claude generate your prompts; manually craft high-leverage instructions using domain knowledge yourself.
- Measure SSE streams with curl to detect hidden reasoning-token latency burning seconds invisibly.
- Add a literal common key to tool schemas enabling deterministic switch statements during streaming events.
- Cache event buffers in Redis keyed by request signature for repeatable agentic workflows.
- Design idempotency boundaries explicitly so prefetched operations cannot corrupt persistent user state.
- Use control flow for control flow; reserve agentic loops for genuinely uncertain decision spaces.
- Treat LLM prompts as append-only buffers and never modify prefixes after initial drafting.
- Build hot-swap UI components that upgrade from JSON tables to custom rendering when generation completes.
- Keep autocomplete results as long as user keystrokes match prefix path, discarding when divergence appears.
- Render meaningful semantic chunks like complete recipe ingredients rather than partial tokens streamed live.
