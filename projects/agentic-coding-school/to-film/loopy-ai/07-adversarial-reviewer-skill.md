---
duration: "10-14 min"
batch: 3
order: 7
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "Pair Every Creator With An Attacker"
aliases: [adversarial-reviewer-skill]
---

Every skill that creates something needs a sibling skill whose only job is to attack what it made.

Same model. Opposite prompt. One is told to build. The other is told that its job is rigour, not agreement. You run them in series, surface only the disagreements, and fix upstream.

That's the whole pattern. It's small, it's portable, and the rest of this class is built on top of it.

---

## The problem: the model wants to agree with you

In the last segment we said self-grading loops are vibes, and we fixed it by borrowing someone else's verifier. A test. A linter. Lighthouse. Something outside the model that touches reality and can't be talked out of its answer.

But a lot of the work you'll point loops at has no borrowed verifier. A PRD has no compiler. A plan has no test suite. A landing-page headline has no linter that tells you it lands. Prose, strategy, structure: there's no tool sitting online that returns a pass or fail.

So what do you do when reality won't grade the work for you?

The naive answer is the one everybody reaches for first. Agent writes a PRD. Same agent reviews the PRD. Says "looks good." Ship it.

You already know why that fails. The model is eager to please you. Ask it whether the thing it just wrote is good, and the most fluent next token is "yes." It's not lying. It just has no reason to disagree with itself.
Source: https://x.com/systematicls/status/2028814227004395561

[IMAGE: dark canvas, a single head looking at a sheet of paper labeled "PRD" that it just wrote, a speech bubble saying "looks good to me", the whole thing circled and crossed out, labeled "vibes"]
![[images/adversarial-reviewer-skill/self-review-vibes.png]]

---

## The core insight: you don't need a different model, you need an opposite job

Here's the trick, and it's smaller than people expect.

You do not need a smarter model to review the work. You do not need a different model to review the work. You need the *same* model, given the opposite job.

The creator is told: build this. The attacker is told something like: your job is to refute this artifact. Default to refuted unless the case is airtight. Specifically hunt for miracle steps, vague assumptions, and untested invariants. Do not be agreeable. If you can't find a real problem, say so explicitly, but look hard first.

Same weights. Asymmetric instructions. That asymmetry is the entire mechanism. You've given the model a reason to disagree, which it never had when you asked it to grade its own homework.

This is the same idea we met with borrowed verifiers, generalised. A borrowed verifier gets its reason to disagree from reality, from a runtime observation the builder couldn't author. When there's no reality to borrow from, you manufacture the reason to disagree inside the prompt instead. You weight the instructions hard toward refusal.

[IMAGE: dark canvas, two identical heads facing each other, same colour and shape, one labeled "build", one labeled "refute", a single document passing from one to the other]
![[images/adversarial-reviewer-skill/build-vs-refute-heads.png]]

---

## Two levers, not one

The prompt is the bigger lever. But there's a second, quieter one, and you want both.

The second lever is context. Run the attacker as a separate subagent, in a fresh window. Not as the next turn in the same conversation.

Think about why. In one context, the model has already typed "here is the PRD." Now it's reading its own work as something to defend. It's committed. A fresh window has never said those words. It reads the same document as something to break.

We named this exact bridge back in closing the loop: fresh context buys honesty, not rigour. That's why you need both levers and not just one. The fresh context stops the reviewer from defending what it already wrote. The asymmetric prompt gives it something to actually do with that independence: refute, don't restate. Fresh eyes alone drift back to "looks fine," because an unprimed model with no instruction to attack is still an agreeable model. Honesty plus a reason to disagree. That's the pair.

This is also why subjective work leans on this pattern harder than code does. Code already has borrowed verifiers that touch reality, so the verifier comes pre-loaded with a reason to disagree. Prose has no compiler. The only independent grade you can get on a PRD is a fresh context pointed at refutation.

---

## The skill-pair shape

Here's the part that makes this more than a clever conversation trick.

You store the two prompts as two separate, named skills. A creator skill and an attacker skill. Both deployable. Both reusable. Both versioned. The PRD reviewer isn't something you retype every time; it's a file you invoke, the same way you invoke the PRD creator.

That's what makes it portable. Once the attacker is a skill and not a one-off message, the same primitive shows up at every level of the stack. L2 uses it as the verifier on a single artifact. The worker loops at L4 invoke it as a gate before anything ships. Discovery loops at L5 use it to pressure-test what they surface. Governance at L6 uses it to audit the fleet's output. One small shape, reused all the way up.

This is the building block the rest of the class compounds on. When we get to the three-role split a few segments from now, the role that attacks the work has a name, the Reflector, and this is exactly what it is. When we get to the bug triage loop, the fix-verification step is this same attacker pointed at a patch. Build the pair once. You'll reach for it constantly.

Three concrete versions of the pair.

**PRD creator and PRD attacker.** The creator writes the spec. The attacker hunts miracle steps, the line that says "and then the system reconciles the two ledgers" as if that's one step instead of a project. It hunts vague assumptions and untested invariants. It defaults to refuted.

**Code writer and code reviewer.** The writer ships the diff. The reviewer's job isn't "is this clean," it's "what shipped versus what was specced." It flags the silent scope drift, the requirement that quietly didn't get built, the edge case the writer waved past.

**Copy writer and AI-slop hunter.** The writer drafts. The attacker's only job is to cut the model's own tells, the "in today's fast-paced world," the tricolon, the em dash, the throat-clearing. The thing that wrote the slop is the worst judge of it. A fresh context told to hunt slop is brutal at it.

[IMAGE: dark canvas, three horizontal pairs stacked vertically, each pair a "creator" box and an "attacker" box with an arrow between, labeled PRD / miracle steps, code / scope drift, copy / slop tells]
![[images/adversarial-reviewer-skill/three-creator-attacker-pairs.png]]

---

## One real-world variant: many attackers, then a synthesizer

You can push this further, and people in the wild already are.

Nolan Lawson runs a code-review skill that doesn't use one attacker. It fans out to several, a Claude subagent, Codex, and a separate bug bot, each finding bugs in the same PR ranked critical to low. Then a synthesizer reads all their findings, rules out false positives, and writes one report. His reported false-positive rate is near zero, and the rule he's careful about is that the main agent does no original research until every reviewer has come back, so it isn't biased by whoever returned first.
Source: https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/

Two things to steal from that. First, you can split the attacker by lens instead of by model: an architect reviewer, a test-engineer reviewer, a security reviewer, each in its own fresh window, then a synthesizer. Second, clearing context between sweeps measurably helps, which is just the second lever again. Each reviewer that starts cold has nothing to defend.

The framing underneath all of it: the model's first output is a first draft. The real work starts at review. The attacker skill is how you make that review independent instead of imaginary.

---

## Aim the sycophancy, don't fight it

Step back at the eagerness to please for a second, because there's a sharper reframe hiding in it.

We've been treating the model's urge to agree as a bug to suppress. It isn't. It's a force you can aim. Set the creator and the attacker opposing incentives and the same sycophancy that made self-review useless becomes the engine that makes adversarial review work.

sysls lays out the cleanest version of this as a three-agent scoring scheme.
Source: https://x.com/systematicls/status/2028814227004395561

The **bug-finder** is rewarded for finds: +1 for a low-impact bug, +5 for moderate, +10 for critical. Because it wants to please, it eagerly returns the *superset* of every possible bug, including ones it half-invents. You let it over-report on purpose.

The **adversarial agent** is paid to knock those bugs down. For every bug it can disprove it earns that bug's score, but it loses *twice* the score when it's wrong. So it attacks hard but with caution, and what survives is the *subset* of bugs that are probably real.

The **referee** adjudicates the two. You tell it, as a deliberate lie, that the human holds the ground truth: +1 when it scores correctly, -1 when it doesn't. Then you spot-check a few yourself. sysls calls the result "frighteningly high fidelity, nearly flawless."

Notice the shape. The +10/-2x asymmetry is the scoring-scheme version of the same asymmetric prompt you've been writing all along. You're not begging the model to be honest. You're making honesty the higher-scoring move.

One detail that cuts against your instinct. When you spin up the bug-finder, don't prompt it "find me a bug." That makes the model engineer a bug to please you, the same failure as self-review wearing a different hat. Use a neutral prompt: "follow the logic of each component and report all findings." Let the incentive structure, not the prompt, decide what counts as a bug.

---

## Demo

Two skills, side by side, and one planted flaw.

1. Show the two skill files open next to each other. On the left, `prd-creator`, a normal system prompt: "you write clear, complete product requirement documents." On the right, `prd-attacker`, and read its system prompt out loud so the asymmetry is undeniable: "your job is to refute this PRD. Default to refuted. Hunt for miracle steps, vague assumptions, and untested invariants. Do not be agreeable." Same model behind both. The only difference is the job.

2. Invoke the creator. It writes a PRD for a feature, and I've nudged it to leave one miracle step in: a single bullet that says "the service automatically migrates existing user data to the new schema." One line. Sounds reasonable. It's a month of work pretending to be a checkbox.

3. Invoke the attacker as a fresh subagent, not a follow-up turn. Hand it the PRD. Watch it come back with a structured refutation. The top finding: "miracle step. 'Automatically migrates existing user data' is unspecified and likely the hardest part of this project. No mention of backfill strategy, rollback, or downtime. Refuted pending a migration plan."

4. Run the control so the contrast is visible. Ask the *creator's own context* "is this PRD good?" Watch it say yes. Same model. Same PRD. The fresh window plus the refute prompt is the only thing that caught the landmine.

5. Fix upstream. Feed the attacker's findings back to the creator. It expands the one bullet into a real migration section. Re-run the attacker. This time it returns "no airtight objection found." That's your exit condition.

Total demo: about four minutes. The point is that the two skills are files you keep, not a conversation you had once, and the planted flaw only dies because the reviewer was given a fresh context and the opposite job.

---

## Key Insight

> You don't need a smarter model to catch your model's mistakes. You need the same model, in a fresh window, told its job is to refute. Same weights, opposite job. That's the cheapest reviewer you'll ever build, and the most reusable.

---

## Where we go next

You now have the L2 primitive the whole class leans on. A creator paired with an attacker, stored as two skills, run in series, fresh context plus an asymmetric prompt.

Next we step back and look at how to architect a loop deliberately, where these creator-attacker pairs sit inside it, and how the pieces wire together before we start running them continuously.

See you in the next one.
