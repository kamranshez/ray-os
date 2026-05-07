---
tags: [youtube, script, claude-code, codex]
status: draft
date: 2026-05-04
---

# Codex /goal vs Ralph

| # | Title | Formula |
|---|---|---|
| 1 | OpenAI Just Built Ralph Into Codex | Bold claim + specificity (references a known pattern) |
| 2 | Codex Just Learned to Know When It's Actually Done | Bold claim + anthropomorphism |
| 3 | The Hidden Codex Command That Changes How Long Agents Run | Curiosity gap + exclusivity |

**Recommended:** #1. References Ralph by name, which makes the pattern-aware audience lean in immediately, and "Built X Into Y" framing has worked on this channel before. #2 is the safer fallback if Ralph is too niche a reference.

**Coined term anchor:** "pre-decomposable vs unfolding work" (the framework). "Vibes-based completion" planted in the problem section as the shared enemy.

**Format:** single-feature deep dive, ~10 minutes.
**Pitch:** masterclass, soft anchor at 1:30, soft close (no live urgency deadline this week).

---

## [0:00 -- 0:25] HOOK -- 3 beats

So after Claude and Basile became shit, I've been using Codex more and more lately. 

*Cut to terminal: `/goal ship the auth-rewrite branch --token-budget 200000`*

You give it one objective, optionally a token budget, and Codex just keeps working on it. Across turns. Without you saying continue. Until it can prove it's done.

---

## [0:25 -- 1:30] THE PROBLEM -- vibes-based completion

You've probably hit this. You kick off an agentic task. Something real -- not "rename this variable" but "ship this feature." It runs for 20 minutes. It reports back: "done." You check.

It's not done.

Maybe three of the five files it was supposed to touch have stale code. Maybe the tests it claimed pass were never actually run. Maybe it just... declared victory because it ran out of energy.

This is **vibes-based completion.** The agent thinks it's done because it *feels* done. It put in effort. It generated a lot of output. The summary message sounds confident. But nobody actually checked the work against the requirements.

*Show: typical agent transcript ending in "✓ All tasks complete!" -- then a `git diff` showing two of the four files unchanged.*

Every long-running agent loop is, fundamentally, a system for preventing vibes-based completion. That's the whole game. And there are two completely different bets about how to win it.

---

## [2:00 -- 3:30] BET ONE: RALPH (throw the context away)

*Visual: the Ralph flowchart. Bash spawning fresh `claude` processes one after another.*

Ralph's bet is that the enemy is your context window. Specifically, the longer a thread runs, the worse the agent gets. It drifts. It forgets the original goal. It starts repeating mistakes from earlier in the conversation. By turn 30, your once-sharp agent is basically drunk.

So Ralph kills the context. Every iteration spawns a fresh `claude` process with a clean context window. The only memory between iterations is three files on disk:

*Show file tree: prd.json, progress.txt, AGENTS.md*

- `prd.json` -- a list of user stories, with a `passes: true` flag for each one
- `progress.txt` -- an append-only log of learnings the agent writes after each iteration
- And the git history itself

*Show: ralph.sh terminal output looping through iterations 1, 2, 3...*

The bash loop is dumb on purpose. Spawn Claude. Pick the highest-priority story where `passes` is false. Implement it. Run typecheck and tests. If green, commit. Mark passes true. Append a learning. Repeat. When all stories pass, the model emits `<promise>COMPLETE</promise>` and the loop exits.

That's it. That's the whole pattern. About 75 lines of bash.

The thing that makes it work isn't the loop. It's the fact that you wrote the PRD. You broke the work into stories small enough to fit in one context window. You set up real quality gates -- typecheck, tests, CI. Ralph doesn't trust the agent. It trusts the test suite.

This is a **discipline pattern.** It works because *you* did the work up front.

---

## [3:30 -- 6:00] BET TWO: /goal (keep the context, fight the drift)

*Visual: open `codex-rs/core/src/goals.rs`. Highlight the GoalRuntimeState struct.*

Codex's `/goal` makes the opposite bet. It says: continuity is the feature. The agent has just been working on this problem -- throwing away its context to start fresh is wasteful. Keep the thread. Use structure to fight drift.

So instead of an external bash loop, `/goal` is a state machine baked into the Codex runtime itself. Four statuses: active, paused, budget-limited, complete.

*Show: the four state pills.*

You set one objective with `/goal <objective>`. Optionally a token budget. The runtime stores it in a per-thread state DB. Then three things happen.

**One. Auto-continuation.** When a turn finishes and there's nothing else queued, the runtime spawns its own next turn. You don't have to type anything. It injects a hidden developer message with the objective, current spend, and a very specific instruction.

*Show the continuation.md template, highlight the relevant section:*

> "Before deciding the goal is achieved, perform a completion audit against the actual current state. Build a prompt-to-artifact checklist that maps every explicit requirement to concrete evidence. Do not accept proxy signals as completion by themselves."

This is what `/goal` substitutes for Ralph's test suite. Ralph trusts the typecheck. `/goal` forces the model to do an evidence-based audit. Map every requirement to a real artifact. Treat uncertainty as not done. Keep working.

**Two. Token accounting.** Every tool call charges the goal's budget. Non-cached input plus output tokens. Cached input is free. Reasoning tokens aren't double-counted. The model can call `get_goal` to see how much budget is left.

**Three. Budget exhaustion is not completion.** This is the part that matters. When you cross the budget, the goal flips to `budget_limited`, and a different developer prompt gets injected mid-turn:

*Show budget_limit.md:*

> "The system has marked the goal as budget-limited. Wrap up this turn soon. Do not call update_goal unless the goal is actually complete."

Out of tokens does not mean done. The model is explicitly forbidden from declaring victory just because it ran out of fuel. That's a small detail and it's the entire reason this feature isn't garbage.

And one nice detail before we move on. While `/goal` is running, you're not locked out. You can type a message at any point. It doesn't interrupt the current turn -- it just gets queued, and at the next turn boundary your message lands first, instead of the auto-continuation prompt. So you can steer mid-loop. Drop a hint, redirect, narrow the scope, whatever. The runtime literally checks for queued input before deciding whether to auto-continue. Nice ergonomics.

*Show: the three model-facing tools -- create_goal, get_goal, update_goal.*

The model gets three tools. `create_goal`. `get_goal`. And `update_goal` -- which can *only* mark the goal complete. The model can't pause itself. Can't reset its own budget. Can't change the goal mid-flight. Pause, resume, and budget changes are user-only. The model gets exactly one verb: declare done.

This is an **infrastructure pattern.** It works because the runtime owns the state machine, and the model can't cheat the loop.

---

## [6:00 -- 8:00] THE INSIGHT -- pre-decomposable vs unfolding work

Now here's the part nobody's talking about. These look like two solutions to the same problem. They're not.

Watch what each pattern *requires you to know* before you start.

*Visual: split screen. Left -- Ralph. Right -- /goal.*

Ralph requires that you can write the PRD. You can list the stories. You can decompose the work into independent units small enough to each fit in one context window. If you can't do that up front, Ralph doesn't work. The whole pattern is gated on your ability to pre-decompose.

`/goal` requires the opposite. You give it one fuzzy objective and it figures out the steps as it goes. The decomposition is lazy, in the model's head, mid-thread. If you tried to give Ralph a vague objective like "make the dashboard not suck," Ralph would have nothing to do -- there are no stories to pick from.

So the question isn't "which pattern is better." It's **what shape is your work?**

Most work falls into one of two shapes.

**Pre-decomposable work** is work where you can write the list before you start. Twelve PRD items. A backlog of UI fixes. A migration that touches twenty known files. The next step doesn't depend on what just happened -- it was already on the list.

**Unfolding work** is work where each step depends on what just happened. Debugging a flaky test. Chasing a perf regression. Iterating on a UI until it feels right. There's a destination but no map. You're laying track as you go.

Pre-decomposable work belongs to Ralph. Fresh context per story is *better*, not worse, because each iteration starts focused with no distraction from previous stories. You pay less per turn and the model is sharper.

Unfolding work belongs to `/goal`. The working memory of the previous step *is* the value. Throwing it away to start fresh would force the model to re-derive context every iteration, which is expensive and lossy.

*Visual: a small decision tree. "Can I list the steps before I start?" Yes -> Ralph. No -> /goal.*

And quick aside on the compaction question, because people ask. Codex actually does compact the thread automatically. There's a whole `compact.rs` module in the runtime. When total token usage crosses the model's auto-compact limit mid-turn, the runtime replaces history with a summary and keeps going. So a long `/goal` loop is not an infinite-append thread. It's a thread that summarises itself when it gets too big.

That changes what "the model matters" actually means. It's not about context length -- Codex will compact for you. It's about **summary fidelity.** Better-reasoning models write better handoff summaries when compaction fires, which means less drift across compaction events. That's the real frontier-model advantage on long loops. But it's still the second filter. The first filter is the shape of the work. A frontier model on pre-decomposable work still loses to Ralph on cost and sharpness. A mid-tier model on unfolding work still beats forced-decomposition that doesn't fit the problem.

Stop asking which model. Start asking which shape.

---

## [8:00 -- 8:45] THE PART NOBODY'S TALKING ABOUT -- /goal makes prompting expensive again

I want to be honest with you about something. Playing with `/goal` made me realise I got lazy with prompting. GPT-5.5 is so good at inferring intent from existing context that on a normal thread, you can throw a half-formed sentence at it and it figures out what you meant. The thread is doing the prompting work for you.

`/goal` exposes this. On a fresh project, a vague `/goal` produces mush. The model has nothing to anchor on, no prior turns to absorb your intent from, and now it's about to spend the next thirty turns of autonomous work compounding whatever it guessed you meant.

**Fuzzy intent at turn one compounds across thirty turns of unsupervised work.** That's the part that's different. In normal mode, a bad prompt produces one bad turn and you correct it. In `/goal` mode, a bad prompt produces a runaway.

So the actual play is: don't run `/goal` cold. Spend two or three turns aligning on what "done" actually looks like first. Even better, do a structured setup interview before kicking off the loop -- agree on the outcome, the done criteria, the decision style, the ask-before boundaries.

*Show: screenshot of @qhn/pi-goal skill -- "Setup-first autonomous goal mode for Pi. /goal &lt;intent&gt; first opens a setup interview so the assistant and user agree on outcome, done criteria, decision style, and ask-before boundaries."*

People are already building this. The `@qhn/pi-goal` skill on Pi explicitly does not start autonomous work immediately -- `/goal` opens a setup interview first, where the assistant and the user agree on outcome, done criteria, decision style, and ask-before boundaries before the loop starts. That's the right shape. Codex's `/goal` doesn't do this yet, but you can do it manually -- treat the first few turns as the interview, and only flip to `/goal` once you've actually agreed on what done means.

This pairs with the completion audit beautifully. The audit only works if you defined the done criteria. If you didn't, the model audits against its own guess of what you wanted. That's not verification -- that's the model marking its own homework.

---

## [8:45 -- 9:15] THE HYBRID

The two patterns also compose, which I think is where this is heading.

*Visual: Ralph's outer loop wrapping around a /goal inside.*

You can run Ralph as the outer loop -- fresh context per story, gated commits, auditable PRD -- and inside each iteration, set a `/goal` to keep that single story focused with a token budget and an audit gate.

Ralph handles the macro discipline. Decomposed work, clean cut-points, real CI. `/goal` handles the micro discipline. Token-bounded, audit-gated, drift-resistant within the iteration. The bash script handles "what to do next." The state machine handles "are we done with what we're doing right now."

That's the actual answer. The interesting agent harnesses of the next year are going to be external orchestration patterns calling into agents that have their own internal loop primitives. Ralph showed the pattern in February. `/goal` is the runtime catching up to it. The next step is them working together.

---

## [9:15 -- 10:00] PRACTICAL TAKEAWAY

If you want to try this:

For Ralph, the repo is `agentic-coding-school/claude-ralph-wiggum`. Clone it, drop it into a project with a real test suite, write a PRD for a small feature, run the bash script. The hard part is writing right-sized stories.

For `/goal`, you need a recent Codex build with the goals feature flagged on. Type `/goal` followed by your objective in a Codex thread. `/goal pause` and `/goal resume` are user-controlled. The state DB persists across thread reopens, so you can walk away and come back.

And before you reach for either: ask yourself the shape question. If you can write the list, write the list. If you can't, set the objective. Don't pick a tool first and then warp the work to fit it.

One more thing. Do not run `/goal` cold on a fresh project. Spend two or three turns aligning on what done means before you flip the autonomy on. Vague intent is cheap in normal mode and ruinously expensive in `/goal` mode.

---

## [10:00 -- 10:30] SOFT CLOSE

If you're running long agentic tasks at work and you want a system for actually getting them to finish -- not just trigger and hope -- I built the Claude Code Masterclass for that exact thing. Over 1,500 engineers have taken it, and the lifetime plan is still up at the moment. Link's in the description.

Otherwise, that's the video. `/goal` and Ralph are two different bets about long agent loops. One throws context away, one keeps it. The choice isn't which model you use. It's whether your work is pre-decomposable or unfolding.

Subscribe if this is the kind of breakdown you want more of. See you next one.

---

## Production notes

- Speak ~50% slower than typical AI tutorial pace. Let the "vibes-based completion" line and the "pre-decomposable vs unfolding work" line both sit for 2-3 seconds before continuing.
- Hold on the `/goal` and `ralph.sh` side-by-side terminal shot for at least 4 seconds in the hook. That's the visual that sells the comparison.
- For the continuation.md and budget_limit.md template reveals, zoom into the highlighted text rather than showing the full file. The point is one phrase in each, not the document.
- The decision tree at 7:00 should be a literal two-node tree, hand-drawn feel, not a corporate flowchart.
- Reference HTML artifacts (built earlier today) live at:
  - `projects/agentic-coding-school/to-film/codex-app/goal-feature-explainer.html`
  - `projects/agentic-coding-school/to-film/codex-app/goal-vs-ralph.html`
  Either can be screenrecorded for B-roll on the deeper sections (the four-state diagram, the comparison table).
- No em or en dashes in any on-screen text. Use double-hyphens or rephrase.
