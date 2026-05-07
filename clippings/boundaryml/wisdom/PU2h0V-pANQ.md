---
video_id: PU2h0V-pANQ
title: "Cracking the prompting interview: Ep #9"
url: https://www.youtube.com/watch?v=PU2h0V-pANQ
channel: BoundaryML
---

### SUMMARY

Vaibhav and Dexter from BoundaryML demonstrate practical prompting techniques for citations, diarization, code generation, and structured outputs using BAML across real-world examples.

### IDEAS

- Models struggle generating long opaque token sequences like URLs that carry no semantic meaning whatsoever.
- Replace URLs in citations with integer indexes, then remap programmatically after the model finishes.
- Each token a model generates accurately compounds error probability across the entire output sequence.
- Reading your own prompt carefully reveals more bugs than continuously adding more prompt instructions.
- Symbol tuning replaces semantic labels with arbitrary symbols so descriptions carry full classification meaning.
- Diarization outputs should reference dialogue indexes, not regenerate transcript text, saving order-of-magnitude tokens.
- Aliasing field names like idx instead of dialogue_index reduces output tokens and inference burden.
- Always give models an "other" escape hatch to prevent hallucination on ambiguous classification cases.
- Asking a model to count line numbers manually is terrifying versus pre-numbering the input.
- Inline reasoning comments per JSON field beat one big upfront reasoning block for targeted analysis.
- Models output backslash-n tokens when forced into JSON, degrading code quality versus markdown backticks.
- Triple backticks inside JSON strings let models write code naturally with real newlines preserved.
- Strict JSON schema enforcement zeroes out the model's most likely tokens, reducing output quality measurably.
- Letting the model pick its highest-probability token usually beats clever pre or post-processing tricks.
- Few-shot example content steers the model heavily, so use few-shot only for structural mimicry.
- Run evals offline on stored data rather than adding latency-expensive reasoning to production pipelines.
- Adding company names and attendees as context dramatically improves event-classification quality on Luma scrapers.
- Building UIs from structured output beats parsing strings; v0 generates these in sixty seconds.
- Most code in training sets is bad, so blindly mimicking common patterns yields mediocre results.
- Role-playing prompts like "you are a senior engineer" rarely improve actual model output quality.
- Mixing instructions and content throughout a prompt confuses models more than clean section separation.
- Linters enforce code style better than prompting; format generated code after the model finishes.
- Generate cursor rules or lint configs from existing code instead of forcing models to read whole files.
- Constraining schemas with required fields drops hallucinated entries during parsing without prompt changes.
- Word-per-minute hints help models estimate durations without actually counting characters themselves.
- Pre-numbering input lines makes coding agents far better at executing precise edits.
- Letting models output broken-but-readable JSON often beats forcing strict valid JSON for complex content.
- Tell the model what indexes mean rather than asking it to infer them across context.
- The token "index" beats "idx" because it has more semantic understanding baked into pretraining.
- Half-percent accuracy improvements compound massively when running prompts a hundred thousand times daily.
- Identifying break points in dialogue can be solved as an indexing problem rather than text generation.
- Cleverness in pre-processing often hurts; computer vision learned to just give models everything.
- Output formats determine attention; programmers see labels but the LLM only attends to descriptions.
- Dynamic enums with aliases let you map model symbols back to real values automatically.

### INSIGHTS

- Reduce model burden by making generated tokens semantically meaningful, structurally short, and mappable through deterministic post-processing.
- Prompt engineering mirrors software engineering: separate concerns, name well, refactor, and read your own code.
- The best models still benefit from indexing tricks because attention works better on focused token segments.
- Strict output formats trade quality for parseability; loose JSON with smart parsers wins both battles.
- Hallucination prevention comes from giving models legitimate escape hatches, not from louder prompt scolding.
- Reasoning placement matters: per-field comments target precision, top-level reasoning sets overall direction.
- Training-set mimicry explains why backticks beat JSON-escaped code; honor what models learned naturally.
- Latency-sensitive pipelines should defer evaluation reasoning to offline batch jobs over the same data.
- Symbolic tuning works because it forces all attention onto descriptions instead of culturally-loaded label names.
- Build small feedback loops: change one thing, run evals, accept or reject, repeat ruthlessly until shipped.
- Context injection from external sources like calendars or LinkedIn dramatically beats clever prompting alone.
- Schema constraints handle edge cases more reliably than prompt instructions about what to skip.
- The smallest indexable unit defines the cheapest representation; find it before generating anything else.
- Reading the actual rendered prompt catches bugs that endless instruction additions never reveal or fix.

### QUOTES

- "Prompting is literally like software engineering." — Vaibhav
- "RTFP means read the fucking prompt." — Vaibhav
- "There's no meaning baked into that random string of characters. It's just a pointer." — Dexter
- "Why make the life harder for the model?" — Vaibhav
- "We want to prevent hallucinations when possible, and we do that by giving the model an out." — Vaibhav
- "Don't try and be clever with token generation. Just let the model pick the best token." — Vaibhav
- "Zero attention on the label name because that's for the coders. All attention on the description." — Dexter
- "If you really want the very best code performance, let it write between markdown backticks." — Dexter
- "The model doesn't care who it is. It just has to know the job." — Vaibhav
- "Just like the most code out there is kind of shit, you probably shouldn't follow most code." — Vaibhav
- "Don't add more latency to a pipeline that has this." — Vaibhav
- "Each of these things that you're generating here is latency." — Vaibhav
- "How do you push things even further? How do you get another half a percent?" — Dexter
- "The break is where I define the line." — Vaibhav
- "If you have a Linter with opinionated formatting, it'll be formatted exactly how you want." — Vaibhav

### HABITS

- Read the rendered prompt aloud before adding more instructions when iterating on outputs.
- Test with a real production bug case before committing to broader eval set runs.
- Show prompts to peers and ask them to roast for honest critique.
- Iterate on one schema field at a time rather than rewriting whole prompts.
- Use BAML test cases inline alongside function definitions for fast feedback loops.
- Default to markdown backticks for code generation rather than escaped JSON strings.
- Add an "other" enum variant whenever building classification prompts to absorb ambiguity.
- Run a separate offline eval pipeline rather than evaluating during latency-sensitive serving paths.
- Switch models when the current one ignores instructions repeatedly during prompt iteration.
- Use cursor or AI tools to generate test cases quickly during live coding sessions.
- Convert duration hints into structured fields with descriptions like "120 words per minute".
- Pre-number transcript lines before passing them to a diarization model.
- Strip role-playing preambles like "you are an expert" from existing prompts during cleanup.
- Generate a v0 UI from any structured output to validate the data model quickly.

### FACTS

- "YouTube" tokenizes as a single token in OpenAI's tokenizer due to platform prevalence.
- "?v=" tokenizes as a single token in OpenAI's tokenizer because of YouTube URL frequency.
- A typical YouTube video ID requires roughly ten tokens for the model to generate accurately.
- Comments are technically not valid JSON syntax according to the official specification.
- Strict JSON mode in OpenAI zeroes out probability for tokens that would break the schema.
- Average human speech runs about 120 words per minute in conversational pacing.
- The tldraw founder presented at AI Engineer about generating SVGs through structured intermediate objects.
- Black is an opinionated Python formatter that explicitly offers no configuration options whatsoever.
- Go enforces capitalization rules for exporting symbols rather than leaving it to convention.
- BoundaryML's "AI That Works" series began in March of the same year.
- Cursor uses a system of cursor rules to enforce codebase consistency during generation.
- BAML supports dynamic enums with aliases that remap model output back to real values.
- Luma hosts roughly a hundred tech events per month in the San Francisco scene.

### REFERENCES

- BAML (BoundaryML)
- 12 Factor Agents by Dexter
- tldraw founder talk at AI Engineer (SVG generation via structured objects)
- OpenAI tokenizer
- Cursor IDE and cursor rules
- v0 by Vercel
- Anthropic Claude (Sonnet 1022, 2024-10-20 model)
- OpenAI GPT-4o
- Black (Python formatter)
- ESLint and Biome (JavaScript linters)
- BoundaryML Discord community
- Luma (event platform)
- Sahill (referenced as automated video content competitor)
- BAML symbol tuning documentation
- BAML dynamic enums documentation

### ONE-SENTENCE TAKEAWAY

Reduce model burden by indexing, aliasing, and reading prompts; let deterministic code handle what models cannot.

### RECOMMENDATIONS

- Replace citation URLs with integer indexes and remap them in code after parsing.
- Pre-number transcript lines so diarization models output indexes rather than rewriting full text.
- Always include an "other" escape hatch in classification enums to prevent forced hallucination.
- Read your rendered prompt completely before adding any new instructions or examples.
- Use markdown triple backticks inside JSON strings for code generation instead of escaped strings.
- Move evaluation reasoning fields to a separate offline pipeline to keep production latency low.
- Apply symbol tuning when descriptions carry meaning that semantic labels would dilute through training associations.
- Place per-field reasoning comments before fields when targeted analysis matters more than overall direction.
- Constrain schemas with required fields like first_name to drop hallucinated entries during parsing automatically.
- Inject contextual information like attendee lists or calendar data instead of relying on memory.
- Generate a v0 UI from any structured output to immediately validate the data model.
- Run a linter or formatter on generated code rather than prompting for stylistic consistency.
- Use few-shot examples for output structure mimicry, never for content the model should learn.
- Switch underlying models when one repeatedly ignores instructions instead of fighting the prompt.
- Submit your prompts to community roasts; observed critique beats solo iteration on quality.
- Drop role-playing preambles like "you are an expert" since they rarely improve real outputs.
- Use BAML test cases inline with function definitions for tight feedback loops during iteration.
- Track accuracy across small prompt changes; half-percent gains compound at production scale.
- Convert any "count things" instruction into pre-computed indexes the model just references.
- Generate cursor rules from a few example files rather than reading whole files repeatedly.
