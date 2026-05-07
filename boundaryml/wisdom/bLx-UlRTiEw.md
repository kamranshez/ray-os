---
video_id: bLx-UlRTiEw
title: "Anthropic Post Mortem: 🦄 #26"
url: https://www.youtube.com/watch?v=bLx-UlRTiEw
channel: BoundaryML
---

### SUMMARY

Vibhav and co-founder Aaron from BoundaryML dissect Anthropic's recent outage post-mortem, covering context routing, output corruption, top-p sampling bugs, and OpenAI's new agent builder.

### IDEAS

- Anthropic detects model regressions primarily by scanning Twitter sentiment rather than running comprehensive automated evaluation pipelines across all production traffic.
- Million-token context windows degrade performance on small requests because positional encodings stretch differently and information bridging becomes harder.
- Tossing extra context at any model forces wasted attention work, even when the model technically supports the larger window.
- Rope scaling expands position encodings by inserting fractional positions, trading precision for length, never coming free of cost.
- Anthropic likely runs multiple model variants with different context sizes and routes shorter requests to compact, faster, more accurate variants.
- Floating-point arithmetic is non-commutative across precision levels, so a*b*c need not equal c*b*a in practice.
- Mixing fp16 and fp32 in TPU compilation introduces nondeterminism that flips token rankings near probability boundaries during top-p sampling.
- Token vocabularies span multiple GPUs, so each shard proposes candidates locally before a central machine picks the global winner.
- A subtle compiler bug caused per-shard candidate selection to occasionally exclude the true top token from final selection entirely.
- Top-p sampling truncates probability mass below 0.99 to avoid floating-point garbage tokens contaminating outputs at scale.
- Temperature zero collapses the distribution onto the highest-probability token; temperature two flattens toward uniform distribution.
- Hand-written SIMD assembly becomes write-once-read-never code that engineers cannot debug without immense friction later on.
- Distributed-systems engineers expect loud failures, but model failures are subtle and require entirely new observability mechanisms.
- Roll back first, diagnose later — the AWS slogan applies perfectly to ambiguous AI pipeline regressions in production.
- Hallucination is poorly defined; technically every unprompted answer is hallucination, but humans only notice when it disagrees.
- Eval datasets must be continuously sourced from production traffic because user behavior distributions drift constantly over time.
- Face ID worked worse in Phoenix because extreme heat expanded camera materials and corrupted stored calibration data.
- The cheapest way to debug an AI regression is swapping models entirely before touching prompts or infrastructure.
- Visual agent builders look beautiful at the marketing layer but collapse the moment schemas and reusable functions appear.
- Code becomes write-once when humans cannot read it but LLMs can regenerate it on demand wholesale.
- OpenAI's responses API entrenches users into provider-specific tools, replicating the same lock-in dynamics as cloud platforms.
- Inference itself is now the least differentiated part of an AI pipeline; integration and composition create real value.
- Model loyalty among engineers is gone — yesterday Claude, today Codex, tomorrow whatever benchmarks well next week.
- Engineers should write type contracts while non-engineers edit everything else within those contracts as a collaboration model.
- Spawning many AI coding agents on the same ticket lets you cherry-pick winners without reviewing every loser carefully.
- Customer thumbs-down feedback comes overwhelmingly from unhappy users, providing reliable negative signal despite extremely low click rates.
- Programmatic validation like checksum verification can catch hallucinations in structured extraction tasks like bank statement parsing reliably.
- Only 0.08% of Anthropic traffic was impacted in some cases, which is why detection took so long.
- The "promised land" of automated evaluation rarely arrives because most problems lack clean definitions of good versus bad.
- Decoder-only transformers now dominate frontier models, departing from earlier encoder-decoder architectures used in translation tasks.

### INSIGHTS

- Subtle model failures demand new observability primitives because traditional distributed-systems heuristics like 500-error rates miss quality regressions completely.
- Latent social signals like Twitter sentiment outperform internal evals at catching cross-cutting model regressions in widely deployed systems.
- The optimal context size is the smallest representation that fully captures the problem, not the largest the model accepts.
- Floating-point nondeterminism compounds across distributed sharding to produce real user-visible quality regressions, not just numerical curiosities.
- Performance optimizations in inference stacks frequently trade quality for throughput in ways operators cannot predict reliably.
- Roll back instantly when something breaks, because eliminating one variable is cheaper than diagnosing across prompt, infra, and model.
- Hallucination as a concept is too vague to be useful; engineers should define failure modes concretely per product.
- Eval sets must be living artifacts continuously refreshed from production data, never built once and frozen forever.
- Visual builders work for shallow pipelines but break catastrophically when schema design, type safety, and function reuse become necessary.
- Provider-specific APIs build moats by entrenching users in tool ecosystems they cannot easily migrate away from later.
- Inference commoditizes; differentiation comes from how AI composes with the rest of the engineering stack and surrounding workflow.
- Token economy is now cheap enough to fan out parallel agent attempts and discard losers as routine engineering practice.
- Engineering hierarchy is shifting toward engineers owning contracts while non-engineers safely modify implementation details within type boundaries.
- Detecting a regression is more valuable than understanding it because rollback restores users while diagnosis happens offline.
- Process overhead like design docs is worth it only when ambiguity exceeds team familiarity with the relevant problem space.

### QUOTES

- "Use less context and less context. I promise you your pipelines will be more accurate." — Vibhav
- "Don't be a hero. Roll back." — Aaron quoting AWS
- "The worst case it's a compiler issue." — Aaron
- "It's actually worse than read-only access. You can't read it. You can only write to the file." — Vibhav
- "Every time I ask a question it's technically hallucinating. It happens to align with how I perceive the world." — Vibhav
- "Every time it disagrees with me I'm sure it's a hallucination." — Aaron
- "If your context can be expressed really tersely, a smaller model can do a better job." — Vibhav
- "You don't deploy worldwide at the same time." — Aaron
- "Use the least amount of tokens you need to represent your problem." — Aaron
- "Code is scary, right? Which is also interesting because code is easier for people to write now." — Aaron
- "There's no loyalty to any of these providers." — Vibhav
- "Quality is better than just having these random bugs happen." — Aaron paraphrasing Anthropic
- "You should definitely unit test the most important parts of the pipeline, not the whole pipeline." — Vibhav
- "It is very order dependent." — Vibhav on floating-point math
- "Anyone that disagrees with this is wrong." — Vibhav on transformer information flow
- "We just keep tagging cursor or claude with random tickets and we don't actually consider it." — Vibhav
- "The magic number is 30." — Aaron on eval sample sizes
- "If you can't help it, don't do that." — Aaron on pushing to prod immediately
- "The minute a customer reports an issue, you want to know one of three things." — Vibhav
- "Even if it's like a thousand lines of code, just redo the whole thing." — Aaron

### HABITS

- Monitor Twitter sentiment as a continuous low-fidelity health signal for systems with broad public consumer exposure.
- Scan social media mentions of products as a qualitative complement to quantitative metrics like watch time.
- Roll back deployments instantly when something breaks rather than spending hours hunting the root cause first.
- Use feature flags as the startup-friendly substitute for staged geographic deployments and one-box rollouts.
- Deploy to platforms like Vercel that support one-click rollback within seconds of detecting a regression.
- Ask thumbs-up or thumbs-down feedback constantly inside AI products, even on every single response interaction.
- Swap models before debugging prompts when an AI pipeline regresses unexpectedly in production environments.
- Bump to the largest model from the same provider before switching providers when troubleshooting quality issues.
- Tag multiple AI coding agents on the same ticket and merge whichever produces an acceptable solution first.
- Write a markdown design doc and review it before coding on genuinely ambiguous high-stakes problems only.
- Skip the design-doc process when the algorithm is clear and the team already knows the right answer.
- Default to Claude Sonnet 4.5 for daily coding and fall back to Codex CLI only on truly tricky problems.
- Sample production traffic continuously to build rolling eval sets that span actual user behavior distributions.
- Add programmatic validation like sum checks for structured extraction tasks to catch hallucinations automatically.
- Build fast debugging loops as the highest-leverage investment for any AI engineering team's productivity.

### FACTS

- Only 0.08% of Anthropic traffic was impacted by some bugs, making detection extremely difficult at scale.
- Approximately 30% of Claude Code users were impacted by Anthropic's recent context-routing performance regression.
- Anthropic serves Claude across AWS Trainium, Amazon Bedrock, and Google Cloud Vertex AI simultaneously today.
- Top-p sampling at Anthropic truncates the probability distribution at cumulative mass of 0.99 reportedly.
- A December 2024 Anthropic bug caused the top token to never be selected during certain inference runs.
- Anthropic stopped using certain performance optimizations entirely because quality regressions outweighed throughput gains they delivered.
- Floating-point operations like a*b*c are not equal to c*b*a due to representation nonlinearity at small values.
- Mixed fp16/fp32 TPU compiler optimizations contributed to Anthropic's third bug by introducing comparison nondeterminism.
- Rope scaling inserts fractional position encodings like 1.5 between integers when extending pretrained context windows.
- OpenAI's agent builder was built in approximately six weeks using their internal Codex CLI tool reportedly.
- Frontier transformer models are now predominantly decoder-only architectures, departing from earlier encoder-decoder designs used previously.
- Aaron worked seven years at Amazon spanning EC2 and Prime Video teams before co-founding BoundaryML with Vibhav.
- Cameras in Phoenix, Arizona miscalibrate from heat expansion, degrading Face ID performance compared to cooler climates.
- Token vocabularies are sharded across machines in 32k chunks during distributed inference at frontier model providers.
- BAML supports a "dynamic type" feature allowing runtime schema modifications for user-editable type-safe AI pipelines.

### REFERENCES

- Anthropic post-mortem blog post on recent outages and quality regressions
- Thinking Machines paper on nondeterminism causes shared by AJ in chat
- AWS EC2 and Prime Video as Aaron's prior employer
- BAML programming language by BoundaryML
- OpenAI Agent Kit and agent builder visual workflow tool
- 11 Labs agent builder
- Lovable for AI-generated apps
- Vercel for instant rollback deployments
- Cursor IDE
- Codex CLI by OpenAI
- Claude Code by Anthropic
- n8n workflow automation
- Zapier integration platform
- Terraform for cross-cloud abstraction
- AWS CDK
- Face ID at Google (Vibhav's prior project)
- Excalidraw for diagramming
- Discord community for BoundaryML

### ONE-SENTENCE TAKEAWAY

Tiny floating-point bugs cascade into model regressions that demand observability, fast rollback, and continuous production-sourced evaluation discipline.

### RECOMMENDATIONS

- Build a latent product-quality signal into every AI pipeline so regressions surface within hours rather than weeks.
- Use the smallest context window that fully captures your problem, not the largest your model technically supports.
- Roll back instantly when production breaks, then diagnose offline rather than patching forward under user pressure.
- Add thumbs-up and thumbs-down feedback widgets to every AI product surface to capture cheap negative signal.
- Sample production traffic continuously and promote a subset into your evaluation dataset as ongoing engineering hygiene.
- Define hallucination concretely per product rather than treating it as a vague catch-all complaint label forever.
- Validate structured AI outputs programmatically with checksums or constraints before trusting them downstream in workflows.
- Invest heavily in fast AI debugging tooling because feedback-loop speed determines team velocity more than anything else.
- Swap models first when troubleshooting AI regressions before spending time rewriting prompts or chasing infrastructure issues.
- Use feature flags instead of staged geographic rollouts when you are a small startup with limited deployment infrastructure.
- Spawn multiple AI coding agents on the same ticket in parallel and merge whichever output meets quality bar.
- Skip detailed design docs when the algorithm is obvious; reserve them for genuinely ambiguous cross-team architectural problems.
- Avoid building bespoke eval suites of hundreds of tests; just look at production outputs more carefully each week.
- Audit your inference stack for fp16/fp32 mixing if you observe inexplicable quality regressions in distributed model serving.
- Treat inference as commoditized and focus differentiation effort on integration depth with the rest of your stack.
- Have engineers write type contracts that non-engineers can safely edit underneath without breaking downstream consumer assumptions.
- Read the full Thinking Machines paper on nondeterminism if you operate large-scale model inference yourself in production.
- Default to Twitter or community-channel scanning as your baseline qualitative model-quality signal before building heavyweight eval pipelines.
