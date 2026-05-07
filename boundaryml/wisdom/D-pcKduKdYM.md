---
video_id: D-pcKduKdYM
title: "🦄 reasoning models vs reasoning prompts: ep#2"
url: https://www.youtube.com/watch?v=D-pcKduKdYM
channel: BoundaryML
---

### SUMMARY

Vaibhav and Dexter from BoundaryML compare reasoning models versus reasoning prompts using a Neo4j movie agent generating Cypher queries through iterative tool-calling loops.

### IDEAS

- Reasoning models add special tokens marking when internal thought processes start and end during generation.
- You cannot inject the actual reasoning-start token yourself; only the provider controls that special demarcation.
- Models trained with reasoning blocks weight tokens between markers heavier than surrounding context during attention.
- Guided reasoning beats free-form reasoning when you know your specific operating domain ahead of time.
- Free-form chain-of-thought in JSON fields produces worse results than markdown plaintext before structured output.
- Reasoning is elastic; chain-of-thought is prescriptive and forces token generation regardless of question difficulty.
- Splitting reasoning across multiple LLM calls causes exponential cost growth from repeated context retransmission.
- Inline reasoning within one prompt achieves similar quality at single-pass cost versus actor-checker loops.
- Turning users into context engineers via UI checkboxes lets them control what enters model context.
- LLMs are exceptionally good spell checkers, making misspelled tokens nearly impossible to force as output.
- Models output reasoning tokens before structured JSON because training data rarely contains thoughtful prose inside JSON.
- Working context can be cleared between turns since users only need final replies preserved.
- A router prompt classifying intent before specialized prompts narrows distributions and increases accuracy per domain.
- Reasoning models trade engineering time for inference cost when shipping fast matters more than optimization.
- You can blend reasoning models with guided reasoning prompts to get both elasticity and domain-specific structure.
- Streaming working-context events to the frontend lets users see progress without seeing opaque blocks.
- Empty database results require injected hints because models cannot distinguish missing data from wrong queries.
- Function calling with thought parameter ordering forces models to reason before producing structured outputs cleanly.
- Misspelled named entities require post-programmatic aliasing since models statistically refuse improbable token sequences.
- Reasoning happens to be overloaded as a name for LLM thought, embeddings, and UI display.
- Markdown headers in prompts dramatically improve output quality compared to bulleted lists or inline instructions.
- A single mega-prompt produces wide variance; specialized routed prompts produce tighter accuracy distributions.
- Models bias attention toward bottom of reasoning blocks more than top during final token generation.
- Test-time compute insight: more pre-answer tokens beat smarter models for many reasoning-heavy tasks.
- Debate prompting structures like initial-reasoning then problems-with-reasoning then improved-reasoning improve cipher query generation.
- Cookie recipe prompts fail when forced through cipher-query reasoning scaffolds, showing tradeoffs in specialization.
- The same reasoning text can serve as model-internal thought and short user-facing summary simultaneously.
- Constraint generation forcing valid JSON disrupts how models naturally write training-distribution text.
- Frontend can hide intermediate working context entirely or show streaming reasoning depending on UX choice.
- Adding deterministic error injection after two failures gives users control instead of infinite model loops.

### INSIGHTS

- Reasoning is elasticity in token budget; chain-of-thought is prescriptive structure that runs regardless of need.
- Specialized prompt pipelines outperform generic mega-prompts by trading cookie-recipe coverage for cipher-query accuracy.
- Cost grows exponentially across multi-call reasoning loops because every call retransmits accumulated context tokens.
- Models cannot generate statistically improbable tokens; aliasing post-processing handles misspellings reasoning never will.
- Guided reasoning headers in markdown beat reasoning-as-JSON-field because training data lives in plaintext markdown.
- The reasoning name conflates model attention weighting, UI display content, and chain-of-thought scaffolding incorrectly.
- Reasoning models save engineering time at higher inference cost; prompt engineering inverts that tradeoff.
- Empty database results need injected hypotheses because pure model retry loops cannot distinguish failure modes.
- Working context streaming separates what model sees from what user sees, enabling deletion between turns.
- Routing intent first lets each downstream prompt specialize narrowly while maintaining coverage through composition.
- Models trained on reasoning blocks learn to weight token sequences inside markers heavier than surrounding context.
- Output reasoning twice: long internal scratchpad guiding generation plus short summary intended for user display.
- Anything possible with prompt scaffolding becomes way more controllable when you know the operating domain.
- Reasoning models plus guided reasoning compose; you do not have to choose one approach exclusively.
- Frontend choices about which intermediate steps to display turn users into participating context engineers.

### QUOTES

- "If we can't iterate on it, then the problem is we rely on the model to be perfectly correct." Vaibhav
- "Turning your users into context engineers along the way so they can make an educated decision." Vaibhav
- "It's just like we're humans are bad at naming and we're using the same name to do two different things." Vaibhav
- "It's not how models write. It's not like the training data set is not going to have large blocks of useful text in JSON objects." Vaibhav
- "Reasoning is a little bit I think the whole goal of reasoning is elasticity." Vaibhav
- "We don't need way smarter models we just need them to generate more tokens before they answer." Dexter
- "I today am willing to spend more money so I spend less time prompting and the model spends more time prompting." Vaibhav
- "Free form reasoning as good as it is just going to be worse than guided reasoning if you know the domain you're operating in." Vaibhav
- "Models are just predictive systems and they will at some point be wrong and you have to build systems on top of it." Vaibhav
- "How LM are just amazing spell checkers." Vaibhav
- "Open AI is pricing you in a way where the question is being priced three different times." Vaibhav
- "If the model doesn't generate thinking text as part of its response, it is bad." Vaibhav
- "It's giving no special weight. But you could imagine in the training loop, the model has learned that things between the reasoning block are actually extra useful." Vaibhav
- "You can build whatever you want. And if you have things structured like this, you have control over it." Dexter
- "It's writing cipher in the way that the training set will be written as cipher in markdown." Dexter
- "How hard do you want it to think is one concept, but really around how many tokens are you allowed to generate." Dexter
- "Even if you write the thinking text yourself, the model provider itself actually has to do the thinking themselves." Vaibhav
- "Constraint generation kind of screws up with it trying to write the way it's been trained to write things." Dexter
- "Just like using GPT4o on average will be better than GPT4o mini, on average a reasoning model will have a slightly better curve." Vaibhav
- "There's no way to prompt a thinking model to do this other than by asking it to do this." Dexter

### HABITS

- Whiteboard the architecture before diving into code so the team has shared mental model.
- Stream working-context events to frontend so users see progress instead of opaque waiting blocks.
- Delete intermediate cipher queries from chat history after final reply preserves the answer.
- Inject deterministic error messages into context when database returns empty rather than retry blindly.
- Use markdown headers in prompts to structure reasoning sections rather than bulleted lists.
- Pull up Excalidraw whiteboard alongside code editor when explaining architectural decisions during pair programming.
- Build router prompts that classify intent before dispatching to specialized domain-specific prompts.
- Put thought parameter first in function-calling schemas to force reasoning tokens before structured outputs.
- Delete previous queries from context when new query succeeds, keeping only successful results around.
- Time-box live coding debugging to two minutes before flipping to questions or alternative approaches.
- Test prompts against intentionally hard examples like Kevin Bacon numbers to expose model failure modes.
- Compare same query with reasoning model versus prompted reasoning to validate elasticity tradeoffs concretely.
- Add aliasing layers post-LLM that map model-output names to actual database entities reliably.
- Output reasoning twice in schemas: long internal version for guidance plus short user-facing summary.
- Always include schema description directly in prompts when querying graph or relational databases.

### FACTS

- OpenAI added thought parameter advice for function-calling APIs when first launched in April 2023.
- Cipher is the SQL-like dialect Neo4j uses for graph database queries.
- Kevin Bacon number measures degrees of separation between any actor and Kevin Bacon through movies.
- Six degrees of Kevin Bacon claims any actor connects to Kevin Bacon within six film collaborations.
- Neo4j hosts a public movie recommendations database with public username and password access.
- Llama 4 was released around the time of this April 2025 BoundaryML episode recording.
- OpenAI's o3-mini is a reasoning model that generates thinking tokens before final response output.
- Early LangChain function-calling loops printed thought parameters to console before executing the function.
- GPT-4o-mini struggles with complex Cypher query generation requiring multi-hop graph traversal reasoning.
- Reasoning tokens between special markers receive heavier attention weighting in fine-tuned reasoning models.
- BAML is the prompt definition language created by BoundaryML for structured LLM function calling.
- Neo4j's browser includes a play command showing example queries with prompts and explanations.
- Test-time compute scaling enables better answers through more pre-answer tokens rather than larger models.
- Constraint generation forcing valid JSON output can degrade model quality versus natural plaintext generation.
- Models cannot generate statistically improbable token sequences regardless of explicit prompt instructions provided.

### REFERENCES

- BoundaryML Discord community
- BAML (BoundaryML's prompt definition language)
- Neo4j public movie recommendations database
- Cypher query language
- Llama 4
- OpenAI o3-mini reasoning model
- GPT-4o and GPT-4o-mini
- Cursor IDE
- Claude (referred to as "Clots")
- LangChain function-calling implementations
- Debate prompting paper
- DeepSeek R1
- Chain-of-thought prompting paper
- Pashant (community member with graph database expertise)
- Vibe (referenced caller on the stream)
- Previous Neo4j stream with the Neo4j team

### ONE-SENTENCE TAKEAWAY

Reasoning models trade engineering time for inference cost; guided prompts win when you know your domain.

### RECOMMENDATIONS

- Whiteboard your agent loop architecture before writing code so team alignment precedes implementation decisions.
- Stream working context events to frontend letting users see model progress instead of opaque waits.
- Delete intermediate failed queries from context when final reply succeeds to keep history clean.
- Inject explicit hint messages when database returns empty rather than letting model retry blindly forever.
- Use markdown headers like Initial Reasoning and Problems With Reasoning to structure debate-style prompt scaffolding.
- Build a top-level router prompt that classifies intent before dispatching to specialized domain prompts.
- Put thought or reasoning fields first in function-calling schemas to force pre-output deliberation tokens.
- Output two reasoning fields: long internal version for model guidance plus short user-facing summary.
- Add post-LLM aliasing layer mapping fuzzy model outputs to canonical database entities and identifiers.
- Time-box live debugging sessions before pivoting to alternative approaches or fielding audience questions.
- Test prompts against intentionally hard cases like Kevin Bacon numbers to expose failure modes early.
- Blend reasoning models with guided reasoning prompts rather than choosing one exclusively for both benefits.
- Add UI checkboxes letting users decide which intermediate queries persist in their conversational context.
- Inline reasoning within single prompt instead of multi-call actor-checker loops to avoid exponential cost growth.
- Reach for reasoning models when shipping fast matters; reach for prompt engineering for cost optimization.
- Watch the previous Neo4j stream for retry handling and misspelling failure-mode techniques in production.
- Skip JSON-embedded reasoning fields; let models output reasoning before structured JSON in their natural format.
- Constrain reasoning prompts to your domain knowing they will fail on unrelated queries by design.
- Cache the database schema in prompt prefix so models always have grounding information available immediately.
- Treat reasoning name as overloaded; separate model-internal thought from UI display content from embeddings explicitly.
