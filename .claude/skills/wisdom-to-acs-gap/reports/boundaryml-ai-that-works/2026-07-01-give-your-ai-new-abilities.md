---
title: The Right Way to Give Your AI New Abilities
videoId: z5inaSXkiTU
url: https://www.youtube.com/watch?v=z5inaSXkiTU
date: 2026-07-01
status: posted
channel: AI That Works (BoundaryML)
---

## The one idea worth a video

**Spine A. MCP's only justifiable use is letting your product's USERS bring their own long-tail tools; anything you the builder control should be a first-class CLI/SDK integration.** Why it is the spine: it reframes the whole "MCP good or bad" debate as a builder decision and subsumes the token-cost, instruction-budget, "don't wrap GitHub in MCP," and first-class-migration beats.
VERDICT: 🔗 next-step video available (complements the scripted `clis-vs-mcps`).

**Spine B. You should shape the exact tool schema the model sees at runtime, using closures to remove dimensions the agent should not reason about.** Why it is the spine: it is a distinct, demo-able tool-design technique (write the closure, collapse the params) with its own slot, not a sub-beat of the MCP-vs-CLI strategy.
VERDICT: ❌ net-new video available.

---

## Summary

Vaibhav (Boundary) and Dexter (HumanLayer) debate MCP on AI That Works podcast: when it helps, why it bloats context, and how to design agent tools.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine A. MCP belongs at the user-extensibility layer, not the builder's integration layer

**The claim.** If you are building an agent product, the only defensible reason to accept MCP is to let your users attach their own long-tail tools; everything you control you should wire in first-class as a CLI or SDK.

**Why it is non-obvious.** The default read is "MCP is the modern way to connect tools," so builders reach for it to talk to GitHub, Linear, or their own APIs. Dexter's line is blunt: "Every other use case is garbage. Don't do it in my opinion. Like do not use MCP to talk to GitHub. Literally just have Claude code use the GitHub CLI."

**Why it is true (the mechanism).** MCP is all-or-nothing: because you do not own the server, you cannot safely whitelist functions (hidden tool-call ordering may break), so every schema loads into context. And "every single function definition in an MCP server is an instruction," so adding an untrusted server "consumed a certain amount of the model's intelligence," making the agent "deterministically worse." Therefore integrations you control belong in code you can trim; MCP earns its place only where the user, not you, owns the tool.

**What it generalizes to.** SaaS extensibility: expose a plugin surface for the long tail, build first-class for the head, and when a user-brought MCP gets popular, that is your "signal to go pull it, migrate it, and build a first-class integration."

**How it goes wrong.** Enterprises that forbid a bash tool cannot shell out to CLIs, so MCP becomes the only door; and "if your customer needs an MCP integration to make the sale, go ship the damn thing." Technical purity is not correctness.

### Spine B. Shape the tool schema at runtime with closures

**The claim.** The method signature you write literally defines the JSON schema handed to the model, so you should generate it dynamically: hide parameters and whole tools that the agent has no business reasoning about.

**Why it is non-obvious.** People expose a generic tool with a `source` param (Jira or Linear or a slug) and let the model choose. Dexter's fix: "If it thinks it can choose from these functions, then it will." Remove the choice. If the user OAuth'd only one source, do not even name the concept of a source.

**Why it is true (the mechanism).** More exposed dimensions mean more instructions competing for attention and more ways to pick wrong. If zero sources are connected you return nothing; if one, you "return a closure over that source"; if many, you return the full multi-source tool. The deterministic side of the system injects what it already knows, so the model is effectively RL'd onto a smaller, sharper tool set.

**What it generalizes to.** Claude Code and OpenCode expose `grep` but run ripgrep underneath, so "it's incorrect to make the agent think about grep versus rip grep." Same move for a working directory: inject it, do not make the agent pass it. A legal chatbot collapses seventy case-law sources into one query.

**How it goes wrong.** It is genuinely hard outside Python: Go, Rust, Java, and even Zod fight dynamic schema generation, "which is kind of why people don't end up doing the right thing." And over-collapsing removes flexibility a power user actually needed, so tie the schema to real runtime state, not guesses.

---

## 🎬 Proposed ACS videos

### 1. The Only Time You Should Reach for MCP

- **HOOK:** You are building an agent and you just added an MCP for GitHub. You picked the wrong tool.
- **THE PROMISE:** For anyone building an agent product: after this you will know the one case MCP is for, and wire everything else first-class.
- **THE SHAPE:**
  1. The flip: as a Claude Code user the CLI-vs-MCP call is about your context; as a builder it is about your users.
  2. The rule: MCP is only for letting users bring long-tail tools you will not integrate yourself.
  3. Everything you control: build first-class OAuth/SDK, expose narrow functions (ticket-github, ticket-linear, all-tickets) instead of one MCP.
  4. The migration ladder: a user-brought MCP that gets popular is your signal to promote it to a first-class integration.
  5. The unpaid tax: show `/context` with an MCP loaded, then the same job on a first-class path.
- **SPINE:** A
- **SLOT:** Advanced Techniques (building agent products/harnesses), or a direct sequel slotted right after `clis-vs-mcps` in Fundamental Techniques > Session & Context Management.
- **RELATIONSHIP:** 🔗 complements `clis-vs-mcps` by being its next step. That video already teaches the Claude Code user "CLI for tools the model knows, MCP for new integrations plus team auth," using the 60,000-token GitHub-MCP fact. This video changes the audience to the agent-product builder and the conclusion: even for integrations you need, build first-class; reserve MCP strictly for user-brought tools, and add the popularity-driven migration ladder that `clis-vs-mcps` does not cover.
- **PROOF TO REUSE:** "The only justifiable reason to use MCP is to let your users bring their own code to attach to your harness." Anthropic builds Claude Code but lets users extend it via MCP. "If someone's MCP starts becoming really popular, that's your signal to go pull it, migrate it, and build a first-class integration."

### 2. Design the Exact Tools Your Agent Sees

- **HOOK:** Your agent keeps picking the wrong tool. The fix is not a better prompt. It is deleting a parameter.
- **THE PROMISE:** For builders writing custom agent tools: after this you can generate tool schemas at runtime so the model only ever sees the choices that actually apply.
- **THE SHAPE:**
  1. The insight: your method signature IS the schema the model receives.
  2. The closure pattern: zero connected sources returns nothing, one returns a closure over that source, many returns the full tool.
  3. Kill the dimension: if there is one source, remove the source param entirely so the model cannot invent a choice.
  4. Inject, do not ask: expose `grep` while running ripgrep underneath; inject the working directory instead of passing it.
  5. The honesty beat: this is hard outside Python (Go, Rust, Zod fight it), which is why most people skip it.
- **SPINE:** B
- **SLOT:** Advanced Techniques > designing-interfaces (currently an empty idea stub; this becomes that video).
- **RELATIONSHIP:** ❌ net-new. `instruction-following-limits` and `progressive-disclosure` cover why fewer instructions help, but nothing in the catalog covers the runtime tool-schema-shaping technique itself; the `designing-interfaces` file is a one-line placeholder with no content.
- **PROOF TO REUSE:** "If it thinks it can choose from these functions, then it will." The closure code Dexter live-writes (zero/one/many source branches). "It's incorrect to make the agent think about grep versus rip grep. You just let the agent think in the form of grep." "You're RLing the model on a way smaller set of tools."

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (Boundary) and Dexter (HumanLayer) debate MCP on AI That Works podcast: when it helps, why it bloats context, and how to design agent tools.

### IDEAS
- MCP is all-or-nothing: you load every schema or none, unlike source code that tree-shakes unused imports.
- You cannot whitelist or blacklist MCP functions safely because hidden tool-call ordering dependencies inside the server.
- Every function definition in an MCP server is an instruction competing for the model's attention budget.
- The GitHub MCP alone costs 50,000 tokens; add HubSpot's 60,000 and you already pass 100,000 immediately.
- The only justifiable MCP use: letting your users attach their own tools to your agent harness.
- If you the builder know what functionality you need, use the SDK or CLI, not MCP.
- Google Cloud SDKs already did dynamic function discovery, fetching schemas from a remote endpoint at runtime.
- Google controls its closed SDK ecosystem; MCP is open, running unaudited, often remote code on you.
- Adding an untrusted MCP consumes model intelligence, making your agent deterministically worse across every scenario immediately.
- Dynamic tool schemas via closures: expose the source parameter only when the user connected multiple sources.
- Remove a directory parameter entirely; let deterministic code inject it instead of making the agent decide.
- Claude Code exposes grep while running ripgrep underneath, so the agent never reasons about the implementation.
- Claude Code moved from MCP to skills because MCP is both too strict and simultaneously insufficient.
- Tool search should keep read, edit, write, grep, bash in context, offloading only the long-tail tools.
- Skills only work with a bash tool; without one, a skill degrades into a prompt module.
- MCP has no native auth; chaining MCP servers forces credential forwarding that leaks how authentication works.
- To secure MCP you must build 'Plaid for MCP': one trusted broker holding credentials for servers.

### INSIGHTS
- The protocol versus package distinction matters: protocols demand a far higher design bar than package managers.
- REST endured by getting descoped to get and post; well-designed protocols extend rather than requiring redefinition.
- Context engineering pushes your jagged frontier outward, letting your agent beat the base market on tasks.
- The 99th-percentile rule: default your API away from choices that ninety-nine percent of engineers would misuse.
- The bitter lesson is survivable: as models improve, your context-engineered frontier extends alongside the base frontier.
- Three alphas exist: agent slightly beating market, superior distribution, or VC money to subsidize burning costs.
- Popular MCP usage is a signal: migrate that into a first-class, context-engineered integration inside your product.
- The method signature you write defines the JSON schema the model receives, so shape it deliberately.
- Browser agents exist only because sites lack auth; a scoped API call always beats clicking buttons.
- Fine-grained, time-boxed, signed permissions (rich authorization) would let agents act within deterministic, revocable, narrow guardrails today.

### QUOTES
- "MCP is kind of like an all or nothing game. You get the MCP or you don't get the MCP." (Vaibhav)
- "every single function definition in an MCP server is an instruction." (Dexter)
- "I think that is the only justifiable reason to use MCP to let your users bring their own code to attach to your harness." (Vaibhav)
- "Every other use case is garbage. Don't do it in my opinion. Like do not use MCP to talk to GitHub." (Dexter)
- "the minute you add an MCP that you're not trusting that you don't really control, you've basically consumed a certain amount of the model's intelligence." (Vaibhav)
- "Claude is just the laziest engineer out there that just happens to be really fast at typing code." (Vaibhav)
- "there's a reason Claude Code stopped pushing MCP as much and moved towards skills." (Vaibhav)
- "the bar for a protocol is infinitely higher than the bar is for a package." (Vaibhav)
- "MCP cannot withstand the test of time because it tries to live up to the bar of a protocol." (Vaibhav)
- "skills only work if you have a bash tool." (Dexter)
- "technical purity is not correctness here." (Dexter)
- "MCP is really a poor man's attempt of trying to build a app store-like ecosystem." (Vaibhav)
- "If you look at what the Claude code team says, they fight for every tool that gets added into there." (Dexter)

### HABITS
- They audit high-frequency tools relentlessly, questioning every parameter and description to keep agent quality climbing steadily.
- They check Claude Code's slash-context command to see exactly how many tokens MCPs and skills consume.
- They default to shelling out to off-the-shelf CLIs for uncommon tasks, optimizing only proven high-frequency paths.
- They build first on beefy reasoning models, then optimize prompts for cheaper models once usage justifies.
- They educate users through application code, prompting them to disable MCPs that haven't been called recently.
- They prefer multiple explicit functions over one clever function, since most engineers won't write harder versions.
- They audit Claude-generated tool code, since the model takes the laziest first approach unless carefully checked.
- They give users visualization tools first, then gradually provide ways to improve their own context usage.

### FACTS
- The GitHub MCP server consumes roughly 50,000 tokens; HubSpot's MCP adds about 60,000 more before use.
- Google Cloud SDKs call a schema endpoint at import time, building function trees dynamically at runtime.
- Boto3, the AWS SDK, lacks native autocomplete for the same dynamic-schema reason Google Cloud SDKs do.
- Twitter's 2011 API pioneered dropping HTTP methods, using only get and post for nearly all operations.
- Models enter a 'dumb zone' once about 20 to 30 percent of context becomes rot in-window.
- A subset of the OAuth specification, called rich authorization, lets clients sign narrowly-scoped, parameterized permission tokens.
- GitHub and Stripe are both known for state-of-the-art fine-grained access tokens with many individually-checkable permission scopes.
- Plaid acts as a trusted middleman so websites never receive a user's actual bank login credentials.
- Vercel shipped a bash tool running in an emulated environment, enabling powerful sandboxed shell execution safely.

### REFERENCES
- Boundary / BAML (Vaibhav's programming language and company)
- HumanLayer (Dexter's company)
- AI That Works podcast (weekly, Tuesdays); April 11 live "unconference" in San Francisco
- MCP (Model Context Protocol); MCP Inspector (npx mcp inspector); mcp-remote
- Linear MCP, GitHub MCP, HubSpot MCP, Jira MCP
- Google Cloud discovery-based SDKs; Boto3 (AWS SDK)
- LangChain, CrewAI (early agent frameworks); Zod (TypeScript schema)
- Claude Code (slash-context command, skills, subagents, commands, tool search); Codex (Dexter was on the team)
- OpenCode; ripgrep
- GitHub personal access tokens / fine-grained tokens; Stripe scoped API keys
- JWTs; YubiKey; Face ID / passkeys; Rich Authorization (OAuth spec subset)
- Plaid; OAuth; REST; gRPC; Protobuf; "Twitter REST" (2011)
- Vercel bash / sandbox tool
- Kyle (Dexter's co-founder, on context rot)

### ONE-SENTENCE TAKEAWAY
Use MCP only for user-brought tools; everything you control should be a deliberately context-engineered CLI.

### RECOMMENDATIONS
- Replace your GitHub MCP with the gh CLI and let Claude Code write the needed commands.
- Run slash-context in Claude Code to measure how many tokens your MCPs and skills currently consume.
- Reserve MCP for letting your product's users attach their own long-tail tools you won't integrate first-class.
- Write dynamic tool schemas: return a closure for one source, the full tool for many sources.
- Strip parameters the agent shouldn't reason about, injecting them deterministically from your application's known runtime state.
- Audit every high-frequency tool: challenge each parameter, tighten each description, remove anything the model doesn't need.
- Keep read, write, edit, grep, and bash always in-context; offload only long-tail tools behind tool search.
- Prompt users to disable MCPs your agent hasn't called recently, protecting their context from silent bloat.
- Treat popular user-brought MCPs as a signal to promote them into first-class, context-engineered product integrations soon.
