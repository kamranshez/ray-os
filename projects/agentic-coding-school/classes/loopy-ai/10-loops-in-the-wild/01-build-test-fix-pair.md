---
duration: "8-12 min"
batch: 9
order: 33
batch_name: "Loops In The Wild"
class: "loopy-ai"
chapter: "The Build-Test-Fix Pair"
status: "scripted"
aliases: [build-test-fix-pair]
---

This chapter is different from every one before it. Up to now I taught you how to build loops. This chapter is a cookbook of the loops people are actually running right now, every one attributed, every one a command you can paste tonight. And we start with the single most demoed loop on the entire internet.

It is two agents passing work back and forth until the code is clean. A builder that writes, and a checker that breaks. You already know exactly what this is, because it is the builder-verifier loop from chapter three, wearing street clothes.

[IMAGE: dark canvas, an open cookbook labeled "loops people are actually running", its first recipe card pulled out and enlarged, showing two figures passing a code block back and forth, one labeled Builder (a pen), one labeled Checker (a magnifying glass). A small tag clipped to the card reads "builder-verifier from chapter three, in street clothes". Caption: "the most demoed loop on the internet".]
![[loopy-build-test-fix-pair-intro-v1-1.png]]
![[loopy-build-test-fix-pair-intro-v1-2.png]]
![[loopy-build-test-fix-pair-intro-v1-3.png]]
![[loopy-build-test-fix-pair-intro-v1-4.png]]
![[loopy-build-test-fix-pair-intro-v1-5.png]]

---

## The problem it kills

A one-shot agent ships its bugs.

You ask for a feature, it writes the feature, it hands you the feature, and the feature is forty percent wrong in ways neither of you can see yet. The agent has no second pair of eyes, so the only verifier in the room is you, three hours later, when the build is red and you have lost the context to fix it fast.

The whole pitch of this loop is that the second pair of eyes is built in, and it never gets tired.

[IMAGE: dark canvas, a one-shot agent on the left handing a glossy "feature" box to a tired human on the right. Hidden inside the box, drawn faint, several red "bug" marks the human cannot see. A clock above the human reads "3 hours later" with the build turned red and a thought bubble "lost the context". Label under the human: "the only verifier in the room is you". Caption: "a one-shot agent ships its bugs".]
![[loopy-build-test-fix-pair-the-problem-it-kills-v1-1.png]]
![[loopy-build-test-fix-pair-the-problem-it-kills-v1-2.png]]
![[loopy-build-test-fix-pair-the-problem-it-kills-v1-3.png]]
![[loopy-build-test-fix-pair-the-problem-it-kills-v1-4.png]]
![[loopy-build-test-fix-pair-the-problem-it-kills-v1-5.png]]

---

## The loop

This is the version a creator named raycfu walked through, and that walkthrough did 43,587 views and over a thousand comments on Instagram. That engagement is not an accident. It is the loop people most want to see working, because it is the one that most obviously saves them from themselves.

```
/loop build the next item on the plan, then run tests, typecheck, and lint. Feed every failure back as the next instruction and fix it. Stop when the build is green and the checker has nothing left to report.
```

Read the shape of it. There is a builder: "build the next item on the plan." There is a checker: "run tests, typecheck, and lint." And there is the handoff that makes it a loop and not a script: "feed every failure back as the next instruction." The output of the checker becomes the input of the builder, over and over, until there is nothing left to feed back.

[IMAGE: dark canvas, two boxes labeled Builder and Checker facing each other, an arrow from Builder to Checker labeled "code", an arrow back from Checker to Builder labeled "every failure", the pair circled to show it is one loop, a green checkmark exit arrow leaving only when the checker is empty]

![[loopy-litw-build-test-fix-pair.png]]

---

## Why it works: the verifier is real

This is the lesson from chapter three made concrete, so say it again here. The reason this loop is trustworthy is that its checker touches reality. Tests, typecheck, lint. Three graders that do not care how confident the builder feels. They run, they pass or they fail, and the failure is a fact, not an opinion.

That is the difference between this loop and the one that looks like it but is not: an agent grading its own work. If you let the builder decide whether it is done, it will tell you it is done, because that is the cheapest way to end the turn. The separate checker is what keeps it honest. Two roles, held apart, so the thing that writes the code is never the thing that signs off on it.

You are not adding intelligence here. You are adding a wall between the writer and the judge.

[IMAGE: dark canvas, a solid wall down the middle. On the left, a Builder writing code. On the right, a Checker holding three graders labeled "tests", "typecheck", "lint", each touching a small globe labeled "reality". The wall is labeled "the writer is never the judge". A crossed-out ghost on the left shows the bad version: an agent grading its own work with a thought bubble "looks done to me". Caption: "the verifier touches reality".]
![[loopy-build-test-fix-pair-why-it-works-the-verifier-is-real-v1-1.png]]
![[loopy-build-test-fix-pair-why-it-works-the-verifier-is-real-v1-2.png]]
![[loopy-build-test-fix-pair-why-it-works-the-verifier-is-real-v1-3.png]]
![[loopy-build-test-fix-pair-why-it-works-the-verifier-is-real-v1-4.png]]
![[loopy-build-test-fix-pair-why-it-works-the-verifier-is-real-v1-5.png]]

---

## The catch

One green run is not the same as correct.

A test suite that passes once can pass on luck, on a flake, on a case the tests never covered. This loop's stop condition is "the checker has nothing left to report," and that is exactly as strong as your checker. A weak checker stops the loop early and proudly. So the quality of this whole loop lives in the quality of the three graders you handed it, and that is the thing to invest in, not the prompt.

We sharpen that exact idea later in this chapter, with a loop that refuses to stop on a single green run at all.

[IMAGE: dark canvas, a single green checkmark on a pedestal labeled "one green run", with a question mark hanging over it. Three leaks drawn around it: a "flake" die showing different faces, a "luck" clover, and an "uncovered case" gap in the test net letting a bug slip through. A meter labeled "loop quality" wired not to the prompt but to a box labeled "the three graders you wrote". Caption: "one green run is not the same as correct".]
![[loopy-build-test-fix-pair-the-catch-v1-1.png]]
![[loopy-build-test-fix-pair-the-catch-v1-2.png]]
![[loopy-build-test-fix-pair-the-catch-v1-3.png]]
![[loopy-build-test-fix-pair-the-catch-v1-4.png]]
![[loopy-build-test-fix-pair-the-catch-v1-5.png]]

---

## Demo

Put the pair on screen with a small, real task.

1. Show the plan. One file, five checklist items for a feature. Point at the first unchecked one and say: this is what "the next item" means.

2. Run the loop. On screen, the builder writes the first item. The checker immediately runs tests, typecheck, and lint. One test fails. Watch the failure text get handed straight back as the builder's next instruction.

3. Watch the fix land. The builder reads the failure, patches it, the checker runs again. Green. The loop ticks to item two without you touching anything.

4. Force a flake. Re-run a known flaky test so it fails once and passes on retry. Show the loop feed the failure back, the builder shrug, and the suite go green. Name it out loud: this is the catch, the checker is only as good as the tests you wrote.

5. Let it drain the plan. Five items, builder and checker trading turns, and you reading the final diff once at the end instead of babysitting every step.

Total demo: four minutes. The point is that you never graded a single line. The checker did, and you only read the result.

---

## Key Insight

> A one-shot agent ships its bugs because the only verifier in the room is you, later. The build-test-fix pair puts the verifier inside the loop, so the code is checked before you ever see it.

---

## Where we go next

This is the loop most people build first, and it is the right one to build first.

Next in the cookbook is a loop that does not wait for a plan at all. It picks its own work, every five minutes, while you do something else.
