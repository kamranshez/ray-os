---
video_id: "vsLXI68M"
duration: "12-16 min"
batch: 5
order: 13
batch_name: "Command & Control"
class: "loopy-ai"
chapter: "Decision Surfaces"
aliases: [decision-surfaces]
---
A decision surface is the output shape that turns your normal work into a free training signal. Get the shape right and every correction you make while doing your job becomes data the loop can learn from. Get it wrong and you throw that signal away every single day without noticing.

This is the segment that makes the [[self-improvement-loop]] possible. Not the part where the loop rewrites its own skill. The part before that, where you decide what the loop's output even looks like. Because if the output is the wrong shape, there is nothing to learn from, and the whole self-improving stack collapses into a loop that runs and never gets better.

---

## The output shape is the whole game

Here is the move almost everyone gets wrong. They build a loop that does judgment work, and they let it answer in prose.

The triage loop reads an issue and writes a paragraph: "This looks like a feature request that's mostly ready, though there's some ambiguity around configuration." The reply loop drafts three sentences. The review loop leaves a comment. All prose, all fluent, all reasonable.

Then a human reads it, disagrees, and rewrites it in their own words. And that disagreement vanishes. There is no clean way to say what the agent got wrong, because there was no discrete thing it claimed in the first place. You can't subtract one paragraph from another.

Now change the shape. The triage loop doesn't write a paragraph. It picks a label: ready-to-implement, duplicate, or needs-info. The reply loop doesn't just draft, it first decides: reply, like, note, or skip. The output is a choice from a known set.

The instant the output is a discrete labeled decision, a human override becomes legible. The agent said ready-to-implement. The human said needs-info. That is a clean, comparable signal you can diff mechanically, store, and count. The deviation has a shape because the decision had a shape.

[IMAGE: dark canvas, two panels. Left panel labeled "prose output": an agent paragraph and a human paragraph side by side with a tangled scribble and a minus sign between them that can't resolve, a red X underneath reading "nothing to subtract". Right panel labeled "labeled decision": agent picks one chip from {ready, duplicate, needs-info}, human picks a different chip, a clean subtraction arrow between them, a green check reading "diffable signal".]
![[loopy-decision-surfaces-prose-vs-label-1.png]]
![[loopy-decision-surfaces-prose-vs-label-2.png]]
![[loopy-decision-surfaces-prose-vs-label-3.png]]
![[loopy-decision-surfaces-prose-vs-label-4.png]]
![[loopy-decision-surfaces-prose-vs-label-5.png]]

---

## The override is only legible because the output was a label

Watch how this plays out in a real triage loop. The agent reads an incoming issue and assigns a label: ready to implement. A reviewer looks at it and disagrees.

In Zach Lloyd's words: "I switch the issue from 'ready to implement' to 'needs info' and add a comment on the thread as to why it was mis-categorized."
Source: https://x.com/zachlloydtweets/status/2066908445425496348

The reason it was mis-categorized, in that case, was ambiguity over whether the feature should ship with a configurable setting. That nuance lives in the comment. But the comment alone would be just one more paragraph in a sea of paragraphs. What makes it usable is the label flip sitting next to it.

The flip is the index. The comment is the explanation. Together they say: here is exactly what the agent decided, here is exactly what a human decided instead, and here is why. The outer loop can find every issue where the label was changed, read the attached reason, and look for a pattern. None of that is possible if the agent only ever wrote prose.

State the choice as a label first. Let the reasoning hang off it. The label is what makes the reasoning findable.

---

## Deviation is the label

So who labels the training data?

Nobody. That is the entire point. You never sit down to annotate examples for the loop. You just do your job. You read the agent's recommendation, and where you disagree, you change it. You flip the label, you edit the draft, you react with a thumbs down. That override is the ground truth.

This is the answer to the question that kills most self-improvement schemes: who keeps teaching it? The honest answer for most teams is "nobody, because nobody has time," and so the loop never improves. The decision surface dissolves that problem. The teaching is a byproduct of the work you were already doing. You are not adding a labeling step. You are harvesting the exhaust of normal work.

And notice what is actually being captured. Not rules you wrote down. Your taste. Every time you flip ready-to-implement to needs-info, you are encoding a judgment call that you might never be able to fully articulate. The deviation is your taste made measurable. That is the raw material the [[self-improvement-loop]] runs on, and it only exists because the output was shaped as a decision.

[IMAGE: dark canvas. A horizontal flow: a person doing their normal job (reading a feed of agent decisions) at the left. As they flip labels and react, small "deviation" tokens drop out of their workflow like exhaust from a pipe, falling into a collector bin labeled "ground truth / taste". An arrow from the bin feeds an outer loop gear labeled "skill update". Caption: "the teaching is a byproduct".]
![[loopy-decision-surfaces-exhaust-of-work-1.png]]
![[loopy-decision-surfaces-exhaust-of-work-2.png]]
![[loopy-decision-surfaces-exhaust-of-work-3.png]]
![[loopy-decision-surfaces-exhaust-of-work-4.png]]
![[loopy-decision-surfaces-exhaust-of-work-5.png]]

---

## The surface has to live where you already are

A decision surface only collects signal if you actually touch it. And you will only touch it if it costs you nothing.

This is why the surface belongs in the place you already live, not in a separate dashboard you have to remember to open. For most teams that place is Slack, which is why the next segment makes it the [[slack-as-your-command-center]]. The loop posts its decision into a channel: here is the issue, here is my label, here is my recommendation, with options laid out.

Then you respond two ways, both near-zero cost.

You react with an emoji for what you actually did. One click. That alone is enough signal: the agent recommended reply, you reacted with the skip emoji, deviation recorded. Petra Donka's team runs exactly this, reacting with an emoji for what they actually did, and optionally adding a note in the thread. One click is enough signal, a thread is extra context.
Source: https://x.com/petradonka/status/2054897826149101588

Or you reply in the thread, and the loop reads the thread back. The emoji is the label flip. The thread reply is the comment that explains why. Same two-part structure as the issue tracker: a discrete signal plus optional reasoning, captured in the tool you never left.

The failure mode is making feedback expensive. The moment giving it requires a separate app, a form, or a weekly meeting, participation dies, and a decision surface with no deviations is just a loop talking to itself. Keep the cost at one click and the signal keeps flowing.

[IMAGE: dark canvas. Center, a single Slack thread on a phone. A loop posts a card: issue title, a label chip "ready-to-implement", and a recommendation line. Below, two cheap response paths drawn as short arrows: one to an emoji react (labeled "1 click = the label"), one to a one-line thread reply (labeled "optional = the why"). Off to the side, a greyed-out separate "feedback dashboard" with a cobweb and an X, labeled "where signal goes to die".]
![[loopy-decision-surfaces-slack-feedback-1.png]]
![[loopy-decision-surfaces-slack-feedback-2.png]]
![[loopy-decision-surfaces-slack-feedback-3.png]]
![[loopy-decision-surfaces-slack-feedback-4.png]]
![[loopy-decision-surfaces-slack-feedback-5.png]]