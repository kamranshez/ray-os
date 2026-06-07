---
duration: "12-16 min"
batch: 2
order: 1
batch_name: "Foundations"
class: "loopy-ai"
chapter: "Closing The Loop"
status: stub
---

Stub for the canonical L2 segment. Build, check, on fail fix, check again. Loop until the bar is met.

## Thesis

L1 is the model deciding "I think I'm done." L2 is something *other than the model* checking "are you actually done." That other thing is the verifier. Until the check passes, the loop keeps going.

This is the first loop most students should actually build. Everything in The Climb sits on top of it.

## Key beats

- The four-part anatomy: builder, work artifact, verifier, exit condition.
- Steipete's /review loop. Write code, run /review, fix the findings, /review again. Exits when /review finds nothing material.
- Playwright write-test-fix. Generate a test, run it, watch it fail, fix the implementation, re-run. Exits when test goes green.
- Cursor's quality-review skill. Same shape, different artifact.
- One agent or two? Same model can play both roles, switching prompts. Or two agents in series. The L2 shape doesn't care, but the failure mode is the same: don't let the *checker* be a re-statement of the *builder*.
- This is the pattern that [[borrowed-verifiers]] then makes concrete by sourcing the verifier from outside the model.
- This is the pattern that [[adversarial-reviewer-skill]] then sharpens by making the checker asymmetric.

## What this segment is *not*

Not the same as Ralph (that's L3, runs the *whole* outer task in a fresh window). Not the same as goal mode (that's the runtime owning the loop). L2 is one artifact, one verifier, one exit condition.

## Sources / refs

- Pairs with [[strip-the-model-out]] (the deterministic version), [[borrowed-verifiers]] (where the check comes from), [[adversarial-reviewer-skill]] (the asymmetric-prompt variant), [[architecting-the-loop]] (what tools the agent needs to close it).

## TODO

- Demo: a tiny build-test-fix loop on screen. Three iterations max. Show the loop exit when the test passes.
- Image: builder box, artifact, verifier box, arrow back from "fail" to builder, arrow out from "pass."
