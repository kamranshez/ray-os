---
video_id: KJkvYdGEnAY
title: "🦄 building a coding bot: ep#3"
url: https://www.youtube.com/watch?v=KJkvYdGEnAY
channel: BoundaryML
---

### SUMMARY
Vaibhav and Dax from BoundaryML build a coding agent live, decomposing the problem into diff generation, application, and validation using progressively smaller models.

### IDEAS
- Coding agents transform an environment plus instructions into a new environment with modified files.
- Three core sub-problems exist: clarifying instructions, finding right files, and generating correct code.
- Generating whole files fails because output token limits cannot handle sophisticated codebases beyond eight thousand tokens.
- Diffs naturally compress information to only what the model actually needs to communicate back.
- Each pipeline stage may itself be a full agentic loop with its own internal structure.
- Apply diffs deterministically rather than agentically since string replacement needs no language model.
- Validation should run actual code rather than relying on language model self-assessment of correctness.
- Naming output fields uniquely matters because overloaded words like "diff" confuse model attention significantly.
- Telling the model "do not" something is harder than describing what to do positively.
- Triple backticks let the model produce multiline strings without worrying about JSON escape characters.
- Models trained on flat code generation perform worse when forced to embed code inside JSON.
- Role boundaries between system and user messages function as well-tuned automatic content separators.
- Smaller models benefit dramatically from supporting systems like ASTs rather than pure prompt engineering.
- Context management means deleting failed attempts so models pretend they got it right first try.
- Find-match-then-string-replace beats naive plus-minus diff parsing because matching is the hard verification step.
- Levenshtein distance and secondary LLM calls serve as fallbacks when exact string matching fails.
- AST validation catches syntax errors precisely without involving any language model in the loop.
- Recursive update-files calls with hardcoded fix-error instructions handle syntactical mistakes elegantly through self-similarity.
- Python's ast.parse walks the tree and yields imports without requiring any LLM call.
- Build pipelines that shift cost distribution leftward over time by replacing big-model calls.
- Ninety-five percent users cheap-and-fast matters more than optimizing the expensive long tail.
- Start with big models that work, then incrementally swap parts for smaller fine-tuned ones.
- The same accuracy techniques applied to big models make them dramatically better than naive prompting.
- New-code generation and code-update generation are fundamentally different problems requiring separate dedicated systems.
- V0 excels at first drafts but degrades by message twenty-five because updates are harder.
- UX innovations like element selection and file references solve context-providing problems no model can.
- Bad context cannot be corrected by any model; only good context unlocks accurate output.
- Indentation in prompts helps models the same way it helps humans — pattern recognition.
- Few-shot examples in dedicated fields beat instructions buried inside output schema descriptions.
- Temperature zero stabilizes outputs when iterating on prompt-engineering changes for diff generation tasks.
- Observations objects passed downstream track unfixable errors so plans can abort and retry.
- Different error types require different remediation strategies: missing libraries differ from typos significantly.
- Web search agents help fix install errors that LLM cannot solve from internal knowledge alone.

### INSIGHTS
- Decomposing agents into deterministic glue between focused prompts beats one giant bag-of-tools loop dramatically.
- The hard part of coding agents is applying diffs correctly, not generating the diffs themselves.
- Models perform best when output formats match how they were trained, not how engineers prefer.
- Context engineering equals deleting failed turns so the model never sees its own mistakes downstream.
- Traditional tools like ASTs and parsers should always replace LLMs for deterministic verification tasks.
- The LLM's only true job is converting context into tokens; surrounding code provides everything else.
- Pipeline maturity moves cost distributions leftward as engineering replaces capability with deliberate structural choices.
- UX design and model accuracy are inseparable — better interfaces capture the context models cannot.
- Recursive self-similar functions emerge naturally when you decompose problems into uniform fix-and-retry loops.
- Generating from scratch and updating existing code are fundamentally different problems with different optimal architectures.
- Negation instructions consume model attention disproportionately compared to equivalent positive capability statements.
- Smaller models become viable not through better prompts but through scaffolding around their weaknesses.
- Schema field naming directly affects output quality because models pattern-match on word semantics.
- Every probe and dial added to a pipeline becomes a knob for future cost optimization.
- Big models with good engineering beat big models with naive prompting by larger margins than expected.

### QUOTES
- "Diffs seem a little bit more tractable and naturally compressing the information I need to just what I need." — Vaibhav
- "It's not possible given the output token limits of the models today to really solve the constraint." — Vaibhav
- "I'd want to figure out the smallest model that I can use for each task." — Vaibhav
- "The idea of a not is just very very hard for it to go do." — Vaibhav
- "By renaming it to update code, it's probably a just a little bit easier for the model." — Vaibhav
- "I'm basically just managing the context. I'm pretending like I got the answer on the first try." — Vaibhav
- "If you have the right context and you have good instructions, it is really easy to go do that." — Vaibhav
- "Bad context is virtually impossible to correct." — Vaibhav
- "The LLM should not be doing syntax validation." — Vaibhav
- "It hasn't been trained on generating code inside a JSON object. It's been trained on generating code as a flat thing." — Dax
- "Your job of everything else is to get exactly the right most optimal context into the LM." — Dax
- "You're constantly shifting that curve to the left and making it kind of better." — Dax
- "Chat message twenty-five, I'm ripping my hair out trying to get it to do the thing." — Vaibhav
- "Just help the user give you the right piece of code." — Vaibhav
- "What we're really doing is we're applying engineering to make it cheaper, faster, more accurate." — Vaibhav
- "I showed it to Vaibhav. He said it sucks. I was like perfect." — Dax
- "I treat it like a system message even though it's user incoming message." — Vaibhav
- "It will just struggle to apply a diff. And it will struggle to perfect it." — Vaibhav

### HABITS
- Set temperature to zero when iterating on prompt-engineering changes to stabilize comparison between attempts.
- Read the full raw rendered prompt repeatedly to verify what the model actually receives.
- Rename overloaded schema fields whenever models seem confused about which concept they target.
- Use triple backticks for multiline code outputs instead of fighting JSON escape character problems.
- Treat user messages as content separators rather than as semantically meaningful chat conversation turns.
- Keep diffs small and emit multiple per file rather than one large monolithic patch.
- Track an observations object across the pipeline that downstream stages can inspect and modify.
- Build pipelines from big models first, then incrementally swap stages for cheaper smaller ones.
- Validate generated code with AST parsing before invoking any language model for error correction.
- Delete failed model turns from context windows once you finally get a successful response.
- Decompose every agent loop into smallest possible deterministic functions with focused prompts between them.
- Pass file names as parameters because models perform worse without explicit identifying context information.
- Add few-shot examples as standalone instructions rather than burying them inside schema descriptions.
- Indent prompts the way humans would for readability since models also pattern-match indentation.
- Run a hack day to convert pseudocode session notes into actual working repository code.

### FACTS
- GPT-4o and similar OpenAI models default user-role text into effectively system-message instruction handling behavior.
- Output token limits of current frontier models cannot fit most production codebase files entirely.
- Python's ast module exposes ast.Import and ast.ImportFrom node types via tree walking.
- Common Python install mistakes include pip install dot when python dash dot is required.
- V0 added element selection UX specifically because finding correct context proved foundationally difficult.
- Cursor lets users reference specific files inline because automated context selection remains unreliable.
- GPT-4o mini struggles with diff application while GPT-5 or 4.1 handle it in one shot.
- Four-space indentation tokens exist in tokenizer vocabularies allowing models to recognize nesting structure.
- Levenshtein distance measures approximate string similarity for fuzzy matching when exact matches fail.
- Llama 8B and DeepSeek-coder are candidate small models for narrow tasks like import detection.
- BAML's prompt rendering shows the literal final string sent to the underlying language model.
- The Python ast.parse function returns a syntax tree that yield statements can walk.
- BoundaryML hosts weekly community sessions building coding agents with viewer participation and questions.
- Claude code uses string-to-replace diffs and falls back to sed and grep on failure.
- Cypher query generation served as an earlier session example for context-window management techniques.

### REFERENCES
- BoundaryML BAML prompting framework
- GPT-4o, GPT-4o mini, GPT-4.1, GPT-5 (OpenAI)
- Claude code (Anthropic CLI tool)
- Cursor IDE
- V0 by Vercel
- StackBlitz
- Llama 8B
- DeepSeek-coder
- Ollama
- Python ast module (ast.parse, ast.Import, ast.ImportFrom)
- Levenshtein distance algorithm
- Browser tools MCP
- Next.js framework and TypeScript
- Cypher query language
- Earlier BoundaryML session on context management for query generation

### ONE-SENTENCE TAKEAWAY
Decompose coding agents into focused deterministic stages so smaller models with better scaffolding outperform monolithic loops.

### RECOMMENDATIONS
- Decompose agentic coding pipelines into update-files, generate-diffs, apply-diff, and validate stages with deterministic glue.
- Generate diffs as multiple small triple-backtick blocks rather than one monolithic patch per file.
- Pass file paths as explicit parameters since models lose accuracy without identifying file context.
- Replace negation instructions with positive capability statements because models follow do-this better than don't-do-that.
- Use AST parsing to validate generated syntax before involving language models in error correction.
- Apply diffs by finding the old string match first, then string-replacing rather than parsing.
- Delete failed model turns from context windows so future calls only see successful exchanges.
- Build observation objects threaded through every stage to track unfixable errors and abort cleanly.
- Start every pipeline with a big capable model, then swap individual stages for smaller alternatives.
- Detect imports using Python's ast module instead of asking a language model to enumerate them.
- Treat new-code generation and existing-code updating as fundamentally different problems requiring separate architectures.
- Add UX affordances like element selection and file references so users supply correct context themselves.
- Set model temperature to zero when iterating on prompts to stabilize output comparison between runs.
- Use triple backticks for multiline string outputs instead of fighting JSON escape character problems.
- Rename schema fields uniquely when models seem confused — never overload one word for multiple concepts.
- Read the full rendered prompt every iteration to confirm what the model actually receives.
- Place few-shot examples as standalone instructions rather than burying them inside output schema descriptions.
- Recursively call update-files with fix-error instructions when validation finds syntactical mistakes in generated code.
- Route different error types to different remediation strategies: web search for installs, AST for syntax.
- Optimize for the 95% user case distribution rather than over-engineering the expensive long tail.
