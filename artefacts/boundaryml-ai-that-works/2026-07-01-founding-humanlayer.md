---
title: Founding HumanLayer
videoId: LEOA19Ss9lc
url: https://www.youtube.com/watch?v=LEOA19Ss9lc
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works
---

## The one idea worth a video

**Skills over MCP: use the file system + bash + a markdown skill as the substrate for connecting an agent to services, and only reach for MCP when third parties need to extend YOUR app.** This is the load-bearing reframe because it collapses "which integration layer do I use" into a clear rule and subsumes the whole SDK-vs-MCP confusion Dexter watched a hundred builders fall into.
VERDICT: ❌ net-new video available

**The RPI loop: store zero durable context and rebuild understanding fresh from live code on every task, because maintained docs are "the amount of lies," not the source of truth.** It is a spine because it reframes documentation, planning, and subagents into one repeatable research-plan-implement motion that runs three or four parallel research passes and reuses their output as a session seed.
VERDICT: 🔗 next-step video available

**12-factor agents applied to Claude Code: keep control flow in code, not in the prompt, by chunking one overloaded planning prompt into small deterministic workflow steps.** It stands as its own spine because the concrete demo (a five-step plan prompt that Sonnet forgets halfway through, fixed by decomposition) is distinct from constraining a single task.
VERDICT: 🔗 next-step video available

## Summary

Vibhav (BAML) interviews Dexter (HumanLayer) for an end-of-year AI That Works special covering his founding journey plus practical agent techniques: RPI, skills over MCP, and 12-factor decomposition.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - Skills over MCP (the substrate question)

The claim: with coding agents now at real product-market fit, the cheapest universal way to connect an agent to external services is the file system plus bash plus a skill (a markdown file in a folder, optionally bundling CLIs), and MCP earns its place only when you want third parties to extend an app you built.

Why it is non-obvious: through 2024 the industry sold a different promise, that if you built into the agent "ecosystem" you would get free distribution through a uniform interface, the way Chroma shipped one-pip integrations for Crew, LangChain, and LangGraph. Dexter's counter is blunt: "if you know what the tools should be and you know what the workflow is then just write the dang code or just use the dang SDK."

Why it is true: MCP is a layer of indirection. If you already own the loop, the prompts, and the structured outputs, that indirection buys nothing and costs safety and control. MCP pays off in the opposite shape, where your app is the MCP client and a barely-technical user pastes in an MCP JSON to get their Gmail. It generalizes cleanly to non-coding startups for sales and ops teams that run on the Claude Agent SDK and pull Gmail or calendar data into the file system rather than wiring each API in.

How it goes wrong: bash is less safe than a scoped MCP server, and file-system access is a real blast-radius concern, so the substrate choice trades safety for simplicity and needs guardrails.

### Spine 2 - The RPI loop (rebuild context, do not store it)

The claim: instead of maintaining documentation about your system, store nothing durable and rebuild the context every single task by running a research pass over the live code, then plan, then implement. Vibhav's framing: "you store no information about the actual system and every single time you do a task you build that context up individually."

Why it is non-obvious: the reflex is to invest in docs, a CLAUDE.md, agents.md files, or a startup that "keeps your docs up to date." Dexter stopped writing agents.md entirely because his codebase changes too fast to keep synced, and on his AI Engineer slide the y-axis of maintained docs is not source of truth, "it's actually the amount of lies."

Why it is true: docs decay because code changes faster than humans update them, so a research agent reading current code beats any stale artifact. Because the research prompt is reliable, you can run three or four in parallel, background the five-to-ten-minute pass, and reuse the resulting document to seed a fresh session even for a one-line change. It generalizes to onboarding a human engineer via an end-to-end plumbing task rather than a doc.

How it goes wrong: RPI burns extra tokens and time, and Vibhav is explicit it is "not to perfectly oneshot a long complex task," it is a two-to-three-times speedup, so treating it as full autonomy overshoots.

### Spine 3 - 12-factor agents in Claude Code (control flow for control flow)

The claim: the builders selling six-figure enterprise contracts avoid opinionated frameworks that own the loop; they decompose the problem, stay deterministic, and treat the LLM as what it is, a machine that turns unstructured data into structured data. Applied to Claude Code, that means keeping control flow in code and chunking a bloated planning prompt into small workflow steps.

Why it is non-obvious: the hype pushed full-fat "tools in a loop" agents and a single mega-prompt that encodes every branch. Dexter lived both sides, first as the 12-factor skeptic of autonomous agents, then obsessed with Claude Code once models improved.

Why it is true: a five-step planning prompt with five to ten instructions each overloads a weaker model, so Sonnet forgets what it was doing halfway through step two and needs constant reminding. Move the branching ("if the user says this, do that") out of the prompt and into real control flow, and each small step becomes reliable again. That is his "guided planning" prototype, marrying 12-factor decomposition with Claude Code. It generalizes to any long prompt doing routing it should not.

How it goes wrong: decomposition adds orchestration overhead, and cutting a prompt too finely can lose the shared context a single pass would have held, so the seams need care.

## 🎬 Proposed ACS videos

### 1. Skills or MCP or Just Write the Code: The Decision That Ends the Confusion

- HOOK: Everyone is bolting MCP onto agents they fully control, and it is the wrong layer almost every time.
- THE PROMISE: For builders wiring agents to real services, a one-rule decision framework for when to use a Skill, when to use MCP, and when to just write code.
- THE SHAPE: (1) The 2024 ecosystem promise and why it broke. (2) The rule: own the loop, write the code or use the SDK. (3) MCP's real job, making your app extensible for third parties who paste MCP JSON. (4) Skills as the new substrate: file system plus bash plus a markdown folder. (5) Demo pulling Gmail or calendar into the file system instead of an API integration.
- SPINE: 1 (Skills over MCP).
- SLOT: Claude Skills class > foundations (a "Skills vs MCP vs SDK" decision video), with a cross-link from Claude Code > mcps-connectors-that-i-use.
- RELATIONSHIP: ❌ net-new. The Skills class teaches building, chaining, and selling skills, and the catalog has skills-vs-subagents plus mcps-connectors-that-i-use, but nothing teaches the MCP-vs-Skills-vs-SDK decision itself or the file-system-as-substrate thesis.
- PROOF TO REUSE: "just write the dang code or just use the dang SDK"; "I would be very bullish on skills over MCP"; the Chroma one-pip integration story; MCP-is-for-extensibility framing; startups running on the Claude Agent SDK that pull data into the file system.

### 2. Delete Your Docs, Rebuild Context: The RPI Loop

- HOOK: The best AI engineers store nothing about their system and rebuild the whole context from scratch on every task.
- THE PROMISE: For engineers past their first week with Claude Code, a repeatable research-plan-implement loop that beats maintained docs and reliably gives a two-to-three-times speedup.
- THE SHAPE: (1) Why maintained docs are "the amount of lies." (2) The research pass that reads live code. (3) Running three or four research subagents in parallel and backgrounding them. (4) Reusing a research doc to seed a fresh session for a small change. (5) Framing RPI as a speedup, not a one-shot.
- SPINE: 2 (RPI loop).
- SLOT: Techniques > agent workflow (next to delete-your-readme), with a cross-link to the Context Engineering class.
- RELATIONSHIP: 🔗 complements "Delete Your README" by being its next step. Delete Your README teaches that code is the only source of truth and maintained docs go stale, so it already argues the "why." This video does not re-teach that; it delivers the positive method, the parallel research pass plus research-doc-as-session-seed loop you run instead.
- PROOF TO REUSE: "it's actually the amount of lies"; "you store no information about the actual system"; "RPI is not to perfectly oneshot a long complex task, it's to speed you up by two to 3x"; the 15,000-line BAML Rust PR built almost entirely with RPI.

### 3. Control Flow Belongs in Code, Not Your Prompt

- HOOK: Your planning prompt is doing branching logic, and that is exactly why the weaker model keeps forgetting the plan.
- THE PROMISE: For anyone who has written a giant multi-step prompt, how to chunk it into small deterministic steps so even Sonnet follows every instruction.
- THE SHAPE: (1) The 12-factor thesis: the best builders decompose and stay deterministic. (2) The failure: a five-step plan prompt Sonnet forgets halfway through step two. (3) Pull the branching out of the prompt into real control flow. (4) Chunk into small workflow steps ("guided planning"). (5) Show the before and after on one bloated prompt.
- SPINE: 3 (12-factor in Claude Code).
- SLOT: Techniques > prompt architecture (near core-agent-loop / prompt-contracts), cross-linked to Context Engineering.
- RELATIONSHIP: 🔗 complements "Boxing the Model In" by being its next step. Boxing the Model In teaches constraining the model inside a single task so it cannot wander. This adds the architecture-level move above that: split the whole workflow into deterministic steps and let code, not the prompt, own the routing between them.
- PROOF TO REUSE: "use control flow for control flow, which is the whole point of 12-factor agent"; the five-step prompt Sonnet forgets at step two; the "guided planning" or "autotune for planning" prototype; LLMs as unstructured-to-structured-data transformers.

Also film-able (not deep-dived): **Hand the mic to the codebase expert.** In a pairing session the person who knows the codebase must drive the prompting while the workflow expert "sprinkles in the magic words"; Dexter's rule is to hand over the SuperWhisper mic the moment the workflow driver starts saying things that are wrong about the code. Rough slot: My Daily Workflows > pairing, likely 🔗 complement.

## 📚 Full wisdom (reference)

### SUMMARY
Vibhav (BAML) interviews Dexter (HumanLayer) for an end-of-year AI That Works special covering his founding journey plus practical agent techniques: RPI, skills over MCP, and 12-factor decomposition.

### IDEAS
- The RPI method stores zero durable context and rebuilds understanding fresh from live code every task.
- Documentation you maintain sits on a y-axis measuring lies, the inverse of actual source of truth.
- Run three or four research subagents in parallel, each mapping a different slice of the codebase.
- Background the five to ten minute research pass, do other work, then return to reliable output.
- Skills beat MCP: a markdown file in a folder plus bundled CLIs connects agents to services.
- MCP fits when you want users to extend your app, not when you own the loop.
- If you know the tools and workflow already, just write the code or use the SDK.
- The top one percent selling six-figure enterprise contracts avoid opinionated frameworks that own the agent loop.
- LLMs are best understood as machines that turn unstructured data into other kinds of structured data.
- Use control flow for control flow: chunk giant prompts into small deterministic workflow steps not prompts.
- Sonnet forgets a five-step planning prompt halfway through step two and needs constant reminding of position.
- RPI aims for two to three times speedup, not a perfect one-shot of long complex tasks.
- Reuse a research document to seed a fresh session for even a one-line targeted change quickly.
- The codebase expert, not the workflow expert, must hold the mic and drive the actual prompting.
- Guided planning marries 12-factor decomposition with Claude Code so Sonnet can plan without losing track completely.
- Non-coding startups for sales and ops now build their core on the Claude Agent SDK loop.
- Pull external data like Gmail or calendar into the file system rather than wiring APIs in.
- Duplication beats the wrong abstraction; racing to build shared standards produced many incorrect early agent abstractions.

### INSIGHTS
- Maintained docs decay because code changes faster than humans update them, so freshly derived context wins.
- The ecosystem promise failed because real agent architectures are too bespoke to plug into shared standards.
- Reliability at enterprise scale comes from determinism and decomposition, not clever fully-autonomous agent loops left unsupervised.
- Coding-agent product-market fit makes the file system the cheapest universal substrate for connecting agents to services.
- Prompts encoding branching logic overload weaker models; moving that logic into code restores reliable instruction following.
- A reliable research prompt lets teams stop reading research entirely and trust the assembled context blindly.
- Watching real users daily balances founder emotion and surfaces bugs that both hype and rankings hide.
- A workflow that convinces your most AI-skeptical senior engineer is the workflow worth productizing across teams.
- Teaching a planning workflow that only works after seven hours of pairing does not scale organizationally.

### QUOTES
- "It's actually the amount of lies." - Dexter, on the y-axis of maintained documentation.
- "if you know what the tools should be and you know what the workflow is then like just write the dang code or just use the dang SDK you don't need an extra layer of abstraction" - Dexter.
- "I would I would be very bullish on skills over MCP." - Dexter.
- "the easiest way to connect your agent to services is file systems and bash commands." - Dexter.
- "duplication is better than the wrong abstraction." - Vibhav, citing a 2015 Rails talk.
- "RPI is not to perfectly oneshot a long complex task. It's to speed you up by two to 3x." - Vibhav and Dexter.
- "you store no information about the actual system and every single time you do a task you build that context up individually for that system." - Vibhav, describing RPI.
- "use control flow for control flow, which is the whole point of 12actor agent." - Dexter.
- "if you want to be a founder just go be a founder." - Dexter.
- "if people aren't complaining then your [stuff] doesn't matter." - Tariq, relayed by Dexter.
- "you have to have a codebase expert with lots of opinions and lots of knowledge and you have to have a workflow expert." - Dexter, on pairing.

### HABITS
- Dexter runs several onboarding calls weekly and watches new signups actually use freshly shipped product features.
- He backgrounds long research passes and fills the wait with a second parallel piece of work.
- He always tries early prototypes to understand how people want to build AI pipelines long term.
- He gives new hires end-to-end plumbing tasks so they traverse and learn the entire codebase fully.
- He runs the mom test at meetups, asking about problems without revealing what he is building.
- He stops writing agents.md files because his fast-changing codebase makes them impossible to keep properly synced.
- He keeps honest critics close, treating a smart friend's harsh feedback as a valuable early signal.
- He deliberately hands the microphone to whoever actually knows the codebase during a live pairing session.

### FACTS
- The Rails talk claiming duplication beats the wrong abstraction dates from roughly 2015 in the community.
- MCP launched around November 2024, before coding agents had strong product-market fit and mass developer adoption.
- The Claude Code SDK shipped a headless JSON interface over standard out around Sonnet 4's release.
- Dexter started a company in October 2023 after spending roughly seven years working at Replicated beforehand.
- Dexter was accepted into YC as a solo founder holding only half of a CS minor.
- Chroma gained distribution by building one-pip integrations with Crew, LangChain, and every major agent framework available.
- Aspiration's founders reportedly ended up in jail for allegedly defrauding their own investors, per Dexter's account.
- 12-factor agents grew from a November hackathon Discord chatbot built completely differently from existing agent frameworks.

### REFERENCES
- Books: The Mom Test.
- Frameworks and methods: 12-factor agents (Dexter), RPI / Research-Plan-Implement (Vibhav / BAML).
- Tools and products: BAML, HumanLayer, code layer, Claude Code, Claude Code SDK / Claude Agent SDK, MCP, Chroma DB, Crew AI, LangChain, LangGraph, SuperWhisper, Dr. Racket / Scheme.
- Models: Sonnet 4, Opus 4, Opus 4.1.
- Companies: Replicated, Sprout Social, Aspiration, Docker, metalytics.
- People: Dexter, Vibhav, Kyle (co-founder), Tariq (Claude Code), Jeff (Chroma), Dalton (YC).
- Talks and events: the 2015 Rails "duplication vs wrong abstraction" talk, the AI Engineer talk, AI Tinkerers Seattle, the MCP debate.

### ONE-SENTENCE TAKEAWAY
Rebuild context from live code each task and keep control flow in code, not prompts.

### RECOMMENDATIONS
- Replace maintained docs with a research agent that rebuilds context from current code each task fresh.
- Launch three or four research subagents in parallel to map different areas of the codebase simultaneously.
- Save each research document and reuse it to seed later sessions for small targeted code changes.
- When you already know the tools and workflow, skip MCP and just write the straightforward code.
- Use MCP only to let external users extend your application, not to build your own loop.
- Pull Gmail, calendar, and CRM data into the file system rather than integrating each separate API.
- Chunk an overloaded planning prompt into smaller steps and route between them with actual control code.
- Hand the prompting microphone to whoever knows the target codebase best during any live pairing session.
- Watch a friendly customer use each new feature weekly to stay grounded amid competitive market noise.
