---
video_id: niR896pQWOQ
title: "Entity extraction from LLMs - extracting, deduping, enriching -🦄 Ep #10"
url: https://www.youtube.com/watch?v=niR896pQWOQ
channel: BoundaryML
---

### SUMMARY

Dex from Human Layer and Vibhav from BoundaryML demonstrate entity extraction, deduplication, resolution, and enrichment pipelines using BAML on resume parsing examples.

### IDEAS

- Entity resolution mixes three distinct subproblems together, making the overall system far harder than necessary.
- Always map varied input strings like Xbox, MSFT, Microsoft, misspellings to one canonical database entity ID.
- Naive approach passes a candidate options list and asks the LLM to pick best.
- Add runtime guards verifying LLM choice exists in options, retrying with error context when invalid.
- Database of valid entities is always incomplete on day zero, requiring an enrichment pipeline alongside.
- Use a separate independent pipeline that scrapes web, finds candidates, then proposes new entities asynchronously.
- Caller decides resolution behavior: escalate humans, return none, retry, or kick web search jobs.
- Force specific reasoning flavors onto extraction by structuring data model fields like company type explicitly.
- Classify extracted entities as well-known, well-known subsidiary, or startup to filter likely hallucinations.
- Skip legal name extraction for startups since the model would hallucinate garbage data anyway.
- Bigger ATS databases cannot fit all companies in one prompt, so classification must narrow first.
- Treat entity validation as a classification problem against a small relevant subset, not full database.
- Maintain alias dictionaries mapping legal names to many surface forms like Microsoft, MSFT, Xbox.
- Use cheap heuristics like alias dictionary lookup before escalating to expensive LLM classification calls.
- Invalidate any LLM-returned legal name not matching your trusted database before downstream consumption.
- Enrichment pipeline pushes proposed-status rows into database, separate agent promotes proposed to committed.
- Wikipedia keeps every edit; Git tracks history; your data model must represent task complexity faithfully.
- Topic clustering, Gmail labeling, hierarchical news categories are all the same entity resolution problem underneath.
- Multi-entity grouping just returns an array, then runs identical validation checks per element with flattening.
- Extract company clues from raw resume text, then convert clues into prioritized targeted Google search queries.
- Have models output indexed IDs instead of full URLs; URL tokens corrupt outputs and reduce reliability.
- Function type signatures decouple implementation from callers, letting you swap heuristics, tiny models, or GPT-4.
- Collect production data, train tiny task-specific models, evaluate against F1 benchmarks, iterate until constraints satisfied.
- Async or batch human-in-the-loop fits enrichment well; commit immediately and let reviewers edit later.
- Future programming may replace standard library calls like URL encoding with LLM function invocations entirely.
- Status fields like proposed and ready let humans promote entities through review stages safely.
- Build internal web UIs sorted by last-updated so colleagues can manually promote entity proposals quickly.
- Risk level dictates rigor: tax data needs human review; resume search enrichment can auto-commit cheaply.
- Restrict function input scope through software contracts so test cases reflect realistic narrow input distributions.
- Choose smaller faster models for narrow validated subproblems; reserve large models for ambiguous high-stakes work.
- Iterate on hundred-record subsets first, learn small-model limits, then scale to thousands or millions.

### INSIGHTS

- Decomposing entity resolution into extraction, deduplication, classification, and enrichment unlocks tractable engineering instead of monolithic AI complexity.
- Type signatures abstract implementation, letting heuristics, embeddings, or frontier models substitute behind identical contracts as constraints evolve.
- Force-structuring outputs with reasoning categories like well-known versus startup filters hallucinations cheaply without expensive validation rounds.
- Database completeness is dynamic; treat entity tables as living state with proposed, committed, and human-reviewed status flags.
- Most production entity problems share one shape: surface forms map to canonical IDs through alias dictionaries plus enrichment.
- Cheap deterministic heuristics often suffice; reserve LLM calls for genuine ambiguity, not for problems string matching solves.
- Asynchronous enrichment via job queues separates fast extraction paths from slow web-search-driven entity discovery workflows.
- Your data model must mirror real-world ambiguity; multiple drafts, edit history, and review states reflect actual workflow.
- Software engineering rigor beats one-size-fits-all RAG when problems have clear structure and known data constraints.
- Start with biggest models and prompts to ship fast; optimize down only when measurable cost or latency demands it.
- Collecting production data plus benchmarks creates a training loop that gradually replaces LLMs with cheaper specialists.
- Hierarchical entity systems compose naturally: same algorithm runs at each level, returning arrays then flattening upward.
- Indexed IDs outperform URLs as model outputs because token entropy degrades extraction reliability under query-string complexity.
- LLM functions may eventually replace deterministic library calls when compute economics shift like RAM economics did.
- Human-in-the-loop comes in two flavors: blocking pre-commit review versus async post-commit corrective editing freedom.

### QUOTES

- "All of these kind of map to the same entity as far as I'm concerned." — Vibhav
- "It's about how do you build and maintain an entity database that is changing ever so often." — Vibhav
- "Peak working hours they make all the models dumber. It's my new conspiracy theory." — Vibhav
- "Skip if startup." — Vibhav
- "If you can do the software engineering behind this, you can build the tool that fits your problem." — Vibhav
- "It's mostly engineering." — Vibhav
- "Use the biggest model and the biggest prompt and the most powerful thing first." — Dex
- "It would be wasteful for me to go even write the base prompt because by definition I can't do it." — Vibhav
- "Match is pretty freaking cool." — Vibhav
- "Your data model represent the complexity of your problem." — Vibhav
- "Wikipedia for example, they keep track of every edit that every human makes." — Vibhav
- "It's really up to me as the developer of this application to decide the requirements." — Vibhav
- "Shipping your product is way more important than cost in the very beginning." — Vibhav
- "Get it tight on a small subset, figure out what you can do with smaller models." — Dex
- "All of this whole thing just becomes like a workflow that we've built out." — Vibhav
- "Languages might not need a standard library anymore because everything can be an LLM function." — Vibhav
- "Slack using 70 gigs of RAM would have been insane 10 years ago." — Vibhav
- "Tokens get completely screwed and hard to go extract." — Vibhav
- "If it's a startup, I always need to do an agentic workflow." — Vibhav
- "Once you do the classification, you're basically able to go move on." — Vibhav
- "The 12-factor agent stuff is all about let's get right in the weeds and engineer everything." — Dex
- "All we're doing is designing API contracts that have some guaranteed data model." — Vibhav
- "It's a very very general problem." — Vibhav
- "Resolving something to the same shared ID is generally useful when things have many multitudes of inputs." — Vibhav
- "Every laptop's got enough. We just go spend the RAM." — Vibhav

### HABITS

- Pull latest repo before starting any live coding session to avoid conflicts on shared examples.
- Write function signatures first to anchor design conversations before implementation begins.
- Build toy examples deliberately because production examples overwhelm audience digestion during pedagogical walkthroughs.
- Add test cases immediately when extracting structured data so regressions surface during iterative prompt edits.
- Print intermediate results during pipeline debugging instead of stepping through with interactive Python debuggers.
- Run static type checkers continuously to catch refactoring bugs early in evolving extraction pipelines.
- Drop comments at function boundaries clarifying scope assumptions when input distributions could change later.
- Default to large models initially, then progressively swap to smaller specialists once benchmarks confirm coverage.
- Iterate on hundred-example subsets before scaling pipelines to thousands or millions of records.
- Maintain alias dictionaries mapping canonical names to surface variations encountered in real data over time.
- Push proposed entities through async review queues notifying Slack channels for batched human approval.
- Track every database edit with timestamps and reviewer attributions to enable rollback investigations later.
- Sort internal admin tables by last-updated column so reviewers process newest proposals first.
- Reserve LLM calls for ambiguous cases; default to deterministic alias matching for cheap straightforward lookups.
- Collect production traces continuously to feed F1 benchmarks driving smaller-model training and validation.

### FACTS

- BAML is a domain-specific language for structured LLM outputs developed by BoundaryML.
- Microsoft owns Xbox as a subsidiary, illustrating common entity hierarchy collapsing in resolution tasks.
- GCP stands for Google Cloud Platform, owned by Alphabet Inc., not Google LLC directly.
- Slack desktop application reportedly uses around seventy gigabytes of RAM during typical operation.
- Wikipedia maintains every individual edit ever made, enabling fine-grained rollback of any change.
- Git tracks complete file history through commits, enabling precise rollback of code changes anytime.
- F1 score is a numerical benchmark combining precision and recall for classification system evaluation.
- AWS SQS provides queue infrastructure commonly used for asynchronous job dispatching in enrichment pipelines.
- BERT and Albert are embedding-style models distinct from generative LLMs supported by BAML currently.
- Tavily is a web search API used for retrieving real-time context during LLM enrichment workflows.
- Crunchbase is a public company registry where startups list themselves for funding tracking purposes.
- Barnes and Noble Digital Nook had ten thousand Adobe contracts collapsed into forty unique categories.
- Python's match statement supports OR patterns using pipe syntax in case clauses since version 3.10.
- Recursion isn't typically idiomatic in Python for retry loops compared to standard while constructs.
- Human Layer is Dex's company building safer, more useful agents through human approval workflows.

### REFERENCES

- BAML by BoundaryML
- Human Layer (Dex's company)
- AI That Works podcast
- Crunchbase
- AWS SQS
- BERT, Albert embedding models
- Tavily search API
- Antonio's expose on LLM URL encoding
- Wikipedia edit history model
- Git version control
- Sean's question on entity linking spans
- Michaela's web search BAML example
- Earlier eval episode of AI That Works
- Earlier classification episode of AI That Works
- Twelve-factor agents framework
- GPT-4 Mini, Llama latest, Ollama
- Cursor IDE debugger

### ONE-SENTENCE TAKEAWAY

Decompose entity resolution into extraction, classification, validation, and enrichment with type signatures and database state.

### RECOMMENDATIONS

- Split entity resolution explicitly into extraction, deduplication, validation, and enrichment subproblems before writing any code.
- Define function type signatures first so implementation choice stays flexible across heuristics and frontier models.
- Add runtime guards that verify LLM-chosen identifiers belong to your trusted options list every time.
- Structure your output schema to force categorization fields like well-known versus startup before legal name extraction.
- Maintain an alias dictionary mapping canonical legal names to all observed surface variations across data.
- Use cheap deterministic alias matching first; escalate to LLM classification only when straightforward lookups fail.
- Build a separate enrichment pipeline kicked off via SQS jobs whenever extraction produces unrecognized entity candidates.
- Add status columns like proposed and committed to entity tables so humans gate sensitive promotions safely.
- Surface internal admin dashboards sorted by last-updated so reviewers process newest proposals efficiently.
- Mirror Wikipedia and Git: track every edit with reviewer attribution to enable rollback investigations later.
- Start with the largest available model to ship quickly; optimize downward only when constraints demand it.
- Collect production traces continuously, build F1 benchmarks, iterate on smaller specialist models against them.
- Iterate prompts and pipelines on hundred-example subsets before scaling to thousand-record or million-record runs.
- Have models emit indexed IDs instead of URLs to avoid token entropy corrupting downstream extraction reliability.
- Generate prioritized search queries from extracted entity clues, then run high-priority queries in parallel batches.
- Use match statement with OR patterns in Python for cleaner multi-case entity-type dispatch logic.
- Skip legal name extraction entirely for startup-classified entities since hallucinated answers are guaranteed garbage.
- Restrict function input scope via software contracts so test cases reflect realistic narrow distributions accurately.
- For low-risk enrichment, auto-commit and notify Slack; for tax-grade data, require pre-commit human review.
- Treat topic clustering, label resolution, and category assignment as instances of the same entity resolution pattern.
