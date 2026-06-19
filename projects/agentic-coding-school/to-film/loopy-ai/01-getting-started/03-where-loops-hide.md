---
duration: "10-14 min"
batch: 1
order: 3
batch_name: "Setup"
class: "loopy-ai"
chapter: "Intro"
aliases: [where-loops-hide, finding-loops, message-bus]
---
You don't add loops to your work. You find them.

That's the part people get backwards. They hear "write loops instead of prompts" and picture sprinkling automation on top of everything, building robots for the sake of building robots. That's not it. The loops are already in your day. They're already running. The only problem is that the thing closing them, over and over, is you.

So the first real skill of this whole class isn't building a loop. It's spotting one. Looking at an ordinary afternoon of your work and seeing the loop-shaped holes you've been filling with your own hands.

This segment is about how to find them. There are a few reliable tells, and one of them is so common and so high-signal that once you learn to see it, you'll see it everywhere.

---

## A loop is already there, wearing you as a costume

Go back to the map from the intro. The shape of a loop never changes. Decide what matters, do it, check it, go again. What changes across the eight levels is only how long a turn takes and who's closing it.

For almost everything you do, the answer to "who's closing it" is still you.

That's what a loop-shaped hole is. It's a spot in your work where the cycle is already happening, on its own cadence, with its own check and its own repeat, and you happen to be the component sitting in the middle of it. You're not deciding much. You're keeping the cycle turning.

Finding a loop means finding one of those spots. Not inventing a new process. Catching an existing one with your face in it.

So how do you spot them? You learn the tells.

---

## The strongest tell: you're acting as a message bus

Here's the one that catches the most loops, by far.

Watch for the moments where your actual job is to carry information from one place to another. You take the output of one thing and you hand it to the next thing. You read the error and paste it into a prompt. You copy the review comments off the pull request and paste them into the agent. You take the plan out of this thread and feed it into that thread. You read what the dashboard says and you go tell someone.

In every one of those, you are a message bus. You're the wire between two systems. The information needed to flow from A to B, and the way it flowed was through you, by hand.

[IMAGE: dark canvas, two system boxes on the left and right labeled "A" and "B", a small human figure in the middle with arrows passing THROUGH it carrying labeled packets "error", "review comment", "plan", the human glowing red as the wire where everything funnels]

![[loopy-msgbus-tell-1.png]]
![[loopy-msgbus-tell-2.png]]
![[loopy-msgbus-tell-3.png]]
![[loopy-msgbus-tell-4.png]]
![[loopy-msgbus-tell-5.png]]

This is the highest-signal tell for a reason. When you're being a message bus, two things are almost always true at once. The work has no judgment in it, copying a comment from one window to another is not a decision, and it repeats, because information always needs carrying again next time. No taste, plus repetition, is the exact signature of something that wants to be a loop.

And it should sting a little, because it means you're spending your scarcest resource, your attention, on being plumbing. The agent can generate a fix in twelve seconds. Then it waits hours for you to notice the comment came in and paste it across. You're not the genius in that loop. You're the latency.

So the first question in any loop hunt: where am I just moving information around? Every honest answer is a loop you've found.

---

## Two more tells worth knowing

The message bus is the big one. Two others catch most of what's left.

**The thing you always do after "done."** Pay attention to the ritual that fires every single time an agent finishes a task. You run the dev server. You click around to see if it works. You commit. You push. You open the PR. You wait for the bots. It's the same sequence every time, in the same order, triggered by the same event. A fixed sequence that always follows the same trigger is not a habit. It's a loop body you happen to be executing manually.

**The watch-and-react.** Notice where you keep checking something and only act when it changes. You refresh the PR to see if review came in. You glance at the revenue dashboard. You skim the issues tab. You're polling, and reacting on a condition. Polling on a cadence and acting on a change is a loop with the trigger and the check already fully specified. You're just being the cron job yourself.

[IMAGE: dark canvas, three labeled "tell" cards in a row, each a small icon. Card 1 "MESSAGE BUS": human passing a packet between two boxes. Card 2 "AFTER DONE": a repeating chain of icons run-commit-push looping back. Card 3 "WATCH AND REACT": an eye staring at a dashboard with a refresh arrow. A magnifying glass hovering over all three]

![[loopy-loop-tells-1.png]]
![[loopy-loop-tells-2.png]]
![[loopy-loop-tells-3.png]]
![[loopy-loop-tells-4.png]]
![[loopy-loop-tells-5.png]]

Three tells. Am I carrying information by hand? Am I running the same sequence after every "done"? Am I watching something and reacting when it changes? Any yes is a candidate loop. Most afternoons have several.

---

## You found one. Now what?

Spotting the loop is the skill this segment is teaching. Closing it is the rest of the class. But here's the shape of what comes next, so the hunt has a point.

Once you've found a loop you're sitting in, getting out is two moves.

**Move one. Hand the next step to the agent.** Whatever you were about to do by hand, the thing you do after "done," the comment you were about to paste, tell the agent to do that instead. Each handoff is a prompt you never write again.

**Move two. Ask the agent to build the loop.** This is the leverage, and it's why the class exists. You don't have to wire the loop together yourself. You describe the outcome and the rails, and the agent builds an orchestration shaped to this exact problem. We'll do real versions of this all the way up the stack.

For now, just hold the order of operations: find the loop first, then close it. You can't automate a loop you haven't noticed you're in.

---

## One caution: not every loop-shaped hole should become a loop

A tell tells you a loop *could* exist there. It doesn't tell you it *should*.

The line is judgment. When you're a message bus, you're moving information and making no decision, that's the safe stuff to automate. But sometimes the thing that looks like ferrying is actually a checkpoint in disguise. Reading a review comment and deciding whether the fix is even right is a decision. Approving a merge is a decision. Spending real money is a decision.

So when you find a candidate, ask one more question: is this carrying, or is this a call? Automate the carrying. Keep yourself on the calls, especially the irreversible ones. Merging to main, publishing, spending. Those are gates, and gates get a human. Everything leading up to the gate is fair game.

Find the loop. Strip out the ferrying. Keep yourself on the gate.

---

## Demo

Let's do an actual loop hunt on a real afternoon of work.

1. Open up your day. Pick one real task you ran with an agent recently, from the prompt all the way to merged. Write down, honestly, every single thing you personally did after the agent first said "done."
2. Go down the list and tag each line with a tell. Is it message bus, you carrying information? Is it the after-"done" ritual? Is it watch-and-react? Most lines will get a tag. The ones that do are the loop you've been closing by hand.
3. Find the fattest one. Usually it's the review ferrying, copying bot comments into the agent over and over. That's the message bus at its most obvious.
4. Mark the gate. Find the one or two lines that are actually decisions, the merge, the "ship it." Circle those. Those stay yours.
5. Now you can see the whole loop on paper. Everything tagged as a tell is the loop body. The circled lines are the gate. That picture is the spec for the thing you'll build in the next chapters.
6. Notice you didn't build anything yet. You just found it. That's the rep. Do this hunt on three different tasks and you'll never not see the loops again.

---

## Key Insight

> You don't add loops to your work, you find them, because they're already running with you sitting in the middle. The fastest way to spot one is to catch yourself acting as a message bus: carrying information from one place to another by hand, no judgment, on repeat. No taste plus repetition is the signature of a loop wearing you as a costume.

---

## Where we go next

You can spot the loops now. That's the hard part, and most people never even get there.

But finding a loop and building the thing that replaces you in it are two different skills. Before you can hand off a whole chain of "run, check, commit, review, fix," you need the smallest real loop underneath all of it: an agent builds something, and a second agent checks it. Get that one right and every bigger loop in this class is just that pattern, stacked.

That's the builder and verifier. The first loop you'll actually build. Let's go.
