Worked example for Day 6. The principle lives on Day 5 in [[Designing Codebases AI Loves]]; this stub turns it into a skill students build.

## What the skill does

Walks the codebase, finds shallow modules and other AI-hostile patterns, and proposes refactors. Output is a prioritised list, not a sprawling diff:

- **Shallow modules** — fat interface, thin implementation. Candidates to inline or absorb.
- **God files** — one file doing five jobs. Candidates to split.
- **Leaky abstractions** — interfaces that force callers to know the implementation. Candidates to redesign.
- **Naming drift** — same concept named differently across files. Candidates to unify.
- **Dead code** — unreferenced exports, unused branches. Candidates to delete.

Each item gets: where it is, why it's a problem for an agent, and the smallest refactor that fixes it.

## Why "for an agent" changes the calculus

Agents pay for every line they read. A shallow module forces an 800-line pull for a one-line change; a deep module with the same surface area cuts that to 80. This isn't generic clean-code advice — it's "make the repo cheap to navigate for an agent." The refactor that nobody bothered to do when humans were the only readers now has a measurable payoff: next session uses 10× less context for the same edit.

That framing also tells students *which* findings to act on first. Refactor the modules the next PRD will touch. Leave the cold corners of the repo alone.

## One skill or several?

Useful Day 6 design moment: should this be one `/improve-my-codebase` skill or several smaller ones — `/find-shallow-modules`, `/dedupe-naming`, `/find-god-files`?

- **One big skill** — fewer commands to remember, holistic ranking across pattern types, but harder to evaluate and harder to iterate when one detection rule misfires.
- **Several small skills** — each one is independently testable, easier to chain into other workflows, easier to improve in isolation. Cost: more surface area for the student to keep in their head.

No single right answer. The point of raising it is that *skill scope is a design decision*, and Day 6 is where students should start having an opinion about it.

## Why this earns a slot on Day 6

Day 6 is skills as a discipline. This skill is a clean teaching case because:

- It has a clear input (the repo) and a clear output (a list).
- The principles behind it ([[Designing Codebases AI Loves]]) were taught the day before, so students aren't learning two things at once.
- It's the kind of skill students will actually re-run — codebases drift, and re-running the skill quarterly is a real workflow.
- It pairs with [[Simplify Skill]] as the other "improve the code" skill. Simplify is line-level; this one is module-level.

## Building it in the lesson

The lesson follows the same arc as [[Blog Post to Skill]] — start from the principle, write the skill, measure it. The measurement piece ([[Measuring Skill Effectiveness]]) matters here because "did the refactor help?" isn't obvious until the next AI session works in the changed area. Good eval: pick a feature, ask an agent to add it before and after the refactor, compare context use and edit accuracy.

## The PRD update

After students build this skill, the Day 4 PRD skill gets a small extension: when planning a feature, run the codebase improvement skill on the modules the PRD touches *first*. Refactor for legibility, then write the PRD against the cleaner shape. This is the "module-aware PRD" idea — and it only works once students have the skill that finds the modules.
