---
duration: "14-18 min"
batch: 3
order: 5
batch_name: "The Climb"
class: "loopy-ai"
chapter: "Autoresearch"
status: stub
---

Stub — Karpathy-style eval-driven autonomous loop. Run a skill, score against binary evals, mutate the prompt, keep improvements.

Local skill version lives at `~/.claude/skills/autoresearch/`. This is the segment where the loop optimises the *prompt*, not just the work.

## What an eval suite actually is

Before we mutate anything, define the artifact this segment leans on.

> An **eval suite** is a fixed set of inputs plus a borrowed verifier per input, run end-to-end against any candidate prompt, returning one structured score per case and an aggregate pass/fail for the run.

Three properties: **fixed inputs** (so you compare runs apples-to-apples), **borrowed verifier per case** (from [[borrowed-verifiers]] — no self-grading), and **aggregate gate** (binary "did the candidate beat the incumbent" — see next beat for why binary).

This is the artifact you write before the prompt. The autoresearch loop mutates the prompt; the eval suite never moves. If the eval suite moves, you're not running an experiment, you're drifting.

## Key beats

- The eval-first mindset: write the evals before the prompt.
- Binary evals beat scored evals for mutation gating. "Did it improve" is the question, not "by how much."
- The mutation engine: how to propose prompt changes that don't drift the policy.
- Connection to [[ace-three-role-split]]: autoresearch is an ACE variant where the Curator's job is to mutate the Generator's prompt and keep what wins.
- Connection to [[../automation/auto-research-for-non-technical-work]]: the operator-grade version with experiment tables and real-world graders.

## Sources / refs

- Karpathy's framing
- Pairs with [[ralph-loops]] (the outer loop), [[goal]] (the runtime), [[borrowed-verifiers]] (where the eval signal comes from), [[ace-three-role-split]] (the formal architecture), [[echo-chamber]] (the failure mode this segment most needs to warn about).
