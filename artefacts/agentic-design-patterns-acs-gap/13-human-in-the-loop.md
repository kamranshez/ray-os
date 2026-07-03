---
title: "Ch 13: Human-in-the-Loop -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "13"
pattern: "Human-in-the-Loop"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 13: Human-in-the-Loop** - Antonio Gulli

> One buildable complement: give an unattended Loopy AI loop an "escalate-to-human" checkpoint so it pauses and pages you on high-stakes or ambiguous decisions instead of auto-merging. The permission-gate and clarifying-question halves of HITL are already covered.

## The one idea worth a video

- **An agent should carry an explicit escalate-to-human tool plus a policy for WHEN to use it, so autonomous work stops at the boundary of its own competence.** This is the spine because every other HITL flavour (oversight, intervention, decision augmentation) collapses into "the agent knows when to hand off"; it subsumes the escalation-policy, caveats-of-scale, and human-on-the-loop material. VERDICT: 🔗 next-step video available (complements Loopy AI's task lifecycle).
- **Human-on-the-loop: a human writes the policy once up front and the AI executes autonomously within those bounds** (the trading-rule / call-routing examples). This is the "define allow/ask/deny once, let it run" pattern. VERDICT: ✅ already covered (Auto Permission Mode + /fewer-permission-prompts), kept for context.

## Summary + counts

HITL interleaves human judgment with AI efficiency via oversight, intervention, feedback, decision augmentation, and escalation policies, trading scalability for accuracy in high-stakes domains.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - The escalate-to-human checkpoint
THE CLAIM: an agent operating unattended needs an explicit escalation path and a written policy for when to invoke it, so it hands off at the edge of its competence rather than plowing through. WHY IT'S NON-OBVIOUS: the default framing of autonomy is "remove the human"; Gulli argues the durable design keeps a human reachable but rare - "Escalation Policies are established protocols that dictate when and how an agent should escalate tasks to human operators, preventing errors in situations beyond the agent's capability." WHY IT'S TRUE / MECHANISM: (1) LLM confidence and correctness diverge on ambiguous or high-stakes inputs, so a fixed autonomy threshold silently ships bad decisions; (2) an escalation TOOL (the chapter's `escalate_to_human`) plus policy converts that silent failure into an observable pause, and (3) each escalation becomes labelled training data that "informs future agent improvements." WHAT IT GENERALIZES TO: an unattended coding loop (Loopy AI) that auto-merges PRs. The coding move is a checkpoint stage: the loop self-classifies a change as high-stakes (touches auth, migrations, prod config) or ambiguous, then pauses and pings a human instead of merging - "only a skilled developer can accurately identify subtle errors." HOW IT GOES WRONG: escalate on everything and you destroy the scalability that justified the loop ("operators cannot manage millions of tasks"); escalate on nothing and the loop confidently ships the one change that mattered.

### Spine 2 - Human-on-the-loop policy (covered, for context)
THE CLAIM: instead of approving each action, a human writes the overarching policy once and the AI executes within it - "human experts define the overarching policy, and the AI then handles immediate actions to ensure compliance." WHY IT'S NON-OBVIOUS: it inverts per-action approval into per-policy approval, which is what makes unattended operation safe at volume. MECHANISM: (1) the human encodes bounds (Gulli's "do not invest more than 5% in any single company"; the call-center "route any 'service outage' to a specialist"); (2) the agent acts instantly inside those bounds without waking the human. GENERALIZES TO coding directly: Claude Code's allow/ask/deny rules and Auto Mode ARE human-on-the-loop - you write the policy once, the classifier executes it. This is why the spine is covered: ACS already teaches the policy-authoring move under permissions. HOW IT GOES WRONG: a too-loose policy is indistinguishable from `--dangerously-skip-permissions`; a too-tight one degrades back into per-action prompting.

## 🎬 Proposed ACS videos

### 1. Build a Human Escalation Checkpoint Into Your Loop
- **HOOK:** Your unattended loop auto-merges everything - including the one PR that touches auth and should have woken you up.
- **THE PROMISE:** For anyone running a Loopy AI loop, add a self-escalation stage so the loop pauses and pings you only on high-stakes or ambiguous work, and runs silently on everything else.
- **THE SHAPE:** (1) Take an existing auto-merge PR-backlog loop; (2) add an escalate-to-human step that classifies each change as routine vs high-stakes (auth, DB migration, prod config, low-confidence review); (3) on escalation, post to Slack / send a notification with the diff and the loop's reasoning, and hold the merge; (4) on routine, proceed as before; (5) log every escalation so the policy gets tuned over runs.
- **SPINE:** Spine 1 (escalate-to-human checkpoint).
- **SLOT:** Loopy AI -> L3: Task Lifecycle (new video, sits after "Testing the Loop" / "Improving the Loop").
- **RELATIONSHIP:** 🔗 complements "Going Through a PR Backlog" by being its next step - that video selects the next PR, runs consult reviews, fixes findings, and AUTO-MERGES; this adds the missing human-approval gate so the loop knows which merges to withhold and escalate rather than merging all of them. Do not re-teach PR selection or the review-fix cycle; teach only the classify-and-escalate stage.
- **PROOF TO REUSE:** the `escalate_to_human` tool from the chapter's ADK example; "Escalation Policies are established protocols that dictate when and how an agent should escalate"; the caveat "only a skilled developer can accurately identify subtle errors and provide the correct guidance to fix them."

## 📚 Full wisdom (reference)

### SUMMARY
Gulli's HITL chapter interleaves human judgment with AI efficiency through oversight, intervention, feedback, decision augmentation, and escalation policies, trading scalability for accuracy in high-stakes domains.

### IDEAS
- HITL weaves human judgment and creativity into AI's computational efficiency deliberately.
- Full autonomy is imprudent in complex, ambiguous, or high-risk decision domains.
- HITL positions AI as augmentation of human capability, not replacement.
- Humans act as validators, real-time correctors, or co-solving partners with agents.
- Six aspects: oversight, intervention, feedback-learning, decision augmentation, collaboration, escalation.
- Escalation policies dictate when and how an agent hands off to humans.
- Decision augmentation gives humans AI analysis while humans keep final authority.
- Human-on-the-loop: humans set policy, AI executes immediate compliant actions.
- Trading system example: human sets portfolio rules, AI executes trades instantly.
- Call center example: manager sets routing policy, AI routes calls autonomously.
- HITL's chief caveat is a fundamental lack of scalability.
- Human oversight buys accuracy but cannot cover millions of tasks.
- Hybrid approach: automation for scale, HITL for accuracy at the margin.
- Effectiveness depends heavily on the expertise of human operators.
- Only skilled developers can spot subtle AI-generated code errors.
- Human annotators may need training to correct AI into high-quality data.
- HITL raises privacy concerns; sensitive data must be anonymized before human review.
- Escalation tool converts silent bad decisions into observable pauses.
- RLHF is the prominent methodology where human preferences shape agent learning.
- HITL feedback loops enable continuous, ongoing model improvement.

### INSIGHTS
- Autonomy is a spectrum; the design question is where the handoff boundary sits.
- An escalation TOOL plus policy is what makes "knowing when to stop" executable.
- Every escalation is also a labelled training example for future improvement.
- Human-on-the-loop shifts approval from per-action to per-policy, enabling safe scale.
- The scalability-accuracy trade-off forces a hybrid, not a purist, architecture.
- HITL is only as good as the domain expert operating it.
- Anonymization is an under-discussed operational tax on any HITL deployment.
- Confidence and correctness diverge exactly where escalation matters most.

### QUOTES
- "Rather than viewing AI as a replacement for human workers, HITL positions AI as a tool that augments and enhances human capabilities." - Gulli
- "Escalation Policies are established protocols that dictate when and how an agent should escalate tasks to human operators, preventing errors in situations beyond the agent's capability." - Gulli
- "While human oversight provides high accuracy, operators cannot manage millions of tasks, creating a fundamental trade-off." - Gulli
- "While an AI can generate software code, only a skilled developer can accurately identify subtle errors and provide the correct guidance to fix them." - Gulli
- "Human experts define the overarching policy, and the AI then handles immediate actions to ensure compliance." - Gulli
- "The escalation tool is a core part of the HITL design, ensuring complex or sensitive cases are passed to human specialists." - Gulli

### HABITS / PRACTICES
- Equip agents with an explicit escalate-to-human tool, not just instructions.
- Write escalation policies that name when and how a handoff triggers.
- Monitor agent output via log reviews or real-time dashboards.
- Collect human corrections as feedback data to refine the model.
- Anonymize sensitive data before exposing it to human operators.
- Combine automation for scale with HITL only at high-stakes margins.

### FACTS
- RLHF lets human preferences directly influence an agent's learning trajectory.
- Large corporate loan approval requires a human officer to judge leadership character.
- Legal sentencing demands a human judge retain final authority.
- The ADK code example uses the model "gemini-2.0-flash-exp".
- LangChain also provides tools to implement HITL interactions, per the chapter.
- Data labeling is continuous because models keep evolving.

### REFERENCES
- Google ADK (Agent, ToolContext, CallbackContext, LlmRequest, google.genai).
- LangChain (named as also supporting HITL interactions).
- RLHF (reinforcement learning with human feedback).
- Wu, Xiao, Sun, Zhang, Ma, He - "A Survey of Human-in-the-loop for Machine Learning," arXiv:2108.00941.

### ONE-SENTENCE TAKEAWAY
Give autonomous agents an explicit escalation path so they hand off at the edge of competence.

### RECOMMENDATIONS
- Add an escalate-to-human tool to any agent operating in a high-stakes domain.
- Define escalation policies by decision type, not by ad-hoc feel.
- Turn each escalation into logged training data for the next model version.
- Author policy once (human-on-the-loop) instead of approving every single action.
- Anonymize sensitive fields before any human review step.
- Reserve HITL for the ambiguous margin; automate the routine bulk.
