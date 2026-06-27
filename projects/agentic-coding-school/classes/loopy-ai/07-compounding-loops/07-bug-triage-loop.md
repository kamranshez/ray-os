---
video_id: "zlLeKrUL"
duration: "14-18 min"
batch: 6
order: 23
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Bug Triage Loop"
aliases: [bug-triage-loop]
---

If you build exactly one loop after this class, build this one.

Failing traces go in. Fixes come out. The eval suite re-runs to confirm. A human reviews and merges. That's it. Five stages.

It looks modest on the diagram. It is the single highest-leverage loop a team can run, because it is the only loop in the whole stack that fixes the thing that makes the other loops. Every bug it closes makes every other loop you've built slightly more reliable. It compounds on the entire system underneath it.

This is the loop Rippling used to ship AI across every product, for over a million users, in roughly six months.

Let me show you why it's different, and why almost nobody has built it.

[IMAGE: dark canvas, a tall stack of the class's other loops drawn as tiers, and one loop sitting underneath the entire stack labeled "the bug triage loop". Each bug it closes emits an upward pulse that makes every tier above it slightly more reliable, little green "+reliability" ticks lighting up across the whole stack. Caption: "the one loop that fixes the thing that makes the other loops".]

---

## The loop that fixes loops

Every other loop in this class fixes one kind of artifact.

The closing-the-loop pattern fixes one code change. A worker fixes one ticket at a time. A discovery loop surfaces one shortlist. Useful, but each one operates on the output.

The bug triage loop operates one level up. It does not fix an artifact. It fixes *the system that produces artifacts*. When a fix lands, it doesn't just close one bug, it tightens the eval suite, and the tightened suite now guards every future run of every loop that touches that code path.

That's the compounding property, and it's worth being precise about. The first time this loop runs, you have N bugs and one fixer. The hundredth time, you have far fewer bugs, *and* a fixer that has now seen ninety-nine failure modes, every one of them frozen into the eval suite so it can never silently come back.

Most loops get you a better artifact. This loop gets you a better factory.

[IMAGE: dark canvas, two loops side by side. Left loop labeled "fixes the artifact" circling a single document icon. Right loop labeled "fixes the factory" circling a machine that itself stamps out documents, with a small upward arrow showing the improvement flowing back into the machine]

![[loopy-bug-triage-loop-fixes-the-factory-1.png]]
![[loopy-bug-triage-loop-fixes-the-factory-2.png]]
![[loopy-bug-triage-loop-fixes-the-factory-3.png]]
![[loopy-bug-triage-loop-fixes-the-factory-4.png]]
![[loopy-bug-triage-loop-fixes-the-factory-5.png]]

---

## What Rippling actually built

Rippling is a workforce platform. HR, IT, payroll, finance, global operations. Their data model spans thousands of tables with overlapping entity names across domains, so "what's my balance?" could mean a health savings account, a credit card, a contractor payment account, or a time-off policy.

Source: https://blog.langchain.com/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith/

They shipped AI across all of it, in production, for over a million users, in six months. The thing that let them move that fast was not a smarter model. It was a loop they call the self-healing eval loop. Here is how their principal engineer describes it, almost verbatim:

> We pull failing traces, have an agent understand what's going on, propose a few solutions, run the evals again to see if it improves, and loop until it's complete. Then a human reviews and merges the PRs.

Read that again, because every clause maps onto a level of the loop stack you already know.

That sentence is an L5 discovery loop, an L4 worker, and an L2 verifier, composed into one pipeline. They didn't invent a new level. They wired three levels you've already met into a single production circuit.

[IMAGE: dark canvas, the principal engineer's sentence laid out as a ribbon with each clause underlined and tagged: "pull failing traces" tagged source, "an agent understands and proposes solutions" tagged L4 worker, "run the evals again to see if it improves" tagged L2 verifier, "a human reviews and merges" tagged human gate. An arrow shows the tagged clauses snapping together into one production circuit. Caption: "no new level, three levels you already know wired into one circuit".]

---

## The five stages, by L-level

Let me name each stage by the level it operates at, because the whole point of this class is that you can now read a pipeline this way.

**Stage one. Source.** LangSmith, their trace store, emits failing production traces. This is just the trigger slot from strip-the-model-out, fed by real users instead of a clock. The world generates the work.

**Stage two. The L5 triager.** Failing traces arrive faster than you can fix them, so something has to decide which ones are worth fixing today. This is the triager shape from the discovery segment: many streams in, one ranked shortlist out, ordered by user impact and reproducibility. It does not fix anything. It decides what should become work.

**Stage three. The L4 worker.** For each trace the triager picked, an agent runs a full task lifecycle. It reads the failing trace, analyses the failure, proposes a fix, opens a PR. This is the worker anatomy: a pick rule at the front door, a full L3 in the work slot.

**Stage four. The L2 verifier.** This is the part that makes it safe. The agent re-runs the eval suite against its own fix. The PR only survives if the fix closes the specific regression *and* doesn't break the rest of the suite. This is a borrowed verifier in the purest form. The eval suite is external to the fixer, it returns a structured pass or fail, and the fixer cannot rephrase its way past a failing assertion.

**Stage five. Human review.** A person reads the action log, not just the diff, and merges. We'll come back to why the human stays in.

[IMAGE: dark canvas, hexagonal flow. Trace store at the top. Triager (L5) and worker (L4) down the left side. Eval suite (L2) and human review on the right. A PR merging at the bottom center. Each node tagged with its L-level]

![[loopy-bug-triage-loop-five-stage-pipeline-1.png]]
![[loopy-bug-triage-loop-five-stage-pipeline-2.png]]
![[loopy-bug-triage-loop-five-stage-pipeline-3.png]]
![[loopy-bug-triage-loop-five-stage-pipeline-4.png]]
![[loopy-bug-triage-loop-five-stage-pipeline-5.png]]

Rippling actually run this against a layered eval system. Offline mocks on every commit, three to four hundred integration queries against a live sandbox post-merge, about ten deploy-blocking critical scenarios, and continuous scheduled evals against production multiple times a day. The loop fixes the failures the bottom catches before the top ever blocks a deploy.

---

## The eval suite is the moat, not the fixer

Here is the part most people get backwards.

When teams imagine building this loop, they obsess over the fixer. Which model, which prompt, how clever does the agent need to be. Wrong end of the telescope.

The fixer is replaceable. Swap the model next quarter and the loop keeps running. What you cannot swap, what took real work to build, is the eval suite. The suite is where ninety-nine failure modes are encoded. It is the thing that says "this used to break, prove it doesn't anymore" on every single run, forever.

This is the same property as the ACE playbook from the three-role-split segment. The model is frozen and replaceable, the accumulated context is the asset that survives model swaps. The eval suite *is* a playbook. It's a version-controlled record of everything your system has ever gotten wrong, written in a form a machine can check.

And it has the same second life the ACE playbook has. New engineers join Rippling and the eval suite is how they learn the product. Want to know what this system is supposed to do, and every way it has historically failed? Read the evals. The suite is the documentation, the regression net, and the onboarding doc, all at once.

So the uncomfortable truth: most teams cannot run this loop. Not because the loop is hard to wire, the loop is five stages you already understand. They can't run it because they have no eval suite for the fixer to grade against, and without one stage four collapses into self-grading. The agent proposes a fix, the agent decides the fix is good, you're back to vibes wearing a loop costume.

If you don't have an eval suite, that is the first thing to build. Not the loop on top of it.

[IMAGE: dark canvas, a layered stack labeled "eval suite" growing taller over time, each new layer labeled with a past bug. A small swappable "fixer" box plugs into the side with a dotted "replaceable" arrow, while the eval stack is anchored with a "this is the asset" label]

![[loopy-bug-triage-loop-eval-suite-is-the-moat-1.png]]
![[loopy-bug-triage-loop-eval-suite-is-the-moat-2.png]]
![[loopy-bug-triage-loop-eval-suite-is-the-moat-3.png]]
![[loopy-bug-triage-loop-eval-suite-is-the-moat-4.png]]
![[loopy-bug-triage-loop-eval-suite-is-the-moat-5.png]]

---

## This is ACE running in production

If the shape feels familiar, it should. The bug triage loop is the ACE three-role split wearing production clothes.

The **Generator** is the fixer. It produces the candidate, exactly the L1 builder role.

The **Reflector** is the eval suite. In the original ACE pattern the Reflector was the adversarial reviewer run across a window of attempts, the skill whose only job is to find what's wrong. Here that role is played by a frozen suite of assertions that have each caught a real failure. Same job, refuse the candidate, find the break, hand back a structured report.

The **Curator** is whoever maintains the evals. Every time a new failure mode slips through, someone has to add the assertion that catches it next time. That's the Curator's structured-delta job: the suite only ever grows, and it grows by absorbing exactly the failures that got past it.

That mapping is not a cute analogy. It's the reason the loop compounds. ACE works because the context evolves while the model stays still. The bug triage loop works for the identical reason, the eval suite evolves while the fixer stays replaceable. You've seen the abstract version. This is what it looks like when it's guarding a product a million people depend on.

[IMAGE: dark canvas, the three ACE roles on the left mapped by arrows to their production counterparts on the right. "Generator" maps to "the fixer", "Reflector" maps to "the eval suite" (a frozen wall of assertions that refuses the candidate and hands back a structured break), "Curator" maps to "whoever adds the assertion that catches the next miss". The fixer is tagged "frozen, replaceable", the eval suite tagged "evolves, the asset". Caption: "the same split, wearing production clothes".]

---

## Why the human stays in for the merge

Stage five is a human reading the log and clicking merge. After everything this class has said about closing the loop, you might expect me to tell you to remove that human. I'm not going to.

The human is not there because the loop is untrustworthy. The verifier is real, the evals are borrowed, the fix is grounded. The human is there because of the *consequences*. This is a production code change to a system a million people use. That's the autonomy dial talking: the dial is set per action, and it's judged on the world, not on the filesystem. A merge to production has a large blast radius and an embarrassing failure mode, so it sits at the top notch, never-without-me.

And notice what the human reads. Not the diff. The action log. By the time it reaches the human, the diff has already passed the eval suite, so re-reading the code line by line is low-value. What the human is actually checking is the *judgement*: did the agent fix the real problem or paper over a symptom, did it pick the right trace to begin with, is the fix the kind of change we want in this codebase. That's a review of reasoning, not syntax. The borrowed verifier already handled syntax.

This is the autonomy dial doing exactly what it's for. Stages one through four ship silently. Stage five never ships without you. One loop, two notches, because the actions inside it carry different blast radius.

[IMAGE: dark canvas, the five-stage loop with an autonomy-dial notch on each stage. Stages one through four sit at a low "ships silently" notch, stage five sits pinned at the top "never without me" notch because its blast radius is a production change for a million users. At stage five a human reads an "action log" (which trace, what changed, the eval delta) rather than the diff, with a tag "reviewing judgement, not syntax, the verifier already did syntax". Caption: "one loop, two notches, set by blast radius".]

---

## Demo

I'll run a stand-in for the full pipeline using one of my own loops, because the shape is identical at small scale.

1. **Source.** I point at my sentence-mining loop's failure log instead of LangSmith. Cards that got flagged wrong, bad audio cuts, mistimed screenshots, the i-plus-one diff misfiring. These are my "failing traces."

2. **Triager.** A small discovery pass ranks the failures. Not by recency, by impact: how many future cards would this failure mode poison? The audio-offset bug ranks above a one-off typo. On screen, a shortlist of three failure modes out of maybe twenty.

3. **Worker.** For the top failure, an agent reads the failing card, traces the cause back into the skill, and proposes a fix to the skill itself, not to the one card. It opens a PR against the skill.

4. **Verifier.** This is the load-bearing part. Before that PR can stand, the agent re-runs my mining eval suite: a fixed set of recorded clips with known-correct cards. The fix has to make the broken case pass *and* leave the other cases passing. I show one run where the fix passes the target case but regresses two others, and the loop discards it and tries again. That discard is the whole game. Without the suite, the agent would have called its first attempt a success.

5. **Human review.** The PR surfaces in Slack with the action log: which failure, which trace, what changed, what the eval delta was. I read the log, not the diff. I merge.

Then I do the thing that proves the point. I add the failure mode I just fixed as a permanent case in the eval suite. Now I cold-open a fresh session and ask it to "improve the timing logic," a change that would have silently reintroduced the old bug. The suite catches it instantly, red, before any card is ever generated.

Total demo: six minutes. The point lands at the end: the artifact I fixed was one card. The asset I built was a suite that will never let that bug back in.

---

## Key Insight

> Every other loop fixes an artifact. This one fixes the factory. The fixer is replaceable; the eval suite is the moat, and it gets stronger every time a bug gets past it.

---

## Where we go next

You now have the highest-leverage loop in the class, and the one warning that comes with it.

This loop only compounds as long as the eval suite keeps absorbing *new* failures from the real world. The moment the suite stops seeing fresh signal and starts grading itself against its own past answers, the compounding quietly reverses. The loop gets more confident and less correct at the same time, and nobody notices.

That failure has a name, and it's the next segment. The echo chamber.

See you in the next one.
