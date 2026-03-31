# Reference Script: "Skills 2.0" (Skill Creator Evals Update)

**YouTube ID:** qXWz-V_XMOc
**Published:** 2026-03-04
**Title:** "Anthropic Just Dropped Claude Code Skills 2.0"
**Length:** ~12 minutes

### Actual Performance Data

| Metric | Value |
|--------|-------|
| Day 1 views | 28,251 |
| Day 2 views | 9,384 |
| 48hr total | 37,635 |
| Total (27 days) | 44,486 |
| Day 1 avg watch duration | 246s (4:06) — highest of all 3 hits |
| Day 1 likes | 808 (2.86% like:view) |
| Day 1 subs gained | 343 (1.21% sub:view) |

### Retention Curve (key checkpoints)

| Position | Retention | Notes |
|----------|-----------|-------|
| 10% | 56% | Steeper early drop than the other two |
| 25% | 43% | |
| 30-33% | 39% -> 42% | **BUMP (+3pp)** — PDF skill benchmark data with concrete pass rates |
| 50% | 30% | |
| 65% | 24% | |
| 75% | 22% | |
| 100% | 10% | |

---

## Why This Script Worked

1. **Immediately useful framing** — Opens with "you can now *test* your skills" — viewers instantly know what they'll get and why it matters.
2. **Explains jargon for newcomers** — Defines "eval" as "just a test case, like a teacher grading an exam" in the first 30 seconds. Doesn't assume the audience knows ML terminology.
3. **Capability vs Preference taxonomy** — Creates a mental model (capability uplift vs encoded preference) that helps viewers think about ALL their skills differently, not just the one being discussed.
4. **Concrete benchmark tables** — Shows real numbers (PDF skill: 40% -> 100% pass rate). Viewers can see the skill paying for itself in data, not vibes.
5. **Calls out the gap** — "Anthropic kind of buries the lede" and "here's something the blog doesn't really address" — positions Ray as someone who thinks deeper than the announcement, not just parroting it.
6. **Full demo walkthrough** — The SEO audit skill demo is a complete loop: write evals -> run benchmark -> review in viewer -> iterate -> optimize trigger. Viewers can follow along.
7. **Procedural vs capability eval distinction** — The insurance claim example is the strongest section. Shows that "which output is better?" is the wrong question for most real skills. This insight isn't in Anthropic's blog.
8. **Forward-looking thesis** — "Eventually the eval might *be* the skill" — gives viewers a principle to think about, not just a tool to use.

---

## Full Script

So Anthropic just updated skill-creator -- the thing you use to build skills for Claude Code and Claude.ai. The update is basically: you can now *test* your skills. Like, actually test them. Not "try it and see if it looks right" -- proper evals with pass/fail, benchmarks, and even blind A/B comparisons.

Quick context if you're new to the term: an "eval" is just a test case. You give AI a specific input, describe what the output should look like, and check whether it passes. Same idea as a teacher grading an exam -- here's the question, here's what a good answer includes, did the student hit the marks? That's it. Evals for skills just means: testing whether your skill does what you built it to do.

## The problem this solves

Up until now, building a skill was pure vibes. You'd write a SKILL.md, try it a few times, go "yeah that seems to work," and move on. Then a new model drops, or you tweak something, and the skill silently breaks. You'd never know.

There was no way to regression-test a skill. No way to measure if it actually triggers when it should. No way to compare "version A vs version B" of a skill and know which is better.

That's what this update fixes.

## The two types of skills (and why this matters for testing)

Anthropic makes a useful distinction here:

**Capability uplift** -- skills that teach Claude something it can't do well on its own. PDF form filling, handling concurrency in a programming language its unfamiliar with, that kind of thing. The skill has techniques baked in that beat raw prompting.

**Encoded preference** -- skills where Claude already knows how to do each step, but the skill sequences them *your* way. An NDA review checklist, a weekly report template, a deploy workflow.

The testing angle is different for each.

1. Capability skills might become unnecessary as models get smarter -- evals tell you when the base model has caught up and you can retire the skill.
2. Preference skills are more durable, but evals make sure the workflow still matches what you actually want.

## Testing output quality (evals + benchmarks + blind A/B)

The first system answers: "Does my skill actually produce good output?"

Think unit tests but for prompts. You write test cases -- a prompt, optionally some files, and a description of what "good" looks like. Run them, get pass/fail with timing and token counts.

Real example from Anthropic: their PDF skill couldn't handle non-fillable forms. Claude had to guess coordinates for text placement with no form fields to guide it. Evals caught it, they fixed the positioning logic, done. Without evals that's just a vague "PDFs sometimes look wrong" bug. With evals it's a specific, reproducible failure.

Under the hood, an executor agent runs your skill on each test task and captures the full transcript plus output files. Then a **grader agent** evaluates each of your assertions as pass or fail with *cited evidence* -- not vibes.

For A/B comparisons, it goes further: two executors run in parallel (one with skill, one without), outputs get labeled "A" and "B" and handed to a blind **comparator agent**. It scores both on rubrics, picks a winner. Then an **analyzer agent** unblinds the results and figures out *why* the winner won -- with prioritized suggestions for improving the losing version.

Everything gets aggregated into benchmark stats: mean, standard deviation, min, max for pass rate, time, and tokens. With deltas so you see exactly what the skill costs vs. what it buys you.

**But here's something the blog doesn't really address.** The A/B benchmark asks "which output is better?" For most skills people are actually building, that's the wrong question.

Here's an example. Say you work at an insurance company and you've built a skill that triages incoming claims. It reads the submission, categorizes severity, flags missing documentation, and routes to the right department. Your company requires that any claim over $10k includes a police report -- if it's missing, the skill must flag it. Claims with injury require medical documentation. Property claims get routed to a different team than auto claims.

Now run the A/B benchmark -- Claude *without* the skill will still produce a perfectly reasonable triage. It might even read more naturally. The benchmark says "tie" or maybe even "no skill wins." But that completely misses the point.

You don't care if Claude's freestyle triage is more eloquent. You care: did it catch the missing police report on the $15k claim? Did it flag that the injury claim has no medical docs attached? Did it route the property claim to property, not auto? Did it categorize severity correctly using *your* company's scale, not some generic one?

So for procedural skills -- which is most skills -- skip the A/B baseline entirely. Write assertions that check *process*, not *output*.

## Testing trigger accuracy (description optimization)

The second system answers: "Does Claude even pick up my skill when it should?"

It takes your list of test queries -- some that *should* trigger the skill, some that *shouldn't* -- and splits them into a training set and a held-out test set. Like machine learning.

For each query, it fires up a fresh Claude session and stream-parses the response in real time. The moment Claude starts calling the Skill tool, it checks if it's calling *your* skill. Each query runs multiple times in parallel to get a trigger *rate* -- "triggered 2 out of 3 times" means a flaky description, not a pass.

If queries fail, it calls Claude through the API with extended thinking, feeds it the failures, the full skill content, and every previous attempt -- then asks for a better description. Key trick: it only shows the *training* failures. Test set stays hidden so it can't overfit.

It's genuinely using ML principles -- train/test split, holdout validation, iterative optimization -- applied to prompt engineering instead of model weights.

## Demo: testing an SEO audit skill end to end

Let's say I built a skill that audits any webpage for SEO issues. Not generic "you should add keywords" advice -- a proper checklist. Title tag length, H1 hierarchy, image alt text coverage, internal vs external link ratio, missing schema markup, mobile viewport issues. It follows a specific priority order: critical issues first, nice-to-haves last.

I've been using it for a few weeks and it *seems* to work. But does it? Let's find out.

[Full demo walkthrough: write evals -> run benchmark -> grade -> review in viewer -> iterate -> optimize trigger description]

## The bigger picture

Anthropic kind of buries the lede in the blog: right now a SKILL.md tells Claude *how* to do something. But evals describe *what* good output looks like. As models get smarter, the gap between "what" and "how" shrinks.

Eventually the eval might *be* the skill. You just describe what you want, and the model figures out how. The eval framework is building that bridge.

For now: if you're building skills, add evals. Takes five minutes. Turns "seems to work" into "I know it works." And when the next model drops, you'll know immediately if anything broke.
