---
duration: "10-14 min"
batch: 3
order: 5
batch_name: "The Climb"
class: "loopy-ai"
chapter: "Don't Pre-Sequence The Backlog"
status: stub
---

Stub — when you hand a loop a big backlog, don't hand it an order. Give it the whole set, the goal, and the hard constraints, then let it pick the next most important ticket each pass. Pre-specifying the dependency chain is waterfall in a hoodie.

> **The one-line rule:** Prompt the loop to pick the next most important ticket instead of pre-specifying elaborate dependency graphs.

## Thesis

The instinct, once the model has generated forty tickets for you, is to sequence them. Ticket 1, then 2, then 3. Draw the dependency arrows. Lock the order.

You just rebuilt a Gantt chart. You froze a plan at the moment of *least* knowledge — before a single ticket has been touched — and the whole reason agile beat waterfall is that execution order should be *discovered*, not decreed. Pre-specifying ticket dependencies recreates waterfall: a rigid up-front plan that the first day of real work makes obsolete.

The loop has more context at ticket-time than you had at planning-time. Every completed ticket changes what "most important next" means — it unblocks things, makes things obsolete, reveals work you didn't know existed. A frozen order throws all of that away. So don't freeze it. Give the loop the backlog as an unordered set plus a prioritisation rubric, and let it re-decide the next ticket on every pass.

## Key beats

- **The waterfall tell.** A numbered, arrowed ticket list is a plan made before the work. That's the exact thing waterfall got wrong. You're not being organised, you're being premature.
- **The war story (Chris Parsons).** A 30-year engineer and agile consultant breaks a project into tickets, breaks those into sub-tickets, maps every dependency by hand, then fires up six or seven parallel agents to chew through it. It fails horribly. Two agents both wait on the same shared ticket, both decide to unblock it, and **both implement the same thing.** His own diagnosis: *"what I'd done effectively was recreate the waterfall processes… the entire project specified up front with all the intricate dependencies handed to the development team."* He'd handed a Claude the worst process of the 1990s. This is the cold-open.
- **Real dependencies vs imagined ones.** Some ordering is physics: you can't build the API client before the schema exists. Encode *those* as hard constraints. But most pre-sequencing is a guess about order, not a fact about order — and the guess ages badly. The skill is telling the two apart and only writing down the physics. And note: the AI finds the physics on its own — when Parsons let an agent team read the whole backlog, it concluded *"they're all sequential, run none in parallel"* and was right. You don't pre-encode what it can detect.
- **Re-prioritise, don't pre-prioritise.** The loop body becomes: survey the backlog, pick the single highest-value unblocked ticket *now*, do it, repeat. The decision is remade every iteration against the current state of the world, not made once against a guess. Parsons' version of the fix is a one-liner: *"just run a loop where you say pick the next most important ticket… the AI is quite capable of looking at all of them, figuring out the dependencies on the fly based on what's just been done."*
- **Don't reach for parallelism to fix this.** The seductive escape hatch is "run more agents at once." Resist it — that's the move that produced the contention disaster above. The one thing the AI genuinely struggles to manage is many tickets in parallel; the one thing you don't actually need is more of them. As Parsons puts it: *"the bottleneck is usually not the number of agents. It's usually you just keeping up."* Start with a single loop. One AI, running continuously, re-picking the next ticket, is already faster than you can keep pace with. Parallelism, orchestration, agent teams — that's a later problem, and most people never hit it.
- **Explore before you execute.** Don't go ticket → code. Between "picked" and "building," let the loop look around: is this ticket now obsolete? Did an earlier change make it trivial? Does it still unblock what you thought it unblocked? A few minutes of orientation beats confidently shipping work a later ticket invalidates.
- **What you hand the loop instead of an order:** (a) the backlog as a set, (b) a prioritisation rubric — favour unblocking, favour user-visible, favour reversible, favour cheap-to-verify — and (c) the hard constraints only. Then it sorts itself, continuously.
- **The cost of getting it wrong.** A stale dependency chain makes the loop grind low-value work first, or build something a downstream ticket deletes. You get motion that photographs like progress and isn't.
- **Why this is the *only* interesting Ralph loop now.** On current models the single-ticket re-run — "build the ticket, now build it again" — barely catches anything; the model finishes the first time. All the value has moved to pointing the loop at a *backlog*. So this isn't a refinement of Ralph loops; it's where Ralph loops actually earn their keep.

## Connections

- [[writing-effective-goals]] — this is the *inverse* failure mode. That segment warns against under-specifying success. This one warns against over-specifying execution order. Both are "putting the constraint in the wrong place."
- [[goal]] — extends the "pre-decomposable work versus unfolding work" line. This is what to do when work *looks* decomposable but the order doesn't actually hold still. Also the home of the spec caution Parsons echoes: over-speccing a project up front "fossilises" a waterfall plan. Just-in-time specs over big-bang specs.
- [[mission-command]] — the doctrinal parent. Intent plus constraints, latitude on method. This is Auftragstaktik at ticket altitude: tell the loop what good looks like and what's out of bounds, not which ticket to pull first.
- [[ralph-loops]] — Ralph's "pick the single most important thing each pass" is precisely this loop shape. This segment is the *why* behind that discipline.

## Sources / refs

- Ray's thesis (the seed). Agile-versus-waterfall as the framing.
- **Chris Parsons, Ralph Loops workshop (2-hour, live-coded).** The primary-source war story: hand-mapped dependency graph + 6–7 parallel agents → contention failure → "I'd recreated waterfall" → fix is "pick the next most important ticket" in a single loop. Also the source of the "bottleneck is you keeping up, not the number of agents" line and the spec-driven-development caution. Parsons is a CTO / ex-agency-CEO / agile consultant — the 30-years-of-agile credibility is part of why the waterfall reframe lands.
- **Matt Pocock** — Parsons credits Pocock's YouTube video for the "point Ralph at a whole backlog" move (the leap from one-ticket loops to backlog loops). Same Pocock already referenced elsewhere in the class.
- Pairs with [[writing-effective-goals]] (the inverse failure), [[goal]] (the runtime), [[mission-command]] (the doctrine), [[ralph-loops]] (the loop shape).

## TODO

- Cold-open with the Parsons contention failure, told fast: the hand-drawn dependency graph, the six parallel agents, two of them building the same ticket. Land the "I recreated waterfall" line, *then* introduce the fix. Failure first, doctrine second.
- Demo: hand the *same* backlog to a loop two ways. Version A — a fixed numbered dependency chain. Version B — an unordered set plus a one-paragraph prioritisation rubric ("pick the next most important ticket"). Run both. Show Version A dutifully completing a ticket that an earlier change already made unnecessary, while Version B skips it. The contrast is the whole argument.
- Optional second demo for the parallelism beat: show the single loop already outrunning the human's ability to review, to make "you're the bottleneck, not the agent count" concrete before anyone asks "why not parallel?"
- Image: split frame. Left — a Gantt chart with a red X through it. Right — a backlog as a loose stack of cards, a loop reaching in and pulling the top one, an arrow curving back to "pick again."
- Image (war story): two robot arms reaching for the same card off a shared stack, colliding.
