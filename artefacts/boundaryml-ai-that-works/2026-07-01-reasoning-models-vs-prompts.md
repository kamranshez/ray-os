---
title: Reasoning models vs reasoning prompts #2
videoId: D-pcKduKdYM
url: https://www.youtube.com/watch?v=D-pcKduKdYM
date: 2026-07-01
status: posted
source: BoundaryML "AI that works" (Vibhav + Dexter)
---

## The one idea worth a video

**Spine 1 (the reframe): Reasoning is a behavior you architect into any model, not a model tier you buy.** You can turn GPT-4o-mini into a "reasoning model" by prompting it to note what is hard before answering; buying o3 versus building your own reasoning is a money-versus-time decision.
VERDICT: next-step video available.

**Spine 2 (the net-new gem): Do the reasoning inline in one prompt; a separate actor/checker loop costs exponentially more.** Each separate call re-passes the whole context, so a two-step loop pays for the question three times; the same propose-critique-revise loop inside one prompt is a single generation cost.
VERDICT: net-new video available.

**Spine 3 (the architecture): Guided, domain-specialized reasoning beats free-form reasoning when you know your domain.** Prescribe the reasoning steps and route to a narrow specialist prompt that is great at cipher and deliberately trash at everything else.
VERDICT: next-step video available.

---

## Summary + counts

Vibhav and Dexter of BoundaryML build a Neo4j movie-query agent to compare reasoning models against reasoning prompts, proving any model can be guided to reason.

Counts (one tally per promoted spine): 🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 - Reasoning is a behavior you architect, not a model you buy

The claim: you do not need to buy a reasoning model to get reasoning; you can turn any capable model into one by telling it to note what is useful and particularly hard before answering, and the choice to buy versus build is a money-versus-time decision. This is non-obvious because most people treat reasoning as a model tier you upgrade into (swap GPT-4o-mini for o3-mini). The episode strips that away: mechanically, a reasoning model just adds special reasoning-start and reasoning-end tokens that fine-tuning taught it to over-weight through the attention mechanism. Nothing stops you approximating that in a cheap model. The mechanism is sequential generation: a model emits one token at a time and only attends backwards, so forcing it to first write "notes on what is hard" seeds the context with a scratchpad the eventual answer attends to, instead of computing everything in one forward pass. Vibhav proves it live by deleting the instruction and watching the model collapse back to raw JSON with no reasoning. This generalizes hard to on-prem and edge deployments running small llama models that lack a reasoning mode entirely, and to any code or query task. How it goes wrong: fine-tuned reasoning keeps a genuine edge that prompt engineering cannot fully replicate, and when your time is worth more than tokens, just buying o3 is correct.

### Spine 2 - Inline reasoning is one cost; separate actor/checker loops cost exponentially

The claim: running a critique or self-correction loop inside a single prompt is dramatically cheaper than orchestrating it across separate actor and checker calls. This is non-obvious because the reflexive advice is "add a checker agent," and people assume more verification calls add linear cost. The mechanism is token geometry: every separate call re-sends the entire prior context. To generate the checker response you pay for question plus actor; to generate the next actor pass you pay question plus actor plus checker; so even a two-step loop passes the question three times and the actor twice, and it keeps compounding. Doing propose then critique then revise inside one generation pays for each token once. As Vibhav puts it, "your costs boil up exponentially really fast with this approach." Prompt caching softens repeated context but does not save you across genuinely separate requests, which providers treat as new. This generalizes to any LLM-as-judge or debate-prompting pipeline; the same math tells you when to inline a review step versus fan it out. How it goes wrong: separate calls buy control and isolation a single prompt cannot, such as deterministically stopping after two errors and sending the user a message, and sometimes that control is worth the cost.

### Spine 3 - Guided, domain-specialized reasoning beats free-form reasoning

The claim: when you know your domain, prescribing the reasoning structure and routing to a specialist prompt beats generic free-form reasoning, even a reasoning model's. This is non-obvious because the industry reflex is "use the smartest general model and let it think." But an everything-model has a wide, high-variance output distribution, so you are paying for generality you do not need. The mechanism: a prompt tuned narrowly on cipher (propose a query, list problems with the query, produce an improved query) collapses the output distribution to high accuracy on cipher while becoming, in Vibhav's words, "trash at making cookie recipes." Put an intent router in front to dispatch queries, and compose specialists into a system whose variance keeps shrinking. Crucially, a reasoning model will not invent a propose-critique-revise cipher scaffold on its own; you have to prescribe it, and you can even layer that scaffold on top of o3. As Vibhav says, "free form reasoning as good as it is just going to be worse than guided reasoning if you know the domain." This generalizes to SQL generation, structured extraction, and any narrow high-stakes task with a knowable shape. How it goes wrong: specialization destroys generality, so it is wrong for open-ended assistants, and a badly prescribed structure can underperform free-form.

---

## 🎬 Proposed ACS videos

### 1. Why Your Actor Checker Loop Costs 10x Too Much

- HOOK: Everyone tells you to add a checker agent. Nobody tells you it re-bills your whole prompt every single turn.
- THE PROMISE: For anyone building verification or self-correction into an agent, you will learn exactly when to collapse a multi-call loop into one inline prompt and when the extra cost buys real control.
- THE SHAPE:
  1. Whiteboard the actor-checker loop and count tokens: question paid three times, actor twice, for a two-step loop.
  2. Show the same propose-critique-revise loop running inside a single structured prompt as one generation cost.
  3. Explain where prompt caching helps (inline, shared context) and where it cannot (separate requests treated as new).
  4. Name the counterpoint: separate calls buy deterministic gating (stop after two errors, message the user), which is sometimes worth the cost.
- SPINE: Spine 2.
- SLOT: Techniques > Multi-Agent Orchestration (sits directly beside test-time-compute.md; feeds the planned subagent-verification-loops backlog video).
- RELATIONSHIP: 🔴 net-new. test-time-compute.md teaches that more subagents plus verification means "more tries plus checking, not one longer guess" and treats fan-out as pure upside; it never covers the cost geometry that tells you when to collapse that loop inline. The planned subagent-verification-loops has only a title and no brief, so the cost math is unclaimed.
- PROOF TO REUSE: the exponential token whiteboard ("question plus actor plus checker" compounding); the exact quote "your costs boil up exponentially really fast with this approach"; the caching exchange ("open pricing you is only for the new tokens that you're generating").

### 2. You Do Not Need a Reasoning Model

- HOOK: A reasoning model is just a few special tokens the model was trained to trust more. You can fake that in a model a tenth the price.
- THE PROMISE: For engineers deciding whether to reach for o3, you will leave able to turn any model into a reasoner and to make the buy-versus-build call on purpose instead of by reflex.
- THE SHAPE:
  1. Swap GPT-4o-mini to o3-mini on a hard cipher query and watch reliability jump, and cost and latency with it.
  2. Explain reasoning under the hood: reasoning-start and reasoning-end tokens the model learned to over-weight.
  3. Turn 4o-mini into a reasoner by prompting "before answering, note what is useful and particularly hard," then delete the line and watch reasoning vanish.
  4. Frame the decision: buy a reasoning model to spend money and save your time; build your own for speed, on-prem, or edge llama that lacks reasoning.
- SPINE: Spine 1.
- SLOT: Prompt Engineering > Core Techniques (next to 06-chain-of-thought.md).
- RELATIONSHIP: 🔗 complements 06-chain-of-thought.md, which already teaches that smaller and local models benefit from explicit chain of thought and that you can direct the reasoning; this adds the two things that draft does not, the reasoning-token mechanism and the explicit buy-versus-build decision framework. It also complements test-time-compute.md's "use a bigger model" knob with "roll your own reasoning when you cannot just reach for a bigger model."
- PROOF TO REUSE: the quote "I've turned this model into a reasoning model without actually using any reasoning under the hood"; the reasoning-start/reasoning-end token whiteboard; the money-versus-time framing "I want to spend more money in favor of time to get a slightly better response."

### 3. Route to a Specialist, Not a Genius

- HOOK: A giant general model gives you a wide, noisy distribution. A narrow prompt that is great at one thing and useless at everything else beats it.
- THE PROMISE: For anyone building a reliable pipeline over a known domain, you will learn to prescribe reasoning steps and route to specialist prompts instead of throwing everything at one mega-model.
- THE SHAPE:
  1. Show the wide, high-variance distribution of a single everything-prompt versus a narrow specialist's tight distribution.
  2. Prescribe a guided reasoning scaffold in markdown headers: propose cipher query, problems with query, improved reasoning, final.
  3. Add an intent router in front that dispatches to the cipher specialist or a general prompt.
  4. Show that you can layer the same guided scaffold on top of a reasoning model, since it will not invent that structure itself.
- SPINE: Spine 3.
- SLOT: Prompt Engineering > Steering Models (next to 01-steering-distributions.md).
- RELATIONSHIP: 🔗 complements 01-steering-distributions.md, which teaches narrowing attention within a single prompt (the flashlight metaphor, attention is zero-sum); this is the next step, the intent-router-to-specialist-prompt architecture plus a prescribed propose-critique-revise scaffold, and it deliberately trades generality for domain accuracy across composed prompts.
- PROOF TO REUSE: the quote "free form reasoning as good as it is just going to be worse than guided reasoning if you know the domain"; the "trash at making cookie recipes" specialization demo; the intent-router whiteboard composing specialist distributions.

### Also film-able (not deep-dived)

- **LLMs are spell-checkers that cannot emit an unlikely token: alias and correct programmatically.** You cannot force a model to output a genuinely misspelled or statistically unlikely name; fall back to aliasing (let it output canonical text, convert after) or constrained generation, and treat an empty result as ambiguous (wrong, missing, or misspelled) by retrying differently rather than assuming missing. One-line pitch: "The one thing no reasoning model can fix for you." SLOT: Prompt Engineering > Core Techniques (08-constraints-and-negatives.md). RELATIONSHIP: 🔗 complements the enum/constraints material with a reliability fallback pattern. PROOF: "models are just predictive systems and they will at some point be wrong ... you have to build systems on top of it to make it correct."

---

## 📚 Full wisdom (reference)

### SUMMARY
Vibhav and Dexter of BoundaryML build a Neo4j movie-query agent to compare reasoning models against reasoning prompts, proving any model can be guided to reason.

### IDEAS
- A reasoning model just adds special reasoning-start and reasoning-end tokens the model learns to weight heavily.
- You can turn GPT-4o-mini into a reasoning model by telling it to note hard parts first.
- The model provider controls the reasoning-start token; writing your own thinking text stays merely prompt input.
- Reasoning tokens carry no inherent meaning; training teaches the model to over-weight text between the markers.
- Reasoning is elasticity: the model itself chooses zero, five hundred, or a thousand reasoning tokens here.
- Chain of thought is prescriptive and forced; reasoning is a freer superset the model may skip.
- Function calling can force reasoning: order a thought_process string field before the actual answer field emits.
- Reasoning written inside JSON fields is worse; models naturally write useful reasoning as plain text first.
- Free-form reasoning loses to guided reasoning whenever you actually know the domain you operate in well.
- An intent router sends queries to specialist prompts that outperform narrowly while failing everything else badly.
- Actor-checker loops across separate calls re-pass question, actor, and checker, so token costs compound exponentially fast.
- Running the same critique loop inline in one prompt is a single, far cheaper generation cost.
- Swapping to a reasoning model trades money for time: you prompt less, the model thinks more.
- Roll your own reasoning for speed, on-prem models, or tiny edge llama deployments lacking reasoning entirely.
- Working context is a choice: delete solved queries, keep only the replies, inject synthetic error messages.
- UI checkboxes can turn end users into context engineers, choosing which queries persist per turn themselves.
- LLMs are excellent spell-checkers but cannot emit a genuinely misspelled, statistically unlikely target token on demand.
- For unlikely tokens use aliasing: let the model output canonical text, then convert it programmatically afterward.
- An empty database result is ambiguous: it could be wrong, missing, or simply misspelled user input.
- Inference-time compute is simply generating more tokens before answering, buying accuracy at a higher GPU cost.

### INSIGHTS
- Reasoning is not a model you buy but a behavior you architect into any capable model.
- The word reasoning is overloaded; separate model-improving thinking cleanly from the summary you display to users.
- Fine-tuned reasoning gives markers extra attention weight, an advantage no prompt-engineering trick can fully replicate here.
- Guided reasoning beats generic reasoning-model output precisely because you encode domain structure the model won't invent.
- Collapsing multi-call verification into a single inline prompt saves cost, latency, and reprocessing while keeping control.
- Choosing a reasoning model is really a time-versus-money decision about where engineering effort should go next.
- Models are predictive systems; you must build correction systems around them rather than trusting outputs blindly.
- How you shape context for the user is a deliberate product choice, not a technical accident.
- Elasticity, letting the model decide how much to reason, is reasoning's genuine advance over rigid chain-of-thought.

### QUOTES
- "I've turned this model into a reasoning model without actually using any reasoning under the hood." (Vibhav)
- "reasoning is now becoming a thing that I can choose what I'm doing with rather than a thing that I have to go do in a specific way." (Vibhav)
- "free form reasoning as good as it is just going to be worse than guided reasoning if you know the domain you're operating in." (Vibhav)
- "the way you build the context for the user is really a choice of what you do." (Vibhav)
- "turn your users into context engineers." (Vibhav)
- "we're using the same name to do two different things." (Vibhav)
- "your costs boil up exponentially really fast with this approach." (Vibhav)
- "I want to spend more money in favor of time to get a slightly better response." (Vibhav)
- "LLMs are just amazing spell checkers." (Vibhav)
- "models are just predictive systems and they will at some point be wrong ... you have to build systems on top of it to make it correct." (Vibhav)
- "It's not how models write ... the training data set is not going to have large blocks of useful text in JSON objects." (Vibhav)
- "if you really want to ship something really really fast just throw an o3 model, let it do its reasoning, and you basically save time." (Vibhav)

### HABITS
- They always ground abstract reasoning discussions in one concrete demo: a live Neo4j movie-recommendation query agent.
- They whiteboard the architecture before writing code so viewers understand the system while reading it later.
- On a failed query they inject a synthetic error message into context, then re-prompt the model.
- They delete previous cipher queries from context once a clean result arrives, preserving only the replies.
- They stream each working-context event to the frontend so users watch the agent reason live throughout.
- They always put the thought_process field first in structured output so thinking precedes the committed answer.
- They experiment with different thinking-tag names to find which name yields the best model results empirically.
- They prototype pipelines live, timeboxing debugging to two minutes before flipping over to audience questions instead.

### FACTS
- Neo4j uses Cypher, a SQL-like query dialect, for querying nodes and relationships in property graph databases.
- A Kevin Bacon number measures degrees of separation from actor Kevin Bacon through shared co-starring films.
- OpenAI released function calling in April 2023, advising a thought field placed as the first parameter.
- OpenAI lets developers set a reasoning-token budget, choosing exactly how hard the model thinks per call.
- Early LangChain function-calling loops output a thought field, stripped and printed to console before running functions.
- A reasoning model can terminate mid-thought when its token budget runs out before finishing its reasoning.
- Prompt caching lets providers charge only for newly generated tokens, not reprocessed prior context each request.
- Llama 4 released shortly before this episode, prompting the reasoning-model discussion among several recent model launches.

### REFERENCES
- BoundaryML "AI that works" series (weekly episodes); previous episode on classification with a thousand-plus classes.
- Neo4j public movie-recommendations database; Cypher query language; a livestream Vibhav did with the Neo4j team.
- BAML (BoundaryML) function definitions used to define the chat-with-graph function.
- Models discussed: GPT-4o-mini, o3-mini, DeepSeek R1, Llama 4.
- Concepts and papers: chain of thought, debate prompting paper, LLM-as-judge, inference-time / test-time compute.
- OpenAI function calling (April 2023) and its "thought first parameter" advice; early LangChain function-calling loops.
- Kevin Bacon number / six degrees of Kevin Bacon.
- BoundaryML Discord (Pashant cited as knowledgeable on graph databases).

### ONE-SENTENCE TAKEAWAY
Reasoning is a behavior you architect into any model, not an expensive model you buy.

### RECOMMENDATIONS
- Turn a cheap model into a reasoner by prompting it to note hard parts first explicitly.
- Place a thought_process field before the answer field to force reasoning through structured output schemas reliably.
- Collapse actor-checker loops into one inline prompt to avoid paying exponential multi-call token costs unnecessarily here.
- Build an intent router that dispatches queries to narrow, domain-specialized prompts for reliably better domain accuracy.
- Prescribe explicit reasoning steps like propose, critique, revise rather than trusting free-form model reasoning entirely alone.
- Add a separate user-facing summary field so displayed reasoning does not bias the actual generation tokens.
- Handle empty query results as ambiguous: retry differently instead of assuming the data is simply missing.
- For impossible tokens, alias canonical output then correct programmatically against a known list of valid values.
- Choose reasoning models when shipping speed matters more than money; engineer reasoning when performance does instead.
