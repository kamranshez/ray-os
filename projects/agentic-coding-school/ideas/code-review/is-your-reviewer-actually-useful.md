---
duration: "12-16 min"
batch: 1
order: 2
batch_name: "Evaluating Reviewers"
class: "code-review"
chapter: "Evaluating Reviewers"
status: "idea"
aliases: [is-your-reviewer-actually-useful]
---

A reviewer that is right once and noisy forty times is worse than no reviewer at all.

That sounds backwards, so sit with it. If the reviewer says nothing, your team reads the diff themselves. If the reviewer leaves two real findings buried in thirty-eight nitpicks, your team reads the first five comments, sees they are garbage, and starts skipping every comment the bot leaves. Including the two that mattered. You did not add a safety net. You added noise, and then you trained everyone to tune the net out.

This video is about the question the backtest cannot answer: not "can the reviewer catch a disaster," but "is it worth reading on a normal Tuesday."

---

## What everyone gets wrong: usefulness is not correctness

People evaluate a reviewer by asking "is it ever right." That is the wrong axis. The axis that decides whether a reviewer survives contact with a real team is signal density. Of everything it says, how much is worth a human's attention.

A reviewer that is correct ten percent of the time and silent the rest is useful. A reviewer that is correct ninety percent of the time but says something on every line is useless, because no one can find the ninety percent through the volume.

This is alert fatigue, and every engineer who has ever worked next to a screaming monitoring dashboard already knows the ending. The signal is in there somewhere. Nobody is looking, because looking stopped being worth it. **The thing that kills an AI reviewer in production is almost never that it was wrong. It is that it was noisy, and noise gets the whole reviewer muted.**

[IMAGE: dark canvas, a single PR with a long stack of forty review comments down the side, only two of them glowing as real signal and the rest greyed as nits, a human figure at the top reading the first few, throwing up their hands and clicking a "mute reviewer" toggle, the two real comments going unread in the pile]
![[code-review-useful-noise-tax-1.png]]
![[code-review-useful-noise-tax-2.png]]
![[code-review-useful-noise-tax-3.png]]
![[code-review-useful-noise-tax-4.png]]
![[code-review-useful-noise-tax-5.png]]

---

## The problem: you have no labels here

In the backtest, you had ground truth. Each PR carried a tag, this one caused an incident, and you could score the reviewer against it.

Out on the everyday stream, that tag does not exist. The overwhelming majority of PRs never caused an incident and never will. There is no label that says "this comment was good." So you cannot run the backtest here. You have thousands of PRs and zero answers attached to them.

This is exactly the wall you hit when you try to evaluate anything at scale. The honest signal is missing. And the tempting shortcut is to ask a model to grade the comments: "rate this review from one to ten." Do not do that. That is the self grading trap. The model that writes confident comments will rate confident comments highly. You have measured the model's opinion of itself, which is worth nothing.

You need a grader that lives outside the model. You need a borrowed verifier.

[IMAGE: dark canvas, a vast field of grey unlabeled PR cards stretching back, only a tiny handful at the front carrying a red "incident" label, a big question mark hovering over the grey majority captioned "no ground truth here", contrasted against a small boxed-off region labeled "the backtest lived here"]
![[code-review-useful-no-labels-1.png]]
![[code-review-useful-no-labels-2.png]]
![[code-review-useful-no-labels-3.png]]
![[code-review-useful-no-labels-4.png]]
![[code-review-useful-no-labels-5.png]]

---

## The core insight: let the humans grade it for you, without asking them

Here is the borrowed verifier, and it is sitting in your git history already.

For every comment a reviewer left, ask a simple question: did a later commit on that PR change the code the comment pointed at. If the reviewer flagged line forty, and the next push edited line forty, somebody read that comment and acted on it. The comment moved code. That is a vote, cast by a human, with their hands, not their opinion.

This is the actioned rate. And it is beautiful because nobody had to fill out a survey. The signal is already in the diff history. The grader is human behavior, which is exactly the kind of exogenous signal you want, the same principle as grading a discovery loop against the real world instead of against the model's mood.

So now you can score a reviewer with no incident labels at all. Run it over a hundred historical PRs, look at every comment it would have left, and measure what fraction got actioned. A reviewer whose comments consistently move code is earning its place. A reviewer whose comments are consistently ignored is talking to itself.

[IMAGE: dark canvas, a review comment pinned to line 40 of a diff on the left, a forward arrow to a later commit on the same PR that visibly edits line 40, the pair stamped "actioned" with a green check; below it a second comment pinned to a line that never changes again in any later commit, stamped "ignored" in grey; caption "the human voted with a commit"]
![[code-review-useful-actioned-rate-1.png]]
![[code-review-useful-actioned-rate-2.png]]
![[code-review-useful-actioned-rate-3.png]]
![[code-review-useful-actioned-rate-4.png]]
![[code-review-useful-actioned-rate-5.png]]

---

## The honest caveat: actioned is not the same as correct

I have to put the knife in my own idea here, because if I do not, your evaluation will lie to you.

Actioned does not mean correct. People action nits too. The reviewer says "rename this variable," somebody shrugs and renames it, the comment got actioned and it was still a waste of everyone's time. If you optimize for actioned rate alone, you will reward a reviewer that leaves lots of small, easy, agreeable changes, because those get actioned at a high rate. You will have built a machine for generating busywork that people comply with.

So actioned rate never travels alone. You pair it with signal density: how many comments did the reviewer leave per PR in the first place. A reviewer with a high actioned rate and three comments per PR is gold. A reviewer with the same actioned rate and thirty comments per PR is the noise machine from the start of this video wearing a disguise.

Think of it as a two by two. A comment is either actioned or ignored, and either substantive or a nit. The reviewer you want lives in one corner: substantive and actioned, and not many comments total. Everything else is either noise, busywork, or a reviewer talking to a wall.

[IMAGE: dark canvas, a 2x2 grid, x-axis ignored to actioned, y-axis nit to substantive; the top-right cell (substantive AND actioned) glowing as "the gold quadrant", bottom-right (nit but actioned) labeled "busywork compliance", top-left (substantive but ignored) labeled "good points, muted reviewer", bottom-left labeled "pure noise"; a separate small gauge on the side labeled "comments per PR" with an arrow pointing low as "and keep this small"]
![[code-review-useful-actioned-vs-correct-1.png]]
![[code-review-useful-actioned-vs-correct-2.png]]
![[code-review-useful-actioned-vs-correct-3.png]]
![[code-review-useful-actioned-vs-correct-4.png]]
![[code-review-useful-actioned-vs-correct-5.png]]

---

## The full set of signals, strongest to weakest

Actioned rate is the workhorse, but it is not the only exogenous signal in your history. Use them in this order.

1. **Actioned rate.** Did a later commit change the flagged code. Strongest, because it is a human acting with their hands.

2. **Thread resolution.** Most platforms already track whether a review thread was resolved or dismissed. Cheaper to read than diffing commits, slightly noisier, because people resolve threads for all kinds of reasons.

3. **Overlap with the eventual fix.** For the PRs that did later get a bugfix, did the reviewer's comment point at the same lines that fix touched. This is the bridge back to the backtest, applied to the everyday stream. When it lines up, that is a strong correct signal, not just an actioned one.

4. **Judge rubric, as a tiebreaker only.** You can have a model score each comment for whether it is actionable and substantive. But this is the self grading trap again, so it never decides anything on its own. Use it to break ties between two reviewers that are close on the real signals, and never as the headline number.

The discipline is the same as everywhere in this course. The further up this list, the more the grade is grounded in something outside the model. Lead with behavior. Let the model's opinion be the last word, never the first.

---

## The artifact: a reviewer scorecard

Now put it together, because this is the deliverable, the thing the whole video builds to.

Take a hundred historical PRs. Run two reviewers over all of them, reviewer A and reviewer B. That can be Claude versus Codex, or one prompt versus another, or the AI reviewer versus your team's actual human review history. For each one, compute two numbers: actioned rate, and comments per PR. Maybe a third, overlap with eventual fixes, where you have them.

That table is the scorecard. And it settles arguments. Reviewer A actions at sixty percent and leaves four comments per PR. Reviewer B actions at forty percent and leaves nineteen comments per PR. You do not need a meeting. A is the keeper. B is the one that was going to get muted in week two.

This is the same decision from the council idea, made rigorous. When you have several reviewers on a council, the scorecard is how you decide who keeps their seat. A reviewer that stops earning its actioned rate gets retired, the same way a discovery loop's verifier has to stay grounded or get pulled. The council is not a fixed roster. It is a roster the scorecard keeps honest.

[IMAGE: dark canvas, a two-column scorecard comparing Reviewer A and Reviewer B across rows labeled "actioned rate", "comments per PR", "overlap with later fixes"; A's column glowing as the winner (high actioned, low comment count), B's column flagged with a small mute icon (lower actioned, high comment count); above it the input drawn as a stack of "100 PRs" feeding both columns]
![[code-review-useful-scorecard-1.png]]
![[code-review-useful-scorecard-2.png]]
![[code-review-useful-scorecard-3.png]]
![[code-review-useful-scorecard-4.png]]
![[code-review-useful-scorecard-5.png]]

---

## The best part: you can run this tonight

The backtest needed an incident history, which is a high bar. Plenty of people watching this do not have a clean one.

This needs none of that. Every repo with a pull request history already has everything required: comments, and the commits that came after them. You do not need a single logged incident. You point the loop at your last hundred PRs and it tells you, today, whether the reviewer you are about to trust is signal or noise.

That makes this the cheaper, more honest first move for most teams. Run the usefulness audit before you even think about backtesting. If a reviewer cannot clear the noise tax on your everyday PRs, it does not matter how well it would have done on your worst day, because your team will have muted it long before that day arrives.

---

## Demo

Put it on screen end to end.

1. **Pull a hundred PRs.** Grab the last hundred merged PRs from a real repo with their full comment and commit history. On screen: the list, with comment counts next to each.

2. **Replay two reviewers.** Run Claude and Codex, through the codex-bridge, over each PR's diff, generating the comments each one would have left. Two sets of comments per PR.

3. **Score the actioned rate.** For each generated comment, check whether a later commit on that PR touched the lines it flagged. Tally the fraction. Do it for both reviewers.

4. **Score the noise.** Count comments per PR for each. Show one PR where reviewer B left twenty three comments and two got actioned, next to one where reviewer A left three and two got actioned. Same useful output. Wildly different cost to read.

5. **Print the scorecard.** Two columns, the numbers filled in. Say the verdict out loud: A is worth turning on, B would have been muted by Thursday. One reviewer earned its seat, measured against your own history, with not a single incident label in sight.

Total demo: about five minutes. The point is you decided which reviewer to trust on the everyday stream using a signal you already had and never looked at, the commits your team made right after reading the comments.

---

## Key Insight

> A reviewer does not die because it was wrong. It dies because it was noisy and got muted. Usefulness is not how often it is right, it is how much of what it says is worth reading. Your team already grades that, one commit at a time.

---

## Where we go next

You can now answer both halves of the question. Backtesting tells you whether a reviewer catches the disasters. The usefulness audit tells you whether it is worth reading on the days nothing is on fire. Recall on your worst day, signal density on every other day.

Put those two together and you are not choosing a reviewer on faith anymore. You are choosing it on evidence, both kinds, measured against your own code.

Which means you can finally run more than one of them and know which to believe. That is the council, and it is where we go next.

See you in the next one.
