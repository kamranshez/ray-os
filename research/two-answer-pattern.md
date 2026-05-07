---
status: idea
---

**The two-answer pattern.** *"Give me your answer. Then give me the answer you'd give if your first one was wrong."*

The first answer is whatever the model converges to fastest. It's the path of least resistance through its weights. The second answer is the one it would have given if the first one didn't exist. Often it's better, because the first answer was a local optimum and the model just needed permission to step away from it.

This is functionally a one-shot way to get diverse samples without spinning up a second context. You're forcing the model to model the distribution of plausible answers, not just emit the mode of it.

Works best for design decisions, naming, framing, and anywhere the "obvious" answer is suspiciously obvious.
