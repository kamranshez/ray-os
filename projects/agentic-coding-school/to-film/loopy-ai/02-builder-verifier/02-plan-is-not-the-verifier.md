---
duration: 8-12 min
batch: 2
order: 2
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [plan-is-not-the-verifier, dont-verify-against-the-plan]
---

> STUB. The drawback teed up on camera in 01-builder-verifier ("I'll talk about verifying against the original plan in a later video"). This is that video.

## Thesis

If the model checks its output against the plan it wrote, you don't have a loop — you have a mirror. A flawed plan rubber-stamps flawed work.

## The trap

The seductive setup: agent writes a spec, builds against it, then "verifies" by re-reading the spec and confirming it matches. Every box ticked. The plan and the build came from the same model with the same blind spots, so the check passes on exactly the cases it should catch. This is the GPT-5 "76% fabricated pass" failure from the intro, in miniature — self-grading wearing a loop costume.

## The fix — the verifier must be *outside* the plan

Three escape hatches, in order of strength:

- **Reality** — run the code, hit the endpoint, render the page, open Chrome and click. The world doesn't care what the plan said.
- **An independent artifact** — tests written *before* the plan, an acceptance rubric the model didn't author, ground-truth data.
- **A fresh-context reviewer** — a second agent that never saw the plan, judging the output cold. (Callforward to 04-pair-creator-with-attacker.)

## Map onto the five components

The failure is entirely in **Check** — it was wired to **State** (the plan) instead of an external signal. Naming it that way is the whole lesson.

## Demo

Show an agent "verifying" a function against its own spec and passing — then run the actual test and watch it fail. Same artifact, two checks, opposite verdicts.

## Key Insight

> A verifier that can read the plan is not a verifier. It's a co-author.
