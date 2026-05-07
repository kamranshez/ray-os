---
video_id: OawyQOrlubM
title: "Evals: How to compare models 🦄#16"
url: https://www.youtube.com/watch?v=OawyQOrlubM
channel: BoundaryML
---

### SUMMARY
Vibhav (BAML) and Dex (Human Layer) discuss evaluating LLMs, building bespoke vibe-eval dashboards, and comparing models for production prompts during the AI That Works podcast.

### IDEAS
- Most engineers wait for community vibes before swapping a working production model to newer alternatives.
- A known enemy beats unknown enemy when production systems work well enough already today.
- Simon Willison vibe-tests models by asking them to generate SVG pelicans riding bicycles from scratch.
- Speed improvements often justify accepting slightly dumber models in user-facing latency-sensitive applications immediately.
- New models require flipping off prior assumptions about capability limits to test honestly.
- Behavior-driven development specifications break down because LLM capabilities emerge unpredictably during product exploration.
- Building features now is fast but evaluating AI pipelines remains the bottleneck slowing iteration.
- Vibe evaluations dominate because most teams lack automated evaluation infrastructure for their prompts.
- Multi-turn tool calling capability matters more than single-prompt performance for modern agentic workflows.
- Accuracy is poorly defined and means different things across hallucination rates, code correctness, tone.
- Pre-AI performance meant cost, latency, uptime, security; AI added accuracy as new dimension.
- A REST API failing 20% of requests would trigger outages but LLMs accept this regularly.
- LLM-as-judge can compound stochastic errors when judge models hallucinate as much as production models.
- Different model families like Llama, OpenAI, Anthropic vet results because they hallucinate differently from each other.
- Splitting emails into intro, body, CTA enables segment-level evaluation rather than monolithic body assessment.
- The assembly era of prompting means systems cannot yet auto-heal without clear problem definitions.
- Async parallel test execution beats pytest for evaluations because of network failure handling needs.
- Streamlit dashboards rendering side-by-side outputs beat JSON dumps for evaluating subjective quality dimensions.
- Adding regex highlighting for em-dashes catches AI-generated patterns developers might miss when scanning quickly.
- Building eval harness equals building internal tooling for teammates to vote on outputs.
- Side-by-side A/B comparison with notes annotation beats viewing all model outputs simultaneously.
- Eval dimensions include test case, model, prompt version, and evaluator prompt creating multidimensional problems.
- Cursor accidentally deleting an hour of work motivated switching to Claude Code workflows entirely.
- Heaviest Anthropic per-token users are Claude Code power users running ten parallel instances.
- Implementation plans matter more than code review when working with capable coding agents.
- The ten-minute rule: try AI for ten minutes per feature, decide whether to continue or revert.
- Pre-AI machine learning engineers spent ninety percent of time shaping data not training models.
- Outbound sales emails reach LLMs reading executives' inboxes, requiring different formatting than human-targeted versions.
- Validating links return 200 status codes serves as runtime guard for hallucinated URLs.
- Detecting placeholder brackets like [name here] catches incomplete generations before sending to users.
- Hard-coded human results define what good looks like, enabling later iteration toward consistent quality.
- Using em-dashes incorrectly with surrounding spaces proves human authorship since LLMs always use them correctly.
- Multipplexing Claude Code instances enables shipping eight pull requests in a single day.
- Reading implementation plans as markdown files replaces nitpicking pull request code line by line.
- Wielding coding agents requires skill beyond shouting prompts, including subagent research and continual compaction.
- Open-source vibe coders gate meetup entry by requiring fifty dollar daily AI tool spend.
- DeepSeek's open-source value matched GPT-4o quality and unlocked use cases requiring local deployment.
- Dynamic client builders allow swapping models per test without regenerating BAML clients each time.
- Eval pipelines should test single steps first before composing into full multi-stage pipeline evaluations.
- The C compiler analogy: humans wrote better assembly once, but compilers eventually surpassed everyone.
- Taste and knowing user needs becomes the moat as code generation becomes commoditized through AI.
- Different harnesses test smartness differently; one-shot LinkedIn post generation reveals tool-calling depth.
- The model alone is not the unit of evaluation; the entire harness contributes to outcomes.

### INSIGHTS
- Evaluation infrastructure mirrors data engineering: ninety percent shaping data, ten percent on actual model evaluation.
- Vibe evals beat automated evals when problem definition remains ambiguous and subjective like email quality.
- New models tempt swapping but switching costs equal building features without comparable user-visible value.
- Accuracy definitions must derive from business outcomes not abstract metrics divorced from user experience.
- Bespoke eval dashboards beat generic platforms because each domain needs unique visualization for human judgment.
- The eval bottleneck shifts engineering value from writing code toward defining what good output means.
- LLM judge prompts require their own evaluation creating recursive meta-problems in evaluation pipelines.
- Multi-dimensional comparison across prompts, models, versions, and tests demands custom internal tooling investment.
- Implementation planning replaces code review as the leverage point in agentic coding workflows today.
- Detecting AI tells like em-dashes via regex augments human pattern matching during quality reviews.
- Speed-accuracy tradeoffs depend on whether humans remain in loop or systems run fully headless.
- Headless agents demand higher accuracy because humans cannot easily intervene to fix wrong outputs.
- Iteration speed in AI feels faster than other engineering, creating pressure for premature model swaps.
- Generic eval tools fail because successful eval workflows require specific user experience knowledge.
- The C compiler analogy suggests current prompting is assembly era awaiting higher-level abstractions.

### QUOTES
- "Let someone else vibe check for you." — Dex
- "It's like the known enemy and a new model is like the unknown enemy." — Vibhav
- "I vibed it in 30 seconds. I was like, yep, we're going to use this one from now on." — Dex
- "Can you imagine if your REST API failed on 20% of requests? You would update your status page." — Dex
- "Switching prompts takes almost as much time as actually writing a new feature usually." — Vibhav
- "Evaluating an AI pipeline is always going to be really slow because most people don't have automated evals." — Vibhav
- "We're probably in the assembly era of prompting right now." — Vibhav
- "I haven't opened an editor in about a month, and I shipped eight PRs yesterday." — Dex
- "If you're not spending more than fifty dollars a day on AI coding tools, you don't get in." — Dex
- "Cursor hallucinated a generator version." — Dex
- "Most things that are worth solving from a business standpoint have no infinite goal." — Vibhav
- "You can keep your em-dash as long as you use it wrong." — Dex
- "Ninety percent of the job is getting the data in the right shape so you can make the right decisions." — Vibhav
- "JSON files are garbage. They're not very useful at all." — Vibhav
- "I love Python. Best language." — Dex
- "I hate Python." — Vibhav
- "There's no perfect UI to be completely honest." — Vibhav
- "I'm restraining my instinct to do my old thing." — Dex
- "The skill of wielding coding agents." — Dex paraphrasing Sourcegraph CTO
- "It's quite easy to build, and the actual value is generating data of what's good." — Dex
- "Most people remove them now because em-dashes signal AI authorship." — Vibhav
- "If marketing was solved we wouldn't have to do any of this stuff ever again." — Vibhav
- "An LLM is essentially a very complex instrument and we all need to learn to play it." — Dex
- "Our REST API would have outage pages if accuracy dropped twenty percent." — Dex
- "Forty mini is amazing at regex." — Vibhav

### HABITS
- Wait for community vibe checks on new models before updating your own production prompts.
- Maintain a private personal benchmark of secret prompts to evaluate every newly released model.
- Spend ten minutes attempting features with AI before deciding between continuing or reverting manually.
- Read implementation plans as markdown documents rather than reviewing code line by line afterward.
- Run twenty to thirty test prompts on new models before evaluating production task fit.
- Save evaluation results to disk as JSON before rendering them through Streamlit dashboards later.
- Wrap async test functions in try-except so individual failures cannot crash entire evaluation runs.
- Skip pytest for evaluation work and use Jupyter-style exploratory dashboards for parallel async runs.
- Vibe code UIs side-by-side rather than viewing JSON dumps when judging subjective output quality.
- Add regex highlighters for AI tells like em-dashes to evaluation dashboards for quick scanning.
- Test single pipeline steps before evaluating end-to-end pipelines to isolate evaluation signals cleanly.
- Use intentional typos and incorrect em-dash spacing as proof of human authorship in writing.
- Run multiple Claude Code instances in parallel via multiplexer for shipping eight PRs daily.
- Close the editor entirely and rely on Claude Code with markdown plans for implementation.
- Keep a results directory structured by model so the dashboard can dynamically discover new variants.
- Use dynamic client builders to swap models in BAML rather than regenerating clients each test.
- Pump every prompt through Claude before judging it, since one-shot LinkedIn posts reveal capability.
- Validate URLs return 200 status as runtime guard against hallucinated links in generated emails.
- Detect placeholder brackets in generated emails to catch incomplete substitutions before sending users.
- Reset assumptions about model capabilities every release to avoid bias from prior version limits.

### FACTS
- GPT-4o launched roughly twice as fast as GPT-4 enabling real-time UX improvements for batch summarization.
- Anthropic likely served ten to twenty percent of inference to Claude Code, potentially jumping to fifty percent.
- Claude Code's heaviest five percent power users run multiple parallel instances daily for compounding speed.
- Pre-LLM machine learning engineers spent ninety percent of time on data shaping not model training.
- Behavior-driven development uses Cucumber or Gherkin syntax for non-technical stakeholders writing specifications.
- Simon Willison's pelican-on-bicycle SVG benchmark tests Nova, Llama 3.3, DeepSeek and other frontier models.
- DeepSeek's release matched GPT-4o quality while being open-source unlocking previously impossible local deployment use cases.
- BAML provides dynamic client registries for swapping models without regenerating client code per evaluation.
- Sourcegraph's CTO discussed wielding coding agents at the AI Engineer conference recently this year.
- Amplify Partners' Sarah Cat interviewed one hundred AI founders finding eval harnesses require building data.
- Em-dashes correctly touch surrounding words without spaces, but most humans incorrectly add spaces around them.
- Loops API substitutes hello first name variables when emails are sent through their automation platform.
- Streamlit applications run via uvx streamlit run command after dependencies are installed via uv add.
- Pydantic models with mode equals JSON serialize timestamps correctly when dumping to disk for storage.
- Twelve Factor Agents methodology was authored primarily by Dex Horthy with significant contributions from Vibhav.
- Human Layer is the company Dex founded after the prior SQL audit log summarization product.
- Cursor IDE has user-reported incidents of deleting a month of work without recovery options.
- BAML test cases generate random adjective-animal names like married guan or burning guinea fowl.
- The MLOps community virtual conference featured talks on agents in production this year recently.
- Ben Stein discussed product management in AI at AI Engineer conference covering emergent properties.

### REFERENCES
- BAML (Boundary ML) — prompt engineering framework with type-safe structured output and dynamic clients
- Human Layer — Dex's company building tools for multiplexing Claude Code agents
- Twelve Factor Agents — methodology document by Dex Horthy
- Simon Willison's pelican-on-bicycle SVG benchmark
- Claude Code, Cursor, Gemini CLI — agentic coding tools mentioned
- Streamlit — Python dashboarding library used to render eval results
- Pydantic — Python data validation library used for serialization
- Cucumber / Gherkin — behavior-driven development frameworks
- Ben Stein's AI Engineer talk on product management with emergent AI properties
- Sourcegraph CTO talk on wielding coding agents at AI Engineer conference
- Sarah Cat / Zarah at Amplify Partners — research on one hundred AI founders and eval harnesses
- DeepSeek — open-source model rivaling GPT-4o quality
- GPT-4o, GPT-4o Mini, Claude Sonnet 4, Claude Opus 4, Gemini Flash, Gemini Pro — models compared
- shadcn/ui — scaffolding pattern referenced as analogy for bespoke eval dashboards
- AI That Works podcast — the show this episode belongs to
- Loops — email automation platform with first name variable substitution
- Jeff Huntley's "deliberate intentional practice" framing for vibe coding
- Brian's previous AI That Works episode on evals as competitive moat
- MLOps community / agents in prod virtual conference

### ONE-SENTENCE TAKEAWAY
Build bespoke side-by-side eval dashboards because generic tools cannot capture your domain's quality definitions.

### RECOMMENDATIONS
- Wait for community vibe checks before swapping production models that already work reliably.
- Build a personal secret benchmark suite for evaluating each new model against your tasks.
- Test new models with twenty parallel ambiguous prompts to discover capability ceilings independently.
- Define accuracy in business outcome terms before building any evaluation harness for prompts.
- Use Streamlit or React dashboards rendering side-by-side outputs rather than dumping raw JSON.
- Wrap async evaluation functions in try-except blocks so individual failures cannot crash full runs.
- Skip pytest for exploratory evaluation work and embrace Jupyter-style parallel async exploration patterns.
- Add regex-based highlighters for AI tells like em-dashes to evaluation dashboards for scanning.
- Test single pipeline steps in isolation before composing end-to-end pipeline evaluation runs.
- Spend ten minutes attempting each feature with AI tools before reverting to manual coding.
- Read implementation plans as markdown rather than reviewing AI-generated code line by line.
- Run multiple Claude Code instances in parallel using a multiplexer for compound daily output.
- Validate generated URLs return 200 status codes as runtime guards against hallucinated links.
- Detect placeholder brackets in generated content to catch incomplete substitutions before user delivery.
- Use intentional em-dash misuse with surrounding spaces to prove human authorship in writing.
- Save evaluation results to a structured directory the dashboard can discover dynamically per run.
- Annotate evaluation results with reviewer notes and X-out invalid options for team workflows.
- Compare prompt versions across models to track regression risk when iterating on production prompts.
- Write LLM-as-judge prompts as separate prompts requiring their own evaluation harness recursively.
- Bias toward bespoke evaluation tooling because generic platforms cannot encode domain-specific quality criteria.
