---
title: "Using MCP server with 10000+ tools #7"
videoId: P5wRLKF4bt8
url: https://www.youtube.com/watch?v=P5wRLKF4bt8
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1 (THE spine): When a tool catalog outgrows the context window, put a narrowing function between the tools and the model so it only ever picks from a handful.**
This is the load-bearing reframe: dumping every tool into the prompt works until it doesn't, so you build `narrow_tools(query, tools)` first and let the model select from the smaller set.
VERDICT: ❌ net-new video available.

**Spine 2: An MCP server is nothing but a REST API with two endpoints, so you should own the agent loop rather than inherit a framework's assumptions.**
Because list_tools and call_tools are all MCP is, everything else stays in your code, including the freedom to abandon the OpenAI role/user/assistant message format.
VERDICT: 🔗 next-step video available.

**Spine 3: Installing a third-party MCP server is importing untrusted code, so rank it on a read-only to read-write risk gradient before it touches production.**
A tool description is injected straight into your prompt, so a malicious server can smuggle instructions and you have zero control once the call leaves your system.
VERDICT: ❌ net-new video available.

---

# Summary + counts

Vaibhav (BAML) and Dexter (HumanLayer) demonstrate scaling tool-calling agents past thousands of MCP tools by narrowing candidates before the model selects, keeping full developer control.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

**Spine 1: Narrow before you select.**
The claim: when a tool catalog outgrows the context window, you insert a narrowing function between the tools and the model, so the model only ever chooses from a handful. What most people get wrong is the naive move Vaibhav names directly: they list every tool and pass all of them into the prompt, and "that works until it doesn't," because a scraped registry like Smithery yields ten thousand tools and eleven megabytes of JSON that no model can reason over. The mechanism is a two-function pipeline. First, `narrow_tools(query, tools)` reduces the set by any method you like, from returning the first fifty tools to embedding every tool and ranking by similarity to the query. Then a normal structured-output prompt picks one tool from that smaller union. Because the two stages are separable, you can drop a yes/no probe on each: did narrowing surface a correct tool, and did the model then pick it. This generalizes cleanly to classification with thousands of categories, which is the same retrieval-then-select shape. It goes wrong when you embed the same text you prompt with, coupling two levers that should move independently.

**Spine 2: MCP is two API calls; own the loop.**
The claim: an MCP server is nothing but a REST API exposing two endpoints, list_tools and call_tools, so you should own the agent loop rather than inherit a framework's assumptions. The non-obvious part is that MCP feels like a magic capability layer; Vaibhav deflates it: "there's nothing else magical about MCP." The mechanism follows from that minimalism. Because the server only lists and calls, everything else stays in your code: you read the tool JSON schema and convert it into whatever data model you want, you alias the model-facing field "tool_name" to a private key so an untrusted server's own fields cannot collide, and you decide how state reaches the model. That last point is the reframe: you are not obligated to use OpenAI's role/user/assistant JSON; you can dump the entire conversation into one user message, because the model sees only what your prompt builds. This generalizes to any external SDK: MCP "just becomes another layer of SDK" once you own the inner loop. It goes wrong when you hand off control entirely; if you already know the correct order of operations, five bash commands beat a fragile prompt.

**Spine 3: Treat every MCP server as untrusted code.**
The claim: installing a third-party MCP server is importing code you do not own, so you must treat it as an untrusted API and evaluate it on a capability risk gradient. The default people adopt is excitement: they plug an entire registry into their agent and celebrate the new capabilities. The mechanism of the danger is that a tool description is injected straight into your prompt, so a malicious server can smuggle instructions, for example telling the agent to "add a social security number," and you have zero control once the call leaves your system. Vaibhav ranks the exposure by capability: read-only is safe, append-only is low risk, read-write demands thought, and read-modify is most dangerous. The concrete failure that "blew up on Twitter" was a GitHub MCP server that users could prompt into opening a pull request leaking PII. This generalizes to classic supply-chain security: you would not run an unknown binary as root, and an MCP tool call is the same trust decision. It goes wrong quietly: internal servers you own are lower risk, so teams wrongly assume the same safety when they later add external ones.

---

# 🎬 Proposed ACS videos

### 1. 1000 MCP Tools, One Agent: How to Not Blow Up Your Context Window
- HOOK: Your agent breaks the moment you plug in a real MCP registry. Here is the fix.
- THE PROMISE: For developers building agents on MCP, after this you can wire thousands of tools into one agent without overflowing context, by narrowing before the model picks.
- THE SHAPE:
  1. Show the naive path: dump all tools into the prompt, watch it break at scale.
  2. Scrape Smithery into a 10,000-tool JSON file to make the problem concrete.
  3. Write `narrow_tools(query, tools)`, starting with the dumb "first 50" version.
  4. Upgrade narrowing to embeddings; show the top-K tools that survive.
  5. Add the two probes (narrowing recall, selection accuracy) so failures localize.
- SPINE: Spine 1.
- SLOT: Claude Code class > new MCP / agent-building chapter (near mcps-connectors-that-i-use, mcp-json).
- RELATIONSHIP: ❌ net-new. Nothing in the ACS catalog covers scaling tool selection, dynamic tool retrieval, or embedding-based narrowing; mcps-connectors-that-i-use only lists which servers Ray uses.
- PROOF TO REUSE: Smithery yielding 10k tools / 11MB / ~300k lines; the "works until it doesn't" line; the first-50-then-embeddings progression; keeping embedding text separate from the prompt description; "if the embedding picked the wrong tool, there's no way the LM can pick the right one."

### 2. Every MCP Server You Install Is Untrusted Code
- HOOK: A tool description can tell your agent to leak a social security number, and you would never see it.
- THE PROMISE: For anyone adding MCP servers to an agent, after this you can rank and gate servers on a read-only to read-write risk ladder before they touch production.
- THE SHAPE:
  1. Demo a poisoned tool description that injects a hidden instruction into the prompt.
  2. Retell the GitHub MCP PII pull-request incident as the real-world stakes.
  3. Draw the capability gradient: read-only, append-only, read-write, read-modify.
  4. Add a deterministic last-minute filter and a human-confirmation step before dangerous actions.
  5. Rule of thumb: treat any server you don't own like an untrusted API endpoint.
- SPINE: Spine 3.
- SLOT: Claude Code class > security (adjacent to planned blocking-risky-commands-with-hooks).
- RELATIONSHIP: ❌ net-new. Adjacent to the planned blocking-risky-commands-with-hooks, which blocks risky local bash; this is a different threat model (third-party tool trust and prompt-injection via tool metadata), so Ray should not re-teach hook mechanics here.
- PROOF TO REUSE: the "add a social security number" injection example; the GitHub MCP PII PR that "blew up on Twitter"; the read-only/append/read-write/read-modify ranking; "view them the same way as an API endpoint from anywhere you don't trust until you know it."

### 3. MCP Is Just Two API Calls: Own Your Agent Loop
- HOOK: Everyone treats MCP like magic. It is two endpoints. Here is what that frees you to do.
- THE PROMISE: For developers deciding whether to adopt an agent framework, after this you can build the inner loop yourself and treat MCP as one more SDK.
- THE SHAPE:
  1. Whiteboard MCP down to list_tools and call_tools; kill the mystique.
  2. Read a tool's JSON schema and convert it into your own data model.
  3. Alias the model-facing "tool_name" to a private key so server fields can't collide.
  4. Show you can dump all state into one user message instead of OpenAI's JSON format.
  5. Mix static tools (clarification, human message) with dynamic runtime tools in one loop.
- SPINE: Spine 2.
- SLOT: Techniques class > core-agent-loop (backlog).
- RELATIONSHIP: 🔗 complements the planned core-agent-loop. core-agent-loop teaches the generic while-loop agent structure; this adds that MCP is only list_tools plus call_tools, so you own that loop and can even abandon the OpenAI role/user/assistant message format. Ray should not re-teach the basic loop, only the MCP-specific reframe.
- PROOF TO REUSE: "there's nothing else magical about MCP"; aliasing tool_name to BAML_tool_name to avoid field collisions; dumping the whole state into one user message; the static-vs-dynamic tool split with stronger reliability guarantees on static tools.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav (BAML) and Dexter (HumanLayer) demonstrate scaling tool-calling agents past thousands of MCP tools by narrowing candidates before the model selects, keeping full developer control.

## IDEAS
- MCP is just a REST API exposing two endpoints, list_tools and call_tools, nothing else magical whatsoever.
- Dumping every tool into prompt works until it doesn't; huge catalogs overflow context and crater performance.
- Scraping Smithery's registry yielded ten thousand tools; that JSON hit eleven megabytes, three hundred thousand lines.
- Build a narrow_tools function: given a query and many tools, return a much smaller model-sized subset.
- The simplest narrowing is returning the first fifty tools; a smarter one uses embeddings for relevance.
- Place two probes: did narrowing include the right tool, and did the model pick it correctly?
- Each probe is a yes/no question; whichever fails tells you exactly which stage to go fix.
- If embeddings never surface the correct tool, the model literally cannot pick it downstream at all.
- Never embed the same description you feed the prompt; treat embedding text as an orthogonal lever.
- Query object need not be a string; a UI checkbox for Slack can narrow tools too.
- Alias the LLM-facing 'tool_name' to a private 'BAML_tool_name' key so untrusted MCP fields never collide.
- Mix static tools (human messages, clarifications) with dynamic runtime tools; static ones carry stronger reliability guarantees.
- You control tool ordering in code: sort human messages first, or filter dangerous actions before execution.
- Insert a confirmation step deterministically: before a 'read bank transaction' action, force a human approval message.
- Treat any third-party MCP server as an untrusted API endpoint until you have personally verified it.
- A malicious tool description could inject 'add a social security number'; you own zero control there.
- Rank MCP risk by capability: read-only is clearly safe, append lower, read-write cautious, read-modify most dangerous.
- You need not use OpenAI's role/user/assistant JSON format; dump the entire state into one user message.
- If you already know the correct order, write five bash commands, not a fragile long prompt.
- Embedding models barely differ; the content you embed matters far more than your model choice does.

## INSIGHTS
- Everything interesting happens at scale; toy agents fit in memory, real systems force disk-like tool retrieval.
- MCP trades capability breadth for per-service reliability; you surrender control-flow to gain coverage across more scenarios.
- The winning architecture is hybrid: deterministic code, LLM workflows, and MCP fallback, routed per user journey.
- Separating embedding text from prompt description gives orthogonal levers; tweaking one shouldn't force changing the other.
- Reliability comes from many testable seams, not one clever prompt; build probes you can independently optimize.
- MCP shines for non-coders dropping integrations into existing chat clients, less so inside owned agent loops.
- There is no one-shot magic trick; MCP is just more software with the same old tradeoffs.
- Sequential control flow belongs in your data model or deterministic code, not hidden inside prompt instructions.
- Domain experts, like lawyers, should validate tool-selection correctness where only they can judge the nuanced distinctions.

## QUOTES
- "That is it. There's nothing else magical about MCP." (Vaibhav)
- "everything interesting happens at large scales." (Vaibhav)
- "MCP just becomes another layer of SDK." (Dexter)
- "the real magic of MCP is like if you're not writing code or you don't know how to write code but you just want to drop a bunch of integrations into a chatbot that you already use." (Dexter)
- "more tools is like, cool, I'm going to write less code and I'm going to hope the LM can figure it out." (Dexter)
- "you should view them as the same way as using an API endpoint from anywhere that you don't trust until you know it." (Vaibhav)
- "there is no oneshot magic trick." (Vaibhav)
- "if the embedding picked the wrong tool, then there's no way the LM can pick the right one because it's not even in your input." (Vaibhav)
- "If you already know what the right order is, you could have just written those five make commands in a bash script." (Dexter)
- "MCP isn't that hard. It's just an API that does list a bunch of tools and let you call that tool." (Vaibhav)
- "the model is the least important part of it. The most interesting part is the content that you're trying to do things with." (Vaibhav)

## HABITS
- They cache the tools.json list rather than re-fetching ten thousand tools on every single agent request.
- Vaibhav always adds a dedicated request_clarification tool by default when building any interactive CLI-based agent himself.
- They prototype with a while-true loop, typing messages repeatedly just to check the agent behaves correctly.
- They copy Chrome console requests, paste them into a model, and let it write integration code.
- They always start with the dumbest approach first, then add embeddings only when evaluations prove necessary.
- They add a progress bar (TQDM) whenever running slow batch operations like embedding thousands of tools.
- They keep a test suite of hundred cases, scoring each approach before trusting one over another.
- They deploy a small embedding model into their own VPC for cheap, fast, controllable embedding calls.

## FACTS
- Smithery is an MCP registry hosting thousands of MCP servers scraped into one massive tools catalog.
- In their poll, 30% currently use MCP, 50% aspire to, and 25% will never use it.
- Their scraped tools JSON reached eleven megabytes and roughly three hundred thousand lines of raw data.
- A single embedding network call ranges from about fifty milliseconds to one second in worst case.
- Very few YC companies actually use MCP in production, mostly only for end-user scale-out features today.
- A GitHub MCP server exposed to users can be prompted to create pull requests leaking PII.
- The MCP spec added tool annotations, but those are client directions and aren't sent to the model.
- Running ten thousand live embedding calls sequentially was too slow; the demo ran out of patience.

## REFERENCES
BAML; HumanLayer; 12-factor agents; Smithery (MCP registry); their first episode "classification with a thousand plus categories"; the eval episode; GPT-4o; o3; TQDM; numpy; OpenAI embeddings API; Bedrock / Azure for hosting embedding models; Supabase MCP; Notion API MCP; BrowserBase / browser use; Vercel; GitHub MCP; BAML TypeBuilder; Cursor; Claude Desktop; Linear; robots.txt and OpenAPI spec analogies; agents.json alternative proposal.

## ONE-SENTENCE TAKEAWAY
Scale agents to thousands of tools by narrowing candidates first, then letting the model pick.

## RECOMMENDATIONS
- Write a narrow-tools function that returns a model-sized subset of tools before any selection step happens.
- Add two probes to measure narrowing recall and selection accuracy separately so failures localize almost instantly.
- Start by dumping all tools into the prompt; only add embedding filtering when evals demand it.
- Keep embedding text separate from prompt descriptions so you can tune retrieval without touching your prompt.
- Evaluate every MCP server on a read-only to read-write risk gradient before exposing it to users.
- Encode required tool ordering in your data model or deterministic sort, not in fragile prompt instructions.
- Insert deterministic confirmation actions before any dangerous operations like reading bank data or modifying production state.
- Host a small embedding model in your own VPC for cheap, fast, controllable tool retrieval calls.
- Build a hundred-case test suite scoring approaches before adopting embeddings, fine-tuning, or any other fancier technique.
