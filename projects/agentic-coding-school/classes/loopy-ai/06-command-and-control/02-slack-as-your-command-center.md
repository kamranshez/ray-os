---
video_id: "PaDaaz8z"
duration: "14-18 min"
batch: 7
order: 13
batch_name: "Command & Control"
class: "loopy-ai"
chapter: "Command & Control"
aliases: [slack-as-your-command-center, decision-surfaces]
---
Your loops are confined. Each one runs wide open on your laptop or out on Claude's cloud, with no path to anything that matters. You stopped supervising them in the last segment. So now you need one surface to do three things: watch them, feed them, and let them feed each other.

That surface is Slack.

Not because Slack is special. Because you already live there, it is already on your phone, and it gives a loop a place to talk that survives across runs. The terminal is where a loop is born. Slack is where it reports back, where you correct it, and where the next run picks up everything that happened while you were asleep.

This is the command center and the decision surface at once. Watch the fleet, leave the feedback the loops read next time they spawn, and let one loop route work to another. Three kinds of traffic, one channel.

---

## The terminal was never the interface

Here is the mistake almost everyone makes after building their first worker. They keep the terminal as the command center.

It works for one loop. You start it, you watch it, you Ctrl-C it when it goes wrong. But a fleet is the set of loops sharing one budget, one kill switch, one log directory, and a fleet does not fit in a terminal. You cannot watch five panes at once, you cannot watch any of them from your phone, and the moment you close the laptop the only window into your running loops goes dark.

And remember what we just did to these loops. We confined them, precisely so you would never sit and approve their actions again. So the terminal is not failing you as an approval console. You threw that console away on purpose. It is failing you as a window. You have loops running in boxes you cannot see into, and no way to glance at them from where you actually are.

Slack is that window. It is the surface the confined fleet reports into.

[IMAGE: dark canvas, left side a cramped terminal with five overlapping panes and a tiny laptop, an X over it; right side a single clean Slack channel on a phone with three loops posting threads into it, a check mark over it]
![[loopy-slack-as-your-command-center-terminal-vs-slack-1.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-2.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-3.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-4.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-5.png]]

---

## One channel per routine: the channel is the new stdout

Stop thinking of Slack as a notification destination. Think of it as the loop's primary output stream when it is running unattended. And give each routine its own channel.

One loop, one channel. A features routine posts into #features. A bug-log analysis routine posts into #bug-log. That channel is two things at once: the routine's logbook, the running record of everything it did, and the routine's memory, the place its next run will read before it does anything. The channel is where this loop lives.

How the message gets there does not matter much. A loop on your laptop and a loop on Claude's cloud both just need to post into their channel: a webhook, a small post step at the end of a run, whatever is simplest. You are not building infrastructure. You are giving every routine one cheap habit, when something matters, say it in your channel, and keep the routine spam in the box where it belongs.

What you read is one clean feed per kind of work. #features says it opened three pull requests. #bug-log says it found two new issues and labeled them. You scroll the channel for the work you care about right now, and the rest sit quietly in theirs. And because the action already happened safely inside the box, you are always reading after the fact. Nothing is waiting on you to read it.

[IMAGE: dark canvas. Three sealed boxes stacked, each a loop, each wired to exactly one Slack channel: box "features loop" to #features, box "bug-log loop" to #bug-log, box "deploy loop" to #deploys. Each channel shows a couple of short posts. A small loop-arrow on each channel labeled "next run reads this first", showing the channel feeds back into its own box. A phone reading the channels on the side.]
![[loopy-slack-as-your-command-center-one-channel-per-routine-1.png]]
![[loopy-slack-as-your-command-center-one-channel-per-routine-2.png]]
![[loopy-slack-as-your-command-center-one-channel-per-routine-3.png]]
![[loopy-slack-as-your-command-center-one-channel-per-routine-4.png]]
![[loopy-slack-as-your-command-center-one-channel-per-routine-5.png]]

---

## Why there are no Approve buttons here

You will see Slack setups that wire up Approve and Deny buttons. A loop hits something and waits for you to tap. It looks responsible. Resist it.

That is supervision wearing a nicer coat. A loop that has to stop and ask before it acts is a loop you are still babysitting, except now the pager is your phone instead of your terminal. You have not removed the supervision. You have made it follow you around. Same with steering, if you are jumping into the thread to redirect a loop mid-run, it was not ready to run unattended.

A confined loop never waits, because it never has to. It decides by reversibility. If the action is reversible, it just does it inside the box and notes what it assumed: "assumed staging, not prod, say so if wrong." If the action is irreversible, it does not do it at all. It collects that one dangerous edge into a pull request and ends. The merge button is the only thing that waits, and it waits for you at the gate, on your schedule.

So the run is never blocked and you are never paged. The dangerous action is the only thing that touches a human, and it touches the human gate, not an in-thread prompt. This is why bypass-permissions, full power with no confirmation, is the right default for a loop on a sealed box, the same setting Stripe runs their minions with. The urge to add an approval button is the fear that the box might not hold. If you trust the box, you do not need the button. If you do not trust the box, fix the box.

[IMAGE: dark canvas, split. Left side labeled "supervision in disguise": an Approve/Deny button pair on a phone at midnight, a tired figure tapping it, greyed and crossed out. Right side labeled "confined, never waits": one loop inside a sealed box with two outgoing arrows, a green arrow "reversible -> do it, flag assumed X" and a red arrow "irreversible -> PR, end, wait at merge gate". An arrow between the sides labeled "fix the box, not the button".]
![[loopy-slack-as-your-command-center-no-approvals-1.png]]
![[loopy-slack-as-your-command-center-no-approvals-2.png]]
![[loopy-slack-as-your-command-center-no-approvals-3.png]]
![[loopy-slack-as-your-command-center-no-approvals-4.png]]
![[loopy-slack-as-your-command-center-no-approvals-5.png]]

---

## Write messages we can decide in one tap

Here is where the channel stops being a logbook and becomes a decision surface. It hinges entirely on one habit: the loop should write its messages to make your decision easy.

The move almost everyone gets wrong is to let a loop that does judgment work answer in prose. The bug-log loop writes "this looks like it's probably a config issue, though there's some ambiguity." Fluent, reasonable, and impossible to answer quickly. To respond you would have to type a paragraph back, so you don't, and the loop never hears from you.

Now flip whose job it is. It is the loop's job to hand you a decision you can make with your thumb. So the loop posts the call, lays out the options, and tells you exactly which reaction means which choice. A refactor loop drops this into #claude-code:

> Same date-formatting logic copy-pasted in 7 files. PR #305 pulls it into one helper.
> ✅ merge it · 🔍 review first · 🚫 don't touch this again, too risky · 💬 reply and I'll walk you through it

Now you are not writing anything. You glance at your phone and tap once. Notice the shape of those options. There is the cheap yes, merge it. There is the slower path, review first. There is a boundary you can set in one tap, don't touch this again, which the loop will read and obey next run. And there is always an escape hatch, reply and I'll explain, for the rare time a tap isn't enough. The cheapest possible action from you is still a real answer.

That is the whole discipline. Every message a loop posts should arrive with the choice already framed and the reactions already laid out. And because each reaction maps to a known option, your tap is unambiguous. The loop reads it back next time it runs and knows precisely what you picked, no parsing, no guessing. Make it easy to decide, and you will actually decide, which is the only way the loop ever learns what you want.

[IMAGE: dark canvas. Center, a Slack message from a loop in a channel header reading #claude-code, on a phone. The message reads "Same logic copy-pasted in 7 files. PR #305 pulls it into one helper" and below it lays out an explicit reaction key: "✅ merge it   🔍 review first   🚫 don't touch again   💬 reply and I'll explain". A thumb is tapping one emoji. A small arrow loops from the tapped reaction back into a box labeled "next run reads your pick". Off to the side, greyed and crossed out, a loop posting a wall of prose with a frustrated human having to type a long reply, captioned "hard to answer = no answer".]
![[loopy-slack-as-your-command-center-present-options-1.png]]
![[loopy-slack-as-your-command-center-present-options-2.png]]
![[loopy-slack-as-your-command-center-present-options-3.png]]
![[loopy-slack-as-your-command-center-present-options-4.png]]
![[loopy-slack-as-your-command-center-present-options-5.png]]

---

## Your reaction is the only signal that counts

So who labels the training data? Nobody. You just do your job, and your reaction is the ground truth.

There are two surfaces and they work the same way. On a pull request, you merge, you comment, or you close. On a labeled post in the channel, you tap an emoji for what you actually did, or you reply a line of why. The emoji is the corrected label. The reply is the reason. One click is enough signal, the thread is extra context, and both cost you almost nothing because they live in the place you never left.

The rule for what counts has to be strict, or the signal rots. A merge, a thumbs up, an agreeing reply is positive. A close, a thumbs down, an edit, a flipped label is a deviation, the thing the loop should learn from. And silence is nothing at all. An unmerged PR is just pending, not a rejection. A post you scrolled past is not approval. Only an explicit reaction is signal, so your backlog and your busy days never get mistaken for "good job, keep doing that."

What you are actually capturing, every time you flip a label or close a PR, is your taste, the judgment call you might never be able to fully write down. The deviation is your taste made measurable. The failure mode is making that reaction expensive. The moment feedback needs a separate app, a form, or a meeting, participation dies and the decision surface goes quiet. Keep it at one tap and the signal keeps flowing.
Source: https://x.com/petradonka/status/2054897826149101588
Source: https://x.com/zachlloydtweets/status/2066908445425496348

[IMAGE: dark canvas. Center, a Slack channel post on a phone: a labeled decision chip and a linked PR. Three reaction paths drawn as short arrows: a green "merge / thumbs up / agree" arrow to a bin labeled "positive", a red "close / thumbs down / flip label" arrow to a bin labeled "deviation (learn)", and a greyed "scroll past / leave pending" arrow to a crossed-out bin labeled "no signal". Caption: "explicit only, silence is neutral".]
![[loopy-slack-as-your-command-center-reaction-is-signal-1.png]]
![[loopy-slack-as-your-command-center-reaction-is-signal-2.png]]
![[loopy-slack-as-your-command-center-reaction-is-signal-3.png]]
![[loopy-slack-as-your-command-center-reaction-is-signal-4.png]]
![[loopy-slack-as-your-command-center-reaction-is-signal-5.png]]

---

## The loop reads it next time it spawns

Now the part that makes the channel a memory and not just a record. Your reactions are sitting in the channel. The loop is asleep. Then its schedule fires.

The first thing the next run does is read its own channel since the last time it ran. It sees the PR you merged and the two you closed. It sees the label you flipped from P1 to P2 and the one-line reason you left. And it adjusts this run accordingly, before it does any new work. You corrected it once, in passing, from your phone, and the correction shows up in its behavior the very next morning without you teaching it anything on purpose.

That is the whole loop. Report into the channel, you react in the channel, the next run reads the channel. The channel carries your taste forward across runs that share nothing else.

Be clear about the boundary, though. Reading the channel makes the next run smarter about recent corrections. It does not yet make the routine permanently better. Turning a pile of repeated deviations into an updated skill, so the lesson generalizes instead of being re-read as raw history forever, is its own move. That is the [[self-improvement-loop]], and it is the next thing we build. For now, hold the simpler shape: the channel is the routine's short-term memory, and your reactions are what is written into it.

[IMAGE: dark canvas, a horizontal timeline of one routine. Run 1 inside a box posts decisions to its channel. In the gap, a phone drops reactions onto those posts (a merge, a flipped label). Run 2 (the box again, later) has a bold arrow reading FIRST from the channel into the box labeled "reads since last run", then acts differently. A faded gear off to the side labeled "self-improvement-loop: distills into a skill (next video)".]
![[loopy-slack-as-your-command-center-memory-next-spawn-1.png]]
![[loopy-slack-as-your-command-center-memory-next-spawn-2.png]]
![[loopy-slack-as-your-command-center-memory-next-spawn-3.png]]
![[loopy-slack-as-your-command-center-memory-next-spawn-4.png]]
![[loopy-slack-as-your-command-center-memory-next-spawn-5.png]]

---

## Loops feeding loops

So far you are on one end of the channel. There is a third kind of traffic that does not involve you at all.

Once every routine has a channel, a loop can read across all of them. Picture a skimmer, a routine whose whole job is to read the other channels. It finds work, three stale bugs nobody triaged, and it posts them into #bug-log as items for that routine to pick up next time it spawns. It analyses loops, #features has opened five PRs this week and you closed every one, and it posts that observation into a roll-up channel so you see a loop that is quietly misfiring.

Notice the hard limit on what it does. The skimmer only ever posts. It routes work into other channels and it writes analysis, and that is all. It never opens a PR, never acts, never reaches into another loop and runs it. The dangerous capability still lives only inside the confined routines and behind the merge gate. A loop reading another loop's channel is just one more reader, and a reader cannot hurt you.

That is the point of treating channels as the shared surface. One read-only skimmer can watch your whole fleet, surface the work that fell through the cracks, and flag the loops that have gone off the rails, all without a human in the path and without ever touching anything it could break. Same surface, three kinds of traffic: loop to you, you to loop, and loop to loop.

[IMAGE: dark canvas. Several routine channels in a column (#features, #bug-log, #deploys), each fed by its own boxed loop. A single "skimmer" loop on the left with read-only eyes drawn reading from all of them. Two outputs from the skimmer, both dashed and labeled "posts only": one arrow dropping a work item back into #bug-log, one arrow posting "#features misfiring: 5 PRs, 5 closed" into a #roll-up channel. A bold crossed-out arrow from the skimmer to a PR/merge icon labeled "never acts".]
![[loopy-slack-as-your-command-center-skimmer-routes-1.png]]
![[loopy-slack-as-your-command-center-skimmer-routes-2.png]]
![[loopy-slack-as-your-command-center-skimmer-routes-3.png]]
![[loopy-slack-as-your-command-center-skimmer-routes-4.png]]
![[loopy-slack-as-your-command-center-skimmer-routes-5.png]]

## Key Insight

> You confined your loops so you would never supervise them again. Slack is what is left: one channel per routine, where the loop reports, where your reaction is the only signal that counts, and where the next run reads your corrections before it starts. Make the output a labeled decision, never an Approve button. The channel is the loop's memory, your one-tap steering, and the bus your loops use to feed each other, all at once.
