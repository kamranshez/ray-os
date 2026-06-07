---
duration: "10-14 min"
batch: 5
order: 1
batch_name: "Closing"
class: "loopy-ai"
chapter: "Mission Command"
status: stub
---

Stub for the L7 operating model segment. Auftragstaktik for your fleet.

## Thesis

The Prussian and later US military doctrine of *Auftragstaktik* gives subordinates the commander's intent plus latitude on method. Tell them *what good looks like*, *what tradeoffs are acceptable*, *what is out of bounds*. Don't tell them what to do.

This is the L7 operating model for a fleet of loops. At L1-L3 you write prompts. At L4-L6 you write *intent documents*.

Most people micromanage the prompt and call it strategy. The diagnostic is simple: if your loops can't operate without you editing their prompts weekly, you have not written intent. You have written a script.

## Key beats

- The Auftragstaktik origin and why it beat the rival doctrine of detailed orders. The world is fast. Subordinates see things commanders can't. Latitude is a feature.
- What an intent doc contains: the mission, the success criteria, the tradeoff order (when speed beats quality, when quality beats speed, when neither), the kill criteria, the escalation rules.
- What an intent doc does *not* contain: step-by-step instructions, prompt templates, specific tools to use.
- The two-line test: a new loop joining your fleet should be operable from the intent doc alone. A senior engineer joining your team should be able to ship without checking with you. Same test.
- Where intent docs fail: vague success criteria, no tradeoff order, no kill criteria. Then they're just vibes in a document.
- Connection to [[writing-effective-goals]]: a /goal is a tactical intent doc for one task. A fleet intent doc is the same thing zoomed out for a continuous operation.
- Connection to [[governance-primitives]]: the intent doc is what governance enforces against. Without it, governance has nothing to compare to.

## The prompt-versus-intent diagnostic

> If you edit a loop's prompt more than once a month, you have a prompt.
> If you edit its intent doc more than once a quarter, you have a draft.
> If you edit neither, you have a working operation.

## Sources / refs

- Auftragstaktik / mission command military doctrine
- Loop Bank idea #4
- Pairs with [[writing-effective-goals]] (tactical version) and [[governance-primitives]] (the enforcement layer).
- Sets up [[loop-design-as-craft]] (the closing argument — taste lives in rubrics and intent docs, not in single prompts).

## TODO

- Demo: open one of Ray's actual intent docs on screen. Read it out. Count the lines of "what" versus lines of "how." Should be heavily weighted toward what.
- Image: a commander on a hill pointing at the horizon. Below, several squads moving differently toward the same point.
