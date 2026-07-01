---
title: "What the Best Agents Share — Mardu Swanepoel, Flinn AI"
video_url: https://www.youtube.com/watch?v=7CrPrHgoEYk
video_id: 7CrPrHgoEYk
channel: AI Engineer
published: 2026-05-26
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**What the Best Agents Share — Mardu Swanepoel, Flinn AI**](https://www.youtube.com/watch?v=7CrPrHgoEYk) - AI Engineer - uploaded 2026-05-26

> next-step videos available: two complements to the multi-model and steering chapters (one spine already covered)

## 1. The ideas worth a video

- **Reversibility is a delegation multiplier: bound the worst-case cost and you delegate bolder, riskier, higher-value work.** It is the spine because it reframes undo from a safety nicety into the thing that changes what you hand off, and its top rung (best-of-N model racing) is a concrete film-able demo. VERDICT: 🔗 next-step video available.
- **Transparent execution turns delegation into collaboration: watch the live to-do list and every tool call's I/O so you intervene at step two, not step twenty.** Spine because it captures both payoffs of transparency (trust + early interruption to cut waste) in one reframe. VERDICT: 🔗 next-step video available.
- **Speed to understanding beats speed to output: personalize the agent with your own methods so it does the right thing, not just something.** Load-bearing for reading the talk, but the technique (CLAUDE.md, skills, memory) is deeply covered by ACS. VERDICT: ✅ already covered.

*Not promoted:* **focus modes** (constrain the action space to raise output quality). For a coding-agent user this is plan mode / scoped subagents, which ACS covers; no distinct new video.

## 2. Summary + counts

Mardu Swanepoel of Flinn AI reverse-engineers Harvey, Cursor, Manus, and Claude to extract four shared agent patterns: focus modes, transparent execution, personalization, and reversibility.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

## 3. 🔬 Deep dive

**Spine 1 — Reversibility as a delegation multiplier.**
The claim: reversibility is not a safety nicety, it is the lever that decides how much you are willing to delegate. Most people treat undo as insurance for when things go wrong; the speaker's point is stronger. Because the worst case is now known and capped, roll back a single line, a file, or a whole conversation, the ROI math on a risky handoff flips positive, so you attempt the ambitious task instead of doing it by hand. As he puts it, bounding "the cost of our mistakes" makes users "bolder and much more prone to actually taking risks." In a coding agent this maps cleanly: git checkpoints and worktrees are your reversibility layer, and the top rung is best-of-N, running the same prompt through Claude Code and Codex in parallel, then keeping the strongest diff and discarding the rest exactly because undo is free. It goes wrong two ways. Reversibility you do not trust, partial undo or uncommitted state, makes you more timid, not less. And free undo can breed spray-and-pray prompting, where you launch attempts instead of thinking one through.

**Spine 2 — Transparent execution turns delegation into collaboration.**
The claim: surfacing the live to-do list and every tool call's inputs and outputs turns delegation into collaboration. The non-obvious part is the reason. Teams ship transparency as a trust or polish feature, but its larger payoff is economic. When you can see the agent's next step and what it just read, you catch a wrong assumption at step two, the agent pulled "Notion docs A and B" it never should have, and redirect before the error compounds. The cost of that mistake becomes one step, not twenty, which is the waste reduction the speaker highlights. Trust is the second effect: "if I give you a task and you come back with just simply the results, I will have less of trust" than if the process is visible. For a coding agent this is the discipline of reading the plan and watching tool calls to steer mid-run rather than fire and forget. It fails when transparency has no cheap intervention handle, visibility without an interrupt is just noise, and when the detail firehose is so dense that people stop watching entirely and lose the early-catch benefit.

**Spine 3 — Speed to understanding, not speed to output (covered).**
The claim: personalize the agent with the methods you would use yourself, optimizing for speed to understanding rather than speed to output. The trap is treating fast output as the goal. As the speaker notes, "it's very easy to just generate an output for a user, but if it's not really in line with what the user wants," it is useless, so the raw speed was wasted. The mechanism: front-loading your principles, playbooks, and memory shrinks the gap between what you asked and what you meant, so the agent does "the right thing and not just something." Harvey's playbooks encode a firm's contract-review method so the agent works the firm's own way. In a coding agent the same move is CLAUDE.md, skills, memory, and a project glossary, all of which ACS already teaches in depth, which is why this spine gap-checks to covered. It fails through over-personalization: stale or bloated rules mislead the agent and inflate context cost, so the personalization meant to speed understanding starts degrading it instead. Excluded from the pitches below.

## 4. 🎬 Proposed ACS videos

**1. Race Your Models: Run One Task Through Multiple CLIs and Keep the Winner**
- HOOK: The cheapest quality upgrade is generating the same change three ways and throwing two away.
- THE PROMISE: For engineers who already use git as a safety net, spend spare agent capacity on parallel best-of-N runs and select the strongest diff.
- THE SHAPE: (1) Why reversibility, not raw model IQ, is what lets you take bigger swings. (2) Set up checkpoints and worktrees so any run is undoable at line, file, or conversation level. (3) Fire the same prompt at Claude Code and Codex in parallel. (4) Diff-review the outputs, keep one, discard the rest. (5) When best-of-N beats a single careful run, and when it just burns tokens.
- SPINE: 1 (reversibility as a delegation multiplier).
- SLOT: Advanced Techniques → Multi-Model & Multi-CLI Workflows.
- RELATIONSHIP: 🔗 complements "Combining CLIs & Models" (that video has one model implement and a second critique the diff, then converge); this is the parallel best-of-N variant where several models implement the SAME task independently and you select the winner, framed by reversibility. Do not re-teach the critique loop.
- PROOF TO REUSE: the "we're binding the cost of our mistakes" ROI framing; "it actually gives the ability to really do multiple outputs with the same input in parallel using different models"; "we will undo all but ideally one of our outputs."

**2. Steer at Step Two, Not Step Twenty: Reading Your Agent's Live Tool Calls**
- HOOK: Most wasted agent runs were salvageable three tool calls in, if you had been watching.
- THE PROMISE: For Claude Code users who fire and forget, read the live to-do list and each tool call's inputs and outputs so you redirect a wrong approach before it compounds.
- THE SHAPE: (1) Delegation versus collaboration: why watching beats waiting. (2) Read the to-do list to see the next step before the agent takes it. (3) Spot the tell, a wrong file read or wrong assumption, at step two. (4) Interrupt and redirect versus letting it finish. (5) Calibrated trust: process visibility makes you actually believe the final answer.
- SPINE: 2 (transparent execution as collaboration).
- SLOT: Master Claude Code → The Fundamentals (the Claude Code counterpart to Codex's "Queuing vs Steering").
- RELATIONSHIP: 🔗 complements "Queuing vs Steering" (Codex-app follow-up mechanics: queue later, steer now); this teaches the transferable Claude Code principle, watch transparent execution to intervene early and cut wasted work. That video already covers the queue-vs-steer keystroke mechanics, so lead instead with the "catch it at step two" discipline.
- PROOF TO REUSE: "the crux ... is to shift from delegation to collaboration"; the step-two "Notion docs A and B" example; "it also enables the user to intervene at an earlier point in time ... thereby reducing waste."

## 5. 📚 Full wisdom (reference)

**SUMMARY** — Mardu Swanepoel of Flinn AI studies Harvey, Cursor, Manus, and Claude to extract four shared patterns that make the best agents effective.

**IDEAS**
- The best agents across law, coding, and general work share four patterns despite completely different domains.
- Focus modes constrain the action and input space so engineers can tune output quality more tightly.
- A constrained mode lets you drop tools, refine the system prompt, and optimize evals more effectively.
- Modes also align user expectations, telling them what inputs and behavior suit this particular agent state.
- Cursor planning mode writes no code: it produces a plan and asks you clarifying questions instead.
- Cursor debug mode uses a hypothesis-driven approach, spinning up a dedicated debug server pushing logs there.
- Transparent execution surfaces the agent's tools, thoughts, and actions, shifting delegation toward genuine collaboration with users.
- Sharing the agent's process, assumptions, and uncertainties builds more trust than returning only a finished result.
- Transparency lets users intervene early, stopping a wrong approach at step two and reducing wasted work.
- Claude Cowork shows a live to-do list, the context used, skills drawn from, and tool inputs/outputs.
- Personalization gives the agent the thoughts, systems, principles, and patterns you would use doing it yourself.
- Most agents optimize speed to output, but the real goal should be speed to understanding instead.
- Harvey playbooks encode a legal firm's methods so the agent reviews contracts the firm's own way.
- Reversibility bounds the cost of mistakes, making the ROI of delegating a risky task clearly calculable.
- Cursor supports rollback at line, file, and conversation levels, undoing several messages of recent agent changes.
- Cursor runs multiple outputs from one input in parallel using different models, keeping only the best.
- Bounded downside makes users bolder, prone to tackling higher-value tasks they would otherwise avoid delegating entirely.

**INSIGHTS**
- Cross-domain convergence suggests these four patterns are agent design fundamentals, not quirks of any single product.
- A narrow, constrained mode is far easier to optimize than an open-ended agent that attempts everything.
- Trust in agent output scales with visible process, not with the polish of the final answer.
- Early intervention is cheaper than late correction: catching a wrong turn at step two saves rework.
- An output produced fast but misaligned with implicit user standards is effectively useless, wasting the speed.
- Encoding your methods upfront makes the agent do the right thing, not merely something vaguely plausible.
- Capping worst-case cost reshapes delegation decisions, converting hesitation into willingness to attempt ambitious agent tasks confidently.
- Granular rollback, line to conversation, lets users experiment freely since any bad path is easily undoable.
- Parallel model outputs trade cheap compute for quality: generate several, keep one, discard all the rest.

**QUOTES**
- "Steal ... going and looking at something, studying it deeply, really understanding it, and making it your own." — Mardu Swanepoel (glossing Picasso)
- "The biggest benefit is for us as engineers, we get the ability to improve the agent's output quality on the smaller constrained action space." — Mardu Swanepoel
- "The crux of what we're trying to achieve here is to shift from uh delegation to collaboration." — Mardu Swanepoel
- "If I give you a task and you come back with just simply the results, I will have less of trust in the results." — Mardu Swanepoel
- "Optimizing for speed to understanding ... is really critical for agent to do the right thing and not just something." — Mardu Swanepoel
- "The agent would then do it in the same way as what your legal firm would have done it." — Mardu Swanepoel
- "The big thing that we are achieving from this is we're binding the cost of our mistakes." — Mardu Swanepoel
- "This number one then results in users being bolder and much more prone to actually taking risks and tackling higher value tasks." — Mardu Swanepoel
- "You can worst case just undo and and carry on." — Mardu Swanepoel

**HABITS**
- He keeps the Picasso steal quote close to him while personally developing his own AI agents.
- He studies leading agents deeply first, then adapts their patterns into his own improved agent builds.
- For each pattern he explains what it is, its user value, then a real product example.
- He drops unnecessary tools and refines system prompts before optimizing evals on constrained action spaces first.
- He relies on Claude Cowork, valuing its transparent to-do list and visible tool-call inputs and outputs.

**FACTS**
- Harvey offers playbooks that encode a law firm's contract-review methods for the agent to follow directly.
- Harvey ships as a Microsoft Word add-in integrating with the native Word API for tracked edits.
- Cursor exposes selectable modes via a dropdown, including planning, debug, and other specialized agent behaviors too.
- Cursor rolls back changes at line, file, or conversation granularity, and runs parallel model outputs too.
- Claude offers skills, connectors, and memory-like systems to expand knowledge and improve the agent's personalization directly.
- Manus displays task progress showing completed and pending steps plus what it examined and concluded overall.

**REFERENCES**
- Pablo Picasso ("good artists copy, great artists steal" / the "steal" quote)
- Cursor (focus modes, granular rollback, parallel model outputs)
- Claude and Claude Cowork (transparent execution, skills, connectors, memory)
- Harvey (playbooks, memory, Microsoft Word add-in via native Word API)
- Manus (task progress display)
- Notion (example docs the agent might read)
- Mardu Swanepoel, Flinn AI (speaker and company); AI Engineer (conference / channel)

**ONE-SENTENCE TAKEAWAY** — Steal from the best agents these four patterns: focus modes, transparency, personalization, and genuine reversibility.

**RECOMMENDATIONS**
- Add explicit modes to your agent so users know what inputs each constrained state expects clearly.
- Constrain one focus mode first, drop tools, tighten the prompt, and optimize evals before expanding.
- Surface every tool call's inputs and outputs so users can intervene before the agent goes further.
- Show a live to-do list so users see the next step before the agent takes it.
- Build playbooks capturing how you personally do a task, then have the agent replicate them.
- Optimize your agent for speed to understanding, not just fast output that misses your real intent.
- Add reversibility at multiple granularities so users can undo a line, file, or whole conversation cleanly.
- Generate several parallel outputs with different models, keep the best, and discard all the rest afterward.
- Bound the worst-case cost of agent actions so you feel safe delegating riskier, higher-value tasks confidently.
