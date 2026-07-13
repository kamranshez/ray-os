---
duration: "12-16 min"
batch: 1
order: 3
batch_name: "Planning Before Implementing"
class: "techniques"
chapter: "Planning Before Implementing"
status: "scripted"
---

## Stop Accepting the First Correct Answer

Here is the idea this whole video turns on. When you hand Claude a task, it jumps to the first correct-looking answer. One plan, delivered with total confidence. And because it is plausible, you approve it. Not because it was the best option. Because it was the only one you saw.

The fix is a one-sentence change in how you prompt: before the agent commits to anything, make it **show you the distribution**. Fan out subagents that attack the same task from deliberately opposed perspectives, put their disagreement on the table, and pick with your eyes open.

Confidence should not come from how sure the model sounds. It comes from having seen the space of options and knowing why the losers lost.

And here is the part that makes this more than a nice idea: Anthropic already ships this. It is wired into Claude Code's plan mode as the default planning workflow. We are going to pull it out of the binary, see exactly how they do it, and then take the pattern out of plan mode entirely. Because the built-in version is tuned for small everyday tasks, and the interesting wins are everywhere else.

---

## The Problem: The First Plan Anchors You

Ask Claude to plan a feature and it produces something plausible in thirty seconds. Numbered steps, file paths, a testing section. It looks like the answer.

But every task has a whole space of workable plans behind it. Cheap ones, deep ones, ones that sidestep the problem entirely. When you sample once, you get one point from that space, usually the most conventional one, the answer shaped like the ticket.

[IMAGE: dark chalkboard, a wide bell curve labeled "the space of workable plans", one glowing pin dropped at the center peak labeled "the plan you got", the long regions either side shaded dark with faint ghost documents in them and a label "never seen"]

![[plan-with-contrasts-one-draw-1.png]]
![[plan-with-contrasts-one-draw-2.png]]
![[plan-with-contrasts-one-draw-3.png]]
![[plan-with-contrasts-one-draw-4.png]]
![[plan-with-contrasts-one-draw-5.png]]

You have no idea where that plan sits in the space. Was there a version with a tenth of the diff? A version that avoids the fragile module entirely? A version that questions whether the feature should work that way at all?

You cannot know, because you only saw one draw. And once you have read it, you are anchored. Every alternative now gets judged against the accidental first sample instead of on its own merits.

This is not a model quality problem. A smarter model gives you a better single sample. It is still a single sample.

---

## Anthropic Already Ships This

Open up the Claude Code binary and search the strings, and you find that plan mode is not one agent writing a plan. Since December 2025 it has been a five phase workflow, and phase two launches **Plan subagents in parallel, each assigned a different perspective on the task**. Not an experiment. Not a beta flag. It has shipped in every release since.

The prompt tells the orchestrator to generate perspectives dynamically, and it ships three worked examples, verbatim from the binary:

- **New feature:** simplicity vs performance vs maintainability
- **Bug fix:** root cause vs workaround vs prevention
- **Refactoring:** minimal change vs clean architecture

[IMAGE: dark chalkboard, five phase pipeline left to right labeled Explore, Multi-Agent Plan, Review, Final Plan, Exit; the second phase node fans out into three small agent figures each with a speech bubble labeled simplicity, performance, maintainability, then converges back into the pipeline]

![[plan-with-contrasts-plan-mode-internals-1.png]]
![[plan-with-contrasts-plan-mode-internals-2.png]]
![[plan-with-contrasts-plan-mode-internals-3.png]]
![[plan-with-contrasts-plan-mode-internals-4.png]]
![[plan-with-contrasts-plan-mode-internals-5.png]]

So when people tell you multi-perspective planning is overkill, the counterargument is sitting in the shipped product. And two details from the binary's history tell you how much Anthropic believes in it.

First, they tuned it rather than killed it. The contrasts shipped four way in November 2025, and two weeks of production data trimmed each one to three. Four was more than it was worth. Three survived. When a company that pays for every token keeps three parallel planning agents after a cost pass, that is the signal.

Second, the full fan-out is a premium feature. The agent count is three on Max 20x, Team, and Enterprise plans, and one everywhere else, and the perspectives only fire when there is more than one agent. So if you have watched plan mode and never seen it fan out, you are not imagining it. By the end of this video you will be running the version Anthropic reserves for its biggest customers, by hand, on any plan, with better contrasts than the autopilot picks.

Because even at full strength, the built-in version is deliberately the small version. Three limits.

**Claude picks the perspectives itself.** It gets that one-line hint in its prompt and improvises from there. It does not know your deadline, your team, or which module is radioactive. The contrasts it picks are generic by construction.

**It synthesizes silently.** The subagent plans get merged into one recommendation before you see anything. Plan mode will ask you clarifying questions about requirements, but it never shows you the alternatives it considered and discarded. You get a veto on the final plan, not a choice between plans. The disagreement between the perspectives, which is the most valuable thing the fan-out produced, is gone before it reaches you.

**It only lives inside plan mode.** It fires for implementation plans, at whatever strength your tier allows. The pattern itself generalizes to any decision you would hand an agent, but the built-in version will never follow you there.

For small tasks, autopilot is exactly right. You do not want a tradeoff interview to rename a function. But the moment the stakes are real, you want to take this pattern off autopilot: choose the contrasts yourself, keep the disagreement visible, and put yourself back in the loop. That is the rest of this video.

---

## The Technique: Fan Out, Compare, Interview

Three moves.

**Move one: fan out.** Before any plan gets written, spawn two or three subagents in parallel. Each gets the same task and a different perspective. A perspective is not a mood. It is an instruction about **which region of the plan space to search**. One agent digs where the cheap plans live, one where the durable plans live, one where the plans that question the task live.

[IMAGE: dark chalkboard, the same wide bell curve from earlier, but now three small agent figures standing at three different regions of the curve, each holding up a flag pin: one near the peak labeled "conventional", one on the left tail labeled "cheapest", one on the right tail labeled "question the task"]

![[plan-with-contrasts-sampling-1.png]]
![[plan-with-contrasts-sampling-2.png]]
![[plan-with-contrasts-sampling-3.png]]
![[plan-with-contrasts-sampling-4.png]]
![[plan-with-contrasts-sampling-5.png]]

This is why perspectives beat rerolling. Resample the same prompt three times and you mostly get the same peak three times. A perspective is how you force the draw into a different region.

**Move two: compare.** The main agent collects the plans and builds a contrast, not a summary. What each approach optimizes for, what it gives up, roughly how big the diff is, what breaks if the assumption behind it is wrong. The disagreement stays visible. That disagreement is the product.

**Move three: interview.** This is where you break hardest from the autopilot, and it is the move that matters most. Instead of merging the plans and recommending a winner, the agent puts the named, costed alternatives in front of you and asks concrete questions. Is the latency target hard or soft? Can this data be five minutes stale? Is anyone else touching this module this sprint? Your answers eliminate options. Then it recommends.

[IMAGE: dark chalkboard, three panel loop: panel one shows one task node fanning into three agent figures each holding a different shaped plan document, panel two shows the three documents side by side on a comparison board with tradeoff arrows between them, panel three shows a question mark speech bubble pointing at a person icon and one document getting a checkmark]

![[plan-with-contrasts-fan-compare-interview-1.png]]
![[plan-with-contrasts-fan-compare-interview-2.png]]
![[plan-with-contrasts-fan-compare-interview-3.png]]
![[plan-with-contrasts-fan-compare-interview-4.png]]
![[plan-with-contrasts-fan-compare-interview-5.png]]

Why interview instead of recommend? Because the tiebreaker between good plans is almost never in the codebase. It is in your head. Whether the deadline is real, whether the workaround is politically acceptable, whether you will still own this code in six months. The model cannot read that. It has to ask.

And the objection forming in your head right now, "you just tripled my planning cost": the agents run in parallel, so the wall-clock cost is roughly one plan. The token cost triples. Planning tokens are a rounding error next to one wrong implementation.

---

## What Actually Changes in Your Prompting

Concretely, this is a one-sentence habit. Take a security vulnerability. The reflex prompt:

> There's a SQL injection in the export endpoint. Fix it.

That gets you the center of the distribution: parameterize the query, ticket closed. Correct, and decided for you before you ever saw a choice.

The distribution version:

> There's a SQL injection in the export endpoint. Before fixing anything, launch three Plan subagents in parallel: one patches the vulnerability directly, one asks whether this endpoint and its attack surface should exist at all, one assumes any patch will eventually be bypassed and plans a second layer that catches it. Show me what each costs and protects against, then interview me before recommending.

One extra instruction. And here is the honest part: **you will often still pick the patch.** That is fine. The point was never that the first answer is usually wrong. It is that before, you were hoping it was right, and now you know why it is right, because you watched the alternatives lose on their merits. Same diff, completely different level of confidence. And every so often, the agent told to question the endpoint comes back with "this export has had zero calls in six months, delete it", and that is the day the habit pays for itself.

---

## The Contrast Library

The technique lives or dies on picking real contrasts. Here are six task types with contrasts that force genuinely different plans. The first three are Anthropic's own, straight from the binary. The next three are where this starts earning serious money.

**New feature:** simplicity vs performance vs maintainability. The simplicity agent writes the smallest thing that works. The performance agent designs for the load you might have. The maintainability agent designs for the engineer who inherits it. Three real plans, three different diffs.

**Bug fix:** root cause vs workaround vs prevention. One agent traces the actual defect. One patches the symptom so you can ship today. One asks how this class of bug gets caught automatically next time. You often want two of the three: workaround now, root cause this week.

**Refactoring:** minimal change vs clean architecture. The tension between "touch as little as possible" and "leave it the way it should have been built". Neither is always right, and you will not know which until you see both diffs sized up.

**Performance work:** better algorithm vs caching vs do less work at all. That third perspective is the sleeper. The algorithm agent optimizes the query. The caching agent memoizes it. The third agent asks why you are computing this for every user on every page load when four percent of them scroll down far enough to see it. When that agent wins, it wins by an order of magnitude.

[IMAGE: dark chalkboard, three agent figures attacking the same large block labeled "the slow thing": first agent reshaping the block with a wrench, second agent standing behind a smaller copy of the block labeled cache, third agent simply crossing out three quarters of the block with a big X]

![[plan-with-contrasts-do-less-work-1.png]]
![[plan-with-contrasts-do-less-work-2.png]]
![[plan-with-contrasts-do-less-work-3.png]]
![[plan-with-contrasts-do-less-work-4.png]]
![[plan-with-contrasts-do-less-work-5.png]]

**Security fix:** patch the vuln vs remove the attack surface vs defense in depth. You saw the prompt already. The reason it needs three agents is that a single agent reliably plans the patch, because that is what the ticket says. The alternatives show up as a throwaway sentence at the bottom, if at all. Never as a costed plan you can hold next to the patch and compare.

**Unfamiliar or legacy code:** follow the existing pattern even if it's bad vs introduce the better pattern locally vs isolate it behind a boundary. This is the contrast for every codebase you did not write. Consistency with a bad pattern versus a local island of good code versus wrapping the whole mess so nothing new touches it. Three defensible answers, and the right one depends entirely on how long that code has left to live. Which is exactly the kind of thing the interview step should ask you.

---

## What Makes a Contrast Real

One rule decides everything here. A perspective is an instruction about where in the plan space to search. A **real contrast sends the agents to different regions. A fake contrast sends them all to the same spot wearing different name tags.**

Take "correctness vs speed". Sounds like a contrast. It is not, because no agent will ever hand you a plan it believes is broken. Tell one agent "prioritize correctness" and another "prioritize speed" and both come back with a correct plan, probably the same one, because correctness is not a region of the space. It is the entry fee for every region. You paid for two agents and bought one plan twice.

Same with "thorough vs pragmatic". Those are adjectives about tone. They change how the plan is written, not what the plan does.

[IMAGE: dark chalkboard, split panel: left side labeled fake contrast shows the bell curve with two agent figures wearing different name tags both standing on the exact same center point; right side labeled real contrast shows the same curve with the two agents standing on clearly separated regions, each with their own distinct document]

![[plan-with-contrasts-fake-vs-real-1.png]]
![[plan-with-contrasts-fake-vs-real-2.png]]
![[plan-with-contrasts-fake-vs-real-3.png]]
![[plan-with-contrasts-fake-vs-real-4.png]]
![[plan-with-contrasts-fake-vs-real-5.png]]

So here is the test, and it takes five seconds: **imagine each agent's finished diff. If the diffs would be the same, the contrast is fake.** The patch agent and the remove-the-endpoint agent touch different files. The caching agent and the do-less-work agent touch different files. Different regions, different diffs, real contrast.

One more thing, because it looks like failure and is the opposite. Sometimes agents sent to genuinely different regions come home with the same plan anyway. That is not a wasted run. Converged because the contrast was fake, you learned nothing. Converged despite a real contrast, that is the strongest confidence certificate you can get. Three searches from opposed starting points landed on the same answer. Ship it.

Where do real contrasts come from? From decisions the task genuinely leaves open. How deep to intervene: workaround, local fix, structural fix, rewrite. Where to intervene: at the source, at the boundary, or at the caller. When: mitigate now versus prevent forever. And the one nobody gives their agents: whether to change the code at all, versus changing the requirement or the environment. If two reasonable engineers could argue about it in a design review, it is a region boundary, and it will survive the diff test.

The six contrasts above are the ones you will use weekly. There are contrasts for migrations, incidents, schema changes, dependency upgrades, scaling, test strategy, and a dozen more. Full catalogue on screen now, screenshot it.

[IMAGE: dark chalkboard, large reference poster titled The Contrast Library, a clean grid of about fourteen rows, each row a task type on the left in bold with its contrast options on the right separated by vs: migration: big bang vs strangler fig vs expand then contract; production incident: roll back vs fix forward vs flag it off; dependency upgrade: upgrade in place vs pin and defer vs delete the dependency; schema change: normalize vs denormalize vs additive and versioned; test strategy: unit heavy vs integration heavy vs property and fuzz; concurrency: locking vs immutability vs message passing; error handling: fail fast vs degrade gracefully vs retry idempotently; third party integration: thin wrapper vs anti corruption layer vs build in house; scaling: scale up vs scale out vs reduce demand; rollout: ship it vs feature flag vs canary; deleting a feature: delete now vs deprecate vs hide behind a flag; cost reduction: cheaper infra vs cheaper algorithm vs cut the feature; slow CI: cache vs parallelize vs only test what changed; tech debt: pay it down vs fence it off vs delete the code]

![[plan-with-contrasts-contrast-library-1.png]]
![[plan-with-contrasts-contrast-library-2.png]]
![[plan-with-contrasts-contrast-library-3.png]]
![[plan-with-contrasts-contrast-library-4.png]]
![[plan-with-contrasts-contrast-library-5.png]]

---

## Demo

Real codebase, real problem: the analytics dashboard endpoint takes about four seconds to load. This is exactly the prompt you would type, start to finish.

1. **Open Claude Code in plan mode** in the repo. Type the whole thing in one message:

   > The analytics dashboard endpoint takes ~4 seconds to load. Before writing any plan, launch three Plan subagents in parallel with these perspectives: 1) better algorithm, make the computation itself faster, 2) caching, avoid recomputing what we already computed, 3) do less work, question whether this computation needs to happen here, at request time, for every user. Have each return its own plan. Then show me a comparison of what each optimizes for and what it sacrifices, and interview me about my constraints before recommending one.

2. **Watch the fan-out in the terminal.** Three Task calls fire in a single message, three Plan agents reading the same code through three different lenses, in parallel. Same mechanic plan mode runs on autopilot, except we chose the lenses.
3. **The comparison lands.** Agent one: rewrite the aggregation query, kill the N+1 calls, roughly 4s to 800ms, medium diff. Agent two: cache the aggregation with a five minute TTL, 4s to 50ms on hits, small diff, staleness cost. Agent three: the endpoint computes all-time stats on every load, but the page only shows the last 30 days above the fold. Precompute nightly, lazy-load the rest, 4s to under 100ms, and the hot path mostly disappears.
4. **The interview arrives as actual question prompts in the terminal.** Is five minute staleness acceptable for these numbers? Are users complaining about load time or about the data? Is there already a scheduled job runner in this codebase? I click through: staleness is fine, and yes, there is a runner.
5. **Two answers just eliminated agent one.** The recommendation comes back: agent three's plan, with agent two's TTL cache as a safety net on the lazy-loaded section. The final plan merges them. I approve, exit plan mode.
6. **The kicker, on camera:** "make this endpoint faster" would have gotten me agent one's plan. Correct, shippable, 800ms. The distribution had a plan eight times better sitting in a region that prompt never searches.
7. **Make it permanent.** This prompt is a template with two blanks: the task and the three perspectives. Wrap it in a skill or a slash command, pull the perspectives from the contrast library, and the whole technique becomes `/contrast` plus one sentence describing the task.

---

## Key Insight

> Confidence in a plan should come from seeing the distribution it was drawn from, not from how sure the single sample sounds.

---

Anthropic trusts this pattern enough to wire it into plan mode itself. That built-in version is the small-task version: automatic perspectives, silent synthesis, plan mode only.

You now have the full-size version. Contrasts you choose, disagreement you actually get to see, an interview before anything gets picked, and no reason to stop at implementation plans. Architecture decisions, migrations, tooling choices, anything you would hand an agent: fan out, compare, interview.

Next time an agent hands you a single confident answer, ask the only question that matters: what did the rest of the distribution look like?
