---
title: "Stop babysitting your agents... — Brandon Waselnuk, Unblocked"
video_url: https://www.youtube.com/watch?v=BiG2ssibKGc
video_id: BiG2ssibKGc
channel: AI Engineer
published: 2026-05-26
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Stop babysitting your agents... — Brandon Waselnuk, Unblocked**](https://www.youtube.com/watch?v=BiG2ssibKGc) - AI Engineer - uploaded 2026-05-26

> net-new plus next-step ACS videos available: build a pre-flight research packet, and resolve code-vs-discussion conflicts

## The one idea worth a video

**Spine 1: Access is not understanding, so build a reasoned research packet across all your sources before the agent writes a line.** It subsumes the three myths (naive RAG, more MCPs, the million token window all fail) and the outcome data: front-loading beats correcting output. VERDICT: 🔗 next-step video available.

**Spine 2 (LATENT): The source of truth is contested, so teach the agent to resolve code-vs-discussion conflicts by authority and recency.** The shipped code in main can be wrong when a CTO overruled it later in Slack; the agent must settle that, not silently pick. VERDICT: ❌ net-new video available.

## Summary + counts

Brandon Waselnuk of Unblocked argues agents fail from missing context, not intelligence; a context engine builds research packets across code, Slack, and org before coding.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1: Front-load a reasoned research packet, because access is not understanding.**
The claim: outcomes change not when you give the agent more pipes (MCPs, a million token window) but when something reasons exhaustively across your code, Slack, PR history, and org first, then hands it a compressed brief before it plans. Why it is non-obvious: the intuitive fix is more access, but access only lets the agent reach data, not understand which of it matters. The mechanism runs in steps: naive retrieval suffers "satisfaction of search" and stops at the first plausible pattern; the agent then confidently builds on a wrong or incomplete premise; you read the output, reject it, and drop into the correction doom loop that is babysitting. Get the context right up front and every downstream choice improves, which is also why it is more token efficient. It generalizes cleanly to solo Claude Code work: a pre-flight research pass that greps code, reads relevant Slack, and writes a research-packet.md the planner consumes. How it goes wrong: cache that packet and it silently goes stale within a day, and a shallow non-exhaustive pass just reproduces the naive failure.

**Spine 2 (LATENT): Truth is contested, so resolve conflicts by authority and recency.**
The claim: the code in main is not automatically the source of truth; a later authoritative correction, like a CTO saying in Slack "that was implemented wrong," can override it, and the agent must settle that rather than pick arbitrarily. Why it is non-obvious: most retrieval treats shipped code as ground truth, so the agent trusts a pattern the team has already privately abandoned. The mechanism: conflicting signals exist (code says X, a senior voice says X is wrong); if the agent hides the conflict it inherits a stale decision; if it surfaces and weighs the sources by who said it and when, it aligns with the team's real current intent. It generalizes to any solo codebase where stale docs, old ADRs, or TODO comments contradict the live code. How it goes wrong: authority signals can be noisy, recency is not always correctness, and the source treats this thinly in one exchange, so a full video needs extra sourcing on conflict-resolution heuristics.

## 🎬 Proposed ACS videos

### 1. Give Your Agent a Research Packet Before It Writes Any Code
- HOOK: Same prompt, same model: 2.5 hours and a rejected PR, or 25 minutes and one nitpick. The difference was context up front.
- THE PROMISE: For engineers on real codebases who keep correcting their agents: build a pre-flight research packet so the agent plans from your patterns, not from its first guess.
- THE SHAPE: (1) Show the babysitting doom loop from a starved run. (2) Run explore subagents across code AND non-code sources (Slack MCP, PR history). (3) Force exhaustive retrieval so it does not stop at the first pattern. (4) Compress findings into research-packet.md. (5) Feed the packet to the planner and merge cleanly.
- SPINE: 1
- SLOT: Context Engineering (new chapter: Pre-flight Research Packets)
- RELATIONSHIP: 🔗 complements "Improving Explore Subagent" (Master Claude Code > Subagents) and "Continuing Plan in New Context Window" (Master Claude Code > Planning), which already teach exploring the codebase and carrying a plan into a fresh window; this adds the next step beyond them: reaching non-code sources and persisting a durable, token-optimized packet so context is not re-grepped every session.
- PROOF TO REUSE: The 25 min / 10.8M tokens vs 2.5 hr / 20.9M tokens comparison; "satisfaction of search" from radiology; "getting the best context up front makes all agent choices and actions after that even better."

### 2. When Your Code and Your Slack Disagree: Teaching Agents Which Source Is True
- HOOK: Your agent trusts the code in main. But the CTO said three months ago that exact pattern was wrong. Who wins?
- THE PROMISE: For teams whose docs, threads, and code drift apart: teach the agent to detect conflicting sources and resolve them by authority and recency instead of silently picking one.
- THE SHAPE: (1) Plant a conflict: main code plus a Slack thread overruling it. (2) Watch a naive agent pick arbitrarily. (3) Give it a resolution rule (weigh who said it, when, and where). (4) Have it flag the conflict and cite the winning source in its plan.
- SPINE: 2
- SLOT: Context Engineering (new chapter: Resolving Conflicting Sources)
- RELATIONSHIP: ❌ net-new. The closest catalog videos, "The One-Pattern Rule for Agents" (Advanced Techniques) and "Reducing Agent Confusion in Growing Projects" (Techniques), are about standardizing on one pattern and auditing confusing architecture, not about resolving a truth conflict between shipped code and a later human correction.
- PROOF TO REUSE: "if you see the CTO saying in the Slack thread that's wrong the CTO is probably right"; the truthiness framing; conflicts hidden vs serviced as one of Unblocked's hard lessons.

## 📚 Full wisdom (reference)

**SUMMARY**
Brandon Waselnuk of Unblocked argues agents fail from missing context, not intelligence; a context engine builds research packets across code, Slack, and org before coding.

**IDEAS**
- A freshly spawned agent knows nothing about your org, your services, or your existing codebase conventions.
- Right now you personally are the context engine, manually feeding your agents everything they actually need.
- Access is not understanding: MCP pipes merely reach data but cannot reason across those disparate systems.
- Naive RAG suffers satisfaction of search, stopping at the very first plausible result it happens upon.
- Satisfaction of search is borrowed from radiology, where radiologists stop scanning after finding one obvious abnormality.
- Even a full million token window mostly sits idle, because agents cannot reason over that volume.
- A context engine reasons across your code, Slack, PR history, and org structure before writing begins.
- Getting the best context up front makes every downstream agent choice and subsequent action measurably better.
- A research packet up front lets explore agents grep the right places, saving a bajillion tokens.
- Static context repos like CLAUDE.md and AGENTS.md go stale quickly and lack any live runtime data.
- Without context, an agent rewrote code entirely from scratch, missing an existing internal service already built.
- A social graph pivots retrieval on who you are, whose code you review, and your history.
- The context engine must resolve conflicts when shipped main code contradicts a CTO's later Slack correction.
- Caching good answers for latency backfires: the cached answer silently goes stale within a single day.
- The same prompt ran twice: naive MCP access wrote system-breaking code that the senior engineer rejected.

**INSIGHTS**
- The bottleneck has shifted from model intelligence to context; smarter models cannot rescue a starved agent.
- Front-loading context beats correcting output, since fixing a starved agent afterward traps you in endless babysitting.
- Exhaustive retrieval matters more than fast retrieval, because the first match is rarely the correct pattern.
- Code compiling and passing every check proves almost nothing about architectural correctness at real organizational scale.
- Truth is not the code alone; the last authoritative human correction can override the shipped source.
- Rediscovered context dies the moment a terminal closes, forcing costly re-grepping in every fresh agent session.
- Background and headless agents need a machine to query for context, not a human to interrupt.
- Compressing exhaustive reasoning into a small token-optimized packet beats handing the agent raw, entirely unfiltered data.

**QUOTES**
- "my goal is to make it so that you don't have to babysit your agents anymore" — Brandon Waselnuk
- "not long ago, you were the context engine" — Brandon Waselnuk
- "The gap is not intelligence at this point. It is context" — Brandon Waselnuk
- "people think that access is the answer but it is not understanding" — Brandon Waselnuk
- "the first piece of data it finds it goes oh this this must be the pattern it stops looking" — Brandon Waselnuk
- "I don't know if anyone's ever whacked it full with something and then tried to get the agent to do anything. It can't." — Brandon Waselnuk
- "if you see the CTO saying in the Slack thread that's wrong the CTO is probably right" — Brandon Waselnuk
- "The moment you write it, it's no longer valid because things are changing" — Brandon Waselnuk
- "if you cache a correct answer and then tomorrow someone asks the same question and you answer it, you you probably lied to them now" — Brandon Waselnuk
- "it compiled but the senior engineer was like this is totally wrong and what it tried to do would have broken our entire system if we had shipped it" — Brandon Waselnuk
- "getting the best context up front makes all agent choices and actions after that even better" — Brandon Waselnuk
- "An agent should write code that feels like it was written by someone who's been on your team for years" — Brandon Waselnuk

**HABITS**
- Use the context engine for planning, run the execution, then leverage it again during code review.
- Surface data conflicts openly instead of hiding them, since agents will otherwise pick a source arbitrarily.
- Avoid caching answers, even optimized ones, because underlying systems keep changing constantly on a daily clock.
- Deliver context over MCP so the OAuth model carries through cleanly for data governance and permissions.
- Never return another person's private Slack or Teams chats when answering a different colleague's separate query.
- Instruct the agent to search exhaustively rather than accept the first pattern it happens to discover.
- Point the graph builder directly at your repo, then inspect who authors and reviews each area.
- Force high reasoning effort on the research task so the resulting packet returns genuinely thorough results.

**FACTS**
- With a context engine, the same task took 25 minutes and roughly 10.8 million tokens total.
- Without a context engine, the identical task took 2.5 hours and about 20.9 million tokens total.
- Satisfaction of search is a documented phenomenon in radiology, affecting how second abnormalities often get missed.
- Unblocked serves customer organizations as large as twenty thousand members, each needing personalized, scoped context retrieval.
- The naive run passed all automated code checks yet still would have broken the entire system.
- Unblocked's context engine sits inside every customer's ask-engineering Slack channel, scoring and answering incoming questions automatically.
- The demo social graph was procedurally generated, sizing each node by how much that person ships.
- Unblocked labeled its social graph nodes using an API key from Anthropic during the graph construction.

**REFERENCES**
- Unblocked (getunblocked.com), the context engine product being described
- Andrej Karpathy, cited for "the gap is not intelligence, it is context"
- Basim Eld, whose maturity ladder work the context stages were adapted from
- Claude and Claude Code (CLI), plus an Anthropic API key for labeling
- CLAUDE.md and AGENTS.md static context files
- MCP (Model Context Protocol) as the delivery layer
- Zendesk integration (used in the research packet demo)
- Ghostty terminal (used in the demo)
- AWS Bedrock (used as a fallback the naive run missed)
- Slack and Microsoft Teams (ingested data sources)
- Anthropic cloud agents launch and Ryan's Codex talk (both referenced from the same event)
- An open-source social graph builder from Unblocked's workshop

**ONE-SENTENCE TAKEAWAY**
Stop feeding agents by hand: build a reasoned research packet across all sources before coding.

**RECOMMENDATIONS**
- Before any coding, have your agent build a research packet reasoning across code and team discussions.
- Add non-code sources like Slack and PR history to your agent's retrieval, not merely code files.
- Instruct agents to keep searching well after the first hit until they surface any conflicting patterns.
- When code and team discussion conflict, tell the agent to weigh source authority and recency explicitly.
- Persist the research packet to a durable file so future sessions skip the expensive re-grepping entirely.
- Do not trust caching for evolving answers; treat any cached context as expiring within a day.
- Give background agents a queryable context source so they never stall waiting on a human overnight.
- Compress all your gathered context into a small token-optimized brief before handing it to the agent.
