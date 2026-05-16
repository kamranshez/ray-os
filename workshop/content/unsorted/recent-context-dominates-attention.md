---
status: stub
acs: []
mapping: workshop-original
day: 2
block: core
recording-needed: true
---

# Recent context dominates model attention

## The idea
Models are trained to attend most strongly to the most recent messages and the system prompt. The middle of the context window is the "dumb zone" — information lives there but has dramatically reduced influence on output. This means you don't always need to serialize every decision to disk. If the decision was made in the last few messages, the model is heavily biased toward respecting it. Disk serialization (writing to a design doc after every decision) costs tool calls, latency, and consistency overhead — and isn't always worth it.

## The tradeoff
- **Pro disk serialization (Dex's approach):** every decision is durable, survives session crashes, can be reloaded into a fresh context anytime. Lower context anxiety.
- **Pro keeping it in context (Vibhav's approach):** moves at 2x speed, doesn't waste tokens on tool calls, model still respects recent decisions strongly. The human's brain holds long-term consistency.

## How to apply
- For *heavy design constructs* with lots of decisions and active back-and-forth: stay in context, write to disk at checkpoints only
- For *long-running implementation* where the session might die: serialize aggressively
- For *anything you'd want a fresh chat to pick up*: serialize
- Recognize that "losing information" and "losing influence" are different — middle-context info is still there, just under-weighted

## Surrounding context
Vibhav explicitly defended this against Dex's "always update the doc" approach. His framing: "I'm not too worried about being deep into the context window because I'm actively engaged. Everything I care about is in the last couple messages." His brain is the durable store for long-term consistency; the context window is the working memory. Dex's counter: "I always treat the context window as something that might veer off or my session might shut down — I want every decision tracked outside the context window."

Both work. The choice depends on whether *you* are the durable store or whether you need the *document* to be.

## Open questions to explore
- Is there a token-count threshold where context-only stops working reliably?
- How do you recover gracefully when a context-only session dies mid-design?
- Does writing a "key decisions" summary every N turns capture most of the disk-serialization benefit at lower cost?
- Is this strategy model-dependent? (e.g., does Opus handle it differently than Sonnet?)
