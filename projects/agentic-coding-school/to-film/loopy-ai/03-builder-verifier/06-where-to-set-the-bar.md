---
duration: 8-12 min
batch: 2
order: 6
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [where-to-set-the-bar, stopping-the-verifier]
---

You've spent this whole chapter building verifiers. A borrowed one when reality hands you a number. An attacker when it doesn't. Now there's one question left, and it's the one nobody answers properly: when does the loop stop.

This video is about the **Terminate** condition. Not the part where the verifier fires. The part where you decide the verifier's verdict is good enough to walk away.

---

## The model will always find something

Back in the first video of this chapter I flagged a problem and promised to come back to it. Here it is.

Tell a model "find what's wrong with this," and it will find something. Always. There is no artifact in the universe a sufficiently motivated reviewer cannot pick at. Ask it again and it picks again. The well of plausible criticism is infinite, because the model is generating, not measuring.

This is the same sycophancy you met with the attacker skill, just pointed the other way. When you ask a model "is this good?" the fluent answer is yes. When you ask "what's wrong with this?" the fluent answer is a list. You built the attacker by aiming that eagerness at refutation. Brilliant for finding the real flaw. Fatal if you never tell it when to stop, because now the eagerness has no off switch.

So an adversarial loop with no calibrated bar does one of two things. It runs forever, or you kill it at a random moment and call whatever it produced "done." Neither is convergence. Both are you pretending the loop terminated when really you just got tired.

[IMAGE: dark canvas, hand-drawn. A loop arrow circling between a box labeled "BUILD" and a box labeled "ATTACK". On the right, a tall stack of sticky notes spilling endlessly downward labeled "findings", each one smaller and fainter than the last, fading into the dark. No exit arrow anywhere. Caption underneath: "no bar, no exit".]

![[loopy-where-to-set-the-bar-no-bar-no-exit-3.png]]

---

## What the spiral actually looks like

Watch an uncapped review run and the findings degrade in a predictable shape.

Round one catches the real stuff. A broken assumption, a missing case, a claim with no support. Load-bearing. This is the round you wanted.

Round two is thinner. Some genuine medium issues, some "you could also consider." Round three is cosmetic. Naming, hypothetical edge cases that can't occur given the constraints, suggestions to "add more detail here" with no reason why. By round five the model is inventing concerns to justify being asked again. None of it is load-bearing. All of it keeps the loop alive and burns your tokens and your time.

The trap is that every one of these findings is *phrased* like the round-one findings. Same confident tone, same structure, same "Issue:" prefix. The model does not flag its own nits as nits. You have to be the one who decides a finding doesn't count, because the model never will.

That decision is the bar.

---

## Two ways to set it

There are exactly two levers, and you want both.

**Severity threshold.** Iterate until no medium or high severity issues remain. Low severity findings get logged, not gated on. The model still reports the cosmetic stuff, you just don't treat it as a reason to loop again. This is the quality lever, and it's my default. It says: I will keep going as long as something that actually matters is broken.

**Round cap.** At most N rounds, then ship what you have. A hard number, independent of what the findings say. This is the safety lever. It exists for the case where the threshold never trips because the model keeps manufacturing one more medium issue, or where two reviewers disagree forever. Three is a sane default. The cap doesn't care about quality. It cares that the loop is guaranteed to end.

Use them together. Threshold for quality, cap for safety, whichever trips first wins. If the artifact goes clean before round three, you exit on the threshold and save the rounds. If it never goes clean, you exit on the cap and ship the best version with the remaining lows logged. Either way the loop has a guaranteed exit, and the exit is calibrated to "is anything left that matters," not "did the model run out of things to say."

[IMAGE: dark canvas, hand-drawn. Two gates side by side feeding into one exit door. Left gate labeled "SEVERITY THRESHOLD — no med/high left", a small funnel below it dropping "low" findings into a tray labeled "logged, not gated". Right gate labeled "ROUND CAP — max 3". A bold arrow from "whichever trips first" pointing through the single exit door labeled "SHIP". Caption: "quality gate + safety gate".]

![[loopy-where-to-set-the-bar-two-gates-1.png]]
![[loopy-where-to-set-the-bar-two-gates-2.png]]
![[loopy-where-to-set-the-bar-two-gates-3.png]]
![[loopy-where-to-set-the-bar-two-gates-4.png]]
![[loopy-where-to-set-the-bar-two-gates-5.png]]

---

## Severity is your job, not the model's

One thing that trips people up. If you let the model assign severity with no scale, every finding is suddenly "high," because high feels important and the model wants to be helpful. You have to define the levels or the threshold means nothing.

Keep it blunt. High is "the artifact is wrong or will break." Medium is "the artifact is weaker than it should be in a way a reasonable reviewer would block on." Low is everything else: taste, polish, optional, hypothetical. Hand the reviewer that scale in the prompt and make it justify the rating against it.

This is the same move as the neutral attacker prompt from the last video. You don't tell the reviewer "find me a blocker," because then it engineers a blocker to please you. You give it the scale, ask it to report all findings rated honestly against that scale, and let the threshold do the gating. The incentive structure decides what stops the loop, not a phrasing you tuned by hand.

---

## This is the Terminate component, done on purpose

Map it back onto the five components from the start of this chapter. Trigger, Work, Check, Terminate, State.

Most people nail Work and Check and then leave Terminate implicit. "Loop until it looks done." That single lazy phrase is where both failure modes live. "Looks done" to an eager critic is never, so you get a runaway. "Looks done" to an eager builder is immediately, so you get a premature exit on round one with real issues still open. Same vague condition, opposite disasters, depending on which way the model's eagerness happens to point that day.

An explicit Terminate is the whole difference between a loop that converges and a loop that just stops. Threshold plus cap is what makes Terminate a real signal instead of a vibe. You are not asking the model "are we done." You are telling it the two conditions under which we are done, and letting it run until one is true.

[IMAGE: dark canvas, hand-drawn. The five-component spine as five linked boxes left to right: Trigger, Work, Check, Terminate, State. The "Terminate" box is circled in a bright accent stroke and pulled forward, with two inputs feeding it: a thermometer icon labeled "severity threshold" and a counter icon labeled "round cap", joined by a small "OR" symbol. Caption: "Terminate, made explicit".]

![[loopy-where-to-set-the-bar-terminate-component-1.png]]
![[loopy-where-to-set-the-bar-terminate-component-2.png]]
![[loopy-where-to-set-the-bar-terminate-component-3.png]]
![[loopy-where-to-set-the-bar-terminate-component-4.png]]
![[loopy-where-to-set-the-bar-terminate-component-5.png]]