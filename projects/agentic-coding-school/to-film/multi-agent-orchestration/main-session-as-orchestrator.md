---
class: "claude-code"
chapter: "Subagents"
---

## The Mindset Shift

For two years, you've been using Claude Code the same way. Type something. Claude does something. Read the result. Respond. The session grows. Eventually it gets dumb. You start a new one.

That whole loop is about to change.

There's a pattern from recent research called Recursive Language Models. RLM for short. And once forked subagents shipped in Claude Code, RLM stopped being a research idea and started being something you can use every day.

The shift is this. Stop being the worker. Start being the orchestrator.

[IMAGE: dark background. Left side shows a person labeled "you" working at a desk, sweating, surrounded by paper. Right side shows the same person sitting calmly at a desk, while three smaller workers in the background do the actual work and slide finished reports onto the desk]

![[images/main-session-as-orchestrator/mindset-shift.png]]

---

## The RLM Idea in Plain English

A normal LLM session works like this. You have a context window. You stuff things into it. The model reads everything every time it thinks. The bigger the context, the more it has to process. Past a certain size, the model gets worse, not better, even though everything technically fits.

That degradation has a name. Context rot.

Recursive Language Models flip the script. Instead of stuffing the data into the model, you treat the data as something sitting outside the model. The main model writes code or spawns subagents to look at chunks of the data, summarize them, and report back. The main model only ever sees the summaries. It never has to read the raw thing.

The classic example from the research is "list every named character in Frankenstein."

Naive approach. Dump 78,000 tokens of novel into the prompt. Ask. The model misses minor characters because of context rot.

RLM approach. Split the novel into chunks. Spawn a subagent for each chunk. Each subagent finds named characters in its chunk. Root model deduplicates the lists. Result is dramatically more complete.

The main model never read the book. It read summaries of the book.

[IMAGE: dark background. Top half labeled "Naive" shows the entire book being shoved into a single fat model that's drooling and confused. Bottom half labeled "RLM" shows the book split into chunks, each chunk handled by a small subagent, with results bubbling up into a calm main model that just stitches the pieces together]

![[images/main-session-as-orchestrator/rlm-frankenstein.png]]

---

## Why Forked Subagents Are the Right Primitive

For RLM to work, you need delegation that's basically free. If every subagent costs you a fortune to spin up, you can't recursively delegate. The pattern collapses under its own cost.

Forked subagents are the missing primitive. They share the parent's prompt cache, so spinning one up costs the price of the new tokens, not the inherited context. They start with the parent's full state, so you don't have to write a long handoff prompt. They return only the result, so the parent stays clean.

That's the trifecta. Cheap to spawn. Inherits context. Returns clean.

That's what makes RLM viable in a real Claude Code session, not just in a research paper.

---

## What This Looks Like in Practice

Here's what the orchestrator pattern actually feels like when you use it.

You start a session with a goal. Maybe "redesign the auth flow for this app."

In the old world, you'd start reading code. The session would grow. You'd hit 50k tokens just understanding the codebase before you wrote a line. By the time you actually started designing, you'd be at 100k tokens of context and the model would be getting fuzzy.

In the orchestrator world, you don't read the code. You fork a subagent and tell it to read the auth flow and report back with a summary. It comes back with two thousand tokens of "here's how auth currently works, here are the four files involved, here are the edge cases."

Now the main session has the summary, not the code. You're at 5k tokens, not 50k.

You think about the design. You make decisions. You write a plan. Then you fork another subagent and tell it to implement section one. It works in its own context, ballooning to whatever size it needs, and returns with "done, here are the files I touched, here's a summary of the changes."

Your main session gains 500 tokens. The fork did 100k tokens of work and threw it all away.

You repeat. Section two, section three. Each one is a fork. Each one returns a summary. By the end of the project, your main session has maybe 30k tokens in it. It's still sharp. It's still capable of high-quality reasoning. The expensive thinking all happened in temporary contexts that lived and died with their tasks.

[IMAGE: dark background. Top half shows a "Traditional Session" timeline that grows fatter and fatter, eventually turning red and labeled "context rot". Bottom half shows an "Orchestrator Session" that stays thin and lean throughout, with little forked balloons branching off, ballooning to large size, then collapsing back into the main timeline as small "result" nodes]

![[images/main-session-as-orchestrator/orchestrator-timeline.png]]

---

## The Shift in Your Head

The mental model change is the real unlock.

Stop thinking of your session as the place work happens. Start thinking of it as the place work gets coordinated.

Your job in the main session is no longer "do the task." It's "decide what subagents to spawn, what they should do, and how to combine their outputs." You're a manager now. The subagents are the workers.

This sounds abstract until you try it. Then it feels obvious. The main session becomes a small log of decisions. The actual code reading, code writing, search, verification, all happens in forks that return summaries.

Because the main session stays small, you can run for hours without it degrading.

---

## The Recursion Part

Here's where it gets interesting. Subagents can spawn subagents.

You fork an orchestrator subagent. Its job is "implement the entire auth refactor." It then forks its own subagents. One to read the existing code. One to write the new code. One to write tests. One to verify. The orchestrator subagent coordinates them, and reports back to the main session with a summary of what it did.

Now you have two levels of orchestration. The main session orchestrates a few high level subagents. Each high level subagent orchestrates its own pool of workers. The actual work is happening three layers deep, and the main session has no idea about the details. Just the outcomes.

This is recursive language models. Not a metaphor. Literally what's happening.

[IMAGE: dark background, tree diagram. Main session at the top, a few orchestrator forks branching off, each spawning their own worker forks underneath. Arrows showing results bubbling back up the tree. Bottom-most workers are large and busy, top of the tree stays small and clean]

![[images/main-session-as-orchestrator/recursion-tree.png]]

---

## When This Pattern Wins

Three signals that you should reach for orchestration.

**Long sessions.** If you'd normally hit context limits or feel the model going dumb, orchestrate. The whole point is to keep the main session short.

**Heavy data.** If the task involves reading a lot of code, docs, logs, or data, you don't want any of it in the main session. Fork subagents to summarize and only keep the summaries.

**Multi-step tasks where each step generates noise.** If a task involves twenty tool calls of intermediate state that you don't actually need long-term, fork it. Let the noise stay in the fork.

If your task is small and the main session has the right context already, just do it. Orchestration is for when context discipline is the bottleneck.

---

## When Not to Bother

Don't orchestrate work that's already small. Don't fork a subagent to read one file. Don't spawn a worker for a one line edit. The setup cost isn't worth it.

The pattern earns its keep when the inner work would otherwise pollute your main context. If the inner work is small, just do it inline.

---

## Demo

The demo is a real workflow.

1. Start with an empty session. State the goal: "Refactor the user dashboard to use the new design system."
2. Fork a reader subagent. "Read the dashboard code and report back what's there."
3. Reader returns. Show the main session is still under 10k tokens. Show the summary is rich.
4. Make a design decision based on the summary.
5. Fork an implementer subagent. "Implement the refactor based on this plan."
6. Implementer balloons to 80k tokens internally. Show this in the background panel.
7. Implementer returns. Main session gains 800 tokens.
8. Fork a verifier subagent. "Run the tests and verify the refactor works."
9. Verifier returns clean.
10. End the session. Show the main session is at 25k tokens after a full refactor that would normally have consumed 200k.

The viewer should see the contrast. Same work. Wildly different context economy.

---

## Key Insight

> When you stop putting work into your main session, your main session stops getting dumb. Forks are how you offload work without losing continuity.

---

## What Changes For You

Your sessions get longer. Your output gets sharper. You stop dreading the moment the model starts getting worse. You stop having to compact or restart sessions.

The cost is one habit change. Before you do anything that would put noise into your main session, ask "could a fork do this and just give me the summary?" The answer is almost always yes.

That single question, asked twenty times a day, changes how the model behaves for you. The session you used to lose at 4pm stays sharp until midnight. Because the session was never doing the work in the first place.
