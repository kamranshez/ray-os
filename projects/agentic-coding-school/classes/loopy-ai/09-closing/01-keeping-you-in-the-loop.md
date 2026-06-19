---
video_id: "DCxfwHqq"
duration: "10-14 min"
batch: 8
order: 28
batch_name: "L7 Closing"
class: "loopy-ai"
chapter: "Keeping You In The Loop"
aliases: [keeping-you-in-the-loop]
---

A loop that does perfect work and dumps it where you'll never see it is a loop that doesn't exist.

That sentence is the whole segment. We have spent this entire class making loops better at the work. This one is about the last six inches: getting the work back up to you at a rate one human can actually absorb.

Because here's the thing nobody tells you when they sell you the dream of twenty agents running overnight. The agents are not the constraint. You are.

---

## You are the bottleneck. This is what that costs.

We planted this in the [[intro]] and named it formally in [[loop-stack]]: at L7, the scarce resource is not the model, not the harness, not the prompts. It's your attention. The portfolio decision about what to even look at.

For most of the class that's been a strategic idea. Here it becomes an engineering problem, because the bottleneck has a physical location: the moment work crosses from the loop into your head.

Picture the failure. You've got ten terminals open. Thirty diffs landed overnight. A worker fixed four bugs, a discovery loop surfaced six "interesting" signals, a routine groomed tomorrow's backlog, and somewhere in there is one PR that's about to delete a production table if you approve it.

You open the first terminal. Wall of log. You scroll. Your eyes glaze. And now you do one of two things, both bad.

You rubber-stamp. You approve everything because reading it properly would take three hours you don't have. That's cognitive debt, and it compounds: every rubber-stamp is a thing you no longer understand about your own system.

Or you freeze. You don't trust the output, you can't verify it fast enough, so you stop the loops and go back to doing it yourself. Which means the whole stack you built is now decorative.

[IMAGE: dark canvas, ten cluttered terminal windows on the left all dumping walls of text toward a single small human head on the right, the human visibly overwhelmed, one red diff labeled "DROP TABLE" buried in the pile]
![[loopy-keeping-you-in-the-loop-ten-terminals-overwhelm-1.png]]
![[loopy-keeping-you-in-the-loop-ten-terminals-overwhelm-2.png]]
![[loopy-keeping-you-in-the-loop-ten-terminals-overwhelm-3.png]]
![[loopy-keeping-you-in-the-loop-ten-terminals-overwhelm-4.png]]
![[loopy-keeping-you-in-the-loop-ten-terminals-overwhelm-5.png]]

The instinct, when this happens, is to think you have too many loops. You don't. You have a bad pipe.

---

## The fix is not fewer loops. It's a deliberately engineered pipe.

Stop treating the delivery interface as an afterthought. It's the design problem. The work being good is table stakes now. Getting it to you cleanly is the differentiator.

> The next moat isn't a better model. It's the cleanest pipe into your decision surface.

That line is a literal engineering instruction, not a slogan. "Cleanest pipe into your decision surface" means: design the report so a tired human at 6am can act on it in seconds. Everything in this segment is a way of honouring that sentence.

And the first move is to notice that a loop hands you two completely different kinds of thing, and they need completely different pipes.

---

## The two things a loop can hand you

Name them, because they want different channels and different cadences.

**Artifacts.** Finished or near-finished work. Drafts, PRs, reports, slide decks, the groomed backlog. These want a single channel and a batched cadence. One inbox, not thirty terminals. You read them when you choose to, in a block, and the work waits patiently for you.

**Decisions.** The things the loop can't or shouldn't settle alone. Irreversible actions, ambiguous calls, anything high-stakes. These want interrupt cadence and a crisp shape: here's the call, here are the options, here's my recommendation. You answer in one line and the loop moves on.

Most people's loops surface neither cleanly. The work is scattered across sessions and the decisions are buried inside walls of log, so the one PR that matters is sitting in paragraph forty of a transcript you're never going to finish reading.

Separating the two is the move. Artifacts go in a tray you visit on a cadence. Decisions reach out and tap you on the shoulder. Different channel, different urgency, different format.

[IMAGE: dark canvas, a fan of many loops on the left all funnelling into one narrow pipe, the human standing at the narrow end, and on the right two clearly labelled trays splitting off the pipe, an "Artifacts" tray marked batched and an "Decisions" tray marked interrupt]
![[loopy-keeping-you-in-the-loop-pipe-two-trays-1.png]]
![[loopy-keeping-you-in-the-loop-pipe-two-trays-2.png]]
![[loopy-keeping-you-in-the-loop-pipe-two-trays-3.png]]
![[loopy-keeping-you-in-the-loop-pipe-two-trays-4.png]]
![[loopy-keeping-you-in-the-loop-pipe-two-trays-5.png]]

This split sounds obvious once you say it. Almost nobody does it. They build one firehose and point it at themselves.

---

## The menu of ways to stay in the loop

Six design calls. None of them is about a notification tool. They're about what gets surfaced, when, and in what form.

**One channel, not thirty windows.** Pick a single pipe and make every loop write to it. A Slack channel, a Telegram thread, an email digest, a review queue, a kanban board. The point is that you check one place, not hunt across sessions wondering which terminal had the thing. Parsons runs a morning brief plus a worker kanban. Boris's loops "surface three drafts a day" into one surface. The channel is an implementation detail; the discipline is convergence onto one surface.

**Batch on a cadence.** A 6am digest of everything that happened overnight beats real-time pings every single time, because real-time pings are pings you learn to ignore. Match the cadence to the work: hourly for a hot worker, daily for a research loop, Sunday night for a fleet review. This is the same instinct as the weekly fleet-health report from [[governance-primitives]], just a different payload. That one reports on the health of the loops. This one reports your actual work output.

**Surface decisions, not transcripts.** The loop hands up the call, not the diff that produced it. "I can ship A or B. A is faster but loses property X. Recommend A. Your call." That's cheap to read and fast to answer. The diff is available if you want to drill in, but the default view is the decision, already framed. This is the same move as the HTML-artifact rule from earlier: don't make the loop talk to you, make it hand you a shaped thing.

**Reversibility decides which tier an action lands in.** Which actions even get surfaced as decisions, versus shipped silently, versus shipped-and-logged, is the per-action policy we built in [[the-autonomy-dial]]. That segment decides which actions reach you. This segment is how they reach you once the dial says they should. Don't re-derive the dial here; just wire its output into the pipe. The dial picks the tier; the pipe delivers it.

**Format for absorption, not for the machine.** A wall of unified diff is formatted for git, not for a human at 6am. Slides beat a diff. A three-line summary with a recommendation beats a transcript. A rendered HTML report beats raw JSON. The loop's last step should be a translation step: take the machine-shaped result and re-shape it for the specific tired human who has to act on it.

**Never let a loop close its own ticket.** The human owns the final close. Not because the loop got the work wrong, but because closing is how you stay current with your own system. If the loop opens and closes its own tickets, you wake up one day with a system that runs itself and that you no longer understand. The close is your checkpoint. It's the antidote to the rubber-stamp.

[IMAGE: dark canvas, a phone showing a single Slack message that reads "Decision: ship A or B? A faster, loses property X. Recommend A." with two buttons Approve and Deny, contrasted against a faded greyed-out wall of raw diff behind it]
![[loopy-keeping-you-in-the-loop-decision-not-transcript-1.png]]
![[loopy-keeping-you-in-the-loop-decision-not-transcript-2.png]]
![[loopy-keeping-you-in-the-loop-decision-not-transcript-3.png]]
![[loopy-keeping-you-in-the-loop-decision-not-transcript-4.png]]
![[loopy-keeping-you-in-the-loop-decision-not-transcript-5.png]]

That's the menu. Pick a channel, batch artifacts, surface decisions framed, let the dial pick tiers, format for a human, and keep the close in your hands.

---

## The diagnostic

Here's the test that tells you whether you've earned the right to add another loop.

Can you keep up with the output of one loop?

If the answer is no, then adding a second loop makes it worse, not better. Six parallel agents make it six times worse. The bottleneck is your decision surface, and more throughput upstream just floods it faster. You don't have a loop problem. You have a pipe problem, and scaling the loops scales the flood.

This is the operational version of the [[intro]] thesis, and it's the reason this segment sits in Closing rather than in The Climb. We taught you to build the loops first. Now, at the top of the stack, the binding constraint is the interface between those loops and your head. Fix the pipe before you add agents. Every time.

It's also why the "just run more agents in parallel" advice keeps disappointing people. They scale the cheap thing. The expensive thing, your attention, doesn't scale, so the parallelism just converts into a bigger pile you can't read.

---

## What this segment is not

Three quick boundaries, because this one sits next to a lot of adjacent material.

It's not [[governance-primitives]]. That governs the loops: budgets, kill switches, retirement, the fleet's health. This governs the interface between the loops and you. Adjacent, not the same. Governance keeps a runaway loop from burning a thousand dollars. This keeps you from drowning in the output of the well-behaved ones.

It's not [[mission-command]], which is the next segment. That's intent flowing down into the loops. This is work flowing back up to you. They're a matched pair, the two human-facing halves of the stack, and we film them to reference each other. Mission-command is how you tell the loops what you want. This is how they tell you what they did.

And it's not a tour of notification tools. The channel is plumbing. The design call is what gets surfaced, when, and in what form. Get those three right and it works in Slack, in email, on a kanban board, or on an index card.

---

## Demo

Let's make this real. One screen, one delivery channel, one of each kind of handoff.

1. **Open the channel.** Pull up a single Slack channel called `#loop-deck`. Every loop I run, worker and discovery and routine, writes here. No terminals on screen. This is the only surface I check.

2. **The artifact that landed overnight.** Scroll to the 6am batch digest. One message, posted by the fleet, sectioned: "Shipped: 4 bug-fix PRs (links). Drafted: 2 blog outlines. Groomed: tomorrow's backlog (12 tickets)." Each item is a link, not a diff. Click one PR link, glance at the rendered summary, move on. Twenty seconds to absorb a whole night of work.

3. **The decision the loop kicked up.** Above the digest, a separate message, posted at 2am, with a red marker: "Decision needed. Migration loop wants to drop column `legacy_user_id`. Reversible: no, data loss. Recommend: snapshot first, then drop. Approve / Hold." This one interrupted because the dial flagged it irreversible. It did not sit in a digest.

4. **Answer in one line.** Reply in the thread: "Snapshot first, then proceed." One sentence. Hit send.

5. **Watch the loop pick it up and continue.** The migration loop, which paused itself at the decision and was polling the thread, reads the reply, takes the snapshot, runs the drop, and posts "Done, snapshot saved to `backups/`, column dropped." The loop was blocked on me for exactly as long as it took to read one framed decision and type one line.

Total demo: three minutes. The point is the asymmetry. The artifacts waited in a batch I read on my schedule. The one decision that mattered reached out and got answered in a sentence. I never opened a terminal, never read a diff, and never rubber-stamped anything I didn't understand.

---

## Key Insight

> A loop that does perfect work and dumps it where you'll never see it does not exist. The next moat isn't a better model. It's the cleanest pipe into your decision surface.

---

## Where we go next

So that's work flowing up. One channel, artifacts batched, decisions framed, the close in your hands, and a hard diagnostic: fix the pipe before you add agents.

The next segment is the other half of the pair. If this is how work reaches you, [[mission-command]] is how your intent reaches the loops, so they make the right calls without surfacing every one of them to you in the first place.

Tighten the intent going down and you thin out the decisions coming back up. That's the whole game at the top of the stack.

See you in the next one.
