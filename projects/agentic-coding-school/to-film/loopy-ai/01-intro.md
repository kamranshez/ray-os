---
duration: "8-12 min"
batch: 1
order: 1
batch_name: "Setup"
class: "loopy-ai"
chapter: "Intro"
aliases: [intro]
---

The guy who built Claude Code uninstalled his IDE six months ago. He hasn't opened one since. His job, in his own words, is to write loops.

Most people hear that and assume he means a cron job. Or a while loop. Or one of those overnight scripts where you tell Claude to keep going until it's done.

He doesn't mean any of those things. He means something bigger. And almost nobody is doing it yet.

Once you learn to see them, loops are everywhere. A developer's inner loop is write, run, read the error, fix, run again. Project management is a loop: plan the sprint, ship it, review what happened, plan the next one. A CEO runs a loop measured in weeks instead of seconds, set the bet, watch the numbers, correct course, repeat. Zoom out far enough and an entire startup is one big loop wrapped around a stack of smaller ones, all the way down to a single keystroke.

The shape never changes. Decide what matters, do it, check it, go again. What changes is two things: how long one turn of the loop takes, and who, or what, is the one closing it. For most of history the answer to that second question was always a human. That is the part coming loose. The moment a loop can close itself, the person who used to sit inside it gets to step up a level and start writing the loop instead of being it. That move, repeated at every altitude, is the whole story of this class.

This class is the map for that territory.

Source: Boris Cherny on Acquired Unplugged, June 2026.

---

## Three engineers walk into a bar

Three engineers tell you "I built a loop."

The first one wired up a builder and a verifier. Write code, run the tests, fix the failures, run them again. That's a loop.

The second one set up a cron job that pings Claude every hour to check on something. That's also a loop.

The third one has two hundred Claudes running right now. They watch Slack, GitHub issues, Twitter, and customer support tickets. They decide what should be worked on next. That's a loop too.

They're all right. They're all pointing at completely different things.

And if you can't tell them apart, you can't reason about them. You can't decide which one to build, when, or how to keep it from burning your whole monthly token budget in an afternoon.

[IMAGE: three speech bubbles from three different engineers, each saying "I built a loop", each bubble pointing at a different diagram below it]

![[images/intro/three-engineers.png]]

---

## Why now

This wasn't possible twelve months ago.

Three things converged in 2025 and 2026. The context window got long enough to hold a real task. Inference got cheap enough to run a fleet. And the models got good enough to verify their own work — under specific structural conditions you have to actually build.

That third one is the one most people miss, and it's the one I have to qualify. Models do not magically verify themselves. GPT-5 was caught fabricating "passed" results on 76% of a benchmark when graded honestly. SWE-bench self-reports overstate completion by 35 points against ground truth. Self-grading is still vibes wearing a loop costume. What changed is that we now know how to structure the loop so verification actually bites: prompt asymmetry, borrowed verifiers from outside the model, and the three-role split we'll get to in the back half of the class. Build those scaffolds and the model can tell the difference between "I did it" and "I think I did it." Skip them and every long-running agent is a slot machine, same as it was twelve months ago.

The economics flipped. Not "AI got smarter." The shift that matters to you is that it's now affordable to run dozens of agents continuously, and reliable enough that they're worth running at all.

---

## The map

There are eight levels of loop. They nest. Each one wraps the one below it.

[IMAGE: vertical stack diagram, L0 at the bottom, L7 at the top, each level a labeled box, the boxes nested inside each other matryoshka-style]

![[images/intro/loop-stack.png]]

At the bottom is the model generating tokens. You don't touch that. Level zero.

Above that, the agent harness. Think, tool call, observe, think, tool call. One task, one context window. This is what Claude Code is when you open it. Most people stop here and call this "using AI." Level one.

Above that, the builder and verifier. Build, test, fix, test. If you've ever wired up a closing the loop pattern, you've built one. Level two.

Above that, the full task lifecycle. Spec, plan, build, review, push. Ralph loops live here. Goal mode lives here. This is where the "overnight Claude" stories on Twitter actually happen. Level three.

Then it gets interesting.

Level four is the worker loop. An agent that picks its own work from a queue without being told each time.

Level five is the discovery loop. An agent that doesn't do the work, it decides what *should become* work. This is where Boris's two hundred Claudes live.

Level six is governance. The loop that watches the other loops, kills the misbehaving ones, retires the stale ones, allocates the token budget. Once you have twenty loops running, you need this or your token bill detonates.

And level seven is you. Deciding which loops should exist at all.

That's the map. The class is a walk up it.

---

## Where you are right now

Be honest about your starting point. It makes the next few hours land harder.

If you've used Claude Code, you're at level one.

If you've written a closing the loop pattern, build, test, fix, test, you've touched level two.

If you've ever fired off a Ralph loop or used goal mode, you've touched level three.

Almost nobody listening to this is operating at level four or above. That's not a problem. That's the opportunity. The territory above level three isn't crowded yet, because almost no one has the vocabulary to even talk about it.

---

## What this looks like in practice

[VISUAL: cut to screen reveal, desktop with 10 to 15 Claude windows open, each doing something different, hold for 4 seconds in silence before voiceover resumes]

![[images/intro/desktop-fleet.png]]

This is what working looks like for me now.

One of those windows is mining Japanese sentences from a video I watched last night. Another is scanning a watchlist of YouTube channels for outlier videos in my niche. Another is going through GitHub issues on a side project, deciding which ones are worth pulling into the next sprint. Another is watching my Stripe account and pinging me if revenue does something weird.

None of those needed me to type anything today. They run on their own. I designed them once and they keep going.

That's level four and five. By the end of this class you'll have built one of these on something you actually care about. And you'll know how to design more.

---

## What I'm promising

Two things.

First, a built thing. By the end you will have one running loop, on your own work, that is still running when you close your laptop. Not a demo. A loop that earns its keep.

Second, the vocabulary. You'll be able to look at someone's "I built an agent" post and immediately know whether they built an L2, an L4, or an L5. And what that means about what they had to figure out, and what they got to skip.

That second one matters more than people realise. Almost every confused conversation about AI agents right now is two people pointing at different levels of the stack, assuming they mean the same thing. Once you can see the levels, the confusion dissolves.

---

## What this class is not

A few things to clear up.

It is not a tutorial on Claude Code basics. If you've never opened it, go watch the Claude Code class first and come back.

It is not a tour of every prompt trick. Prompts are the easy part. The whole thesis is that the work lives in everything *around* the prompt.

It is not a hype reel. Loops burn tokens. They make mistakes at scale. They create failure modes you have never had to think about before. We're going to be honest about all of that as we go.

What it is. A walk up the stack. One worked example at each level. Ending with you having built something that runs when you're not watching it.

---

## Key Insight

> A loop isn't one thing. It's eight things stacked on top of each other. Once you can name the level you're at, you can see the level you haven't reached yet.

---

## Where we go next

Before we get to level four, we have to be honest about what level one actually is. Most people misuse the word. They think they're "using AI" when they're doing something much smaller than that.

Once you see what level one really is, the rest of the stack starts to make sense.

That's the next segment. Let's go.
