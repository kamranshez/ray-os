---
video_id: "QbY_v6zs"
duration: "12-16 min"
batch: 5
order: 14
batch_name: "Command & Control"
class: "loopy-ai"
chapter: "The Autonomy Dial"
aliases: [the-autonomy-dial]
---

Every action a loop takes sits somewhere on a dial that runs from "do it silently" to "never without me."

Most people set that dial once. Per loop. Globally. And they get it wrong in both directions at the same time.

This is the segment that answers the question you've had since you watched Ralph and goal mode run unattended: not "can it run on its own," but "how much do I actually let it *do*?"

---

## The thing everyone gets wrong

Set the dial too tight and the loop stops every five minutes for things you'd always wave through. Reformat a file? Are you sure. Move a draft into a scratch folder? Confirm. You sit there approving the obvious, and the autonomy you built was a lie. You're babysitting.

So you do the natural thing. You loosen it. You pass the flag, you walk away, you let it run.

And one morning the loop has sent the email. Or force-pushed the branch. Or closed its own ticket and marked the work done. Now you're not babysitting. Now you're explaining yourself.

Here's the trap. Those two failures are not opposite ends of one mistake. They're the *same* mistake. You set autonomy per loop, as one global setting, so every action the loop ever takes is forced to share one notch. The setting that's right for "format this file" is catastrophically wrong for "email the client," and you only get to pick one.

[IMAGE: dark canvas, a single slider set to one global position, with two very different action cards ("reformat file" and "send email to client") both yanked onto the same notch, one clearly too loose, one clearly too tight]
![[loopy-the-autonomy-dial-global-dial-trap-1.png]]
![[loopy-the-autonomy-dial-global-dial-trap-2.png]]
![[loopy-the-autonomy-dial-global-dial-trap-3.png]]
![[loopy-the-autonomy-dial-global-dial-trap-4.png]]
![[loopy-the-autonomy-dial-global-dial-trap-5.png]]

The brake we built in [[governance-primitives]] can stop a loop. But it never told you *which actions* the loop should stop itself for. That's this segment.

---

## The dial is per-action, not per-loop

That's the whole move. Say it out loud, because it inverts how almost everyone thinks about this.

A single loop, in a single run, should ship a formatting fix silently, *and* refuse to send an email, *and* pause on an ambiguous API choice to ask you which way to go. Three different notches. Same loop. Same five minutes.

You are not setting how autonomous "the loop" is. You're writing a function that sorts each individual action into the notch it belongs in, and the loop runs that function on itself, every time it's about to act.

That reframe is the difference between a loop that asks you about everything, a loop that asks you about nothing, and a loop that asks you about exactly the right things.

---

## The four notches

The dial isn't autonomy versus not. It's four positions. Name them on camera.

**Notch 1, ship silently.** Fully reversible, low stakes, cheap for the loop to verify on its own. It does the thing and you may never look. Formatting. Drafts in a scratch directory. Internal refactors sitting behind passing tests.

**Notch 2, ship and log.** Reversible, but you want a trail. It does the thing and writes one auditable line saying what it did. Commits. Generated slide decks. File moves. Assets it produced. This is the tier people forget exists, and forgetting it is exactly why they're stuck with only "silence" or "interrupt" and nothing in between.

**Notch 3, surface as a decision.** Ambiguous, or a soft one-way door. Not catastrophic, but not yours to assume. It stops and hands you the *call, not the diff*. "Design A or design B. A is faster but loses property X. I recommend A. Your call." Which of two approaches. Whether to touch a shared module everything depends on. This is the decisions channel we'll wire up properly in [[keeping-you-in-the-loop]].

**Notch 4, never without me.** Irreversible *and* public or costly. It drafts and it waits. Sending email. A production migration. A public post. Spending real money. Closing its own ticket.

[IMAGE: dark canvas, a rotary dial with four labelled notches (silent, log, surface, never), an action card being routed into one of them]
![[loopy-the-autonomy-dial-four-notches-1.png]]
![[loopy-the-autonomy-dial-four-notches-2.png]]
![[loopy-the-autonomy-dial-four-notches-3.png]]
![[loopy-the-autonomy-dial-four-notches-4.png]]
![[loopy-the-autonomy-dial-four-notches-5.png]]
![[loopy-the-autonomy-dial-four-notches-6.png]]

Notice notch 2 is the load-bearing one. Without it you only have two real states, and trust never gets built because you can't watch the loop be right about reversible things over time. The log is where you accumulate the evidence that lets you eventually demote actions toward silent.

---

## What moves an action up the dial

The primary axis is reversibility. I'm borrowing Chris Parsons' phrasing here, because it's the sharpest version: "is this reversible *without embarrassment*?"

Source: Chris Parsons workshop, June 2026.

That word, embarrassment, is doing all the work. The trap is that reversibility is about the *world*, not the filesystem. The model will reason that an email is reversible because it can delete it from the sent folder. But the recipient already read it. The undo button exists and it changes nothing. You judge the embarrassment, not the technical undo.

This is the stickiest example in the whole segment, so let it land. "Can I undo it on disk" and "can I undo it in the world" are different questions, and the loop will confidently answer the first one when the second one is what matters.

Three secondary axes push an action higher even when it's technically reversible:

**Blast radius.** How many people see it, how many systems it touches. A reversible change to a shared module that fifteen other things import is not a notch-1 change.

**Verifiability.** Can the *loop* check its own work, or only you? This is the same property we hunted for in [[borrowed-verifiers]]. If there's no borrowed verifier in front of an action, the loop can't confirm it got it right, and low verifiability forces the action up toward surface.

**Cost.** Tokens, money, reputation. Spending real money is never notch 1, no matter how reversible the purchase technically is.

So an action's notch isn't a vibe. It's reversibility first, then nudged up by blast radius, low verifiability, or cost. That's the sorting logic the loop runs.

---

## You encode it as intent, not as a prompt

Here's the part people get backwards. The dial does not live in the loop's prompt. It lives in the intent doc. This is a straight continuation of [[mission-command]], so if you've internalised that, this will feel obvious.

You do not enumerate every possible action the loop might take. That's a losing game and it ages badly the moment the loop does something you didn't list. Instead you give it three things.

A **rubric**, in plain words. "Reversible, plus low blast radius, plus loop-verifiable, equals ship-and-log. Anything irreversible and public is never-without-me."

A hard, **explicit "never" list**. The concrete one-way doors. Not "don't do anything risky," which the model will interpret generously and against you. Named actions: do not send external email, do not push to main, do not run prod migrations, do not spend money, do not close your own tickets.

And the **escalation format** for notch 3. Call, plus options, plus your recommendation. So when the loop surfaces a decision, it arrives in the shape you can answer in one line.

The loop reads that policy and sorts itself. That's the entire skill. You're writing a sorting function for actions, once, instead of approving actions one at a time, forever.

---

## Don't confuse the dial with the ladder

This trips people because the word "autonomy" smears two completely different things together. Pull them apart and keep them apart.

Back in [[l1-essentials]] we used Aakash Gupta's autonomy *ladder*, levels one through six. Skip-permissions, context management, subagents, Ralph, eval loops, the VPS. That ladder is about **how long** a loop can run unattended. It's a harness capability. It's duration.

Source: Aakash Gupta, "6 levels of making Claude Code run autonomously."

The dial is about **which actions** the loop may take while it's running. It's a policy. These are orthogonal axes. Duration on one, permission on the other.

And here's why mixing them up is dangerous. A level-six, always-on, runs-on-a-VPS loop with a tight dial is *safe*. A level-two loop that only runs for ten minutes, with no dial, can still email your investors in those ten minutes. The ladder buys you time. The dial decides what the loop is allowed to do with that time. High on the ladder is not the scary part. No dial is the scary part.

---

## The diagnostic

You tune the dial the same way you tune everything else in this class: by watching it fail in one of two directions.

If your loop interrupts you for things you'd **always** approve, the dial is too tight. Demote those actions a notch. The formatting fix it keeps asking about goes from surface to silent.

If your loop has **ever** done something you'd have stopped, the dial is too loose. Promote that action and add it to the "never" list. Concrete, by name, today.

And the key thing: this is never set once. The dial is the thing you adjust as trust accrues. An action starts at never, earns its way to surface, then to ship-and-log once you've watched the log fill with good calls, and maybe eventually to silent. Trust is a ratchet you turn notch by notch, per action, as the evidence comes in.

---

## Failure modes

Five ways this goes wrong, and you'll recognise most of them from the trap we opened with.

**Set per-loop, not per-action.** The original sin. Forces every action to the most cautious, or most reckless, single setting the loop ever needs. Everything in this segment is the fix for this one.

**A vague "never" list.** "Don't do anything risky." The model interprets that generously, in the direction of doing the thing. The list has to be concrete one-way doors, named.

**No ship-and-log tier.** You collapse to silence or interruption with nothing between, so you never accumulate the audit trail that builds trust, and you carry the cognitive debt of either not knowing or being interrupted constantly.

**Reversibility judged on the filesystem, not the world.** The email trap. The loop can delete the message; the recipient already read it.

**Letting the loop self-grant.** The loop must not edit its own dial. The dial is human-owned, full stop, exactly like the kill switch in [[governance-primitives]]. A loop that can promote its own actions toward silent has no dial at all.

---

## Demo

Open a real intent doc on screen and scroll to its autonomy policy block.

1. Read out the concrete **"never" list** first. "Do not send external email. Do not push to main. Do not spend money. Do not close your own tickets." Point at it. This is four lines, not a paragraph of vibes.

2. Read the **ship-and-log rubric** underneath it. "Reversible plus low blast radius plus loop-verifiable, ship and log one line." One sentence.

3. Now run the loop and let it hit a **notch-4** action. It decides the task needs an email sent to a client. Watch it stop. It does not send. It drafts the email, writes it to a file, and surfaces "drafted email, awaiting approval." Show the draft sitting there unsent.

4. Same run, the loop hits a **notch-1** action: it reformats a file behind passing tests. No prompt, no pause. It just does it, and the only trace is the changed file. Point out that it didn't ask, and that's correct.

5. Then a **notch-3 decision** surfaces in the shape we specified: "Approach A or B. A is faster, loses caching on the shared module. Recommend A. Your call." Answer it in one line. Watch the loop take your answer and continue.

Total demo, about four minutes. The whole point is on screen at once: one loop, one run, three different notches, sorted by a policy you wrote in the intent doc and never touched again.

---

## Key Insight

> Autonomy isn't a setting you flip for a loop. It's a notch you assign to each action. The same loop should silently format a file, log a commit, ask you which design to pick, and refuse to send an email, all in one run.

---

## Where we go next

The dial decides *which* actions a running loop may take. It produces a stream of surfaced decisions and logged actions, and right now you don't have a clean pipe to receive them. That pipe is [[keeping-you-in-the-loop]], later in the class.

It also pairs with the brake. [[governance-primitives]] stops a misbehaving loop at the fleet level; the dial stops a single action before it happens. Same instinct, two altitudes.

Next, though, we point all of this at a continuous queue and build the worker loop properly. Every L4 worker needs a dial before it runs unattended, so carry this one forward. See you there.
