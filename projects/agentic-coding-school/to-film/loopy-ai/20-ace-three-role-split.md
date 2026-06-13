---
duration: "14-18 min"
batch: 6
order: 20
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Three Role Split (ACE)"
aliases: [ace-three-role-split]
status: stub
---

Stub for the ACE segment. The canonical architecture for self-improving loops without RL.

## Thesis

Stanford, SambaNova, and Berkeley shipped ACE in October 2025: a three-role split that lets the model improve without changing weights. The model weights stay frozen. The *instructions and lessons* the model sees before working get updated.

This is the formal version of what the rest of the class has been building toward. Once students see ACE, they realise every prior segment was an instance of this architecture. The class snaps into shape.

## The three roles

- **Generator.** Does the work. The L1 builder.
- **Reflector.** Reviews what the Generator did. Finds patterns of failure, names them. **This is the [[adversarial-reviewer-skill]] you built earlier — the asymmetric attacker-prompt is the Reflector primitive, now lifted out of the L2 loop and run at the playbook scale.** Name it explicitly on camera: students should feel the "oh, I've already built one of these" moment land.
- **Curator.** Updates the playbook the Generator reads before its next attempt. The thing that captures the lessons, not the lessons themselves.

The model weights never change. The Curator changes the *context* the model sees. Taste lives in the playbook, not in the weights.

## Why a third role instead of "Verifier with memory"

The fair question: why not just bolt a memory store onto the L2 verifier and call it done?

Two answers, both structural. **First, separation of concerns.** A verifier judges *one artifact*. A Reflector looks across a window of iterations and extracts *patterns* — "the Generator keeps over-fitting to recent failures," "every fix that touches X regresses Y." Cramming that role into the verifier collapses the cross-iteration view back into a single-shot judgment and you lose the pattern. **Second, the Curator is a write role, not a memory role.** A memory store is a passive log. The Curator actively rewrites the playbook the Generator reads next iteration, with bullet-level dedup and obsolescence rules. That's not "verifier plus memory" — it's a different job.

## Failure routing: what does the Architect see on a plan-fail?

When a plan-and-execute split fails, there's a real design call: does the Architect (plan author) see the Coder's raw diff when drafting plan v2, or only the verifier's structured failure report?

**The class commits to: verifier's structured failure report, not the diff.** Reasoning: showing the Architect the diff puts implementation context into a role whose job is to plan, and it leaks Coder-local concerns upstream. The structured failure report ("test X failed because assertion Y, the affected module is Z") is the right Architect-grain signal. The Coder's diff is the Coder's local concern.

This matches Anthropic's three-agent "sprint contract" framing more than ACE's Curator framing — and it's the right pick here because we're a class about loop design, not weight-free continual learning. If you ever flip this for your own loops, write down why, because the wrong default will silently turn your three-role split back into two roles.

## Why this matters

- Reported +10.6% on the AppWorld agent benchmark with DeepSeek-V3.1-671B; +12.3% over in-context learning baselines; +11.9% over GEPA. Cite the specifics, not the bare headline — the bare number won't survive a skeptical learner.
- No GPU cluster needed. Anyone can run this architecture.
- **The playbook survives model swaps.** Upgrade from Sonnet 4.6 to Sonnet 5.0 next year, your taste files are still your taste files. Compounding asset on top of the model, not inside it.
- Reframes "prompt engineering" as a Curator role, not a one-shot writing task.

## Key beats

- The architecture diagram: Generator does the work, Reflector reviews it, Curator updates the playbook, Generator reads the playbook on the next iteration. Loop.
- Connect back: every example in the class so far has had a Generator and a check. ACE just names the third role and makes it explicit.
- The Curator role is where taste *lives*. This is where the "Where Taste Went" closing argument lands.
- Operational advice: keep the playbook in version control. The diff *is* the learning. Read the diff like you'd read a code review.

## Sources / refs

- Stanford / SambaNova / Berkeley ACE paper, October 2025
- Source: Karo Zieminski substack on context engineering
- Loop Bank idea #1
- Pairs with [[adversarial-reviewer-skill]] (the Reflector building block) and [[bug-triage-loop]] (an ACE in production).
- Sets up [[loop-design-as-craft]] (the Curator is where taste went).

## TODO

- Demo: one of Ray's actual loops, broken open. Show the Generator prompt, the Reflector prompt, the playbook file the Curator maintains, and the git diff on the playbook from the last week.
- Image: three boxes in a triangle. Generator does, Reflector judges, Curator writes. The playbook sits in the middle and everyone reads or writes it.
