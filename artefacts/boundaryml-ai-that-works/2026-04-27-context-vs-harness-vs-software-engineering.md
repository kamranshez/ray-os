---
title: Context Engineering vs Harness Engineering vs Software Engineering
videoId: gX9WpYY61xA
url: https://www.youtube.com/watch?v=gX9WpYY61xA
date: 2026-07-01
status: posted
channel: BoundaryML - AI That Works
---

## The one idea worth a video

**Spine A: Models are RL'd onto one specific tool schema, so the leverage move is reshaping your tools to look like the primitives the model already masters, not fine-tuning.** The labs burned a huge chunk of the weights teaching Claude Code old-string/new-string edits and Codex apply-patch diffs; reliability lives in the schema, not raw IQ, so mimic the schema and inherit it for free.
VERDICT: ❌ net-new video available

**Spine B: Treat the frontier lab's RL'd model as a compiler, and only handwrite your own harness where you have real alpha and need near-perfect accuracy, eval first.** Beating a 50-person team that evals Claude Code daily is like beating the compiler by handwriting assembly: possible only when you know something about your data it cannot generalize, and only worth it above 90%.
VERDICT: ❌ net-new video available

**Spine C: An agent, a harness, a sub-agent, and an orchestrator are the same primitive, a while loop, and harness engineering means configuring the harness you are given, not building one.** Swap the LLM call for a Claude Code call and the architecture does not change; each nested loop adds one abstraction level because the layer below does more autonomous work.
VERDICT: 🔗 next-step video available

---

## Summary + counts

BoundaryML's AI That Works podcast, from AI Engineer Miami, debates harness versus context versus software engineering with LangChain's Viv and harness-builder Jeff, cutting through hype.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine A: Fit your tools to the model's RL'd primitives

The claim: frontier models are reinforcement-learned onto one exact tool interface, so the highest-leverage move is not fine-tuning a model to your tools, it is reshaping your tools and data to look like the primitives the model already masters. Most people get this backwards: when the model fumbles a custom tool, they conclude "the model is bad at tool calling" and reach for a bespoke harness or a fine-tune. The mechanism says otherwise. The labs "took a dedicated a huge chunk of the weights in that model to being able to call these tools really really well," and that specialization does not transfer. Claude models dropped into the Codex harness are "complete trash," while GPT-OSS-120B "can call apply patch really easily" but "has no idea how to" run old-string/new-string. So the tool schema, not intelligence, gates reliability. Therefore if you make your data system present as the file-system read/write/search tools the model is already RL'd on, you inherit that reliability for free and skip training. This generalizes directly to MCP design: instead of inventing an exotic schema for your database, wrap it in file-system-shaped operations. It goes wrong when a task genuinely needs a capability the model never saw, or when file semantics leak on stateful systems.

### Spine B: Beat the compiler

The claim: treat the frontier lab's RL'd model as a compiler, and only handwrite your own harness, compaction, or tool definitions where you have genuine alpha and the task demands near-perfect accuracy, with an eval built first. The harness-engineering hype implies you should always be customizing; the guests argue the opposite default. The mechanism: the model is optimized by "the Frontier Labs like 40-person or 50-person engineering team who's sitting there like evaling Claude code every single day," their compaction team, their tool-definition team. Like a modern compiler it beats you in the general case, and "most people probably can't beat the compiler for most situations, even extreme experts." You only win where you understand something about your own data the general optimizer cannot generalize, exactly like handwriting assembly when you know a cache-locality trick the compiler cannot see. And the payoff only exists when the accuracy delta matters: dragging a financial-regulation or tax-filing flow from 90% to 99.8%. Below that, breaking from the happy path is negative expected value. The gate is always an eval, because "how do you even know you got better?" This generalizes to performance engineering and any "should I optimize this by hand" call. It fails when people overestimate their alpha, or overfit without production data.

### Spine C: It is while loops all the way down

The claim: an agent, a harness, a sub-agent, and an orchestrator are the same primitive, a while loop, and harness engineering means bringing systems discipline to the configuration surface of the harness plus model you already have, not building a harness from scratch. The hype frames harness engineering as "build your own harness"; the reframe is that you almost never do, you configure the given one, and the whole stack is one recursive primitive. The mechanism: the 2024 agent was a while loop calling an LLM with tools; Claude Code just swapped the LLM call for a batteries-included call (auto CLAUDE.md load, compaction, MCPs, skills), and "the architecture fundamentally doesn't change." Nest a while loop inside a tool and you get sub-agents ("disposable heaps in memory"); wrap a bash while-true loop around Claude Code and you get an orchestrator, Ralph, then Gas Town. Each nesting adds one abstraction level "because the thing underneath me is doing more work." So harness engineering is deciding which skills, system prompt, context, and MCPs to inject into the given surface. This generalizes via the Shadcn-versus-Tailwind analogy: composed components you still reach in and tweak, all built off one primitive. It goes wrong when "just add another while loop" hides that the details at each layer matter enormously; exhaust the inner loop before adding an outer one.

---

## 🎬 Proposed ACS videos

### 1. Stop Fine-Tuning: Make Your Tools Look Like the Ones Claude Already Knows

HOOK: Claude models dropped into the Codex harness are "complete trash," not because they got dumber, but because one tool changed shape.
THE PROMISE: For anyone building MCPs or custom tools, you will leave designing tools the model already masters instead of fighting it with a fine-tune.
THE SHAPE:
- Put Claude Code's old-string/new-string edit next to Codex's apply-patch diff, side by side.
- Demo the cross-harness failure: GPT-OSS-120B nails apply-patch, cannot run old-string/new-string.
- Explain RL burns weights onto one schema, so reliability is the schema, not IQ.
- Reframe: expose your database or data layer as file-system-shaped read/write/search tools.
- Rule of thumb: mimic the primitives the model was trained on, skip the fine-tune.
SPINE: A
SLOT: Claude Code > agent-harness-concept (or a new "Designing Tools and MCPs" chapter)
RELATIONSHIP: ❌ net-new. Nothing in the catalog covers models being RL'd onto a specific tool schema or designing your tools to match what the model already masters.
PROOF TO REUSE: "if you try to use cloud code models in the Codex harness, it's complete trash"; "GPT OSS 120B can call apply patch really easily. It cannot run an old string new string"; "make your thing fit into the tool set the model already is really freaking good at using."

### 2. Beat the Compiler: When to Override Claude Code (and When Not To)

HOOK: A 50-person team evals Claude Code every single day. That is the compiler. Do you actually have alpha over it?
THE PROMISE: For builders tempted to hand-roll compaction or a custom harness, a three-part test for when customizing pays off and when it is wasted effort.
THE SHAPE:
- The compiler analogy: frontier RL model is the compiler, a custom harness is handwritten assembly.
- Most people cannot beat the compiler, even experts, so default to the happy path.
- The alpha test: do you know something about your data the general model cannot generalize?
- The accuracy test: does this flow actually need 90% to 99.8% (tax filing, financial regulation)?
- The gate: build the eval first, because "how do you even know you got better?"
SPINE: B
SLOT: Techniques > new decision-framework chapter (or Context Engineering strategy)
RELATIONSHIP: ❌ net-new. Adjacent to the filmed "high-level-strategy-low-level-details," but that teaches delegating detail to the agent, not deciding when a human should drop below the model's default and customize.
PROOF TO REUSE: "It's beating the Frontier Labs like 40-person or 50-person engineering team"; "It's time compression over everything else"; "most people probably can't beat the compiler for most situations, even extreme experts"; the cache-locality/assembly metaphor; "And you build an eval for it first."

### 3. Agents, Sub-Agents, Orchestrators: It Is All One While Loop

HOOK: Swap the LLM call for a Claude Code call and the architecture does not change. It is while loops all the way down.
THE PROMISE: For anyone drowning in harness/agent/orchestrator jargon, one mental model that unifies the whole stack and tells you when to add a layer.
THE SHAPE:
- Draw the 2024 agent loop, then swap in Claude Code as the batteries-included loop.
- Nest a loop inside a tool to get sub-agents; wrap a loop around Claude Code to get Ralph, then Gas Town.
- Each nesting adds one abstraction level because the layer below does more autonomous work.
- Use the Shadcn-versus-Tailwind analogy for "engineer on top of what you are given."
- The trap: exhaust the inner loop (prompt, tool design, context) before adding an outer one.
SPINE: C
SLOT: Claude Code > agent-harness-concept and Techniques > core-agent-loop (both planned, unscripted)
RELATIONSHIP: 🔗 complements planned "agent-harness-concept" and "core-agent-loop." Those slots name the concept but have no script yet; this supplies the unifying while-loop model, the inner-versus-outer harness framing, and the "configure what you are given" reframe they would teach.
PROOF TO REUSE: "a harness is just another while loop that happens to have environmental controls"; "Sub agents are really just disposable heaps in memory... they just rebuilt Erlang"; the bash while-true outer-harness example; the Shadcn/Tailwind analogy.

### Also film-able (not deep-dived)

- **Surfing the models / design for deletion.** Design capabilities to be easy to delete because the next model turns them into tech debt; be careful what you expose to users as a product substrate; evals are the durable asset that survives model changes. 🔗 complements the filmed "gravitational-pull-from-older-models" and the to-film "build-it-twice" (throwaway first build); the fresh angle is deletion-readiness driven by model advancement, not spec discovery. Slot: Techniques or Context Engineering strategy. Proof: Dan Shipper's "surfing the models," "you will always be 5 to 10% ahead," "designing so it's easy to delete. That's the skill."
- **Auto-research overfits, so use production traces as your eval.** Auto-research "basically enumerated like 60 if else cases" into the system prompt and will not generalize without real data. 🟡 relates to the filmed "closing-the-loop"; the fresh warning is the overfitting failure mode plus the Google/Facebook "watch the metric at 1% rollout" fix. Slot: Techniques > evals. Proof: "we've just like overfit to the entire eval set"; "Just look at the damn data."

---

## 📚 Full wisdom (reference)

### SUMMARY

BoundaryML's AI That Works podcast, from AI Engineer Miami, debates harness versus context versus software engineering with LangChain's Viv and harness-builder Jeff, cutting through hype.

### IDEAS

- Harness engineering means engineering on top of Claude Code's configuration surface, not building one entirely yourself.
- Agents, sub-agents, and orchestrators are the same primitive: nested while loops, each adding one abstraction layer.
- Models are RL'd onto specific tool schemas: Claude Code learned old-string/new-string, Codex learned the apply-patch format.
- Using Claude models inside the Codex harness is "complete trash"; the tool-calling weights do not transfer.
- GPT-OSS-120B calls apply-patch easily but has no idea how to run Claude Code's old-string/new-string edit tool.
- Instead of fine-tuning, make your data systems mimic the file-system tools the model already really masters.
- The frontier lab's RL'd model is the compiler; handwriting your own harness is like handwriting assembly.
- Only "beat the compiler" when you truly have alpha the general model cannot possibly generalize from.
- Break from the happy path only when going from 90% to 99.8% accuracy matters, like taxes.
- An outer harness can be a dumb bash while-true loop that just reruns Claude Code forever.
- Sub-agents are just disposable heaps in memory; Claude Code effectively rebuilt Erlang's message-passing using file names.
- Dan Shipper's "surfing the models" means redoing context engineering each release to stay 5-10% ahead forever.
- The bitter lesson was coined when code was expensive; auto-research now makes throwaway harness code cheap.
- Design capabilities to be easy to delete because the next model may make them redundant overnight.
- Exposing a capability as a user-facing product substrate hamstrings you when the model absorbs it later.
- Auto-research often overfits: it enumerates sixty if-else cases into the system prompt without generalizing at all.
- Your eval becomes the ultimate deterministic spec; the model rewrites code until the eval finally passes.
- Use production traces as your eval set so the harness fits reality, not a synthetic benchmark.
- The plan tool routes to a different model; Claude Code delegates "is this command safe" checks.
- Shadcn-versus-Tailwind is the analogy: the harness gives components you can still reach in and tweak freely.
- Anthropic hires regular engineers, so you can plausibly out-engineer them on your own narrow problem domain.

### INSIGHTS

- The architecture never really changes; you just swap the LLM call for a Claude Code call.
- Each nested while loop buys abstraction because the layer beneath it autonomously does more real work.
- The details at each stack layer matter so much that "just add loops" advice misleads builders.
- Exhaust system-prompt, tool-design, and context work before adding a second orchestration loop on top of it.
- Coding was never the hard part; designing invariants that survive future features is the real difficulty.
- "Philosophy engineering" is choosing the right metric and eval, not the mere writing of eval code.
- RL builds a general-purpose model; narrow classification RL rarely justifies its cost unless saving real money.
- Locking into loom, Ralph, or Gas Town codifies a worldview the models may soon completely contradict.
- Production data prevents overfitting; without it the eval loop optimizes toward the wrong target entirely undetected.
- Being flexible and refusing to lock in one workflow is currently the most valuable engineering skill.

### QUOTES

- "if you own the harness and you own the model, you do have alpha" (Viv)
- "most people probably can't beat the compiler for most situations, even extreme experts" (Viv)
- "It's time compression over everything else." (Dexter, host)
- "you will always be 5 to 10% ahead." (host)
- "coding is art to me" (Jeff)
- "we're going to have to call this episode philosophy engineering" (host)
- "Just look at the damn thing. Like look at the damn data." (Viv)
- "Sub agents are really just disposable heaps in memory." (Jeff)
- "a harness is just another while loop that happens to have environmental controls" (Viv)
- "No one should fine-tune, in my opinion." (guest)
- "every team that doesn't have an AI code review bot is freaking dumb" (host)
- "The hardest part is picking the part of the code that should be written in assembly." (Viv)

### HABITS

- Add an AI code-review bot to every pull request before doing anything else on your team.
- Grind hard on the system prompt, tool design, and context before adding any orchestration loops whatsoever.
- Build the eval first, before you try to understand or optimize any high-accuracy agent system properly.
- Always look at the actual data instead of telling Claude to just figure it out blindly.
- Read the leaked Claude Code and Codex source to learn context-window recycling and delegation techniques firsthand.
- Watch the metric at rollout; be at your desk when a feature ships to production live.
- Keep trying dumb or futuristic things that feel unlikely to work, because occasionally they actually do.
- Pick one narrow AI topic, go deep for a month, then blog and post it publicly.
- Refuse to lock into one build method; keep making things up and trying different approaches constantly.

### FACTS

- Codex's apply-patch edit format uses git-patch-style plus and minus lines to modify files on disk directly.
- Claude Code's edit tool is essentially find-and-replace taking an old-string span and a new-string replacement value.
- The speaker built his first agent in April 2023, using LangChain to ingest an OpenAPI spec.
- GPT-OSS-120B is an open-weight model that natively calls Codex's apply-patch edit format very easily without training.
- Both the Claude Code and Codex source code have leaked and are publicly readable online now.
- Google and Facebook roll features to one percent of traffic while engineers watch a tied metric.
- Git's core abstraction is so strong it has barely evolved since its original creation in 2005.
- Claude Code's plan tool routes reasoning to a different type of model than the execution model.
- Ralph, the dumbest possible orchestration layer you could build, still works surprisingly well in practice today.

### REFERENCES

LangChain, Claude Code, Codex, GPT-OSS-120B, apply-patch, old-string/new-string edit tool, Ralph / Ralph Loga, Gas Town, Floordcode, loom, Pi (harness-building), auto-research, Dan Shipper ("surfing the models"), Simon Willison, Amazon leadership principle ("leaders are right a lot"), the bitter lesson (Rich Sutton), Steve Yegge, Gary ("skills is the operating system"), Cheng / Preact / React, Git, Unix philosophy, Erlang, Temporal, Tailwind, Shadcn, Code Rabbit (podcast studio and PR review bot), Terminal Bench, AI Engineer Miami, hexagonal architecture / ports and adapters, property-based testing, clean code, SOLID, functors / functional programming, LeetCode data structures.

### ONE-SENTENCE TAKEAWAY

Harness engineering configures the model you're given; override the labs only where you hold alpha.

### RECOMMENDATIONS

- Design your MCP tools to mirror the file-edit primitives the model was already RL'd on heavily.
- Before customizing the harness, ask whether you truly have alpha the frontier model genuinely lacks here.
- Reserve custom compaction and tool definitions for the few flows demanding near-perfect accuracy, like tax filing.
- Start any high-stakes agent project by building the eval loop before touching the system prompt itself.
- Feed production traces into your eval set so you optimize for reality, not synthetic benchmarks alone.
- Learn to draw the tool-calling loop as a sequence diagram and design a tool from scratch.
- Study the leaked Claude Code source to understand context recycling and command-safety delegation to helper models.
- Build capabilities you can delete cheaply, and hesitate before exposing them as permanent product features externally.
- Redo your context engineering every model release to keep surfing 5-10% ahead of everyone else consistently.
