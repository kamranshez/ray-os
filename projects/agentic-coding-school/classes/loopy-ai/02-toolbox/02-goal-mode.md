---
duration: "12-16 min"
batch: 4
order: 11
batch_name: "The Toolbox"
class: "loopy-ai"
chapter: "/goal Mode"
aliases: [goal]
---

Ralph was a discipline. Goal mode is infrastructure.

Last segment, you ran the same prompt in a fresh window over and over by hand, with a five-line bash script holding the outer loop together. The loop lived in your shell. If your script was brittle, the loop was brittle.

Goal mode moves that exact loop down into the runtime. You set an objective once. The runtime keeps the agent working against it, turn after turn, and a separate judge decides when it's actually done. You don't babysit the "keep going." The harness owns it.

Same L3 task lifecycle. Different ownership. And that difference in ownership is the whole reason this segment exists.

---

## What goal mode actually is

`/goal` is one line: you type a completion condition, and the agent keeps working toward it without you prompting each step.

Source: https://code.claude.com/docs/en/goal

Here's the mechanism, because the mechanism is the whole point. Two models run together. Your expensive worker, Sonnet or Opus, does the actual coding. After every turn, a small fast model, Haiku by default, reads the transcript and asks one question: is the condition met?

If yes, the goal clears and control comes back to you. If no, the runtime starts another turn instead of returning to you, and it hands the worker the judge's reason so the next turn has direction.

That's it. The judge is cheap. The worker is not. So the condition you write is the dial that controls how many expensive turns you pay for.

This is the same shape Anthropic shipped first-party. The same shape OpenAI shipped in Codex. Greg Brockman described the Codex version in one line: keep working on a persistent objective until it's solved.

Source: https://x.com/gdb/status/2056430780809892252

[IMAGE: dark canvas, two boxes side by side. A big box labeled "worker (Opus)" doing work, feeding a transcript into a small box labeled "judge (Haiku)". The judge has two arrows out: "met -> return to you" and "not met -> start another turn", with the not-met arrow looping back into the worker carrying a "reason" tag]
![[loopy-goal-worker-judge-loop-1.png]]
![[loopy-goal-worker-judge-loop-2.png]]
![[loopy-goal-worker-judge-loop-3.png]]
![[loopy-goal-worker-judge-loop-4.png]]
![[loopy-goal-worker-judge-loop-5.png]]

---

## Why this is infrastructure, not discipline

Recall how Ralph held state. Three files on disk: the spec, the progress log, the gates. The discipline was yours. You wrote the bash loop, you enforced the restart, you decided the exit. Ralph is a pattern you perform.

Goal mode takes the parts you were performing by hand and bakes them into the runtime as a state machine.

If you read the open-source implementation, the goal is a row in a table. An objective. A status that's one of active, paused, budget-limited, or complete. An optional token budget. Usage accounting. And tools the agent can call to read the goal and to mark it done.

Source: https://x.com/jarrodwatts/status/2052372045829382430

The auto-continuation is the load-bearing part. When a goal is active and the agent tries to stop, the runtime injects a hidden continuation message that says, in effect, keep going, here's the objective, here's what's still missing. The agent never gets to quietly end the turn. The state machine won't let it.

One detail in that continuation prompt is worth pausing on. The objective gets wrapped in an `<untrusted_objective>` tag. The runtime treats your own goal text as untrusted input, the same way it would treat content scraped off a web page. That's deliberate. Your objective rides along in every single continuation message, turn after turn, so if it carried an injected instruction it would get re-fired hundreds of times. Tagging it untrusted tells the worker to act on the objective without obeying any commands hidden inside it.

Source: https://x.com/jarrodwatts/status/2052372045829382430

That's the shift. In Ralph, the outer loop is your script and the model can technically wander off because nothing structurally stops it between restarts. In goal mode, the outer loop is the harness. The model cannot cheat the loop because the loop isn't in the prompt anymore. It's in the runtime.

This is why the segment exists as its own thing. Goal mode is not "Ralph but easier." It's the moment the L3 outer loop stops being something you hand-build and becomes something the platform guarantees.

[IMAGE: dark canvas, a small state machine diagram. Four nodes: active, paused, budget-limited, complete. Arrows between them. The "active" node has a self-loop labeled "auto-continue (hidden message)". Only the transition into "complete" is gated by a box labeled "completion audit"]
![[loopy-goal-state-machine-1.png]]
![[loopy-goal-state-machine-2.png]]
![[loopy-goal-state-machine-3.png]]
![[loopy-goal-state-machine-4.png]]
![[loopy-goal-state-machine-5.png]]

---

## Budget exhaustion is not completion

This is the line to tattoo on the inside of your skull.

A goal can carry a token budget. When the worker burns through it, the runtime marks the goal budget-limited and steers the worker to wrap up. Stop starting new work. Summarize what's done. Leave a clear next step.

Source: https://github.com/grp06/goalcraft

Budget-limited is not complete. They are different states for a reason. A loop that treats "I ran out of budget" as "I finished" is the exact runaway failure from the loop stack segment, the one that burns a thousand dollars overnight and then declares victory because it stopped.

The runtime is careful about this. Completion has to be audited against actual evidence. Not effort. Not elapsed time. Not a green test suite by itself. Not the fact that the budget ran dry. The continuation prompt explicitly tells the worker: restate the objective as concrete success criteria, map every requirement to evidence, reject proxy signals, and treat uncertainty as not-done.

So you have three distinct end states, and you have to design for all three. Complete means the audit found evidence. Budget-limited means you spent what you allotted and there's a clear handoff. Unmet means the agent is blocked or the objective was weakly verified. Only the first one is success. The other two are decision points, where you read the wrap-up, decide whether to raise the budget, narrow the objective, or unblock the agent, and re-run.

A Ralph loop with no exit condition cannot stop. Goal mode gives budget exhaustion its own behavior precisely so the dangerous version of the loop can't happen by accident.

---

## The completion audit, and why it can lie to you

Here's where it gets subtle, and where most people get burned.

The judge defaults to evaluating your condition against what the worker surfaced in the conversation. By default it does not run commands or read files on its own. It reads the transcript.

Source: https://code.claude.com/docs/en/goal

Sit with that. The judge grades the worker's own account of the work. If your condition is "complete the migration," the worker writes "migration complete" in the transcript, the judge reads "migration complete," and the goal clears. Nothing got verified. You just paid a fast model to rubber-stamp the slow model's homework.

This should sound familiar. It's the self-grading failure from the borrowed-verifiers segment, wearing a new costume. The judge sharing the transcript with the worker is the same trap as the model grading its own output. Fresh model, sure. But fresh eyes buy honesty, not rigour, and a judge with nothing new to look at drifts to "looks done" for the same reason the worker did.

There are two real fixes, and you want both.

First, write conditions the worker's own output can prove. "All tests in `test/auth` pass" works, because the worker runs the tests and the actual result lands in the transcript for the judge to read. That's a borrowed verifier whose output you've forced into the conversation. "Make the app production-ready" never works, because nothing in the transcript can ever prove it, so the loop runs until the budget dies.

Second, and stronger: move verification out of the prompt and into the infrastructure. Pair the goal with a Stop hook that runs your tests, hits CI, or fires a real grader after every turn. Now the loop doesn't close on the worker's say-so. It closes on a machine check the worker can't phrase its way past. The most serious implementations go further, spawning an adversarial audit in a separate process with a hostile prompt, write tools disabled, no access to the worker's reasoning, that can only see the objective and the repo on disk, and whose job is to prove the worker wrong.

Source: https://github.com/balakumardev/claude-code-goal

That adversarial auditor is the pair-every-creator-with-an-attacker pattern, dropped into the exit gate of the loop. The worker builds. A fresh, asymmetric, refute-by-default agent decides whether it's actually done. If the auditor finds a gap, its list of what's missing gets injected straight into the next continuation prompt, and the worker has to clear every item before it's allowed to claim completion again.

---

## When to reach for goal mode versus Ralph

They're not competitors. They're the same L3 loop with the outer ring owned by different things, and the work tells you which to grab.

Reach for Ralph when the work is pre-decomposable. You can write the whole PRD up front. You know the milestones. The task tree is knowable before you start. Bootoshi ran an eleven-hour-twenty-six-minute overnight build off a fifteen-hundred-line PRD this way, with goal mode re-pinging the agent back to the PRD every time it compacted. The PRD specified goals and non-goals, the guardrails were enforced in code, and "done means proper because of the guardrails." His other rule: have a feature, have a goal, and above all have a solution, an end to the goal, because without a defined end the agent runs forever.

Source: https://x.com/kingbootoshi/status/2052510026535936157

Reach for the lighter hand-rolled loop when the work unfolds. When you can't pre-sequence it, when each step reveals the next, when over-specifying up front would just plant wrong assumptions you then have to dig back out. We have a whole segment coming on why pre-sequencing the backlog is often a mistake, so I'll leave that hook there.

And here's the honest part. Goal mode is new, and the people running it hardest are split on it. Jarrod Watts read the internals and concluded the bare command underwhelms, that his own setup, a sharp interview phase up front plus an orchestrator with separate implementer and reviewer agents, beats it. He's not wrong. Goal mode is the runtime giving you a guaranteed outer loop. It is not the runtime giving you a good objective or a real verifier. Those are still on you. Goal mode just makes sure that whatever loop you do design actually runs to a real exit instead of dying when your bash script hiccups.

The vague objective and the missing audit are the failure modes. The runtime can't fix either. Writing the objective so it can't loop forever is its own skill, and it's the next segment.

---

## What "done means proper" actually requires

Go back to that line: "done means proper because of the guardrails." It's easy to nod at and miss. The point is that completion was enforced programmatically, by the project's tooling, not by the model deciding it was finished. An eleven-hour unattended run only stays honest if the agent physically cannot mark sloppy work done.

Source: https://x.com/kingbootoshi/status/2052510026535936157

Here's the stack Bootoshi ran, and it's worth seeing in full because every layer closes a different escape hatch:

- **Strict TypeScript.** The build refuses to compile on bad types, so the agent can't paper over a type error and move on.
- **Biome formatting and linting**, plus **custom ESLint plugins** that encode the architecture itself, so structural drift gets caught, not just style.
- **Files capped under 500 lines** and a **Biome no-excessive-cognitive-complexity rule**, so the agent can't grow god functions or dump everything into one file.
- **A centralized logger** the agent has to route through instead of scattering its own.
- **knip** to delete dead code, so abandoned half-implementations don't accumulate.
- **A custom test harness that programmatically forbids skipping tests**, and a **written testing philosophy** so the agent can't satisfy a quota with useless `1+1==2` mock tests.
- **Three layers of tests**: unit with mocks, integration against a real SQLite database, and real end-to-end in Docker.
- **A lefthook pre-commit gate** that blocks any commit unless types, lint, and format all pass, and that denies `--no-verify` so the agent can't bypass the gate.

Look at the shape of that. It's the borrowed-verifiers segment taken to its conclusion. Every one of these is a machine check the worker runs into, not a judgment the worker makes. The goal's auto-continuation keeps the loop open; this stack is what the loop has to close against. That's also why his build-test-fix cycle worked unattended: the real end-to-end tests in Docker surfaced problems he never anticipated, the agent read the failure and fixed it, and the gates made sure the fix was real before the commit landed.

Strip the guardrails out and "done means proper" collapses back into "done means the model said so." The guardrails are not polish. They are the verifier the runtime doesn't give you.

---

## Demo

Open Claude Code on a small repo with a known failing test suite. Say the auth tests are red.

One. Type the naive version first to show the trap. `/goal complete the auth refactor`. Let it run two or three turns. Watch the worker write "refactor complete" and watch the goal clear with the auth tests still red. Pull up `/goal` after, point at the turns and tokens spent. On screen: "the judge read the transcript, not the repo."

Two. Clear it. Now the verifiable version. `/goal all tests in test/auth pass, or stop after 15 turns`. Run it. After each turn, show the status line: the judge's one-sentence reason for why the condition isn't met yet, feeding the next turn. Watch the worker actually run the suite each turn because that's the only way the result lands in the transcript.

Three. Show the budget edge. Set a tight turn cap so it hits the wall before the suite goes green. Watch the goal flip to budget-limited, not complete. Read the wrap-up the worker leaves: what's done, what's left, the next concrete step. Say it out loud: "this is the runaway loop being caught by design."

Four. The infrastructure fix. Add a Stop hook that runs `pytest test/auth` after every turn. Re-run the same goal. Now completion isn't the worker's word, it's an exit code. Push a commit that intentionally breaks a test, watch the hook block the stop, watch the worker get the failure and fix it before the goal will clear.

Total demo: six minutes. The arc is the point. Naive goal lies to you, verifiable goal is honest but soft, infrastructure-backed goal can't be cheated.

---

## Key Insight

> Ralph put the loop in your bash script. Goal mode puts it in the runtime, so the model can't quietly stop. But the runtime only guarantees the loop runs, never that it ran on a real objective with a real check. Budget exhaustion is not completion.

---

## Where we go next

You now have a runtime that will hold a loop open against an objective until a judge says stop.

Which means the objective is suddenly the most important sentence you'll write. A vague one loops until the budget dies. A subjective one lets the worker grade its own homework through the transcript.

Next segment is exactly that: how to write a goal that has a measurable end state, a stated check, and constraints, so the loop you just learned to run actually converges.

See you in the next one.
