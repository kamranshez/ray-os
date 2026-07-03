---
title: "Ch 14: Knowledge Retrieval (RAG) -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "14"
pattern: "Knowledge Retrieval (RAG)"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 14: Knowledge Retrieval (RAG)** - Antonio Gulli

> Two net-new videos: (1) build a docs-grounded Q&A bot end-to-end with Claude Code, and (2) build an Agentic-RAG retrieval skill that validates sources and reconciles conflicts before answering. GraphRAG is a lighter third.

## The one idea worth a video

- **RAG turns a closed-book LLM into an open-book one by retrieving external chunks and stapling them onto the prompt before generation.** This is the spine because embeddings, chunking, semantic search, vector DBs, and citations are all just the plumbing that serves this one retrieve-then-augment move. VERDICT: ❌ net-new video available (ACS teaches codebase retrieval, never a build-your-own RAG feature).
- **Agentic RAG puts a reasoning agent BETWEEN retrieval and generation - it interrogates the retrieved chunks for freshness, reconciles contradictions, decomposes multi-part questions, and reaches for tools when the knowledge base has a gap.** Distinct demo, distinct "one thing after," so it de-merges from plain RAG. VERDICT: ❌ net-new video available.
- **GraphRAG swaps the vector store for a knowledge graph so the agent can traverse explicit entity relationships and answer questions whose evidence is fragmented across many documents.** VERDICT: ❌ net-new (lighter, listed as also-film-able).

## Summary + counts

RAG grounds LLMs in external data by retrieving semantically relevant chunks and augmenting the prompt; Agentic RAG and GraphRAG add reasoning and relationship-aware retrieval for reliability.

🔴 3 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - Retrieve-then-augment (build a RAG feature)
THE CLAIM: instead of sending a user's question straight to the model, first search an external knowledge base, pull the most relevant "chunks," and append them to the prompt so the answer is grounded in verifiable data. WHY IT'S NON-OBVIOUS: the intuitive fix for "the model doesn't know our docs" is fine-tuning or a bigger model; RAG argues you should leave the weights alone and change the *prompt* at query time. WHY IT'S TRUE / MECHANISM: text is embedded into vectors where "furry feline companion" lands near "a domestic cat," so a vector DB using HNSW finds meaning, not keywords; the retrieved chunk carries the fact, and the LLM merely phrases it, which is why hallucination drops and citations become possible. WHAT IT GENERALIZES TO: for ACS this is the canonical "build an internal-docs Q&A bot" business feature - chunk a manual, embed to Chroma/pgvector, wire a retriever, prompt with the context. The book's own LangChain+Weaviate walkthrough (`CharacterTextSplitter`, `chunk_size=500`, `retriever.invoke`) is a ready demo skeleton. HOW IT GOES WRONG: the answer spans multiple chunks the retriever never co-locates, or irrelevant chunks add noise and confuse the model; and the whole corpus needs periodic re-indexing to stay current.

### Spine 2 - Agentic RAG (a reasoning gatekeeper over retrieval)
THE CLAIM: bolt a reasoning agent between retrieval and generation so it actively "interrogates" the retrieved data for quality, recency, and completeness rather than passively trusting it. WHY IT'S NON-OBVIOUS: standard RAG treats the top-k results as ground truth; Gulli argues the retriever is often wrong or conflicting, so the pipeline needs judgment, not just similarity. WHY IT'S TRUE / MECHANISM: the book gives four concrete moves - reflection/source-validation (discard the 2020 blog, keep the 2025 policy via metadata), conflict reconciliation (a €50,000 proposal vs a €65,000 finalized report -> trust the report), query decomposition (compare our features+pricing vs Competitor X's = four sub-searches synthesized), and gap-filling with tools (nothing in the weekly-updated base about yesterday's launch -> call a live web-search API). Each step adds a decision the vanilla retriever cannot make. WHAT IT GENERALIZES TO: this is the most ACS-native idea in the chapter - it is a retrieval *skill/subagent* you build in Claude Code that reads candidate docs, checks dates, flags contradictions, and only then answers. HOW IT GOES WRONG: the agent loops uselessly, misjudges relevance and discards the right doc, and adds latency plus cost per Gulli's own "challenges" section.

### Spine 3 - GraphRAG (relationship-aware retrieval)
THE CLAIM: replace the vector store with a knowledge graph so the agent answers by traversing explicit edges between entities, solving RAG's classic failure of evidence fragmented across documents. MECHANISM: nodes are entities, edges are relationships; a query walks the graph (company -> market event, gene -> disease) instead of hoping semantically-near chunks happen to contain the full picture. WHAT IT GENERALIZES TO: for a coding audience the buildable version is smaller - extract entities/relations from a repo or doc set into a graph, then let the agent hop it. HOW IT GOES WRONG: Gulli is blunt that graph construction is costly, brittle, and higher-latency, and the whole thing is only as good as the graph's completeness - which is why this is the lightest of the three.

## 🎬 Proposed ACS videos

### 1. Build an Agentic RAG That Fact-Checks Its Own Sources
- **HOOK:** Your docs bot confidently quoted a policy that was retired in 2020 - here is the reasoning layer that would have caught it.
- **THE PROMISE:** For anyone shipping a retrieval feature, you will build a Claude Code skill/subagent that validates recency, reconciles conflicting sources, and only then answers.
- **THE SHAPE:** (1) Seed a corpus with a deliberate trap - a 2020 blog and a 2025 policy that disagree; (2) show naive RAG returning the wrong one; (3) build a retrieval subagent that inspects metadata and prioritizes the authoritative source; (4) add conflict-reconciliation (€50k proposal vs €65k report -> pick the report); (5) add a gap-detection branch that fires a web-search tool when the base has nothing recent.
- **SPINE:** Spine 2 (Agentic RAG).
- **SLOT:** Advanced Techniques -> new chapter "Retrieval & Grounding" (or For Business).
- **RELATIONSHIP:** ❌ net-new. ACS teaches agentic retrieval over a *codebase* (Explore subagent, The Context Layer) but has no video on building a validating retrieval agent over external knowledge with conflict/recency logic.
- **PROOF TO REUSE:** The four Agentic-RAG scenarios verbatim (source validation, the €50,000/€65,000 reconciliation, the four-way competitor decomposition, the "market reaction to yesterday's launch" gap-fill).

### 2. Ship a Docs-Grounded Q&A Bot End to End
- **HOOK:** Stop fine-tuning to teach a model your handbook - retrieve the answer at query time and cite the source.
- **THE PROMISE:** For a business builder, you will stand up a working Q&A bot over your own PDFs/wiki - chunk, embed, retrieve, augment, answer with citations.
- **THE SHAPE:** (1) Load and chunk a real manual; (2) embed into a local vector store (Chroma/pgvector); (3) wire a retriever; (4) prompt-template the retrieved context; (5) prove grounding by asking a question only the docs can answer, then show the citation.
- **SPINE:** Spine 1 (retrieve-then-augment).
- **SLOT:** For Business -> "Internal Knowledge & Q&A."
- **RELATIONSHIP:** ❌ net-new. "1M Token Context" uses huge context as an intake layer, but that is stuff-it-all-in, not a retrieval pipeline over an unbounded corpus with citations.
- **PROOF TO REUSE:** The LangChain/Weaviate skeleton (`CharacterTextSplitter` chunk_size=500/overlap=50, `retriever.invoke`, the concise 3-sentence answer template); the "cat" vs "kitten" vs "car" embedding intuition; the hallucination-reduction and citation benefits.

### Also film-able (not deep-dived)
- **GraphRAG for multi-hop questions (Spine 3):** build a small entity/relationship graph from a doc set and let the agent traverse it to answer a question no single chunk contains - contrast latency/cost against vector RAG. Net-new but niche; good as an Advanced Techniques one-off.

## 📚 Full wisdom (reference)

### SUMMARY
Gulli explains RAG: retrieve semantically relevant external chunks, augment the prompt, and ground LLM answers in verifiable data; Agentic RAG and GraphRAG add reasoning and relationships.

### IDEAS
- LLM knowledge is frozen at training time, missing real-time, proprietary, and specialized information.
- RAG lets an LLM "look up" information before answering, like consulting a book.
- The query hits the knowledge base first, not the LLM directly.
- Retrieval uses semantic search that understands intent, not just keyword matching.
- Retrieved chunks are appended to the prompt, creating a richer augmented query.
- RAG reduces hallucination by grounding responses in retrievable, verifiable sources.
- Citations pinpoint the exact source, raising trust and verifiability.
- Embeddings are numeric vectors placing similar-meaning text close together in space.
- Semantic distance is the inverse of semantic similarity; RAG finds smallest-distance chunks.
- Chunking breaks big documents into focused pieces so retrieval stays fast and relevant.
- Vector search, keyword BM25, and hybrid search are the three retrieval techniques.
- Hybrid search fuses BM25 precision with semantic understanding for robust retrieval.
- Vector databases (Pinecone, Weaviate, Chroma, Milvus, Qdrant) store embeddings for semantic search.
- HNSW, FAISS, and ScaNN are the algorithms/libraries powering fast vector search.
- RAG fails when the answer is fragmented across multiple chunks or documents.
- GraphRAG uses a knowledge graph to traverse explicit relationships between entities.
- Agentic RAG inserts a reasoning agent that validates, reconciles, and refines retrieved data.
- An agent can decompose a complex question into sub-queries then synthesize the results.
- An agent can detect a knowledge gap and call an external tool like web search.
- Advanced RAG variants trade added complexity, latency, and cost for reliability.

### INSIGHTS
- RAG changes the prompt at query time instead of retraining the model's weights.
- The retriever, not the LLM, is what actually carries the fact.
- Similarity search finds meaning even when wording shares no words.
- Retrieval quality caps answer quality - noisy chunks confuse the model.
- The hard problems are conflicting and fragmented sources, not single-fact lookup.
- Agentic RAG converts a passive pipeline into an active problem-solving loop.
- Metadata (dates, authority) lets an agent rank sources beyond similarity.
- Every reliability upgrade in this chapter costs latency and tokens.
- Knowledge bases require periodic reconciliation or they silently go stale.
- Graphs beat vectors precisely where relationships, not raw similarity, matter.

### QUOTES
- "Instead of relying solely on their internal, pre-trained knowledge, RAG allows LLMs to 'look up' information, much like a human might consult a book or search the internet." - Gulli
- "This search is not a simple keyword match; it's a 'semantic search' that understands the user's intent and the meaning behind their words." - Gulli
- "while other techniques search for words, vector databases search for meaning." - Gulli
- "an 'agent'—a specialized AI component—acts as a critical gatekeeper and refiner of knowledge." - Gulli
- "An Agentic RAG would identify this contradiction, prioritize the financial report as the more reliable source, and provide the LLM with the verified figure." - Gulli
- "it transforms LLMs from closed-book conversationalists into powerful, open-book reasoning tools." - Gulli

### HABITS / PRACTICES
- Chunk large documents by section/paragraph to preserve context before embedding.
- Set SIMILARITY_TOP_K and a vector-distance threshold to control retrieval breadth.
- Use hybrid search to combine keyword precision with semantic recall.
- Attach citations so every grounded answer is traceable to a source.
- Periodically re-index evolving sources like company wikis to prevent staleness.
- Have the agent check source metadata before trusting a retrieved chunk.

### FACTS
- The seminal RAG paper is Lewis et al. (2020), arXiv 2005.11401.
- HNSW (Hierarchical Navigable Small World) is a common vector-search index algorithm.
- FAISS is from Meta AI; ScaNN is from Google Research.
- pgvector adds vector search to Postgres; Redis and Elasticsearch also support it.
- BM25 is a keyword algorithm ranking by term frequency without semantic understanding.
- Vertex AI RAG exposes SIMILARITY_TOP_K and VECTOR_DISTANCE_THRESHOLD parameters.
- The GraphRAG survey is arXiv 2501.00309.

### REFERENCES
- Papers: Lewis et al. 2020 (RAG); GraphRAG survey (2501.00309); Leonie Monigatti's LangChain RAG tutorial.
- Vector DBs: Pinecone, Weaviate, Chroma DB, Milvus, Qdrant; Redis, Elasticsearch, Postgres/pgvector.
- Libraries/algorithms: FAISS (Meta AI), ScaNN (Google Research), HNSW, BM25.
- Frameworks/tools: Google ADK, VertexAiRagMemoryService, Vertex AI RAG Corpus, google_search tool, LangChain, LangGraph, OpenAIEmbeddings, ChatOpenAI (gpt-3.5-turbo), gemini-2.0-flash-exp.

### ONE-SENTENCE TAKEAWAY
Retrieve relevant external chunks and augment the prompt so the LLM answers from verifiable data.

### RECOMMENDATIONS
- Build a Q&A bot over your own docs before reaching for fine-tuning.
- Add a reasoning agent to validate source recency and reconcile conflicts.
- Use hybrid search when exact terms and meaning both matter.
- Decompose comparison questions into sub-queries then synthesize.
- Give the agent a web-search fallback for knowledge-base gaps.
- Weigh added latency and cost before adopting Agentic RAG or GraphRAG.
- Reach for GraphRAG only when relationships across documents dominate the query.
