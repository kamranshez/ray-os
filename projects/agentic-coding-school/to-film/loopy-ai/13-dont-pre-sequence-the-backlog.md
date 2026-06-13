---
duration: "10-14 min"
batch: 4
order: 13
batch_name: "L3 Task Lifecycle"
class: "loopy-ai"
chapter: "Don't Pre-Sequence The Backlog"
aliases: [dont-pre-sequence-the-backlog]
---

A thirty-year agile consultant, a man who has spent his entire career fighting waterfall, sat down to run a coding project with Claude. He broke it into tickets. He broke the tickets into sub-tickets. He hand-mapped every dependency. Then he fired up six or seven parallel agents to chew through it.

It failed horribly. Two agents both landed on the same shared blocker. Both decided to unblock it. Both implemented the same thing, on top of each other.

His own diagnosis is the thesis of this whole segment. "What I'd done effectively was recreate the waterfall processes. The entire project specified up front, with all the intricate dependencies handed to the development team." Source: Chris Parsons, Ralph Loops workshop.

He had handed a Claude the single worst process of the 1990s. And so will you, the first time the model generates forty tickets for you and your hands itch to put them in order.

---

## The instinct that betrays you

You point the model at a project. It produces a backlog. Forty tickets, clean, numbered.

And the moment you see them, you want to sequence them. Ticket 1, then 2, then 3. Draw the arrows. This blocks that. Lock the order before you start.

It feels like diligence. It is the opposite.

You just rebuilt a Gantt chart. You froze a plan at the moment of *least* knowledge, before a single ticket has been touched, before anything real has been learned. The entire reason agile beat waterfall is that execution order should be *discovered*, not decreed. Pre-specifying ticket dependencies recreates the exact thing waterfall got wrong: a rigid up-front plan that the first day of real work makes obsolete.

A numbered, arrowed ticket list is a plan made before the work. That's the tell. You're not being organised. You're being premature.

[IMAGE: dark canvas, split frame. Left side a Gantt chart with a big red X struck through it. Right side a loose stack of backlog cards, a curved loop arrow reaching in to pull the top card, then curving back to a label that reads "pick again"]
![[images/dont-pre-sequence-the-backlog/gantt-vs-backlog.png]]

---

## Why the order ages so badly

Here is the thing the frozen plan ignores. The loop has more context at ticket-time than you had at planning-time.

Every completed ticket changes what "most important next" even means. It unblocks things. It makes things obsolete. It reveals work you didn't know existed when you were drawing arrows. The map you drew on day zero is describing a world that stops existing the moment the first ticket lands.

A frozen order throws all of that away. So don't freeze it.

This is the inverse of the failure we met in [[writing-effective-goals]]. There, the danger was under-specifying success, leaving the goal so vague the cheap judge can't grade it. Here, the danger is over-specifying execution, nailing down an order the work won't hold still for. Same mistake in mirror image: putting the constraint in the wrong place. A goal should be tight on *what good looks like* and loose on *which ticket comes first*.

---

## Real dependencies versus imagined ones

Now, not all ordering is a guess. Some of it is physics.

You cannot build the API client before the schema exists. You cannot write tests against an endpoint that has no signature yet. Those are facts about order, not opinions about order. Encode those. They belong in your hard constraints.

But most pre-sequencing is not physics. It's a guess about which thing should come first, dressed up as a fact. And the guess ages badly, while the physics never moves. The skill is telling the two apart, and only writing down the physics.

And here is the part that should make you relax: the AI finds the physics on its own. In Parsons' workshop, when he stopped hand-mapping and instead let an agent team read the *whole* backlog, the team came back and said, in effect, "these are all sequential, run none of them in parallel." And it was right. Source: Chris Parsons, Ralph Loops workshop.

You don't need to pre-encode what the model can detect by reading. Hand it the set, hand it the real constraints, and let it work out the dependencies on the fly from what's actually been done.

[IMAGE: dark canvas, two columns. Left column "physics" with a few solid locked arrows (schema then client), labeled "write these down". Right column "guesses" with a tangle of faded dotted arrows over a pile of tickets, labeled "let the loop decide"]
![[images/dont-pre-sequence-the-backlog/physics-vs-guesses.png]]

---

## Re-prioritise, don't pre-prioritise

So what does the loop body actually become?

Survey the backlog. Pick the single highest-value unblocked ticket *right now*. Do it. Repeat.

The decision gets remade every iteration, against the current state of the world, not made once against a guess. Parsons' version of the fix is a one-liner. "Just run a loop where you say, pick the next most important ticket. The AI is quite capable of looking at all of them, figuring out the dependencies on the fly based on what's just been done." Source: Chris Parsons, Ralph Loops workshop.

This is exactly the loop shape we built in [[ralph-loops]]. Run the same prompt in a fresh context against files on disk, until the goal is met. Back there, the instruction was "pick the single most important thing each pass." This segment is the *why* behind that line. The pass-by-pass re-pick isn't a stylistic choice. It's the only way to keep the order honest as the work teaches you things.

And there's a discipline that sits between "picked" and "building." Don't go straight from ticket to code. Let the loop look around first. Is this ticket still relevant? Did an earlier change make it trivial, or delete the need for it entirely? Does it still unblock what you thought it unblocked? A few minutes of orientation beats confidently shipping work that a later ticket invalidates. Explore, then execute.

---

## Don't reach for parallelism to fix this

When the loop feels slow, there's a seductive escape hatch. Run more agents at once. Fan it out.

Resist it. That is the exact move that produced the contention disaster in the cold open. Two agents, one shared blocker, the same code written twice. The one thing the AI genuinely struggles to manage is many tickets in parallel. And the one thing you don't actually need is more of them.

Parsons again. "The bottleneck is usually not the number of agents. It's usually you, just keeping up." Source: Chris Parsons, Ralph Loops workshop.

Start with a single loop. One AI, running continuously, re-picking the next ticket each pass, is already faster than you can review. You will hit your own reading speed long before you hit the loop's ceiling. Parallelism, orchestration, agent teams: that's a later problem, and honestly most people never reach it. We touch the governance of many loops much later in the class. For now, one loop, pointed at the whole backlog, is the whole game.

This connects straight to the doctrine we'll formalise in [[mission-command]]: intent plus constraints, latitude on method. Telling the loop "pull this ticket first" is dictating method. Telling it "here's what good looks like, here's what's out of bounds, now choose" is intent. You give the loop a mission, not a march order.

---

## Why this is the only interesting Ralph loop now

One more thing, and it reframes where Ralph earns its keep.

The original Ralph pitch was the single-ticket re-run. Build the ticket, now build it again, now again, until it's right. On the models we had a year ago, that repetition caught real bugs. On current models, it barely catches anything. The model finishes the ticket the first time. Running it twice mostly burns tokens to confirm what you already had.

So all the value has moved. It moved from re-running *one* ticket to pointing the loop at the *whole backlog* and letting it re-pick. That's the leap, and Matt Pocock's the one who put a name on it: stop looping a ticket, start looping a backlog. Source: Matt Pocock (credited in Parsons' workshop).

Which means this isn't a footnote to Ralph loops. It's where Ralph loops actually become worth running. The backlog re-pick *is* the modern Ralph loop.

---

## Demo

Hand the same backlog to a loop two ways, side by side, and let the contrast make the argument.

1. Generate the backlog once. Forty-ish tickets for a small real feature. Save it as a flat file.

2. **Version A, pre-sequenced.** Feed the loop a fixed numbered dependency chain. Ticket 1 blocks 2 blocks 3, the whole graph drawn up front, exactly the way your instinct wants to draw it.

3. **Version B, re-picked.** Feed the loop the *same* tickets as an unordered set, plus one paragraph: the prioritisation rubric. Favour unblocking. Favour user-visible. Favour reversible. Favour cheap-to-verify. And the instruction: each pass, pick the next most important ticket.

4. Run both loops. Plant one trap in the backlog: a ticket that an *earlier* change quietly makes unnecessary.

5. Watch Version A march into that ticket and dutifully build it, because the chain said it was next, even though the work is now dead. Watch Version B reach the same ticket, look around, notice it's been obsoleted, and skip it.

That skip is the entire point. One loop executed a stale plan. The other read the world.

6. Optional second run, for the parallelism beat. Let the single Version B loop run while you try to review its output in real time. Show yourself falling behind. The loop is not the bottleneck. You are. Make that concrete *before* anyone in the comments asks "why not run ten of these at once."

[IMAGE: dark canvas, two terminals side by side. Left terminal labeled "pre-sequenced" showing an agent building a ticket with a tombstone icon marked "already obsolete". Right terminal labeled "re-picked" showing the same ticket crossed out with a "skipped, obsoleted" note and the loop moving to the next card]
![[images/dont-pre-sequence-the-backlog/demo-a-vs-b.png]]

---

## Key Insight

> Don't hand the loop an order. Hand it the whole backlog, the goal, and the hard constraints, then let it re-pick the next most important ticket every pass. A frozen sequence is waterfall in a hoodie.

---

## Where we go next

You now know the shape: unordered set, prioritisation rubric, hard constraints, re-pick every pass. One loop, not ten.

But there's a dial hiding inside all of this. How much do you let the loop decide before it checks back with you? Pick the ticket, sure, but does it also pick the approach, ship the PR, merge it? That's the autonomy question, and it's the next segment.

See you in the next one.
