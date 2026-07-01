---
title: Building a 12 Factor Agent #4
videoId: yxJDyQ8v6P0
url: https://www.youtube.com/watch?v=yxJDyQ8v6P0
date: 2026-07-01
status: posted
---

# The one idea worth a video

**1. Own the loop: an agent is just four pieces of ordinary code you write yourself (a prompt, a switch statement, a context-string builder, and a for-loop), not a framework you adopt.**
Why: this is the 12-factor master reframe; it subsumes owning your prompt, owning context building, owning control flow, unifying state, pause/resume, and triggering from anywhere.
VERDICT: 🔗 next-step video available (complements "The Core Agent Loop").

**2. Structured output, not "tool calls": the LLM is a stateless goto-statement that emits a data model your code interprets, so "tool use" is a harmful abstraction and forcing JSON often hurts quality.**
Why: it reframes the entire mental model of how models interact with your system, and it is a distinct, demo-able technique with its own slot.
VERDICT: 🔗 next-step video available (complements "Structured Output").

**3. Test-driven agents: because inputs and outputs are just strings and typed values, you assert on intent and parameters with cheap deterministic tests and rerun them on every prompt change, no LLM judge needed.**
Why: it turns "seems to work" into a repeatable proof and is the practical discipline that makes owning the loop safe to iterate on.
VERDICT: 🔗 next-step video available (complements "Evaluating Your Skills").

---

# Summary

Vaibhav (BAML) and Dexter (HumanLayer) live-code a framework-free 12-factor agent in TypeScript, teaching developers to own the loop, prompt, context, serialization, and evals, not frameworks.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1 — Own the loop

The claim: a production agent is not a framework you adopt, it is four pieces of ordinary code you write and control: a prompt, a switch statement, a context-string builder, and a for-loop. Why it is non-obvious: the industry default is "we need an agent, let's grab LangChain or CrewAI and go greenfield from scratch," which the speakers say "never works." Most people assume the framework's hidden while-loop is doing something sophisticated. The mechanism: an LLM is stateless, so the only thing determining the next step is the string you serialize into it. If you own the loop, you own where to break, pause, summarize, or insert an LLM-as-judge, and you can reassemble state from a database and resume via webhook, because there is no hidden execution system to integrate with. Because the loop is plain code, you reuse familiar software paradigms instead of relearning "LLM voodoo magic." It generalizes to adding AI to existing software piecemeal: a mature CRM where you replace one deterministic step with an LLM call rather than rebuilding as an "agent." How it goes wrong: bigger agents with more tools and steps "spin out and fail," so keep them small and focused and only widen the box as models improve.

## Spine 2 — Structured output, not tool calls

The claim: the LLM does not "call tools," it is a stateless goto-statement that emits a data model your code chooses to interpret, so model every capability as a typed structured output rather than a magic function call. Why it is non-obvious: "I actually think the concept of tool use is harmful," Dexter says; the framing that a model is "acting on its environment" is hype that hides what really happens, which is input tokens in, JSON out saying "I think the next step is X." The mechanism: once you see the output as just a typed value (a class, an array), you stop reaching for special "tool" machinery and gain leverage, for example rendering a message field directly to the user, or flipping a BAML return type from string to a tool class and watching the prompt regenerate itself. Crucially, forcing JSON can hurt: models are trained on far more markdown code than JSON, so constraining output zeroes out newline tokens and forces worse samples. Let the model output markdown and parse it flexibly. It generalizes to extraction pipelines that pull data out of images with no JSON at all. How it goes wrong: a flexible parser is real work, and if you will not build one, forcing JSON is the safer default.

## Spine 3 — Test-driven agents

The claim: because an agent's input and output are just strings and typed values, you can write cheap deterministic unit tests that assert on intent and parameters, and rerun them on every prompt change, without an LLM judge. Why it is non-obvious: most people evaluate agents by vibes, running it once and eyeballing the result, and assume you always need an expensive LLM-as-judge. The mechanism: structured output gives you a discrete value to assert against ("the intent was multiply, the params were 3 and 4"), so a change that breaks behavior fails a test before it merges. When a test breaks you decide whether you changed behavior on purpose or actually regressed, then update the test or fix the prompt. This is what "you want to prove to yourself that it's working" means in practice. It generalizes to guardrail evals: assert that garbled math must return "request more information," so a prompt edit that quietly breaks safety is caught in CI. How it goes wrong: assertions on exact strings get brittle as prompts evolve, and some subjective qualities (tone, style) still need a judge; structured assertions cover intent and parameters, not everything.

---

# 🎬 Proposed ACS videos

## 1. Own the Loop: Build an Agent Without a Framework
- **HOOK:** Every agent framework is just hiding a while-loop from you. Write it yourself in about forty lines.
- **THE PROMISE:** For engineers who already have real software and want agentic features: after this you can hand-build an agent loop and drop LLM calls into existing code without adopting a framework.
- **THE SHAPE:**
  1. Show software as a directed graph and point at where an LLM replaces the branching.
  2. Build the four parts live: prompt, switch statement, context-string builder, for-loop.
  3. Add a second tool and show that only the prompt changed, not the loop.
  4. Store the thread and resume it via a webhook to demonstrate pause and resume.
  5. Trigger the same agent from a CLI and a web endpoint to show UX decoupling.
- **SPINE:** 1
- **SLOT:** Fundamental Techniques > Core Agent Loop (the next-step build video)
- **RELATIONSHIP:** 🔗 complements "The Core Agent Loop (Observe, Think, Act)", which teaches the loop conceptually as the thing Claude Code and Codex run so you understand context management; this video has the viewer WRITE that loop themselves as plain deterministic code for their own software.
- **PROOF TO REUSE:** "An LLM is really just a really really smart go-to statement"; "Own the loop. Own the loop. That's it. It's not that hard"; the calculator agent where adding tools changes only the prompt, never the loop.

## 2. Stop Calling Tools: Treat the LLM as a Stateless Function
- **HOOK:** The model never calls your tools. It emits a typed value and your code decides what to do.
- **THE PROMISE:** For anyone building on the OpenAI or Anthropic APIs: after this you model every capability as a typed structured output and stop fighting tool-calling abstractions.
- **THE SHAPE:**
  1. Reframe the loop: input tokens in, a typed data model out, your switch statement acts.
  2. In BAML, flip a return type from string to a tool class and watch the prompt regenerate.
  3. Show multiple return types (calculator tools, human tools) as a union the model chooses from.
  4. Killer demo: force JSON output versus letting the model write markdown code, then compare quality.
- **SPINE:** 2
- **SLOT:** Prompt Engineering > Core Techniques (structured-output)
- **RELATIONSHIP:** 🔗 complements "Structured Output", which already teaches format-as-a-first-class-concern and the schema-as-prompt idea across JSON, XML, and YAML; this video adds the higher-altitude reframe that tool-use is a harmful abstraction and that forcing JSON can degrade quality versus flexible parsing.
- **PROOF TO REUSE:** "the concept of tool use is harmful"; "Do not ask the model to output JSON and JSON.parse it. That is really, really, really bad"; "if the model wants to write code in markdown, you should let the model write code in markdown."

## 3. Unit-Test Your Agent: Evals Without an LLM Judge
- **HOOK:** You changed the prompt. Did anything break? Vibes will not tell you. A test suite will.
- **THE PROMISE:** For agent builders: after this you assert on your agent's structured output and run those tests on every prompt change, catching regressions before they merge.
- **THE SHAPE:**
  1. Why "seems to work" is not a standard for a stochastic system.
  2. Write an assertion: for this input, intent must be multiply with params 3 and 4.
  3. Change the prompt, watch a test fail, decide whether it was intentional or a real regression.
  4. Add a guardrail eval: garbled math must return request-more-information.
- **SPINE:** 3
- **SLOT:** Fundamental Techniques > Evals for hand-built agents
- **RELATIONSHIP:** 🔗 complements "5.1 Evaluating Your Skills" (Skills > Quality Control) and loopy-ai's "Generator Evaluator", which teach evals for skills and LLM-judge negotiation; this adds cheap deterministic assertion tests on a hand-built agent's structured output, with no judge needed.
- **PROOF TO REUSE:** "You want to prove to yourself that it's working"; the hello-world test that broke once request-more-information was added; "we don't need LLM eval when you use structured outputs" for intent and parameter checks.

**Also film-able (not deep-dived):**
- The engineering-effort reliability curve: more engineering reshapes the whole distribution (the orange, green, and red curves), so you do not just wait for smarter models. One line: "there's no moat in saying I'll use the best model, everyone has the best model." Rough slot: Fundamental Techniques or Prompt Engineering.
- Unify execution state and business state into one inspectable context object (the massively-multiplayer single-source-of-truth analogy). Rough slot: Context Engineering.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav (BAML) and Dexter (HumanLayer) live-code a framework-free 12-factor agent in TypeScript, teaching developers to own the loop, prompt, context, serialization, and evals, not frameworks.

## IDEAS
- Code is fundamentally a directed graph; agents let an LLM traverse that graph choosing steps dynamically.
- An agent is just a prompt that repeatedly determines the next step from the current event.
- An LLM is really a very smart goto statement, not something that actually calls external tools.
- Every agent reduces to four parts: a prompt, a switch statement, a for-loop, and string serialization.
- The prompt means the entire serialized state you feed the model, not merely the system prompt.
- LLMs are completely stateless; the only memory is whatever tokens you pass into the context window.
- Tools are just structured output; ask the model for a typed class or array, not functions.
- Unify execution state and business state into one context window to drastically simplify debugging and rebuilding.
- Owning the loop lets you pause, store context in a database, and resume later via webhook.
- Add tool errors back onto the context window so the model can just retry and self-correct.
- Small focused agents fail less than big ones; added engineering reshapes the whole reliability distribution curve.
- Because inputs and outputs are strings, you can assert on them and build simple deterministic evals.
- Every prompt change should run a test suite proving the same inputs produce the same outputs.
- Forcing models to output JSON is bad; let them output markdown and parse it flexibly instead.
- Serialization choice matters: XML-style formatting uses far fewer tokens than quote-heavy JSON for the identical data.
- Give the model multiple human-contact tools, letting it declare intent such as clarification versus final answer.
- There is no model moat; Cursor and Claude Code use identical models, differentiated only by engineering.
- Trigger agents from anywhere: email, Slack, or webhooks, because the agent is decoupled from its UX.
- Magical AI experiences come from operating right at the boundary of model capability, done consistently right.
- What we need is shadcn for agents: scaffolded opinions you own and edit, not hidden abstractions.

## INSIGHTS
- Building agents greenfield from scratch usually fails; instead sprinkle LLM calls piecemeal into existing deterministic software.
- Control over what enters the prompt, in what order, unlocks the optimizations that reach best performance.
- Frameworks aren't the enemy; the requirement is how tightly you can own the final emitted prompt.
- Treating tool-use as the model acting on its environment is hype obscuring a stateless JSON-emitting function.
- One unified source of truth, like multiplayer game state, makes building and maintaining agent systems easier.
- You rarely need LLM-as-judge when structured outputs let you assert directly on intent and returned parameters.
- Smarter models raise the ceiling, but engineering still extracts the last differentiating ten-x of product quality.
- Owning the loop means reusing familiar software paradigms rather than relearning some framework-specific LLM voodoo magic.
- Because the model outputs its natural token distribution, forced JSON constraints zero-out newlines and degrade quality.
- Protocols like MCP can win on adoption momentum long before they are actually the cleanest design.

## QUOTES
- "An LLM is really just a really really smart go-to statement." — Vaibhav
- "I actually think the concept of tool use is harmful." — Dexter
- "Own the loop. Own the loop. That's it. It's not that hard." — Vaibhav
- "LMs are stateless. The only state is basically this context window, which is also nice because it's very inspectable." — Dexter
- "We're all using the same models. Claude Code versus Cursor, they're both using Sonnet 3.7. There's no difference. It's just the UX and all the engineering in between." — Vaibhav
- "The only way to create really impressive or even magical experiences in AI is to find something that is right at the boundary of what the model is capable of and get it right consistently." — Vaibhav (paraphrasing the Notebook LM team)
- "If you think of this whole thing as just one big string, you can do anything you want with this." — Dexter
- "Do not ask the model to output JSON and JSON.parse it. That is bad. That is really, really, really bad." — Vaibhav
- "If the model wants to write code in markdown, you should let the model write code in markdown." — Dexter
- "You want to prove to yourself that it's working." — Vaibhav
- "There's no moat in saying I'm going to use the best model. Everyone has the best model." — Vaibhav

## HABITS
- They commit to git after each incremental chapter or change while building the agent up step-by-step.
- They run the full test suite after every prompt change to catch unintended behavioral regressions immediately.
- They whiteboard concepts first before coding, believing diagrams convey ideas better than jumping straight into implementation.
- They enable BAML debug logging to inspect the exact full prompt string sent to the model.
- They test the same task across multiple models by swapping one line, keeping the tests identical.
- They keep agents small and focused rather than piling on tools and steps that spin out.
- They open-source all the code from every episode, believing shared code helps everyone discover better architectures.
- They reverse-engineer exactly how a framework builds its prompt once its black-box abstractions eventually hit a wall.

## FACTS
- Cursor and Claude Code both ran on Anthropic's Sonnet 3.7 model at the time of recording.
- BAML is a language whose CLI generate command compiles BAML source code into native TypeScript code.
- Vaibhav is a co-creator of BAML and a Y Combinator founder from the Winter 2023 batch.
- Dexter founded HumanLayer, a YC company building safer, more reliable agents and human-approval layers for them.
- The demo used GPT-4o, then swapped to o3-mini via a single line change, keeping tests unchanged.
- The 12-factor agents blog post was written by Dexter, seeded by an October or November hackathon.
- The pair claim to have collectively seen hundreds of companies ship real AI agents to production.
- Helm won Kubernetes packaging through early momentum despite Google later releasing a cleaner competing protocol design.
- Most MCP servers are technically clients: run locally, they actually call the real remote server themselves.

## REFERENCES
- BAML (BoundaryML) and its playground, debug logging, and token visualizer.
- HumanLayer (Dexter's company, human approval for agents).
- The 12-factor agents blog post (Dexter / HumanLayer).
- "AI That Works" series (this show; described as episode 4 of season 1).
- LangChain and LangGraph; CrewAI.
- DAG orchestrators: Prefect, Airflow, Dagster.
- OpenAI API/SDK and Anthropic SDK.
- Models named: GPT-4o, GPT-4o-mini, o3-mini, o3, o1, Sonnet 3.7.
- Notebook LM team (quote on operating at the boundary of capability).
- shadcn/ui (the "shadcn for agents" analogy); React (beauty-of-code analogy).
- MCP (Model Context Protocol) and the Agent Development Kit.
- BFCL (Berkeley Function Calling Leaderboard) and the OpenAI tokenizer.
- The GPT-4.1 prompting guide (discussed re: forcing literal output formats).
- Helm, Kubernetes, and Google (protocol-momentum analogy).
- "Goto Considered Harmful" (Dijkstra) referenced as a planned blog post.
- Redis, SQLite, Postgres (thread-store options); Luma (event signup); Slack and email (agent triggers).

## ONE-SENTENCE TAKEAWAY
Own the loop, prompt, context, and tests yourself; an agent is just ordinary controllable code.

## RECOMMENDATIONS
- Build your agent's loop yourself with a switch statement and for-loop instead of adopting a framework.
- Choose frameworks by how completely they let you inspect and edit the final prompt being sent.
- Model tools as typed structured outputs, then interpret the returned data model in your own code.
- Write assertion-based tests on agent outputs and rerun them after every single prompt or schema change.
- Serialize your context window deliberately; compare JSON versus XML token counts using the OpenAI tokenizer tool.
- Add reasoning by simply instructing the model to think first, without prescribing what it should reason.
- Unify execution and business state in one inspectable context object to enable easy pause and resume.
- Decouple the agent from its UX so you can trigger it from CLI, web, Slack, or email.
- Give the model distinct tools for different human contacts, like clarification versus delivering a final answer.
- Add failed tool results back into context and let the model retry instead of just hard-crashing.
