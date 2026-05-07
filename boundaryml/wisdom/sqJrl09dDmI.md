---
video_id: sqJrl09dDmI
title: "🦄 ai that works: PDFs, Multimodality, Vision Models: Part 1"
url: https://www.youtube.com/watch?v=sqJrl09dDmI
channel: BoundaryML
---

### SUMMARY

Vibhav and Dexter from BoundaryML explore PDF parsing, multimodality, and vision models, demonstrating bank transaction extraction techniques using image preprocessing and runtime evaluation loops.

### IDEAS

- Multimodal LLMs are currently the absolute state-of-the-art systems for OCR text extraction tasks today.
- Models work best when fed standard data; pre-processing manually before training was historically a wasted effort.
- Trust AI pipelines using images completely once verification through deterministic backed data validation is established.
- PDFs internally are often XML metadata, but sometimes purely scanned images saved inside PDF containers.
- OpenAI converts PDFs into page images plus OCR text rather than training models specifically on PDFs.
- Anthropic likely crops or resizes oddly-shaped images, hurting performance when aspect ratios deviate from recommendations.
- Image tokenization remains opaque because vocabulary generalization is much harder than text token vocabulary creation.
- Tokenizers grid-split images so content crossing cell boundaries performs worse than content fitting cleanly inside.
- Detail-oriented tasks benefit from breaking images into smaller high-resolution pieces rather than single compressed inputs.
- Where's Waldo problems mirror counting Rs in strawberry, both being detail tasks LLMs handle poorly.
- Breaking hard problems into two prompts works, but compounded error rates make pipeline accuracy fall fast.
- Two percent accuracy difference per step becomes twenty-seven percent difference at twenty pipeline steps total.
- Runtime evaluations validating sums against extracted transactions catch hallucinations before bad data reaches users.
- Strawberry was once tokenized as multiple tokens until vocabulary updates merged it into single token.
- Convert PDFs to pages, then process each page individually for cleaner control over extraction performance.
- Use cheap mini models for simple boolean classification tasks like detecting transaction-containing pages.
- Models hate answering pure boolean true-false questions and perform better with yes-no string responses.
- Detect headers and footers cheaply by diffing pages pixel-by-pixel using OpenCV image difference operations.
- Headers semantically span entire horizontal rows, allowing y-coordinate band detection for clean masking.
- Page boundary transactions split between pages require stitching cropped previous page bottoms with current pages.
- Ask LLMs which header candidate fits best rather than writing complex algorithmic frequency analysis code yourself.
- Solve problems with whichever tool gets eighty percent right first; only escalate when accuracy proves insufficient.
- Detail-oriented extraction benefits from splitting images into upscaled smaller images for better token attention.
- Multimodal API providers chunk and resize images automatically, hurting performance for non-standard input shapes.
- Don't use LLMs to generate UUIDs, database IDs, URL encodings, or other deterministic computational tasks.
- Bank statements often include before-and-after balances per transaction, providing intermediate validation checkpoints automatically.
- Human-in-the-loop fallbacks let pipelines handle uncertain cases by surfacing failures rather than silently miscomputing.
- Extracting both transactions and summary balance separately enables runtime cross-validation through arithmetic equality.
- Aspect ratio mismatches force model providers to crop or resize, degrading downstream extraction performance silently.
- LLMs answer questions well when given correct data; getting correct context is the hardest engineering problem.
- Image differencing zeros identical pixels between pages, exposing variable content while masking common header chrome.

### INSIGHTS

- The right tool for each job matters; LLMs solve some problems but cause unnecessary unreliability elsewhere.
- Verification through deterministic cross-checking transforms probabilistic AI outputs into reliable production-grade systems with confidence.
- Pipeline accuracy compounds multiplicatively, making seemingly small per-step errors catastrophic across long agentic workflows.
- Context engineering is fundamentally about deliberately controlling which exact tokens reach the model's attention layer.
- Standardization assumptions break silently; non-standard inputs receive automatic preprocessing that degrades quality invisibly.
- Breaking hard problems into multiple validated subproblems beats trying to solve everything in one prompt.
- Image tokenization tradeoffs mirror text memory architectures, balancing summarization capability against detail preservation precisely.
- The best engineers iterate quickly through prompt variations rather than overthinking initial architectural decisions upfront.
- Asking models for structured discriminative output works better than asking for raw boolean classification answers.
- Combining algorithmic preprocessing with LLM reasoning produces better results than either approach used alone.
- Knowing what providers do under the hood lets you replicate or surpass their default behavior intentionally.
- Human-in-the-loop systems should surface failures gracefully rather than masking uncertainty behind confident-sounding hallucinated answers.
- Cross-validation between independent extractions using deterministic rules catches errors single-pass approaches cannot detect.
- Deterministic fallback rules give complete confidence on covered cases even when full coverage remains impossible.
- Real-world data is weird, so building audit trails matters more than chasing theoretical accuracy benchmarks.

### QUOTES

- "There's no better OCR system than a multimodal LLM. Those are state-of-the-art." — Vibhav
- "Math is correct because math I can see, I can understand these multiplications." — Vibhav
- "It turned out that was dumb and the better thing was to just collect more data." — Vibhav
- "When you're using AI, that's what you need. You need that 110% guarantee." — Vibhav
- "Models are in my opinion in front when it comes to OCR." — Vibhav
- "The LM architecture doesn't fundamentally change when you toss multimodality into it." — Vibhav
- "It's all about attention management. Context engineering. You're just controlling which tokens go in." — Dexter
- "I'm literally deliberately choosing what tokens go in by effectively spellchecking my images." — Vibhav
- "Don't get a credit card with interest rates. Or don't pay interest on your credit card." — Vibhav
- "Use the fastest thing first. Not in terms of speed but the thing that gets you running." — Vibhav
- "If you have a 99% accurate pipeline with 20 steps, it behaves like 80% accurate." — Vibhav
- "All tokenization means is the most simplistic version where you break it down to a grid." — Vibhav
- "LMs are pretty good at generally answering the question that you want." — Vibhav
- "The hard part is getting the right data in there. That's all context engineering is." — Vibhav
- "You all thought you were going to get a break from context engineering." — Dexter
- "Models perform based on training data; if 95% is this resolution, it'll work better." — Dexter
- "It's just like probabilities, right? It's the same thing. Probabilities matter." — Vibhav
- "This is basically like a leetcode problem in the world of AI." — Vibhav
- "Detecting headers is a non-LM problem. It's the thing I was talking about." — Vibhav
- "I came from a background where I think of, I used to hate machine learning." — Vibhav

### HABITS

- Start with the largest, most capable model first then optimize for cost afterward.
- Try the simplest dump-it-into-the-API approach before building custom preprocessing pipelines for production.
- Read the actual provider documentation to understand image aspect ratios and PDF handling specifics.
- Iterate prompts live, trying ten or twelve variations before declaring a technique broken.
- Count expected outputs manually before running extraction to validate model accuracy against ground truth.
- Build runtime evaluation loops that verify mathematical relationships between independently extracted data fields.
- Use cheap mini models for simple binary classification tasks rather than expensive frontier models.
- Crop image data deliberately to focus model attention on relevant tokens before extraction.
- Prefer yes-no string outputs over true-false booleans when designing classifier prompts for LLMs.
- Stitch overlapping page bottoms with following pages to handle boundary-spanning data cleanly.
- Use OpenCV ImageChops difference for pixel-level page comparison instead of writing custom code.
- Ask the LLM to choose between options rather than writing frequency-counting algorithms yourself manually.
- Build human-in-the-loop fallbacks for cases where automated validation cannot establish sufficient confidence.
- Track exact failure points in audit logs so engineers can debug systemic extraction problems later.
- Validate extracted data against external databases when working with medical or financial transaction systems.

### FACTS

- OpenAI converts PDFs to images plus OCR text before passing them through multimodal model APIs.
- Anthropic publishes maximum image aspect ratios in their documentation that affect model preprocessing behavior significantly.
- Multimodal model providers do not expose their image tokenizers publicly unlike text tokenizer transparency.
- Claude pricing math suggests image regions tokenize at approximately 750 pixels per token unit.
- Strawberry is now a single token in modern tokenizers but used to require multiple tokens.
- A 99% accurate pipeline run twenty times in sequence behaves like an 80% accurate single-step pipeline.
- A 97% accurate pipeline run twenty times in sequence behaves like a 50% accurate single pipeline.
- Two percentage points of per-step accuracy difference creates 27 percentage points difference across twenty steps.
- GPT-4 mini frequently refuses to extract data from passport or identification card document images.
- Bank transaction PDFs are often longer than standard A4 paper, breaking common API preprocessing assumptions.
- Python's PIL library includes ImageChops difference function used commonly for pixel-level image comparison tasks.
- Apple's Face ID engineering originally used geometric math approaches before transitioning toward larger neural network training.
- The naming convention strawberry-without-leading-space tokenizes differently than strawberry-with-leading-space in OpenAI tokenizer outputs.
- Bank statements typically include before-and-after balance fields per transaction enabling automated arithmetic validation per row.
- LLMs hallucinate transaction values like converting 234 to 311 with no apparent provenance from source.

### REFERENCES

- BoundaryML BAML library for structured LLM output extraction
- OpenAI tokenizer web tool for visualizing text token boundaries
- OpenAI PDF documentation describing page-image plus OCR conversion pipeline
- Anthropic image documentation specifying maximum aspect ratios
- Gemini PDF parser and ChatGPT image generation full-stack experiences
- OpenCV computer vision library
- Python Imaging Library PIL ImageChops difference function
- NumPy array library for pixel band detection
- Apple Face ID geometric preprocessing pipelines
- Where's Waldo image search puzzle as multimodal benchmark
- AI That Works episode five covering evaluation loops in depth
- 12 Factor Agents presentation on accuracy compounding
- Gemini bounding box detection capabilities
- GPT-4o, GPT-4o mini, o3, Claude Opus, Claude Haiku frontier models

### ONE-SENTENCE TAKEAWAY

Combine deterministic preprocessing with focused LLM extraction and runtime validation loops for reliable production-grade multimodal pipelines.

### RECOMMENDATIONS

- Start with the dumbest possible API call before building custom multimodal image preprocessing pipelines yourself.
- Read provider PDF and image documentation to learn what preprocessing happens automatically before model inference.
- Convert PDFs to individual page images yourself for explicit control over resolution and cropping behavior.
- Use cheap mini models for simple page classification tasks before invoking expensive frontier reasoning models.
- Build runtime evaluation loops that cross-check extracted summaries against the sum of extracted transaction lists.
- Detect page headers and footers using pixel-level diff operations between adjacent pages cheaply with OpenCV.
- Mask out common header and footer regions before extracting transaction data to reduce attention noise.
- Stitch overlapping bottom-page crops with following pages when transactions span across PDF page boundaries.
- Replace boolean true-false outputs with yes-no string fields for more reliable classification prompt responses.
- Add structured discriminative outputs like page-type enumerations to improve weak model classification reliability significantly.
- Break complex single prompts into multiple validated steps when accuracy compounds problematically across pipeline steps.
- Surface failure cases to humans through UI affordances rather than masking uncertainty behind hallucinated outputs.
- Skip LLMs entirely for deterministic computational tasks like UUID generation, URL encoding, or database identifier creation.
- Validate extracted data against authoritative external databases when handling regulated financial or medical document workflows.
- Track exact transaction counts manually before extraction to establish ground truth for evaluating model accuracy.
- Use intermediate per-row validations like before-and-after balance checks to catch single-row hallucinations early.
- Crop irrelevant image regions before extraction to maximize model attention on important target token regions.
- Ask the LLM to pick between candidate options rather than writing complex frequency-counting algorithms yourself.
- Build audit trails with exact failure point recording so engineering teams can debug systemic issues later.
- Iterate prompts live through ten or more variations before declaring a multimodal technique fundamentally broken.
