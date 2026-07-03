---
title: "Ch 11: Goal Setting and Monitoring -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "11"
pattern: "Goal Setting and Monitoring"
status: covered
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 11: Goal Setting and Monitoring** - Antonio Gulli

> Already covered. The chapter's whole payload (define measurable goals, loop generate->judge->refine with a stop criterion, and never let an agent grade its own work) is the exact spine of the Loopy AI "Builder Verifier Pattern" and "Writing Effective Goals" videos, plus Codex "/goal". No net-new or complement video here.

## The one idea worth a video

- **An agent needs an explicit, measurable goal plus a monitoring loop that judges progress and stops when the goal is met (or a cap is hit).** This subsumes SMART criteria, the True/False verdict, the refine cycle, and the runaway-loop caveat. VERDICT: ✅ already covered (kept for context).
- **Do not let the same model both write the work and judge it; separate the reviewer into its own role for objective evaluation.** Distinct enough to be its own video (separate DEMO: a second agent as judge), but ACS already ships it. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Agents need explicit measurable goals and a monitoring feedback loop that self-evaluates, refines, and stops on success or an iteration cap; separate the judge from the generator.

🔴 0 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 2 covered

## 🔬 Deep dive

### Spine 1 - Goal + monitoring loop with a stop criterion
THE CLAIM: an effective agent needs a specific, measurable objective and a monitoring mechanism that continuously checks progress against it, then adapts, revises, or stops. WHY IT'S NON-OBVIOUS: the naive default is "generate once and ship"; Gulli argues the value is the loop -- "it doesn't just generate code once, but enters into an iterative cycle of creation, self-evaluation, and improvement." WHY IT'S TRUE / MECHANISM: (1) a measurable success criterion turns a fuzzy request into a testable predicate, so the agent can ask an LLM to answer "just True or False which makes it easier to stop the iterations"; (2) the True/False verdict feeds a refine step that "uses the insights from its self-critique to pinpoint the weaknesses and intelligently rewrite," closing a feedback loop that converges. WHAT IT GENERALIZES TO: in agentic coding this is exactly a long-running loop with acceptance criteria -- give Claude Code or Codex a goal plus explicit "done" tests, let it iterate against them, and cap the attempts. HOW IT GOES WRONG: Gulli's own caveat -- the model "may hallucinate," may "incorrectly assess its performance as successful," and the "monitoring... creates a potential risk of the process running forever," which is why a max-iteration cap and a real (non-LLM) test matter.

### Spine 2 - Separate the judge from the generator
THE CLAIM: when "the same LLM is responsible for both writing the code and judging its quality, it may have a harder time discovering it is going in the wrong direction," so a more robust design gives review to a distinct agent. WHY IT'S NON-OBVIOUS: self-grading feels efficient and cheap; the chapter argues it is structurally biased. WHY IT'S TRUE / MECHANISM: (1) the generator is anchored on its own reasoning, so its self-review inherits the same blind spots; (2) a separate Code Reviewer agent "acting as a separate entity from the programmer agent... significantly improves objective evaluation," and the structure "naturally leads to better practices" because a dedicated Test Writer fills a need the coder would skip. WHAT IT GENERALIZES TO: builder/verifier splits in coding loops -- one agent implements, an independent read-only agent (or a different model) verifies against user flows, and findings feed back. HOW IT GOES WRONG: a verifier that rigidly grades against a stale plan, or a reviewer with the same context/bias as the builder, recreates the problem it was meant to solve.

## 🎬 Proposed ACS videos

No pitches -- both spines are ✅ covered. Reference existing videos instead:

- Spine 1 is covered by **"Writing Effective Goals"** (Loopy AI -> The Toolbox: vague goals, unreachable finish lines, unfalsifiable verification, baselines, constraints), **"Builder Verifier Pattern"** (Loopy AI -> L2: stop criteria, feedback to builder), and **"/goal"** (Master Codex -> Codex App: defining objectives and acceptance criteria, update_goal completion, automatic continuation).
- Spine 2 is covered by **"Builder Verifier Pattern"** (Loopy AI -> L2), whose agentContext explicitly names "avoiding self-grading, feeding verifier findings back to builders, adversarial review rounds," plus **"Don't Verify Against the Plan"** and **"Verifiers Go Stale"** for the failure modes.

## 📚 Full wisdom (reference)

### SUMMARY
Gulli explains the Goal Setting and Monitoring pattern: give agents specific measurable objectives and a feedback loop that tracks progress, self-evaluates, refines, and stops on success.

### IDEAS
- Effective agents need direction (a goal) and a way to know they are succeeding.
- Planning turns a high-level objective into autonomously generated intermediate sub-goals.
- Planning underpins tool use, routing, and multi-agent collaboration as a foundational pattern.
- A goal converts a reactive system into one proactively working toward an objective.
- Monitoring observes agent actions, environmental states, and tool outputs against the goal.
- Feedback loops let agents adapt, revise the plan, or escalate when off course.
- Goals should be SMART: specific, measurable, achievable, relevant, time-bound.
- The code example loops generate -> self-critique -> refine instead of generating once.
- An LLM judge answering only True or False gives a clean stopping condition.
- A max-iteration cap prevents the monitoring loop from running forever.
- Success measured by the agent's own AI judgment is fragile and can be wrong.
- Same model writing and judging struggles to detect it is going wrong.
- Separating roles into a crew improves objective evaluation of the work.
- A dedicated Code Reviewer agent significantly improves evaluation objectivity.
- Role separation naturally produces better practices, e.g. a Test Writer writing tests.
- Monitoring spans customer support, trading, robotics, moderation, learning, project management.
- In Google's ADK goals live in agent instructions; monitoring uses state management and tools.
- LLMs do not produce flawless code by magic; you still must run and test it.

### INSIGHTS
- A measurable success predicate is what makes autonomous stopping possible at all.
- The judge's binary verdict is a design choice to make loop control deterministic.
- Self-evaluation inherits the generator's blind spots; independence is structurally, not just stylistically, better.
- Role separation is a forcing function: a Test Writer exists so tests get written.
- Monitoring without a hard cap is a latent infinite loop, not a safeguard.
- Well-understood goals still fail when the model hallucinates the assessment.
- Goal-in-instructions plus state-as-monitoring is how frameworks operationalize this abstractly.

### QUOTES
- "It doesn't just generate code once, but enters into an iterative cycle of creation, self-evaluation, and improvement." (Gulli)
- "I am asking the LLM to judge this and answer just True or False which makes it easier to stop the iterations." (Gulli)
- "When the same LLM is responsible for both writing the code and judging its quality, it may have a harder time discovering it is going in the wrong direction." (Gulli)
- "The 'monitoring' in the simple example is basic and creates a potential risk of the process running forever." (Gulli)
- "LLMs do not produce flawless code by magic; you still need to run and test the produced code." (Gulli)
- "In this multi-agent system, the Code Reviewer, acting as a separate entity from the programmer agent... significantly improves objective evaluation." (Gulli)
- "Goals should be specific, measurable, achievable, relevant, and time-bound (SMART)." (book)

### HABITS / PRACTICES
- Define a strict quality checklist (goals) before the agent starts work.
- Have the agent self-review against every checklist item before submitting.
- Reduce the pass/fail decision to a single True/False verdict.
- Cap iterations to bound runtime and cost.
- Give review its own agent/role rather than trusting self-grading.
- Always run and test generated code; never trust the model's self-assessment alone.

### FACTS
- The example uses LangChain and OpenAI (gpt-4o, temperature 0.3), max 5 iterations.
- SMART is specific, measurable, achievable, relevant, time-bound.
- Google's ADK conveys goals through agent instructions and monitors via state management.
- The author runs a personal Gemini crew: Peer Programmer, Code Reviewer, Documenter, Test Writer, Prompt Refiner.

### REFERENCES
- LangChain; OpenAI API; GPT-4o; python-dotenv (dependencies).
- Google Agent Development Kit (ADK).
- Gemini (author's multi-agent crew).
- SMART Goals / SMART criteria (Wikipedia).
- Example code MIT-licensed, credited to Mahtab Syed.

### ONE-SENTENCE TAKEAWAY
Give agents measurable goals and a monitoring loop that judges, refines, stops -- and never self-grades.

### RECOMMENDATIONS
- Attach explicit, measurable acceptance criteria to every autonomous coding task.
- Build a generate -> evaluate -> refine loop with a hard iteration cap.
- Use a separate reviewer agent (or different model) to judge, not the builder.
- Add a dedicated test-writer role so tests actually get produced.
- Treat any LLM self-assessment as a hypothesis; confirm with real execution and tests.
- Watch for runaway loops; make the stop criterion falsifiable and time-bound.
