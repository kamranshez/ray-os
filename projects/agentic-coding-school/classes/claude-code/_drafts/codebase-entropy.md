---
class: "claude-code"
status: "scripted"
acs: []
mapping: workshop-original
recording-needed: true
day: 1
block: core
---
The load-bearing mental model for the whole workshop: **AI is a multiplier on your codebase, not an additive**. A clean repo compounds AI gains upward. A messy one accelerates decay faster than humans can refactor it back. The sign of the multiplication is set by what you bring to the table.
## The thesis in one line

Productivity gains from AI correlate weakly with token spend (~0.20 R²) and strongly with codebase cleanliness (~0.40 R²). 

Stanford Study

## The entropy spiral

Unchecked AI in a messy codebase doesn't just fail to help — it actively makes things worse:

1. AI ships more PRs.
2. Code quality drops because the agent is pattern-matching against existing mess.
3. Rework and refactor time climbs to compensate.
4. Engineers start rejecting AI output.
5. Trust collapses. AI gets abandoned. The mess remains, now larger.

One real case study: 14% more PRs, 9% drop in code quality, 2.5× rework. Net effective output: roughly zero. The team thought they were winning because PR counts went up.

## The five mechanisms that make cleanliness pay off

Why does cleanliness matter twice as much as token spend? Five reinforcing reasons:

- **Tests are a trust budget.** Their real job isn't catching bugs — it's letting you stop reading every diff. Without tests, the cost of trusting the agent is "re-read everything." With tests, it's "run the suite." That cost gap is the productivity gain.
- **Types are pre-computed inferences.** A typed signature tells the agent the contract before it writes a line. Untyped code forces the agent to guess the contract from usage — and guessing scales badly.
- **Modularity is blast-radius control.** A 200-line module that does one thing caps the worst case at "this module is wrong." A 2,000-line god-class caps it at "the whole system is wrong and the symptoms appear elsewhere."
- **Documentation is compressed context.** Every CLAUDE.md, AGENTS.md, glossary, or invariant-explaining comment is a pre-computed inference. It turns the agent from a detective into a builder.
- **Consistency reduces hallucination surface.** Agents imitate what they see. A uniform codebase produces uniform output; a contradictory one teaches the agent that contradictions are normal.

## What "clean" actually means for an agent

Not "pretty." Not "DRY." Specifically:

- **Test coverage** — behavioural tests against stable contracts, not implementation details.
- **Type coverage** — agents can't reason about untyped surface area.
- **Documentation** — CLAUDE.md hierarchies, glossaries, AGENTS.md (Day 2, Day 5).
- **Modularity** — deep modules, small interfaces (Day 5: [[Designing Codebases AI Loves]]).
- **Predictable shape** — folders an agent can guess at, names that read like sentences.

Cleanliness is **structural, not aesthetic**. Pretty diffs and consistent formatting are downstream of the five items above; structural cleanliness is what the agent actually reads.

## Vanity metrics and the death valley

Two failure modes to watch for as you measure your own gains:

- **PR counts are a vanity metric.** You can always make the number go up by making the underlying thing worse. Honest metrics are rework rate, refactor share, and net effective output.
- **There's a death valley around 10M tokens per engineer per month.** Past a threshold, more AI usage means the codebase is *resisting* the agent — loops, retries, second-guessing. High token spend is a smell, not a flex.

The two-business-units case is the clincher: same licences, same tools, same spend, radically different outcomes. The variable was never the tool. It was the codebase and the culture around it.

## The new shape of the work

With AI, the red and green phases of TDD collapse to minutes. The **refactor phase becomes the dominant block of human time** — the inverse of how TDD used to feel. The high-leverage activity is no longer writing code. It's keeping the codebase legible to the agent. Senior engineers who lean into this become several times more productive. Ones who insist on hand-writing everything become indistinguishable from juniors with autocomplete.

## How the rest of the workshop fights entropy

- **Day 2 — Alignment.** Give the agent the right context up front so it stops pattern-matching against the wrong examples.
- **Day 5 — Context Architecture.** Make the repo physically and documentationally legible.
- **Day 6 — Skills.** Encode hygiene as repeatable skills (`/simplify`, `/improve-codebase`).
- **Day 7 — Verification.** Catch entropy at the door with reviewers, TDD, and adversarial agents.

Without this Day 1 frame, those days look like a checklist. With it, they're one coherent strategy: amplify the upward loop, starve the downward one.

## The closer

Your AI ROI is not a function of how much AI you use. It's a function of how hard you push back on entropy compared to how hard the agent is pushing it forward. Win that fight and the flywheel spins up. Lose it and your "productivity gain" is measurably negative.

## The handoff

The rest of Day 1 ([[Context is Everything]], [[Subagents]], [[Understanding a Repo]], [[The Core Loop]]) shows you how an agent actually reads and works in a repo. Keep this entropy frame in mind while you watch — every technique on later days is either "make the codebase amplify the agent" or "stop the agent from amplifying the codebase's mess."
