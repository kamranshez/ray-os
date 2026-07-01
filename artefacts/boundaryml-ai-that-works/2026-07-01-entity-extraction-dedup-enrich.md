---
title: "Entity extraction from LLMs - extracting, deduping, enriching #10"
videoId: niR896pQWOQ
url: https://www.youtube.com/watch?v=niR896pQWOQ
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1. Entity resolution is not one model call: decompose it into extract, resolve, and enrich, and treat each as a swappable type signature you can back with a heuristic, a tiny model, or a big model.** This is the reframe every other move in the session hangs off; once you see the pipeline as typed functions, the naive prompt, the classification reduction, the F1 benchmark, and the "start small" advice all follow.
VERDICT: net-new video available.

**Spine 2. Design the output data model to steer the model's reasoning, not just to type its output: an enum field forces the model to self-classify before it names anything, which structurally kills a class of hallucinations.** The schema is doing more work than the prompt text.
VERDICT: next-step video available (complements Prompt Engineering structured-output).

**Spine 3. The hard part is not extraction, it is maintaining an ever-changing entity database: a proposed-to-committed lifecycle fed by an async enrichment agent, governed by human-in-the-loop review.** Extraction is the easy first slice; the durable system is the self-repairing store behind it.
VERDICT: net-new video available.

---

## Summary and counts

Dex (HumanLayer) and Vibb (BAML) live-code entity extraction, deduping, resolution, and enrichment in Python, decomposing it into typed functions and a self-maintaining, proposed-to-committed entity database.

Counts (one per promoted spine): 2 net-new, 1 complement, 0 partial, 0 covered.

---

## Deep dive

### Spine 1 - Entity resolution as decomposed typed functions

The claim: entity resolution is really three problems (extraction, deduping to one shared ID, enrichment), and each is a type signature you can implement with the cheapest thing that clears an accuracy bar. Most people get this wrong by mashing all three into one giant prompt ("dump every known company, pick one"), which cannot scale because, as Vibb puts it, "you can't just put it all in a prompt" on day one. The mechanism: because each subproblem is a typed function (string in, entity out; legal name in, known company out), you can benchmark it with an F1 score and then choose the cheapest backing implementation. Resolution collapses into a classification against a narrowed candidate set, so you start with a small model or a plain alias heuristic and only escalate to a big model where accuracy fails, the inverse of the usual "biggest model first" default. It generalizes cleanly: topic clustering for a news feed and auto-labeling Gmail are the same extract-then-resolve pipeline over a controlled vocabulary. How it goes wrong: over-decomposing tiny tasks adds N plus 1 latency across ten thousand emails, and a heuristic that "probably works" silently erodes accuracy unless an F1 benchmark catches it.

### Spine 2 - The schema steers the reasoning

The claim: you improve extraction accuracy by the shape of the output data model, not just the prompt text. This is non-obvious because most engineers treat structured output as a formatting concern (get valid JSON) rather than a reasoning tool. The mechanism: adding a company_type enum (well-known, well-known subsidiary, startup) forces the model to self-classify first, and that category then gates a conditional legal_name field (best guess if well-known, owning company if subsidiary, skipped entirely if startup). Because the model must commit to a category before emitting a name, a hallucinated legal name for a startup becomes structurally impossible, and the category itself doubles as a confidence signal: if the model will not say well-known, the entity probably is not in its training set. Dex names it exactly: "forcing a very specific flavor of reasoning onto the extraction process." It generalizes to any classify-then-extract task, such as support-ticket triage where a severity enum gates which follow-up fields get filled. How it goes wrong: over-constraining fights the model on genuinely ambiguous inputs (GCP kept resolving to "Google Cloud Platform"), and verbatim-from-content fields still need validation because the model drifts.

### Spine 3 - The self-maintaining entity database

The claim: the interesting, durable problem is not pulling an entity out once, it is building and maintaining a database that changes constantly. This is non-obvious because teams assume a static reference list, but real registries always lag reality (neither Human Layer nor Boundary ML shows up in most public registries "yet"). The mechanism: extraction writes each entity with status proposed and enqueues an async job (AWS SQS). An enrichment agent pulls clues from the source, generates prioritized web-search queries, runs them, and drafts a proposal; a commit policy then migrates proposed to committed and back-fills the original row. Because the data model carries status, timestamps, and a full edit log (the way git and Wikipedia keep every revision), the whole thing can be reviewed, rolled back, and repaired asynchronously. Vibb's rule: "your data model must represent the complexity of your problem." It generalizes to any growing controlled vocabulary, such as a skills-tag taxonomy or a product catalog. How it goes wrong: auto-committing AI-proposed facts to prod risks wrong data (a viewer flagged exactly this), and picking blocking versus async human review incorrectly either bottlenecks throughput or ships errors.

---

## Proposed ACS videos

### 1. Build a Self-Updating Entity Database Your AI Pipeline Can Trust
- HOOK: Extraction is the easy 10 percent; the real system is the database that keeps repairing itself.
- THE PROMISE: For engineers building LLM data pipelines, ship an entity store that grows and corrects itself safely.
- THE SHAPE:
  - Extract entities, write each with status proposed, and enqueue an async job (AWS SQS).
  - An enrichment agent pulls clues from the source, generates prioritized web searches, and drafts a proposal.
  - A commit policy migrates proposed to committed: human-in-the-loop for risky data, auto-commit for low-stakes search enrichment.
  - Store status, timestamps, and a git or Wikipedia style edit log so rows roll back and repair.
  - Back-fill the original extraction row once the entity is committed.
- SPINE: 3
- SLOT: Business class, new chapter "LLM Data Pipelines".
- RELATIONSHIP: net-new. The closest catalog item, deep-research-with-exa (Business backlog), builds a one-shot research agent; ACS has nothing on the proposed-to-committed governance lifecycle that turns research into a maintained store.
- PROOF TO REUSE: the "look up info on Boundary ML, row 51" SQS walkthrough; Dex's "two kinds of human in the loop" (block until reviewed vs commit-then-edit); "your data model must represent the complexity of your problem" and the git/Wikipedia edit-log analogy.

### 2. Stop Writing One Giant Prompt: Turn Extraction Into Typed Functions
- HOOK: The reason your extraction prompt keeps failing is that it is secretly three problems wearing one trench coat.
- THE PROMISE: For anyone pulling structured data out of LLMs, decompose the task so each piece uses the cheapest thing that works.
- THE SHAPE:
  - Split entity resolution into extract, dedupe/resolve, and enrich; write each function signature first.
  - Treat each call as a type signature with a heuristic, a tiny model, or a big model behind it.
  - Collapse resolution to a classification against a narrowed candidate set, not the whole database.
  - Reverse the default: start small because you already know all entities never fit one prompt.
  - Benchmark the pipeline with an F1 score, collect data, and later train a tiny model.
- SPINE: 1
- SLOT: Techniques class, new chapter "LLM App Engineering" (or Business).
- RELATIONSHIP: net-new. test-time-compute and the-ambiguity-line teach model selection and routing for coding agents; neither teaches decomposing a production extraction task into swappable typed functions.
- PROOF TO REUSE: "this stuff is pretty much just functions"; "most problems that have an entity resolution problem can't do this on day one, you can't just put it all in a prompt"; the naive ask_lm to runtime-guard to classification progression; the alias heuristic used deliberately instead of an LLM.

### 3. Your Schema Is a Prompt: Make the Model Reason Through Its Output Type
- HOOK: One enum field did more for extraction accuracy than five rounds of prompt tweaking.
- THE PROMISE: For prompt engineers, use the output data model to steer reasoning and structurally block a class of hallucinations.
- THE SHAPE:
  - Add a company_type enum (well-known, well-known subsidiary, startup) so the model self-classifies before naming anything.
  - Gate a conditional legal_name on that category; skip it entirely for startups so garbage never appears.
  - Read the category as a confidence signal: if the model refuses well-known, it is probably not in training.
  - Keep a verbatim-from-content name field, then validate it against your database.
- SPINE: 2
- SLOT: Prompt Engineering class, structured-output foundation chapter.
- RELATIONSHIP: complements "structured-output" (PE Foundations), which teaches getting typed JSON out of a model. This is the next step: designing the schema to force a flavor of reasoning and prevent hallucinations, not merely to format output.
- PROOF TO REUSE: "forcing a very specific flavor of reasoning onto the extraction process"; the optional legal_name "skip if startup" trick; the GCP-resolves-to-"Google Cloud Platform" failure that motivates the enum.

---

## Full wisdom (reference)

### SUMMARY
Dex (HumanLayer) and Vibb (BAML) live-code entity extraction, deduping, resolution, and enrichment in Python, decomposing it into typed functions and a self-maintaining, proposed-to-committed entity database.

### IDEAS
- Entity resolution splits into three separate problems: extraction, deduping to one shared ID, and later enrichment.
- Mixing those smaller problems into one giant problem makes entity resolution far harder than actually necessary.
- The naive approach dumps every known company into the prompt and asks the model to pick.
- A runtime guard rejects any answer not in the options list, adding error context then retrying.
- By definition you cannot fit every legal company into one prompt, so classification against candidates wins.
- Start with a small tight model, then zoom out to a bigger model only when needed.
- A company_type enum (well-known, well-known subsidiary, startup) forces the model to self-classify before naming the company.
- Making legal_name optional and skipped for startups prevents the model from hallucinating fake corporate legal names.
- If the model refuses well-known, that itself signals the entity likely isn't in its training set.
- Enrichment runs as a separate async pipeline that scrapes the web to build candidate entity proposals.
- A proposed-versus-committed status lets a separate agent or human promote new entities into the real database.
- Extract clues from the resume first, then generate prioritized web-search queries ranked by which to run.
- Swap raw URLs for indexed IDs like idx0 so the model emits fewer, more stable tokens.
- Two human-in-the-loop flavors exist: block until reviewed, or commit now and let anyone edit it later.
- Keep a full edit log per row, like git or Wikipedia, so changes roll back easily.
- Topic clustering and Gmail auto-labeling are the exact same entity-resolution pipeline over a controlled tag vocabulary.
- The system can be benchmarked with an F1 score, enabling data collection and tiny-model training later.

### INSIGHTS
- LLM calls are just type signatures; the implementation can be a heuristic, tiny model, or giant.
- The interesting problem is maintaining an entity database that changes constantly, not the one-time extraction step.
- Your data model must represent the problem's true complexity, including drafts, statuses, and full revision history.
- The output schema forces a specific flavor of reasoning, doing more work than the prompt text.
- Resolution reduces to classification: narrow candidates, then apply the same techniques a classification video already teaches.
- Reduce the entropy of strings the model emits so downstream extraction stays stable and highly reliable.
- Choose model size by constraints: ship with the best model, then pare down where cost bites.
- Whether a given step uses an LLM or a plain heuristic is the developer's engineering prerogative.
- Most of this is just software engineering; get that right and it beats one-size-fits-all RAG easily.
- Public registries always lag reality, so a real entity system must enrich and grow itself continually.

### QUOTES
- "It's about how do you build and maintain an entity database that is changing ever so often all all the time." (Vibb)
- "This is almost like forcing a very specific flavor of reasoning onto the extraction process." (Dex)
- "Most problem that have an entity resolution problem can't do this on day one. You can't just put it all in a prompt." (Vibb)
- "It's really important that your data model represent the complexity of your problem." (Vibb)
- "If you can do the software engineering behind this, you can build the tool that fits your problem and it's going to work a lot better than one of these like one-size-fits-all just like rag against a thing and push it in and hope it works." (Vibb)
- "Use the biggest model and the biggest prompt and the most powerful thing first and then break it down when it becomes a performance bottleneck." (Dex)
- "This stuff is pretty much just functions." (Vibb)
- "You just need to find the right data model that represents the complexity of your task." (Vibb)
- "You want to reduce the noise or like entropy of those strings to be as stable as possible." (Vibb)
- "It's up to me as the developer of this application to decide the requirements for this task." (Vibb)
- "There's two kinds of human in the loop." (Dex)
- "Languages might not need a standard library anymore because technically everything can be an LLM function." (Vibb, quoting engineer Antonio)

### HABITS
- They write the function signature first because it clarifies inputs, outputs, and the real problem shape.
- They add explicit test cases early, including a deliberately ambiguous one, before iterating on the model.
- They deliberately keep a cheap alias-matching heuristic instead of an LLM wherever accuracy still allows it.
- They turn on a Python type checker during development because static analysis catches bugs for them.
- They iterate on a small subset of a hundred records before scaling up to many thousands.
- They constrain each function's input scope so test cases cover only cases that are actually reached.
- They routinely print before-and-after states while debugging pipelines rather than trusting the code silently just worked.
- They push all session code to a public repo so viewers can run it themselves afterward.

### FACTS
- Boundary ML and Human Layer are not in most public registries, though both appear on Crunchbase.
- The naive retry function defaults to three tries before giving up or escalating to a human.
- Wikipedia keeps track of every edit a human makes so revisions can be rolled back easily.
- GPT-4o mini kept resolving GCP to Google Cloud Platform rather than to the parent company Google.
- A Barnes and Noble Nook contract cleanup collapsed forty scattered Adobe entries into two aggregate categories.
- That Barnes and Noble project involved roughly ten thousand Adobe contracts, some paid but never used.
- BAML currently supports only LLM APIs, and not embedding models like BERT or ALBERT for now.
- The system's accuracy can be measured numerically as an F1 score across a benchmark test set.

### REFERENCES
- BAML (Boundary ML) structured-output framework; Human Layer (Dex's company).
- 12-factor agents (referenced by Dex as his engineering philosophy).
- Prior "AI that works" episodes: classification, eval (runtime guards), policy-to-props, prompt hacking.
- Tools and services: AWS SQS, Tavily, Exa API, Ollama (Llama latest), GPT-4o mini, o4-class models.
- Concepts and analogies: F1 score, ATS systems, git, Wikipedia edit history, Crunchbase.
- People: engineer Antonio (LLM-as-standard-library riff), Michaela (Tavily-on-empty-field example).

### ONE-SENTENCE TAKEAWAY
Decompose entity resolution into swappable typed functions, then build a self-maintaining database that enriches itself.

### RECOMMENDATIONS
- Write the function signature and a deliberately ambiguous test case before touching any prompt or model.
- Add an enum type field to force the model to self-classify before extracting any downstream fields.
- Make dependent fields optional and skip them for categories where a value would be hallucinated garbage.
- Reduce entity resolution to classification against a narrowed candidate list instead of the whole entity database.
- Validate every LLM-returned name against your known database and invalidate anything that fails to match cleanly.
- Give each proposed entity a status column and migrate proposed to committed through a review policy.
- Build an async enrichment job that extracts clues then generates prioritized web-search queries for missing entities.
- Have the model output indexed IDs instead of raw URLs to keep extracted strings more stable.
- Benchmark the pipeline with an F1 score, collect data, then train a tiny task-specific model later.
- Choose blocking human review for risky data and async batch review for low-stakes search enrichment tasks.
