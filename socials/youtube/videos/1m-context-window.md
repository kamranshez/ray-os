Anthropic just made 1 million tokens the default context window for Claude Code. Most people hear that and think "I can just code for longer without compacting." That's not the unlock.

---

## What shipped

Opus 4.6 and Sonnet 4.6: 1M context, generally available. No beta header, no long-context price increase — standard pricing across the full window. Up to 600 images or PDF pages per request. Default on all Claude Code plans.

---

## Intake, not working memory

**1M context is intake bandwidth. It's not working memory.**

Use the big window for **reading and understanding** — load the whole repo, the full diff, every version of a contract, a week of production logs. See the connections. Build the map. Spot what you'd miss if you only saw pieces.

Then switch modes. Distill what you learned into artifacts — a plan, a map, notes, a working set. Do the actual work in smaller, focused windows.

**The pattern:** wide ingest → distill into artifacts → execute in smaller windows

This isn't a theory. Anthropic published testimonials from companies using 1M context — Ramp, Obvious, Cognition, Hex — and every single one describes the same thing. None of them are saying "we dumped more in and the execution got better." They're saying the **reading phase** stays intact longer, which makes everything downstream more coherent. Less compaction, fewer repeated passes, no loss of cross-file dependencies mid-investigation.

(Show testimonial screenshots on screen here — flick through them quickly)

![[images/1m-context-window/intake-pattern/placeholder.png]]

---

## Coding: read wide, plan deep, implement narrow

For coding, the pattern is concrete.

**The intake phase:** Load the codebase architecture, the requirements, the existing patterns, the test results. Use the 1M window to understand the full picture. Where do modules connect? What conventions exist? Where will changes ripple? Come up with a detailed plan — not a vague outline, but specific: which files change, what each change does, what the dependencies are, what could break.

**The distill step:** The plan itself is the artifact. It captures everything the intake phase understood, compressed into something actionable.

**The execution phase:** Either dispatch subagents from the same session, or start brand new sessions with the plan as input. Each worker gets the relevant slice — the files they're touching, the conventions they need to follow, the specific piece of the plan they're responsible for.

But first — why subagents at all? Why not just do everything in one session?

Because of what happens when a single session grows. Google's Gemini research put it clearly: as context grew significantly beyond 100K tokens, agents showed "a tendency toward favoring repeating actions from its vast history rather than synthesizing novel plans." The model stops thinking fresh. It starts copying what it already did instead of solving the next problem on its own terms. The context becomes a gravitational pull toward past patterns.

This is a different failure mode than retrieval decline. MRCR measures whether the model can find information in context — that drops from 91.9% to 78.3% at 1M. But there's a separate degradation in **creativity and novelty** that no benchmark currently captures well. The longer the session, the more the model recycles its own outputs instead of generating new approaches.

That's the argument for subagents. Each one starts with a clean context window. No history pulling it toward old patterns. It solves its specific task fresh. The implementation quality stays high because each worker is thinking, not repeating.

But subagents create a different problem: every time one reports back, it adds a few thousand tokens to the main session — the files it changed, decisions it made, tests it ran. After 5-6 reports, that's 20-30K tokens of summaries on top of the plan, the architecture, and your messages. Before 1M, this is where the coordinator would hit compaction. The original constraints get lost. Subagent 7's work contradicts subagent 2's, and the coordinator can't catch it because subagent 2's report got compacted away.

**This is what 1M actually solves.** The coordinator can now absorb 10, 15, 20 subagent reports without compacting. It holds the full plan and every report. It catches contradictions. The 15th review is just as informed as the 1st.

So you have a choice about how to use a session:

**Path 1 — Do the implementation directly.** One session, coding in context. This is fine up to about 200-300K tokens. Beyond that, the session starts degrading — repeating patterns, losing freshness, gravitating toward what it already did. If your task fits in that budget, this is simpler and works.

**Path 2 — Coordinate subagents.** The session focuses on planning and reviewing. Implementation happens in fresh subagent windows. Each subagent thinks clean. The coordinator remembers everything. Before 1M, you could sustain maybe 5-6 cycles before the coordinator hit compaction. Now you can sustain 15-20+. Use this for anything that's too big for a single session's effective range.

Reading and planning happen in the big window. Implementation happens in focused ones.

![[images/1m-context-window/coding-pattern/placeholder.png]]

---

## Data analysis: same files, different angles

For data analysis, the intake pattern plays out differently.

Say you have 12 files to analyze. Load all 12 into a 1M session. It sees how files relate to each other, spots cross-cutting patterns, identifies contradictions between them. But it might miss details within individual files — attention is spread across a million tokens.

Here's a technique that exploits how these models actually work: **load the same files in different orders.** Models have recency bias and positional effects — what they read last gets more attention, and the connections they make depend on what's fresh. So run the analysis multiple times, each time shuffling the order the files appear in the context.

Session 1 might load files A through L in order. It catches the pattern between A and B because they're adjacent. Session 2 loads them L through A — now it catches the connection between L and K that session 1 missed because those were stale by the time it reached conclusions. Session 3 loads them in a random order and catches something neither of the first two found.

Each session sees the same data but makes different connections depending on the ordering. Combine the insights and you get coverage that no single pass achieves.

Same structure works for:
- **Production logs** — load chronologically, then reverse, then grouped by severity
- **Legal documents** — load by date, then by party, then by clause type
- **Research** — load by author, then by methodology, then by conclusion

The 1M window lets you load everything at once. The different orderings make sure you actually find everything that's in there.

![[images/1m-context-window/data-analysis/placeholder.png]]

---

## Simple tasks just work now

Not everything needs this orchestration. Sometimes you're replying to 30 emails. Reviewing a batch of PRs. Translating content. Renaming things across a codebase.

For repetitive, low-effort work, 1M context is a straight upgrade. Just keep going. The model doesn't need to hold complex architectural decisions — it needs to maintain a simple pattern across many repetitions. Long context is built for this.

Chrome browser automation is the clearest example. If you're using Claude Code to control Chrome — replying to emails, filling out forms, working through a checklist — the session can now handle 30-40 actions without compacting. Before, you'd lose continuity halfway through a 15-step browser workflow.

For simple tasks, the intake and the execution are the same thing. There's nothing to distill, nothing to dispatch. You're just doing a long sequence of easy things. The bigger window means you don't run out of runway.

The distinction is **task intensity.** Simple and repetitive? Let the window fill up. Complex and creative? Read wide, then work narrow.

![[images/1m-context-window/simple-tasks/placeholder.png]]

---

## When to start fresh

**Does the accumulated context help or hurt what you're about to do?**

If you finished implementing feature A and you're moving to feature B — start a new session. Unless feature B directly depends on feature A (same module, shared state, tight coupling), the context from A is noise. Thousands of tokens about a solved problem, making the model attend to things that don't matter anymore.

If you finished a feature and want to write tests for it — keep going. That context is pure signal.

If you're coordinating a big project across many subagents — stay in the session. The coordination context is cumulative. Every subagent report builds on the last. This is exactly what the 1M window buys you.

When the project is done, start fresh. The context from the last project isn't helping the next one.

**The one-liner version:** 1M tokens doesn't mean one session all day. It means the sessions that need to be long can finally be long — and the rest should still be short.

![[images/1m-context-window/when-to-start-fresh/placeholder.png]]
