---
title: No Vibes Allowed #33
videoId: fF3GssyaTcc
url: https://www.youtube.com/watch?v=fF3GssyaTcc
date: 2026-07-01
status: posted
---

# The one idea worth a video

**1. Order your implementation plan's phases by what you can independently verify, biggest unknown first, not by architecture layer.**
Dex throws out an entire model-generated plan because it is "horizontal" (all database, then service, then wiring, then API) and therefore only runnable at the very end, when a break is buried in a thousand lines.
VERDICT: 🔗 next-step video available (complements "Ultra Plan").

**2. Keep the research phase objective and walled off from planning: it should describe only how the system works today, never how to build it.**
Contaminating research with implementation detail makes the model lock onto its first nondeterministic idea; keeping it objective preserves the options a good plan needs.
VERDICT: 🔗 next-step video available (complements "What Breaks If I Change This").

**3. Reuse a verified git diff as the spec for the next similar feature instead of re-planning it.**
A shipped diff is "verifiably true", so it encodes the codebase's real conventions and beats a fresh plan that only guesses at them.
VERDICT: 🔗 next-step video available (complements "Build It Twice").

---

# Summary + counts

Dex from HumanLayer and Vaibhav from BAML live-code three features into a coding-agent desktop app, debating research-plan-implement discipline, phase verifiability, context engineering, and model steering.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

**Spine 1: Order plan phases by verifiability, unknowns first.**
The model's instinct, and most engineers', is a horizontal plan: build the whole database layer, then the service, then wire it in, then expose the API. It reads tidy but is only runnable at the very end. Dex rejects a generated plan for exactly this reason. The mechanism: the riskiest part here (invoking the Claude CLI with Haiku, overriding the system prompt, inheriting the Max subscription) is the part most likely to be wrong, and a horizontal plan hides that risk behind hundreds of lines, so you only discover the break at the end when the blame surface is a thousand lines wide. Reorder so phase one is a standalone integration test that proves the risky call works, and make each later phase (database column, go-routine, SSE) end in its own manual check, a SQLite query or a curl. Now any failure is localized to a small diff. This generalizes to any multi-layer migration, for example a payments webhook where you prove signature verification in isolation before building the ledger. It goes wrong two ways: over-slicing a tiny feature that should be one phase, and phases whose "tests" mock the very thing that matters, which gives fake confidence. As Dex puts it, "put your biggest unknowns as the first phase."

**Spine 2: Keep research objective, separate from planning.**
It feels efficient to tell the agent what you are building while it researches. Vibb does exactly that, and Dex predicts worse results, then shows why. A research prompt loaded with implementation detail makes the model "pick the first thing it thinks of" because generation is nondeterministic and, in Dex's words, "models are very bad at evaluating whether something is good." The questions it then asks are implementation questions rather than "here is what I could not figure out from the code." Keeping research objective preserves optionality, so the plan phase can brainstorm across real options. He stashes all implementation notes in a separate text file for the plan, and he gates the plan too: iterate on the phases outline before letting the model write the 600-line file, because writing it burns roughly 8% of the context window and drops you into the "dumb zone." This generalizes to the email-classification episode's rule of keeping the model objective by asking for boolean flags instead of a 1-to-10 score, and more broadly to separating "understand" from "decide." It goes wrong for tiny features with one obvious implementation, where the separation is overkill. "You want to keep the model objective as long as possible."

**Spine 3: Reuse a verified git diff as the spec.**
The reflex is to re-run research and planning for every feature. Dex reuses the diff instead. A diff is "verifiably true": it already compiled, passed its tests, and shipped, so it encodes the codebase's real conventions and wiring that a plan can only guess at. Feed it as "implement a feature very similar to this diff or commit" and the model imitates a known-good pattern instead of re-deriving one nondeterministically. Because the AI-titles feature already established how to call Haiku, wire the deferred go-routine, and publish an SSE event, the follow-on AI-summaries feature is mostly a transform of that same diff. This generalizes to team enablement: publish "use PR #N" or a specific commit as the canonical pattern so everyone builds adjacent features the same way, which is exactly what the BAML team does by shipping small, generalizable sample diffs. It goes wrong when the new feature does not genuinely rhyme with the diff, or when the source diff is too large or poorly scoped and drags in irrelevant patterns. This is the next step beyond "Build It Twice": that video rebuilds the same feature from its own throwaway prototype, whereas this propagates a proven diff to different, adjacent features. "The diff is like verifiably true. It just works way better."

---

# 🎬 Proposed ACS videos

## 1. Order Your Plan by What You Can Prove, Not by Layer
- HOOK: The model's tidy layer-by-layer plan is a trap, because you cannot test any of it until the last line is written.
- THE PROMISE: For anyone who plans with an agent, you leave able to reorder any plan so every phase ends in a check you can run yourself.
- THE SHAPE: (1) Show the model's default horizontal plan (database, service, wire, API). (2) Name the risk: only verifiable at the end. (3) Rewrite it biggest-unknown-first so phase one is a standalone integration test hitting the real Claude CLI. (4) Each later phase ends in a SQLite query or a curl. (5) Fork and regenerate against the new phase order.
- SPINE: 1.
- SLOT: Claude Code > planning (pairs with Ultra Plan); also fits Context Engineering.
- RELATIONSHIP: 🔗 complements "Ultra Plan" (V20) by being its next step. Ultra Plan teaches how to generate a thorough plan with the model; it does not teach that the model's plan is horizontally ordered and unverifiable until the end. This video adds the missing rule: reject the horizontal default and sequence phases by verifiability, unknowns first.
- PROOF TO REUSE: Dex throwing out a whole generated plan; "put your biggest unknowns as the first phase"; the phase-one integration test that invokes the real CLI and inherits the Claude Max subscription instead of mocking the part that matters.

## 2. Your Best Spec Is Last Week's Diff
- HOOK: Stop re-planning features that look like ones you already shipped. Hand the agent the diff.
- THE PROMISE: For anyone shipping a series of similar features, you learn to turn a merged diff into the spec for the next one and cut planning to almost nothing.
- THE SHAPE: (1) Ship a small, generalizable feature normally (AI titles). (2) Grab its diff or commit. (3) Prompt "implement a feature very similar to this diff" for the next feature (AI summaries). (4) Show it inherits real conventions a fresh plan would have guessed at. (5) Publish "use PR #N" as the team pattern.
- SPINE: 3.
- SLOT: Techniques > The First Build Is a Prototype (next to Build It Twice).
- RELATIONSHIP: 🔗 complements "Build It Twice" by being its next step. Build It Twice says throw away your first build and rebuild the same feature from what you learned. This video propagates the verified diff outward: the shipped diff becomes the reusable spec for different, adjacent features and a team-wide pattern reference.
- PROOF TO REUSE: "the diff is like verifiably true. It just works way better"; "We produce sample git diffs that are really small features that are guaranteed to be really generalizable"; the AI-titles to AI-summaries handoff.

## 3. Keep Research Objective: Never Let It Plan While It Reads
- HOOK: The moment you tell the agent what you are building, its research stops being research.
- THE PROMISE: For anyone using a research-plan-implement loop, you learn to wall research off from planning so the model keeps its options open and produces a better plan.
- THE SHAPE: (1) Run two research sessions side by side, one with the spec, one without. (2) Compare the questions: implementation-biased versus "what I could not figure out from the code." (3) Stash implementation notes in a text file for the plan. (4) In planning, iterate the phases outline before writing the file. (5) Explain the 8%-context "dumb zone."
- SPINE: 2.
- SLOT: Context Engineering > Understanding the System (next to What Breaks If I Change This).
- RELATIONSHIP: 🔗 complements "What Breaks If I Change This" by being its next step. That video points the agent at understanding the system before production. This video adds the discipline of a distinct, objective research phase that is walled off from planning, plus the context-budget reason to outline phases before writing the plan file.
- PROOF TO REUSE: "you want to keep the model objective as long as possible"; the with-spec and no-spec parallel research demo; "8% of the context window that is required to write out this 600 line markdown document"; "Models are very bad at evaluating whether something is good or not."

## Also film-able (not deep-dived)
- **The context-engineering dial, calibrated by eval.** Calibrate how much steering to apply by deliberately over-engineering and under-engineering on real tasks, lock every workflow dimension but one and evaluate along that single axis, and reset your assumptions when a new model ships. Slot: Techniques > Multi-Model workflows (near The Ambiguity Line / Scaling Taste). Likely 🔗 complement.
- **Prove-it-works throwaway scripts in the research phase.** Write a bash one-liner proof of concept (open a file in Obsidian) during research to reverse-engineer a black-box behavior before you plan around it. Slot: Context Engineering > research. Likely 🔗 complement to What Breaks If I Change This.
- **Fork to recover from a bad trajectory.** Control-X then command-Y to fork the session back to before the model wrote the bad plan file, instead of restarting. Slot: Claude Code > slash-fork / checkpoints-and-rewind (already in backlog); likely ✅ covered.

---

# 📚 Full wisdom (reference)

## SUMMARY
Dex from HumanLayer and Vaibhav from BAML live-code three features into a coding-agent desktop app, debating research-plan-implement discipline, phase verifiability, context engineering, and model steering.

## IDEAS
- Order plan phases by what you can verify, not by architecture layers, putting biggest unknowns first.
- Models default to horizontal plans testable only at the end; reject that and slice vertically instead.
- Keep research objective: describe only how the system works today, never how you will build it.
- Iterate the phases outline before writing the plan file, which alone eats eight percent of context.
- Reuse a verified git diff as the spec for building the next, very similar feature quickly.
- Give the model a one-off proof-of-concept shell script during research before committing to any full plan.
- Validate AI code with real integration tests and curl, not by reading every generated line yourself.
- Write integration tests that invoke the real Claude CLI instead of mocking the parts that matter.
- Fork the session back to before it wrote the bad plan rather than restarting from scratch.
- Multiplex three or four parallel model sessions, then read and merge the best output at end.
- Generate session titles using a throwaway Haiku call in a temp directory, overriding the system instructions.
- Always ask for boolean flags about the output, not a subjective one-to-ten score models will fake.
- Phased-implement runs each phase inside its own sub-agent, keeping the parent session's context window clean throughout.
- Calibrate context-engineering effort by binary-searching: deliberately try approaches you expect to fail to learn the boundaries.
- Lock every workflow dimension except one, then evaluate along that single axis to build real intuition.
- When new models ship, reset all expectations and re-test how much the model can now do.
- The magic words: end the plan prompt by reinforcing instructions so the model stops skipping steps.
- Context switching is the most expensive operation in software, and equally expensive for a human developer.

## INSIGHTS
- You cannot outsource the thinking; the model needs your opinions before it will produce good work.
- Leverage means not re-reading every line; build a cheap external check that the model cannot fake.
- Models are good at describing what exists, but bad at judging whether something is actually good.
- Feature complexity dictates how much context engineering you need; simple features can tolerate blasting straight through.
- A verified diff beats a plan as a spec because the diff is already verifiably true.
- Keeping research objective preserves options; premature implementation makes the model pick its first, nondeterministic idea instead.
- Writing the plan file too early exhausts the context window and traps you in the dumb-zone.
- Good tooling should do the deterministic work; humans should only do thinking, design, and systems architecture.
- The hardest adoption barrier is discontinuous innovation: workflows even experienced developers cannot anneal to quickly enough.
- Make it work end-to-end first, then build the test loop, and only then refactor for cleanliness.

## QUOTES
- "You cannot out outsource the thinking, man." (Dex)
- "if you know what you want, just tell the model what you want." (Dex)
- "put your biggest unknowns as the first phase." (Dex)
- "Models are very bad at evaluating whether something is good or not. They just want to tell us what we want to hear." (Dex)
- "you don't want to be reviewing the code for correctness because then you're not getting much leverage." (Dex)
- "This took the plan for me from like 70% to 90%. And 90% for me is good enough." (Dex)
- "you want to do as much steering as possible before you eat the like 8% of the context window that is required to write out this 600 line markdown document." (Dex)
- "the diff is like verifiably true. It just works way better." (Dex)
- "make it work and then figure out your test loop and then refactor." (Dex)
- "I find speed is my actual number one alpha." (Vibb)
- "you got to like pick a dimension and then eval across that dimension for your own intuition." (Dex)
- "We produce sample git diffs that are really small features that are guaranteed to be really generalizable." (Dex)

## HABITS
- Draw a quick two-minute architecture diagram first so both people share language before discussing the build.
- Stash all implementation detail in a separate text file, saving it for the later planning phase.
- Title every session immediately so your parallel research and plan sessions never get lost or confused.
- Kick off phase one the moment it looks correct, then read the later phases while running.
- Run every new parallel session in a fresh work tree so runs never overwrite each other.
- Default to Haiku for research and grunt work because raw speed is the biggest productivity lever.
- Use whichever coding tool is already open; the lowest-friction contextualized tool beats the theoretically optimal choice.
- Tell the model when logs are needed and that you, not it, will restart the demon.
- Run experimental builds against a separate dev database, never sharing the real production database while developing.

## FACTS
- Context switching is the most expensive operation across multi-threading, async contexts, and swapping thread state over.
- Research shows light mode is significantly better than dark mode for carefully reading long prose specs.
- Code reads well in dark mode because syntax-keyword high contrast reveals its structure and control flow.
- BAML development began around mid-2023, making that codebase roughly two years old at the recording time.
- Code layer's Tower backend spawns a legacy Go process named HLD, the human layer demon process.
- Claude Code sub-agents in code layer run hardcoded on Sonnet, configured in the agent's own header.
- The term context engineering was coined on this podcast by Dex, from Vaibhav's repeated informal articulations.
- Obsidian's URI opener requires files to live inside a vault rather than opening arbitrary loose paths.
- Opening a title-generation session with Haiku in a temp directory avoids git and surrounding codebase context.

## REFERENCES
- AI That Works podcast (the show; next episode on evals for images and multimodals).
- HumanLayer and "code layer": Tower backend, WUI (Vite front end), CLLD demon, HLD (human layer demon, Go).
- BAML (Vaibhav's framework), the BAML parser, BAML snapshot tests, cargo test.
- Claude Code, the Claude Code Go library, the Claude CLI, Cloud Code TypeScript SDK.
- Models: Opus 4.5 and 4.1, Sonnet, Haiku.
- Tools: Cursor, GPT Codex, Warp, Ghostty (Mitchell Hashimoto), Obsidian (app.opener plugin, Obsidian URI).
- Tech: SQLite, SSE, Go routines, the strangler pattern, TanStack DB replacing zustand.
- "12 Factor Agents" (Dex's methodology).
- "Crossing the Chasm" and its idea of discontinuous innovation (Geoffrey Moore).
- TDD, red-green-refactor.
- The prior email-classification episode (boolean flags versus one-to-ten scoring).
- People: Dex, Vaibhav (Vibb), Kyle, and chat participants David and Max.

## ONE-SENTENCE TAKEAWAY
Order plan phases by verifiability, keep research objective, never outsource thinking to the model itself.

## RECOMMENDATIONS
- Reorder your next plan so the riskiest unknown becomes phase one with a real verification step.
- Reject any model plan that only becomes testable after the very last implementation phase has completed.
- Prompt your research to describe how the system works today without deciding how to build anything.
- Make the model outline phases before writing the file, then fork back if it jumps ahead.
- Save a small, generalizable feature diff and reuse it as the spec for future similar features.
- Add an integration test that invokes the real CLI so you stop reading code for correctness.
- Write a throwaway shell one-liner during research to prove a black-box behavior before planning around it.
- Deliberately over-engineer and under-engineer context on real tasks to learn where the actual useful boundaries sit.
- When a new model ships, reset your assumptions and probe how much it can now handle.
- Replace subjective one-to-ten scoring prompts with boolean flags plus deterministic code that interprets those returned flags.
