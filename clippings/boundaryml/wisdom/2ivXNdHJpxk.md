---
video_id: 2ivXNdHJpxk
title: "Interruptible agents: 🦄 #19"
url: https://www.youtube.com/watch?v=2ivXNdHJpxk
channel: BoundaryML
---

### SUMMARY
Vaibhav (BAML) and Dex (HumanLayer) discuss building interruptible agents that can be safely cancelled and resteered without losing prior work or context.

### IDEAS
- Frameworks save scaffolding time but fight you when reaching into black boxes to customize internal flows.
- Owning the flow yourself is feasible because AI coding agents can implement complex orchestration from architectural diagrams.
- The best agent products today reinvented UX rather than just wrapping LLMs in conventional chat interfaces.
- Cursor's syntax-highlighted inline diffs reinvented code review UX, while Claude Code reinvented terminal queuing UX.
- Rich approval contexts matter: reviewing emails differs from labeling images or approving loan applications visually.
- State machines work well for agents because LLMs reason cleanly about clear boundaries and transitions.
- Mermaid diagrams in chat let humans review architecture quickly versus parsing 300 lines of markdown.
- Inner loop versus outer loop distinction: tool-calling continues internally; humans live in the slower outer loop.
- The runtime should check for queued messages on every meaningful boundary inside the agent execution loop.
- Replanning on interrupt should rewind to an earlier phase rather than continuing forward with stale plans.
- Markdown syntax embedded in code can render as visual diagrams with click-through navigation between views.
- Graph code benefits without graph-code overhead: write linear code that auto-renders as architectural diagrams.
- Warp's "topic changed, new conversation?" prompt shows context-aware UX for handling subject shifts gracefully.
- OpenAI's Responses API moves tool execution server-side, eliminating client roundtrips for web search loops.
- Forcing a required tool call ensures the model performs the search rather than hallucinating an answer.
- Asking GPT to expand one query into 5-20 related queries broadens research scope catching wrong assumptions.

### INSIGHTS
- The hardest part of interruptible agents is system design around race conditions, not the LLM calls themselves.
- True UX innovation in AI comes from owning information flow, not stacking abstractions over model providers.
- Queueing systems need urgency tiers because not all user corrections deserve the same injection latency.
- Voice agents require dual-model architectures: fast responder plus slow supervisor with a one-message lookback.
- State must live in shared storage when multiple threads coordinate, even if that storage is just memory.
- Conversation IDs must flow bidirectionally from the first response so queued messages can route correctly.
- Inner loops handle tool calling autonomously; transitioning back to the outer loop requires explicit human handoff signals.
- Polling and threading interrupt strategies are complementary patterns, not mutually exclusive architectural choices.
- Frameworks become liabilities when their internals don't expose hooks for the customization you actually need.
- LLMs can implement complex orchestration directly from mermaid diagrams given clear architectural prompts and constraints.
- Drift-detection supervisors can resteer agents by appending corrective context instead of restarting from scratch.
- The best AI product moats are UX innovations that competitors can't replicate without rebuilding underlying flows.
- Visual representations of agent architecture catch errors faster than reading equivalent prose specifications.

### QUOTES
- "If you make a workflow so it can be cleanly and safely cancelled anywhere and still resumed then you are probably building a product that is in the 99th percentile." — Dex
- "Interruptability is a way to take the next level of human in the loop." — Dex
- "You can't actually build interruptible agents without doing some kind of state sharing across threads." — Vaibhav
- "Ready ≠ healthy — runtime errors only show under traffic." — Dex paraphrased
- "Claude Code does this exact thing — the first message emitted from the backend to the frontend is a JSON object that gives you the session ID." — Dex
- "Inner loop versus outer loop — outer loop is anything that requires a human to be in the loop." — Dex
- "What makes the best agents today successful is that almost every single one of them has reinvented UX in some way." — Vaibhav
- "If you want to build incredible experiences, I think you're going to want that control." — Dex
- "Building is not as hard anymore because we have AI agents that help you write some of this code." — Vaibhav
- "Naming is not my strength. I use LLMs." — Vaibhav
- "Cued messages can be inserted that won't mess up a tool call in flow." — Dex
- "You can actually run both things in parallel." — Vaibhav
- "We're touring complete now." — Vaibhav
- "I have been waiting half of my life by years for Half-Life 3 to come out." — Dex
- "The model is required to use the tool call along the way." — Vaibhav

### HABITS
- Run agent loops on threads from the start to enable interruption capabilities later without painful refactoring.
- Always emit conversation IDs as the first event from backend to frontend for traceability.
- Save user messages locally before sending so the user can recover if queueing fails server-side.
- Stream events after every single LLM call to keep the user oriented during long-running tasks.
- Use whisperflow or superwhisper for voice input when prompting agents with rich architectural context.
- Take screenshots of whiteboard diagrams and paste into ChatGPT or Claude for mermaid conversion.
- Ask the model for theoretical guidance first before requesting implementation code on architectural problems.
- Specify "no web service, in-memory only" when prompting models that default to web architecture.
- Print queued message content explicitly so users see corrections were received and merged into context.
- Test prompts with single example queries before running them in full agent pipelines.
- Use markdown headers in code as semantic boundaries that documentation tools can render visually.
- Default to live coding from architectural diagrams during livestreams to demonstrate real engineering tradeoffs.

### FACTS
- Wombat poop is square due to anatomical features in their digestive tract producing cube-shaped feces.
- Woodpecker tongues wrap around the back of their skulls and can extend significantly beyond the beak.
- Claude Code emits session IDs as the first JSON event from backend to frontend on every conversation.
- OpenAI's Responses API executes tool calls server-side, returning final outputs without client roundtrips.
- Warp terminal detects topic shifts and prompts users to start new conversations automatically.
- The 12-factor agents methodology distinguishes inner loop tool calling from outer loop human interaction.
- Cursor reinvented coding UX by showing inline diffs with syntax highlighting at human-approval boundaries.
- Claude Code launched without a free tier yet gained popularity rivaling Cursor through superior queuing UX.
- BAML repository was reduced from 280MB to roughly 170MB through repository optimization work.
- HumanLayer focuses on human-in-the-loop systems for agent approvals and interruptions across channels.
- Mermaid diagrams render inline in some chat providers but not yet in Gemini or ChatGPT.
- The Excalidraw shortcut S changes element colors quickly without opening the menu.

### REFERENCES
- BAML — Vaibhav's structured prompting language and runtime
- HumanLayer — Dex's human-in-the-loop infrastructure for agents
- Claude Code — Anthropic's terminal-based coding agent
- Cursor — AI-powered code editor with rich diff approval UX
- 12-factor agents methodology
- OpenAI Responses API and web search preview tool
- GPT-4o for query planning
- GPT-5 Max in Cursor for implementation
- WhisperFlow and SuperWhisper voice transcription tools
- Warp terminal with topic-change detection
- Mermaid diagrams via mermaid.live
- Excalidraw whiteboard tool
- Half-Life 3 (running joke)
- Minecraft block map generation from code

### ONE-SENTENCE TAKEAWAY
Cleanly interruptible, resumable agents win on UX — own the orchestration flow yourself.

### RECOMMENDATIONS
- Run your agent pipeline in a dedicated thread from day one to enable later interruption.
- Always send a conversation ID as the very first event from backend to frontend.
- Track in-progress state per conversation so new messages queue rather than starting fresh chats.
- Build at least two urgency tiers: immediate-interrupt and inject-at-next-safe-boundary for queued messages.
- Use the race pattern with asyncio.gather to listen on agent thread and message thread simultaneously.
- Sleep one second between queue checks but allow hard interrupts to bypass the polling interval.
- Reset polling intervals dynamically based on agent activity rather than using fixed timers everywhere.
- Force tool calls via tool_choice when the model must perform research instead of hallucinating answers.
- Expand single user queries into 5-20 related searches to broaden research and catch wrong assumptions.
- Print queued messages back to users explicitly when merging them into the active agent context.
- Use mermaid diagrams to communicate architecture to coding agents instead of long markdown specifications.
- Pair fast responder models with slower supervisor models that detect drift one message back.
- Have supervisors inject corrective messages into context rather than restarting agents from scratch.
- Skip frameworks when you need deep customization of agent flow internals and race condition handling.
- Use voice transcription tools to dictate richer architectural prompts than you would type manually.
- Treat agents as state machines with clear transitions because coding agents implement them more reliably.
- Save user messages client-side until acknowledged so failures don't lose user input.
- Show topic-change prompts when new messages diverge significantly from current conversation context.
- Test interrupt behavior at every phase boundary in your pipeline, including mid-tool-call edge cases.
- Visualize agent architecture before writing code so you catch design errors before implementation cost.
