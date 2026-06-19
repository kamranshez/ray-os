---
tags: [course, script, skills]
status: "scripted"
lesson: "5.2 A/B Testing Reference Files"
---

## A/B Testing Reference Files

In the last video we learned how to eval a skill — does it pass your criteria or not. Now we're going to use that same system to answer a more surgical question: which reference files are actually pulling their weight?

Because here's the thing. Every reference file has a cost. It takes tokens to load. It takes time. It adds context that Claude has to process. And if a reference file doesn't actually improve the output, it's dead weight. You're paying the cost without getting the benefit.

So we're going to A/B test them. Same skill, same task — once with a reference file, once without. And we'll see if the quality changes.

### The Setup (0:00–1:30)

I'm going to use the AI SEO skill we refactored in Chapter 3. It's got four reference files:

> [SCREEN: the skill folder showing reference files]

```
references/
├── authority-signals.md
├── ai-visibility-audit.md
├── content-type-optimization.md
└── platform-guidelines.md
```

Each of these loads during a specific step of the audit. The question is: do all four of them actually matter? Or could we get the same quality with three? Or two?

### Running the A/B Test (1:30–4:00)

I'm going to test `content-type-optimization.md` first. It's the largest reference file — about 80 lines of rules for different content formats.

> [SCREEN: Claude terminal]

> [TYPE: "A/B test the ai-seo skill — run it 5 times with all reference files, and 5 times with content-type-optimization.md removed. Same task, same criteria as last time."]

Skill Creator sets up the A/B test. It spawns 10 agents — 5 with the full skill, 5 with the reference file removed. Same evaluation criteria from the previous video.

> [SHOW: test agents running in parallel]

While those run, here's what we're looking for. Three possible outcomes:

**Outcome one — same pass rate, fewer tokens.** The reference file didn't contribute to quality. Remove it. You just saved tokens on every activation.

**Outcome two — lower pass rate.** The reference file matters. Keep it.

**Outcome three — same pass rate, but different in ways the assertions don't capture.** This is where you read the actual outputs and judge qualitatively. Maybe the assertions all pass, but the output is subtly worse in a way your criteria didn't measure. That means either keep the file or add a better assertion.

> [SHOW: A/B test results]

```
                        ALL FILES       WITHOUT content-type
────────────────────────────────────────────────────────────
Pass rate               93%             90%
Avg time                48s             39s
Avg tokens             3,400           2,600
```

Interesting. Pass rate barely moved — 93 to 90 percent. But the time dropped by 9 seconds and the tokens dropped by 800. That's a meaningful efficiency gain for a tiny quality difference.

Now I check — which assertion failed in the without-content-type version?

> [SHOW: per-assertion breakdown]

The "checks content format suitability" assertion went from 5/5 to 4/5. One test case didn't get a content format recommendation. Everything else was identical.

So the reference file contributes to one specific assertion about 80% of the time. Is that worth 800 extra tokens on every run? Depends on how important content format recommendations are to you. If it's critical — keep it. If it's nice-to-have — remove it and save the tokens.

### Testing Every File (4:00–5:30)

Now I repeat this for each reference file. Same process — remove one, run 5 tests, compare.

> [SCREEN: results table for all 4 files]

```
REMOVED FILE               PASS RATE    TOKEN SAVINGS
─────────────────────────────────────────────────────
authority-signals.md          72%         -600 tokens
ai-visibility-audit.md       45%         -900 tokens
content-type-optimization.md  90%         -800 tokens
platform-guidelines.md        91%         -400 tokens
```

Now the picture is clear. The AI visibility audit is load-bearing — pass rate drops to 45% without it. Authority signals matter too — 72%. But content-type and platform-guidelines barely move the needle.

So I could remove platform-guidelines entirely and save 400 tokens per run with almost no quality loss. Content-type is borderline — depends on my use case.

This is how you go from a skill with four reference files to a lean skill with two that performs just as well. And in complex workflows where multiple skills chain together, those token savings compound.

### The Principle (5:30–6:30)

Every reference file should earn its place. If removing it doesn't change the output, remove it. If removing it drops quality, keep it. If you're not sure, test it.

A lean skill — fewer files, same quality — will:
- Activate faster
- Leave more context window for your conversation
- Be more reliable when chained with other skills
- Cost less in tokens over hundreds of uses

And the beautiful thing is this testing takes maybe five minutes per reference file. You run it once, get your answer, and make a decision based on data instead of gut feel.

This is the difference between a skill someone threw together and a skill that's been optimized. Same content. Fraction of the cost.

### What's Next

We can now measure skills and optimize their reference files. But so far, improvement requires us to manually run tests and make changes. In the next video, we're going to make skills that improve themselves — automatically, after every use, without you running an eval.
