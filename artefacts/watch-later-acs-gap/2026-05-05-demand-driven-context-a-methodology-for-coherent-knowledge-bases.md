---
title: "Demand-Driven Context: A Methodology for Coherent Knowledge Bases Through Agent Failure"
video_url: https://www.youtube.com/watch?v=_QAVExf_1uw
video_id: _QAVExf_1uw
channel: AI Engineer
published: 2026-05-05
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Demand-Driven Context: A Methodology for Coherent Knowledge Bases Through Agent Failure**](https://www.youtube.com/watch?v=_QAVExf_1uw) - AI Engineer - uploaded 2026-05-05

> 1 net-new ACS video available (context gap scanner) plus 2 complements; post-worthy.

## 1. The ideas worth a video

**Spine 1 (flagship): Demand-driven context.** Do not curate context top-down; give agents real tasks, watch them fail, and let each failure name exactly which undocumented knowledge to write. This subsumes the green/orange/red taxonomy, pull-vs-push, the TDD analogy, and the failure-checklist cycle.
VERDICT: 🔗 next-step video available (complements existing CLAUDE.md / context-layer teaching)

**Spine 2: The context gap scanner.** Point an agent at your archive of past tickets and incidents and have it measure, not fix, how much of your knowledge base is clean, stale, duplicated, or entirely undocumented, ranked by how often the gap recurs.
VERDICT: ❌ net-new video available

**Spine 3 (LATENT): Curate a context block, skip the RAG layer.** For one team's domain, do not build retrieval infrastructure; measure the domain (about 96k tokens), curate the useful 20% into one cache-able context block, and load it directly. Source treats this thinly (Q&A only), so a video needs extra sourcing.
VERDICT: 🔗 next-step video available (complements "1M Token Context")

## 2. Summary and counts

Raj Navakoti, IKEA staff engineer, presents demand-driven context: give agents real problems, watch them fail, and use those failures to build coherent, curated knowledge bases.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 3. 🔬 Deep dive

### Spine 1 — Demand-driven context (failure as the discovery mechanism)

The claim: stop trying to push all institutional knowledge to agents up front; instead assign real work, watch the agent fail, and let each failure produce a precise checklist of what was never documented. Most people get this backwards: the industry answer is to build a retrieval layer, 10 to 20 MCP servers or RAG over the whole wiki, and assume the agent will then just work. That fails because roughly 40% of institutional knowledge is tribal and lives only in people's heads, so you cannot push what nobody ever wrote down. The mechanism is a loop: the agent retrieves, then keeps going and emits a checklist of terms and business logic it cannot find (confidence 1 out of 5); a human answers only those gaps; the agent curates those answers into a reusable context block; the next problem starts higher. Because the failure surfaces the unknown-unknowns, you only ever write docs an agent actually needed. Across 14 incidents Raj's confidence climbed from 1.5 to 4.4. It generalizes cleanly to onboarding a new hire (assign work, they ask, they document) and to TDD (failing tests first). It goes wrong when interrogation "denial-of-service attacks" your experts, when codebase and wiki conflict on source of truth, and when there is no domain expert to answer.

### Spine 2 — The context gap scanner (measure coverage, do not fix)

The claim: point an agent at your archive of real past tickets and incidents and have it measure how much of your knowledge base is clean, stale, incomplete, missing, or tribal, ranked by criticality. It is non-obvious because teams argue "is our documentation good?" with no instrument; the usual fallback is a manual mural of "docs we should write someday." A scanner turns coverage into a measured, prioritized backlog. The mechanism is three steps: demand extraction (each incident yields a checklist of required knowledge), consolidation (group into systems and APIs, tag each clean, stale, incomplete, missing, or tribal), and gap analysis (score criticality by how often a missing entity recurs across incidents). Because it is driven by real historical work items, it scores what actually blocks delivery, not hypothetical gaps; the output is a kanban board, critical first. It generalizes to auditing a codebase's onboarding docs against real bug tickets, and to auditing an internal CLI or platform tool against the calls agents actually make. It goes wrong when tickets are poorly filled (often true), when a latest doc holds wrong information yet still reads as "covered," and on cost and cadence at scale.

### Spine 3 — Curate a context block, skip RAG (LATENT SPINE)

The claim: for a single team's domain, do not build retrieval infrastructure; measure the domain (Raj found about 96k tokens per domain), curate the useful 20% into one cache-able context block, load it directly, and keep the rest as links. It is non-obvious because the industry default says the retrieval layer, a roughly 9 billion dollar market of RAG and knowledge graphs, is what fixes institutional knowledge. Raj's counter: plugging MCP or RAG over a messy monolith produces undeterministic, untested output that is accurate only 10 to 30% of the time, so you end up doing data-entry for the agent. The mechanism: fix the context before retrieval, not live during operations; scope to the smallest team so the surface stays small; with a 1M-token window the whole curated domain fits, and just loading it beat graph-RAG in his tests. The 80/20 rule holds: 20% of docs carry 80% of the value, so cache that block and link the corner cases. It generalizes to any long-context-versus-RAG decision, for example a curated repo-map or AGENTS.md over a vector database. It goes wrong past roughly 1M tokens or multi-domain scope, and when a cached block silently goes stale. Note: the source treats this only in Q&A, so a full video needs extra sourcing.

## 4. 🎬 Proposed ACS videos (ranked)

### 1. Build a Scanner That Grades Your Docs Against Real Bug Tickets

- HOOK: Stop guessing whether your documentation is good; point an agent at last month's incidents and get a score.
- THE PROMISE: For engineers who own a messy codebase or wiki, after this you can build a tool that outputs a ranked backlog of exactly which docs to write first.
- THE SHAPE:
  1. Feed the agent a folder of past tickets and incidents plus your docs (or MCP connectors).
  2. Step 1, demand extraction: each ticket yields a checklist of the knowledge it needs.
  3. Step 2, consolidation: group into systems and APIs, tag each clean, stale, incomplete, missing, or tribal.
  4. Step 3, gap analysis: rank criticality by how often a missing entity recurs.
  5. Emit a kanban board; write the top items back as CLAUDE.md and skills.
- SPINE: 2 (context gap scanner)
- SLOT: Context Engineering, new chapter "Auditing Your Context Layer" (cross-link Loopy AI, alongside "Going Through a PR Backlog")
- RELATIONSHIP: ❌ net-new. ACS audits CODE (/code-review, /simplify, "Reducing Agent Confusion in Growing Projects") but has nothing that audits your knowledge-base coverage against real work items and outputs a prioritized gap board.
- PROOF TO REUSE: the three-step scanner (probes, run, analyze); the clean / stale / duplicated / missing / tribal tags; criticality-by-recurrence ("notification service appears in 20 incidents, fix that doc first"); the 40% tribal, 20% outdated, 20% unreliable, 10% duplicated breakdown.

### 2. Let Your Agent Fail on Purpose to Build Its Own Knowledge Base

- HOOK: The fastest way to find what your codebase never documented is to watch an agent hit the wall.
- THE PROMISE: For engineers drowning in tribal knowledge, after this you can turn a real task the agent fails into a written, reusable context file, one failure at a time.
- THE SHAPE:
  1. Give the agent a real task in an under-documented area (an incident RCA or a feature).
  2. Let it retrieve, then demand the checklist of terms and logic it cannot find (confidence 1/5).
  3. Answer only those gaps as the human domain expert.
  4. Have the agent curate your answers into a reusable context block (skills, rules, plus a knowledge folder).
  5. Repeat across tasks and watch confidence climb (Raj: 1.5 to 4.4 over 14 incidents).
- SPINE: 1 (demand-driven context)
- SLOT: Context Engineering, "The Solution Paradigm" (next to "The Context Layer"); or Master Claude Code, "CLAUDE.md"
- RELATIONSHIP: 🔗 complements "CLAUDE.md Best Practices" (which teaches: add rules only after the agent repeatedly makes a mistake) and "The Context Layer" (context-layer architecture). Those teach reactive rule-adding and structure; the next step is a deliberate, metered loop that manufactures failures to surface undocumented tribal knowledge and curates it back systematically.
- PROOF TO REUSE: the Memento memory analogy; the green/orange/red knowledge taxonomy; pull-not-push plus the new-hire onboarding analogy; the TDD analogy (failing tests first); "unless you don't do this way you will never know what is not documented"; the Claude Code implementation as skills, rules, agents, hooks, and a knowledge folder.

### 3. Measure Your Domain, Then Delete the RAG Layer

- HOOK: Your team's whole domain might be 96k tokens; that fits in the window, so why did you build 20 MCP servers?
- THE PROMISE: For teams over-engineering retrieval, after this you can decide when a curated context block beats RAG and cut the infrastructure you do not need.
- THE SHAPE:
  1. Scope to the smallest team so the knowledge surface stays small.
  2. Measure the domain's token count (Raj: about 96k per domain).
  3. Curate the useful 20% into one cache-able context block; leave the rest as links.
  4. Load it directly instead of RAG; compare answer quality against graph-RAG.
  5. Fix the context before retrieval, not live during operations.
- SPINE: 3 (curate-over-retrieve, LATENT)
- SLOT: Master Claude Code, "1M Context Window"; or Context Engineering
- RELATIONSHIP: 🔗 complements "1M Token Context" (which teaches using the big window as an intake layer). The next step is the enterprise decision: skip building the retrieval layer for a team's institutional knowledge because a measured curated block fits the window and beat RAG in his tests.
- PROOF TO REUSE: the cited McKinsey "80% use AI, 6% see value" figure; the 9 billion dollar retrieval market and "nobody will come fix your knowledge base"; 96k tokens per domain; the 80/20 cache-block-plus-links model; MCP/RAG output described as "undeterministic, unreliable, untested."

## 5. 📚 Full wisdom (reference)

### SUMMARY
Raj Navakoti, IKEA staff engineer, presents demand-driven context: give agents real problems, watch them fail, and use those failures to build coherent, curated knowledge bases.

### IDEAS
- Demand-driven context flips curation: give agents real problems, watch them fail, let failures reveal missing knowledge.
- Raj splits the institutional knowledge into green general, orange teachable, and red tribal undocumented human knowledge.
- Agents excel at the green and orange tasks but stall on red institutional knowledge inside people.
- Pull beats push: assign work items, let agents ask questions, fill gaps, document as they go.
- In one cycle the agent fails, returns a checklist, human answers, agent curates knowledge for reuse.
- Failure surfaces the unknown-unknowns: only a failed task reveals which knowledge was never written down anywhere.
- Confidence scoring tracks the progress: fourteen repeated incidents lifted the knowledge base from 1.5 to 4.4.
- Move the agent from a consumer to a knowledge manager: it curates documentation, not just consumes.
- Automate at scale: feed archived Jira tickets and past incidents through the framework to validate documentation.
- The context gap scanner runs three steps: generate probes, run the tests, then analyze documentation gaps.
- The scanner tags each doc clean, stale, incomplete, missing, or tribal, then ranks them by criticality.
- Criticality is frequency: a doc gap recurring across twenty incidents becomes the first thing to fix.
- Break the knowledge monolith into context blocks, like refactoring a legacy monolith into microservices for agents.
- Store the knowledge base in GitHub so multiple agents and experts get PR review, conflict resolution.
- A meta model maps how business processes, systems, and APIs relate, giving agents a navigation map.
- Fix the context before retrieval, not live during operations, because operational gap-filling is slow and painful.
- One domain averaged 96k tokens, small enough that loading everything directly beat graph-RAG in Raj's experiments.
- Scope down to the smallest team; broad enterprise scope has no single person holding the expertise.

### INSIGHTS
- You cannot push knowledge nobody documented; only demand from real failure surfaces the tribal 40% reliably.
- Retrieval is only half the loop; the agent must also act on and document what's missing.
- Building twenty MCP servers over a messy monolith fails; the monolith itself must be decomposed first.
- Engineers ship MCP servers without any evals, checking only that output appears, not whether it's valuable.
- The failure checklist is the deliverable: it names precisely which undocumented terms and logic block completion.
- Confidence climbing steadily from 1.5 to 4.4 proves the curated knowledge base compounds problem by problem.
- Doing the loop manually is unbearable; the value only appears once the whole process is automated.
- Combining the codebase and wiki creates source-of-truth conflicts, forcing an explicit ranking rule of which wins.
- Nobody external fixes your knowledge base; providers own models, harness, retrieval, but institutional knowledge is yours.
- The 80/20 rule applies: twenty percent of documentation carries eighty percent of an agent's usable value.

### QUOTES
- "If there is an AGI coming the first AGI will be a coding agent for sure." — Raj Navakoti
- "nobody is going to come to your company and fix your knowledge base. You have to fix it yourself" — Raj Navakoti
- "we are moving agent from a consumer to a knowledge manager" — Raj Navakoti
- "unless you don't do this way you will never know what is not documented" — Raj Navakoti
- "when you give a problem it actually surfaces what is not documented" — Raj Navakoti
- "40% of the knowledge is always tribal knowledge which means people know how things work" — Raj Navakoti
- "we give problems that agent will definitely fail and we gradually fill those gaps" — Raj Navakoti
- "I don't want to be the knowledge manager of it so let it do it" — Raj Navakoti
- "just putting the whole context right now in the window gives you more results than actually doing RAG" — Raj Navakoti
- "I'm a bit concerned that this might denial of service attack your team members" — audience member
- "this is very early this approach so by tomorrow morning on YouTube somebody would have already posted something differently" — Raj Navakoti

### HABITS
- Raj implements the whole approach with Claude Code skills, rules, agents, hooks, plus a knowledge folder.
- He scopes every experiment down to the smallest team before attempting any domain or enterprise-wide rollout.
- He always fixes the context before retrieval rather than filling gaps live while an agent operates.
- He prefers GitHub repositories over Confluence for storing knowledge because of the built-in review and merge.
- He builds a meta model mapping business processes to systems to APIs as a navigation add-on.
- He tags every curated document with a date and a state, marking it stale, active, or clean.
- He flags staleness by date threshold but lets a human, not the agent, decide what's outdated.
- He validated the method on real datasets and published a March arXiv preprint on demand-driven context.

### FACTS
- A cited McKinsey figure says 80% of companies use AI yet only 6% see real value.
- A documented knowledge base plus RAG or knowledge graphs achieves roughly 40% factual accuracy on retrieval.
- In Raj's model enterprise institutional knowledge is roughly 40% tribal, 20% outdated, 20% unreliable, 10% duplicated.
- The retrieval market is worth roughly 9 billion dollars, yet cannot fix your specific knowledge base.
- Raj personally built more than twenty MCP servers over institutional knowledge before concluding the approach failed.
- Plugged-in MCP servers gave accurate output only 10 to 30% of the time, per Raj's experience.
- Across tested domains, each averaged around 96,000 tokens, fitting comfortably inside a modern 1M context window.
- Raj works at IKEA in a deliverance-services domain of over 100 engineers across six product teams.

### REFERENCES
- The movie Memento (analogy for agent memory limits and note-taking).
- McKinsey AI value-creation statistic (2026, cited).
- ArXiv preprint on demand-driven context (March, Raj Navakoti); GitHub starter repo and a live context gap scanner demo.
- The ACE paper (cited for comparison on agent context and strategic-versus-domain knowledge).
- Claude Code (skills, rules, agents, hooks); GitHub Copilot; Replit.
- Storage and knowledge systems: Confluence, Slack, Jira, SharePoint, GitHub.
- Retrieval concepts: RAG, knowledge graphs, MCP servers, graph RAG, the 1M-token context window.
- Analogies used: TDD (test-driven development), monolith-to-microservices, waterfall-to-agile.
- Speaker: Raj Navakoti, staff software engineer, IKEA (deliverance services).

### ONE-SENTENCE TAKEAWAY
Give agents real tasks, let them fail, and turn each failure into documented, reusable context.

### RECOMMENDATIONS
- Take one real Jira ticket, hand it to your agent, and grade your current knowledge base.
- Stop pushing all documentation upfront; instead assign work items and let agents pull the missing knowledge.
- Capture the agent's failure checklist, answer only those specific gaps, then have it document them permanently.
- Automate the whole loop over your archived incidents instead of sitting through fifteen painful manual cycles.
- Store your curated knowledge base in GitHub to get PR review and conflict resolution for free.
- Measure your domain's total token count before building RAG, because it may fit directly in context.
- Scope any first attempt to your smallest team, then expand only once the method proves itself.
- Build a meta model mapping your systems, APIs, and business processes so agents can navigate confidently.
- Add a source-of-truth ranking rule for when code and documentation disagree, so the agent resolves conflicts.
- Keep the useful 20% as a cache-able context block and leave the corner cases as links.
