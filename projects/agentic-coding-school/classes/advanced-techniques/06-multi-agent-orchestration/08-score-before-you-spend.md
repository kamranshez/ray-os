---
duration: "12-16 min"
batch: 1
order: 8
batch_name: "Multi-Agent Orchestration"
class: "advanced-techniques"
chapter: "Multi-Agent Orchestration"
status: "scripted"
aliases: [score-before-you-spend]
---

You cannot tell an agent to "fix the codebase."

Point it at thirty thousand files and say "find the bugs," "clean up the tech debt," "make this convert better," and you get nothing useful back. The codebase is too big to fit in context, and the agent has no idea where to start. So it flails, or worse, it laser focuses on the first thing it touches and leaves the actual problem untouched.

The fix is not a smarter agent. It is a cheap judge that runs first and decides where the smart agent should dig.

This video is about that judge. How to score every part of a large codebase before you spend a dollar of agent compute, so the work lands where it actually matters.

---

## We already touched this. Now we go deep on it.

In the stochastic starting points video, we wrapped a model in four steps to hunt security bugs. Step one was a ranker: score every file 1 to 5 by how likely it is to hold a bug, throw out the 1s and 2s, hunt the rest in order.

That ranker was one line in a four step pipeline. This whole video is that one step.

Because the ranker is not a security trick. It is a general tool, and it is the most underrated move in agentic engineering. The fan out, the verifier, the parallelism, those get the attention. The scoring step is the one quietly doing the targeting that makes everything downstream worth running.

[IMAGE: split panel. Left, a single agent labeled "fix the codebase" spraying arrows in every direction across a huge grid of files, hitting nothing. Right, a small "judge" box scoring the grid, the top few files glowing, one agent pointed straight at them.]

![[score-before-spend-agent-spraying-vs-targeted-1.png]]
![[score-before-spend-agent-spraying-vs-targeted-2.png]]
![[score-before-spend-agent-spraying-vs-targeted-3.png]]
![[score-before-spend-agent-spraying-vs-targeted-4.png]]
![[score-before-spend-agent-spraying-vs-targeted-5.png]]

---

## The real story behind the Firefox numbers

There was a chart going around. Firefox security bug fixes by month, flat for years, then a massive spike. The headline gave all the credit to a new model called Mythos.

Brian Grinstead, a distinguished engineer at Mozilla who ran the project, pushed back on that. His take: the model did maybe half of it. The harness did the other half. And inside the harness, the part that made it scale to tens of millions of lines of code was the scoring pass.

Source: How I AI with Claire Vo, "How Mozilla Fixed 500 Security Bugs with Claude Mythos," with Brian Grinstead. https://www.chatprd.ai/how-i-ai

Here is how he put the constraint:

> "Firefox has tens of thousands of source code files and tens of millions of lines of code. It's not possible to say one shot, go find all the potential bugs in this project. It's way too much context for the model."
> Brian Grinstead

So before any expensive agent runs, they ask a model a much smaller question, file by file. And they do not ask for one score. They ask for two.

> "Give me two scores. One score is how likely do you think there's a memory safety issue, and another is how easy could you access this from a web page?"
> Brian Grinstead, paraphrased from the episode

That second question is the clever one. Firefox has tons of code that web content can never reach. Operating system integration, internal tooling. A file can be full of bugs and still be low priority if no attacker can get to it. So you score risk, you score reach, and you multiply.

---

## This only matters in big codebases

Say it plainly, because it changes when you reach for this.

If your project is twenty files, you do not need a judge. You can read all twenty yourself and know where the problem is. Scoring is overhead with no payoff.

The judge earns its keep when the surface area is bigger than any human or any single context window can hold. Tens of thousands of files. Hundreds of components. A monorepo nobody has fully read. That is where "which part do I even look at" becomes the actual bottleneck, and where a cheap scoring pass turns an impossible task into a ranked list.

And the proof that this holds at the extreme is Firefox itself. This is not a toy run on a sample repo. Mozilla points this exact scoring pass at their own production browser, a codebase of tens of thousands of files and tens of millions of lines, built up over more than twenty years, the thing rendering this very page. They cannot one shot it, no human can hold it, so they score every file first and send the agents down the ranked list. If a judge can decide where to dig in something that enormous, it can rank whatever you are working on.

Big codebase, the judge is essential. Small codebase, skip it.

---

## The formula: Impact times Opportunity

Strip away the security specifics and every "where should the agent work" question is the same shape.

**Score = Impact times Opportunity.**

Impact is how much this part matters. Reach, traffic, how often it runs, how many things depend on it. Opportunity is how bad or how fixable it is right now. How buggy, how slow, how far it has drifted from good.

You need both, and you multiply them, because either one alone lies to you. A component everyone hits but that already works is a waste of the agent's time. A component that is broken but that nobody ever touches is also a waste. You want the corner where both are high.

That gives you four corners:

1. **High impact, high opportunity.** This is the hotspot. Work here first.
2. **High impact, low opportunity.** It matters but it is already fine. Leave it.
3. **Low impact, high opportunity.** Broken, but nobody cares. Skip it.
4. **Low impact, low opportunity.** Irrelevant. Ignore.

The judge's entire job is to sort the codebase into these four corners and hand you the first one.

[IMAGE: a 2x2 matrix. X axis "Opportunity, how fixable now," Y axis "Impact, how much it matters." Top right quadrant glowing and labeled "Hotspot, work here." Top left "Already fine, leave it." Bottom right "Nobody cares, skip." Bottom left "Irrelevant." A few dots scattered, the brightest dot in the top right.]

![[impact-opportunity-four-quadrants-1.png]]
![[impact-opportunity-four-quadrants-2.png]]
![[impact-opportunity-four-quadrants-3.png]]
![[impact-opportunity-four-quadrants-4.png]]
![[impact-opportunity-four-quadrants-5.png]]

---

## Where the signal comes from

The whole game is Impact times Opportunity. The interesting part is what you feed each axis. And that ranges from hard data you already have to a rubric you have to sit down and write.

Think of it as a spectrum.

**Telemetry.** The most grounded end. You already have the numbers. Product analytics tells you which components real users hit and where they drop off. A profiler tells you which code path is slow. Git history tells you which files change constantly. The score is objective because it is built on measured reality.

**Tool emitted.** The judge reads a tool's output instead of guessing. A linter's accessibility violations. The type checker's count of untyped surface. A coverage report. Still grounded, just one step removed.

**Rubric you write.** The hardest end, and the most interesting. No data exists, so you author the definition of good. Design consistency. API conventions. Code clarity. You write down what good looks like, and the judge scores drift from it.

That last one is the uncomfortable lesson. Brian told a story about getting off a call with someone in design, not engineering, and the takeaway was the same:

> "This is the moment where you're actually going to have to write down what good design is and how you might quantitatively evaluate that."
> Brian Grinstead

The bottleneck is never the model. It is whether you can state "good" crisply enough to put a number on it. The teams that already did that work, the ones with fuzzing signals and analytics and written conventions, are years ahead. Not because of the model. Because they can score.

[IMAGE: a horizontal spectrum arrow. Left end labeled "Telemetry, analytics / profiler / git history," middle "Tool emitted, linter / type checker / coverage," right end "Rubric you write, design / conventions / clarity." A gradient from "objective" on the left to "you must define good" on the right.]

![[scoring-signal-spectrum-telemetry-to-rubric-1.png]]
![[scoring-signal-spectrum-telemetry-to-rubric-2.png]]
![[scoring-signal-spectrum-telemetry-to-rubric-3.png]]
![[scoring-signal-spectrum-telemetry-to-rubric-4.png]]
![[scoring-signal-spectrum-telemetry-to-rubric-5.png]]

---

## Cheap judge, expensive agent

Here is the economic structure, and it is why this is an architecture and not just a prompt.

Scoring is a shallow, per file judgment. Look at one file, emit two numbers, move on. It is cheap, fast, and embarrassingly parallel. You can run it across thirty thousand files for the price of one deep agent run.

The deep work is the opposite. Read the code, form a hypothesis, write a test, run it, retry fourteen times. That is expensive and slow.

So you use the cheap judge to decide where to send the expensive agent. Tiered compute. The judge spends pennies to save the agent from spending dollars in the wrong place.

And this matters more than people admit, because agent work is not free.

> "There is actually a time cost to shipping, reviewing, verifying AI code. And so you cannot go completely prioritization free."
> Claire Vo, on the episode

You cannot cover the earth in AI code. Every run burns tokens, and every fix burns a human reviewer. Your real budget is attention, and the judge is how you spend it on the highest leverage surface first.

[IMAGE: a funnel. Wide top labeled "30,000 files." A narrow band in the middle labeled "cheap judge, scores all of them." A thin spout at the bottom labeled "top 200, expensive agent runs here." Dollar signs tiny at the top, large at the bottom.]

![[cheap-judge-expensive-agent-funnel-1.png]]
![[cheap-judge-expensive-agent-funnel-2.png]]
![[cheap-judge-expensive-agent-funnel-3.png]]
![[cheap-judge-expensive-agent-funnel-4.png]]
![[cheap-judge-expensive-agent-funnel-5.png]]

---

## A worked example you can picture: tech debt

Take the most common version. You want to attack tech debt in a big repo, but "fix the tech debt" is not a task an agent can act on.

So you score it. Impact is **churn**, how often a file changes. You get that straight from git history with one command that counts the commits touching each file. A file the team rewrites every week is a file they keep fighting with, so churn is a clean proxy for how much pain it causes.

Opportunity is complexity. Size, nesting, tangle. How hard the file is to change.

Multiply them and the four corners come alive. A file that changes constantly and is huge and tangled is the hotspot. A giant file nobody has touched in two years is scary but stable, leave it. A tiny file edited daily is fine. The judge weighs a small frantically changed file against a giant stable one, and that judgment is exactly the thing raw sorting cannot do. It is not "biggest file wins." It is impact times opportunity.

[IMAGE: left side, a raw bar chart "churn, commits per file" with one tall bar. Right side, after multiplying by complexity, the bars reorder, a different file rises to the top, an arrow labeled "x complexity" between them. Caption feel: "raw churn is not the answer, the product is."]

![[churn-leaderboard-to-ranked-hotspots-1.png]]
![[churn-leaderboard-to-ranked-hotspots-2.png]]
![[churn-leaderboard-to-ranked-hotspots-3.png]]
![[churn-leaderboard-to-ranked-hotspots-4.png]]
![[churn-leaderboard-to-ranked-hotspots-5.png]]

---

## Score sits at the front of the loop

Pull all the way back and the Firefox system is one shape, and you have seen most of it in the other videos in this chapter.

**Score.** The cheap judge ranks the surface area. This video.
**Target.** Pick the top of the list, within budget.
**Loop.** Hand the agent one tightly scoped problem with a clear pass or fail signal, and let it retry far past the point a human would quit.
**Verify.** A second fresh agent tries to disprove the result, catching the agent when it cheats.

The loop and the verifier are the stochastic starting points and the point fix to architectural fix videos. This one is the front door. And without the front door, none of the rest scales, because the agent never knows where to begin.

[IMAGE: a left to right pipeline. First box "Score, cheap judge" highlighted and labeled "this video." Then "Target, top N." Then "Loop, scoped retry." Then "Verify, fresh skeptic." An arrow loops from Verify back to Target. The Score box is clearly the entry point.]

![[score-target-loop-verify-pipeline-1.png]]
![[score-target-loop-verify-pipeline-2.png]]
![[score-target-loop-verify-pipeline-3.png]]
![[score-target-loop-verify-pipeline-4.png]]
![[score-target-loop-verify-pipeline-5.png]]

---

## Demo

The worked example is my own course funnel, because it has both halves of the score sitting on the same files: real analytics events for Impact, and git churn for Opportunity.

1. Show the problem. Open the landing and funnel components folder. Thirty something components: Hero, PricingCards, FAQ, testimonials, the paywall, the checkout. Frame it: "an agent cannot fix all of these, which ones earn the work?"

2. Build the Impact signal. Pull the real funnel events out of the code, the analytics captures like paywall viewed, purchase button clicked, video abandoned. That is reach and drop off per component.

3. Build the Opportunity signal. Run the churn command over the same components. PricingCards has been rewritten dozens of times, the legal pages almost never. High churn means contested and unstable, so high opportunity.

4. Hand both feeds to Claude as the judge with the rubric Score = Impact times Opportunity, and ask for a ranked table with a one line reason per component. Watch PricingCards and the paywall float to the top, high traffic, a drop off event sitting right there, heavy churn. Watch the terms and privacy pages sink, maybe churny, but zero funnel impact. That contrast is the whole point on screen.

5. Spend the budget. Tell the agent to act only on the number one ranked component and ignore the rest. Score, target, act.

6. Re run the judge after the fix to show the score move.

Then a sixty second callback to a second repo to prove it is not just analytics. Open a project that ships a written API conventions doc and thirty one endpoints. Now the signal is the rubric end of the spectrum. The judge scores each endpoint against the team's own written rules, response envelope, error format, pagination style, and ranks which endpoints have drifted furthest. Same formula. Different fuel. One grounded in telemetry, one grounded in a document you wrote.

---

## Key Insight

> Intelligence got cheap. Attention did not. In a codebase too big to read, the model finds the fix, but a cheap judge scoring Impact times Opportunity is what decides whether you ever look there. Score before you spend.

---

## What you can score

You will not use all of these. The point is the pattern transfers everywhere. Every line is the same formula, Impact times Opportunity, with different fuel. Here are fifteen.

1. **Conversion and UX components.** Analytics traffic times drop off. Rebuild the worst converting high traffic component.
2. **Tech debt hotspots.** Git churn times complexity. Refactor the files that are both hot and tangled.
3. **Performance.** Run frequency times slowness. The benchmark is the score, make the number go down.
4. **Test coverage gaps.** Blast radius times coverage gap. Test the uncovered code the most things depend on.
5. **Cloud and LLM cost.** Spend times optimizability. Point the agent at the three calls burning the budget.
6. **Bug proneness.** Change frequency times historical fix density from git blame. The files that keep getting hotfixed.
7. **Accessibility.** Page traffic times a11y violations from a linter. Fix where real users land.
8. **Type safety.** Criticality times untyped density from the type checker. Harden the loose code that matters.
9. **Dead code.** Confidence it is unused times size. Delete the big confidently dead stuff first.
10. **Dependency freshness and risk.** Centrality times staleness. Upgrade the dependencies that touch everything.
11. **Design consistency.** Component usage times drift from your design rubric. Fix the most seen, most off system components.
12. **API consistency.** How public it is times drift from your conventions doc. Fix the endpoints that broke the rules.
13. **Documentation gaps.** How used it is times how undocumented it is. Document the depended on, unexplained APIs.
14. **Onboarding friction.** How many users reach a step times how much friction it has. Smooth the screen that loses the most people.
15. **SEO and content.** Page traffic times ranking gap. Improve the pages closest to the prize.

---

## The takeaway

Stop pointing agents at your whole repo and hoping. In anything big, the move is to score first.

Write down what good means, turn it into Impact times Opportunity, let a cheap judge rank the entire surface, and spend your expensive agent and your own review time on the top of the list.

The model is not the moat. The judge that decides where to point it is.
