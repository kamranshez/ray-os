---
video_id: "XX1NEdO5"
duration: "12-16 min"
batch: 5
order: 15
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "L4 Worker Loops"
aliases: [l4-workers]
---

Everything up to now has been "I asked the agent to do a thing." This segment is "I built a thing that asks the agent over and over."

That sentence is the whole jump from L3 to L4. It is small in code and enormous in mindset, and most people watching this have never built one.

A worker is the simplest compounding loop there is. Once it's running, every item that lands in the queue is free work. You wrote the loop once. It pays out forever.

---

## What everyone gets wrong about L4

People hear "worker" and think "cron job." Same thing, right? Schedule a script, walk away.

No. A cron job runs a script. A worker runs an L3 against a stream of work.

That distinction is the entire segment. A script does the same deterministic thing every time it fires. A worker picks an item off a queue, runs a full task lifecycle on it, the spec-plan-build-review-push-verify we covered in the L3 segments, and that lifecycle contains L2 verifier loops, which contain L1 harness loops. The worker is the outermost shell wrapped around all of that, pointed at a queue instead of at a single ticket you typed.

So the scope is different by orders of magnitude. A cron job greps a log. A worker ships a pull request, on a ticket it chose, that it had never seen when you wrote the loop.

The other thing people get wrong: they think L4 needs new machinery. It doesn't. We built every primitive you need in the earlier segments. L4 is not a new kind of loop. It's the L3 you already know, with a queue bolted onto the front and a report bolted onto the back. That's it.

[IMAGE: dark canvas, a queue of stacked task cards on the left feeding into a single worker box in the middle, the worker box exploded to show a nested L3-L2-L1 stack inside it, finished items stacking on the right, a Slack message bubble appearing in the corner]
![[loopy-l4-workers-queue-worker-report-1.png]]
![[loopy-l4-workers-queue-worker-report-2.png]]
![[loopy-l4-workers-queue-worker-report-3.png]]
![[loopy-l4-workers-queue-worker-report-4.png]]
![[loopy-l4-workers-queue-worker-report-5.png]]

---

## The anatomy

Every worker, no matter the domain, is five parts. You already know four of them.

**The trigger source.** What wakes the worker up. This is the strip-the-model-out trigger primitive, just pointed at a stream instead of a single event. Four common ones: a cron tick, a queue webhook, a file watcher, or a Stop hook. We'll come back to the Stop hook, because it's the cleanest of the four and almost nobody uses it.

**The pick rule.** Once the worker wakes up, what does it grab? This is the only genuinely new part. A worker that watches Linear doesn't process every ticket. It picks the ones with a specific label. A worker watching a PR queue picks the ones that match a safe pattern. The pick rule is a filter plus a priority, and it is exactly the unordered-set-and-rubric idea from the don't-pre-sequence-the-backlog segment, applied at the front door instead of inside the loop. Hand the worker a set, give it a rubric, let it re-pick the most important unblocked item every pass.

**The process step.** This is an L3. The whole task lifecycle, running inside the worker. Ralph, or goal mode, or a plain spec-to-PR run. Whatever you'd have done by hand for one ticket, the worker does for the one it picked. Nothing new here. You built this already.

**The report step.** Write the result back where the queue lives. Mark the ticket done. Post a summary to Slack. Open the PR. Close the loop in a place a human, or another worker, can see it. This is the state primitive plus the autonomy dial deciding how loud to be about it.

**The retry rule.** What happens when the process step fails. Re-queue and try again? Escalate to a human? Park it and move on? A worker with no retry rule silently drops work, and you don't find out for a week.

Five parts. Four of them are primitives you've been building since the strip-the-model-out segment. The pick rule is the only new muscle, and it's the backlog rubric wearing a different hat.

---

## The Stop hook is the cleanest trigger

Of the four trigger sources, the Stop hook deserves its own beat, because it solves a problem the other three don't.

Daniel San has a clean framing for this. Every loop is just a different answer to "what makes the agent take another turn?" /goal waits for an outcome. /loop waits for the clock. A Stop hook waits for your script. Normal chat waits for you.
Source: https://x.com/dani_avila7/status/2053945246619251183

For a worker, the question becomes: what fills the queue? And the most natural answer is often "the thing the previous agent just finished."

That's the Stop hook. When an agent run completes, the Stop hook fires your script. The script decides whether that completed work spawns the next item of work. Agent finishes writing a feature, Stop hook fires, your script files a "now write tests for this" item. Agent finishes the tests, Stop hook fires, your script files "now update the docs."

The queue is fed by completion, not by a clock you guessed at or a webhook you have to wire up. The worker's own output becomes the worker's next input. That's the cleanest possible trigger, because the timing is exactly right by construction: the next thing happens precisely when the previous thing finished, never earlier, never on a stale schedule.

We met Stop hooks back in the goal-mode segment as the place to move verification out of the prompt and into the infrastructure. Same hook, different job. There it was a gate at the exit. Here it's a trigger at the entrance. Worth seeing that one primitive does both.

---

## Three workers, three domains

Let me make this concrete with three workers that are running in the wild right now. Watch how identical the shape is across completely different kinds of work.

**The Linear "claude-do" worker.** It watches your Linear board. The pick rule: tickets tagged with a `claude-do` label. The process step: an L3 that reads the ticket, plans, ships a branch, opens a PR. The report step: post a summary comment on the ticket and move it to "in review." The retry rule: if the PR's checks go red, re-open the ticket and tag a human. You triage by adding a label. The worker does the rest.

**The Dependabot auto-merger.** The queue is the stream of dependency-bump PRs. The pick rule: PRs whose diff matches a known-safe pattern, a patch version bump with green tests. The process step: run the test suite, diff the changelog, confirm nothing breaking. The report step: merge it, or escalate. The retry rule: anything outside the safe pattern goes to a human. This one barely uses the model's creativity at all, and that's the point. Not every worker is a genius. Some are just tireless.

**The sentence-mining auto-feeder.** This is one of mine, and it's the easiest to see end to end. The queue is a list of target words I want to learn. The pick rule: the next unprocessed word. The process step: find a natural example sentence, generate the audio, build the Anki card. The report step: stage the card in the deck and mark the word done. The retry rule: if no good sentence turns up, park the word and move on. I add words to a list. Cards appear in my deck. I never touch the middle.

Three domains. Code, infrastructure, language learning. Same five parts every time. Once you see the anatomy, you stop seeing "a coding agent" and "a study tool" as different things. They're the same machine pointed at different queues.

[IMAGE: dark canvas, three worker boxes side by side labeled Linear, Dependabot, Sentence-mining, each with the same five-part skeleton drawn inside (trigger, pick, process, report, retry), different queue icons feeding each one, a faint dotted outline around all three showing they share one shape]
![[loopy-l4-workers-three-workers-one-shape-1.png]]
![[loopy-l4-workers-three-workers-one-shape-2.png]]
![[loopy-l4-workers-three-workers-one-shape-3.png]]
![[loopy-l4-workers-three-workers-one-shape-4.png]]
![[loopy-l4-workers-three-workers-one-shape-5.png]]

---

## Why this is the leverage layer

Here is the part that should change how you think about your own work.

Intercom built workers like these across a fifteen-year-old Rails monolith and doubled engineering throughput in under a year. Not by prompting better. By treating Claude Code like a new hire, writing a skill for every recurring task, and pointing workers at the streams of work that used to land on a human's desk.
Source: https://youtu.be/4_VQBbs2iQA

The numbers tell you where the leverage is. Pull request throughput doubled. Their code-review approval worker now auto-approves 17.6% of PRs, audited and SOC 2 signed off, no human in the loop. Brian Scanlan's framing for all of it: give agents problems, not tasks. He got pulled into a security incident, habitually opened Claude, told it to look at the Slack channel, and a skill he didn't even know existed pulled the files, ran the breach analysis, and handed back next steps in two minutes. He never named the skill. He described the problem. The worker found the rest.

That's the mindset shift L4 forces. At L1 through L3 you hand the agent a task. At L4 you hand it a stream of problems and trust the lifecycle inside to figure out the tasks. One of his best workers fixes flaky test specs, and he didn't write it by hand. He gave an agent the goal "fix flaky specs," guided it through a few rounds, and it wrote the worker that now does the job better than his senior Rails engineers.

The compounding is the whole point. A task is paid for once and gone. A worker is paid for once and runs forever. Every item that enters the queue after you build it is leverage you already banked.

---

## Where workers fail

A worker fails differently from a one-off task, because nobody's watching when it does.

**Silent failure.** The worker hits an error, swallows it, and stops. The queue keeps filling. You assume it's draining. A week later you find a hundred untouched items and a process that died on day one. A one-off task fails loudly in front of you. A worker fails into the void.

**No kill switch.** Something goes wrong, the worker is mid-stream, and you have no clean way to stop it without killing the box. Every worker needs a brake you can reach.

**No budget.** The worker churns through tokens with no ceiling. The first time a runaway worker burns a thousand dollars overnight, you learn this. Better to learn it from me.

**No log review.** Nobody reads what the worker did. It could be quietly shipping garbage and you'd never know, because the whole appeal of a worker is that you stopped looking.

Every one of these is the autonomy dial, applied to a loop that runs unattended. The dial we built in the last segment was per-action: ship-silently, ship-and-log, surface-as-decision, never-without-me. A worker is where that ship-and-log notch stops being optional. Unattended work that doesn't log is work you can't trust, because you weren't there to watch it happen.

But the deeper answer to all four failures is governance, and that's its own level. Once you have one worker, you'll want five. Once you have five, you need a loop that watches the workers, kills the runaway ones, and reads the logs you won't. That's L6, and it gets its own segment in [[governance-primitives]]. For now, the rule is simpler: build the kill switch and the budget before you walk away, not after.

---

## A note on chaining workers

You'll be tempted, fast, to point one worker at the output of another. Worker A finds problems, Worker B fixes them, Worker C reviews the fixes. A queue chain. A little factory.

Don't build that yet.

A worker that watches another worker's output is the seed of a fleet, and a fleet without governance is how you get the runaway-loop horror story. The chain amplifies every failure mode above: silent failure in A starves B, a budget blowout in C cascades back up. Chained workers are real, and they're powerful, the bug-triage loop in [[bug-triage-loop]] is exactly a fleet of workers compounding, but they are a governance problem before they are a worker problem.

Start with one worker. One queue, one process, one report. Get it boring and trustworthy. Earn the second one.

---

## Demo

Let's build the sentence-mining feeder live, because it's the cleanest L4 to watch end to end.

1. **Show the queue.** Open `words.txt`. Twelve Japanese words I want to learn, one per line, nothing processed yet. Say out loud: this is the queue, and the pick rule is "the next unmarked word."

2. **Show the worker, one pass.** Run the loop on the first word. On screen: it searches for a natural example sentence, picks one, generates the audio with TTS, builds the Anki card, pushes it to the deck via AnkiConnect, and writes the word back to the file marked done. That middle chunk is the L3. Point at it and name it: spec the card, build it, verify the audio actually generated, report by staging it.

3. **Show the retry rule fire.** Word three has no clean example sentence anywhere. Watch the worker park it, log "no good sentence, skipped," and move to word four without crashing. That's the difference between a worker and a script. The script would have died on word three.

4. **Let it drain.** Start the loop unattended and let it run the rest of the list. Cards stack up in the deck. The terminal scrolls. I don't touch it.

5. **Show the report land.** When the queue empties, a single Slack message appears: "9 cards staged, 3 words skipped, here's the list." That's the autonomy dial set to ship-and-log. I wasn't watching, but I can see exactly what happened.

Total demo: four minutes. The point is that I added words to a file and finished cards came out the other end, and the whole middle ran without me. That's L4. The queue is the input, the worker is the engine, and the report is the only thing I actually read.

---

## Key Insight

> A task is paid for once and gone. A worker is paid for once and runs forever. The jump from L3 to L4 is two lines of code and a complete change in what you think your job is.

---

## Where we go next

You can now build a worker that drains a queue you fill.

The obvious next question is: who fills the queue? Right now, that's you. You're the one adding labels, listing words, deciding what's worth processing. The worker is tireless, but it's still waiting on your judgment about what to work on.

The next levels take that off your plate too. Routines and scheduled tasks give your workers a heartbeat. And then L5 discovery is the worker that feeds workers, the loop that decides what should become work in the first place. That's where you stop being the one who fills the queue, and the role of the human visibly changes.

See you in the next one.
