---
title: "Agentic Search for Context Engineering — Leonie Monigatti, Elastic"
video_url: https://www.youtube.com/watch?v=ynJyIKwjonM
video_id: ynJyIKwjonM
channel: AI Engineer
published: 2026-05-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Agentic Search for Context Engineering — Leonie Monigatti, Elastic**](https://www.youtube.com/watch?v=ynJyIKwjonM) - AI Engineer - uploaded 2026-05-08

> Three next-step videos available: all three spines complement existing ACS context-engineering content rather than duplicating it.

## The one idea worth a video

**Spine 1 (thesis + framework): Stop hunting for one silver-bullet search tool; design your agent a deliberate retrieval STACK, pairing low-floor specialized tools with a high-ceiling general one, and let logged behaviour tell you which specialists to carve out.** Why it's the spine: it subsumes the RAG-to-agentic-RAG history, the "context engineering is 80% agentic search" thesis, the low-floor/high-ceiling framing, and the log-then-specialize loop. VERDICT: 🔗 next-step video available.

**Spine 2: The shell tool is a universal retrieval interface, and a semantic-grep CLI (Jina's gina-grep) closes its one real gap, keyword-only matching, without standing up a vector database.** Why it's the spine: it is the most concrete, demo-rich technique in the talk and is exactly the surface ACS lives on (Claude Code is grep plus files). Distinct demo and slot from Spine 1, so de-merged. VERDICT: 🔗 next-step video available.

**Spine 3: Whether your agent calls the right tool with the right arguments is decided mostly by the tool description and parameter design, not the model; fix reliability with layered descriptions, progressive-disclosure skills, and error-returning tools.** Why it's the spine: distinct failure-mode framework with its own demo (the ESQL wildcard fix) and its own slot. VERDICT: 🔗 next-step video available.

## Summary + counts

Leonie Monigatti of Elastic argues context engineering is mostly agentic search, walking through semantic search, general query tools, shell retrieval, and agent skills.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Build a retrieval stack, not a silver bullet

The claim: there is no single best search tool, so you curate a stack that pairs low-floor specialized tools with a high-ceiling general one. Leonie's framing is that "context engineering is about 80% agentic search," meaning the interface deciding what enters the window matters more than the model. What most people get wrong is reaching for one tool (just semantic search, or just the shell) and expecting it to cover everything. The mechanism: a specialized tool like get-customer-by-ID has trivial parameters, so even a weak model rarely misfires and rarely needs repeat calls (the low floor), but it cannot answer unexpected questions. A general tool (the shell, or "write the whole query") handles anything (the high ceiling) but needs more iterations and a stronger model to get parameters right. Neither alone is good; combined they cover both the common path and the long tail. And when you do not yet know your agent's query behaviour, start general, log every call, then carve out a specialist wherever you see repeated patterns or four-to-five calls per question. Leonie did exactly this: after three days logging OpenClaw's exec tool, she asked it what patterns it saw, and it recommended specific database tools to build. It generalizes cleanly to Claude Code (grep, glob, read as specialists beside the general Bash tool) and to overloaded MCP suites. It goes wrong at both ends: over-specialize early and you get a brittle tool zoo the agent cannot route; under-specialize and it iterates expensively.

### Spine 2 — The shell as universal retrieval, plus semantic grep

The claim: a bash or exec tool is a near-universal retrieval interface, and its one genuine weakness (keyword-only matching) is closed by a semantic-grep CLI, no vector database required. Why it is non-obvious: people assume file-system retrieval means either exact grep, which misses synonyms, or building an embedding pipeline. Leonie shows a third path. The mechanism: with only a shell tool the agent runs ls, then grep, and for semantic questions it "cheats," chaining synonyms (regulate, compliance, GDPR, governance, sovereignty) until something hits. It works but is inefficient and unreliable, as she jokes: do you really want the agent listing every possible animal to find animal-superhero movies? Installing a semantic-grep CLI such as Jina's gina-grep (or LightOn's cograg, LlamaIndex's semtools) and simply telling the agent it exists lets it run one semantic query and rank the right files on the first try, with retrieval staying in the terminal and no embedding code inside the agent. It generalizes to Claude Code exploring a large unfamiliar repo, where grep misses conceptually related code and a semantic-grep CLI reaches relevant files faster. It goes wrong two ways: shell access is dangerous (agents can delete files, so sandbox it), and you must tell the agent when to use exact grep versus semantic grep or it picks the wrong one.

### Spine 3 — Tool descriptions and parameters decide routing, not the model

The claim: whether the agent calls the right tool with valid arguments is governed mostly by the tool description and parameter design. Why it is non-obvious: teams ship a one-sentence description, then blame the model when the agent calls web search instead of the database tool. The mechanism runs through three failure modes: the agent calls no tool (trusting parametric knowledge), calls the wrong tool, or generates bad parameters. Fix them in order: start with a core-purpose description; if it still misroutes, add trigger conditions (when to use, when not), then relationships ("always load the ESQL skill before calling this"), then reinforce in the system prompt. Parameter complexity is a separate axis: get-by-ID is easy, but writing a full ESQL query from scratch is hard, so wrap general tools in a try/except that returns the error to the agent so it self-corrects instead of crashing. And use progressive-disclosure skills (inject only the description, load the full body on demand) to hand the agent the exact syntax it keeps missing, like ESQL using asterisk not percent as the wildcard. It generalizes to building custom Claude Code skills or MCP servers where overlapping tools must be routed among. It goes wrong when per-error band-aids balloon the prompt (a skill is the durable fix), and when zero results are treated as valid rather than a silent failure.

---

## 🎬 Proposed ACS videos

### 1. Give Claude Code Real Semantic Search Over Your Files

- HOOK: Your agent is faking semantic search by spamming grep with synonyms, and there is a one-command fix.
- THE PROMISE: For anyone whose coding agent misses conceptually related code, install a semantic-grep CLI and get first-try relevant hits.
- THE SHAPE: (1) Show the agent grepping, then chaining synonyms to "cheat" at semantic search; (2) name why that is slow and lossy; (3) install a semantic-grep CLI (gina-grep / cograg / semtools); (4) tell the agent it exists plus when to use it versus exact grep; (5) rerun the same query and land the right file immediately.
- SPINE: 2.
- SLOT: Context Engineering, Foundations (next to "Why Search Isn't Enough").
- RELATIONSHIP: 🔗 complements "Why Search Isn't Enough" by being its next step. That video teaches that keyword and grep-based discovery becomes unreliable in large or old repos and motivates a context layer; this adds a concrete tool that makes grep-style retrieval semantic, so do not re-teach why keyword search fails, just show the fix.
- PROOF TO REUSE: the synonym-chaining grep demo (regulate, compliance, GDPR, governance); the animal-superhero-movies analogy; the gina-grep first-try success finding Bili's talk.

### 2. Your Retrieval Stack Beats Your Model: Low Floor, High Ceiling

- HOOK: There is no silver-bullet search tool, so stop looking for one and design a stack instead.
- THE PROMISE: For agent builders, a repeatable way to choose your tool mix and let the agent tell you which specialists to build.
- THE SHAPE: (1) The thesis, retrieval is roughly 80% of context engineering; (2) low floor (specialized, simple params, weak model is fine) versus high ceiling (general, flexible, needs iteration); (3) start general when behaviour is unknown; (4) log tool calls and watch for four-to-five calls per question; (5) the self-observation loop: ask the agent what patterns it saw, then carve out specialists.
- SPINE: 1.
- SLOT: Context Engineering, or Advanced Techniques / Tooling & Setup.
- RELATIONSHIP: 🔗 complements "Benchmarking Tools & MCPs" by being its next step. That video runs competing tools in parallel to pick the best single one; this designs the whole portfolio (low floor plus high ceiling) and derives specialized tools from logged behaviour, so do not re-teach parallel benchmarking, teach stack architecture.
- PROOF TO REUSE: the low-floor/high-ceiling UX framing; the "one silver bullet is the wrong way to go" line; the three-day OpenClaw logging story where the agent recommended tools.

### 3. Why Your Agent Calls The Wrong Tool (And How To Fix It)

- HOOK: The agent called web search instead of your database, and your one-line tool description is why.
- THE PROMISE: For anyone building custom tools, skills, or MCPs, a reliability ladder that makes agents route and parameterize correctly.
- THE SHAPE: (1) Three failure modes: no tool, wrong tool, bad parameters; (2) layer the description: core purpose, trigger conditions, relationships, reinforce in system prompt; (3) parameter complexity as a failure axis; (4) wrap general tools in try/except that returns the error for self-correction; (5) move stubborn syntax into a progressive-disclosure skill (the ESQL wildcard fix).
- SPINE: 3.
- SLOT: Prompt Engineering, Aligning to Your Intent, or Context Engineering.
- RELATIONSHIP: 🔗 complements "Triggering Skills Reliably" by being its tool-side companion. That video covers why skills fail to fire and how to route knowledge-gap invocation; this covers the tool description and parameter craft plus error-returning tools for the custom tools and MCPs you build, so do not re-teach skill triggering, teach tool-description design.
- PROOF TO REUSE: the "tool description is the most important aspect" line; the colleague's hardest problem (stopping the wrong tool call); the percent-vs-asterisk ESQL wildcard fix via a skill; the band-aids-versus-skill argument.

---

## 📚 Full wisdom (reference)

**SUMMARY** — Leonie Monigatti of Elastic argues context engineering is mostly agentic search, walking through semantic search, general query tools, shell retrieval, and agent skills.

**IDEAS**
- Leonie's hot take: context engineering is roughly eighty percent agentic search, powered by the search tools.
- RAG began as a fixed pipeline: the user message became a vector query retrieving chunks automatically.
- Agentic RAG replaced the fixed pipeline with a search tool the agent chooses whether to call.
- Context lives everywhere: local files, scratchpad memory, plan files, databases, the web, and long-term memory stores.
- The shell tool (bash, exec) lets the agent run terminal commands, making retrieval remarkably versatile everywhere.
- Through the shell an agent can grep files, drive a database CLI, or curl HTTPS endpoints.
- Good search is genuinely hard: vector, keyword, dense, sparse, multi-vector embeddings, plus many indexing techniques exist.
- Three failure modes: the agent skips tools, calls the wrong tool, or generates invalid search parameters.
- A colleague's hardest problem was stopping the agent calling web search instead of the database tool.
- Tool descriptions are the biggest lever, yet teams ship lazy one-sentence descriptions then blame the model.
- Layer descriptions upward: core purpose, then trigger conditions, then relationships, then reinforce inside the system prompt.
- Parameter complexity is a failure axis: get-by-ID is easy, writing a full ESQL query is hard.
- Semantic search limited to top three results, no filters, breaks on keywords like the GEPA example.
- A general purpose ESQL tool needs try/except returning errors so the agent can self-correct its query.
- Agent skills use progressive disclosure: description injected upfront, full skill body loaded only when actually needed.
- The ESQL skill taught the wildcard rule, fixing the agent's percent-sign mistake to use asterisk instead.
- Agents cheat at semantic search by chaining synonyms through grep: regulate, compliance, GDPR, governance, sovereignty repeatedly.
- Semantic grep CLIs like Jina's gina-grep let agents run one query and rank matching files immediately.
- Letting the search tool aggregate and count outsources arithmetic agents perform badly and protects the window.

**INSIGHTS**
- The overlooked arrow from sources to window is actually powered by search tools deciding what enters.
- No single silver-bullet search tool exists; curate a stack matching your agent's real search behaviours instead.
- Low floor means specialized tools rarely misfire; high ceiling means general tools handle unexpected complex queries.
- General purpose power costs iterations: flexible tools often need several attempts before reaching the correct answer.
- Zero search results might be a valid answer or a silent failure; decide which per tool.
- Stronger models sharply reduce parameter error rates, but never guarantee error-free general purpose tool use entirely.
- Band-aid instructions per error bloat the system prompt; a loaded skill is the more durable fix.
- Hybrid agents combining database and shell tools verify each other's results, reaching the highest measured accuracy.

**QUOTES**
- "context engineering is about 80% agentic search because it's this little box right here" — Leonie Monigatti
- "if you take home only one thing from today is that doing good search is incredibly difficult" — Leonie Monigatti
- "the tool description is the most important aspect" — Leonie Monigatti
- "it just chains a bunch of synonyms together" — Leonie Monigatti
- "all an agent needs is a shell tool and a file system" — Leonie Monigatti (citing the ongoing discussion)
- "if you just add like little like band-aids every time you run into an error, then what happens when you run into the next edge case?" — Leonie Monigatti
- "having a low floor... where the agent can just use a tool doesn't make many mistakes" — Leonie Monigatti
- "letting the agent do its own calculation, so... outsourcing the calculation part into the search tool, it's actually quite an efficient way" — Leonie Monigatti

**HABITS**
- Leonie logs her agent's behaviour, then reviews patterns to decide which specialized tools to build next.
- She starts with a general purpose tool whenever the agent's query behaviour is not yet understood.
- She always wraps general query tools in try/except so failures return to the agent, not crash.
- She runs shell tools inside a sandbox, since terminal access lets agents delete files or worse.
- She reinforces critical tool relationships both in descriptions and again inside the agent's system prompt directly.
- After three days logging OpenClaw's exec tool, she asked it which recurring patterns it noticed.
- She chooses model strength deliberately: nano for file navigation, mini for writing the harder search queries.
- She uses LangChain to wrap complexity, letting workshops focus on high-level concepts over boilerplate plumbing instead.

**FACTS**
- Elastic is the company behind Elasticsearch; Leonie works there and discusses retrieval publicly and often on Twitter.
- ESQL is Elasticsearch's piped query language for filtering, transforming, and analyzing data, resembling yet unlike SQL.
- In ESQL the wildcard character is the asterisk, not the percent sign used in standard SQL.
- LangChain calls it the shell tool; Anthropic calls it bash; OpenCloud calls it the exec tool.
- Semantic grep alternatives include LlamaIndex's semtools, LightOn's cograg, and Jina's gina-grep, some using multi-vector embeddings internally.
- A Vercel blog post asking whether bash is all you need benchmarked bash, file, database agents.
- In that benchmark the hybrid bash-plus-database agent, verifying results, achieved the highest overall accuracy measured there.
- The demo used GPT-5.4 nano for file navigation and GPT-5.4 mini for writing the ESQL queries.

**REFERENCES**
- Workshop repo: https://github.com/iamleonie/workshop-agentic-search
- Speaker: Leonie Monigatti (https://x.com/helloiamleonie), Elastic; colleague Joe from Elastic joined the Q&A.
- Elastic / Elasticsearch; ESQL (Elasticsearch query language).
- LangChain (shell tool, skill loading tool, skill middleware boilerplate).
- Anthropic bash tool; OpenCloud / OpenClaw exec tool.
- OpenAI GPT-5.4 nano and GPT-5.4 mini.
- Jina embeddings v5; Jina gina-grep; LightOn cograg; LlamaIndex semtools.
- Vercel blog post (roughly "is bash all you need") benchmarking bash, file-search, database, and hybrid agents.
- Anthropic Claude Code referenced as using subagents for niche search tasks.
- Demo data speakers: Bili (AI systems under server constraints), Samuel (GEPA talk), TAS, Pedro; DeepMind Gemma models.

**ONE-SENTENCE TAKEAWAY** — Curate a search tool stack with low floor and high ceiling; retrieval beats the model.

**RECOMMENDATIONS**
- Audit whether your agent skips, misroutes, or mis-parameterizes tools before blaming the model choice itself.
- Rewrite thin tool descriptions to add trigger conditions and relationships whenever the agent routes incorrectly again.
- Wrap any general query tool in try/except so errors return, letting the agent self-correct its parameters.
- Install a semantic grep CLI and tell your agent when to prefer it over exact grep.
- Move syntax the agent repeatedly gets wrong into a progressive disclosure skill rather than the prompt.
- Log every tool call, and when questions need four or five calls, build something more specialized.
- Let search tools do aggregation and counting so the agent avoids unreliable arithmetic and context bloat.
- Combine a database tool with a shell tool so one verifies the other's retrieved results reliably.
