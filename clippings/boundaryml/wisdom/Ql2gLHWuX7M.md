---
video_id: Ql2gLHWuX7M
title: "How to Scrub Sensitive Data Before it Reaches Your LLM"
url: https://www.youtube.com/watch?v=Ql2gLHWuX7M
channel: BoundaryML
---

### SUMMARY
BoundaryML hosts discuss PII redaction architectures for LLM applications, separating legal-liability data from preference-leak data and building layered detect-check-redact pipelines.

### IDEAS
- PII data splits into two classes requiring fundamentally different handling approaches and architectural decisions throughout systems.
- Class one PII demands codebase-level security controls, not AI-layer solutions, because legal liability eliminates risk tolerance entirely.
- Most companies do not need class-one security controls even when operating within medical or healthcare regulatory environments.
- Intranet deployment handles most class-one concerns by isolating systems from public internet inbound and outbound access.
- Air-gapped networks for PCI compliance prevent data exfiltration even after attackers fully compromise internal infrastructure systems.
- Beyond Corp authentication models replace network perimeter trust with mutual TLS authentication between every infrastructure node.
- Achieving 100% PII guarantees through software is effectively impossible, similar to gaming companies banning profanity through regex.
- PII redaction is fundamentally a masking problem, transmitting concept across without transmitting raw underlying data values.
- Video game profanity filters fail because users invent new words and spelling variations that bypass static rule sets.
- Every PII system trades false positives against false negatives along a bias spectrum that designers must explicitly choose.
- Rejecting matched social security patterns reveals which numbers are real, creating a service-area attack surface for adversaries.
- PII problems are software problems first; LLMs only shift you toward proactive but degraded user experiences.
- Building proxy systems intercepting requests before they reach Anthropic or OpenAI provides the cleanest enterprise PII boundary.
- Static rules are fast and reactive; generative LLM rules provide proactive coverage at higher cost and latency.
- Three rule categories exist: static rules, dynamic runtime-injected rules, and generative LLM-based rules with broader coverage.
- Hybrid systems combine generative address detection with hardcoded business address allowlists to distinguish individuals from public entities.
- Time zone redaction substitutes user-written times with canonical timezone representations to maintain consistent LLM context.
- Don't make LLMs do deterministic work because it detracts attention from tasks only LLMs can perform.
- Detection and labeling tasks are fundamentally different from checking tasks, even when performed by identical underlying models.
- Build evolving test suites from production data rather than synthesizing test cases upfront for redaction quality assurance.
- Any PII system that doesn't show users redaction lists for control and tweaking should be considered garbage architecture.
- Sample 5% of redactions for a check-redaction LLM pass to maintain quality without main-loop performance degradation.
- BAML's ID aliasing trick makes the model think of strings differently when serialized into prompts.
- Removing the "none" risk option biases the model toward finding bad content, requiring different post-processing approaches.
- Use bouncing patterns: layer additional prompts to reclassify medium-risk findings as either none or high-risk.
- Context engineering involves both information budgets and instruction budgets within the model's limited attention window.
- OCR loses structural sentiment, making it inferior to vision-capable LLMs for redaction in image-based content modalities.
- Bounding-box redaction with deterministic blackouts beats generative image rewriting for preserving original content fidelity.
- Dynamic generative rules use per-user context like email and phone to prompt-tune redaction for that specific user.
- Custom user-defined categories let enterprise customers configure their own sensitivity hierarchies while you own the control plane.
- Knowledge workers configuring redaction schemas mirrors the doctor-note intake pattern for domain expert configuration interfaces.
- Therapists need trauma-category generative rules nobody could explicitly define because trauma resists strict definitional boundaries.
- Building infrastructure means giving customers building blocks plus the ability to compose their own building blocks dynamically.
- Face ID team solved data access by getting employee waivers granting developers temporary access to specific facial datasets.
- Building redacted dataset copies for development is usually wrong; customer data waivers with renewal cycles work better.
- Synthetic data generation often duplicates the same reasoning the LLM would apply to listing pattern variations directly.
- Redact-then-check pipelines work because the model spends attention differently on validation versus extraction tasks despite identical weights.
- Spot-checking 100 samples often suffices for check-redaction quality, since looking at production data builds intuitive confidence.
- Discriminated unions in BAML schemas handle the risk-presence boolean cleanly with conditional field requirements per case.
- Five-vendor trust models limit even security-conscious enterprises to AWS, Salesforce, Workday, and few other infrastructure providers.

### INSIGHTS
- Separating legal-liability PII from preference-PII unlocks fundamentally different architectures: control planes versus best-effort masking pipelines.
- The line between leak and no-leak is actually a zone, and better techniques narrow that zone meaningfully.
- LLMs shift PII handling from reactive regex-based recovery toward proactive but slower and degraded user-experience tradeoffs.
- Architecture matters more than model choice; running redaction outside the main control loop preserves user experience.
- Validation and generation are distinct cognitive tasks for LLMs, justifying separate functions rather than retrying the same prompt.
- Software solves more PII problems than AI does; reach for LLMs only after exhausting deterministic approaches.
- Building reactive evolving test suites from production beats synthetic upfront test generation for evolving redaction patterns.
- Bouncing layered prompts narrow ambiguous classifications iteratively, like chiseling marble from rough hammer to polish cloth.
- Context engineering balances information against instruction budgets, requiring careful attention allocation across multiple competing rules.
- True infrastructure exposes building blocks letting customers compose their own redaction primitives while preserving central control planes.
- Customer waivers granting time-bounded data access beat building separate redacted datasets for most development iteration loops.
- Hybrid deterministic-plus-generative systems leverage strengths of each, using LLMs only where regex fundamentally cannot reach.
- Showing redactions to users with override controls turns mandatory friction into participatory feedback for system improvement.
- The check-redaction loop is essentially a metric you can use as a DSPy/GEPA optimization signal.
- Modality matters: PDFs and images require different redaction architectures than text, with bounding boxes preserving structure.

### QUOTES
- "If you really must not leak this data, then you have to build security controls in your code base." - Vaibhav
- "Most people do not need class one security. You should not do this even if you're in the medical space." - Vaibhav
- "It is effectively impossible to get 100% PII guarantees on here." - Vaibhav
- "PII is really really good masking. You want to mask the data in some way that sends the concept of the data across but doesn't actually send the raw data itself." - Vaibhav
- "All of them have to do with pure software. And I think that's the first mistake that people make, which is they think that this is an AI problem." - Vaibhav
- "Don't make the LLM do things that it's either like not good at because you're going to detract attention away from the task that it only the LLM can do." - Dexter
- "If you can do things deterministically, then don't make the LLM do them cuz it's going to be faster, cheaper, and more reliable." - Dexter
- "Any system that doesn't regularly show you the list of redactions and allow you to control that and tweak that over time in my opinion is basically garbage." - Vaibhav
- "You should think of this more like an agent loop than a single LM call." - Dexter
- "This isn't actually a line. This is like a zone." - Dexter
- "It's not really about element as a judge. It's about where are you running this in your orchestration system." - Vaibhav
- "Even the biggest most security conscious enterprises in the world probably have like five vendors they trust." - Dexter
- "If you're a startup you basically send your data everywhere because you don't care because like no one trusts you anyways." - Dexter
- "Checking and labeling are two different tasks. The redact method is a labeling task. The check method is a check task." - Vaibhav
- "Answering a multiple choice question is very different than grading a multiple choice test." - Vaibhav
- "You have an information budget in your context window and then you have an instruction budget." - Dexter
- "The more like rules and instructions you're giving the model to all follow at once, the less well it can attend to any specific one of them." - Dexter
- "You're just slowly narrowing and giving every subsequent step less and less context, but more and more specific context." - Vaibhav
- "Most of the AI stuff that most people really need is actually has nothing to do with the code." - Vaibhav
- "What people really really need to understand is how to like map concepts together." - Vaibhav
- "You're always going to trust some external people with your data." - Dexter
- "It's really about any redactive system and when you might want to substitute a word with some other system." - Vaibhav

### HABITS
- Build evolving test suites from production data rather than predicting test cases up front during initial design.
- Sample 5% of production traffic with check-redaction validation rather than running checks on every single request.
- Spot-check 100 samples regularly to maintain confidence in check-redaction quality without building elaborate eval harnesses.
- Show users their redaction list and let them override decisions to gather feedback and improve over time.
- Run small local models on intranet for first-pass classification before sending data to external frontier providers.
- Map new concepts to familiar mental models like Redis-as-L1-cache to accelerate understanding of unfamiliar technical territory.
- Build proxy interceptors between application code and external LLM APIs to enforce organization-wide redaction policies cleanly.
- Use BAML ID aliasing to make the model think about string fields differently from raw string content.
- Layer subsequent prompts giving each less context but more specific context to iteratively narrow ambiguous classifications.
- Bias risk classification toward only "high" and "none" rather than including medium when medium produces too many false positives.
- Discuss fundamentals for 20-25 minutes before writing code so users learn when and why to apply techniques.
- Run check-redaction continuously as a metric and feed flagged cases into a Slack notification for human review.
- Build reusable rule classes with name, description, and examples that compose into arrays for systematic redaction coverage.
- Renew customer data waivers on time-bounded cycles instead of permanently exposing sensitive datasets to development environments.
- Watch the agent's previous datetime episode before applying redaction patterns since the masking architecture transfers directly.

### FACTS
- Google's Beyond Corp model places infrastructure on the public internet with mutual TLS authentication replacing network perimeter trust.
- PCI compliance requires every node touching credit card numbers to be air-gapped with no outbound network access permitted.
- Online video games used regex-based profanity filters for nearly their entire history before AI-based moderation became viable.
- Spear phishing attacks exploit services that reject existing emails to confirm valid account presence within target organizations.
- Apple's Face ID team used time-limited employee data waivers granting developers 60-day access to specific facial datasets.
- BAML supports type aliasing to rename fields from the model's perspective without changing the underlying string type definitions.
- AWS Bedrock allows running Anthropic Claude models within a company's own VPC without data leaving the network.
- Defense-in-depth security treats network compromise as inevitable and adds outbound restrictions to prevent successful data exfiltration.
- Salesforce, AWS, and Workday represent the typical short list of vendors trusted by security-conscious enterprise customers.
- Amazon Comprehend provides PII redaction services that compete with custom LLM-based approaches for sensitive data masking.
- DSPy and GEPA frameworks let validation functions serve as optimization metrics for upstream prompt and weight tuning.
- Ollama Gemma 3 runs locally on developer machines and suffices for many classification tasks within redaction pipelines.
- BAML examples repository contains a complete PII redaction commit demonstrating mapping-based deterministic restoration after LLM detection.
- The AI That Works show airs weekly with the next episode covering agents, skills, commands, and context engineering.
- The AI That Works unconference is targeting Saturday March 28th in San Francisco pending venue confirmation.

### REFERENCES
- BAML (BoundaryML's prompt engineering language)
- Amazon Comprehend
- AWS Bedrock
- Anthropic API
- OpenAI API
- Cursor IDE
- Claude Code
- Ollama with Gemma 3
- DSPy / GEPA optimization frameworks
- Apple Face ID development data practices
- Google Beyond Corp security model
- Salesforce, Workday infrastructure trust tiers
- Previous AI That Works datetime episode
- Previous AI That Works PDF/multi-modality episode
- Previous AI That Works dynamic types episode
- Coding Agents conference, Mountain View
- HIPAA compliance regulations
- PCI compliance requirements

### ONE-SENTENCE TAKEAWAY
PII redaction is software architecture first, AI second; design proxy pipelines with layered detect-check-redact loops.

### RECOMMENDATIONS
- Classify PII into legal-liability versus preference categories before designing any redaction architecture for your specific application.
- Build security controls in code itself for liability-grade data, never relying on AI-layer protection alone.
- Run intranet deployments to handle most class-one PII concerns without complex application-layer security infrastructure overhead.
- Implement air-gapped networks with no outbound access for PCI-grade data to defend against compromised credentials.
- Choose explicitly which side of false-positive versus false-negative tradeoff your product tolerates before designing redaction.
- Build proxy systems intercepting LLM API calls to enforce company-wide redaction without requiring application-level changes everywhere.
- Combine static regex rules, dynamic database rules, and generative LLM rules based on each rule's coverage requirements.
- Use small local models like 3B or 30B for redaction classification before sending data to external providers.
- Design check-redaction validators as separate LLM calls because validation tasks differ cognitively from detection tasks.
- Run check-redactions on 5% sample rate outside the main loop to avoid degrading user-facing latency.
- Build evolving test suites from production data rather than synthesizing test cases ahead of system deployment.
- Show users their redaction list with override controls turning friction into participatory improvement feedback for systems.
- Use BAML ID aliasing on string fields so the model treats redaction identifiers differently from raw content.
- Layer additional prompts to reclassify medium-confidence findings rather than accepting noisy single-pass classification results directly.
- Bias risk levels toward high-and-none when medium produces too many false positives in your particular dataset.
- Use bounding-box detection plus deterministic blackouts for image PII rather than generative image rewriting approaches.
- Inject per-user context like email and phone numbers into prompts to enable user-specific generative redaction rules.
- Expose user-defined category systems letting enterprise customers configure their own sensitivity hierarchies on your control plane.
- Use customer data waivers with renewal cycles instead of building separate redacted datasets for development iteration speed.
- Spot-check 100 samples regularly rather than building elaborate evals when intuitive quality assessment suffices for systems.
- Build redact and restore as paired functions storing mapping tables for deterministic reconstruction after external LLM processing.
- Treat check-redaction as a DSPy or GEPA optimization metric to automatically improve upstream redaction prompts over time.
- Watch BoundaryML's previous datetime episode since timezone masking patterns transfer directly to general redaction architectures.
- Map unfamiliar AI concepts to familiar systems concepts to accelerate intuition development around novel architectural decisions.
- Reach for AI redaction only after exhausting deterministic options because deterministic approaches are faster, cheaper, and more reliable.
