---
duration: "12-16 min"
batch: 3
order: 5
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "Closing The Loop"
aliases: [closing-the-loop]
---

L1 is the model deciding "I think I'm done." L2 is something other than the model checking "are you actually done." Until that other thing passes, the loop keeps going.

That other thing is the verifier. This whole segment is about it, because the verifier is the single piece that turns a one-shot generation into a loop that converges. Get it right and everything above this in the stack works. Get it wrong and the rest of the class is built on sand.

This is the first loop most of you should actually build. So let's build it properly.

---

## The thing everyone half-builds

Almost everyone watching this has already written something close to an L2 loop. You told the agent to do the work, then told it to check the work, then told it to fix what it found.

And it kind of worked. The agent wrote some code, looked it over, said "looks good," and stopped.

That is the half-built version. The work happened. The loop did not.

Because the check was the same model call that produced the artifact. The agent graded its own homework, found it excellent, and exited. You didn't close the loop. You drew a loop on a whiteboard and let the model trace over it.

In [[strip-the-model-out]] we built loops with no model in them at all, and we named the failure mode for a check that doesn't actually check: it's the difference between a loop that converges and a loop that just stops. L2 is where that failure mode shows up the most, because the model is so fluent at telling you it's done.

[IMAGE: dark canvas, a single agent head drawing a loop arrow that points right back into its own mouth, labeled "self-grade", with a small caption "the work happened, the loop didn't"]
![[loopy-closing-the-loop-half-built-loop-1.png]]
![[loopy-closing-the-loop-half-built-loop-2.png]]
![[loopy-closing-the-loop-half-built-loop-3.png]]
![[loopy-closing-the-loop-half-built-loop-4.png]]
![[loopy-closing-the-loop-half-built-loop-5.png]]

So before we build anything, we need a hard definition of the one part people keep getting wrong.

---

## What a verifier actually is

> A verifier is a non-builder process that takes the work artifact as input and returns a structured pass or fail, or a score against a threshold, that the builder cannot rephrase its way past.

Read that again, because three properties are doing all the work, and all three have to hold at once.

Non-builder. It cannot be the same model call that produced the artifact. If the thing that wrote the code is the thing that grades the code, you have one process wearing two hats, not two processes.

Structured output. A number, a boolean, a typed report. Not prose the builder gets to interpret. The moment your "check" returns a paragraph that the builder then reads and decides how to feel about, the builder is back in control of the verdict.

Rephrase-immune. The verifier judges the artifact, not the builder's description of the artifact. If the agent can change the grade by changing how it talks about its own work, it isn't being verified. It's being believed.

If any one of those three fails, you have a self-graded loop wearing L2 clothes. It will look like a loop. It will run iterations. It will exit. And it will exit at "fine" every single time, because fine is what the model finds most fluent to say about itself.

This is the load-bearing definition for the rest of the class. Every later segment points back at this one. Borrowed verifiers are about where the structured output comes from. The paired attacker is about making the non-builder actually want to fail you. The three-role split is this definition scaled to a fleet. All of it is this.

---

## The four-part anatomy

Strip away the names and an L2 loop is four parts.

The builder. The thing that produces the artifact. A model call, now.

The work artifact. What the builder produced. A file, a diff, a draft, an image.

The verifier. The non-builder process that grades the artifact, per the definition above.

The exit condition. The single rule that ends the loop, expressed as "verifier returns pass."

Builder produces artifact. Verifier grades artifact. On fail, the artifact and the verifier's complaints go back to the builder, and it produces again. On pass, the loop exits. That's the entire shape.

[IMAGE: dark canvas, four labeled boxes, builder to work-artifact to verifier, a "fail" arrow looping back from verifier to builder, a "pass" arrow exiting the loop to the right]
![[loopy-closing-the-loop-four-part-anatomy-1.png]]
![[loopy-closing-the-loop-four-part-anatomy-2.png]]
![[loopy-closing-the-loop-four-part-anatomy-3.png]]
![[loopy-closing-the-loop-four-part-anatomy-4.png]]
![[loopy-closing-the-loop-four-part-anatomy-5.png]]

Now notice something. We already built this shape, twice, in [[strip-the-model-out]], with no model anywhere in it.

---

## It's the five primitives, specialised

In [[strip-the-model-out]] every loop was five primitives: trigger, work, check, terminate, state. L2 does not throw that away. It specialises it.

The builder is the work primitive, now with a model dropped into it. The work artifact is the output of that work primitive. The verifier is the check primitive, made non-trivial. The exit condition is the terminate primitive, expressed as "verifier returns pass." Trigger and state are inherited straight from L1 and don't change shape at all.

Two consequences fall out of that, and they matter for the whole rest of the climb.

First. The four-part anatomy is not a new thing to memorise. It is the five-primitive loop with a model dropped into the work slot and a real check in the check slot. If you understood the deterministic markdown gate, you already understand L2. You just swapped one slot.

Second. Nothing at L3 and above adds new primitives. Ralph, goal mode, worker queues, discovery loops. None of them invent a sixth primitive. They just change which slot owns what, and how many of these loops you run at once. The whole stack is these five primitives, rearranged. That's the payoff for learning them deterministically first.

So the diagnostic from the setup segment still works here. If you're not sure whether your L2 loop is real, ask: would the deterministic version of this loop work? If the check primitive only passes because a model is being nice, you have a broken check, not a hard task.

---

## One agent or two

The most common question at this point is whether the builder and the verifier have to be two separate agents.

The L2 shape does not care. The same model can play both roles, switching prompts between them. Or you run two agents in series, one builds and hands off, one grades. Both are valid L2.

What the shape does care about is the failure mode, and it's always the same one. Do not let the checker be a restatement of the builder. The instant "verify this" becomes "describe what you just did and confirm you're happy with it," the loop collapses back into self-grading no matter how many agents you spun up.

Here's the subtle part, and it's why a separate subagent helps at all. In the builder's own context, the model has already said "done." It now reads its own work as something to defend, not something to inspect. A fresh window hasn't committed to anything yet, so it can actually look at the artifact instead of looking for reasons it was right.

That makes "non-builder" partly a context property, not just a prompt property. The seed of this was in [[l1-essentials]], the uncommitted grading subagent. Fresh eyes are worth a lot.

But fresh eyes only buy you honesty. They do not buy you rigour. A clean context that has nothing concrete to push back with will still drift to "looks fine," for the same reason the original context did. It needs a reason to disagree. Either it observed something the builder didn't get to author, which is the [[borrowed-verifiers]] move, or it was told to refute rather than confirm, which is the paired-attacker move in [[adversarial-reviewer-skill]]. Clean context plus no reason to push back still rubber-stamps. Hold onto that. It's the whole bridge into the next two segments.

[IMAGE: dark canvas, two side-by-side panels. Left: one head labeled "builder context", a thought bubble "I already said done", arrow to a rubber stamp reading FINE. Right: a separate fresh head labeled "non-builder", with two inputs feeding it, "observed signal" and "told to refute", arrow to a real PASS/FAIL gate]
![[loopy-closing-the-loop-fresh-eyes-not-enough-1.png]]
![[loopy-closing-the-loop-fresh-eyes-not-enough-2.png]]
![[loopy-closing-the-loop-fresh-eyes-not-enough-3.png]]
![[loopy-closing-the-loop-fresh-eyes-not-enough-4.png]]
![[loopy-closing-the-loop-fresh-eyes-not-enough-5.png]]

---

## This pattern in the wild

You don't have to invent these. People are shipping them right now, and they all have the four-part anatomy.

Peter Steinberger wrote a skill that runs Codex's `/review` in a loop until, in his words, "there's no booboos anymore." Write code, run `/review`, fix the findings it surfaces, run `/review` again. The loop exits when `/review` finds nothing material. His caveat is the lesson of this whole class in one line: "it won't fix system architecture for ya, so you still need BRAIN as master model." The loop closes the local quality gap. It does not replace the human deciding what to build. That's L7, and it's the last segment for a reason.
Source: https://x.com/steipete/status/2054850632067019173

Eric Zakariasson showed Cursor's internal quality-review skill, which he called the most-used skill inside Cursor at the time. It blocks files over a thousand lines, flags thin wrappers and leaked logic, deletes complexity instead of moving it, and rejects PRs that work but make the codebase messier. Same shape, different artifact. The verifier here grades structure, not correctness.
Source: https://x.com/ericzakariasson/status/2057521364622553442

The cleanest one to picture is Playwright write-test-fix. Generate a test, run it, watch it fail, fix the implementation, re-run. The loop exits when the test goes green. Notice why this one is airtight: the verifier observed something. The test actually executed the code. Red is red and green is green, and no amount of the builder rephrasing its work turns red into green. That's a verifier the builder cannot talk its way past, which is exactly the property we'll chase hard in [[borrowed-verifiers]].

---

## What this is not

Quick boundary lines, because L2 gets confused with things above it constantly.

This is not Ralph. Ralph runs the whole outer task in a fresh window over and over. That's L3, a full task lifecycle. L2 is one artifact.

This is not goal mode. In goal mode the runtime owns the loop and keeps it alive against an objective. That's L3 too. L2 is a loop you hold.

L2 is one artifact, one verifier, one exit condition. The moment you're running a stream of tasks or owning a whole deliverable end to end, you've left L2. We'll get there. Don't skip ahead.

---

## Demo

Let's build the smallest real one on screen. A build-test-fix loop, three iterations, no more.

1. Point an agent at a tiny function with a known bug. Give it the spec in one sentence: "this function should return the nth Fibonacci number, the tests are in test_fib.py, do not edit the tests."

2. Iteration one. The agent reads the failing test, edits the implementation, says it's done. We do not believe it. The script runs pytest. Two of three cases still fail. The raw pytest output, the actual failure lines, goes straight back into the agent's context. That's the verifier returning structured output the agent can't rephrase.

3. Iteration two. The agent now has real failure lines, not its own opinion. It fixes the off-by-one. The script runs pytest again. One case left, an edge case at n equals zero.

4. Iteration three. The agent patches the base case. The script runs pytest. Exit code zero. The loop sees pass and breaks. On screen, the terminal prints "verifier passed, exiting" and stops.

Now the one-line change that makes the point. Comment out the line that feeds pytest output back into the agent, and replace the check with "ask the agent if it thinks it's done." Re-run. It exits on iteration one. Green checkmark, broken code. Same loop, self-graded check, and it lied to us immediately.

That diff, two lines, is the entire difference between a loop that converges and a loop that just stops.

---

## Key Insight

> An L2 loop is just the deterministic five-primitive loop with a model in the work slot and a real check in the check slot. The model decides "I think I'm done." The verifier decides "you're actually done." If those are the same call, you don't have a loop, you have a confident guess.

---

## Where we go next

You now have the canonical L2 loop. Builder, artifact, verifier, exit condition, and a hard rule that the verifier can't be the builder in a costume.

We left one thing hanging on purpose. Fresh eyes buy honesty, not rigour. The checker still needs a reason to disagree.

The next segment, [[borrowed-verifiers]], gives it the first reason: a grader from outside the model that observed something the builder didn't get to author. After that, [[adversarial-reviewer-skill]] gives it the second reason: a checker told to refute instead of confirm.

Same four-part anatomy the whole way. We're just making the verifier harder and harder to fool.

See you in the next one.
