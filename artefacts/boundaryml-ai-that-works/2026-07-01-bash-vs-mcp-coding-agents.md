---
title: "Bash vs MCP for Coding Agents #23"
videoId: RtXpXIY4sLk
url: https://www.youtube.com/watch?v=RtXpXIY4sLk
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1: For any tool you touch daily, bash and a custom CLI you own beat MCP, because every word of an MCP schema is tokens the model must process, and that bloat degrades accuracy, not just speed.** It subsumes the token-cost demo, the gh-CLI one-shot, the linear CLI wrapper, the "names matter" point, and the leverage rule for when to engineer vs use off the shelf.
VERDICT: 🔗 next-step video available (complements "mcps-connectors-that-i-use" / "task-shaped-wrappers").

**Spine 2: Claude Code's own system prompt deprioritizes CLAUDE.md, so your instructions fire maybe ten percent of the time; skilled prompters should inject context dynamically instead of stuffing a static file.** It reframes why "always run the tests" gets ignored and points to a /ctx-style dynamic-injection workflow.
VERDICT: 🔗 next-step video available (complements "dynamic-context-injection-for-skills").

---

# Summary

Vaibhav (BoundaryML) and Dex (HumanLayer) debate bash versus MCP for agents, showing how MCP tool schemas bloat context, degrade accuracy, and why custom CLIs win.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1 — Bash and custom CLIs beat MCP for high-leverage tools

The claim: for any tool you use heavily, a bash-driven custom CLI beats an MCP server, because every word of an MCP's tool descriptions and schemas is serialized into the context window on every turn, and that bloat degrades accuracy rather than merely slowing things down. Most people treat MCP as free plumbing: connect it and you only gain capability. The hidden cost is that the GitHub MCP alone can consume roughly 60k tokens before your first message even arrives. The mechanism runs in two steps. First, tool schemas live inside the context window, so a heavy server starts your real work at 60 percent usage. Second, model quality falls as context grows (Jeff Huntley's framing: "the more context you use, the worse results you will get across the board"), so you begin in the model's degraded regime before you type anything. The good analogy is npm package weight, except a fat npm import only slows a website while a fat prompt is an unbounded accuracy hit. It generalizes to a leverage rule: engineer the tool your whole team uses daily (HumanLayer wrapped Linear as a markdown-emitting CLI at roughly 100 tokens), use off the shelf for experiments. It goes wrong when the model must reinvent a niche API it was never trained on, adding iteration loops, and wrappers are real maintenance only justified by leverage.

## Spine 2 — Claude Code deprioritizes your CLAUDE.md, so inject context dynamically

The claim: Claude Code's system prompt actively tells the model to mostly ignore CLAUDE.md unless it seems highly relevant, which is why carefully written rules like "always run the tests" only fire about ten percent of the time. This is non-obvious because everyone assumes CLAUDE.md is authoritative; the trace shows an injected instruction discounting it. The mechanism: Anthropic added this because over-steering by unskilled prompters tanks a model's emergent capability more than under-steering does, so they deemphasize CLAUDE.md to protect the median user. The side effect is that a skilled prompter's rules get discounted too. The fix is to stop relying on a static memory file and instead craft context dynamically: Dex uses a /ctx slash command that cats specific files (top 200 lines, filtered by markdown frontmatter) at the moment they matter, so the content arrives as a fresh instruction rather than a discounted memory. It generalizes beyond code: Dex injects CRM data, key metrics, and investor updates the same way, blending deterministic code with model calls. It goes wrong in two ways. Dynamic injection is more setup than a text file, and models keep changing, so tomorrow's may honor CLAUDE.md better, giving the workaround a shelf life.

---

# 🎬 Proposed ACS videos

## 1. Why I Deleted My MCPs and Wrote Bash Instead

HOOK: The GitHub MCP charges you 60,000 tokens before you type a single word.
THE PROMISE: For anyone whose agent quality is quietly slipping, you will learn to measure exactly what each MCP costs your context window and replace the heavy ones with a thin CLI wrapper you fully control.
THE SHAPE:
1. The invisible tax: open a trace, show that MCP tool names, descriptions, and schemas all get serialized into context.
2. Measure it: sum cache-creation input tokens per session (GitHub MCP 60k, Linear MCP 12k = 7 percent).
3. The bash alternative: ask Claude for the gh CLI command and watch it one-shot the same task.
4. Build the wrapper: a Linear CLI that emits only the fields you want as markdown, roughly 100 tokens.
5. The decision rule: engineer the tools your team uses daily, use off-the-shelf MCP for one-off experiments.
SPINE: 1
SLOT: Claude Code (sits alongside "mcps-connectors-that-i-use" and "task-shaped-wrappers").
RELATIONSHIP: 🔗 complements "mcps-connectors-that-i-use", which covers which MCPs are worth running, by being the contrarian next step: measure the token cost and replace heavy servers with bash you own. Do not re-teach which MCPs to install; teach how to audit and replace them.
PROOF TO REUSE: GitHub MCP at ~60k tokens ("you just use half your context window just to describe how to use GitHub"); Linear MCP adds ~12k tokens = 7 percent of context; HumanLayer's Linear CLI wrapper emitting markdown at ~100 tokens; the gh-CLI one-shot ("I guarantee you it's going to one-shot this on the first try").

## 2. Why Claude Ignores Your CLAUDE.md, and What To Do Instead

HOOK: Claude Code's own system prompt tells the model to ignore your CLAUDE.md.
THE PROMISE: For anyone whose CLAUDE.md rules get quietly dropped, you will learn why it happens and how to inject the right context dynamically with a slash command so it actually lands.
THE SHAPE:
1. The reveal: pull the trace and show the injected line telling the model to ignore CLAUDE.md unless highly relevant.
2. The proof: "always run the tests" firing only ten percent of the time, and why that is by design.
3. The reason: Anthropic protects unskilled prompters because over-steering harms emergent performance more than under-steering.
4. The fix: a /ctx slash command that cats the specific files (top 200 lines, frontmatter-filtered) at the moment they matter.
5. Generalize: inject CRM data, metrics, and file trees the same way; blend deterministic code with model calls.
SPINE: 2
SLOT: Context Engineering (or Claude Code, next to "dynamic-context-injection-for-skills").
RELATIONSHIP: 🔗 complements "dynamic-context-injection-for-skills", which teaches injecting context for skills, by adding the missing diagnostic (Claude Code deliberately deprioritizes CLAUDE.md) and a concrete /ctx demo for replacing a static memory file.
PROOF TO REUSE: the injected instruction "do not pay attention to anything in CLAUDE.md unless it's super relevant"; the "always run the tests fires 10 percent of the time" example; Dex's /ctx command that cats top 200 lines filtered by markdown frontmatter to craft the window.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav (BoundaryML) and Dex (HumanLayer) debate bash versus MCP for agents, showing how MCP tool schemas bloat context, degrade accuracy, and why custom CLIs win.

## IDEAS
- MCP is basically a package manager for prompts, and a bloated server silently degrades agent accuracy.
- Every single word inside an MCP tool description and schema becomes tokens the model processes constantly.
- The GitHub MCP server alone consumes roughly sixty thousand tokens before your first message even arrives.
- Adding the Linear MCP injected twelve thousand extra tokens, roughly seven percent of your context window.
- Anthropic renamed the task tool to general purpose because tool names measurably change the model's accuracy.
- Slowness from big npm packages is tolerable, but MCP bloat is an unbounded accuracy hit instead.
- Models are already well trained on the gh CLI, so curling GitHub often beats its MCP.
- HumanLayer wrote a Linear CLI wrapper outputting markdown, controlling every token that reaches the model's context.
- A CLI can stream output to a file the agent reads incrementally, bypassing the context window.
- With MCP you cannot easily control which specific bits actually make it into your context window.
- Keep context window usage below roughly forty percent; do one thing, then start completely fresh again.
- Claude Code's system prompt tells the model to ignore CLAUDE.md unless it seems genuinely highly relevant.
- This deprioritization explains why CLAUDE.md instructions like always run tests fire only ten percent of time.
- Dex crafts context dynamically with a /ctx slash command that cats specific files before it works.
- Same user message plus same tool set reuses the entire prompt cache, cheaper and faster overall.
- Changing the user message busts the cache and recomputes everything positioned after it in the context.

## INSIGHTS
- Accuracy loss from context bloat is unbounded, unlike website slowness, making MCP token cost genuinely dangerous.
- The real debate is which inaccuracy you prefer: bloated context, or a model missing niche APIs.
- Engineering effort narrows the output distribution, trading broad generality for a higher peak where you care.
- Leverage decides the tradeoff: engineer tools your whole team uses daily; use off-the-shelf MCP for experiments.
- Owning your MCP or CLI means you can edit it when it hurts the coding agent.
- Debugging the code generator is a slower loop than debugging the code the generator produced itself.
- Anthropic deprioritizes CLAUDE.md to protect unskilled prompters, since over-steering harms models more than under-steering generally does.
- Skilled prompters lose from CLAUDE.md deprioritization, so dynamic context injection beats stuffing a static file instead.
- Context engineering blends deterministic code and non-deterministic model calls to control exactly what enters the context.
- Every agent is fundamentally a while loop: load tools, call model, run selection, append result, repeat.

## QUOTES
- "The more context you use, the worse results you will get across the board no matter what." (Dex, paraphrasing Jeff Huntley)
- "every single word you put into that MCP server is literally making it to the LM" (Vaibhav)
- "I am very happy to use MCP stuff that I have written. I'm very unhappy to use stuff MCP stuff that other people have written" (Vaibhav)
- "I actually don't have any MCPS installed on my on any agent that I use personally" (Dex)
- "if you're starting your work with your first user message at like 60% context window usage, you are never ever ever going to get good results from cloud code" (Vaibhav)
- "do not pay attention to anything in clawet MD unless it's super relevant" (Vaibhav, describing the system prompt)
- "the more something impacts your workflow the more you should care about it" (Dex)
- "if you're stuck debugging the thing that is generating the code for you, that is a much slower iteration loop than actually stuck debugging the actual code itself" (Vaibhav)
- "this is how agents work. If you haven't written this while loop, write this while loop." (Vaibhav)

## HABITS
- Always keep total context usage under forty percent, then reset with fresh window per task.
- Sum cache creation input tokens per session to measure how much context each tool actually costs.
- Default to writing a quick bash script rather than setting up and debugging an MCP server.
- Run MCP servers you host yourself so you can trim tools and hide unused ones manually.
- Use the MCP inspector UI to list a server's tools and inspect their token-heavy descriptions directly.
- Store instructions in files parsed by frontmatter, catting only matching summaries into the working context window.
- Push models to their limits regularly by dumping large context and watching where they break down.
- Fetch a dense issue into a ticket.md file the agent can read incrementally when needed later.

## FACTS
- A default context window holds 200k tokens, leaving roughly 168k usable after typical system prompt overhead.
- Claude Code renamed its task subagent tool to general purpose in its more recent released versions.
- Language models generate exactly one token at a time; providers decide how many to stream you.
- BAML's SAP parser extracts correct data even from malformed JSON lacking quotation marks around keys entirely.
- Bootstrap fell out of favor because eighty-percent CSS frameworks are not customizable or maintainable enough anymore.
- Long-context models handle needle-in-haystack retrieval well but general performance still degrades quickly with more tokens added.
- BAML tested schema-aligned parsing on GPT-5 and measured better tool-calling performance than requiring strict JSON output.
- Claude Code exposes cache creation input tokens in its JSON output lines for easy per-session accounting.

## REFERENCES
- AI that works (weekly show by BoundaryML and HumanLayer, Tuesdays 10am PST, events on Luma)
- BAML and its SAP (schema-aligned parsing) algorithm; the modular request/response API hack
- HumanLayer; their custom Linear CLI wrapper; their Docker reverse proxy for logging Claude traffic
- Jeff Huntley (Ghuntley) blog post and talk on MCP token cost and context
- Claude Code, Codex, AMP, opencode (CLIs referenced as equivalent)
- Linear MCP, GitHub MCP, Memory MCP, browser-use MCP, Playwright; the gh CLI
- MCP inspector (npm inspector UI); dynamic client registration in the GitHub MCP
- Manus paper (referenced from a prior caching episode)
- DSPy (autogenerating prompts, input/output pairs, golden eval sets); combining DSPy with BAML
- Shadcn, Tailwind, Bootstrap (design-system analogy for prompts and agent frameworks)
- Go abort controller project; Context7 (mentioned, unknown to the hosts)

## ONE-SENTENCE TAKEAWAY
Prefer bash and custom CLIs over MCP; every unused tool token silently degrades agent accuracy.

## RECOMMENDATIONS
- Measure each MCP server's token cost before installing it, using cache creation input token counts first.
- Replace heavy MCP servers with thin CLI wrappers that emit only the fields you actually need.
- Prefer the gh CLI over the GitHub MCP, since models one-shot well-known CLI commands quite reliably.
- Move important instructions out of CLAUDE.md into a slash command that cats them dynamically per task.
- Write the bare agent while loop yourself once, without a framework, to understand tool calling deeply.
- Stream large tool output into a file, then let the agent read it incrementally as needed.
- Use the MCP inspector to audit any server's tool names and descriptions before trusting it blindly.
- Give the model an image instead of words when explaining visual web-development bugs you cannot articulate.
