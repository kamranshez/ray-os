---
title: Can You Outsmart the Model Makers?
videoId: h99bTZTR_IU
url: https://www.youtube.com/watch?v=h99bTZTR_IU
date: 2026-07-01
status: posted
show: AI That Works (Boundary / BAML + HumanLayer)
---

## The one idea worth a video

**1. The harness has no moat: because the agent runs on your machine over an observable API, you can always reverse-engineer a lab's tool shapes and out-think its harness.** The whole "should I build a harness" debate collapses once you see the model call is observable and copyable, which subsumes the proxy, the binary-disassembly, and the system-prompt-leak beats.
VERDICT: net-new video available.

**2. Post-training welds a model to one exact tool schema, so matching (or deliberately mismatching) your tool definitions to the model is a real, measurable performance lever.** Explains why GPT-5 degrades in Claude Code's harness, why the 0.01%-per-call penalty compounds, and why a schema-aware library can beat the raw model on recursive types.
VERDICT: net-new video available.

**3. Outer-harness orchestration is just stacking while-loops: each loop that carries more information than the one inside it makes the inner loop perform better, and your job is to always build the next loop.** Reframes RPI, goal mode, and orchestrators as one repeatable move.
VERDICT: next-step video available (complements the existing test-time-compute video).

---

## Summary

Vaibhav (Boundary/BAML) and Dexter (HumanLayer) debate whether building custom agent harnesses beats the labs, covering post-training, tool-call shapes, observability, benchmarks, and stacking orchestration loops together.

Counts (one tally per promoted spine):
🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: The harness has no moat

**The claim.** Building your own coding harness is worth it, because no model lab can permanently own the harness layer: the agent runs on the user's machine and talks to the model over the same observable API everyone else uses. **Why it's non-obvious.** Ryan LaPopolo's widely-shared take is the opposite, that alternative harnesses get "bitter lessoned away," so be bearish on any harness not from your model's lab, because you are fighting post-training. That sounds authoritative. **Why it's true.** Vaibhav's counter is that this is a software question, not a model question. Because the harness must run where your files and shell live, and because you are billed on API usage, at some point the exact request to the model is exposed. You can proxy it, read the tool shapes, even disassemble the binary (models now do this trivially). Any alpha a lab bakes into its harness is immediately observable and copyable, so "you think, then they big think" for far less money. **What it generalizes to.** Performance engineering: every new Nvidia GPU instruction is an invitation to rewrite your kernel and beat your old system; new models are the same invitation. **How it goes wrong.** Labs can gate specific tool calls to their own harness or fingerprint-block clones (the OpenClaw cat-and-mouse), producing a permanent false-positive tax rather than a real moat.

### Spine 2: Match the tool shape to the model

**The claim.** Post-training welds a model to one exact tool schema, so matching (or deliberately mismatching) your tool definitions to the model is a real, measurable performance lever. **Why it's non-obvious.** People assume a frontier model is generally good at "tool calling," so any reasonable schema should work. It does work, just slightly worse, and the penalty hides in aggregate. **Why it's true.** Labs post-train on a specific edit-tool shape (Claude Code's old-string / new-string) because SweBench rewards calling that tool correctly the first time without wasting context on retries. Swap in a foreign shape and each call loses maybe 0.01% accuracy; run 50 to 500 tool calls in one coding task and it compounds fast. Put GPT-5, post-trained on apply-patch, inside Claude Code's edit harness and performance drops. **What it generalizes to.** The inverse: for complex recursive types or discriminated unions the Anthropic API cannot even express, a schema-aware library like BAML can beat the raw model, because there is little training data for exotic shapes. **How it goes wrong.** "Terrible" overstates it; these are strong general-purpose machines, so mismatch is a slight compounding tax, not a cliff, and it is easy to misattribute to the model.

### Spine 3: Software is stacking while-loops

**The claim.** Outer-harness orchestration is just stacking while-loops: each loop you wrap around the agent that carries more information than the loop inside it makes that inner loop perform better, and your real job is to always build the next loop. **Why it's non-obvious.** People chase the perfect single agent or the perfect prompt; the speakers say the unit of progress is the loop, not the prompt, and it never stops at one. **Why it's true.** An inner agent loop that must infer the whole process performs worse than one wrapped by an outer loop that already knows "we are doing a research-plan-implement process." The outer loop constrains and informs, so the inner loop does less and succeeds more; add another loop with still more context (goal mode, an orchestrator fanning out goals) and you climb again. **What it generalizes to.** Ralph Wiggum / goal mode: a hundred lines of Python that generates goals, then fans out and completes them, is "one more loop on top." **How it goes wrong.** Each added loop is often only ~100 lines with no moat, so alpha is real but not defensible, and stacking loops indefinitely trades simplicity for coordination cost.

---

## 🎬 Proposed ACS videos

### 1. Match the Tool Shape or Pay the Compounding Tax
- HOOK: Put GPT-5 inside Claude Code and it gets worse, and the reason is not the model.
- THE PROMISE: For anyone building or swapping harnesses, learn to read the exact tool schema a model was post-trained on and match it, instead of blaming the model when accuracy quietly drops.
- THE SHAPE:
  1. Put a proxy between your coding agent and the API and capture the outgoing call.
  2. Show the edit tool's old-string / new-string shape versus ChatGPT's patch / diff shape.
  3. Route a mismatched model through the harness and watch the 0.01%-per-call penalty compound over hundreds of calls.
  4. Flip it: use a schema-aware layer (BAML) to beat the raw model on a recursive type.
  5. Rule of thumb: match the native shape, keep custom tools flat.
- SPINE: 2 (Match the tool shape to the model).
- SLOT: Techniques class > new "Harness Internals" chapter.
- RELATIONSHIP: ❌ net-new. Nothing in the catalog covers proxying an agent to extract tool schemas, tool-shape / model matching, or beating a model on recursive types; the nearest backlog titles (task-shaped-wrappers, designing-interfaces) are bare titles with no script and a different angle.
- PROOF TO REUSE: "if you switched new string and old string. That might impact your performance by 0.01% per call"; "if you're doing like 50 tool calls ... it compounds real freaking fast"; "The reason why Claude code works is cuz the tools that are the core of it read write edit bash are damn simple. There is no nested object."

### 2. The Harness Has No Moat (And Why That's Good for You)
- HOOK: A lab told you your harness will be "bitter lessoned away." Here is why that is wrong.
- THE PROMISE: For builders deciding whether to invest in a custom harness, get the mental model that the harness layer is un-ownable, so you can confidently keep out-thinking the lab's harness release after release.
- THE SHAPE:
  1. State Ryan LaPopolo's bitter-lesson claim, then the counter: this is a software problem, not a model problem.
  2. Prove observability live: proxy the agent, capture the request, note you are billed on it so it cannot be hidden.
  3. Show disassembly and system-prompt leaks as the backstop (Devin, Vercel, Cognition all leaked).
  4. The performance-engineering analogy: every new GPU (model) is an invitation to rewrite and win.
  5. The limit: labs can fingerprint-block clones (OpenClaw), a tax not a moat.
- SPINE: 1 (The harness has no moat).
- SLOT: Claude Code class > agent-harness-concept (currently a bare backlog title with no script).
- RELATIONSHIP: ❌ net-new. The agent-harness-concept slot is only a planned title; nothing teaches the "observable API, no durable lab moat" reframe or the bitter-lesson rebuttal.
- PROOF TO REUSE: "while alternative coding harnesses may have short-term lift, they will be bitter lessoned away ... You're fighting against post training"; "How are they going to ban you from seeing your own API calls"; "you think and then they big think ... they spend way less money."

### 3. Software Is Just Stacking While Loops
- HOOK: Your job is not to build one agent loop. It is to always build the next one.
- THE PROMISE: For anyone orchestrating agents, learn to layer loops so each outer loop feeds the inner one more context, which makes the inner loop do less and succeed more.
- THE SHAPE:
  1. Start with the raw agent loop, then wrap it in a research-plan-implement outer loop.
  2. Show the inner loop performing better because the outer loop already knows the process.
  3. Add a third loop: goal mode / an orchestrator that generates goals and fans them out.
  4. Name the pattern: whichever loop carries more information wins.
  5. Caveat: each loop is ~100 lines and has no moat, so keep building the next one.
- SPINE: 3 (Software is stacking while-loops).
- SLOT: Techniques class > Multi-Agent Orchestration (alongside test-time-compute).
- RELATIONSHIP: 🔗 complements "test-time-compute" (Techniques > Multi-Agent Orchestration), which already teaches loops as one of four compute knobs ("a loop turns it up over time" / "use a workflow"). This video adds the distinct move it does not cover: an outer loop that injects MORE information so the inner loop does LESS, and the "always build the next loop" framing. Do not re-teach the compute-knob framing.
- PROOF TO REUSE: "Your job is not to build any one while loop. Your job is to always build the next while loop"; the RPI loop "is a while loop that has more information than the one inside of it"; "Codex is a goal mode now, which is kind of Ralph Wiggum mode."

### Also film-able (not deep-dived)
- **Token-wise tool calling and why your tools should be flat.** Labs post-train special tokens (old-code, new-code, done) so models emit code without JSON-escaping it, which is still grammar enforcement, just not JSON-shaped. Actionable takeaway: keep custom tools flat (read/write/edit/bash), never hand agents deeply nested or recursive schemas. One-line pitch: "Why Claude Code's tools have no nested objects, and what that means for the tools you write." Rough slot: Techniques > tool / interface design (near the designing-interfaces backlog title). Net-new; edged out of the top three because its most actionable core overlaps Spine 2's flat-tools point.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (Boundary/BAML) and Dexter (HumanLayer) debate whether building custom agent harnesses beats the labs, covering post-training, tool-call shapes, observability, benchmarks, and stacking orchestration loops together.

### IDEAS
- The fastest way to learn harness engineering is cloning Codex and OpenCode, then rebuilding one better.
- To learn a feature, clone a repo demonstrating it and have Claude explain every design decision.
- Ryan LaPopolo argues alternative harnesses get bitter-lessoned away; be bearish on harnesses outside your model's lab.
- Labs cannot own harness alpha because the agent runs on your machine over an observable API.
- Proxying between Claude Code and the API reveals the edit tool's exact old-string, new-string call shape.
- Post-training welds a model to one tool schema; a mismatched shape costs roughly 0.01% per call.
- That tiny per-call penalty compounds fast across fifty to five hundred tool calls in one task.
- Running GPT-5 inside Claude Code's harness degrades performance because it was post-trained on apply-patch, not edit.
- Claude Code's edit tool differs from ChatGPT's patch tool, which looks like a long git-diff string.
- You can beat models at tool calling for complex recursive types by not assuming JSON shape.
- Recursive data types and discriminated unions are hard; the Anthropic API does not support discriminated unions.
- Labs post-train special tokens like old-code and new-code so models output code without JSON-escaping it constantly.
- Token-wise tool calling is still grammar enforcement, just not JSON-shaped, using special start and end tokens.
- Claude Code works because its core tools, read, write, edit, and bash, contain no nested objects.
- Opus 4.7 in Claude Code starts at 50,000 tokens: 32,000 tokens of tools, 10,000 system prompt.
- SweBench started as Django-only tasks; SweBench verified are human-reviewed PRs; multilingual spans Java, Go, and C.
- RL environments check out pre-PR code, ask the agent to fix it, then score with verifiers.
- Reward functions score test-correctness but also penalize extra lines of code and total token cost too.
- Software is stacking while-loops: each outer loop carrying more information makes the inner loop perform better.
- Anthropic blocked OpenClaw users by system prompt, then by scanning recent git history for telltale commits.
- Opus 4.7 and Codex now hide raw tool traces, keeping the reasoning-trace alpha to themselves entirely.

### INSIGHTS
- Harness alpha is a software problem, not a model problem, so labs hold no durable advantage.
- Whoever controls the machine controls observability; user-run code can always sniff the outgoing model API call.
- Model quality is a curve; post-training reshapes the tail for tasks with abundant labeled training data.
- Tool-shape matching is a real performance lever because post-training bakes one specific schema into the model.
- Simpler tool shapes have more training data, so flat tools beat nested recursive schemas for reliability.
- Every new model release is an optimization opportunity, mirroring how new GPUs force rewriting performance-critical software.
- You can context-engineer models faster than labs ship new ones, so the arbitrage window stays open.
- Keeping models updated and A/B tested is now a permanent devops layer requiring evals to manage.
- The durable engineering skill is applying fundamentals to new problems repeatedly, not memorizing one stable stack.
- Lab engineers building harnesses are just like you, holding only mild information arbitrage about upcoming releases.

### QUOTES
- Vaibhav: "the worst harness in the world is just go low prompting a model."
- Ryan LaPopolo (read by Vaibhav): "while alternative coding harnesses may have short-term lift, they will be bitter lessoned away. I am bearish on any harness that doesn't come from the lab whose model you were using. You're fighting against post training."
- Vaibhav: "The reason why Claude code works is cuz the tools that are the core of it read write edit bash are damn simple. There is no nested object in there."
- Vaibhav: "you think and then they big think."
- Vaibhav: "Your job is not to build any one while loop. Your job is to always build the next while loop."
- Vaibhav: "How are they going to ban you from seeing your own API calls"
- Vaibhav: "you can context engineer the models faster than the labs can release a new model every 6 months."
- Vaibhav: "Your skill set is your ability to understand core concepts and reapply them over and over and over again."
- Vaibhav: "once you start selling to a large number of people, you will leak your system prompt. It's an inevitability."
- Dexter: "if you're doing like 50 tool calls because you're doing a coding agent task, it compounds real freaking fast."
- Vaibhav: "This is also a form of grammar enforcement ... It's just a special kind of grammar enforcement that is not JSON compliant."
- Dexter: "make a thing that makes people's lives easier, that solves their problem, that they're willing to pay you money for."

### HABITS
- Vaibhav learns new features by cloning an exemplar repo and letting Claude explain every design decision.
- They routinely put a proxy between Claude Code and the LLM to inspect outgoing tool calls.
- Vaibhav picks models lazily, defaulting to whichever model he used last unless his context runs out.
- When context runs low, Vaibhav upgrades to the one-million-token window in whatever model he is using.
- Dexter uses GPT-5.5 on low mode for pre-planned work, reserving Claude for human-readable strategy plans instead.
- They prompt agents explicitly to do the right refactor every time rather than minimizing entropy changes.
- To master harness engineering they clone Codex and OpenCode and rebuild something that beats them once.
- They test every new model against their product to see if it lifts customer value meaningfully.

### FACTS
- The original SweBench benchmark consisted solely of tasks drawn from the Django Python repository's past PRs.
- SweBench verified filtered thousands of PRs down to human-validated tasks confirmed solvable and well-specified for models.
- SweBench multilingual extends the benchmark across languages including Java, Go, and C beyond the original Python.
- The Anthropic API does not support discriminated unions, complicating structured recursive tool-call outputs for developers today.
- Claude Code's edit tool uses old-string and new-string parameters; ChatGPT's patch tool uses a diff-like format.
- Opus 4.7 in Claude Code consumes roughly 32,000 tokens of tools plus 10,000 system prompt tokens.
- Anthropic's Opus 4.7 stopped exposing raw tool traces, showing only summarized thinking to end users now.
- Anthropic blocked OpenClaw users first by system-prompt fingerprint, later by scanning recent git commit history patterns.
- Codex now offers a goal mode resembling Ralph Wiggum mode, relaunching context windows until task completion.

### REFERENCES
- Ryan LaPopolo (OpenAI) tweet on harness-engineering hype and the bitter lesson.
- BAML (Boundary's programming language) and DSPy for structured tool calling.
- Codex (OpenAI CLI), OpenCode / "pi", Claude Code as reference harnesses.
- SweBench, SweBench verified, SweBench multilingual, Terminal Bench.
- GRPO and RLHF as post-training methods.
- The Bitter Lesson (Rich Sutton, implied).
- OpenClaw; Devin / Cognition and Vercel system-prompt leaks.
- Calvin (Codex launch OG); Mejiro (suggested guest on CodeRL); Ben Davis (GPT-5.5 reasoning efforts).
- Ralph Wiggum mode / Codex goal mode; RPI loop; "bees and gas town" orchestration loops.
- HumanLayer, Boundary, and the "AI That Works" show.

### ONE-SENTENCE TAKEAWAY
Harness alpha stays with whoever out-thinks the observable API fastest, not the model's home lab.

### RECOMMENDATIONS
- Clone Codex and OpenCode, then build a harness that beats them at one specific narrow task.
- Put a proxy between your coding agent and the API to read its exact tool calls.
- Match your tool definitions to the model's native post-trained schema before blaming the model for failures.
- Keep custom tools flat and simple, avoiding nested objects and recursive types the model calls poorly.
- To learn any feature, clone an exemplar repo and have the agent walk every design decision.
- Build a custom harness for your team's known long-running workflow, where general harnesses lack training data.
- Add an outer while-loop carrying more context, so the inner agent loop can do less work.
- Test every new model release against your product and swap it in when it lifts value.
- Write evals so you can objectively A/B test whether a new model improves your outputs measurably.
