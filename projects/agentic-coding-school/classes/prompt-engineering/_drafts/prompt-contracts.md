---
class: "prompt-engineering"
status: "scripted"
aliases: [prompt-contracts]
---

# Prompt Contracts

## What This Video Covers

A prompting pattern where before implementing any non-trivial task, the agent generates a structured 4-section contract: Goal, Constraints, Format, and Failure conditions. The user reviews and approves the contract before any building begins. Think of it as a freelance scope of work — but between you and your AI agent.

## Why This Matters

Vague tasks are the #1 cause of poor agent output. "Build me a Netflix" or "make me a million dollars" fails because there's no definition of done, no constraints, no failure conditions. The agent has infinite room to interpret — and it will interpret differently than you imagined.

Prompt contracts force BOTH the user and the agent to agree on exactly what "done" looks like before any work starts. This dramatically improves one-shot success rate and reduces the back-and-forth correction cycle.

## The 4 Sections

1. **Goal** — What does "done" look like? Specific deliverables, measurable outcomes.
   - Example: "A single-page marketing site with hero, services, testimonials, and CTA sections"

2. **Constraints** — Technical and scope limits.
   - Example: "Under 500 lines of HTML. No external dependencies. Must load in under 2 seconds."

3. **Format** — How the output should be structured.
   - Example: "Single index.html file. Smooth scroll animations. Fade-in on scroll. Hover states on buttons."

4. **Failure** — What would make the output WRONG. Explicit rejection criteria.
   - Example: "Failure if it looks like a generic Bootstrap template. Failure if broken on mobile. Failure if animations are janky."

## How the Competitor Teaches It

- Builds a skill called "prompt-contract" that auto-generates the 4 sections
- Demos on "build me a beautiful site for leftclick.ai" (deliberately vague prompt)
- The skill forces Claude to analyze the request, identify implicit assumptions, and draft a contract
- Claude even goes to the existing leftclick.ai website for context before writing the contract
- User reviews and approves or modifies the contract
- Then chains it with reverse prompting (agent asks 5 clarifying questions BEFORE the contract)
- Shows the quality difference: with contract = much closer to what user wanted on first try

## Key Concepts to Cover

- The 4 sections: Goal, Constraints, Format, Failure
- Why vague prompts fail (no definition of done, infinite interpretation space)
- Analogy to freelance scopes of work (same concept, applied to AI)
- Building it as a skill that triggers automatically before non-trivial tasks
- How the agent drafts the contract (it analyzes the request, identifies implicit assumptions)
- User approval step — review and modify before building
- Chaining with reverse prompting for even better results:
  1. Agent asks 5 clarifying questions (reverse prompting)
  2. User answers
  3. Agent generates contract from answers
  4. User approves
  5. Agent builds
- Demo on a real build task showing the quality improvement

## Demo Plan

1. Give a deliberately vague prompt: "build me a beautiful site for [business]"
2. Show what happens WITHOUT a contract (mediocre, wrong assumptions)
3. Run the same prompt WITH the prompt-contract skill
4. Walk through the generated contract — show how it surfaces hidden assumptions
5. Approve and build — show the much better result
6. Chain with reverse prompting for maximum quality

## Suggested Class Placement

Techniques — Fundamental Techniques
