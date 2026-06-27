---
duration: "12-16 min"
batch: 1
order: 1
batch_name: "Evaluating Reviewers"
class: "code-review"
chapter: "Evaluating Reviewers"
status: "idea"
aliases: [backtesting-a-new-reviewer]
---

You are about to put an AI reviewer on every pull request in your repo. It is going to read more code than any human on your team, and it is going to do it forever. Here is the question nobody asks before they flip that switch: is it any good?

Not "does it sound smart." Not "did it leave nice comments on the three PRs I tried it on." Is it actually going to catch the thing that takes prod down at 2am.

You can answer that before you trust it. You backtest it.

---

## What everyone gets wrong: you can't eval a reviewer on vibes

The normal way people pick an AI reviewer is the worst possible way. They turn it on, watch it comment on a few PRs, read the comments, think "yeah, that seems reasonable," and ship it to the whole team.

That is not an evaluation. That is a demo. You picked the reviewer because its prose was confident, not because it caught anything that mattered.

The problem is you tested it on PRs that were already fine. Of course the comments looked reasonable. There was nothing to catch. You learned that the reviewer can write English. You learned nothing about whether it can find the bug that costs you a weekend.

To actually evaluate a reviewer you need PRs where you know the answer. You need code that broke, and you need to know exactly how it broke. And here is the thing: you already have that. You have been generating it for years and throwing it away.

---

## The core insight: your incidents are a labeled dataset you already paid for

Every incident you have ever had traces back to a change. A commit, a PR, a specific diff that introduced the thing that eventually broke. That pairing, the diff on one side and "this caused an incident" on the other, is a label. It is ground truth. And it cost you an outage to generate.

Most teams treat an incident as a story. Postmortem, action items, a wiki page nobody reads again, move on. The signal evaporates.

Backtesting says the opposite. That incident is a permanent test case. Keep it forever. The diff that caused it is now an exam question with a known answer: would a candidate reviewer, shown only this diff, have flagged the line that broke?

That is the whole reframe. **Code review evaluation is not a vibe check. It is a regression test suite for your reviewer, and the test cases are your own past disasters.**

[IMAGE: dark canvas, left side a production incident drawn as a red alert/flame, an arrow tracing back through git history to the single PR diff that caused it, that diff getting boxed and filed into a stack labeled "eval corpus" on the right as a labeled card (diff on top, a red "caused incident" tag on the bottom), caption feel of "the outage paid for this label"]
![[code-review-backtest-incidents-as-labels-1.png]]
![[code-review-backtest-incidents-as-labels-2.png]]
![[code-review-backtest-incidents-as-labels-3.png]]
![[code-review-backtest-incidents-as-labels-4.png]]
![[code-review-backtest-incidents-as-labels-5.png]]

---

## Where the word comes from

Backtesting is borrowed from trading, and the analogy is exact enough that it is worth one minute.

A quant has historical price data. That is the ground truth, the market actually did a thing. They have a strategy, which is just a decision rule: when X happens, buy. They want to know if the strategy is any good before they put real money behind it. So they replay it against history. Run the rule over the last ten years of prices and measure what it would have made. No real money at risk. Just the rule, the history, and a score.

Map it across one to one. The historical prices are your past PRs. The strategy is your reviewer, which is a decision rule made of three parts: a model, a prompt, and a technique. The replay is running that reviewer over your labeled PRs. The score is whether it caught the diffs that caused incidents.

You are not asking the reviewer to predict the future. You are asking it to prove itself against a past where you already know what happened.

---

## The two traps that come with the analogy

Backtesting in finance has two famous ways to fool yourself, and both of them transfer directly. If you do not know about them, your backtest will lie to you and you will deploy a reviewer that looks great and is useless.

**The first trap is look-ahead leakage.** In trading, the cardinal sin is letting the strategy peek at data from the future. The PR version is sneakier than it sounds. When you replay a past PR, you have to reconstruct the repo exactly as it was at that commit and show the reviewer only the diff as it existed then. If you accidentally let it see the fixed version, or the linked postmortem, or even the issue title that says "null pointer crash in checkout," it catches the bug instantly. Of course it does. You handed it the answer key. Your catch rate looks incredible and means nothing.

The fix is discipline. Snapshot the parent commit. Strip anything that references the fix. The reviewer sees what a reviewer would have seen the day that PR was opened, and nothing else.

[IMAGE: dark canvas, a horizontal git timeline left to right, a PR diff sitting at one point on the line, a reviewer figure standing at that point; a forbidden dotted arrow reaching forward in time to the later "fixed" commit and the postmortem doc, with a big red circle-slash over that forward peek; caption "show it only what was visible the day the PR opened"]
![[code-review-backtest-lookahead-leakage-1.png]]
![[code-review-backtest-lookahead-leakage-2.png]]
![[code-review-backtest-lookahead-leakage-3.png]]
![[code-review-backtest-lookahead-leakage-4.png]]
![[code-review-backtest-lookahead-leakage-5.png]]

**The second trap is overfitting.** A trading strategy tuned until it perfectly explains every past crash is worthless, because it learned the noise, not the pattern. It nails history and dies on the next live trade. A reviewer tuned until it catches every one of your past incidents has the same disease. It has memorized your specific disasters and learned nothing general. The next incident will be a class it has never seen, and it will sail right past it.

Two defenses. Hold some incidents out, never let the reviewer's tuning touch them, and measure on those. And measure by incident class, not by individual incident. You do not care that it caught that one race condition. You care that it catches race conditions.

And there is a third thing that is not exactly a trap but is the most common rookie mistake: you must also run the reviewer over clean PRs. PRs that shipped fine and never caused anything. Because a reviewer that screams "this looks dangerous" on every single PR will catch one hundred percent of your incidents and be completely useless. It has perfect recall and zero precision. Every PR is a false alarm. The real number you are chasing is the tradeoff between the two, the same way a trader chases return against drawdown, not return alone.

---

## The pipeline

Here is the actual loop, start to finish. Six steps.

1. **Label.** Link each incident to its root cause PR. Sometimes this is already in your incident tracker. Sometimes you point an agent at the postmortem and the git history and let it find the commit. Either way you end up with a list of diffs that each carry a "caused an incident" tag.

2. **Snapshot.** For each one, check out the parent commit so the world looks exactly like it did before the bad change landed. This is your leakage defense.

3. **Replay.** Run the candidate reviewer over the isolated diff, in that snapshot context. One reviewer, or several, which we will get to.

4. **Score.** Did it flag the offending lines? At what severity? Run the clean PRs through too and count how often it cried wolf.

5. **Compare.** Now vary the three knobs. Different model. Different prompt. Different technique, like adding a specialized security critic or an adversarial pass. Each combination gets a catch rate and a false alarm rate. You are building a grid.

6. **Promote.** Pick the combination that sits on the good edge of that grid, high catch rate without drowning everyone in false alarms, and deploy that one to live PRs. Then add every new incident to the corpus so the next evaluation is sharper than this one.

[IMAGE: dark canvas, a left-to-right pipeline of six labeled stages as connected boxes: Label (incident linking to a diff), Snapshot (a git commit checkout icon), Replay (a reviewer reading the diff), Score (a catch/miss tally plus a false-alarm tally), Compare (a small grid of model x prompt cells), Promote (one cell highlighted and shipped to a live PR queue); a thin loop arrow from Promote back to Label labeled "every new incident feeds the corpus"]
![[code-review-backtest-pipeline-1.png]]
![[code-review-backtest-pipeline-2.png]]
![[code-review-backtest-pipeline-3.png]]
![[code-review-backtest-pipeline-4.png]]
![[code-review-backtest-pipeline-5.png]]

---

## What you actually walk away with

The output of all this is not just "reviewer B beat reviewer A." The thing you build is more valuable than the decision it helped you make.

You end up with a benchmark that is specific to your codebase. SWE-bench does not know your incident patterns. The generic leaderboard does not know that your team keeps shipping the same category of migration bug. Your backtest corpus does. It is a private eval, grown from your own failures, and it gets richer every time something breaks.

That is an asset most teams will never have, because they keep throwing the labels away. The first time you swap models, you will not argue about which one feels smarter. You will run both against your corpus and read the number.

---

## Why this makes software more reliable, not less

There is a hot take going around that AI generated code will make everything more reliable, not less, even though the raw number of incidents goes up. Backtesting is the mechanism that makes that true, and it is worth seeing why.

The raw count goes up because you are simply shipping more. More volume, more changes, more chances to break something. But the rate, incidents per change, goes down, and it goes down because of a ratchet.

Every incident becomes a permanent test case. The reviewer gets tuned until it catches that class of bug. From then on, that entire class is guarded, forever, on every future PR. The failure does not just get fixed. It gets converted into an antibody. The system cannot get that disease the same way twice.

That is the same compounding idea from everywhere else in this course. A test case is paid for once and pays out forever. Reliability stops being a thing you maintain and becomes a thing that only moves in one direction, because every failure permanently raises the floor.

[IMAGE: dark canvas, a ratchet wheel drawn climbing one direction only, each tooth labeled with a past incident class (race condition, null case, migration, auth bypass), a pawl preventing it from slipping back; a rising reliability floor line underneath, with raw incident count drawn going up while a "per change" rate line drops]
![[code-review-backtest-ratchet-1.png]]
![[code-review-backtest-ratchet-2.png]]
![[code-review-backtest-ratchet-3.png]]
![[code-review-backtest-ratchet-4.png]]
![[code-review-backtest-ratchet-5.png]]

---

## Demo

Let me make this concrete on a real repo, and I will use a trick so you can run it even if you have never had a logged incident.

1. **Build the corpus from bugfix PRs.** Most repos do not have a clean incident log, but every repo has bugfix PRs. Pull the merged PRs whose titles start with `fix:` and reference an issue. Treat each one as a proxy incident: the bug it fixed is the thing a good reviewer should have caught, and the diff that introduced that bug is sitting in the history just before it. On screen: a list of twelve `fix:` PRs pulled from the repo.

2. **Snapshot and strip.** For one of them, check out the commit just before the fix. Show that the broken code is now in front of us, and the fix and its description are nowhere in context. This is the leakage guard, live.

3. **Run a council, not one reviewer.** Send the broken diff to two reviewers at once: Claude, and Codex through the codex-bridge. Two different models reading the same change in fresh context. Watch them come back. One flags the off-by-one. One misses it. That disagreement is data.

4. **Score it.** Mark the catch. Then run the same two reviewers over three clean PRs and count the false alarms. Put the four numbers on screen: catches and false alarms for each reviewer.

5. **Read the verdict.** Across the twelve proxy incidents, one configuration caught nine and cried wolf twice. The other caught seven and cried wolf six times. You are not guessing anymore. You are reading a scoreboard, and the scoreboard tells you exactly which reviewer earns a seat on every PR.

Total demo: about five minutes. The point is that you walked in with an opinion about which reviewer was better and walked out with a number, measured against your own code.

---

## Key Insight

> An AI reviewer you have not backtested is a reviewer you are trusting on faith. Your incidents are a labeled exam you already paid for in outages. Grade the reviewer before you give it the keys.

---

## Where we go next

Backtesting answers one question: will the reviewer catch the things that blow up. That is recall, measured against your worst days.

But your worst days are rare. The vast majority of PRs never cause an incident and never will. So how do you know the reviewer is worth having on those? A reviewer can ace the backtest and still be a disaster on the everyday stream, because it buries its one good catch under forty pointless nits and trains your whole team to ignore it.

That is the other half of the problem, and it is the next video. Not "does it catch the bad stuff," but "is it worth reading at all."

See you in the next one.
