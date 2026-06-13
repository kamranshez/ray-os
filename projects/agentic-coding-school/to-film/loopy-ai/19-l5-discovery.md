---
duration: "12-16 min"
batch: 5
order: 19
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "L5 Discovery Loops"
aliases: [l5-discovery]
---

A discovery loop does not do the work. It decides what should become work.

That one sentence is the whole level. Everything you have built up to now takes a thing you already decided needed doing and gets it done. L1 through L3 execute your decisions. L4 executes them on a stream without you re-asking each time. But every one of those loops is downstream of a human who looked at the world and said "this is worth doing."

L5 is the loop that makes that call for you.

This is the level where your job visibly changes. Up to here you decide what to do and the agent executes. At L5 the agent decides what is worth considering and you choose from the shortlist. That swap is the entire game, and once you feel it you cannot unfeel it.

---

## What everyone gets wrong: discovery is not search

The mistake is thinking you already have this. You have search. You ask Claude "what should I work on this week," it reads your repo and your notes, it hands you a list. Feels like discovery. It is not.

Search returns what you asked for. Discovery returns what you did not know to ask for.

When you search, you are still the one who decided the question. The agent just answers faster. The decision about what to point at, what matters, what is worth a list at all, that decision is still yours. You are at L3 with a fast assistant.

A discovery loop runs without a question. It sits on top of live input streams, your GitHub issues, your Twitter mentions, your Stripe events, your support inbox, and it watches. Its output is not an answer to your prompt. Its output is "here are three things you should probably look at, and you didn't ask." The agent generated the question.

That is the line. If the human supplied the question, it is search. If the loop surfaced the question, it is discovery.

[IMAGE: dark canvas, split panel. Left side labeled "Search": a human icon with a question mark feeding into an agent box, one answer coming out. Right side labeled "Discovery": no human question, many live input streams feeding an agent box, and the agent emitting its own question mark]

![[images/l5-discovery/search-vs-discovery.png]]

---

## The core insight: Boris's couple hundred Claudes

Here is the pattern in the wild, from the person who is furthest down this road.

Boris Cherny, who built Claude Code, said the part most people skipped past. He does not prompt Claude anymore. He writes loops, and the loops prompt Claude. And among those loops are hundreds of Claude instances that are not writing code at all. They are monitoring his Twitter feedback, his GitHub issues, and his internal Slack, generating product ideas about what to build next.
Source: https://workos.com/blog/boris-cherny-claude-code-acquired-interview-takeaways
Source: https://www.productmarketfit.tech/p/stop-prompting-ai-and-start-building

Read that carefully, because it is easy to miss what is actually new.

Those hundreds of instances are not L4 workers. An L4 worker picks a known task off a known queue and does it. These instances have no queue. There is no list of tasks waiting. Their job is to manufacture the queue. They read the unstructured noise of a product, thousands of issues and tweets and threads, and they decide which sliver of it is worth turning into work.

Boris is blunt about the quality. Most of those ideas are bad today. He expects most of them to be good within months.
Source: https://workos.com/blog/boris-cherny-claude-code-acquired-interview-takeaways

That honesty is the whole point of the level. A discovery loop is allowed to be wrong most of the time, because the human is still the filter at the end. The loop's job is recall, not precision. Surface everything that might matter. You provide the precision by choosing.

And then watch what he says happens next. "Many mornings I wake up, and Claude already has pull requests that it came up with, verified end to end, it has screenshots for me."
Source: https://tech.yahoo.com/ai/claude/articles/head-claude-code-hasn-t-161516682.html

That sentence is two loops composed. The discovery loop found the thing worth doing. It handed that thing to a worker loop, which built it and verified it. He wakes up to the output of an L5 feeding an L4. He never wrote the ticket. He just chooses whether to merge.

[IMAGE: dark canvas, two stacked boxes. Top box labeled "L5 discovery" emitting a ticket arrow downward into a bottom box labeled "L4 worker", which emits a finished PR with a screenshot icon. A sleeping human icon to the side, waking to a single yes/no choice]

![[images/l5-discovery/l5-feeds-l4.png]]

---

## The shape: a triager

Every discovery loop has the same physical shape, and it is the inverse of a worker.

A worker has one queue in, many finished tasks out. A discovery loop has many streams in, one short list out. It is a funnel. We met this in the loop stack as the triager: many input streams flow into a single filtering box, and one ranked shortlist of "things worth doing" flows out the other side.

Reach back to the strip-the-model-out primitives, because a triager is just those five slots filled in a particular way.

The trigger is a schedule or a stream event. The clock ticks, or a new issue lands, and the loop wakes. This is the scheduled-routine trigger we built two segments ago, pointed at discovery instead of grooming.

The work is the scan plus the judgment. Read everything new across the streams, and decide what is worth surfacing. This is the only genuinely new muscle in the whole level, and it is where the leverage and the danger both live.

The check is the part people forget. A discovery loop needs a verifier just like any other loop, and its verifier is the borrowed verifier we have been using all along, applied to the question "is this signal real?" An outlier is real if its lift over baseline clears a threshold. An anomaly is real if it breaks a statistical band, not because the model felt something. If your discovery loop's check is the model saying "this seems important," you have built the self-grading failure again, just at a higher altitude. The streams are the exogenous signal. The check has to be grounded in them, not in the model's mood.

The state is the memory of what it already surfaced, so it does not flag the same outlier nine days running.

The terminate is per-run: scan complete, shortlist posted, sleep until the next trigger.

[IMAGE: dark canvas, a triager funnel. Many labeled input arrows on the left (GitHub issues, Twitter, Slack, Stripe, support inbox) converging into a central box labeled "triager: scan + judge + rank". One arrow leaving the right edge labeled "things worth doing"]

![[images/l5-discovery/triager-funnel.png]]

---

## Three discovery loops worth building

The pattern generalises far past code. Here are three, each pointed at a different kind of stream.

The YouTube outlier scout. It watches a watchlist of a hundred channels in your niche. It does not make videos. Every morning it pulls recent uploads, compares each video's view velocity against that channel's own baseline, and flags the ones breaking out. The output is not "make a video about X." It is "this topic is getting three times the channel's normal lift, you might want to look." You decide whether to make it. The loop decided it was worth your attention.

The content idea factory. It reads your existing library, your audience data, and your DMs, and surfaces three drafts a day for you to pick from. Not twenty titles on demand, which is the search version. Three drafts, unprompted, grounded in what your audience is actually reacting to this week. You kill two and keep one. The keep becomes a queue item for a worker.

The revenue anomaly detector. It watches Stripe. It does not touch the anomaly. When a metric breaks its normal band, refunds spiking, a plan's conversion cratering, a sudden churn cluster, it surfaces the anomaly so you can investigate. The autonomy dial here sits firmly at surface-as-decision: a revenue anomaly is exactly the kind of high-blast-radius signal you never let a loop act on silently. It tells you. You decide what it means.

Notice the discipline across all three. The loop never builds. It never fixes. It never ships. It produces problems, not solutions. The moment a discovery loop starts doing the work, you have collapsed it back into a worker, and you have lost the thing that made it valuable: a clean separation between finding and doing, so the human filter sits exactly at the find-to-do boundary.

---

## Where you stay in the loop, and where you don't

This is the cleanest place in the whole stack to see the human role move.

You do not stay in the loop for building the shortlist. That is the entire point of paying for L5. If you are reading every tweet and every issue yourself to decide what is worth surfacing, you have not built a discovery loop, you have hired yourself to do triage.

You absolutely stay in the loop for choosing from the shortlist. The loop hands you three to five candidates with its reasoning and its evidence attached, and you pick. That choice is cheap, it is fast, and it is where your taste actually compounds.

This is the autonomy dial applied to a whole level. A discovery loop is, almost by definition, pinned at notch three, surface-as-decision. It comes to you with the call, the options, and a recommendation, and it waits. It does not get notch one, ship-silently, because the whole reason it exists is to put a human judgment at the front of the work pipeline. If you ever find yourself letting a discovery loop act on its own findings without you, you have quietly turned it into an unsupervised worker, and you should ask whether you meant to.

---

## The failure mode this level is most prone to

There is one way discovery loops rot, and it is worth naming now even though it gets its own segment soon.

A discovery loop that reads only its own prior outputs converges to a fixed point. If the content idea factory reads yesterday's ideas to generate today's, and tomorrow reads today's, the loop folds in on itself and the surface narrows until it is recommending variations of one idea forever. That is the echo chamber, and it is the L5 version of self-grading: a loop sampling from its own distribution and mistaking the second sample for new information.

The defense is structural, and it is baked into the definition of the level. A discovery loop's input must be exogenous. The streams are the world, not the loop's memory. The whole reason L5 watches Twitter and Stripe and GitHub instead of its own notes is that those streams carry signal the loop could not have generated. The day your discovery loop's richest input is its own back catalogue is the day it stopped discovering. We will take this failure mode apart properly later.

---

## Demo

Put the YouTube outlier scout on screen.

1. Show the input. One file: a watchlist of a hundred channel IDs in the AI and coding niche. That is the entire configuration. No tasks, no queue.

2. Show the trigger. A scheduled routine fires the loop every morning at 7am. Same scheduled-task primitive from two segments ago, pointed at discovery.

3. Show the filter logic in plain English on screen. For each channel, pull uploads from the last seven days. Compute each video's views-per-hour. Compare against that channel's trailing median. Flag anything above three times baseline. Rank the flags by lift. That comparison against baseline is the borrowed verifier: the channel's own history is the external grader, not the model's opinion.

4. Show the state file. A list of outliers already surfaced this week, so the loop does not re-flag the same breakout four days in a row.

5. Show the output. One line in Slack: "Outlier: [video title], 4.2x this channel's baseline, topic looks like agent memory. Worth a video? yes / no." One candidate, ranked above the noise, with its evidence and a single decision attached.

6. Click yes. Watch that single yes become a queue item for the worker loop we built earlier. The discovery loop is done. It found the problem. The worker takes it from here.

Total demo: three minutes. The point is that nothing in this loop wrote a video, and nothing wrote a ticket by hand. The loop read a hundred channels you would never watch yourself and handed you exactly one decision worth making.

---

## Key Insight

> A worker takes problems and produces solutions. A discovery loop takes the world and produces problems. The first one needs your instructions. The second one replaces them.

---

## Where we go next

You can now build a loop that decides what is worth doing, and hand its output to a loop that does it.

But the hardest discovery loops, the ones generating ideas with no borrowed verifier in sight, need more than one agent watching. They need a generator, a critic, and something holding the two apart. That three-role split is next, and it is the structure that keeps a discovery loop honest.

See you in the next one.
