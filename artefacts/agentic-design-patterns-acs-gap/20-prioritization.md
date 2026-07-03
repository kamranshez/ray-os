---
title: "Ch 20: Prioritization -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "20"
pattern: "Prioritization"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 20: Prioritization** - Antonio Gulli

> The dynamic re-prioritization loop is already nailed by "Don't Pre-Sequence the Backlog" and "Going Through a PR Backlog". The one net-new angle: encode an explicit prioritization rubric (criteria + weights) as a skill so "most important" reflects YOUR business rules, not the model's default hunch.

## The one idea worth a video

- **Prioritization is a loop, not a plan: reassess and re-rank at every step instead of pre-sequencing the whole queue.** This is the load-bearing idea of the chapter (dynamic re-prioritization) and it subsumes criteria definition, action selection, and adaptability. VERDICT: ✅ already covered (kept for context).
- **The agent's "most important" judgment is only as good as the criteria you hand it -> encode a weighted prioritization rubric as a reusable skill.** Distinct video: the demo is building the ranking function, not the loop that consumes it. VERDICT: 🔗 next-step video available.

## Summary + counts

Prioritization lets agents rank tasks by urgency, importance, dependencies, and cost, selecting the most critical next action and re-prioritizing dynamically as conditions change.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Prioritization is a loop, not a plan
THE CLAIM: an effective agent does not pre-order its whole queue; it repeatedly asks "what is the single most important next thing?" and re-ranks as reality shifts. WHY IT'S NON-OBVIOUS: the intuitive move with a backlog is to sort it once, top to bottom, then execute in order - which feels organized but is secretly waterfall. WHY IT'S TRUE / MECHANISM: (1) every completed item changes the state of the world - a merged PR closes three dependent issues, a new outage outranks everything queued; (2) a static ordering computed at t=0 is stale by t=1, so re-evaluating each cycle strictly dominates. Gulli calls this "dynamic re-prioritization... ensuring agent adaptability and responsiveness" and notes prioritization happens at goal, sub-task, and action-selection levels. WHAT IT GENERALIZES TO: an autonomous coding loop chewing an issue or PR backlog - pick the next most important item in a fresh subagent, do it, re-assess. HOW IT GOES WRONG: re-ranking every cycle with no stable criteria produces thrash (the agent oscillates), and without dependency awareness it starts work that is blocked. This is squarely ACS Loopy-AI territory and is already taught.

### Spine 2 - Encode the prioritization rubric as a skill
THE CLAIM: "most important" is not self-evident; the agent needs explicit criteria - urgency, importance, dependencies, resource cost, cost/benefit - to rank reliably, and those criteria should be a reusable, version-controlled rubric rather than an ad-hoc phrase in a prompt. WHY IT'S NON-OBVIOUS: once you learn "just ask for the next most important item," it is tempting to let the model's default judgment decide - but the model's default weights are not your business's weights. WHY IT'S TRUE / MECHANISM: (1) the chapter's whole first half is "criteria definition establishes the rules or metrics for task evaluation... urgency, importance, dependencies, resource availability, cost/benefit"; (2) if those weights live nowhere, every run re-derives them differently and the ranking is non-reproducible. Gulli's code makes this concrete: the PM agent maps "urgent/ASAP/critical" to P0 and falls back to P1 defaults - a tiny hard-coded rubric. WHAT IT GENERALIZES TO: a `prioritize.md` skill that scores each backlog item on impact, effort, blast-radius, and dependency-unblock count, then hands the loop a ranked shortlist. HOW IT GOES WRONG: over-engineered numeric scoring invites false precision; too-vague criteria collapse back to vibes.

## 🎬 Proposed ACS videos

### 1. Encode a Prioritization Rubric as a Skill
- **HOOK:** Your loop asks for the "most important" issue every cycle - but whose definition of important is it using? The model's, not yours.
- **THE PROMISE:** For anyone running an autonomous backlog loop, you will leave with a reusable prioritization skill that ranks work by YOUR criteria (impact, effort, blast-radius, dependency-unblock) so every run's ordering is consistent and defensible.
- **THE SHAPE:** (1) Show the failure: run the backlog loop twice, watch it pick different "top" items because "most important" is undefined. (2) Write a `prioritize.md` skill: explicit criteria, a lightweight P0/P1/P2 mapping, and a dependency-unblock tie-breaker. (3) Point the loop at the skill so the next-item subagent scores against the rubric before choosing. (4) Re-run and show a stable, explainable ranking with each item's score reasoning. (5) Show dynamic re-prioritization still works - the rubric re-scores after each merge.
- **SPINE:** Spine 2.
- **SLOT:** Loopy AI -> "L4 & L5: The Climb" (sits right after "Don't Pre-Sequence the Backlog").
- **RELATIONSHIP:** 🔗 complements "Don't Pre-Sequence the Backlog" by being its next step - that video teaches WHY you re-ask for the next most important item each cycle instead of pre-ordering; this adds HOW to define "most important" as a version-controlled rubric so the agent's ranking is reproducible and matches your business rules, not the model's default hunch.
- **PROOF TO REUSE:** Gulli's criteria list - "urgency... importance... dependencies... resource availability... cost/benefit analysis (effort versus expected outcome)"; the code's rubric mapping "urgent/ASAP/critical" to P0 with P1 defaults; the line "criteria definition establishes the rules or metrics for task evaluation."

## 📚 Full wisdom (reference)

**SUMMARY:** Gulli explains the Prioritization pattern: agents rank tasks by urgency, importance, dependencies, and cost, select the most critical next action, and re-prioritize dynamically as conditions change.

**IDEAS:**
- Agents in dynamic environments face many actions, conflicting goals, and limited resources needing ordering.
- Prioritization ranks tasks by significance, urgency, dependencies, and established criteria.
- Criteria definition sets the rules or metrics for evaluating each candidate task.
- Urgency measures a task's time sensitivity; importance measures impact on the primary objective.
- Dependencies flag whether a task is a prerequisite that unblocks others.
- Cost/benefit analysis weighs effort against expected outcome before committing.
- Task evaluation scores each option against criteria, from simple rules to LLM reasoning.
- Scheduling/selection logic picks the optimal next action, often via a queue.
- Dynamic re-prioritization lets the agent shift focus when new critical events arise.
- Prioritization operates at goal, sub-task, and immediate action-selection levels.
- Effective prioritization mirrors human managers weighing input from all team members.
- Autonomous driving prioritizes collision-avoidance braking over lane discipline or fuel efficiency.
- Cybersecurity agents rank alerts by threat severity, impact, and asset criticality.
- A LangChain PM agent creates, prioritizes (P0/P1/P2), and assigns tasks to workers.
- Default assignments (P1, 'Worker A') fill in when priority or assignee is unspecified.
- Interpreting ambiguous requests and sequencing tool calls is what separates agents from scripts.

**INSIGHTS:**
- A static ordering computed once is stale the moment any item completes.
- Re-asking "what matters most now" beats pre-sequencing because state changes each step.
- Priorities need explicit criteria or the ranking is non-reproducible across runs.
- Prioritization is layered: strategic goal choice down to tactical action selection.
- Ambiguity handling (mapping "ASAP" to P0) is itself an act of prioritization.
- Dependency awareness prevents starting blocked work that cannot progress.
- The same pattern serves triage, scheduling, and resource allocation across domains.
- Self-managing its own workflow is the mark of a true agentic system.

**QUOTES:**
- "The prioritization pattern addresses this issue by enabling agents to assess and rank tasks, objectives, or actions based on their significance, urgency, dependencies, and established criteria." - Gulli
- "criteria definition establishes the rules or metrics for task evaluation." - Gulli
- "Dynamic re-prioritization allows the agent to modify priorities as circumstances change... ensuring agent adaptability and responsiveness." - Gulli
- "This ability to self-manage its workflow is what separates a true agentic system from a simple automated script." - Gulli
- "Use the Prioritization pattern when an Agentic system must autonomously manage multiple, often conflicting, tasks or goals under resource constraints." - Gulli

**HABITS/PRACTICES:**
- Define explicit evaluation criteria before letting an agent rank tasks.
- Map fuzzy user language ("urgent", "ASAP") to concrete priority levels.
- Provide sensible defaults (P1, default assignee) for missing information.
- Re-prioritize when a new critical event or deadline emerges.
- Create the task first to get an ID, then attach priority and assignee.

**FACTS:**
- The example uses LangChain with `create_react_agent`, `AgentExecutor`, and `gpt-4o-mini`.
- Priority levels in the demo are P0 (highest), P1 (medium), P2 (lowest).
- Task arguments are validated with Pydantic `BaseModel` field schemas.
- The task manager uses a dictionary for O(1) lookup, update, and deletion.
- `ConversationBufferMemory` maintains contextual continuity across turns.

**REFERENCES:**
- LangChain (`langchain_core`, `langchain.agents`, `ConversationBufferMemory`).
- `langchain_openai.ChatOpenAI`, model `gpt-4o-mini`.
- Pydantic (`BaseModel`, `Field`, `model_copy`).
- IRE Journals paper on AI-driven project scheduling and resource allocation security.
- MDPI Systems paper on AI-driven decision support in agile project management.

**ONE-SENTENCE TAKEAWAY:** Agents act intelligently by ranking tasks against explicit criteria and re-prioritizing dynamically as circumstances change.

**RECOMMENDATIONS:**
- Build a PM-style agent that creates, prioritizes, and assigns tasks via tools.
- Encode urgency/importance/dependency criteria explicitly rather than trusting default judgment.
- Add dynamic re-prioritization so a new critical event preempts the queue.
- Use Pydantic-validated tool arguments to keep priority values well-formed.
- Give the agent defaults so missing priority or assignee never blocks progress.
