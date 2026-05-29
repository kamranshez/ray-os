---
tags: [youtube, script, claude-code]
status: draft
date: 2026-05-29
---

## Video Plan: "Claude Code Is Now a Recursive Language Model"

**Title options:**

1. **Claude Code Can Now Call Itself** (bold claim + personification)
2. **Claude Code Is Now a Recursive Language Model** (bold claim + specificity)
3. **Anthropic Quietly Turned Claude Code Into a New Kind of Model** (curiosity gap + exclusivity)

**Coined term:** recursive language model
**Format:** thesis / industry take (idea-driven, ~17K view ceiling, RLM threaded as the philosophical anchor)
**Pitch:** Masterclass only (soft anchor ~1:30, urgency close, lifetime price up 100 dollars in one week)
**Backbone analogy:** a senior researcher who never reads the whole library, but writes a plan, sends assistants to read sections, and only reads the summaries that come back
**Demo surface:** the example workflow files plus the live `/workflows` tree, narrated. No project repo on screen.
**Relationship to existing draft:** `workflow-tool.md` ("The Orchestration Tax") attacks the same tool from the coordination-cost angle. This script is the retrieval and recursion angle. Different thesis, different coined term, reuses the example files.

---

### Hook (0:00-0:35)

*Cold open on screen, no talking head: the `/workflows` view live, a tree of agents lighting up green one after another for about four seconds. Then a single line of code highlighted: `await agent(...)` inside a loop.*

So I was deep in a repo last week. A big one. Hundreds of thousands of lines, way more than fits in any context window. And I watched Claude Code do something I had genuinely never seen it do before.

It did not try to read the codebase. It wrote a small program. And that program spawned copies of Claude, dozens of them, each one reading a different slice of the repo and reporting back.

Claude wrote code that called itself.

And once that clicked, I could not unsee what had actually happened here. With one new tool, Claude Code quietly turned into a different kind of thing. Not a chatbot you talk to. A recursive language model. A model that, when the job is too big for its own head, writes a program that runs more copies of itself. Let me show you why that is a much bigger deal than it sounds.

---

### The problem: the job is bigger than the window (0:35-1:30)

*On screen: a single huge block labelled "5,000,000 tokens" next to a small frame labelled "context window" that only covers a sliver of it.*

Here is the problem, and if you have ever pointed Claude at a serious codebase, you have felt this one.

Say you have got five million tokens of context. A large repo, a pile of documents, a year of logs. And you have one specific question you need answered out of all of it.

You cannot just load the whole thing in. It does not fit. And even the parts that do fit are not free. Every token you pour into the window is a token the model now has to pay attention to. So the question is not "how do I get it all in." It is "how do I pull the signal out, without drowning the model in everything else."

And the honest answer, until pretty recently, is that every option you had was a compromise.

---

### Sponsor / soft anchor (1:30-2:15)

Quick word before I get into those options, from this video's sponsor, which is me.

I run the Claude Code Masterclass. Over fifteen hundred engineers have taken it, from companies you have heard of, and a lot of them are now the person their whole team goes to for this stuff, the best Claude Code user at their company. It is lifetime access, one payment, and you get every future update.

One thing on timing. The lifetime price goes up by a hundred dollars one week from now. So if the rest of this video lands for you, the link is in the description, and it is worth a look before that change.

Okay. Back to the problem.

---

### The old way: grep, and why it falls apart (2:15-3:15)

*On screen: a terminal. A `grep` command runs and returns a wall of matches that keeps scrolling.*

So, option one. You search. You grep for the terms you think matter, and you pull the matching lines into context.

And sometimes that is fine. But here is where it falls apart. You do not control how much comes back. You grep for one common function name and suddenly you have got four hundred matches, and all of them just got poured into the window. Now the thing you actually cared about is buried in noise, and the model is making dumber decisions for the rest of the session because its attention is split across four hundred things instead of the three that mattered.

And there is a quieter problem underneath that one. A grep match is a single line, ripped out of its file. You lose the meaning around it. The function that called it, the comment above it, the reason it exists. You got the hit, but you lost the context that made the hit make sense.

So raw search gives you two bad outcomes at once. Too much noise, and not enough meaning.

---

### The better way: subagents, and the noise they bring back (3:15-4:30)

*On screen: a root Claude box spawning three subagent boxes, each labelled with a part of the codebase. Each one explores, then sends a result back up into the root box.*

So the smarter move, and this is what a lot of us landed on, is subagents.

Instead of grepping into your own window, you spin up separate agents. One goes and explores the auth layer. One digs through the database code. One reads the tests. And the trick is, each of them can do the thing grep could not. They can look at the matching line and the wider file around it, get the full meaning, and then hand you back just the part that matters.

And each subagent gets its own clean, empty context window to do that in. So all of that searching, all of that reading, all of that mess, it happens over there, in their windows, not in yours. You stay clean.

That is genuinely good. That is why people reach for subagents.

But there is a catch, and it is the whole reason this video exists.

*On screen: the three subagents all finish, and each one dumps a large block of text back up into the root box, which starts to overflow.*

What comes back? Whatever the subagent decides to send. And a lot of the time, a subagent finishes its little job and rams a big pile of text back into your main window. Half of it you needed. Half of it is padding, restated context, "here is everything I looked at." And now the exact thing you were trying to avoid, a window full of noise, has happened anyway. It just took a detour through three agents first.

The model is still the one deciding what comes back. And the model is generous. It over-returns. So you cleaned up the searching, but you never cleaned up the handoff.

---

### The fix: make the orchestrator code, not the model (4:30-6:15)

*On screen: the root Claude MANAGER box gets crossed out and replaced with a small file icon labelled `workflow.js`.*

So here is the move that changes everything. And it is the new Workflow tool in Claude Code.

What if the thing coordinating all of this was not the model at all. What if it was code.

A workflow is just a single JavaScript file. You write it once, or honestly you get Claude to write it for you. And inside that file there is one special function, called `agent`. Every time your code calls `agent`, it spawns one fresh Claude, clean empty window, to do exactly one task. It runs, it hands its answer back into your code as plain data, and then its context is thrown away.

*On screen, reveal a few lines at a time:*

```js
// spawn a worker to read one slice of the repo
const finding = await agent(`Search the auth layer for ${target}. Return only what matters.`, { schema: FINDING })

// it comes back as data. now YOUR code decides what to do with it.
if (finding.relevant) {
  keep.push(finding)          // worth keeping
}
// if it is not relevant, it never enters your context. it just gets dropped.
```

Look at what just happened. The subagent's answer came back into an ordinary variable. It is data now. And because it is data, your code gets to decide whether it lives or dies. If it is relevant, you keep it. If it is not, you throw it away on the very next line, and it never touches your main window.

That is the piece that was missing. The return is no longer the model being generous. The return is gated by code. Nothing comes back into your context unless your code lets it.

*Pause. Let that land.*

And once the orchestrator is code, you get the entire toolbox that comes with code. You can loop. You can branch. You can break out early. You can run a hundred of these in parallel and only keep the three that came back relevant.

```js
// fan out across the whole repo, keep only the signal
const slices = splitRepo(repo)
const hits = []
for (const slice of slices) {
  const r = await agent(`Read ${slice}. Is there anything about ${target}? Return only that.`, { schema: FINDING })
  if (r.relevant) hits.push(r)      // signal climbs. noise gets dropped right here.
}
return hits
```

This is the thing I want you to really sit with. You have got `agent` calls, which is the model thinking, interleaved with `for` and `if` and `return`, which is plain deterministic code. Thinking, then logic, then more thinking, then more logic. Mixed together, in one file. That mix is the whole unlock.

---

### Why the mix is so powerful (6:15-7:15)

*On screen: two patterns side by side. Left, labelled `parallel`: a row of agents all firing at once. Right, labelled `pipeline`: items flowing through stages, each advancing on its own.*

And the tool gives you real shapes for that mix.

There is `parallel`, which fires off a batch of agents at the same time and waits for all of them. There is `pipeline`, which is the clever one. It runs each item through a series of stages, and the second one item clears a stage, it moves straight on to the next while the others are still behind it. Nothing sits idle.

And here is the part that surprised me most. All of that orchestration code, the loops, the branching, the filtering, all of it runs for free. It spends zero tokens. The model is never once asked "what should we do next," because the next step is just the next line of code. The model only ever gets called for the actual thinking, inside the `agent` calls.

So you are not paying the model to be a project manager anymore. You are only paying it to think. And every piece of thinking happens in a clean window, and only the answers your code chooses to keep ever come home.

That is a fundamentally cleaner, faster, and frankly smarter way to work through more data than any single window could ever hold.

---

### The deeper point: this is a recursive language model (7:15-8:30)

*On screen: the full loop drawn once. A big block labelled "context" sitting outside a frame labelled "the model's window." The model reads a summary, writes a program, the program spawns workers that each read a slice, and only chosen answers flow back.*

So step back, because this is the thing I actually want you to take away.

What is this, really? You have a body of context too big to hold. So instead of holding it, the model keeps it outside itself, and writes a program. That program runs more copies of the same model, each one reading a piece, each one reporting back, and the code decides what is worth keeping.

A model that, faced with a job too big for its own head, writes a program that calls itself.

Researchers recently gave this exact pattern a name. They call it a recursive language model. The idea is simple once you see it. You stop treating context as something you cram into the prompt, and you start treating it as data that lives outside the model, that the model can point at, slice up, and send other copies of itself to go read. The top-level model barely reads the raw data at all. It mostly reads summaries, and orchestrates.

And that word, recursive, is the right one. A function that calls itself is recursion. This is a language model that calls itself. The Workflow tool is the thing that finally makes that practical inside Claude Code.

That is the shift. Claude Code stopped being a single model answering in a single window. It became a model that can spin up a structured tree of itself to handle things no single window could.

---

### Ray thinks deeper: they trained it for this (8:30-9:30)

Now here is the question I kept getting stuck on, and it is the one to sit with.

You could technically spawn subagents a year ago. Parallel agents are not new. Calling a model from a script is not new. So why is this landing now? Why does it suddenly feel like a different kind of model and not just a new button?

And I think the answer is not the tool. I think the answer is the model.

*On screen: three stages, the first two faded, the third bright. [the idea existed] then [the model could not reliably drive it] then [now it can].*

The pieces were always sitting there. What you could not do was get a model to reliably drive a program like this. To write the orchestration code, hold the thread across dozens of agents, and make good judgement calls about what to keep and what to throw away, without losing the plot halfway through. That is not a tooling problem. That is a model capability.

And capabilities like that do not just appear. They get trained. This new generation, Opus 4.8, is very likely trained with exactly this in mind, almost certainly with reinforcement learning, to be good at driving these recursive, code-orchestrated runs. The primitive sat there for a year. The thing that showed up this year is a model that can actually drive it.

So when people argue about whether this is genuinely new, I think they are looking at the wrong layer. The pattern is old. The model that can run the pattern reliably is the new part. And that is the part you cannot fake with a clever wrapper.

---

### Limits and how to turn it on (9:30-10:05)

A couple of honest limits, so you know the edges.

An agent cannot spawn another agent. Only your code does the spawning. A workflow can nest one level deep, not infinitely. And the orchestration is fixed code once it starts, so it is deterministic, which is actually what lets a failed run resume from where it died instead of starting over.

And one practical thing. The Workflow tool is off by default. You turn it on with an environment variable, `CLAUDE_CODE_WORKFLOWS` equals one. No variable, no tool. Once it is on, you get the slash workflows view, that live tree of every agent running, so you can watch the whole thing happen.

I also put together a free one-page cheat sheet of the core patterns, parallel, pipeline, nesting, and the code-gated return trick from earlier, so you do not have to memorise any of it. That link is in the description.

---

### Close / urgency pitch (10:05-11:00)

So that is the real shift. Claude Code is not just a model in a box anymore. It is a model that can write a program that runs more of itself, keep the big context outside its own head, and only pull back the signal. A recursive language model. And it works now because they trained a model that can actually drive it.

If that is the level you want to operate at, going from someone who chats with Claude Code to someone who designs systems that Claude Code runs for them, that is exactly what the Masterclass is for. It is lifetime access, one payment, every future update included.

And I know the obvious worry. Why buy lifetime when in a year there might be a better tool. Honestly, there probably will be. And when there is, you get lifetime access to that class too. That is the whole point of lifetime.

The lifetime price goes up by a hundred dollars one week from now. And in case you are wondering whether it is worth the risk, the refund rate on it is under nought point two percent. People do not ask for their money back.

Link is in the description. Take a look before the price changes.

I will see you in the next one.

---

## Production notes

**Decisions locked (2026-05-29):**
- Format: thesis / industry take. Calibrated for the idea, not a feature tour. View ceiling ~17K, accepted.
- Pitch: Masterclass only. No newsletter, no free-video cross-link.
- Coined term: recursive language model. Named in the hook, defined at 7:15, used in the close.
- Demo surface: example files plus the live `/workflows` tree. No project repo on screen.
- Free artifact: workflow patterns cheat sheet (download link in the description, not a newsletter pitch).

**Placeholders to fill before recording:**
- Price-increase date: "one week from now" is written into the soft anchor and the close. Today is 2026-05-29, so the hard date is approximately 2026-06-05. Confirm the exact date and drop it in if you want a dated callout instead of "one week from now."
- Current lifetime price and the post-increase price: spoken lines only say "goes up by a hundred dollars," which is safe. Add the actual numbers on screen if you want them visible.
- Social proof company names in the soft anchor: "companies you have heard of" is a placeholder. Drop in 1 or 2 real names if cleared.

**Pitch checklist (from promotion-playbook.md):**
- Soft anchor at 1:30 with social proof ("best Claude Code user at their company") and the price-increase deadline. Done.
- Verbatim objection-handler (lifetime vs a better tool next year) in the close. Done.
- Single primary paid CTA (Masterclass), no newsletter stacking. Done.
- Micro-scarcity (100 dollars in one week). Done.
- Refund stat (under 0.2 percent) in the close. Done.
- Named free artifact (patterns cheat sheet). Done, but the cheat sheet needs to be created before publish.

**Verified content notes:**
- "Recursive language model" is the term from recent work by Alex Zhang and colleagues (MIT). Spoken line keeps it light ("researchers recently gave this pattern a name") rather than citing the paper on camera.
- The "trained for it" claim is phrased as "very likely" and "almost certainly with reinforcement learning," not as confirmed fact. Anthropic publicly credits improved long-context and tool-triggering behaviour. Keep the hedge in delivery.
- Limits are accurate: an agent cannot spawn an agent (only the script orchestrates), workflow nests one level, deterministic JS is what enables resume.
- Zero tokens for orchestration code is correct: only `agent` calls cost tokens.

**Pacing (improvements #1 and #7):**
- Deliver about 50 percent slower than a typical tutorial. Let every code reveal and diagram linger 2 to 3 seconds.
- Keep the marked pause after the code-gated return reveal ("nothing comes back unless your code lets it").
- Build both code blocks up a few lines at a time. Do not flash a finished block.
- Keep the screen minimal: no logos, no titles, just the code and the diagrams.

**Visuals checklist:**
- 0:00 cold-open on the live `/workflows` tree, then the single `await agent(...)` line. Visual hook in the first 10 seconds (improvement #2).
- The 5,000,000-tokens block next to a small context-window frame.
- The grep wall of matches scrolling.
- Subagents exploring, then the overflow beat where they dump text back into the root box.
- The MANAGER box getting replaced by `workflow.js`.
- The two code blocks (single gated return, then the for-loop fan-out), revealed line by line.
- The parallel vs pipeline side-by-side.
- The full recursive loop: context outside the window, model writes a program, workers read slices, only chosen answers return.
- The three-stage "why now": idea existed, could not drive it, now it can.

**Structure check against the formula:**
- 3-beat hook, discovery-framed (a thing Ray saw, not an announcement). Done.
- Coined term named early, threaded, used in close. Done.
- Problem then old workaround (grep, then subagents) then new solution (code-gated orchestration). Done.
- Real internals shown (actual code, the toolkit). Done, kept tighter than a full deep dive because this is a thesis cut.
- "Ray thinks deeper": the model-was-trained-for-it argument and the is-this-actually-new debate. Done.
- Philosophical anchor (the RLM thesis) threading the whole video. Done (improvement #6).
- Single pitch system, soft anchor plus urgency close. Done.
