---
status: filmed
---

**Boxing the Model In** is the anti-pattern of over-engineering how the AI works instead of trusting it to figure things out.

![[images/boxing-the-model-in.png]]
## What it looks like

- **Rigid orchestration** — Writing strict step-by-step pipelines: "do step 1, then step 2, then step 3." It feels thorough, but you're really just encoding your assumptions about how the problem should be solved. The model might have found a better path, but you've locked it out.
- **Context hoarding** — Dumping everything upfront: every file, every spec, every constraint. The model drowns in irrelevant context instead of pulling in exactly what it needs, when it needs it. It's like giving someone a 500-page manual before asking them to fix a lightbulb.

![[images/boxing-the-model-in-2.png]]
## Why it backfires

- **Brittle vs adaptive** — A rigid pipeline breaks the moment something unexpected happens. Step 3 assumes step 2 produced a certain output, but it didn't, and now the whole chain collapses. A model with tools and a goal can just adapt — hit a wall, try something else, read another file.
- **The control illusion** — A 20-step orchestration *feels* like control, but it's really just your assumptions hardcoded into a sequence. You're constraining the model to your solution path, not the best solution path.
- **The trust gap** — This is fundamentally about not trusting the model. A year ago, that distrust was justified — models needed guardrails. But capability has moved faster than habits. People are still building scaffolding for a model that doesn't need it anymore.

![[images/boxing-the-model-in-4.png]]
## What to do instead

- Give it tools (file reading, search, code execution), give it a clear goal, and get out of the way. It's the difference between giving someone turn-by-turn GPS directions vs giving them a destination and a car. The second approach lets them adapt to traffic, take shortcuts, and recover from wrong turns.

![[images/boxing-the-model-in-3.png]]

> Source: [Boris Cherny (1:03:44)](https://www.youtube.com/watch?v=We7BZVKbCVw&t=3824)
