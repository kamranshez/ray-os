---
duration: "10-14 min"
batch: 2
order: 3
batch_name: "Foundations"
class: "loopy-ai"
chapter: "Pair Every Creator With An Attacker"
status: stub
---

Stub for the adversarial reviewer skill segment. Every creation skill ships with a sibling whose only job is to refute the output.

## Thesis

A skill that creates something needs a partner skill that attacks it. Same model. Opposite prompt. The creator is told to build, the attacker is told that its job is rigour, not agreement. Run them in series, surface only the disagreements, fix upstream.

This is the L2 building block that the rest of the class needs. ACE (segment 4.1) calls it a Reflector. The bug triage loop (4.2) uses it for fix verification. The class compounds on this primitive.

## Key beats

- Bad pattern: agent writes a PRD, same agent reviews the PRD, says "looks good." Vibes.
- Good pattern: PRD creator skill writes the PRD. PRD attacker skill is invoked next, with a system prompt that says "your job is to refute. Default to refuted unless the case is airtight. Specifically hunt for miracle steps, vague assumptions, and untested invariants."
- The two prompts are stored as separate skills, both deployable, both reusable. Not a one-off conversation pattern.
- Three examples:
  - PRD creator / PRD reviewer (hunts miracle steps, vague assumptions)
  - Code writer / Code reviewer (flags what shipped versus what was specced)
  - Copy writer / AI-slop hunter (cuts the model's tells)
- The skill-pair shape is what makes this portable across the loop stack. Same primitive shows up in L2, L4, L5 and L6.

## What makes this different from "use a different model"

You don't need a different model. You need a different *prompt*. The attacker prompt is heavily weighted toward refusal. Same weights. Asymmetric instructions. That's the trick.

Two levers, though, not one. The prompt is the bigger lever: same weights, instructions weighted toward refusal. The context is the quieter one. Run the attacker as a separate subagent, not a follow-up turn in the same thread. In one context the model has already written "here is the PRD" and now reads its own work as something to defend; a fresh window reads it as something to break. This is why subjective work (a PRD, a plan, copy) leans harder on this pattern than code does: code has borrowed verifiers that touch reality, so the verifier already has a reason to disagree. Prose has no compiler, so the only independent grade you can get is a fresh context pointed at refutation. Use both levers: the asymmetric prompt for the reason to disagree, the fresh context so nothing is already committed.

## Sources / refs

- Loop Bank idea #2 (adversarial reviewer skill pattern)
- Source: PMData substack on skill pairing
- Pairs with [[borrowed-verifiers]] (external grader) and [[closing-the-loop]] (verifier-in-the-loop)
- Sets up [[ace-three-role-split]] (Reflector role)

## TODO

- Demo: a PRD creator skill outputs a PRD with one miracle step in it. The PRD reviewer skill catches it. Show the system prompts side by side so the asymmetry is obvious.
- Image: two heads facing each other. Same colour, same shape. One labelled "build." One labelled "refute."
