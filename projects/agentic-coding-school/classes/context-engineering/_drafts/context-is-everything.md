---
class: "context-engineering"
status: "scripted"
aliases: [context-is-everything]
---

- Context windows
- Context rot
- Setting up a status line

You'll find agents perform best in this zone.

## Context window strategy is correlated with engagement level

"Stay under 100k tokens" is not a universal rule. It's a heuristic for people without intuition. The real variable is *how engaged you are with the task*. If you're highly engaged — reading every model response in real time, steering actively — you can use much bigger context (Vibhav routinely hits 800k). If you're disengaged — running tasks in the background, batching, multitasking — you should keep context small so the model makes fewer mistakes you won't catch.

### The mapping
| Engagement | Context size | Why |
|---|---|---|
| Highly engaged, real-time steering | Large (up to 800k+) | Human catches drift as it happens |
| Background / parallel work | Small (under 100k) | Smaller context = fewer mistakes to miss |
| Multi-turn tool calling loops | Small (under 50k for hard reasoning) | Spin-out crisis at high token counts |
| Document summarization / writing | Large (200-400k fine) | Single-pass attention, low feedback loop |

### How to apply
- Ask "how engaged am I going to be?" before picking a session strategy
- For background tasks: keep context small, accept that you're trading speed for safety
- For active design work: let it rip, you're the safety net
- Don't pretend you'll be engaged when you won't — be honest about your attention budget
- Don't pretend small-context is always safer — it costs you exploration depth

Vibhav: "If you want the model to make less mistakes, stay smaller context. If you want to be lazy, use bigger context — but then you have to make up for the laziness in some other ways." The "other ways" are reiteration, active steering, and the human brain holding long-term consistency.

## Recent context dominates model attention

Models are trained to attend most strongly to the most recent messages and the system prompt. The middle of the context window is the "dumb zone" — information lives there but has dramatically reduced influence on output. This means you don't always need to serialize every decision to disk. If the decision was made in the last few messages, the model is heavily biased toward respecting it. Disk serialization (writing to a design doc after every decision) costs tool calls, latency, and consistency overhead — and isn't always worth it.

### The tradeoff
- **Pro disk serialization (Dex's approach):** every decision is durable, survives session crashes, can be reloaded into a fresh context anytime. Lower context anxiety.
- **Pro keeping it in context (Vibhav's approach):** moves at 2x speed, doesn't waste tokens on tool calls, model still respects recent decisions strongly. The human's brain holds long-term consistency.

### How to apply
- For *heavy design constructs* with lots of decisions and active back-and-forth: stay in context, write to disk at checkpoints only
- For *long-running implementation* where the session might die: serialize aggressively
- For *anything you'd want a fresh chat to pick up*: serialize
- Recognize that "losing information" and "losing influence" are different — middle-context info is still there, just under-weighted

Both work. The choice depends on whether *you* are the durable store or whether you need the *document* to be.
