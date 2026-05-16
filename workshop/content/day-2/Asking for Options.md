---
status: stub
acs:
  - class: fundamental-techniques
    title: "Multiple Proposals"
mapping: mapped-partial
day: 2
block: core
---

# Asking models for options preserves human judgment

## The idea
If you tell a model to do a thing, it just starts tumbling out tokens. Whatever first token it spits out sets a path, and it follows that path because each next token is the most likely continuation. Once it's down that road, it's hard to steer off. But if you ask "which of these things should we do?" the model tries to read what you actually want and surfaces tradeoffs. The human then does the thinking — the model just lays out the option space.

## Why this works
- Models can pull patterns from your codebase that you haven't thought of
- They can enumerate tradeoffs faster than you can
- But they cannot make the *decision* without rolling dice on first-token momentum
- The valuable part of the model is the breadth of options, not the choice

## How to apply
- Default phrasing: "give me 3-5 options for X with tradeoffs" instead of "do X"
- Read the options, do real human thinking, pick one, then commit
- If you don't know which to pick, ask the model to advocate for one — but recognize you're now back in sycophancy territory
- Once you commit, *then* tell the model the decision and let it execute

## Surrounding context
Dex's framing: "do not outsource the thinking. If you let the model make decisions you're rolling the dice." This is the core of the design-discussion workflow Vibhav and Dex use — the markdown doc isn't just a spec, it's a forcing function that makes the model produce options at every branch point so the human can resteer before code gets written. The whole "five hours iterating on ticket two" workflow exists specifically to maximize the number of decision points where the human can intervene.

## Open questions to explore
- What's the right number of options? 3 feels artificial, 10 is overwhelming
- How do you get the model to surface *non-obvious* options, not just the conventional three?
- Can you train a habit of always demanding options, or does it feel like overkill on small tasks?
- When is "just do it" actually the right call vs. always-options-mode?
