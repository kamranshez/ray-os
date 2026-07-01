---
title: Prompt Engineering is dead.
video_url: https://www.youtube.com/watch?v=Cs7QiSi8KLY
video_id: Cs7QiSi8KLY
channel: Confluent Developer
published: 2026-02-10
status: covered
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Prompt Engineering is dead.**](https://www.youtube.com/watch?v=Cs7QiSi8KLY) - Confluent Developer - uploaded 2026-02-10

> already covered by ACS

Tim Berglund's lightboard talk is a clean, provider-agnostic context-engineering 101: context is a finite budget you engineer, not a window you dump into. Its load-bearing spine, treat the context window as a scarce resource and note that past roughly 60-70 percent fullness the model degrades, is already taught directly in "Long Context Failure" (Techniques, Session and Context Management) and "Opus 4.6's Context Window" (My Daily Workflows), which cover context poisoning, distraction, and the exact fullness sweet spot with live examples.

The video's other beats are each covered too. The six-part context schema (user message, system prompt, tools, resources, assistant messages, tool calls) is shown live in "/context" (Master Claude Code, The Fundamentals), which breaks the window into system prompt, tools, MCP tools, memory files, and message history. The long-horizon toolkit maps one-to-one onto existing videos: compaction to "Economising with Prompt Cache" and "Compaction and Monothreading"; sub-agent decomposition to the whole Subagents and Multi-Agent Orchestration chapters plus "Forked Contexts for Skills"; the system-prompt Goldilocks principle to "Instruction Following Limits" (Context Engineering, Foundations) and "System Prompt Config".

The only near-gap is the runtime economy trick of passing an ID instead of a full record and prompting the model to hydrate the resource only if it needs it, which sits adjacent to T-shaped loading in "The Context Layer" but is not filmed as its own beat. That is a tip, not a spine, and does not clear the bar for a new ACS video. No net-new or complement spine; no pitch.
