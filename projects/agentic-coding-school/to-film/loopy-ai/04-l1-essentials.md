---
duration: "10-14 min"
batch: 2
order: 4
batch_name: "L1 On-Ramp"
class: "loopy-ai"
chapter: "L1 Essentials"
aliases: [l1-essentials]
---

L1 is the harness. It's boring, and that's the point. Almost all the "agent tips and tricks" content on the internet is L1 housekeeping wearing a costume that says "advanced agent design."

We're going to cover it once, compactly, and then never talk about it again. Because every minute you spend fighting the harness is a minute you're not spending designing loops, and the rest of this class is about designing loops.

Three things. That's all you actually need to know to stop fighting L1.

---

## What everyone gets wrong about L1

Go look at how agent content gets sold. "Ten prompts that turn Claude into an autonomous engineer." "The context trick the pros don't want you to know." "How I got my agent to run for six hours unattended."

Peel the packaging off and almost all of it is the same three boring skills. Skipping permission prompts. Managing context. Using subagents. That's L1 housekeeping. It's real, it matters, but it is not agent design. It's the equivalent of learning where the gear stick is before you learn to drive.

The problem with dressing housekeeping up as design is that it never ends. There's always one more keyboard shortcut, one more slash command, one more config flag. People spend months collecting L1 tricks and never climb a single level up the stack.

So here's the deal. We learn the three that matter, we learn why they matter, and then we leave L1 behind for good.

[IMAGE: dark canvas, a single box labeled "L1: the harness" with three sub-skills written inside it: skip permissions, context management, subagents. A pile of crossed-out "tips and tricks" labels sitting outside the box]
![[images/l1-essentials/l1-three-skills.png]]

A useful frame for the three: Aakash Gupta's autonomy ladder. Level one is letting the agent act without asking. Level two is keeping the agent's working memory clean. Level three is splitting work across fresh windows. Same three skills, climbing order. We'll take them in that order.

---

## One: skip permissions on the trusted path

Out of the box, Claude Code asks before it does anything consequential. Run a command? Confirm. Edit a file? Confirm. Run the same kind of command again? Confirm again.

For interactive work, that's correct behaviour. You want a human gate on every action when you're pairing with the agent in real time.

But a loop doesn't pair with you. A loop runs. And a loop that stops every five seconds to ask permission isn't a loop, it's a very slow conversation. Every level above L1 in this class assumes the agent can act without a human tapping "yes" on every step.

The unlock is `--dangerously-skip-permissions`. It does exactly what it says. The agent stops asking. It just does the work.

That flag name is doing a job. It's called "dangerously" because it is. You are handing the agent the ability to run any command it decides to run, with no gate. So you don't sprinkle it everywhere. You earn it.

The way you earn it is the diagnostic from the strip-the-model-out segment: would the deterministic version of this loop be safe to run unattended? If the answer is no, if a wrong move could delete the wrong directory or push to the wrong branch, you don't skip permissions yet. You put guardrails around the loop first. A scratch git worktree. A container. A folder the agent can't escape. Then you skip permissions inside the sandbox.

Skip permissions is not "trust the model." It's "build a box the model can't hurt anything inside, then let it move freely in the box." The flag unlocks autonomy. The box is what makes the autonomy safe. We'll get deep into that box, and the dial that controls how big it is, much later in the class. For now: this flag is the on-switch for everything above L1, and it only belongs on a path you've made safe.

---

## Two: context management

The second skill is keeping the agent's working memory clean.

An L1 loop lives inside one context window. Think, tool call, observe, repeat, until the task is done or the window fills up. Everything the agent has read, every command it has run, every file it has touched is sitting in that window taking up space.

Two failure modes come from a dirty window. One, you run out of room and the agent forgets the start of its own task. Two, leftover context from an unrelated task bleeds into the current one and the agent starts confidently solving the wrong problem.

You have three moves against this.

`/clear` between unrelated tasks. You finished debugging the auth flow, now you're writing release notes. Different task, different world. Clear the window. Start fresh. The single most common mistake I see is people running task after task in one ever-growing conversation and then wondering why the agent got dumber over the afternoon. It didn't get dumber. Its window got polluted.

`/compact` when the same task drags on. Sometimes one task genuinely needs more than a window's worth of work. Compact summarises the conversation so far into a tight digest and keeps going with room to breathe. Use clear when the task changed. Use compact when the task is the same but long.

And scratchpadding to survive resets. This is the one that matters most for loops. A context window is temporary. A file on disk is not. So you have the agent write its plan, its progress, and its open questions to a markdown file as it goes. When the window resets, whether you cleared it or it filled up, the agent reads the scratchpad back and picks up where it left off.

That last move is not a trick. It's the thing that lets a loop outlive a single context window, which is the entire premise of everything from L3 up. The state primitive from strip-the-model-out, the thing that survives between runs, in L1 that's a scratchpad file.

[IMAGE: dark canvas, a context window filling up over time, with a small markdown "scratchpad.md" file off to the side catching the important state. An arrow shows the window resetting and re-reading the scratchpad to continue]
![[images/l1-essentials/scratchpad-survives-reset.png]]

---

## Three: subagents as parallel context

The third skill is the one that's actually interesting, so we'll spend a little more on it.

A subagent is a fresh window with its own context budget. Your main thread spawns it, hands it a task, and gets back only the answer. Everything the subagent did to produce that answer, every file it read, every tool it called, stays in the subagent's window and never touches yours.

There's a rule that follows from this, and it's the one to tattoo on your wrist. Your main thread is precious. Anything that produces a lot of tool output should happen in a subagent.

Why? Because tool output is the fastest way to pollute a window. The agent greps the codebase and gets back four hundred lines. It reads six files to find one function. It runs a test suite and gets a wall of output. None of that noise is the answer. The answer is one sentence. So you send the noise to a subagent and let it come back with the sentence.

Two shapes cover almost all of it. "Go and find" and "go and grade."

Go and find. "Search the codebase and tell me where the rate limiting happens." The subagent reads twenty files, you get back one paragraph. The nineteen files you didn't need never enter your context.

Go and grade. "Here's the code I just wrote. Tell me what's wrong with it." And this one is doing something deeper than saving tokens.

Think about what's happening when your main thread grades its own work. It watched itself write that code. It's already committed. It chose every line, defended every decision, and concluded "done." Asking that same window to now find the flaws is asking it to argue against itself. It won't, not honestly. It'll glance at its own work and say "looks good," because that's the most fluent thing for it to say.

A subagent grading the same code starts in a window that never watched the work get made. It has no commitment to defend. It can look at the code as a stranger would.

That clean, uncommitted window is the seed of the verifier you'll meet in closing-the-loop, and the seed of the attacker you'll meet in pair-every-creator-with-an-attacker. Both of those patterns start here, with a fresh window grading work it didn't author.

But here's the honest caveat, and both of those later segments hammer it, so I'll plant it now. A fresh window grades honestly only if it also has a reason to disagree. Clean context stops the grader from defending what it just wrote. It does not, on its own, give the grader anything new to check against. Give a fresh window the same artifact and nothing else to look at, and it drifts to "looks fine" for the same reason the first window did.

Fresh eyes are necessary for an honest grade. They are not sufficient for a real one. Hold that thought. It's the whole hinge that the L2 chapter swings on.

---

## Demo

Three terminal windows, side by side on screen.

Terminal one. The permission gate. I run a small task without the flag, and you watch me tap "yes" eight or nine times as the agent reads, edits, and runs. Then I run the same task with `--dangerously-skip-permissions` inside a scratch worktree, and it runs start to finish with zero clicks. Same work, eighty percent fewer interruptions. The difference between a conversation and a loop.

Terminal two. Context management. I finish one task, a quick debugging job, and the window is now full of stack traces and file dumps. I start a completely unrelated task in the same window, and you watch the agent reference the old debugging context where it doesn't belong. I `/clear`, run the second task fresh, and it's clean. Then I show a scratchpad file: the agent writing its progress to `progress.md`, me clearing the window mid-task, and the agent reading the scratchpad back and continuing without missing a beat.

Terminal three. Subagents. The main thread is working on a task. It needs the codebase searched, so it spawns a "go and find" subagent. You watch the subagent's window fill with grep output and file reads, while the main thread's window stays clean and only receives the one-paragraph answer. Then a "go and grade" subagent: the main thread hands it freshly written code, and the subagent, in a window that never wrote that code, flags two real problems the main thread had already talked itself past.

Total demo: four minutes. The point of all three is the same. These are not clever tricks. They are the minimum housekeeping that lets an L1 loop run long enough to be worth building on.

---

## Key Insight

> Most "advanced agent" content is L1 housekeeping in disguise. Three skills cover it: skip permissions on a safe path, keep the context window clean, and push noisy work into subagents. Learn them once, then go build loops.

---

## Where we go next

That's L1. You can now run the harness for the long haul without fighting it every five seconds.

Notice that the last skill, the subagent grading work it didn't write, pointed straight up the stack. A fresh window that can look at an artifact as a stranger is the raw material for a verifier. And a verifier checking a single artifact is exactly what L2 is.

So that's where we go. Closing the loop. The first time we put a model inside a loop and let an external check, not the model's own opinion, decide when the loop is done.

See you in the next one.
