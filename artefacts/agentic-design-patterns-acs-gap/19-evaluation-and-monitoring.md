---
title: "Ch 19: Evaluation and Monitoring -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "19"
pattern: "Evaluation and Monitoring"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 19: Evaluation and Monitoring** - Antonio Gulli

> Two net-new videos: an LLM-as-a-Judge rubric harness that scores agent output on subjective quality, and trajectory evaluation that grades the *sequence of tool calls* an agent took, not just its final answer.

## The one idea worth a video

- **You cannot unit-test an agent, so you score its outputs with a rubric-driven LLM judge that returns structured JSON.** This is the spine because it converts "does it feel good?" into a repeatable, versioned number - it subsumes helpfulness, bias, clarity, and correctness scoring. VERDICT: ❌ net-new video available.
- **Evaluate the agent's trajectory - the ordered steps and tool calls - against a ground-truth path, not only the final output.** Distinct demo (capture and diff tool-call sequences with exact/in-order/any-order match) and distinct "one thing after," so it de-merges from the judge idea. VERDICT: ❌ net-new video available.
- **Move from underspecified prompts to formal "contracts" with verifiable deliverables the agent can negotiate and self-validate against.** Adjacent to spec-driven planning; kept as a complement/also-film-able rather than a third deep dive. VERDICT: 🔗 next-step video available.

## Summary + counts

Agents are probabilistic, so traditional pass/fail tests fail; evaluate outputs, latency, tokens, and trajectories continuously using LLM-as-a-Judge rubrics and formal contracts.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - LLM-as-a-Judge rubric harness
THE CLAIM: subjective output quality ("helpfulness", neutrality, clarity) can be scored consistently by handing another LLM an explicit rubric and demanding a structured JSON verdict. WHY IT'S NON-OBVIOUS: the instinct is `assert output == expected`, and the chapter's own `evaluate_response_accuracy` demo shows why that is a trap - "The capital of France is Paris." vs "Paris is the capital of France." scores 0.0 despite identical meaning. Exact-match, Levenshtein, and keyword checks all miss semantics. WHY IT'S TRUE / MECHANISM: (1) a frozen rubric with per-criterion 1-5 anchors (Clarity, Neutrality, Relevance, Completeness, Audience) turns a vibe into a rank-ordered scale; (2) forcing `response_mime_type="application/json"` plus low temperature (0.2) makes the judge deterministic and machine-parseable, so scores can be logged, diffed across versions, and gated in CI. The chapter's `LLMJudgeForLegalSurvey` correctly splits a biased "Don't you agree that..." question from a neutral one. WHAT IT GENERALIZES TO: in agentic *coding*, the judged artifact is a diff, a PR description, or a skill's output - you build a rubric (correctness, security, readability) and a Claude/Codex judge that scores every agent run. HOW IT GOES WRONG: the judge inherits the base model's blind spots ("Limited by LLM capabilities") and can miss intermediate reasoning steps, so a plausible-but-wrong answer scores high.

### Spine 2 - Trajectory evaluation
THE CLAIM: for agents, grading the final answer is not enough - you must grade the *trajectory*, the ordered sequence of tool selections and steps taken to get there. WHY IT'S NON-OBVIOUS: "Standard code yields predictable pass/fail results, whereas agents operate probabilistically"; two agents can produce the same output while one wastes ten tool calls or picks the wrong database. Output-only scoring is blind to that. WHY IT'S TRUE / MECHANISM: (1) the chapter defines a ground-truth trajectory (intent -> DB search -> review -> report) and a family of comparison metrics - exact match, in-order match, any-order match, precision, recall, single-tool-use - so you can pick strictness per stakes; (2) capturing the actual tool sequence exposes cost and reliability failures (endless "perfect rental car" loops, wrong-agent selection) that a correct final string hides. WHAT IT GENERALIZES TO: agentic coding is nothing but tool-call trajectories - Claude Code's Read/Grep/Edit/Bash sequence *is* the trajectory. You dump the JSONL of a run, define the ideal path for a task, and score in-order match to catch when the agent skips exploration or over-edits. HOW IT GOES WRONG: over-tight exact-match penalizes valid alternate paths; the "ideal" trajectory can be stale as the environment shifts, so the metric must adapt over time.

## 🎬 Proposed ACS videos

### 1. Grading Your Agent with an LLM Judge
- **HOOK:** Your evals do `output == expected` and mark a correct answer wrong because the words are in a different order.
- **THE PROMISE:** For anyone who wants a repeatable quality number on agent output, build a rubric-driven LLM judge that scores every run and returns JSON you can gate on.
- **THE SHAPE:** (1) show the exact-match trap live (Paris example scoring 0.0); (2) write a frozen rubric with per-criterion 1-5 anchors; (3) wire a Claude/Codex judge at temperature 0.2 forced to emit JSON; (4) score a good vs a biased/vague output; (5) log scores and diff two prompt versions.
- **SPINE:** Spine 1.
- **SLOT:** Advanced Techniques -> new chapter "Evaluating Agents" (or Prompt Engineering).
- **RELATIONSHIP:** ❌ net-new. Closest is "Evaluating Code Review Tools", which uses an LLM to judge *which external PR tool* earns its cost against a backlog - a one-off tool bake-off, not a reusable rubric-scored judge you run on your own agent's output every time. Do not re-teach the tool-comparison framing.
- **PROOF TO REUSE:** the `evaluate_response_accuracy` false-0.0 example; the five-criterion `LEGAL_SURVEY_RUBRIC`; the biased "Don't you agree that overly restrictive... laws" question; the strengths/weaknesses table ("Consistent, efficient, scalable" vs "Intermediate steps may be overlooked").

### 2. Scoring the Agent's Trajectory, Not Just Its Answer
- **HOOK:** Two agents give the same final answer - one used 3 tool calls, the other 30. Your eval says they're identical.
- **THE PROMISE:** For developers running agents beyond prototype, learn to capture the tool-call sequence and score it against an ideal path so you catch wasted steps and wrong-tool picks.
- **THE SHAPE:** (1) run a Claude Code task and dump its Read/Grep/Edit/Bash trajectory; (2) hand-write the ground-truth path for that task; (3) score exact vs in-order vs any-order match; (4) show precision/recall catching a skipped-exploration or over-edit run; (5) discuss when high-stakes work demands exact match.
- **SPINE:** Spine 2.
- **SLOT:** Advanced Techniques -> "Evaluating Agents" (pairs with video 1).
- **RELATIONSHIP:** ❌ net-new. "Agent Introspection" and "Understanding Agent Output" inspect *why* an agent went wrong after the fact; neither defines a ground-truth trajectory or scores the tool sequence with match metrics.
- **PROOF TO REUSE:** the customer-query ideal path (intent -> DB search -> review -> report); the six comparison metrics (exact, in-order, any-order, precision, recall, single-tool-use); "traditional software tests are insufficient... agents operate probabilistically"; the multi-agent handoff failure (flight dates lost to the hotel agent).

### Also film-able (not deep-dived)
- **The AI "Contract" instead of a prompt** (🔗 complements spec-driven planning): turn "analyze last quarter's sales" into a formal contract naming deliverables, data sources, cost budget, and acceptance tests the agent negotiates and self-validates against. The four pillars (formalized contract, negotiation lifecycle, quality-focused iterative execution, hierarchical subcontracts) map cleanly onto writing a rigorous spec file for Claude Code.
- **Evals in CI: test files vs evalsets** (🔗 complement): the ADK split between single-session test files (unit tests) and multi-session evalsets (integration tests), run via `adk eval` / pytest, translated to running your judge + trajectory suite on every build.

## 📚 Full wisdom (reference)

### SUMMARY
Gulli argues agents are probabilistic, so traditional pass/fail tests fail; evaluate outputs, latency, tokens, and trajectories continuously via LLM-as-a-Judge rubrics, evalsets, and formal contracts.

### IDEAS
- Traditional pass/fail software tests are insufficient for probabilistic, non-deterministic agents in dynamic environments.
- Evaluation is continuous and often external: effectiveness, efficiency, and compliance measured after deployment.
- Exact-match accuracy scoring falsely fails semantically identical answers phrased differently.
- Better response metrics: Levenshtein, Jaccard, keyword analysis, embedding cosine similarity, LLM-as-a-Judge, RAG faithfulness.
- Latency monitoring matters for interactive agents; log it to persistent time-series or observability stores.
- Token usage tracking (input plus output) directly controls LLM operating cost and flags prompt inefficiency.
- LLM-as-a-Judge scores subjective qualities like helpfulness using a predefined rubric and structured output.
- A good judge uses low temperature and forced JSON output for deterministic, parseable verdicts.
- Trajectory evaluation grades the ordered sequence of steps and tool calls, not just final output.
- Compare actual trajectory to ground truth via exact, in-order, any-order, precision, recall, single-tool matches.
- Test files (JSON) are single-session unit tests; evalsets are multi-session integration tests.
- Multi-agent evaluation checks cooperation, plan adherence, correct agent selection, and scalability of adding agents.
- Concept/data drift degrades agent performance after deployment and must be monitored over time.
- Anomaly detection flags unusual agent actions signaling errors, attacks, or emergent undesired behavior.
- The "contractor" model replaces underspecified prompts with formal, verifiable contracts.
- Contracts define deliverables, data sources, scope, cost, and time - making outcomes objectively verifiable.
- Contractor pillars: formalized contract, negotiation lifecycle, iterative self-validation, hierarchical subcontracts.
- Google ADK supports evaluation via web UI, pytest integration, and `adk eval` CLI.

### INSIGHTS
- Determinism is the real deliverable of evaluation: turn "feels right" into a versioned, diffable number.
- The final answer can be right while the path is wasteful, wrong-tooled, or unsafe - measure both.
- An LLM judge is only as trustworthy as the base model; it inherits blind spots and skips intermediate reasoning.
- Metric strictness should scale with stakes: exact-match for high-stakes, any-order for flexible tasks.
- Evaluation methods themselves must adapt because agents and their environments are constantly in flux.
- Reliability at scale comes from specification and negotiation, not from bigger models alone.
- Monitoring cost (tokens) and speed (latency) is evaluation too, not just correctness.

### QUOTES
- "Standard code yields predictable pass/fail results, whereas agents operate probabilistically, necessitating qualitative assessment of both the final output and the agent's trajectory." (Gulli)
- "A straightforward comparison falls short in assessing semantic similarity, only succeeding if an agent's response exactly matches the expected output." (Gulli)
- "This LLM-as-a-Judge approach assesses another AI agent's output based on predefined criteria for 'helpfulness.'" (Gulli)
- "Today's common AI agents operate on brief, underspecified instructions, which makes them suitable for simple demonstrations but brittle in production, where ambiguity leads to failure." (Gulli)
- "This internal loop of generating, reviewing, and improving its own work until the contract's specifications are met is crucial for building trust in its outputs." (Gulli)
- "Evaluating multi-agent systems is challenging because they are constantly in flux." (Gulli)

### HABITS / PRACTICES
- Log latency to persistent storage (JSON logs, InfluxDB, Prometheus, BigQuery, Datadog) - never just print it.
- Track cumulative input and output tokens per interaction for cost management.
- Set the judge LLM temperature low and require JSON output for deterministic scoring.
- Define a ground-truth trajectory per task and pick a match metric by stakes.
- Use test files for rapid unit-test iteration and evalsets for complex multi-turn integration tests.
- Run evals via CLI (`adk eval`) in regular build/verification pipelines.

### FACTS
- The chapter's exact-match function returns 0.0 for two semantically identical France/Paris sentences.
- Recommended judge model example is `gemini-1.5-flash-latest` at temperature 0.2.
- ADK offers three evaluation entry points: web UI (`adk web`), pytest, and `adk eval` CLI.
- Comparison metrics enumerated: exact match, in-order match, any-order match, precision, recall, single-tool-use.
- Rubric criteria in the legal-survey judge: Clarity, Neutrality, Relevance, Completeness, Audience Appropriateness.

### REFERENCES
- Google ADK (adk web, adk eval, AgentEvaluator), ADK Web repo, ADK Evaluate docs.
- google.generativeai library; Gemini 1.5 Flash / Pro models.
- Observability/storage: InfluxDB, Prometheus, Snowflake, BigQuery, PostgreSQL, Datadog, Splunk, Grafana Cloud.
- Survey on Evaluation of LLM-based Agents (arXiv:2503.16416).
- Agent-as-a-Judge: Evaluate Agents with Agents (arXiv:2410.10934).
- Agent Companion, Gulli et al. (Kaggle whitepaper).

### ONE-SENTENCE TAKEAWAY
Score agent outputs and trajectories continuously with rubric-driven LLM judges, because probabilistic agents defeat traditional pass/fail tests.

### RECOMMENDATIONS
- Replace exact-match accuracy with embedding similarity or an LLM judge for semantic correctness.
- Build a frozen rubric and a low-temperature JSON judge; version it alongside your prompts.
- Capture and diff tool-call trajectories against an ideal path to catch wasted or wrong steps.
- Persist latency and token metrics to a time-series store and alert on drift.
- Split evals into fast unit test files and richer multi-turn evalsets, run in CI.
- For high-stakes tasks, write a formal contract with deliverables and acceptance tests instead of a loose prompt.
