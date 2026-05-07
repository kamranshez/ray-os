---
video_id: bak7-C--azc
title: "🦄 Dynamic Schemas: #25"
url: https://www.youtube.com/watch?v=bak7-C--azc
channel: BoundaryML
---

### SUMMARY
Dex (Human Layer) and Vibhav (BoundaryML) demonstrate dynamic schemas — using LLMs to generate runtime schemas from images, then extracting structured data via BAML.

### IDEAS
- Dynamic UIs become possible when models generate schemas at runtime from arbitrary unknown input data sources.
- Two-step process: ask model for schema given image, then extract data using that schema.
- Meta-programming with LLMs resembles form builders and templating engines but works on arbitrary inputs.
- Type Form succeeded primarily by making schema creation visually pretty and effortless for users.
- React components themselves can be generated dynamically from schemas to render arbitrary JSON beautifully.
- Human review steps fit naturally between schema generation and data extraction for quality control.
- Saving generated schemas to a database lets you reuse them rather than regenerating constantly.
- Caching with semantic similarity lets similar images reuse previously approved schemas instead of regenerating.
- Return type must be specified separately from schema since multiple schemas may exist simultaneously.
- BAML output is roughly four times more token-efficient than equivalent JSON schema representations.
- Giving the model an "other code" dumping ground field prevents pollution of cleaner structured fields.
- The schema generation process ironically benefits from less rigid type systems for the meta layer.
- Dynamic schemas with no static types feel uncomfortable but unlock entirely new application categories.
- BAML's parser maps loose model output back into expected schemas even when prompts mislead it.
- GPT-OSS reportedly converts JSON schemas to TypeScript-like syntax internally for efficiency before reasoning.
- Building incrementally — schema first, then extraction, then rendering — makes complex AI workflows testable.
- Entity resolution patterns from prior episodes apply: consolidate schemas over time as drift becomes apparent.
- The any-type problem in dynamic rendering forces switch-based recursive renderers regardless of approach.
- Type builder in BAML lets you inject runtime schemas into otherwise statically typed function signatures.
- Streaming dynamic schemas requires custom SSE bridges since type completeness signals must propagate manually.
- Generated TypeScript and Python bindings from BAML guarantee zero drift between client and server types.
- Anthropic's recent custom UI feature uses essentially this same schema-then-render pattern under the hood.
- Schemas should be reseeded by humans editing model-generated initial drafts rather than purely autonomous.
- A dumping ground field is a generally underrated prompt engineering technique for cleaner structured outputs.
- Workflow drift between dynamic schemas and stable production extraction needs explicit consolidation steps.
- The model never knows it's working with a dynamic schema — it just sees a regular schema.
- Bezos's "good intentions don't work, mechanisms do" applies to AI workflow design and reliability.
- Removing rigid process can unlock Jevons-paradox effects where people try ideas they wouldn't have before.
- Open sourcing tools matters because otherwise inference gets wasted asking Einstein to count loose change.

### INSIGHTS
- Meta-programming with LLMs separates "what shape is the data" from "what are the values" elegantly.
- Token density beats expressiveness — concise schema syntaxes outperform verbose JSON schema for model generation.
- Giving models an explicit dumping ground beats fighting them on unwanted output through restrictive prompting.
- Dynamic systems need eventual consolidation; pure dynamism becomes a weakness once volume scales meaningfully.
- The two-call pattern (plan then execute) generalizes from agents to schemas to UI generation broadly.
- Type safety can be preserved across dynamic boundaries through generated bindings shared between client and server.
- Caching previously approved schemas turns a model problem into a database lookup over time naturally.
- Building AI features incrementally with testable units beats trying to demo full magical end-to-end flows.
- Rendering arbitrary JSON requires recursive switch-based logic; there's no shortcut around dynamic type rendering.
- Human-in-the-loop fits most naturally at structural decision points rather than at every data extraction.

### QUOTES
- "Dynamic UIs is one of the most powerful concepts that becomes possible in the world of genai." — Vibhav
- "This is basically just meta programming. You're having the LLM do some of the programming." — Vibhav
- "Type Form makes so much money because of how pretty they made making schemas." — Vibhav
- "Hide your keys, hide your wife." — Dex
- "Turns out the model was dumb at that. So I just gave it a dumping ground." — Vibhav
- "JSON schema is just extremely verbose. You get way worse results when you use JSON schema." — Vibhav
- "The LLM doesn't even know it's a dynamic schema. It just thinks it is the schema." — Vibhav
- "Any types suck and the whole point of using this is having static types you catch at compile time." — Dex
- "If you can define the schema really well, then you can actually have the model output this stuff." — Vibhav
- "These are all kind of well modeled as individual parts of the workflow that can be tested independently." — Dex
- "The original agent was use one LLM call to make a plan and then use another LLM call to execute it." — Dex
- "Worst case, you'll fail, but most things can be — and you start getting better at it." — Eugene
- "Good intentions don't work, mechanisms do." — Eugene quoting Bezos
- "If it's not open source, inference gets wasted — asking Einstein to count loose change." — Eugene
- "We just know for sure that during streaming the type is this type and when done it's this type." — Vibhav

### HABITS
- Define function signatures first before writing any prompt body when designing BAML functions.
- Always specify both schema and explicit return type rather than letting the model infer top-level.
- Use backticks in schema generation prompts to avoid escape character issues with model output.
- Save generated schemas to a database for reuse rather than regenerating on every similar request.
- Add human review steps between schema generation and downstream extraction for quality control.
- Run partial-state and final-state code paths separately when implementing streaming for typed outputs.
- Test dynamic schemas with manual type builder additions rather than relying on full pipeline.
- Use AI-generated images as filler music or visual placeholders during live stream lobby periods.
- Cross-post announcements to multiple Discord servers including external community spaces for reach.
- Read existing schemas from the database before asking models to generate new ones from scratch.
- Build SSE bridges manually when streaming structured output between backend and frontend systems.
- Render arbitrary JSON with recursive switch-based components since no library handles full dynamism.
- Always provide return type alongside schema when asking models to generate dynamic structures.
- Treat type drift detection as a signal for human review rather than automatic schema replacement.
- Open source internal tools whenever possible to avoid wasted inference across many users.

### FACTS
- A simple JSON schema describing the same data can be 333 tokens vs 86 tokens for BAML.
- BAML's full syntax description fits in roughly 30 to 60 lines for cursor-rules style injection.
- A required field declaration in JSON schema can take 73 tokens versus near zero in BAML.
- Anthropic recently shipped a custom UI feature using the same dynamic schema rendering pattern.
- GPT-OSS converts JSON schemas to TypeScript-like syntax internally before passing to the model.
- BAML auto-generates both Python and React TypeScript bindings from a single source-of-truth file.
- Type Form built a major company largely on making schema creation visually delightful for users.
- BAML's parser remaps loose model output to declared schemas even when prompts omit some fields.
- BAML supports dynamic class extension at runtime through a feature called type builder.
- Eugene's company is self-funded which lets them control open-sourcing decisions independently.
- The original agent pattern from 2023 used one LLM call for planning, another for execution.
- Skyrim loading art has become a meme placeholder for showing while Claude Opus is thinking.

### REFERENCES
- BAML — BoundaryML's structured generation framework, open source.
- Human Layer — Dex's company building AI human-in-the-loop infrastructure.
- AI That Works — the weekly show hosted by Dex and Vibhav.
- Type Form — referenced as a successful schema-builder UX example.
- Anthropic Claude — referenced for recently shipped dynamic UI feature.
- GPT-OSS — open weights model whose tool calling format was analyzed.
- LISP reader macros — referenced as conceptual analog to schema meta-programming.
- Swagger / OpenAPI — referenced as analog for schema-plus-return-type pattern.
- Pydantic — used by BAML for Python model dumping during streaming.
- FastAPI — used as the demo backend server in the live coding portion.
- Cursor — IDE used for the live walkthrough of BAML code.
- Skyrim loading screen meme — circulating as Claude thinking-state placeholder.
- Jeff Bezos — quoted on mechanisms versus good intentions.
- Jevons paradox — referenced regarding removing process unlocking exploration.
- Kindle — Eugene's co-founder reportedly worked on it.
- MCP (Model Context Protocol) — Eugene exposing Claude-Code-like product via MCP.
- Discord — used for cross-posting episode announcements and async discussions.
- Loom — referenced regarding weekly recap distribution patterns.

### ONE-SENTENCE TAKEAWAY
Use LLMs to generate schemas at runtime, then extract typed data — meta-programming unlocks dynamic UIs.

### RECOMMENDATIONS
- Build a two-call pipeline: one prompt generates schema, another extracts data using that schema.
- Add a return type field separate from schema since multiple types may exist simultaneously.
- Provide an "other code" dumping ground field to prevent pollution of cleaner structured fields.
- Prefer BAML or TypeScript-style schema syntax over JSON schema for four-times better token efficiency.
- Save generated schemas to a database and reuse them via semantic similarity rather than regenerating.
- Insert human review steps between schema generation and extraction for high-stakes production flows.
- Build incrementally: get schema working first, then extraction, then dynamic rendering on top.
- Use type builder or equivalent runtime type extension to inject dynamic schemas into typed functions.
- Generate client and server bindings from one source of truth to eliminate type drift entirely.
- Implement custom SSE bridges with partial, final, and error states for streaming structured output.
- Render arbitrary JSON with recursive switch-based components — there's no shortcut for dynamic types.
- Test dynamic schemas by manually constructing type builder inputs before integrating full pipeline.
- Consolidate schemas over time as patterns emerge; pure dynamism becomes weakness at production scale.
- Open source internal tooling so others don't waste inference solving the same problems.
- Use AI-generated images as background visuals during live stream lobby periods for ambiance.
- Cross-post episode announcements across multiple Discord servers to maximize community reach.
- Treat large schema drift as a human review signal rather than auto-accepting model output.
- Watch for entity resolution patterns: consolidate Microsoft, Azure, Xbox into single canonical entities.
- Apply Bezos's mechanisms-over-intentions principle when designing AI workflows for reliability.
- Keep detailed test cases that exercise type builder with realistic dynamic class additions.
