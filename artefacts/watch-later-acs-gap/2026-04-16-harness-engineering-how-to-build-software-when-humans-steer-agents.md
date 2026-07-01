---
title: "Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI"
video_url: https://www.youtube.com/watch?v=am_oeAoUhew
video_id: am_oeAoUhew
channel: AI Engineer
published: 2026-04-16
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI**](https://www.youtube.com/watch?v=am_oeAoUhew) - AI Engineer - uploaded 2026-04-16

> Three next-step ACS videos available: all three spines complement adjacent catalog videos rather than duplicate them.

## 1. The ideas worth a video

**Spine A: Harness engineering is the discipline: code is free, so stop writing code and instead build the systems that surface the right instruction to the agent at the right time.** This is the load-bearing reframe the whole talk hangs off, subsuming the "code is free" economics, the scarce-resource shift (human time, attention, context window), and the "everything is a prompt" taxonomy.
VERDICT: 🔗 next-step video available (complements "Instruction Following Limits").

**Spine B: Convert every recurring agent mistake into a durable, self-healing guardrail, a bespoke lint or structure test whose error message is itself a remediation prompt, harvested on a weekly "garbage collection day".** The operational heart of the talk: how you actually stop re-reviewing the same slop.
VERDICT: 🔗 next-step video available (complements "Agent Introspection").

**Spine C: Architect the codebase FOR the agent, and enforce it with tests that assert code STRUCTURE, not behavior (350-line file caps, package-privacy edges, single canonical helpers), so context stays local and token output stays predictable.** Uniformity treated as deliberate context engineering.
VERDICT: 🔗 next-step video available (complements "The One-Pattern Rule for Agents").

## 2. Summary + counts

OpenAI's Ryan Lopopolo explains harness engineering: since agents write all code freely, engineers should build docs, lints, tests, and review agents that steer agents autonomously.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

## 3. 🔬 Deep dive

### Spine A: Harness engineering, surfacing the right instruction at the right time

**The claim:** When agents can produce every line, your job is no longer writing code; it is engineering the harness that gives the model the right context at the right moment. **Why it is non-obvious:** most people treat AGENTS.md and rules files as the whole game and frontload every constraint, which Lopopolo says overwhelms the agent. **Why it is true:** the models are trained to follow instructions and have seen "trillions of lines of code that make every possible choice" of the underspecified non-functional requirements; so quality is not a model gap but a specification-delivery gap. Because context is scarce and pages out over long runs, the harness must surface each instruction just in time, "let the agent cook and prototype," then enforce structure at lint or test time. **What it generalizes to:** technical writing, where a good runbook reveals the next step exactly when the operator needs it, not a wall of caveats upfront. **How it goes wrong:** frontloading everything, or over-building bespoke harness plumbing that the next model capability jump ("the bitter lesson") simply obsoletes. Context management survives; plumbing does not.

### Spine B: Self-healing guardrails and garbage-collection day

**The claim:** Every human review comment is evidence of a context failure, so instead of repeating it you convert it once into a bespoke lint, test, or review agent whose failure message tells the agent exactly how to self-heal. **Why it is non-obvious:** teams treat code review as the permanent human checkpoint; Lopopolo treats each comment as a bug in the harness. **Why it is true:** with three to five PRs per engineer per day, human review became the merge blocker and the source of conflicts; so his team ran a Friday "garbage collection day" to bucket recurring slop, write a durable check, and then the agent "would selfheal when it produced this bad behavior." The key mechanism is that a lint error message is a prompt: "no no no you shouldn't have an unknown here at all because we parse don't validate at the edge." **What it generalizes to:** customer support, where a recurring ticket becomes a macro plus a product fix rather than a human answering it forever. **How it goes wrong:** making every reviewer comment blocking "bullies" the agent; bias toward code accepted, not perfect, and let the agent defer or reject feedback.

### Spine C: Tests that assert code structure as context engineering

**The claim:** Beyond linting syntax, write "wholesome" tests that assert the structure of the code itself, file length caps, package-privacy edges, deduplicated Zod schemas, a single canonical async helper, because uniform, small, local code is what keeps the agent context-efficient. **Why it is non-obvious:** structure is usually a human aesthetic preference; here it is a hard performance lever for the model. **Why it is true:** "code in the file system is also text which means it's effectively prompts." So making everything the same means "the tokens that you want the model to produce are easier to predict and more consistently predicted regardless of where it looks," and capping files at 350 lines keeps each unit inside the scarce context window. Because large-scale migration is now free, you can enforce this uniformity across a 750-package monorepo. **What it generalizes to:** database schema design, where a normalized, consistent schema lets any query planner (or engineer) reason locally. **How it goes wrong:** over-treeing early (his blank Electron app "ended up with a mess"), or standardizing before the codebase is mature enough to know the right pattern.

## 4. 🎬 Proposed ACS videos

### Pitch 1 — Self-Healing Guardrails: Turn Every Review Comment Into a Lint the Agent Fixes Itself

- **HOOK:** Stop leaving the same PR comment twice; make the codebase say it for you.
- **THE PROMISE:** For anyone reviewing agent PRs, after this you can convert a recurring mistake into a bespoke lint or test whose error message re-prompts the agent to self-heal.
- **THE SHAPE:** (1) Spot a recurring slop pattern, for example fetch without a retry and timeout. (2) Write a bespoke ESLint rule for it. (3) Make the error message a remediation prompt, not just "lint failure." (4) Re-run the agent and watch it self-correct. (5) Run a weekly "garbage collection" pass to harvest the next batch, plus a persona review agent on every push.
- **SPINE:** B.
- **SLOT:** Advanced Techniques, chapter "Cleaning Up Legacy Code" (or a new "Self-Healing Guardrails" chapter).
- **RELATIONSHIP:** 🔗 complements "Agent Introspection" (Techniques, Debugging & Verifying Output), which teaches adding one deterministic guardrail after a single surprising action; this is its next step, the systematic loop that harvests every recurring mistake into a self-healing lint whose message is the prompt, and adds persona review agents on push (distinct from "Automatic Plan Reviewing with Subagents," which reviews plans before code, not pushed diffs).
- **PROOF TO REUSE:** the fetch retry-and-timeout lint story ("I am not a reliable reviewer or author of code with respect to this non-functional requirement"); the "no no no you shouldn't have an unknown here" error-message-as-prompt; "garbage collection day" on Fridays; "bias toward code being accepted, not perfect."

### Pitch 2 — Harness Engineering: Stop Writing Code, Start Surfacing Instructions

- **HOOK:** If code is free, the only thing left worth engineering is when the agent sees each instruction.
- **THE PROMISE:** For engineers drowning in a giant AGENTS.md, after this you can map every prompt-injection surface you own and deliver each instruction just in time instead of all at once.
- **THE SHAPE:** (1) The reframe: code is free, scarce resources are human time, attention, and context window. (2) The taxonomy: AGENTS.md, skills, lint messages, test failures, and review agents are all prompts. (3) Why frontloading fails and just-in-time wins: let the agent prototype, enforce at lint time. (4) The bitter-lesson filter: invest in context, not plumbing.
- **SPINE:** A.
- **SLOT:** Context Engineering, chapter "Foundations."
- **RELATIONSHIP:** 🔗 complements "Instruction Following Limits" (Context Engineering, Foundations), which teaches finite instruction-following capacity and loading the right instruction at the right moment; this adds the full taxonomy of injection surfaces (lint and test messages, review agents as prompts) and the "code is free, engineer the harness not the code" economic reframe on top of that principle.
- **PROOF TO REUSE:** "All the harness should do is surface instructions to the model at the right time"; "you can just prompt things ... without touching the model weights at all"; the React-component "let the agent cook, then break it apart at lint time" example; "Every time I have to type continue to the agent is like a failure of the harness."

### Pitch 3 — Fitness-Function Tests: Make Your Codebase Legible to Agents

- **HOOK:** Write a test that fails when a file gets too long, because context is your real budget.
- **THE PROMISE:** For teams on a growing agent-built codebase, after this you can add structure-asserting tests and lints that keep the repo uniform and context-efficient for every agent.
- **THE SHAPE:** (1) Why structure is context engineering: code is text is prompts. (2) A file-length cap test (350 lines) for context efficiency. (3) Package-privacy and dependency-edge checks. (4) Canonical-implementation enforcement, one async helper, one Zod schema. (5) Migrate the whole repo to uniform in parallel because refactoring is now free.
- **SPINE:** C.
- **SLOT:** Context Engineering, new chapter "Structure as Context" (or Advanced Techniques).
- **RELATIONSHIP:** 🔗 complements "The One-Pattern Rule for Agents" (Advanced Techniques, Cleaning Up Legacy Code), which teaches picking one gold-standard pattern and migrating to it; this adds automated tests and lints that assert the code's structure itself (file caps, package-privacy edges, canonical-implementation dedup) as deliberate, enforced fitness functions rather than a one-time manual standardization.
- **PROOF TO REUSE:** "you can write a test that limits the fact that files are no longer than 350 lines"; "code in the file system is also text which means it's effectively prompts"; the 750-package PNPM monorepo isolated by domain and layer; "you should have one way to construct a observable and instrumented side effectful command."

## 5. 📚 Full wisdom (reference)

**SUMMARY**
OpenAI's Ryan Lopopolo explains harness engineering: since agents write all code freely, engineers should build docs, lints, tests, and review agents that steer agents autonomously.

**IDEAS**
- For nine months Ryan built software exclusively through agents, banning his team from touching their editors.
- Implementation stopped being the scarce resource; code is now free to produce, refactor, delete, and maintain.
- Each engineer now commands five, 50, or 5,000 engineers of capacity, constrained only by GPU, tokens.
- Scarce resources became human time, human and model attention, and the model's finite context window now.
- With free code every P3 ticket ships immediately, often four in parallel; then pick one winner.
- Internal tools get full localization and internationalization from day one without trading against any team capacity.
- The important artifact is not the code but the prompt and guardrails that ultimately produced it.
- Breadcrumbs, ADRs, persona-oriented docs, ticket logs, and code-review history are what get agents to good output.
- Everything is a prompt: agents.md, rules files, skills, lint error messages, review agents, and structure tests.
- Lint and test error messages should carry remediation prompts telling the agent exactly how to proceed.
- You can write tests asserting source structure, like capping files at 350 lines for context efficiency.
- Fire off 15 agents to finish any six-month migration; large-scale refactoring is now essentially free, fast.
- Doing a good job means specifying 500 underspecified non-functional requirements the agent otherwise chooses itself randomly.
- Write a bespoke lint checking every fetch call has a retry and timeout, durably solved forever.
- Reviewer agents run on every push, primed with persona docs, surfacing P2s that block the merge.
- Ryan pointed Codex at OpenAI's prompting cookbooks to synthesize a reusable skill for automatically writing prompts.
- Codex is the entry point; skills teach it to launch the app, logging, and observability stack.
- They centralize leverage in five to 10 skills, making them better rather than adding thousands more.
- The infrastructure swapped Chrome DevTools protocol for a daemon; Codex adapted silently, unnoticed, for three weeks.
- Their monorepo grew to 750 PNPM packages isolated by business domain and layer of the stack.
- Package privacy enforces invariants on which APIs are public, giving agents concrete clear filesystem architectural hooks.
- Making all code uniform means the model's token output is easier to predict regardless of directory.
- Friday garbage-collection day: bucket every recurring slop pattern, then categorically eliminate it from ever happening again.
- Code is a disposable build artifact; the spec is source, the LLM a fuzzy compiler backend.

**INSIGHTS**
- Code being free inverts prioritization: P3s that never shipped now launch immediately in small parallel batches.
- A good harness surfaces the right instruction at the right time, never frontloading everything all upfront.
- Just-in-time instructions beat upfront ones: let agents prototype, then enforce structure at lint or test time.
- Every human review comment signals a context failure worth converting into an automated durable repository guardrail.
- Documenting one expert's persona once gives every future agent trajectory the best of that single specialist.
- Depending on first-party harnesses lets you ride the labs' in-loop post-training leverage almost entirely for free.
- Context management survives the bitter lesson; harness plumbing risks obsolescence by the next big capability jump.
- Being prescriptive that every comment must be addressed bullies agents; bias toward accepted, imperfect code instead.
- Uniformity is context engineering: identical patterns everywhere let agents reuse transferable context across the whole repo.
- Typing continue to an agent means the harness failed to encode enough context for full completion.
- Approving an unread plan silently encodes many instructions you never actually wanted the agent closely following.

**QUOTES**
- "I am a token billionaire and I believe that in order for us to get into our AGI future, we want everybody to be token billionaires" — Ryan Lopopolo
- "implementation is no longer the scarce resource of what it means to do the job of software engineering. Code is free." — Ryan Lopopolo
- "each engineer today in this room has access to five, 50, or 5,000 engineers worth of capacity 247 every day of the year." — Ryan Lopopolo
- "The important thing is not the code but the prompt and the guardrails that got you there." — Ryan Lopopolo
- "You can just simply say do not produce slop. Don't accept slop. You won't get slop in your codebase." — Ryan Lopopolo
- "you can just prompt things ... you can do this without touching the model weights at all" — Ryan Lopopolo
- "I use the skill to write prompts that I wrote with the agent looking at the prompts to write the prompts." — Ryan Lopopolo
- "code in the file system is also text which means it's effectively prompts that you're giving to your coding agent." — Ryan Lopopolo
- "Every time I have to type continue to the agent is like a failure of the harness" — Ryan Lopopolo
- "using LLM as fuzzy compiler is like an interesting mental model to have" — Ryan Lopopolo
- "we want to bias toward code being accepted, not perfect, not drowning in minutia" — Ryan Lopopolo
- "All the harness should do is surface instructions to the model at the right time." — Ryan Lopopolo
- "Do not hesitate to remove yourselves from the loop by getting the agents to do the full job because they can." — Ryan Lopopolo

**HABITS**
- He banned his team from touching editors, forcing all their work through the coding models exclusively.
- He starts every task from a ticket handed to an agent alongside a couple scoped skills.
- He tethers his laptop in the back seat, letting agents run inference during his home commute.
- His team runs Friday garbage-collection days to systematically eliminate recurring slop patterns from the entire codebase.
- He keeps skills to five or 10, improving existing ones instead of constantly proliferating new ones.
- He runs security and reliability review agents on every single push and CI run as standard.
- When writing prompts consumes too much time, he shells out to Codex to generate them instead.
- He rarely types slash-new, relying on Codex autocompaction to keep his long-running context fresh entirely automatically.
- He avoids plan mode, preferring to drop a ticket and have it completed without diverting further.

**FACTS**
- Ryan Lopopolo is a member of technical staff at OpenAI who authored the Harness Engineering essay.
- He spends over a billion output tokens daily, costing him roughly a thousand dollars per day.
- He credits GPT-5.2 as the model that could finally do a full software engineer's job entirely.
- His team runs a PNPM monorepo containing 750 packages isolated by business domain and stack layer.
- GPT-5.4 and Codex are, he says, fantastic at autocompaction, so he now rarely resets his context.
- Coding agents took over software development within roughly the last six months, per his own account.
- Each engineer on his three-person team produced three to five pull requests every single working day.
- OpenAI released Symphony, an agent orchestrator, and published exec plans as an early planning proto-skill format.

**REFERENCES**
- Harness Engineering essay (openai.com/index/harness-engineering/)
- Latent Space podcast episode on harness engineering (latent.space/p/harness-eng), cohost Vibhu Sapra (@vibhuuuus)
- Ryan Lopopolo (X @_lopopolo, LinkedIn ryanlopopolo, GitHub lopopolo)
- Models: GPT-5.2, GPT-5.4, Codex (Codex app server, Codex SDK)
- OpenAI prompting cookbooks (OpenAI developer guide); exec plans (proto-skill); Symphony (agent orchestrator)
- Tooling: Chrome DevTools protocol, ESLint, PNPM workspace, Zod, Kafka, CarPlay voice mode, Slido
- Analogy: LLVM, Cranelift, and the Rust compiler as codegen backends
- Event: AI Engineer conference (London)

**ONE-SENTENCE TAKEAWAY**
Stop writing code; engineer the harness that surfaces the right instructions to your agents automatically.

**RECOMMENDATIONS**
- Convert each recurring review comment into a bespoke lint whose error message prompts the agent's fix.
- Write tests asserting code structure, capping files at 350 lines to preserve scarce model context window.
- Run persona review agents on every push, each primed with docs defining that persona's quality standards.
- Let agents prototype freely, then enforce component decomposition and constraints only at lint or test time.
- Standardize on one canonical helper, one language, one CI style so token output stays highly predictable.
- Document a good QA plan once, specifying critical user journeys and media to attach for verification.
- Keep skills to five or 10, hiding fast-changing infrastructure beneath a stable, simple human invocation surface.
- Make Codex the entry point, giving it skills to launch your app, logging, and observability stack.
- Push any plan you actually use as a reviewed PR, blocking on explicit human approval first.
