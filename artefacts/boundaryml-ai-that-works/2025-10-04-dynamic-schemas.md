---
title: Dynamic Schemas #25
videoId: bak7-C--azc
url: https://www.youtube.com/watch?v=bak7-C--azc
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Meta-programming with LLMs: have the model author the schema first, then run that schema to extract the data.**
The whole episode is one reframe. When you do not know the shape of incoming data, you stop asking the model for values and instead ask it for the *program* (the schema), then execute that program in a second call.
VERDICT: 🔗 next-step video available (complements the planned Structured Output PE Foundations video).

**2. The output format itself is an accuracy lever: express schemas as concise code, not JSON schema.**
The same simple schema is 333 tokens in JSON schema and 69 tokens as code, and the terser form measurably improves generation accuracy.
VERDICT: 🟡 fills a spine-level gap in Structured Output.

**3. The "dumping ground field": give the model a sanctioned junk field so unwanted output stops polluting your real fields.**
A novel prompt-engineering hack the hosts had not heard before: name an "other code" field, and the model self-sorts its stray logic there, keeping key fields clean.
VERDICT: ❌ net-new video available.

## Summary

Dex (Human Layer) and Vibhav (BoundaryML/BAML) demo dynamic schemas: an LLM generates a schema from an image, then extracts and renders live data against it.

🔴 1 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1: Meta-programming with LLMs (model authors the schema, you run it).**
The claim: the most powerful thing LLMs unlock on unknown data is not extraction, it is meta-programming. You ask "given this image, give me a schema plus a return type," then in a second call "given this image and this schema, return the return type." Most people get this wrong because they reach for "AI, turn this into data" in one shot. The mechanism is separation of concerns: call one decides *what shape the data has* and call two decides *what the values are*, so each half is independently testable (you can verify schema generation on samples before wiring up extraction) and each half fails legibly. It generalizes cleanly beyond documents: Dex notes the original 2023 agent was "one LLM call to make a plan, then another to execute it," and the same structure powers Typeform-style form builders and Anthropic's "press the button" custom UIs. Where it goes wrong: unbounded dynamism becomes a liability in production, so you eventually cache, freeze, and consolidate schemas into stable entities. As Vibhav puts it, "you're having the LM do the programming so you can run that program later."

**Spine 2: The output format is an accuracy lever (concise code beats JSON schema).**
The claim: how you represent a schema to the model materially changes both cost and correctness, and JSON schema is the wrong default. Non-obvious because teams treat schema format as cosmetic. The mechanism has two steps: JSON schema is syntactically dense (quotes, braces, required arrays, ISO metadata), so a trivial "string array" costs 23 tokens where code costs a handful, and Vibhav measures the same schema at 333 tokens in JSON schema versus 69 as code, roughly a quarter the size; fewer, information-richer tokens then leave the model less noise to fumble, which he reports as higher accuracy on dynamic generation. It generalizes to model internals: GPT-OSS models accept JSON schema at the API but convert it to a TypeScript-ish syntax before showing the model, for the same reason. Two supporting tricks: tell the model to answer with backticks to dodge escape-character breakage, and prefer a code-like DSL described in roughly 60 lines. How it goes wrong: overly terse formats can lose constraints (required-ness, formats) the model actually needs, so concision has a floor.

**Spine 3: The "dumping ground field" prompt hack.**
The claim: when a model keeps adding stuff you did not ask for, do not fight it with prohibitions; give it a sanctioned field to dump the unwanted output. Non-obvious because the instinct is "don't output code, don't output code," which Vibhav tried and the model ignored ("it turns out the model was dumb"). The mechanism: field names are a control surface. By splitting the schema object into interface_code, return_type, and other_code, any stray logic the model wants to emit lands in other_code, which you simply discard, so your two real fields stay clean and reliable. This is the inverse of constraint-by-prohibition: it is constraint-by-redirection, an escape valve. It generalizes to any structured-output task where the model over-produces: add a "notes" or "scratch" field to absorb reasoning, rationale, or caveats away from the fields you parse. Dex called it "a really cool technique that I don't think I've really heard about before." How it goes wrong: it is a band-aid over an under-specified prompt, and a dumping ground can hide real signal you should have captured.

## 🎬 Proposed ACS videos

### 1. Let the Model Write the Schema: Dynamic Extraction for Data You Have Never Seen

- TITLE: Let the Model Write the Schema: Dynamic Extraction for Data You Have Never Seen
- HOOK: You do not need to know the shape of your data. Make the model draw the schema first, then fill it.
- THE PROMISE: For AI engineers building extraction over unpredictable inputs (invoices, resumes, scans), the one thing you can do after: split any extraction into a schema-generation call and a data-extraction call.
- THE SHAPE:
  1. The naive one-shot "turn this into data" and why it breaks on unknown inputs.
  2. Call one: "given this image, give me a schema plus a return type."
  3. Call two: "given this image and schema, return the return type."
  4. Why splitting shape from values makes each half independently testable.
  5. Production hardening beats: human review between the two calls, caching schemas per image type, freezing schemas into stable columns over time.
- SPINE: 1 (meta-programming).
- SLOT: Prompt Engineering > PE Foundations (sits directly after Structured Output).
- RELATIONSHIP: 🔗 complements the planned "Structured Output" PE Foundations video. That video teaches "define a schema and force the model to fill it"; this is the next step: have the model author the schema at runtime for data whose shape you do not know in advance. Do not re-teach basic structured output; open by assuming it.
- PROOF TO REUSE: the two-prompt whiteboard ("take image, give me a schema" then "take image and schema, output the return type"); Dex's line that the 2023 agent was "one LLM call to make a plan and then another to execute it"; the Typeform framing that a whole business was built on making schema creation pretty and easy.

### 2. The Dumping Ground Field: Stop Fighting the Model, Give It Somewhere to Put the Junk

- TITLE: The Dumping Ground Field: Stop Fighting the Model, Give It Somewhere to Put the Junk
- HOOK: The model keeps adding code you did not ask for. Do not forbid it. Give it a junk drawer.
- THE PROMISE: For anyone doing structured output, the one thing you can do after: add a sanctioned throwaway field so your real fields stay clean instead of prompting "don't do X" and losing.
- THE SHAPE:
  1. The failure: telling the model "don't output logic" and watching it do it anyway.
  2. The reframe: field names are a control surface, not just labels.
  3. Add an other_code / notes / scratch field as an escape valve.
  4. Parse only your real fields; discard the dumping ground.
  5. When this is a band-aid versus a fix (under-specified prompts, hidden signal).
- SPINE: 3 (dumping ground field).
- SLOT: Prompt Engineering > PE Foundations (adjacent to constraints-and-negatives).
- RELATIONSHIP: ❌ net-new. The closest existing video is "Boxing the Model In" (Techniques, filmed), but that is constraint-by-prohibition; this is constraint-by-redirection, the opposite move, and is not covered anywhere in the catalog.
- PROOF TO REUSE: Vibhav's "it turns out the model was dumb... well, let me just give it a dumping ground"; the interface_code / return_type / other_code split; Dex naming it a technique "I don't think I've really heard about before."

### 3. JSON Schema Is Costing You Accuracy: Why Concise Code Beats It 4 to 1

- TITLE: JSON Schema Is Costing You Accuracy: Why Concise Code Beats It 4 to 1
- HOOK: The same schema is 333 tokens in JSON schema and 69 as code. The terser one is also more accurate.
- THE PROMISE: For anyone requesting structured output, the one thing you can do after: measure your schema in both formats and switch to a code-like representation.
- THE SHAPE:
  1. Live token count: JSON schema (333) versus code (69) for the identical schema.
  2. Why density hurts: quotes, braces, required arrays, and metadata are noise.
  3. The accuracy claim: fewer, information-richer tokens generate better.
  4. Evidence from the wild: GPT-OSS converts JSON schema to a TypeScript-ish syntax internally.
  5. The floor: when terseness drops constraints the model actually needs.
- SPINE: 2 (output format economy).
- SLOT: Prompt Engineering > PE Foundations (inside Structured Output) / Context Engineering.
- RELATIONSHIP: 🟡 fills a gap in "Structured Output". That topic covers getting structured data out at all; it does not cover the choice of schema representation and its measured effect on tokens and accuracy, which is spine-level on its own.
- PROOF TO REUSE: the live 333-vs-69 token demo and "one-fourth the size" math; "JSON schema is just extremely verbose"; the GPT-OSS internal-format observation; the backticks-to-avoid-escape-characters trick.

## 📚 Full wisdom (reference)

**SUMMARY**
Dex (Human Layer) and Vibhav (BoundaryML/BAML) demo dynamic schemas: an LLM generates a schema from an image, then extracts and renders live data against it.

**IDEAS**
- Ask the model to look at any PDF and invent a schema that fully models it.
- The entire system is two prompts: image to schema, then image plus schema to filled data.
- This is meta-programming: the LLM writes the program that you later run against the same input.
- Schema generation needs two parts: model every schema, and then declare which return type comes back.
- Output schemas as concise code, not JSON schema: the same model costs 69 versus 333 tokens.
- Give the model an "other code" dumping-ground field so unwanted logic stops polluting your key fields.
- Field names themselves steer the model: name a junk field and it self-sorts its unwanted output.
- Tell the model to answer using backticks to avoid escape characters; the schema quality improved noticeably.
- Inject the runtime schema into a compiled response class that carries one dynamic field named data.
- A bad schema raises a compile exception before any LLM call, so validation comes essentially free.
- The extraction prompt stays trivial: "extract data with this format," then just dump the raw content.
- The model never knows the schema is dynamic; it just sees an ordinary statically typed contract.
- Streaming forces a custom SSE bridge emitting partial, final, and error events between backend and frontend.
- Arbitrary schemas force a recursive renderer that switches on type to draw tables, JSON, or YAML.
- Cache schemas in a database: for a similar image, reuse a saved schema instead of regenerating.
- Even if the model omits the data field, the BAML parser maps output into the schema.
- Typeform monetized almost nothing but making schema creation pretty and stupid-easy to do on the fly.

**INSIGHTS**
- Dynamic schemas turn the model into a program author rather than merely a passive data-filling function.
- Splitting shape-inference from value-extraction into two separate calls makes each half independently testable and easily debuggable.
- The verbosity of your output format directly degrades accuracy; concise code significantly beats dense JSON schema.
- Field naming is a control surface: a sanctioned junk field redirects the noise away from signal.
- Dynamic power is both a superpower and a weakness; production often needs schemas frozen over time.
- Static types at the boundary let you keep type-safety even when the middle is fully dynamic.
- Human review fits naturally between schema generation and extraction, right before anything irreversible actually happens downstream.
- Over many documents, you consolidate generated schemas into stable entities, flagging real drift for human review.
- Handling arbitrary schemas has no real shortcut; a dynamic recursive renderer is unavoidable for open output.

**QUOTES**
- "This is basically just meta programming." (Vibhav)
- "It's one of the most powerful concepts that becomes possible in the world of GenAI." (Vibhav)
- "This is like a really interesting flavor of context engineering where you're using AI to generate something that goes into that a downstream prompt." (Dex)
- "The original agent was like use one LLM call to make a plan and then use another LLM call to execute it." (Dex)
- "JSON schema is just extremely verbose." (Vibhav)
- "It turns out the model was dumb." (Vibhav)
- "Well, let me just give it a dumping ground." (Vibhav)
- "Giving the model other fields to dump the things that you don't want to so that your key fields that you're working with stay really clean and concise." (Dex)
- "The LLM doesn't even know it's a dynamic schema. It just thinks it is." (Vibhav)
- "No matter what you do, you will have to build some sort of dynamic rendering at some point if you're going to handle arbitrary schemas." (Vibhav)
- "You want to be extracting the same thing from every one of those, otherwise you just have a bunch of JSON in your database rather than like structured columns." (Dex)
- "Typeform... makes so much money because of how pretty they made making schemas." (Vibhav)

**HABITS**
- Vibhav always defines a return type alongside every schema, never treating the schema itself as enough.
- He instructs the model to answer with backticks, thereby sidestepping fragile escape-character handling in generated code.
- He keeps entirely separate hooks for streaming versus non-streaming responses rather than forcing one code path.
- He writes test cases feeding the type builder directly, simulating what the model would have generated.
- He builds first, verifies each workflow part on samples, then slowly composes toward the full system.
- Dex reflexively probes any guest by asking what problem are you actually trying to solve here.
- He generates a schema live on webcam, screenshotting his own phone to prove nothing is prerecorded.
- He renders every extraction result three ways, as table, JSON, and YAML, via one tab switch.

**FACTS**
- The same simple schema costs 333 tokens in JSON schema but only 69 tokens as code.
- That token difference is roughly a fourth the size, computed live as 333 divided by 86.
- BAML syntax is described to the model in roughly 60 lines of code serving as context.
- BAML is described as pretty much TypeScript except for one difference: it uses no colon character.
- GPT-OSS models accept JSON schema over the API but actually receive a TypeScript-ish syntax internally instead.
- BAML's type builder registers dynamic types additively at runtime and refuses to redefine an already-named type.
- The plan-then-execute two-call agent pattern has existed since roughly 2023, back in the early ChatGPT days.
- BAML generates Python and React bindings automatically from one source of truth via a generate file.

**REFERENCES**
BAML / BoundaryML; Human Layer; the "AI That Works" show and its open-source repo; Cursor; VS Code; FastAPI; Pydantic; Zod; Typeform; Swagger / OpenAPI spec; GPT-OSS models; Anthropic's recent "press the button" custom-UI feature; ChatGPT; Server-Sent Events (SSE); YAML; JSON schema; TypeScript; Jevons paradox; Bezos ("good intentions don't work, mechanisms do"); the Kindle (Eugene); Suno; Luma; Discord.

**ONE-SENTENCE TAKEAWAY**
Have the model generate a concise-code schema, then run that schema to extract dynamic data.

**RECOMMENDATIONS**
- Build the two-call pipeline yourself: first infer a schema, then extract values against that same schema.
- Compare token counts of JSON schema versus code for your schema before choosing an output format.
- Add a junk "other code" field whenever the model keeps polluting your otherwise clean structured output.
- Insert a human review step between schema generation and extraction for any high-stakes irreversible extraction workflow.
- Cache generated schemas keyed on image similarity so that repeat document types skip schema regeneration entirely.
- Freeze schemas into stable columns once you process many similar documents, not endless untyped JSON blobs.
- Test your dynamic extraction by feeding the type builder directly instead of relying on live generation.
- Keep static types at your API boundary so that any-typed dynamic middles stay debuggable and safe.
