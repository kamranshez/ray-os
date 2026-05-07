---
video_id: 6B7MzraQMZk
title: "🦄 large scale classification: ep#1"
url: https://www.youtube.com/watch?v=6B7MzraQMZk
channel: BoundaryML
---

### SUMMARY
Vaibhav (Boundary, BAML) and Dex (Human Layer) demonstrate large-scale classification techniques using probes, vector databases, embedding text customization, and BAML dynamic enums.

### IDEAS
- AI models stuck in demo land while shipped production apps quietly use proven engineering techniques behind the scenes
- Solving hard problems with small models proves techniques scale up to frontier models effectively
- Non-probable AI systems force you to wait helplessly for the next model release
- Prompts make terrible probe points because every word edit poisons many distant outputs
- Electrical engineers add detection points to circuits; LLM pipelines deserve the same introspection probes
- The naive classification solution dumps the entire category list directly into the prompt blindly
- Structured outputs inject categories into JSON schema specially but still leave only one probe point
- Vector databases let you prune massive category lists down to manageable LLM-digestible subsets dynamically
- Hierarchical categories sound clean but create confusion because human-defined hierarchies always bleed into each other
- LLMs handle disjoint categories well but break when categories overlap with subtle nuanced differences
- The text you embed for retrieval should differ from the text you give the LLM
- Custom embedding text lets you force semantic similarity toward queries you actually want to match
- Domain experts or LLMs can generate descriptions, example queries, and keywords to enrich category embeddings
- Fine-tuning embedding models has painfully slow iteration loops compared to editing embedding text strings
- BAML aliases hide raw category names from the LLM so attention focuses purely on descriptions
- Single-word category names like account-issue and technical-issue create overlap noise that aliases eliminate
- Multi-stage classification narrows many categories to few, then picks one from the smaller set
- You can replace vector search with thumbs-up Boolean classifiers running across every category in parallel
- Smaller, simpler steps in a pipeline are easier to optimize than one giant prompt
- Treat the whole system as one function: text in, category out
- Top-K is just another knob; tune it by introspecting where the right answer disappears
- Waterfall debugging through pipeline stages tells you exactly which probe to adjust
- Smaller LLM input token counts run dramatically faster because attention is non-linear in input length
- 100,000 categories fit in memory on your laptop without needing a real vector database
- Live user feedback loops beat handwritten test sets for evolving classification systems in production
- Tracing every internal function call lets you replay why a classification decision went wrong
- Reasoning models versus reasoning prompts is the next frontier of practical AI engineering
- GPT-3.5 was already good enough for many production pipelines people never bothered to ship
- More probes increase introspection complexity slightly but eliminate the worse problem of opaque black-box prompts
- Dynamic enums let BAML guarantee output values even when categories are decided at runtime

### INSIGHTS
- Build probe points into AI pipelines so failures localize instead of cascading through opaque prompt edits
- Separate the text used for retrieval from the text used for LLM reasoning to maximize control
- Iteration speed compounds: changing strings beats changing models or fine-tuning every single time
- Compose pick-category as a function so any sub-step becomes swappable without rewriting the system
- Disjoint categories tolerate scale; overlapping categories demand small focused prompts with careful disambiguation
- Aliases strip name connotations so the LLM judges descriptions purely on meaning, not lexical overlap
- Production data from real user interactions produces evals that hand-written test sets cannot match
- Latency improves with pipelines because narrowed prompts run faster than monolithic huge-category single-shot prompts
- Engineering rigor for AI looks like circuit design: many small testable nodes, not one giant blob
- The right answer often is "it depends" — but only after you have probes to depend on
- Vector search is one implementation of pruning, not the only one; LLM pruners work too
- Tightening a model's output distribution requires adding knobs, not praying to prompting gods harder
- Direct engineer access to user feedback creates the tightest possible AI iteration feedback loop

### QUOTES
- "AI models seem to just be stuck in demo land." - Vaibhav
- "If we can do this with small models, we can probably get away with very large models." - Vaibhav
- "GPT-3.5 honestly was already pretty good for a lot of scenarios." - Vaibhav
- "The minute a system becomes non-probable, it really becomes hard to go edit." - Vaibhav
- "You're stuck waiting for GPT-26 to come out." - Vaibhav
- "The hardest part about circuits is once they get really small, you can't really introspect them." - Vaibhav
- "AI pipelines don't really get these probing points." - Vaibhav
- "Hierarchies end up bleeding over a lot more." - Vaibhav
- "Fine-tuning a model is so painfully slow in your iteration loop." - Vaibhav
- "We're trying to remove these soft edges and pull the model in closer." - Vaibhav
- "The smaller and simpler the steps are, the easier they are to optimize." - Dex
- "You actually have the worst system right now, which is a model you cannot modify." - Vaibhav
- "It's like step through debugging in code." - Vaibhav
- "Praying to the prompting gods." - Dex
- "All things in ML, the real answer is it depends." - Vaibhav
- "BAML will guarantee that this will return one of the categories in the list." - Vaibhav
- "LLMs are non-linear based on the number of input tokens you have." - Vaibhav
- "The best eval you can have is to ship this product into the user database." - Vaibhav

### HABITS
- Sketch system diagrams before writing classification code to clarify probe points and data flow visually
- Cache embeddings to a pickle file locally rather than spinning up a real vector database prematurely
- Turn on Python type checking mode by default because runtime-disappearing types still annoy careful engineers
- Trace every internal pipeline function so debugging a single bad output never requires rerunning everything
- Use BAML aliases like K0, K1, K2 to strip name bias from category disambiguation prompts
- LLM-generate initial example queries, scenarios, and keywords for each category before refining manually later
- Ship classifiers to real users early and harvest their feedback as the primary evaluation dataset always
- Write a separate small prompt for closely-overlapping category pairs instead of forcing one giant prompt
- Pause screen sharing briefly before opening any .env file containing secrets during live demos
- Rotate API keys immediately after any session where they may have been visible on screen
- Always start with the simplest pipeline shape and add probes only when failures expose real needs
- Default to small models first and reach for frontier models only after small ones genuinely fail
- Sort vector matches by cosine similarity and cap at top-K before passing anything into the LLM
- Run end-to-end traces while debugging so you see narrowed categories alongside final selection results
- Build classification as a pure function signature: text in, category out, implementation hidden behind it

### FACTS
- LLM performance degrades noticeably once routing agents must choose between more than twenty possible routes
- MCP servers can expose more than a thousand tools, which overwhelms LLM tool-selection abilities completely
- Most companies have classification systems with fewer than one hundred thousand total categories overall
- LLM inference cost scales non-linearly, roughly quadratically, with the number of input tokens given
- Boundary makes BAML, a structured-output language for LLMs guaranteeing typed outputs across model providers
- Human Layer helps companies deploy safer, more reliable AI agent applications in production environments
- BAML aliases replace category names in the prompt while preserving the original names in returned objects
- Cosine similarity over embedding vectors is the standard scoring function for vector database retrieval
- GPT-4o mini is commonly used as a small, fast LLM for classification tasks in production pipelines
- Pydantic v2 requires keyword arguments and rejects positional arguments when constructing model instances
- BAML supports dynamic enums whose values are added programmatically at runtime via type builder objects
- Boundary's observability tool was free at recording time but transitioning to paid with freemium tier soon
- The medical, regulatory, and manufacturing industries commonly require classifying hundreds of distinct categories at scale
- SVG generation has historically been the hardest task for LLMs to perform reliably across versions

### REFERENCES
- BAML (Boundary's structured-output language)
- Boundary (company building BAML)
- Human Layer (Dex's company for safer AI agent deployment)
- Excalidraw (diagramming tool used during the talk)
- OpenAI GPT-4o mini (model used in the live demo)
- GPT-3.5 (referenced as historically capable enough)
- GPT-4 image model (mentioned for SVG-style improvements)
- NumPy (used for cosine similarity computations)
- Pydantic (Python data validation library used in code)
- Cursor (AI coding editor used live)
- UV (Python package runner used to execute the script)
- MCP (Model Context Protocol, referenced for tool servers)
- Vector databases (generic, used for category pruning)
- LinkedIn (channel for sharing the next talk)
- GitHub (BAML and Human Layer repos for stars)

### ONE-SENTENCE TAKEAWAY
Build probe points into classification pipelines so failures localize and iteration speeds up dramatically.

### RECOMMENDATIONS
- Decompose large classification problems into pruning, narrowing, and selection stages with introspectable probes between each
- Store categories with custom embedding text containing example queries, scenarios, and keywords rather than raw names
- Use a separate description field for the LLM prompt that differs from the embedding retrieval text
- Apply BAML aliases to category enums so the model judges descriptions without name-overlap bias
- Cap LLM-facing category lists at a small disjoint number to keep accuracy and speed high
- Cache embeddings locally in a pickle or in-memory store before reaching for a hosted vector database
- Trace every pipeline function during development so failures point directly to the broken stage
- Generate example queries and keywords with an LLM, then refine them with a domain expert iteratively
- Allow LLMs to pick multiple candidate categories then narrow with a deterministic or secondary LLM pass
- Replace vector retrieval with parallel Boolean relevance classifiers when category descriptions vary widely in style
- Tune top-K by tracing whether the correct category appears in narrowed results before blaming the LLM
- Ship classification systems to real users and mine their feedback as your primary evaluation dataset
- Avoid hierarchical category trees unless your taxonomy is genuinely clean and non-overlapping at every level
- Write small disambiguating prompts for category pairs that frequently confuse the model in production logs
- Treat the whole pipeline as one typed function so internal implementations remain swappable over time
- Prefer string and embedding-text edits over fine-tuning since iteration loops are orders of magnitude faster
- Pause screen sharing before exposing .env files and rotate any keys visible during recorded sessions
- Use dynamic enums in BAML to guarantee outputs match runtime-defined category lists without parsing fragility
- Build unit tests at each probe layer plus end-to-end tests on the full classification pipeline
- Start with small models first and only escalate to frontier models when small ones provably fail
