---
video_id: RnyicgiSkis
title: "Prompt Shepherds - October 4, 2024"
url: https://www.youtube.com/watch?v=RnyicgiSkis
channel: BoundaryML
---

### SUMMARY
BoundaryML co-founders Vaibhav and Aaron host Faaez from Sherlock AI to demonstrate building agentic frameworks using BAML, structured prompting, and live coding fact-extraction.

### IDEAS
- Agents are fundamentally just while loops wrapping switch statements that route inputs into distinct typed actions.
- Mixed structured outputs require modeling actions as separate types, not stuffing branching logic into one massive prompt.
- User actions exit the outer while loop; tool actions stay inside the inner loop and recurse.
- Structured prompting reduces token count both on input schema description and on output by removing Json overhead.
- Forcing OpenAI structured outputs makes models hallucinate fitting unrelated queries into rigid schemas regardless of intent.
- BAML lets the model output freeform text, then parses it locally without strict schema enforcement on tokens.
- Schema descriptions in BAML use eleven tokens where Json schema would consume dozens for the same field.
- Streaming UI updates like loading dots dramatically improve perceived accuracy and user trust in agent responses.
- Citations should be matched against source content programmatically to detect hallucinated quotes via simple string containment.
- Breaking prompts into smaller typed functions beats one massive prompt with conditional branching instructions inside.
- Iterating on prompt structure beats adding more instructions; data model changes guide the model's thought process.
- Chain of thought can be embedded directly in the schema as a "thoughts" field instead of separate calls.
- Always start prompt engineering by collecting real test cases before writing any actual prompt code.
- Enums with explicit options outperform freeform classification because the model maps responses into your finite type system.
- The "other" enum variant catches cases where models pick training-data values not in your schema.
- Aliasing field names in prompts versus code lets you optimize prompt clarity without breaking python type bindings.
- Direct quote citations enable supporting context display in UI by surrounding the matched text with article context.
- Approximate matching beats exact string matching for citation verification since models drop minor punctuation often.
- Retry policies belong on the function definition, not scattered through agent code that orchestrates flow.
- Models can reasonably output unparseable Json with a missing escape; lenient parsers fix this without retries.
- Multimodal types in BAML accept either string or image, letting the same function handle both inputs.
- Quick-prompt UX patterns hide prompt engineering from users who are bad at writing prompts themselves.
- Each fact should bundle a summary plus citation array, separating semantic content from supporting evidence.
- Speaker attribution within quotes adds another structured layer beyond plain citation extraction.
- Function calling structures the agent's decision space as a discriminated union of action types.
- Static analysis errors on prompts catch typos and missing variables before runtime LLM calls happen.
- Treating LLM outputs as data transformations enables composing pipelines like regular software functions.
- Live preview of rendered prompts including injected variables shortens the prompt iteration feedback loop.
- A single broken citation can be debugged with a follow-up LLM call analyzing why matching failed.
- Cheaper models like GPT-4o-mini handle simple classification tasks adequately without burning expensive tokens.

### INSIGHTS
- Treating LLMs as untyped functions with structured returns transforms prompt engineering into ordinary software composition work.
- The right abstraction for agents is two nested while loops separated by user-action versus tool-action boundaries.
- Strict schema enforcement on output tokens trades robustness for hallucinations when inputs don't match expected structure.
- Token efficiency on schema descriptions improves model accuracy because shorter prompts present easier comprehension tasks.
- Verifying citations programmatically against source text catches hallucinations cheaper than asking another model to verify.
- Structured prompting moves intelligence from sprawling instruction text into typed data models the model populates.
- Streaming partial outputs requires every field be optional so consumers handle in-flight incomplete states gracefully.
- Discriminated union return types let one function gracefully fall back when primary intent doesn't match.
- Prompt iteration speed depends on having real test cases captured upfront, not synthesized after writing prompts.
- Chain of thought embedded in schema beats separate reasoning calls because it stays in one cheap inference.
- Software composition wins over prompt complexity; if statements outside the LLM beat conditionals inside the prompt.

### QUOTES
- "When you realize nothing is lacking the whole world belongs to you." — wall quote
- "Agents are just while loops." — Vaibhav
- "Prompts should have static analysis errors available to you." — Vaibhav
- "What if everything doesn't have to come from an LLM?" — Vaibhav
- "Mixed output is very challenging to do in just one long prompt." — Faaez
- "The way I think about it is you exit the while loop anytime you respond to a user." — Faaez
- "Is it a user action or is it a tool action?" — Faaez
- "You're guiding the thought process by changing the structure." — Aaron
- "It doesn't matter what the model said, what matters is my data type." — Vaibhav
- "Giving it a specific example can often make your model worse not better." — Vaibhav
- "On the input side you've made the problem harder." — Vaibhav
- "Your code should not be complex." — Vaibhav
- "We just made it on the web as well because people shouldn't have to install BAML." — Vaibhav
- "I write code instead of writing prompts." — Vaibhav
- "Agents are just while loops, if statements, and regular functions transforming data." — Vaibhav

### HABITS
- Always start prompt engineering work by collecting concrete test case files before writing any prompt code.
- Use cheaper models first, then escalate complexity only if the simpler model fails on tasks.
- Test prompts in isolated playground before integrating into application python or typescript code paths.
- Write data types as code first, then let prompt structure follow the type definitions naturally.
- Add retry policies declaratively on function definitions rather than wrapping calls in try-except blocks.
- Inspect raw web requests in the playground to verify nothing magic is being injected behind scenes.
- Prefer UV as python package manager for faster dependency resolution and rust-based performance benefits.
- Stream LLM outputs whenever latency might exceed two seconds to maintain user perceived responsiveness.
- Validate citations by string-matching against source content programmatically before showing them to end users.
- Save real-world failure examples as test cases the moment they happen during development sessions.
- Break prompts into smaller typed functions whenever conditional branching logic appears inside one prompt.
- Keep python iteration loops separate from BAML iteration loops to avoid context-switching overhead during debugging.
- Use enums with explicit "other" variants to catch model outputs that fall outside expected categories.
- Watch other engineers prompt engineer to absorb different mental models for the same problem space.
- Alias field names in prompts versus code when prompt clarity conflicts with maintainable variable naming.

### FACTS
- BAML is a programming language built specifically to make LLMs more consistent without any fine-tuning.
- BAML is written in Rust, the same language behind UV the python package manager.
- OpenAI structured outputs force the model to emit exact tokens matching the provided Json schema.
- Json mode alone produces parseable Json but cannot enforce specific field schemas like structured outputs can.
- Sherlock AI is an AI co-pilot for traders and investors aiming to democratize market expert access.
- The BAML playground runs entirely in the browser via WebAssembly for prompt iteration without server calls.
- BAML's parser handles unquoted Json keys and missing escape characters that strict Json parsers reject outright.
- Removing quotes around keys in BAML output reduced a sample prompt from 115 tokens to 105 tokens.
- Json schema representation of a string-typed date field consumes eleven tokens versus two in BAML syntax.
- BAML supports retry policies declaratively with model fallback chains like GPT-4o falling back to GPT-4o-mini.
- Structured outputs from OpenAI never refuse requests; they always force-fit responses into the provided schema.
- BAML data structures are globally available across all .baml files in a project without explicit imports.
- The BAML playground supports multimodal inputs where types accept either string or image references.
- Sherlock's quick-prompts feature pre-structures user queries to avoid requiring users to write prompts themselves.
- BAML's CTX.output_format helper injects type schema information into prompts automatically at render time.

### REFERENCES
- BoundaryML — programming language and tooling company building BAML
- BAML — domain-specific language for structured LLM prompting
- Sherlock AI — Faaez's AI co-pilot product for traders and investors
- LangGraph — framework Faaez tried before switching to BAML
- UV — rust-based python package manager
- OpenAI GPT-4o and GPT-4o-mini — models used in live demos
- Phi-3 and Llama 3 — local models that work with BAML
- Cursor — IDE used during the live coding session
- VS Code — supports BAML extension officially
- promptfiddle.com — web playground for trying BAML without local install
- CNN, BBC, Reddit, Twitter, Facebook — news source enums in the demo
- boundaryml/prompt-shepherds — github repo for the session code
- Luma — event platform used to gather pre-meeting topics
- Zoom — video conferencing platform hosting the session
- Tailwind CSS and Next.js — used in the resume rendering demo

### ONE-SENTENCE TAKEAWAY
Agents are while loops over typed actions; structured prompting beats massive prompts at scale.

### RECOMMENDATIONS
- Model your agent as a switch statement over typed action variants rather than one branching prompt.
- Verify LLM citations by string-matching them against source content before displaying to end users.
- Write real test cases first, then iterate prompts against them rather than synthesizing examples afterward.
- Use enums with explicit "other" fallback variants to catch outputs falling outside expected categories.
- Stream long-running LLM responses with loading indicators to maintain user trust during agent processing.
- Embed chain-of-thought as a "thoughts" field in your schema instead of making separate reasoning calls.
- Break monolithic prompts into smaller typed functions whenever conditional branching logic appears inside.
- Avoid OpenAI strict structured outputs when input intent might not match your schema exactly.
- Try BAML at promptfiddle.com before committing to install the VS Code or Cursor extension locally.
- Inspect raw HTTP requests during prompt development to verify nothing unexpected gets injected automatically.
- Add retry policies as declarative function annotations rather than wrapping calls in application code.
- Use cheaper smaller models for simple classification tasks; escalate to larger models only when needed.
- Alias field names between prompt and code when prompt clarity conflicts with python variable naming.
- Watch other engineers prompt engineer live to expand your mental models for similar problem spaces.
- Keep all action types as a discriminated union return so functions gracefully handle off-topic queries.
- Pull source-context windows around matched citations in UI to build user trust through verification transparency.
- Store API keys in environment variables and never share them on screen during live demos.
- Use UV as python package manager for faster dependency resolution and rust-backed performance gains.
- Treat LLM outputs as data transformations, composing them like regular software functions in pipelines.
- Skip the prompt rewrite when changing data model alone produces the desired thought process improvement.
