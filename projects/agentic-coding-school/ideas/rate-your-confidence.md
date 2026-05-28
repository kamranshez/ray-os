---
status: idea
---

**Rate your confidence.** After any non-trivial answer, ask: *"rate your confidence 1-10 and explain what would have to be true for this to be wrong."*

Models default to a flat, confident tone whether they actually know the answer or are stitching plausibility together. Forcing a numeric rating breaks the flatness. A 9/10 with a weak counterfactual is suspicious. A 5/10 with a sharp counterfactual is honest, and useful.

The second half is the load-bearing part. The number alone is cheap. The "what would have to be true for this to be wrong" forces the model to actually model its own uncertainty, not just label it.

Use it on architectural decisions, debugging hypotheses, and anything where being wrong costs you a day.
