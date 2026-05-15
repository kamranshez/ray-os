---
tags: [agentic-coding, context-windows, workflow]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Context window strategy is correlated with engagement level

## The idea
"Stay under 100k tokens" is not a universal rule. It's a heuristic for people without intuition. The real variable is *how engaged you are with the task*. If you're highly engaged — reading every model response in real time, steering actively — you can use much bigger context (Vibhav routinely hits 800k). If you're disengaged — running tasks in the background, batching, multitasking — you should keep context small so the model makes fewer mistakes you won't catch.

## The mapping
| Engagement | Context size | Why |
|---|---|---|
| Highly engaged, real-time steering | Large (up to 800k+) | Human catches drift as it happens |
| Background / parallel work | Small (under 100k) | Smaller context = fewer mistakes to miss |
| Multi-turn tool calling loops | Small (under 50k for hard reasoning) | Spin-out crisis at high token counts |
| Document summarization / writing | Large (200-400k fine) | Single-pass attention, low feedback loop |

## How to apply
- Ask "how engaged am I going to be?" before picking a session strategy
- For background tasks: keep context small, accept that you're trading speed for safety
- For active design work: let it rip, you're the safety net
- Don't pretend you'll be engaged when you won't — be honest about your attention budget
- Don't pretend small-context is always safer — it costs you exploration depth

## Surrounding context
Vibhav: "If you want the model to make less mistakes, stay smaller context. If you want to be lazy, use bigger context — but then you have to make up for the laziness in some other ways." The "other ways" are reiteration, active steering, and the human brain holding long-term consistency.

This pairs with the "long context inverts dumb-zone advice" idea — the inversion only works *because* engagement compensates for forgotten middle context. Disengaged + long context = worst of both worlds.

## Open questions to explore
- Can you measure your own engagement level honestly enough to pick the right strategy?
- Is there a tooling signal (e.g., response latency, edit distance per turn) that detects engagement?
- How do teams normalize this when multiple engineers share workflows with different engagement profiles?
- Does engagement degrade predictably during a long session, requiring strategy shifts mid-task?
- What's the right way to teach this to people building their first agentic workflows?
