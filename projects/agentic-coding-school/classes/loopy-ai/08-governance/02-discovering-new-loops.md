---
duration: "10-14 min"
batch: 7
order: 26
batch_name: "L6 Governance"
class: "loopy-ai"
chapter: "Discovering New Loops"
status: "scripted"
aliases: [discovering-new-loops]
---

You have spent this entire class learning how to build a loop. This segment is about the question that decides whether any of it pays off: which loops are worth building in the first place.

Because here is the quiet trap. Once you can build loops, you do not run out of ability. You run out of ideas. You automate the three things that were annoying enough to notice, and then you stop, not because there is nothing left, but because you genuinely cannot see what else you do over and over. The repetition that is costing you the most is the repetition you have stopped noticing.

So this is a discovery loop, pointed in an unusual direction. Back in the climb you built a discovery loop that watches the world and surfaces new tasks. This one watches you, and surfaces new loops.

[IMAGE: dark canvas, two discovery loops side by side. Left, an eye pointed outward at the world's streams (issues, tweets, Stripe) emitting "new tasks". Right, an eye pointed back at a person at a desk, replaying their own past few hours of work, emitting "new loops". A label under the right one reads "the stream is you". Caption: "a discovery loop aimed at your own work".]
![[loopy-discovering-new-loops-intro-v1-1.png]]
![[loopy-discovering-new-loops-intro-v1-2.png]]
![[loopy-discovering-new-loops-intro-v1-3.png]]
![[loopy-discovering-new-loops-intro-v1-4.png]]
![[loopy-discovering-new-loops-intro-v1-5.png]]

---

## The real bottleneck is noticing, not building

Walk back through the whole stack for a second. L1 through L4 execute the work. L5 decides what work is worth doing. Every level so far assumes you already know the shape of the loop you want. You point it at a queue, or a stream, or an ideal state, and it runs.

But where did that shape come from? You. You noticed you kept triaging the same kind of issue, or replying to the same kind of email, or running the same five commands before every deploy, and you thought "this should be a loop." The noticing is the input to everything. And the noticing is the part nobody automated, so it stays a manual, lossy, once-in-a-while act of self-reflection.

That is the bottleneck now. Not "can I build the loop." You proved you can. The bottleneck is "do I even know which of my days is loop-shaped." And the cruel part is that the better you get at the work, the worse you get at seeing it, because the most repeated work is the most habitual, and habit is invisible from the inside. You are the fish, and the repetition is the water.

[IMAGE: dark canvas, a stack of loop levels L1 to L5 all running smoothly, each fed by a small "loop shape" card. An arrow traces every card back to a single source: a thought bubble over a tired human head labeled "I noticed I keep doing this". That bubble is circled in red and labeled "the one input nobody automated". Caption: "the loops are easy now, the noticing is the bottleneck".]
![[loopy-discovering-new-loops-the-real-bottleneck-is-noticing-not-building-v1-1.png]]
![[loopy-discovering-new-loops-the-real-bottleneck-is-noticing-not-building-v1-2.png]]
![[loopy-discovering-new-loops-the-real-bottleneck-is-noticing-not-building-v1-3.png]]
![[loopy-discovering-new-loops-the-real-bottleneck-is-noticing-not-building-v1-4.png]]
![[loopy-discovering-new-loops-the-real-bottleneck-is-noticing-not-building-v1-5.png]]

---

## What everyone gets wrong: you cannot introspect your way to your loops

The obvious move is to just sit down and ask yourself, or ask the agent, "what do I do repeatedly that I could automate?"

Try it cold and you will get the same three answers everyone gets. The deploy checklist. The standup note. The PR triage. You will get the loops you already half-knew about, the ones loud enough to surface from memory. You will miss the other thirty, because human memory does not store frequency. It stores what was salient, not what was frequent. The thing you did eleven times on Tuesday left no trace, precisely because each instance was small enough to forget.

This is the same lesson as the discovery chapter, turned on yourself. Asking "what should I automate" from memory is search: you only get back what you already knew to look for. Real discovery needs a stream you did not author from recall. It needs a record of what actually happened, minute by minute, that you can read back over without your memory editing it down to the highlights.

So the move is not to think harder. The move is to capture the stream.

[IMAGE: dark canvas, split. Left "from memory": a head emitting three large obvious bubbles (deploy checklist, standup, PR triage) while dozens of tiny faded bubbles fall out the bottom unrecorded, labeled "frequency is not what memory stores". Right "from a record": an append-only log of the day's actual actions, the same tiny bubbles all captured and now clusterable, labeled "read back what really happened". Caption: "you cannot remember your way to your loops".]
![[loopy-discovering-new-loops-what-everyone-gets-wrong-you-cannot-introspect-you-v1-1.png]]
![[loopy-discovering-new-loops-what-everyone-gets-wrong-you-cannot-introspect-you-v1-2.png]]
![[loopy-discovering-new-loops-what-everyone-gets-wrong-you-cannot-introspect-you-v1-3.png]]
![[loopy-discovering-new-loops-what-everyone-gets-wrong-you-cannot-introspect-you-v1-4.png]]
![[loopy-discovering-new-loops-what-everyone-gets-wrong-you-cannot-introspect-you-v1-5.png]]

---

## The core insight: capture the stream automatically

If the input you need is an honest record of your work, the cleanest version of that record is a tool that watches your screen and writes down what it sees, continuously, without you having to remember to log anything.

That is what Codex's Chronicle feature is for. It keeps a rolling buffer of the last several hours of your screen, runs OCR over it so the text on screen becomes searchable, and rolls that up into a short markdown summary of what you were doing, a ten-minute summary that refreshes about once a minute. The raw frames are ephemeral, they live in a temp folder and age out after a few hours. What persists is the readable memory: the summaries stack up for days as a log an agent can grep and read back.

Source: [PASTE EXACT CHRONICLE / CODEX SCREEN RECORDING DOC URL]

Now point the discovery loop at that. The agent does not have to guess what you do all day. It reads its own memory of your screen, looks for the same workflow recurring, and surfaces it: "you opened the Stripe dashboard, copied three figures into a spreadsheet, and pasted them into a Slack message. You did this Monday, Wednesday, and Friday. That is a loop." You never told it. It read the repetition straight off the record.

I would personally reach for Codex Chronicle here, because it is passive and continuous, which is exactly the two properties self-reflection lacks. You do not have to decide in advance that a task is worth logging. It is all already captured, and the discovery loop decides afterward what mattered.

And its real edge is that it sees the whole machine, not one window. It watches every program you have open, and it watches the switching between them, the part of your work that no single tool ever records. The most valuable loops usually live in that switching: you pull a number out of Stripe in the browser, drop it in a spreadsheet, then retype it into Slack. No single app saw that workflow, because the workflow lived in the gaps between three apps. A screen recorder is the only thing standing high enough to see all of it at once.

[IMAGE: dark canvas, Chronicle drawn as a passive recorder beside a working person. A film strip of screen frames runs into an OCR box, which writes into a "rolling memory" scroll labeled "rolling 10-min summaries, refreshed ~every minute". A discovery-loop agent reads the scroll and circles three identical sequences across different days, emitting a card "this repeats, make it a loop". Caption: "the agent reads its own memory of your screen".]
![[loopy-discovering-new-loops-the-core-insight-capture-the-stream-automatically-v1-1.png]]
![[loopy-discovering-new-loops-the-core-insight-capture-the-stream-automatically-v1-2.png]]
![[loopy-discovering-new-loops-the-core-insight-capture-the-stream-automatically-v1-3.png]]
![[loopy-discovering-new-loops-the-core-insight-capture-the-stream-automatically-v1-4.png]]
![[loopy-discovering-new-loops-the-core-insight-capture-the-stream-automatically-v1-5.png]]

---

## The shape: it is the triager again

You already know this loop's anatomy, because it is the same triager from the discovery chapter, with one input swapped. Reach back to the five primitives you stripped a model down to in the toolbox, and watch them fill in.

The trigger is a clock, end of day or end of week. The loop wakes once your work has accumulated into a record worth reading.

The work is the scan plus the clustering. Read back over the captured history and group the moments that look like the same workflow repeated. The new muscle here is recognizing "these eight scattered moments are actually one recurring task," which is exactly the judgment a triager makes about a stream, only the stream is your own activity.

The check is the borrowed verifier, and it matters as much here as anywhere. A candidate is a real loop only if two things are true: it actually recurred above some threshold, say at least three or four times in the window, and its output is something checkable. Frequency alone is grounded in the record, not the model's hunch. And "is there a verifier for this" is the gate that keeps the loop from proposing things that can never be safely automated. If the agent cannot point to how often you did it and how a result would be checked, it has surfaced a vibe, not a loop.

The state is the memory of what it already proposed, so it does not pitch you the same Stripe-to-Slack loop every Friday after you have already said no, or already built it.

The terminate is per-run: scan the window, post the shortlist of loop candidates, sleep until the next one.

[IMAGE: dark canvas, the five-primitive loop labeled as a triager. Trigger: a clock, end of week. Work: read the captured history, cluster repeated workflows. Check: borrowed verifier, "recurred at least 3-4 times AND has a checkable output", with a red X on a one-off and on a vibe. State: a memory of candidates already proposed or built. Terminate: per-run, post shortlist then sleep. Caption: "the same triager, with you as the input stream".]
![[loopy-discovering-new-loops-the-shape-it-is-the-triager-again-v1-1.png]]
![[loopy-discovering-new-loops-the-shape-it-is-the-triager-again-v1-2.png]]
![[loopy-discovering-new-loops-the-shape-it-is-the-triager-again-v1-3.png]]
![[loopy-discovering-new-loops-the-shape-it-is-the-triager-again-v1-4.png]]
![[loopy-discovering-new-loops-the-shape-it-is-the-triager-again-v1-5.png]]

---

## You do not need Chronicle to start

Chronicle is the richest capture, but it is not the only one, and you should not let "I do not have it set up" stop you tonight. Because there is a record you have already been generating this entire class, without lifting a finger: your previous agent session transcripts.

Every time you have used Claude Code or Codex, it logged the whole session. Not just the commands that ran, but what you asked for, in your words, and what the agent did about it. That is the honest record this loop wants, and it is sitting on your disk right now. 

So the cheapest version of this whole segment is one prompt. Point your agent at its own past transcripts and ask it to read back over them and cluster the recurring patterns: what do I keep asking you to do, how often, and which of those requests look like the same task wearing different words. It is analyzing the record of your real work, the same move as Chronicle, just over the log it was already keeping.

The honest tradeoff is the surface. Transcripts only see the work you did inside the agent. Everything you do in the browser, the spreadsheet, the dashboards, the apps you never pointed the agent at, leaves no mark in them. That is exactly the whole-machine view Chronicle has and the transcripts do not. So treat this as the on-ramp, not the ceiling: it costs you nothing, it works tonight, and it will find the loops that already passed through your agent. When you want the loops hiding in the rest of your day, you graduate to capturing the screen. The principle does not change across either one: point the discovery loop at a record of what you actually did, not at your memory of it.

[IMAGE: dark canvas. A stack of past agent session transcripts (each a small chat-log card showing a user request and the agent's actions) flows into a discovery-loop agent reading back over them. The agent circles three transcripts that contain the same underlying request phrased differently and emits a card "you keep asking for this, make it a loop". A callout reads "transcripts capture intent, not just commands". Caption: "your agent already logged your real work, just read it back".]
![[loopy-discovering-new-loops-you-do-not-need-chronicle-to-start-v1-1.png]]
![[loopy-discovering-new-loops-you-do-not-need-chronicle-to-start-v1-2.png]]
![[loopy-discovering-new-loops-you-do-not-need-chronicle-to-start-v1-3.png]]
![[loopy-discovering-new-loops-you-do-not-need-chronicle-to-start-v1-4.png]]
![[loopy-discovering-new-loops-you-do-not-need-chronicle-to-start-v1-5.png]]

---

## From candidate to loop, and the recursion

Here is where this segment closes the circle of the whole chapter. The output of this loop is not a finished loop. It is a candidate, a description of repeated work plus the evidence that it repeated. What happens to that candidate is the governance you just learned.

Because a loop that proposes new loops is a self-modifying system, and you do not let those run silent. So the candidate does not become a live loop on its own. It becomes a proposal you approve, the same shape as skills-as-code: the discovery loop can even draft the new skill file and open it as a pull request, with the evidence attached, "here is the workflow, here is how many times it recurred, here is the draft." You read it, and you decide whether it graduates into something that runs.

And every brake from this chapter applies to the new loop the moment it is born. It gets a budget. It gets a kill switch. Its instructions live in the repo. A loop that mints loops without those is exactly the runaway you spent this whole chapter learning to prevent, just one level up. The factory needs the same guardrails as the machines it builds.

[IMAGE: dark canvas, a pipeline. A "discover loops" box emits a candidate card into a PR gate (the skills-as-code gate, three rows: workflow, recurrence evidence, draft skill). A human check approves it. The approved candidate becomes a new live loop, which is immediately wrapped in three small icons: a budget meter, a kill switch, a repo file. Caption: "a loop that builds loops earns the same brakes as the rest".]
![[loopy-discovering-new-loops-from-candidate-to-loop-and-the-recursion-v1-1.png]]
![[loopy-discovering-new-loops-from-candidate-to-loop-and-the-recursion-v1-2.png]]
![[loopy-discovering-new-loops-from-candidate-to-loop-and-the-recursion-v1-3.png]]
![[loopy-discovering-new-loops-from-candidate-to-loop-and-the-recursion-v1-4.png]]
![[loopy-discovering-new-loops-from-candidate-to-loop-and-the-recursion-v1-5.png]]

---

## Where you stay in the loop, and where you don't

The human role here lands in the cleanest possible place.

You do not stay in the loop for the watching. The entire reason to use a capture tool is so you never have to be your own activity logger. If you are sitting down once a quarter trying to remember what you do all day, you have appointed yourself the recorder, and you will be as lossy as you always were.

You absolutely stay in the loop for one thing. Promoting a candidate into a real loop, because that is a judgment about whether this repetition is worth standardizing, and that is yours. Second, the privacy decision, which is why this is a governance segment and not a climb one.

[IMAGE: dark canvas, the human placed at exactly two points and removed from a third. Removed: "watching and logging my own work", crossed out with "do this yourself and you are just a lossy recorder". Present: "promote a candidate into a live loop" tagged judgment, and "decide what gets recorded and where it lives" tagged privacy and trust, with a small lock icon and a "keep it local" note. Caption: "stay out of the watching, stay in for the promotion and the privacy".]
![[loopy-discovering-new-loops-where-you-stay-in-the-loop-and-where-you-don-t-v1-1.png]]
![[loopy-discovering-new-loops-where-you-stay-in-the-loop-and-where-you-don-t-v1-2.png]]
![[loopy-discovering-new-loops-where-you-stay-in-the-loop-and-where-you-don-t-v1-3.png]]
![[loopy-discovering-new-loops-where-you-stay-in-the-loop-and-where-you-don-t-v1-4.png]]
![[loopy-discovering-new-loops-where-you-stay-in-the-loop-and-where-you-don-t-v1-5.png]]

---

## The failure mode this level is most prone to

There is one specific way this loop rots, and it has a name: paving the cowpath. Automating a thing just because you repeat it, when the right move was to stop doing the thing entirely.

The discovery loop is very good at finding repetition and completely blind to whether the repetition should exist. It will happily surface "you manually reconcile these two spreadsheets every morning" and propose a loop for it, when the real fix is that the two spreadsheets should have been one system and the task should vanish, not get faster. A loop that automates waste just produces waste more efficiently, forever, and now it is invisible because it is automated.

So the candidate review has a second question stapled to "is this worth automating": "should this task exist at all." Some of your most repeated work is a symptom, not a workflow. The highest-value output of this loop is sometimes not a new loop, it is the realization that you have been hand-running something a real fix would delete. Read every candidate with both questions, automate the genuine workflows, and use the rest as a map of what to go fix at the root.

[IMAGE: dark canvas, a candidate card going through a two-question gate. Question one "is this worth automating?" with a green path to "build the loop". Question two "should this task even exist?" with a separate path to a trash icon labeled "fix at the root, delete the task". A worn dirt path labeled "cowpath" is shown being paved into a smooth road that still goes the wrong way, marked with a red X. Caption: "automating waste just makes faster waste".]
![[loopy-discovering-new-loops-the-failure-mode-this-level-is-most-prone-to-v1-1.png]]
![[loopy-discovering-new-loops-the-failure-mode-this-level-is-most-prone-to-v1-2.png]]
![[loopy-discovering-new-loops-the-failure-mode-this-level-is-most-prone-to-v1-3.png]]
![[loopy-discovering-new-loops-the-failure-mode-this-level-is-most-prone-to-v1-4.png]]
![[loopy-discovering-new-loops-the-failure-mode-this-level-is-most-prone-to-v1-5.png]]

---

## Demo

Put one discover-loops run on screen, kept small.

1. Show the capture. Open the Chronicle memory directory and show a few of the rolling ten-minute markdown summaries stacked up across the day. That is the input. No queue, no tasks, just a readable record of the last several hours of work.

2. Show the trigger. A scheduled routine fires Friday at 5pm. Same scheduled-task primitive from earlier in the class, pointed at your own history instead of at a stream of issues.

3. Show the scan and cluster in plain English. The loop reads the week's summaries, groups recurring sequences, and counts how many times each one appeared. On screen: a cluster like "open Stripe, copy MRR and churn and refunds, paste into the numbers sheet, summarize in Slack, seen 3 times this week."

4. Show the check. For each cluster, two gates: did it recur at least three times, the count comes straight off the record, and does it have a checkable output. The Stripe summary passes both. A one-off debugging session that never repeated gets dropped.

5. Show the state file. Candidates already proposed or already built, so the loop does not re-pitch a loop you turned down last week.

6. Show the output. One Slack line: "Loop candidate: weekly Stripe-to-Slack revenue summary, recurred 3x, output is checkable against the dashboard. Draft a skill and open a PR? yes / no." Click yes, and watch that become a pull request adding a new skill, which lands you right back in the skills-as-code gate from the last segment.

Total demo: three minutes. The point is that you never sat down to list what you do. A loop read a week of your actual work and handed you one loop worth building, with the evidence attached.

---

## Key Insight

> Once you can build loops, the scarce thing is not skill, it is noticing. Your memory will not surface your most repeated work, because it stores what was salient, not what was frequent. So point a discovery loop at an honest record of your screen, let it find the repetition you are too close to see, and keep yourself in the loop for the one decision that matters: which candidates are worth making real.

---

## Where we go next

You now have a loop that finds your other loops, which means the system can grow itself without waiting for you to have the idea.

That is the last piece of governance: not just keeping your existing loops safe, but keeping the safety in place as new ones appear on their own. Next we point all of this at a standing target instead of a stream of work, and ask the loop to hold reality where you said it should be.

See you in the next one.
