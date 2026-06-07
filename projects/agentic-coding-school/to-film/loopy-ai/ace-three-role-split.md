---
duration: "14-18 min"
batch: 4
order: 1
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Three Role Split (ACE)"
status: stub
---

Stub for the ACE segment. The canonical architecture for self-improving loops without RL.

## Thesis

Stanford, SambaNova, and Berkeley shipped ACE in October 2025: a three-role split that lets the model improve without changing weights. The model weights stay frozen. The *instructions and lessons* the model sees before working get updated.

This is the formal version of what the rest of the class has been building toward. Once students see ACE, they realise every prior segment was an instance of this architecture. The class snaps into shape.

## The three roles

- **Generator.** Does the work. The L1 builder.
- **Reflector.** Reviews what the Generator did. Finds patterns of failure, names them. The adversarial reviewer from segment 2.3, applied at scale.
- **Curator.** Updates the playbook the Generator reads before its next attempt. The thing that captures the lessons, not the lessons themselves.

The model weights never change. The Curator changes the *context* the model sees. Taste lives in the playbook, not in the weights.

## Why this matters

- Reported +10.6% on agent benchmarks at lower cost than fine-tuning.
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
