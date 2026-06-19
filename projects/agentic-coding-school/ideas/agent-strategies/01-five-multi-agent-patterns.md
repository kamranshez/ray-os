---
tags: [agentic-coding, multi-agent, taxonomy]
date: 2026-05-07
source: Luke (Factory) — missions talk, https://www.youtube.com/watch?v=ow1we5PzK-o
status: "idea"
---

## What this video covers

A taxonomy. The multi-agent space is messy: every framework invents new vocabulary for the same five primitives. This video names them, shows the failure mode each one solves, and explains why every real multi-agent system you'll build is just a recombination of these five.

## Why this matters

Without a vocabulary, every conversation about agent architectures starts from scratch. You can't compare designs, you can't predict failure modes, and you can't reason about which pattern fits the problem in front of you.

Luke's framing:

> "When you start researching multi-agent frameworks and systems, you quickly realize that the field's a bit of a mess. Everyone has their own framework, their own terminology, their own opinions of what works and doesn't work."

His proposal: five primitives. Once you see them, you can't unsee them.

## Sub-chapter 1: Delegation

One agent spawns another. The parent says "go figure out the database schema" and waits for an answer. This is what most people implement first because it's the simplest form of multi-agent communication.

> "You have you know subagents and coding tools are the most common example."

Where you've already used it: every time you spawn a subagent in Claude Code or Codex.

Failure mode: the parent agent has to know what to ask for. Bad delegation produces a confident but wrong answer that the parent then trusts.

## Sub-chapter 2: Creator-verifier

One agent builds. Another agent checks. Critically, they have separate contexts.

> "The agent that implemented the code has some cost bias, right? It wants that code to work. A fresh agent with fresh context is way more likely to find issues. And this is why we do code review as humans as well."

This is the pattern with the strongest empirical support. Cost bias is structural, not a model weakness. Solo agents will defend their own implementations because every token they generate commits them further.

We have a whole video on this in the validation pillar.

## Sub-chapter 3: Direct communication (and why it usually breaks)

Agents talk to each other without a coordinator. Like DMs.

> "It's hard to get right though because state fragments across conversations without that coordinator and there's no single source of truth."

This is the pattern most often invented from scratch by people who haven't tried it before. It looks elegant on a whiteboard. In practice, three agents DMing produce three slightly different views of the world and no way to reconcile them.

Default to a coordinator. Reach for direct communication only when the coordination overhead is the actual bottleneck.

## Sub-chapter 4: Negotiation

Agents communicate over a shared resource: the same API, the same file, the same budget. Negotiation does not need to be adversarial.

> "Negotiation doesn't need to be adversarial. In fact, the best use case is when there's net positive sum trading, right? And that's when agents have like a potential win-win situation while interacting."

Example: two workers both need to modify the same module. Negotiation is what lets one go first and the other inherit the result, instead of both writing conflicting changes.

## Sub-chapter 5: Broadcast

One agent sends information to many. Status updates, new constraints, shared context that applies to every worker.

> "It's a bit less flashy than the other ones, but it's critical for maintaining coherence over long-running tasks."

Underrated. The reason missions can run for sixteen days without drift is that broadcast keeps every active agent on the same shared state. Skip broadcast and you get five agents each operating on a slightly different version of the truth.

## Sub-chapter 6: Real systems combine these

> "Missions is our answer. It's a system that combines four of those: delegation, creator-verifier, broadcast, and negotiation into a single workflow."

Notice direct communication is the one Luke leaves out. That's deliberate. The other four route through shared state; direct communication doesn't.

The takeaway for the rest of the class: when you sketch your own architecture, label every arrow with which of these five it is. If you can't, you don't yet understand the design.

## Talking points for filming

- Open with the messy-field framing
- Walk through each pattern with one concrete coding-agent example
- Spend extra time on direct communication's failure mode (people keep reinventing it)
- Close on the missions composition: four of five, deliberately

## Key takeaway

Every multi-agent system is a recombination of delegation, creator-verifier, direct communication, negotiation, and broadcast.
