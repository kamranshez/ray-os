---
title: Understanding Latency
videoId: wadVIkJnjQE
url: https://www.youtube.com/watch?v=wadVIkJnjQE
date: 2026-07-01
status: posted
source: BoundaryML "AI That Works" podcast (Vaibhav Gupta + Dexter Horthy)
---

## The one idea worth a video

**Spine 1 (ROUTE B, latent + broad) - Latency is a perception problem, not a speed problem.** You cannot make the underlying model faster than a competitor using the same models and networks, so the entire game is making the app *feel* faster: skeletons, meaningful-chunk streaming, fake progress, prefetch, generative-UI hot-swap.
VERDICT: net-new video available.

**Spine 2 (de-merged concrete technique) - Cache-aware prompt architecture.** Structure the prompt so the KV cache prefix never breaks: static context first, dynamic schema and question last (the opposite of instinct), append-only buffer, the sub-1024-token caching floor, and warm-one-then-parallelize.
VERDICT: next-step (complement) video available.

**Spine 3 (de-merged concrete technique) - Prefetch agent work by gating tool permissions.** Run the agent's read-only prefix speculatively before the user hits enter, blocking every write and non-idempotent tool, and fork/cancel the session if the input changes.
VERDICT: net-new video available.

---

## Summary

BoundaryML's AI That Works: Vaibhav Gupta and Dexter Horthy break down agentic-app latency, from perceived-speed UX tricks to prompt-cache architecture, streaming, prefetching, and hidden reasoning-tokens.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 - Latency is a perception problem, not a speed problem

The claim: since everyone builds on the same foundation models and networks, you cannot win on raw speed, so you compete on *perceived* speed instead. What most people get wrong is treating latency as a backend metric to shave, when it is really a UX design surface. The mechanism is a two-step chain: first, actual model time is largely fixed and shared across competitors, so the differentiable variable is what the user sees while waiting; second, the brain reads pixel movement as progress, so streaming a meaningful chunk, showing reasoning tokens, or rendering a skeleton converts dead wait into felt momentum. Vaibhav is blunt: latency "isn't actually about making your app faster, only about making your app feel faster." It generalizes cleanly to any agent product UI: a data-extraction tool that streams each completed row, or a plotting agent that draws points as they arrive. It goes wrong when the "meaningful chunk" is chosen badly (streaming a half-formed number, "530 53,000"), which feels more broken than a clean spinner, and when fake progress outlives real work and users notice the lie.

### Spine 2 - Cache-aware prompt architecture

The claim: how you *order* a prompt, not just what is in it, sets your latency, because providers cache a contiguous prefix and any change to the front blows that cache. Non-obvious part: the intuitive layout (schema and instructions in the system message, user context in the user message) is exactly backwards for speed. The mechanism: providers hash a contiguous prefix and reuse computation on cache hits; because the cache breaks at the first differing token, the most static content must lead and the most dynamic content (the per-call schema or question) must trail, so the stable head stays cacheable. Two derivatives follow: providers skip caching prefixes under 1024 tokens, so padding a 800-token prompt past the floor is *faster*; and for parallel calls sharing a prefix, firing one first to warm the cache then parallelizing the rest beats a naive gather. It generalizes to any high-volume classifier serving one big system prompt to thousands of short user messages. It goes wrong when the "static" base context silently changes per call, quietly invalidating everything downstream.

### Spine 3 - Prefetch agent work by gating tool permissions

The claim: you can start an agent's work before the user commits by speculatively running only its safe, read-only prefix. Non-obvious part: naive prefetch is dangerous for agents because a speculative run could send an email or write a file, so the enabling trick is a permission whitelist, not a caching layer. The mechanism: treat the agent as an API that turns a string into an event buffer; mark every write and non-idempotent tool as blocked and every read tool as auto-allowed, then when the user pauses typing, fire the prompt roughly 200ms early and stop the event buffer at the first write event, caching the read-only result in Redis. If the user edits the prompt, cancel and fork a fresh session from the previous point. It generalizes to any form-driven agent where a dominant field is stable and the rest are checkboxes. It goes wrong if permissions are not actually paused (a speculative write escapes) or if inputs churn faster than the prefetch completes, burning compute for nothing.

---

## 🎬 Proposed ACS videos

### 1. Make Your Agent Feel 10x Faster Without Touching the Model
- HOOK: You will never beat a competitor on raw model speed. You beat them on perceived speed.
- THE PROMISE: For anyone shipping an agent product, learn to audit every wait your app forces and convert it into felt progress.
- THE SHAPE: (1) The reframe: same models, same networks, feelings win. (2) The streaming spectrum: token, semantic chunk, whole object, demoed on the recipe and plot examples. (3) Choosing the meaningful chunk (render math only when complete). (4) Skeletons, ghost components, reasoning-token displays, and the honest limits of fake progress. (5) Generative-UI hot-swap: ship a JSON table now, upgrade to a custom component when its stream finishes.
- SPINE: 1
- SLOT: Techniques class, new chapter "Designing Agentic UX" (or Business class, agent-product build).
- RELATIONSHIP: ❌ net-new. No ACS video covers perceived latency or agent-app streaming UX; the-shifting-bottleneck teaches finding the constraint, and the context-engineering class teaches context, but neither touches the feel-faster surface.
- PROOF TO REUSE: "you can magically make your app feel 10 times faster than your competitors"; the recipe-slider streaming demo (block the ingredient until the unit is present); "math is pointless unless it's done"; TurboTax/Honey/Windows-file-copy fake loaders.

### 2. Build Prefetch for Your Coding Agent
- HOOK: Start the agent before the user hits enter, safely, by turning off its ability to do anything irreversible.
- THE PROMISE: For agent builders, learn to speculatively run an agent's read-only prefix on user pause and shave seconds off perceived response time.
- THE SHAPE: (1) The idea: Instagram and Gmail prefetch on pause; do the compute twice and hope the user does not change it. (2) Why agents are different: a speculative run must never send an email. (3) The whitelist: block every write and non-idempotent tool, auto-allow reads, at the app level not the user level. (4) Stop the event buffer at the first write event and cache it in Redis. (5) Fork-and-cancel when the user edits the prompt.
- SPINE: 3
- SLOT: Claude Code class (backlog near blocking-risky-commands-with-hooks / background-hooks) or Techniques class.
- RELATIONSHIP: ❌ net-new. Nothing in the Claude Code backlog covers speculative prefetch; the closest is blocking-risky-commands-with-hooks, which gates commands for safety, not for speculative execution.
- PROOF TO REUSE: "You're just doing the compute twice in the hope that the user won't change it"; the Claude-Code-prefetch walkthrough (every write tool blocked, every read tool allowed); "by the time I hit enter it immediately asks me for approval, that's just a good dopamine hit"; warm the cache by loading the files it was going to read.

### 3. Order Your Prompt for the Cache, Not for Humans
- HOOK: The intuitive prompt layout is the slow one. Static first, dynamic last, and never touch the prefix.
- THE PROMISE: For anyone serving prompts at volume, learn to architect the prompt so the KV cache prefix survives and latency drops.
- THE SHAPE: (1) Treat the prompt as an append-only, write-only buffer. (2) Why the cache breaks: any change to the prefix blows the whole computation. (3) The counterintuitive reorder: user/base context first as a cache block, schema and question last. (4) The sub-1024-token floor: pad a short shared prompt to earn caching. (5) Warm-one-then-parallelize for calls sharing a prefix.
- SPINE: 2
- SLOT: Context Engineering class (complement) or Prompt Engineering (structured-output neighbor).
- RELATIONSHIP: 🔗 complements the shipped Context Engineering class. That class teaches WHAT to put in context; this adds WHERE to put it so the provider's KV cache prefix stays intact, plus the caching-floor and cache-warming tricks. State that the class already covers context selection so Ray does not re-teach it.
- PROOF TO REUSE: "Think of your LLM prompt as a write only buffer. It's an append only array"; the 1024-token caching floor ("add some random tokens as dead space"); "Fire one, then fire the rest right afterwards for parallelism reasons"; the static-first/schema-last reorder ("you have to do it the opposite way").

---

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's AI That Works: Vaibhav Gupta and Dexter Horthy break down agentic-app latency, from perceived-speed UX tricks to prompt-cache architecture, streaming, prefetching, and hidden reasoning-tokens.

### IDEAS
- Performance work is not about making code faster; it is about finding where the bottleneck lives.
- Latency is mostly perception; you cannot beat competitors on raw model speed, only on perceived speed.
- Never use an instantaneous request-response callback; always use event streams or a database reader-writer pattern instead.
- Skeletons, ghost components and fake loaders make waiting feel like progress; TurboTax and Honey do this.
- Prefetch by pressing enter yourself for users after they pause typing, doing the compute twice speculatively.
- Prefetching agent work requires blocking every write and non-idempotent tool, whitelisting only the safe read operations.
- If the user edits the prefetched prompt, just cancel the session and fork a fresh one.
- Latency improvements only matter above a threshold; a minute to ten seconds changes the user's behavior.
- Treat your LLM prompt as an append-only, write-only buffer so the KV cache prefix never breaks.
- Providers do not cache prompts under 1024 tokens, so padding a short prompt can be faster.
- For parallel calls sharing a prefix, fire one first to warm the cache, then parallelize rest.
- Put the most static content first in your prompt; put dynamic schema and question last, counterintuitively.
- Reasoning models trap users in HTTP hang time because providers now hide the actual reasoning tokens.
- Setting reasoning effort to minimal cut output from 548 tokens to 34, six seconds to two.
- Reasoning summaries make latency worse; you generate summary tokens on top of the hidden reasoning tokens.
- Stream by meaningful semantic unit, not tokens, because math is pointless to render until fully done.
- Block streaming a tool argument until complete so the front-end type system stays clean and simple.
- Generative UI can hot-swap a basic JSON table for a custom component once its stream completes.
- The single biggest latency win is cutting a 4000-token prompt to 400 after actually reading it.
- Represent your prompt as a type system instead of few-shot examples; the model needs no example.
- Letting Claude write your prompts just injects training-set knowledge the model already has; tune prompts yourself.
- Alias verbose schema field descriptions to short names so the model reads fewer redundant tokens overall.
- The streaming triplet state mirrors environment variables, where a field is present-unset, set, or entirely absent.

### INSIGHTS
- You compete on perceived speed, not real speed, since everyone shares the same models and networks.
- Every latency optimization is a derivative of one behavior; enumerate what patterns that behavior makes possible.
- Prompt-cache awareness reshapes prompt architecture: static context leads, dynamic schema trails, opposite of most people's instinct.
- Perceived progress beats truthful progress; a fake loader that shows movement satisfies users more than honesty.
- Designing streaming is a semantic decision: choose the smallest chunk the user can meaningfully interact with.
- Clean streaming type guarantees keep business rules out of the front end, enabling prefetching and parallelism.
- Reasoning tokens are hidden latency; measuring the SSE stream reveals where the invisible thirty seconds went.
- Providers hide reasoning traces to protect training data, trading your latency for their competitive moat deliberately.
- Token reduction is the highest-leverage latency fix, yet the least glamorous and most consistently skipped step.
- Decoupling components is the precondition for parallelism, which combined with cache-warming produces the real speed gains.
- Match latency ambition to the work: deep interactive loops need speed; background batch jobs tolerate slowness.

### QUOTES
- "It's actually not about making your code faster... It's actually about knowing what where you want to make your code faster." (Vaibhav)
- "latency isn't actually about making your app faster... only about making your app feel faster. Feelings are a lot more important than the actual latency." (Vaibhav)
- "You're not going to magically make your model system like 10 times faster than your competitor... But you can magically make your app feel 10 times faster than your competitors." (Vaibhav)
- "Think of your LLM prompt as a write as a write only buffer. It's an append only array." (Vaibhav)
- "if your prompt is around like 800 tokens, you'll actually be slightly slower than if your prompt is around like just over a thousand." (Vaibhav)
- "Fire one, then fire the rest right afterwards. for parallelism reasons." (Vaibhav)
- "I don't think I've heard that before. I think that's some fresh viob alpha." (Dexter)
- "You're just doing the compute twice on the in the hope that the user won't change it." (Dexter)
- "math is pointless unless it's done." (Vaibhav)
- "you can go from like literally having 548 output tokens to 34. And that's the difference between 6 seconds and 2.3 seconds." (Vaibhav)
- "The more you let Claude write your prompts... you're literally just going to like be telling the model stuff it already knows." (Vaibhav)
- "the semia async valley of death." (Dexter)
- "autocomplete cannot take one second. It has to be like sub 200 milliseconds." (Dexter)

### HABITS
- Vaibhav profiles the SSE stream directly to locate where invisible reasoning time is actually being spent.
- One host always runs coding agents with 32000 max thinking tokens, trading time for reliable correctness.
- The co-host stops ChatGPT and switches to auto whenever a simple question triggers unnecessarily slow reasoning.
- He deletes every redundant schema description Claude Code auto-generated, trimming the prompt live from 1300 tokens.
- He reads the entire prompt end-to-end before condensing, keeping only the tokens that actually still matter.
- He refuses few-shot prompting, always representing schemas as a full type system rather than example JSON.
- He uses electric SQL, an open-source sync engine sitting in front of Postgres, for real-time UI.
- He writes throwaway coding agents constantly to test latency ideas, spinning up new ones for demos.

### FACTS
- Anthropic and many providers do not cache prompt prefixes shorter than 1024 tokens at all currently.
- Anthropic prompt caching is not automatic; you must manually mark cache blocks within the prompt yourself.
- OpenAI's responses API defaults to reasoning on; unset reasoning still silently generates many hidden reasoning tokens.
- One customer's system produced 400 output tokens but 1400 hidden reasoning tokens, roughly seventy percent invisible.
- Prompt caching only helps under constant request flow within roughly five minutes, not sporadic scattered traffic.
- Cursor tab autocomplete must respond under 200 milliseconds or it breaks the developer's flow of thought.
- Firebase and Convex work by letting the UI read the database while servers only write changes.
- Go removed null strings, treating an unset environment variable identically to an empty string by design.
- Switching reasoning effort to minimal dropped one measured demo from 548 to 34 output tokens instantly.

### REFERENCES
- HumanLayer (Dexter Horthy's company; tools making coding agents effective in large complex codebases).
- BoundaryML / BAML ("Vibbot's" blog; schema-in-prompt parsed into a type system, function calling out of the box).
- electric SQL (open-source sync engine that sits in front of Postgres).
- Firebase and Convex (sync-engine architectures where the UI reads the database, servers write).
- 12-factor agents paper (Dexter, published April; teaser for next episode on schema-first agent development).
- Manus paper (masking tool calls / putting the schema at the end vs the sampler).
- Swix chart ("not fun to wait, not enough to delegate" - the semi-async valley of death).
- OpenAI responses API docs (reasoning effort: none / minimal / summary).
- Cursor and Replit (coding agents building the expectation that the user will wait; reasoning-summary display).
- TurboTax, Honey, Windows file-copy dialog (deliberate fake-progress loaders).
- Prior episodes referenced: one on KV cache / prompt caching; one on GPT-4o-mini chain-of-thought.

### ONE-SENTENCE TAKEAWAY
You cannot make models faster than competitors, but you can make your app feel faster.

### RECOMMENDATIONS
- Profile your SSE stream first to find where reasoning or network time actually disappears before optimizing.
- Replace instantaneous request-response with event streams or a sync engine like electric SQL over your Postgres.
- Add skeleton components and reasoning-token displays so users see movement during any unavoidable long waiting period.
- Reorder prompts so static context sits first and dynamic schema last, keeping the cache prefix intact.
- Pad short shared prompts past 1024 tokens so provider prompt caching actually kicks in for you.
- Fire one call to warm the cache before parallelizing the rest that share the same prefix.
- Prefetch agent runs on user pause, whitelisting read tools and blocking every write or dangerous command.
- Block streaming each tool argument until it is complete so front-end business logic stays trivially simple.
- Set reasoning effort to minimal or none when auditability matters less than a fast responsive experience.
- Replace few-shot example JSON with a type system and alias verbose field descriptions to shorter names.
- Stop letting Claude auto-write prompts and schema descriptions; hand-tune them to remove redundant training-set filler yourself.
