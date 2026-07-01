---
title: "Why Your AI Coding Agent Keeps Writing Bad Code (It's Not the Prompt)"
videoId: 0LPBw3NO3Jc
url: https://www.youtube.com/watch?v=0LPBw3NO3Jc
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Split the design phase into product, technical, and program design, so architectural decisions land upstream where you have the most leverage.** Bad agent code is not a prompt failure; it is a decision the model was left to make too late, at implementation, because the design step collapsed into one blob and never settled the program-level choices.
VERDICT: 🔗 next-step video available (complements "the-shifting-bottleneck").

**2. Standardize a "what deviated from the plan" section in every PR, then review only that delta instead of all the code.** The leverage is not the plan itself, it is the guaranteed habit of surfacing divergences, which is where bugs actually hide.
VERDICT: ❌ net-new video available.

**3. Drop the universal CLAUDE.md for conditional architecture pointer files and context shards the model loads only when a task needs them.** An always-on doc goes stale and skews more features wrong than right; conditional context pays its token cost only when relevant.
VERDICT: 🔗 next-step video available (complements "delete-your-readme").

---

## Summary

Dex (HumanLayer) and Vaibhav (BoundaryML) split agentic design into product, technical, and program phases, moving architectural decisions upstream where leverage is highest, preventing bad code.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Split design into product, technical, and program design

The claim: bad agent code is rarely a prompt failure. It is an architectural decision made too late, at implementation, instead of settled upstream in an explicit, staged design phase. Most people reach for a better prompt when the output is wrong. Dex argues the real defect is that the design step silently collapses into one blob that "defaults to leaning more heavily one way or the other," so program-level questions (which state library, which pattern) never get decided until the model guesses them mid-PR. The fix is a three-way split: product design (UX, CLIs, "what the user's code looks like," how success is measured), technical design (system architecture, contracts between systems), and program design (test seams, function signatures, file layout). The mechanism is a leverage gradient: "at each stage you have less clarity and more leverage." Because settling "provider or TanStack collection?" before implementation heads off the model's defaults (React context, useEffect) that "make the codebase really hard to reason about," the PR lands 95 to 99% correct and review gets cheap. It generalizes to a PM aligning a spec before engineering starts. It goes wrong when you over-plan cheap exploratory work: Dex deliberately skips success metrics on a pure UI change, because knowing which phase a task actually needs is itself the skill.

### Spine 2 — Review only what deviated from the plan

The claim: standardize a PR section that reports what diverged from the plan, and review only that delta rather than every line of the diff. The non-obvious part is where the leverage sits. It is tempting to credit the plan, or to lean on AI code review, but Vaibhav's insight is that "the thing that's fascinating to me is actually not the plan at all. It's the fact that you chose to add that step" of self-reporting deviations. The mechanism runs in two steps: when a PR self-reports "here is what differs from the plan," your attention goes straight to the surprises, and a surprise is exactly one of three things, a bug, a decision you never made, or a consequence you can live with. Because the format is guaranteed every time, "by standardizing that, my verification loop got faster." You stop reading all the code and read only the divergences, which is "how I found bugs." It generalizes to a diff-against-spec gate in CI. It fails when the plan is not specific enough, because then "the PR is just going to be whatever the model chose," and the deviation list becomes meaningless. So it depends on spine 1 having settled a real plan first.

### Spine 3 — Conditional architecture files and context shards over a universal CLAUDE.md

The claim: a universal CLAUDE.md guarantees failure; replace it with pointed architecture files and small context shards the model loads only when a task needs them. The common belief is that a rich CLAUDE.md steers the model well. Vaibhav "stopped having Claude MD in our repo" because "it always becomes out of date" and "it skews the program more incorrectly than correctly most of the time." The mechanism: an always-loaded doc pays a token cost on every task and applies stale or irrelevant rules to tasks they do not fit. Instead, an arch-header.md answers only "what lives here or what doesn't," with a memorable rule ("always prefer to add a feature upstream whenever possible," "almost definitely don't add a new layer"), and the model reads it only during language-design work, never during a bug fix. Dex's "context shards" generalize this: sixty to seventy paragraph-sized snippets, of which the model selects five to ten per implementation phase during research. Both replace one big always-on prompt with conditional, task-scoped context. It generalizes to skills (conditionally invoked instructions) versus a monolithic system prompt, and to .env cascading per directory. It fails without a research step that reliably selects the right shards, or discipline to keep them current.

---

## 🎬 Proposed ACS videos

### 1. Why Your Agent Writes Bad Code (And the Design Split That Fixes It)

- HOOK: Your agent's bad code is not a prompt problem. It is a decision you let it make too late.
- THE PROMISE: For engineers already using plan-then-implement workflows; after this you split design into three phases so architectural choices land before the model writes a line.
- THE SHAPE:
  1. Show the failure: design looked good, then implementation introduced a React provider you explicitly avoid.
  2. Introduce the leverage gradient: less clarity, more leverage, the further upstream you decide.
  3. Product design phase: UX, CLIs, "what the user's code looks like," how success is measured.
  4. Technical then program design: architecture and contracts, then test seams, signatures, file layout.
  5. Payoff demo: program design asks "provider or TanStack collection?" before any code exists.
- SPINE: 1
- SLOT: context-engineering (or start-here, adjacent to "the-shifting-bottleneck")
- RELATIONSHIP: 🔗 complements "the-shifting-bottleneck" by being its next step. That video teaches that the constraint moved upstream to design and requirements (the drained-middle-tank idea); it does not teach how to structure that upstream work. This video films the three-phase split and the program-design catch, so Ray does not re-teach the bottleneck theory, he operationalizes it.
- PROOF TO REUSE: "at each stage you have less clarity and more leverage"; the provider-versus-Zustand catch ("why the [__] are you introducing a React provider?"); CRISPI where "the D is silent."

### 2. Review Only What Changed From the Plan

- HOOK: Stop reading every line of the PR. Read only what deviated from the plan.
- THE PROMISE: For anyone reviewing agent-written PRs; after this you add a standard deviation section so your review reads surprises, not the whole diff.
- THE SHAPE:
  1. The problem: too much code, too many PRs; AI review only gets you so far.
  2. The move: make the PR self-report what diverged from its plan, as a fixed section.
  3. Standardize it so it appears on every pull request, every time.
  4. Review flow: each surprise is a bug, an unmade decision, or an acceptable consequence.
  5. Payoff: throw it out and replan, iterate to fix, or accept; the loop gets faster.
- SPINE: 2
- SLOT: techniques (Multi-Agent Orchestration, a review chapter) or correction
- RELATIONSHIP: ❌ net-new. Adjacent to the filmed "closing-the-loop," but distinct: this is specifically a plan-deviation artifact you review in place of the full diff, not a general verification loop. Catalog has no video on self-reported plan divergence as the review surface.
- PROOF TO REUSE: "I want to know what deviated from the plan and that's just useful for me cuz that's how I found bugs"; "by standardizing that... my verification loop got faster"; the restart-or-iterate-or-accept decision.

### 3. Delete Your CLAUDE.md, Point to Architecture Files Instead

- HOOK: A universal CLAUDE.md guarantees failure. Give the model context it loads only when it needs it.
- THE PROMISE: For teams whose CLAUDE.md keeps going stale; after this you replace it with conditional architecture files and context shards.
- THE SHAPE:
  1. Why the universal CLAUDE.md fails: stale, always-on, skews more features wrong than right.
  2. The arch-header file: answers "what lives here or what doesn't," loaded only when relevant.
  3. Rules that help model and human alike: "add features upstream," "never add a new layer."
  4. Context shards: sixty to seventy snippets, the model selects five to ten per phase.
  5. When to load which: a bug fix loads nothing, a language change loads the whole doc.
- SPINE: 3
- SLOT: context-engineering
- RELATIONSHIP: 🔗 complements the filmed "delete-your-readme" by being its next step. That video argues stale docs should go; this one gives the positive replacement, conditional model-selected architecture files and context shards, so the model gets accurate context without paying for a stale monolith on every task.
- PROOF TO REUSE: "having more stuff in the Cloud MD just guarantees failure"; "always prefer to add a feature upstream whenever possible... almost definitely don't add a new layer"; the .env cascading analogy; context shards borrowed from a grocery-delivery engineer.

---

## 📚 Full wisdom (reference)

**SUMMARY** — Dex (HumanLayer) and Vaibhav (BoundaryML) demo splitting agentic design into product, technical, and program phases, moving decisions upstream where leverage is highest to prevent bad code.

**IDEAS**
- HumanLayer split their design step into product design and technical design, each needing a different mindset.
- At each earlier stage you have less clarity but more leverage, so decisions there matter most.
- Program design settles test seams, function signatures, and file layout before any implementation code gets written.
- The model defaults to React providers and useEffect, patterns HumanLayer avoids, unless you head it off.
- They dropped the plan step entirely and let a smarter implementation model handle late-stage flexibility instead.
- Reviewing only what deviated from the plan is how Vaibhav actually finds bugs in pull requests.
- Standardizing the deviation report made the verification loop faster than reading every single line of code.
- Vaibhav stopped keeping a CLAUDE.md because it always goes out of date and skews the output.
- An architecture header file answers what lives here and what should never live here, nothing else.
- The core rule: always add a feature upstream in the AST and never add a layer.
- During research the model selects which five-to-ten context shards each implementation phase actually needs to load.
- HTML is information-dense and bad raw, but the rendered artifact is one of the richest formats.
- Markdown stays better for model-facing research docs because it is far more token efficient than HTML.
- Prompting the model with a queue of creativity pushes it out of its default safe output.
- Feed the model an SVG or PNG of HTML rather than raw HTML for better comprehension.

**INSIGHTS**
- Bad agent code is rarely a prompt failure; it is a decision made far too late.
- Moving decisions upstream costs fewer tokens to fix than catching them deep in a finished PR.
- Do breadth early where clarity is low; do verification late where the surface is very large.
- The real leverage was the standardized deviation-review habit itself, not the plan document that fed it.
- A universal CLAUDE.md skews more features wrong than right because no single doc fits every task.
- Conditional context that loads only when relevant beats an always-on prompt paying a token cost everywhere.
- Dev-tools builders skip product empathy because they are their own user, which hides the real problems.
- Choosing HTML versus markdown is a deliberate tradeoff of richness against iteration speed, not a default.
- Product design asks what the user's code looks like; you are designing a program's whole surface.

**QUOTES**
- Dex: "at each stage you have less clarity and more leverage."
- Dex: "how do we make it so that when the PR lands, it's already 99% correct or 95% correct."
- Dex: "how do you remove the cognitive burden of reviewing stuff later and how do you move it earlier in the pipeline?"
- Dex: "The earlier you are, do more breadth. The later you are, do more verification."
- Vaibhav: "by standardizing that, that makes it really easy for me to guarantee that I expect that every time and now the quality of my... verification loop got faster."
- Vaibhav: "I find that having more stuff in the Cloud MD just guarantees failure."
- Vaibhav: "Claude MD will always become out of date... stuff just gets out of date, man. It's not worth it."
- Dex: "it always prefer to add a feature upstream whenever possible."
- Vaibhav: "the raw file is kind of bad, but the rendered artifact is amazing."
- Dex: "the D is silent."
- Vaibhav: "90% of the tasks are so freaking boring. I just want AI to do it for me."

**HABITS**
- Vaibhav's team assigns someone to spend two or three days designing, producing a spec not commits.
- Dex spends about five minutes whiteboarding, then goes hands-on with the actual coding agent almost immediately.
- He reviews the deviated-from-plan section of every pull request rather than reading all of the code.
- When surprised by a deviation, he either restarts with a new plan or iterates to correct.
- Vaibhav points the model at a small arch-header file only when doing language-design work, never bug-fixes.
- Dex asks the agent during building to define how success will be measured for new features.
- He often converts HTML to SVG or PNG before feeding it back into the model again.
- Vaibhav opens two design artifacts side by side, finding that comparison highly valuable while actively iterating.

**FACTS**
- HumanLayer shipped a new PRD-and-TDD workflow overhaul on a Sunday night with a program-design section added.
- Their biggest design doc had over one hundred twelve comments and seven sub-pages from the team.
- Dex made many design decisions at only seventy-thousand tokens, well inside the two-hundred-thousand-token context window comfortably.
- Cursor was acquired, celebrated at its conference at Fort Mason in San Francisco earlier this week.
- Vaibhav's team builds a programming language designed to be agent-first and human-second in its overall ergonomics.
- MDX requires a React runtime with an MDX renderer, so it breaks across editors and GitHub.
- HumanLayer dropped the plan step and now uses a smarter model during the implementation phase instead.
- CLAUDE.md automatically loads a directory's file when Claude touches files inside that directory, similar to dotenv.

**REFERENCES** — AI That Works podcast; HumanLayer; BoundaryML / BAML; the Human Layer task-page redesign ticket; Cursor (conference at Fort Mason, acquisition, Michael Truel, Cursor rules); Claude and Claude Code; CLAUDE.md and Claude rules; Vim, Vim Tutor, tmux configs; MDX; Mermaid; TanStack DB; Zustand; React (context, useEffect, providers); the SQL / JSON-AST intermediate-representation trick; Figma; S3 plus iframe rendering; Superwhisper; the RPI / CRISPI framework; "context shards" (from an engineer at a large grocery-delivery company); the earlier feature-flags episode.

**ONE-SENTENCE TAKEAWAY** — Split design into product, technical, and program phases to move decisions upstream where leverage lives.

**RECOMMENDATIONS**
- Break your design step into explicit product design and technical design before touching any implementation code.
- Add a program-design phase that settles state-management and pattern choices before the model writes any code.
- Make every PR report what deviated from its plan, then review only that delta section first.
- Replace a stale universal CLAUDE.md with a pointed architecture file the model reads only when relevant.
- Write architecture rules as what lives where, like always add features upstream, never add new layers.
- Prompt the model with an explicit creativity cue when you want non-default design exploration back quickly.
- Use HTML for human-facing artifacts, but markdown for token-efficient model-facing research docs, choosing between each deliberately.
- Ask the agent to define measurable success during building so it can propose future improvements itself.
