---
duration: "10-15 min"
batch: 1
order: 7
batch_name: "Research & Intelligence"
class: "business"
chapter: "Research & Intelligence"
---

## Parallel Subagents: Attack a Problem from Every Angle

Instead of researching sequentially (finish one angle, start the next), spawn multiple subagents simultaneously — each with a different persona — to cover every dimension of a business question in parallel.

> "My research skill instructs Claude to launch parallel research across every relevant angle simultaneously rather than working through them sequentially: the securities analysis, the state licensing requirements, the banking regulations, the consumer protection implications."
> — [Zack Shapiro (@zackbshapiro)](https://x.com/zackbshapiro/status/2027389987444957625)

### The Persona Vector Principle

Anthropic's research on [persona vectors](https://www.anthropic.com/research/persona-vectors) shows that language models have internal neural patterns that control character traits and expertise. When you give a subagent a specific persona — "You are a regulatory compliance specialist" vs "You are a pricing strategist" — you're not just decorating the prompt. You're activating different regions of the model's knowledge that a generic "research this topic" prompt would never invoke.

A basic prompt like "research UK market expansion" gets you surface-level, generalist output. But when you define persona vectors for each subagent:
- **Regulatory analyst**: activates deep knowledge of compliance frameworks, licensing, data protection law
- **Competitive intelligence specialist**: activates pattern-matching on market positioning, pricing models, competitor weaknesses
- **Operations strategist**: activates supply chain, fulfillment, and logistics reasoning
- **Cultural consultant**: activates local market norms, communication styles, consumer behavior

Each persona steers the model toward expertise and vocabulary that the others wouldn't surface. The same base model produces meaningfully different — and deeper — analysis depending on the persona it's given. This is the practical business application of what Anthropic's interpretability research demonstrates at the neural level.

### What to Cover

1. **The mental model** — Sequential research is how most people use AI. You ask one question, get an answer, ask the next. Parallel subagents let you ask 5 questions at once, each answered by a differently-configured "specialist."

2. **Defining persona vectors** — Show how to write subagent prompts that go beyond "research X" and instead define:
   - Who the subagent is (expertise, perspective, what they care about)
   - What they're specifically looking for (not just "findings" but the *type* of signal)
   - How to format their brief (so the synthesis step is clean)

3. **Demo: "Should we expand into the UK market?"** — Spawn 4-5 subagents in parallel:
   - Regulatory landscape subagent (persona: compliance officer)
   - Competitor analysis subagent (persona: market intelligence analyst)
   - Pricing & unit economics subagent (persona: CFO)
   - Logistics & fulfillment subagent (persona: operations director)
   - Cultural & comms subagent (persona: local market consultant)

4. **Synthesis** — The main agent collects all briefs and produces a unified recommendation with cross-references between dimensions (e.g. "the regulatory subagent flagged X, which conflicts with the pricing subagent's assumption about Y")

5. **Time comparison** — Show wall-clock time: sequential approach (~45 min for the same depth) vs parallel (~8 min). Same quality, fraction of the time.

> "It tracked how every proposed concession interacted with provisions across the agreement, flagged where accepting one change would create exposure in another section, and helped me build a response that conceded the points worth conceding and held firm on the ones that mattered."
> — [Zack Shapiro (@zackbshapiro)](https://x.com/zackbshapiro/status/2027389987444957625)

### Key Demo

Start with a single business question. Show the subagent prompts with their persona definitions. Launch them all at once. Watch the briefs come back. Synthesize into a decision-ready memo. Emphasize: the personas are what make each brief *different* — without them, you'd get five copies of the same generic research.

### Connection to Existing Content

Builds on the "Multi Subagents for Hard Problems" technique video (which covers the coding pattern). This video is the *business application* — the focus is on persona design and real-world decision-making, not the technical implementation.
