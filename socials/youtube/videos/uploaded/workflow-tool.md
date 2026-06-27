---
tags: [youtube, script, claude-code]
date: 2026-05-22
youtube-id: c0gVowvMR-g
youtube-title: "Anthropic Just Dropped the Update Everyone's Obsessed With: Dynamic Workflows"
published: 2026-05-22
duration: "15:10"
views: 45355
likes: 996
comments: 133
status: uploaded
fetched: 2026-06-27
revenue: 1250
revenue-lift: 0
revenue-utm: 866
revenue-sessions: 10
revenue-method: "3-day time-proximity"
revenue-fetched: 2026-06-27
---

## Video Plan: "The Orchestration Tax" (Claude Code Workflow Tool)

| # | Title | Formula |
|---|-------|---------|
| 1 | **"Claude Code Can Now Run a Whole Team of Itself"** | Bold claim + personification |
| 2 | **"Claude Code's Hidden Tool Runs 1,000 Agents From One File"** | Bold claim + specificity |
| 3 | **"Claude Code Has a Tool You Have to Switch On Yourself"** | Curiosity gap + exclusivity |

**Coined term:** the orchestration tax
**Format:** single-feature deep dive, ~11:30
**Pitch:** cohort workshop (soft anchor ~1:30, urgency close)
**Backbone analogy:** the model as an improvising manager you can fire and replace with a written plan
**Note:** "the orchestration tax" is the working angle. The Problem and old-workaround sections are framed around a job you already run, implement then review then fix, that Claude manages for you today.

---

### Hook (0:00-0:30)

*Open on screen: the `/workflows` view live, a tree of agents lighting up green one after another. No talking head yet, just this for three seconds.*

So Anthropic just released workflows inside of Claude Code.

You write one file, and that file can spin up a whole fleet of Claude agents, dozens of them, hundreds of them, and coordinate the entire thing from start to finish.

But the fan-out isn't actually the interesting part. Subagents already existed. The interesting part is what's doing the coordinating. Because for the first time, it isn't Claude. It's code. And once you see why that matters, you can't unsee it.

---

### The Problem: the orchestration tax (0:30-1:30)

So here is the problem, and if you already use Claude Code seriously, you have felt this even if you never put words to it.

You almost certainly have a job you run over and over. Mine is this. Implement a feature, review it, fix what the review found, then review it again. You have one too. Maybe it is research something, verify it, then write it up. And at some point you got tired of typing it out every time, so you packaged it. You turned it into a skill, or you wired it up as three or four subagents, and now you just say "go."

And that works. But look at who is actually running it. Claude is. Claude is the manager.

*On screen: a 4-step job board, with a single Claude box labelled MANAGER standing over it.*

And being the manager is a whole job on its own. Claude has to decide what runs next. It has to take the output of step one and feed it into step two. It has to hold every half-finished result in its head while it waits. None of that is the actual work. It is pure coordination. And because it is the model doing the coordinating, every one of those decisions is a model call. Tokens spent producing nothing.

I call this the orchestration tax. It is the price you pay for letting the model run the project instead of just doing the tasks.

*On screen: a token counter ticking up on the MANAGER box while nothing visible gets done.*

And the tax has two more costs that are easy to miss. The first is visibility. While Claude is managing, you are watching a wall of text scroll past, and you genuinely cannot tell which step it is on right now. The second one is worse. Because the manager is a language model, it improvises, so the same job goes a little differently every run. And the longer it runs, the more its own context fills up, and the worse it gets. You told it at the start to use four subagents. Forty minutes in, context full, it quietly forgets, and just starts doing the work itself.

---

### Sponsor / soft anchor (1:30-2:05)

Quick word before I show you the fix, from this video's sponsor, which is me.

I run a live cohort workshop on exactly this. Going from using Claude Code casually, to actually engineering agent systems that run themselves. It's hands-on, it's live, and because it's a cohort, there is a real sign-up deadline. Doors close on **[SIGN-UP DEADLINE]**. If the phrase "orchestration tax" just made something click, that workshop is where we go deep on it. Link is in the description.

Okay. Back to it.

---

### The old workaround (2:05-3:10)

So how do you actually get rid of the orchestration tax? Let me show you what people have tried, because I tried both of these myself.

The first one you already know, because it is the setup we just described. Subagents. And subagents do genuinely help with one piece of this. Each subagent gets its own clean context window, does its job, reports back, and its mess does not pile up in your main conversation. That part is real. That is why you reached for them.

But spawning a subagent does not remove the manager. It just means the manager is still Claude. And here is the part that actually costs you.

*On screen: subagent A finishes; its result travels up into the Claude MANAGER box; the tax meter clicks. Claude passes it down into subagent B; B finishes; back up through Claude; the meter clicks again; down into C. Every join lights up the meter.*

Every handoff goes through Claude. Subagent one finishes, and its result has to travel back up through the manager, get read, get thought about, and then get passed down into subagent two. That is a model call. Every single arrow between your subagents is the orchestration tax being charged again. Four subagents is not one tax. It is a tax at every join between them. The more you fan out, the more you pay.

The other thing people try is leaving Claude Code altogether. You write a bash script that calls Claude on the command line, over and over. And yes, now your control flow is real code. But it is clunky. Every one of those calls is a cold start. They share nothing. There is no live view, no record of what happened, and no way to resume a half-finished run.

So you have got two options, and neither one is good. Let the model orchestrate, and pay the tax at every handoff. Or duct-tape it together from the outside, and lose everything that made Claude Code nice in the first place.

The Workflow tool is Anthropic saying, what if you did not have to choose.

---

### What the Workflow tool actually is (3:10-4:00)

So here's the idea, and it's genuinely simple once it clicks.

A workflow is a single JavaScript file. You write it once. Or honestly, you get Claude to write it for you. And that file is the manager. The coordination, which subagent runs, in what order, in parallel or one after another, what happens to all the results, every bit of that is now plain JavaScript code.

And then there is one special function you can call inside that file. It's called `agent`. Every time your code calls `agent`, it spawns one fresh Claude subagent, with a clean, empty context window, to do exactly one task. It runs, it hands back just its result, and then its context is thrown away.

So the model still does all of the actual thinking. But the model is no longer the manager. The code is the manager. And that single move is what kills the orchestration tax.

---

### What a workflow actually looks like (4:00-6:45)

So let me actually show you one, because they are smaller than you would expect. And I want to use the exact job from the start of this video, the one Claude keeps fumbling. Implement a feature, review it, fix it, review again.

*On screen, build the basic example up a few lines at a time:*

```js
export const meta = {
  name: 'implement-and-review',
  description: 'Implement a feature, then loop review-and-fix until it passes',
}

// step one: implement the feature
await agent(`Implement ${args}. Make the change in the codebase.`)

// step two: review what step one just did
let review = await agent(
  `Review the uncommitted changes for ${args}.`,
  { schema: REVIEW }   // forces a clean { passed, issues } object back
)
```

At the very top, every workflow has a block called `meta`. Just a name and a one-line description. It is the label on the tin.

Everything underneath is the body, and the body is plain JavaScript. This is where you orchestrate.

Step one calls `agent`. That spawns one fresh Claude subagent, clean empty context, and tells it to implement the feature. Step two calls `agent` again to review what step one just did. And look at the handoff. The review comes back into an ordinary variable, `review`. It is just data now. There is no manager in the middle reading it and deciding what to do, the code already knows what comes next.

One quick thing on that second call. I am handing it a `schema`. That just forces the review agent to answer in a fixed shape. Did it pass, yes or no, and a list of issues. Which means on the very next line, I can check `review.passed` in plain code.

And that is the move. Once the answer is data, the next part is just ordinary programming.

*On screen: the loop wraps around the file.*

```js
let round = 0
do {
  round++
  review = await agent(`Review the changes for ${args}.`, { schema: REVIEW })

  if (review.passed) break                  // good enough, stop

  await agent(`Fix these issues:\n${review.issues.join('\n')}`)
} while (round < 3)                         // otherwise go around again, 3 times max
```

That is a real loop, in real JavaScript. It reviews. If the review passed, it stops. If it did not, it fixes the issues it was just handed, and goes around again, up to three times. `if`, `do while`, a counter, all the normal stuff. It all just works, because a workflow file is real code.

And this is the whole point of the video, sitting in about eight lines. That loop is not a polite instruction to Claude that it might forget once its context is full. It is code. It runs every single time, the same way, on round one and a thousand workflows deep. The model cannot forget to review, because reviewing is not the model's decision anymore. It is the file's.

Now let me show you what a bigger one looks like, because this is where the rest of the toolkit shows up.

*On screen, reveal the complex example section by section:*

```js
export const meta = {
  name: 'review-branch',
  description: 'Review the branch across dimensions, verify each finding',
  phases: [{ title: 'Review' }, { title: 'Verify' }],
}

// structured output: each reviewer must return findings in this exact shape
const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: {
    type: 'object', required: ['title', 'file'],
    properties: { title: { type: 'string' }, file: { type: 'string' } } } } },
}
const VERDICT = {
  type: 'object', required: ['isReal'],
  properties: { isReal: { type: 'boolean' }, reason: { type: 'string' } },
}

const DIMENSIONS = [
  { key: 'bugs',  prompt: 'Find logic bugs in the changed files on this branch.' },
  { key: 'perf',  prompt: 'Find performance regressions in the changed files.' },
  { key: 'tests', prompt: 'Find missing test coverage in the changes.' },
]

const results = await pipeline(
  DIMENSIONS,
  // stage 1: review one dimension
  d => agent(d.prompt, { phase: 'Review', schema: FINDINGS }),
  // stage 2: verify every finding from that review, in parallel
  review => parallel((review?.findings ?? []).map(f => () =>
    agent(`Try to refute this finding: ${f.title} (${f.file})`,
          { phase: 'Verify', schema: VERDICT })
      .then(v => ({ ...f, verdict: v })))),
)

// keep only the findings that survived verification
const confirmed = results.flat().filter(Boolean).filter(f => f.verdict?.isReal)
return { confirmedCount: confirmed.length, confirmed }
```

This one reviews a whole code branch. It uses pretty much the rest of the toolkit, so let me walk the new pieces as they show up.

First, `phase`. You will see `phase` labels dotted through it. That is just labelling. When this runs, you get a clean little tree of what is happening, grouped into a Review phase and a Verify phase. Remember the visibility problem from earlier, not being able to tell what step Claude was on? This is the fix. You watch the phases light up live.

Second, `schema`, which you already met in the basic example. Here it is doing more work. Every reviewer is handed the `FINDINGS` schema, so it cannot ramble. It has to hand back a clean list of findings, each one an object with a title and a file. Structured data in, structured data out.

Third, `parallel` and `pipeline`, and this is the important pair. `parallel` runs a batch of agents at the same time and waits for all of them. `pipeline` is the cleverer one. It runs each item through a series of stages, and the moment one item clears a stage, it moves straight on to the next, while the others are still behind it. So here, the second the "bugs" review finishes, its findings start getting verified, while the "performance" dimension is still being reviewed. And inside that, each batch of findings gets verified with `parallel`. Nothing sits idle.

*On screen: the pipeline animation, items advancing independently, no barrier between stages.*

And notice what is happening to the data. A reviewer returns findings. Those findings flow straight into the next stage as its input. There is no model in the middle reading them and deciding what to do. The code already knows. Findings go to verifiers, verified results get filtered down to the real ones, and the workflow returns one clean object at the end.

Fourth, and this one is easy to miss, you can pick the model per agent. Every `agent` call takes a `model` option. So you run the cheap, mechanical agents on Haiku, and you save Opus for the one step that actually needs the judgement. I have an outreach workflow, linked below, that does this. The agent that just reads a file of leads, and the agents that go and research each lead, all run on Haiku. Only the agent that writes the actual personal message runs on Opus. You stop paying top-tier prices for the boring parts of the job.

*On screen: the three phases of the outreach workflow, each tagged with its model — Haiku, Haiku, Opus.*

So that is the toolkit. `agent` to spawn a worker. `parallel` and `pipeline` to shape the flow. `schema` for structured handoffs. `model` to put each task on the right-sized model. `phase` and `log` for the live view. There is a little more, there is a `budget` for token-aware loops, and you can even nest one workflow inside another. But that handful is ninety percent of what you will ever use.

---

### The pro move: determinism, resume, and caching (6:45-8:15)

Now I want to come back to one thing, because this is the part that genuinely surprised me.

Everything I just showed you, the orchestrator, the `parallel`, the `pipeline`, all of that logic, it runs for free. It spends zero tokens. The model is never once asked "what should we do next," because the next step is just the next line of code. The model only ever gets called for the actual work, inside the `agent` calls.

So you are not just reducing the orchestration tax. You have deleted it.

*Pause. Let that land.*

And because the orchestration is now fixed code, instead of a model improvising, you get something I have not seen anywhere else. Workflows can resume.

Think about what determinism buys you. If the same script always runs the same way, the runtime can remember what it already did. So if your workflow falls over forty minutes in, you just run it again, and every step that already finished comes straight back from cache, instantly. It does not redo them. It picks up from exactly where it died.

*On screen: a run resuming, finished steps flashing green instantly, new work starting from the failure point.*

And it gets better. Say you have got a five-stage workflow and stage four had a bad prompt. You fix stage four, re-run, and stages one, two and three replay from cache, for free. Only stage four onward actually runs again. You are editing a live pipeline and only paying for the part you changed.

This is also why, inside a workflow, there are a few strict little rules. You cannot call random. You cannot ask for the current time. Because those would make two runs come out different, and that would break resume. The whole thing is engineered to stay deterministic.

And a couple of guardrails. One workflow can spawn up to a thousand agents in total, and it runs somewhere around ten to sixteen of them at once. The script itself is capped at half a megabyte. You will not hit these by accident. They are there so a runaway loop cannot quietly spawn ten thousand agents and drain your account overnight.

I am keeping this part deliberately high level, because determinism and resume honestly deserve a video of their own. For now, just hold onto the headline. The orchestration is code, the code is free, and because it is code, it can pick up exactly where it left off.

---

### The deeper point: a workflow is the inverse of a skill (8:15-9:30)

So here's the thing I kept turning over in my head.

We already have skills in Claude Code. And on the surface, a skill and a workflow sound like the same thing. They are both a reusable, packaged procedure. So when would you ever build one instead of the other?

And I think the cleanest way to put it is this. A workflow is the inverse of a skill.

*On screen: two columns, SKILL on the left, WORKFLOW on the right, built up one line at a time.*

A skill is a set of instructions you hand to Claude, and Claude decides how to carry them out. You are encoding what you want. The model stays in charge of the how. It is flexible, it adapts, and it is a little bit different every single time.

A workflow is the opposite. You encode the how. The exact orchestration, written as code. And the model is only allowed to fill in the small pieces, inside the `agent` calls. The structure is locked. It is rigid on purpose, and it is identical every time.

So it is not a question of which one is better. It is a question of who you want in charge of the plan. A skill says, "Claude, you handle it." A workflow says, "no, I will handle the plan, you just do the tasks."

And once you see it that way, you start to notice that this is where the whole industry has been heading. The serious agent frameworks, the LangGraphs of the world, they all converged on the same realisation. You do not want a language model improvising your control flow. You want the control flow to be a fixed graph, and you want the model to be the thing that fills in each node. The Workflow tool is just Anthropic baking that idea directly into the terminal, where you already work.

---

### What this means for you (9:30-10:30)

So, practically. What do you do with this.

First, you have to turn it on. Like I said, it is off by default. You set an environment variable, `CLAUDE_CODE_WORKFLOWS` equals one, and that is a hard requirement. No variable, no tool. Once it is on, you also get a slash command, slash workflows, which is a live view. A little tree of every agent that is running, so you can watch the whole thing happen in real time.

Second, when should you actually reach for one. Not for everything. If it is a one-off task, just let Claude do it, or spawn a single subagent. A workflow earns its keep when the job is repeatable, when it fans out across a lot of agents, and when you would genuinely want the option to resume it. Code review across a big branch. Research across twenty sources. Auditing every file in a folder. That is the sweet spot.

And third. You do not actually have to learn the JavaScript format yourself. Because this tool is not documented yet, I took everything I worked out about it and packaged it into a skill. You point Claude at the skill, you describe the job in plain English, and it writes you a correct, runnable workflow file. Templates, the rules, a built-in validator, all of it. I will put that in the description, so you can just install it and skip straight to the good part.

---

### Close (10:30-11:30)

So that is the Workflow tool.

The real shift here is not the fan-out. It is that you stop letting the model be the manager. You write the plan as code. The plan runs for free, and it runs the same way every time. And the model goes back to doing the one thing it is genuinely brilliant at, which is the work.

And honestly, that shift, going from someone who chats with Claude Code, to someone who designs systems that Claude Code runs for them, that is the entire jump I am trying to get people to make.

That is what the cohort workshop is. It is live, it is hands-on, and we go from the fundamentals all the way through to building agent workflows that run themselves while you are not even at the desk. Because it is a live cohort, there is a real sign-up deadline. Doors close on **[SIGN-UP DEADLINE]**, and once that cohort starts, that is it until the next one.

If this video made the orchestration tax click for you, the workshop is where you actually learn to engineer your way out of it. Link is in the description. Go and take a look before the deadline closes.

I will see you in the next one.

---

## Production notes

**Placeholders to fill before recording:**
- `[SIGN-UP DEADLINE]` — appears twice (soft anchor + close). Drop in the real cohort sign-up date.
- Optional: a line of social proof in the soft anchor once the cohort has a track record. Left out deliberately rather than invented.

**Open decision:**
- "The orchestration tax" is the working angle and the Problem and old-workaround sections are now built on it. If the angle changes, the Hook and Problem sections get rewritten and the coined term re-threaded. The feature walkthrough, the examples, and the determinism section carry over to any angle.

**Two example files to screen-record:**
- `implement-and-review` — the basic example. Implement once, then a `do/while` loop of review and fix. The on-screen version is trimmed for teaching; the full runnable file is `.claude/workflows/implement-and-review.js`.
- `review-branch` — the complex example. Phases, schema, parallel, pipeline. Full runnable file at `.claude/workflows/review-branch.js`.
- Both should be shown running with the `/workflows` tree visible.

**Pacing (from improvements.md):**
- Deliver ~50% slower than a typical AI tutorial. Let every on-screen file or diagram linger 2-3 seconds after it is referenced.
- Keep the natural pauses, especially the one marked after "you have deleted it."
- Use progressive reveal for both example files and the SKILL vs WORKFLOW columns. Build them up, do not flash a finished slide.

**Visuals checklist:**
- 0:00 cold-open on the live `/workflows` tree (visual hook in the first 10 seconds).
- MANAGER box standing over a 4-step job board, token counter ticking up, for the orchestration-tax beat.
- The subagent-handoff diagram: each result travelling up through the MANAGER and back down into the next subagent, the tax meter clicking at every join.
- Basic example (`implement-and-review`) built up a few lines at a time, then the complex example (`review-branch`) section by section.
- Pipeline animation with no barrier between stages.
- The outreach workflow's three phases tagged with their models — Haiku, Haiku, Opus.
- A real resume: cached steps flashing green instantly.
- Two-column SKILL vs WORKFLOW build.

**Structure check against the formula:**
- 3-beat hook structure ✓  — but the spoken opening ("So Anthropic just released workflows") is announcement framing; the formula wants discovery framing ("I noticed something..."). Flagged for a rewrite when the hook is finalised.
- Coined term ("the orchestration tax") named early, threaded through, used in the close ✓
- Problem → old workaround (subagents / bash) → new solution triple ✓
- Single feature, concept-first, real internals, basic-then-complex example walkthrough ✓
- Pro material (determinism, resume, caching) kept as a clearly-flagged later beat ✓
- "Ray thinks deeper": inverse-of-a-skill insight + broader-trend (LangGraph) ✓
- Soft anchor ~1:30, urgency close tied to the topic, one pitch system only ✓
