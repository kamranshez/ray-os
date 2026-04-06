---
duration: "10-12 min"
order: 17
class: "skills"
chapter: "Quality Control"
status: "new"
tags: [course, script, skills]
lesson: "5.1 Evaluating Your Skills"
---

## Evaluating Your Skills

So we've built skills. We've used them. They seem to work. But "seems to work" isn't a standard. How do you know the research skill actually produces better output than Claude without the skill? How do you know the contract reviewer catches what it should? How do you know that change you made last week to the description didn't break something else?

Up until now, the answer was vibes. You'd run it, look at the output, go "yeah that seems right," and move on. No measurement. No comparison. No data.

That changes in this chapter. We're going to use Skill Creator's eval system to actually test our skills — with pass rates, benchmarks, and before-and-after comparisons.

### What an Eval Actually Is (0:00–1:30)

An eval is just a test case. You define what the input looks like, describe what a good output includes, and check whether the skill hits the marks. Same idea as a teacher grading an exam — here's the question, here's the rubric, did the student pass?

The difference from just "trying it" is that evals are structured and repeatable. You can run the same test after making changes and see whether things got better or worse. You can compare with-skill output versus without-skill output on the same task. And you get numbers — not feelings.

### Setting Up the Eval (1:30–4:00)

I'm going to eval our research skill from Chapter 2. We've been using it for a few lessons now — time to actually measure it.

> [SCREEN: Claude terminal]

> [TYPE: "Run evals on the research skill using Skill Creator"]

Skill Creator asks what I want to test. I need to define my criteria — the things a good research brief should always include. I'm going to keep it to four. You want three to five criteria per eval — more than that and the grading gets noisy.

> [TYPE: defining the criteria]

```
1. Does the output include a TLDR section at the top?
2. Does it cite at least 2 specific sources with URLs?
3. Does it include a pros and cons assessment?
4. Does it give a clear bottom-line verdict — worth pursuing or not?
```

Those are my assertions. Each one is a yes-or-no question that can be graded objectively.

Now Skill Creator sets up the test. It's going to run 10 parallel agents — five with the skill loaded, five without. Same prompts, same topics. And it grades each output against my four criteria.

> [SHOW: Skill Creator spawning test agents — 5 with skill, 5 without]

This is running in parallel. Five agents researching the same topic with my skill, five doing it vanilla. Takes a minute or two.

### Reading the Benchmark (4:00–6:30)

> [SHOW: the benchmark results dashboard]

And here are the results. Three columns. Pass rate — what percentage of my criteria did the output meet. Time — how long it took. Tokens — how much context it used.

> [SHOW: specific numbers on screen]

```
                    WITH SKILL      WITHOUT SKILL
─────────────────────────────────────────────────
TLDR section           5/5              3/5
Cites sources          5/5              2/5
Pros/cons              4/5              4/5
Bottom-line verdict    5/5              1/5
─────────────────────────────────────────────────
Overall pass rate      95%              50%
Avg time               42s              35s
Avg tokens            3,100            2,200
```

With the skill: 95% pass rate. Without: 50%. The skill takes slightly more time and tokens — that's expected, it's loading more context. But the quality jump is massive. Half the time, vanilla Claude doesn't even include a verdict. The skill guarantees it.

And that per-assertion breakdown is where the real insight is. Pros and cons scored the same with or without — Claude does that naturally. But TLDR, sources, and verdict only happen consistently with the skill loaded. Those are the things the skill is actually adding.

### Fixing Failures (6:30–8:30)

Now, one of my with-skill runs failed the pros/cons check. Four out of five passed, but one didn't. That's a 80% pass rate on that specific criterion. Not bad, but not reliable.

I can click into that specific test run and see exactly what happened. The output had advantages and disadvantages, but it formatted them as a paragraph instead of a clear pros/cons section. The grader marked it as a fail because it wasn't structured as the assertion expected.

So I have two options. Either the assertion is too strict — maybe a paragraph format is fine and I should loosen the criterion. Or the skill needs to be more explicit about formatting.

I'm going to tighten the skill. I'll add a line to the output template in the reference file:

```markdown
Always format pros and cons as two separate bulleted lists,
not as running prose.
```

> [TYPE: updating the reference file]

And now I rerun the eval.

> [SHOW: Skill Creator rerunning — new results]

Five out of five on pros/cons now. Overall pass rate: 100%. That took about two minutes — update the file, rerun, verify.

And this is the loop. Test → find failures → fix → retest. Each cycle takes a few minutes. And instead of wondering "is this skill good?" you have a number.

### When to Eval (8:30–9:30)

You don't need to eval every skill. The interrogate skill from Chapter 2? It asks questions. The output is subjective — there's no pass/fail criteria that makes sense. Don't force evals onto skills where human judgment is the only meaningful measure.

But for skills with structured output — the research skill, the contract reviewer, the receipt scanner, the invoice generator — evals are valuable. Any skill where you can describe "what good looks like" as a checklist should have evals.

And definitely eval when you make changes. If you update a reference file, change the process steps, or modify the description — rerun the eval to make sure you didn't break something.

### What's Next

We just measured whether a skill works. In the next video, we're going to take this further — A/B testing individual reference files to figure out which ones are actually improving quality and which are just costing tokens.
