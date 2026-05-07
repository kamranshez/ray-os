---
video_id: jzhVo0iAX_I
title: "Multimodal Evals:🦄 #34"
url: https://www.youtube.com/watch?v=jzhVo0iAX_I
channel: BoundaryML
---

### SUMMARY
Kevin Gregory and Dexter join Vivoth on AI That Works to demonstrate building multimodal receipt extraction evals using Indonesian receipt data and BAML.

### IDEAS
- Useful self-driving training data is the weird edge cases, not sunny empty highways every day
- Designing systems remains crucial knowledge even as AI writes most production code for engineers
- Programming is fundamentally about building a theory, not merely typing characters into editors
- Switching from GPT-4o to Gemini Flash dramatically improved OCR accuracy with no prompt changes
- Real-world receipts contain rounding, discounts, taxes that randomly appear and surprise extraction systems
- OCR loses structural semblance whenever images tilt slightly off the rotational normal axis
- Runtime invariant evals eliminate the need for expensive hand-labeled golden datasets initially
- Sum validation, subtotal consistency, grand total calculation work as algebraic invariants on extractions
- Building tooling that screams obvious mistakes accelerates iteration faster than hand labeling everything
- Hard-coding absolute values on negative line items would break correctly cancelling discount-and-item pairs
- Designing data shape upfront makes the second similar project trivially fast to build
- Three to four hours sufficed because Kevin reused architecture from his prior classification pipeline
- Two pipelines plus visualizer with shared data contract is the clean separation pattern
- Each new eval costs effectively zero because they append into a shared list
- Tolerance margins matter for floating-point math because exact equality always fails eventually
- Prompt optimizers overfit when your eval definitions themselves contain false positive failures
- The real optimization target is finding rare relevant data, not optimizing on common data
- Ship at 95% with UI flagging failures rather than waiting for perfect prompt accuracy
- Self-correcting loops feed eval failures back as prompt context for second-attempt extraction
- Evals as a business resemble UI components: domain-specific metrics belong to your product
- JSON serves humans as much as machines, otherwise everyone would just use protobuf
- Iterating data structure and prompt together leverages prompting through your output format pattern
- Looking at raw data first uncovered Indonesian currency conventions before any code was written
- Cursor brainstorming sessions accelerate eval design when you describe the extraction task clearly
- Discount appearing as negative-priced line item produces correct totals through cancellation magic
- Restaurant taxes like Indonesian PB1 only sometimes apply and only sometimes hit the total
- Human-in-the-loop on flagged failures beats requiring users to enter every receipt manually
- Vertical AI pipelines need reliability comparable to deterministic software, not vague excuses
- Checkpoint pipelines need different JSON shape than single-shot extraction pipelines like receipts
- Multiple right answers existed in classification but receipt totals have one correct number
- Streamlit reads the same JSON the eval harness wrote, eliminating any custom integration code
- Versel-like preview environments could exist for evals if someone packaged them cleanly
- Retry with exponential backoff handles flaky multimodal extraction failures cheaply and effectively

### INSIGHTS
- Invariant-based runtime evals replace golden datasets for problems with mathematical structure inside outputs
- Investing in data-shape design upfront compounds across every subsequent project sharing the abstraction
- Prompt optimizers magnify whatever eval signal you provide, including its silent false positives
- Ship products at imperfect accuracy by transferring the burden of verification onto the user interface
- The hard part of code was always design and theory, never the actual typing of characters
- Real-world data discovery beats specification: the discounts and rounding emerged through eval observation
- Tooling that screams mistakes obviously accelerates discovery faster than tooling demanding manual interpretation
- Self-correcting agent loops convert eval failures into runtime guardrails inside the production pipeline
- Buying evals as metrics is a scam; buying eval harnesses and infrastructure can be reasonable
- Looking at your data with no abstractions remains the highest-leverage debugging activity always
- Floating-point tolerance is non-optional infrastructure for any numerical extraction or calculation pipeline
- Edge-case data has higher value per sample than abundant common data for genuinely improving systems
- Pipeline architecture must mirror eval architecture; checkpoints in code beget checkpoints in evaluation
- Structured outputs let you iterate prompt and schema simultaneously, exposing missing fields through failures

### QUOTES
- "Knowing how to design systems is going to be really really important" — Vivoth
- "Programming is building a theory, and building a theory and designing this stuff is really really important" — Vivoth
- "One of the biggest improvements I made was just switching to Gemini Flash" — Kevin
- "Tons of data of cars driving perfectly fine on a sunny day is completely useless" — Vivoth
- "What I want to see is a car carrying three other cars on a tow truck" — Vivoth
- "If it doesn't work, it's just not interesting" — Dexter
- "Hopefully we build AI that works" — Kevin
- "It seems like some of the restaurants randomly have different taxes that they apply" — Kevin
- "The more you look at these, the more challenges you find" — Kevin
- "JSON was meant for humans. If we cared about machines we'd use protobuf" — Vivoth
- "You don't really buy front end. You can buy someone to build your front end" — Vivoth
- "Anyone selling you a metric is scamming you because the metric is so domain specific" — Vivoth
- "The writing of the code was never the hard part" — Vivoth
- "If you can only ship your product when it's perfect, you will lose the battle" — Vivoth
- "The very first thing I did was looked at my data" — Kevin
- "There's no real magic way around it. You have to understand the problem" — Kevin
- "I tried Gemini 3 last night and got a ton of extraction failures" — Kevin
- "Subtotal versus grand total. I wanted the LLM to be really clear on the distinction" — Kevin
- "If I only have to do that one in 20 receipts, you're still saving me a ton of time" — Dexter
- "Gemini Flash seems to be the best at OCR, notably better than Sonnet or 4o" — Kevin

### HABITS
- Look at raw data manually before writing any abstraction or pipeline code on top
- Brainstorm runtime evals with cursor or sonnet before committing to implementation choices
- Start with cheap familiar models like GPT-4o for baseline before investing in optimization
- Always add floating-point tolerance to any numerical eval to avoid spurious failures
- Write extracted JSON to disk after every pipeline step for human inspection and resumption
- Keep extraction pipeline and eval pipeline separate sharing only the structured data contract
- Add exponential retry on flaky multimodal extraction calls before debugging the underlying model
- Iterate prompt and data schema together rather than fixing prompt against rigid schema
- Build dashboards that visualize eval results so failures jump out without manual reading
- Reuse architectural patterns from prior pipelines to compound design investment over projects
- Compare same image across multiple models and runs by encoding metadata into result JSON
- Spot-check failures by clicking through dashboard rather than reading raw JSON output dumps
- Treat eval failures as candidate seeds for building golden datasets rather than ignoring them
- Ship imperfect AI behind UI that flags low-confidence cases for human review and correction
- Feed eval failures back into the model as self-correcting context before escalating to human

### FACTS
- Indonesian receipts use commas where American receipts use decimals for currency formatting
- The CORD dataset on Hugging Face contains Indonesian receipt images with metadata fields included
- PB1 is an Indonesian restaurant tax that appears on some receipts but not others
- Gas stations historically priced fuel in fractions of a penny on signage and pumps
- Gemini 2.5 Flash outperformed both GPT-4o and Sonnet on this receipt OCR extraction task
- Kevin's full eval system with dashboard took roughly three to four hours to build
- Final eval run covered 350 receipts after starting with 21 baseline samples earlier
- BAML separates prompt definitions, structured output classes, and runtime calls into one file
- Streamlit can render dashboards by reading JSON files written by separate pipeline processes
- Parquet and Lance DB are columnar formats well-suited to multimodal dataset storage at scale
- Vercel ships preview URLs per pull request, a pattern Sprout previously built internally
- Evolution IQ builds AI claims guidance software for insurance companies handling medical documents
- The 12 Factor Agents framework emerged from interviewing enterprise AI shipping practitioners
- Receipts at CVS can reach roughly 30 feet long, far exceeding LLM expected image dimensions
- Hugging Face datasets often include metadata that requires significant integration effort to use

### REFERENCES
- BAML by BoundaryML for structured output extraction
- CORD receipt dataset on Hugging Face
- Gemini 2.5 Flash, Gemini 3, GPT-4o, Claude Sonnet
- Cursor IDE for brainstorming
- Streamlit for dashboards
- Evolution IQ insurance claims guidance product
- 12 Factor Agents framework
- Excalidraw for diagramming
- Brian's decaying resolution memory system from prior episode
- Vercel preview deployment pattern
- DSPy and Jeppa prompt optimization frameworks
- MongoDB, S3, Parquet, Lance DB for data storage
- Brex and Concur as receipt management product examples
- Tail scale URL sharing for internal tools
- Sprout's internal preview environment platform

### ONE-SENTENCE TAKEAWAY
Design invariant runtime evals from your data shape, then iterate prompt and schema together quickly.

### RECOMMENDATIONS
- Look at raw multimodal data manually before designing any pipeline architecture or abstractions
- Define structured outputs in BAML and brainstorm runtime evals with an LLM partner first
- Use mathematical invariants like sum equals subtotal as eval signal without golden datasets
- Add floating-point tolerance to every numerical eval to prevent spurious comparison failures
- Separate extraction pipeline from eval pipeline sharing only the typed data contract between them
- Write JSON results to disk after every pipeline step for human inspection and resumption
- Build a Streamlit dashboard that reads result JSON so failures jump out visually quickly
- Start cheap with GPT-4o baseline before testing Gemini Flash or Claude Sonnet on multimodal tasks
- Iterate prompt and schema together because new fields often emerge from observing extraction failures
- Add exponential retry to multimodal calls before assuming the underlying model is broken
- Ship at 95% accuracy with UI flagging low-confidence cases rather than chasing perfect prompts
- Build self-correcting loops that feed eval failures back as prompt context for retry
- Avoid hard-coding assumptions like absolute values that break correctly cancelling negative line items
- Reuse architectural patterns across pipelines because data-shape investment compounds project over project
- Skip prompt optimizers until your eval definitions are trustworthy and free of false positives
- Treat eval failures as candidate seeds for golden datasets rather than ignoring or hand-labeling everything
- Encode model name and run metadata into result JSON for cross-model and cross-run comparison
- Buy eval harnesses and preview infrastructure but never buy domain-specific metrics from vendors
- Use Parquet or Lance DB once result volumes outgrow plain JSON files on local disk
- Compare model outputs side by side in the dashboard to spot improvements without rerunning everything
