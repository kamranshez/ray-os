---
video_id: HsElHU44xJ0
title: "Getting Tone Just right with LLMs: 🦄 #12"
url: https://www.youtube.com/watch?v=HsElHU44xJ0
channel: BoundaryML
---

### SUMMARY
Vaibhav and Dexter from BoundaryML demonstrate building an automated content pipeline that nails tone through context engineering, structured prompts, and model selection.

### IDEAS
- Getting tone right starts with assembling correct factual data before prompting the model anything.
- Trivially prompting a model rarely produces correct tone for content like emails or summaries.
- Context engineering means deciding which subset of object fields actually reaches the language model.
- The goal of automation is good time value, not eliminating every human touch point.
- Whiteboards and small custom edits are faster manually than coding pipelines to automate them.
- Catastrophic mistakes like "Hello first name" destroy trust faster than slightly imperfect AI prose.
- Software complexity comes from architectural questions you ask, not from the AI components themselves.
- Replace random UUIDs with sequential labels like event_1 to reduce token-prediction confusion for models.
- Models hallucinate random tokens because random strings simply do not exist in training distributions.
- Give the LLM only the choices it needs, not full flexibility over every decision.
- Hardcode file paths when you know exactly which two files should always be modified.
- Breaking dependencies into smaller intermediate steps unlocks parallelism in otherwise sequential AI pipelines.
- Gemini outperforms other models for YouTube-style transcription tasks, likely from training data exposure.
- Long context confuses models when instructions get buried among the actual content being processed.
- Putting instructions after content rather than before improves Gemini's adherence to formatting rules.
- Two-stage prompting beats one-stage when you want both content correctness and coherent prose.
- The first prompt generates raw structured drafts; the second prompt smooths them into polished output.
- Mad-libs templates feel mechanical because dynamic content needs more flexibility than fixed slot-filling.
- Use placeholder URLs that look real instead of obvious placeholders to prevent model substitutions.
- Copy and paste should be replaced with AI generation or cursor tab autocomplete entirely.
- Use more AI than you think for surprising tasks; use less for trivial code.
- MCP works as an extension layer for end users, not as production agent SDK.
- Production agents should expose MCP clients so users can add functionality without app updates.
- Data leakage is the most underrated risk surface as more pipelines accept untrusted inputs.
- Prompt injection has no equivalent to SQL escaping; the surface remains fundamentally unsolved.
- Computers double productivity but also generate twice the work, so net gains stay marginal.
- Prompt optimization tools edit middle text but ignore the structural signature surrounding the prompt.
- Changing a string field to a string array can dramatically improve output quality without prompt changes.
- Karpathy's autonomy slider concept matters: good AI tools span tab-complete to full-agent modes.
- Agentic UX must allow mid-execution interruption and course correction to avoid catastrophic divergence.
- Gemini handles system messages strangely, separating them from user content in the request payload.
- Two consecutive user messages can outperform system+user when targeting Gemini's attention behavior.
- Smaller cheaper models work fine for easy classification tasks like matching events.
- Picking the right model after prompt design matters more than picking it first.
- The actual prompt is comprised of an AST that's far more complex than visible English.
- Automating five hours of work with ten hours of code still pays off long-term.

### INSIGHTS
- Tone emerges from correct data plus correct structure, not from clever prompt phrasing alone.
- Context engineering treats prompt, history, memory, and rag as one unified token stream.
- Constraining LLM choices upfront beats prompting your way out of overly flexible agent failures.
- Model selection should follow problem decomposition, not precede it as a default assumption.
- Decomposition into smaller dependencies enables parallel execution while preserving overall pipeline correctness guarantees.
- Catastrophic small errors matter more than overall quality when shipping automated communications.
- Schema modifications often improve output more than rewriting prompt instructions in plain English.
- Prompt optimizers ignore the structural AST that comprises most actual prompt complexity.
- Two-stage generation separates content correctness from prose coherence, letting each stage specialize.
- Random tokens exist outside training distributions, so models inevitably hallucinate when reproducing them.
- The autonomy slider, not full agency, determines whether AI products feel genuinely useful.
- Production agents should consume MCP, not be built from it as foundation.
- Use AI aggressively for unexpected tasks like clipboard work; ignore it for trivial code.

### QUOTES
- "Before we can get the tone right, we have to understand what we're aiming for." — Vaibhav
- "If we hold off on deploying a system until everything is perfect, we'll never get anything out." — Vaibhav
- "The goal of a project is to get a good value for the time you put in." — Vaibhav
- "Let the LM do things the LM is really good at." — Vaibhav
- "This is all just engineering the right context." — Dexter
- "Tokens that are random are just not in the data set of the model." — Vaibhav
- "If you already know exactly what should happen, let the LM do what it does well." — Vaibhav
- "Software is complicated. The part that's complicated is not the AI part." — Vaibhav
- "There's no prompt that will magically make a perfect email. At least not yet." — Vaibhav
- "We tried GPT-4o, didn't work. We tried Claude, didn't work. Gemini works with Flash." — Vaibhav
- "Use more AI than you think and use less AI than you think at the same time." — Vaibhav
- "Copy and paste is just an AI feature for me now." — Vaibhav
- "Stop trying to use AI for dumb stuff that you could vibe code in five lines." — Dexter
- "MCP is not a building block for building production AI agents as products." — Dexter
- "There's no way to escape inputs to your prompts." — Vaibhav
- "Computers generate 100% more work, so it's kind of a wash." — Dexter
- "Don't try to make your code perfectly fast. You can just use Python." — Vaibhav
- "Full agent mode without being able to course correct along the way is really really bad." — Vaibhav
- "Things become cool when they actually work 99.9% of the time." — Vaibhav

### HABITS
- Draw architectural whiteboard diagrams before writing pipeline code to clarify dependencies between components.
- Use small cheap models like Gemini Flash for trivially easy classification or matching tasks.
- Test prompts immediately on realistic data instead of synthetic stubbed example payloads first.
- Hardcode file paths and constraints whenever you know exactly which outputs should change.
- Replace random IDs with sequential numbered labels before passing entities to language models.
- Place instructions at the bottom of the prompt when working with Gemini specifically.
- Dump content first then instructions when context windows get long during summarization tasks.
- Use placeholder URLs that resemble real ones rather than obvious dummy strings during development.
- Validate generated links and substitute placeholder URLs with real ones in post-processing.
- Build two-stage pipelines: first generate structured draft, then polish into final prose.
- Manually edit whiteboards instead of automating screenshot extraction when AI cost exceeds time saved.
- Run prompt iterations across multiple frontier models before committing to one for production.
- Use AI for clipboard operations and tab autocomplete instead of manual copy-paste workflows.
- Spawn parallel pipeline branches by introducing intermediate dependency steps to break sequential bottlenecks.
- Test edge cases like missing events to ensure graceful failure modes in production pipelines.

### FACTS
- Gemini models likely train more heavily on YouTube data than competitor frontier models do.
- Gemini does not support system messages in the standard chat format used by OpenAI.
- The kit toolkit from Cased lets you traverse remote GitHub repositories programmatically without cloning.
- The supersonic library from Cased lets you create GitHub PRs in a single function call.
- BAML is adding native Go support imminently with Rust support planned shortly afterward.
- Frontier models reliably reproduce short URLs without random characters but struggle with UUIDs.
- Karpathy described an autonomy slider concept in his Y Combinator talk on AI tools.
- The episode pipeline takes Dexter and Vaibhav roughly five to eight hours weekly to operate.
- Cursor's strength comes from allowing users to chat with the agent during execution.
- Claude Code hooks enable pre-tool-use, post-tool-use, and notification triggers for custom integrations.

### REFERENCES
- BoundaryML BAML configuration language for prompt engineering and structured outputs
- Luma events platform integrated via API for event matching
- Zoom recordings API for transcript and meeting metadata extraction
- Gemini 2.5 Flash and Pro models from Google
- GPT-4o and GPT-4o mini from OpenAI
- Claude Sonnet from Anthropic
- supersonic GitHub PR automation library from Cased
- kit GitHub repo traversal toolkit from Cased
- Cursor AI code editor with tab autocomplete and agent mode
- Claude Code with hooks system for ecosystem extensions
- DSPy prompt optimization framework
- Karpathy's Y Combinator talk on AI autonomy sliders
- Boundary cloud evaluation platform for input-output pair recording
- Model Context Protocol (MCP) for extending AI applications
- Previous AI That Works episode on evaluations and testing tiers

### ONE-SENTENCE TAKEAWAY
Tone is downstream of data: get context engineering right before optimizing prompts or selecting models.

### RECOMMENDATIONS
- Draw a dependency diagram of your pipeline before writing any AI integration code.
- Strip object payloads to only fields the model actually needs for its task.
- Replace UUIDs and random tokens with sequential labels before passing them to LLMs.
- Hardcode file paths and constraints whenever the LLM has exactly two valid choices.
- Test the same prompt across Gemini, Claude, and GPT before committing to production.
- Place instructions at the bottom of the prompt when targeting Gemini Flash or Pro.
- Use two-stage generation: structured draft first, prose polishing second, for higher quality.
- Substitute placeholder URLs that look realistic rather than obvious dummies during prompt development.
- Validate generated URLs in post-processing and find-replace with verified real links.
- Break sequential dependencies by introducing intermediate steps that unlock parallel pipeline execution.
- Use small cheap models like Flash for easy classification tasks rather than premium models.
- Implement MCP clients in your products so users can extend functionality independently.
- Treat data leakage and prompt injection as primary risk surfaces in production AI systems.
- Build interruption and course-correction UX into any agent pipeline before considering full autonomy.
- Switch a string field to a string array when output quality feels too constrained.
- Manually handle steps where automation would cost more time than it saves long-term.
- Embrace AI for unexpected tasks like clipboard operations and code generation, not trivial scripting.
- Record input-output pairs from production traffic to build evaluation datasets over time.
- Run a token visualizer on prompts to confirm context size before debugging poor outputs.
- Send the transcript before instructions in long-context summarization to keep instructions salient.
