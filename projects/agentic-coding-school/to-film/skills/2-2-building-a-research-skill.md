---
duration: "10-12 min"
order: 5
class: "skills"
chapter: "Your First Skill"
status: "new"
---

## Building a Research Skill with Skill Creator

Flagship Skill Creator build video. The viewer's first experience using Skill Creator to build something from scratch.

### Core Concept

Use Skill Creator to build a research/summarizer skill. Full flow: describe what you want → answer clarifying questions → skill gets drafted → skill gets tested automatically.

### What to Show

**Live Skill Creator session:**

1. Invoke `/skill-creator`
2. Describe: "I want a skill that researches any topic and gives me a TLDR brief with key facts, pros/cons, and sources"
3. Skill Creator spins up sub-agents to explore the problem
4. "Similar to plan mode, it actually asks me questions to answer before it drafts up the new skill." (Chase)
5. It drafts the skill, then auto-tests it

**The benchmarking step** (the "wow" moment):
- "It started running its own test cases. It did six at once, three with the skill, and three without the skill to see if the skill is even worth it." (Chase)
- "It gave me the benchmark tab — assertion pass rate, time, tokens both with and without." (Chase)
- "You get a nice summary about what the skill is actually adding over the baseline and what the baseline does fine on its own." (Chase)

**The iterative feedback loop** (competitor gap — nobody shows this well):
- First output is 70-80% of what you want
- Give feedback: "make the sources section shorter, add a bottom-line verdict"
- Claude updates the skill, re-tests
- From Brand DNA video: his research skill scores topics 1-10, filters last 30 days only, cross-references with content pillars. All added through iteration.

### Conversational Building Alternative

"You can even offload some of this to Claude. Say 'Hey, look at how we've been creating stuff in my repo. Do you have any ideas for skills? If so, use the skill creator to create it.'" (Chase)

Also: "You could just tell Claude 'help me build a skill that does X' and it will interview you and draft it." — Skill Creator is better for complex skills with evals, but conversational building works great for simple ones.

### Test the Result

"I'm saying I'm doing a 10-minute master class on Claude Code. Use this new skill. And it came back with quite a bit — analyzed my top performers over the last 3 months, winning patterns vs what's flopping, competitive landscape, then title options in tiers." (Chase)
