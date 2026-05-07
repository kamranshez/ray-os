---
video_id: gkekVC67iVs
title: "LLMs to analyze Enron Emails: 🦄 Ep #6"
url: https://www.youtube.com/watch?v=gkekVC67iVs
channel: BoundaryML
---

### SUMMARY
Dex and Vaibhav from BoundaryML build a policy-violation detector live, processing Enron emails against JP Morgan and Sarbanes-Oxley rules using BAML pipelines.

### IDEAS
- Engineers want shadcn-style components for agents, not bootstrap frameworks that abstract control away from developers entirely.
- Policy-to-prompt is one of the highest-value AI applications, generating seven-figure businesses by codifying compliance rules through LLMs.
- Solving problems slowly and expensively first proves feasibility before optimization grinds the solution into production-ready efficient code.
- Generic policy evaluators fail because domain terminology varies wildly between companies, where words like asset mean different things.
- Picking two critical policies and building specialized pipelines beats trying to evaluate every policy with one generic prompt.
- Hardcoding reasoning steps directly into structured output schemas forces the model through specific analytical paths reliably every time.
- Reading actual data manually catches bugs that any amount of automated evaluation infrastructure would completely miss in iteration.
- The model returning null instead of valid enums signals you should give it explicit escape hatches like NotAGift.
- LLM-generated test inputs produce LLM-generated low-quality outputs, so real production data must seed your golden test sets.
- Async parallel processing with concurrency limits transforms minute-long iteration loops into ten-second feedback cycles for development.
- Progress bars become essential when scaling from ten thousand to one hundred thousand records during pipeline development cycles.
- Caching and mocking are two foundational capabilities every serious LLM developer needs for fast deterministic iteration loops.
- Most LLM application time is spent writing Python infrastructure code, not actually crafting prompts or tuning models.
- Saving each result to individual files indexed by order makes inspection vastly easier than dumping monolithic JSON blobs.
- Human-in-the-loop dashboards filtering only high-risk results scale better than perfecting model accuracy across millions of inputs.
- Building rails, pipelines, testing, and eval infrastructure beats spending days perfecting one prompt that catches every case.
- Vibe evaluations come first, real data exploration second, then deterministic test cases capture validated behavior permanently.
- Embeddings outperform LLMs for cheap pre-filtering when searching large corpora for content semantically related to specific topics.
- Three-way email forwards make compliance evaluation hard because gifts hop through individuals before reaching their final destination.
- Returning union types like Analysis or NotAGift gives models structured permission to indicate when their assumption fails.
- Try-catch around validation errors lets pipelines tolerate occasional model failures without halting entire batch processing jobs.
- Tracing the entire pipeline as a single grouped run makes debugging multi-step LLM workflows dramatically easier to inspect.
- Forty engineers attended an eight-hour Saturday workshop instead of going outside, signaling massive demand for hands-on prompt engineering.
- Fan-out architectures using SQS queues become necessary when processing five million emails because rate limits cap parallel throughput.
- The bottleneck for most pipelines is which step burns the most tokens, not overall accuracy or model intelligence levels.
- Recipient type enums with values like individual, corporation, charity force structured reasoning about who actually received the gift.
- Asking what next agentic research steps would clarify ambiguous evidence enables future tool-calling extensions of the pipeline.
- Vibe consideration of models matters less than confirming the underlying problem can actually be solved at all first.
- Companies making seven figures simply pump policy documents through LLMs against evidence and surface the violations for review.
- Greping for keywords like gift before LLM analysis dramatically reduces token spend by filtering obvious negatives instantly.

### INSIGHTS
- Specialization beats generalization when policies contain domain-specific terminology that loses nuance under generic evaluation prompts at scale.
- Iteration speed compounds, so investing minutes in parallelism, progress bars, and caching pays dividends across thousands of subsequent runs.
- Structured output schemas function as forced reasoning chains, hardcoding the analytical path you want the model to traverse.
- Real data reveals problems vibes evaluations cannot, because models often confidently misclassify edge cases like sender versus receiver gifts.
- Policy compliance at scale requires human-in-the-loop dashboards, not perfect models, since high-risk events are rare and verifiable.
- Building infrastructure first lets you change prompts deliberately later, knowing exactly what regression each modification introduces or fixes.
- Escape hatches like NotAGift union types prevent silent failures by giving models valid ways to express absent conditions.
- Eight-hour engineer engagement indicates the field genuinely lacks accessible advanced prompt engineering education despite ubiquitous tutorial content online.
- Test cases derived from real surfaced examples become deterministic guardrails ensuring known-good behavior survives future prompt or model changes.
- Three-way evidence chains demand agentic follow-up research because static prompts cannot resolve relationships between forwarded emails alone.
- Production rate limits, not model intelligence, become the actual constraint when processing millions of records through compliance pipelines.
- Saving intermediate artifacts to disk creates a fast inspection layer that monolithic blob storage architectures completely fail to provide.
- Pre-filters using regex or embeddings shrink the LLM workload dramatically while preserving recall on the policy violations that matter.
- Pipelines beat prompts because pipelines compose, mock, cache, parallelize, and version, while prompts only template strings together.
- Reading the actual data is the highest-leverage action a developer can take when an LLM pipeline produces confusing results.

### QUOTES
- "We don't need bootstrap for agents. We need shadcn for agents." — Dex
- "We need prompts that we control, not prompts that a library or framework controls." — Vaibhav
- "If you can solve the problem slowly and expensively at the start, you can grind it down later." — Vaibhav
- "If you use a bunch of LLM-generated inputs, you're going to get low-quality LLM-generated outputs." — Vaibhav
- "Spending a day building a perfect prompt is way less productive than setting up the rails." — Dex
- "We're going to create a thousand AI companies this year just by showing people simple stuff." — Dex
- "I'd just look at the freaking data — most people skip that step entirely." — Vaibhav
- "Policy to prompt is the theme — turning guidelines into AI pipelines that mimic them." — Dex
- "We don't use type checking in this house — I'll turn it off just to trigger you." — Dex
- "Caching and mocking are two key things every LLM developer will need long-term." — Vaibhav
- "Now we have a thing that's pretty good — let's stop and write some Python code." — Vaibhav
- "We can hardcode that in cursor rule files — there is one I can share later." — Vaibhav
- "Using an LLM for copy-paste is really a great approach — write it yourself instead." — Vaibhav
- "Caught some real scenarios that looked high risk and I just put a human in the loop." — Dex
- "Spend most of our time writing the Python part, very little on the AI part." — Vaibhav
- "Read the email — no amount of evals would catch this until you actually look." — Vaibhav
- "We just want to invest time in workload first before worrying about model size." — Vaibhav
- "If the problem can't be solved, it doesn't matter what models can do it." — Vaibhav
- "44 emails — we can use an LLM, this isn't going to be a big deal." — Vaibhav
- "I want record replay because most people don't have good data sets initially." — Vaibhav

### HABITS
- Read individual data points manually before writing any evaluation infrastructure or attempting to optimize the pipeline further.
- Build deterministic pytest cases for every confirmed-good example you discover during manual data review and exploration sessions.
- Save intermediate artifacts as individual files indexed by order rather than dumping into one giant JSON blob structure.
- Wrap async LLM calls in semaphores limiting concurrency to ten parallel requests to respect provider rate limits gracefully.
- Add tqdm progress bars when batch sizes exceed ten thousand items so iteration loops give immediate visible feedback.
- Group multi-step pipeline traces into single runs so debugging surfaces complete context rather than fragmented individual call logs.
- Use try-catch around validation errors so one model failure does not crash entire batch processing pipeline jobs.
- Filter cheaply with regex or string contains before invoking expensive LLM calls on every record in the dataset.
- Return union types with explicit NotAGift escape hatches so models can structurally indicate when conditions do not apply.
- Cache LLM responses aggressively during iteration so unchanged prompts do not re-spend tokens on identical inputs across runs.
- Hardcode reasoning steps as fields in the structured output schema rather than relying on free-form chain-of-thought prompting.
- Mock the LLM boundary cleanly so Python pipeline code can be tested without round-tripping to real model APIs.
- Start with vibe evaluations on real data before investing in formal evaluation infrastructure or golden test set construction.
- Keep policies scoped narrowly per pipeline so domain terminology nuances stay contained within specialized prompt contexts.
- Run pipelines on small samples like ten thousand emails before scaling to hundreds of thousands or millions records.

### FACTS
- The Enron email dataset published by CMU contains roughly 1.7 gigabytes of sent messages from company employees historically.
- Sarbanes-Oxley was published by the SEC in the early 2000s establishing corporate accountability rules after major accounting scandals.
- Enron collapsed because executives engaged in widespread fraud and shady accounting practices that eventually destroyed the entire company.
- JP Morgan published a 2004 code of conduct covering gifts, public statements about business, and finance disclosure requirements.
- BoundaryML hosted an eight-hour AI That Works workshop attended by forty engineers on a Saturday afternoon.
- The word asset means different things in different financial contexts including macro trading, oil fields, bonds, and crypto.
- FINRA, SEC guidelines, and European accounting laws are common policy domains where AI compliance startups generate seven-figure revenue.
- Processing five million emails through any LLM pipeline runs into rate limits before computational cost becomes the bottleneck.
- Async.io with semaphore-controlled concurrency of ten requests reduced 44-email processing from minutes to roughly ten seconds.
- The 12 Factor Agents methodology was taught from scratch during the BoundaryML eight-hour deep-dive workshop session.
- DeepSeek and Qwen models follow strict enum instructions less reliably than GPT-4 in BoundaryML's structured output testing.
- Embeddings provide semantic pre-filtering that runs orders of magnitude faster than full LLM evaluation across entire corpora.
- Amazon SQS queue infrastructure becomes necessary architecture when scaling LLM pipelines to process millions of records reliably.
- Vibhav and Dex run a recurring AI That Works podcast where each episode tackles a practical AI engineering problem live.
- The Enron dataset contains genuine compliance-relevant examples including charitable donation forwards and gift exchanges between employees and partners.

### REFERENCES
- BAML by BoundaryML — the structured prompting framework used throughout the live coding session
- shadcn — referenced as the analogy for what agent libraries should look like
- Bootstrap — referenced as the anti-pattern for agent frameworks today
- 12 Factor Agents — methodology covered during the eight-hour workshop weekend
- Sarbanes-Oxley Act — plain text version available on Wikipedia
- JP Morgan 2004 Code of Conduct PDF
- Enron email dataset published by Carnegie Mellon University
- FINRA, SEC guidelines, European accounting laws
- Cursor IDE and Cursor rule files for hardcoded context
- Ruff Python linter
- pytest with pytest-asyncio for async test cases
- tqdm Python progress bar library
- asyncio with semaphores for concurrency control
- Amazon SQS for queue-based scaling architectures
- DeepSeek and Qwen open-source models
- GPT-4 and GPT-4 Mini from OpenAI
- O3 model referenced for harder cases
- Kinder Morgan, NB USA — companies surfaced in actual Enron emails analyzed
- AI That Works podcast (BoundaryML's recurring series)

### ONE-SENTENCE TAKEAWAY
Build pipelines and infrastructure first, read real data manually, then optimize prompts deliberately with deterministic regression tests.

### RECOMMENDATIONS
- Pick two critical policies and build dedicated specialized pipelines instead of one generic policy evaluator covering everything.
- Read individual emails manually before writing evaluation infrastructure so you catch nuance bugs that automation completely misses.
- Save high-risk and medium-risk results to separate folders with email and analysis files indexed by order numerically.
- Add tqdm progress bars whenever batch sizes exceed ten thousand items to maintain visibility during long-running pipeline executions.
- Wrap LLM calls in async with semaphore-limited concurrency around ten so rate limits do not crash batch jobs.
- Return union types with explicit NotAGift escape hatches so the model can structurally indicate inapplicable conditions cleanly.
- Hardcode reasoning steps as schema fields like sender, recipient, risk level, follow-up actions rather than free-form chain of thought.
- Build deterministic pytest cases from real surfaced examples so future prompt changes have regression coverage on known-good cases.
- Pre-filter with regex contains checks like gift in email before invoking LLM calls to slash token spend dramatically.
- Trace entire multi-step pipelines as grouped runs so debugging surfaces full context instead of fragmented individual call logs.
- Group serialization output by risk level into folders so high-risk dashboards become immediately scannable for human reviewers.
- Mock the LLM boundary cleanly so Python pipeline code can be unit tested without expensive round trips to APIs.
- Use embeddings for cheap semantic pre-filtering when the keyword you care about might appear under different terminology variants.
- Build human-in-the-loop dashboards filtering high-risk results rather than chasing perfect model accuracy across millions of records.
- Start with GPT-4 to confirm feasibility, then scale down to smaller models once the pipeline proves it works.
- Add try-catch around validation errors so occasional model failures do not crash the entire batch processing pipeline.
- Use Amazon SQS or similar queue infrastructure when scaling beyond hundreds of thousands of records to handle rate limits.
- Investigate which pipeline step burns the most tokens before attempting general accuracy improvements across all model calls.
- Use cursor rule files to hardcode domain terminology like asset definitions specific to your company's financial context.
- Treat ambiguous evidence as a signal to add agentic follow-up research steps like web search for unknown company names.
