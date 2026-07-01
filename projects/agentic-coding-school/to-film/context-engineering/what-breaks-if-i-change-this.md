---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Understanding the System"
class: "context-engineering"
chapter: "Understanding the System"
---

Before you let an agent touch a large codebase, ask it one question. Not "make the change." Ask "what breaks if I make this change?" And make it draw you the answer.

That single question, turned into a diagram, is the highest leverage move you have in a codebase too big to fit in your head.

This video is about pointing the agent at understanding instead of production. You already know it can write the change. The skill worth having is getting it to show you the blast radius first, as an artifact you can look at, so you decide before you commit and not after.

---

## The change you didn't know you were making

In a small project you can read the whole thing. You know what calls what. You make a change, you hold the consequences in your head, you move on.

That stops being true fast.

The danger in a large codebase was never writing the change. It's the *second* change you made without realizing it. The caller three directories away. The test that asserts on the old shape. The config flag that quietly branches on the value you just renamed.

You can break a million line system with one bad line of code, or one bad config flag.

Source: Google I/O 2026, Adam Bender, "Software Engineering at the Tipping Point"

That fragility is the whole problem. And it gets worse the moment agents are making changes at speed, because now the invisible ripple you never see is being created faster than any human can track it.

[IMAGE: dark background, a single node labeled "your change" at center, thin ripple lines fanning out to faded, half-hidden nodes labeled caller, test, config, billing, most of them greyed out to signal "you can't see these"]

![[what-breaks-invisible-ripple-1.png]]
![[what-breaks-invisible-ripple-2.png]]
![[what-breaks-invisible-ripple-3.png]]
![[what-breaks-invisible-ripple-4.png]]
![[what-breaks-invisible-ripple-5.png]]

---

## Nobody actually holds the map

Here's a test. Go back to your team and ask everyone to draw an architecture diagram of your system. Count how many different pictures you get.

Source: Google I/O 2026, Adam Bender, "Software Engineering at the Tipping Point"

You will get a different diagram from every person. Not because anyone is wrong. Because nobody holds the whole thing anymore. Each person carries the slice they touch, and the slices don't agree at the edges.

That is the state you make changes in. Everyone is confident about their corner and blind to the seam where their corner meets someone else's.

[IMAGE: dark background, three rough hand-drawn architecture sketches side by side of the "same" system, each clearly different in shape and connections, a puzzled question mark above them]

![[what-breaks-divergent-maps-1.png]]
![[what-breaks-divergent-maps-2.png]]
![[what-breaks-divergent-maps-3.png]]
![[what-breaks-divergent-maps-4.png]]
![[what-breaks-divergent-maps-5.png]]

Agents make this cut both ways. Worse, because they edit faster than anyone can keep up with. Better, because an agent can actually read the entire graph in one pass and hand you the map no single person on the team was holding.

That second half is the opportunity. You just have to ask for it in the right direction.

---

## Don't ask it to change it. Ask it to map it.

Here is the move.

Before the edit, get the agent to trace the blast radius of the change and render it as an artifact you can look at. Callers, consumers, tests, the config that reads the value, the migration that assumes the old shape. All of it, drawn.

"What breaks if I change this?" takes an invisible dependency graph and turns it into a picture you can hold.

That is the reframe. The exciting use of the agent here is not making the code machine go faster. It's deepening your understanding of the thing you already built before you reach in and disturb it.

[IMAGE: left side a tangled invisible web of faint grey lines labeled "the dependency graph you can't see", an arrow labeled "what breaks if I change this?" pointing right to a clean, bold, readable node-and-edge diagram labeled "an artifact you can hold"]

![[what-breaks-invisible-to-artifact-1.png]]
![[what-breaks-invisible-to-artifact-2.png]]
![[what-breaks-invisible-to-artifact-3.png]]
![[what-breaks-invisible-to-artifact-4.png]]
![[what-breaks-invisible-to-artifact-5.png]]

---

## Why the artifact beats the answer

You could ask the agent for this in prose. Do not.

A paragraph reads smooth even when it is missing the one thing that matters. The agent lists six affected files in a tidy sentence, you nod, and the seventh, the caller that writes to billing, never makes it into the text. Prose hides the surprise edge.

A diagram cannot hide it. The shape forces it out. You see the fan-out. You see the one red edge running into a module you forgot this code even touched. Your eye catches the thing your reading skipped.

The diagram is not decoration. The diagram is the deliverable. The code change is easy. The picture of what the change touches is the part worth paying attention to.

[IMAGE: two panels. Left panel a smooth grey paragraph of text with one critical line faded and easy to miss. Right panel the same information as a node graph where one bright red edge to a "billing" node is impossible to overlook]

![[what-breaks-prose-vs-diagram-1.png]]
![[what-breaks-prose-vs-diagram-2.png]]
![[what-breaks-prose-vs-diagram-3.png]]
![[what-breaks-prose-vs-diagram-4.png]]
![[what-breaks-prose-vs-diagram-5.png]]

---

## Why "before" beats "after"

We already have videos on diagramming a change *after* the agent makes it. Reading the shape of a git diff. Turning a completed change into a Mermaid diagram so you can review it without reading every line.

This is the same tool pointed at a different moment in time.

Those are review. You look at what already happened and judge it. This is simulation. You draw the map *before* you commit, so you can decide whether to commit at all.

Same diagram, one step earlier, and the value completely changes. After the change, a diagram tells you what you did. Before the change, it tells you what you are about to set off. One is a receipt. The other is a decision.

[IMAGE: a horizontal timeline with a "commit" marker in the middle. Left of it labeled "before: simulate the blast radius, decide" with a magnifying glass. Right of it labeled "after: review what happened" with a checkmark. Arrow emphasizing the left side]

![[what-breaks-before-vs-after-1.png]]
![[what-breaks-before-vs-after-2.png]]
![[what-breaks-before-vs-after-3.png]]
![[what-breaks-before-vs-after-4.png]]
![[what-breaks-before-vs-after-5.png]]

---

## The loop

In practice it is a short, repeatable cycle.

1. **Point and name.** Show the agent the code and state the exact change. Not "improve this." "I want to change the return shape of this function from an object to an array."
2. **Trace, don't touch.** Tell it explicitly not to edit anything yet. Have it walk callers, consumers, tests, config, and migrations that depend on the current behavior.
3. **Render the fan-out.** Ask for a Mermaid diagram with the change at the center and the risky edges colored. The ones that cross into money, auth, or data get their own color.
4. **Interrogate it.** Now ask the what-if questions. "What if I also keep the old field for a release?" "What if this path is hit by the mobile client too?" Each question reshapes the map.

Then, and only then, do you decide whether the change is a five minute edit or a thing that needs a plan.

[IMAGE: a four-step cycle drawn as a loop: "point and name" arrow to "trace don't touch" arrow to "render the fan-out" arrow to "interrogate" arrow back to the start, with the center of the loop labeled "decide"]

![[what-breaks-the-loop-1.png]]
![[what-breaks-the-loop-2.png]]
![[what-breaks-the-loop-3.png]]
![[what-breaks-the-loop-4.png]]
![[what-breaks-the-loop-5.png]]

---

## Keep it honest

Two ways this goes wrong, and both are avoidable.

The map drifts. A blast radius you drew last week is describing a codebase that no longer exists. So you never save the map and trust it later. You regenerate it from the real code every time you ask the question. A stale architecture diagram is worse than none, because it lies with confidence.

The agent hallucinates structure. It will happily invent a dependency that sounds right. So you make it cite. Every edge in that diagram should come with the file and line it found. Then you spot-check the scariest edge yourself, the one running into billing, before you believe the rest.

Grounded in the real graph, cited, and freshly generated. That is the difference between a map you can act on and a nice-looking guess.

---

## Demo

Open Claude Code in a real production repo. Not a toy. Something with enough history that no one on the team could draw it from memory.

1. Pick a genuinely scary change. "I want to change `getSubscription` to return an array of subscriptions instead of a single object."
2. Prompt it to map, not edit: *"Do not change any code. Trace every caller of this function, every test that depends on its shape, every place that reads the returned fields, and any migration or config that assumes the current shape. Cite the file and line for each."*
3. Ask for the artifact: *"Now draw that as a Mermaid diagram. Put the change at the center. Color any edge in red that touches billing, auth, or the database schema."*
4. Read the picture. Watch the surprise land, the caller in the mobile checkout flow nobody remembered, sitting on a red edge.
5. Interrogate it: *"What breaks if I keep the old single-object endpoint alive for one release and add the array as a new field?"* Watch the red edges drop to two.
6. Only now make the call. The naive version was a landmine. The interrogated version is a safe, staged change. You found that out before you wrote a line.

The whole thing takes a few minutes and it happens entirely before the risky edit exists.

---

## Key Insight

> A diagram drawn after the change is a receipt. A diagram drawn before it is a decision.

---

Stop treating the agent as only a code machine. Point it at the thing you actually lack in a big codebase, which is the map. Ask what breaks before you break it, make it draw the answer, and you turn every scary change into one you can see all the way through.
