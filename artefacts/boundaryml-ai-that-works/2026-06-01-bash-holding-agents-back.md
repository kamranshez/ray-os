---
title: Why Bash Might Be Holding AI Agents Back | Rhys Sullivan
videoId: 0dx3j4CmSFw
url: https://www.youtube.com/watch?v=0dx3j4CmSFw
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Every way an agent "does things" is the same primitive, a tool call (name + inputs + outputs); inline tools, MCPs, bash, and code mode are just skins you should render your catalog into.**
Why: it dissolves the whole "MCP vs bash" debate into a single question, which representation do I expose, and turns the durable asset into one callable catalog (ideally a great OpenAPI spec).
VERDICT: net-new video available.

**Code mode, letting the agent write one script that calls many tools and running it in an execution environment, beats one-call-at-a-time because it shapes output, accumulates results, and caps model round-trips.**
Why: it is the concrete, demo-able technique the whole episode builds toward, and it directly attacks context bloat (return one field, not a JSON blob) and hop count (two calls, not N).
VERDICT: net-new video available.

**Bash works for agents not by luck but because it is massively over-represented in training data, which makes alignment-to-training-data a real design axis for every tool you build.** (LATENT SPINE)
Why: it reframes tool design, the model is good at what it saw millions of times (edit tool beats sed), so shape your schemas and commands to resemble abundant patterns.
VERDICT: next-step video available (complements an existing techniques video).

---

## Summary and counts

On the AI That Works podcast, Dex, Vaibhav, and Rhys Sullivan compare inline tools, MCPs, bash, and code mode as competing agent execution environments today.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

**Spine 1, the tool-call primitive.** The claim: inline structured-output tools, MCPs, bash plus CLIs, and code mode are four surface renderings of one thing, a tool defined only as "a name, input arguments and output arguments." It is non-obvious because teams treat "MCP vs bash" as a religious war; Vaibhav's reframe is that "they're basically the same thing," differing only semantically "cuz we organize our programs differently around them." The mechanism has real steps: every format ultimately compiles down to the model emitting an instruction to call the same underlying mechanism, so the choice is not about capability but about which representation the harness exposes and how the ecosystem is reached. Therefore the durable asset is a callable catalog, best captured as a strong OpenAPI spec, that you render into a CLI today and code mode tomorrow, exactly as Rhys advises: "look at the primitives not the implementation of the primitives." It generalizes cleanly to a company that standardizes on one OpenAPI spec and auto-generates SDKs, CLIs, and MCP servers from it. Where it goes wrong: over-indexing on today's winner (Rhys expects a better primitive within six months), and the semantic differences genuinely matter for user expectations and permissions, so "same thing" cannot be taken literally.

**Spine 2, code mode.** The claim: instead of calling tools one at a time, have the model write a script that calls many tools and run it in an execution environment. It sounds like a marginal convenience, but the real payoff is context control and bounded hops. The mechanism: with bespoke or MCP calls each tool dumps a full JSON blob into context and each step is another round-trip, so an N-step chain costs N calls plus N blobs. In code mode the model writes something like const pr = await tools.github.createPR() then console.log(pr.url), filters in-code, accumulates intermediate results it never has to read, and returns only the final field, so hops are "guaranteed two calls as opposed to N calls if you know what you're running." It generalizes to the test-suite loop: today a model reruns a five-minute suite piping to grep just to find the failure and "keeps doing this over and over"; code mode captures and filters once. It also buys readability, a syntax-highlighted script instead of an opaque bash one-liner. How it goes wrong: the supporting infrastructure is not there yet (swap in a raw JS tool and you lose tool search and type declarations), type checking can be too slow to run per block, and the python-c "superpower" tempts you into a language you might not want the model writing.

**Spine 3, training-data alignment (latent).** The claim: bash is good for agents because it dominates training data, not because it is an elegant agent interface. People assume bash "just works" as if by design; Vaibhav insists "it's not a coincidence that the model just happens to be good at this," because "most of the internet and most of software navigation and most tutorials on the web" are bash. The mechanism: model competence tracks token frequency in pretraining, so an interface that mirrors what developers actually type outperforms a bespoke one you can only marginally post-train onto. The evidence is concrete: Claude's edit tool beats sed because "no one else uses sed," so sed is thin in the data and the model fumbles it; models are "very very good at Python" largely because python-c is everywhere. It generalizes to designing skills, slash commands, and tool schemas to resemble common patterns rather than clever novel DSLs. How it goes wrong: alignment is a moving target that post-training and new model releases keep shifting, and leaning on it can entrench a local maximum whose ceiling (global state, no read-only versus destructive signal, poor output shaping) is precisely why the hosts think bash will be "considered harmful by the end of 2026."

---

## 🎬 Proposed ACS videos

### 1. Code Mode: Stop Calling Tools One at a Time
- HOOK: Your agent just burned 5,000 tokens re-running the whole test suite only to find out which test failed.
- THE PROMISE: For anyone wiring tools into an agent, you will learn to make it write one script that calls many tools, filter the output in-code, and return only the field you actually need.
- THE SHAPE: (1) The problem, every MCP or CLI call dumps a full JSON blob and each step is another round-trip. (2) The bash half-fix, pipe gh pr create through jq to surface only the URL. (3) Code mode, write const pr = tools.github.createPR() then console.log(pr.url). (4) Accumulate and filter intermediate results the model never sees, so hops cap at two. (5) When to reach for it (thousands of tools, serverless or no-VM agents) and the caveats (immature infra, slow type checking).
- SPINE: 2.
- SLOT: Context Engineering (new chapter, agent execution environments) or Bonus Techniques.
- RELATIONSHIP: ❌ net-new. The catalog has mcp-json and mcps-connectors-that-i-use, but nothing on code mode or on having the agent write tool-calling scripts. No matching title or chapter exists.
- PROOF TO REUSE: the jq-to-URL example ("changing it into GH PR create and pipe it into jq"); "guaranteed two calls as opposed to N calls if you know what you're running"; the test-suite grep loop where "the model just like keeps doing this over and over again."

### 2. Inline Tools, MCP, Bash, Code Mode: They Are All the Same Thing
- HOOK: The MCP-versus-bash debate is a distraction, they are four skins on one primitive.
- THE PROMISE: For agent builders, you will be able to reason about any tool format as name plus input plus output and swap between them deliberately instead of by fashion.
- THE SHAPE: (1) A tool is just a function, a name, input arguments, output arguments. (2) The four renderings on a whiteboard, inline or structured-output tools, MCPs, bash plus CLIs, code mode. (3) What actually differs, semantics, who can add tools, and how you reach the ecosystem, not capability. (4) The durable asset, one great OpenAPI spec you render into a CLI, MCP, or code mode. (5) "MCP for flows, APIs for raw data, CLIs for humans" and why the context-bloat complaints about MCP are outdated.
- SPINE: 1.
- SLOT: Context Engineering (foundational chapter) or Master Claude Code (mcps and connectors chapter).
- RELATIONSHIP: ❌ net-new. mcps-connectors-that-i-use is a practical "which MCPs I use" video; this is the missing conceptual map of all tool-use formats and how to swap between them.
- PROOF TO REUSE: "just remember that they're basically the same thing" (Vaibhav); "you have to look at the primitives not the implementation of the primitives, and bash is an implementation of the primitives" (Rhys); the whiteboard taxonomy of tool-use formats; the closing "MCP for flows, APIs for raw data, CLIs for humans" framing.

### 3. Why Your Agent Is Good at Bash and Bad at Sed
- HOOK: Claude's edit tool beats sed for one reason, almost nobody trains on sed.
- THE PROMISE: For anyone designing tools, skills, or slash commands, you will learn to shape them to look like abundant training data so the model wields them reliably.
- THE SHAPE: (1) The claim, bash works because the internet is mostly bash, not because it is well designed. (2) The evidence, edit versus sed, and models being "very very good at Python" because python-c is everywhere. (3) The design corollary, make your schemas and commands resemble common patterns, not clever DSLs. (4) The limit, alignment is a moving target and can trap you in a local maximum whose ceiling (global state, no read-only signal) is why bash may be "considered harmful."
- SPINE: 3.
- SLOT: Techniques class (backlog, next to gravitational-pull-from-older-models).
- RELATIONSHIP: 🔗 complements "gravitational-pull-from-older-models" by being its design corollary. That filmed video teaches that models drift toward older, more common patterns from their training; this adds the actionable move, deliberately design your agent's tools to match the abundant training-data patterns the model already knows.
- PROOF TO REUSE: "it's not a coincidence that the model just happens to be good at this"; "bash is way more aligned to the training data than any of these bespoke tools are"; the edit-versus-sed anecdote ("whenever I see Claude starting to do sed commands... it's better than sed").

---

## 📚 Full wisdom (reference)

**SUMMARY**
On the AI That Works podcast, Dex, Vaibhav, and Rhys Sullivan compare inline tools, MCPs, bash, and code mode as competing agent execution environments today.

**IDEAS**
- Inline tools, MCPs, bash, and code mode are really all just implementations of one tool-call primitive.
- A tool is really only a function: a name, input arguments, and output arguments, nothing more.
- Code mode has the agent write a full script calling your tools, then just executes it.
- Bash was the agent's first execution environment: invoke tools, chain them, filter output, and live-reload them.
- Models are good at bash because the internet, tutorials, and software navigation overflow with bash commands.
- Claude's edit tool beats sed precisely because developers rarely use sed, so training data lacks it.
- With bespoke tools the power lives with the developer; with bash it lives with the user.
- Bespoke tools limit the agent to what the developer defined; bash unlocks the whole CLI ecosystem.
- With bash the model itself can add new tools mid-context, not just the user at startup.
- Dumping every tool's name and full schema into context is expensive; search-and-describe instead scales to thousands.
- Code mode caps model round-trips at two calls; chained bespoke tool calls grow with N steps.
- Piping GH PR create through jq surfaces only the URL instead of a giant JSON blob.
- Models good at Python largely because python-c runs arbitrary code inline, a superpower for code mode.
- Global CLI state, like one Google account per whole machine, forces sandboxes and breaks multi-agent auth.
- Bash gives you no signal about which commands are read-only versus destructive, so approvals stay crude.
- Rewriting a 500-line bash script as a program mirrors the instinct pushing agents toward code mode.
- Type declarations let the model see a tool's input and output shape before writing any code.

**INSIGHTS**
- The primitive is the tool call; bash and code mode are implementations you should freely swap.
- Bash's success comes mostly from training-data alignment, not from any inherent fitness as a tool interface.
- The real bash tradeoff is autonomy for the user against loss of output shaping and permissions.
- Code mode's biggest win is context control: return just one field, not the whole tool response.
- CLIs were designed for humans with tab completion; agents instead need schemas, types, and structured discovery.
- A great OpenAPI spec is the durable asset; CLI, MCP, or code mode are downstream renderings.
- Complaints about MCP context bloat are mostly outdated; it is really a harness problem, not MCP's.
- Don't over-index on code mode itself; a better primitive rendering may replace it within six months.
- Choosing a format is really semantics: MCP suits flows, APIs suit raw data, CLIs suit humans.

**QUOTES**
- "It's not a coincidence that the model just happens to be good at this." (Vaibhav)
- "Bash is way more aligned to the training data than any of these bespoke tools are." (Vaibhav)
- "I think bash is going to be considered harmful by the end of 2026." (Dex)
- "You want your agent to be able to do everything that you can do." (Rhys)
- "The power of bash is that the power of the software relies on the person running the system." (Vaibhav)
- "This is my biggest pain point with bash, is you have no idea what's read-only and what's destructive." (Rhys)
- "It's guaranteed two calls as opposed to N calls if you know what you're running." (Dex)
- "You have to look at the primitives not the implementation of the primitives, and bash is an implementation of the primitives." (Rhys)
- "Agents don't use tab. The default way to build a CLI and all the tooling around it is dumb." (Vaibhav)
- "That is basically a superpower to a model." (Vaibhav, on python-c)
- "If you have a 5,000-line bash script, please delete it and write a Python script or a JavaScript." (Vaibhav)
- "CLIs are for humans and not for agents." (Rhys)

**HABITS**
- Rewrite any bash script that grows past roughly 500 lines into a clean, maintainable, proper program.
- Refuse to let the model write Python, and prefer languages with fast compilers for type checking.
- Verify install commands before pasting them so the audience does not get slop-squatted by hallucinated packages.
- Let the agent read a CLI's own source to confirm it is only an API wrapper.
- Expose primitives the model can compose, letting it control recursion depth and when to describe tools.
- Recurse tool types only about two levels deep, leaving references the model looks up on demand.
- Screenshot any code block and simply ask a cheap chat model to add syntax highlighting instantly.
- Ship a skill alongside your CLI so the model actually learns its outputs and combined actions.

**FACTS**
- Code mode originated in an Apple research paper roughly twelve months before this conversation was recorded.
- OpenAI's Codex shipped a code mode feature gated behind an opt-in flag still marked under development.
- Twitter adopted REST with only GET and POST around 2011, becoming an early massively viral API.
- ChatGPT and Claude both offload tools to a search interface when far too many are registered.
- The Google Workspace CLI allows only one signed-in account per entire machine, not merely per session.
- The GitHub CLI exposes destructive endpoints, including a delete-project one, offering no read-only versus write distinction.
- Python lets models run arbitrary code inline via python-c; Rust has no such equivalent inline mechanism.
- UV now supports single-file Python scripts, letting each code mode script run in its own environment.

**REFERENCES**
- Code mode (OpenAI Codex feature, behind an opt-in flag)
- The deleted OpenAI tweet announcing Codex code mode
- Apple research paper that introduced code mode (roughly 12 months prior)
- BAML, the programming language built by Boundary (BoundaryML)
- Humanlayer (Dex's company); Boundary (Vaibhav's company)
- Rhys Sullivan's tool for MCP, API, and GraphQL source management via code mode (Executa / executor SDK)
- MCP (Model Context Protocol)
- GitHub CLI (gh), Google Workspace CLI
- jq (JSON filtering), UV (Python single-file scripts)
- tRPC (proxy object pattern reference)
- PostHog, Axiom, Stripe, WorkOS, Auth0
- OpenAPI, GraphQL, and Google Discovery specs
- The AI That Works podcast

**ONE-SENTENCE TAKEAWAY**
Every agent tool is one primitive; render your catalog into whatever format currently wins today.

**RECOMMENDATIONS**
- Stop debating MCP versus bash; treat both as swappable renderings of one single callable tool catalog.
- Pipe verbose CLI output through jq so that only the needed field enters the context window.
- Try code mode when your agent needs thousands of tools or must run without a VM.
- Design agent tools to resemble abundant training data; prefer patterns models have seen millions of times.
- Publish one strong OpenAPI spec so you can later generate a CLI, MCP, or code mode.
- Sandbox any agent using global-state CLIs so that per-machine auth cannot collide across parallel agent runs.
- Give tools both search and describe primitives so the agent discovers capabilities without dumping every schema.
- Block destructive agent actions explicitly rather than trusting a crude bash-level auto-approve for read-only versus write.
