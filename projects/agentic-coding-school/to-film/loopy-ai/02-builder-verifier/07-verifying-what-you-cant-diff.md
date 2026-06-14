---
duration: 12-16 min
batch: 2
order: 7
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [verifying-what-you-cant-diff, image-gen-verifier]
---

Text comes with a verifier built in. You can grep it, lint it, type-check it, run it through a test and read an exit code. The check is free because someone already manufactured it for you. An image gives you none of that. No diff. No exit code. No assertion that goes red. You stare at a picture and the only verifier in the room is your own eyeballs.

So when the output isn't text, the loop you spent this whole chapter building has a hole in it. The **Check** component, the thing that decides pass or fail, doesn't exist yet. Nobody hands it to you. You have to build it.

This video is that build, start to finish. We're going to take the exact skill I use to make the diagrams in this class, the Excalidraw image generator, and bolt a real verifier onto it. Not the pretty version. The honest version, including the part where the first few attempts just generate and trust the output, and that fails.

---

## The problem: a soft artifact has no native check

Every verifier you've met so far in this chapter rode in on a signal that already existed.

Borrowed verifiers worked because reality already runs your code and tells you whether it crashed. Pytest exists. Lighthouse exists. The type-checker exists. You didn't write the check, you wired it in. Even the attacker pattern leaned on something concrete: you pointed the model at a claim and asked it to find the contradiction, and "is this claim false" is a question with a sharp answer.

An image is different in kind. Ask "is this image right" and there is nothing underneath the question. No process to run. No output to compare against a known value. The picture doesn't crash. It doesn't return 1. It just sits there, plausible and wrong.

This is what I mean by a *soft artifact*. The work product is correct or incorrect against taste, not against a spec the machine can read. Images. Copy. A landing page's vibe. A diagram's clarity. The thing you're judging lives in your head, not in the file, and the file has no opinion about whether it matched.

[IMAGE: dark canvas, hand-drawn. Two panels side by side. LEFT panel labeled "TEXT", a code block with a bold green checkmark and a little terminal line reading "exit 0" beneath it. RIGHT panel labeled "IMAGE", a framed picture with a large hand-drawn question mark over it and a crossed-out terminal reading "exit ???" beneath it. A thin divider down the middle. Caption underneath: "the diff comes free on the left. on the right you build it."]

![[loopy-verifying-what-you-cant-diff-text-has-diff-image-has-none-1.png]]
![[loopy-verifying-what-you-cant-diff-text-has-diff-image-has-none-2.png]]
![[loopy-verifying-what-you-cant-diff-text-has-diff-image-has-none-3.png]]
![[loopy-verifying-what-you-cant-diff-text-has-diff-image-has-none-4.png]]
![[loopy-verifying-what-you-cant-diff-text-has-diff-image-has-none-5.png]]

And without a check, you don't have a loop. You have a generator. You press the button, you get an output, you accept it because you're tired of pressing the button. That's not L2. That's a slot machine.

---

## The core insight: you manufacture the check, and that manufacturing is the skill

Here is the move. If the artifact doesn't come with a verifier, you build one from the only general-purpose judge available: another model.

A vision model can look at an image and answer questions about it. That's the raw capability. On its own it's useless, the same way "a model can find what's wrong" was useless until video four gave it an asymmetric job and a fresh context. You have to shape the capability into a check. You have to tell it exactly what right looks like, in terms specific enough that its answer means something.

That specification is the verifier. Writing it is the work. Once it exists, the loop is ordinary L2: generate, judge, on-fail regenerate with the critique, judge again, stop when it passes.

So the skill you're building isn't "generate an image." Generating is the easy half, the model already does it. The skill is the *verifier you wrap around the generator*. That's the part that doesn't come for free, and that's the part that turns a slot machine into a loop.

Let me show you what that verifier is actually made of, because it's less magical and more boring than people expect.

---

## The rubric is the verifier

When I built the Excalidraw skill the first time, there was no rubric. The skill generated ten images, I looked at them, I picked one. That's not a verifier, that's me being the verifier, by hand, every time. It worked until it didn't.

The day it broke was the dark-mode switch. I moved the whole class aesthetic from white-background diagrams to a near-black charcoal canvas. The image model didn't get the memo. It kept drifting back to white backgrounds, because white is the statistical center of "diagram" across everything it ever saw. Half my generations came back the wrong color. Some had text spilling out past the edges of a box. Some looked like clip art instead of hand-drawn chalk. There was no `assert background == dark`. There was just me, squinting, rejecting eight out of ten and getting annoyed.

So I sat down and wrote the annoyance out as criteria. What was I actually checking when I squinted? Four things, every time:

- Is the background a solid near-black charcoal, not white, not a gradient?
- Do the strokes look hand-drawn and chalky, not crisp vector clip art?
- Is every caption fully inside the frame and legible, no overflow, no clipping?
- Does the image carry exactly one concept, not three crammed together?

That list is the rubric. It is, unromantically, four lines in a file. And those four lines are the verifier. They're the test suite for an artifact that has no test suite, because they take the taste that lived in my head and pin it down as questions a vision model can answer one at a time.

This is the single most important habit for soft artifacts. **Your taste feels holistic and unspeakable. It isn't. It decomposes into criteria.** The work of building the verifier is the work of forcing yourself to say what "looks right" actually means, in checkable pieces. The moment you can write it as a list, a model can score it.

[IMAGE: dark canvas, hand-drawn. On the left, a small file icon titled "rubric.md" with four short checklist lines visible: "dark canvas?", "hand-drawn stroke?", "caption legible?", "one concept?". A bold equals sign in the middle. On the right, the classic test-suite shape: a stack of green and red dots beside lines labeled "test_1 ... test_4". Caption underneath: "four lines of taste = a test suite for a thing with no tests."]

![[loopy-verifying-what-you-cant-diff-rubric-is-the-verifier-1.png]]
![[loopy-verifying-what-you-cant-diff-rubric-is-the-verifier-2.png]]
![[loopy-verifying-what-you-cant-diff-rubric-is-the-verifier-3.png]]
![[loopy-verifying-what-you-cant-diff-rubric-is-the-verifier-4.png]]
![[loopy-verifying-what-you-cant-diff-rubric-is-the-verifier-5.png]]

---

## The vision judge loop

Now you have a rubric. You wire it into the loop exactly where pytest would go.

A second agent, the judge, gets one job: look at this generated image, score it against these four criteria, and write down what fails and why. Not "is this good," which a model will always wave through. Specific questions with a fresh context, the same two levers you learned with the attacker. Each criterion gets a verdict. The image either clears the bar or it doesn't.

If it clears, you stop. If it doesn't, the judge's written critique becomes the input to the next generation. "Background came back white, force the charcoal harder. Caption on the right box is clipped, shorten it or shrink the type." That critique is the **State** that carries forward. The builder reads it, rewrites the prompt, generates again. Judge again. Loop.

That's the whole machine. It is plain L2 with a vision model sitting in the Check slot instead of a test runner. Nothing exotic. The only thing that was hard was admitting the check had to be built and then building it.

And notice what the judge gives you that your own eyeballs didn't: a *written* reason. When you reject an image by hand, the reason dies in your head and the next generation can't use it. When the judge rejects it, the reason is text, and text feeds back. The critique is the bridge that turns a one-shot generator into a loop that actually converges.

[IMAGE: dark canvas, hand-drawn. A ring loop. Top node "GENERATE (prompt → image)". Arrow clockwise to right node "JUDGE vs rubric". From JUDGE, two arrows: a short one going down-and-out to a box "score ≥ bar → SHIP" with an exit door, and a longer one curving back to the top labeled "below bar → critique". The return arrow is annotated with a small sticky note "white bg / caption clipped" being carried back into GENERATE. Caption underneath: "the critique is the state the next generation reads."]

![[loopy-verifying-what-you-cant-diff-vision-judge-loop-1.png]]
![[loopy-verifying-what-you-cant-diff-vision-judge-loop-2.png]]
![[loopy-verifying-what-you-cant-diff-vision-judge-loop-3.png]]
![[loopy-verifying-what-you-cant-diff-vision-judge-loop-4.png]]
![[loopy-verifying-what-you-cant-diff-vision-judge-loop-5.png]]

---

## When you have a target: builder writes the prompt, verifier compares to a reference

The rubric handles "does this match my taste in the abstract." But sometimes you have something stronger than taste. You have a *reference image*, a specific picture you're trying to match.

This is exactly what happened when I migrated the class slides off Gemini's Nano Banana model onto GPT Image 2. I already had a deck I liked. The job wasn't "make a nice diagram," it was "make this new model produce that specific look." Now the verifier has a ground truth to compare against, which is a far sharper check than a rubric alone.

The loop changes shape slightly. The builder writes the image-gen prompt. The new image comes back. The verifier puts it next to the reference and reports the gap: the strokes are too thin, the accent color is too saturated, the layout is centered when the reference is left-weighted. That gap is the critique. It flows back, the prompt changes, you regenerate, and you loop until the new model's output sits close enough to the reference that you can't tell which engine made it.

This is the closest a soft artifact ever gets to a real diff. You're not comparing pixels for exact equality, that would fail instantly and tell you nothing. You're comparing against a target along the same axes the rubric named, and letting the model describe the distance. Reference plus rubric is the strongest verifier you can build for an image, and it's still a built thing. You wrote the rubric. You chose the reference. The model just runs the comparison you designed.

[IMAGE: dark canvas, hand-drawn. Three boxes in a row. LEFT "PROMPT (builder writes)" → arrow → MIDDLE "generated image". Below MIDDLE, a separate framed "REFERENCE" image. A double-headed compare bracket linking generated and reference, labeled "gap: strokes too thin, color too hot". A feedback arrow curving from the gap label all the way back to the PROMPT box. Caption underneath: "compare to a target, feed the gap back, regenerate."]

![[loopy-verifying-what-you-cant-diff-builder-prompt-compare-reference-1.png]]
![[loopy-verifying-what-you-cant-diff-builder-prompt-compare-reference-2.png]]
![[loopy-verifying-what-you-cant-diff-builder-prompt-compare-reference-3.png]]
![[loopy-verifying-what-you-cant-diff-builder-prompt-compare-reference-4.png]]
![[loopy-verifying-what-you-cant-diff-builder-prompt-compare-reference-5.png]]

---

## Where it stays fuzzy, and why a human glance survives

I'm going to be straight with you, because the chapter would be dishonest otherwise.

A vision judge is softer than a unit test. Pytest is deterministic, it returns the same verdict every run. A vision model is generating its judgment, which means it can be inconsistent, it can rubber-stamp an image that's subtly off, and it can flag something that's actually fine. The rubric tightens this a lot. It does not eliminate it.

So I do not run this fully closed for anything that ships in front of people. The loop does the heavy lifting, kills the obvious failures, the white backgrounds and the clipped captions and the clip-art strokes, the eight-out-of-ten rejections I used to do by hand. Then a cheap human glance sits at the very end. Two seconds. Does this actually look right. That last glance catches the soft misses the judge waved through.

That's not a failure of the design. That's the design. You moved the human from grading *every* generation to spot-checking the *winner*. The verifier you built didn't replace your taste, it scaled it, so your taste only has to show up once at the end instead of ten times in the middle.

How much you trust the closed loop versus how often you glance is a dial, not a switch. We turn that dial deliberately later in the class. For now, just know the honest setting for a soft artifact is "mostly closed, briefly human."

---

## Demo

Let me run the real thing.

1. **Stand up the skill.** I invoke the Excalidraw generator on one section of this very script. It writes a prompt, the dark-mode instruction wrapped around the section text, and generates a candidate image.

2. **Watch it fail the rubric.** First candidate comes back with a clean white background. On screen: the image, clearly white, exactly the failure the dark-mode switch introduced.

3. **Read the judge's critique.** The judge scores it against the four criteria and writes its verdict out loud: "Criterion 1, background: FAIL, returned white, rubric requires solid near-black charcoal. Criterion 3, caption: borderline, right-hand label is clipping the frame edge. Criteria 2 and 4: pass." That written verdict is the State. I put the judge's actual text on screen so you can see it's plain language, not a magic number.

4. **Show the regeneration.** The critique feeds back into the prompt. The builder hardens the background instruction and shortens the offending caption. Regenerate. New candidate: charcoal background, caption inside the frame.

5. **Judge passes, loop exits.** Second pass clears all four criteria. Score above bar, loop terminates. We did not hit the round cap, but it's there as the safety net.

6. **Put the rubric file on screen.** Last shot is the least glamorous and the most important: the rubric itself. Four lines. That file is the entire reason any of this converged. Without it, step two never happens, the white image just gets accepted, and you never know.

---

## Key Insight

> When the output isn't text, the verifier doesn't come for free. There's no diff, no exit code, no assertion waiting in the box. So you build one: decompose your taste into a rubric, hand it to a vision judge, feed the critique back, and loop. Building that verifier *is* the loop. The skill was never generating the image. The skill is the check you wrapped around it.

---

## Closing the chapter, and where we go next

Step back and look at what this chapter actually taught, because seven videos point at one idea.

You learned to aim the check *outward*, at constraints and user flows and reality, never at the stale plan the build already outgrew. You learned to *borrow* a verifier when reality hands you a signal, pytest, Lighthouse, the type-checker. You learned to *manufacture* one with an attacker when reality stays silent. You learned to *calibrate* the bar, a severity threshold for quality and a round cap for safety, so the loop actually stops. And you learned to *wire the interface first*, because a loop that can't perceive its own result is a brain in a jar.

This last video is the punchline. For a soft artifact, an image, none of those come for free. Reality won't run it. There's no contradiction to attack. There's no signal to borrow. So you build the verifier by hand, out of a rubric and a vision judge, and that build is the whole loop. Everything in this chapter has been one move in different clothes: the loop is only as good as its external check, so when the check doesn't exist, your job is to bring it into existence.

That's L2. A single build, a single verifier, a single loop that runs until it passes.

Next we climb a layer. A real task isn't one build, it's a lifecycle, many builds and checks and handoffs stitched into something that takes work from "asked" all the way to "done." That's L3, and it's where these loops stop being a trick and start being a system.
