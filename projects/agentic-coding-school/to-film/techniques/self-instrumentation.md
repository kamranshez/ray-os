---
duration: "10-14 min"
batch_name: "Techniques"
class: "techniques"
chapter: "Advanced Techniques"
---

## The Thesis

You do not know what you use Claude Code for.

You think you know. You would describe yourself as someone who uses it to write code, refactor things, debug. That is the story you tell when somebody asks. It is also wrong.

The way to find out the real answer is to feed your own Claude Code transcripts back to Claude and ask it to classify them. The data has been sitting on your disk the whole time. You just have not read it.

This video is about how to do that, what you will find, and what to do once you find it.

---

## The Problem

Priscila Andre de Oliveira, a senior engineer at Sentry, ran exactly this experiment on her own work. She fed 116 of her recent Claude Code sessions into Claude and asked for a classification.

Her expectation, roughly: lots of code generation, some debugging, occasional refactoring.

The actual result: **67% comprehension. 2% code generation.** The rest split across modification, process, review, and other.

She had spent months thinking of herself as someone who used AI to write code. She was actually using AI to read code. The gap between her self-image and her actual behavior was the thing she had been missing every time she sat down to think about which skills to build.

This is the trap. You build skills based on what you think you do. The skills that would actually help are for the things you do without noticing.

[IMAGE: split chart. Left side labeled "What you think you do" shows code generation as the biggest slice. Right side labeled "What you actually do" shows comprehension as the biggest slice, generation tiny]

![[images/self-instrumentation/expected-vs-actual.png]]

---

## The Core Insight

Claude Code already logs everything. Every prompt, every response, every tool call, every file read, every subagent dispatch. It writes them as JSONL files to:

```
~/.claude/projects/<encoded-cwd>/<session-id>.jsonl
```

One file per session. One line per message. Months of your actual behavior, structured, machine-readable, sitting there unread.

Self-instrumentation is the act of reading your own logs. You feed them back to Claude and ask it questions about yourself.

**This is the highest-leverage prompt you will run all month.** Not because the analysis itself is hard. Because the output is the answer to "what should I build next" expressed as data, not opinion.

---

## The Classification Framework

Priscila used six categories. They are a fine starting point:

- **Comprehension.** "Explain this." "How does this work." "What does this file do."
- **Modification.** "Change X to Y." "Refactor this function."
- **Process.** "Run the tests." "Commit this." "Deploy."
- **Review.** "Is this correct." "Why did this break."
- **Generation.** "Write me a new component for X."
- **Other.** The catch-all.

For a skills-heavy workflow, the six are not enough. Extend with these:

- **Skill invocation patterns.** Which skills do you actually trigger. Which sit there gathering dust.
- **Subagent dispatch.** How often do you fan out vs do it inline. Which subagent types do you use.
- **Tool usage shape.** Read versus Grep versus Bash distribution. Which tools dominate.
- **Session length.** One-shot Q&A versus long work sessions. Where is the bimodal split.
- **Abandonment.** Sessions that ended without a resolution. These are friction points, and they are gold.

The extended categories are where the real signal is. The six-category split tells you what kind of user you are. The skill-and-tool extensions tell you what skill to build next.

[IMAGE: a dashboard mockup showing six pie slices on the left for the basic categories, four bar charts on the right for skill invocations, subagent dispatch, tool shape, and session length]

![[images/self-instrumentation/dashboard.png]]

---

## What You Actually Walk Away With

The point of running this is not to admire the chart. The point is to produce four ranked lists you can act on the same day.

**1. The usage breakdown.** A single pie chart of where your time goes. If yours is 67/2 like Priscila's, your next skill needs to be about comprehension. If it is 50/40 modification and process, your next skill is probably a workflow wrapper.

**2. The repeated prompts.** Cluster your prompts and pull the top twenty most repeated shapes. Every one of those is a candidate for a skill. The heuristic is the same one you have heard before: typed it twice, make it a skill. Self-instrumentation finds the ones you typed twenty times without noticing.

**3. The dead skills.** Cross-reference the skills you have installed against the skills you have actually invoked in the last 30 days. Anything you have not used is dead. Delete it. A skill that does not fire is worse than no skill, because it pollutes the skill-selection layer for every prompt.

**4. The abandoned sessions.** Pull every session that ended without a resolved task. Those are friction points. They are the places Claude Code failed you. Read them. Each one is either a missing skill, a bad prompt pattern you keep falling into, or a tool you should have reached for and did not.

The chart is the reveal. The four lists are the work.

---

## Why This Beats Asking Yourself

You will object that you could just sit down and list out what you use Claude for. You cannot.

Three reasons.

**You forget.** A session you ran on a Tuesday at 10pm three weeks ago is gone. You cannot remember what you asked. The log remembers exactly.

**You round up.** When you describe your usage, you describe the impressive parts. You remember the big refactor, not the eighteen times you asked "wait what does this file do" the day after returning from vacation.

**You cannot count.** You can tell whether you use comprehension more than generation. You cannot tell whether the ratio is 60/40 or 95/5. The shape of the answer changes which skill you build.

Self-instrumentation removes all three. The data is exhaustive, untouched, and counted.

---

## The Loop You Are Building

Run this analysis once and you get a snapshot. Run it monthly and you get a feedback loop.

Each month, you rerun the classification. You see your usage shift. You see which new skills you actually adopted (they appear in the invocation chart). You see which skills you built last month and never used (they belong on the delete list). You see which prompt patterns are emerging as the next skill candidates.

This is the same loop the [[scaling-taste]] video describes for prompt-engineering, applied to your own meta-behavior. You are training a feedback loop on yourself. The data is your transcripts. The output is a smarter skill set every month.

> The hardest part of building skills is knowing which ones to build. Self-instrumentation answers that question with data instead of guesses.

---

## Demo

Film this with your real transcripts. Real numbers. React on camera.

1. **Show where the data lives.** Open `~/.claude/projects/` in a terminal. Show the encoded directory names. Open one JSONL file. Show what a single line looks like, a single tool call, a single response.
2. **Show the classifier skill.** A single markdown skill at `~/.claude/skills/self-instrumentation/SKILL.md`. The prompt: read the last N sessions, classify each turn, count by category, also pull repeated prompts, dead skills, abandoned sessions.
3. **Run it on your own data.** Last 30 days. Show the model reading the JSONL files. Watch the dashboard build.
4. **React on camera.** Do not script the reaction. The whole point of the video is the surprise. Find the gap between your self-image and the chart. Say it out loud.
5. **Pick one repeated prompt and turn it into a skill, on camera.** Show the prompt cluster. Show the skill file. Show it firing the next time you would have typed the prompt.
6. **Pick one dead skill and delete it.** Show the cleanup. The viewer should leave the video with the urge to do both moves the same night.

End on the rerun cadence. "Next month, do it again."

---

## Key Insight

> Your transcripts already know which skill you should build next. The only reason you have not built it is that you have not read them. Self-instrumentation is the thirty-minute prompt that turns months of unread logs into a ranked todo list of skills, deletions, and friction points to fix.

---

## Closing

You will run this once and discover a chart that surprises you. You will build two or three skills the same week from the repeated-prompt list. You will delete four or five skills you thought were useful. You will fix one friction point you had been ignoring.

Then you will put it on a monthly cadence and forget about it, because every month the chart will quietly tell you what to build next.

**See also:** the most common finding from this analysis is that you spend most of your time on comprehension, not generation. The skill that addresses that is [[catch-me-up]]. If your chart shows the codebase is the bottleneck rather than the prompt, the prior video is [[quality-quarter]].
