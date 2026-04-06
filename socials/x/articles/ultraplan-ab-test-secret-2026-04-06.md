---
tags: [x-article, distribution, claude-code, ultraplan]
date: 2026-04-06
source: socials/youtube/videos/ultraplan.md
---

## Claude Code's Ultraplan Has Three Different Modes — You Don't Get to Choose

Anthropic shipped Ultraplan last week. The pitch: instead of planning in your terminal, hand it off to the cloud, keep coding, come back when it's ready. Review inline. Leave comments. Send it back to your terminal or let the cloud implement it and open a PR.

I've been using it for a few days. The plans were... inconsistent. Some runs caught every edge case, traced every consumer of a changed interface, showed visible reasoning. Other runs felt like a slightly better version of local plan mode. Same prompt, same codebase, wildly different output.

So I dug into it. And here's what I found.

### There Are Three Planners, Not One

When you trigger ultraplan, the server doesn't always run the same planning prompt. There are three variants, and you get assigned one silently:

**simple_plan** — Explores the codebase, writes a plan, done. No subagents, no diagrams. Takes a few minutes. This is the default.

**visual_plan** — Same thing plus Mermaid or ASCII diagrams when the change has meaningful structure. Better presentation, same depth.

**three_subagents_with_critique** — Fundamentally different. Spawns three parallel agents: one to understand architecture, one to find every file that needs changing, one dedicated entirely to risks and edge cases. Then a *fourth* agent reviews the whole plan for missing steps. Takes 10 to 30 minutes.

You don't choose. A server-side config flag assigns you a variant. It's an A/B test.

### The Quality Gap Is Real

I ran the same tasks through local planning and ultraplan multiple times. The deep variant — the one with the dedicated risk agent — caught things like: what happens if the user closes their browser tab mid-call and the webhook never fires? That's not something a simple planning pass surfaces.

Remote plans in general audit blast radius better than local ones. When remote sees "change this interface," it traces every consumer. Local plans make the change and assume the build will catch misses.

Think of it like replacing a light switch. Local approach: swap the switch, flip the breaker, see if the lights work. Remote approach: before touching anything, trace which wires go where, check if anything else shares the circuit. Both get the lights working. If there's a hidden connection to the garage door opener, only remote finds it first.

But here's the nuance — the gap shrinks as the task gets bigger. For a small, 2-file change, remote was massively better. Caught five edge cases local missed entirely. For a 60-file rename, the plans were 90% identical. Remote's advantage is anticipating what *else* might break, which matters less when the task is enumeration.

### The Review Surface Is the Real Feature

Even ignoring the variant lottery, the review experience is a genuine upgrade. You can highlight any passage and leave an inline comment. React to sections. Jump between sections via an outline sidebar. It's closer to reviewing a Google Doc than reading terminal output.

This changes how you interact with plans. In the terminal, you approve or reject. In the browser, you can say "this migration step needs a rollback path" on the exact line. The feedback loop is tighter.

### How I Actually Use It Now

**If the first plan feels thin, run it again.** You might have gotten simple_plan. A second run might land you on the deep variant. The quality difference is worth the extra minutes.

**Or just steal the pattern.** Since we know what those prompts actually say, you can structure your own planning the same way: spawn three subagents — one for architecture, one for file discovery, one for risks — then a fourth to critique the synthesis. You can do this in Claude Code right now with the Agent tool. The prompt engineering is the insight. Ultraplan's infrastructure is just one delivery mechanism.

**Send big tasks to the cloud, keep small tasks local.** Ultraplan frees up your terminal, which matters when planning takes time. But for a quick change where you already know the approach, local plan mode is faster. The sweet spot is medium-to-large tasks where you want the review surface and don't mind waiting.

**Use the cloud for thinking, your terminal for doing.** You can review and iterate on the plan in the browser, then teleport it back to your CLI for implementation. Your local setup has all your tools, environment variables, running services. The cloud has the better review surface. Use both.

### What This Really Is

Ultraplan isn't just a planning feature. It's an A/B testing framework for Anthropic. Every time you approve or reject a plan, every inline comment, every choice between "run in cloud" vs. "send to terminal" — that's signal. They can track acceptance rates per variant. See which prompt structure leads to plans that get implemented vs. rewritten.

The architecture supports swapping in anything: different models, agent configs, critique strategies. They can add a fourth variant tomorrow and route 10% of users to it without a client update.

So the inconsistency you're feeling right now? That's Anthropic figuring out what good planning looks like at scale. The plans will get better because of it. Every time you approve or push back, you're training the system — not the model, but the prompt engineering around it.

Until you can choose your variant, run it twice if it matters. Or just take the three-subagent-with-critique pattern and build your own. The secret was never the feature. It was the prompt.

---
**Source**: [Ultraplan video script](socials/youtube/videos/ultraplan.md)
**Word count**: ~870
