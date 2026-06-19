---
class: "skills"
chapter: "Your First Skill"
status: "idea"
tags: [course, script, skills]
lesson: "2.2 Building a Research Skill with Skill Creator"
---

## Building a Research Skill with Skill Creator

In the last video we built the interrogate skill by hand — 30 lines in a text editor. And that's a great way to understand the format. But for anything more complex, you don't want to write these manually. You want to use Skill Creator.

Skill Creator is a skill that builds other skills. It interviews you, drafts the skill, and then — this is the part nobody expects — it tests the skill automatically, with benchmarks, to see if it actually makes a difference.

We're going to build a research skill from scratch. Start to finish.

### Invoking Skill Creator (0:00–1:30)

> [SCREEN: Claude Code or Co-work terminal]

We installed Skill Creator in the setup video. Now we use it.

> [TYPE: /skill-creator]

That invokes it. And now I describe what I want.

> [TYPE: "I want to build a skill that researches any topic and gives me a TLDR brief with key facts, pros/cons, sources, and a bottom-line verdict on whether the topic is worth pursuing"]

Now watch. Skill Creator doesn't just start writing the skill. It does what any good consultant would do — it asks me questions first. Same principle as the interrogate skill we just built, actually. It needs to understand what I'm building before it builds it.

> [SHOW: Skill Creator asking clarifying questions]

"What kind of topics will you research? How deep should it go? Do you want it to search the web or work from documents you provide? What format do you want the output in? Should it include competing perspectives?"

I answer those. Takes a couple minutes. And then it starts working.

### The Draft (1:30–3:30)

> [SHOW: Skill Creator spinning up sub-agents]

It spins up sub-agents to explore the problem space. It's figuring out what tools the skill will need, what the process flow should look like, how to structure the output. This is similar to how plan mode works if you've used that before — it's doing research before it commits to anything.

And then it drafts the skill.

> [SHOW: the generated SKILL.md file]

There it is. A complete skill file. Name, description with trigger keywords, step-by-step process instructions. It's got a research phase, an analysis phase, a formatting phase. References to web search tools. Output template with TLDR, key facts, pros and cons, sources list, and the bottom-line verdict I asked for.

Now here's an important moment. This first draft is probably 70 to 80 percent of what you want. It's good. It's structured well. But it's not exactly yours yet. Maybe the sources section is too long. Maybe you want the pros and cons formatted differently. Maybe you want it to always score topics on a 1-to-10 scale.

We'll iterate on that. But first — Skill Creator does something unexpected.

### The Benchmarking Step (3:30–6:00)

> [SHOW: Skill Creator launching test cases]

It starts testing the skill. On its own. Without me asking.

It spins up six parallel test runs. Three with the skill loaded. Three without — just baseline Claude with no skill at all. Same prompts, same tasks. And it's going to compare the results.

This is the moment that surprised me the first time I used this. It's not just drafting a skill and saying "here you go." It's actually running experiments to see if the skill makes Claude better or if it's dead weight.

> [SHOW: the benchmark results tab]

And here are the results. You get a benchmark tab with three columns. Assertion pass rate — what percentage of quality criteria did the output meet. Time — how long it took. And tokens — how much context it used.

> [SHOW: specific numbers — e.g., with skill: 87% pass rate, 45s, 3200 tokens / without: 52% pass rate, 38s, 2100 tokens]

With the skill, 87% pass rate. Without, 52%. The skill takes slightly longer and uses more tokens — that's expected, it's loading more context. But the quality jump is massive. 52 to 87 percent. That tells me the skill is actually doing something, not just adding noise.

You also get a summary of what the skill adds over baseline and what baseline handles fine on its own. So if there's something in the skill that doesn't actually help, you can strip it out. We'll go deeper on this in Chapter 5 when we cover evals.

### The Iteration Loop (6:00–9:00)

Now. The first draft is 80 percent there. Time to fix the other 20.

> [SCREEN: Claude Code terminal]

I look at the test outputs and I have feedback. The sources section is listing every URL it found — I want three max, the highest quality ones. And I want each topic scored on a scale of 1 to 10 for relevance to my business.

> [TYPE: "Make the sources section max 3 links — pick the highest quality ones, not just the first ones found. Also add a relevance score from 1-10 based on how well the topic fits my content pillars"]

Skill Creator takes that feedback, updates the skill.md, and re-runs the tests.

> [SHOW: updated test results]

Better. Sources are tighter. Relevance score is there. Pass rate went up to 91%.

Now I could keep iterating — and for production skills, you absolutely should. But this shows the loop. Describe what you want. Answer questions. Get a draft. Review the benchmarks. Give feedback. Repeat. Each cycle takes a few minutes and the skill gets measurably better.

And here's a thing worth noting — this loop is exactly what separates a skill that "kind of works" from one that's genuinely reliable. Most people skip it. They get the first draft, use it twice, decide skills are overhyped. The iteration is where the real value gets built.

### Testing It For Real (9:00–10:30)

Now the skill is built. Time to use it on a real task.

> [TYPE: "Research what's trending in AI automation tools this month. Use the research skill."]

And it goes. Searches the web. Pulls sources. Analyzes what it found.

> [SHOW: the research output — TLDR, key facts, pros/cons, sources, relevance score, bottom-line verdict]

TLDR at the top. Key facts. Pros and cons of the trending tools. Three high-quality sources. Relevance score: 8 out of 10 for my content. Bottom-line verdict: "Strong topic — low competition, high search interest, directly relevant to your audience."

That's a research brief I can act on. And I got it in about 30 seconds without writing a detailed prompt. The skill handled the prompting for me. That's the whole point.

### The Conversational Alternative (10:30–11:00)

One more thing. You don't always need Skill Creator. For simpler skills, you can just talk to Claude directly. "Hey, I want to build a skill that does X. Help me create it." Claude will interview you, draft the skill.md, and save it. No benchmarks, no test runs — but for simple skills like the interrogate one we built last time, that's fine.

Skill Creator is for when you want the full loop — the testing, the benchmarks, the iteration. For anything you're going to use repeatedly and need to be reliable, use Skill Creator. For quick one-offs, just ask Claude.

### What's Next

We just built a skill with Skill Creator and it works. But we went through it fast and I glossed over why the skill file is structured the way it is. In the next video, we're going to open this skill up and dissect it — the folder structure, the 200-line rule, reference files, and the guardrails section. That's the anatomy of a well-built skill.
