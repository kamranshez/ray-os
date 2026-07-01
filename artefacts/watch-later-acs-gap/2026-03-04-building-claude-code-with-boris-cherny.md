---
title: Building Claude Code with Boris Cherny
video_url: https://www.youtube.com/watch?v=julbw1JuAz0
video_id: julbw1JuAz0
channel: The Pragmatic Engineer
published: 2026-03-04
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Building Claude Code with Boris Cherny**](https://www.youtube.com/watch?v=julbw1JuAz0) - The Pragmatic Engineer - uploaded 2026-03-04

> net-new ACS video available (1 net-new, 2 complements): agentic search beats RAG, the lint-rule ratchet, and uncorrelated context as test-time compute

## The idea worth a video

1. **Agentic search (glob plus grep) now beats a RAG or vector database for navigating a codebase.** Anthropic built the embedding index, then deleted it once the model could just search. VERDICT: net-new video available.
2. **Make nondeterministic AI review reliable by ratcheting its recurring findings into deterministic lint rules.** Boris tells Claude to write a lint rule for each repeated review comment. VERDICT: next-step video available.
3. **The magic of parallel agents is uncorrelated context windows acting as test-time compute, not the agent configuration.** Fresh windows explore independently, so aggregating them raises answer quality. VERDICT: next-step video available.

## Summary and counts

Boris Cherny, creator of Claude Code, details Anthropic's workflow: parallel plan-mode agents, layered verification, agentic search over RAG, and uncorrelated context windows as test-time compute.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: Agentic search over RAG

The claim: for letting an agent navigate a large codebase, plain agentic search (glob plus grep) now beats a purpose-built RAG or vector-database retrieval layer. It is non-obvious because the papers and the conventional instinct say to index your code into embeddings for semantic retrieval, so most teams reach for a vector DB first. The mechanism: Boris built exactly that, a local TypeScript vector database with cloud-computed embeddings, and hit three structural problems. The index drifted out of sync (a function you just wrote is not indexed yet, so RAG cannot find it), permissioning the index safely is hard (who can read it, how do you stop a rogue IT person reaching someone else's data), and once the model got good enough it could simply grep. Because the model can iteratively run glob and grep, read results, and refine, it retrieves against live ground truth instead of a stale snapshot, so freshness and accuracy both rise while the security surface disappears. This generalizes to any internal knowledge tool: letting an agent search the raw source of truth beats maintaining a parallel embedding store you have to keep synced and permissioned. How it goes wrong: on truly massive monorepos naive grep can be slow, and this leans on a capable model, so weaker models still benefit from structured retrieval. Boris: "agentic search, this is a fancy word for glob and grap. That's all it is."

### Spine 2: The deterministic ratchet (lint rules from AI review)

The claim: the way to make nondeterministic LLM code review trustworthy is to ratchet its recurring findings into deterministic checks, having Claude write a lint rule for each repeated comment. It is non-obvious because teams treat AI review as a straight replacement for human review and worry it will miss things precisely because it is nondeterministic; the fix is not a better prompt, it is converting judgment into determinism. The mechanism: Kirk raises exactly this concern, that an LLM reviewer might catch an issue on one run and miss it the next. Boris's old habit at Meta was to tally every review comment in a spreadsheet and, once a pattern recurred three or four times, write a lint rule for it. Now he tells Claude "write a lint roll for this" directly on the PR, so that class of bug is caught deterministically from then on and never needs human attention again. Layer that under Claude reviewing every PR in CI (which catches roughly 80% of bugs) plus a required human final pass and you get Swiss-cheese reliability. This generalizes to any agent output you review repeatedly: promote recurring corrections into automated guardrails rather than re-catching them by hand. How it goes wrong: not everything is lintable (taste and architecture are not), and over-linting creates noise that trains people to ignore the linter.

### Spine 3: Uncorrelated context windows as test-time compute

The claim: the real reason parallel agents, subagents, and swarms improve output is that each uncorrelated (fresh) context window is a form of test-time compute, not any particular agent configuration. It is non-obvious because people obsess over how to wire up a multi-agent system, the roles, prompts, and handoffs, assuming the topology is the magic. Boris locates the magic upstream: "throwing more context at the problem, when the windows are uncorrelated gives you better results. it's actually a form of test time compute." The mechanism: a correlated second task shares the first task's context window and inherits its framing and its mistakes, whereas an uncorrelated window starts fresh knowing only its prompt, so N independent windows explore genuinely different paths, and aggregating them (best-of-N, majority vote, or a dedup pass) raises the odds of a correct answer the same way more sampling does. This also yields a clean decision rule: reach for a subagent when you want fresh uncorrelated context, reach for a skill or slash command when you want the parent context, because skills see the parent window and subagents do not. It generalizes to hard bug hunts and complex builds: spin up several fresh agents rather than pushing one long thread. How it goes wrong: it burns a lot of tokens (which is why agent teams are opt-in), and uncorrelated windows lose shared state, so tasks needing tight coordination suffer.

## 🎬 Proposed ACS videos

### 1. Delete Your Vector Database: Why Grep Beats RAG for Codebases

- **HOOK:** Anthropic built a codebase RAG system, then threw it away because glob and grep won.
- **THE PROMISE:** For engineers building agents on large codebases, stop maintaining an embedding index and retrieve against live source instead.
- **THE SHAPE:**
  1. Show the intuitive but wrong instinct: index the repo into a vector database.
  2. Build a tiny RAG retrieval demo and expose the drift problem (a just-written function is not indexed).
  3. Replace it with Claude doing glob plus grep agentically on the same query.
  4. Compare freshness and permissioning side by side, and close on the Instagram "foo(" origin story.
- **SPINE:** Agentic search over RAG.
- **SLOT:** Context Engineering (Tackling large-scale production codebases), or Techniques > Working with the Codebase.
- **RELATIONSHIP:** ❌ net-new. The catalog has no RAG-versus-grep or retrieval-architecture video; the closest hits ("1M Token Context" for intake, "Reducing Agent Confusion in Growing Projects") are about context intake and codebase hygiene, not whether to build a retrieval layer at all.
- **PROOF TO REUSE:** the thrown-away local TypeScript vector DB with cloud embeddings; the three failure modes (drift out of sync, index permissioning, rogue IT person); the Instagram global-index "foo(" search that inspired it; quote "agentic search... is a fancy word for glob and grap. That's all it is."

### 2. Make AI Code Review Deterministic: Turn Every Review Comment Into a Lint Rule

- **HOOK:** LLM review is nondeterministic, so Boris ratchets each recurring comment into a lint rule that never misses.
- **THE PROMISE:** For teams relying on AI review, convert repeated findings into permanent deterministic checks instead of re-catching the same bug forever.
- **THE SHAPE:**
  1. Frame the nondeterminism problem: the reviewer catches a bug today, misses it tomorrow.
  2. Boris's Meta spreadsheet tally, then the three-strikes lint rule.
  3. Demo: ask Claude to write a lint rule directly on a PR from a repeated nit.
  4. Stack the layers: Claude reviewing every PR in CI plus a required human final pass (Swiss cheese).
- **SPINE:** The deterministic ratchet.
- **SLOT:** Master Claude Code > Built-In Skills (beside /code-review), or Master Claude Code > Hooks.
- **RELATIONSHIP:** 🔗 complements "/code-review", which teaches deep LLM bug-hunting review with finder and verifier stages. That video shows how to run the review; this one adds the move after: promoting the reviewer's recurring findings into deterministic lint rules so that class of bug is caught for free from then on, addressing the nondeterminism /code-review cannot fix on its own.
- **PROOF TO REUSE:** Kirk's explicit nondeterminism question about marrying LLM review with linting; the Meta spreadsheet-to-lint-rule habit ("more than three or four instances I would write a lint rule"); "at Claude, please write a lint roll for this in that PR"; claude in CI catching "maybe like 80% of bugs"; the Swiss cheese model quote.

### 3. Uncorrelated Context Windows: The Real Reason Parallel Agents Win

- **HOOK:** The magic of subagents and swarms is not their configuration, it is fresh context acting as test-time compute.
- **THE PROMISE:** For anyone orchestrating agents, learn when parallel fresh contexts beat one long thread, and why.
- **THE SHAPE:**
  1. Define correlated versus uncorrelated context windows with a concrete example.
  2. Show subagent (fresh) versus skill or slash command (sees parent) and the decision rule that follows.
  3. Demo best-of-N: three fresh agents plus a dedup pass on one hard bug.
  4. Scale up to agent teams and swarms, and explain why they are token-hungry and opt-in.
- **SPINE:** Uncorrelated context as test-time compute.
- **SLOT:** Advanced Techniques > Multi-Agent Orchestration.
- **RELATIONSHIP:** 🔗 complements "Multi Subagents for Hard Problems", which shows spawning read-only strategy subagents and implementing the convergent fix. That video teaches the tactic; this one adds the WHY (uncorrelated context is a form of test-time compute) plus the subagent-versus-skill decision rule that generalizes it beyond stubborn bugs to any parallel workload.
- **PROOF TO REUSE:** Boris's correlated-versus-uncorrelated definition; "it's actually a form of test time compute to do this"; the subagent-sees-fresh versus skill-sees-parent distinction; the weekend swarm that built the plugins feature (hundreds of agents, 100 Asana tasks); agent teams shipped as opt-in research preview "because it uses a ton of tokens."

### Also film-able (not deep-dived)

- **Retry What Failed: Re-testing Old Ideas as Models Improve** - because a newer model can succeed where an older one failed, systematically re-run techniques you abandoned (RAG, microservices, a workflow that broke). Rough slot: Techniques or Advanced Techniques. Not covered; "Gravitional Pull from Older Models" teaches the inverse (old code dragging new models down).

## 📚 Full wisdom (reference)

### SUMMARY
Boris Cherny, creator and head of Claude Code, tells The Pragmatic Engineer how Anthropic builds software when agents write most of the code.

### IDEAS
- Boris joined Anthropic, wrote his first pull request by hand; Adam rejected it for being handwritten.
- "Clyde," Claude Code's janky Python predecessor, one-shotted a working PR once Boris held the tool right.
- Boris gave the model a single bash tool; it wrote AppleScript to report his playing music.
- Do not put the model in a box; give it tools and let it run freely.
- Claude Code writes roughly 80% of Anthropic's code on average; Boris writes essentially none himself now.
- Switching to Opus 4.5, Boris uninstalled his IDE because he no longer needed to edit code.
- Boris runs five terminal tabs, five repository checkouts, starting each Claude in plan mode cycling round-robin.
- Once a plan is good, Opus 4.5 or 4.6 one-shots the implementation almost every single time.
- Boris starts several coding agents from his phone each morning; they run in Anthropic's cloud environment.
- Every Anthropic pull request is reviewed by Claude in CI, catching roughly 80% of bugs first.
- Boris turns recurring review comments into lint rules, telling Claude to write them on PRs directly.
- Claude Code spontaneously launches itself in a subprocess to end-to-end test that it still works correctly.
- Best-of-N: tell Claude to start three agents, then parallel dedup agents to remove false positives afterward.
- Anthropic threw away its local vector database; agentic search, meaning glob and grep, outperformed everything else.
- RAG drifted out of sync: new local functions were unindexed, and index permissioning raised security concerns.
- Prompt injection is defended in three layers: model alignment, runtime classifiers, and sub-agent web-fetch result summarization.
- Uncorrelated context windows, throwing fresh tokens at a problem, act as a form of test-time compute.
- Subagents get fresh uncorrelated context; skills and slash commands instead see the parent context window directly.
- A swarm ran an entire weekend, spawned hundreds of agents, and built the plugins feature shipped.
- Boris built twenty interactive to-do-list prototypes in a day and a half, then chose by feel.

### INSIGHTS
- The model is not a component in your program; it is its own tool-using thing entirely.
- Nondeterministic AI review becomes reliable when its recurring findings are ratcheted into deterministic lint rules permanently.
- Agentic search beat RAG because the model improved enough to navigate codebases with plain tools alone.
- Parallelism helps because uncorrelated context windows add test-time compute, independent of the specific agent configuration used.
- Because building is now cheap but aim is uncertain, prototype many options and choose by feel.
- Ideas that failed with an older model deserve retrying, since a newer model may succeed now.
- Safety uses a Swiss cheese model: many imperfect layers together drive the failure probability down sharply.
- Understanding the layer beneath your work still matters; today that lower layer is the model itself.
- The uniform "member of technical staff" title assumes everyone does everything, inverting default cross-discipline collaboration here.
- Coordination systems built for humans, specs and task boards, now organize swarms of collaborating agents instead.

### QUOTES
- "when I say agentic search, this is a fancy word for glob and grap. That's all it is." - Boris Cherny
- "every pull request at Enthropic is code reviewed by quad code... and that actually catches maybe like 80% of bugs" - Boris Cherny
- "Opus 4.5 and quad code wrote 100% of every single one. I didn't edit a single line manually" - Boris Cherny
- "the way to think about it is the model is its own thing. You give it tools... but you don't make it a component of this larger system" - Boris Cherny
- "just let the model do it do its thing. Don't try to put it in a box." - Boris Cherny
- "it turned out that agentic search just outperformed everything" - Boris Cherny
- "uncorrelated context windows and just throwing more context at the problem... gives you better results. Um, it's actually a form of test time compute to do this." - Boris Cherny
- "the model is improving so quickly that the ideas that worked with the old model might not work with the new model." - Boris Cherny
- "it's actually not crazy to just try the same idea every few months because the model improves and it just works." - Boris Cherny
- "we don't really write stuff. We just we show." - Boris Cherny
- "if you're building some personal side project like you can just yolo straight to main" - Boris Cherny
- "it's a Swiss cheese model. You just need a bunch of layers and with enough layers, the probability of catching anything goes up." - Boris Cherny

### HABITS
- Boris keeps five parallel repository checkouts and starts each Claude Code session in plan mode first.
- He starts a few coding agents from his phone every morning before touching a computer keyboard.
- When a coworker's PR is lintable, Boris asks Claude to write a lint rule there immediately.
- He uses the GitHub app daily, tagging @Claude on any pull request or open issue directly.
- Boris uses co-work weekly with a Chrome extension, pinging engineers on Slack about unfilled spreadsheet rows.
- He runs Claude in plan mode across tabs, revisiting each only when notified it finished planning.
- Boris throws away most code he writes, keeping only prototypes that genuinely feel good enough afterward.
- He avoids ticketing systems personally, managing his own work directly rather than through a tracking board.
- Boris prototypes fifteen-plus variations, tries them himself, then shares only the ones that felt right afterward.

### FACTS
- Boris authored the first TypeScript book with O'Reilly and founded the world's largest TypeScript meetup ever.
- Before Anthropic, Boris spent seven years at Meta, eventually leading code quality across all products there.
- Meta's "Better Engineering" program mandated engineers spend twenty percent of time fixing accumulated technical debt constantly.
- Meta measured that code quality contributes double-digit percentage points to overall engineering productivity through causal analysis.
- Claude Code's first internal release in September 2024 already shipped the run-once-or-always permission prompt system unchanged.
- Claude Code adoption at Anthropic is essentially 100% of technical employees and approaching 100% overall now.
- Claude Cowork was built end-to-end in ten days, entirely with Claude Code, using Electron and TypeScript.
- Claude Code was not overnight; growth turned exponential in May with Opus 4 and Sonnet 4.
- Anthropic cannot view user data for privacy, so debugging relies on privacy-preserving event logging entirely.

### REFERENCES
- People: Adam Wolf, Ben Mann, Fiona Fun, Jared Sumar, Vlad Klesnikov, Will Bailey, Mike Krieger, Dario Amodei, Cat Woo, Daisy, Suzanne, Karen, Felix (co-worker on Electron), Andrej Karpathy, Marc Andreessen, Anders Hejlsberg, Chris Cowell (General Theory of Reactivity), Ryan Dahl (Node), Joe Pamer.
- Tools and tech: Clyde (Claude Code predecessor), Claude Code, Claude Cowork, agent teams / swarms, plugins, Claude Agent SDK, claude -p, the open-source code-review skill in the Claude Code repo, git worktrees, session-start hooks, Statsig, Sonar / SonarQube MCP, WorkOS, Bolt.js, ReactJS, GraphQL, HHVM, Hack, Relay, Django, Electron, TypeScript, Scala, Haskell.
- Companies: Meta, Instagram, Facebook, WhatsApp, Messenger, Anthropic, Y Combinator, Agile Diagnosis, Uber, Google, Microsoft, Reddit.
- Concepts: the bitter lesson, the printing press analogy, the Swiss cheese safety model, RAG, uncorrelated context windows, Meta's Better Engineering program, member of technical staff.
- Books: Programming TypeScript (Boris Cherny); Liu Cixin short-story collections (the Three-Body Problem author); Accelerando by Charles Stross; Functional Programming in Scala.

### ONE-SENTENCE TAKEAWAY
When AI writes all your code, your job becomes designing verification layers and orchestrating agents.

### RECOMMENDATIONS
- Start every task in plan mode, iterate the plan, then let Claude one-shot the implementation cleanly.
- Run several parallel checkouts or worktrees so multiple agents work without interfering with each other simultaneously.
- Add Claude as a CI reviewer on every pull request to catch most bugs early automatically.
- Whenever a review comment recurs, have Claude write a permanent lint rule catching it deterministically forever.
- Delete your codebase vector database, and let Claude search with glob and grep agentically instead now.
- For genuinely hard tasks, run best-of-N: several agents plus dedup agents removing the false positives afterward.
- Prototype many interactive variations quickly, try each yourself, and keep only what genuinely feels right afterward.
- Retry techniques that failed a few months ago; a newer model may now handle them fine.
- Configure session-start hooks so cloud and phone agents inherit your environment for consistent parallel runs everywhere.
- Defend against prompt injection in multiple layers: alignment, runtime classifiers, and summarizing fetched web content safely.
