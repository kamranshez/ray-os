---
video_id: qdfwmYTO0Aw
title: "Prompting Is Becoming a Product Surface: 🦄 #43"
url: https://www.youtube.com/watch?v=qdfwmYTO0Aw
channel: BoundaryML
---

### SUMMARY
Vaibhav (Boundary/BAML) and Dex (HumanLayer) demonstrate building dynamic schemas so end users like doctors customize AI prompting interfaces without engineering involvement.

### IDEAS
- Prompting resembles dashboards where users define their own structure rather than receiving hardcoded outputs from vendors.
- Hardcoding AI output formats forces engineers to choose customers, narrowing market reach to compatible workflows only.
- Pure freeform text input degrades reliability; constraining users into form builders dramatically increases output consistency and accuracy.
- Dynamic structured outputs let each customer define schemas while preserving engineering guardrails underneath the user-facing layer.
- Translation layers convert user-friendly concepts like bullet points into engineer-friendly types like string arrays underneath.
- Schema fields should split into extraction concerns and rendering concerns, kept separate for cleaner system architecture.
- Display-only metadata like units never reaches the LLM but controls how UI renders the structured output.
- Doctors should never see words like object, JSON, or array anywhere in the form builder interface presented.
- Custom canonical types like Temperature beat nested object definitions because they encode domain knowledge once for everyone.
- Generating schemas from prior notes lets first demos look exactly like a doctor's existing workflow patterns.
- Schemas need only be generated once per customer or per structure change, not on every transcript.
- Three doctor input modes coexist: regenerate from scratch, edit form fields meticulously, or chat-amend natural language.
- Hybrid static plus dynamic schemas let engineers lock universal fields like name while leaving domain fields flexible.
- A list of strings produces dramatically more detail than a paragraph string when extracting bullet points from transcripts.
- The how-to-render decision is separate from the extraction decision and most builders forget this entirely.
- Vertical SaaS edge comes from understanding customers deeply enough that they do less configuration work themselves.
- Prompting will not generalize across domains because defaults, types, and UI hybrids depend on customer context.
- Structured output parsers reject prompt injection attacks because malicious responses fail schema validation deterministically before reaching code.
- Engineering-team prompts and user prompts merge into one description, with engineering opinions winning on universal preferences.
- Multi-step pipelines fuse a transcript plus an output description to produce structured data plus rendered display.
- Field render variants like exact, elevated-only, or grouped change UI behavior without changing extraction prompts at all.
- Schema generation from English description converts vibes into concrete typed JSON saved to database for repeated use.
- The model can infer that height is a number, so users describing fields shouldn't need to specify primitive types.
- Form builders feel outdated but pure-text chat UIs lose precision; the right answer combines both progressively.
- Recursive schema definitions let object types nest within object types just like JSON schema but with friendlier vocabulary.
- Live coding humbles engineers and reminds everyone that humans still make typing mistakes despite AI assistance available.
- Default values can fill ungiven fields like height and weight automatically without disrupting the extraction pipeline.
- A union of literal strings constrains LLM output to predefined options like normal, elevated, low for temperature.
- Bulleted-list as a JSON-schema array-of-strings wastes tokens; a custom type called bulleted-list reads more accurately.
- Image and PDF inputs work transparently as long as the type system supports multimodal modality declarations.

### INSIGHTS
- The best AI products treat prompting as a customizable product surface, not a static engineering artifact baked in.
- Constraining user input through form builders preserves flexibility while raising reliability above unconstrained natural-language prompting interfaces dramatically.
- Separating extraction schema from rendering schema is the architectural insight most AI builders miss when shipping production systems.
- Domain-specific canonical types beat generic JSON-schema primitives because they encode tribal knowledge once for all downstream consumers.
- Vertical SaaS wins by absorbing customer-specific defaults so users configure less while getting more accurate output every time.
- Structured output validation provides incidental prompt-injection defense because malicious responses fail deterministic parsers before reaching application code.
- Schema generation from natural-language descriptions converts ambiguous vibes into reusable typed contracts saved per-customer in databases.
- The translation layer between user vocabulary and engineering vocabulary is where customer empathy becomes durable competitive advantage.
- Generating onboarding demos from a customer's prior data produces instant familiarity beating any generic example you could imagine.
- Engineering opinions should override user preferences for universal truths like avoiding six-sentence bullet points across all customer contexts.
- Hybrid schemas combining static engineer-defined fields with dynamic user-defined fields balance reliability against per-customer customization elegantly.
- The model can infer primitive types from context, so user-facing schema builders should expose only domain-meaningful concepts.
- Multi-modal inputs slot into structured-output pipelines transparently when the type system declares image, PDF, audio, or video natively.

### QUOTES
- "Prompting feels very much like databases sometimes where the most powerful systems let users build their own." — Vaibhav
- "I've never seen a dashboard company that actually has hardcoded dashboards." — Vaibhav
- "If your users do stuff then it's not going to work, and if you do stuff then it's flexible." — Vaibhav
- "The more flexible your doctors give you of an input, the worse the quality and reliability." — Vaibhav
- "You want the users to have some control over what you do, but not all control." — Vaibhav
- "You don't want them to have to be like height is a number — a model can tell you." — Dex
- "Salesforce at the end of the day is just a layer of automation on top of a SQL database." — Dex
- "Clients are king in this world for at least a little while longer." — Dex
- "Live coding has a trade-off, as much as I wish it didn't." — Vaibhav
- "Vibe likes to live code because it humbles him and reminds him that he's still human." — Dex
- "If you build a thing called bulleted list, it's going to be more accurate for end users." — Vaibhav
- "Bulleted list would end up being an array of strings — that's so dumb." — Vaibhav
- "Description goes to the LLM, display unit goes to the rendering system." — Vaibhav
- "Some of these doctors will fight with each other based on the description that they have." — Vaibhav
- "If you deeply understand the customer, the customer will have to do less work." — Vaibhav
- "There's a meta level here we can go — generate a schema from prior notes." — Vaibhav
- "The deterministic parser is just going to blow up and that data never reaches your code." — Dex
- "Nobody wants six sentence items in that list." — Dex
- "It's all deeply technical AI stuff, but it's all about clients are king." — Dex

### HABITS
- Vaibhav lets cursor scaffold test cases describing patient backgrounds while he keeps thinking about output schema design.
- Dex sketches whiteboard pipeline diagrams during live demos to verify mental models match the implementation accurately.
- The hosts run weekly Tuesday 10am livestreams called AI networks demonstrating practical AI pipeline architecture patterns.
- Vaibhav prefers writing custom domain-specific types over reusing JSON Schema primitives for end-user-facing schema definitions.
- The team flags topics during demos to revisit so architectural threads aren't lost in tangential live discussion.
- Dex maintains parallel structures for display metadata separate from extraction types to keep deterministic overlays clean.
- Vaibhav tests prompt injection scenarios deliberately to verify structured-output parsers reject schema-violating responses every single time.
- The hosts share working code repositories publicly after each session so viewers can experiment with the demonstrated patterns.
- Vaibhav uses GPT-4o-mini as a default cheap model for schema-extraction prototypes during live demonstrations and exploration.
- Dex frames complex topics by demanding zoom-out summaries from Vaibhav so viewers get actionable takeaways consistently delivered.
- The pair invite domain experts like medical-tech specialists to contribute deeper knowledge during dedicated future episodes.

### FACTS
- Boundary makes BAML, a programming language designed specifically for handling nondeterministic AI system behavior in production.
- HumanLayer builds agentic coding systems and an IDE for getting agents to solve complex codebase problems.
- Salesforce custom objects are dynamically created database tables under the hood despite the user-facing object terminology.
- Medical scribe products help doctors write patient notes after conversations using AI transcription and summarization pipelines.
- BAML supports image, PDF, video, and audio types as inputs for multimodal extraction across structured-output schemas.
- Python dictionaries preserve insertion order since version 3.7 but ordering can break across serialization boundaries unexpectedly.
- The BAML examples repository contains a project converting JSON schemas into dynamic BAML schema definitions automatically.
- PostHog visualizes the same underlying data in totally different ways making the visualization the actual product value.
- Type form and Google Forms popularized recursive form-builder UX patterns that everyone in the world knows how to operate.
- Epic is a major electronic health record system into which medical scribe AI outputs commonly get injected programmatically.

### REFERENCES
- BAML programming language by Boundary
- HumanLayer agentic coding IDE
- Salesforce custom objects
- PostHog dashboards
- Type form
- Google Forms
- Epic ERP / EHR
- GPT-4o-mini (OpenAI)
- Cursor IDE
- Storybook
- Niston (Twitter, medtech AI builder)
- Ralph Wiggum episode (prior livestream reference)
- BAML examples repo (dynamic JSON-to-BAML converter)
- AI networks weekly livestream (Tuesdays 10am)

### ONE-SENTENCE TAKEAWAY
Expose dynamic schemas as a product surface so each customer defines structure while engineers preserve guardrails.

### RECOMMENDATIONS
- Build form builders not chat boxes when collecting user-defined output structure for AI extraction pipelines today.
- Separate extraction schema from rendering schema so display metadata never pollutes the LLM prompt context unnecessarily.
- Create domain-specific canonical types like Temperature instead of nesting generic objects everywhere across customer-facing schema builders.
- Generate onboarding demo schemas from each customer's prior data so first impressions match their existing workflow exactly.
- Save generated schemas to a database per-customer so you regenerate only when the user changes structure preferences.
- Offer three schema-editing modes: regenerate from English, edit fields directly, or chat-amend with natural language updates.
- Hide engineering vocabulary like JSON, object, and array completely from non-technical user-facing schema configuration interfaces always.
- Inject engineering-team opinions like length limits as hardcoded prefixes regardless of what individual end users specify themselves.
- Combine static engineer-defined fields with dynamic user-defined fields in the same schema for predictable plus flexible behavior.
- Use union-of-literal-string types to constrain LLM outputs to predefined option sets like normal, elevated, or low.
- Render display-only metadata like units in the UI layer without ever including those fields in the LLM prompt.
- Trust models to infer primitive types from context instead of asking users to specify number versus string explicitly.
- Test prompt-injection scenarios deliberately to confirm structured-output parsers reject schema-violating responses before they reach application code.
- Skip JSON Schema entirely; design a vocabulary that matches your domain users instead of generic engineering primitives.
- Pass images, PDFs, audio, or video through the same structured-output pipeline using multimodal type declarations natively supported.
- Watch next week's episode on agentic back pressure for executable research and feedback-loop optimization techniques covered live.
