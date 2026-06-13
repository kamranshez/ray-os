---
duration: "14-18 min"
batch: 3
order: 6
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "Borrowed Verifiers"
aliases: [borrowed-verifiers]
---

Every closing the loop pattern needs a verifier. The agent does the work, the verifier checks the work, the loop only exits when the check passes.

If your verifier is the model itself, you don't have a loop. You have vibes wearing a loop costume.

The interesting skill is not writing the loop. It's hunting for someone else's verifier and plugging it in. There are hundreds of free graders sitting around online right now, waiting to be wired up. This segment is how to find them, choose between them, and put them in front of your agent so the loop actually closes.

---

## Why self-grading doesn't work

The most common L2 loop in the wild looks like this. Agent writes some code. Agent reviews the code. Agent says "looks good." Loop exits.

That is not a verifier. That is the same model asking itself a question. The output is whatever the model finds most fluent to say, which is almost always "yes, this is fine."

The same failure shows up in non-code work. Agent writes a cold email. Agent rates the cold email. Agent says it's 8 out of 10. Send it. Get zero replies. Run the loop again. Still 8 out of 10.

The model is not lying on purpose. It just doesn't have a way to check itself against reality. Its grading is the same distribution as its writing. You're sampling from the same well twice and pretending the second sample is independent of the first.

[IMAGE: a closed loop with the same head feeding back into itself, labeled "vibes". Next to it, an open loop reaching out to an external box labeled "the world", with the result flowing back in]

![[loopy-borrowed-verifiers-self-vs-borrowed-1.png]]
![[loopy-borrowed-verifiers-self-vs-borrowed-2.png]]
![[loopy-borrowed-verifiers-self-vs-borrowed-3.png]]
![[loopy-borrowed-verifiers-self-vs-borrowed-4.png]]
![[loopy-borrowed-verifiers-self-vs-borrowed-5.png]]

A real verifier is *outside the model*. It returns a number, a pass/fail, or a structured score that the model cannot influence by changing how it phrases the answer.

The work is finding one. For most domains, someone has already built it. You just have to know where to look.

---

## What counts as a borrowed verifier

Three categories. Each one has different properties and different failure modes.

### Deterministic verifiers

These return the same answer every time for the same input. They are usually free. They are usually fast. And they have been around for decades.

For code: tests, type checkers, linters, formatters, compilers. If pytest passes, pytest passes. If tsc compiles, tsc compiles.

For accessibility: axe-core, WAVE. They return a list of violations. The list does not depend on the model's mood.

For HTML: a validator. For Markdown: markdownlint. For shell: shellcheck.

For data: schema validation, JSON Schema, Pydantic, Zod.

These are the verifiers that should be in every L2 loop you build. They cost nothing. They run in milliseconds. They cannot be talked out of their answer.

### Scored verifiers

These return a number, often probabilistic, often based on a model of their own. Less deterministic, more informative.

For web performance: Lighthouse, WebPageTest, Core Web Vitals from the Chrome User Experience Report.

For React performance: React Doctor. Source: https://www.react.doctor

For SEO: Ahrefs, SEMrush, Surfer SEO, Google PageSpeed Insights. Score against keyword targets, page authority, on-page factors.

For copy: Hemingway, Grammarly, readability scores like Flesch-Kincaid.

For image quality: aesthetic score models, CLIP similarity to a reference, OCR confidence.

For code review at the structural level: SonarQube, Codacy, Codex review, Claude review, GitHub's own code scanning.

These are noisier than deterministic verifiers. The score moves around. But they encode judgment that would take you a week to build from scratch, and they encode it consistently across runs.

**Why scored verifiers with models inside them still count as external.** Lighthouse has model-tuned weighting. SonarQube and React Doctor lean on classifiers. Aren't we right back at self-grading?

No, and the test is sharp: **did the verifier observe something the builder didn't get to author?** Lighthouse runs the page in a headless browser and measures actual LCP, CLS, render times. axe-core traverses the actual DOM. React Doctor watches actual component re-renders. The model parts aggregate real signals into a number; they don't invent the signals. The grading is grounded in runtime observation the builder can't phrase its way past.

A pure static-prompt model scorer — "rate this code 1-10" — fails this test. The model sees only what the builder wrote. There's no second observation. That's self-grading even if you swap to a different model, or run the score in a fresh subagent. A clean context window helps with one thing: the checker hasn't already committed to "this is done," so it stops defending what it just wrote. But a fresh window does not manufacture a second observation. With nothing new to look at, it drifts to "looks fine" for the same reason the first context did. Fresh eyes are necessary for an honest grade. They are not sufficient for a real one.

The rule: a scored verifier is safe to borrow when it touches reality. A scored verifier that only re-reads the artifact is not.

### Real-world verifiers

These are the ones that take time but cannot be faked. The world tells you whether you were right.

For YouTube titles: CTR after publish. Source: YouTube Analytics.

For cold email: positive reply rate. Source: Smartlead, Instantly, your inbox.

For landing pages: conversion rate. Source: your analytics tool.

For ads: cost per acquisition.

For products: retention, NPS, churn.

These are the slowest verifiers. They might take a day or a week to read. But they are the only verifiers that grade against the thing you actually care about. Everything else is a proxy.

A serious L4 or L5 loop uses all three. Deterministic verifiers for safety. Scored verifiers for fast iteration. Real-world verifiers for ground truth. Cross referenced in the same experiment table.

That last shape is covered in detail in [[auto-research-for-non-technical-work]]. Read it after this segment.

[IMAGE: three stacked boxes labeled Deterministic, Scored, Real-world. Each one has a speed label on the left, a noise label on the right. Arrows show the relative tradeoff]

![[loopy-borrowed-verifiers-three-categories-1.png]]
![[loopy-borrowed-verifiers-three-categories-2.png]]
![[loopy-borrowed-verifiers-three-categories-3.png]]
![[loopy-borrowed-verifiers-three-categories-4.png]]
![[loopy-borrowed-verifiers-three-categories-5.png]]

---

## The hunt

This is the skill that almost nobody teaches. Finding the right verifier for your domain.

Three places to look.

**Look for the tool that an expert in the domain already uses.** If you're optimising React component performance, a senior React engineer is opening React Doctor or the DevTools profiler. That's your verifier. You don't need a custom score. You need that tool, in a script, callable by your agent.

**Look for the platform's own grading.** YouTube grades your titles with CTR. Google grades your page with Lighthouse and PageSpeed. Smartlead grades your cold email with reply rate. The platform you are publishing to is usually already grading you. Wire your loop to read that grade.

**Look for the open source linter, validator, or analyser.** For almost any technical domain there is a free CLI tool that returns a structured score. axe-core for accessibility. eslint for JavaScript. mypy for Python types. pa11y for whole-page accessibility audits. hadolint for Dockerfiles. shellcheck for bash. The list is enormous and most of them are free.

If you cannot find a borrowed verifier for your domain, that is a strong signal you're optimising the wrong thing, or you're working in a domain where the only verifier is real-world feedback. Both are useful answers.

---

## Examples by domain

Once you see the pattern, you can apply it almost anywhere.

**React component performance**
- Verifier: React Doctor (https://www.react.doctor) or React DevTools Profiler
- Loop: agent edits component, runs the profiler against a fixture, reads the score, fixes the worst offender, re-runs. Exits when the score is above target.

**Web performance**
- Verifier: Lighthouse, Core Web Vitals
- Loop: agent edits a page, runs `lighthouse` CLI in headless mode, reads the Performance score, applies the top suggested fixes, re-runs. Exits at a target score.

**Accessibility**
- Verifier: axe-core, pa11y
- Loop: agent edits a page, runs pa11y, reads the violations list, fixes the top three, re-runs. Exits when violations are zero or below threshold.

**SEO**
- Verifier: Surfer SEO, Ahrefs Site Audit, or a custom on-page checklist via Lighthouse SEO category
- Loop: agent edits a page, runs the audit, reads the issues, fixes them, re-runs. Exits at the target score or when no more high-priority issues exist.

**Copy and readability**
- Verifier: Hemingway, LanguageTool, a custom GPT-4 grader with a fixed rubric
- Loop: agent drafts, runs the grader, rewrites sentences flagged as hard to read, re-runs.

**Cold email**
- Verifier (fast): a fixed rubric agent that scores against your "good email" examples
- Verifier (slow): smartlead reply rate after sending to 100 leads
- Loop: agent drafts, fast verifier filters bad ones, slow verifier ranks the survivors after sending. Winning variants go back into the rubric.

**Code review**
- Verifier: Codex review, Claude review, or a project-specific reviewer
- Loop: agent writes code, reviewer flags issues, agent fixes the issues, reviewer re-checks. Exits when reviewer finds nothing material.

The shape is always the same. Find the grader. Make it callable from a script. Wire it into the loop.

---

## Wiring it in

The minimum viable borrowed verifier loop is twelve lines of bash plus an agent.

```
while true; do
  claude run --task "$TASK" --constraints "$CONSTRAINTS"
  if borrowed_verifier > threshold; then
    echo "passed"
    break
  fi
  echo "failed, iterating"
done
```

That's it. The agent runs once per iteration. The borrowed verifier grades. If the grade is high enough, exit. Otherwise the agent runs again, this time with the previous attempt and the grader's complaints in context.

Three things matter in this setup.

**One: the verifier output has to be machine readable.** Lighthouse returns JSON. axe returns JSON. React Doctor returns structured findings. If your candidate verifier only outputs prose, write a wrapper that pulls out the score, or pick a different verifier.

**Two: the verifier has to be fast enough to put in a loop.** Lighthouse takes 10 seconds. axe takes one second. React Doctor takes a few seconds. A platform like YouTube takes a week. The slow ones go in L4 and L5 loops with experiment tables. The fast ones go straight in L2.

**Three: the verifier's output has to land back in the agent's context.** Otherwise the agent has no idea what to fix. The loop is not just "did it pass." It's "here is what failed, please fix specifically those things."

[IMAGE: a flowchart, agent writes code, borrowed verifier produces a structured report, report flows back into agent's next iteration with the parts that failed highlighted]

![[loopy-borrowed-verifiers-wiring-1.png]]
![[loopy-borrowed-verifiers-wiring-2.png]]
![[loopy-borrowed-verifiers-wiring-3.png]]
![[loopy-borrowed-verifiers-wiring-4.png]]
![[loopy-borrowed-verifiers-wiring-5.png]]

---

## Trigger on every commit

The natural home for a borrowed verifier loop is your CI.

Every commit triggers the verifier. If the verifier fails, the loop wakes up, an agent attempts the fix, opens a PR, and the verifier runs again on the PR branch. Loop until green.

This is the same shape as Dependabot, but generalised. Dependabot watches your `package.json`. A borrowed verifier loop watches your Lighthouse score, your axe violations, your test coverage, your accessibility audit, your SEO checklist.

You can have ten of these running on the same repo, each one guarding a different score. Lighthouse stays above 90. axe violations stay at zero. Test coverage stays above 80%. Bundle size stays below 500kb. SEO score stays above target.

Each one is a loop. Each loop is cheap. Each commit becomes one iteration of every loop, in parallel. That's compounding feedback you don't have to do anything to keep running.

This is the bridge from L2 single-task loops into L4 continuous worker loops. The CI run is the queue. The commits are the items. The verifier is the gate.

---

## The bigger version: experiment tables

What we've just covered is the L2 version of borrowed verifiers. Loop until a score passes. Single artifact. Single verifier.

The L4 and L5 version is the same idea, but with memory.

Instead of looping until the score passes once, you log every iteration to an experiment table. Each row is: what you changed, what the verifier said, did it ship, what was the real-world outcome. The agent reads the table before proposing the next change.

That is the full auto research pattern. It is covered in detail in [[auto-research-for-non-technical-work]], applied to YouTube titles, cold email, landing pages, and newsletters.

The connection: borrowed verifiers are the *grader* that makes auto research possible. Without a real grader, the table is just opinions. With one, the table is a compounding learning system.

Watch this segment for the building block. Watch the auto research segment for the operating system.

---

## Demo

Open a small React project. Pick a component that's known to re-render too often. Open `react.doctor` and import the component.

Show the score before. Read out the worst offender.

In the terminal next to it, start a closing the loop script. The agent gets the React Doctor report as input. It edits the component, saves, calls the React Doctor CLI (or screenshot-the-page wrapper) to re-grade, reads the new report.

Show three or four iterations on screen. The score goes from red to yellow to green.

Switch to GitHub. Open the repo's CI config. Add a single line that runs the same loop on every PR if the React Doctor score drops below a threshold. Push a commit that intentionally regresses the component. Watch CI fire the loop, watch the bot open a PR with a fix, watch CI re-grade and merge.

Total demo: five minutes. The point is that this is not a one-off script. It's a guard that lives on the repo forever.

---

## Key Insight

> Self-graded loops are vibes. Borrowed verifiers are the unlock. Find someone else's grader, wire it into your loop, and your agent stops lying to itself.

---

## Where we go next

You now have the building block. A loop that grades against the world instead of against itself.

The next segment is Ralph, where we take this pattern and run it across a full task lifecycle. After that, /goal, where the runtime owns the loop and the model can't cheat it. After that, the worker loops where this whole thing gets pointed at a continuous queue.

And later in the class, the full L4 version of borrowed verifiers as a memory system, where every iteration becomes a row in a table the agent reads before the next try. That's auto research, and it's where this pattern becomes a compounding advantage instead of a one-shot trick.

See you in the next one.
