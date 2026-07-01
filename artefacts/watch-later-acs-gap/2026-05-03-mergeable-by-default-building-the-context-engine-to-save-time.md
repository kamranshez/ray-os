---
title: "Mergeable by default: Building the context engine to save time and tokens, Peter Werry, Unblocked"
video_url: https://www.youtube.com/watch?v=5ID22ACI7IM
video_id: 5ID22ACI7IM
channel: AI Engineer
published: 2026-05-03
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Mergeable by default: Building the context engine to save time and tokens, Peter Werry, Unblocked**](https://www.youtube.com/watch?v=5ID22ACI7IM) - AI Engineer - uploaded 2026-05-03

> Two next-step ACS videos available: mining your repo's history into expert context, and the "satisfaction of search" retrieval failure.

## The one idea worth a video

- **Bottle your codebase experts (spine 2).** Distill who owns each code area and the review conventions they repeatedly enforce from your own git and PR history, then load that as seed context before the agent starts. VERDICT: 🔗 next-step video available.
- **Satisfaction of search (spine 1).** Agents stop retrieving at the first plausible finding and miss the context that actually matters, the rejected past approaches and the why-decisions buried in Slack and incident reports. VERDICT: 🔗 next-step video available.
- **Access does not equal understanding (spine 3).** A pile of MCP servers plus naive RAG plus a bigger context window is not a context engine; you need a reasoning layer that resolves conflicts and personalizes. VERDICT: ✅ already covered by ACS.

## Summary and counts

Peter Werry of Unblocked explains why context engines, not naive RAG or MCP servers, give coding agents the organizational understanding needed to ship correct code.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 2, Bottling the expert

The claim: your repository already encodes who owns what and which conventions get enforced, so distill that from git and PR history into loadable "expert" context the agent seeds from before it writes anything. Most people assume an exploratory agent can just rediscover this each run. Werry's counter is mechanical: to reconstitute a real expert map the agent would have to write and run a social-graph algorithm every single time, so you short-circuit it by precomputing once. The build has clear steps: construct a graph from PR authorship and review relationships (a page-rank-like pass), derive the experts per code area, then distill each expert's past PR comments and decisions into memories that auto-load when someone touches that area. The proof is the Richie moment: Unblocked's review told an author to dry up duplicated tests, a best practice distilled from earlier PRs whose author was Richie himself. It generalizes cleanly to ticket enrichment and incident timelines. It goes wrong when you count naively (PRs submitted versus reviewed produces wrong team clusters), when synthesis crosses permission boundaries, or when a noisy junior drowns out real signal.

### Spine 1, Satisfaction of search

The claim: coding agents stop retrieving the moment they hit something that looks like an answer, so they miss the context that actually matters. This is non-obvious because everyone blames lack of access, when the real failure is a behavioral stopping bias that persists even with full access wired up. The mechanism runs in two steps: the agent rips around the codebase and docs, finds a superficially plausible explanation, treats the search as satisfied, and locks in a plan, but the golden nuggets (rejected past approaches, deleted code, incident reports, the why-decisions in old Slack threads) live where it never thought to look, so a shallow-but-plausible hit produces a confident wrong plan and a doom loop. The term is borrowed from radiology, where technicians who spot one finding that explains the symptoms stop and miss a second tumor. It generalizes to code review, where a reviewer catches the obvious diff issue and quits. It goes wrong on the other side too: over-corrected, the agent searches forever, burns tokens, and hits compaction.

### Spine 3, Access does not equal understanding (covered, no pitch)

The claim: wiring up MCP servers and RAG gives an agent access to data but not understanding of the relationships between it, and a bigger context window will not close the gap. The mechanism: access hands over raw documents, but understanding requires resolving conflicts (what is true when a doc and the main branch disagree), knowing why past decisions were made, and respecting who is asking. A million-token window is good at needle-in-a-haystack but cannot reason across conflicting sources, and most organizations already hold more than a million tokens of context anyway. This is the video's overarching reframe and it subsumes the three myths, but ACS already teaches it: "Why Search Isn't Enough" makes the case that access and keyword search miss tribal knowledge, and "The Context Layer" is the build-your-own answer. Load-bearing for understanding the talk, so it keeps this deep dive, but it earns no pitch and does not count toward the post gate.

## 🎬 Proposed ACS videos

### 1. Bottle Your Codebase Experts: Mine Git History Into Context Your Agent Loads First

- **HOOK:** Your repo already knows who owns what and which conventions get enforced; the agent just never reads it.
- **THE PROMISE:** For teams whose agents keep ignoring local conventions, build a skill that turns your PR history into expert memories the agent loads before it touches the code.
- **THE SHAPE:** (1) Build a lightweight social graph from PR authorship and review pairs, run locally with a PR limit. (2) Derive the experts and owners per code area. (3) Distill repeated PR review comments into named best-practice memories. (4) Wire those memories to auto-load when the agent works in that area. (5) Show the before and after on a real task.
- **SPINE:** 2, bottling the expert.
- **SLOT:** Context Engineering, The Solution Paradigm (sits beside "The Context Layer").
- **RELATIONSHIP:** 🔗 complements "The Context Layer," which teaches building the externalized context layer by hand (root guidance, semantic boundary nodes, skills, invariants, examples). This adds the missing next step: how to auto-populate that layer by mining your own git and PR history and expert map, rather than authoring every node manually.
- **PROOF TO REUSE:** the Richie anecdote (the convention was distilled from his own PRs); "bottling the expert" as a retrieval pivot point that steers the agent's next move; the local, all-offline social graph builder demo; expert-weighted human feedback.

### 2. Satisfaction of Search: Why Your Agent Stops Digging Before It Finds the Real Answer

- **HOOK:** Agents quit at the first plausible finding, exactly like a radiologist who misses the second tumor.
- **THE PROMISE:** For anyone whose agent confidently ships the wrong plan, learn to spot premature-stop retrieval and force it to keep looking in the places that hold the real context.
- **THE SHAPE:** (1) Name the failure and its radiology origin. (2) Show an agent stopping early and missing a rejected past approach. (3) Add a "keep digging past the first hit" instruction plus a checklist of non-obvious sources (closed PRs, incident reports, old Slack threads). (4) Show the corrected plan. (5) Warn about the opposite failure, the agent that searches forever and hits compaction.
- **SPINE:** 1, satisfaction of search.
- **SLOT:** Context Engineering, Foundations (sits beside "Why Search Isn't Enough").
- **RELATIONSHIP:** 🔗 complements "Why Search Isn't Enough," which teaches why keyword discovery is unreliable in large or old repos and misses tribal knowledge. This adds the specific named behavioral bias (the agent stops at the first plausible match even with access) and the concrete anti-premature-stop technique, rather than just arguing for a context layer.
- **PROOF TO REUSE:** the radiology origin of the term; the iceberg meme (original intent, rejected approaches, deleted code all sit below merely compiling code); the doom-loop consequence; "where you've been tells it what not to do, where you're going tells it what to do."

### Also film-able (not deep-dived)

- **Output tokens, not input tokens, are your real latency tax.** Time to first output token is already optimized, so front-load high-signal context to kill doom loops rather than trimming input. Rough slot: Techniques, Session and Context Management (beside "Economising with Prompt Cache" and "Long Context Failure"). Adjacent to existing token work, likely a short 🟡.
- **Surface conflicts, never cache answers.** A context system should admit when it cannot resolve truth and ask the human, and must never recycle old answers as context or it regresses to a polluted mean. Rough slot: Context Engineering, Foundations. Likely 🟡 next to "The One-Pattern Rule" and "Reducing Agent Confusion."

## 📚 Full wisdom (reference)

**SUMMARY.** Peter Werry of Unblocked explains why context engines, not naive RAG or MCP servers, give coding agents the organizational understanding needed to ship correct code.

**IDEAS**
- Context engineering supplies all context an agent needs and, crucially, none of the context it doesn't.
- Satisfaction of search: agents stop at the first plausible finding and miss the real golden context.
- Access does not equal understanding; wiring up many MCP servers cannot reveal relationships between your data.
- Naive RAG over your docs is not a context engine; conflicts and personalization both go unresolved.
- A bigger context window fails you: models find needles but cannot reason across many conflicting sources.
- Most organizations already hold more than a million tokens of context, overflowing any single model window.
- Bottling the expert: distill an individual's past decisions and PR comments into loadable seed context memories.
- A social graph of PR reviews reveals your real teams and who owns each code area.
- Conflict resolution by recency alone is naive; main branch is truth, except where you're heading matters.
- Where you've been tells the agent what not to do; where you're going tells what to.
- Flow access controls upward: private Slack channels answer questions only for people already permitted to see.
- Never cache a context engine's answer to reuse later; code, docs, and reasons change constantly underneath.
- Feeding previous answers back as context makes the model regress toward a polluted, misbehaving mean output.
- Surface conflicts you cannot resolve; a context engine should admit uncertainty and learn from user input.
- Output tokens, not input tokens, drag agent performance; time to first output token is already optimized.
- Planning is where context engines pay off most, followed closely by review, triage, and incident management.
- Agent context collection consumes roughly ninety percent of task time; actual code writing is very fast.

**INSIGHTS**
- Retrieval time is a microcosm of implementation time, so front-loaded high-signal context slashes the whole task.
- The humans became the bottleneck: context switching across parallel agents creates painful cognitive disconnect without automation.
- Valuable context is submerged: original intent, rejected approaches, and deleted code hide beneath merely compiling code.
- Good AI-generated code should feel written by a colleague embedded in your team for twenty years.
- Experts act as retrieval pivot points: their distilled learnings steer the agent's next directional search move.
- Graph RAG unavoidably crosses permission boundaries, so synthesis must stay compartmentalized within accessible repositories and channels.
- As agents grow autonomous, MCP latency matters less; getting the answer exactly right matters far more.
- Success is measured in vibes: rising user sentiment beats any single benchmark for these context systems.

**QUOTES**
- "access doesn't mean understanding" (Peter Werry)
- "AI generated code should just feel like it was written by someone that's been in your team for like 20 years" (Peter Werry)
- "we optimized for access not understanding" (Peter Werry)
- "we hid conflicts instead of surfacing them" (Peter Werry)
- "the puck is going down down the line towards background agents for sure" (Peter Werry)
- "bleeding edge today is like yesterday's news in six months" (Peter Werry)
- "where you've been helps it understand what not to do. where you're going helps it understand what you should do" (Peter Werry)
- "the more high quality correct like high signal context you have up front the better every single thing the agent's going to do until it says it's done" (Brandon)

**HABITS**
- Werry triages production issues by whacking them into an agent connected to the context engine immediately.
- Always give the social graph builder a PR limit or time range, or it runs forever.
- They run best-practice distillation weekly, since organizational conventions change slowly compared with everyday source code changes.
- They wire Claude Code into CI with an API key to run context-aware background jobs autonomously.
- For sensitive setups they still recommend cloud over on-prem, which lags behind on patches and maintenance.
- They bias conflict resolution first to recency, then to the main branch as source of truth.

**FACTS**
- The adaptive-thinking task took 2.5 hours and 21 million tokens without the context engine switched on.
- With the context engine, the same task finished in 25 minutes using just 10 million tokens.
- Early coding models operated with roughly eight thousand token context windows, forcing heavy manual token optimization.
- Satisfaction of search originates in radiology, where technicians immediately stop after finding one symptom-explaining x-ray abnormality.
- Unblocked reports its customer sentiment around 60 on a scale running from minus 100 to 100.
- Across users, Claude Code is Unblocked's most used agent, followed by Cursor, then surprisingly Claude Desktop.
- At 20-30 person teams they see hundreds of user feedback signals; larger teams see hundreds more.

**REFERENCES**
- Unblocked (the context engine product, MCP server, CLI, dashboard, Slack and Teams surfaces; repo to be MIT-licensed open source).
- Anthropic adaptive thinking mode and the older explicit thinking-token-budget method (the benchmark task).
- Gemini (first model to ship a million-token window, strong at needle-in-a-haystack).
- Andrej Karpathy (the "LLM wiki" idea, treating a wiki like a file system agents traverse).
- Boris Cherny (Claude Code creator, interview on measuring success internally via vibes and sentiment).
- "Mythos" (a code-intelligence model release described as near-perfect at code intelligence).
- Sentry and Datadog (incident management integrations); Slack, Microsoft Teams, Notion, Confluence (data sources).
- GraphRAG (the layered pyramid summarization that unavoidably crosses permission boundaries); Composio (cited for high tool-use token usage).
- Vim (adoption-curve slide borrowed); Andrej ("systems are intelligent") on reaching the exponential in code intelligence.

**ONE-SENTENCE TAKEAWAY.** Give agents distilled, personalized context, not more tools, so generated code respects hard-won institutional reasoning.

**RECOMMENDATIONS**
- Bring your context engine into the planning phase first, where it delivers the biggest measurable return.
- Build reusable curation skills in a GitHub repo, like ticket-enrich, that call your context engine directly.
- Wire an incident agent to Sentry and Datadog so it relates signals to past incident discussions.
- Run the social graph builder locally against your own repo to reveal experts per code area.
- Seed the agent with expert context before starting, since it cannot hydrate its memory reliably itself.
- Distill repeated PR review comments into memories that load when someone touches that same code area.
- Let humans correct agent answers in natural language; weight corrections by the responder's measured expertise level.
- Give any long codebase-mining agent a bounded scope upfront, or it burns tokens and stalls badly.
