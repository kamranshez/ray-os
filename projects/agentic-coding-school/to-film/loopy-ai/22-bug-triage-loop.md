---
duration: "14-18 min"
batch: 6
order: 22
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Bug Triage Loop"
aliases: [bug-triage-loop]
status: stub
---

Stub for the Rippling bug triage segment. The highest-leverage loop a team can run.

## Thesis

Rippling shipped AI across every product in six months for over a million users. The mechanism is a single loop: failing traces in, fixes out, re-run evals to confirm, human reviews and merges.

This is L4 worker + L5 discovery + L2 verifier composed into one production pipeline. It is the highest-leverage agentic loop most teams haven't built, because it compounds on every other loop in the system. Every bug it fixes makes every other loop slightly more reliable.

If you build one loop after this class, build this one.

## The pipeline

1. **Source.** LangSmith (or your trace store) emits failing production traces.
2. **L5 triager.** Picks the traces worth fixing today. Ranks by user-impact and reproducibility.
3. **L4 worker.** For each picked trace, an agent analyses the failure, proposes a fix, opens a PR.
4. **L2 verifier.** Re-runs the eval suite. The PR only stays open if the fix closes the regression *and* doesn't break the rest of the suite.
5. **Human review.** Final merge gate. The human reads the action log, not just the diff.

## Why it compounds

Most loops fix one artifact. This loop fixes the *thing that fixes artifacts*. The first time it runs, you have N bugs and one fixer. The hundredth time, you have far fewer bugs *and* a fixer that's seen 99 failure modes encoded in its evals.

The eval suite is the asset. The fixer is replaceable. New Rippling devs join and the suite is what they learn the product from. Same property as the ACE playbook.

## Key beats

- Why this is the compounding meta-loop. It improves the loops that produce the things it fixes.
- The eval suite is the moat. Without one, this loop can't run. With one, it gets better forever.
- Why the human stays in for the merge. Production code change. Not because the loop is untrustworthy. Because the *consequences* are.
- This is an instance of ACE: Generator is the fixer, Reflector is the eval suite, Curator is whatever maintains the evals.
- Most teams don't have an eval suite. That's the first thing to build, not the loop on top of it.

## Sources / refs

- LangChain blog: "How Rippling went AI-native across every product in 6 months with deep agents and LangSmith"
- Loop Bank idea #3
- Pairs with [[ace-three-role-split]] (this is ACE in production) and [[adversarial-reviewer-skill]] (the eval suite is the structured Reflector).
- Sets up [[echo-chamber]] (the failure mode that catches teams that don't refresh their eval suite).

## TODO

- Diagram: the five-stage pipeline on screen, with each stage labelled by its L-level.
- Demo: ideally one of Ray's own loops in this shape, even a smaller one. Sentence-mining with a re-grader works as a stand-in.
- Image: a hexagonal flow. Trace store at the top. Triager and worker on the left. Eval suite and human on the right. PR merging at the bottom.
