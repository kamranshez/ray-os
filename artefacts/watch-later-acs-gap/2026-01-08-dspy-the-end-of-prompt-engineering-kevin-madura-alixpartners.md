---
title: "DSPy: The End of Prompt Engineering - Kevin Madura, AlixPartners"
video_url: https://www.youtube.com/watch?v=-cKUW6n8hBU
video_id: -cKUW6n8hBU
channel: AI Engineer
published: 2026-01-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**DSPy: The End of Prompt Engineering - Kevin Madura, AlixPartners**](https://www.youtube.com/watch?v=-cKUW6n8hBU) - AI Engineer - uploaded 2026-01-08

> Two buildable ACS videos: one net-new (compile prompts instead of hand-writing them), one complement (optimize prompts with data, the quantitative sequel to "Getting Prompt Feedback").

## The one idea worth a video

**Spine 1 — Prompts are implementation details, not the deliverable: declare a typed input/output interface and let the framework generate the actual prompt string.** It subsumes signatures, shorthand vs class-based, field-names-as-mini-prompts, adapters, and the "survives model churn" pitch.
VERDICT: ❌ net-new video available.

**Spine 2 — A prompt optimizer tunes your prompt against a small dataset plus metric, surfacing "latent requirements" you never specified and recovering a cheap model's accuracy at a fraction of the cost.** It subsumes MIPRO/GEPA, metrics, teacher-model feedback, and the transferability/cost story.
VERDICT: 🔗 next-step video available.

## Summary + counts

Kevin Madura, a technical consultant at AlixPartners, explains why DSPy replaces brittle prompt engineering with declarative, typed, modular programs whose prompts the system optimizes automatically.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1 — Prompts as compiled artifacts.**
The claim: stop hand-crafting prompt strings; declare a typed input/output interface and let the framework produce the prompt. Why it is non-obvious: most engineers treat the prompt as the prized deliverable they craft and guard ("I have a really good prompt, I don't want this thing"). Madura argues the prompt is an implementation detail, closer to assembly you never write by hand. Why it is true: because intent is expressed as a typed signature whose field names double as mini-prompts ("part of the prompt itself"), an adapter translates that into the concrete string sent to the model, so swapping the adapter (JSON versus BAML) changes the wire format without touching your logic and can move accuracy five to ten percent; and because the string is generated rather than authored, the same control flow "bounces from model to model" as new releases land almost daily. It generalizes to writing CLAUDE.md and skill instructions: declare intent, let the layer compile the phrasing. How it goes wrong: a hard-won prompt still has a home (inject it in the docstring as a starting point), and for one-off tasks the abstraction overhead is not worth it.

**Spine 2 — Optimizers surface latent requirements.**
The claim: an optimizer automatically rewrites your prompt against a small dataset plus metric, and in doing so discovers requirements you never wrote down. Why it is non-obvious: people hear "DSPy" and think "optimizers," then dismiss it as expensive magic; the real payoff is subtler. Why it is true: you define a metric (exact match or LLM-as-judge); the optimizer iterates the prompt; GEPA uses a teacher model to return textual feedback ("not only did you get this wrong, here is why"), tightening the loop toward the Pareto frontier. Madura frames it as inverting the LLM-as-judge failure: instead of the judged model finding cracks to cheat the judge, the optimizer finds the model's cracks to improve it, "using AI to build AI." Concretely it lifts a task 86 to 89, and injects instructions like "you must capitalize names properly" that a human forgot. It generalizes to cost: downgrade GPT-4.1 to 4.1-nano, re-optimize from ~70 back to ~87 percent, cutting cost by orders of magnitude. How it goes wrong: you need ~10 to 100 quality examples and a real metric, and it is offline, not live (delayed feedback just appends to the dataset for the next run).

## 🎬 Proposed ACS videos

### 1. Stop Writing Prompts, Start Declaring Intent
- **HOOK:** The best prompt engineers are about to be automated by the very systems they spent years hand-tuning.
- **THE PROMISE:** For engineers shipping LLM features who are tired of babysitting prompt strings: after this you can structure an LLM feature as typed functions the framework compiles, so it survives every model release without a rewrite.
- **THE SHAPE:** (1) The reframe: the prompt is assembly, not your source code. (2) Signatures: field names act as mini-prompts. (3) Shorthand versus class-based, a live one-line sentiment classifier. (4) Adapters: same program, JSON versus BAML, a five to ten percent swing. (5) Why generated prompts survive model churn.
- **SPINE:** 1.
- **SLOT:** Prompt Engineering class, new chapter "Programming with LLMs" (alternatively Advanced Techniques).
- **RELATIONSHIP:** ❌ net-new. The Prompt Engineering class teaches hand-writing better prompts ("Customized Terminology for Better Prompts", "System Prompt Config"); nothing treats the prompt as a compiled artifact you declare rather than author.
- **PROOF TO REUSE:** Omar Khattab's "DSPy is not an optimizer... it's a way to program"; "the names of the fields act almost as mini prompts"; the JSON-versus-BAML five to ten percent result; the one-line shorthand classifier demo.

### 2. Optimize Your Prompts With Data, Not Vibes
- **HOOK:** An optimizer rewrote a prompt overnight and told the team a requirement they never knew they had.
- **THE PROMISE:** For anyone with a repeated LLM task who keeps tweaking prompts by feel: after this you can build a tiny eval set plus metric and let an optimizer surface latent requirements and recover a cheap model's accuracy.
- **THE SHAPE:** Central demo: build a labeled dataset of 10 to 100 examples, write a metric (exact match or LLM-as-judge), run MIPRO/GEPA, watch it climb 86 to 89, read the auto-injected "capitalize names properly" instruction, then downgrade to a nano model and re-optimize back to ~87 percent.
- **SPINE:** 2.
- **SLOT:** Prompt Engineering class, "Improving Your Prompting" chapter (sits beside "Getting Prompt Feedback").
- **RELATIONSHIP:** 🔗 complements "Getting Prompt Feedback", which reviews your session history and qualitatively rewrites unclear prompts. This is the quantitative sequel: instead of you reading the transcript and guessing, you measure against a dataset and let the optimizer, not you, find the fix. Do not re-teach session-history review; teach dataset plus metric plus optimizer loop.
- **PROOF TO REUSE:** "a poor man's deep learning... it's learning from the data"; "using AI to build AI"; the latent-requirements capitalization example; the GPT-4.1 to 4.1-nano cost-recovery story; the inverted-LLM-as-judge framing (Dwarkesh/Karpathy).

### Also film-able (not deep-dived)
- **Poor Man's RAG:** feed a small document set straight to a multimodal model (via the attachments library, which OCRs PDFs and pulls images) and skip vector stores and embeddings entirely. One-sentence pitch: "You do not need RAG infrastructure for a handful of documents, just hand them to the model." Rough slot: For Business (document processing) or Techniques.

## 📚 Full wisdom (reference)

**SUMMARY**
Kevin Madura, a technical consultant at AlixPartners, explains why DSPy replaces brittle prompt engineering with declarative, typed, modular programs whose prompts the system optimizes automatically.

**IDEAS**
- DSPy treats each LLM call as a typed function, deferring the actual prompt to the framework.
- Signatures declare inputs and outputs; field names themselves act as mini-prompts fed directly into the model.
- A shorthand signature such as text to sentiment integer scaffolds a working classifier in one line.
- Modules structure programs like PyTorch, embedding one or more signatures plus arbitrary hard-coded business logic beneath.
- Adapters sit between the signature and model, formatting the prompt as JSON, XML, or BAML variants.
- Swapping the JSON adapter for BAML can improve performance five to ten percent while cutting tokens.
- React modules expose your plain Python functions as tools, capping rounds so agents cannot spin forever.
- Poor man's RAG feeds a PDF straight to a multimodal model, skipping vector stores and embeddings.
- The attachments library auto-converts PDFs and images into OCR text plus images ready for any model.
- Optimizers iteratively rewrite the prompt string against a metric, requiring no expensive fine-tuning infrastructure or GPUs.
- GEPA uses a teacher model's textual feedback, explaining why answers were wrong to tighten iteration loops.
- Optimizers surface latent requirements, such as learning the model must be instructed to capitalize names correctly.
- Optimizing on GPT-4.1-nano recovered classification accuracy from seventy to eighty-seven percent, slashing cost by many orders.
- The optimizer output is a serializable module, essentially an optimized prompt string you save and reload.
- DSPy automatically caches calls, so unchanged signatures return instantly, making testing and rapid iteration dramatically faster.
- Python context managers let one specific call use a different model without changing the global configuration.

**INSIGHTS**
- Prompts are implementation details, not the deliverable; you should encode transferable intent, not hand-craft fragile strings.
- Your program's design changes slower than model capabilities, so decouple control flow from any specific model.
- Optimizers are DSPy's famous feature, but the real value is the structured, composable programming abstractions underneath.
- LLM-as-judge fails because the judged model finds adversarial cracks; optimizers invert this to improve performance instead.
- Prompt optimization can match or beat fine-tuning like GRPO without any of the training infrastructure overhead.
- Transferability is enabled by optimizers: preserve accuracy while migrating from expensive models to far cheaper ones.
- The right abstraction level matters: DSPy stays out of your way more than heavier frameworks do.
- You can defer output structure entirely to the model, or enforce a strict Pydantic schema instead.
- Optimization is fundamentally offline; delayed user feedback simply appends to the dataset for the next run.
- DSPy is not inherently expensive; the cost comes from how many calls you choose to make.

**QUOTES**
- "It's not iterating with prompts and tweaking things back and forth. It is building a proper Python program." — Kevin Madura
- "You're just declaring your intent of how you want the program to operate, what you want your inputs and outputs to be." — Kevin Madura
- "DSPI is not an optimizer. I've said this multiple times. It's just a set of programming abstractions or a way to program. You just happen to be able to optimize it." — Omar Khattab (quoted by Madura)
- "This is poor man's rag. It's literally just pulling in the document images. The model does the rest." — Kevin Madura
- "The optimizer is basically finding latent requirements that you might not have specified initially up front, but based off of the data." — Kevin Madura (on Chris Potts)
- "It's kind of like a poor man's deep learning, I guess, but it's learning from the data." — Kevin Madura
- "It's using the LLM to dynamically construct new prompts which are then fed into the system, measured, and then it iterates. So it's using AI to build AI." — Kevin Madura
- "The expensive part is totally up to you. If you call a function a million times asynchronously, you're going to generate a lot of cost." — Kevin Madura
- "The names of the fields themselves act almost as mini prompts. It's part of the prompt itself." — Kevin Madura
- "It's really about how you're encoding or expressing your intent, most importantly in a way that's transferable." — Kevin Madura (on Omar Khattab's point)

**HABITS**
- Madura defines multiple LLMs upfront in a config object, mixing reasoning and cheap models per workload.
- He routes image tasks to Gemini and other file types to GPT-4.1 based on their strengths.
- He starts with the shorthand signature to test quickly, then upgrades to class-based signatures for production.
- He uses inspect_history to dump the raw prompt actually sent, verifying what happens under the hood.
- He runs Phoenix from Arize to add observability and tracing across every underlying LLM call automatically.
- He recommends trying optimizers before fine-tuning, seeing how far in-context learning goes without any extra infrastructure.
- He caps React tool-calling loops at roughly five rounds to stop the agent spinning off unpredictably.
- He keeps ten to one hundred quality input-output examples, enough for optimizers without thousands being needed.

**FACTS**
- DSPy uses LiteLLM under the hood to interface with many different model providers through one interface.
- Omar Khattab is the original creator of DSPy and recently appeared on the popular A16Z podcast.
- DSPy modules are modeled on PyTorch's structure, including the forward method invoked when calling them directly.
- Chain of thought modules automatically inject reasoning fields into responses that signatures never explicitly define themselves.
- Research suggests DSPy optimizers like GEPA can match or exceed GRPO fine-tuning in certain measured situations.
- The BAML format is more token-efficient and human-readable than DSPy's default verbose JSON schema adapter output.
- The attachments library was created by a developer named Maxim to simplify feeding files to LLMs.
- Chris Potts recently gave a talk arguing GEPA optimizers rival fine-tuning methods like GRPO very closely.

**REFERENCES**
DSPy; Omar Khattab (creator) and his A16Z podcast appearance; LiteLLM; PyTorch; LangChain; Pydantic and Pydantic AI; Agno; the JSON adapter and BAML adapter; the attachments library (by Maxim); Phoenix by Arize (observability); OpenRouter; MIPRO and GEPA optimizers; GRPO (fine-tuning); Chris Potts' recent optimizer talk; the Dwarkesh and Karpathy podcast (LLM-as-judge point); Pashant (JSON-versus-BAML adapter testing); the "DSPy Hub" concept; the Nvidia Form 4 SEC filing demo; the talk's GitHub repo.

**ONE-SENTENCE TAKEAWAY**
Stop hand-tuning prompts; declare typed intent and let optimizers compile better prompts from your data.

**RECOMMENDATIONS**
- Start any LLM task with a one-line shorthand signature before investing in class-based schemas and modules.
- Build a small dataset and clear metric, then run an optimizer before reaching for expensive fine-tuning.
- Swap the JSON adapter for BAML on complex schemas to gain accuracy and cut tokens measurably.
- Feed small document sets directly to a multimodal model instead of building any vector-store RAG infrastructure.
- Use inspect_history to audit the exact prompt DSPy sends before fully trusting any production pipeline output.
- Optimize a task on a large model, then transfer it to a cheaper one to save.
- Define multiple models in one config and route each workload to whichever model suits it best.
- Keep your existing great prompt by injecting it into the module's docstring as a starting point.
