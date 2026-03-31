---
duration: "5-7 min"
order: 7
class: "skills"
chapter: "Your First Skill"
status: "new"
---

## Writing Descriptions That Actually Trigger

The activation rate problem and how to fix it.

### The Problem

"Studies suggest skill activation sits around 20% for marketplace skills. They'd activate only one in five times — which begs the question, what's the point?" (7 Levels)

Even with proper hooks and optimized descriptions, best case is ~84%. "Still one out of five times it will not run the correct skill." (7 Levels)

### The Three-Part Description Framework

1. **Trigger**: When should this fire? "triggers on: research, trending, what's new in, find me topics..."
2. **Not-trigger**: When should it NOT fire? "does NOT trigger for: general web browsing, simple URL fetching, reading a single article"
3. **Outcome**: What does it produce? "produces: a research brief with TLDR, key facts, pros/cons, sources"

From the 7 Levels video: "Firstly write the trigger — what is the event or situation. What should NOT trigger it. And what is the outcome produced."

Chase's example of good description: "When the user needs marketing ideas, inspiration or strategies. Also used when: marketing ideas, growth ideas, how to market, marketing strategies, marketing tactics, ways to promote, ideas to grow."

### What to Show

1. Take the research skill from 2.2
2. Give it a vague description: "helps with research"
3. Run 5 different prompts — count how many times it triggers (~2/5)
4. Optimize with the 3-part framework
5. Run same 5 prompts — count again (~4-5/5)

### The Three Invocation Modes

1. **Vague** ("let's research this") — pray it triggers. ~20-84% depending on description quality.
2. **Explicit** ("use the research skill") — Claude takes the hint. Much more reliable.
3. **Forced** (`/research-skill`) — 100% guaranteed. "I find the best way to get around all that is just to use the slash command so there's not that confusion of the AI trying to decide." (Lenny)

### Three Layers of Trigger Reliability

Callback to Ch 1.3:
1. Global profile setting ("Always consider using the most appropriate skill") — the foundation
2. Good 3-part description — helps Claude pick the right skill
3. /slash invocation — guarantees it fires

### Cross-Links

- [[Triggering Skills Reliably]] (context-engineering class) — layer-node tricks to boost rates to 95%
