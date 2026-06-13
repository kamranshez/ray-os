---
duration: "14-18 min"
batch: 5
order: 17
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "Autoresearch"
aliases: [autoresearch]
---

Every loop so far has optimised the work. This one optimises the prompt.

That is the whole jump. Up to now, the model produces an artifact, a borrowed verifier grades the artifact, and the loop iterates on the artifact until it passes. The prompt was a fixed thing you wrote once and trusted. Autoresearch turns the prompt itself into the thing under test. The artifact becomes evidence, the prompt becomes the variable, and the loop keeps whatever version of the prompt scores higher.

This is the Karpathy-style eval-driven loop, ported out of machine learning and onto your skills. In ML you change a training script, run a benchmark, keep the change if the number went up. Here you change a SKILL.md, run an eval suite, keep the change if the score went up. Same loop. Different artifact.

---

## What everyone gets wrong about improving a skill

Your skill works seventy percent of the time. The other thirty percent you get garbage. So you open the SKILL.md and start rewriting.

That is the mistake. You are mutating the prompt by hand, judging the result by vibe, and you have no idea whether your change helped, hurt, or did nothing. You rewrite three paragraphs, the next output looks fine, you ship it. Two days later it is back to seventy percent and you cannot tell which of your edits caused the regression because you changed five things at once and measured none of them.

That is self-grading wearing a new costume. You met it back in the closing-the-loop segment as the model saying "looks good" about its own work. Here it is the *author* saying "looks better" about their own edit. Same well, sampled twice.

The fix is the same fix it has always been in this class. Put a verifier outside yourself, and let the loop decide what survives.

[IMAGE: dark canvas, left side a person hand-editing a SKILL.md with a thought bubble "looks better?", right side a closed loop where a prompt feeds runs feed an eval suite feeds a keep/discard gate that feeds back to the prompt]
![[loopy-autoresearch-hand-edit-vs-loop-1.png]]
![[loopy-autoresearch-hand-edit-vs-loop-2.png]]
![[loopy-autoresearch-hand-edit-vs-loop-3.png]]
![[loopy-autoresearch-hand-edit-vs-loop-4.png]]
![[loopy-autoresearch-hand-edit-vs-loop-5.png]]

---

## What an eval suite actually is

Before we mutate anything, define the artifact this whole segment leans on.

> An eval suite is a fixed set of inputs plus a borrowed verifier per input, run end to end against any candidate prompt, returning one structured score per case and an aggregate pass or fail for the run.

Three properties matter.

Fixed inputs, so you compare runs apples to apples. The same three to five test scenarios every time, chosen to cover different use cases so you do not overfit to one.

A borrowed verifier per case, straight out of the borrowed-verifiers segment. No self-grading. Each output is checked against an external, structured question, not against the model's own opinion of itself.

And an aggregate gate. Binary. Did this candidate beat the incumbent, yes or no. Not "by how much."

Here is the part people skip. You write the eval suite *before* you touch the prompt. The autoresearch loop mutates the prompt. The eval suite never moves. If the eval suite moves mid-run, you are not running an experiment, you are drifting, and you will fool yourself exactly the way hand-editing fools you. The suite is the one fixed point the whole loop pivots on.

---

## Why the evals have to be binary

This is the load-bearing design choice, and it is the one most people get wrong.

The instinct is to score each output one to seven. "Rate the readability." "Rate the structure." It feels more informative. It is worse.

Scales compound variability. A model asked to rate one to seven will give you a five this run and a six next run on identical output, because the difference between five and six is a coin flip the model is making on your behalf. Now multiply that wobble across four evals and five runs and your aggregate score is mostly noise. You will keep mutations that did nothing and discard mutations that helped, because the signal is drowned.

Binary collapses the wobble. "Are all words spelled correctly with no truncated sentences?" Yes or no. "Does the output use only pastel colors?" Yes or no. There is no five-versus-six judgment call to be unstable about. The eval either fires or it does not, and across runs it fires consistently.

So every eval is a yes-or-no question with a specific pass condition and a specific fail condition. Three to six of them. Fewer than three and you are barely measuring. More than six and the skill starts parroting your eval criteria back at you instead of actually getting better, which is its own kind of overfitting.

Your max score is simply the number of evals times the number of runs. Four evals, five runs, max score of twenty. That number never changes for the life of the experiment, which is exactly why a fixed binary suite lets you compare run three against run thirty honestly.

[IMAGE: dark canvas, top row a wobbly 1-to-7 scale with the same output scoring 5 then 6 then 4 across three runs labeled "noise", bottom row a clean PASS/FAIL stamp giving the same answer three times labeled "signal"]
![[loopy-autoresearch-binary-vs-scored-evals-1.png]]
![[loopy-autoresearch-binary-vs-scored-evals-2.png]]
![[loopy-autoresearch-binary-vs-scored-evals-3.png]]
![[loopy-autoresearch-binary-vs-scored-evals-4.png]]
![[loopy-autoresearch-binary-vs-scored-evals-5.png]]

---

## The mutation engine

Now the loop. You have a fixed binary suite and a baseline score. The engine that proposes prompt changes has exactly one rule that keeps it from destroying your skill: change one thing.

Each pass: read the outputs that actually failed. Not the aggregate, the actual failing outputs. Find the pattern. Is it a missing instruction, an ambiguous directive, a buried rule that should sit higher because position is priority? Form one hypothesis. Make one targeted edit. Run the suite again. Score it.

Then the gate, and the gate is brutal on purpose.

Score went up: keep it. That mutation is the new incumbent.

Score stayed flat: discard it. Revert. A change that added words without moving the number added complexity for nothing, and complexity is debt.

Score went down: discard it. Revert.

That flat-equals-discard rule is what stops the policy from drifting. This is the trap the segment exists to warn you about. If you let "no worse" survive, your skill slowly bloats with neutral edits, and somewhere in that accumulated cruft a behavior you cared about quietly breaks, with no single experiment to blame. Only improvements survive. Everything else snaps back to the last known-good prompt.

You log every attempt, kept or discarded, to a changelog: the score, the one change, why you expected it to help, what actually moved. That changelog is the real prize. It is a research log a future, smarter model can pick up and continue, and it is the difference between an experiment and a guess you forgot you made.

And critically, the loop runs unattended. Once it starts, it does not stop to ask whether it should continue, because you are not at the keyboard, the same way the worker loops from the last few segments do not wait for permission on every turn. It stops on three conditions only: you stop it, it hits a budget cap of experiment cycles, or it hits ninety-five percent for three runs straight and admits diminishing returns.

---

## This is ACE wearing a lab coat

If the keep-what-wins, discard-what-doesn't shape feels familiar, it should, and the next chapter on the three-role split will name it formally.

Autoresearch is a special case of that pattern. A Generator produces work under a prompt. A verifier scores it. And a third role mutates the Generator's prompt and curates which version survives. The thing being curated here is not a fact or a memory. It is the policy itself, the SKILL.md.

I am flagging the connection now and leaving it there. We build the formal version, with all three roles named and separated, in the three-role-split segment. For this segment, hold one idea: the loop that improves the work and the loop that improves the prompt are the same machine pointed at a different artifact.

The other warning I will only name. A loop that proposes its own changes and grades them against a suite it could learn to game is one bad eval away from optimising for the test instead of the task. That failure has a name, the echo chamber, and it gets its own segment later. The defense is the one you already have: borrowed verifiers that touch reality, and a suite small enough that the skill cannot just parrot it back.

---

## Demo

Open a skill that misbehaves. I will use a diagram-generator skill that is right about eighty percent of the time and keeps slipping numbered steps and bright red into outputs that are supposed to be clean and pastel.

One. Write the eval suite first. Four binary checks. Is all text legible and correctly spelled? Pastel colors only? Linear left-to-right or top-to-bottom layout? Free of step numbers and ordinals? Pick five test inputs that vary: OAuth flow, CI pipeline, microservices, onboarding funnel, schema relationships. Five runs each. Max score forty.

Two. Establish the baseline. Run the skill as-is, score all ten, sorry, all twenty outputs. Result on screen: thirty-two of forty, eighty percent. Failures clustered: three diagrams with numbered steps, two with red, three with illegible small text.

Three. Stand up the live dashboard. A single self-contained HTML file that reads the results log and auto-refreshes, plotting the score line and coloring each experiment green for keep, red for discard, blue for the baseline. Open it in the browser and walk away.

Four. Let the loop run. On screen, four experiments fly past. Experiment one adds one anti-pattern line, "never include step numbers or ordinals," and the number climbs to thirty-five. Keep, green bar. Experiment two adds a minimum font-size rule, legibility ticks up but color compliance drops, net flat. Discard, red bar, reverted. Experiment three swaps the vague word "pastel" for five literal hex codes and color compliance goes ten of ten. Keep. Experiment four adds a redundant "no neon" rule that the hex codes already solved, no movement. Discard, reverted to stay simple.

Five. Read the result back. Thirty-two to thirty-nine of forty. Eighty to ninety-seven point five percent. Five experiments, three kept, two discarded, and a changelog that names exactly which three edits earned it. The original SKILL.md was never touched; the winning prompt lives in a separate file you diff and apply on purpose.

Total demo: the loop runs on its own while you do something else. You come back to a better skill and a paper trail of why.

---

## Key Insight

> Stop hand-editing your prompts and calling the result better. Freeze a binary eval suite, mutate one line at a time, and keep only what beats the incumbent. The prompt becomes the artifact under test, and the loop, not your taste, decides what survives.

---

## Where we go next

You now have a loop that optimises the policy, not just the work. That is the same machine you have been building all class, pointed one level inward.

The next segment takes this exact pattern off code and skills and onto the work most people actually care about: YouTube titles, cold email, landing pages, the stuff that looks good and still dies in the real world. Same experiment table, same fixed graders, but the verifier is now the world itself, on a delay. That is autoresearch as an operating system, not a one-shot trick.

See you in the next one.
