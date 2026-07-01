---
title: "Spec-Driven Development: Agentic Coding at FAANG Scale and Quality — Al Harris, Amazon Kiro"
video_url: https://www.youtube.com/watch?v=HY_JyxAZsiE
video_id: HY_JyxAZsiE
channel: AI Engineer
published: 2026-01-09
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Spec-Driven Development: Agentic Coding at FAANG Scale and Quality — Al Harris, Amazon Kiro**](https://www.youtube.com/watch?v=HY_JyxAZsiE) - AI Engineer - uploaded 2026-01-09

> net-new ACS video available: make agent output provably correct with property tests derived from your spec (plus two next-step complements)

## The idea worth a video

**1. Machine-verifiable specs: turn structured requirements into property-based tests and auto-scan them for ambiguity.** Kiro closes the gap between the agent saying "done" and the code provably meeting the spec, by parsing EARS requirements into invariants a falsifying test hunts to break.
VERDICT: ❌ net-new video available

**2. Plan with your tools on: use MCP servers in the requirements and design phases, not just implementation.** Most people wire MCP for execution; the leverage is feeding tickets and live docs into the plan so errors surface at design time.
VERDICT: 🔗 next-step video available

**3. Your prompt anchors the agent: after it designs, make it argue for the idiomatic alternative.** Anything you state "rounds" the agent toward it, so a detailed prompt can railroad the design unless you invite dissent.
VERDICT: 🔗 next-step video available

## Summary + counts

Al Harris, Amazon principal engineer, demonstrates Kiro's spec-driven development: turning prompts into EARS requirements, designs, property tests, and executable tasks for reproducible, high-quality agentic coding.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 — Machine-verifiable specs (EARS requirements → property tests + ambiguity scan)

**The claim.** Kiro parses structured natural-language requirements into machine-checkable invariants, so "done" means the code provably satisfies the spec rather than the model saying so.

**Why it's non-obvious.** Most people trust the agent's self-report or eyeball the diff. Al is blunt that anybody who has used an agent can testify the models are very good at saying "I'm done, I'm happy" while the tests quietly fail and the agent moves on.

**Why it's true.** EARS ("when X, then the system shall Y") is structured enough to parse without an LLM; each requirement becomes an invariant; property-based testing (Hypothesis, fast-check, Clojure spec) then searches for a single case that falsifies it. Find a counterexample and the requirement is unmet; find none and you get high confidence (Al concedes "high" is doing heavy lifting). Separately, automated reasoning scans requirements for ambiguity and conflicting constraints before any code exists, so the throughline runs requirement to verified code.

**What it generalizes to.** In Claude Code, write acceptance criteria in EARS, have the agent emit Hypothesis or fast-check property tests, and use those as a deterministic verifier gate instead of the model's word. Same idea powers API contract testing.

**How it goes wrong.** Property quality caps the confidence; PBT cannot test what you never specified; prototyping phases may not warrant it.

### Spine 2 — Use MCP servers to author the spec, not just to execute

**The claim.** Your MCP servers belong in requirements and design, not only implementation: pull tickets in, and ground decisions in live docs while the plan is still being written.

**Why it's non-obvious.** "What I think people don't do enough is use their MCPs when they're building their specs." People reach for MCP at execution time (run the migration, hit the API), leaving the plan ungrounded.

**Why it's true.** The plan is where architectural decisions get locked. If the agent drafts requirements from an Asana ticket via MCP and grounds the design against an AWS-docs MCP, mistakes get caught at design time (cheap) instead of implementation time (expensive), left-shifting the concerns. In the demo it was the docs MCP that surfaced LangGraph's native persistence, which the operator did not know existed.

**What it generalizes to.** Claude Code plan mode plus a Linear or Jira connector to seed requirements, plus a docs MCP (Context7, Exa) to ground library choices before code is written.

**How it goes wrong.** Changing MCP config mid-session is a caching operation that slows deep sessions; too many enabled tools bloat context; the agent may still ignore a docs MCP ("flip of a coin whether it discovers it").

### Spine 3 — Your prompt anchors the agent; ask for the idiomatic alternative

**The claim.** Anything you put in the prompt "rounds" the agent toward it, so after the agent produces a design you should explicitly ask "is this idiomatic? what are the alternatives?" to surface the better path you did not know existed.

**Why it's non-obvious.** People assume a detailed prompt is purely good. Al shows his implicit "dump conversations to an S3 file" instruction biased the entire design, even though Agent Core memory was the more idiomatic answer. "Anything you put in the prompt is effectively rounding the agent, for better or for worse."

**Why it's true.** The agents are "very easy to please" and will faithfully build what you said; because they defer to your stated approach, the better idiomatic option never surfaces unless you invite dissent. Asking mid-flow for alternatives makes the agent research (via its MCP tools) and propose options to compare.

**What it generalizes to.** In Claude Code, after plan mode produces a plan, ask "what would you do if I had not told you to use X?" before accepting. Applies squarely to architecture and library selection.

**How it goes wrong.** Al notes this normally takes "pretty hard" prompting; the easy-to-please agent may rubber-stamp your bias; you still must evaluate the alternatives it returns.

## 🎬 Proposed ACS videos

### 1. Make Your Agent Prove It: Property Tests From Your Spec
- **HOOK:** Your agent says "tests pass, done." It lied. Here is how to make "done" mean provably correct.
- **THE PROMISE:** For engineers shipping agent-written code to production: turn acceptance criteria into property tests so "done" is deterministic, not the model's word.
- **THE SHAPE:** (1) write acceptance criteria in EARS when-then-shall form; (2) have the agent translate each into an invariant; (3) generate Hypothesis or fast-check property tests that hunt a falsifying case; (4) wire them as the verifier gate; (5) scan the requirements for ambiguity and conflicting constraints before coding.
- **SPINE:** 1
- **SLOT:** Techniques → Debugging & Verifying Output (or a new "Spec Verification" chapter)
- **RELATIONSHIP:** ❌ net-new. ACS verifier content (Builder Verifier Pattern, Don't Verify Against the Plan, Checking After Spec Developer) teaches LLM-as-judge and adversarial review; none teach deterministic property-based tests derived from structured requirements.
- **PROOF TO REUSE:** the EARS "when-then-shall" example; "the LMS are very good at saying I'm done"; property test defined as "a single test case that falsifies the invariant"; Kiro's requirements scan for "over ambiguity" and "conflicting requirements" via automated reasoning.

### 2. Plan With Your Tools On: MCP In the Requirements Phase
- **HOOK:** You connect MCP servers to write code. The bigger win is connecting them to write the plan.
- **THE PROMISE:** For anyone using plan mode: pull tickets and live docs into requirements and design so mistakes get caught before code exists.
- **THE SHAPE:** (1) connect a ticket MCP (Asana, Linear, Jira) and a docs MCP; (2) generate requirements straight from a ticket URL; (3) during design, make the agent ground library choices against the docs MCP; (4) left-shift errors to design time; (5) avoid re-editing MCP config mid-session for caching reasons.
- **SPINE:** 2
- **SLOT:** Master Claude Code → MCP Servers (or Techniques → Planning Before Implementing)
- **RELATIONSHIP:** 🔗 complements "Starting in Plan Mode" (which teaches that planning lets the agent search the codebase, find patterns, and ask clarifying questions) by adding external MCP data sources feeding the plan itself; also the next step beyond the "MCP Servers" setup video, which stops at installation and permissions.
- **PROOF TO REUSE:** "use their MCPs when they're building their specs"; the Asana-task-to-requirements demo; the AWS-docs MCP surfacing LangGraph native persistence; "changing MCP is a caching operation."

### 3. Your Prompt Is Biasing the Agent: Ask For the Idiomatic Way
- **HOOK:** The instruction you were proud of just railroaded your agent into the wrong architecture.
- **THE PROMISE:** For engineers who write detailed prompts: spot prompt-anchoring and make the agent surface the better option you did not know existed.
- **THE SHAPE:** (1) recognize any stated approach in your prompt anchors the design; (2) let the agent produce its first design; (3) ask "is this idiomatic? what are the alternatives?"; (4) make it research via a docs MCP; (5) compare options before committing.
- **SPINE:** 3
- **SLOT:** Prompt Engineering → Aligning to Your Intent (or Advanced Techniques → Cleaning Up Legacy Code)
- **RELATIONSHIP:** 🔗 complements "Avoiding 'Code Bias' Caused Loops" (which covers how loading bad existing config biases the agent toward additive patches, fixed by asking a fresh chat for an ideal config) by adding the distinct prompt-authored bias case and the "ask for the idiomatic alternative mid-design" move.
- **PROOF TO REUSE:** "anything you put in the prompt is effectively rounding the agent"; the S3 versus Agent Core memory story; "all of these agents are going to be very easy to please"; "is this the idiomatic way to achieve session persistence?"

## 📚 Full wisdom (reference)

**SUMMARY.** Al Harris, Amazon principal engineer, demonstrates Kiro's spec-driven development: turning prompts into EARS requirements, designs, property tests, and executable tasks for reproducible, high-quality agentic coding.

**IDEAS**
- Kiro compresses the whole software development lifecycle into a tight requirements, design, and execution inner loop.
- Vibe coding relies on the operator getting guardrails right; spec-driven development bakes those guardrails into structure.
- EARS, the easy approach to requirement syntax, expresses acceptance criteria as structured when-then-shall natural language statements.
- Property-based testing translates each requirement into an invariant a falsifying test case tries hard to break.
- Kiro scans requirements for ambiguity and conflicting constraints, resolving them with classic automated reasoning techniques today.
- You can invoke your MCP servers in every spec phase: requirements generation, design, and final implementation.
- Kiro reads an Asana task URL through MCP and generates requirements from that assigned ticket's metadata.
- Because specs are natural language, you can inject ASCII wireframe mocks directly into the design artifact.
- Tasks can embed explicit unit test cases that must pass before that task counts as complete.
- Anything you put in the prompt rounds the agent toward it, whether for better or worse.
- Asking the agent for the idiomatic alternative surfaced Agent Core memory over the operator's S3 bias.
- Steering docs behave like memory or cursor rules, encoding commit style, deployment commands, and project priorities.
- Kiro writes learned deployment pain into a steering doc so the lesson persists across future sessions.
- Specs mutate over time: Kiro diffs the requirements rather than accreting endless new markdown spec files.
- The Kiro team replaced design-doc reviews with spec reviews blasted into their internal wiki via MCP.
- Each task runs as a fresh session seeded only with the specification, sharing no prior context.
- The agent performs better with less context but tools to self-discover where the relevant code lives.

**INSIGHTS**
- Structure, not raw LLM output, is what lets Kiro build reproducible tooling atop the living spec.
- The spec is three things: point-in-time artifacts, a structured workflow, and reproducibility tools layered on top.
- Upfront spec investment trades a little latency for far higher accuracy and reproducible delivery outcomes overall.
- Left-shifting UI mocks and test cases into design catches disagreements before costly implementation time actually arrives.
- Kiro is not merely an LLM with a workflow; a neurosymbolic amalgam handles different task types.
- LLMs will cheerfully declare completion while tests fail, so verification must never trust their own self-reports.
- Well-separated, highly cohesive codebases let agents traverse and modify them almost as effectively as human developers.
- Prompt caching hit rate, not summarization, drives Kiro's speed and cost decisions during long working sessions.
- The rigid requirements, design, and tasks flow exists because structure enables deterministic tooling raw prompting cannot.

**QUOTES**
- "vibe coding is great, but vibe coding relies a lot on me as the operator getting things right" - Al Harris
- "anybody who's used an agent can probably testify that um the LMS are very good at saying I'm done" - Al Harris
- "Anything you put in the prompt is effectively rounding the agent. Um, for better or for worse." - Al Harris
- "you should not lock yourself into the rigid flow that is sort of the starting point here" - Al Harris
- "what I think people don't do enough is use their MCPs when they're building their specs" - Al Harris
- "we want to use classic automated reasoning techniques to give you high quality results not just you know whatever the latest model is going to tell you" - Al Harris
- "our agent is not just an LLM with a workflow on top of it" - Al Harris
- "all of these agents are going to be very easy to please" - Al Harris
- "if I spend an hour generating a design doc reviewing it with my team and then synthesizing from that I wanted to get it right" - Al Harris
- "once I go through that pain of learning I just say kira write what you learned into a steering doc" - Al Harris
- "the agent does ... better when given less context but given the tools to understand where to go find things" - Al Harris
- "you're not just talking to like Sonnet or Gemini or whatever. You're talking to sort of an amalgam of systems" - Al Harris

**HABITS**
- Al asks Kiro to add MCP servers by describing them rather than pasting JSON config manually.
- He avoids tweaking MCP or tool config deep into sessions because caching invalidation slows things dramatically.
- He runs all spec tasks together, finding that more understandable and higher-performing than running them individually.
- After learning a fussy deployment flag, he has Kiro summarize the lesson into a steering doc.
- He challenges the agent mid-design, asking whether its proposed approach is actually the idiomatic one here.
- He steers commit attribution so Kiro-authored commits are co-authored, distinguishing them from his own manual work.
- He adds a documentation MCP server so the agent grounds decisions in authoritative vendor docs directly.
- He vibe codes the scaffolding first, then switches to spec-driven development for the meaningful feature work.

**FACTS**
- Kiro launched public preview around July 14th; general availability arrived on the recent Monday, the 17th.
- EARS stands for the easy approach to requirement syntax, a widely used structured natural-language requirement format.
- Established property-based testing tools include Python's Hypothesis, Node's fast-check library, and Clojure's built-in spec library today.
- Kiro is a Code OSS fork, just like Cursor and Windsurf, built atop VS Code itself.
- Kiro's auto mode runs with a roughly 200k token limit, similar to Sonnet's own context window.
- Al reports achieving 90 to 95 percent cached token usage per turn in normal Kiro use.
- Kiro's current summarization can take up to 30 or 45 seconds, a horrendous user experience today.
- Kiro was built by three or four engineers, funded from the org supporting Amazon Q Developer.
- A cold request without caching would send roughly 160,000 tokens straight to Amazon Bedrock each time.

**REFERENCES**
- Kiro (Amazon agentic IDE, Code OSS fork); Kiro CLI (recently rebranded); Kiro Desktop; custom agents in the CLI.
- EARS (Easy Approach to Requirement Syntax); property-based testing; Hypothesis (Python), fast-check (Node), Clojure spec library.
- MCP servers used: Asana, GitHub, fetch, Brave/Tavily search, AWS documentation MCP, plus Al Harris's Nobel Prize MCP and lofty-views sample app (both public on GitHub).
- AWS: Agent Core (runtime + memory feature), Bedrock, CDK, DynamoDB, S3, the use-aws tool / AWS SDK, Amazon Q Developer.
- LangGraph (agent framework with native persistence/checkpointing).
- Tessl (spec-for-knowledge-base conference earlier that week; Tessl "level 7" docs mentioned).
- Kiro features: steering docs, agent hooks, MCP integration, code search / codebase indexing, requirements verification, summarization.
- Tooling: husky, commitlint, prettier, eslint, TypeScript, Node.js.
- LLMs referenced: Anthropic Sonnet, Google Gemini; the Anthropic API's tool-ordering requirement (drove Kiro's message-history sanitizer spec).
- Kiro blog (kiro.dev/blog) with property-based-testing accuracy benchmarks; a distinguished database engineer's blog post on specs; upcoming re:Invent talk.
- Concepts: ADR (architecture decision record), waterfall, XP, incremental disclosure, neurosymbolic reasoning.

**ONE-SENTENCE TAKEAWAY.** Invest upfront in structured, verifiable specs so agents deliver reproducible, provably correct software at scale.

**RECOMMENDATIONS**
- Write your acceptance criteria in EARS when-then-shall form so non-LLM tools can parse them deterministically reliably.
- Generate property-based tests directly from your requirements so completion means provably correct, not the model's word.
- Feed your MCP servers into the requirements and design phases, not just the implementation step alone.
- Pull tickets straight from Asana or Jira through an MCP server to seed your requirements automatically.
- After the agent designs something, ask whether its approach is idiomatic and request several concrete alternatives.
- Add wireframe mocks and explicit unit test cases directly into your design and task artifacts today.
- Capture hard-won deployment lessons into a steering doc so agents stop repeating the same painful mistakes.
- Keep the agent's context small; give it tools to self-discover relevant code rather than dumping everything.
- Mutate existing specs with diffs instead of accreting endless new markdown spec files over project time.
- Avoid changing MCP config mid-session, since cache invalidation will dramatically slow a long deep working session.
