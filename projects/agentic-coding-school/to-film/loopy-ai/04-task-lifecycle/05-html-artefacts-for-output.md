---
duration: "8-12 min"
batch: 3
order: 9
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "HTML Artefacts For Output"
aliases: [html-artefacts-for-output]
---

Most of your loops can already think. What they can't do is hand you something you can look at, click through, and disagree with.

Last segment we said a loop only closes if the agent can act on and perceive the exact thing it works on. We wired the input cables. This segment is about the output cable, and there is one format that wins almost every time: a single HTML file.

Not a chat reply. Not a wall of markdown. A self-contained artifact the agent writes to disk, you open in a browser, and the loop reads back.

---

## The problem with text output

Watch what happens when a loop's output is just text in a chat window.

The agent does twenty minutes of real work. Then it dumps a thousand words back at you. A plan, a research summary, a list of options. You skim the first paragraph, lose the thread by the third, and approve it because reading the whole thing properly would take longer than the work did.

That is not verification. That is rubber-stamping with extra steps.

The output is in the wrong shape for the thing you need to do with it, which is *judge it*. Text forces you to hold the entire structure in your head at once. A decision buried in paragraph nine looks exactly like a sentence of throat-clearing in paragraph two. You can't see the shape of the work, so you can't see where it went wrong.

[IMAGE: dark canvas, left side a cramped wall of chat text with a tiny "approve" button, right side a clean browser window with tabs, panels, and a highlighted decision point, an arrow labeled "same work, judgeable shape" pointing right]
![[loopy-html-artefacts-for-output-text-vs-artifact-1.png]]
![[loopy-html-artefacts-for-output-text-vs-artifact-2.png]]
![[loopy-html-artefacts-for-output-text-vs-artifact-3.png]]
![[loopy-html-artefacts-for-output-text-vs-artifact-4.png]]
![[loopy-html-artefacts-for-output-text-vs-artifact-5.png]]

And it gets worse at the next level. When this loop runs unattended, the chat scrolls away. There is no durable thing left over. The work happened and then evaporated into a transcript nobody will ever open again.

You need an output that survives the run, that you can scan in ten seconds, and that the loop itself can pick back up next time. Text is none of those things.

---

## The core move: the artifact is the interface

Tell the agent to write its output as one HTML file.

That's it. That's the whole move. But it quietly fixes three problems at once, because an HTML artifact is three things wearing one coat.

It's the *output* you read. A browser mockup, a flow diagram, a comparison table, a decision tree, an email draft rendered the way it will actually look. You see the work in its final shape, not a description of its final shape.

It's the *spec* you correct. This is the prototypes-as-specs idea, and it's worth stealing. David K from the XState team put it as "the spec should fall out of the prototype, not the other way around. One prototype is worth a hundred spec drafts."
Source: https://x.com/DavidKPiano/status/2052448434142269741

That's the inversion to internalize. The whole category of spec-driven tools runs the arrow the wrong way: write the spec, then generate the thing. Flip it. Generate the thing, then read the spec back off it. Matt Pocock, who triggered that thread, found the same edge: the more he replaced plans with prototypes, the better the outputs got, and low-fidelity prototypes beat walls of spec.
Source: https://x.com/mattpocockuk

You don't write a paragraph describing the onboarding flow and hope the agent builds the right thing. You let the agent render the onboarding flow as a clickable artifact, you click through it, and the places where you wince *are* the spec. The HTML artifact is the prototype. The spec is whatever survives your corrections to it. Correcting a rendered thing is faster and more honest than authoring an abstract description of a thing that doesn't exist yet.

And it's the *runtime* the loop reads. This is the part people miss. The artifact isn't a dead screenshot. It's a live file on disk the loop writes to on every iteration and reads back on the next. The dashboard for a worker loop. The experiment table for a research loop. The plan a long-running agent updates as it goes. The artifact is where the loop's state becomes something you can both see.

Output, spec, runtime. One file. That's why this is a workflow primitive and not a formatting tip.

[IMAGE: dark canvas, a single HTML file icon in the center with three labeled arrows radiating out, "OUTPUT you read", "SPEC you correct", "RUNTIME the loop reads back", three roles one file]
![[loopy-html-artefacts-for-output-three-roles-one-file-1.png]]
![[loopy-html-artefacts-for-output-three-roles-one-file-2.png]]
![[loopy-html-artefacts-for-output-three-roles-one-file-3.png]]
![[loopy-html-artefacts-for-output-three-roles-one-file-4.png]]
![[loopy-html-artefacts-for-output-three-roles-one-file-5.png]]
---
## Where this lands in a real loop

Three quick shapes, so this stops being abstract.

A planning loop. The agent researches a feature and renders the plan as an artifact: mockups of each screen, a server-flow panel, the decision points called out. You click through, you object to two of them, the agent regenerates only those. The artifact you stop objecting to is the spec the build loop runs against. No separate spec doc ever gets written.

A worker loop. Out front sits a dashboard artifact: the queue, what's in flight, what passed its borrowed verifier, what got escalated. The loop rewrites it every iteration. You glance at it once a day instead of reading a transcript. Same output cable, pointed at continuous work.

A research loop. The artifact is the experiment table. We met this in the borrowed-verifiers segment: each row is what changed, what the verifier said, did it ship. Rendered as a sortable HTML table with the JSON underneath, the agent reads the table before proposing the next change, and you read the same table to see what it's learned.

Notice the pattern. Same artifact, three roles, every level of the stack. That's why we're teaching it down here in the foundations, before the climb. Every loop above L2 is going to want an output cable, and this is the one that works.