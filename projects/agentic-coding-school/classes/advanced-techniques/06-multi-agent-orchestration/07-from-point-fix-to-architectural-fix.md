---
duration: "12-16 min"
batch: 1
order: 7
batch_name: "Multi-Agent Orchestration"
class: "advanced-techniques"
chapter: "Multi-Agent Orchestration"
status: "scripted"
aliases: [from-point-fix-to-architectural-fix]
---

The harness found the bug. It wrote the test that proves the bug. A verifier confirmed the bug is real. A patching agent fixed the bug and built the project and watched the crash go away.

And it still left the entire class of that bug alive in your codebase.

That gap is what this video is about. The pipeline you already built ranks files, fans out agents, perturbs their starting points, and verifies their findings. It is very good at producing one confirmed fix at a time. The move almost nobody automates is the one that happens after a fix is confirmed: take that single bug, recognise the class it belongs to, find every other place the class lives, and ship one architecturally clean fix that closes all of them at once.

Point fixes treat a bug as an event. The next step treats it as evidence.

---

## Where this came from

This is the unsolved frontier Brian Grinstead pointed at on How I AI. He is a distinguished engineer at Mozilla, and his team ran an agentic security harness against Firefox, tens of millions of lines of code, and shipped close to 500 security fixes in a single month.

The harness worked. But watch what the human reviewers kept writing on the fixes:

> "Yep, this looks like a real issue, the fix looks good, but actually we should check in a few other places."
> Brian Grinstead, How I AI

That sentence is the whole video. The agent landed a correct patch. A world-class browser engineer looked at it and immediately knew the same mistake was sitting in three other files. The agent never looked, because nobody told it the bug was a symptom.

Claire Vo, hosting, had hit the exact same wall with a commercial security tool on her own much smaller codebase:

> "It will get laser focused on the specific patch. It'll say, for this bug, this is the patch. But it doesn't do the next level of, go categorically find similar issues across the codebase and then come up with an architecturally clean global fix for this class."
> Claire Vo, How I AI

Two people, two codebases four orders of magnitude apart in size, same complaint. The tooling stops at the leaf.

[IMAGE: dark chalkboard, a single bug fixed with a green check on a leaf node, while three identical red bug nodes sit untouched elsewhere on the same tree, faded]

![[point-fix-leaves-class-alive-1.png]]
![[point-fix-leaves-class-alive-2.png]]
![[point-fix-leaves-class-alive-3.png]]
![[point-fix-leaves-class-alive-4.png]]
![[point-fix-leaves-class-alive-5.png]]

---

## The two kinds of fix

Get the distinction crisp, because everything else hangs off it.

A **local fix** answers one question: this line is wrong, here is the corrected line.

A **global fix** answers a bigger one: this line is wrong because the codebase repeats a pattern, here is the structural change that makes the pattern impossible, here is every place it occurred, and here are the issues that closing it resolves.

Today's harnesses, and frankly most coding agents run in headless mode, are tuned for the first. They converge hard on the patch and stop. They treat each bug as a leaf, never as a symptom of a missing invariant.

The difference is not effort. It is altitude. A point fix works at the bug site. A global fix climbs up the stack to the thing that allowed the bug site to exist, and changes that instead.

[IMAGE: dark background, two side-by-side panels. Left panel "Local fix" shows a single line edited at the bottom of a stack. Right panel "Global fix" shows an edit near the top of the stack with arrows cascading down to many bug sites that all disappear]

![[local-fix-vs-global-fix-1.png]]
![[local-fix-vs-global-fix-2.png]]
![[local-fix-vs-global-fix-3.png]]
![[local-fix-vs-global-fix-4.png]]
![[local-fix-vs-global-fix-5.png]]

---

## Why your harness defaults to local

This is not the model being lazy. It is the shape of the loop rewarding the leaf. A point fix wins on all three axes that a harness optimises for:

**It is cheap to verify.** One diff, one test case, one crash that stops crashing. Your AddressSanitizer build gives a clean yes or no.

**It has a bounded blast radius.** One file, a few lines. Reviewers trust it on sight.

**It is trivially scoped.** The bug report is the spec. The agent does not have to decide what the task even is.

A global fix is the opposite on every one. It is expensive to verify because it touches many files. Its blast radius is wide, so reviewers slow down. And it is unscoped, because turning one bug into a class is a judgement call the bug report does not make for you.

So every incentive in the loop pushes toward the leaf. And that is the trap. You ship 500 leaf fixes, the literal number from the episode, and the class of bug is still alive. One instance is quieter. You mowed the lawn. You did not pull the root.

[IMAGE: dark chalkboard, three labelled scales all tipped toward "Local": cheap to verify vs expensive, bounded blast radius vs wide, trivially scoped vs judgement call]

![[why-harness-defaults-local-1.png]]
![[why-harness-defaults-local-2.png]]
![[why-harness-defaults-local-3.png]]
![[why-harness-defaults-local-4.png]]
![[why-harness-defaults-local-5.png]]

---

## The four moves that take a fix global

The reason this still needs an engineer who knows the codebase is that going global is four cognitive moves the point-fix loop never makes. Each one is a separate agent step you can bolt on after a confirmed finding.

**1. Generalise.** Abstract the single bug into a class signature. Not "line 412 is wrong." Instead: "unchecked length before a memcpy." The class, not the instance.

**2. Canvas.** Search the whole repository for that signature, including the variants that do not look identical to the original. This is the hard one. It is semantic, not grep. The same mistake wears different clothes in different files.

**3. Re-architect.** Design the change that makes the class unrepresentable. A safe wrapper type. An invariant enforced at a boundary. A lint that fails the build. An API that deletes the footgun entirely. The fix moves up the stack, away from the bug site.

**4. Reconcile.** Map the new architecture back onto every site you found, and close the related issues as a single unit.

Here is the part that makes it real engineering instead of a bigger patch: a true global fix often does not touch the original bug line at all. It changes the thing that allowed the line to exist. You delete the category, not the example.

[IMAGE: dark background, a horizontal flow of four stages labelled Generalise, Canvas, Re-architect, Reconcile. Generalise shows one bug becoming a class label, Canvas shows the label matching many scattered files, Re-architect shows a single boundary drawn above them, Reconcile shows all the files turning green at once]

![[four-moves-point-to-global-1.png]]
![[four-moves-point-to-global-2.png]]
![[four-moves-point-to-global-3.png]]
![[four-moves-point-to-global-4.png]]
![[four-moves-point-to-global-5.png]]

---

## The harness change: promotion, not point-fix

You already have the pipeline. Rank the files, fan out agents in parallel, perturb their starting points, verify every finding. We covered that whole machine in the four-step pipeline video, so I am not rebuilding it here.

The change is one new stage, and one new rule.

The rule: a confirmed point fix does not ship immediately. It gets **promoted** into a class investigation first.

The stage sits right after your verifier approves a finding:

1. **Verified finding** comes out of the existing loop.
2. **Generalise.** An agent writes the class signature. What invariant was violated?
3. **Canvas.** Fan out a search across the repo for that signature. Semantic, not just text. Out comes a list of candidate sites.
4. **Cluster.** Dedup and group the candidates. Is this one bug, or forty?
5. **Architect.** An agent proposes the structural fix. The prompt matters here: the point fix is the fallback, not the goal.
6. **Verify the cluster.** Run the same verifier subagent you already trust, now against every site the new architecture touches.
7. **Ship one change** that closes the whole cluster of issues together.

Notice the design choice hiding in step 4. You do not go global on everything. A class with one member is just a point fix wearing a costume. You promote the high-yield classes, many sites, high accessibility, and you let the cheap singletons stay local on purpose. That is the same prioritisation logic the LLM judge applied to files at the start of the pipeline, now applied one level up, to classes of bug instead of files.

The judge ranks where to look. Promotion ranks what is worth eliminating wholesale.

[IMAGE: dark chalkboard, the existing four-step pipeline shown compressed on the left feeding into a new vertical "Promote" column: Generalise, Canvas, Cluster, Architect, Verify cluster, Ship one. A small singleton bug branches off early with a label "stays local"]

![[promotion-stage-after-verifier-1.png]]
![[promotion-stage-after-verifier-2.png]]
![[promotion-stage-after-verifier-3.png]]
![[promotion-stage-after-verifier-4.png]]
![[promotion-stage-after-verifier-5.png]]

---

## This is not a security technique

The security framing is just where the blast radius of missing the global fix is scariest. The pattern underneath is class-recognition plus structural fix, and it works anywhere you have a large codebase full of the same mistake repeated.

**Tech debt.** "Fix tech debt" is unscoped and useless. "Find every place we hand-roll retry logic and replace it with one policy" is a global fix with a clear class signature.

**Performance.** One slow query is a point fix. "Every N plus one in this access pattern" is the class. You give the agent a benchmark, tell it to drive the number down, and promote the winning optimisation across every site that shares the shape.

**Design and conversion.** Every form missing inline validation. Every component that does not handle the empty state. Claire made exactly this leap on the show, pointing at product managers and designers scoring components and applying one best-practice fix across the class.

The promote-then-architect loop does not care what domain it runs in. Security just has the crispest pass-fail signal, which is why it got there first.

[IMAGE: dark background, one central loop labelled "Generalise, Canvas, Architect, Verify" with four arrows pointing out to four domain cards: Security, Tech Debt, Performance, Design, each showing the same loop shape in miniature]

![[same-loop-many-domains-1.png]]
![[same-loop-many-domains-2.png]]
![[same-loop-many-domains-3.png]]
![[same-loop-many-domains-4.png]]
![[same-loop-many-domains-5.png]]

---

## Two ways this goes wrong

Going global is not free, and done badly it is worse than 500 boring patches. Two failure modes to design against.

**Over-abstraction.** A global fix that invents a clever abstraction to unify forty sites can be worse than forty point fixes if it couples things that should have stayed independent. The architect stage needs a skeptic built into it: is this genuinely one class, or am I forcing three different classes into one bad shape because they rhyme? Make a verifier argue the other side before you commit to the abstraction.

**Blast radius against your verification budget.** This is Brian's cost point, and it bites hardest here. A point fix is one diff to review. A global fix might touch forty files and need its verifier to run on each. AI fixes feel limitless and free right up until a human has to review, verify, and ship them, and that time is not free.

> "You cannot go completely prioritisation free, especially when you're looking at the kinds of fixes you need to verify and they're taking 14 loops to even get to a yes or no."
> Claire Vo, How I AI

So going global is only worth it when the sites you close, times the cost of each future incident, beats the cost of one big risky review. Cheap classes stay local. Expensive, dangerous classes get promoted. The economics are part of the design, not an afterthought.

[IMAGE: dark chalkboard, a balance scale. Left pan "Sites closed x cost per future incident" stacked with many bug icons. Right pan "Cost of one wide review" with a clock and a magnifying glass. A dashed threshold line labelled "promote only above this"]

![[promote-economics-threshold-1.png]]
![[promote-economics-threshold-2.png]]
![[promote-economics-threshold-3.png]]
![[promote-economics-threshold-4.png]]
![[promote-economics-threshold-5.png]]

---

## Demo plan

1. Run the existing pipeline against a real codebase until the verifier confirms one bug. Show the point fix it would normally ship.
2. Promote it. Feed the confirmed finding into a generalise agent. Watch it write the class signature, not the line fix.
3. Canvas. Fan out subagents across the repo searching for that signature semantically. Surface the other sites that the original run never touched. Show the count: one bug became, say, nine.
4. Cluster and architect. Have an agent propose the structural fix that makes the whole class unrepresentable, and contrast it against the nine separate point fixes it replaces.
5. Run the skeptic. A second agent argues the abstraction is wrong before you accept it.
6. Verify the cluster with the same verifier subagent, now run against all nine sites, and show the single change that closes all nine issues.
7. Point the identical promote loop at a non-security class. Take one N plus one query, generalise it, canvas the repo, and watch it find the rest of the pattern in front of the camera.

---

## Key Insight

> A point fix treats a bug as an event. A global fix treats it as evidence of a missing invariant. The next step beyond a good harness is the stage that, on every confirmed finding, asks "what invariant would have prevented this, and where else is it missing?" before it asks "what is the patch?"

---

The harness that finds and fixes one bug at a time is already built and already working. The asymmetry left on the table is not a better model. It is the promote stage: the discipline of climbing from the leaf to the root, eliminating the class instead of the instance, and shipping one architecturally clean change that closes every issue the class was hiding.

When your agent lands a fix, the next question is not "what's the next bug." It is "what was this one an example of, and where else does it live."

---

## Sources

- How I AI with Claire Vo, "Claude Mythos for security testing: a Firefox engineer's playbook" with Brian Grinstead (Mozilla), June 22, 2026.
- Companion pipeline video in this chapter: [[coverage-through-stochastic-starting-points]].
