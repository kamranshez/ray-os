---
status: filmed
---

In coding, closing the loop is easy — the compiler tells you if it worked. Types break, tests fail, lints complain. The feedback is structured, immediate, and automatic. You barely have to think about it.

Non-technical tasks don't have that. When you ask an AI to write YouTube titles, draft marketing copy, generate subject lines, or propose strategy, there's no compiler. The output _looks_ fine. The model is fluent. But you have no idea if it actually worked until the thing ships and real-world results come back — click-through rates, open rates, conversions, watch time, replies.

The gap between "the AI produced output" and "the output performed well" is where most teams lose compounding. If you never feed those results back, every run starts from scratch. Closing the loop means connecting real-world outcomes back to the AI's process so that future runs are measurably better than past ones.

![[images/closing-the-loop-2.png]]

## What's actually happening

### 1) Without a loop, you pay "first-time cost" forever

Most AI usage for non-technical work looks like: _"Here's a prompt, give me output, I'll judge it in my head."_ The problem is that judgment never gets persisted. So the next time you (or a teammate) run a similar task, the model has no memory of what worked, what failed, or what your standards even are.

The result: every run feels like the first run.

### 2) Real-world outcomes are the only ground truth

For non-technical tasks, "correctness" isn't binary — it's probabilistic and audience-dependent. A YouTube title isn't right or wrong, it's high-CTR or low-CTR. A marketing email isn't correct or incorrect, it converts or it doesn't.

This means the feedback signal comes _after_ execution, not before. You have to:

- Ship the thing (publish the title, send the email, post the ad)
- Measure what happened (A/B test results, engagement metrics, reply rates)
- Feed that signal back to the AI for next time

Without that last step, you have data sitting in your analytics dashboard that never improves your AI workflow.

### 3) Quality stays vibes-based without measurement

Without a loop, quality assessment is anecdotal. A loop forces you to pick a metric, even a simple one:

- "Accepted with no edits / light edits / heavy edits"
- Rubric scores (accuracy, completeness, tone, structure)
- A/B test win rate
- Downstream performance (CTR, conversion, churn, NPS)

Once you can measure, you can improve. Without measurement, the model/tooling doesn't get better — you just _hope_ it does.

![[images/closing-the-loop-3.png]]

---

## Why closing the loop matters

### A) It turns outcomes into signal (even without fine-tuning)

You don't need to retrain the model. You can feed signal back as:

- Better prompts / checklists
- Stronger examples (good and bad)
- Retrieval memory (past winners, past losers, and _why_)
- Evaluators (rubrics) that gate acceptance

Say you're using AI to generate YouTube titles. You A/B test five variants, and variant C wins with 2x the CTR. That result is _signal_. If you just move on, the signal dies. But if you log it — "Title C won because it used a specific number + curiosity gap, while titles A and B were too generic" — the next time you prompt for titles, that log is context. The model gets better _at your audience_ without any fine-tuning.

The key insight: **the feedback doesn't have to reach the model's weights to be useful.** It just has to reach the model's _context_ next time.

### B) It creates compounding returns via project memory

When you store feedback artifacts inside the project (not in someone's head), you get compounding benefits:

- New teammates ramp faster
- The AI becomes "project-native" quickly
- Repeated tasks become templated + testable
- Regressions become detectable

Treat feedback as a first-class project asset, like source code.

### C) It aligns the AI to _your_ definition of "done"

Generic models optimize for general helpfulness. Your organization has specific style constraints, domain rules, risk tolerances, preferred tradeoffs, and its own definition of success. Closing the loop is how you translate those local preferences into enforceable, reusable constraints.

Without that translation, you get **definition drift** — the AI's idea of "good" and your team's idea of "good" slowly diverge, and nobody notices until the gap is painful.

![[images/closing-the-loop-4.png]]

---

## How to close the loop (without boiling the ocean)

### 1) Start with rejection reasons, not rubrics

The easiest entry point: every time you reject or heavily edit AI output, write down _why_ in one sentence. After a week you'll have a natural rubric — the failure modes that actually matter for your work.

### 2) Ship, measure, and log the result

This is the part most people skip. The loop isn't closed until the outcome is recorded in a form the AI can use later:

- Generated 5 YouTube titles → A/B tested → Title B won → logged _why_ it won
- Drafted 3 email subject lines → sent to segment → Subject A had 2x open rate → logged the pattern
- Wrote ad copy variants → ran campaign → noted which hooks converted

The log doesn't need to be fancy. A simple file with entries like "Title pattern: [specific number] + [curiosity gap] → 12% CTR vs 6% average" is enough.

### 3) Build a "two-channel loop"

**Inner loop (fast, per-run):**
Prompt → Output → Validator (rubric/checklist) → Fix → Output

**Outer loop (slow, per-week/month):**
Outputs + Outcomes → Pattern mining (top failures, top wins) → Update artifacts (examples/rubrics/policies) → Update tooling/prompts → affects next runs

The inner loop catches obvious errors now. The outer loop makes the whole system smarter over time.

### 4) Pick the 20% that causes 80% of rework

You don't need to instrument everything. Pick:

- The task type you repeat most often
- The one with the most human edits
- The one where mistakes are most costly
- The one blocking a workflow improvement

Make that task the _gold standard_ with full feedback artifacts, so the pattern spreads naturally.

![[images/closing-the-loop.png]]


