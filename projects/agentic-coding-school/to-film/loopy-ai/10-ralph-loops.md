---
duration: "12-16 min"
batch: 4
order: 10
batch_name: "L3 Task Lifecycle"
class: "loopy-ai"
chapter: "Ralph Loops"
aliases: [ralph-loops]
---

Here is the dumbest loop that works. You run the same prompt. In a fresh context window. Over and over. Until the goal is met.

That's it. No orchestration framework. No clever agent graph. A while loop in bash and one prompt that says "read the PRD, do the next undone thing, update progress." This is the Ralph loop, and it is the first L3 you should ever build.

It feels too stupid to work. It works.

---

## What everyone gets wrong about Ralph

People think Ralph works because the model is smart. It doesn't. Ralph works because of two things that have nothing to do with intelligence.

The first is test-time compute. A long-running agent does better than a one-shot agent for the same reason a person who works on something for eight hours beats a person who works for eight minutes. More attempts. More tokens spent thinking. The loop is just a way to spend more compute on one deliverable without you sitting there babysitting it.
Source: https://x.com/jarrodwatts/status/2052372045829382430

The second is the context window. This is the part people miss. A single context window has a ceiling. When the task needs more context than the window holds, a one-shot session degrades, starts forgetting the early decisions, and goes off the rails near the end. Ralph exists precisely to defeat that ceiling. Each iteration gets a fresh window. The work that survives between windows does not live in the model's head. It lives in files on disk.
Source: https://x.com/jarrodwatts/status/2052372045829382430

So when people say "Ralph is autonomous," remember what we said back in the loop stack segment. It isn't. It's L3. The model is not deciding what to do. You decided what to do when you wrote the PRD. The loop is just executing your decisions in a windowed way.

[IMAGE: dark canvas, on the left one big context window overflowing and degrading near the bottom; on the right a row of small fresh context windows each reading from and writing to a shared "files on disk" box underneath]
![[images/ralph-loops/why-fresh-context.png]]

---

## The core insight: state lives on disk, not in the window

This is the whole trick, so slow down here.

A normal Claude Code session keeps its state in the conversation. The plan, the decisions, what's done, what's left, all of it lives in the context window. When the window resets, that state is gone.

Ralph refuses to keep state in the window. It keeps state in files. The PRD is a file. The progress log is a file. The standards the work has to meet are a file. The window is disposable. The files are the memory.

Concretely, a Ralph loop reads and writes a small set of plain files:

- `prd.json` or `GOAL.md`, the spec. What we are building and what done looks like.
- `progress.txt` or `PROGRESS.md`, the running log. What's shipped, what's next, what got tried and rejected.
- `AGENTS.md` or `STANDARDS.md`, the quality gates. The rules every iteration has to obey.
Source: https://x.com/jarrodwatts/status/2052372045829382430

Every iteration is the same three moves. Read the files. Do one unit of work. Write the files back. Then the window dies and a brand-new one picks up exactly where the last left off, because everything it needs is sitting on disk.

This is the state primitive from the strip-the-model-out segment, made physical. Back there, state was "what survives between runs." In Ralph, what survives between runs is literally a folder. And it connects straight to the previous segment: the HTML artifact with its embedded JSON state block was one shape of this. Ralph is the same idea in plain files instead of one rendered page.

[IMAGE: dark canvas, three labeled files prd.json, progress.txt, agents.md in the center; an arrow loop around them labeled read - work - write, with a small "fresh window" icon being born and dying on each pass]
![[images/ralph-loops/state-on-disk.png]]

---

## Why fresh context beats long context

There's a reflex in the agent world that says: bigger context window, better. Just put everything in and let the model sort it out.

For repetitive deliverables, that reflex is wrong, and Ralph is the proof.

A long context degrades. The further you get, the more the model is distracted by its own earlier output, the more it drifts from the original instructions, the more it forgets a constraint you set ten thousand tokens ago. A fresh context has none of that. It reads a clean PRD, a clean progress log, a clean set of standards, and does one clean thing.

This is the same idea we keep circling back to. Fresh context buys honesty. We said it in closing the loop, we said it again with the attacker. A fresh window isn't carrying the baggage of "I already decided this is fine." Ralph applies that same principle not to grading but to building: every iteration starts clean, judges the current state of the files on its own terms, and does the next right thing without defending the last thing it did.

The caveat from those earlier segments still holds. Fresh context is necessary, not sufficient. A fresh window with a vague PRD will confidently build the wrong thing, fast. Which is exactly why the discipline matters more than the loop.

---

## Ralph is a discipline, not a script

Here is the thing nobody tells you. The bash loop is five lines. Anyone can write it. That is not the work.

The work is everything you write before you start the loop. Ralph is only as good as the PRD and the quality gates you hand it. The loop is dumb on purpose. All the intelligence you get out of it is the intelligence you put into those files up front.
Source: https://x.com/kingbootoshi/status/2052510026535936157

Bootoshi ran an eleven-and-a-half-hour overnight Ralph-style loop that built a working secure micro-VM sandbox system. The loop didn't make that happen. What made it happen was a fifteen-hundred-line PRD with explicit goals and non-goals, plus quality gates enforced in code so the agent physically could not cheat: strict TypeScript that won't build on bad types, a linter, a file-size cap, a pre-commit hook that blocks any commit failing tests, with the bypass flag disabled.
Source: https://x.com/kingbootoshi/status/2052510026535936157

Read that list again. Every one of those is a borrowed verifier from the segment two videos back, wired so the loop closes against something real instead of against the model's own opinion. That is why his punchline is "done means proper, because of our guardrails." The guardrails are the check primitive. Ralph without guardrails is just a fast way to generate plausible garbage all night.

So the mental model is: you are not writing a loop. You are writing a contract. The PRD says what to build. The standards say what good looks like. The progress log says where we are. The loop just turns the crank.

---

## In-window versus out-of-window

There are two ways to run Ralph, and knowing which one you are using saves you from a whole class of confusion.

**In-window Ralph** lives inside one long session. The agent works, the context fills up, it compacts, and it keeps going against the same goal. State partly survives through compaction. This is what goal mode does under the hood, and we'll get to that next segment. The risk here is compaction quality. If the compaction drops a key decision, the loop drifts and you don't see it happen.

**Out-of-window Ralph** kills the window completely between iterations. Each pass is a brand-new process with empty context that rebuilds its entire understanding from the files on disk. Nothing survives except what you wrote down. This is slower per iteration and it is more robust, because there is no hidden state to silently corrupt. If it isn't in the files, it doesn't exist.

The rule of thumb. Compact when one coherent task is just running long and you trust the summary. Restart when the deliverable is big, repetitive, and you want a hard guarantee that every iteration is grounded only in the files. For an overnight build you can't watch, prefer the restart. The discipline of "if it isn't on disk it's gone" is what keeps an unattended loop honest.

---

## Demo

Let's build the dumbest possible Ralph and watch it ship a small feature.

1. Make a folder with three files. `PRD.md` says: "Build a CLI todo app. Commands: add, list, done. Store in todos.json. Done when all three commands work and tests pass." `PROGRESS.md` is empty. `STANDARDS.md` says: "TypeScript strict. Every command has a test. No file over 200 lines."

2. Write the outer loop. Five lines of bash.
```
while true; do
  claude -p "Read PRD.md, PROGRESS.md, STANDARDS.md. Do the next undone item. \
    Run the tests. Update PROGRESS.md. If PRD is fully met and tests pass, write DONE to PROGRESS.md." \
    --dangerously-skip-permissions
  grep -q "DONE" PROGRESS.md && break
done
```
This reuses the skip-permissions on-switch from the L1 essentials segment, in a scratch folder that is safe to let it run wild in.

3. Run it. Watch the first iteration scaffold the project and implement `add`, then write to `PROGRESS.md`. The window closes.

4. Watch the second iteration start cold. It has no memory of iteration one. It reads `PROGRESS.md`, sees `add` is done, and builds `list`. Tests run. Progress updates. Window closes.

5. Third iteration builds `done`, runs the full test suite, sees all three commands pass against the PRD, and writes `DONE`. The `grep` catches it and the loop exits.

6. Now break it on purpose. Open `PRD.md` mid-run and add a vague line: "make it production ready." Watch the loop never exit, because nothing in the files can ever prove "production ready" is true. That is the exit-condition failure mode, live. Replace it with "done when `npm test` exits zero" and watch it terminate cleanly.

Total demo: six minutes. The point is that no iteration remembers any other iteration. The folder remembers. The loop is trivial. The files are everything.

---

## The four ways Ralph fails

Every one of these traces back to the files, not the model.

**PRD drift.** The spec is vague or contradicts itself, so each iteration interprets it slightly differently and the work fans out instead of converging. Ambiguity compounds, because every iteration's output is the next iteration's input. One off-taste decision early poisons everything after it. The fix is upstream: spend real effort turning a vague goal into a specific, unambiguous spec before the loop starts. That setup phase is its own segment coming up.
Source: https://x.com/jarrodwatts/status/2052372045829382430

**A brittle outer loop.** The bash that drives Ralph crashes, hangs, or can't tell success from failure, and your overnight run silently stalls at 2am. The outer loop is plumbing and it needs the same care as any of the five primitives from strip-the-model-out: a real trigger, a real terminate condition, real state.

**Unclear exit condition.** This is the one that burns money. If "done" isn't something the files can prove, the loop runs forever, or worse, the agent self-reports "done" and you trust it. Your terminate condition must be machine-checkable. `pytest exits 0`. The file exists. The count is zero. Never "it looks complete."

**No guardrails.** The loop runs to completion and produces something that compiles and is wrong, because nothing external ever told it what good means. This is just self-grading wearing a Ralph costume. Borrow a verifier. Put it in the standards. Make the loop close against the world.

[IMAGE: dark canvas, four failure cards in a row labeled PRD drift, brittle outer loop, unclear exit, no guardrails, each with a small icon, and a caption underneath reading "all four are file problems, not model problems"]
![[images/ralph-loops/four-failures.png]]

---

## Key Insight

> Ralph is a dumb loop made smart by what you write before you run it. The window is disposable. The files are the brain. If a decision isn't on disk, it doesn't survive the night.

---

## Where we go next

Ralph is the manual version. You wrote the outer loop, you wrote the exit grep, you babysat the files.

Next segment, goal mode. Same idea, but the runtime owns the loop instead of your bash script, and the model can't cheat the exit condition because a separate judge holds it. Then the segment after that is the part that actually decides whether any of this works: writing the spec the loop runs against.

The loop was never the hard part. Turn the page.

See you in the next one.
