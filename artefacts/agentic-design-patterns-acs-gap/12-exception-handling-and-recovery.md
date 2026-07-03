---
title: "Ch 12: Exception Handling and Recovery -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "12"
pattern: "Exception Handling and Recovery"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 12: Exception Handling and Recovery** - Antonio Gulli

> Two film-able videos: a Loopy-AI reliability ladder (retry -> fallback -> degrade -> escalate) that is the next step after "Designing a Task Lifecycle," plus a net-new "fallback chains for agents" build. Self-correction is already covered.

## The one idea worth a video

- **A production agent must be architected to expect its own tools to fail: detect the error, retry transient ones, fall back, degrade gracefully, and escalate to a human -> never crash or spin.** This is the spine because every other item in the chapter (logging, rollback, notification) is a rung on this same ladder. VERDICT: 🔗 next-step video available (complements Loopy AI lifecycle).
- **Build a layered fallback chain so the agent always returns partial value: primary path fails -> a broader/cheaper fallback path runs -> a final agent presents whatever was salvaged.** Distinct DEMO (the book's actual `SequentialAgent` code) and distinct "one thing you can do after" -> its own spine. VERDICT: ❌ net-new video available.
- **Recovery can be reflective: feed the exception back into the agent so it reattempts with a refined prompt or plan.** VERDICT: ✅ already covered (kept for context).

## Summary + counts

Agents in real environments must detect errors, then handle them via logging, retries, fallbacks, graceful degradation, notification, rollback, self-correction, and escalation to stay reliable.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - The reliability ladder for unattended loops
THE CLAIM: a durable agent is one that assumes its tools and services *will* fail and has a pre-planned response ladder - detect, log, retry, fall back, degrade, notify, roll back, escalate - so it "maintains functionality, minimizes downtime" instead of collapsing. WHY IT'S NON-OBVIOUS: the default when prototyping is the happy path; you only discover the agent is fragile when an overnight run silently dies or burns tokens re-trying an invalid action. Gulli's trading-bot example is exact: on an "insufficient funds" error the bot must log it and *stop* retrying the same invalid trade, not loop. WHY IT'S TRUE / MECHANISM: (1) real services return 404/500, timeouts, and malformed output, so any agent touching them has a non-zero failure rate per step; (2) over a long autonomous run those independent failures compound, so without explicit handling the expected outcome of a multi-step loop is failure. WHAT IT GENERALIZES TO: Ray's Loopy AI world - an unattended Claude Code loop hitting a flaky API, a failing test, or a rate limit needs a designed response (retry transient, escalate persistent) or it either halts or spins. HOW IT GOES WRONG: retrying non-transient errors (the invalid trade) wastes budget; or escalating everything defeats the point of unattended automation. The skill is classifying transient vs terminal.

### Spine 2 - Fallback chains and graceful degradation
THE CLAIM: architect the agent so a failed primary path routes to a broader fallback path and a final stage always presents *some* value - "the agent can maintain partial functionality to provide at least some value." WHY IT'S NON-OBVIOUS: developers reach for try/except that just logs and returns nothing; the book instead makes the fallback a first-class agent in the workflow. WHY IT'S TRUE / MECHANISM: (1) the book's `SequentialAgent` runs `primary_handler` -> `fallback_handler` -> `response_agent` in guaranteed order; (2) the fallback reads a state flag (`state["primary_location_failed"]`) and, only if set, calls a coarser tool (`get_general_area_info` instead of `get_precise_location_info`); (3) the response agent reasons purely over final state and apologizes if empty. So failure is routed, not thrown. WHAT IT GENERALIZES TO: coding agents - precise tool -> broader tool, expensive model -> cheaper model, live API -> cached snapshot. HOW IT GOES WRONG: the fallback silently masks a real outage nobody notices; or the state flag is never set on failure, so the fallback never fires.

### Spine 3 - Reflective self-correction (covered)
THE CLAIM: recovery can be intelligent - "if an initial attempt fails and raises an exception, a reflective process can analyze the failure and reattempt the task with a refined approach, such as an improved prompt." WHY IT'S NON-OBVIOUS: it treats an exception as *training signal* for the next attempt, not just an error to swallow. MECHANISM: (1) capture the failure detail; (2) feed it back so the agent replans rather than repeating the identical action. WHAT IT GENERALIZES TO: exactly Ray's existing debugging-loop material - recording failed fix attempts and forcing a fresh strategy. This is why it is covered: ACS "Bug Fixing Across Chats" and "Avoiding Code Bias Caused Loops" already teach the feed-the-failure-back-in move. HOW IT GOES WRONG: reflecting inside the same poisoned context repeats the mistake - which is precisely what those existing videos warn against.

## 🎬 Proposed ACS videos

### 1. Fallback Chains for Agents (Always Return Something)
- **HOOK:** Your agent's precise tool 404s and the whole run returns nothing - here's how to make it degrade to a good-enough answer instead.
- **THE PROMISE:** For anyone wiring tools into an agent: architect a primary -> fallback -> present path so the agent never hands back a blank failure.
- **THE SHAPE:** (1) Recreate the book's pattern in Claude Code: a primary handler calling a precise tool; (2) a fallback handler that fires only when a state flag says the primary failed, calling a coarser tool; (3) a final agent that presents whatever landed in state, apologizing if empty; (4) force the primary to fail and watch the graceful degradation; (5) generalize to expensive-model -> cheap-model and live-API -> cached-snapshot fallbacks.
- **SPINE:** Spine 2.
- **SLOT:** Advanced Techniques -> new chapter "Resilient Agent Design" (or Loopy AI L2).
- **RELATIONSHIP:** ❌ net-new. Nothing in the catalog architects an explicit fallback/graceful-degradation path; the closest videos ("Bug Fixing Across Chats") are about *your* recovery across chats, not the agent's own designed fallback route.
- **PROOF TO REUSE:** The `primary_handler -> fallback_handler -> response_agent` SequentialAgent code; the `state["primary_location_failed"]` flag driving the fallback; "the agent can maintain partial functionality to provide at least some value (graceful degradation)."

### 2. Make Your Loop Fail Gracefully (Retry, Fall Back, Escalate)
- **HOOK:** An unattended loop hits a flaky API at 3am - does it die, spin forever burning tokens, or handle it? Design the third option.
- **THE PROMISE:** For Loopy AI builders: give your loop a reliability ladder so transient errors self-heal and only genuinely stuck runs escalate to you.
- **THE SHAPE:** (1) Take an existing loop and inject a failing step; (2) classify transient (retry with backoff) vs terminal (do NOT retry - the "insufficient funds" trap); (3) add a fallback branch; (4) add graceful degradation so partial work still ships; (5) escalate only on persistent failure via a notification carrying a diagnosis, not a raw stack trace; (6) log every rung for later diagnosis.
- **SPINE:** Spine 1.
- **SLOT:** Loopy AI -> new chapter "Reliability & Recovery."
- **RELATIONSHIP:** 🔗 complements "Designing a Task Lifecycle" by being its next step. That video builds the end-to-end spec -> PR -> monitor loop and mentions log-triggered hotfixes; it does not teach the in-loop failure-handling ladder (retry-vs-escalate classification, graceful degradation, escalation payload). Note that "Super Simple Loop" explicitly excludes "advanced reliability patterns" - this fills that gap. Do not re-teach lifecycle stage design; assume the loop exists and harden it.
- **PROOF TO REUSE:** The detect -> handle (log/retry/fallback/degrade/notify) -> recover (rollback/diagnose/self-correct/escalate) three-stage taxonomy; the trading-bot "don't repeatedly try the same invalid trade"; the data-processing agent that "skips the corrupted file, logs the error, continues... and reports skipped files at the end rather than halting."

### Also film-able (not deep-dived)
- Error *detection* as its own micro-topic: validating tool outputs, checking API error codes (404/500), and timeouts as triggers - could fold into Pitch 2's opening beat.

## 📚 Full wisdom (reference)

SUMMARY: Gulli's chapter presents Exception Handling and Recovery - agents must detect errors, then log, retry, fall back, degrade, notify, roll back, self-correct, or escalate to stay reliable.

IDEAS:
- Agents in real environments inevitably meet errors, tool failures, and malfunctions; they need robust detect-and-recover systems.
- The pattern splits into three stages: error detection, error handling, and recovery.
- Error detection catches malformed tool output, API codes (404/500), long response times, and incoherent responses.
- Other agents or monitoring systems can proactively watch for anomalies before they escalate.
- Error handling spans logging, retries, fallbacks, graceful degradation, and notification.
- Retries suit transient errors, sometimes with slightly adjusted parameters.
- Fallbacks use alternative strategies so some functionality survives.
- Graceful degradation keeps partial functionality when full recovery is impossible.
- Notification alerts human operators or other agents when intervention is required.
- Recovery restores stable operation via state rollback, diagnosis, self-correction, and escalation.
- Self-correction adjusts the agent's plan, logic, or parameters to avoid repeating the error.
- Escalation delegates severe cases to a human or higher-level system.
- The pattern pairs well with reflection: analyze a failure, retry with a refined prompt.
- Do not blindly retry non-transient errors (e.g. an invalid trade) - that wastes effort.
- Skip-and-continue: a batch agent skips a corrupted file, logs it, and reports at the end.
- Implementing the pattern turns fragile agents into dependable, resilient components.

INSIGHTS:
- An exception is not just an error to swallow; it is signal that can drive a smarter retry.
- Reliability is designed in advance, not patched after the first silent failure.
- Classifying transient vs terminal failures is the core judgment that makes retries safe.
- Making the fallback a first-class agent (not a bare try/except) keeps the workflow legible.
- Graceful degradation reframes success as "return some value," not "return the perfect answer."
- Escalation is the honest admission that full autonomy has bounds worth encoding.
- Guaranteed execution order (SequentialAgent) is what lets a fallback reliably follow a primary.

QUOTES:
- "the agent can maintain partial functionality to provide at least some value (graceful degradation)." - Gulli
- "if an initial attempt fails and raises an exception, a reflective process can analyze the failure and reattempt the task with a refined approach, such as an improved prompt, to resolve the error." - Gulli
- "It needs to handle these exceptions by logging the error, not repeatedly trying the same invalid trade, and potentially notifying the user or adjusting its strategy." - Gulli
- "It should skip the corrupted file, log the error, continue processing other files, and report the skipped files at the end rather than halting the entire process." - Gulli
- "Implementation of this robust exception handling and recovery pattern can transform AI agents from fragile and unreliable systems into robust, dependable components." - Gulli

HABITS/PRACTICES:
- Log every error with enough detail for later debugging and analysis.
- Retry only transient failures; never re-fire an action a terminal error already rejected.
- Design a fallback path for every critical tool call.
- On partial failure, ship partial value rather than halting the whole job.
- Notify or escalate to a human when a failure is persistent or severe.
- Roll back recent changes to a known-good state when an operation corrupts progress.

FACTS:
- Specific detectable API errors named: 404 (Not Found), 500 (Internal Server Error), 503 (Service Unavailable).
- The ADK example uses `SequentialAgent` with three sub-agents on `gemini-2.0-flash-exp`.
- The fallback agent keys off `state["primary_location_failed"]`; the responder reads `state["location_result"]`.

REFERENCES:
- Google ADK (`google.adk.agents`: Agent, SequentialAgent).
- Model `gemini-2.0-flash-exp`.
- Reflection pattern (cross-referenced).
- McConnell, S. (2004). Code Complete (2nd ed.), Microsoft Press.
- Shi et al. (2024). Towards Fault Tolerance in Multi-Agent Reinforcement Learning. arXiv:2412.00534.
- O'Neill, V. (2022). Improving Fault Tolerance and Reliability of Heterogeneous Multi-Agent IoT Systems. Electronics, 11(17), 2724.

ONE-SENTENCE TAKEAWAY: Assume every tool fails; design agents to detect, retry, fall back, degrade, and escalate.

RECOMMENDATIONS:
- Add a fallback agent behind every critical tool call and drive it with a state flag.
- Classify each failure as transient or terminal before deciding to retry.
- Emit structured logs of every error for post-run diagnosis.
- Escalate to a human with a diagnosis, not a raw stack trace, on persistent failure.
- For batch jobs, skip-log-continue and report skipped items at the end.
- Pair recovery with reflection: reattempt with a refined prompt rather than the identical one.
