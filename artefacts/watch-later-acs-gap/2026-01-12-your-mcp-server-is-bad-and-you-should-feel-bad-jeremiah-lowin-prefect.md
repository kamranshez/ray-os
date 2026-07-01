---
title: "Your MCP Server is Bad (and you should feel bad) - Jeremiah Lowin, Prefect"
video_url: https://www.youtube.com/watch?v=96G7FLab8xc
video_id: 96G7FLab8xc
channel: AI Engineer
published: 2026-01-12
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Your MCP Server is Bad (and you should feel bad) - Jeremiah Lowin, Prefect**](https://www.youtube.com/watch?v=96G7FLab8xc) - AI Engineer - uploaded 2026-01-12

> net-new ACS videos available: ACS teaches using MCP servers but never authoring good ones

## The idea worth a video

**Spine 1 - An MCP server is a user interface for agents, so design it around outcomes, not the atomic REST operations you already have.** It is the talk's thesis and subsumes naming, argument-flattening, and "stop converting REST APIs." VERDICT: ❌ net-new video available.

**Spine 2 - Tool count is a context budget spent on every handshake; past ~50 tools per agent, performance degrades, so curate ruthlessly.** Distinct demo (measure handshake cost, cut tools) and distinct action from Spine 1. VERDICT: 🔗 next-step video available (complements the consumer-side MCP Search Tool).

**Spine 3 - Everything the agent reads back is a prompt: errors, descriptions, and examples are all context you author.** The most counter-intuitive reframe, distinct demo (recovery-oriented errors). VERDICT: ❌ net-new video available.

## Summary + counts

Jeremiah Lowin, Prefect CEO and FastMCP creator, argues MCP servers are interfaces for agents, teaching the agentic product design mindset: outcomes, curation, budget, recoverable errors.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 - Design for outcomes, not operations

The claim: an MCP server is a user interface for agents, so you design it around the outcome the agent wants, not the atomic operations your REST API exposes. Why it is non-obvious: engineers instinctively mirror endpoints one-to-one, because that is genuinely best practice for a REST API and feels clean. Lowin argues that instinct is exactly backward. The mechanism runs through three agent-specific costs he names: discovery is expensive because the agent re-enumerates every tool on each startup; iteration is expensive because every extra call resends the whole history; and context is tiny. So a server of atomic operations forces the agent to plan a multi-call sequence, guess argument formats, and pay the iteration tax repeatedly, when a human developer would have written that sequence once. Bury the three sequential calls inside one track_latest_order(email) tool and the agent gets a single, hard-to-misuse outcome. Where it generalizes: the same logic governs internal Python tool definitions and Claude skills, not just MCP, since any agent-facing surface pays these costs. How it goes wrong: collapse too far and you build an agent-as-orchestrator that hides logic the model cannot steer, or you lose observability into which sub-call failed.

### Spine 2 - Respect the token budget, curate ruthlessly

The claim: tool count is a context budget you spend on every handshake, and past roughly fifty tools per agent selection performance degrades, so you curate ruthlessly. Why it is non-obvious: more capability feels strictly better, and each individual tool looks cheap. Lowin makes the cost legible with arithmetic: if a company exposes 800 endpoints inside a 200,000 token window, each tool gets a sliver just to name and document itself, and once every tool fits, the agent is lobotomized on connect with no room left to think. The mechanism: descriptions load up front, not lazily, so the whole catalog competes with the actual task for the same scarce window, and it is additive across every server the agent connects to. The fix is curation, which he calls the single most important verb: his colleague, now at Fiverr, went from 188 tools down to five. Where it generalizes: the same budget governs CLAUDE.md files, skill libraries, and system prompts, where more instruction quietly starves the task. How it goes wrong: naive curation deletes genuinely needed capability, so pair cuts with progressive disclosure or meta-tools that reveal detail on demand.

### Spine 3 - Errors are prompts, instructions are context

The claim: everything the agent reads back from your tool is a prompt, so error messages, descriptions, and examples are all context you author whether you notice or not. Why it is non-obvious: engineers treat errors as status codes for a caller that will parse them, and examples as harmless illustrations. Lowin flips both. An LLM does not see a 400; it sees information about what to do next, so a cryptic value error teaches it nothing, while a message that names the fix turns a failed call into a recovery. This enables a strange progressive disclosure: rather than documenting every argument up front, you document how to recover from the most common failures, which also saves handshake tokens. The examples-are-contracts effect is the sharp edge: an example with two tags yields exactly two tags almost every time, because the model treats the pattern, not just the values, as instruction. Where it generalizes: the same reflex governs tool descriptions in Claude skills and sub-agent definitions. How it goes wrong: errors that are too scary make the agent abandon the tool permanently, and duplicating docs across prompt and schema creates a contradictory, out-of-sync tool.

---

## 🎬 Proposed ACS videos

### 1. Build an MCP Server Agents Actually Use: Outcomes, Not Operations

- **HOOK:** Your MCP server is probably a REST wrapper, and the agent quietly hates it.
- **THE PROMISE:** For developers shipping MCP servers, rebuild one bad tool into an outcome tool the agent calls correctly on the first try.
- **THE SHAPE:**
  1. Show the "bad" server: atomic check-order-status tools mirroring the REST API, and watch the agent fumble the call sequence.
  2. Explain the three agent costs (discovery, iteration, context) that make atomic tools expensive.
  3. Rewrite into one outcome tool that buries the three sequential API calls internally.
  4. Flatten arguments to top-level primitives, name the tool and arguments for the agent, use enums or literals.
  5. Re-run: one clean call, one clear outcome. State the limit (do not turn the agent into an orchestrator).
- **SPINE:** 1
- **SLOT:** Master Claude Code > MCP Servers (new authoring video; the chapter today is entirely consumer-side setup)
- **RELATIONSHIP:** ❌ net-new. Every existing MCP video ("MCP Servers", "Claude.ai MCP Servers / Connectors", "MCP Search Tool") teaches installing and connecting servers; none teaches authoring one.
- **PROOF TO REUSE:** the order-status rewrite worked example; "outcomes not operations"; "you are not building a tool, you are building a user interface"; the flatten-arguments and enum tips.

### 2. The 50 Tool Ceiling: Curate Your MCP Server's Token Budget

- **HOOK:** The GitHub server can ship 200,000 tokens before your agent does anything.
- **THE PROMISE:** For MCP authors, measure your handshake token cost and curate tool count until the agent actually performs.
- **THE SHAPE:**
  1. Connect a bloated server and show the handshake eating the context window via /context.
  2. Do the arithmetic: 800 tools in 200k tokens leaves each tool a sliver, and the agent is lobotomized on connect.
  3. Introduce the ~50-tools-per-agent degradation line and the needle-in-a-haystack framing.
  4. Curate: split admin from user tools, collapse operations into outcomes, land at five to fifteen.
  5. Preserve capability with progressive disclosure or meta-tools instead of raw deletion.
- **SPINE:** 2
- **SLOT:** Master Claude Code > MCP Servers (or Context Engineering)
- **RELATIONSHIP:** 🔗 complements "MCP Search Tool" (Master Claude Code > MCP Servers). That video teaches the consumer to load only relevant tool descriptions to save context on a bloated server; this teaches the server author to curate the budget so the server never bloats in the first place. Do not re-teach the consumer-side /mcp toggling.
- **PROOF TO REUSE:** the 800-endpoint customer story; the 188-to-5 Fiverr curation arc; "curate is the single most important verb"; "an agent finds a needle by inspecting every strand of hay".

### 3. Errors Are Prompts: Designing MCP Failures Agents Recover From

- **HOOK:** Your error message is the agent's next prompt, whether you meant it to be or not.
- **THE PROMISE:** For MCP authors, write recovery-oriented errors and descriptions so agents self-correct instead of abandoning the tool.
- **THE SHAPE:**
  1. Raise a raw value error and show the agent looping blindly on retry.
  2. Reframe: the LLM never sees a 400, only text it treats as its next instruction.
  3. Rewrite the error to name the fix; watch the agent recover on the next call.
  4. Progressive disclosure via errors: document recovery paths instead of every argument up front.
  5. Show examples-are-contracts (two tags yields two tags) and the doubly-documented tool trap; add read-only hints.
- **SPINE:** 3
- **SLOT:** Master Claude Code > MCP Servers (authoring) or Prompt Engineering
- **RELATIONSHIP:** ❌ net-new. "Instruction Following Limits" (Context Engineering) covers consumer instruction files getting ignored; nothing covers authoring tool error messages, descriptions, and examples as agent prompts.
- **PROOF TO REUSE:** "errors are prompts"; "examples are contracts"; the tags example he hit the day before the talk; the doubly-documented tool trap; the read-only annotation hint (ChatGPT developer mode).

---

## 📚 Full wisdom (reference)

**SUMMARY** — Jeremiah Lowin, Prefect CEO and FastMCP creator, argues MCP servers are interfaces for agents, teaching the agentic product design mindset: outcomes, curation, budget, recoverable errors.

**IDEAS**
- Design MCP servers as products for agents, not REST wrappers regurgitating APIs built for human SDKs.
- Agents differ from humans across three key dimensions: discovery, iteration, and context, each far more expensive.
- Discovery is cheap for humans but expensive for agents, which re-enumerate every tool on each startup.
- Iteration is the enemy for agents, since every additional call resends the entire prior conversation history.
- Context is tiny: the model remembers only its last 200,000 tokens plus whatever lives in weights.
- Curate is the single most important verb for MCP developers designing for extremely limited agent brains.
- Build your tools around outcomes, not operations: bury three sequential API calls inside one agent-facing tool.
- Do not use an agent as orchestrator or glue; agents orchestrate expensively, slowly, and painfully stochastically.
- Name your tools and arguments explicitly for the agent choosing them, not for future human developers.
- Flatten your arguments into top-level primitives; avoid nested configuration dictionaries the LLM must invent and populate.
- Use literals or enums for constrained choices; most LLMs do not even know that syntax exists.
- Avoid tightly coupled arguments, where one input's value silently determines which other inputs stay valid choices.
- Errors are prompts: each failure message you return becomes part of the agent's next reasoning attempt.
- Document recovery from common failures inside error messages, a progressive disclosure that also saves handshake tokens.
- Examples are contracts: two tags in your example yields exactly two tags almost every single time.
- Set the read-only annotation hint so clients like ChatGPT can skip permission prompts for safe tools.
- The token budget is scarce: 800 tools alone would lobotomize an agent on the initial handshake.
- Fifty tools per agent is roughly where tool selection performance visibly starts to degrade and break.
- Stop converting REST APIs directly into MCP servers; doing so violates every heuristic agents actually need.
- Auto-generating from OpenAPI is fine for bootstrapping only; strip and curate it before shipping to production.
- One key question is always whether you control the client, unlocking far richer both-sides design options.
- If you control the client, document infrequent workflows as Claude skills or files instead of tools.

**INSIGHTS**
- An MCP server is really a user interface for agents, so apply real product design discipline.
- The false assumption that capable AIs are infallible oracles poisons most agentic product design decisions today.
- Humans almost never use raw APIs; they insert websites, SDKs, or apps between themselves and endpoints.
- Agents deserve their own interface optimized for their strengths and weaknesses, exactly as humans get theirs.
- Making something work and making it work well are two distinct phases of the product journey.
- An agent finds a needle by inspecting every strand of hay, so minimize the haystack surface.
- Doubly documenting one tool, across prompt and schema, is often worse than documenting it poorly once.
- We will soon discuss context products, not MCP servers, once the industry moves past the transport.
- Client non-compliance, like Claude Desktop hashing tools, constrains which spec-legal optimizations server authors can safely use.
- Good error design accepts the first call will fail and teaches recovery through the returned message.

**QUOTES**
- "humans don't use APIs. Very very rarely do humans use APIs. Humans use products." - Jeremiah Lowin
- "an agent can find a needle in a hay stack. The problem is it's going to look at every piece of hay and decide if it's a needle." - Jeremiah Lowin
- "the most important word in the universe for MCP developers is curate." - Jeremiah Lowin
- "outcomes not operations." - Jeremiah Lowin
- "Name the tool for the agent. Don't name it for you." - Jeremiah Lowin
- "errors are prompts." - Jeremiah Lowin
- "examples are contracts." - Jeremiah Lowin
- "instructions are context." - Jeremiah Lowin
- "please, please just, if nothing else, stop converting REST APIs into MCP servers." - Jeremiah Lowin
- "you are not building a tool. you are building a user interface." - Jeremiah Lowin
- "50 tools to the agent is where you start to see performance degradation." - Jeremiah Lowin
- "I choose to interpret this as but you can do better." - Jeremiah Lowin

**HABITS**
- He starts every server by putting too many tools in, then forces himself to remove them.
- He bootstraps with FastMCP's auto-converter first, then strips the REST regurgitation and curates it by hand.
- He solves one problem at a time, first proving an agent will call the tool reliably.
- He studies exemplary MCP playbooks from Block and GitHub rather than cataloguing every bad server's flaws.
- He documents the high-level server purpose in the instructions field, keeping it short rather than novel-length.
- He prefers literals and enums over free strings whenever the set of valid choices is known.
- He avoids putting argument documentation in system prompts, thereby preventing the doubly-documented, contradictory, out-of-sync tool trap.
- He treats any tool count above fifty per agent as a smell worth investigating and splitting.

**FACTS**
- FastMCP was downloaded roughly one and a half million times in a single day just recently.
- MCP and FastMCP were both introduced almost exactly one year before this particular talk was given.
- Anthropic incorporated a version of FastMCP into the official MCP SDK after David personally reached out.
- The GitHub MCP server reportedly ships around 170 tools and roughly 200,000 tokens on initial handshake.
- Kelly, now at Fiverr, grew a server to 188 tools, then curated it down to five.
- Claude Desktop hashes all received tools into a SQLite database on first contact, then ignores updates.
- One respected company needed to expose 800 API endpoints as tools and found no workable solution.
- SEP 1686 proposes adding asynchronous background tasks to MCP for every operation, fully opt-in per client.
- Cloudflare blogged about code mode first, and Anthropic followed, with agents writing code that calls tools.

**REFERENCES**
- FastMCP (the framework the talk is built around) and its documentation
- MCP (Model Context Protocol) and the official MCP SDK
- Prefect / Prefect Technologies (Lowin's company; commercial per-tool masking)
- Marvin (Lowin's earlier agent framework)
- Apache Airflow PMC (Lowin's prior open-source role)
- Block's MCP playbook / blog post (repeatedly recommended)
- GitHub's MCP blog posts on semantic routing (~170-tool server)
- Kelly's two blog posts (Oct and Nov) on building up then curating a Fiverr server
- Lowin's viral blog post: "stop converting REST APIs into MCP servers"
- Futurama (1999 episode; source of the talk's meme title)
- David at Anthropic; colleague Adam (talk on SEP 1686 async tasks)
- Code mode (Cloudflare first, then Anthropic)
- ChatGPT developer mode (uses the read-only annotation hint)
- Claude Desktop and Claude Code (client compliance discussion)

**ONE-SENTENCE TAKEAWAY** — Stop shipping REST wrappers; design your MCP server as a curated product for limited agents.

**RECOMMENDATIONS**
- Rewrite atomic REST-mirroring tools into a few outcome-oriented tools that bury the sequential API calls internally.
- Measure your server's handshake token cost, then curate ruthlessly toward just five to fifteen tools maximum.
- Replace nested configuration dictionaries with flat primitive arguments, using enums or literals for any constrained choices.
- Write genuinely helpful, recovery-oriented error messages, treating each one as the agent's very next corrective prompt.
- Document every tool and the whole server, but keep examples minimal since agents copy them exactly.
- Add read-only annotation hints to your safe tools, letting compliant clients relax their extra permission prompting.
- When you control the client, move infrequent workflows into Claude skills instead of permanent server tools.
- Read the Block and GitHub MCP playbooks carefully before designing any production-facing agent tool surface yourself.
</content>
</invoke>
