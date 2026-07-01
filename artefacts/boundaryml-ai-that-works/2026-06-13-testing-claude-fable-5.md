---
title: "Testing Claude Fable 5: Why New AI Models Rarely Change Everything"
videoId: hTkmSVuDMPg
url: https://www.youtube.com/watch?v=hTkmSVuDMPg
channel: BoundaryML / AI That Works
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1 (the how): Test a new model on your hardest LIVE problem, and judge comprehension before completion.** Before asking "can it solve it," ask it to restate your architecture and name a detail you missed. That coherence check is the cheap signal that predicts everything else.
VERDICT: 🔗 next-step video available (complements the filmed "goal-in-strategy-out").

**Spine 2 (the why): A new model generation is worth one or two more simultaneous constraints, not a categorical leap.** "Most model releases are more hyped than the value they produce." The gain is marginal per task but compounds through corrections avoided.
VERDICT: ❌ net-new video available.

**Spine 3 (the artifact): Keep a private text file of git SHAs plus prompts plus answer keys for problems that once took you a week, and replay it on every release.** Your own regression suite that no lab can overfit to.
VERDICT: ❌ net-new video available.

---

## Summary + counts

Dex and Vibb stress-test the new Fable 5 model live on their hardest real problems, concluding most releases underwhelm their hype rather than transforming work.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: Comprehension before completion

The claim: when a new model ships, test comprehension before completion. Hand it your live architecture, ask it to restate the design and surface a detail you missed, and grade THAT first. Why it is non-obvious: everyone reaches for completion benchmarks (can it one-shot X, did it finally beat Pokemon). Vibb inverts it. As he says, "the first leverage I'm looking for is not can it do the work"; it is whether the model describes the problem back "in a way that's very coherent and picks out one or two key details that I haven't thought about before." Why it is true: you already hold deep context on a live problem, so you can grade a restatement in seconds, whereas grading a full solution to a novel problem is slow and you may not even know the right answer. Comprehension is also upstream of completion: a model that cannot restate your constraints will never satisfy them, so the cheap signal predicts the expensive one. It generalizes to onboarding a human engineer, where you ask the new hire to explain the system back before handing over the ticket. How it goes wrong: on an OLD problem you may not remember enough to grade the restatement, and a fluent but wrong summary can slip past a quick scan of a nuanced doc.

### Spine 2: Why new models rarely change everything

The claim: a new generation is worth roughly one or two more simultaneous constraints handled, not a categorical leap. As Vibb concludes, "most model releases are hype." Why it is non-obvious: marketing frames each release around "breakthrough discoveries," so people expect a step change and feel let down or fool themselves into seeing one. Why it is true: designing a real solution means "being able to attend to tens or hundreds of constraints" at once; if the old model holds ten and the new one holds fifteen, that is invisible on any single task yet compounds hard, because Dex notes cutting corrections "from five to two out of a hundred things the model could get right" doubles your effectiveness. Your correction overhead, not the model's raw output, is the true bottleneck. It generalizes to any tool upgrade judged by errors-avoided rather than headline speed. The demo writes itself: the model failed to proactively flag that spawning thousands of threads makes a U32 thread ID collide (you need U64), "exactly the subtle thing I would have expected a really good model to pick out." How it goes wrong: the yardstick is subjective, and on a problem the previous model already nailed you learn nothing, which is why you must test only your hardest problems.

### Spine 3: Build your own private model benchmark

The claim: keep a private text file of git commit SHAs paired with the prompt and the known answer for problems that once took a week and that past models failed, then replay it on every release. Why it is non-obvious: most people test new models on fresh prompts, which tangles the model's skill with their own recall and leaves no baseline. Why it is true: a solved-and-logged problem is a fixed reference. You check out the exact SHA before the fix, replay the saved prompt, and compare against the answer key you already own, so any improvement is attributable purely to the model. Dex: "if I check out this repo to this Shaw and give it this prompt that is a problem that took me a week to solve," and over time "you accumulate your own little collection of mini bench" that no lab can overfit to. It generalizes to ordinary software regression testing: pin the input, pin the expected output, rerun on every change. The 3am problems are ideal because the bad pattern is "burned into your brain," so grading is instant. How it goes wrong: old problems fade from memory, so log the symptoms and root cause beside the SHA, and a tiny niche bench must complement live testing, never replace it.

---

## 🎬 Proposed ACS videos

### 1. The First Thing to Do When a New Model Drops
- HOOK: Everyone asks "can the new model solve it?" The pros ask something cheaper and smarter first.
- THE PROMISE: For anyone who upgrades models on hype, a 10-minute protocol to judge a release on work you already understand, before you trust any leaderboard.
- THE SHAPE: (1) Why benchmarks and one-shots mislead. (2) Grab your hardest IN-PROGRESS task, the one you hold max context on. (3) Ask the model to restate the architecture and name what you missed. (4) Grade coherence plus one novel detail as the "solid win" bar. (5) The human-onboarding analogy.
- SPINE: 1.
- SLOT: Techniques class > new "Working With Model Releases" chapter (or Claude Code > model selection).
- RELATIONSHIP: 🔗 complements the filmed "goal-in-strategy-out." That video already teaches getting the model to surface strategy and understanding from a goal; this repurposes that exact move as your acceptance test for a NEW model, so do not re-teach the mechanic, teach the evaluation frame around it.
- PROOF TO REUSE: "the first leverage I'm looking for is not can it do the work"; the "describe it back... picks out one or two key details I haven't thought about" win condition; "hardest problem only" over problems the old model already aces.

### 2. Why New Models Rarely Change Everything
- HOOK: A frontier model that "beats Pokemon" still missed a bug a junior would flag. Here is what actually improves between releases.
- THE PROMISE: For engineers deciding whether to chase every release, a mental model that measures progress in constraints-handled and corrections-avoided, not benchmark wins.
- THE SHAPE: (1) The hype gap: "more hyped than the value they produce." (2) Real design means attending to tens or hundreds of constraints at once. (3) The U32-vs-U64 thread-ID demo the model failed to flag. (4) The compounding math: five corrections down to two doubles effectiveness. (5) When marginal is still worth switching for.
- SPINE: 2.
- SLOT: Techniques class > "Working With Model Releases" (mindset video, sits near "gravitational-pull-from-older-models").
- RELATIONSHIP: ❌ net-new. Nothing in the catalog frames model progress as marginal constraint-handling; "the-shifting-bottleneck" is about the workflow bottleneck moving, and "gravitational-pull-from-older-models" is about model bias toward old patterns, neither is this claim.
- PROOF TO REUSE: "most model releases are hype. That's my summary"; "attend to tens or hundreds of constraints"; the U32 thread-ID collision math (10,000 threads/sec collides in ~5 days); "you've just doubled your effectiveness."

### 3. Build Your Own Private Model Benchmark
- HOOK: Public benchmarks get gamed. The one benchmark a lab can never overfit to is the file of problems that personally beat you.
- THE PROMISE: For anyone who wants an honest signal on each release, a repeatable way to build a personal regression suite from your own hardest solved bugs.
- THE SHAPE: (1) Why fresh-prompt testing is noise. (2) Log SHA + prompt + answer key for a week-long bug. (3) Check out the pre-fix SHA and replay the prompt on the new model. (4) Grade instantly against the answer you already own. (5) Grow the collection; store context so you still remember it.
- SPINE: 3.
- SLOT: My Daily Workflows class > new "Model Evaluation" habit (or Techniques class, same "Model Releases" chapter).
- RELATIONSHIP: ❌ net-new. No catalog video covers building a personal eval set; "test-time-compute" is about turning up the compute knob, not curating regression problems.
- PROOF TO REUSE: "I keep a couple commits logged in a txt file... if I check out this repo to this Shaw and give it this prompt that is a problem that took me a week to solve"; "you accumulate your own little collection of mini bench"; the 3am "burned into my brain" answer-key framing.

---

## 📚 Full wisdom (reference)

### SUMMARY
Dex and Vibb stress-test the new Fable 5 model live on their hardest real problems, concluding most releases underwhelm their hype rather than transforming work.

### IDEAS
- Evaluate a new model on your hardest current problem, not benchmarks like Pokemon or toy puzzles.
- First leverage you seek isn't whether it solves the work; it's how coherently it comprehends it.
- Hand the model your design docs and ask what major architectural detail you have possibly missed.
- A solid win: it restates the architecture coherently and surfaces one or two previously overlooked details.
- Keep a text file of git commit SHAs plus prompts for hard problems that took weeks.
- Check out that SHA, replay the saved prompt, and see whether the new model one-shots it.
- Prefer old already-solved problems as evals because you already own the answer key and expected outcome.
- Old problems carry a downside: you may no longer remember their full context well enough yourself.
- One-shotting a problem gives a weaker signal than leaving the model looping in a box overnight.
- A slow model that finds a decade-old ffmpeg vulnerability beats a fast model that only one-shots.
- Minor corrections heavily bias the model's future behavior across the whole rest of the context window.
- Steer around a repeated mistake simply by telling the model to disregard the previous error message.
- Auto mode's bash-safety classifier should use a cheap fast model, never your primary expensive thinking one.
- Switch your own products and evals onto the new model to genuinely experience how it behaves.
- Model releases are consistently more hyped than the actual value they produce over existing frontier models.
- The real generational gain is handling one or two more design constraints than the previous model.
- Cutting corrections from five to two per conversation roughly doubles your real effective throughput with agents.
- A U32 thread ID collides within days at scale; a great model should flag that unprompted.

### INSIGHTS
- Good model evaluation starts with comprehension, not completion; the first leverage is understanding before any output.
- The hardest problem you currently hold maximum context on is your only honest benchmark for models.
- Progress between model generations is marginal but compounding; each correction removed multiplies your effective output substantially.
- The real frontier metric is constraints attended simultaneously, not one-shot benchmark scores, raw speed, or hype.
- Private evals beat public benchmarks because you uniquely know the correct answer and the hidden traps.
- A slow, thinky model often forces a product UX redesign so real users tolerate longer waits.
- The context window stays steerable mid-task; one correction reshapes all of the model's subsequent behavior downstream.
- Zero-prep live testing reveals more about a model than any curated and heavily rehearsed demonstration could.

### QUOTES
- "You're looking for leverage." (Dex)
- "I'm looking for leverage. Exactly. And the first leverage I'm looking for is not can it do the work." (Vibb)
- "Whenever a new model comes out, this is really my task. I take the hardest task I have... and I just try and have the model regurgitate back to me what it understands about the task so far." (Vibb)
- "I keep a couple commits logged in a txt file somewhere... if I check out this repo to this Shaw and give it this prompt that is a problem that took me a week to solve and the model sucked at helping with it." (Dex)
- "You kind of accumulate your own little collection of mini bench." (Dex)
- "If you ever try a problem that Opus is already good at, you're not going to know if it's any better... the recommendation for me always is hardest problem only." (Vibb)
- "The model getting a little bit smarter and doing a oneshot problem is less of a useful evaluation of the gap in quality versus doing something like a slash goal or a Ralph loop." (Vibb)
- "Just use the shitty model for bash approval." (Vibb)
- "It's probably going to heavily bias off of minor corrections... to say disregard the previous error message effectively." (Vibb)
- "Model releases, they're more hyped in general than the value they produce." (Vibb)
- "If you had to do five corrections per conversation and you can cut that down to two out of a hundred things the model could get right, you've just doubled your effectiveness." (Dex)
- "Being able to attend to tens or hundreds of constraints when designing a solution." (Vibb)
- "Most model releases are hype. That's my summary." (Vibb)

### HABITS
- Vibb always takes his single hardest in-progress task to every newly released model before anything else.
- Dex keeps hard-won commit SHAs and their matching prompts logged inside a personal notes text file.
- He asks the model to regurgitate its understanding first, before ever asking it to solve anything.
- They run brand-new models with absolutely zero prep, minutes after the announcement, against real production work.
- Vibb switches his own products and evals to the new model to feel its real behavior.
- Whenever a model errs, they immediately correct it so future turns reliably avoid the same mistake.
- Vibb prefers judging models on deeply nuanced technical problems he cannot quickly scan-read for correctness afterward.
- He often reviews the full Claude Code transcript afterward instead of watching the live real-time preview.

### FACTS
- A U64 gives roughly every atom in the universe its own thread ID; U32 collides fast.
- At ten thousand threads per second, a U32 ID space collides within roughly five short days.
- At one thousand threads per second, a U32 identifier space collides in only about fifty days.
- At one million threads per second, a U64 space still takes about 585,000 years to collide.
- Profiled code runs slower than release code; observability always costs measurable additional CPU cycles at runtime.
- BAML measured a single call roundtrip at roughly 136 cycles, approximately 40 nanoseconds of raw overhead.
- The team targets under ten nanoseconds per event to stay below a 2% total profiling penalty.
- Two wall-clock reads per function call pair add a 40-to-60 nanosecond minimum irreducible profiling cost each.
- Jake Nations ranked among Netflix's top Claude Code engineers before leaving to join an AI lab.

### REFERENCES
- BAML / BoundaryML (agent-readable programming language), and the "AI That Works" podcast.
- Human Layer (tools for coding agents on hard problems), Dex's company.
- Claude Code (harness), `claude --update`, `claude --version`; auto mode and its bash-safety classifier.
- Fable 5 (the new Anthropic model under test) and Opus 4.8 (the comparison baseline).
- Pokemon as a model benchmark; "slash goal" and the "Ralph loop" long-horizon patterns.
- ffmpeg (the 10-year-old vulnerability example); GStack; MCP server; speedscope-style flame graphs.
- Codex (contrast on robotic design-doc writing style); Jake Nations (ex-Netflix Claude Code engineer).
- YC conference in Cancun (where Dex was coding); U32 vs U64 thread IDs; SPSC ring buffers, TLS ring.

### ONE-SENTENCE TAKEAWAY
Test new models on your hardest real problems; most releases improve constraints marginally, not magically.

### RECOMMENDATIONS
- Take your hardest in-progress task to each new model before trusting benchmark leaderboards or the hype.
- Ask a new model to restate your architecture and name the key details you personally overlooked.
- Start a personal text file logging commit SHAs, prompts, and answer keys for previously hard-won problems.
- Replay that private benchmark against each model release to measure the real gains, not marketing claims.
- Favor old already-solved problems as tests; you can instantly judge correctness against a known concrete answer.
- Judge a model on long-horizon loops, not just one-shots, before you conclude it lacks real capability.
- Correct a model's mistake immediately so that fix biases all of its remaining turns in conversation.
- Configure auto mode's safety classifier to run a cheap fast model, not your primary expensive one.
- Switch your real products and evals onto a new model to judge it under genuine load.
