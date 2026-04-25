---
duration: "8-12 min"
batch: 2
order: 2
batch_name: "Advanced Subagents"
class: "claude-code"
chapter: "Subagents"
---

## The Reframe

Kangwook Lee posted something about forked subagents that's worth sitting with. He said a fork is really just the main agent doing a big chunk of work, throwing away the intermediate tokens, and keeping the final result. He calls the underlying primitive *ephemeral context*.

That single sentence changes how you should think about forks.

A fork isn't really about parallelism. It isn't really about isolation. It's about giving your agent a scratchpad. Somewhere it can dump a huge amount of evidence, reason over all of it, reach a conclusion, and then walk away leaving the scratch work behind.

The conclusion comes home. The scratch work disappears.

[IMAGE: dark background, a chalkboard covered in dense scribbles labeled "ephemeral", a tiny sticky note labeled "the answer" being peeled off the chalkboard, the chalkboard then erased]

![[images/ephemeral-context/scratchpad.png]]

---

## What Ephemeral Context Actually Is

Lee's pseudocode is short enough to memorize.

```
while task not completed:
    context = token_history + log
    output = LLM(context)
    token_history += [thoughts, action, result]
```

The `token_history` is the stable prefix. Task instruction, prior decisions, prior results. This grows slowly and stays cache friendly.

The `log` is the ephemeral part. Game state, sensor readings, a compiler dump, a 200 line stack trace, a freshly fetched search result. It's glued onto the context for one call. Then it's gone.

After the call, you only persist the distillate. "Saw enemy at northeast ridge, fired, hit confirmed." Not the raw frame data. Not the 200 line log. Just the conclusion that future steps actually need.

Without ephemeral context, every observation accumulates forever. After ten turns your context is bloated with stale game frames or stale stack traces. The cache invalidates. Reasoning gets noisier. Cost goes up.

With ephemeral context, the agent gets the rich present moment for free, and pays nothing for it later.

---

## The Fork Is the Easy Version

Anthropic shipped this primitive in Claude Code, but they shipped it wrapped as a fork.

When you fork, the fork loads a huge amount of context, reasons over it, and returns a small structured result back to the main session. The main session's `token_history` only gets the conclusion. Everything the fork looked at to reach that conclusion is ephemeral by construction.

That's why forks feel different from regular subagents the moment you understand the framing. A regular subagent is about isolation. A fork is about discarding intermediate tokens. Same physical mechanism, different mental model.

If you came up through Lee's framing first, you'd build forks before anyone asked for them. They're the obvious tool once you see "ephemeral context" as a primitive.

[IMAGE: dark background, two boxes side by side. Left box labeled "Main Session token_history" stays small and stable. Right box labeled "Fork (ephemeral)" balloons to 200k tokens then disappears, leaving a small arrow back to the main box labeled "the answer"]

![[images/ephemeral-context/fork-as-ephemeral.png]]

---

## Forks as a Working Scratchpad

This reframe gives you a new pattern. Treat the fork as a working scratchpad for a critical decision.

You're at a moment in your main session where you need to make a real call. Pick the database schema. Choose between two architectures. Decide whether to ship the fix or roll back. The decision deserves real evidence. Logs, schemas, related code, a long doc, a benchmark output.

You don't want to drag all of that into the main conversation. The main conversation has to keep moving past this decision and live with the cost forever. The decision doesn't.

So you fork. You load every piece of evidence into the fork. The fork chews through it. The fork returns a structured recommendation and a one paragraph rationale. That comes back to the main session. The 80,000 tokens of evidence stay in the fork, which then dies.

You got the depth without the bloat. Your main conversation continues at the same token weight it had before the decision started, plus a clean little block that says "here's what we decided and why."

This is what Kangwook Lee meant by ephemeral context, expressed as a workflow you can run today.

---

## The Permanence Test

Before you fork, ask one question.

*Would I want my main session to remember this evidence in three turns?*

If yes, don't fork. Pull it into the main conversation directly. The evidence is going to keep mattering.

If no, fork. The evidence matters now. It won't matter later. The fork is the right shape for it.

This is the same call game agents make every frame. The current enemy position matters now. It won't matter in three seconds. So it goes into ephemeral context, not into history.

Most decisions in a Claude Code session look like this and we've been getting it wrong by default. We dump the evidence into the main conversation because that's the only place the agent can reason. Now there's a second place. Use it.

[IMAGE: dark background, a fork in the road. Left path labeled "Will I need this in 3 turns?" leads to "Pull into main conversation". Right path labeled "Just for this decision?" leads to "Fork it"]

![[images/ephemeral-context/permanence-test.png]]

---

## Why This Costs Almost Nothing

The math works because of how the cache is keyed.

Your main session's prefix is already cached. When you fork, the fork inherits that exact prefix verbatim. The cache covers the entire history up to the fork point. The fork then loads its ephemeral evidence, runs its reasoning, and returns. You only pay for the new tokens.

The next time you fork from the same conversation, the prefix is *still* cached. You're not paying for context history twice. You're paying for the new evidence and the new reasoning, every time.

This is the unlock. Ephemeral context as a pattern would be too expensive in most setups, because dragging huge evidence in and out of context would cost a fortune. Forks make it cheap because the expensive part, the prefix, is shared and cached.

So you can do this casually. Three forks in one session, each loading 50k tokens of throwaway evidence, each returning a clean conclusion. Your main context grows by maybe 600 tokens of summaries. The bill barely moves.

---

## What Stays, What Goes

The discipline is in the return value. The fork has to give you something small enough to live in your main session forever. If the fork returns 30k tokens, you've defeated the point. You've just moved the bloat from the fork into the main session.

So when you spawn the fork, tell it explicitly. *Return a one paragraph summary and a structured recommendation. Do not return the raw evidence. Do not return your full reasoning trace. Just the conclusion and one paragraph of why.*

That sentence is what makes the fork ephemeral instead of just delayed. Without it, you've built a slow round trip with no actual savings.

The discipline transfers to anything else you build. If you ever write your own agent loop with ephemeral context, the same rule applies. The thing you append to history has to be small. Otherwise the loop is doing nothing.

---

## Demo

This is the workflow worth filming.

1. Open Claude Code in a project with a real decision to make. Pick something concrete, like "we have three candidate schemas for the events table, decide which one to ship."
2. Show the main session at maybe 60k tokens. Keep that number visible.
3. Prompt: "Spawn a forked subagent. Load all three candidate schemas, the migration history file, the query patterns file, and the perf benchmark output. Decide which schema we should ship. Return only a one paragraph recommendation and a bullet list of the top three reasons. Do not return the raw schemas or the benchmark dump."
4. Show the fork starting at the same 60k tokens, then loading 40k more tokens of evidence. Total in the fork: ~100k.
5. Fork returns. Show the result is roughly 300 tokens.
6. Show the main session token count after the fork closes. It went from 60k to roughly 60.3k. The 40k of evidence never landed in main.
7. Compare: do the same task without forking. Pull the schemas, history, query patterns, and benchmark into the main session directly. Show the token count balloon. Then show how the main session is now noisier for every subsequent message.

The viewer should watch the token counter and feel the difference. That's the whole pitch.

---

## Key Insight

> A fork is not a separate agent. It is a scratchpad your agent uses during a critical decision and then throws away. Once you see forks this way, you stop using them for parallelism and start using them for thinking.

---

## What Changes For You

You start treating big decisions differently. You stop loading 80k tokens of evidence into your main conversation just to reason over it for one turn. You fork, you reason, you keep the conclusion, you let the evidence go.

Over a long session this is the difference between a main conversation that stays sharp through hour three and one that gets dull and confused by hour two. You're managing your main context like a budget instead of letting it bloat with every research detour.

Ephemeral context is the principle. The fork is just the cleanest way to use it.
