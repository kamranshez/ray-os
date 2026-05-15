---
tags: [agentic-coding, context-windows, long-context, prompting]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Long context demands active human steering

## The idea
Million-token context isn't free intelligence. The middle of the window still loses attention regardless of how much you preserve there. So when you operate in long context, you take on a responsibility: you, the human, must keep dragging important state forward into recent messages. The model's working memory is "the last few turns plus the system prompt." Everything else is reference material it might or might not weigh. If you're not actively steering, long context becomes a liability rather than an asset.

## What "active steering" looks like
- Re-stating critical decisions in current messages before building on them
- Asking the model to articulate its current understanding back to you periodically
- Catching drift as it happens, not after implementation
- Reading model output as it streams, not in batches
- Re-injecting forgotten constraints whenever you notice the model violating them

## What it isn't
- "Just trust the context window because it's a million tokens"
- Passively letting the model reference 500k tokens back without prompting
- Assuming preservation = influence

## How to apply
- Treat long context as a *cache of explored options*, not as a *permanent shared brain*
- Every N messages, summarize current state in a single message — that summary now lives in recent context
- When you notice the model has forgotten something, don't just re-explain — *re-anchor* it as a current decision
- If you can't steer actively, shorten the context

## Surrounding context
Dex: "the middle of your context window — you're going to pretend like it doesn't exist or it's barely going to impact you. Why not just start a new one?" Vibhav: "convenience. It's not that it doesn't impact you, it just has less influence."

This is the responsibility tax on long context. It's also why the "long context inverts dumb-zone advice" claim is conditional — the inversion requires the human to do work the model can't. Models forget the middle; humans drag the middle forward.

## Open questions to explore
- What does a "steering checklist" look like — concrete behaviors to practice?
- Can you build a tool that auto-detects forgotten-but-important state and surfaces it?
- Is there a training signal for "the model is drifting from earlier decisions" before drift becomes obvious?
- How do you onboard someone into long-context workflows without them flailing?
- Does steering degrade as a skill the longer you go without rest? (i.e., is the dumb zone partly *the human's* dumb zone?)
