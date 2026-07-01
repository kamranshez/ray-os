---
title: Build Faster by Coding Slower
videoId: 0rMG-3iiilc
url: https://www.youtube.com/watch?v=0rMG-3iiilc
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1. Pour hours into the spec so the agent one-shots the entire build.** The whole video is one thesis: iterate at the design altitude until the ticket is perfect, then never touch the implementation loop, because a 200-line spec becomes thousands of lines of code and one wrong line compounds.
VERDICT: 🔗 next-step video available (complements build-it-twice).

**Spine 2. Give the model options, not orders, because it is sycophantic.** Telling a model "do X" makes it commit to your possibly-wrong X; asking "give me the tradeoffs" keeps the thinking with you and stops your unexamined mistake from compounding downstream.
VERDICT: 🔗 next-step video available (complements steering-distributions).

**Spine 3. Non-deterministic systems need a different kind of testing.** Agents and LLMs break the "same input, same output" assumption unit tests rely on, so you need scenario-sliced named metrics, quorum runners, and cases pulled from prod, not boolean asserts.
VERDICT: ❌ net-new video available.

---

# Summary

Vaibhav (BAML) and Dex (HumanLayer) build a testing language feature live, showing how heavy upfront design lets them one-shot thousands of lines of implementation cleanly.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1. Perfect the spec, one-shot the build

The claim: the more time you invest in the design discussion and ticket, the less you touch the implementation, up to the point where a 10,000-line PR just works with zero manual loop. It is non-obvious because the default reaction to cheap tokens is "typing is free, so prompt and iterate in the loop." Vaibhav argues the opposite: iterate at the design altitude, then auto-advance the build untouched. The mechanism is a compounding chain. Because the model now writes code faster than a human can read it, you cannot steer mid-implementation; because you cannot steer there, any ambiguity in the spec drifts into uncontrolled directions; therefore the only place leverage exists is the spec itself, where "200 lines of spec that turn into thousands of lines of code" means "the impact of one wrong line is pretty significant." His move is a fresh rewrite (ticket two) that captures every design decision "as if we had all this from day one," killing the two-truths drift that makes a model pick the wrong branch. This generalizes cleanly to contract or API design, where a cheap upstream ambiguity is catastrophic downstream. Where it goes wrong: it assumes the domain is well understood (his co-founder did heavy legwork first); for genuinely novel features you cannot yet write the spec, and a throwaway prototype teaches you more.

## Spine 2. Options, not orders

The claim: present your ideas to the model as options with tradeoffs, never as decisions, because models are "extremely sycophantic" and will commit to whatever you assert. It is non-obvious because directive prompting feels efficient, yet it quietly poisons the output. The mechanism: the model reasonably assumes that if you tell it something, you know something it does not, so it stops evaluating and follows you; that means your unexamined wrong idea propagates through every downstream token and "whatever mistakes you have are going to compound really fast." The counter-move is to ask "give me a bunch of options" and to "do not outsource the thinking," using the model's dumped high-level reasoning as a surface you do "brain surgery" on before dropping a level. This is exactly why "junior engineers sometimes struggle with these models," because they assert instead of suggesting softly. It generalizes to managing junior humans and to any advisory LLM (legal, medical) where sycophancy manufactures false confidence. Where it goes wrong: too soft and the model dithers in indecision, and there is genuine value in letting it brainstorm patterns it pulls from your codebase, so the goal is steering the conversation, not silencing the model.

## Spine 3. Testing systems that never answer the same way twice

The claim: any non-deterministic system (an LLM, math.random, an uncontrolled network call) needs testing built on scenario-sliced named metrics, quorum runs, and prod-sourced cases, not boolean asserts on static data. It is non-obvious because engineers port deterministic unit-test habits straight onto agents. The mechanism: because the output is a distribution rather than a value, a single pass/fail is noise, and a naive "95% pass" target invites a degenerate classifier that "always returns false" and games the metric; therefore you need aggregate metrics sliced by product scenario (glasses vs no-glasses), each case run N times under a quorum rule ("run it nine times, require at least seven pass"), with cases sampled from real prod logs so you are measuring a moving target: your agent against real user behavior. A parallel move applies to code review, where the model is sycophantic ("if you ask the model if the code is good... oh yeah, it's great"), so you score via boolean classifiers plus deterministic code, asking "is it X" rather than "is it good." This generalizes to Face ID and any classical ML classifier (their worked example) and to fraud detection. Where it goes wrong: infinite scenario slicing (the OLAP-cube trap), metrics that get gamed, and the fact that retrofitting this late is very hard.

---

# 🎬 Proposed ACS videos

## 1. Perfect the Spec, One-Shot the Build

- HOOK: The engineers shipping 10,000-line PRs are the ones who spend five hours before writing a single line of implementation.
- THE PROMISE: For builders stuck babysitting the implementation loop; after this you front-load design so the agent one-shots the whole build and you only read.
- THE SHAPE: (1) Show the compounding-error math: a 200-line spec becomes thousands of lines, so one wrong line is thousands of wrong lines. (2) Walk research to design-discussion to ticket. (3) Rewrite a clean "ticket two" as if you knew everything day one. (4) Auto-advance the implementation untouched. (5) Reset, do not refactor: nuke the branch and restart from a better ticket when it drifts.
- SPINE: 1.
- SLOT: Techniques > new chapter "Design-First Delivery" (sits beside "The First Build Is a Prototype").
- RELATIONSHIP: 🔗 complements "The Cheapest Spec Is a Finished Build" (build-it-twice), which teaches building a throwaway prototype to learn an uncertain feature, then rebuilding from the learnings. This video is the opposite regime: when the domain is already understood, you pour the effort into the spec and skip the loop entirely. Ray should not re-teach the throwaway-prototype idea; the new material is the spec-first, auto-advance, ticket-two workflow.
- PROOF TO REUSE: the ~16,000-line closures feature shipped in about 36 hours; "any one mistake in this ticket is just compounding mistakes I have to deal with"; the ticket-two rewrite; the live 8pm to 11:22pm design timeline.

## 2. Testing Systems That Never Answer the Same Way Twice

- HOOK: Your unit tests assume the same input gives the same output. Your agent breaks that assumption on every single run.
- THE PROMISE: For anyone shipping an LLM or agent feature; after this you can build an eval harness that actually tells you whether to ship.
- THE SHAPE: (1) Why pass/fail breaks for non-deterministic systems, using the Face ID example. (2) Scenario slicing plus named aggregate metrics. (3) Quorum runners: run N times, pass if M succeed. (4) Pull test cases dynamically from prod logs. (5) Sycophancy-proof scoring: boolean classifiers plus deterministic code, asking "what is wrong" not "is it good."
- SPINE: 3.
- SLOT: Techniques > new "Evals for Agents" chapter (net-new area).
- RELATIONSHIP: ❌ net-new. ACS has no video on testing or evals for non-deterministic systems. The closest items ("closing-the-loop", backlog "subagent-verification-loops") are about agents self-correcting inside a run, not about measuring output quality across many runs to decide shippability.
- PROOF TO REUSE: Face ID's asymmetric success (a false positive is far worse than a false negative); glasses vs no-glasses scenario slicing; "quorum nine seven" (run nine, require seven); "take all the logs from the last month and run 1% of them as test cases"; the "ask if code is bad, not good" review insight.

## 3. Give the Model Options, Not Orders

- HOOK: Tell a sycophantic model "do X" and it stops thinking. Ask it "which of these" and it starts.
- THE PROMISE: For anyone who design-discusses with an agent; after this you steer the conversation without accidentally locking in your own wrong idea.
- THE SHAPE: (1) The sycophancy trap: the model treats your assertion as a high-confidence prior. (2) Soft-suggest vs command, and flagging "this is only a suggestion." (3) Ask for options and tradeoffs, then do brain surgery on the model's dumped reasoning before dropping a level. (4) Why juniors struggle: they assert. (5) Do not outsource the thinking, but do let it brainstorm patterns from your codebase.
- SPINE: 2.
- SLOT: Prompt Engineering > next to "01-steering-distributions".
- RELATIONSHIP: 🔗 complements "Steering Distributions" (01-steering-distributions, scripted), which teaches steering the model's output distribution in general. This video is the specific, high-stakes failure mode (sycophancy) and the concrete counter-move (options, not orders) applied to real design discussions. Ray should not re-teach distribution steering from scratch; this adds the sycophancy diagnosis and the options pattern.
- PROOF TO REUSE: "the thing you have to learn about these models is they're extremely sycophantic"; "do not outsource the thinking... you're rolling the dice"; the junior-engineer compounding point; the "brain surgery on markdown docs" quote.

### Also film-able (not deep-dived)

- **Give the agent primary sources: local checkouts of language and dependency repos.** Vaibhav keeps reference implementations of Go, Python, TypeScript, and Rust checked out so the agent researches how each actually handles a feature from source, because "you can't rely on web search to find this information." Net-new, niche. Slot: Context Engineering or a Claude Code research technique.
- **Parallel agents with one primary task (Theory of Constraints, applied tactically).** Keep one primary plus one or two secondaries; when the primary unblocks, drop the secondary and return to it, optimizing cycle time and lead time over utilization. Mostly ✅ covered by the "Start Here: The Shifting Bottleneck" video, which already teaches Goldratt and The Goal; this is the tactical parallel-agent application of that same idea, worth at most a beat inside another video.

---

# 📚 Full wisdom (reference)

## SUMMARY

Vaibhav (BAML) and Dex (HumanLayer) build a testing language feature live, showing how heavy upfront design lets them one-shot thousands of lines of implementation cleanly.

## IDEAS

- Spend hours perfecting the design ticket so the entire implementation phase one-shots without touching the loop.
- One wrong line in a 200-line spec compounds into thousands of wrong lines of generated code.
- After the design discussion, rewrite a fresh ticket as if you knew everything from day one.
- Markdown design docs let the model dump its thinking so you do brain surgery before coding.
- Ask the model for options and tradeoffs, never a single decision, because it commits to yours.
- Models are extremely sycophantic; assert a wrong idea and every downstream mistake compounds from it fast.
- Suggest softly; if it is a suggestion not a command, tell the model that fact explicitly.
- Test non-deterministic systems with product-oriented scenarios, slicing cases across many dimensions like glasses versus no glasses.
- Use named aggregation metrics, not boolean asserts, so soft checks collect signal without failing individual tests.
- A quorum runner runs a test N times and passes if at least M runs succeed.
- Pull real test cases dynamically from production logs, sampling one percent of last month's live traffic.
- Ask the model what is wrong with code, never whether it is good; sycophancy ruins reviews.
- Build boolean classifiers, then attach deterministic code to score good or bad from those raw flags.
- Keep local checkouts of major programming languages so the agent researches source instead of web search.
- Check code for soundness, not correctness, because verifying full correctness demands far too much engineering engagement.
- Read the generated code and ticket while the model writes, so responses take under a minute.
- Run one primary task and one or two secondaries; return to primary whenever it becomes unblocked.
- When code is unrecoverable, nuke the branch and restart from scratch with a better fresh ticket.
- Build the most foundational layer first, end to end, before adding CLI or editor extension features.

## INSIGHTS

- The scarce resource is not typing speed but design correctness; the spec is the true bottleneck.
- Two-truth ambiguity in a spec lets the model drift down any path you cannot steer back.
- Because models weight recent tokens most, the middle of long context matters less than people fear.
- Serializing every decision to disk buys resumability but halves your speed on heavy live design work.
- Larger context lets you be lazy, but you must reiterate what matters in the recent messages.
- Non-deterministic systems need testing built in from the start; retrofitting evals from first principles is hard.
- A test on sampled prod data measures a moving target: your agents against real user behavior.
- Optimizing a station that is not the bottleneck adds work in progress and hurts overall throughput.
- Junior engineers suffer with models because they assert instead of offering their ideas as tentative suggestions.
- Deep code-base knowledge lets a human navigate design tradeoffs the model cannot yet reason about alone.
- Cycle time on one task beats parallel progress; finishing work in progress optimizes end-to-end lead time.

## QUOTES

- "the goal is to just show how we one shot everything." (Vaibhav)
- "I've shipped like multiple 10,000 plus line PRs without by being able to do this." (Vaibhav)
- "the thing you have to learn about these models is they're extremely sycophantic." (Vaibhav)
- "do not outsource the thinking. Um if you let the model make decisions, uh you're rolling the dice." (Dex)
- "these markdown docs are basically an opportunity to have the model dump out everything that it's thinking so that you can do brain surgery on it." (Dex)
- "any one mistake in this ticket is just compounding mistakes I have to deal with earlier." (Vaibhav)
- "it's faster to restart from scratch with a good basis than it is to incrementally fix certain things." (Dex)
- "you don't have to check if it's correct, you check for soundness because correctness requires too much work." (Vaibhav)
- "whatever the slowest thing in the workflow is, that is your constraint." (Dex)
- "This is what we call vertical slices or like tracer bullets." (Dex)
- "Typing code is is too 2024." (Vaibhav)

## HABITS

- He reads the entire design doc and ticket in real time, disappearing for twenty silent minutes.
- He plays League of Legends while two background agents run arbitrary long research tasks in parallel.
- He kicks off the next phase speculatively before confirming the current design document is fully correct.
- He removes uncertain sections from a ticket so they do not enter as pre-baked model decisions.
- He has Claude summarize CodeRabbit's fifty review comments instead of reading each auto-generated comment himself manually.
- He downloads reference implementations of Go, Python, TypeScript, Rust to research how each language handles features.
- He auto-advances tasks through research and design, only pausing to read and verify the final design.
- He copies a finished task's spec into a new task and blindly auto-advances the whole pipeline.
- He measures himself only by whether he ships to main and how large landed tasks are.

## FACTS

- Vaibhav's team shipped a closures feature of roughly 16,000 lines of code using this design-first workflow.
- Face ID launched around 2017 using classical machine learning, before transformers existed in any production systems.
- Eliyahu Goldratt's 1984 novel The Goal sold over ten million copies teaching the Theory of Constraints.
- The Goal was reportedly written as content marketing to sell supply-chain optimization software that later died.
- Vaibhav implemented the entire closures feature in about 36 hours, including two full nights of sleep.
- Google's internal policy discourages before-all and before-each hooks, preferring extremely local, fully self-contained test cases everywhere.
- Rust has no before-each or after-all constructs; shared setup is done with plain functions and macros.
- Vaibhav's largest single continuous context session reached roughly 800,000 tokens without any manual compaction steps taken.
- The whole testing feature design session ran live from 8pm past 11:22pm, roughly three and half hours.

## REFERENCES

BAML (the programming language being built), HumanLayer, Riptide (HumanLayer's agentic-engineering tool), the RPI (Research, Plan, Implement) workflow, CodeRabbit (auto code reviewer), Claude and Opus 4.5, Codex, The Goal by Eliyahu Goldratt, Zig (testing-ergonomics inspiration), Go (testing philosophy and package/namespace semantics), Mitchell Hashimoto (Go testing talk), Face ID, OLAP cubes, JEPA-style optimization, YC / the SF unconference, the "AI That Works" podcast, the "No Vibes Allowed" episode format, the "JP Morgan emails" episode, League of Legends, yarn (context-extension technique), auto-research harnesses, and the CLAUDE.md "important if" XML-block adherence pattern.

## ONE-SENTENCE TAKEAWAY

Front-load design until the spec is perfect, then let the agent one-shot the entire implementation.

## RECOMMENDATIONS

- Pour hours into your ticket and design discussion before letting the agent implement anything at all.
- After designing, have the agent rewrite a clean ticket capturing every decision as prior settled knowledge.
- Phrase your inputs as options to weigh, so the model does not blindly commit to them.
- When reviewing with a model, ask what is wrong, not whether the code is any good.
- Download source repos of the languages you use so agents research primary sources, not web blogs.
- Run tests as scenarios with named metrics and quorum runners, sampling real cases from production logs.
- Keep one primary task; when it unblocks, drop the secondary task and return straight to it.
- If a build becomes unrecoverable, delete the branch and restart from an improved, fresh clean ticket.
- Build the foundational layer end to end first before designing CLIs, extensions, or telemetry side layers.
- Read generated code and tickets while they stream, so you can steer within one single minute.
