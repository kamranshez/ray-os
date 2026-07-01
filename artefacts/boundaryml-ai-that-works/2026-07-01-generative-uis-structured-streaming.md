title: Generative UIs and Structured Streaming #22
videoId: RX8D5oJrV9k
url: https://www.youtube.com/watch?v=RX8D5oJrV9k
date: 2026-07-01
status: posted

## The one idea worth a video

**Spine A. Reflect your UX in the type system: declarative streaming annotations make partial LLM output type-safe, killing the imperative render-guard spaghetti.**
Why: it subsumes the valid-partial guarantee, per-field control, the recipe demo, the number/graph example, and the "UX slider" framing. It is the reframe the whole episode hangs off.
VERDICT: 🔗 next-step video available (complements the Prompt Engineering "structured-output" foundations brief).

**Spine B. Stream-triggered fan-out: emit array items as they complete and pipeline downstream work per item, so processing overlaps generation.**
Why: a distinct latency technique with its own demo (per-item research hydration) and its own slot; the source treats it thinly (Route B latent spine) but it is squarely ACS agent-workflow territory.
VERDICT: 🔗 next-step video available (complements test-time-compute / fan-out-fan-in).

*Also film-able (not deep-dived):* **Type-driven dynamic UI generation.** One model generates the data, a second generates the React component that renders its schema ("different but stable"), guardrailed by a design-system component library like Shad CN. One-sentence pitch: teach the "type as the contract between two models" pattern where the renderer itself is generated. Rough slot: Techniques (speculative; Vaibhav says he would not ship it to production yet), so it stays a mention, not a full pitch.

## Summary + counts

Vaibhav and Dexter demonstrate streaming partial structured LLM outputs with BAML, using per-field type annotations to render type-safe generative UIs without imperative conditional-rendering render-guard spaghetti.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine A. Reflect your UX in the type system.**
The claim: encode your rendering rules as declarative annotations on the data type, and partial streaming output becomes type-safe by construction, with no imperative render guards. Why it is non-obvious: the default is to stream raw tokens or partial JSON and then litter the render function with `field?` optional checks and cascading conditional blocks ("if we have this show this, otherwise show nothing"). The mechanism runs in steps. First, the parser knows each field's grammar and completeness heuristics, so it can guarantee a valid partial object at every step and decide when a value is actually done (a question mark ends an integer; a trailing comma or period does not). Second, a stream-done or not-null annotation tells the parser to withhold a field until it is complete, so the generated type carries that field as non-null at compile time. Third, the UI therefore just maps over guaranteed-present values; the streaming complexity moved out of the component and into the type. What it generalizes to: coding agents, where tool calls, thinking, and progress are all streamed structured outputs, so the same annotations govern how an agent's live state renders. How it goes wrong: it only works when your interface is a real type system (JSON schema, Zod, BAML), not arbitrary code, and hiding sensitive fields midstream is not real security because the raw data still arrives.

**Spine B. Stream-triggered fan-out.**
The claim: when an array streams item by item and each item is guaranteed complete on arrival, you can fire downstream workflows per item instead of waiting for the whole array. Why it is non-obvious: the reflexive mental model is "generate the full list, then process it," a serial latency chain; people do not see that a completeness guarantee quietly turns a stream into a work queue. The mechanism: first, the parser only emits an item once it is fully done, so each emission is a valid unit of work; second, an iteration loop over the stream can immediately kick off a follow-up task on that item (Dexter's example: emit the item, then run a deep-research pass to hydrate it with clickable links); third, because item generation and item processing now overlap, total wall-clock time collapses versus the serial version, and Vaibhav calls the speed boost "insanely high." What it generalizes to: coding agents, where as a plan's steps stream out, each completed step can dispatch a subagent so execution begins before planning finishes. How it goes wrong: it is only safe when items are genuinely independent; per-item fan-out multiplies token cost and can swamp rate limits; and a mis-detected "complete" fires downstream work on a half-formed item.

## 🎬 Proposed ACS videos

### 1. Type-Safe Streaming: Stop Writing Render Guards in Your AI App

HOOK: Your streaming AI UI is a pile of "if this field exists" checks, and it does not have to be.
THE PROMISE: For anyone building apps on structured LLM output, render partial results safely with declarative type annotations instead of conditional guards, in about one line per field.
THE SHAPE:
1. Recipe generator demo: broken partial JSON on the left, always-valid object on the right.
2. Add stream-done to ingredients and not-null to servings and name; watch fields gate themselves.
3. The number/graph example: streaming digits left to right snaps a y-axis; "there is no invalid state, only incomplete."
4. The UX slider: full token streaming vs cards-on-completion vs nothing-until-done, and why you want that control trivially.
5. Payoff: `unit` becomes known at compile time, so the render function maps over guaranteed values.
SPINE: A
SLOT: Prompt Engineering > Foundations (adjacent to the "structured-output" brief), or Bonus Techniques.
RELATIONSHIP: 🔗 complements the Prompt Engineering "structured-output" foundations brief. That brief teaches getting one valid typed object out of the model; this adds the streaming layer, controlling how that partial object renders field by field, so Ray does not re-teach basic structured output.
PROOF TO REUSE: "you use the type system to power what the AI does rather than just do it with vibes"; Vaibhav's "UX slider" reframe of Karpathy's autonomy slider; the tablespoons-of-water graph example; "unit now becomes known at compile time."

### 2. Pipeline Your LLM Stream: Start Work Before Generation Finishes

HOOK: If your user can only act at the end of 8,000 tokens, you built an async workflow they abandon.
THE PROMISE: For agent builders, dispatch downstream work per streamed item so processing overlaps generation and wall-clock time collapses.
THE SHAPE:
1. Show an array that emits items only when each is complete.
2. Add an iteration loop that fires a per-item task the instant an item lands (deep-research hydration attaching links).
3. Contrast the serial "generate everything, then process" latency chain against the pipelined version.
4. Tie it to agents: as plan steps stream out, each finished step dispatches a subagent.
SPINE: B
SLOT: Techniques (near stochastic-consensus-and-fan-out-fan-in and test-time-compute).
RELATIONSHIP: 🔗 complements the fan-out-fan-in / test-time-compute videos. Those parallelize independent runs of the same task for consensus or coverage; this pipelines a single stream so downstream work starts before generation completes. It is a latency technique, not a consensus one, so the two do not overlap.
PROOF TO REUSE: Dexter's "emit the item and then go do a deep research to hydrate it with links"; "if your user can only interact with your component at the end of 5,000 or 8,000 tokens, you've basically built an async workflow"; "the speed boost that you get is just insanely high."

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav and Dexter (AI That Works, by BoundaryML) demonstrate streaming partial structured LLM outputs with BAML, using type annotations to build type-safe interactive generative UIs.

### IDEAS
- Streaming partial JSON shows incremental progress instead of a lone spinner, keeping users engaged during generation.
- BAML guarantees a valid partial object at every streaming step, never exposing broken half-parsed JSON downstream.
- Per-field streaming annotations let you decide exactly which fields appear early and which wait until complete.
- Marking a field stream-done means ingredients only render once each ingredient object has fully finished streaming.
- Marking a field not-null blocks all rendering until essential values like serving size are actually present.
- Streaming numbers left-to-right renders jarring intermediate values; wait until complete so a graph never misplaces points.
- BAML uses per-type heuristics and grammar to detect when a streamed value is actually fully complete.
- A question mark after digits proves an integer is complete; a comma or period stays ambiguous.
- The UX slider ranges from full token streaming to cards-on-completion to nothing shown until entirely done.
- Reflecting your UX in the type system replaces imperative render-guard conditionals with clean declarative class annotations.
- Once an array item pops in complete, downstream workflows can hydrate it before generation even finishes.
- Waiting for 5,000-8,000 tokens before any interaction effectively builds an async tab-away workflow users eventually abandon.
- Coding agents are streamed structured outputs already; tool calls, thinking, and progress are all structured streams.
- One model can generate data while a second generates the React component that renders its schema.
- Interactive components combine live UI state, like a servings slider, with whatever partial output has streamed.
- Editable UI can override streamed values locally, letting users fix a quantity the model keeps regenerating.

### INSIGHTS
- There is no fast-enough model; only earlier visible progress keeps a user from dropping off entirely.
- Incremental UX is really about steerability: seeing wrong thinking early lets users abort and restart immediately.
- Encoding rendering rules declaratively in types beats leaking streaming conditionals into every render function you write.
- Ergonomics decide adoption: if type-safe streaming costs one line, developers use it; if painful, they skip.
- UX, not raw model quality, differentiates most AI applications today; streaming design is central to that.
- The type system, whether JSON schema, Zod, or BAML, should power AI output rather than vibes.
- Streaming-completeness guarantees remove optional-field question marks, so a streamed value stays known non-null at compile time.
- Streaming does not save tokens; it lets you spend more without making the user actually wait.
- A generated renderer is different every run yet stable, because a fixed type constrains its shape.

### QUOTES
- "the thing that differentiates most AI applications today is purely the UX and this is a big part of the UX of how you're actually streaming stuff around" (Vaibhav)
- "There's no such thing as an invalid state. It's incomplete, but there's no invalid states like this" (Vaibhav)
- "if your user can only interact with your component at the end of 5,000 or 8,000 tokens, you've basically built an async workflow" (Vaibhav)
- "for anyone that's building agent code, you're basically doing structured outputs all the time. You're basically just streaming structured outputs. That's what tool calls are" (Vaibhav)
- "Andre Karpathi talks about this autonomy slider all the time. But here we kind of have like this UX slider of how much streaming do you want to do?" (Vaibhav)
- "I feel like we're in like the stone age in terms of hooking LLM up to be able to interact with visual state in that world" (Dexter)
- "the premise of what you do with it is that you use the type system to power what the AI does rather than just do it with vibes" (Vaibhav)
- "the AI is generating the React component that renders that type, but it's different but stable" (Vaibhav)
- "You're doing declarative versus imperative and we all know we all love declarative code over here" (Dexter)
- "if it's literally as easy as writing one line of code to make your object stream and feel more ergonomic, just go do it" (Vaibhav)

### HABITS
- Dexter exits Claude Code midstream the moment output looks wrong, restarting rather than waiting for completion.
- Vaibhav adds streaming annotations directly on the data model rather than handling partial state in components.
- They start episodes with live examples and working demos instead of the usual whiteboard-first theory explanation.
- Vaibhav lets Claude fill in React rendering code he cannot write, admitting he mostly writes Rust.
- He formats fractions with proper UTF-8 half glyphs because multiplied servings produce ugly raw decimal quantities.
- They invite the live chat to critique code and submit PRs to the open-source demo site.
- Vaibhav scaffolds demos with pnpm create next-app plus BAML rather than hand-writing all boilerplate project setup.
- They reference their own past episodes, pointing viewers to episode nineteen for interruptible bidirectional streaming details.

### FACTS
- BAML codegens a React hook, a server action, and client code to propagate streamed data forward.
- The AI That Works show crossed 1,500 subscribers by episode twenty-two, hosted by Vaibhav and Dexter.
- Cursor lets you checkpoint code at a point and roll the whole codebase back to it.
- AGUI is a standard protocol from the CopilotKit project for managing information across an entire application.
- Tambo builds tooling for generating UI components on the fly from AI output and type schemas.
- Numbers default to zero while streaming, so an unbounded graph axis stays valid throughout the generation.
- ChatGPT's thinking model exposes clickable thinking sections users can inspect or skip toward faster content generation.
- Episode nineteen covers interruptible agents: monitoring a stream and cancelling it midway to inject new information.

### REFERENCES
- BAML (BoundaryML) and its streaming traits / parser
- AI That Works show (BoundaryML), episode 19 on interruptible agents, GitHub for topic ideas
- ChatGPT thinking model (clickable thinking sections)
- Cursor (code checkpoints / rollback)
- Andrej Karpathy's autonomy slider
- AGUI protocol (CopilotKit project)
- Tambo UI (on-the-fly UI component generation)
- Zod, JSON schema, Shad CN, Vercel AI SDK
- Next.js, pnpm, TanStack, React virtual DOM
- Rolando (chat commenter suggesting design-system-guardrailed layout generation)

### ONE-SENTENCE TAKEAWAY
Encode streaming rules as type annotations so partial LLM output stays type-safe and effortlessly renderable.

### RECOMMENDATIONS
- Add per-field streaming annotations to your data model so partial objects render safely without conditional guards.
- Mark essential fields non-null so the UI renders nothing until those values are actually fully present.
- Choose a streaming granularity per field: full tokens, cards-on-completion, or all-at-once, matching your actual users' preference.
- Kick off a downstream research task on each array item the moment it streams in complete.
- Use a live UI slider that recomputes streamed values, like scaling recipe quantities by chosen servings.
- Add editable overrides so users can correct a streamed value the model keeps regenerating wrongly anyway.
- Have one model produce data and a second generate the React component rendering its typed schema.
- Constrain generated UI to your design system components, like Shad CN, so output matches your theme.
- Watch AI That Works episode nineteen before building bidirectional or interruptible streaming into your own agents.
