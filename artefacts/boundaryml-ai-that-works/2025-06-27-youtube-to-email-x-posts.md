---
title: "Using LLMs to go from 60+ min YouTube video to email / X posts #11"
videoId: Xece-W7Xf48
url: https://www.youtube.com/watch?v=Xece-W7Xf48
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Build the whole product harness (glue code, DB, UI, types, job system) FIRST, then bolt on and iterate the AI part last.** The AI layer is worthless without infrastructure you can iterate on, so the sequencing itself is the lesson, not the model call.
VERDICT: net-new video available.

**Turn a single real pipeline run into a golden test case, then iterate the prompt in isolation instead of end-to-end.** Fake or synthetic data is the worst input; run once, pay the cost, capture the real record, and tune against it alone.
VERDICT: next-step video available (complements the feedback-loops video).

**Few-shot injects bias because the model cannot tell your example from real input; use partial / dynamic few-shot to guarantee it reads as an example.** Show only the decisive field and vary the names so the example can never be confused with the live case.
VERDICT: next-step video available (complements the few-shot video).

*Also film-able (not deep-dived):*
- **Let the model write natural triple-quoted strings instead of escaped JSON.** Structured generation invalidates tokens and hurts prose quality. Complements Prompt Engineering > Core Techniques > Structured Output.
- **No frameworks: your code is already a directed graph.** Orchestrate with plain asyncio.gather and own every token. Net-new, Advanced Techniques.

---

## Summary

Vaibhav (BAML) and Dexter (12-factor agents) live-build an AI content pipeline turning 60-minute Zoom recordings into email, X, and LinkedIn drafts, iterating prompts live throughout.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: Build the harness before the AI

**The claim.** Before you touch a prompt, build the entire product around it: ingestion, database, UI, typed contracts, and the job runner. Only then does iterating the AI become possible.

**Why it's non-obvious.** The instinct is to start with the exciting part, the prompt, and glue the rest on later. Vaibhav argues the opposite: "if we hadn't built this whole system up that could do the glue code, building the AI part is completely useless."

**Why it's true.** The AI part is not a destination, it is one node inside a loop. Because you cannot judge an email draft without seeing it rendered, feeding back edits, and re-running, the loop IS the product. Build the loop and every prompt tweak is a five-second experiment; skip it and you have "a bunch of Python scripts you don't actually use," which is a waste.

**What it generalizes to.** The same holds for internal tools generally: the eight-hour SaaS scaffold pays for itself the moment you can iterate on the valuable layer instead of hand-assembling inputs.

**How it goes wrong.** Over-building the harness can become procrastination; the antidote is his real-time-DB architecture where the schema is the whole API contract, keeping the scaffold thin.

### Spine 2: Real runs become golden test cases

**The claim.** The fast prompt loop is: run the real pipeline once, capture the exact input-output record, then iterate on that single case in isolation, never end-to-end.

**Why it's non-obvious.** Most people either test the whole pipeline each time (painfully slow) or fabricate inputs. Vaibhav is blunt: "Fake data is the worst thing I can do," because synthetic data works and then fails on the real distribution.

**Why it's true.** Running end-to-end couples prompt quality to Zoom download, YouTube upload, and streaming state, so a five-second idea costs minutes. Capturing one real record decouples the prompt from the plumbing, so you iterate at the speed of thought, then let the agent fix downstream. He instruments API keys precisely so real runs convert into test cases.

**What it generalizes to.** This is golden-file testing for non-deterministic work: bless the outputs you like as regressions, and take the ones you dislike to the workbench, the same move his A/B title work relies on.

**How it goes wrong.** You can iterate fast without an eval set only when you already hold a golden target in your head; on an unfamiliar domain there is no target and you stall.

### Spine 3: Partial / dynamic few-shot prompting

**The claim.** Few-shot examples inject bias because the model cannot reliably separate "this is a demonstration" from "this is real data," so you must engineer the example to read unambiguously as an example.

**Why it's non-obvious.** Few-shot is treated as a free reliability win. Vaibhav's counterexample: a rare-liver-disease example plus a real patient named Sarah, and the model starts inferring that Sarah has the condition, because the example leaked into the live case.

**Why it's true.** The model predicts from tokens; identical surface features (a shared name) collapse the boundary between example and input. His fix is partial few-shot, showing only the decisive field ("because they don't code, the category is product") and dynamically changing names so the example can never match the live input.

**What it generalizes to.** Any style-transfer prompt where you show tone: a marketing-email example tuned to one author will silently drag every output toward that author unless you fence it as an example.

**How it goes wrong.** When you fully control the domain (only your own videos), the bias is desirable, so the technique matters most on general, multi-tenant inputs.

---

## 🎬 Proposed ACS videos

### 1. Build the Harness Before You Touch the AI
- HOOK: You are excited to write the prompt. That is exactly why your AI project will die.
- THE PROMISE: For builders shipping AI features, learn to sequence the build so the AI layer is the last thing you tune, not the first.
- THE SHAPE:
  1. The trap: a great prompt with no product around it is unusable.
  2. Build the thin real-time-DB scaffold: front end reads DB, backend reads and writes, schema is the API.
  3. Codegen one type contract into Python and TypeScript so mismatches break at compile time.
  4. A job system that is just a table of nullable columns plus a status field.
  5. Only now: drop in the prompt and iterate, because the loop already exists.
- SPINE: 1
- SLOT: Advanced Techniques (or Start Here as a build-order principle)
- RELATIONSHIP: ❌ net-new. The catalog's Agent Harness Concept video teaches what a harness IS (the infra wrapping an LLM); this teaches the build ORDER for AI products, that you scaffold the product before tuning the model. Distinct claim, no existing video.
- PROOF TO REUSE: "building the AI part is completely useless" without the glue code; the 8-hour nothing-to-SaaS build; "build the workflow first. Once you've built the workflow, add the AI part."

### 2. Turn Real Runs Into Golden Test Cases
- HOOK: Stop testing your prompt by running the whole pipeline. Run it once, then never again.
- THE PROMISE: For anyone iterating on prompts, learn to capture one real record and tune against it in seconds instead of minutes.
- THE SHAPE:
  1. Why end-to-end iteration is too slow and why synthetic data lies.
  2. Instrument the pipeline so every model call is logged.
  3. Run once, pay the cost, download the real input-output pair as a test case.
  4. Iterate the prompt on that record alone, then let the agent fix downstream.
  5. Bless the good outputs as golden files; take the bad ones to the workbench.
- SPINE: 2
- SLOT: Advanced Techniques > feedback loops (sits next to Building Inner and Outer Feedback Loops)
- RELATIONSHIP: 🔗 complements "Building Inner and Outer Feedback Loops" by being its next step. That video teaches outer loops for non-technical work (feeding real-world CTR and open-rate outcomes back in); this adds the INNER loop, capturing a single real production record as a golden test case and iterating the prompt on it in isolation. Do not re-teach the outcome-metric loop.
- PROOF TO REUSE: "Fake data is the worst thing I can do"; "run the pipeline once, pay the cost, download the test case"; adding API-key observability specifically to convert logs into test cases.

### 3. Dynamic Few-Shot: Make the Model Know It's Just an Example
- HOOK: Your few-shot examples are quietly poisoning your outputs, and you can't see it.
- THE PROMISE: For prompt engineers, learn to write examples the model cannot confuse with real input, killing the hidden bias few-shot injects.
- THE SHAPE:
  1. The failure: the Sarah / rare-liver-disease case, where the example leaks into a real patient.
  2. Why it happens: the model cannot separate demonstration tokens from input tokens.
  3. Partial few-shot: show only the decisive field, omit the rest.
  4. Dynamic names: vary example names so they never match the live input.
  5. When the bias is actually fine (fully controlled, single-tenant domains).
- SPINE: 3
- SLOT: Prompt Engineering > Core Techniques (next to Few-Shot Prompting)
- RELATIONSHIP: 🔗 complements "Few-Shot Prompting" by being its next step. That video teaches when and how to use examples (zero to many-shot, cover the edges, show what not to do); this adds the failure mode it does not cover, that examples inject bias and can be mistaken for real data, plus the partial and dynamic fixes. Do not re-teach the basics of when to use few-shot.
- PROOF TO REUSE: "you want to guarantee the model thinks of the thing you're providing as an example"; the liver-disease / Sarah example; the "because they don't code, the category is product" partial example.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BAML) and Dexter (12-factor agents) live-build an AI content pipeline turning 60-minute Zoom recordings into email, X, and LinkedIn drafts, iterating prompts live throughout.

### IDEAS
- Build the entire product infrastructure and glue code first, then bolt on and iterate the AI.
- Without infrastructure you can iterate on, building the AI part alone is completely useless and unusable.
- Front end reads only from the database and issues requests; it never fetches data from backend.
- A real-time database is your single state of truth, rendered to the front end extremely fast.
- Codegen one BAML contract into both Python and TypeScript types so backend and frontend stay synchronized.
- Change the shared type and the front end breaks at compile time; Claude Code fixes it.
- A job system can just be a database table with nullable columns plus a status field.
- Skip frameworks entirely; your code already expresses a directed graph, orchestrated with a plain asyncio gather.
- Your output quality is strictly bound by the exact tokens sent into and out of models.
- Frameworks inject hidden preambles and reshape tools, capping quality at whatever generic users can achieve too.
- Capture real production data as a golden test case; never iterate prompts on synthetic fake data.
- Few-shot prompting injects bias because the model cannot reliably distinguish your example from real incoming data.
- Partial few-shot shows only the differing field, guaranteeing the model reads the provided pair as example.
- Dynamically change names in examples so they differ from the actual input the prompt runs on.
- JSON structured generation invalidates tokens, forcing escape characters and biasing the model away from natural output.
- Let the model write triple-quoted multi-line strings instead of escaped JSON to improve email writing quality.
- Add a reasoning preamble so the model outlines a dense summary before filling the structured schema.
- Streaming structured data forces a duality of type systems: partial nullable during stream, complete when done.

### INSIGHTS
- The AI layer is the last mile; the iteration harness around it determines whether you ship.
- Unidirectional data flow removes implicit agent decisions about whether logic belongs in the frontend or backend.
- A shared type contract gives agents so little room that mistakes have almost nowhere to hide.
- Owning the full prompt lets you push past the quality ceiling generic framework users hit permanently.
- The fastest prompt loop is a single real captured record, iterated in isolation from the pipeline.
- Few-shot works safely only when you can guarantee the model treats the example strictly as example.
- You can iterate without an eval set when you personally hold a golden target in mind.
- JSON was the wrong primitive for structured generation; the constraint exists only because parsers are weak.
- The best eval runs the whole pipeline end-to-end, then narrows into individual prompts to isolate failures.
- Building internal tools for yourself is extremely high leverage now that a SaaS takes just hours.

### QUOTES
- "before you can even work on your AI part of your pipeline, you're not even at the point where you can start working on that." (Vaibhav)
- "if we hadn't built this whole system up that could do the glue code, building the AI part is completely useless." (Vaibhav)
- "code is already a directed graph." (Dexter)
- "Your quality is strictly bound by the tokens you send in and out of the model." (Vaibhav)
- "Fake data is the worst thing I can do." (Vaibhav)
- "the idea of few-shot prompting is you want to guarantee the model thinks of the thing you're providing as an example." (Vaibhav)
- "JSON was like totally the wrong decision for for structured generation just in general." (Dexter)
- "It turns out just like let the model do its thing." (Vaibhav)
- "build the tools that you need, build the workflow first. Once you've built the workflow, add the AI part." (Vaibhav)
- "when you're streaming, you actually live in a duality of type systems, and that is the part that people really miss out on." (Vaibhav)
- "We don't do frameworks here." (Vaibhav)
- "Today everyone uses Excel, tomorrow everyone's going to write code." (Vaibhav)

### HABITS
- They publish every episode's full code and notes to a public GitHub repo every Friday morning.
- Vaibhav stages finished changes in git before asking Claude Code to make the next code edit.
- He runs the pipeline once, pays the cost, downloads the real test case, then iterates locally.
- He keeps each test in its own file because transcripts are long and bloat agent context.
- He sets temperature to zero to force the model to follow dense-summary instructions much more reliably.
- He adds observability by wiring API keys so every model call is logged and fully traceable.
- He prefers Anthropic models for instruction-following on structured tasks, noting they listen better than OpenAI here.
- They bless good real outputs as golden files to lock working behavior against future prompt changes.
- He prompts agents to read whole long files rather than skimming a partial hundred-line window only.

### FACTS
- The whole pipeline was built in roughly eight hours, from nothing to a generating SaaS flow.
- The build ran from 6pm to about 2:30am, including a ninety-minute break in the middle overnight.
- AI that works airs Tuesdays at 10am and publishes recorded videos on Fridays at 8am each week.
- Zoom takes roughly four hours to process a recording and generate its transcript after recording ends.
- A single Zoom meeting can produce multiple video files when presenters stop and restart the recording.
- Vaibhav wrote the tool-call streaming for vLLM and contributed streaming to the Vercel AI SDK too.
- The unidirectional data-flow pattern echoes React's Flux era, when six frameworks emerged in one single summer.
- Almost every text file is valid YAML, making YAML nearly impossible to parse as constrained output.

### REFERENCES
- BAML (BoundaryML), including its React hooks client (useSummarizeVideo hook) and Vercel integration.
- 12-factor agents (Dexter / HumanLayer).
- Vercel AI SDK (structured object generation, streaming, React helpers), and its opinionated use of Zod.
- Zod schema library; Pydantic (Python data models).
- vLLM (Vaibhav wrote its tool-call streaming).
- Claude Code and Cursor agent (Vaibhav prefers Claude Code).
- Zoom API and Luma (meeting creation / title inheritance).
- v0 (Vercel UI generation) and its limits when syncing front end with a non-TypeScript backend.
- Temporal (named as the heavier job-orchestration alternative they deliberately avoid).
- Postgres JSONB columns and materialized views for the real-time data layer.
- Models referenced: GPT-4o mini, GPT-4.5, Anthropic Sonnet, Gemini (for video-as-context).
- Prior AI that works episodes: the evals episode, the emails episode, the reasoning episode; the "RTFP" (read the prompt) idea.
- GitHub repo shortlink: hlyr.dev/aitw.

### ONE-SENTENCE TAKEAWAY
Build the whole iteration harness first; only then can you make the AI part good.

### RECOMMENDATIONS
- Build your product's plumbing and UI first so you have something real to iterate AI on.
- Adopt unidirectional flow: front end reads database, issues requests; backend reads and writes the database only.
- Generate both frontend and backend types from one contract so mismatches surface as compile-time errors immediately.
- Run your real pipeline once, capture the input-output pair, and iterate the prompt on that record.
- Replace heavyweight job frameworks with a simple table of nullable columns and an explicit status field.
- Use partial few-shot: show only the decisive field and vary names so examples read as examples.
- Let models emit natural triple-quoted strings instead of escaped JSON when writing prose like long emails.
- Add a reasoning preamble field so the model plans densely before emitting your structured data model.
- Instrument every model call with logging so real runs convert directly into reusable test cases easily.
- Split large tests into separate files so coding agents can read each one fully without truncation.
