---
title: Agentic Backpressure Deep Dive
videoId: Zx_GOhGik0o
url: https://www.youtube.com/watch?v=Zx_GOhGik0o
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Learning tests: have the agent write a throwaway probe that proves how a black-box system actually behaves before you build against it.** Research that only reads code and docs quietly inherits assumptions; an executable learning test converts a guess into a verified fact and stops a wrong assumption leaking all the way into implementation.
VERDICT: net-new video available.

**2. Design the back pressure before you write the code: give the agent deterministic, observable feedback loops so it corrects itself.** The high-leverage act is designing the check harness (compiler, type checker, tests, hooks), not writing features; deterministic signals beat LLM-as-judge because you can accidentally steer a model, never a type checker.
VERDICT: next-step video available (complements the filmed "Closing the Loop").

**3. Make the other mistake: calibrate how much planning a problem needs by deliberately overshooting, then undershooting. (LATENT SPINE)** Agentic coding rewards variatic technique selection, and you develop that instinct faster by binary-searching the extremes than by inching toward the ideal. Sourced thinly here, so the video needs extra grounding.
VERDICT: net-new video available (latent, thinly sourced).

---

## Summary + counts

Boundary's Vibb and Human Layer's Dexter, hosts of AI That Works, explain learning tests for black-box systems and deterministic back pressure loops for self-correcting agents.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

**Spine 1: Learning tests for black boxes.**
The claim: before you build against a system you cannot read (a closed API, a CLI, an LLM), have the agent write a small throwaway test that runs it and documents what actually comes back. What most people get wrong is trusting the standard "research, plan, implement" loop, which silently assumes it can learn everything by reading source. It cannot when the source is a closed binary or a probabilistic model. The mechanism: because the assumption forms during research, it flows unchecked into the plan and then the implementation; you pass phase one and two, then phase three hits reality and invalidates everything upstream, forcing a full redo. A learning test moves that discovery to the cheapest possible moment. It generalizes cleanly to performance engineering, which Dexter calls "a learning test all the time": you do not model the assembly, you compile, read the emitted output, and iterate. It goes wrong when the problem is a design problem with no runnable surface (Vibb's three-way type-system refactor), or when you over-invest in tests for stable libraries that never change their contract.

**Spine 2: Design the back pressure first.**
The claim: back pressure is any observable feedback loop that lets the model detect and fix its own mistakes, and the highest-leverage move is designing that harness before writing code. The non-obvious part: people reach for LLM-as-judge, a builder and a manager that "are both using the same freaking model," so the judge can be accidentally steered exactly like the builder. The mechanism: a deterministic check (type checker, compiler, pre-commit hook, stop hook) is either right or wrong and emits tokens describing why, so the model loops to green without a human in the seat; the more deterministic layers you stack, the less you review. That is why the best engineers "spend three days designing the back pressure system, not even writing the code," then let Opus run for two days and get 20,000 working lines. It generalizes to flaky database test suites, where a pre-check gates the rest. It goes wrong when checks are only binary rather than observable, or when a file too important to automate (a dependency allow-list) gets auto-edited and opens the floodgates.

**Spine 3: Make the other mistake (latent).**
The claim: the scarce skill in agentic coding is not any single technique, it is the instinct for how much planning a given problem needs, and you build that instinct fastest by deliberately overshooting then undershooting. Non-obvious because most people try to increment toward the right amount and stay "too constant with their technique." The mechanism: treat calibration as a binary search; do what feels like far too much planning, then far too little, and the ideal range for that problem type reveals itself in a couple of reps instead of dozens. It generalizes to any calibrated behavior (the speakers cite executive-coaching advice about over- and under-doing traits like extroversion). Where agentic coding differs from human typing: a human can use one reliable technique all day, but an agent forces you to be variatic, switching approach per problem, per model, even per day. It goes wrong as pure "it just vibes" hand-waving unless anchored to concrete agentic examples, which is why this needs extra sourcing before filming.

---

## 🎬 Proposed ACS videos

### 1. Prove It Before You Build It: Learning Tests for Black-Box APIs
- HOOK: Your agent's research is quietly guessing how that closed API works, and the guess ships straight into your code.
- THE PROMISE: For anyone building against an SDK, CLI, or LLM they cannot read, walk away able to make the agent prove a system's real behavior before writing a line of the feature.
- THE SHAPE: (1) The assumption that leaks from research to implementation and forces a full redo. (2) hello-world probe: "read the meta.md and console.log all messages" against the Claude Agent SDK. (3) Grow it into assertions ("what does query emit and in what order"). (4) Live demo: "read the v2 docs and the existing learning tests and create a learning test for the new stream send API." (5) Bank a hundred of them, rerun on every dependency bump.
- SPINE: 1
- SLOT: Context Engineering > Understanding the System
- RELATIONSHIP: ❌ net-new. Sibling to the planned "What breaks if I change this?", which makes the agent diagram blast radius inside code you own; this covers systems you cannot read, and uses an executable probe rather than a static diagram, so neither re-teaches the other.
- PROOF TO REUSE: "You can accidentally steer a model. You cannot accidentally steer a type checker." The Claude SDK v1-to-v2 change that now needs forkSession true. The team's ~100 documented learning tests that flag broken external contracts on upgrade.

### 2. Design the Back Pressure First
- HOOK: The best AI engineers spend three days building nothing but the checks, then let the model write 20,000 lines while they watch.
- THE PROMISE: For engineers who babysit their agent's every diff, leave able to design a deterministic feedback harness so the model corrects itself and you review only what matters.
- THE SHAPE: (1) Define back pressure: observable feedback that lets the model fix its own mistakes. (2) The escalation ladder: type check, compiler, unit tests, MCP/browser screenshot, pre-commit, stop hook. (3) Why deterministic beats LLM-as-judge (same model, steerable both ways). (4) The stop hook that reinjects failures into context. (5) The one file you never automate: the dependency allow-list.
- SPINE: 2
- SLOT: Techniques > Closing the Loop (next to the filmed video)
- RELATIONSHIP: 🔗 complements "Closing the Loop". That video teaches that the agent needs a feedback loop to verify its own work; this adds the move after it: how to DESIGN the harness up front and why to reach for deterministic signals over an LLM judge. Do not re-teach "give it a loop"; teach "engineer the loop before the code."
- PROOF TO REUSE: "The back pressure mechanism doesn't have to be binary. It just needs to be observable." Engineers who "spend 3 days designing the back pressure system, not even writing the code." The cargo-sto dependency matrix as human back pressure you review as a diagram, not code.

### 3. Make the Other Mistake: Calibrating How Much to Plan
- HOOK: Stop inching toward the right amount of planning. Overshoot on purpose, then undershoot, and you find it in two reps.
- THE PROMISE: For anyone unsure whether to plan hard or just vibe a task, leave with a deliberate method for building the instinct that separates fast agentic engineers from slow ones.
- THE SHAPE: (1) Why one constant technique fails in agentic coding (you must be variatic). (2) The calibration spectrum: too much planning versus too little. (3) Binary-search it: do too much, then too little, converge. (4) Bank the pattern: "a problem that looks like this, I can just vibe." (5) Why the ideal range shifts with model, problem, and even the day.
- SPINE: 3
- SLOT: Techniques > (developing instinct) or Start Here
- RELATIONSHIP: ❌ net-new (latent, thinly sourced). Adjacent to "The Shifting Bottleneck" (the meta-skill of finding the constraint) and "Build It Twice" (throwing out a wrong first pass), but neither teaches the deliberate over/under-shoot calibration method. Needs extra sourcing before filming.
- PROOF TO REUSE: "If you apply everything everywhere you will just be the slowest engineer in the world." "Sometimes you should do what feels like too much and sometimes you should do what feels like way not enough." The claim that most people struggle at AI coding because they are too constant with their technique.

---

## 📚 Full wisdom (reference)

### SUMMARY
Boundary's Vibb and Human Layer's Dexter, hosts of AI That Works, explain learning tests for black-box systems and deterministic back pressure loops for self-correcting agents.

### IDEAS
- Learning tests are throwaway scripts that poke a black-box system to observe how it actually behaves.
- You can accidentally steer a model, but you can never accidentally steer a deterministic type checker.
- Back pressure is any observable feedback loop letting the model detect and fix its own mistakes.
- The strongest engineers spend three days designing the back-pressure harness before they write any actual code.
- A wrong assumption made high up leaks through research and planning into implementation, invalidating everything downstream.
- Calling an LLM is itself a learning test, which is exactly what the BAML playground enables.
- The Claude Agent SDK wraps the CLI, translating a giant options blob into command-line flags underneath.
- The team keeps a hundred learning tests documenting their contract with external systems they cannot control.
- LLM-as-judge is overapplied; builder and manager sharing one model just injects the manager prompt into builder.
- Back pressure need not be binary; it only needs to be observable, emitting tokens describing failures.
- A global stop hook can deterministically run checks and inject failures back into the model's context.
- Auto-generated dependency matrices expose broken architectural boundaries visually, so humans review a diagram instead of code.
- To calibrate planning depth, deliberately make the other mistake: overshoot, then undershoot, binary-searching toward the ideal.
- Agentic coding demands variatic technique: different problems need different methods, unlike human typing's single reliable approach.
- Docs alone are insufficient; they are long, easy to misread, and subtle behaviors get silently missed.
- Two repos open at once lets you explore two solution strategies in parallel, mapping bug space.
- Cloud SDK v1 to v2 changed session defaults, now requiring an explicit forkSession equals true flag.

### INSIGHTS
- Reading code and docs silently inherits assumptions; executable proof tests convert those assumptions into verified facts.
- The value of deterministic back pressure is that it removes the human from routine correctness checking.
- Designing the check harness, not the code, is highest-leverage because the model then self-corrects without you.
- Learning tests double as regression tripwires: rerun them on dependency upgrades to detect changed external contracts.
- The scarce skill is not implementing back pressure but instinct for which technique fits each problem.
- Most people struggle with AI coding because they apply one constant technique instead of selecting adaptively.
- Because generating code now costs almost nothing, throwing away a wrong plan is cheap, not wasteful.
- Human back pressure means designing artifacts, like dependency diagrams, that surface violations without humans reading code.
- Professional growth requires deliberate off-clock practice; developing agentic instincts mirrors doctors reading journals beyond working hours.

### QUOTES
- "You can accidentally steer a model. You cannot accidentally steer a type checker." (Vibb)
- "Code humans created this for humans. We wanted back pressure." (Dexter)
- "The back pressure mechanism doesn't have to be binary. It just needs to be observable. That's the key." (Dexter)
- "The model has to be able to get tokens in to tell it what was wrong." (Vibb)
- "So back pressure is exactly this is you give the model a way to fix its own mistakes." (Vibb)
- "they would spend 3 days designing the back pressure system. Not even writing the code, not building anything." (Dexter)
- "performance engineering is basically a learning test all the time." (Dexter)
- "if you apply everything everywhere you will just be the slowest engineer in the world." (Dexter)
- "sometimes you should do what feels like too much and sometimes you should do what feels like way not enough." (Vibb)
- "Steer the models to the things you want. You can do anything." (Vibb)

### HABITS
- The team drops external docs directly into the episode folder before building learning tests against them.
- They rerun their learning-test suite manually whenever pulling a new dependency version to catch broken contracts.
- Vibb uses Zed for reading and writing Markdown because it opens instantly and renders Markdown nicely.
- They run type checks before compiler checks, letting the model self-correct before any human review begins.
- He keeps two repositories open, implementing the same feature via two strategies to explore bugs faster.
- They kick off Opus for planning while Codex simultaneously attempts the same ticket from scratch independently.
- They add PR rules flagging sensitive files, requiring human code review whenever those specific files change.
- They read manual verification steps in plans and convert curl checks into automatable spun-up service tests.

### FACTS
- Learning tests were named by Michael Feathers in his book Working Effectively with Legacy Code originally.
- The phrase learning test has terrible SEO because it collides with educational tests that assess students.
- BAML generates two separate type systems, one partial for streaming and one full for non-streaming outputs.
- Boundary's compiler actually maintains three separate type systems: streaming, non-streaming, and the compiler's own internal representation.
- The bypassPermissions option in the Claude Agent SDK translates to the dangerously-skip-permissions CLI flag under the hood.
- The Claude Agent SDK invokes the Claude CLI under the hood, converting TypeScript options into flags.
- Uncle Bob recommended giving employers forty-five hours weekly while spending twenty additional hours honing your craft.
- Boundary built an internal tool called cargo sto that autogenerates the codebase dependency matrix diagram automatically.

### REFERENCES
- BAML and Boundary (the streaming-aware LLM programming language and company)
- Riptide, at Human Layer (Dexter's tool and company)
- Claude Agent SDK and the Claude CLI (query method, allowedTools, forkSession, unstable stream send API)
- Michael Feathers, "Working Effectively with Legacy Code" (origin of the learning-test term)
- Zed editor; Rust; TypeScript; Anders Hejlsberg (cited as a "goat")
- OpenAI responses API (thinking-token preservation behavior)
- context7 and web search as doc-ingestion options
- cargo sto (Boundary's internal dependency-matrix generator)
- Jeff Huntley (the back-pressure spec/build/test/update-specs loop diagram)
- AI That Works prior episodes: "Advanced context engineering for coding agents" (Aug 5), the Ralph Wiggum episode
- pre-commit / PRK (pre-commit hooks as deterministic back pressure)
- Uncle Bob (the 45-plus-20 hours professionalism recipe)
- Codex 5.3 and Opus (parallel planning-versus-implementation workflow)
- node child_process API, node crypto HMAC verification (other documented learning tests)
- LLM-as-judge, fuzz testing, penetration testing (analogies for probing black boxes)

### ONE-SENTENCE TAKEAWAY
Give coding agents deterministic feedback loops and prove black-box behavior before building on your assumptions.

### RECOMMENDATIONS
- Before implementing against a black-box API, have the agent write a learning test proving its behavior.
- Prefer deterministic feedback like type checkers and compilers over LLM-as-judge for reliable automated back pressure signals.
- Add a global stop hook that runs checks and reinjects failures into the model's context automatically.
- Spend real time upfront designing the back-pressure harness before writing a single line of feature implementation.
- Keep a documented suite of learning tests and rerun them whenever upgrading any external dependency versions.
- When uncertain about planning depth, deliberately overshoot then undershoot to develop instinct through rapid binary search.
- Convert manual curl verification steps into automated tests that spin up the service on isolated ports.
- Invest time building tooling, like a dependency-diagram generator, so boundary violations become visually obvious to reviewers.
- For small tasks skip planning and vibe it; when it fails, note that pattern next time.
