---
duration: "12-16 min"
batch: 3
order: 5
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "Closing The Loop"
aliases: [closing-the-loop]
status: stub
---

Stub for the canonical L2 segment. Build, check, on fail fix, check again. Loop until the bar is met.

## Thesis

L1 is the model deciding "I think I'm done." L2 is something *other than the model* checking "are you actually done." That other thing is the verifier. Until the check passes, the loop keeps going.

This is the first loop most students should actually build. Everything in The Climb sits on top of it.

## What a verifier actually is

> A **verifier** is a non-builder process that takes the work artifact as input and returns a structured pass/fail (or score against a threshold) that the builder cannot rephrase its way past.

Three properties have to all hold. **Non-builder**: it can't be the same model call that produced the artifact. **Structured output**: a number, a boolean, a typed report — not prose the builder gets to interpret. **Rephrase-immune**: the verifier judges the artifact, not the builder's description of the artifact.

If any one of those fails, you have a self-graded loop wearing L2 clothes.

This is the load-bearing definition for the rest of the class. Every later segment — borrowed verifiers, the adversarial reviewer, ACE — points back at it.

## Mapping back to the five primitives

In [[strip-the-model-out]] we built a loop with five primitives: trigger, work, check, terminate, state. L2 doesn't replace that taxonomy; it specialises it.

- **builder** = the work primitive, now with a model in it
- **work artifact** = the output of the work primitive (file, diff, draft)
- **verifier** = the check primitive, made non-trivial
- **exit condition** = the terminate primitive, expressed as "verifier returns pass"
- **trigger** and **state** are inherited from L1 and don't change shape at L2

Two consequences. First: the four-part anatomy is the five-primitive loop with the model dropped into one slot. Second: anything you do at L3 and above doesn't add new primitives — it just changes which slot owns what.

## Key beats

- The four-part anatomy: builder, work artifact, verifier, exit condition.
- Steipete's /review loop. Write code, run /review, fix the findings, /review again. Exits when /review finds nothing material.
- Playwright write-test-fix. Generate a test, run it, watch it fail, fix the implementation, re-run. Exits when test goes green.
- Cursor's quality-review skill. Same shape, different artifact.
- One agent or two? Same model can play both roles, switching prompts. Or two agents in series. The L2 shape doesn't care, but the failure mode is the same: don't let the *checker* be a re-statement of the *builder*.
- Why a separate subagent helps, and where it stops. In the builder's own context the model has already said "done" and now reads its own work as something to defend. A fresh window hasn't committed to anything, so it can actually look. That makes "non-builder" partly a *context* property, not just a *prompt* one. But fresh context only buys honesty, not rigour. The checker still needs a reason to disagree: a borrowed verifier that observed something, or an asymmetric prompt told to refute. Clean context plus no reason to push back still rubber-stamps. See [[borrowed-verifiers]] for the grounded version, [[adversarial-reviewer-skill]] for the prompted version.
- This is the pattern that [[borrowed-verifiers]] then makes concrete by sourcing the verifier from outside the model.
- This is the pattern that [[adversarial-reviewer-skill]] then sharpens by making the checker asymmetric.

## What this segment is *not*

Not the same as Ralph (that's L3, runs the *whole* outer task in a fresh window). Not the same as goal mode (that's the runtime owning the loop). L2 is one artifact, one verifier, one exit condition.

## Sources / refs

- Pairs with [[strip-the-model-out]] (the deterministic version), [[borrowed-verifiers]] (where the check comes from), [[adversarial-reviewer-skill]] (the asymmetric-prompt variant), [[architecting-the-loop]] (what tools the agent needs to close it).

## TODO

- Demo: a tiny build-test-fix loop on screen. Three iterations max. Show the loop exit when the test passes.
- Image: builder box, artifact, verifier box, arrow back from "fail" to builder, arrow out from "pass."
