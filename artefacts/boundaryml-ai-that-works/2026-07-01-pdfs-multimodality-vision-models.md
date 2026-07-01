---
title: "PDFs, Multimodality, Vision Models: Part 1 #15"
videoId: sqJrl09dDmI
url: https://www.youtube.com/watch?v=sqJrl09dDmI
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1: Multimodality never changes the architecture, it is still just tokens, so an image is a grid of tokens whose resolution, cropping, and aspect ratio silently decide your accuracy.**
Once you see that the provider quietly turns your PDF into images plus OCR text and resizes it for you, you realize you should own that image pipeline yourself.
VERDICT: net-new video available.

**Spine 2: Wrap the probabilistic extraction in deterministic runtime evals (does the summary equal the sum of transactions?), then self-heal the failing page in a loop.**
This is how you get from a naive 80% extraction to a "110% guarantee": break the problem down, cross-check with plain math, and re-send only what broke.
VERDICT: next-step video available (complements a filmed technique).

**Spine 3: A per-step accuracy that looks fine compounds catastrophically, a 97% step across 20 steps behaves like a 50% pipeline.**
This is the non-intuitive reason agents "feel like they don't work," and it is the motivation behind every verification technique.
VERDICT: net-new video available (latent, source treats it briefly).

## Summary

Vaibhav and Dexter of AI That Works go under the hood on multimodality, showing how to extract bank transactions from PDFs using vision models reliably.

Counts: 🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1: An image is a grid of tokens, and you should own the pixels.**
The claim: multimodality does not change the LLM architecture, "in the end all we have is tokens," so an image is chopped into a grid where each cell becomes a token. What most people miss is that this is happening at all: when you hand a PDF to the OpenAI or Anthropic API, the provider silently converts each page to images plus OCR text and resizes it to a trained aspect ratio. The mechanism matters because tokenization forces a tradeoff. Text straddling a grid boundary generalizes worse; dense text crammed into one cell compresses away detail. So resolution is task-dependent: a Where's-Waldo detail task wants many tiny upscaled tiles, while summarization tolerates one compressed image. This generalizes cleanly to any document pipeline, invoices, medical scans, ID cards, where the "standard API" quietly crops non-standard shapes. Where it goes wrong: if you assume the provider handles resizing well, a long or skewed page gets cropped and you never see it. The fix is to do the resizing and cropping yourself for determinism.

**Spine 2: Deterministic checks around a probabilistic core.**
The claim: to trust an image pipeline you back its outputs with verification, aiming for a "110% guarantee." The non-obvious part is that the guarantee comes from deterministic code, not a better prompt. The mechanism is a chain: first break the task into extract-then-answer so each stage is testable; then run a runtime eval that is just basic math, does the extracted summary equal the sum of extracted transactions; if not, locate the failing page, re-send only that page, and loop until the constraint holds. Because LLMs "are pretty good at generally answering the question," focusing their attention on the two numbers that matter fixes most errors. This generalizes to legal-clause extraction and medical records, where you validate against a database instead of a sum. The failure mode is subtle: the answer stage can hit 90% while extraction sits at 70%, so the whole thing "feels worse" than either number, which is why you decompose and measure separately. The final move is honest coverage: sacrifice recall so that everything you do return is 100% correct, escalating the rest to a human.

**Spine 3: Accuracy compounds against you.**
The claim: a per-step success rate that sounds acceptable collapses over a multi-step pipeline, "when you have a pipeline that's 97% accurate and you have 20 steps, it behaves like a pipeline that's 50% accurate." Non-obvious because people reason linearly: 97% feels like an A, so a 20-step agent feels like it should mostly work. The mechanism is multiplicative, 0.97^20 is roughly 0.5, and a mere 2% per-step improvement becomes a 27% swing by step twenty. That is the causal root of "this is why agents feel like they don't work," since agents are inherently multi-step. It generalizes far past extraction, to any chained workflow: RAG stacks, tool-calling agents, ETL. Where the naive version goes wrong is treating the fix as "use a smarter model everywhere," when the leverage is reducing the number of independent steps and adding deterministic gates that reset accuracy to 100% at checkpoints. The source treats this in a two-minute aside (Dexter: "this should really be the 12 factor agents presentation"), so a full video needs extra sourcing, but the graphic alone carries a video.

## 🎬 Proposed ACS videos

### 1. How vision models actually see (it is all tokens, and you should own the pixels)

- HOOK: Your model is not "reading" your PDF, it is chopping it into a grid of tokens and cropping it behind your back.
- THE PROMISE: For engineers building any document or image pipeline, walk away able to control resolution, tiling, and cropping yourself instead of trusting the provider's defaults.
- THE SHAPE:
  1. Show the naive path: toss a PDF at the API, get 48 of 54 transactions back, one dropped at a page boundary.
  2. Whiteboard the grid, one cell becomes one token; show boundary text and the compression tradeoff.
  3. Where's Waldo demo: one image fails, many upscaled tiles succeed.
  4. Read the provider docs on aspect ratios; show what silent resize costs you.
  5. Land on the rule: if the provider will resize anyway, resize it yourself.
- SPINE: Spine 1.
- SLOT: Techniques class, new "Working with vision and multimodal models" chapter (adjacent to the shipped Context Engineering class).
- RELATIONSHIP: ❌ net-new. Nothing in the catalog covers image tokenization, resolution, or building a vision pipeline; Claude Chat "09 Files and Documents" is about uploading files in the chat UI, not engineering an extraction pipeline.
- PROOF TO REUSE: "in the end all we have is tokens"; the 48-of-54 dropped-transaction demo; "There's no better OCR system than a multi-modal LM"; the OpenAI PDF docs that reveal pages-as-images-plus-OCR.

### 2. The 110% guarantee: deterministic runtime evals that self-heal your pipeline

- HOOK: LLMs are great at answering questions and terrible at answering all of them correctly, so stop trusting the output and start checking it with math.
- THE PROMISE: For anyone shipping an extraction pipeline, learn to wrap a probabilistic model in deterministic checks that catch and repair its own mistakes.
- THE SHAPE:
  1. Break the task into extract-then-answer so each stage is independently testable.
  2. Add a runtime eval: does the summary equal the sum of transactions?
  3. On failure, find the broken page, re-send only it, loop until constraints hold.
  4. Add intermediate per-transaction balance checks to focus attention on two tokens.
  5. Ship honest coverage: escalate the unfixable to a human so returned data is 100% correct.
- SPINE: Spine 2.
- SLOT: Techniques class (verification/loops cluster, alongside "closing-the-loop").
- RELATIONSHIP: 🔗 complements "closing-the-loop" by being its next step. That video teaches giving the agent a feedback signal so it can iterate; this adds the specific move of making the signal a deterministic invariant (sum equals summary), locating the failing unit, and defining coverage-versus-correctness with a human fallback.
- PROOF TO REUSE: "it might not have 100% coverage on the data, but ... it will be 100% correct"; the live sum-check eval; the "focus all of its attention ... only on the two [tokens] that really, really matter" repair step.

### 3. Why your agent silently fails: the compounding-accuracy trap

- HOOK: A 97% accurate step feels like an A, but run it twenty times and you are shipping a coin flip.
- THE PROMISE: For anyone building multi-step agents, get the mental model (and the graphic) for why chains degrade and where to put deterministic gates.
- THE SHAPE:
  1. Present the graph: 99%^20 behaves like 80%, 97%^20 like 50%.
  2. Show why it is non-intuitive: humans reason linearly, accuracy multiplies.
  3. Tie it to real agents: multiple steps, so "it's not working."
  4. Prescribe the fix: cut steps, and add checkpoints that reset accuracy to 100%.
- SPINE: Spine 3 (latent, needs extra sourcing beyond this clip).
- SLOT: Context Engineering or Techniques, as a foundational reliability concept.
- RELATIONSHIP: ❌ net-new. "the-shifting-bottleneck" is about where the constraint sits, not accuracy compounding; "test-time-compute" is about spending tokens for quality. No video teaches the multiplicative reliability math.
- PROOF TO REUSE: "when you have a pipeline that's 97% accurate and you have 20 steps, it behaves like a pipeline that's 50% accurate"; "a 2% difference ... is a 27% difference at a 20-step mark"; "this should really be the 12 factor agents presentation."

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav and Dexter of AI That Works go under the hood on multimodality, showing how to extract bank transactions from PDFs using vision models reliably.

### IDEAS
- Models don't understand PDFs directly; providers silently convert each raw page into images plus OCR text.
- Multimodality never changes the architecture; in the end everything an LLM processes is still just tokens.
- An image gets broken into a grid where each cell becomes a token of some kind.
- Text straddling grid-cell boundaries performs worse because the model struggles to generalize across the split cells.
- Cramming dense text into one cell compresses tokens, boosting summarization but destroying fine detail-oriented extraction accuracy.
- For Where's-Waldo-style detail tasks, splitting an image into many tiny upscaled tiles beats one big image.
- Providers hide their image tokenizers; only some open-source models reveal exactly how image tokenization actually works.
- Because image tokenization is hidden, vision-model costs are always rough estimates, never exactly predictable up front.
- Anthropic's docs list maximum image aspect ratios; violating them forces silent cropping or resizing hurting accuracy.
- If the provider will resize your image anyway, resize it yourself to keep control and determinism.
- Detecting headers and footers is a non-LLM problem: diff a page against an anchor with OpenCV.
- Overlaying pages and zeroing identical pixels reveals shared headers and footers as matching horizontal pixel bands.
- To join transactions split across pages, crop the previous page's bottom 25% and stitch it forward.
- Extracting structured fields like page_type reveals what the model actually sees inside an otherwise opaque image.
- A runtime eval checking whether the summary equals the sum of transactions catches extraction errors deterministically.
- When validation fails, locate the broken page, re-send only that page, and loop until constraints hold.
- Models answer better with yes/no enums than raw booleans, since true/false alone confuses them surprisingly often.

### INSIGHTS
- Use the biggest model first to get running, then optimize down once cost or performance bites.
- Trusting an AI image pipeline requires backing its outputs with deterministic verification for a 110% guarantee.
- Breaking a hard extraction into extract-then-answer lets you test, optimize, and locate failure in each stage.
- Resolution choice is task-dependent: detail tasks want tiled high-res, summarization tolerates compression, match resolution to intent.
- A pipeline can sacrifice coverage for correctness: guarantee 100% accuracy on the data it does handle.
- Every episode secretly concerns context engineering: deliberately choosing which tokens the model sees, even for images.
- LLMs answer questions well given correct data; the hard part is getting the right data in.
- Understanding a system's constraints tells you when the standard API will quietly hurt your real-world performance.
- Constraints for verification aren't always direct; being creative, combining two signals, is often the real answer.

### QUOTES
- "There's no better OCR system than a multi-modal LM." (Vaibhav)
- "the way that you convert a page into an image can vary a lot with PDFs." (Vaibhav)
- "in the end all we have is tokens." (Vaibhav)
- "no one actually knows the answer to this, so everyone is speculating at best." (Vaibhav)
- "when you have a pipeline that's 97% accurate and you have 20 steps, it behaves like a pipeline that's 50% accurate." (Vaibhav)
- "this is why agents feel like they don't work because agents typically have multiple steps and people are like, 'What the heck? It's not working.'" (Vaibhav)
- "this should really be the 12 factor agents presentation." (Dexter)
- "extracting the data is a really like clean way to like look inside what the LM is seeing." (Vaibhav)
- "detecting headers is a non-LLM problem." (Vaibhav)
- "it might not have 100% coverage on the data, but on for all the data it has coverage on, it will be 100% correct." (Vaibhav)
- "You all thought you were going to get a break from context engineering, but it turns out every episode of this show is actually about context engineering." (Vaibhav)
- "use the fastest thing first, not in terms of speed, but the thing that gets you up and running first." (Vaibhav)
- "It turned out that was dumb and the better thing to have done would have been to just collect more data and try to build a bigger model." (Vaibhav)

### HABITS
- They always reach for the biggest model first, then scale down after hitting cost or performance.
- He iterates prompts live, trying roughly twelve variations before landing on page_type plus transaction-count validation together.
- He counts the expected items manually first, so any mismatch immediately exposes a dropped extraction quickly.
- He prefers asking a simple LLM call over writing a clever algorithm whenever accuracy roughly suffices.
- He always records exactly where a pipeline failed, giving engineers clear audit logs into failure points.
- He answers enums with yes/no rather than booleans because models dislike replying with plain true/false values.
- He constrains inputs deliberately, assuming standardized bank PDFs rather than handling every tilted phone-photo edge case.
- He generates the boring image-diff utility code with ChatGPT rather than hand-writing OpenCV boilerplate code himself.

### FACTS
- OpenAI's documentation states it processes PDFs by converting pages to images and adding OCR text separately.
- A 97%-accurate step across twenty pipeline steps compounds down to roughly 50% overall end pipeline accuracy.
- A mere 2% accuracy difference per step becomes a 27% difference by the twentieth pipeline step.
- In OpenAI's tokenizer 'strawberry' is now one token, though it used to be split into multiple.
- The naive PDF extraction returned only 48 of 54 transactions, dropping ones spanning the page boundaries.
- GPT-4o mini often refuses to parse ID cards like passports, assuming possible misuse of the document.
- Claude's image cost math divided by 750, suggesting roughly 750-pixel regions map to each image token.
- The Python Pillow library's ImageChops.difference computes pixel-by-pixel diffs used here to detect headers and footers cheaply.

### REFERENCES
- AI That Works podcast (weekly show), hosted by Vaibhav and co-host Dexter.
- Vaibhav's background working on Apple Face ID and geometric/deterministic computer vision.
- OpenAI PDF documentation (describes pages-as-images-plus-OCR processing).
- Anthropic image documentation (maximum image aspect ratios).
- OpenAI tokenizer tool (shows text tokens; multimodal tokenizers are hidden).
- Gemini (PDF parser and bounding-box detection training).
- ChatGPT image generation (cited as a full-stack multimodal experience) and used to generate utility code.
- Models named: GPT-4o, GPT-4o mini, O3, Opus, Haiku.
- Libraries: OpenCV, Python Pillow (PIL) ImageChops.difference, NumPy.
- BAML (BoundaryML) referenced in the live coding ("import b", "b.extract").
- "12 factor agents" (the compounding-accuracy graphic).
- Where's Waldo (detail-extraction example).
- Prior episode #5, where they covered the eval loop in detail.

### ONE-SENTENCE TAKEAWAY
Wrap probabilistic vision extraction in deterministic checks and control your image pipeline to reach reliability.

### RECOMMENDATIONS
- Read your provider's PDF and image documentation to learn the exact conversion, resolution, and aspect-ratio rules.
- Do your own image resizing and cropping instead of letting the model provider handle it silently.
- Add a runtime eval asserting your extracted summary equals the computed sum of extracted line items.
- When a validation fails, isolate the offending page and re-send only it back for targeted correction.
- Break hard extraction problems into extract-then-answer so each stage can be tested and optimized fully independently.
- For detail-heavy extraction, split images into smaller high-resolution tiles rather than one downscaled full page image.
- Strip repeated headers and footers using a cheap pixel diff, not an expensive LLM call ever.
- Debug opaque vision failures by extracting structured fields to reveal what the model actually perceives inside.
- Stitch page-spanning records by appending the previous page's bottom crop to the current page's image directly.
