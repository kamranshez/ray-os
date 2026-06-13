---
class: "claude-code"
chapter: "Subagents"
---

## The Reframe

Kangwook Lee posted something about forked subagents that's worth sitting with. He said a fork is really just the main agent doing a big chunk of work, throwing away the intermediate tokens, and keeping the final result. He calls the underlying primitive *ephemeral context*.

That single sentence changes how you should think about forks.

A fork isn't really about parallelism. It isn't really about isolation. It's a scratchpad. Somewhere your agent can run noisy tool calls, reason across multiple turns, you can FAQ itself about a decision, and then walk away leaving the scratch work behind.

The conclusion comes home. The scratch work disappears.

[IMAGE: dark background, a chalkboard covered in dense scribbles labeled "ephemeral", a tiny sticky note labeled "the answer" being peeled off the chalkboard, the chalkboard then erased]

![[images/ephemeral-context/scratchpad.png]]

---

## You Can Chat With It

Here's the part most people miss. A fork isn't a fire-and-forget batch job. It's a live subagent you can talk to.

You spawn a fork, it loads up some context, it does some thinking, it returns a summary. Most people stop there. But the fork is still alive in your background panel. You can press into it and keep the conversation going.

You ask a follow up. "What about edge case X?" The fork answers, using everything it already loaded. You ask another. "Compare option two and option three side by side." It answers again. None of that round trip lands in your main session. The main session only sees the summary the fork sends back at the end of each turn.

This changes what a fork is for. It stops being a one-shot delegation. It becomes a side conversation you can pull into whenever you need to think out loud, with the full evidence on the table, and none of the noise leaking back into your main thread.

[IMAGE: dark background. Main session is a clean vertical conversation on the left. A side panel branches off labeled "fork" with a messy back-and-forth chat happening inside, while only small summary arrows feed back into the main conversation]

![[images/ephemeral-context/chat-with-fork.png]]

---

## Three Use Cases That Earn Their Keep

Three places where this pattern is obviously the right move.

**Noisy tool calls.** You need to run a bunch of tool calls to figure something out. Greps, web searches, MCP queries, log dumps. Each one returns a wall of output you have to read to find the signal. In your main session, all that output gets stuck in your history forever. In a fork, you let the fork do all the calling, all the reading, and just hand back a one paragraph "here's what I found." The 30k tokens of tool output never land in main.

**Multi-turn reasoning.** Some decisions take five rounds of thinking. You consider option A, you find a problem, you pivot to option B, you check it against constraint X, you pivot again. That whole zig-zag is valuable for arriving at the answer, but useless to retain. Do the zig-zag in a fork. The fork sweats through all five rounds. The main session gets the conclusion, not the false starts.

**FAQ before committing.** You have a decision to make and you want to interrogate it before you ship. Spawn a fork. Ask it the obvious question. Push back. Ask the harder question. Push back again. Run a counter argument. Run a what-if. By the time you've exhausted your concerns, the fork has done a twenty message back and forth with you about the decision. You take the answer back to main. The twenty messages never bloat your main thread.

The pattern under all three is the same. The thinking is rich and noisy. The output is small and clean. The fork holds the noise. The main session takes the cream.

---

## The Summary-Per-Turn Flow

Here's the mechanic worth understanding.

When you talk to a fork, every turn returns a summary to your main session. You see it in main as a small tool result. The result is whatever the fork chose to surface from that turn. The rest of the fork's working tokens stay in the fork.

So a five turn conversation with a fork shows up in main as five small tool results. Not five long transcripts. Five summaries.

You control what the summaries contain. If you tell the fork "give me the answer plus a one line note on what you considered," that's what comes back. If you say "just yes or no," that's what comes back. The fork is verbose with itself. It is concise with you.

That compression is what makes the pattern usable. Without it, every fork interaction would still bloat main, just slower. With it, you can have arbitrarily deep conversations with a fork and your main session stays under budget.

---

## Why This Costs Almost Nothing

The cache is what makes this affordable.

Your main session's prefix is already cached. When you fork, the fork inherits that exact prefix verbatim. You only pay for the new tokens the fork generates and consumes inside its own working space.

The next time you talk to that fork, its own working prefix is now also cached. So the multi-turn back and forth inside the fork is itself cheap. The cache is doing all the heavy lifting.

This is the unlock. Interactive scratchpads would be too expensive in most setups, because every round of thinking would re-pay for the context. Forks dodge that bill by reusing the parent's cached prefix and then caching their own.

So you can do this casually. Three forks running side conversations in the same main session, each chewing on different evidence, each costing almost nothing to keep talking to.

---

## The Permanence Test

Before you fork, ask one question.

*Would I want my main session to remember this evidence in three turns?*

If yes, don't fork. Pull it into the main conversation directly. The evidence is going to keep mattering.

If no, fork. The evidence matters now. It won't matter later. The fork is the right shape for it.

Most decisions in a Claude Code session look like this and we've been getting it wrong by default. We dump the evidence into the main conversation because that's the only place the agent can reason. Now there's a second place, and you can chat with it. Use it.

[IMAGE: dark background, a fork in the road. Left path labeled "Will I need this in 3 turns?" leads to "Pull into main conversation". Right path labeled "Just for this decision?" leads to "Fork it"]

![[images/ephemeral-context/permanence-test.png]]

---

## What Stays, What Goes

The discipline is in the return value. Each turn the fork sends back to main has to be small enough to live in your main session forever. If a turn returns 5k tokens, you've defeated the point. You've moved the bloat from the fork to the main session, just slower.

So when you spawn the fork, set the rule up front. *Each time I ask you something, return a short answer plus a one line note on what you considered. Do not return raw evidence. Do not return your reasoning trace. Just the conclusion.*

That sentence is what makes the fork ephemeral instead of just delayed. Without it, you've built a slow round trip with no actual savings.

---

## Demo

This is the workflow worth filming.

1. Open Claude Code in a project with a real decision. Pick something concrete, like "we have three candidate schemas for the events table, decide which one to ship."
2. Show the main session at maybe 60k tokens. Keep that number visible.
3. Prompt: "Spawn a forked subagent. Load all three candidate schemas, the migration history file, the query patterns file, and the perf benchmark output. Be ready to chat about the tradeoffs. Each turn, return a short answer and a one line note on what you considered."
4. The fork loads up. Show it ballooning to 100k+ tokens internally. Main is still 60k.
5. First question: "Which schema gives us the best read latency for the dashboard query?"
6. Fork answers in 200 tokens. Main grows by 200 tokens.
7. Press in. Keep chatting. "What about write throughput?" "What if we sharded by user ID instead?" "Can option three handle the deletion case?" Five turns of FAQ.
8. Each turn shows up in main as a small tool result. Main is now 61k tokens. Fork is 130k.
9. Make the call. Take the recommendation back to main as a clean decision block.
10. Compare: do the same back and forth in main directly. Show main balloon to 110k tokens. Then show how the main session is now noisier for every subsequent message.

The viewer should watch the token counter and feel the difference. That's the whole pitch.

---

## Key Insight

> A fork is not a separate agent. It is a scratchpad your agent uses during a critical decision and then throws away. You can talk to it like a colleague, run it through five rounds of FAQ, and your main session never sees the noise.

---

## What Changes For You

You stop dragging evidence into your main conversation just to reason over it. You stop running noisy tool calls in main. You stop having long internal debates with yourself in main and bloating the context with questions you didn't end up needing the answer to.

You fork. You chat. You decide. You take the conclusion back. The fork dies.

Over a long session this is the difference between a main conversation that stays sharp through hour three and one that gets dull and confused by hour two. You're managing your main context like a budget. The fork is where the spending happens.

Ephemeral context is the principle. Chatting with a fork is the workflow.
