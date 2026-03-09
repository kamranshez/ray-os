---
status: filmed
---

## The Core Insight

You've seen the constraints:

- **Signal-to-noise is everything.** Every token in context affects every other token. Noise drowns signal.
- **Search adds noise.** Agentic exploration fills context with dead ends before finding what matters.
- **Instruction following has limits.** Even frontier models hit 68% accuracy at 500 instructions. Dump everything into CLAUDE.md and the model drops rules silently.

So what's the answer?

**Progressive disclosure.** Load only what you need, when you need it.

![[images/01-progressive-disclosure/core-insight.png]]

---
## Where This Comes From

Progressive disclosure isn't new. In the 1990s, usability researchers at Nielsen Norman Group popularized the concept for user interfaces: show users only what they need right now, defer advanced features until requested. The goal was simple—reduce cognitive load, prevent overwhelm, let people focus.

Thirty years later, the same principle applies to AI agents. The most capable systems won't be the ones with the largest context windows. They'll be the ones that know what to know, and when to know it.

---

## The Kitchen Sink Problem

When developers first build AI agents, the instinct is to front-load everything. Documentation, API references, coding guidelines, conversation history, tool definitions—throw it all into the system prompt. More context means better answers, right?

Wrong.

This "kitchen sink" approach creates **context rot**. As irrelevant information accumulates, the agent's effective intelligence degrades. It struggles to identify what matters. It hallucinates connections between unrelated concepts. It loses track of the actual task.

The problem is architectural. LLMs process context through attention mechanisms that weigh every token against every other token. Stuffing the context window with marginally relevant information isn't just wasting tokens—it's actively introducing noise into the reasoning process.

Think of it like having a focused conversation in a crowded room where everyone is talking at once. The information you need might be present, but it's drowned out by everything else competing for attention.

The answer isn't more context. It's the right context, at the right time.

![[images/01-progressive-disclosure/kitchen-sink.png]]

---

## The Industry Convergence

One of the most interesting trends over the past several months: AI infrastructure companies—Cloudflare, Anthropic, Vercel, Cursor—are all arriving at the same conclusion independently.

> Progressively disclose only what you need to the model when you need it.

Give agents a file system and bash. Let them grep, glob, find. Load files only when needed.

Examples
- https://cursor.com/blog/dynamic-context-discovery
- https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## The Three-Layer Architecture

Progressive disclosure translates into a layered architecture:

**Layer 1: Index.** Lightweight metadata—titles, descriptions, capabilities. Enough to know what exists and make routing decisions. Costs 10-100 tokens.

**Layer 2: Details.** Full content, loaded only when the agent determines it's relevant to the current task.

**Layer 3: Deep Dive.** Supporting materials, examples, reference documentation. Accessed only when the agent needs to go deeper.

The philosophy: provide the map, let the agent choose the path. Context becomes a resource to spend wisely, not a dump truck to empty into every conversation.

![[images/01-progressive-disclosure/three-layer-architecture.png]]

---

## Why This Works

Remember the blindfolded genius? Dropping an AI into a giant repo is like blindfolding an expert and asking them to navigate an unfamiliar building.

- **Agentic search** lets them fumble around
- **Progressive disclosure** hands them a flashlight and a map

The genius is still a genius. But now they can see.

Progressive disclosure works because it addresses every constraint from the foundations:

1. **Signal-to-noise** — Context stays small. Only relevant information loads.
2. **Instruction limits** — You're not dumping 500 rules. You're loading 5-10 when they matter.
3. **Search noise** — The agent still explores, but with guidance. Less fumbling, more finding.

![[images/01-progressive-disclosure/why-this-works.png]]
---
## The Conclusion

The industry has converged. Progressive disclosure is the pattern.

The most capable AI systems won't be the ones with the largest context windows or the most comprehensive knowledge bases. They'll be the ones that know what to know, and when to know it.

Less context, thoughtfully managed, means smarter systems. The art isn't in knowing everything. It's in knowing when to look.
