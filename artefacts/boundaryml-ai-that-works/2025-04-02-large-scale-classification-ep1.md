---
title: Large scale classification #1
videoId: 6B7MzraQMZk
url: https://www.youtube.com/watch?v=6B7MzraQMZk
date: 2026-07-01
status: posted
source: BoundaryML / "AI That Works" (Vaibhav, Boundary/BAML + Dex, HumanLayer)
---

## The one idea worth a video

**Spine 1 (framework, ROUTE B latent-ish altitude): Build probe points into your LLM pipeline.** A black-box LLM gives you exactly one lever, the prompt, and that lever gets worse as the system grows; decompose the system into independently tunable, unit-testable control points instead.
VERDICT: 🔗 next-step video available (complements "closing-the-loop").

**Spine 2 (concrete pattern, de-merged): Retrieve then classify against huge category sets.** When you must pick from hundreds or thousands of categories (MCP tools, routing agents, taxonomies), prune the list with a cheap retrieval step to about twenty, then let a small LLM pick.
VERDICT: ❌ net-new video available.

**Spine 3 (concrete technique, de-merged): The text you embed is not the text the LLM should see.** Embedding text, LLM-facing description, and the code-level name are three separate knobs; alias the name away so attention lands on the description you control.
VERDICT: ❌ net-new video available.

## Summary + counts

Boundary's Vaibhav and HumanLayer's Dex teach large-scale classification: prune huge category lists with retrieval, then let a small LLM pick, building tunable probe points throughout.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1: probe points.** The claim: a black-box LLM offers one place to change behavior, the prompt, and that single knob gets worse as the system grows, so the fix is to decompose into independently tunable, testable control points. It is non-obvious because the default instinct is to keep editing the prompt; Vaibhav argues the opposite. The mechanism runs in two steps. Because the model is a black box you cannot modify, prompt text is your only naive lever; because prompt edits have global effects that worsen with size ("changing the word in 100 categories is way more likely to poison your output than with 10"), you can never isolate a fix. So you add explicit control points (embedding text, top-K, alias serialization, multi-pick pruning) and every failure now maps to one localized knob, and each layer becomes unit-testable alone. Vaibhav grounds this in chip design: circuits too small to introspect get deliberate detection points added. It generalizes to any multi-step LLM system, a RAG answerer or an agent router, not just classification. It goes wrong when probe count balloons: Anubha's point that more knobs add real introspection cost and complexity.

**Spine 2: retrieve then classify.** The claim: for hundreds or thousands of categories, never dump the full list into the prompt; prune with a cheap retrieval step to roughly twenty, then let the LLM pick. It is non-obvious because people either stuff everything into the prompt or reach for hierarchical categories, and Vaibhav warns hierarchies "bleed over" and add confusion. The mechanism: LLM selection accuracy falls as lists grow and categories overlap, and latency scales non-linearly (roughly quadratically) with input tokens, so cutting 500 categories to 20 raises accuracy and cuts latency at once. The pruning step is a swappable function: vector-DB top-K, a small boolean model judging each option relevant, or looping tiny models to halve the set repeatedly. It generalizes cleanly to MCP tool routing at scale (over a thousand tools), agent route selection past twenty routes, and analytic SQL column selection. It goes wrong when the user query does not embed near the right category, or when top-K is too small and drops the correct answer, after which the final LLM can never recover it.

**Spine 3: three texts, not one.** The claim: the text you embed for retrieval, the text you show the LLM to disambiguate, and the category's code-level name are three separate knobs you should control independently, and aliasing the name (K0, K1) forces the model's attention onto your description. It is non-obvious because people embed the raw category name and reuse it verbatim in the prompt; both assumptions are wrong. The mechanism: the embedding model and the generation model are different black boxes optimized differently, so text that maximizes retrieval proximity (fifteen example queries, twenty keywords) can poison the classifier through few-shot over-influence, while the text that best disambiguates for the LLM is a clean description. Because you cannot fine-tune fast, controlling the input strings is your fast lever. Aliasing removes name subtext, so "account issue" and "technical issue" stop colliding on their overlapping single words and the model spends all attention on your description. It generalizes to any RAG system, where chunks are embedded with synthetic questions but presented to the LLM as clean prose. It goes wrong when the two texts should differ but you keep them identical, capping accuracy.

## 🎬 Proposed ACS videos

### 1. Route 1000 MCP Tools With One LLM Function
- HOOK: Your agent has a thousand MCP tools and picks the wrong one; stop stuffing them all into the prompt.
- THE PROMISE: For anyone whose classifier, router, or tool-picker degrades past a few dozen options, you will leave able to build a retrieve-then-classify funnel that stays fast and accurate at any scale.
- THE SHAPE: (1) Show the naive prompt-stuffed classifier failing at 100+ categories. (2) Push categories into an in-memory embedding cache, retrieve top-K to about twenty. (3) Hand the pruned set to a small LLM (GPT-4o mini) to pick. (4) Swap the retriever for a boolean small-model filter to prove it is just "reduce many to some." (5) Add a second pruning pass for overlapping categories.
- SPINE: Spine 2.
- SLOT: Techniques class, new topic "large-scale-classification / routing at scale."
- RELATIONSHIP: ❌ net-new. No ACS video covers classification, retrieval/RAG, vector search, or routing among many categories or MCP tools. The nearest title, "the-ambiguity-line," is about choosing Claude versus Codex, an unrelated kind of routing.
- PROOF TO REUSE: "how do you deal with an MCP server that has over a thousand tools"; "if you have a routing agent with more than 20 routes... we sometimes see degradation"; the pick_category = narrow_down then pick_best code; "LLMs are quadratic... so if you have fewer input tokens, they will be a lot faster."

### 2. The Text You Embed Is Not the Text the LLM Should See
- HOOK: Everyone embeds the raw category name and reuses it in the prompt; both moves quietly cap your accuracy.
- THE PROMISE: For anyone building retrieval or classification, you will leave able to split embedding text, LLM-facing text, and the code name into three separate knobs, and alias names away so the model attends only to what you wrote.
- THE SHAPE: (1) Embed a bare category name and watch the right query miss it. (2) Replace the embedding text with LLM-generated example queries, scenarios, and keywords, and watch retrieval snap closer. (3) Show that dumping those same fifteen examples into the LLM prompt poisons it via few-shot influence, motivating a separate description. (4) Add a BAML alias (K0) and show it strip the name from the prompt so attention lands on the description.
- SPINE: Spine 3.
- SLOT: Prompt Engineering class (Foundations), adjacent to few-shot and structured-output; alternatively Context Engineering.
- RELATIONSHIP: ❌ net-new. Prompt Engineering has few-shot, structured-output, and constraints-and-negatives, but nothing on decoupling embedding text from prompt text, or on aliasing category names to redirect attention.
- PROOF TO REUSE: "usually what people do when they add an embedding is they just take the raw string"; "recognizing that these two texts are very different because the models under the hood are very different is an important distinction to hitting really high accuracy"; the K0/K1 alias demo where "it puts all of its attention metric onto the description that we want."

### 3. Build Probe Points Into Your LLM Pipeline
- HOOK: When your AI pipeline is wrong, you are praying to the prompting gods; give yourself real knobs instead.
- THE PROMISE: For engineers shipping LLM features, you will leave able to decompose a black-box pipeline into independently tunable, unit-testable probe points, so a failure tells you exactly which stage to fix.
- THE SHAPE: (1) Frame the black box with one knob, the prompt, and why bigger prompts are worse. (2) Introduce probe points: embedding text, top-K, serialization/alias, multi-pick pruning. (3) Show the waterfall trace that localizes a failure to retrieval versus final pick. (4) Unit-test one layer in isolation ("if the model returns these four categories, we should return this one"). (5) Close on the cost: more knobs add complexity, so add them deliberately.
- SPINE: Spine 1.
- SLOT: Techniques class, next to "closing-the-loop" and "boxing-the-model-in."
- RELATIONSHIP: 🔗 complements "closing-the-loop." That video teaches iterating on model behavior with feedback; this adds WHERE to place the probes so each subsystem is independently tunable and unit-testable, instead of iterating on one giant prompt. Do not re-teach the general iterate-with-feedback loop; teach the decomposition and localization move.
- PROOF TO REUSE: "the minute a system becomes non-probable, it really becomes hard to go edit"; "it's more about building probes into our software so that when things don't work, we have a thing to change that isn't like praying to the prompting gods"; the electrical-engineering detection-points analogy; "all we're doing... is we're writing a function that says pick category."

## 📚 Full wisdom (reference)

### SUMMARY
Boundary's Vaibhav and HumanLayer's Dex teach large-scale classification: prune huge category lists with retrieval, then let a small LLM pick, building tunable probe points throughout.

### IDEAS
- LLM systems become black boxes offering one knob, the prompt, which worsens as it grows larger.
- Prove techniques on tiny models first; if small models succeed, frontier models will do incredible things.
- Classifying over one hundred categories degrades LLM performance; routing agents past twenty routes often pick wrong.
- Push the massive category list into a vector database, retrieve top-K, then classify the small subset.
- Disjoint categories tolerate many options; overlapping categories with tiny nuances break LLM selection accuracy quite badly.
- The text you embed for retrieval need not match the text shown to the classifying LLM.
- Instead of embedding raw category names, embed LLM-generated example queries, scenarios, and keywords for tighter closeness.
- Aliases like K0, K1 strip category names so the LLM attends purely to your written description.
- Single-word category names overlap by default; aliases remove that subtext when many similar categories compete closely.
- Top-K is a probe you tune: increase it, or fix embedding text, when correct targets disappear.
- A waterfall debugging flow reveals whether retrieval or the final pick caused a given classification mistake.
- The whole system is really just one function: given text, return a category, with swappable internals.
- Retrieval need not use vectors; a small boolean model judging each option relevant works just fine.
- Fewer input categories mean much faster responses because LLM latency scales non-linearly with input token count.
- Fewer than one hundred thousand categories fit in memory; no dedicated vector database software is required.
- Allow the LLM to pick multiple categories, then prune again for genuinely overlapping, complex category spaces.
- Dynamic enums guarantee the returned value matches a category, eliminating fragile parsing of messy LLM output.

### INSIGHTS
- Controllability beats raw model quality; more independent knobs mean faster convergence on any given hard problem.
- A prompt is a terrible sole knob because each edit ripples unpredictably across many competing categories.
- Decomposing into smaller steps lets you optimize and unit-test each sub-function independently from the whole pipeline.
- The embedding model is a black box, but the text you feed it is fully controllable.
- Fine-tuning is too slow for iteration; manipulating embedding input text achieves control almost instantly by comparison.
- Retrieval optimization and prompt disambiguation are different problems because the underlying models work fundamentally differently underneath.
- Classification pipelines contain a built-in eval: input query, expected category, assert on the returned final answer.
- The best eval comes from shipping, capturing real user queries, and detecting rejected downstream user actions.
- More probes add introspection but also add complexity, so each knob carries a real maintenance cost.
- With unfixable black-box models, extra probes are worth far more than they cost in traditional software.

### QUOTES
- "It's been about 2 years and the AI models seem to just be stuck in demo land." (Vaibhav)
- "Let's do really hard problems with tiny models to prove that... you can even get small models to do impressive things." (Dex)
- "The minute a system becomes non-probable, it really becomes hard to go edit." (Vaibhav)
- "Now you're stuck waiting for GPT-26 to come out." (Vaibhav)
- "The problem with AI pipelines is we don't really get these probing points." (Vaibhav)
- "The more control you have and the more knobs you give yourself access to, the faster you're going to find the best way to solve a particular problem." (Dex)
- "It's more about building probes into our software so that when things don't work, we have a thing to change that isn't like praying to the prompting gods." (Vaibhav)
- "All we're doing in reality is we're writing a function that says pick category... and we're returning a category type." (Vaibhav)
- "Usually what people do when they add an embedding is they just take the raw string and add it directly into the vector database." (Vaibhav)
- "Recognizing that these two texts are very different because the models under the hood are very different is an important distinction to hitting really high accuracy." (Vaibhav)
- "The smaller and simpler the steps are, the easier they are to optimize." (Dex)
- "It puts all of its attention metric onto the description that we want and it recognized that K0 is purely an identifier." (Vaibhav)
- "Having engineers have direct access to user feedback on what LLMs are doing... super super important to like have that tightest possible iteration loop." (Dex)
- "The real answer is my favorite little meme... It depends." (Vaibhav)

### HABITS
- I LLM-generate example queries, scenarios, and keywords for each category to seed its embedding text initially.
- Run everything locally in memory first, caching embeddings to a pickle file for quick iteration cycles.
- I turn on strict type checking in Python rather than trusting its default permissive runtime mode.
- I write the whole pipeline in pseudocode first to see how the pieces fit before executing.
- I trace each pipeline method so I can inspect exactly what every stage returned during debugging.
- I alias every category to a neutral identifier so its name never leaks into the prompt.
- Ship to real users, collect their queries, and evaluate the pipeline against actual production traffic data.
- When classification fails, first locate the failing stage before touching any prompt or embedding text blindly.

### FACTS
- LLM inference latency scales non-linearly, roughly quadratically, with the number of input tokens it must process.
- Some production systems must classify against more than five hundred distinct categories reliably in daily practice.
- MCP servers can expose over one thousand tools, which LLMs simply cannot select from reliably well.
- Routing agents with more than twenty routes begin selecting slightly wrong routes in commonly observed practice.
- Fewer than one hundred thousand categories can run in machine memory without any dedicated vector-database software.
- BAML injects JSON-schema-like category definitions into the model's system prompt in a special, carefully structured way.
- Top-K in vector search is the returned entry count, unrelated to top-K token sampling in LLMs.
- Vaibhav believes even GPT-3.5 was already good enough for many real production pipeline scenarios back then.

### REFERENCES
- BAML (Boundary's markup/prompting framework, used throughout the demo)
- Boundary (Vaibhav's company)
- HumanLayer (Dex's company, safer/reliable AI deployment)
- Excalidraw (diagramming, called "scalar draw" in the auto-captions)
- Cursor (editor used for the live coding)
- OpenAI GPT-4o mini (classification model in the demo)
- GPT-3.5, GPT-4 image model (mentioned in passing)
- NumPy (cosine similarity for the in-memory embedding search)
- Pydantic (base-model / data-class typing)
- UV (Python runner: uv run hello.py)
- Vector databases (generic, plus in-memory pickle cache alternative)
- Boundary's observability/tracing tool (on-prem availability mentioned, roughly four weeks out)
- Next session teased: reasoning models versus reasoning prompts

### ONE-SENTENCE TAKEAWAY
Turn black-box LLM systems into decomposed pipelines with independent, tunable, unit-testable probe points placed everywhere.

### RECOMMENDATIONS
- Replace prompt-stuffed category lists with a retrieval step that first prunes down to a manageable subset.
- Embed LLM-generated queries, scenarios, and keywords per category instead of just the bare category name string.
- Keep your embedding text and prompt text separate, and optimize each independently for its own model.
- Alias category names to neutral identifiers so the model attends only to the descriptions you control.
- Trace every pipeline stage so you can localize whether retrieval or final picking caused a given failure.
- Use dynamic enums to guarantee outputs match valid categories, removing brittle parsing from your whole pipeline.
- For heavily overlapping categories, let the LLM pick several candidates, then prune again to one deterministically.
- Prefer a fast in-memory embedding cache over standing up dedicated vector-database infrastructure for most classification workloads.
- Build your evals from real production traffic, flagging every case where users rejected the suggested action.
