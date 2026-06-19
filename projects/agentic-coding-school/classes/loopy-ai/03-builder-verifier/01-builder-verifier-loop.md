---
video_id: "JXKjbw8I"
duration: 14-18 min
batch: 2
order: 1
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [builder-verifier-loop]
---
## Kernel (from the old stack walkthrough)

Build. Test. On fail, fix. Test again. Loop until the bar is met.

Sometimes one agent plays both roles, switching between them. Sometimes two agents. Either way, the loop only exits when an external check passes.

Examples.

Write code, run pytest, fix failures, run pytest again. That's the canonical L2.

Generate a thumbnail. A judge agent rates it on a rubric. If the score is below eight, regenerate. That's L2 too.

Draft an email. A critic agent flags issues. Rewrite. Re-critique. That's L2.

The thing that makes L2 different from L1 is the *verifier*. L1 is the model deciding "I think I'm done." L2 is something other than the model checking "are you actually done." Until the check passes, the loop keeps going.

[IMAGE: a build -> test -> on-fail-fix -> test-again loop around a single artifact, with an external verifier check gating the loop exit, the artifact converging to a quality bar]

![[loopy-loop-stack-l2-builder-verifier-4.png]]
## Map onto the five components (the spine for this segment)

- **Trigger** — a manual run, or the previous artifact landing.
- **Work** — the builder produces/edits one artifact.
- **Check** — the verifier (pytest, a rubric judge, a critic) — the *external* signal that defines L2.
- **Terminate** — "until the bar is met" / max iterations / budget.
- **State** — the failing output carried back into the next build.

## Notes to incorporate

- This is the on-ramp to the "closing the loop" pattern (segment 05) — preview it, don't fully unpack it here.
- The underclaim misnaming example (a queue worker is L4, not "closing the loop"/L2) now lives in the intro; can callback to it here.
