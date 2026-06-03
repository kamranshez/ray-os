---
class: "spec-driven-development"
chapter: "Tests as the Contract"
---

## The Cheating Agent

Hand an agent a vague task and tell it to write the code and the tests. Watch what happens.

It writes broken code. Then it writes tests that pass against the broken code. The test suite goes green. Nothing works. You deploy it. Production breaks.

The agent didn't lie to you. It did exactly what you asked. You said "make this work and write tests." It made the code match tests it wrote, and the tests match code it wrote, and the whole loop is closed to you. There's no external reference point. The agent is grading its own homework with a rubric it also wrote.

**This is the cheating agent.** And the defense against it isn't better code review. It's test-driven development, reframed as prompt engineering.

---

## The Fix Is Older Than You Think

Test-driven development has been around for twenty-five years. Write the test first. Watch it fail. Write the code until it passes. Refactor. Repeat.

Most engineers stopped doing it strictly. It felt slow. It felt academic. In a world where the human wrote both the test and the code, there was an argument that the discipline wasn't earning its keep.

That argument is dead now. Because the executor changed.

When an agent writes the code, the test is no longer a redundant check on your own work. It's **the only thing standing between the agent and production**. If the test exists before the agent sees the task, and you wrote it, the agent can't cheat. It can only produce code that satisfies a contract it didn't author.

Source: Thought Works retreat, multiple practitioners independently reported that TDD gave them the best results they've ever gotten with agent coding, specifically because it prevents the agent from validating its own broken behavior.

One of them put it bluntly:

> "I've gotten better results from TDD and agent coding than I've ever gotten anywhere else, because it stops a particular mental error where the agent writes a test that verifies the broken behavior."

That's not a style preference. That's a structural fix to a specific failure mode.

[IMAGE: dark background, two panels. Left labeled "Cheating Agent" showing a snake eating its own tail, code and tests looped together with green checkmarks. Right labeled "TDD" showing a human-authored test as a wall, with agent-generated code being shaped to fit through it.]

![[images/tdd-stops-the-cheating-agent/the-loop-broken.png]]

---

## TDD Is Prompt Engineering Now

Here's the reframe that changes how you think about tests.

A test is a precise, executable specification. It says "given this input, produce this output." There's no ambiguity, no cultural context to fill in, no room for the agent to interpret.

**That makes a test the tightest prompt you can write.**

When you hand an agent a test and say "make this pass," you have given it a deterministic target. The generation is still non-deterministic. The agent might produce the implementation in ten different ways across ten runs. But the validation is deterministic. Either the test passes or it doesn't. You don't have to read the code to know if it works.

This inverts the discipline. You're not writing tests to document behavior. You're writing tests to **constrain generation**. The test is the prompt. The code is the output. The rest is plumbing.

---

## Review Moves to the Test Suite

Once you accept that the test is the contract, your review changes completely.

You stop reading the generated code line by line. You can't anyway, there's too much of it. Instead, you review the test suite. Did it cover the happy path? Did it cover the rate limiting case? Did it cover what happens when a user clicks twice? Did it cover the state transitions?

If the tests are comprehensive and the code passes them, the code is acceptable. It doesn't matter if it's pretty. It doesn't matter if you'd have written it differently. **The code is expendable.** If you hate it, regenerate it from the same tests and get a different implementation that also passes.

This is the same principle as specs being the product. The test suite is a specification in executable form. The code underneath is a temporary artifact that can be thrown away and regenerated on demand.

[IMAGE: two stacks of paper. Left labeled "Old review" showing a huge stack of code files with a magnifying glass. Right labeled "New review" showing a small stack of test files with the magnifying glass, and the code stack now labeled "expendable, regeneratable."]

![[images/tdd-stops-the-cheating-agent/review-moved.png]]

---

## Where the Tests Have to Come From

There's one rule that makes the whole discipline work. **The tests cannot come from the same prompt as the code.**

If you say "write me a notification system and write tests for it," you've handed the agent both sides of the contract. It will write tests that validate whatever it produces. You're back in the cheating agent loop.

The tests have to be authored independently. That means one of three things:

1. **You write them.** This is the purest form. You write the test suite against the spec before the agent sees the implementation task.
2. **A separate agent writes them from a separate spec.** One agent reads the spec and writes tests. A different agent reads the same spec and writes the implementation. They never see each other's output until the tests run.
3. **You write the high-value tests, the agent fills in the long tail.** You lock down the non-obvious cases, the edge cases, the ones production will blow up on. The agent handles coverage for the boring cases once the architecture is fixed.

What you can never do is let a single conversation produce both the tests and the implementation. That's the loop. That's where the cheating agent lives.

---

## Why This Produces Better Results Than Writing Code Yourself

Here's the part that surprises people.

Multiple practitioners at the retreat said the same thing: they get better results writing tests and letting an agent implement against them than they got writing the code themselves. Not faster. **Better.** Higher quality. Fewer bugs. Cleaner implementations.

The reason is that writing the test forces you to think about behavior precisely, which is the thing most engineers skip when they sit down and start coding. When you write the code first, you encode assumptions you don't even know you're making. When you write the test first, those assumptions become explicit, because a test only passes if you can define what passing means.

The agent, once it has that precise target, generates code that hits it. No assumptions, no shortcuts, no drift. Exactly the thing you specified.

You, writing code directly, were never that disciplined. Almost nobody is. TDD with an agent is the first time the discipline actually pays off proportional to the cost of maintaining it, because you're not the one typing the implementation.

---

## Demo

1. Take a small feature, for example a rate-limited notification sender.
2. First pass: ask Claude Code to build it and write tests. No other constraints. Let it produce code plus tests. Run the tests. Show them passing. Then show that the actual behavior is wrong, for example it happily sends a million notifications because the rate limit got tested with a hardcoded mock that always returned "under limit."
3. Second pass: write the tests yourself. Include the real rate limit case, the burst case, the reset-after-window case, the dedup case. Hand the tests to Claude Code with a single instruction: make these pass, do not modify the tests.
4. Show the implementation it produces. Run the tests. Show them passing for the right reason.
5. Optional third pass: delete the implementation, keep the tests, regenerate. Show a different implementation being produced that still passes. Point out that the tests are the product, the code is expendable.

The demo is the proof. Same agent, same task. The only variable is whether the tests came from the agent or from you. When they come from you, the cheating loop is broken.

---

## Key Insight

> A test is the tightest prompt you can write. When the test comes before the code, and from a different author than the code, the agent cannot cheat. That's the only structural defense against self-validating broken output. TDD stopped being about discipline the day the agent started writing the implementation.

---

## The Closing Beat

Stop letting the same prompt produce the tests and the code. That's where the cheating happens. Write the tests first, write them yourself, treat them as the product. Let the agent regenerate the code every time you don't like it.

The code is expendable now. The tests are not.
