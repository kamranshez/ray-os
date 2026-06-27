---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Start Here"
class: "start-here"
chapter: "Start Here"
---

## Start Here

This is the first video in the school, and it is the only one that is not about a tool.

It is about a single idea that sits underneath everything else you are going to learn: the work is never finished, and that is not a problem to solve. It is the shape of the job now.

If you take one thing from this entire school, take this. The constraint never disappears. It moves. Your whole job, from today onward, is finding where it moved to.

---

## The illusion of "done"

Here is the trap almost everyone walks into in their first month with AI coding.

You point an agent at your codebase, you watch it write in minutes what used to take you a week, and you feel it. The finish line. You think, "this is it, I have arrived, I am 10x now."

Then you look at the actual output of your work, or your team, or your business, and it did not move 10x. It barely moved at all.

You did not do anything wrong. You sped up the one part of the process that was already the easiest to speed up. The middle. The typing.

Cole Medin put it cleanly when he broke down Google's playbook on the new software lifecycle. Faster implementation is "not actually 10xing the output of the business," because implementation was never the only thing standing between you and the result. You drained one tank and discovered there were five more behind it.

[IMAGE: a pipeline of five tanks labeled idea, requirements, design, implementation, validation; only the middle tank drained empty while the other four stay full, a frustrated figure standing next to the one empty tank]

![[start-here-bottleneck-illusion-of-done-1.png]]
![[start-here-bottleneck-illusion-of-done-2.png]]
![[start-here-bottleneck-illusion-of-done-3.png]]
![[start-here-bottleneck-illusion-of-done-4.png]]
![[start-here-bottleneck-illusion-of-done-5.png]]

So before we name a single tool, you have to internalize why the finish line you are chasing does not exist.

---

## The law underneath it

This is not new, and it is not specific to AI. It is a law of any system that turns inputs into outputs.

In the 1980s a physicist named Eliyahu Goldratt wrote it down for factories. Every system has exactly one constraint at a time. One workstation that is slower than all the others. And here is the part that breaks people's intuition: speeding up any workstation that is not the constraint does nothing for the output of the whole line. The work just piles up in front of the real bottleneck.

Throughput is set by the constraint. Only the constraint.

Now read that again with software in your head. The agent that writes code in minutes is a workstation you just made absurdly fast. If coding was not your actual constraint, you got nothing. And if coding was your constraint, congratulations, you just moved it somewhere else, and now there is a new slowest station you have never had to think about before.

That is the whole game. Find the constraint. Dissolve it. Watch it jump. Repeat.

[IMAGE: a factory conveyor line of workstations, one station glowing red as the bottleneck with parts piled up before it, an arrow showing the red glow jumping to the next station after the first is cleared]

![[start-here-bottleneck-theory-of-constraints-1.png]]
![[start-here-bottleneck-theory-of-constraints-2.png]]
![[start-here-bottleneck-theory-of-constraints-3.png]]
![[start-here-bottleneck-theory-of-constraints-4.png]]
![[start-here-bottleneck-theory-of-constraints-5.png]]

The reason you never feel done is that there is always a constraint. The moment there is not, the system is not producing anything at all.

---

## Why it never stops, engine one: the tide rises on its own

There are two separate forces pushing the bottleneck around, and you control exactly one of them.

The first you do not control at all. The base model keeps getting better, on its own, whether you do anything or not.

Watch what that did inside Anthropic, in Boris Cherny's own words. Boris runs Claude Code. Typing used to be the throttle on how much code an engineer could produce. The model removed that throttle, and code per engineer went up eightfold. Source: https://www.youtube.com/watch?v=Z47vatpsGPI

So what happened next? All that code flooded the next station, review. A human cannot review eight times the code. So review became the constraint, and Anthropic built a product to dissolve it. That exposed security as the new slowest station, so they built for that. Then the constraint moved upstream, to whether you even had good enough ideas and specifications to point all this capability at.

Coding, then review, then security, then ideas. The interviewer watched Boris walk that whole chain and said it back to him: "you basically just keep going after the next bottleneck."

You did not move that bottleneck. The model moved it for you, by getting better while you slept. This is why Boris's advice on spending is the opposite of most people's instinct. Most teams cap it, a token budget, a cost ceiling, the "1,500 dollars per engineer" mindset. Boris says "focus almost all your effort on increasing returns," not on cutting cost, because the constraint is never the cost of the tokens, it is whether you are pointing them at the station that is actually binding.

---

## Why it never stops, engine two: you compound too

The second engine is the one you do control, and it is the one that turns this from a treadmill into a craft.

Every time you solve a problem well, you do not just solve that problem. You build something that prevents the entire family of that problem from coming back. And the moment you do that, you have raised your own floor, which means the next thing that breaks is one level higher than anything that has broken before.

Cole calls this the system evolution mindset. When you hit a bug, you do not fix it and move on. You ask the agent: where could we change our rules, our workflows, our setup, so this class of issue is less likely to ever come up again? "Every single time you go through this process over and over again, you are making it more and more reliable." Source: https://www.youtube.com/watch?v=zbmuiaPuiNM

That is you, manually, compounding. You are not just shipping output. You are upgrading the machine that makes the output. And an upgraded machine surfaces a higher-altitude bottleneck, every single time.

[IMAGE: two side-by-side engines pushing one marker labeled "the bottleneck" to the right; left engine labeled "the model gets better (outside you)", right engine labeled "you fix the class, not the instance (inside you)", both arrows converging on the same moving marker]

![[start-here-bottleneck-two-engines-1.png]]
![[start-here-bottleneck-two-engines-2.png]]
![[start-here-bottleneck-two-engines-3.png]]
![[start-here-bottleneck-two-engines-4.png]]
![[start-here-bottleneck-two-engines-5.png]]

Put the two engines together and you can see why "done" is not on the map. The model raises the floor from below you. You raise the floor from inside. The bottleneck is always being pushed somewhere new from both directions at once.

---

## The move that powers engine two: fix the class, not the instance

This is the single habit that separates someone who feels like they are drowning from someone who feels like they are compounding, so it is worth slowing down on.

When something breaks, you have two options. You can fix the instance, the one bug, the one failure, and move on. That feels fast. It is the slowest possible path, because the same shape of problem will be back next week wearing different clothes, and you will pay for it again.

Or you can fix the class. You ask: what would have to be true for this kind of mistake to be impossible? Then you build that. A rule. A check. A guardrail in your setup that catches the whole family before it ever reaches you again.

The first option keeps the bottleneck exactly where it is. The second one dissolves it and forces it to move. That is the difference between effort and leverage.

---

## The operating rule

So here is what to actually do with all of this. It is short.

Stop optimizing what is already fast. The thing that feels satisfying to improve is almost never the constraint, because if it were the constraint it would feel painful, not satisfying.

Each week, ask one question: what is actually binding right now? Not what is fun to work on. What, if it were twice as good, would actually move my output. Then point everything at that one thing until it is no longer the slowest station. Then expect it to move, and go find it again.

And do not plan in years. Both engines are shoving the constraint around faster than an annual plan can survive. Boris plans in weeks for exactly this reason. The map is redrawn that often.

One honest limit, so you do not take this too far. The chain does not dissolve every station equally. It stalls at human judgment. The model is still worse than a good human at product sense, at generating the actual ideas, at designing a hard distributed system. Boris admits this freely. Which means the one bottleneck you cannot automate away is knowing which bottleneck matters. Taste. That stays your job. And noticing where the constraint sits is precisely the skill this whole school is built to train.

[IMAGE: a simple weekly loop, four nodes in a cycle, find the binding constraint, point everything at it, dissolve it, watch it move, then back to find]

![[start-here-bottleneck-operating-rule-1.png]]
![[start-here-bottleneck-operating-rule-2.png]]
![[start-here-bottleneck-operating-rule-3.png]]
![[start-here-bottleneck-operating-rule-4.png]]
![[start-here-bottleneck-operating-rule-5.png]]

---

## The map of everything that comes next

Once you are holding this idea, the rest of the school stops looking like a pile of disconnected tools and starts looking like a toolbox, where each tool is shaped for a specific constraint.

Claude Code, for when the constraint is raw building speed. Context engineering, for when the constraint is the agent drowning in a large codebase. Prompt engineering, for when the constraint is getting the agent aligned to what you actually want. Loopy AI, for when the constraint is that you are the thing standing in the loop, and the work should keep going after you close your laptop. The business class, for when the constraint has moved all the way downstream to distribution and revenue.

You do not start at the top and grind to the bottom. You find your constraint, and you walk straight to the tool for it.

[IMAGE: a central node labeled "your current bottleneck" with spokes out to labeled tool-boxes, claude code, context engineering, prompt engineering, loopy ai, business, each box tagged with the constraint it dissolves]

![[start-here-bottleneck-the-map-1.png]]
![[start-here-bottleneck-the-map-2.png]]
![[start-here-bottleneck-the-map-3.png]]
![[start-here-bottleneck-the-map-4.png]]
![[start-here-bottleneck-the-map-5.png]]

That is what this school is. Not a course you finish. A set of instruments for a target that never stops moving.

---

## Demo

I want to show you the compounding move in one concrete loop, so it is not just a metaphor.

1. Start with a real, small bug that an agent introduced. Show the lazy fix first, patch the one line, tests pass, move on. Name it out loud as the instance fix.
2. Now do it properly. Ask the agent the system-evolution question on screen: "what class of mistake is this, and what rule or check would make this whole class impossible going forward?"
3. Watch it propose the guard. A lint rule, a test that asserts the invariant, or a line added to the project's rules file. Add it.
4. Re-run and show the guard catching a second, different instance of the same class that the one-line fix would have missed entirely.
5. Step back and name what just happened. The constraint at the start of this demo was "this bug." It is now gone, and gone for its whole family. Point at what is now the slowest part of the workflow. That is your new bottleneck. The work did not end. It moved up a level. That is the whole video in ninety seconds.

---

## Key Insight

> You will never be done, and that is not failure, it is the shape of the work. The constraint never disappears, it moves. Mastery is not "I finished," it is "I always know what is binding next."

---

## Closing

So drop the finish line. It was never real, and chasing it is what keeps people stuck optimizing things that are already fast.

The skill that compounds for the rest of your career is not any one tool in this school. It is the eye for where the constraint actually sits, today, this week. Build that eye, and every tool that comes next has an obvious place to go.

Now let us go find your first bottleneck.
