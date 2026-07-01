---
title: "Context Engineering lessons from Manus #18"
videoId: OaUOHEHtlOU
url: https://www.youtube.com/watch?v=OaUOHEHtlOU
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works (Vibhav Gupta + Dexter Horthy)
---

# The one idea worth a video

**1. Design around the KV cache: pin the prefix, push everything dynamic to the end.** Caching is purely prefix-continuous, so any early edit (the date, a swapped tool list) throws away all downstream precomputed attention and quadruples your cost.
VERDICT: 🔗 next-step video available (complements "Forked Subagents").

**2. Mask, don't remove: gate tools at the logit layer instead of swapping the tool set.** Leave every tool defined and zero out the disallowed tool-name tokens at decode time, so you change behaviour without breaking the cache. Then watch the tokenizer, because "call_mom" and "call_me" can collide.
VERDICT: ❌ net-new video available.

**3. Restorable-reference compaction: offload big observations, keep a handle to reload them.** Replace a fetched webpage or a generated file with a URL or key plus a restore tool, so context stays small but nothing is lost.
VERDICT: 🔗 next-step video available (complements "Progressive Disclosure").

*Also film-able (not deep-dived):*
- **Recitation:** re-state the objective or to-do list near the context's end during long tool-call runs to fight attention drift. Slot: Context Engineering. Complements dynamic context injection (Ray can demo Claude Code's to-do re-injection).
- **Keep the wrong turns in context:** leaving failed tool calls and stack traces visible can improve self-correction on 50-step tasks (12-factor agents, factor 9). Slot: Advanced Techniques.
- **Tool-call representation and tokenizer-aware naming:** how you encode tool calls (BAML vs JSON schema) and whether names are single tokens change accuracy. Slot: Prompt Engineering (complements "Structured Output").

---

# Summary + counts

Vibhav Gupta and Dexter Horthy dissect the Manus context-engineering paper: KV caching, masking tools via logits, recitation, restorable compression, and why few-shot prompting usually backfires.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

### Spine 1: Design around the KV cache

The claim: because an LLM re-reads its entire prefix every token, providers cache the precomputed attention for stable prefixes, so the single biggest lever on agent speed and cost is never changing the front of your context. Why it is non-obvious: most engineers treat the system prompt as free scratch space and cheerfully stamp today's date into it, or swap the tool list when state changes. Both silently invalidate the cache. Why it is true: caching is purely prefix-continuous. The provider hashes the token sequence and reuses stored attention only up to the first mismatch, so one early edit forces full recomputation downstream, "way slower and also like four times the cost." Therefore the discipline is structural: pin the system prompt, and push every dynamic value (date, retrieved state, tool set) to the very end, where a growing chat history can still cache everything before it. It generalizes cleanly to RAG pipelines, where injecting freshly retrieved chunks at the top of a long, otherwise-stable prompt destroys cache hits that end-appending would keep. How it goes wrong: for short one-or-two-call interactions none of this matters ("don't do any of this crap"), and a manually placed cache-control block can hurt more than automatic prefix caching if you put it wrong.

### Spine 2: Mask, don't remove (logit-level tool gating)

The claim: to change which tools an agent may call without breaking the cache, leave every tool defined in context and instead mask the logits at decode time, zeroing the probability of any tool name that is currently disallowed. Why it is non-obvious: the intuitive move (OpenAI's original Swarm pattern) is to hand each agent a different tool set, which mutates the prefix and guarantees a cache miss on every hop. Why it is true: function calling is just a special token that flips the model into constrained decoding; once it fires, the very next tokens are the function name. If you restrict the allowed grammar at that point, you gate tools while the prefix stays byte-identical. The catch is the tokenizer: if "call_mom" and "call_me" share the leading tokens "call", "m", masking "call_mom" can force the model down the "call_me" branch it never intended. It generalizes to any structured-output field, as when Kimi-K2 emitted "propra" because "approach" was two tokens and a single-token synonym fixed it. How it goes wrong: on smaller models with longer contexts these collisions bite hardest, and you cannot apply the technique blind. You must inspect the tokenizer, or the gating backfires into confidently wrong tool calls.

### Spine 3: Restorable-reference compaction

The claim: instead of carrying every full observation forever, replace bulky content (a fetched webpage, a generated file) with a compact reference plus a restore tool, so context stays small but nothing is permanently lost. Why it is non-obvious: the default agent loop appends every tool result verbatim, betting that ever-larger context windows will save you. Why it is true: attention degrades over distance and cost scales with tokens, so a fifty-step agent that hoards raw observations both slows down and drifts off track. Swapping observation two's full webpage for its URL, with a documented "restore with this key" action, lets the model reload on demand while the working context represents each step in a handful of tokens. It generalizes precisely to coding agents: once a file edit is confirmed, "keeping the actual code that it generated is kind of useless." Keep a one-line summary and reload the file only when a later change fails. A deterministic rule ("after about 15 observations, compress the oldest") keeps the compressed tail stable, so the cache re-stabilizes over time. How it goes wrong: every restore is an extra tool call, and generic compaction is genuinely hard. Narrow agents can hard-code exactly what to drop; a general agent trades tool-call count against accuracy.

---

# 🎬 Proposed ACS videos

## 1. Design Your Prompt Around the Cache

- **TITLE:** Design Your Prompt Around the Cache
- **HOOK:** Putting the date in your system prompt is quietly costing you 4x on every single call.
- **THE PROMISE:** For anyone building an agent or chatbot loop, you will leave able to reorder one prompt so cache hits stay alive across a long conversation.
- **THE SHAPE:** (1) Whiteboard why an LLM re-reads its whole prefix every token, so caching is prefix-continuous. (2) Show the date-in-system-prompt anti-pattern breaking the cache. (3) Move dynamic values to the end; watch a growing chat still cache everything before them. (4) Compare provider control: Anthropic cache-control blocks, OpenAI's opaque prefix plus prompt_cache_key, Gemini's manual route. (5) Live proof: send the same request twice and read the cached-token count.
- **SPINE:** 1 (KV cache design).
- **SLOT:** Context Engineering > new chapter "Optimizing Cost and Latency" (or Advanced Techniques).
- **RELATIONSHIP:** 🔗 complements "Forked Subagents." That video already teaches that the prompt cache is prefix-keyed per model and that a fork hits it for free because it shares the parent's prefix. This adds the general design discipline: order every agent's context so the cache survives (system prompt pinned, dynamic values last, never mutate the front mid-thread).
- **PROOF TO REUSE:** "that's killing the KV cache for no reason" (date in system prompt); "put the dynamic stuff of your system as late as possible"; Anthropic's documented 1024-token minimum cacheable prompt; the live twice-run request that shows zero cached tokens until the prompt is long enough.

## 2. Mask, Don't Remove: Change an Agent's Tools Without Breaking the Cache

- **TITLE:** Mask, Don't Remove: Change an Agent's Tools Without Breaking the Cache
- **HOOK:** Swapping an agent's tool list mid-run breaks the cache 100% of the time. There is a better way.
- **THE PROMISE:** For engineers building multi-mode agents, you will leave knowing how to enable and disable tools at the logit layer, and why your tool names decide whether it works.
- **THE SHAPE:** (1) Explain function calling as a special token that flips the model into constrained decoding. (2) Show the naive Swarm approach (different tools per agent) killing the cache. (3) Leave all tools defined, mask the disallowed tool-name logits instead. (4) The tokenizer trap: mask "call_mom" and accidentally force "call_me". (5) Fix it by naming tools so leading tokens differ, and by dumping the tokenizer to check.
- **SPINE:** 2 (logit-level tool gating).
- **SLOT:** Context Engineering (advanced) or Advanced Techniques > Multi-Agent Orchestration.
- **RELATIONSHIP:** ❌ net-new. Nothing in the catalog teaches constrained decoding, logit masking, or tokenizer-aware tool naming; the Prompt Engineering "Structured Output" draft covers getting valid JSON out, not gating tools at decode time without breaking the prefix.
- **PROOF TO REUSE:** the "call me, call mom, call Dexter" work-mode walkthrough of how masking "call_mom" backfires into "call_me"; Kimi-K2 emitting "propra" because "approach" is two tokens; "you can see how actually doing this can actually backfire ... if you're not careful about how you're naming your tools."

## 3. Give Your Agent a Restore Button: Compaction Without Losing Anything

- **TITLE:** Give Your Agent a Restore Button: Compaction Without Losing Anything
- **HOOK:** Your fifty-step agent is drowning in its own observations. Hand it a restore tool instead.
- **THE PROMISE:** For anyone building long-running agents, you will leave able to shrink context by replacing bulky observations with restorable references the model can reload on demand.
- **THE SHAPE:** (1) The problem: appending every full observation slows the agent and drifts it off task. (2) Replace observation two's full webpage with its URL plus a "restore with this key" tool. (3) The coding-agent case: drop generated file contents after a confirmed edit, keep a summary, reload only when a change fails. (4) A deterministic compaction rule (compress the oldest observation after fifteen) that lets the cache re-stabilize. (5) The trade-off: extra tool calls versus accuracy versus context size.
- **SPINE:** 3 (restorable-reference compaction).
- **SLOT:** Context Engineering > The Solution Paradigm (next to Progressive Disclosure).
- **RELATIONSHIP:** 🔗 complements "Progressive Disclosure." That video teaches disclosing a static, authored context layer only as needed. This applies the same idea to runtime agent observations: offload the fetched page or file to a restorable handle and deterministically compress the oldest, so a live agent loop stays lean.
- **PROOF TO REUSE:** "from this URL, I got this action" as the compact observation; "keeping the actual code that it generated is kind of useless"; "after about 15 observations, I always compress the oldest one"; the framing that this beats "hoping that GPT-26 has a 20 million token window."

---

# 📚 Full wisdom (reference)

## SUMMARY
Vibhav Gupta (BAML) and Dexter Horthy (HumanLayer) unpack the Manus context-engineering paper on the "AI That Works" show: caching, tool masking, recitation, compression, and few-shot pitfalls.

## IDEAS
- KV cache reuses precomputed attention math for identical token prefixes, so stable prefixes make inference faster.
- Putting today's date in the system prompt silently breaks the KV cache on every single call.
- Place dynamic variables at context's end so a growing chat history still caches everything before them.
- Anthropic enforces a 1024-token minimum cacheable prompt, tied to their architecture's internal cache-alignment block size decision.
- Anthropic gives explicit cache-control blocks; OpenAI's caching is opaque prefix-matching; Gemini offers the most manual control.
- Recitation deliberately re-injects the objective near context's end so the model refocuses before the next action.
- Manus reportedly runs roughly fifty tool calls per task, where mid-sequence attention drift becomes the failure.
- Instead of swapping tools mid-loop, leave them in context and mask invalid tool tokens via logits.
- Function calling is a special token that triggers constrained decoding onto your tool grammar immediately afterward.
- Poor tool names collide at the token level, so masking "call_mom" can accidentally force "call_me" instead.
- Kimi-K2 kept emitting "propra" because "approach" tokenizes as two tokens; a single-token synonym fixed the problem.
- Compress large observations into restorable references: replace a full webpage with its URL plus a restore-tool.
- A coding agent can drop generated file contents after editing, reloading them only when something breaks.
- Keeping wrong tool calls and stack traces visible can help the model self-correct in later attempts.
- Few-shot examples usually bias the model toward the example rather than teaching the actual intended behavior.
- Building an agent is itself few-shot: earlier turns bias every subsequent action that the model takes.
- Prefer clearing context and re-steering over correcting mid-thread, which trains the model to expect repeated mistakes.
- Changing tool-call representation from JSON schema toward BAML's format improved accuracy for every model by default.
- Deterministic context compaction beats hoping every future model ships a twenty-million-token window and abundant cheap RAM.

## INSIGHTS
- Caching depends purely on prefix continuity, so any early mutation invalidates all downstream precomputed attention work.
- Attention favors nearby tokens, so relevant instructions belong close to where the model must act next.
- These optimizations only matter for long-running agents; short one-shot calls should skip all this machinery entirely.
- Speed and cost are a separate eval axis from accuracy, since identical tokens yield identical outputs.
- Understanding token generation lets you derive these techniques from first principles instead of copying other people.
- Manual cache control beats automatic when you understand it, but backfires badly when you don't know how.
- Constrained decoding zeroes out any token probability that violates your allowed grammar or current tool set.
- General-purpose agents make compaction genuinely hard; narrow single-purpose agents can hard-code exactly what to discard when.
- Tokenizer vocabularies differ per model, so tool-naming reliability must be verified against each model's own tokenizer.
- Smaller models and longer contexts amplify tokenizer and stack-trace pitfalls; larger models forgive them far more.

## QUOTES
- "that's killing the KV cache for no reason. You're literally just hurting the cash every single time." (Vibhav Gupta)
- "It's generally always going to be good to put the dynamic stuff of your system as late as possible." (Vibhav Gupta)
- "this is why we always say like use clear rather than resteer." (Dexter Horthy)
- "you're telling the model it's okay to make a mistake and then get corrected." (Dexter Horthy)
- "Random hashes are just not good. Like the model is just never going to be good at that." (Vibhav Gupta)
- "most people are better off not doing it rather than doing it." (Vibhav Gupta, on few-shot prompting)
- "The only thing that impacts the model is actually like tokens in tokens out." (Vibhav Gupta)
- "if you do something manually, you will always get better throughput if you know what you're doing than someone that does it automatically." (Vibhav Gupta)
- "keeping the actual code that it generated is kind of useless for that kind of task." (Vibhav Gupta)
- "tell the model what it did wrong because it will probably fix it." (Dexter Horthy)
- "there's always a distance at which it will never work as well." (Vibhav Gupta)
- "you can see how actually doing this can actually backfire in certain ways if you're not careful about how you're naming your tools." (Vibhav Gupta)

## HABITS
- Vibhav tests caching locally by running the same request twice and inspecting the cached-token counts returned.
- He dumps a model's tokenizer to diagnose why single words split into problematic multiple output tokens.
- For Anthropic models he asks the model to repeat a word, then counts the returned tokens.
- Dexter reverse-engineers Claude Code through a proxy to learn what the to-do tool actually does internally.
- Dexter iterates prompt snippets locally with Raycast dynamic variables before wiring them into his orchestrated agents.
- He deliberately avoids influencing teammates so they independently discover agent-design decisions, like how to get help.
- They publish every episode, its whiteboards, and code openly in a public GitHub repo for viewers.
- Vibhav replaces UUIDs and random hashes in prompts because models handle them poorly for tool calls.
- He defines clearly-good and clearly-bad outputs first, then gradually builds evals around those anchored quality judgments.

## FACTS
- Anthropic's documented minimum cacheable prompt length is 1024 tokens, below which no caching occurs at all.
- Breaking the KV cache forces full recomputation, at roughly four times the cost and much slower.
- Manus is a viral generalist agent whose speed and UX polish set it apart from competitors.
- OpenAI added a prompt-cache-key parameter, giving developers more explicit control over its previously opaque prefix caching.
- Transformers split input into subsequences computed individually, enabling stackable, cacheable, partially-parallel and deterministic prefix computation blocks.
- OpenAI's original Swarm framework passed the same context between agents having different system messages and tools.
- Photoshop eventually forgets undo history past a certain point because undoing action sequences is genuinely hard.
- Anthropic does not publicly expose its tokenizer, unlike some other providers that publish theirs for inspection.
- Content-addressable caching means identical token sequences hash identically, so caches are usually not shared across users.

## REFERENCES
- Manus context-engineering paper / blog post (the primary source discussed)
- BAML (boundaryml) and the boundaryml.com/discord tool-naming anecdote
- HumanLayer and the "AI That Works" show, with all episodes, whiteboards, and code in a GitHub repo
- 12-factor agents (specifically factor 9, on telling the model what it did wrong)
- DSPy, and Prashant's experiment moving DSPy's prompt format toward the BAML representation
- OpenAI Responses API, JSON mode, custom-grammar function calling, and the prompt_cache_key parameter
- Anthropic caching docs and cache-control blocks; Anthropic "micro-compaction"
- Gemini caching (most flexible / manual)
- OpenAI Swarm multi-agent framework
- A roughly 90-minute explainer video on how DeepSeek works under the hood
- Raycast (dynamic variables for local prompt iteration)
- Kimi-K2 model; GPT-4o and GPT-5 references; the needle-in-a-haystack benchmark
- DRM (decaying resolution memory) from a prior episode; "cracking the prompting interview" reference
- CC proxy (a tool from a Gauntlet AI student that strips traces from local Claude Code)

## ONE-SENTENCE TAKEAWAY
Understanding how LLMs generate tokens lets you engineer context for speed, cost, and reliability deliberately.

## RECOMMENDATIONS
- Move every dynamic value, especially the current date, to the very end of your context window.
- Never mutate the system prompt mid-thread; instead append changes at the very end to preserve caching.
- Re-inject the current objective or to-do list near the context's end during long repetitive tool-call sequences.
- Mask invalid tool tokens via logits instead of dynamically swapping tools and breaking your KV cache.
- Name tools so their leading tokens differ clearly, preventing logit masking from forcing the wrong selection.
- Replace bulky observations with restorable references and expose a restore tool to reload them on demand.
- Test caching locally by sending the exact same request twice and inspecting the reported cached-token usage.
- Dump or probe your model's tokenizer before trusting any tool names or constrained-decoding-sensitive output field values.
- Prefer starting a fresh context with brief steering over repeatedly correcting the model mid-conversation each time.
- Only apply these optimizations to agents running many tool calls, never to short one-shot chat interactions.
