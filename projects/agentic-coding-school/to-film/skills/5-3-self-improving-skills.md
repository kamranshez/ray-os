---
tags: [course, script, skills]
status: "scripted"
lesson: "5.3 Self-Improving Skills"
---

## Self-Improving Skills

So far, improving a skill has been manual. You run it, notice a problem, update the file, run it again. That works. But it means skills only get better when you actively spend time on them.

What if skills could learn from every interaction on their own? You use them, they get better. No manual evals. No editing files. Just a feedback loop that accumulates what works and prunes what doesn't.

That's what we're building now.

### The Learnings File (0:00–2:30)

The concept is simple. Every skill gets a `learnings.md` file in its folder. This file accumulates observations from real usage — what worked, what didn't, patterns that emerged.

> [SCREEN: the research skill folder]

I'm adding a new file to the research skill.

> [SCREEN: editor — creating learnings.md]

```markdown
# Learnings

Observations from real usage. The skill.md reads this file
and incorporates these patterns.

## What works
- Research briefs that open with a direct answer to the query
  get better feedback than ones that start with background context.
- Limiting sources to 3 high-quality links performs better than
  listing every source found.

## What doesn't work
- Scoring topics without explaining the reasoning makes the
  scores feel arbitrary. Always include a one-line justification.
```

Now I need the skill.md to actually read this. I add one line to the process:

```markdown
## Context
Before generating output, read `learnings.md` and incorporate
any relevant patterns into the current task.
```

That's the feedback loop. The learnings file is a living document. Every time I notice something about the skill's output — good or bad — I add it here. And next time the skill runs, it incorporates those observations.

### Manual vs Automatic Capture (2:30–5:00)

Adding learnings manually works. But it depends on me remembering to do it. A better approach is a wrap-up skill that captures feedback automatically.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build a wrap-up skill. At the end of a session, it reviews every skill that was used, checks the outputs against each skill's criteria, and appends any new observations to that skill's learnings.md file. If the user gave feedback during the session — corrections, preferences, complaints — capture those too."]

The wrap-up skill does three things:

**One** — it identifies which skills were used in the session.

**Two** — for each skill, it checks: did the output meet the expectations? Were there corrections? Did the user say "no, shorter" or "no, use bullet points" or "that's perfect, keep doing that"?

**Three** — it appends findings to each skill's learnings.md. Positive observations go under "what works." Corrections go under "what doesn't work."

> [SHOW: the wrap-up skill running at end of a session]

I just finished a session where I used the research skill and the LinkedIn skill. The wrap-up skill reviews what happened.

For the research skill: "User accepted the output without changes. The three-source format was used. Relevance score included justification." → Adds under "what works": "Three-source format with justification consistently accepted."

For the LinkedIn skill: "User said 'too long, keep posts under 150 words.' Current skill says under 200." → Adds under "what doesn't work": "200-word limit is too high. User prefers under 150 words."

Next time I use the LinkedIn skill, it reads learnings.md and sees the 150-word preference. Output gets shorter. Without me editing the skill.md.

### Watching It Improve (5:00–7:00)

Now let me show the compound effect. I'm going to run the research skill three times on similar topics and watch the output change as learnings accumulate.

> [SCREEN: Claude terminal]

**Run one.** I get a research brief. It's good but the TLDR is two paragraphs. I give feedback: "TLDR should be one paragraph max."

> [SHOW: wrap-up skill appending to learnings.md]

**Run two.** New topic. The TLDR is one paragraph. The learnings file worked. But the sources section has four links — I want three max. Feedback: "Cap sources at three."

> [SHOW: learnings.md growing — now has TLDR preference and source cap]

**Run three.** New topic. One-paragraph TLDR. Three sources. Relevance score with justification. The output is noticeably better than run one — and I didn't touch the skill.md once. The learnings file did the work.

> [SPLIT: left — run one output | right — run three output]

Same skill. The skill.md hasn't changed. But the output improved across three iterations because the learnings file accumulated preferences from real usage.

### The Pruning Caveat (7:00–8:00)

Now — there's a trap here. The learnings file can't just grow forever. If you accumulate 200 observations over a few months, you've got a reference file that's bigger than the skill.md itself. And at that point, you're back to the context bloat problem we solved in Chapter 2.

So every week or two, prune the learnings file. Look for observations that overlap — merge them. Remove ones that are obvious or no longer relevant. Keep it tight. Maybe 20-30 lines max.

And here's where evals connect back. You can use the eval system from the last video to verify that your learnings are actually helping. Run the same eval before and after the learnings are applied. If the pass rate doesn't improve, the learnings aren't adding value — prune harder.

The principle: a skill in three months should be dramatically better than the one you built on day one. And you shouldn't have had to manually run evaluations to get there.

### What's Next

Your skills now improve themselves through a feedback loop. But here's a question — how do you know what skills to build NEXT? In the next video, we're building a meta-skill that looks at your entire system and tells you what's missing.
