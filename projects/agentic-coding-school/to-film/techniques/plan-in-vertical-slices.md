---
duration: "12-16 min"
batch: 1
order: 1
batch_name: "Planning Before Implementing"
class: "techniques"
chapter: "Planning Before Implementing"
status: "scripted"
---

## The plan that looks senior is the plan that hurts you

When you ask a coding model to plan a feature, it builds the whole thing in horizontal layers, and that single decision is why your agent runs for an hour and produces something that has never once run.

Watch it happen. You say "add a comments feature." The model writes a plan. Phase one: the database schema and migrations. Phase two: all the service functions. Phase three: all the API routes. Phase four: the frontend.

It reads beautifully. It is also a trap.

[IMAGE: a clean four-tier stack drawn top to bottom, DB then Services then API then Frontend, with a single green checkmark hanging off the very bottom edge and the top three tiers greyed out as untested]

![[images/plan-in-vertical-slices/horizontal-stack-one-checkpoint.png]]

---

## Why every model defaults to this

Horizontal slicing looks like the disciplined senior way to build. That is exactly the problem.

It groups like with like. All the database work sits together. All the services sit together. The plan is tidy, symmetrical, easy to skim. It mirrors how your codebase is already laid out into folders: a `db/` folder, a `services/` folder, a `routes/` folder, a `components/` folder.

So the plan feels correct because it matches the shape of the repo on disk.

But here is what that tidiness costs you. Horizontal slicing defers all integration to the very end. Nothing talks to anything else until the last phase. The first moment the feature can actually run is also the moment 1,200 lines of code already exist.

This is exactly the failure Dexter Horthy from HumanLayer named in his talk "Everything We Got Wrong About Research-Plan-Implement" at the Coding Agents Conference. His words: **"models love to do all the database and then all the services... before you know it, you're on the other side of 1,200 lines of code and it's not working."**

Source: https://www.youtube.com/@RAmjad/videos

On the other side of 1,200 lines. And it's not working. Sit with that. You have no runnable checkpoint, no oracle, no idea which of four untested layers is lying to you.

---

## The fix: slice vertically, wire one thin path end to end

Force the agent to build one thin slice that runs all the way through, before it builds anything wide.

Instead of "all the DB, then all the services," you say: mock one endpoint, wire it straight to the frontend so a fake but real flow works end to end, and only then backfill the real layers underneath it.

[IMAGE: two columns side by side, left labeled Horizontal stacked as DB / Services / API / Frontend with one test gate only at the very bottom, right labeled Vertical sliced as four thin end-to-end columns each with its own green checkmark]

![[images/plan-in-vertical-slices/horizontal-vs-vertical.png]]

Same total code. Same four layers. But now the build is sliced the other way. Each slice cuts through every layer, thin, and each slice runs.

The first checkpoint is a hardcoded endpoint returning fake comments, rendered in a real component, in a real page you can click. It is not the finished feature. It is a spine. And a spine that runs is worth more than four organs that don't.

---

## Why it works: two mechanisms, not one

This is not just about feeling productive earlier. Two concrete things change, and both compound.

**One: the debugging search space collapses.**

A vertical slice compiles and runs after each phase. That makes every checkpoint a testable oracle. So when something breaks, the fault is localized to the roughly 200 lines you just added, not smeared across four layers that were all written blind.

Horizontal build breaks and you ask "which layer?" Vertical build breaks and you already know: it's the slice you just added. You went from searching 1,200 lines to searching 200.

[IMAGE: left side a tangled red zone spanning all four layers with a question mark, right side a single highlighted 200-line band with a precise red pin dropped on it]

![[images/plan-in-vertical-slices/fault-localization.png]]

**Two: the human can steer on behavior before the expensive layers get written.**

Because a runnable artifact exists early, you can look at the actual flow and say "this isn't the flow I meant" while it is still cheap to change. You are correcting behavior at 200 lines, not at 2,000.

Steering after 2,000 lines exist means unwinding 2,000 lines. Steering at the spine means retyping one mock. The vertical slice moves your most valuable feedback, "that's not what I wanted," to the cheapest possible moment.

---

## Where this comes from: it's how you build a house

You have seen this principle work in the physical world your whole life. A general contractor does not rough plumbing through the entire house before a single fixture works.

They frame one room. Plumb it. Wire it. Get it to a livable, inspectable state. One finished room. Then they replicate that room across the house.

[IMAGE: a house floor plan where one room is fully rendered with fixtures and a checkmark, and the remaining rooms are faint dashed outlines waiting to be replicated from it]

![[images/plan-in-vertical-slices/one-finished-room.png]]

Same total labor either way. But the vertical builder surfaces defects in one inspectable room, early, where a mistake costs one room's worth of rework. The horizontal builder who runs every pipe through every wall first finds the leak after everything is sealed.

A migration is the same. You do not migrate all tables, then all queries, then all callers, then flip a switch and pray. You migrate one path end to end, verify it in production behind a flag, then replicate. Vertical slicing is not a coding trick. It is how competent people build anything large under uncertainty.

---

## Be honest: where vertical slicing goes wrong

This is a default to force, not a religion. Two failure modes are real.

**Mocks calcify into shipped shortcuts.** That hardcoded endpoint from checkpoint one was supposed to be temporary. If you never circle back and replace it with the real service, you have shipped a fake. The vertical method depends on the discipline of backfilling. Skip the backfill and you have just built a very convincing demo that lies.

**Some work is genuinely horizontal.** A pure schema migration with no new behavior. A design-system swap where you replace one button component everywhere. Forcing verticality onto that adds ceremony with no checkpoint payoff, because there is no thin end-to-end path to run. There is just the wide change.

The tell: if a "slice" has no runnable behavior at its end, you are inventing structure that pays you nothing. Ship it wide.

---

## The two artifacts that make this work

Vertical slicing lives or dies on the plan you hand the agent. Two artifacts do the heavy lifting, and both are deliberately short so a human can actually review them.

**The design doc. Roughly 200 lines.**

Matt Pocock calls this the "design concept." It captures five things: current state, desired end state, patterns in the codebase to follow, decisions already resolved, and open questions still to answer.

This is where you do brain surgery on the agent. Before a single line of code exists, you are reshaping how it will think about the whole feature. Reviewing 200 lines of intent gives you far more resteering leverage than reviewing a 1,000-line plan of mechanics, because at 200 lines you are correcting the idea, not the typing.

[IMAGE: a small 200-line document with a surgeon's hands and a scalpel editing it, an arrow leading to a large 1,000-line code block downstream that reshapes to match]

![[images/plan-in-vertical-slices/brain-surgery-on-the-agent.png]]

**The structure outline. Roughly two pages.**

Here is the analogy from Horthy's talk that makes it click: **"if the plan is the implementation, the outline is the C header files."**

The plan is the full `.c` file, every line of logic. The outline is the `.h` file. Just the signatures. The new types. The phase order. And how you test each phase.

[IMAGE: a C header file on the left showing only function signatures and type declarations, an arrow to a full implementation file on the right dense with logic, the header labeled review this the implementation labeled generate this]

![[images/plan-in-vertical-slices/header-vs-implementation.png]]

That is it. Two pages. Short enough that you will actually read every line, which means correction happens at the outline, not deep in the generated code.

---

## The leverage punchline

Reviewing a two-page outline beats reviewing a 1,000-line plan.

Nobody reads a 1,000-line plan carefully. You skim it, you approve it, you find out what it actually said when the code breaks. A two-page outline you read every word of. So the outline is where you catch the wrong pattern, the missing type, the phase in the wrong order.

You save the deep review for the actual code, once, at the end, when it is worth it. You do not spend it on a plan you were never going to read.

[IMAGE: a scale balance, one pan holding a thick 1,000-line plan tilted down and unread, the other pan holding a thin 2-page outline tilted up and marked with review checkmarks, and steering leverage arrows pointing to the light side]

![[images/plan-in-vertical-slices/outline-leverage-scale.png]]

---

## Demo: watch it flip in real time

Here is the whole thing, concrete, in four moves.

1. **Ask for a horizontal plan and name the tell.** Ask Claude to plan a real feature, say a comments system. Watch it emit exactly this: "Phase 1, all the DB. Phase 2, all the services. Phase 3, all the API. Phase 4, the frontend." Say the tell out loud so you can never unsee it: four phases, and the feature first runs only at the end of phase four.

2. **Rewrite it vertically, together.** Slice one comment path top to bottom. Checkpoint one: mock the endpoint, hardcode a fake comment, wire it to a real frontend component so a fake-but-real flow works end to end, and click it. Checkpoint two: backfill the services layer so the endpoint calls real logic. Checkpoint three: run the real DB migration and connect it. Same total code as the horizontal plan. Four checkpoints instead of one.

3. **Break something on purpose at checkpoint two.** Introduce a bug in the services layer you just wired. Watch the fault localize instantly, because the DB isn't in play yet and the frontend already worked at checkpoint one, so it has to be the 200 lines you just touched. Then imagine that same bug in the horizontal build, surfacing at line 1,200, with four untested layers and no idea which one lied.

4. **Show the two artifacts and correct before any code exists.** Put up the 200-line design doc and the two-page structure outline, signatures plus new types plus phase order. Spot a bad pattern the agent chose, maybe it invented its own data-fetching approach instead of following the codebase's existing one, and fix it right there in the outline. Zero lines of implementation written. That correction just saved you a 1,000-line rewrite.

---

### Key Insight

> Coding models plan horizontally because it looks senior, but horizontal plans hide every bug until 1,200 lines exist. Slice vertically so every checkpoint runs, and your fault localizes to 200 lines instead of four blind layers.

---

You are going to catch the horizontal tell in the very next plan your agent writes.

Name it. Flip it to vertical. Review the two-page outline, not the 1,000-line plan.

Correct at 200 lines, not 2,000.
