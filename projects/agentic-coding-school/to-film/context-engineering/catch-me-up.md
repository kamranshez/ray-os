---
class: "context-engineering"
chapter: "Advanced Techniques"
status: "scripted"
---

## The Thesis

The biggest unlock from agents in a large codebase is not generation. It is comprehension. And comprehension only happens when you give the agent a **named mode** to explore in, not a vague "tell me about this repo."

Catch Me Up is a skill that does this. Six exploration modes. Each one structured. Each one producing a specific kind of output that loads enough context for you to actually act.

You will use this skill every week. Maybe every day.

---

## The Problem

You clone an unfamiliar repo. You open it. You stare at it.

What do you do?

If you are honest, the first thing you type into Claude is something like "can you explain this codebase to me." And what you get back is a thousand-word summary that sounds plausible, looks structured, and gives you almost nothing you can use. It tells you there is a `src` folder. It tells you the tests are in `tests`. It tells you this is a Node project.

You knew that.

The problem is not the agent. The agent did exactly what you asked. The problem is that "explain this codebase" is the wrong prompt. It is open-ended. It has no constraint. The model has to guess what you actually want, and when models guess, they regress to the mean. The mean is a generic README-shaped summary.

[IMAGE: split screen. Left side shows a vague prompt "explain this codebase" producing a generic bulleted summary. Right side shows "Catch Me Up: architecture mode" producing a sharp dependency diagram]

![[images/catch-me-up/vague-vs-named.png]]

You need to ask a sharper question. And the sharpness is not something you should have to invent each time. It should be the skill itself.

---

## The Core Insight

Catch Me Up is a markdown skill with **six named exploration modes**. You invoke the skill, you pick a mode, and the agent runs that specific exploration for you.

The modes:

- **Architecture.** Where does data flow. What calls what. Which boundaries are real, which are sketches.
- **Conventions.** How does this codebase do naming, error handling, testing, file structure. What patterns are load-bearing.
- **Feature trace.** Pick a single feature. Trace it from the UI down to the database. Tell me every file it touches.
- **Syntax.** What language features and idioms are used here that I might not know. What custom DSLs exist.
- **Testing.** What is tested. What is not. How are tests organized. Where do I start if I want to add one.
- **History.** Who wrote the load-bearing parts. When did the architecture last change. What were the big refactors.

Each mode has a specific output shape. Architecture produces a diagram and a dependency map. Conventions produces a table. Feature trace produces a numbered list of files in execution order. The shape is part of the skill.

This is the move Priscila Andre de Oliveira described at the AI Engineer conference. She built it for herself at Sentry, where she works on a codebase that is fifteen years old and changes by 100 PRs a day. After analyzing 116 of her own Claude sessions she found that 67% of them were comprehension. Two percent were generation.

She built the skill because her comprehension prompts kept repeating. Once you see the pattern, you make the skill. Once you have the skill, you use it for everything.

---

## Why Named Modes Beat Free Form

There is a deeper reason this works, and it is worth understanding.

When you give a model an open-ended task, the first token it produces sets the direction of the entire response. That first token is the most likely continuation of your prompt, which for "explain this codebase" is going to be something like "this" or "the" leading into a generic summary. Once it starts down that path, every subsequent token is the most likely continuation of the previous one. The whole response is locked in by the first word.

When you give a model a **named mode**, you collapse the space of likely first tokens. "Architecture mode" pulls for diagrams, not prose. "Feature trace" pulls for numbered lists, not paragraphs. The mode is a constraint on the output shape, and the constraint propagates through the whole response.

You are not just asking a better question. You are forcing a better answer shape.

[IMAGE: a fan of arrows leaving a single point labeled "explain this codebase", most arrows lead to similar generic blobs. Second image shows arrows leaving "architecture mode", all arrows converge on a tight cluster of diagrams]

![[images/catch-me-up/mode-collapse.png]]

---

## The Two Use Cases

Priscila uses this skill in two situations. They cover most of what a senior engineer actually does day to day.

**Dropping into an unfamiliar repo.** New job, new team, new project, new OSS dependency you have to debug. You run Catch Me Up in architecture mode to get the skeleton, conventions mode to learn how to write code that fits in, and feature trace mode on whatever feature you have been asked to extend. Two hours of work compressed into about ten minutes.

**Loading PR review context.** A colleague tags you on a PR in a part of the codebase you do not work in. You have enough context to half-understand it, not enough to confidently approve. You run Catch Me Up against the files the PR touches. Now you can review.

The second one is the use case nobody talks about. Most PR review videos are about reviewing your own agent's output. This is the opposite. This is about using an agent to load enough context to review a human's work.

Both use cases share the same structure. You need to act in a part of the codebase you do not own. You do not have time to read it all. You need the named mode that gives you exactly the right slice.

---

## Steering Before the Plan

There is one more thing this skill does that nobody else talks about.

The standard agentic loop is **Research, then Plan, then Implement**. Claude Code has a plan mode that bakes this in. The standard story is that you let the agent research, then you approve the plan, then you let it implement.

Priscila's view, which I agree with, is that there is a missing step between research and plan. The agent does research. Before it can plan, **you have to read what it found and correct its mental model**. Not approve. Correct.

This is the step where you catch the agent thinking the codebase uses Redux when it actually uses Zustand. Where you catch it thinking the API is REST when it is actually tRPC. Where you catch it thinking the tests use Jest when half the codebase migrated to Vitest two years ago.

If you skip this step, the plan looks fine. The plan is internally consistent. The plan is also wrong, because it is built on a wrong understanding of the codebase. The agent will implement the plan, the implementation will look fine, and then it will fail in a way that takes you two hours to diagnose.

Catch Me Up is the skill that runs in this gap. Before the plan. After the research. You read what the agent thinks it found. You correct it. Then you let it plan.

[IMAGE: a flow with four boxes labeled Research, Comprehend (highlighted in red), Plan, Implement. The Comprehend box has a caption: "you correct the agent's mental model here"]

![[images/catch-me-up/four-step-loop.png]]

---

## Demo

You will build the skill from scratch on camera. Then run it on a real OSS repo.

1. **Build the skill.** A single markdown file at `~/.claude/skills/catch-me-up/SKILL.md`. Frontmatter with name and description. Body with the six modes, each as a section with a prompt template and an expected output shape.
2. **Clone an OSS repo you do not know.** Use Sentry's `getsentry/sentry` itself, or pick something you actually want to learn. Vite, tRPC, Next.js, whichever you have been curious about.
3. **Run architecture mode.** "Catch me up on how this repo is structured. Use architecture mode." Watch it produce the dependency diagram and the boundary map.
4. **Run feature trace mode on something specific.** Priscila's example, slightly adapted: "Catch me up on how this repo's test infrastructure works. Use feature trace mode. Does it simulate envelopes, or does it intercept real ones?" The fact that the prompt asks a sharp question inside the mode is the key. Modes work best with a specific question, not a vague one.
5. **Run conventions mode before writing any code.** This is the step that determines whether the code you add will look like it belongs.
6. **Show the steering moment.** After the model produces its understanding, deliberately catch it being wrong about one thing. Correct it. Then ask it to plan based on the corrected understanding. Show how the plan changes.

The demo lands because the viewer can clone the same repo, install the same skill, and reproduce every step.

---

## Key Insight

> Comprehension is a skill, not a prompt. Give the agent a named exploration mode and an expected output shape, and you get a slice of the codebase you can act on. Run it before every plan. Run it for every PR review. The biggest unlock in a large codebase is not generation. It is the ten minutes you spent loading the right context before you started.

---

## Closing

You will write this skill once. You will use it for the rest of your career. Every new repo, every PR review, every onboarding, every "wait how does this part work" moment runs through the same six modes.

The skill is twenty lines of markdown. The leverage is permanent.

**See also:** [[quality-quarter]] is the prerequisite. Catch Me Up only produces clean summaries from clean code. [[self-instrumentation]] is the thing that will tell you, after a month of using this skill, which mode you reach for most and which mode you can probably delete.
