---
video_id: zU8GpxgYDvc
title: "Prompt-Hackers are coming for your data"
url: https://www.youtube.com/watch?v=zU8GpxgYDvc
channel: BoundaryML
---

### SUMMARY
Vaibhav from Boundary and Dex from Human Layer discuss prompt injection defenses, structured outputs, deterministic guardrails, background guardrail agents, and layered security architectures.

### IDEAS
- Prompt injection through Zendesk tickets caused cursor to exfiltrate database contents to attacker URLs.
- The lethal trifecta combines untrusted content, private data access, and external communication capability dangerously.
- A car dealership chatbot once sold a Chevy Tahoe for one dollar legally.
- Structured output with strict validation transforms invalid model responses into deterministic exceptions instead.
- Adding automation to systems makes them faster but exponentially more brittle to single-point failures.
- Toilet paper supply chains failing during COVID exemplifies streamlined automation pipelines breaking catastrophically downstream.
- System prompts protecting model instructions follow stronger than equivalent user message instructions empirically.
- Putting validation constraints in schema prevents prompt injection because models throw parse exceptions reliably.
- Deny lists and allow lists both have tradeoffs but combining both increases overall safety.
- Background guardrail agents inspect streaming context and cancel inference when malicious patterns detected mid-output.
- ChatGPT outperforms OpenAI API on safety because they own the full vertical UX stack.
- Training fast classifiers from guardrail agent outputs achieves sub-10ms safety checks at scale.
- Voice agent latency constraints inspire creative solutions that transfer directly to general agent architectures.
- AI engineering is roughly ninety percent traditional software engineering layered with model inference calls.
- Stacking three layers of injection-detection prompts makes telephone-game attacks practically infeasible for attackers.
- Once attackers have your API access, hiding system prompts becomes wasted defensive engineering effort entirely.
- Cache hierarchy from registers to CDN provides architectural blueprint for layering AI guardrail systems.
- Speed and accuracy form fundamental tradeoff that current models cannot escape simultaneously without engineering.
- Triage queues with human review prevent prompt injections from reaching agents through ticket pipelines.
- Prompt injection's highest value framing is alignment guarantee rather than just leak prevention.
- Building guardrail agents teaches alignment agent design transferable to real production agent systems.
- GPT-4 remains exceptionally vulnerable to gaslighting through manipulated previous assistant message history.
- Coding agents like Claude Code default to broad permissions because constant approval prompts destroy usability.
- Reactive evals built from real user complaints outperform proactive Claude-generated test cases dramatically.
- Smaller models hallucinate schemas more aggressively making structured output validation more critical defensively.
- Network sniffing concerns vanish when inference runs server-side with proxy-friendly enterprise gateway support.
- Image modality inputs make prompt injection detection significantly harder than pure text inputs.
- Iterative prompt injection works by reading model responses and adjusting attacks based on observed behavior.
- Multiple defense layers with seven-dimensional optimization replace one-size-fits-all guardrail thinking entirely.
- Anthropic and OpenAI explicitly publish papers on layered classifier architectures for inference safety.
- Constraints breed creativity which is why voice agents constantly invent novel latency solutions today.
- Substring matching against system prompt content provides dirt-simple deterministic leak prevention regex layer.
- Prior classical machine learning experience accelerates intuition development about transformer behavior under hood.

### INSIGHTS
- Layering security models mirrors traditional software architecture, applying cache and CI/CD patterns to inference.
- Deterministic guardrails preceding probabilistic ones short-circuit obvious attacks before expensive inference cycles execute uselessly.
- Owning the full UX vertical stack enables stronger safety than exposing raw API endpoints externally.
- Speed-accuracy tradeoff resolves by training fast classifiers from slow guardrail agent labeled outputs.
- Alignment and security share architecture because both require keeping agents inside intended behavioral domains.
- Schema validation acts as deterministic guardrail by transforming uncertain model outputs into binary exceptions.
- Defense in depth with stacked classifier layers exhausts attackers via combinatorial complexity of bypasses.
- Background streaming inspection beats sequential gates because latency hides behind already-running inference processes.
- Reactive eval-building from real failures yields better coverage than synthetic test generation upfront.
- Prompt injection severity depends entirely on whether all three lethal-trifecta capabilities exist simultaneously.

### QUOTES
- "Hackers will find a way." - Vaibhav
- "AI engineering is 90% software engineering." - Dex
- "It's just software. How do you build software?" - Vaibhav
- "Your value better not be the system prompt cuz if that is you have no value." - Vaibhav
- "You can't have speed and accuracy at the same time." - Vaibhav
- "Everything in life that's interesting is things with constraints." - Vaibhav
- "GPT-4 will do whatever you want. We don't care about instructions anymore." - Vaibhav
- "Once the inference is happening outside my infrastructure they're just going to have it." - Dex
- "Be more reactive with your evals rather than proactive." - Dex
- "Use your own brain be deliberate about the first 10 test cases." - Dex
- "Evals will slow you down not speed you up in the beginning." - Vaibhav
- "I actually think of prompt injection's highest value as being an alignment value." - Vaibhav
- "You're just shifting it slightly with every single layer." - Vaibhav
- "There's very little invention you have to do in AI." - Vaibhav
- "This is engineering. This is why everyone still has a job." - Vaibhav
- "If you're vibing you just vibe the whole way through." - Vaibhav
- "What models fail is really an art not really a science yet." - Vaibhav

### HABITS
- Run cursor in network-sandboxed environments with whitelisted URLs only for inference calls.
- Manually triage every incoming Linear issue before allowing background agents to access them.
- Build single happy-path yes-case and no-case eval first before scaling test suites.
- Drop user-reported failure data directly into eval suite as new regression test cases.
- Practice prompt injection attacks against own systems regularly to develop empirical intuition.
- Stack multiple layers of injection-detection guardrails when system prompt secrecy is mission-critical.
- Use system messages over user messages when stronger instruction following is required deterministically.
- Test defensive systems against deliberately weaker models like GPT-4 to expose vulnerabilities.
- Block streaming output to frontend until guardrail agent produces at least one validation token.
- Add length-greater-than-zero schema constraints to force exceptions on hallucinated empty fields reliably.
- Read model responses iteratively and adjust prompts based on observed behavior patterns directly.
- Skip writing eval test cases proactively until you understand the actual failure modes empirically.
- Layer deny lists and allow lists together rather than choosing one approach exclusively.
- Run inference server-side and never ship inference clients to untrusted user workstations.
- Cancel streaming inference mid-flight when guardrail agent detects suspicious token patterns appearing.

### FACTS
- A judge ruled the car dealership had to honor the AI's one-dollar Chevy Tahoe sale.
- Simon Willison coined the lethal trifecta concept describing three combined prompt injection prerequisites.
- A public repository collects extracted system prompts from major AI coding agents like Vercel V0.
- OpenAI published a paper detailing fast classifier plus LM-judge layered safety architecture.
- Pliny is a renowned prompt injector who appeared on the Latent Space podcast previously.
- Cache hierarchies typically span registers, L1, L2, DRAM, browser cache, CDN, Redis, database.
- AI That Works Unconference scheduled for April 11th in San Francisco off-the-record Chatham House.
- COVID supply chain failures demonstrated how streamlined automation pipelines fail catastrophically at scale.
- Sub-10ms classifier inference becomes possible after distilling guardrail agent outputs into trained models.
- BAML is a programming language created by Boundary for prompt engineering work specifically.
- Human Layer helps companies solve hard problems in complex legacy codebases with coding agents.
- ChatGPT owns the full vertical stack which OpenAI's responses API increasingly tries to replicate.
- Claude Code system prompt was extracted via inference happening on user workstations directly.
- Two-factor authentication and SSO follow same defense-in-depth philosophy as layered AI guardrails.
- Anthropic's Claude Code defaults to broad permissions to avoid constant user approval friction issues.

### REFERENCES
- Simon Willison's lethal trifecta concept
- Pliny the prompt injector
- Latent Space podcast
- BAML programming language by Boundary
- Human Layer (Dex's company)
- OpenAI responses API
- OpenAI paper on layered safety classifiers
- Supabase MCP
- Linear issue tracking
- Zendesk support tickets
- Cursor AI editor
- Vercel V0
- Lovable
- Claude Code
- OpenAI Codex
- ChatGPT
- GPT-4
- GPT-5
- AI That Works podcast
- AI That Works Unconference (April 11, San Francisco)
- mini GPT (Karpathy)
- Promptfoo eval framework
- JEPA architecture
- Voice agents background supervisor episode

### ONE-SENTENCE TAKEAWAY
Layer deterministic schemas, fast classifiers, and background guardrail agents to balance safety, speed, and alignment.

### RECOMMENDATIONS
- Apply lethal trifecta analysis to every agent system before granting tool access permissions.
- Force structured outputs with strict schema validation to convert injection attempts into parse exceptions.
- Build human triage queues for any ingestion path feeding agents from external untrusted sources.
- Run coding agents in sandboxed networks restricted to inference APIs and trusted documentation domains only.
- Implement background guardrail agents that monitor streaming context and cancel suspicious inference mid-flight.
- Train small fast classifiers from guardrail agent labeled outputs to achieve sub-10ms safety checks.
- Stack multiple injection-detection layers when protecting mission-critical system prompts from sophisticated attackers.
- Add length-greater-than-zero constraints to required schema fields to catch hallucinated empty responses.
- Combine deny lists and allow lists rather than choosing one defensive approach exclusively.
- Build evals reactively from real user failure reports instead of synthetic test generation upfront.
- Practice prompt injection on your own agents using GPT-4 to expose existing vulnerabilities cheaply.
- Buffer streaming tokens until guardrail agent emits at least one validation token before frontend display.
- Search agent outputs for substrings of system prompt content as cheap deterministic leak prevention.
- Never run inference clients on untrusted user workstations because system prompts will leak inevitably.
- Build guardrail agents specifically to develop transferable alignment-agent design skills for production work.
- Test defensive systems against weaker models to surface vulnerabilities that stronger models temporarily mask.
- Use system messages over user messages whenever stronger instruction following is operationally required.
- Treat AI engineering as ninety percent software engineering and apply traditional architectural patterns aggressively.
- Drop reported failures directly into eval suite as regression tests using coding agents to expand.
- Study transformer architecture fundamentals to develop intuition about prompt behavior under the hood.
