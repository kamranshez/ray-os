---
duration: "10-14 min"
batch: 1
order: 3
batch_name: "Setup"
class: "loopy-ai"
chapter: "Strip The Model Out"
aliases: [strip-the-model-out]
status: stub
---

Stub for the Setup hands-on opener. Build a fully deterministic loop before the model ever shows up.

## Thesis

New students conflate "loop" with "LLM." The fastest way to fix that is to build a loop with no LLM in it at all. Cron plus bash plus a static rubric plus a state file. Once you've felt the rhythm of trigger, work, check, terminate, statefulness, dropping a model into one slot becomes intuitive.

Most failed loop builders skipped this step. So when something breaks they can't tell if it was the model or the loop. This segment buys that diagnostic skill cheaply.

## Why exactly five primitives

Not borrowed from control theory or OODA — those have different commitments. Five is the minimum set where each primitive answers a question the loop cannot avoid:

- **Trigger** — when does the loop start? (cron, file change, queue item, manual)
- **Work** — what runs in one iteration?
- **Check** — did this iteration succeed?
- **Terminate** — should the loop keep going?
- **State** — what survives between iterations?

Strip any one and the loop breaks in a named way. No trigger: the loop never starts, or starts at the wrong cadence. No work: nothing happens. No check: you can't tell if the work worked. No terminate: it runs forever. No state: every iteration starts from scratch and the loop can't learn or resume.

When something goes wrong, this is the diagnostic surface: name the primitive that misbehaved. That's faster than blaming "the agent."

## Key beats

- The five primitives of any loop: **trigger** (what fires it), **work** (what runs), **check** (what tells you it's done), **terminate** (when to stop), **state** (what survives between runs).
- Worked example: a loop that checks every five minutes whether your homepage returns 200, retries up to three times, posts to Slack on the third failure. No model. Pure bash + cron + a state file.
- Add a second example: a loop that watches a folder for new markdown files, runs `markdownlint` on each one, writes a `.passed` or `.failed` marker. Still no model.
- The reveal: drop a model into exactly one slot (the "fix the lint failures" slot). Everything else stays deterministic. Now you have an L2 loop and you can see exactly what changed.
- Diagnostic: if your AI loop is misbehaving, ask "would the deterministic version of this loop work?" If yes, the model is the problem. If no, the loop design is the problem.

## Pedagogical claim

This is the segment that justifies the reorder. After this, students understand that verification and governance are loop primitives, not LLM features. The rest of the class teaches them how to wire models into those primitives instead of around them.

## Sources / refs

- Loop Bank idea #6 (deterministic-first pedagogy)
- Pairs with [[closing-the-loop]] as the model-augmented version
- Pairs with [[governance-primitives]] as the rules-around-the-loop layer

## TODO

- Demo: show the cron job running, show the state file changing on disk, show one iteration of the loop, then add the model.
- Image: side by side. Deterministic loop on the left (five labelled boxes). Same loop on the right with one box swapped for a model call.
