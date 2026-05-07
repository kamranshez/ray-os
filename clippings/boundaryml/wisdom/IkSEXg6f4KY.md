---
video_id: IkSEXg6f4KY
title: "Building a Prompt Optimizer:🦄 #36"
url: https://www.youtube.com/watch?v=IkSEXg6f4KY
channel: BoundaryML
---

### SUMMARY

Vibhav, Dex, and guest Greg from BoundaryML build a GEPA-based prompt optimizer for BAML, demonstrating algorithm internals, candidate generation, and structured evaluation tooling.

### IDEAS

- Prompt optimizers cannot beat humans who deeply understand a problem domain.
- Software quality scales directly with the time and love invested into it.
- Optimizers shine on code nobody loves, where humans refuse to invest attention.
- Optimizers need automated feedback loops, otherwise the model cannot improve trajectories.
- Coding agents lack deterministic backpressure unless tests provide structured pass-fail signals.
- Cloud Code uses a special notebook-edit tool because raw Jupyter JSON contains noise.
- Prompt optimizers should constrain edits to relevant file regions, not whole files.
- Shared types across pipelines prevent reoptimizing the same instructions repeatedly across prompts.
- Overspecializing a system instruction for one prompt degrades performance on other dependent prompts.
- GEPA combines candidate generation, prompt merging, and reflection into one optimization loop.
- Combine-prompts step takes Pareto frontier prompts and breeds them into hybrid candidates.
- Pareto frontier balances metrics like accuracy, latency, token cost, and test performance.
- Out-of-the-box GEPA only provides one metric: fraction of tests passing.
- Convergence happens when the metric maxes out, stopping further candidate generation early.
- The GEPA prompts themselves can be customized and even optimized recursively.
- Reflection prompts analyze failure patterns to determine where optimization should focus next.
- Including full source code beats passing only failure messages, since models reason structurally.
- Showing only one failed assertion wastes iterations as later asserts then fail.
- BAML implements GEPA using BAML itself, dogfooding structured outputs throughout the optimizer.
- Three-day implementation proves GEPA is approachable, not magical, for any developer.
- Different LLM providers can power different optimization stages based on cost-power tradeoffs.
- TUIs differ from CLIs because they have interactive panes, not pure stdin-stdout pipes.
- Token efficiency optimization can use aliases to dramatically shrink prompts while preserving accuracy.
- Without reading prompts, you cannot detect overfitting from underrepresentative test samples.
- Human intuition often beats designing fifty metrics for first-pass evaluation work.
- Type contracts stay frozen during optimization to avoid breaking generated client code.
- BAML repurposed soft check assertions as named ancillary metrics for weighted optimization.
- Optimizing whole workflows beats optimizing isolated LLM functions in production systems.
- Discovery process for optimizers means signaling available shared resources without forcing usage.
- Markdown-only optimizer flows lose visibility, while structured plumbing enables rich UIs.
- Prompt token weight inversion shows optimizers will brutally compress when incentivized correctly.
- BAML supports up to seven hash levels for nested raw string escaping in prompts.
- Default DSPy philosophy hides prompts as implementation details, opposite to BAML's transparency thesis.
- The optimizer-of-optimizers pattern (GEPA-on-GEPA) is the natural recursive next step.
- Reachable classes in BAML are pulled by traversing input and output type references.
- Domain-specific knowledge injection into optimizer prompts unlocks codebase-aware refinement strategies.
- Building your own optimizer matters more than depending on third-party libraries.

### INSIGHTS

- Effort allocation defines software quality; optimizers automate the unloved code humans neglect.
- Structured plumbing throughout pipelines enables observability that pure markdown architectures cannot provide.
- Transparency over prompts is philosophical, not technical, separating BAML from DSPy's abstraction approach.
- Constraining the edit surface area prevents optimizers from corrupting unrelated parts of codebases.
- Rich failure context including source code outperforms terse error messages for reasoning models.
- Co-optimizing dependent prompts together prevents local improvements from causing global regressions.
- Convention-over-configuration optimization tools democratize techniques previously gated behind research expertise.
- Human intuition beats elaborate metric scaffolding when validating whether optimization actually preserved intent.
- Recursive self-optimization (optimizing the optimizer) becomes inevitable once primitives are clean.
- Type-safe contracts as immutable optimization boundaries protect downstream consumers from generated-code churn.

### QUOTES

- "Software quality is basically based on amount of time and love you give it." — Vibhav
- "An optimizer is great for that scenario." — Vibhav
- "Optimizers don't work unless you can give them automated feedback." — Dex
- "The type is part of the prompt because it's the instructions you're asking it to do." — Dex
- "We didn't just copy paste the stock JEPA prompts from DSPy; they wouldn't work for BAML." — Greg
- "If your metric is 100%, where else are you going to go?" — Greg
- "Of course, this is implemented in BAML as well." — Vibhav
- "It's so hard to remember your own implicit knowledge when you're prompting." — Greg
- "I want to keep my old crummy prompts for other demonstrations." — Greg
- "Most of these systems that you're building are not that complex." — Vibhav
- "Everybody should build a prompt optimizer from scratch." — Vibhav
- "I am at least as good as a bad LLM." — Greg
- "It's unlikely that the dog was 21." — Greg
- "AI that works is a mandatory companywide attendance policy." — Vibhav
- "You shouldn't have to look at your prompts." — Vibhav (paraphrasing DSPy)

### HABITS

- Limit optimization trials initially with command-line flags to speed up iteration cycles.
- Run optimizers in dry-run mode first to extract customizable prompt files for editing.
- Always test prompts end-to-end alongside individually-evaluable smaller pipeline pieces in parallel.
- Keep failing prompts around as demonstration material rather than overwriting them immediately.
- Pull only minimum reachable code into optimization context to keep prompts focused.
- Inspect generated prompts manually to catch overfitting that metrics alone cannot detect.
- Apply prompt optimization mentally during code review when migrating colleagues to new prompts.
- Define multiple soft check assertions to track ancillary metrics beyond hard pass-fail.
- Use thinking-capable reflection models like Claude Opus 4.5 for the highest-leverage optimization stage.
- Write prompts knowing they may be the parent for descendants in candidate generation trees.
- Default to single-hash raw strings, escalating hashes only when escape conflicts arise.
- Co-host weekly Tuesday episodes covering practical AI engineering topics with real working code demos.
- Maintain Pareto frontiers explicitly when balancing accuracy against token cost in production systems.
- Save run history per optimization session for retroactive inspection of candidate evolution.
- Pair-program complex algorithm implementations with team members smarter than yourself.

### FACTS

- GEPA originated as an algorithm inside DSPy before becoming a standalone library.
- DSPy has been pursuing prompt optimization research for several years already.
- BAML allows up to seven nested hash levels for raw string escaping in prompts.
- The GEPA paper diagram is freely available on arXiv for visual reference.
- BAML's GEPA implementation took Greg approximately three days from concept to working.
- DSPy includes multiple optimizers beyond GEPA, including various other algorithms.
- Combine-prompts is optional, only activated when multiple Pareto-optimal prompts exist.
- Convergence in GEPA occurs as soon as the primary metric reaches one hundred percent.
- BAML manipulates AST representations rather than raw source files for safe prompt edits.
- Cloud Code's notebook tools exist specifically because Jupyter files are JSON blobs.
- The Pareto frontier always starts as just the single original baseline prompt.
- Reachable classes traversal follows input and output type references recursively only.
- BAML reuses existing test infrastructure as evaluation harness without language changes required.
- DSPy's philosophy treats prompts as hidden implementation details developers shouldn't manipulate.
- Token-weighted optimization can produce prompts with field aliases to reduce output verbosity.

### REFERENCES

- BAML — programming language for AI pipelines built by BoundaryML
- DSPy — Stanford framework for declarative LLM programming and optimization
- GEPA — genetic-Pareto prompt optimization algorithm originating from DSPy
- GEPA paper on arXiv — primary academic reference for algorithm details
- Claude Code — Anthropic's coding agent, referenced for notebook-edit tool design
- Cloud Opus 4.5 — model used as default reflection LLM in BAML's implementation
- Zed editor — used during demo, with command palette quirks noted
- Human Layer — Dex's company helping coding agents tackle complex codebases
- SWE-bench — benchmark mentioned for future agent optimization tests
- Y Combinator — incubator referenced in upcoming founder backstory episodes
- jeepa.baml — file containing GEPA prompts inside .baml-optimize directory

### ONE-SENTENCE TAKEAWAY

Prompt optimizers automate care for unloved code, but humans must inspect outputs.

### RECOMMENDATIONS

- Build your own prompt optimizer from scratch to truly understand the underlying mechanics.
- Pass full test source code into reflection prompts, not just terse failure messages.
- Constrain optimizer edits to specific file regions using AST-aware tools, not raw editors.
- Define soft checks alongside hard assertions to power weighted ancillary optimization metrics.
- Always inspect generated prompts manually before accepting them, regardless of metric scores.
- Use different LLM providers for different optimization stages based on cost-power tradeoffs.
- Co-optimize all related prompts together when shared instructions appear across multiple pipelines.
- Limit trial counts during exploration to speed iteration before committing to full optimization runs.
- Keep type contracts immutable during optimization to protect downstream generated client code consumers.
- Treat optimization-output prompts as worth reading, not as opaque implementation details to ignore.
- Apply prompt optimization to entire workflows including control flow, not just isolated functions.
- Write evals before attempting any optimization, since optimizers require automated feedback loops to function.
- Build TUIs over CLIs when optimization output benefits from structured navigation and color highlighting.
- Inject domain-specific guidance into optimizer prompts when working in specialized codebases or unusual domains.
- Save optimization run history to disk for retroactive analysis of how candidates evolved over time.
- Test prompts end-to-end alongside individually evaluable pipeline pieces for comprehensive validation coverage.
- Customize the GEPA prompts themselves to teach optimizers about your specific framework conventions.
