---
title: Claude for non-code tasks #20
videoId: NJcph4j9sNg
url: https://www.youtube.com/watch?v=NJcph4j9sNg
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Claude Code is a general-purpose agent: run your whole back office (CRM, release notes, standups) on interlinked markdown files, because it writes its own scripts instead of needing an MCP per service.**
Because the harness is tuned for reading and writing files, markdown-that-points-at-markdown fakes a relationship graph with zero tool integrations, and any missing capability is a throwaway script away.
VERDICT: net-new video available.

**2. You are still context-engineering as a user, so proxy Claude Code to read its real system prompt, and discover CLAUDE.md is injected with a suffix that tells the model it may not be relevant.**
The "IMPORTANT" lines you write get quietly deprioritized, and seeing the raw prompt also tells you to say "launch a task," not "launch a sub-agent."
VERDICT: net-new video available.

**3. Pack context deterministically with a front-matter index plus a make print-context command, instead of trusting agentic search or stuffing everything into CLAUDE.md.**
A high-signal index at the top of each file plus a script that assembles your core context gives the model maximum signal and minimum noise, cheaply and repeatably.
VERDICT: next-step video available.

---

## Summary

BAML's Vaibhav and HumanLayer's Dex show how Claude Code handles non-coding work through markdown-as-database CRMs, deterministic context packing scripts, release-note SOPs, and practical system-prompt inspection.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: Markdown as database, Claude Code runs the back office

**The claim.** You can run real operations, a CRM, release notes, daily standups, investor updates, entirely on Claude Code, with interlinked markdown files as the database and no SaaS or per-service MCP. **Why it is non-obvious.** The reflex is to reach for Salesforce, Airtable, or at minimum an MCP tool per system; markdown feels too lossy to be a system of record. **Why it is true.** Claude Code's harness is exquisitely tuned to read and write files in a repo, so the only "tool calls" are file reads and writes. Markdown files that point at each other fake a relationship graph, with front matter carrying deterministic metadata and the body carrying prose for the model. Crucially, because Claude writes its own scripts on demand, any missing capability (fetch files modified in the last day, pull metrics) is a quick TypeScript script rather than a vendor integration. As Dex put it, "Claude Code runs our CRM." **What it generalizes to.** Any internal ops surface: release notes from merged PRs, standups reconstructed from Git branch diffs, monthly investor updates compacted from daily reviews. **How it goes wrong.** It is not perfect; markdown is the lossiest V0, you migrate to SQL only once scale demands, and tasks needing clean or exact output should drop down to real code.

### Spine 2: Proxy the system prompt, and why your CLAUDE.md gets ignored

**The claim.** As a user you are still doing context engineering, just with fewer levers, so you should proxy Claude Code to read its real system prompt, tool descriptions, and subagent instructions. Do that and you find CLAUDE.md is injected with a suffix telling the model the content "may or may not be relevant" and to ignore it unless highly relevant. **Why it is non-obvious.** People treat CLAUDE.md as authoritative and write "this is really important," never realizing the harness explicitly discounts it. **Why it is true.** Claude Code just makes a network call, so pointing it at a logging proxy exposes the raw body: system message, the task tool description (what people call subagents), and the CLAUDE.md block with its deprioritizing suffix. Since the model is told to discount that block, instructions you need guaranteed cannot live only there. Reading the exact tool wording also sharpens prompts: say "launch a task," not "sub-agent." **What it generalizes to.** Any agent or MCP: read the tool descriptions and phrase requests in the tool's own vocabulary, and debug refusals by inspecting what was actually sent. **How it goes wrong.** You cannot edit the suffix except by rewriting in the proxy layer, proxying adds setup, and the system prompt shifts across versions.

### Spine 3: Deterministic context packing beats agentic search and CLAUDE.md

**The claim.** Instead of letting the agent search agentically or dumping everything into CLAUDE.md, pack context deterministically: a front-matter index atop each file plus a Makefile or /ctx command that assembles exactly the slices you always need. **Why it is non-obvious.** The default is to trust the built-in LS and grep tools or to overload CLAUDE.md; both burn context and dilute the model's attention. **Why it is true.** Claude Code auto-reads only roughly the first hundred lines of a long file, so putting recent, high-signal information and links at the top lets the model judge relevance cheaply, exactly like docstrings at the top of a source file. A make print-context script then assembles the core context every run, giving maximum signal and minimum noise without the model spending turns searching, and you wrap it in a /ctx slash command. As Vaibhav framed the hierarchy: best is giving the model the answer, second is closely related data, third is minimizing noise. CLAUDE.md is the wrong home precisely because of its deprioritizing suffix. **What it generalizes to.** Large source files (docstrings) and any RAG index design. **How it goes wrong.** As the corpus grows the script must prune to recent projects, and over-managing every word matters less as models improve.

---

## 🎬 Proposed ACS videos

### 1. Run Your Company on Markdown: Claude Code as Your CRM and Back Office
- HOOK: They deleted their CRM. Now Claude Code runs the whole thing on markdown files.
- THE PROMISE: For founders and operators who want to automate back-office work without buying more SaaS; after this you can stand up a working CRM and daily-ops system on markdown alone.
- THE SHAPE: (1) The thesis: Claude Code writes its own scripts, so you rarely need an MCP per service. (2) Build the markdown CRM: contacts, events, engagement history as interlinked files. (3) Front matter for deterministic metadata, body for the model. (4) Wire a daily-review SOP and a release-notes SOP. (5) When to migrate to SQL.
- SPINE: 1.
- SLOT: My Daily Workflows (or Business class), new chapter "Run Ops on Claude Code."
- RELATIONSHIP: ❌ net-new. The catalog has "Airtable Memory for Cloud Scheduled Tasks" (an Airtable-backed memory) and Business-class briefs like skills-as-team-knowledge-base and lead-research-and-outreach, but nothing teaches markdown-as-database replacing a CRM with no vendor tool. This is a distinct system-of-record pattern.
- PROOF TO REUSE: "Claude Code runs our CRM." The burrito-delivery fictional company demo. Markdown files pointing at each other to fake a relationship graph. Standup updates reconstructed for free from Git branch diffs.

### 2. Show Me the Prompt: Proxy Claude Code and Why Your CLAUDE.md Gets Ignored
- HOOK: Your "IMPORTANT" CLAUDE.md line is being ignored on purpose. Here is the proof, in the raw system prompt.
- THE PROMISE: For anyone frustrated that CLAUDE.md instructions do not stick; after this you can read Claude Code's real system prompt and put critical instructions where the model will actually respect them.
- THE SHAPE: (1) Point Claude Code at a logging proxy and capture the request. (2) Read the raw body: system message, tool descriptions, the task (subagent) tool. (3) Find the CLAUDE.md suffix that says "may not be relevant." (4) Consequence: stop trusting CLAUDE.md for must-follow rules. (5) Bonus: match the tool's wording ("launch a task," not "sub-agent").
- SPINE: 2.
- SLOT: Context Engineering class, chapter "Understanding the System" (sits alongside what-breaks-if-i-change-this).
- RELATIONSHIP: ❌ net-new. Catalog has self-modifying-claude-md, global-claude-md-personal-profile, and delete-your-readme, all about writing CLAUDE.md; none teach proxying the network call to read the real system prompt or expose the deprioritizing suffix. It also complements those by explaining why they can silently fail.
- PROOF TO REUSE: "You can literally just point Claude at a proxy and have it log everything out." The exact suffix: "this context may or may not be relevant... only consider it if highly relevant." Saying "launch a task" to hit the task tool.

### 3. Deterministic Context Packing: A make print-context Command Beats Agentic Search
- HOOK: Stop letting the agent grep around. Hand it a packed context with one make command.
- THE PROMISE: For people whose agents waste turns searching or drown in CLAUDE.md; after this you can build a deterministic context-packing command and a /ctx slash command that front-loads exactly the right context.
- THE SHAPE: (1) Why agentic search and CLAUDE.md are the wrong defaults. (2) Front-matter index at the top of every file, mirroring docstrings. (3) Build make print-context and make print-index. (4) Wrap it in a /ctx slash command. (5) The signal hierarchy: answer, then related data, then minimize noise.
- SPINE: 3.
- RELATIONSHIP: 🔗 complements the shipped Context Engineering class, which teaches the principles of shaping context; this adds the concrete deterministic-packing implementation (front-matter index plus a Makefile plus a slash command) and the reason to keep it out of CLAUDE.md. State up front what the CE class already teaches so Ray does not re-teach the principles.
- SLOT: Context Engineering class, new chapter "Deterministic Context Packing" (adjacent to refactoring-to-save-on-context and dynamic-context-injection-for-skills).
- PROOF TO REUSE: Claude Code reads only the first ~100 lines of a long file. The /ctx command running make print-context then following the user's ask. "Give it as little noise about what isn't relevant so it can do the right thing."

**Also film-able (not deep-dived):** The software 3.0 to 1.0 optimization spectrum, prototype a workflow as a loose prompt or SOP, then collapse repeated Claude Code calls into one deterministic TypeScript script once it stabilizes, choosing determinism by your error tolerance. Slot: Techniques class (near refactoring-to-save-on-context / task-shaped-wrappers). Proof: four Claude Code calls collapsed into one metadata script for cost and latency.

---

## 📚 Full wisdom (reference)

**SUMMARY.** BAML's Vaibhav and HumanLayer's Dex show how Claude Code handles non-coding work through markdown-as-database CRMs, deterministic context packing scripts, release-note SOPs, and practical system-prompt inspection.

**IDEAS.**
- Claude Code doubles as a general-purpose agent, writing its own scripts instead of needing MCP tools.
- HumanLayer replaced their CRM entirely with markdown files that Claude Code reads, writes, and freely cross-links.
- Markdown files pointing at each other fake a relationship graph without SQL database or tool calls.
- Front matter holds deterministic index metadata; the document body holds free-form prose written mostly for models.
- A Makefile packs context deterministically, dumping first hundred lines of files instead of slow agentic searching.
- Claude Code auto-reads only the first hundred lines of long files when first opening them initially.
- Put recent, high-signal information atop each markdown file so the model judges relevance without reading everything.
- Collapsing four repeated Claude Code calls into one script saves money, latency, and repeated context rebuilding.
- Claude Code caches at most four segments, so huge repeated contexts still cost real money anyway.
- SOPs become prompts and slash commands; prototype workflows loosely, then bake stable parts into TypeScript scripts.
- Proxying Claude Code's network calls reveals its full system prompt, tool descriptions, and subagent task instructions.
- Claude Code suffixes injected CLAUDE.md with "this may not be relevant," quietly deprioritizing your own instructions.
- Say "launch a task," not "launch a sub-agent," matching the tool's actual internal prompt wording exactly.
- Agents versus workflows is the wrong frame; error tolerance decides how deterministic your system must become.
- Non-coding tasks are still engineering; you just choose which abstraction level, like choosing Python versus C.
- Always be compacting: keep a markdown source-of-truth file separate from the disposable running chat log itself.
- Wrapping the Linear MCP in a script pulls comments cleanly without dumping JSON into your context.

**INSIGHTS.**
- You become a better agent builder by first becoming a demanding, frustrated, opinionated agent user yourself.
- Every user, not just builders, does context engineering; users simply control fewer levers than the builders.
- Over-abstracting a tool lowers its ceiling; exposing internals lets power users min-max their own results dramatically.
- The best context move is handing the model the answer; second best is closely relevant data.
- When perfect exact data is hard, minimize noise so the model isn't distracted by sheer irrelevance.
- Markdown-as-database is the lossiest V0 form; migrate to a SQL database only when scale truly demands.
- Performance engineering and context engineering share one rule: optimize only the parts that actually need it.
- If a working system stops working, only then open the black box and debug it properly.
- Taking over a user's context lifts the floor for novices but lowers the ceiling for experts.

**QUOTES.**
- "I actually become a better agent builder by becoming a better agent user." (Vaibhav)
- "LLMs are stateless functions." (Dex)
- "The only thing that kind of affects the quality of this answer, if you're using a fixed LLM and kind of fixed parameters, is the quality of the tokens you put in." (Dex)
- "Claude Code runs our CRM." (Dex)
- "The best thing you can do in forms of context engineering, whether as a user or as a developer, is give the answer to the model and that's it." (Vaibhav)
- "You now have stand-up updates for free backed by sources of truth." (Vaibhav)
- "Thing is working, don't bother understanding it. The model's good enough, it's working. The minute it stops working, go figure out why." (Vaibhav)
- "I've never read the source code of the cat command and I have no no reason to or desire to, cuz the API is clean and it always does what it says." (Dex)
- "By taking over the user's context completely, while you do lift the floor a little bit, the thing that you don't do is you actually bring down the ceiling a lot." (Vaibhav)
- "The median right now is pretty bad." (Vaibhav)
- "The thing we're doing that Dex is showing you may very well be exactly what engineering is 5 years from now." (Vaibhav)

**HABITS.**
- They run their entire CRM as markdown files in a Git repo, using no CRM SaaS.
- Every single morning Dex runs a daily-review SOP and brain-dumps everything currently on his busy mind.
- They use Opus for everything, accepting roughly a dollar per make command for reliable quality output.
- They prefer /clear over /compact, writing custom prompts that squeeze context into a single markdown file.
- They wrap noisy MCPs like Linear in scripts that fetch comments without polluting the context window.
- They use a /ctx slash command that runs make print-context before following the user's actual ask.
- They spawn subagents per Git branch to summarize diffs when generating loose, quick team standup updates.
- They write design docs through Claude first, deferring implementation details until the interface is fully settled.

**FACTS.**
- Claude Code's only truly primitive tool is bash; higher-level tools like read-file reduce model effort substantially.
- Adding cancellation to BAML took roughly seven hours and around thirty-five thousand lines of generated code.
- Three BAML engineers previously spent four days each attempting that cancellation feature without ever merging it.
- Claude Code injects CLAUDE.md content but appends a system instruction saying it may not be relevant.
- Claude Code supports at most four cache segments, limiting savings on very large repeated context windows.
- Claude Code lets you run background tasks but cannot make later tasks reliably depend on them.
- You can inspect Claude Code's system prompt by pointing it through a logging network proxy layer.
- BAML is a programming language being built in Rust; CodeLayer is HumanLayer's open-source coding CLI tool.

**REFERENCES.** BAML (BoundaryML), HumanLayer, CodeLayer, the "AI That Works" show, Claude Code, Claude Opus, Cursor, Obsidian, Linear (and its MCP), Salesforce, Airtable, GitHub, the GH CLI, Superhuman, Andrej Karpathy's software 1.0/2.0/3.0 framing, Makefiles, TypeScript, Bun, WebAssembly (WASM), the SWE-agent tool chain, Luma, Discord.

**ONE-SENTENCE TAKEAWAY.** Claude Code is a general-purpose agent: run your non-code work as markdown plus deterministic scripts.

**RECOMMENDATIONS.**
- Replace a lightweight SaaS CRM with interlinked markdown files that Claude Code reads and updates directly.
- Put a deterministic front-matter index atop every document so agents assess relevance without full file reads.
- Build a make print-context command that packs your core context deterministically instead of slow agentic searching.
- Collapse repeated Claude Code calls into a single TypeScript script once the underlying workflow clearly stabilizes.
- Encode manual recurring tasks as SOP slash commands, prototyping loosely before hardening into deterministic scripted code.
- Proxy Claude Code's traffic to read its real system prompt and tool descriptions for yourself directly.
- Stop relying on CLAUDE.md for critical instructions; inject them deterministically through a context-packing command approach instead.
- Choose determinism by your error tolerance: write real code only where accuracy genuinely matters the most.
- Keep a markdown source-of-truth file you can re-feed after clearing to restore an agent's full context.
