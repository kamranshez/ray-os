---
title: "Cracking the prompting interview #9"
videoId: PU2h0V-pANQ
url: https://www.youtube.com/watch?v=PU2h0V-pANQ
date: 2026-07-01
status: posted
source: BoundaryML "AI That Works" (Vaibhav "Vib" + Dexter)
---

## The one idea worth a video

**1. Never make the model generate long, meaningless token sequences. Emit the shortest semantically meaningful pointer (an index or a symbol) and reconstruct the real value in deterministic code.** This one reframe subsumes the citation, diarization, and symbol-tuning tricks: each is the same move applied to a different string.
VERDICT: 🔗 next-step video available (complements the scripted Structured Output brief).

**2. Forcing the model into valid JSON at decode time degrades quality. Let it write in its natural format (markdown code fences) and parse the structure outside the model.** Strict decoding masks the model's single best token (the raw newline), collapsing it onto a degenerate distribution of janky code.
VERDICT: 🔗 next-step video available (the correction to the Structured Output brief).

**3. RTFP: when a structured-prompt framework compiles your schema into a hidden prompt, read that rendered prompt.** Debugging what the model actually sees beats blind re-prompting, and it is the fastest iteration loop the presenter uses on stage.
VERDICT: 🔗 next-step video available (complements Iterative Refinement).

## Summary

BoundaryML's Vaibhav and Dexter run a live prompting clinic, showing tokenizer-grounded tricks: emit indexes not strings, parse outside the model, and read your rendered prompt.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: Emit the shortest pointer, rebuild in code

**The claim.** Do not ask the model to regenerate a long, meaning-free string (a URL, a UID, a full transcript line). Have it emit the smallest semantically meaningful token, an array index or a symbol, and let deterministic code map that back to the real value.

**Why it is non-obvious.** The intuitive design is "ask for citations, get citations back." But the presenter opens the tokenizer and shows a single YouTube URL fragmenting into roughly ten tokens: "in order for the model to get this part of the URL correct specifically, it has to generate 10 tokens perfectly." Every extra verbatim token is another independent chance to break the link.

**Why it is true.** Because a random string carries no meaning, the model has no semantic hook to predict it, so accuracy falls off multiplicatively with token count; because an index like `0` or a symbol like `K1` is one confident token, the model reliably emits it; therefore moving the URL into a code-side lookup removes the failure entirely. "There's no meaning baked into that random string of characters. It's just a pointer."

**What it generalizes to.** Diarization: output a dialogue index plus speaker rather than reprinting the transcript, an order-of-magnitude fewer output tokens. Classification: symbol tuning puts "zero attention on the label name, all attention on the description."

**How it goes wrong.** You must own the remap layer, and you cannot use it when the text itself is the deliverable (the video-editing example), where a span-of-indexes trick is the fallback.

### Spine 2: Do not constrain decoding; parse outside the model

**The claim.** Structured extraction should happen in a parser that sits outside the model, not by forcing the model to emit valid JSON at generation time. Let it write code the way it was trained to (inside markdown backticks) and convert to valid JSON afterward.

**Why it is non-obvious.** "Just give me clean JSON" feels safer, and strict/function-calling modes are marketed as reliability features. The scripted ACS Structured Output brief even lists markdown fences as a failure to suppress. This video argues the opposite.

**Why it is true.** At each step the model has a distribution over next tokens; for code the overwhelmingly best token is a raw newline. Strict JSON mode "X's out" that newline because literal newlines are invalid JSON, so probability redistributes across a flat tail of semicolons and odd characters, and "you're likely to get weird janky code." Because the model was trained to write code between backticks (the dominant format in training data), keeping it in that format preserves quality; because a separate parser can turn real newlines back into escaped JSON, you lose nothing downstream.

**What it generalizes to.** Any domain: "anytime you're having the model not pick its best token, you're basically telling the model you know better than the model." Echoes the bitter lesson from computer vision.

**How it goes wrong.** You now need a tolerant parser (their BAML pitch); naive `json.loads` on backticked output fails.

### Spine 3: RTFP, read the rendered prompt

**The claim.** When you use a framework that compiles a schema and instructions into the actual prompt string, read that compiled prompt, especially when you are stuck, instead of blindly adding more instructions.

**Why it is non-obvious.** Structured-prompt tools hide the final prompt, so people iterate against an artifact they never see. "Most people don't actually read the prompt."

**Why it is true.** Because the model only ever responds to the rendered tokens, and because you cannot diagnose what you cannot see, reading the compiled prompt surfaces concrete confusions (the presenter spots nested comments confusing the model and simplifies them); therefore each edit becomes targeted rather than a guess. "It allows us to iterate a little bit faster."

**What it generalizes to.** Coding agents: giving the model line numbers dramatically improves edits, the same "let it read the exact thing" principle. Any templated system prompt with variable injection benefits from dumping and reading the final render.

**How it goes wrong.** You cannot always read it (the v0 example, where the tool's prompt is opaque), and reading without a hypothesis just burns time.

## 🎬 Proposed ACS videos

### 1. Stop Making the Model Type: Emit an Index, Rebuild in Code
- HOOK: A single YouTube URL is ten fragile tokens the model must nail perfectly, or your citation link is dead.
- THE PROMISE: For anyone building RAG, extraction, or classification pipelines, you will stop the model from ever regenerating meaningless strings.
- THE SHAPE: (1) Open the tokenizer, show the URL shattering into ten tokens. (2) Return a citation index instead of the URL, remap in Python. (3) Diarization: emit dialogue index plus speaker, not the transcript. (4) Symbol tuning: replace the label name with a symbol, push all meaning into the description. (5) The rule: shortest meaningful token out, deterministic rebuild in code.
- SPINE: 1
- SLOT: Prompt Engineering > Core Techniques (sits right after 07 Structured Output)
- RELATIONSHIP: 🔗 complements "07 Structured Output" by being its next step. That brief teaches schema-as-prompt and the enum trick (collapse the output to fixed options). This adds the tokenizer-grounded reason WHY, and extends it: make the emitted value the shortest pointer and reconstruct the real value in code, because every verbatim token is another chance to fail.
- PROOF TO REUSE: the tokenizer teardown of the YouTube URL ("10 tokens perfectly"); "There's no meaning baked into that random string of characters. It's just a pointer"; the diarization index trick being "an order of magnitude cheaper."

### 2. Why Strict JSON Makes Your Code Worse (and What to Do Instead)
- HOOK: The reliability feature everyone turns on, strict JSON mode, is quietly degrading your generated code.
- THE PROMISE: For engineers wiring LLMs into systems, you will understand samplers well enough to know when NOT to constrain the model.
- THE SHAPE: (1) Ask for code inside a JSON string, show the forest of forced backslash-n escapes. (2) Whiteboard the sampler: the best next token is a raw newline. (3) Show strict mode masking that token and the distribution collapsing to janky output. (4) Let the model write in backticks, parse to valid JSON outside the model. (5) Generalize: do not tell the model you know better than the model.
- SPINE: 2
- SLOT: Prompt Engineering > Core Techniques (a mechanism companion to 07 Structured Output)
- RELATIONSHIP: 🔗 complements "07 Structured Output" by being its next step and its correction. That brief teaches how to get clean JSON and lists markdown code fences as a failure to suppress. This video explains the decode-time mechanism the brief omits: constrained decoding removes the model's best token and degrades quality, so for code you should let the fences stand and parse externally.
- PROOF TO REUSE: "slash and n are two different tokens"; the strict-mode sampler explanation ("it's just going to X out anything that would break the JSON schema"); the Go/RDS example where the model spontaneously refused to emit escaped JSON on a hard problem.

### 3. RTFP: Read the Prompt Your Framework Actually Sends
- HOOK: You keep adding instructions and it keeps failing, because you have never once read the prompt the model actually receives.
- THE PROMISE: For anyone using a structured-prompt framework, you will trade blind prompt-poking for a fast, targeted debugging loop.
- THE SHAPE: (1) Show a schema plus instructions compiling into a hidden final prompt. (2) A prompt misbehaves; instead of re-prompting, dump and read the render. (3) Spot the concrete confusion (nested comments) a human reader catches instantly. (4) Fix that one thing, rerun. (5) Tie to coding agents: line numbers work for the same reason.
- SPINE: 3
- SLOT: Prompt Engineering > Core Techniques (pairs with 10 Iterative Refinement)
- RELATIONSHIP: 🔗 complements "10 Iterative Refinement" by being its missing first move. Iterative Refinement teaches the tweak-and-rerun loop on outputs; RTFP adds the step before every tweak, read the fully rendered prompt so the loop is targeted rather than a guess, which matters most in frameworks that hide the compiled prompt.
- PROOF TO REUSE: "RTFP means read the prompt... most people don't actually read the prompt"; the live moment where reading the prompt reveals nested comments confusing the model; the line-numbers-for-coding-agents analogy.

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's Vaibhav and Dexter run a live prompting clinic, showing tokenizer-grounded tricks: emit indexes not strings, parse outside the model, and read your rendered prompt.

### IDEAS
- URLs tokenize into ten fragile tokens, so the model must emit all ten perfectly or break.
- Instead of generating a citation URL, return an index into the input array, then remap deterministically.
- For diarization, output only a dialogue index and the speaker instead of reprinting each transcript line.
- Emitting indexes instead of full transcript text makes long diarization jobs an order of magnitude cheaper.
- Symbol tuning replaces label names like 'refund' with opaque symbols so descriptions carry all the meaning.
- Put zero attention on the label name and all attention on the description you actually control.
- Strict JSON mode X's out the model's best token, the raw newline, degrading generated code quality.
- Let the model write code between markdown backticks because that format dominates its training data distribution.
- A parser outside the model can accept natural newlines and convert them back into valid JSON.
- Give the classifier an 'other' escape hatch so it stops hallucinating a confident but wrong label.
- Inline comments in the schema, placed before a field, can steer the model's per-field reasoning cheaply.
- Never make the model count; give explicit line indexes, like line numbers help coding agents edit.
- Role prompting ('you are a senior engineer') has little effect; the model only needs the job.
- Few-shot examples steer by content, so use them to show structure without teaching specific answer content.
- Return a typed schema instead of a plan string, then drop entities failing your validation constraints.
- A runtime guard can bounce any output URL not present in the input set for retry.
- At half-a-percent gains, tiny prompt tweaks compound massively when you run a pipeline 100,000 times daily.

### INSIGHTS
- Prompting is software engineering: minimize what the model must generate, then reconstruct the rest with code.
- The tokenizer is the first place to check whether a model can reliably generate something correctly.
- Constraining decoding tells the model you know better than it does, usually a statistically losing bet.
- The bitter lesson recurs: stop clever pre- and post-processing and just let the model decide directly.
- Reading the rendered prompt beats blind re-prompting because you can finally see what confuses the model.
- Models prefer the safe 'other' answer because a human lacking context would also refuse to guess.
- Meaningless random strings are just pointers; the model has no semantic hook to generate them accurately.
- A schema field is an instruction; changing what you request reshapes what the model reasons about.

### QUOTES
- "There's no meaning baked into that random string of characters. It's just a pointer." (Vaibhav)
- "You really want to do your best to not rely on models generating long sequences of tokens that don't make sense for the model." (Vaibhav)
- "RTFP means read the prompt... most people don't actually read the prompt." (Vaibhav)
- "You want to say zero attention on the label name... all attention on the description so that I can control exactly what the LM is going to output." (Dexter)
- "This is the way models want to write code... let it write it between markdown back ticks because that is what is the majority present in the training set." (Vaibhav)
- "You're basically telling the model you know better than the model, which may be true in some scenarios. But most of the time in machine learning, what we've learned is let the model do what it does best." (Vaibhav)
- "Don't try and be clever with token generation, just let the model pick the best token." (Vaibhav)
- "The model doesn't care who it is. It just has to know the job it wants to do." (Vaibhav)
- "A tiny half a percent improvement either in efficiency or in speed or in token efficiency or in accuracy is massively valuable." (Dexter)
- "If you want stuff to be formatted in a good way, literally just run a linter on the generated code." (Vaibhav)
- "Why make the life harder for the model?" (Vaibhav)

### HABITS
- They always open the tokenizer to inspect how many tokens a target output string actually requires.
- They always read the fully rendered prompt when a result surprises them, before tweaking anything more.
- They generate throwaway test cases with Cursor to quickly probe how a new prompt behaves live.
- They run evals offline in a separate pipeline to avoid adding latency to production inference calls.
- They drop invalid entities via schema constraints rather than trusting the model to self-filter them perfectly.
- They inject known context, like calendar attendees, so the model stops guessing at ambiguous speaker identities.
- They share their own prompts publicly and invite harsh roasting as their fastest prompt-engineering learning loop.
- They prefer opinionated tooling like Go and Black that removes stylistic choices from the model entirely.

### FACTS
- In GPT tokenizers, 'YouTube' and 'watch' each encode as a single token; other URL parts fragment.
- JSON forbids literal newlines, so code strings must escape them as backslash-n to stay syntactically valid.
- Backslash and n are two separate tokens, so escaped newlines cost the model extra generation effort.
- Strict JSON mode and function-calling modes enforce schemas by masking tokens that violate the output structure.
- BoundaryML's 'AI That Works' series started in March, took a break, and runs roughly weekly online.
- Typical speaking pace runs roughly 120 words per minute; slower is 100, and faster near 150.
- Comments are technically invalid in strict JSON, yet models can be coaxed into emitting them anyway.
- SVG generation improves when models emit a structured object that deterministic code converts into the image.

### REFERENCES
- BAML / BoundaryML (structured-prompt framework and external parser)
- Cursor (test-case generation, cursor rules)
- OpenAI GPT-4o; Anthropic Claude Sonnet (20241022)
- v0 by Vercel (UI generation)
- Boundary Discord (prompt-sharing thread)
- Tokenizer visualization tool
- "12 Factor Agents" by Dexter; prior episode on MCP servers with 10,000+ tools
- The tldraw creator's SVG-via-structured-object talk at AI Engineer
- Luma (event listings); Sahil (referenced competitor to a content-pipeline idea)
- Symbol tuning (research technique); the bitter lesson (Rich Sutton)
- Go language; Black (Python formatter); ESLint / Biome; Redis cache

### ONE-SENTENCE TAKEAWAY
Make the model emit the smallest meaningful token, then reconstruct everything else with deterministic code.

### RECOMMENDATIONS
- Replace generated URLs and UIDs with array indexes, then remap to real values in your code.
- For long transcripts, have the model output only line indexes and speakers, not the full text.
- Add an 'other' escape category to every classifier so the model can safely decline uncertain guesses.
- Let the model write code in markdown backticks and parse it with an external parser afterward.
- Avoid strict JSON mode for code; it strips the model's preferred tokens and degrades output quality.
- Read your framework's fully rendered prompt whenever the output surprises you, instead of blindly prompting more.
- Enforce code style with linters and formatters instead of describing style rules inside your prompt text.
- Drop role framing; tell the model the job directly and describe each field's meaning precisely instead.
- Guide field reasoning with inline schema comments, or emit a phrases-only assessment field for evals cheaply.
