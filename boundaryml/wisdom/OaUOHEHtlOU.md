---
video_id: OaUOHEHtlOU
title: "Context Engineering lessons from Manus - 🦄 #18"
url: https://www.youtube.com/watch?v=OaUOHEHtlOU
channel: BoundaryML
---

## SUMMARY

Vibhav (BoundaryML) and Dex (HumanLayer) unpack the Manus paper's context-engineering tricks: KV caching, recitation, masking tools, compression, and tokenizer-aware naming.

## IDEAS

- KV caching exists because token sequences resemble dynamic programming problems with mostly stable inputs across iterations.
- Anthropic enforces a 1024 minimum cacheable prompt because architecture alignment blocks govern what can be precomputed.
- Putting today's date inside system prompts silently destroys KV cache continuity across every long-running thread iteration.
- Dynamic variables belong at the very end of context windows to preserve maximum upstream caching benefits possible.
- Recency bias means models pay more attention to tokens placed near the generation point than upstream.
- Recitation re-injects objectives and to-do lists mid-context so models stay aligned across fifty-plus tool calls.
- Long agent loops drift around the middle because needle-in-haystack performance degrades as token distance grows.
- Manus deliberately keeps incorrect tool observations to help models learn from their own stack traces.
- Random hashes, UUIDs, and Luma URLs poison contexts because models cannot reliably regurgitate arbitrary tokens.
- Few-shot prompting usually backfires because biases pull models toward example outputs rather than intended behavior.
- Resteering inside a chat teaches the model that mistake-then-correction is the expected conversational pattern going forward.
- Clearing context and restarting beats resteering because fresh history avoids reinforcing previous wrong-turn patterns.
- Context compression replaces fat observations with restorable URLs the agent can reload via dedicated tools.
- File-system-as-memory works because agents already understand file primitives and can organize their own recall.
- Masking tool logits beats removing tools because removing breaks KV cache continuity at the system prompt.
- Forcing logits onto invalid tools can backfire when shared token prefixes route generation toward wrong functions.
- Tool naming matters at the tokenizer level because shared prefixes between tool names cause cascading misroutes.
- Kimi K2 returned "propra" two percent of the time because "approach" tokenized as two tokens.
- Smaller models with longer contexts suffer most from tokenizer quirks and architectural shortcuts.
- BAML-style tool representation outperforms raw JSON schema, and combining both produces even better tool-calling accuracy.
- OpenAI's prompt cache key gives manual control whereas Gemini exposes the most flexible caching primitives available.
- Manual cache management beats automatic when you understand it but worsens performance when misconfigured.
- The transformer encoder layer caches deterministically; the KV cache inside attention is a separate optimization.
- Models trained on natural English assume nearby words matter more, biasing attention toward recent context.
- Constrained decoding zeros log probabilities for tokens violating the grammar, JSON, or tool schema.
- Function calling emits a special token, then constrains subsequent tokens to match the chosen tool's grammar.
- Undo is computationally hard because most software cannot reverse arbitrary action sequences cleanly.
- Caching only matters for long workloads; small one-shot prompts gain nothing from optimization effort.
- Agents calling fifty tools benefit dramatically from compressing the oldest fifteen observations into restorable references.
- Tokenizer vocabularies differ per model, so single-token field names like "stance" beat multi-token "approach".
- Discord URLs work better than custom slugs because shorter known strings tokenize predictably for regurgitation.

## INSIGHTS

- Architecture knowledge unlocks intuitions about caching, attention, and tokenization that prompt engineering alone cannot deliver.
- Continuity of token prefixes is the single biggest determinant of inference latency and operational cost.
- Place stable content first, dynamic content last, and mission-critical content nearest the generation point.
- Recitation is cheap insurance against attention decay across long agentic loops with many tool calls.
- Compression via restorable references scales agents beyond the limits of any future giant context window.
- Masking via logits preserves cache while pruning tools, but only when names tokenize without dangerous shared prefixes.
- Resteering trains models to expect mistakes; clearing and restarting trains them to expect first-try success.
- Few-shot examples should differ structurally from real inputs to prevent the model from copying surface patterns.
- Tokenizer-aware naming converts mysterious accuracy losses into deterministic, fixable engineering problems with clear root causes.
- Smaller models magnify every context-engineering decision because they have less slack to absorb noisy or imprecise input.

## QUOTES

- "We're all using the same models. It's not like they have anything special under the hood." — Vibhav
- "Today's date is going to break the KV cache all the time." — Vibhav
- "The model is just likely to pay more attention to it." — Vibhav
- "Use clear rather than resteer." — Dex
- "You're telling the model it's okay to make a mistake and then get corrected." — Dex
- "Random hashes are just not good. Like the model is just never going to be good at that." — Vibhav
- "Approach is two tokens." — Vibhav
- "Eventually I just at some point I was like the model is just too stupid." — Vibhav
- "I literally took the tokenizer for the K2 model and I dumped it out." — Vibhav
- "Don't try to mess with the cache keys if you're not willing to go learn how these systems work." — Vibhav
- "If you're going to do few-shot prompting, be clever about it." — Vibhav
- "It's really freaking hard to command Z a lot of actions." — Vibhav
- "The bigger the model, the shorter your context window, the less they matter." — Vibhav
- "If your tasks are taking like a minute to run, yes, then KV cache matters." — Vibhav
- "This is more applicable to building software that interacts with models than for how you prompt them." — Dex
- "You're literally just hurting the cache every single time." — Vibhav
- "Ssomeone that does it manually will always get better throughput if you know what you're doing." — Vibhav
- "Tool calling, structured output, function calling — they're all the same." — Vibhav
- "Few-shot prompting sucks." — Vibhav

## HABITS

- Dump the model's tokenizer when accuracy mysteriously fails on specific words during structured outputs.
- Inspect HTTP response usage fields to verify cache hit counts on every iteration.
- Place dynamic variables and tool definitions at the end of context windows by default.
- Repeat task lists or objectives near the generation point during long agent loops.
- Replace UUIDs and random hashes with predictable short slugs before injecting into prompts.
- Restart context with two-sentence steering instead of resteering inside an existing failed conversation.
- Test caching by sending identical requests twice and checking reported cached token counts.
- Keep tool sets static during a session and mask via logits rather than removing tools.
- Choose single-token field names over multi-token alternatives when constraining smaller-model outputs.
- Compress old observations after roughly fifteen steps using restorable file or URL references instead.
- Read provider caching docs to learn minimum cacheable prompt sizes before optimizing prefixes.
- Run BAML-style structured output instead of JSON schema for higher tool-calling accuracy across providers.
- Eval speed and cost separately from accuracy when evaluating context-engineering changes for production agents.
- Bias few-shot examples to differ structurally from real inputs so models do not blindly copy.
- Inject the to-do list near the end of context periodically to force attention onto current tasks.

## FACTS

- Anthropic requires prompts of at least 1024 tokens before any caching mechanism activates on input.
- Manus agents average roughly fifty tool calls per task before completing user-requested workflows.
- Haiku models support smaller cache prompts than Opus, possibly using float16 instead of float32 weights.
- Kimi K2 emits "propra" instead of "approach" two percent of the time due to tokenizer artifacts.
- OpenAI added a prompt_cache_key parameter giving developers manual control over cache hit grouping.
- Gemini exposes the most flexible explicit caching API, requiring developers to manage TTLs themselves.
- Transformer architecture splits computation into encoder and decoder layers that can cache independently.
- The KV cache inside attention layers is separate from provider-side prompt prefix caching mechanisms.
- Constrained decoding zeros log probabilities of tokens that violate the specified grammar or schema.
- Cache control blocks in Anthropic's API only work at specific positions within the request payload.
- Photoshop limits undo history because reversing arbitrary action sequences becomes computationally infeasible.
- BAML's tool representation format beat JSON schema in Pashant's DSPy benchmark across multiple models.
- Cache hits reduce inference cost roughly fourfold compared to recomputing the entire token prefix.
- Recency bias in language models comes from training data where nearby words correlate more strongly.
- Gauntlet AI in Austin runs an in-person school training AI engineers with real-world projects.

## REFERENCES

- Manus context-engineering paper / blog post on agent architecture lessons
- HumanLayer (Dex's company) and the AI That Works podcast on GitHub
- BoundaryML and the BAML structured-output framework
- Anthropic prompt caching documentation and cache_control blocks
- OpenAI Responses API with prompt_cache_key parameter
- Gemini explicit context caching API
- Twelve-Factor Agents (factor nine: tell the model what it went wrong)
- Cracking the Prompting Interview talk on JSON-mode versus code-shaped outputs
- DeepSeek architecture explainer video on YouTube
- Pashant's DSPy plus BAML tool-representation benchmark
- Kimi K2 model and its tokenizer vocabulary
- Cursor, Claude Code, and the to-do tool for coding agents
- Eugene's commentary on KV-cache versus prefix-cache distinctions
- CC-Proxy from Gauntlet AI for inspecting Claude Code traces
- Raycast for iterating on prompt snippets locally

## ONE-SENTENCE TAKEAWAY

Master tokenization, caching, attention, and recitation — context engineering is the architecture beneath every agent.

## RECOMMENDATIONS

- Read your provider's caching documentation before optimizing prefixes for production agent workloads.
- Move every dynamic variable, including dates, to the very end of your prompts.
- Inject task lists or objectives near generation points during loops exceeding ten tool calls.
- Compress observations older than fifteen turns into restorable URL or file references.
- Mask invalid tools via logits rather than removing them from the system prompt.
- Audit tool names against the tokenizer to avoid dangerous shared prefixes between similar tools.
- Replace UUIDs and random hashes with short predictable slugs before placing into model contexts.
- Restart conversations with fresh steering instead of resteering inside failing existing chat threads.
- Use BAML-style structured output representations alongside JSON schema for measurably better tool-calling accuracy.
- Verify caching empirically by running identical requests twice and inspecting the usage response fields.
- Skip caching optimization entirely for short one-shot prompts where overhead exceeds any benefit.
- Eval speed and cost as separate metrics from accuracy during context-engineering experiments and rollouts.
- Dump the tokenizer when a model fails on specific words to diagnose multi-token artifacts.
- Choose single-token field names like "stance" over multi-token alternatives like "approach" deliberately.
- Try GPT-5 with full stack traces to test whether bigger models forgive previously toxic noise.
- Test fewer-shot examples that differ from real inputs structurally to prevent surface-level pattern copying.
- Keep system prompts static and append all dynamic content below user history for cache stability.
- Build restorable tool pairs (compress, restore) so agents can reload context only when truly needed.
- Inspect HTTP responses through proxies like CC-Proxy to understand how Claude Code structures its traces.
- Watch the DeepSeek architecture video to build intuition about GPU caching and attention math.
