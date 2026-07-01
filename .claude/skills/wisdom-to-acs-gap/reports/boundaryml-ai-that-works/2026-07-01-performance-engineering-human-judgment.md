---
title: Why Performance Engineering Still Requires Human Judgment | No Vibes Allowed
videoId: mm6n4n09RaU
url: https://www.youtube.com/watch?v=mm6n4n09RaU
date: 2026-07-01
status: posted
---

# The one idea worth a video

**1. Performance engineering is really a data-driven feedback loop, and the exact same loop is how you should profile an AI agent.** Before you optimize anything you build representative workloads, measure with standard deviations, and serialize the results to JSON so the agent re-reads data instead of rerunning slow suites.
VERDICT: 🔗 next-step video available (complements "Closing the Loop").

**2. In high-risk agentic work the model reliably ships one or two subtly wrong sentences, and reading every line to catch them is the whole job.** Because performance is unfakeable pure numbers, the failure surfaces as "it's just not faster," which is exactly what forces the careful reading that makes you better at agents.
VERDICT: 🔗 next-step video available (complements "What Breaks If I Change This?").

**3. Do more research than work: clone the real source-of-truth codebases locally and make the agent study them before it designs.** Vaibhav keeps entire CPython and V8 trees on disk because "nothing is better than the source of truth," and offloads the learning so he only judges trade-offs.
VERDICT: ❌ net-new video available.

---

# Summary

Vaibhav Gupta and Dexter Horthy code live in No Vibes Allowed, showing how to drive Claude through high-performance engineering on the BAML virtual machine responsibly.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

**Spine 1 - Measure first, then the loop is reusable on your agent.**
The claim: performance engineering is not primarily about speed, it is about standing up a good data-driven feedback loop, and that loop is how you should profile an AI agent too. Most people picture clever bit tricks; Vaibhav's actual first move is infrastructure. The mechanism runs in steps: an optimization only means something relative to a baseline, so you need representative "workloads" (Fibonacci recursive and iterative, tree traversal, closures, nested loops) and standard deviations, or you "end up with a loop that has no usage" and cannot tell a real win from noise. Then you serialize every result to JSON by default, because his benchmarks take two-to-three minutes and Claude's iteration loop "completely dies" waiting; cached JSON lets the agent re-read instead of rerun. It generalizes cleanly to a second domain he names outright: profile your AI agent as a black-box workload, measuring cost, tool-call turns, and user turns rather than wall-clock time. How it goes wrong: you cannot run benchmarks in parallel because competing workloads corrupt the CPU profiling, so real isolation needs dedicated hardware.

**Spine 2 - The human's job is catching the one wrong line.**
The claim: in high-risk agentic work the model ships one or two subtly wrong sentences, and catching them by reading every line is the entire job. The non-obvious part is that AI is "incredibly bad at making really good performance engineering decisions by default," precisely because performance is "the act of doing things that are usually dangerous and not very safe." The mechanism: a single hardcoded constant, or the model's quiet decision to "only track 12 call stacks" and truncate the rest, silently makes the result "foundationally incorrect"; recursive JSON serialization alone hits fifty-to-two-hundred frames. Because performance is unfakeable pure numbers, the bug does not hide behind a plausible metric, it shows up as "it's just not faster," which forces the reading. This generalizes to any unfakeable-but-fragile domain: data races, seg-faults, migrations, security. There is an inverse gift here too, which is why performance work is the best gym for agentic skill: the feedback on your own prompting is measurable. How it goes wrong: you cannot read everything, so you must know which few things break everything, and priming the model earns trust you must still spend carefully.

**Spine 3 - Research first, from the real source of truth.**
The claim: do far more research than work, and ground that research in the actual implementation code, not documentation. Vaibhav keeps repos/CPython and repos/V8 fully cloned on disk and says plainly, "even though V8 is well documented, nothing is better than the source of truth." The mechanism: before writing anything he has Claude research every Rust optimization crate he does not already know, the memory layout, the clone cost, the worst string offenders, and exactly how V8 and Python implement string optimizations, then produce "a giant table of all the possible things that we should do." That research offloads the learning so he "doesn't even have to make decisions," only judge the trade-offs, and it lets him confirm a design (single-allocated immutable strings, deferred concatenation, the lazy hash copied from V8) against how the greats actually do it. It generalizes to adopting any unfamiliar library or protocol: point the agent at the implementation, not the changelog. How it goes wrong: the model sometimes "refuses to look" and must be forced, and copied designs need adapting because BAML has true virtual threads that neither V8 nor Python has.

---

# 🎬 Proposed ACS videos

## 1. Measure Before You Optimize: Build the Agent's Feedback Loop
- TITLE: Measure Before You Optimize: Build the Agent's Feedback Loop
- HOOK: Your agent cannot make anything faster until you give it numbers it can trust.
- THE PROMISE: For anyone optimizing code or an agent, you will leave able to build a workload-based benchmark harness, with standard deviations, that the agent reads instead of reruns.
- THE SHAPE:
  1. The trap: optimizing by vibe, where "it's not faster" is the only feedback and it arrives too late.
  2. Build representative workloads (not a single Fibonacci), and add standard deviations so you can see noise.
  3. Serialize every run to JSON by default so Claude re-reads data instead of rerunning a three-minute suite.
  4. Isolation matters: you cannot benchmark in parallel because workloads corrupt each other's CPU profiling.
  5. The generalization demo: point the same loop at an AI agent, measuring cost, tool-call turns, and user turns.
- SPINE: 1
- SLOT: Context Engineering > Measurement and Evals (or Techniques)
- RELATIONSHIP: 🔗 complements "Closing the Loop", which teaches building a verification loop so the agent self-corrects. This adds the missing substrate beneath that loop, the representative workloads, standard deviations, and JSON serialization, and reframes it as profiling your own agent. Do not re-teach the general "give the agent a way to check itself" idea.
- PROOF TO REUSE: The workload list (Fibonacci recursive vs iterative, tree traversal, closures, nested loops); "if you don't have standard deviations, then you can't possibly measure exactly how much noise you have"; the JSON-by-default learning; "build a benchmark suite that helps you profile the workload of your AI agent."

## 2. Point the Agent at the Source of Truth
- TITLE: Point the Agent at the Source of Truth
- HOOK: Stop letting the model guess from documentation. Put the real implementation on its disk.
- THE PROMISE: For engineers working in unfamiliar territory, you will learn to clone the real reference codebases locally and make the agent research them into a decision table before it writes a line.
- THE SHAPE:
  1. The default failure: the agent invents an approach from its weights and half-remembered docs.
  2. Clone the ground truth (CPython, V8, a library you are integrating) so the agent reads implementation, not changelog.
  3. Make it research broadly: every optimization crate, memory layouts, clone costs, the worst offenders.
  4. Force it when it refuses, then have it produce a giant table of options to choose from.
  5. Judge trade-offs, do not learn everything: the research offloads learning so you only pick.
- SPINE: 3
- SLOT: Context Engineering > Grounding and Research
- RELATIONSHIP: ❌ net-new. The catalog has no video on cloning source-of-truth codebases locally as the agent's research ground; the nearest neighbour, "Test-Time Compute", spends compute on research in general but never grounds it in real reference implementations you keep on disk. (Context Engineering shipped thirteen videos whose titles were not fully enumerated in the inventory, so re-confirm before filming.)
- PROOF TO REUSE: "nothing is better than the source of truth"; the repos/CPython and repos/V8 setup; "I don't even have to make decisions... all I have to do is go understand what are the trade-offs"; the model "refused to look at V8 and Python" until forced.

## 3. Catch the One Wrong Line: Human Judgment in Unfakeable Work
- TITLE: Catch the One Wrong Line: Human Judgment in Unfakeable Work
- HOOK: The model will hand you fast, confident, consistent code that is quietly, foundationally wrong.
- THE PROMISE: For anyone shipping high-risk changes with an agent, you will learn which few lines to read and why performance work is the best gym for that judgment.
- THE SHAPE:
  1. Why AI is bad at this by default: performance means doing dangerous, unsafe things for the last ounce.
  2. The failure pattern: one hardcoded constant, or "truncate call stacks at 12", breaks everything downstream.
  3. Prime the model on the governing principle (think about allocations), then trust selectively.
  4. Read the few load-bearing lines; you do not need to understand every detail.
  5. Why it trains you: unfakeable numbers give honest feedback on your own upstream prompting.
- SPINE: 2
- SLOT: Techniques > Reading and Verification
- RELATIONSHIP: 🔗 complements "What Breaks If I Change This?", which teaches asking the agent to diagram a change's blast radius before you commit. This is the after-the-change discipline: reading the diff line by line to catch the model's one subtly wrong sentence in a domain where numbers cannot lie. Do not re-teach blast-radius diagramming.
- PROOF TO REUSE: "one late night prompt is the difference between good and bad"; the truncate-at-12-call-stacks bug ("12 is enough for 99% of animal stacks... It's not enough"); "the worst things you can do with your tokens is spend a lot of tokens generating wrong code"; "performance engineering is a great way to force yourself to read stuff because everything is measurable."

Also film-able (not deep-dived):
- **Three isolated design discussions in three worktrees for competing approaches** (Habit): distinct from parallel execution because you cannot benchmark in parallel; likely 🟡 partial against the in-progress "Worktrees" video.
- **Inline HTML mockups to align mental models during design** (the memory-layout and design-evolution diagrams): likely ✅/🟡 against "What Breaks If I Change This?" and V24 "Interactive Artifacts", so it rides as a beat, not its own video.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav Gupta and Dexter Horthy code live in No Vibes Allowed, showing how to drive Claude through high-performance engineering on the BAML virtual machine responsibly.

## IDEAS
- Performance engineering is unfakeable pure numbers, so no metric lets you pretend something got slightly better.
- AI makes terrible performance decisions by default because the fastest optimizations are inherently dangerous and unsafe.
- The only three real performance levers are: use more caches, do less work, allocate less heap.
- Vaibhav made BAML strings roughly six times faster at heavy concatenation by drastically reducing memory allocations.
- Short strings live on the stack while big strings, slices, and concatenations each use different representations.
- A concatenation defers work: it just points at two strings until access forces one allocated string.
- Slices store a pointer, offset, and length instead of copying characters out of the parent string.
- The lazy hash trick, copied directly from V8, turns repeated string hashing from O(n) into O(1).
- Benchmarks lacking standard deviations cannot separate a real improvement from ordinary measurement noise in your system.
- You cannot run performance benchmarks in parallel because competing workloads corrupt each other's CPU profiling numbers.
- Vaibhav keeps entire CPython and V8 source trees cloned locally as the ground truth for research.
- He deliberately does more research than work, letting Claude study crates, memory layouts, and clone costs.
- Claude truncated call-stack tracking at twelve frames, yet recursive JSON serialization easily reaches hundreds of frames.
- Python replaces the call instruction with an instrumented version for tracing, adding roughly a hundredfold slowdown.
- JavaScript's V8 profiles via a sampling thread probing the call stack every millisecond, missing some functions.
- BAML's multi-threaded virtual threads break the single-threaded profiling assumptions inherited from both Python and V8 designs.
- Claude Code learned to summarize his benchmark tables just by grepping for the vertical bar character.

## INSIGHTS
- Performance engineering is fundamentally a good data-driven feedback loop, not merely the pursuit of raw speed.
- Because output is measurable, performance work forces the careful reading that makes you better at agents.
- Models are superb data reformatters, rotating patterns from huge reference codebases into your specific target codebase.
- A single subtly wrong sentence from the model can quietly make the entire result foundationally incorrect.
- Best token spend is few tokens on right code; worst is many tokens on wrong code.
- Priming the model to think about allocations first earns you justified trust in its later reasoning.
- Reading the source of truth beats documentation: nothing explains behavior better than the actual implementation code.
- You need not understand every detail, only reliably catch the few key things that break everything.
- Long context is worth slow generation because rediscovering the whole system each turn is far costlier.

## QUOTES
- "It's like one late night prompt is the difference between good and bad." - Dexter Horthy
- "performance engineering is one of the few things that you cannot fake... It's pure numbers. It's totally unfakeable." - Vaibhav Gupta
- "the worst things you can do with your tokens is spend a lot of tokens generating wrong code." - Vaibhav Gupta
- "nothing is better than the source of truth." - Vaibhav Gupta
- "You have to read lines extremely carefully." - Vaibhav Gupta
- "agents are just like data reformatters." - Dexter Horthy
- "the key to doing hard [stuff] with LLMs is like how can you maximize your alignment with the LLM." - Dexter Horthy
- "I wish we had a model that was like maybe like 20% dumber, but like 100% faster." - Vaibhav Gupta
- "12 is enough for 99% of animal stacks... It's not enough." - Vaibhav Gupta
- "now that I've primed it to think about allocations, I trust this." - Vaibhav Gupta

## HABITS
- He saves every benchmark result to JSON by default so Claude re-reads data instead of rerunning.
- He reads every single line of the sensitive code snippets the agent produces during performance work.
- He runs a deliberately long design stage, hunting the model's bugs before any real implementation begins.
- He watches specifically for hardcoded variables because a single missed constant corrupts all downstream performance verification.
- He spins up three separate worktrees and workspaces for competing designs, avoiding cross-contamination between the approaches.
- He feeds the finished design doc back into the research prompt and iterates with it longer.
- He rewrites the ticket from scratch repeatedly until one is clean enough to seed real work.
- He always asks Claude to research state-of-the-art implementations so he avoids reinventing known optimizations from scratch.

## FACTS
- A virtual machine executes a fetch, decode, execute, and store cycle, like Python's and JavaScript's runtimes.
- Python uses a global interpreter lock, whereas V8 runs a single event loop on one worker.
- Python's tracing rewrites the call opcode at runtime, giving rich line-level detail but a hundredfold slowdown.
- V8's sampling profiler probes the call stack roughly every single millisecond using a separate, safe thread.
- Neither V8 nor Python has true threading, so both profilers assume a purely single-threaded execution model.
- Hashing a large string is an O(n) operation, but storing the hash makes later comparisons O(1).
- BAML's optimized strings now run roughly thirty percent faster than Bun's JIT-compiled JavaScript version does today.
- A machine stack can hold around fifty thousand elements, but filling it blows out the cache.
- Tail-call optimization reuses the current stack frame instead of allocating a new one per recursive call.

## REFERENCES
- BAML (BoundaryML virtual machine), the codebase under optimization.
- Claude and Claude Code, the coding agent used throughout.
- CPython source repository, cloned locally as ground truth.
- V8 source repository, cloned locally as ground truth.
- Bun, Node, Python, JavaScript/TypeScript, Java/JVM (benchmark comparison targets).
- Lua, referenced for interesting optimization approaches.
- Rust and its optimization crates; LLVM (a bug in it changed a data-structure choice).
- perf, the Linux profiling tool, and Python trampolining to attach to it.
- 12-factor agents (Dexter Horthy) and the "agents as data reformatters" framing.
- Jarred Sumner / Bun, cited for still reading many PRs.
- Excalidraw; inline HTML mockup feature; Codex 5.5 low; SWE-bench.
- No Vibes Allowed, the recurring live-coding series.

## ONE-SENTENCE TAKEAWAY
In unfakeable performance work, your judgment catching the model's one wrong line still decides everything.

## RECOMMENDATIONS
- Build a benchmark suite of representative workloads before optimizing anything, and always report their standard deviations.
- Serialize benchmark results to JSON by default so your agent re-reads data without rerunning slow suites.
- Clone the real source-of-truth codebases locally and make the agent study them thoroughly before designing anything.
- Read every line of the high-risk code the agent writes; never trust any unread performance-critical changes.
- Prime the model with the governing principle first, then judge its later decisions with justified confidence.
- Watch specifically for hardcoded constants and truncated limits, the small assumptions that silently break performance downstream.
- For three competing ideas, run three isolated design discussions in separate worktrees rather than blending them.
- Practice agentic engineering by optimizing one real hot path in your own system, not toy problems.
- Profile your own AI agent itself: measure cost, tool-call turns, and user turns as performance metrics.
