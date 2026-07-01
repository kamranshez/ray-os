---
title: Applying 12-Factor Principles to Coding Agent SDKs
videoId: qgAny0sEdIk
url: https://www.youtube.com/watch?v=qgAny0sEdIk
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1 (MASTER): If you know the workflow order, encode it as deterministic control flow, not a prompt, and use typed structured outputs as the seams between the LLM phases.**
This subsumes the two-levers claim, the accuracy-compounding chart, the "control flow via prompt" anti-pattern, breaking the monolithic create-plan prompt into phases, and wrapping Ralph in a harness.
VERDICT: ❌ net-new video available.

**Spine 2: The background verification agent, run the fast golden path in the foreground while an expensive agent verifies in the background and pings you.**
This is how you give a human-in-the-loop workflow both speed and consistency instead of trading one for the other.
VERDICT: 🔗 next-step video available (complements subagent verification loops).

**Spine 3: A diffable dependency-graph diagram plus pre-commit boundary enforcement to stop vibe-coded architecture from rotting.**
Generate the graph, diff it to catch bad new edges, and let CI emit compiler errors when a package imports what it must not.
VERDICT: 🔗 next-step video available (complements "What Breaks If I Change This?").

---

# Summary + counts

Dex (Human Layer) and Vibhav (BAML), with guest Mike, apply 12-factor-agent principles to coding SDKs: replacing prompt control-flow with deterministic workflows joined by structured outputs.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1 — Control flow belongs in code, not in a prompt

**The claim.** If you already know the order the steps run in, you do not need an agent for that part; encode it as deterministic control flow and reserve the model for genuinely undefined transitions.

**Why it is non-obvious.** The 12-factor-agents promise was seductive: give the model a bag of tools and a loop, write less code. So people push everything into one giant prompt with sequential "you must, critical, never" instructions, what Dex names "control flow via prompt."

**Why it is true.** Because reliability is step-count times per-step accuracy: even at 99 percent per step, twenty chained undefined transitions veer off course fast. And because a model attends to only about 150 to 200 instructions before losing track, a hundred-plus-instruction prompt silently skips the steps that mattered. Therefore the fix is fewer undefined steps: break the workflow into phases, each ending in a typed structured object (current state, desired end state, an open-questions array), and let plain code advance when that array empties.

**What it generalizes to.** Classic classifier design: a cheap CPU model handles the thousand common categories, an "other" bucket escalates to an expensive LLM. Same shape, different domain.

**How it goes wrong.** Over-codify and you lose the model's ability to wiggle out of an unforeseen error, and, as Vibhav found, "the more I codified it, the less other people wanted to do it."

## Spine 2 — The background verification agent

**The claim.** Run the fast golden path in the foreground and put the expensive checking in a background agent that pings you, so the user gets speed and consistency at once.

**Why it is non-obvious.** People treat speed and reliability as a straight trade: interactive back-and-forth is accurate but slow, one-shot is fast but wrong 5 percent of the time. The instinct is to pick a point on that line.

**Why it is true.** You do not have to pick. Because the foreground loop assumes correctness and moves, it stays fast; because a separate expensive agent re-checks the design phase asynchronously, it stays correct. When the background agent finds something you missed, it surfaces a prompt, append this insight, roll back to design, or ignore, so the human only pays attention at the moment a decision actually needs them. Dex extends the same idea to running research in the background and injecting insights as messages mid-conversation.

**What it generalizes to.** Any mission-critical human-in-the-loop pipeline, not just coding: Mike's team gets a Slack message, "all comments taken care of" or "you missed these, deliberate?"

**How it goes wrong.** The background agent needs a crisp scope (just the design step, not the whole conversation) or it becomes an expensive loop that never converges, and interruptions can derail a user who was in flow.

## Spine 3 — A diffable map that stops vibe-coded architecture from rotting

**The claim.** Generate a dependency-graph diagram of your codebase, diff it to catch bad new edges, and enforce boundaries with pre-commit hooks so leakage cannot compound.

**Why it is non-obvious.** When you vibe code, "dependencies and abstractions start leaking really poorly, and once that happens you diverge and it will only get worse over time." The rot is invisible until review is impossible, and most people never think to make the structure itself an artifact.

**Why it is true.** Because a 485-line SVG of the control flow is small enough to pass to any agent, and diffable, the agent (or a human) can look only at the diff and say "you added a bad dependency" without reading all the code. Because graph layouts are unstable, one added node reshuffles everything, you pass it as an image for review, not raw SVG. And because CI can emit a compiler error when a non-compiler package imports a compiler package, the boundary is enforced, not merely documented.

**What it generalizes to.** Context hygiene generally: the same team enforces warning-free builds because build-step warnings inject noise that bloats the agent's context window.

**How it goes wrong.** The map drifts if you trust a stale copy, so it must be regenerated from real code, and layout instability means you cannot cheaply regenerate it in CI for diffing.

---

# 🎬 Proposed ACS videos

## 1. If You Know the Steps, Don't Use an Agent (rank 1)

- TITLE: If You Know the Steps, Don't Use an Agent
- HOOK: Dex spent two hours making an agent do what a 90-second bash script already did.
- THE PROMISE: For engineers building coding-agent workflows, after this you will know exactly when to hardcode a workflow and when to hand the wheel to the model.
- THE SHAPE: (1) the make-file agent story and its lesson; (2) the two levers plus the accuracy-compounding chart (99 percent over 20 steps); (3) "control flow via prompt" as the anti-pattern, a hundred-plus instructions the model silently skips; (4) break the create-plan prompt into a design phase and a structure phase, each with a structured-output schema; (5) deterministic code advances only when the open-questions array is empty.
- SPINE: 1
- SLOT: Techniques class > new "Agent Architecture" chapter (adjacent to Context Engineering's research/plan/implement).
- RELATIONSHIP: ❌ net-new. Context Engineering teaches the research/plan/implement loop itself; nothing in the catalog teaches the architectural reframe of replacing prompt control-flow with deterministic code joined by typed structured outputs.
- PROOF TO REUSE: the make-file / 90-seconds story; "the only two things you can do is have fewer steps or a more accurate step selection system, everything else is totally garbage"; the empty-open-questions-array advance trick.

## 2. The Background Agent That Checks Your Work (rank 2)

- TITLE: The Background Agent That Checks Your Work
- HOOK: Let the user fly down the golden path, and put the expensive checking in the background.
- THE PROMISE: For anyone building human-in-the-loop agent workflows, after this you can give users speed AND consistency instead of trading one for the other.
- THE SHAPE: central demo, kick off the fast design phase in the foreground; spawn an expensive background agent that evaluates the design as it runs; when it finds something you missed, it pops up or pings Slack asking whether to append the insight, roll back to the design phase, or ignore it.
- SPINE: 2
- SLOT: Claude Code class > background agents (or Techniques, as the async sibling of subagent-verification-loops).
- RELATIONSHIP: 🔗 complements "subagent-verification-loops" (Techniques backlog), which teaches spawning subagents to verify work synchronously; this adds the asynchronous, notification-driven pattern where the verifier runs beside a fast foreground loop and only interrupts you when it finds something.
- PROOF TO REUSE: Dex's "constant re-research in the background" idea with insights injected as messages; Mike's Slack "all comments taken care of" / "you missed these, deliberate?" notification; Vibhav's "that's the only way to give the user the balance of speed along with consistency."

## 3. The Diffable Architecture Map That Stops Vibe Rot (rank 3)

- TITLE: The Diffable Architecture Map That Stops Vibe Rot
- HOOK: A 485-line SVG of your codebase, diffable, so the agent catches a bad dependency in seconds.
- THE PROMISE: For anyone vibe-coding a growing codebase, after this you can stop architectural leakage before it compounds, using one diagram and a pre-commit hook.
- THE SHAPE: (1) vibe coding leaks abstractions and it only gets worse over time; (2) generate a dependency-graph SVG of the codebase; (3) pass it as an image to the agent (layouts are unstable) and diff the SVG to catch bad new edges; (4) add pre-commit hooks that emit compiler errors when a package imports what it must not, and enforce warning-free builds to cut context bloat.
- SPINE: 3
- SLOT: Context Engineering class > Understanding the System (next to "What Breaks If I Change This?").
- RELATIONSHIP: 🔗 complements "What Breaks If I Change This?", which has the agent draw a one-off blast-radius diagram before a single edit; this adds the persistent, regenerated, diffable architecture map plus pre-commit enforcement that keeps the boundaries honest continuously, not just at one change.
- PROOF TO REUSE: "dependencies and abstractions start leaking really poorly and it will only get worse over time"; the 485-line diffable SVG passed as an image; the CI rule that only compiler and LSP packages may call compiler packages; "every build step you run needs to run warning free."

---

# 📚 Full wisdom (reference)

## SUMMARY
Dex (Human Layer) and Vibhav (BAML), with guest Mike, apply 12-factor-agent principles to coding SDKs: replacing prompt control-flow with deterministic workflows joined by structured outputs.

## IDEAS
- Only two levers exist: fewer steps or a more accurate step-selection system; everything else is garbage.
- If you already know the workflow order, you probably do not need an agent at all.
- Dex spent two hours coaxing a two-tool agent to do what a bash script did instantly.
- Even at ninety-nine percent per-step accuracy, twenty chained steps compound errors and veer off course fast.
- LangChain's cognitive-architectures chart plots autonomy against determinism: code, one call, a chain, router, fully autonomous agent.
- Dex calls stuffing sequential instructions into one giant prompt control-flow-via-prompt, an anti-pattern that fails on errors.
- Each workflow phase emits a typed structured object, letting deterministic code decide when to advance stages.
- The design phase returns an open-questions array; deterministic code advances only once that array is empty.
- HumanLayer's create-plan prompt packed over a hundred instructions; models silently skipped the most important steps.
- Kyle's blog cited frontier models reliably following only about 150 to 200 instructions before losing track.
- Feedback given early in the context window steers far more cheaply than corrections after token-heavy output.
- Editing a plan with consistency is much harder than creating one, because feedback scatters across trajectory.
- Everyone building AI starts fully agentic for input variance, then codifies toward consistency after learning inputs.
- Composing loops within loops lets a system gain both consistency and tolerance for input variance simultaneously.
- A tiny CPU classifier handles common categories cheaply; an 'other' bucket escalates rare cases to LLMs.
- Run the golden path fast while an expensive background agent verifies and pings you about problems.
- Jump straight into design discussion while research runs in the background, injecting new insights as messages.
- Wrap Ralph's while-true loop inside a deterministic harness using structured-output exit conditions instead of raw bash.
- Mike's Wreckit stores plans as PRD.json with a todo/in-progress/done status enum so non-model code orchestrates features.
- A 485-line SVG dependency graph is diffable, so agents catch bad new dependencies from the diff.
- Graph layouts are unstable, so pass the diagram as an image, not SVG, to reviewing agents.
- Pre-commit hooks emit compiler errors when a package imports a compiler package it should never touch.
- Enforce warning-free builds because build-step warnings inject noise that compounds into serious agent context bloat over time.
- Plans are too long to review; HumanLayer now reviews the shorter structure outline for mental alignment.

## INSIGHTS
- Reliability is step-count times per-step accuracy, so long undefined agent chains degrade fast for longer tasks.
- Deterministic workflows shatter on unforeseen errors; an LLM step can improvise a recovery you never anticipated.
- Mature AI systems compose loops within loops, buying both consistency and wide input tolerance at once.
- Structured outputs are the seam that lets probabilistic LLM phases plug cleanly into deterministic orchestration code.
- Context-window position is leverage: early cheap back-and-forth reshapes trajectory before expensive committed tokens lock it in.
- Codifying a repeated workflow trades a little variance for the consistency repeated team tasks actually demand.
- Process checkpoints like code review exist to cap entropy; agent workflows need the same deliberate gates.
- An opinionated coding agent is a style guide: it makes the correct choice the default path.
- Human leverage is migrating upstream from writing code toward the design decisions agents cannot safely make.
- Ironically, the more someone rigidly codifies a workflow, the less their teammates want to adopt it.
- Design docs can live outside code because code evolves faster than the design that checkpointed it.

## QUOTES
- "The only two things you can do is have fewer steps or have a more accurate step selection system. Everything else is totally garbage in terms of making your system better." — Dex
- "Not everything is a good task for an agent. And if you know the order stuff is going to happen in, then you probably don't need it." — Dex
- "This is what I call like control flow via prompt." — Dex
- "Editing with consistency is a much harder task than creating with consistency." — Vibhav
- "You just want to reduce the number of things it has to think about." — Dex
- "The more I codified it, the less other people wanted to do it." — Vibhav
- "Don't use prompts for control flow. If you know what the workflow is, use control flow for control flow because it's very very good." — Dex
- "It makes the default thing the correct thing instead of them having to learn how to do the stuff." — Dex
- "There's a place for what I term classical AI state machines, behavior trees. These are control flows that have been with us for 30 years, and now we're trying to insert this agentic loop with all this non-determinism, and you need both." — Mike
- "Consistency is actually way more variable, way more useful than variance." — Vibhav
- "Compaction is lossy and you lose intent." — Mike
- "You have a file as a source of truth, but you also want something where humans can collaborate." — Vibhav
- "How do you move the SDLC upstream? And how do you automate as much of it as possible? Well, making sure that humans have leverage over the parts that matter." — Dex

## HABITS
- Dex kicks off two plan attempts, running the fast one first and restarting deterministically if wrong.
- Rather than steering a derailed plan mid-flight, Dex deletes it and restarts from a deterministic path.
- The team spends significant time building tooling to evaluate generated code, not just generating the code.
- Mike reviews teammates' AMP agent threads as his primary coaching tool for climbing the agentic-coding curve.
- The team enforces warning-free builds and wraps git subtrees in workspace CLI tools to avoid friction.
- Vibhav keeps context windows out of the dumb zone, avoiding lossy compaction by exiting contexts early.
- They review the short structure outline instead of the thousand-line plan to reach mental alignment faster.
- Vibhav exports design docs to folders, edits them with Claude Code, then reimports as linear versions.
- Dex rotates between Claude Code, Cursor, and Antigravity, usually just reusing whichever model was last selected.
- An AI assistant checks every design-doc comment and verifies whether each one was actually addressed manually.

## FACTS
- LangChain published a cognitive-architectures chart ranking agent systems by autonomy versus determinism years before this discussion.
- Kyle's blog post cited a study showing frontier models reliably follow roughly 150 to 200 instructions.
- Sprites.dev by Fly.io launched just days before recording, offering stateful cloud sandboxes managed programmatically via API.
- Vibhav's dependency-graph SVG for the BAML compiler is only 485 lines long yet fully diffable today.
- Mike manages over twenty Elixir packages as git subtrees and teaches AI coding to twenty-five engineers.
- Mike built his Wreckit CLI, wrapping Ralph Wiggum in a structured workflow, in a 24-hour vibe-code.
- The burrito-delivery SaaS vibe-coding benchmark originated with Ben Swearlo over at Freestyle, not the show hosts.
- Dex's make-file agent failure ran on Sonnet 3, well before the notably stronger Sonnet 3.5 shipped.

## REFERENCES
- 12 Factor Agents (methodology and talk, "it's everywhere")
- "Advanced context engineering for coding agents" (their episode 85)
- LangChain cognitive-architectures chart (autonomy versus determinism)
- HumanLayer create-plan prompt (the OG research-to-plan prompt)
- BAML / BoundaryML (Vibhav's programming language for reliable AI systems)
- Claude Agent SDK (wrapped with a non-TUI UI in the demos)
- AMP agent (used alongside Claude Code by Mike's team)
- Claude Code, Cursor, Antigravity (agents/editors Dex rotates between)
- Ralph Wiggum technique (the while-true loop)
- Kyle's blog post on writing a good plan.md (with the instruction-following study)
- Ryan Carson's PRD.json approach (structured plan capture)
- Ben Swearlo / Freestyle (burrito-delivery vibe-coding benchmark)
- Sprites.dev by Fly.io (stateful cloud sandboxes)
- git subtrees (versus submodules)
- Mike's Wreckit CLI and his GTO open-source project
- bun, cargo, make, just (build tooling mentioned)
- AI Engineer World's Fair (where Dex and Mike met)
- Next episode: a coding agent that uses email as an API

## ONE-SENTENCE TAKEAWAY
If you know the workflow order, encode it as deterministic control flow, not a prompt.

## RECOMMENDATIONS
- Before building an agent, ask whether you already know the step order; if so, script it.
- Break a giant multi-step prompt into separate phases, each emitting a typed structured-output object between them.
- Advance your workflow phases with deterministic code checking a structured field, like an empty open-questions array.
- Give feedback early in the conversation, before the model dumps a thousand-line plan you must rewrite.
- Start broad and agentic, then codify happy paths into control flow as you learn real inputs.
- Run the fast golden path while a background agent verifies and pings you about surprising issues.
- Wrap your while-true Ralph loops in a harness with structured-output exit conditions instead of raw bash.
- Generate a diffable dependency-graph diagram so agents and reviewers catch bad new dependencies from the diff.
- Add pre-commit hooks that fail the build whenever packages import dependencies they should never touch anywhere.
- Enforce warning-free builds so noisy build-step output never needlessly bloats your coding agent's active context window.
- Review the short structure outline rather than the full plan to reach mental alignment much faster.
