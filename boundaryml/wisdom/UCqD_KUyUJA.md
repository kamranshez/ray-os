---
video_id: UCqD_KUyUJA
title: "Voice Agents and Supervisor Threading - 🦄 #21"
url: https://www.youtube.com/watch?v=UCqD_KUyUJA
channel: BoundaryML
---

### SUMMARY

Vivov (BAML) and Dex (Human Layer) discuss building production voice agents using speech-to-text pipelines, supervisor threading, latency hiding, and conversation evaluation strategies.

### IDEAS

- Voice agents operate on continuous timelines unlike chatbots which exist in discrete message turns
- Speech-to-speech models lack consistency for structured generation, tool calling, and prompt context engineering
- Building pipelines beats single-platform voice solutions because no platform optimizes every component well
- Interrupts are not optional design decisions in voice agents but the primary architectural mechanism
- Voice agents have no UX modality beyond audio meaning loading spinners and graying text are unavailable
- Latency hiding works by speaking pre-recorded filler phrases before LLM tokens actually start streaming back
- Instagram pioneered optimistic uploads starting transfers before users confirmed publishing the photo
- A four-second filler phrase like "let me take a look" buys generous LLM thinking time naturally
- Semantic voice activity detection beats waveform detection for distinguishing speech from background slamming doors
- End-of-utterance models matter because pauses for thinking shouldn't trigger premature LLM agent responses
- Run multiple parallel LLM calls fired at every semantic chunk and discard ones that become irrelevant
- Support agents should err cautious not aggressive because interrupting customers feels worse than waiting briefly
- Supervisor agents inject placeholder messages like "sorry, I may have gone off track" while reasoning
- Use small fast models like GPT-OSS on Cerebras for main flow and slower thinky models for supervision
- Don't prompt-engineer supervisor agents heavily because throwing larger models at them solves quality cheaply
- Build text mode for voice agents because debugging voice-only systems is brutally hard otherwise
- Run supervisor on intervals or critical pipeline stages, not every message, to control runaway costs
- Multiple specialized validators beat one monolithic supervisor agent for compliance, typos, and email validation
- Think of supervisor as workflow over conversation snapshots producing structured state outputs
- Form-filling agents naturally compact context by replacing previous messages with current form state
- Conversation checkpoints at meaningful tool calls let you revert state when things go horribly wrong
- Phased prompts for different conversation stages outperform monolithic prompts spanning entire interactions
- Tell users when conversations get long that response times will increase rather than degrade silently
- Plot conversation timelines colored by on-track versus off-track status to find optimization targets
- Vibes matter as much as accuracy because friend-like personality emerges from copying user's actual communications
- Time-to-market platforms cost accuracy meaning critical-business voice agents justify custom pipeline builds
- Real conversation data of 100+ samples beats vibes-based debugging from listening to two calls
- Classify rules in parallel small-LLM calls instead of one giant prompt asking ten questions
- Stateful bidirectional WebRTC for speech-to-speech models scales worse and recovers worse than text pipelines
- Old phone trees handle obscenity routing with keywords and that pattern still works for modern voice agents

### INSIGHTS

- Voice agents fail when designers treat them like chatbots ignoring time as fundamental design substrate
- Latency hiding through pre-recorded filler creates illusion of intelligence faster than real intelligence
- Platforms trade accuracy for speed of integration which kills business-critical applications dependent on quality
- Supervisor threading externalizes conversation governance so main agents stay fast while quality stays high
- Specialization beats generalization in agent design through parallel small-purpose validators over monolithic supervisors
- Cost optimization comes last after latency, accuracy, and vibes have proven the system works
- Checkpointing creates recoverable conversation states letting agents gracefully degrade instead of catastrophically derailing
- Compaction emerges naturally from form filling because state representation replaces conversation history elegantly
- Eval quality determines voice agent success more than prompt engineering or model selection ever does
- Transparency with users about system limitations builds tolerance better than pretending limitations don't exist
- Background validation threads enable course correction without sacrificing main conversation responsiveness or fluidity
- Personality and vibes correlate with interruption handling more than with text-to-speech voice quality
- Engineering teams need conversation timeline dashboards because skipping inactive periods reveals actionable signal patterns
- Production AI systems require multiple cooperating models each optimized for different speed-accuracy-cost tradeoffs

### QUOTES

- "Voice agents are weird and the first weirdest thing is that they operate on a timeline" — Vivov
- "In voice agents interrupts are not optional to design around. They are the primary design mechanism" — Vivov
- "Speech to speech models are just not good. You can't do this yet" — Vivov
- "You can't context engineer them at all because they're receiving audio tokens" — Kyle
- "The trick to having better latency is literally to start speaking before the LM starts generating tokens" — Vivov
- "Sure let me take a look is like a four second utterance" — Vivov
- "While you're right, we could do a background test, but we want to minimize interruptions from the agent side" — Vivov
- "We basically do our best not to spend a lot of time prompt engineering this" — Dex
- "I had to name the assistant Tony because the model went and like Claude Code started continuing the conversation" — Dex
- "If time to market comes at the cost of accuracy, for almost everything else it's just not worth it" — Vivov
- "Vibes are really good when you're listening to one or two conversations" — Vivov
- "The most useful part in those screen recordings is actually not the screen recording" — Vivov
- "This part of your pipeline is your secret sauce. This is the secret sauce for every single voice agent" — Vivov
- "You're basically building out a state machine and there's all these different transitions" — Dex
- "If you build on one specific platform like you're going to get cooked" — Kyle

### HABITS

- Build text-only debug modes alongside voice modes because voice-only debugging hides too much state
- Run supervisor agents on fixed cadences not every message to control runaway operational costs
- Use small fast models for main conversation flow and bigger thinky models for background supervision
- Plot conversation timelines with color coding showing on-track versus off-track segments over time
- Track KPI of percentage time supervisor spent on-task versus off-task across customer conversations
- Add transparency messages telling users when latency will increase rather than degrading silently
- Default to cautious agent behavior over aggressive behavior in support and sales conversation scenarios
- Send LLM calls speculatively at every semantic chunk and abort when newer chunks supersede them
- Pre-record common filler phrases like "let me take a look" to mask first-token latency
- Build dashboards showing snapshot moments when conversation state flips from green to red
- Wait for others to prove emerging tech works before investing build time in fragile platforms
- Use semantic VAD models from Hugging Face or LiveKit instead of waveform-based detection systems
- Modify main agent prompts based on supervisor-flagged failure patterns observed across real conversations
- Build form-filling agents to compact context by replacing message history with structured state
- Skip inactive periods in recordings to find actionable conversation events worth optimizing against

### FACTS

- GPT-4 real-time and Gemini real-time speech-to-speech models cost roughly an order of magnitude more than text models
- WebRTC and WebSockets are required for stateful bidirectional speech-to-speech model communication patterns
- Cerebras provides one of the fastest time-to-first-token inference speeds available in the LLM market
- OpenAI recently introduced semantic voice activity detection beyond traditional waveform-based audio analysis
- LiveKit offers off-the-shelf semantic end-of-utterance models that handle pauses and thinking gaps reliably
- Deepgram streaming transcription marks user-finished events but unreliably enough to harm production user experience
- Instagram historically uploaded selected images to backend before users confirmed publishing then discarded unpublished
- A 12B parameter model running on Cerebras handles voice agent main conversation flow without latency tricks
- GPT-5 serves as the supervisor model in the demo because slower thinking is acceptable in background threads
- 95% accuracy in end-of-utterance detection still produces noticeably bad user experience in production voice agents
- BAML supports turning logs on and off mid-execution for debugging voice agent context windows
- Dex's demo voice agent supervisor checks rules like email-before-booking and dog-only boarding policies
- Speech-to-speech models separate audio tokens into semantics then regenerate tokens making prompts opaque black boxes
- PostHog session recordings include skip-inactivity features that surface meaningful events from hours of footage

### REFERENCES

- BAML (Vivov's company)
- Human Layer (Dex's company)
- AI That Works (the show itself)
- Cerebras (inference platform powering the small voice model)
- GPT-OSS (12B small model used for main agent)
- GPT-5 (supervisor model)
- GPT-4 real-time, Gemini real-time (speech-to-speech models criticized)
- LiveKit (semantic VAD and EOU models)
- Deepgram (streaming transcription)
- Hugging Face (open-source EOU models)
- Claude Code (referenced via Tony naming anecdote)
- PostHog (session recording reference)
- Instagram (latency-hiding upload anecdote)
- Cursor (latency hiding speculation)
- Previous AI That Works episode on interruptible agents

### ONE-SENTENCE TAKEAWAY

Voice agents win through pipeline composition, latency hiding, supervisor threading, and ruthless conversation timeline observability practices.

### RECOMMENDATIONS

- Build voice pipelines from speech-to-text, LLM, and text-to-speech components rather than using speech-to-speech models
- Speak pre-recorded filler phrases before LLM token generation starts to mask first-token latency cleanly
- Run a background supervisor agent on conversation snapshots to detect off-track state and inject corrections
- Use small fast models like Cerebras-hosted GPT-OSS for the main agent conversation flow
- Use bigger slower models like GPT-5 for supervisor agents where throughput matters less than judgment
- Implement semantic voice activity detection from LiveKit or Hugging Face instead of basic waveform-based detection
- Fire speculative LLM calls at every semantic chunk and abort obsolete ones when newer chunks supersede
- Build a text-mode debugging interface alongside voice mode because pure voice debugging is impossibly slow
- Run supervisors on fixed cadences or critical pipeline stages instead of every single agent message
- Spawn multiple specialized validator agents for compliance, typos, and emails rather than one monolithic supervisor
- Plot a colored conversation timeline showing on-track green and off-track red segments for each call
- Track percentage time on-task as primary KPI for voice agent quality across customer conversations
- Add transparency messages warning users when conversation length will increase response latency going forward
- Use form-filling agents to compact long conversations by replacing history with structured form state
- Establish conversation checkpoints at meaningful tool calls so you can recover from catastrophic state derailment
- Phase prompts for different conversation stages instead of one monolithic prompt spanning all interactions
- Modify main agent prompts based on supervisor-flagged failure patterns from real production conversation data
- Wait until you have 100+ real customer conversations before optimizing prompts based on listened vibes
- Default to cautious agent behavior in support and sales contexts to avoid interrupting your own customers
- Don't prompt-engineer supervisors heavily because throwing larger models at them solves quality more cheaply
