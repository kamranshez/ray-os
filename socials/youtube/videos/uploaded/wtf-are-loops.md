---
duration: "10-12 min"
batch: 0
order: 0
batch_name: "Promo"
class: "loopy-ai"
chapter: "Trailer"
status: draft
---

The guy who built Claude Code, on a podcast last week: *"I don't prompt Claude anymore. What I mostly use now is loops. I create loops, they do the rest of my job."*

Another engineer, same week: *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*

A third, same week: *"Subagentmaxxing. /goal plus subagents, depth two. You replace your oversight with another agent, then theirs with another."*

Three people. Same week. Same shift.

The unit of work just changed.

Now, I've been teaching this in my classes for months. Link down below if you're interested.

---

## Three stages, pick yours

Boris, the guy who built Claude Code, tells it as three stages. Placing yourself on his ladder is the fastest way to get this.

A year ago he wrote code by hand with autocomplete. One human, one cursor, one file at a time. Stage one.

Then he started running five to ten Claude sessions in parallel and prompting each one. Window-tiling. Juggling agents. Still in the loop, still firing the prompts, just firing them at a fleet. Stage two.

Now he doesn't prompt at all. He writes the loops that prompt Claude. A couple hundred agents read his GitHub, his Slack, and his Twitter, and they decide what to build next. He has the receipt for stage three because he's living it.

Most people watching this are somewhere between stage one and stage two. That's fine. The point of this video, and the class, is the bridge from there to stage three.

![[images/wtf-are-loops/three-stages/excalidraw_1.png]]
![[images/wtf-are-loops/three-stages/excalidraw_2.png]]
![[images/wtf-are-loops/three-stages/excalidraw_3.png]]
![[images/wtf-are-loops/three-stages/excalidraw_4.png]]
![[images/wtf-are-loops/three-stages/excalidraw_5.png]]
![[images/wtf-are-loops/three-stages/excalidraw_6.png]]
![[images/wtf-are-loops/three-stages/excalidraw_7.png]]

---

## Where we've seen this so far

You've probably been bumping into loops without naming them.

There's the /loop command. It re-fires a prompt on a schedule. You've seen it. You've probably used it.

There's /goal. Codex has it. Claude Code has it. You give the agent an objective, the runtime owns a state machine, the loop runs until the objective is genuinely met. The runtime can't be sweet-talked into declaring victory early.

There's auto research. The agent runs an experiment, scores itself against binary evals, mutates the codebase and the files on disk, keeps anything that improved the score and discards everything else. Karpathy-style. The loop is optimising the code itself, run after run.

There's the Ralph loop. Same prompt, fresh context window, run it again. You let it grind for hours because every iteration sees the previous iteration's git history and picks up where the last one left off.

Goal. /loop. Auto research. Ralph.

Different commands. Different vocabularies. Same idea underneath. Something fires the loop. The loop runs. Something checks whether it's done.

Until now you've probably seen each of these come up independently. They sit in different tweets, different docs, different blog posts, and nobody bothers to point out that they're the same shape. They are. Whichever family fires your loop, the rest of this video applies.

![[images/wtf-are-loops/where-weve-seen-this/excalidraw_1.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_2.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_3.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_4.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_5.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_6.png]]
![[images/wtf-are-loops/where-weve-seen-this/excalidraw_7.png]]

---

## A loop is a unit of work

You have probably been running loops without naming them.

Think about the last feature you shipped. You worked with the agent on spec. The agent built it. You told it to run a couple of rounds of code review. You got an agent to use a browser to verify it. Then you deployed it.

You may have then told it to monitor the logs for changes after it was deployed and fix them.

That whole thing was one loop. One unit of work.

What changed isn't the shape. What changed is who sits in the middle of it.

At stage two, you used to sit *inside* the loop. You'd prompt the next step, get the agent to use a skill to fix the bugs. Then you'd prompt the step after that, tell it to open the browser and verify. You were the thing moving between steps. The unit of work was a prompt, and you ran the loop manually.

At stage three, you design the loop and the loop runs without you. You also design what fires it. A spec goes in at the top, and the whole thing runs through to the merged PR without you in the middle. The unit of work is *a loop*, and you run a portfolio of them.

There are a lot of angles you can take on this idea. This video takes one of them. Loops as disposable units of work, with surfaces you interact through, that you compose into bigger loops.

![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_1.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_2.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_3.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_4.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_5.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_6.png]]
![[images/wtf-are-loops/disposable-unit-of-work/excalidraw_7.png]]

---

## What makes up a loop

This part isn't obvious, so it's worth slowing down on.

You don't sit at a blank document and write the loop spec yourself. You go back and forth with the agent. You sketch the shape. The agent pushes back on what's vague. You iterate until the loop has six things settled before it ever runs.

Inputs. Action. Check. Memory. Exit. Surface.

The first five are the body of the loop. The sixth is where you and the loop actually meet. We'll come back to memory and surface in a minute.

That conversation with the agent is the work. The agent helps you design the unit that will eventually run without you in the chair.

This is the move most people skip. They jump straight to *can I get an agent to do X for me*, hit the first bad output, and walk away. The unlock is sitting with the agent first and designing the unit together. The agent has read more loops than you have. Use it.

[IMAGE: two-panel diagram, left panel a person and an agent passing a sketch back and forth labeled "co-design", right panel a finished loop diagram with six labeled boxes for inputs, action, check, memory, exit, surface]

![[images/wtf-are-loops/co-design-the-loop.png]]

I'll have a separate video on this, so stay subscribed.

![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_1.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_2.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_3.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_4.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_5.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_6.png]]
![[images/wtf-are-loops/what-makes-up-a-loop/excalidraw_7.png]]

---

## Outer loops

Now you go up a level.

The outer loop decides *which* task the inner loop runs next. Same inner loop. Different choices for the outer.

The first one is a scheduled outer loop. Every morning it grabs the next ticket off the queue and hands it to the inner loop. You wake up, your laptop is humming, three pull requests are sitting there ready to review.

The second one is a competitor monitor. It watches a competitor's changelog or their public site. The moment they ship something new, it specs the equivalent for you and hands the spec down to the task loop. You did not type a thing.

Two outer loops. Same inner loop underneath. The shape of the inner loop didn't change. The thing that *triggers* it did.

That's depth two. The agent that watches the agent.

[IMAGE: nested boxes, outer box labelled "outer loop: scheduled trigger / competitor monitor", inner box labelled "inner loop: task to PR", arrow from outer down into inner]

![[images/wtf-are-loops/inner-outer-loops.png]]

![[images/wtf-are-loops/outer-loops/excalidraw_1.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_2.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_3.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_4.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_5.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_6.png]]
![[images/wtf-are-loops/outer-loops/excalidraw_7.png]]

---

## A quick aside

Before the second example, fair warning. This video is the trailer for the Loopy AI class. The class drops next week. The link in the description is the early-bird price, and it goes up the day the class launches. Fourteen day money back, no questions.

If any of this is landing for you, click the link, lock the price in, then come back. I'll wait.

Now back to it.

---

## Memories for loops

Every loop needs a memory. A place where it parks state between turns. And it needs a surface, the place where you and the loop actually meet.

In practice these are the same thing. Where the loop writes its memory is where you read it. The choice you're making is one choice with two names.

There are two real options.

A file system. Files on disk that the loop reads and writes. The surface is your terminal, or your editor. Spec docs. Progress logs. Action histories. Anything you'd want to look back at like a notebook. Great for fast loops, where you want to grep the trail later, diff between runs, recover state if the loop crashes.

A Slack thread, or any chat channel. The surface is your phone, or Slack on your laptop. Great for the slower loops, the ones whose feedback can't come back instantly. An SEO loop waiting days for analytics. A cold email loop waiting for replies. A research loop that surfaces something interesting and waits for you to react before it goes deeper. The loop posts. You react. The loop reads your reaction and takes its next turn. Codex has thread automations that wire this up cleanly. We cover the setup in the class.

The file system is the loop's notebook. Slack is the loop's conversation with you.

Which one you pick depends on how long the loop has to wait between turns. If it can take its next turn in a second, files. If it has to wait hours or days for a signal, Slack.

![[images/wtf-are-loops/memories-for-loops/excalidraw_1.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_2.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_3.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_4.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_5.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_6.png]]
![[images/wtf-are-loops/memories-for-loops/excalidraw_7.png]]

---

## Worked example two, the email loop

Say you're sending a thousand cold emails a day. Boring, repetitive, the kind of thing nobody actually wants to optimise by hand.

Take twenty percent of those, two hundred emails a day, and run them through a loop instead.

The inner loop is the writer. Each day it tweaks the wording. Different opener. Different CTA. Different subject line. Small, deliberate variations on the control. Then it surfaces the batch it's about to send to a Slack channel and waits for you to react. Thumbs up, the batch goes out. Thumbs down, it tries again.

You're the human in the inner loop. The decision is yours. Slack is the surface.

The next morning, the loop runs again. New variations. Another check-in. Another decision. It keeps going.

Now wrap the outer loop around it. The outer loop is the analyst. It has access to reply rates, open rates, meetings booked. Every few days it pulls the data, compares the variations against the control, and posts the insights back to the same Slack channel.

*The subject lines with a question outperformed by eighteen percent. The shorter openers underperformed by twelve. Kill the long ones, double the question-based subject lines.*

You read it on your phone. You make the call.

Slack is both the surface and the memory. The whole channel is the loop's record of what it tried, what you said yes to, what you said no to, and what the data said about all of it.

[IMAGE: three-column diagram, left column "inner email loop, writes variations", middle column "outer loop, checks reply rates", right column "Slack channel, surface and memory" with a phone icon]

![[images/wtf-are-loops/email-loop.png]]

This shape generalises. Same skeleton for ad campaigns, for SEO, for content, for outbound, for product analytics. Inner loop does the work. Outer loop checks whether the work mattered. Slack is the surface between you and both.

![[images/wtf-are-loops/email-loop/excalidraw_1.png]]
![[images/wtf-are-loops/email-loop/excalidraw_2.png]]
![[images/wtf-are-loops/email-loop/excalidraw_3.png]]
![[images/wtf-are-loops/email-loop/excalidraw_4.png]]
![[images/wtf-are-loops/email-loop/excalidraw_5.png]]
![[images/wtf-are-loops/email-loop/excalidraw_6.png]]
![[images/wtf-are-loops/email-loop/excalidraw_7.png]]

---

## Entropy is the part nobody warns you about

Here is the trap.

Loops compound while you sleep. So does slop.

A bad commit goes in. The next iteration treats that bad commit as canon. The pattern repeats. Two weeks in, you have a ball of mud that looks like progress but is actually decay.

This is the failure mode that kills most of the loops people try to build. They get the agent running, they let it cook, they come back to garbage at scale.

The fix is a code review step built into the loop, not a thing you remember to do later. And the reviewer cannot be the same agent that wrote the code. You need an adversarial reviewer. Something with no ego in the work, willing to be ruthless.

Wherever possible, the reviewer shouldn't even be looking at the model's word. It should be looking at an oracle outside the model. Tests passing. Lighthouse scores. Real production errors. Stripe revenue numbers. Reply rates. Things the model cannot sweet talk.

That is what stops the slop.

![[images/wtf-are-loops/entropy/excalidraw_1.png]]
![[images/wtf-are-loops/entropy/excalidraw_2.png]]
![[images/wtf-are-loops/entropy/excalidraw_3.png]]
![[images/wtf-are-loops/entropy/excalidraw_4.png]]
![[images/wtf-are-loops/entropy/excalidraw_5.png]]
![[images/wtf-are-loops/entropy/excalidraw_6.png]]
![[images/wtf-are-loops/entropy/excalidraw_7.png]]

---

## Why this matters

The pattern in software is the same pattern, every decade. It's historically routed, not a vibe.

In the 1940s, you programmed computers by punching holes in cards. You were the one moving the bits. The unit of work was a physical card.

Then assembly came along in the late 1940s. You wrote mnemonics for machine instructions. You weren't toggling bits anymore, you were writing symbols. One level up.

Then high-level languages came along. FORTRAN in 1957. C in 1972. You wrote what you wanted, the compiler turned it into assembly for you. Another level up.

Then libraries. You stopped writing the same primitives over and over. You called code other people had written. Another level up.

Then frameworks. Rails. Django. React. Code other people had written that called *yours*. Inversion of control. You filled in the parts that were specific to your app, and the framework ran the loop. Another level up.

Then prompts. You stopped writing code at all for entire categories of work. You wrote intent. The model wrote the code based on the framework.

And now loops. You stop typing the prompts. You design the unit that fires the prompts, that fires the agents, that ships the work.

Every leap is the same leap. You stop being the thing that runs. You design the thing that runs. The leverage moves up one level.

Loops compound while you sleep. Prompts don't.

That is the whole pitch.

![[images/wtf-are-loops/why-this-matters/excalidraw_1.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_2.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_3.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_4.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_5.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_6.png]]
![[images/wtf-are-loops/why-this-matters/excalidraw_7.png]]

---

## What we cover in the class

This video was the overview. The class goes much deeper into the parts I deliberately skipped here.

**Exit conditions.** The prompt stops being the hard part the moment you start running loops. The exit condition becomes the whole game. A while loop that re-prompts is trivial. Knowing when the agent is *done* versus *stuck* versus *confidently wrong* is the entire job. Three different failure states. Three different signals. We walk through each.

**Writing the goal itself.** A real goal condition is three things. A measurable end state. A stated check. A constraint set. Most people write subjective conditions that the model gleefully self-reports as complete. We walk through the nine-section template that fixes that.

**Deliverables.** Loops that drop artifacts on a regular cadence. Daily reports. Weekly PRs. Slack summaries. So the loop's output is the thing you actually consume, not a buried log file you have to go dig for.

**Kill switches.** So an unbounded loop doesn't quietly eat a week of your token budget while you're at a conference. The kill switch is the design, not the loop body. We cover token budgets, action log review, and retirement rules that fire automatically.

**Memory done right.** A loop with no memory starts from zero every run. A loop with memory remembers every mistake and repeats it. A loop that learns turns those mistakes into rules it has to follow. Memory is a footgun before it's an upgrade. We cover the three tiers and which one you actually want.

**Borrowed verifiers.** Three categories of external oracle, how to hunt for one for your specific loop, and how to wire it into CI so every commit is one iteration.

**The three-role split.** Generator does. Reflector reviews. Curator updates the playbook. Why this is the structure that lets your taste files survive a model swap.

**Strip the model out.** Before you let a model anywhere near your loop, build one with cron and bash and a static rubric. Hands-on. So you can see what the loop actually is, with the model factored out.

**Mission command.** The German military doctrine of auftragstaktik. Intent documents instead of orders. The operating model for running a fleet of loops, not just one.

**The discovery layer.** Stage three at scale. Hundreds of agents whose entire job is to decide what should *become* a loop, reading your GitHub, your Slack, your inbox. We won't get you to two hundred. We will get you to ten.

That is the class.

---

## Humble close

Look. I don't have all the answers here. I'm still figuring this out, and so is everyone else.

The vocabulary is two months old. The patterns are still being named. Half of what I just walked through, I learned this month. The people writing the most useful things about loops right now are figuring it out in public the same way I am.

But this is where things seem to be heading. The unit of work is moving from a prompt to a loop. The leverage is moving from how well you write a prompt to how well you design the unit that runs without you.

If that's the direction you want to be moving in, the class is the fastest way I know to get there.

---

## Key Insight

> A prompt asks for work. A loop keeps finding, doing, checking, and learning. The leverage moved up one level. So should you.

---

## Closing beat

If you're still typing prompts one at a time, you're still being the loop.

The class drops next week. Lock the early bird in before it goes up.

See you in there.
