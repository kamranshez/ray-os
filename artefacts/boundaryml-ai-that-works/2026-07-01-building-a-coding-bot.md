---
title: "Building a coding bot #3"
videoId: KJkvYdGEnAY
url: https://www.youtube.com/watch?v=KJkvYdGEnAY
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1 - Build the coding agent as small deterministic glue between focused prompts, giving each stage a hard guarantee and offloading everything a parser can do off the LLM.** This is the reframe the whole session hangs off: the model only turns context into tokens, so you decompose the job and let string-matching and Python's AST carry the rest.
VERDICT: 🔗 next-step video available (complements closing-the-loop).

**Spine 2 - Design the pipeline as a cost distribution and migrate each step leftward to the smallest model that works, adding scaffolding rather than prompts.** Start everything on a big model for accuracy, then shift the expensive station (applied-diff) to smaller models over time.
VERDICT: ❌ net-new video available.

**Spine 3 - Author the context retroactively: when the model errors then recovers, delete the failed turns so downstream steps see a clean first-try success.** A manufactured clean history beats an honest record of the model's mistakes.
VERDICT: 🔗 next-step video available (complements the Context Engineering class).

---

## Summary + counts

Vaibhav and Dax build a diffing coding agent in pseudocode: decomposing it into deterministic stages, offloading work off the LLM, and routing across model sizes.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

**Spine 1 - Deterministic glue with per-stage guarantees.**
The claim: a homemade coding agent should be small deterministic glue between focused prompts, not one model loop asked to do everything. Non-obvious, because the default everyone reaches for is exactly the naive loop Vaibhav names: "ask the LM to go fix something, if it breaks, give it the error and go build that loop forever." Why it collapses: as errors pile into one window the model loses the thread and spins out, and the real failure is unmanaged context, not weak reasoning. So you decompose: generate a diff, apply it per file, validate, loop. Each stage carries a guarantee, "the old string exists in the file," which shrinks what the model must reason about to almost nothing, "all I have to do is find a match." Anything deterministic leaves the model entirely: syntax validation runs through Python's AST, imports are found by walking the parse tree. It generalizes past code to any structured-output agent (SQL generation, form-filling) where a validator can gate each step. How it goes wrong: over-decompose and you drown in glue; the AST catches syntax, never broken imports or logic.

**Spine 2 - The model-routing distribution play.**
The claim: shape your pipeline as a cost distribution and push each step to the smallest model that still works. Non-obvious because most people pick one model for the whole system and tune prompts; Vaibhav instead tunes which model handles which sub-task. The mechanism: on day zero you run everything on GPT-4o and ignore cost, because you only care that accuracy is high; once a step proves valuable you add supporting systems around it so a smaller model can succeed, and "you incrementally replace parts of your pipeline with smaller and smaller models." Finding imports is small enough for Llama 8B; the expensive station is applied-diff, so shifting that one leftward drags the whole cost curve left. It generalizes to any high-volume LLM product where a long expensive tail is tolerable but the median must be cheap and fast. The kicker: every accuracy scaffold you built for a small model also lifts a big model dropped back on top, so you get a better big-model result than a naive single prompt. Goes wrong when a task genuinely needs frontier reasoning and you starve it to save cents.

**Spine 3 - Manufacture a clean context history.**
The claim: when a model errors and then recovers over several turns, delete the failed turns and present the next stage a history where it got the answer right the first time. Non-obvious because it feels dishonest, and most people keep the full transcript "for context." The mechanism: Vaibhav walks the Cypher-query case, model gets it wrong, you add correction context, it gets it right, then "I will literally just ignore everything that the model did in the middle and only give the right query." The failed attempts are noise that costs attention and, in a long window with many error types, is exactly what makes the model lose the thread. Keeping only the successful trajectory means every downstream step reasons over a short, clean, high-signal window. It generalizes to any agent loop, tool-use recovery, retry chains, and it "becomes even more important when you're doing a complex task like code generation." Goes wrong if the failures carried information the next step needed, so this is for recoverable, self-contained errors, not for hiding systematic problems.

---

## 🎬 Proposed ACS videos

### 1. Stop Looping the LLM on Errors: Build a Coding Agent as Deterministic Glue
- HOOK: The reason your homemade coding agent spins out is that you handed the entire job to one model loop.
- THE PROMISE: For engineers building their own coding agents, decompose the agent into stages that each carry a hard guarantee, so no single model call reasons about everything.
- THE SHAPE:
  1. The brittle default: ask, run, feed the error back, repeat, watch it collapse.
  2. Decompose into generate-diff, apply-diff (find match), validate, loop, each a focused prompt.
  3. Give each stage a guarantee ("the old string exists") so the model's scope shrinks.
  4. Offload syntax validation and import detection to Python's AST, not the model.
  5. Abort with an observation when no match is found instead of forcing a guess.
- SPINE: 1
- SLOT: Techniques > Agent Architecture (near closing-the-loop and core-agent-loop)
- RELATIONSHIP: 🔗 complements "closing-the-loop", which teaches run-it, feed-the-error-back, repeat; this adds the next step, that the naive loop is brittle and must be broken into guaranteed deterministic stages with parsers doing the verification.
- PROOF TO REUSE: the calculator "add exponent" demo; "the most important part to do is be able to decompose the problem to very small problems"; the AST validate-and-repair while-loop; "I've seen cloud code mess this up a lot... find replace... fall back to sed and grep."

### 2. Route Every Step to the Cheapest Model That Works
- HOOK: You do not need GPT-4o to find imports. You need it for one hard step and a tiny model for the rest.
- THE PROMISE: For anyone running a multi-step LLM pipeline, shape it as a cost distribution and migrate each step leftward to smaller models without losing accuracy.
- THE SHAPE:
  1. The distribution mental model: most requests cheap, a tolerable expensive tail.
  2. Day zero: run everything on the big model, ignore cost, chase accuracy.
  3. Find the smallest model per task (find-imports runs on Llama 8B).
  4. Shift the expensive station (applied-diff) leftward by adding scaffolding, not just prompts.
  5. Drop the big model back on top of the scaffolding for a free accuracy boost.
- SPINE: 2
- SLOT: Techniques > Multi-Model & Multi-CLI Workflows (adjacent to the-ambiguity-line)
- RELATIONSHIP: ❌ net-new. No existing video routes internal pipeline steps by model cost and capability; the-ambiguity-line routes whole tasks between Claude Code and Codex, a different axis (agent choice, not sub-step model size).
- PROOF TO REUSE: swapping GPT-4o to 4o-mini to Llama 8B on find-imports; "you incrementally replace parts of your pipeline with smaller and smaller models"; the hand-drawn cost distribution curve shifting left; "drop in a big model again and... your big model is going to perform a lot better."

### 3. Lie to Your Agent: Rewrite Its History So Every Failure Disappears
- HOOK: When the model finally gets it right after three wrong tries, delete the wrong tries from its memory.
- THE PROMISE: For anyone building multi-step agents, author the context retroactively so downstream steps see a clean first-try success instead of a pile of failed attempts.
- THE SHAPE:
  1. Show the honest transcript: attempt, error, correction, error, correction, success.
  2. Why that pollutes the window and derails the next step.
  3. The move: keep only the successful query, delete the failed turns.
  4. Present a manufactured "got it right first try" history to the next stage.
  5. Clear the observations once the system reaches a good state.
- SPINE: 3
- SLOT: Context Engineering > Managing the Window (new video in the shipped class)
- RELATIONSHIP: 🔗 complements the Context Engineering class, which teaches managing and compacting context; this adds the specific move of retroactively editing the trajectory to hide the model's failed attempts so later steps reason over a clean window.
- PROOF TO REUSE: the Cypher-query error example; "I'm pretending like I got the answer... on the first try"; "remove these two messages out of the context window... becomes even more important when you're doing a complex task like code generation."

### Also film-able (not deep-dived)
- **Let the Model Write Code the Way It Was Trained: Flat Multi-Line Strings, Never JSON** - the no-NOTs rule plus triple-backtick multi-line output plus role boundaries as free separators. SLOT: Prompt Engineering > Structured Output. 🟡 partial: constraints-and-negatives already covers negatives and structured-output covers formatting, but the specific nugget (never wrap code in JSON, stream it flat via triple backticks because that matches the model's training distribution) is missing.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BoundaryML) and Dax build a diffing coding agent live in pseudocode, decomposing it into deterministic stages, offloading work off the LLM, and routing across model sizes.

### IDEAS
- Break a coding agent into small deterministic glue connecting focused prompts, not one giant do-everything loop.
- Regenerating whole files fails because output token limits cap models; generate small diffs instead for tractability.
- Apply diffs a single file at a time, never all at once, keeping each edit tractable.
- Give each stage a hard guarantee, like "the old string exists," shrinking what the model handles.
- To apply a diff, first find the old snippet via string match, LLM, or Levenshtein distance.
- When no match for the old snippet exists, abort the edit instead of forcing a guess.
- Use Python's AST library rather than an LLM to check that generated code is syntactically valid.
- Detect imports by walking the AST tree with ast.parse, not by running code and reading errors.
- When the model errors, add correction context, get the fix, then delete the failed turns entirely.
- Rewrite the final context so the model appears to have gotten the answer right first try.
- Design the pipeline as a cost distribution; keep most requests cheap, tolerate an expensive long tail.
- Start every pipeline step on a big model, then shift work leftward to smaller models later.
- Finding imports is small enough for GPT-4o-mini or even Llama 8B; reserve GPT-4o for hard generation.
- Smaller models gain less from prompt tweaks and more from supporting systems like surrounding AST scaffolding.
- Never make the model output code inside JSON; escaping quotes derails it from writing good code.
- Have the model stream code as flat multi-line strings using triple backticks, matching its training distribution.
- Remove negative instructions; models struggle with "nots," so grant a capability instead of forbidding a behavior.
- Role boundaries act as free, well-trained separators that mark exactly where the pasted code block begins.
- Treat the user's instructions as trustworthy system-level guidance, not as a suspicious chat turn to second-guess.
- Generating new code and editing existing code are separate problems; build two systems with a router.
- V0 nails the first draft but degrades by message twenty-five because editing is a different problem.
- Good context and clear instructions make editing easy; bad context is almost always impossible to correct later.
- The best UX for coding tools solves context-gathering, like Cursor's @-file references and V0's element selection.

### INSIGHTS
- The LLM's only job is turning context into tokens; everything else exists to feed it context.
- The brittle default agent, loop the LLM on errors forever, collapses precisely because nobody manages context.
- Decomposition lets each sub-problem carry one guarantee, so no single model call must reason about everything.
- Offloading deterministic work to parsers frees smaller models to attempt only near-correct generation, not perfection.
- Prompt engineering aligns a model with its training; asking for JSON-wrapped code fights how it learned.
- Negative instructions cost attention; reframing a prohibition as a capability is easier for models to follow.
- Context can be authored retroactively; a clean invented history outperforms an honest record of model's mistakes.
- Engineering around a model, not just prompting it, is what actually shifts cost, latency, and accuracy.
- Every accuracy technique built for small models also amplifies a big model dropped back into pipeline.
- Editing precision, not generation, is the expensive station where diffing pipelines actually break and burn money.
- Solving context-gathering is largely a UX problem, because the model cannot invent context the user withheld.

### QUOTES
- "the LM's job is to turn context into new tokens, new code." - Dax
- "the most important part to do is be able to decompose the problem to very small problems." - Vaibhav
- "Good instructions are a lot easier to correct... Bad context is virtually impossible to correct." - Vaibhav
- "let the model write code in the way that it's most trained to write code, which is not code inside a big JSON object, but is just stream the code out flat." - Dax
- "the idea of a not is just very very hard for it to go do." - Vaibhav
- "I'm basically just managing the context. I'm pretending like I got the answer on the right on the first try." - Vaibhav
- "the way most people apply this agent is a very simple loop of ask the LM to go fix something, if it breaks, give it the error and go build that loop forever." - Vaibhav
- "V0 is so freaking good at giving you a UI out of the box, but it's so bad at updating code eventually." - Vaibhav
- "you incrementally replace parts of your pipeline with smaller and smaller models." - Vaibhav
- "the LM should not to be doing syntax validation." - Vaibhav
- "I want to do the hard part as much as possible with a big model. I want to do the small parts with smaller models." - Vaibhav

### HABITS
- Vaibhav starts on GPT-4o for accuracy on day zero, ignoring cost until the system proves valuable.
- He hunts for the smallest model that can reliably handle each individual task in the pipeline.
- He rewrites negative prompt instructions into positive capabilities, deleting every "not" he catches himself writing down.
- He renames overloaded variables, like "diff," when the model confuses the field name with the action.
- He sets temperature to zero for code generation to reduce variance in the model's structured output.
- He caps retry loops, breaking after roughly five attempts or twenty errors instead of looping forever.
- He indents nested prompt content so the model reads structure the way a human scanning would.
- He tracks an observations object threaded through every downstream stage, appending unfixable errors before aborting cleanly.
- He clears the observations history once the system reaches a good state, keeping later context clean.
- He prototypes architecture in pseudocode first, admitting he could not write the real code in realtime.

### FACTS
- Modern model output token limits make regenerating files longer than 4,000 to 8,000 tokens generally impractical.
- Python's standard library ast module can parse code and yield every import node via tree walking.
- GPT-4o-mini struggles to apply diffs reliably, whereas GPT-5 or GPT-4.1 can often one-shot the same task.
- Ollama requires the explicit "latest" tag to run a model, a common setup annoyance Vaibhav hit.
- Cursor lets users reference specific files inline; V0 lets users click and select page elements directly.
- AST syntax validation catches missing commas and malformed syntax but cannot detect broken imports or logic.
- One attendee generated roughly 200 files, half docs, across eleven directories in V0 with few errors.
- A common install error is running "pip install ." when the package needs a different invocation.

### REFERENCES
- BoundaryML "AI That Works" series (the recurring session this is episode 3 of)
- BAML / BoundaryML (the schema and output-format tooling shown, with the raw-prompt viewer)
- Models: GPT-4o, GPT-4o-mini, GPT-5, GPT-4.1, Llama 8B
- Ollama (local model runner), Python AST library, Levenshtein distance
- Cursor (@-file references, browser tools MCP), V0 by Vercel (element selection), StackBlitz
- Next.js and TypeScript (cited for V0's easy import detection)
- People: Vaibhav (BoundaryML, lead), Dax (co-host); attendees Gabe, Jonathan, Tal, Derek

### ONE-SENTENCE TAKEAWAY
Decompose the agent, give each stage a guarantee, and route work to the cheapest model.

### RECOMMENDATIONS
- Build a diffing agent that generates diffs, applies them per file, then validates in a loop.
- Replace LLM syntax checking with ast.parse, feeding only the pinpointed error line back for a repair.
- Detect imports by walking the AST, then auto-install packages instead of running code to discover them.
- Rewrite failed correction turns out of context so downstream steps only see a clean successful trajectory.
- Start your whole pipeline on GPT-4o, then swap the expensive applied-diff step onto smaller models first.
- Reframe every "do not" prompt instruction into a positive capability the model can act on directly.
- Ask the model to emit code as triple-backtick multi-line strings rather than JSON-escaped string fields entirely.
- Build separate systems for new-code generation and existing-code editing, connected by a simple routing decision layer.
- When building a coding tool, invest in UX that makes users hand you the right context.
- Abort an edit and log an observation when no reliable match exists, rather than forcing output.
