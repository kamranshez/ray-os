---
title: Building a Prompt Optimizer
videoId: IkSEXg6f4KY
url: https://www.youtube.com/watch?v=IkSEXg6f4KY
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works
---

## The one idea worth a video

**Spine 1 (reframe, net-new): Prompt optimization is now a build-it-yourself commodity. You point an automated GEPA-style optimizer at the prompts you will never lovingly maintain, and reserve human effort for the code you actually care about.**
Why: it subsumes the "build one from scratch in three days," the GEPA mechanics, the "optimizers need evals," the economics of software-quality-equals-love, and the human-in-the-loop beats. It is the altitude the whole episode hangs off.
VERDICT: net-new video available.

**Spine 2 (technique, de-merged): The quality of any fix loop is dominated by the richness of the failure signal. Feed the model the full source of the failing test, not just the assertion error string, so it reasons over every assertion at once instead of playing whack-a-mole.**
Why: distinct central demo (a Claude Code TDD loop with rich vs thin failure signal), distinct slot, distinct takeaway. It is the concrete move you actually film, so it rides as its own spine.
VERDICT: next-step (complement) video available.

---

## Summary

On the AI That Works stream, Vibhav, Dex, and Greg build a working GEPA-style prompt optimizer inside BAML, live, in just three days from scratch.

Counts: 🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

**Spine 1: optimize the code you have no love to give.**
The claim: an optimizer will not beat a human who truly understands a problem, but it will crush a human on the prompts nobody will ever read. Most people frame optimizers as a race against expertise. Vibhav flips it: "software quality is basically based on amount of time and love you give it," and if you have no love to give a piece of software, it cannot improve regardless of intent. Because human attention is the scarce input, and because an optimizer needs only automated feedback to run unattended, the payoff is inverse to how much you care: highest exactly where you would never look. The mechanism is a closed loop, generate a candidate, evaluate against tests, reflect on failures, combine Pareto-frontier winners, and it only turns when you can supply deterministic back-pressure (evals). This generalizes cleanly to CI-time codegen: auto-tuning the dozens of boilerplate extraction prompts in a data pipeline while you hand-write the one customer-facing prompt. It goes wrong when you have no evals (nothing to optimize against) or when you stop reading the output and ship an overfit prompt.

**Spine 2: the signal you feed the loop matters more than the model.**
The claim: passing only the failing assertion's error message is strictly worse than passing the whole source of the failing test. The naive instinct, which Vibhav admits was his, is to hand the model the error string. Greg found the opposite while building: the optimizer failed repeatedly because it did not know what the test was actually checking. The mechanism is two-step. First, the model reasons over source code better than over terse strings, so the full test tells it the intent, not just the symptom. Second, a single failure message hides the other assertions, so the model fixes assertion two, then assertion four breaks, and you burn iterations on whack-a-mole. Give it every assertion up front and it optimizes for all of them at once. This generalizes directly to Claude Code's TDD loops: feed the agent the full failing spec file, not the truncated pytest tail. It goes wrong when the test source is enormous or leaks the answer, so you scope to the reachable, relevant slice.

---

## 🎬 Proposed ACS videos

### 1. Build a Prompt Optimizer From Scratch
- HOOK: In 2025 everyone built a coding agent from scratch. In 2026, build a prompt optimizer.
- THE PROMISE: For engineers shipping LLM features who still hand-tune prompts. After this you can stand up an automated GEPA-style optimizer and know exactly where to point it.
- THE SHAPE:
  1. The economics: optimize the prompts you will never love; keep human effort for the code you care about.
  2. The loop in five beats: initial prompt plus tests, evaluate, reflect on failures, generate or combine candidates, repeat until convergence.
  3. Live demo: run an optimizer on a deliberately broken prompt (no input, no output type) and watch it hit 100 percent on the first candidate.
  4. Multi-metric: add token cost as a weighted objective and watch the Pareto frontier trade accuracy against length.
  5. The guardrail: always read the resulting prompt, because sparse samples make overfitting invisible to metrics.
- SPINE: 1
- SLOT: Prompt Engineering class, new chapter "Automated Prompt Optimization" (sits after the manual iterative-refinement foundation).
- RELATIONSHIP: ❌ net-new. The catalog and to-film briefs have nothing on prompt optimizers, GEPA, DSPy, or Pareto-frontier tuning. The nearest neighbor is the unfilmed "iterative-refinement" PE brief, which is the manual human loop; this is the automated, evolutionary version and a distinct video.
- PROOF TO REUSE: "everyone should build a prompt optimizer from scratch" (the 2025-to-2026 framing); Greg built the whole thing in three days; "software quality is basically based on amount of time and love you give it"; the live run converging to 100 percent on trial one; adding a token-cost weight and watching the prompt shrink via aliases.

### 2. Feed the Loop Better: Give Your Fixing Agent the Whole Test
- HOOK: Your agent keeps fixing one thing and breaking another. It is not the model. It is the signal you feed it.
- THE PROMISE: For anyone running an agent in a test-fix loop. After this you know why the full test source beats the error string, and how to scope what you feed in.
- THE SHAPE:
  1. The naive default: pipe the assertion failure message to the agent and let it patch.
  2. Why it fails: the message hides the other assertions, so the agent whack-a-moles one at a time.
  3. The fix: hand it the full source of the failing test so it reasons over intent and all assertions at once.
  4. Scope control: give it only the minimum reachable code, not the whole repo, so it stays focused.
  5. Demo: same broken function, thin signal versus rich signal, side by side.
- SPINE: 2
- SLOT: Techniques class.
- RELATIONSHIP: 🔗 complements "closing-the-loop". That video teaches you to give the agent an automated feedback loop at all (so do not re-teach the loop itself). This is the next step: the content of the signal you put IN the loop determines the fix quality, and full test source beats the terminal error string.
- PROOF TO REUSE: Vibhav admitting "the naive person in me would have just put the error message"; Greg's discovery that the optimizer "doesn't know the source code of the test that failed, so it doesn't know what it's trying to get the prompt to actually do"; the five-asserts whack-a-mole example (pass the second, break the fourth); "because the model can reason about source code, putting the whole source code in there is way more optimal."

---

## 📚 Full wisdom (reference)

**SUMMARY**
On the AI That Works stream, Vibhav, Dex, and Greg build a working GEPA-style prompt optimizer inside BAML, live, in just three days from scratch.

**IDEAS**
- A prompt optimizer beats humans only on prompts you never read: optimize code you never love.
- Software quality equals the time and love you invest; unloved code cannot improve no matter what.
- Optimizers work only with automated feedback, the same deterministic back-pressure that coding agents need to progress.
- GEPA generates a candidate prompt, evaluates it against tests, reflects on failures, then combines Pareto-frontier winners.
- Feeding the optimizer full failing-test source, not the assertion error, dramatically improves the fixes it generates.
- Only the failing assertion message hides later asserts, so the model fixes one and breaks another.
- The optimizer sees only minimum reachable code: classes and enums traversed from your function's signature recursively.
- Constrained editing tools, like Claude Code's notebook_edit, edit specific file regions instead of raw text blobs.
- The optimizer itself is just prompts and types, so you can read, edit, and control it.
- You can swap models per stage, reflection, candidate generation, merging, trading power against price where needed.
- Metric weights convey relative importance to the model: orders of magnitude matter, exact decimals do not.
- BAML shoehorned evals into existing tests: named soft checks power ancillary metrics without new language features.
- Always read your prompts after optimizing, because metrics alone cannot reveal overfitting on unrepresentative sample points.
- GEPA needs few sample points to converge, which makes accidental overfitting on unrepresentative examples dangerously easy.
- Human intuition on whether output looks good is far cheaper than designing fifty metrics up front.
- Input and output types stay hard contracts during optimization because they generate client code developers consume.
- Convergence stops the algorithm once your metric maxes out, since there is nowhere better to go.
- Future optimizers should tune entire workflows, not just single prompts: control flow plus multiple LLM functions.

**INSIGHTS**
- Automated optimization pays off precisely where you have no attention to spare, inverting the effort-quality relationship.
- The bottleneck in any fix loop is signal richness, not the model's raw reasoning capability alone.
- Exposing meta-tooling as editable prompts turns the optimizer into a domain-tunable system, not a black box.
- Structured output is what makes visibility possible; markdown-only pipelines cannot render a navigable, inspectable optimization interface.
- Building the tool forces you to externalize implicit knowledge you never articulate while prompting by hand.
- Optimizing one shared prompt for a single caller risks overspecializing it against every other consumer downstream.
- Convention over configuration beats faithfully reimplementing a research algorithm when your goal is shipping usable optimization.
- The right blend keeps human intuition in the loop while automation explores the prompt state space.
- Constraining the editable region, whether a notebook cell or a prompt block, prevents collateral damage elsewhere.

**QUOTES**
- Vibhav: "is a prompt optimizer going to do a better job than a human that really understands a problem? Probably not."
- Vibhav: "software quality is basically based on amount of time and love you give it."
- Dex: "the model can't ... solve its way out of a puzzle if it has no deterministic ... back pressure or feedback system to tell it if what it's doing is working."
- Dex: "in 2025 it was everyone should build a coding agent from scratch. And in 2026, everyone should build a prompt optimizer from scratch."
- Vibhav: "it's so hard to remember your own implicit knowledge when you're prompting and to remember the fact that you have to be explicit about all those things."
- Vibhav: "if you don't look at the prompt you can't possibly know if it overfit by accident or not. the metrics are not enough."
- Dex: "your human intuition is incredibly powerful. And if you can just look at something and know if it's good or not, that's way cheaper than designing 50 metrics."
- Vibhav: "the type is part of the prompt because it's the instructions that you're asking it to do the output in."
- Greg: "it was three days."
- Vibhav: "Most of these systems that you're building are not that complex. Anyone can go build them."
- Vibhav: "why not make the plumbing be structured rather than ... markdown flowing everywhere."

**HABITS**
- Reserve human prompt-writing effort for code you care about; delegate throwaway prompts to an automated optimizer.
- Always inspect the optimized prompt before accepting it, scanning in seconds for obvious signs of overfitting.
- Limit optimization trials, using a flag like three, to keep demos and iteration cycles fast enough.
- Run optimization in dry-run mode first to inspect and customize the generated GEPA prompts before committing.
- Do a first eval pass with human judgment before investing in fifty carefully engineered numeric metrics.
- Keep old crummy prompts around by quitting without saving, preserving them for future demonstrations and comparisons.
- Pass API credentials through environment variables rather than hardcoding them when running optimization against a model.
- Name your soft assertions so they double as tunable metric weights during the optimization run itself.

**FACTS**
- DSPy has focused on prompt optimization for years and ships its own GEPA implementation in Python.
- BAML's GEPA implementation is roughly fifty percent faithful to the paper and fifty percent BAML-specific departure.
- Greg built the entire BAML GEPA implementation, with all its tooling, in three days of work.
- BAML raw strings support up to seven nested hash levels for escaping quotes inside prompt text.
- GEPA out of the box provides one metric: the fraction of your test cases that pass.
- BAML's reflection, candidate, and merge prompts currently all share one model, Claude Opus 4.5, by default.
- The optimizer manipulates the BAML AST directly, splicing new prompt text into the exact relevant region.
- GEPA generates candidates one at a time, greedily hill-climbing or combining two Pareto-frontier prompts each step.

**REFERENCES**
- GEPA (the DSPy prompt optimizer) and its arXiv paper diagram.
- DSPy (Python framework, the standard-bearer for prompt optimization).
- BAML by BoundaryML (structured-output language; the "AI pipelines" programming language).
- Human Layer (Dex's company; getting coding agents to solve hard problems in complex codebases).
- Claude Code tools notebook_edit and notebook_read (constrained editing of Jupyter files).
- Zed editor (used by Greg for the demo).
- Claude Opus 4.5 (the default reflection/candidate/merge model in BAML's implementation).
- SWE-bench (raised as a target for plugging in a BAML coding agent).
- Prior AI That Works episodes: the evals episode, the "coding agent built in BAML" episode.
- CodeLayer / context engineering (Dex's upcoming backstory topic).

**ONE-SENTENCE TAKEAWAY**
Prompt optimizers are now a three-day build; point them at code you will never love.

**RECOMMENDATIONS**
- Build your own GEPA-style prompt optimizer from scratch to understand its mechanics before adopting any library.
- Point an optimizer at unloved throwaway prompts while hand-crafting the prompts that genuinely matter to you.
- Feed fixing agents the full source of failing tests, not just the terminal assertion error string.
- Read the GEPA arXiv paper's diagram before trying to reproduce the algorithm from a podcast whiteboard.
- Expose your optimizer's internal prompts as editable files so you can inject domain-specific knowledge when needed.
- Give the optimizer only the minimum reachable code by traversing types from your function signature recursively.
- Always eyeball your optimized prompts to catch overfitting, since sparse GEPA samples make accidental overfitting easy.
- Name soft checks in your test suite so they become weighted, tunable metrics during optimization runs.
